from nicegui import ui
import networkx as nx
from PIL import Image, ImageDraw
import io, base64
import math

# ============================================================================
# CUSTOM CSS STYLES
# ============================================================================

CAMPUS_CSS = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
    
    * {
        font-family: 'Inter', sans-serif !important;
    }
    
    body {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%) !important;
        min-height: 100vh;
    }
    
    .glass-header {
        background: rgba(255, 255, 255, 0.95) !important;
        backdrop-filter: blur(10px) !important;
        border-bottom: 1px solid rgba(255, 255, 255, 0.2) !important;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1) !important;
    }
    
    .glass-card {
        background: rgba(255, 255, 255, 0.95) !important;
        backdrop-filter: blur(10px) !important;
        border: 1px solid rgba(255, 255, 255, 0.3) !important;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.15) !important;
        border-radius: 16px !important;
    }
    
    .btn-back {
        background: linear-gradient(135deg, #4a5568 0%, #2d3748 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 10px !important;
        font-weight: 600 !important;
        text-transform: none !important;
        transition: all 0.3s ease !important;
    }
    
    .btn-back:hover {
        transform: translateX(-3px) !important;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3) !important;
    }
    
    .btn-voice {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 12px !important;
        font-weight: 700 !important;
        text-transform: none !important;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4) !important;
        transition: all 0.3s ease !important;
    }
    
    .btn-voice:hover {
        transform: scale(1.02) !important;
        box-shadow: 0 6px 25px rgba(102, 126, 234, 0.5) !important;
    }
    
    .btn-beta {
        background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 12px !important;
        font-weight: 700 !important;
        text-transform: none !important;
        box-shadow: 0 4px 15px rgba(17, 153, 142, 0.4) !important;
        transition: all 0.3s ease !important;
    }
    
    .btn-beta:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 25px rgba(17, 153, 142, 0.5) !important;
    }
    
    .legend-card {
        background: rgba(255, 255, 255, 0.9) !important;
        border-radius: 12px !important;
        border: 1px solid #e2e8f0 !important;
    }
    
    .map-container {
        background: rgba(255, 255, 255, 0.95) !important;
        border-radius: 16px !important;
        box-shadow: 0 8px 40px rgba(0, 0, 0, 0.2) !important;
        overflow: hidden !important;
    }
    
    .main-title {
        background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    .gps-badge {
        background: linear-gradient(135deg, #ffecd2 0%, #fcb69f 100%) !important;
        border: 2px solid #f5af19 !important;
        border-radius: 20px !important;
        box-shadow: 0 4px 15px rgba(245, 175, 25, 0.3) !important;
    }
    
    .zoom-btn {
        background: linear-gradient(135deg, #ff4757 0%, #ff6b81 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 8px !important;
        box-shadow: 0 2px 8px rgba(255, 71, 87, 0.4) !important;
        min-width: 36px !important;
        min-height: 36px !important;
    }
    
    .zoom-btn:hover {
        transform: scale(1.1) !important;
        box-shadow: 0 4px 15px rgba(255, 71, 87, 0.5) !important;
    }
    
    @keyframes pulse-glow {
        0%, 100% { box-shadow: 0 0 5px rgba(102, 126, 234, 0.5); }
        50% { box-shadow: 0 0 20px rgba(102, 126, 234, 0.8); }
    }
    
    .pulse-glow {
        animation: pulse-glow 2s ease-in-out infinite;
    }
</style>
"""

# ============================================================================
# DATA DEFINITIONS
# ============================================================================

# Visible locations for user selection
VISIBLE_LOCATIONS = {
    "PARKING LOT A": (190, 840), "GATE": (500, 900), "PARKING LOT B": (170, 600),
    "THE THINKER": (470, 760), "ALPHA BUILDING": (400, 500), "BETA BUILDING": (720, 700),
    "CANTEEN": (580, 390), "SOCCER": (880, 440), "BASKETBALL": (840, 330),
    "VOLLEYBALL": (850, 370), "VOVINAM": (900, 300),
    "HIGHSCHOOL DORMITARY": (1300, 300), "UNIVERSITY DORMITARY": (1370, 480),
}

# Virtual nodes for path connections (hidden from UI)
VIRTUAL_NODES = {
    "1": (300, 980), "2": (170, 970), "3": (80, 960), "4": (100, 640),
    "5": (590, 840), "BETA": (570, 740), "6": (280, 700), "7": (170, 760),
    "ALPHA": (420, 640), "8": (530, 600), "9": (420, 900), "10": (350, 700),
    "11": (380, 800), "12": (700, 540), "13": (730, 500), "14": (910, 380),
    "15": (930, 340), "16": (480, 420), "18": (720, 435), "19": (1060, 320),
    "20": (1120, 350), "21": (1065, 370), "22": (1240, 420), "23": (1300, 410),
}

LOCATIONS = {**VISIBLE_LOCATIONS, **VIRTUAL_NODES}

# GPS coordinates
LOCATIONS_GPS = {
    "GATE": (13.804553052179601, 109.21950215399711),
    "BETA BUILDING": (13.804037728087135, 109.21905987562394),
    "ALPHA BUILDING": (13.803719317148747, 109.21978179205664),
    "CANTEEN": (13.80346943932719, 109.21935393966768),
    "SOCCER": (13.80358132697852, 109.21871383179098),
    "UNIVERSITY DORMITARY": (13.803615255456071, 109.21766757243233),
    "PARKING LOT A": (13.804426590467092, 109.22022472831937),
    "PARKING LOT B": (13.803952661753089, 109.22022791802131),
    "THE THINKER": (13.804240736184244, 109.21961230554994),
    "BASKETBALL": (13.803398194907908, 109.21879893155109),
    "VOLLEYBALL": (13.803320755299886, 109.21882444916649),
    "VOVINAM": (13.80322163256409, 109.21863625675296),
    "HIGHSCHOOL DORMITARY": (13.803221632561929, 109.21778460632828),
}

# Voice aliases
VOICE_ALIAS = {
    "CANTEEN": ["CANTEEN", "CAN TEEN", "CAN TIN", "CANTIN", "CANTEAN"],
    "ALPHA BUILDING": ["ALPHA", "ALPHA BUILDING"],
    "BETA BUILDING": ["BETA", "BETA BUILDING"],
    "GATE": ["GATE", "MAIN GATE", "ENTRANCE"],
    "PARKING LOT A": ["PARKING LOT A", "PARKING A", "PARK A"],
    "PARKING LOT B": ["PARKING LOT B", "PARKING B", "PARK B"],
    "THE THINKER": ["THE THINKER", "THINKER", "STATUE"],
    "SOCCER": ["SOCCER FIELD", "SOCCER", "FOOTBALL FIELD", "FOOTBALL"],
    "BASKETBALL": ["BASKETBALL COURT", "BASKETBALL"],
    "VOLLEYBALL": ["VOLLEYBALL COURT", "VOLLEYBALL"],
}

# Graph edges
EDGES = [
    ('BETA', 'BETA BUILDING'), ('ALPHA BUILDING', 'ALPHA'),
    ("GATE", "1"), ("1", "2"), ("2", "3"), ('2', 'PARKING LOT A'), ('3', '4'),
    ("PARKING LOT B", "4"), ('GATE', 'THE THINKER'), ('GATE', '5'), ('5', 'BETA'),
    ('BETA', 'THE THINKER'), ('6', 'ALPHA'), ('6', '7'), ('6', 'PARKING LOT B'),
    ('7', 'PARKING LOT A'), ('BETA', '8'), ('8', '16'), ('8', 'ALPHA'), ('9', 'GATE'),
    ('9', '10'), ('10', '6'), ('10', 'ALPHA'), ('10', '11'), ('11', 'THE THINKER'),
    ('8', '12'), ('BETA BUILDING', '12'), ('12', '13'), ('13', 'SOCCER'),
    ('SOCCER', '14'), ('14', '15'), ('VOLLEYBALL', '15'), ('BASKETBALL', '15'),
    ('VOVINAM', '15'), ("BASKETBALL", "VOLLEYBALL"), ("VOLLEYBALL", "VOVINAM"),
    ("BASKETBALL", "VOVINAM"), ('ALPHA BUILDING', '16'), ('16', 'CANTEEN'),
    ('CANTEEN', '18'), ('18', '13'), ('18', '14'), ('14', '19'), ('19', '20'),
    ('20', 'HIGHSCHOOL DORMITARY'), ('SOCCER', '21'), ('21', '22'), ('22', '23'),
    ('19', '21'), ('23', 'UNIVERSITY DORMITARY'),
    ("HIGHSCHOOL DORMITARY", "UNIVERSITY DORMITARY")
]

IMAGE_PATH = "khuonvientruong.jpg"


# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def build_graph():
    """Build navigation graph."""
    G = nx.Graph()
    for a, b in EDGES:
        xa, ya = LOCATIONS[a]
        xb, yb = LOCATIONS[b]
        G.add_edge(a, b, weight=((xa - xb) ** 2 + (ya - yb) ** 2) ** 0.5)
    return G


def haversine(lat1, lon1, lat2, lon2):
    """Calculate Haversine distance between two GPS points."""
    R = 6371000
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)
    a = math.sin(dphi / 2) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(dlambda / 2) ** 2
    return 2 * R * math.atan2(math.sqrt(a), math.sqrt(1 - a))


def normalize_text(text: str):
    """Normalize text for voice matching."""
    return text.upper().replace(" ", "").replace("-", "")


def draw_dashed_line(draw, p1, p2, dash_len=20, gap_len=12, fill="red", width=8):
    """Draw dashed line between two points."""
    x1, y1 = p1
    x2, y2 = p2
    dx, dy = x2 - x1, y2 - y1
    distance = math.hypot(dx, dy)
    
    if distance == 0:
        return
    
    vx, vy = dx / distance, dy / distance
    pos = 0
    
    while pos < distance:
        start, end = pos, min(pos + dash_len, distance)
        sx, sy = x1 + vx * start, y1 + vy * start
        ex, ey = x1 + vx * end, y1 + vy * end
        draw.line([(sx, sy), (ex, ey)], fill=fill, width=width)
        pos += dash_len + gap_len


# ============================================================================
# MAIN PAGE FUNCTION
# ============================================================================

def create_page():
    """Create Campus Map page."""
    
    # Inject CSS
    ui.add_head_html(CAMPUS_CSS)
    
    # Build graph
    G = build_graph()
    
    # State variables
    user_lat, user_lon = None, None
    zoom_level = 1.4
    
    # ========== HELPER FUNCTIONS ==========
    
    def snap_gps_to_node(lat, lon):
        """Find nearest node from GPS coordinates."""
        min_dist, nearest = float('inf'), None
        for name, (nlat, nlon) in LOCATIONS_GPS.items():
            d = haversine(lat, lon, nlat, nlon)
            if d < min_dist:
                min_dist, nearest = d, name
        return nearest
    
    def find_shortest_path(start, end):
        """Find shortest path between two locations."""
        try:
            path = nx.shortest_path(G, source=start, target=end, weight="weight")
            dist = nx.shortest_path_length(G, source=start, target=end, weight="weight")
            return path, dist
        except nx.NetworkXNoPath:
            return [], float("inf")
    
    def draw_base_map():
        """Draw base map without path."""
        try:
            img = Image.open(IMAGE_PATH).convert("RGB")
            buf = io.BytesIO()
            img.save(buf, format="PNG")
            return f"data:image/png;base64,{base64.b64encode(buf.getvalue()).decode('utf-8')}"
        except FileNotFoundError:
            return ""
    
    def draw_path(path, user_pixel=None):
        """Draw path on map."""
        try:
            img = Image.open(IMAGE_PATH).convert("RGB")
            draw = ImageDraw.Draw(img)
            
            if path and len(path) == 1:
                # Single point
                p = LOCATIONS[path[0]]
                r = 15
                draw.ellipse((p[0]-r, p[1]-r, p[0]+r, p[1]+r), fill="#FF0000", outline="white", width=3)
                draw.ellipse((p[0]-r*2, p[1]-r*2, p[0]+r*2, p[1]+r*2), outline="#FF0000", width=2)
            elif path and len(path) > 1:
                # Draw path lines
                for i in range(len(path) - 1):
                    p1, p2 = LOCATIONS[path[i]], LOCATIONS[path[i+1]]
                    draw_dashed_line(draw, p1, p2, dash_len=22, gap_len=12, fill="#FF4757", width=8)
                
                # Draw start point (Blue)
                start = LOCATIONS[path[0]]
                draw.ellipse((start[0]-12, start[1]-12, start[0]+12, start[1]+12), 
                            fill="#007bff", outline="white", width=2)
                
                # Draw end point (Green)
                end = LOCATIONS[path[-1]]
                draw.ellipse((end[0]-12, end[1]-12, end[0]+12, end[1]+12), 
                            fill="#28a745", outline="white", width=2)
                
                # Draw user position (Red)
                if user_pixel:
                    draw.ellipse((user_pixel[0]-10, user_pixel[1]-10, 
                                user_pixel[0]+10, user_pixel[1]+10), fill="red")
            
            buf = io.BytesIO()
            img.save(buf, format="PNG")
            return f"data:image/png;base64,{base64.b64encode(buf.getvalue()).decode('utf-8')}"
        except FileNotFoundError:
            return ""
    
    def update_path():
        """Update path display."""
        nonlocal user_lat, user_lon
        if user_lat is None or user_lon is None:
            return
        
        end = end_sel.value
        start = snap_gps_to_node(user_lat, user_lon)
        
        if not start or not end:
            return
        
        if start == end:
            image_view.source = draw_path([start])
            distance_label.text = ""
            return
        
        path, dist = find_shortest_path(start, end)
        image_view.source = draw_path(path)
        distance_label.text = f"📏 {dist:.0f} px"
    
    def adjust_zoom(delta):
        nonlocal zoom_level
        zoom_level = max(1.0, min(3.0, zoom_level + delta))

        image_wrapper.style(
            f'''
            transform: scale({zoom_level});
            transform-origin: top left;
            transition: transform 0.2s ease;
            '''
        )

        lbl_zoom.text = f"{int(zoom_level * 100)}%"
    
    def start_voice():
        """Start voice recognition."""
        ui.run_javascript('''
            const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
            if (!SpeechRecognition) {
                emitEvent('voice-error', {message: 'Browser không hỗ trợ'});
                return;
            }
            const recog = new SpeechRecognition();
            recog.lang = 'en-US';
            recog.continuous = false;
            recog.interimResults = false;
            recog.onresult = (event) => {
                const text = event.results[0][0].transcript.toUpperCase();
                emitEvent('voice-result', { text });
            };
            recog.onerror = (e) => emitEvent('voice-error', {message: e.error});
            recog.start();
        ''')
    
    def start_gps_watch():
        """Start GPS tracking."""
        ui.run_javascript('''
            navigator.geolocation.watchPosition(
                (pos) => emitEvent('gps-update', {
                    lat: pos.coords.latitude.toString(),
                    lon: pos.coords.longitude.toString()
                }),
                (err) => emitEvent('gps-error', {message: err.message}),
                { enableHighAccuracy: true }
            );
        ''')
    
    # ========== EVENT HANDLERS ==========
    
    def on_gps_update(e):
        nonlocal user_lat, user_lon
        user_lat, user_lon = float(e.args['lat']), float(e.args['lon'])
        gps_status.text = f"📍 {user_lat:.4f}, {user_lon:.4f}"
        update_path()
    
    def on_voice_result(e):
        spoken_raw = e.args['text'].upper().strip()
        spoken_label.text = f"🎙 {spoken_raw}"
        spoken_norm = normalize_text(spoken_raw)
        
        # Match location
        for loc in VISIBLE_LOCATIONS.keys():
            if normalize_text(loc) in spoken_norm:
                end_sel.value = loc
                update_path()
                ui.notify(f"🎯 {loc}", type='positive')
                return
        
        # Fallback to aliases
        for canonical, aliases in VOICE_ALIAS.items():
            for a in aliases:
                if normalize_text(a) in spoken_norm:
                    end_sel.value = canonical
                    update_path()
                    ui.notify(f"🎯 {canonical}", type='positive')
                    return
        
        ui.notify(f"❌ Không nhận ra: {spoken_raw}", type='warning')
    
    # Register events
    ui.on('gps-update', on_gps_update)
    ui.on('gps-error', lambda e: setattr(gps_status, 'text', f"❌ GPS lỗi"))
    ui.on('voice-result', on_voice_result)
    ui.on('voice-error', lambda e: ui.notify(f"🎤 Lỗi: {e.args['message']}", type='negative'))
    
    # ========== UI LAYOUT ==========
    
    with ui.column().classes('w-full min-h-screen items-center p-2 gap-2'):
        
        # GPS Status Badge (Fixed)
        gps_status = ui.label("📡 Chờ GPS...").classes(
            'fixed top-2 right-2 z-50 gps-badge px-3 py-1 text-xs font-bold text-orange-800'
        )
        
        # Header
        with ui.row().classes('w-full items-center gap-2 glass-header p-2 rounded-xl'):
            ui.button("⬅ Menu", on_click=lambda: ui.navigate.to('/')).classes(
                'btn-back text-xs py-1 px-2'
            )
            ui.label("🌍 CAMPUS").classes('text-base font-bold main-title')
        
        # Control Panel
        with ui.card().classes('w-full glass-card p-3'):
            with ui.column().classes('w-full gap-2'):
                # Destination selector
                end_sel = ui.select(
                    options=list(VISIBLE_LOCATIONS.keys()),
                    value="BETA BUILDING",
                    label="🏁 Điểm đến"
                ).classes('w-full').props(
                    'outlined dense options-dense hide-dropdown-icon'
                ).style('font-size: 12px;')
                
                # Voice button
                with ui.row().classes('w-full gap-2'):
                    ui.button("🎤 Nói điểm đến", on_click=start_voice).classes(
                        'flex-1 btn-voice text-xs py-2'
                    )
                    spoken_label = ui.label("🎙 ...").classes(
                        'flex-1 text-xs font-bold text-purple-700 self-center text-center'
                    )
                
                # Beta building button
                ui.button(
                    "🏢 VÀO TÒA BETA",
                    on_click=lambda: ui.navigate.to('/beta')
                ).classes('w-full btn-beta text-xs py-2')
        
        # Legend
        with ui.card().classes('legend-card p-2 w-full'):
            ui.label("📝 Chú thích").classes('font-bold text-gray-700 text-xs mb-1')
            with ui.row().classes('gap-3 flex-wrap'):
                with ui.row().classes('items-center gap-1'):
                    ui.element('div').classes('w-3 h-3 rounded-full bg-blue-600')
                    ui.label("Đi").classes('text-[10px]')
                with ui.row().classes('items-center gap-1'):
                    ui.element('div').classes('w-3 h-3 rounded-full bg-green-600')
                    ui.label("Đến").classes('text-[10px]')
                with ui.row().classes('items-center gap-1'):
                    ui.element('div').classes('w-3 h-3 rounded-full bg-red-600')
                    ui.label("Hiện tại").classes('text-[10px]')
        
        # Map Container - có thanh kéo scroll
        with ui.element('div').classes(
            'relative w-full map-container'
        ).style(
            'height: calc(100vh - 280px); min-height: 300px; '
            'overflow: scroll; '
            '-webkit-overflow-scrolling: touch;'
        ) as map_scroll_container:
            
            # Zoom controls - fixed góc trái dưới
            with ui.element('div').classes('fixed bottom-24 left-4 z-50'):
                with ui.column().classes('gap-1'):
                    with ui.row().classes('gap-1'):
                        ui.button("+", on_click=lambda: adjust_zoom(0.2)).classes(
                            'zoom-btn text-xl font-bold'
                        ).props('dense flat')
                        ui.button("−", on_click=lambda: adjust_zoom(-0.2)).classes(
                            'zoom-btn text-xl font-bold'
                        ).props('dense flat')
                    lbl_zoom = ui.label('140%').classes(
                        'bg-white/90 px-2 py-1 rounded text-[10px] font-bold text-center shadow'
                    )
            
            # Image wrapper - thên transform để scroll hoạt động
            image_wrapper = ui.element('div').classes('inline-block').style(
                '''
                transform: scale(1.4);
                transform-origin: top left;
                transition: transform 0.2s ease;
                '''
            )

            with image_wrapper:
                image_view = ui.image(draw_base_map()).classes('w-full h-auto')
            
            # Distance label
            distance_label = ui.label().classes(
                'fixed bottom-24 right-4 z-50 text-sm font-bold '
                'px-3 py-1 rounded-full bg-white/90 shadow text-gray-700'
            )
    
    # Bind events
    end_sel.on_value_change(update_path)
    
    # Initialize
    update_path()
    start_gps_watch()