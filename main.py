from nicegui import ui
import campus_map 
import beta_map

# --- CUSTOM CSS ---
MAIN_CSS = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
    
    * {
        font-family: 'Inter', sans-serif !important;
    }
    
    body {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%) !important;
        min-height: 100vh;
        overflow-x: hidden;
    }
    
    .glass-container {
        background: rgba(255, 255, 255, 0.15) !important;
        backdrop-filter: blur(20px) !important;
        border: 1px solid rgba(255, 255, 255, 0.3) !important;
        border-radius: 24px !important;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1) !important;
    }
    
    .main-title {
        background: linear-gradient(135deg, #fff 0%, #f0f0f0 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        text-shadow: 0 4px 30px rgba(255, 255, 255, 0.3);
    }
    
    .card-campus {
        background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%) !important;
        border: none !important;
        border-radius: 20px !important;
        box-shadow: 0 10px 40px rgba(17, 153, 142, 0.4) !important;
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275) !important;
        overflow: hidden !important;
    }
    
    .card-campus:hover {
        transform: translateY(-8px) scale(1.02) !important;
        box-shadow: 0 20px 60px rgba(17, 153, 142, 0.5) !important;
    }
    
    .card-beta {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        border: none !important;
        border-radius: 20px !important;
        box-shadow: 0 10px 40px rgba(102, 126, 234, 0.4) !important;
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275) !important;
        overflow: hidden !important;
    }
    
    .card-beta:hover {
        transform: translateY(-8px) scale(1.02) !important;
        box-shadow: 0 20px 60px rgba(102, 126, 234, 0.5) !important;
    }
    
    .card-icon {
        background: rgba(255, 255, 255, 0.2) !important;
        border-radius: 50% !important;
        padding: 16px !important;
        margin-bottom: 12px !important;
    }
    
    .subtitle {
        color: rgba(255, 255, 255, 0.9) !important;
        text-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
    }
    
    @keyframes float {
        0%, 100% { transform: translateY(0px); }
        50% { transform: translateY(-10px); }
    }
    
    .floating {
        animation: float 4s ease-in-out infinite;
    }
    
    @keyframes pulse-ring {
        0% { box-shadow: 0 0 0 0 rgba(255, 255, 255, 0.4); }
        70% { box-shadow: 0 0 0 15px rgba(255, 255, 255, 0); }
        100% { box-shadow: 0 0 0 0 rgba(255, 255, 255, 0); }
    }
    
    .pulse-ring {
        animation: pulse-ring 2s ease-out infinite;
    }
    
    /* Mobile responsive */
    @media (max-width: 640px) {
        .mobile-stack {
            flex-direction: column !important;
        }
        .mobile-card {
            width: 100% !important;
            max-width: 280px !important;
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
ui.run(title="University Navigation", port=8000)