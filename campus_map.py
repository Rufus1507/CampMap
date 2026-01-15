from nicegui import ui
import networkx as nx
from PIL import Image, ImageDraw
import io, base64
import math
import os
# ============================================================================
# CUSTOM CSS STYLES
# ============================================================================

CAMPUS_CSS = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
    
    * {
        font-family: 'Inter', sans-serif !important;
        box-sizing: border-box;
    }
    
    body {
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 50%, #0f172a 100%) !important;
        min-height: 100vh;
    }
    
    .glass-header {
        background: rgba(255, 255, 255, 0.98) !important;
        backdrop-filter: blur(20px) saturate(180%) !important;
        -webkit-backdrop-filter: blur(20px) saturate(180%) !important;
        border-bottom: 1px solid rgba(255, 255, 255, 0.3) !important;
        box-shadow: 0 4px 30px rgba(0, 0, 0, 0.08) !important;
    }
    
    .glass-card {
        background: rgba(255, 255, 255, 0.98) !important;
        backdrop-filter: blur(15px) !important;
        border: 1px solid rgba(255, 255, 255, 0.4) !important;
        box-shadow: 
            0 8px 32px rgba(0, 0, 0, 0.12),
            inset 0 1px 0 rgba(255, 255, 255, 0.5) !important;
        border-radius: 18px !important;
    }
    
    .btn-back {
        background: linear-gradient(135deg, #374151 0%, #1f2937 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 12px !important;
        font-weight: 600 !important;
        text-transform: none !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15) !important;
    }
    
    .btn-back:hover {
        transform: translateX(-4px) !important;
        box-shadow: 0 6px 20px rgba(0, 0, 0, 0.25) !important;
    }
    
    .btn-voice {
        background: linear-gradient(135deg, #7c3aed 0%, #a855f7 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 14px !important;
        font-weight: 700 !important;
        text-transform: none !important;
        box-shadow: 0 6px 20px rgba(124, 58, 237, 0.4) !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
    }
    
    .btn-voice:hover {
        transform: scale(1.03) translateY(-2px) !important;
        box-shadow: 0 10px 30px rgba(124, 58, 237, 0.5) !important;
    }
    
    .btn-beta {
        background: linear-gradient(135deg, #059669 0%, #34d399 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 14px !important;
        font-weight: 700 !important;
        text-transform: none !important;
        box-shadow: 0 6px 20px rgba(5, 150, 105, 0.4) !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
    }
    
    .btn-beta:hover {
        transform: translateY(-3px) scale(1.02) !important;
        box-shadow: 0 10px 30px rgba(5, 150, 105, 0.5) !important;
    }
    
    .legend-card {
        background: linear-gradient(135deg, rgba(255,255,255,0.95), rgba(248,250,252,0.95)) !important;
        border-radius: 14px !important;
        border: 1px solid rgba(226, 232, 240, 0.8) !important;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.05) !important;
    }
    
    .map-container {
        background: linear-gradient(135deg, rgba(255,255,255,0.98), rgba(248,250,252,0.98)) !important;
        border-radius: 18px !important;
        box-shadow: 
            0 10px 50px rgba(0, 0, 0, 0.15),
            inset 0 1px 0 rgba(255, 255, 255, 0.5) !important;
        overflow: auto !important;
        touch-action: pan-x pan-y;
    }
    
    .main-title {
        background: linear-gradient(135deg, #059669 0%, #34d399 50%, #6ee7b7 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        filter: drop-shadow(0 2px 10px rgba(5, 150, 105, 0.3));
    }
    
    .gps-badge {
        background: linear-gradient(135deg, #fef3c7 0%, #fcd34d 100%) !important;
        border: 2px solid #f59e0b !important;
        border-radius: 24px !important;
        box-shadow: 0 4px 20px rgba(245, 158, 11, 0.35) !important;
        animation: gps-pulse 2s ease-in-out infinite;
    }
    
    @keyframes gps-pulse {
        0%, 100% { opacity: 1; transform: scale(1); }
        50% { opacity: 0.9; transform: scale(1.02); }
    }
    
    .zoom-btn {
        background: linear-gradient(135deg, #ef4444 0%, #f87171 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 12px !important;
        box-shadow: 0 4px 15px rgba(239, 68, 68, 0.4) !important;
        min-width: 44px !important;
        min-height: 44px !important;
        transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1) !important;
    }
    
    .zoom-btn:hover {
        transform: scale(1.1) !important;
        box-shadow: 0 6px 25px rgba(239, 68, 68, 0.5) !important;
    }
    
    .zoom-btn:active {
        transform: scale(0.95) !important;
    }
    
    @keyframes pulse-glow {
        0%, 100% { box-shadow: 0 0 8px rgba(124, 58, 237, 0.4); }
        50% { box-shadow: 0 0 25px rgba(124, 58, 237, 0.7); }
    }
    
    .pulse-glow {
        animation: pulse-glow 2.5s ease-in-out infinite;
    }
</style>
"""

# ============================================================================
# DATA DEFINITIONS
# ============================================================================

# Visible locations for user selection
VISIBLE_LOCATIONS = {
    "PARKING LOT A": (190, 840), "GATE": (500, 900), "PARKING LOT B": (170, 600),
    "THE THINKER": (470, 760), "GAMMA BUILDING": (400, 500), "BETA BUILDING": (720, 700),
    "CANTEEN": (580, 390), "SOCCER": (880, 440), "BASKETBALL": (840, 330),
    "VOLLEYBALL": (850, 370), "VOVINAM": (900, 300),
    "DOM A": (1300, 300), "DOM B": (1370, 480),
}

# Virtual nodes for path connections (hidden from UI)
VIRTUAL_NODES = {
    "1": (300, 980), "2": (170, 970), "3": (80, 960), "4": (100, 640),
    "5": (590, 840), "BETA": (570, 740), "6": (280, 700), "7": (170, 760),
    "GAMMA": (420, 640), "8": (530, 600), "9": (420, 900), "10": (350, 700),
    "11": (380, 800), "12": (700, 540), "13": (730, 500), "14": (910, 380),
    "15": (930, 340), "16": (480, 420), "18": (720, 435), "19": (1060, 320),
    "20": (1120, 350), "21": (1065, 370), "22": (1240, 420), "23": (1300, 410),
}

LOCATIONS = {**VISIBLE_LOCATIONS, **VIRTUAL_NODES}

# GPS coordinates
LOCATIONS_GPS = {
    "GATE": (13.804553052179601, 109.21950215399711),
    "BETA BUILDING": (13.804037728087135, 109.21905987562394),
    "GAMMA BUILDING": (13.803719317148747, 109.21978179205664),
    "CANTEEN": (13.80346943932719, 109.21935393966768),
    "SOCCER": (13.80358132697852, 109.21871383179098),
    "DOM B": (13.803615255456071, 109.21766757243233),
    "PARKING LOT A": (13.804426590467092, 109.22022472831937),
    "PARKING LOT B": (13.803952661753089, 109.22022791802131),
    "THE THINKER": (13.804240736184244, 109.21961230554994),
    "BASKETBALL": (13.803398194907908, 109.21879893155109),
    "VOLLEYBALL": (13.803320755299886, 109.21882444916649),
    "VOVINAM": (13.80322163256409, 109.21863625675296),
    "DOM A": (13.803221632561929, 109.21778460632828),
}

# Voice aliases
VOICE_ALIAS = {
    "CANTEEN": ["CANTEEN", "CAN TEEN", "CAN TIN", "CANTIN", "CANTEAN","CĂNG TIN","NHÀ ĂN","CĂN TIN","NHÀ EM","NHÀ ANH","KÊNH TINH"],
    "GAMMA BUILDING": ["GAMMA", "GAMMA BUILDING","TÒA GAMMA"],
    "BETA BUILDING": ["BETA", "BETA BUILDING","TÒA BETA","BETTA"],
    "GATE": ["GATE", "MAIN GATE", "ENTRANCE","CỔNG","CỔNG TRƯỜNG","CỔNG CHÍNH"],
    "PARKING LOT A": ["PARKING LOT A", "PARKING A", "PARK A","NHÀ XE A","BÃI ĐẬU XE A","ĐẬU XE A","BÃI ĐỖ XE A","NHÀ XE","BÃI ĐỖ XE","BÃI ĐẬU XE","BÃI GỬI XE A","NHÀ GỬI XE A"],
    "PARKING LOT B": ["PARKING LOT B", "PARKING B", "PARK B","NHÀ XE B","BÃI ĐẬU XE B","ĐẬU XE B","BÃI ĐỖ XE B","BÃI GỬI XE B","NHÀ GỬI XE B"],
    "THE THINKER": ["THE THINKER", "THINKER", "STATUE","TƯỢNG THINKER","TƯỢNG THIN CƠ","TƯỢNG THIÊN CƠ","TƯỢNG","TƯỢNG ĐỜI THIÊN CƠ","TƯỢNG ĐỜ THIÊN CƠ"],
    "SOCCER": ["SOCCER FIELD", "SOCCER", "FOOTBALL FIELD", "FOOTBALL","SÂN BÓNG ĐÁ","BÓNG ĐÁ","SÂN BÓNG","SÂN BANH"],
    "BASKETBALL": ["BASKETBALL COURT", "BASKETBALL","SÂN BÓNG RỔ","BÓNG RỔ"],
    "VOLLEYBALL": ["VOLLEYBALL COURT", "VOLLEYBALL","SÂN BÓNG CHUYỀN","BÓNG CHUYỀN"],
    "DOM A":{"DOM A", "DORM A", "KÝ TÚC XÁ A","KÝ TÚC XÁ"},
    "DOM B":{"DOM B", "DORM B", "KÝ TÚC XÁ B"},
    "VOVINAM": {"VOVINAM AREA", "VOVINAM","SÂN VÕ VOVINAM","SÂN VÕ","SÂN VOVINAM"},
}

# Graph edges
EDGES = [
    ('BETA', 'BETA BUILDING'), ('GAMMA BUILDING', 'GAMMA'),
    ("GATE", "1"), ("1", "2"), ("2", "3"), ('2', 'PARKING LOT A'), ('3', '4'),
    ("PARKING LOT B", "4"), ('GATE', 'THE THINKER'), ('GATE', '5'), ('5', 'BETA'),
    ('BETA', 'THE THINKER'), ('6', 'GAMMA'), ('6', '7'), ('6', 'PARKING LOT B'),
    ('7', 'PARKING LOT A'), ('BETA', '8'), ('8', '16'), ('8', 'GAMMA'), ('9', 'GATE'),
    ('9', '10'), ('10', '6'), ('10', 'GAMMA'), ('10', '11'), ('11', 'THE THINKER'),
    ('8', '12'), ('BETA BUILDING', '12'), ('12', '13'), ('13', 'SOCCER'),
    ('SOCCER', '14'), ('14', '15'), ('VOLLEYBALL', '15'), ('BASKETBALL', '15'),
    ('VOVINAM', '15'), ("BASKETBALL", "VOLLEYBALL"), ("VOLLEYBALL", "VOVINAM"),
    ("BASKETBALL", "VOVINAM"), ('GAMMA BUILDING', '16'), ('16', 'CANTEEN'),
    ('CANTEEN', '18'), ('18', '13'), ('18', '14'), ('14', '19'), ('19', '20'),
    ('20', 'DOM A'), ('SOCCER', '21'), ('21', '22'), ('22', '23'),
    ('19', '21'), ('23', 'DOM B'),
    ("DOM A", "DOM B")
]
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
IMAGE_PATH = os.path.join(BASE_DIR, "khuonvientruong.jpg")

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
BASE_SCALE = 1 / 3   # 👈 thu nhỏ 3 lần

current_zoom = 1.0  # zoom logic chỉ lo zoom, không lo scale gốc
img0 = Image.open(IMAGE_PATH)
BASE_W, BASE_H = img0.size


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
        if not os.path.exists(IMAGE_PATH):
            print("❌ KHÔNG TÌM THẤY ẢNH:", IMAGE_PATH)
            return ""

        img = Image.open(IMAGE_PATH).convert("RGB")
        buf = io.BytesIO()
        img.save(buf, format="PNG")
        return f"data:image/png;base64,{base64.b64encode(buf.getvalue()).decode()}"

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
        nonlocal user_lat, user_lon
        if user_lat is None or user_lon is None:
            return

        start = snap_gps_to_node(user_lat, user_lon)
        end = end_sel.value

        if not start:
            return

        # ✅ CHƯA CHỌN ĐIỂM ĐẾN → chỉ vẽ điểm hiện tại
        if end is None:
            image_view.source = draw_path([start])
            distance_label.text = "📍 Vị trí hiện tại"
            return

        # ✅ ĐIỂM ĐẾN TRÙNG ĐIỂM BẮT ĐẦU
        if start == end:
            image_view.source = draw_path([start])
            distance_label.text = "📍 Bạn đang ở đây"
            return

        # ✅ CÓ ĐƯỜNG ĐI
        path, dist = find_shortest_path(start, end)
        image_view.source = draw_path(path)
        distance_label.text = f"🚶‍♂️ {dist*2/10:.0f} bước"
        
    # ========== ZOOM HANDLER ==========

    def adjust_zoom(delta):
        global current_zoom

        current_zoom = max(0.5, min(3.0, current_zoom + delta))

        image_view.style(
            f'''
            transform: scale({current_zoom});
            transform-origin: top left;
            transition: transform 0.2s ease;
            '''
        )

        lbl_zoom.text = f"{int(current_zoom * 100)}%"
        
    def start_voice():
        ui.run_javascript('''
            const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
            if (!SpeechRecognition) {
                emitEvent('voice-error', {message: 'Browser không hỗ trợ'});
                return;
            }

            function runRecognition(lang) {
                return new Promise((resolve, reject) => {
                    const r = new SpeechRecognition();
                    r.lang = lang;
                    r.continuous = false;
                    r.interimResults = false;

                    r.onresult = (e) =>
                        resolve(e.results[0][0].transcript);

                    r.onerror = () => reject();
                    r.start();
                });
            }

            // Thử tiếng Việt trước
            runRecognition('vi-VN')
                .then(text => emitEvent('voice-result', { text: text.toUpperCase() }))
                .catch(() => {
                    // Fail → thử tiếng Anh
                    runRecognition('en-US')
                        .then(text => emitEvent('voice-result', { text: text.toUpperCase() }))
                        .catch(() =>
                            emitEvent('voice-error', { message: 'Không nhận dạng được giọng nói' })
                        );
                });
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
        spoken_label.text = f"{spoken_raw}"
        spoken_norm = normalize_text(spoken_raw)

        # 🔥 Gom alias + sắp xếp theo độ dài giảm dần
        alias_map = []
        for canonical, aliases in VOICE_ALIAS.items():
            for a in aliases:
                alias_map.append((canonical, normalize_text(a)))

        alias_map.sort(key=lambda x: len(x[1]), reverse=True)

        # 🎯 Match alias dài trước
        for canonical, alias_norm in alias_map:
            if alias_norm in spoken_norm:
                end_sel.value = canonical
                update_path()
                ui.notify(f"✅ {canonical}")
                return

        ui.notify(f"❌ Không nhận ra: {spoken_raw}")
    
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
                    value=None,
                    label="🏁 Điểm đến"
                ).classes('w-full').props(
                    'outlined dense options-dense hide-dropdown-icon'
                ).style('font-size: 12px;')
                
                # Voice button
                with ui.column().classes('w-full gap-2'):
                    ui.button("🎤 Nói điểm đến", on_click=start_voice).classes(
                        'flex-1 btn-voice text-xs py-2'
                    )
                    spoken_label = ui.label("🎙 ...").classes(
                        'flex-1 text-xs font-bold text-purple-700 self-center text-center'
                    )
                    ui.label(
                            '💡 Bạn có thể nói tiếng Việt hoặc tiếng Anh\n'
                            'Ví dụ: "NHÀ ĂN" → CANTEEN'
                        ).classes(
                            'text-[12px] text-center text-red-500 italic'
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
        # Distance label will be defined below in the map container


        # ================= MAP CONTAINER =================
        with ui.element('div').classes(
            'relative w-full map-container'
        ).style(
            '''
            height: calc(100vh - 280px);
            min-height: 300px;
            overflow: scroll;
            -webkit-overflow-scrolling: touch;
            '''
        ) as map_scroll_container:
        
            # ================= ZOOM CONTROLS =================
            with ui.element('div').classes('fixed bottom-60 left-4 z-50'):
                with ui.column().classes('gap-1'):
                    with ui.row().classes('gap-1'):
                        ui.button("+", on_click=lambda: adjust_zoom(0.2)).classes(
                            'zoom-btn text-xl font-bold'
                        ).props('dense flat')
                        ui.button("−", on_click=lambda: adjust_zoom(-0.2)).classes(
                            'zoom-btn text-xl font-bold'
                        ).props('dense flat')

                    lbl_zoom = ui.label('100%').classes(
                        'bg-white/90 px-2 py-1 rounded text-[10px] font-bold text-center shadow'
                    )

            # ================= MAP IMAGE =================
            image_view = ui.image(draw_base_map()).style(
                f'''
                width: {int(BASE_W * BASE_SCALE * current_zoom)}px;
                height: {int(BASE_H * BASE_SCALE * current_zoom)}px;
                max-width: none;
                max-height: none;
                display: block;
                '''
            )



            # ================= DISTANCE LABEL =================
            distance_label = ui.label().classes(
                'fixed bottom-24 right-4 z-50 text-sm font-bold '
                'px-3 py-1 rounded-full bg-white/90 shadow text-gray-700'
            )
    
    # Bind events
    end_sel.on_value_change(update_path)
    
    # Initialize
    update_path()
    start_gps_watch()