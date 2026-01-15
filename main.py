from nicegui import ui
import campus_map 
import beta_map

# --- CUSTOM CSS ---
MAIN_CSS = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
    
    * {
        font-family: 'Inter', sans-serif !important;
        box-sizing: border-box;
    }
    
    body {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 40%, #0f3460 70%, #1a1a2e 100%) !important;
        background-size: 400% 400%;
        animation: gradientShift 15s ease infinite;
        min-height: 100vh;
        overflow-x: hidden;
    }
    
    @keyframes gradientShift {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    .glass-container {
        background: rgba(255, 255, 255, 0.08) !important;
        backdrop-filter: blur(25px) saturate(180%) !important;
        -webkit-backdrop-filter: blur(25px) saturate(180%) !important;
        border: 1px solid rgba(255, 255, 255, 0.15) !important;
        border-radius: 28px !important;
        box-shadow: 
            0 8px 32px rgba(0, 0, 0, 0.3),
            inset 0 1px 0 rgba(255, 255, 255, 0.1) !important;
    }
    
    .main-title {
        background: linear-gradient(135deg, #00d4ff 0%, #7c3aed 50%, #f472b6 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        filter: drop-shadow(0 4px 20px rgba(0, 212, 255, 0.3));
        letter-spacing: 1px;
    }
    
    .card-campus {
        background: linear-gradient(135deg, #059669 0%, #34d399 50%, #6ee7b7 100%) !important;
        border: none !important;
        border-radius: 20px !important;
        box-shadow: 
            0 10px 40px rgba(5, 150, 105, 0.4),
            0 4px 15px rgba(52, 211, 153, 0.3),
            inset 0 1px 0 rgba(255, 255, 255, 0.2) !important;
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275) !important;
        overflow: hidden !important;
        position: relative;
    }
    
    .card-campus::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.2), transparent);
        transition: left 0.5s ease;
    }
    
    .card-campus:hover::before {
        left: 100%;
    }
    
    .card-campus:hover {
        transform: translateY(-10px) scale(1.03) !important;
        box-shadow: 
            0 25px 60px rgba(5, 150, 105, 0.5),
            0 10px 30px rgba(52, 211, 153, 0.4),
            inset 0 1px 0 rgba(255, 255, 255, 0.3) !important;
    }
    
    .card-beta {
        background: linear-gradient(135deg, #7c3aed 0%, #a855f7 50%, #c084fc 100%) !important;
        border: none !important;
        border-radius: 20px !important;
        box-shadow: 
            0 10px 40px rgba(124, 58, 237, 0.4),
            0 4px 15px rgba(168, 85, 247, 0.3),
            inset 0 1px 0 rgba(255, 255, 255, 0.2) !important;
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275) !important;
        overflow: hidden !important;
        position: relative;
    }
    
    .card-beta::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.2), transparent);
        transition: left 0.5s ease;
    }
    
    .card-beta:hover::before {
        left: 100%;
    }
    
    .card-beta:hover {
        transform: translateY(-10px) scale(1.03) !important;
        box-shadow: 
            0 25px 60px rgba(124, 58, 237, 0.5),
            0 10px 30px rgba(168, 85, 247, 0.4),
            inset 0 1px 0 rgba(255, 255, 255, 0.3) !important;
    }
    
    .card-icon {
        background: rgba(255, 255, 255, 0.25) !important;
        border-radius: 50% !important;
        padding: 18px !important;
        margin-bottom: 14px !important;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    
    .card-campus:hover .card-icon,
    .card-beta:hover .card-icon {
        transform: scale(1.1) rotate(5deg);
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.15);
    }
    
    .subtitle {
        color: rgba(255, 255, 255, 0.85) !important;
        text-shadow: 0 2px 15px rgba(0, 0, 0, 0.2);
        letter-spacing: 0.5px;
    }
    
    @keyframes float {
        0%, 100% { transform: translateY(0px) rotate(0deg); }
        25% { transform: translateY(-8px) rotate(-2deg); }
        50% { transform: translateY(-12px) rotate(0deg); }
        75% { transform: translateY(-8px) rotate(2deg); }
    }
    
    .floating {
        animation: float 5s ease-in-out infinite;
    }
    
    @keyframes pulse-ring {
        0% { box-shadow: 0 0 0 0 rgba(52, 211, 153, 0.5); }
        50% { box-shadow: 0 0 0 12px rgba(52, 211, 153, 0); }
        100% { box-shadow: 0 0 0 0 rgba(52, 211, 153, 0); }
    }
    
    .pulse-ring {
        animation: pulse-ring 2.5s ease-out infinite;
    }
    
    @keyframes shimmer {
        0% { opacity: 0.5; }
        50% { opacity: 1; }
        100% { opacity: 0.5; }
    }
    
    .shimmer {
        animation: shimmer 2s ease-in-out infinite;
    }
    
    /* Mobile responsive */
    @media (max-width: 640px) {
        .mobile-stack {
            flex-direction: column !important;
        }
        .mobile-card {
            width: 100% !important;
            max-width: 300px !important;
        }
    }
</style>
"""

# --- TRANG CHỦ (MENU) ---
@ui.page('/')
def main_menu():
    ui.add_head_html(MAIN_CSS)
    
    with ui.column().classes(
        'w-full min-h-screen items-center justify-center p-4'
    ):
        # Glass Container
        with ui.column().classes(
            'glass-container p-6 sm:p-8 items-center gap-6 w-full max-w-md'
        ):
            # Logo/Icon
            with ui.element('div').classes('floating'):
                ui.label("🏛️").classes('text-5xl sm:text-6xl')
            
            # Title
            ui.label("HỆ THỐNG DẪN ĐƯỜNG").classes(
                'text-xl sm:text-2xl font-extrabold main-title text-center'
            )
            ui.label("Đại học FPT Quy Nhơn").classes(
                'text-sm sm:text-base subtitle font-medium -mt-4'
            )
            
            # Cards Container
            with ui.column().classes(
                'w-full gap-4 mt-4 items-center mobile-stack'
            ):
                # Card 1: Campus Map
                with ui.card().classes(
                    'card-campus mobile-card w-full p-5 items-center cursor-pointer pulse-ring'
                ).on('click', lambda: ui.navigate.to('/campus')):
                    with ui.element('div').classes('card-icon'):
                        ui.icon('🌳 KHUÔN VIÊN', size='2.0rem').classes('text-white')
                    ui.label("Dẫn đường giữa các tòa nhà").classes(
                        'text-xs text-white/80 text-center'
                    )
                
                # Card 2: Beta Building Map
                with ui.card().classes(
                    'card-beta mobile-card w-full p-5 items-center cursor-pointer'
                ).on('click', lambda: ui.navigate.to('/beta')):
                    with ui.element('div').classes('card-icon'):
                        ui.icon('🏢 TÒA BETA', size='2.0rem').classes('text-white')
                    ui.label("Dẫn đường trong tòa nhà (5 tầng)").classes(
                        'text-xs text-white/80 text-center'
                    )
            
            # Footer
            ui.label("© 2026 FPT University").classes(
                'text-[10px] text-white/50 mt-4'
            )

# --- ĐỊNH NGHĨA TRANG CON ---
@ui.page('/campus')
def page_campus():
    campus_map.create_page()

@ui.page('/beta')
def page_beta():
    beta_map.create_page()

# --- CHẠY SERVER ---
ui.run(title="University Navigation", port=8080)