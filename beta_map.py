from nicegui import ui
import networkx as nx
from PIL import Image, ImageDraw
import io
import base64
import random
import math

# ============================================================================
# CONSTANTS - DỮ LIỆU TỌA ĐỘ CÁC TẦNG
# ============================================================================

FLOOR_PLANS = {
    "Floor 1": "floor1.PNG",
    "Floor 2": "floor2.PNG",
    "Floor 3": "floor3.PNG",
    "Floor 4": "floor4.PNG",
    "Floor 5": "floor5.PNG"
}

# Tọa độ các phòng theo tầng
FLOOR_1_LOCATIONS = {
    "EXTRA FRONT": (520, 1000),
    "STAIRS_F1_A": (900, 500),
    "STAIRS_F1_B": (240, 500),
    "LAB AI": (890, 290),
    "IT SP": (803, 351),
    "MEETING ROOM": (798, 608),
    "STUDENTS SP": (682, 753),
    "BRONZE DRUM": (520, 800),
    "ADMISSIONS OFFICE": (370, 900),
    "WC FEMALE (F1)": (236, 400),
    "WC MALE (F1)": (238, 584),
    "EXTRA BACK": (126, 290),
    "F1_2": (800, 300),
    "F1_1": (795, 497),
    "F1_3": (677, 679),
    "MAIN HALL": (520, 650),
    "F1_4": (379, 680),
    "F1_5": (275, 315),
    "LIBRARY": (275, 315),
    "ELEVATOR_1": (745, 500)
}

FLOOR_2_LOCATIONS = {
    "201": (245, 165), "202": (510, 200), "203": (780, 165),
    "204": (780, 50), "205": (780, 100), "206": (780, 225),
    "207": (950, 270), "208": (830, 270), "209": (950, 695),
    "210": (830, 695), "211": (780, 750), "212": (780, 895),
    "213": (780, 950), "214": (780, 825), "215": (510, 750),
    "216": (245, 825), "217": (245, 950), "218": (245, 895),
    "219": (245, 750), "220": (245, 225),
    "WC MALE (F2)": (245, 600), "WC FEMALE (F2)": (245, 380),
    "ELEVATOR_2": (750, 500), "STAIRS_F2_A": (900, 500),
    "STAIRS_F2_B": (245, 500),
    "F2_1": (245, 270), "F2_2": (510, 270), "F2_3": (780, 270),
    "F2_4": (830, 695), "F2_5": (510, 695), "F2_6": (245, 659),
    "F2_7": (780, 500)
}

FLOOR_3_LOCATIONS = {
    "301": (520, 200), "302": (520, 201), "303": (780, 167),
    "304": (780, 42), "305": (780, 90), "306": (780, 230),
    "307": (957, 272), "308": (841, 272), "309": (958, 695),
    "310": (838, 695), "311": (780, 736), "312": (780, 900),
    "313": (780, 957), "314": (780, 818), "315": (520, 781),
    "316": (520, 780), "317": (247, 817), "318": (247, 955),
    "319": (247, 904), "320": (247, 735), "321": (247, 233),
    "322": (247, 95), "323": (247, 43), "324": (247, 170),
    "WC MALE (F3)": (247, 604), "WC FEMALE (F3)": (247, 370),
    "ELEVATOR_3": (746, 500), "STAIRS_F3_A": (918, 500),
    "STAIRS_F3_B": (247, 488),
    "F3_1": (247, 272), "F3_2": (520, 272), "F3_3": (780, 272),
    "F3_4": (780, 500), "F3_5": (780, 695), "F3_6": (520, 695),
    "F3_7": (247, 695)
}

FLOOR_4_LOCATIONS = {
    "401": (520, 200), "402": (520, 201), "403": (780, 167),
    "404": (780, 42), "405": (780, 90), "406": (780, 230),
    "407": (957, 272), "408": (841, 272), "409": (958, 695),
    "410": (838, 695), "411": (780, 736), "412": (780, 900),
    "413": (780, 957), "414": (780, 818), "415": (520, 781),
    "416": (520, 780), "417": (247, 817), "418": (247, 955),
    "419": (247, 904), "420": (247, 735), "421": (247, 233),
    "422": (247, 95), "423": (247, 43), "424": (247, 170),
    "WC MALE (F4)": (247, 604), "WC FEMALE (F4)": (247, 370),
    "ELEVATOR_4": (746, 500), "STAIRS_F4_A": (918, 500),
    "STAIRS_F4_B": (247, 488),
    "F4_1": (247, 272), "F4_2": (520, 272), "F4_3": (780, 272),
    "F4_4": (780, 500), "F4_5": (780, 695), "F4_6": (520, 695),
    "F4_7": (247, 695)
}

FLOOR_5_LOCATIONS = {
    "501": (740, 350), "502": (780, 416), "503": (790, 689),
    "504": (740, 733), "505": (740, 856), "506": (740, 905),
    "507": (740, 800), "508": (500, 768), "509": (501, 768),
    "510": (258, 806), "511": (258, 911), "512": (258, 855),
    "513": (258, 734), "514": (258, 318), "515": (258, 106),
    "516": (258, 200),
    "WC MALE (F5)": (258, 600), "WC FEMALE (F5)": (258, 406),
    "STAIRS_F5_B": (141, 505), "ELEVATOR_5": (703, 503),
    "STAIRS_F5_A": (503, 862),
    "F5_1": (258, 505), "F5_2": (258, 689), "F5_3": (500, 689),
    "F5_4": (740, 689), "F5_5": (740, 503)
}

ALL_FLOORS = {
    "Floor 1": FLOOR_1_LOCATIONS,
    "Floor 2": FLOOR_2_LOCATIONS,
    "Floor 3": FLOOR_3_LOCATIONS,
    "Floor 4": FLOOR_4_LOCATIONS,
    "Floor 5": FLOOR_5_LOCATIONS
}

# Danh sách phòng hiển thị cho user chọn
ROOMS_DATABASE = {
    "Floor 1": [
        "EXTRA FRONT", "STAIRS_F1_A", "LAB AI", "IT SP", "MEETING ROOM",
        "STUDENTS SP", "BRONZE DRUM", "ADMISSIONS OFFICE", "WC MALE (F1)",
        "WC FEMALE (F1)", "LIBRARY", "STAIRS_F1_B",
        "MAIN HALL",
        "EXTRA BACK", "ELEVATOR_1"
    ],
    "Floor 2": [
        "201", "202", "203", "204", "205", "206", "207", "208", "209",
        "210", "211", "212", "213", "214", "215", "216", "217", "218",
        "219", "220", "WC MALE (F2)", "WC FEMALE (F2)", "ELEVATOR_2",
        "STAIRS_F2_A", "STAIRS_F2_B"
    ],
    "Floor 3": [
        "301", "302", "303", "304", "305", "306", "307", "308", "309",
        "310", "311", "312", "313", "314", "315", "316", "317", "318",
        "319", "320", "WC MALE (F3)", "WC FEMALE (F3)", "ELEVATOR_3",
        "STAIRS_F3_B", "STAIRS_F3_A"
    ],
    "Floor 4": [
        "401", "402", "403", "404", "405", "406", "407", "408", "409",
        "410", "411", "412", "413", "414", "415", "416", "417", "418",
        "419", "420", "WC MALE (F4)", "WC FEMALE (F4)", "ELEVATOR_4",
        "STAIRS_F4_B", "STAIRS_F4_A"
    ],
    "Floor 5": [
        "501", "502", "503", "504", "505", "506", "507", "508", "509",
        "510", "511", "512", "513", "514", "515", "516", "WC MALE (F5)",
        "WC FEMALE (F5)", "ELEVATOR_5", "STAIRS_F5_B", "STAIRS_F5_A"
    ]
}
DISPLAY_NAMES = {
    # ===== FLOOR 1 =====
    "EXTRA FRONT": "Cổng trước",
    "EXTRA BACK": "Cổng sau",
    "MAIN HALL": "Sảnh chính",
    "BRONZE DRUM": "Trống đồng",
    "ADMISSIONS OFFICE": "Phòng tuyển sinh",
    "STUDENTS SP": "Phòng công tác sinh viên",
    "MEETING ROOM": "Phòng họp",
    "IT SP": "Phòng IT",
    "LAB AI": "Phòng Lab AI",
    "LIBRARY": "Thư viện",
    "WC MALE (F1)": "WC Nam (Tầng 1)",
    "WC FEMALE (F1)": "WC Nữ (Tầng 1)",
    "STAIRS_F1_A": "Cầu thang A (Tầng 1)",
    "STAIRS_F1_B": "Cầu thang B (Tầng 1)",
    "ELEVATOR_1": "Thang máy (Tầng 1)",

    # ===== FLOOR 2 =====
    "WC MALE (F2)": "WC Nam (Tầng 2)",
    "WC FEMALE (F2)": "WC Nữ (Tầng 2)",
    "STAIRS_F2_A": "Cầu thang A (Tầng 2)",
    "STAIRS_F2_B": "Cầu thang B (Tầng 2)",
    "ELEVATOR_2": "Thang máy (Tầng 2)",

    # ===== FLOOR 3 =====
    "WC MALE (F3)": "WC Nam (Tầng 3)",
    "WC FEMALE (F3)": "WC Nữ (Tầng 3)",
    "STAIRS_F3_A": "Cầu thang A (Tầng 3)",
    "STAIRS_F3_B": "Cầu thang B (Tầng 3)",
    "ELEVATOR_3": "Thang máy (Tầng 3)",

    # ===== FLOOR 4 =====
    "WC MALE (F4)": "WC Nam (Tầng 4)",
    "WC FEMALE (F4)": "WC Nữ (Tầng 4)",
    "STAIRS_F4_A": "Cầu thang A (Tầng 4)",
    "STAIRS_F4_B": "Cầu thang B (Tầng 4)",
    "ELEVATOR_4": "Thang máy (Tầng 4)",

    # ===== FLOOR 5 =====
    "WC MALE (F5)": "WC Nam (Tầng 5)",
    "WC FEMALE (F5)": "WC Nữ (Tầng 5)",
    "STAIRS_F5_A": "Cầu thang A (Tầng 5)",
    "STAIRS_F5_B": "Cầu thang B (Tầng 5)",
    "ELEVATOR_5": "Thang máy (Tầng 5)",
    "501": "501: Hội truường",
    "516": "516: Hội trường",
}
def display_name(node):
    return DISPLAY_NAMES.get(node, node)

# ============================================================================
# GRAPH EDGES - ĐỊNH NGHĨA CÁC ĐƯỜNG ĐI
# ============================================================================

EDGES_FLOOR_1 = [
    ("EXTRA FRONT", "BRONZE DRUM"), ("BRONZE DRUM", "ADMISSIONS OFFICE"),
    ("BRONZE DRUM", "STUDENTS SP"), ("MAIN HALL", "BRONZE DRUM"),
    ("MAIN HALL", "WC MALE (F1)"), ("MAIN HALL", "WC FEMALE (F1)"),
    ("MAIN HALL", "MEETING ROOM"), ("MAIN HALL", "ADMISSIONS OFFICE"),
    ("MAIN HALL", "STUDENTS SP"), ("MAIN HALL", "LIBRARY"),
    ("MEETING ROOM", "F1_1"), ("F1_1", "ELEVATOR_1"),
    ("F1_1", "STAIRS_F1_A"), ("LIBRARY", "EXTRA BACK"),
    ("IT SP", "LIBRARY"), ("IT SP", "F1_1"), ("IT SP", "F1_2"),
    ("LAB AI", "F1_2"), ("LIBRARY", "F1_2"),
    ("IT SP", "WC MALE (F1)"), ("IT SP", "WC FEMALE (F1)"),
    ("F1_2", "WC MALE (F1)"), ("F1_2", "WC FEMALE (F1)"),
    ("LIBRARY", "WC MALE (F1)"), ("LIBRARY", "WC FEMALE (F1)"),
    ("MAIN HALL", "F1_3"), ("MEETING ROOM", "F1_3"),
    ("STUDENTS SP", "F1_3"), ("BRONZE DRUM", "F1_3"),
    ("F1_4", "F1_3"), ("MAIN HALL", "F1_4"),
    ("WC MALE (F1)", "F1_4"), ("LIBRARY", "F1_4"),
    ("STUDENTS SP", "F1_4"), ("BRONZE DRUM", "F1_4"),
    ("EXTRA FRONT", "F1_4"), ("F1_4", "STAIRS_F1_B"),
    ("WC MALE (F1)", "STAIRS_F1_B"), ("WC FEMALE (F1)", "STAIRS_F1_B"),
    ("MAIN HALL", "STAIRS_F1_B"), ("F1_3", "STAIRS_F1_B"),
    ("LIBRARY", "STAIRS_F1_B"), ("F1_2", "STAIRS_F1_B"),
    ("IT SP", "STAIRS_F1_B"), ("F1_4", "ADMISSIONS OFFICE"),
    ("MAIN HALL", "LIBRARY"), ("MEETING ROOM", "F1_1"),
    ("F1_1", "ELEVATOR_1"), ("F1_1", "STAIRS_F1_A"),("EXTRA FRONT", "ADMISSIONS OFFICE"),
    ("STAIRS_F1_A", "WC MALE (F1)"), ("STAIRS_F1_A", "WC FEMALE (F1)"),
    ("STAIRS_F1_A", "STAIRS_F1_B"), ("STAIRS_F1_A", "EXTRA BACK"),
    ("MEETING ROOM", "WC MALE (F1)"),( "MEETING ROOM", "WC FEMALE (F1)"),
    ("MEETING ROOM", "LIBRARY"), ("MEETING ROOM", "STAIRS_F1_B"),
    ("MEETING ROOM", "EXTRA BACK"), ("STUDENTS SP", "EXTRA FRONT"),
    ("BRONZE DRUM", "WC FEMALE (F1)"), ("ADMISSIONS OFFICE", "WC FEMALE (F1)"),
    ("EXTRA FRONT", "WC FEMALE (F1)"),  ("LIBRARY", "STAIRS_F1_A")
]

EDGES_FLOOR_2 = [
    ('201', '220'), ('220', 'F2_1'), ('F2_1', 'WC FEMALE (F2)'),
    ('WC FEMALE (F2)', 'STAIRS_F2_B'), ('STAIRS_F2_B', 'WC MALE (F2)'),
    ('WC MALE (F2)', 'F2_6'),('F2_6', '219'), ('219', '216'),
    ('216', '218'), ('218', '217'), ('F2_1', 'F2_2'),
    ('F2_2', '202'), ('F2_2', 'F2_3'), ('F2_3', '208'),
    ('208', '207'), ('F2_3', '206'), ('206', '203'),
    ('203', '205'), ('205', '204'), ('F2_3', 'F2_7'),
    ('F2_7', 'STAIRS_F2_A'), ('F2_7', 'ELEVATOR_2'),
    ('F2_7', 'F2_4'), ('F2_4', '210'), ('210', '209'),
    ('F2_4', '211'), ('211', '214'), ('214', '212'),
    ('212', '213'), ('F2_4', 'F2_5'), ('F2_5', '215'), ('F2_5', 'F2_6')
]

EDGES_FLOOR_3 = [
    ('323', '322'), ('322', '324'), ('324', '321'),
    ('321', 'F3_1'), ('F3_1', 'F3_2'),
    ('F3_2', '301'), ('301', '302'), ('F3_2', 'F3_3'),
    ('F3_3', '306'), ('306', '303'), ('303', '305'),
    ('305', '304'), ('F3_3', '308'), ('308', '307'),
    ('F3_3', 'F3_4'), ('F3_4', 'ELEVATOR_3'), ('F3_4', 'STAIRS_F3_A'),
    ('F3_4', 'F3_5'), ('F3_5', '310'), ('310', '309'),
    ('F3_5', '311'), ('311', '314'),
    ('314', '312'), ('312', '313'), ('F3_5', 'F3_6'),
    ('F3_6', '315'), ('315', '316'), ('F3_6', 'F3_7'),
    ('F3_7', '320'), ('320', '317'), ('317', '319'),
    ('319', '318'), ('F3_7', 'WC MALE (F3)'), ('WC MALE (F3)', 'STAIRS_F3_B'),
    ('STAIRS_F3_B', 'WC FEMALE (F3)'), ('WC FEMALE (F3)', 'F3_1')
]

EDGES_FLOOR_4 = [
    ('423', '422'), ('422', '424'), ('424', '421'),
    ('421', 'F4_1'), ('F4_1', 'F4_2'),
    ('F4_2', '401'), ('401', '402'), ('F4_2', 'F4_3'),
    ('F4_3', '406'), ('406', '403'), ('403', '405'),
    ('405', '404'), ('F4_3', '408'), ('408', '407'),
    ('F4_3', 'F4_4'), ('F4_4', 'ELEVATOR_4'), ('F4_4', 'STAIRS_F4_A'),
    ('F4_4', 'F4_5'), ('F4_5', '410'), ('410', '409'),
    ('F4_5', '411'), ('411', '414'),
    ('414', '412'), ('412', '413'), ('F4_5', 'F4_6'),
    ('F4_6', '415'), ('415', '416'), ('F4_6', 'F4_7'),
    ('F4_7', '420'), ('420', '417'), ('417', '419'),
    ('419', '418'), ('F4_7', 'WC MALE (F4)'), ('WC MALE (F4)', 'STAIRS_F4_B'),
    ('STAIRS_F4_B', 'WC FEMALE (F4)'), ('WC FEMALE (F4)', 'F4_1')
]

EDGES_FLOOR_5 = [
    ('501', '502'), ('501', 'F5_5'), ('F5_5', 'ELEVATOR_5'),
    ('502', 'F5_5'), ('F5_5', 'STAIRS_F5_A'), ('F5_5', 'F5_4'),
    ('F5_4', '503'), ('F5_4', '504'), ('504', '507'),
    ('507', '505'), ('505', '506'), ('F5_4', 'F5_3'),
    ('F5_3', '508'), ('508', '509'), ('F5_3', 'F5_2'),
    ('F5_2', '513'), ('513', '510'), ('510', '512'),
    ('512', '511'), ('F5_2', 'WC MALE (F5)'),
    ('WC MALE (F5)', 'F5_1'), ('F5_1', 'WC FEMALE (F5)'),
    ('F5_1', 'STAIRS_F5_B'), ('WC FEMALE (F5)', '514'), ('514', '516'),
    ('516', '515')
]

# ============================================================================
# CUSTOM CSS STYLES
# ============================================================================

CUSTOM_CSS = """
<style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    
    body {
        font-family: 'Inter', sans-serif !important;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        min-height: 100vh;
    }
    
    /* Glass Card Effect */
    .glass-card {
        background: rgba(255, 255, 255, 0.95) !important;
        backdrop-filter: blur(10px) !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1) !important;
        border-radius: 16px !important;
    }
    
    /* Elevator Status Card */
    .elevator-card {
        background: linear-gradient(135deg, #ffecd2 0%, #fcb69f 100%) !important;
        border: 2px solid #f5af19 !important;
        box-shadow: 0 4px 15px rgba(245, 175, 25, 0.3) !important;
        border-radius: 12px !important;
        transition: transform 0.3s ease, box-shadow 0.3s ease !important;
    }
    
    .elevator-card:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 20px rgba(245, 175, 25, 0.4) !important;
    }
    
    /* Primary Button */
    .btn-primary {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 12px !important;
        font-weight: 600 !important;
        text-transform: none !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4) !important;
    }
    
    .btn-primary:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.5) !important;
    }
    
    /* Back Button */
    .btn-back {
        background: linear-gradient(135deg, #4a5568 0%, #2d3748 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 10px !important;
        font-weight: 500 !important;
        text-transform: none !important;
        transition: all 0.3s ease !important;
    }
    
    .btn-back:hover {
        transform: translateX(-3px) !important;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2) !important;
    }
    
    /* Campus Button */
    .btn-campus {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 12px !important;
        font-weight: 700 !important;
        text-transform: none !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 15px rgba(245, 87, 108, 0.4) !important;
    }
    
    .btn-campus:hover {
        transform: scale(1.02) !important;
        box-shadow: 0 6px 20px rgba(245, 87, 108, 0.5) !important;
    }
    
    /* Selection Cards */
    .selection-card {
        background: linear-gradient(180deg, #f8fafc 0%, #e2e8f0 100%) !important;
        border: 2px solid #e2e8f0 !important;
        border-radius: 16px !important;
        transition: all 0.3s ease !important;
    }
    
    .selection-card:hover {
        border-color: #667eea !important;
        box-shadow: 0 4px 12px rgba(102, 126, 234, 0.2) !important;
    }
    
    /* Legend Card */
    .legend-card {
        background: rgba(255, 255, 255, 0.9) !important;
        border: 1px solid #e2e8f0 !important;
        border-radius: 12px !important;
    }
    
    /* Map Container */
    .map-container {
        background: rgba(255, 255, 255, 0.95) !important;
        border-radius: 16px !important;
        padding: 20px !important;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08) !important;
    }
    
    /* Floor Label */
    .floor-label-start {
        background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%) !important;
        color: white !important;
        padding: 8px 20px !important;
        border-radius: 20px !important;
        font-weight: 600 !important;
    }
    
    .floor-label-end {
        background: linear-gradient(135deg, #eb3349 0%, #f45c43 100%) !important;
        color: white !important;
        padding: 8px 20px !important;
        border-radius: 20px !important;
        font-weight: 600 !important;
    }
    
    /* Title */
    .main-title {
        background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-weight: 700 !important;
    }
    
    /* Image Styling */
    .map-image {
        border-radius: 12px !important;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1) !important;
        transition: transform 0.3s ease !important;
    }
    
    .map-image:hover {
        transform: scale(1.02) !important;
    }
    
    /* Select Styling */
    .q-field--outlined .q-field__control {
        border-radius: 10px !important;
    }
    
    /* Animation */
    @keyframes float {
        0%, 100% { transform: translateY(0px); }
        50% { transform: translateY(-5px); }
    }
    
    .floating {
        animation: float 3s ease-in-out infinite;
    }
    
    @keyframes pulse-glow {
        0%, 100% { box-shadow: 0 0 5px rgba(245, 87, 108, 0.5); }
        50% { box-shadow: 0 0 20px rgba(245, 87, 108, 0.8); }
    }
    
    .pulse-glow {
        animation: pulse-glow 2s ease-in-out infinite;
    }
</style>
"""

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

count = 0


def calculate_distance(p1, p2):
    """Tính khoảng cách Euclidean giữa 2 điểm."""
    return ((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2) ** 0.5


def build_graph():
    """Xây dựng đồ thị từ các tầng."""
    G = nx.Graph()
    
    # Thêm edges cho từng tầng
    floor_edges = [
        (EDGES_FLOOR_1, FLOOR_1_LOCATIONS),
        (EDGES_FLOOR_2, FLOOR_2_LOCATIONS),
        (EDGES_FLOOR_3, FLOOR_3_LOCATIONS),
        (EDGES_FLOOR_4, FLOOR_4_LOCATIONS),
        (EDGES_FLOOR_5, FLOOR_5_LOCATIONS),
    ]
    
    for edges, locations in floor_edges:
        for u, v in edges:
            if u in locations and v in locations:
                weight = calculate_distance(locations[u], locations[v])
                G.add_edge(u, v, weight=weight, type='walk')
    
    # Nối trục dọc (cầu thang + thang máy)
    for i in range(1, 5):
        G.add_edge(f"STAIRS_F{i}_A", f"STAIRS_F{i+1}_A", weight=50, type='stair')
        G.add_edge(f"STAIRS_F{i}_B", f"STAIRS_F{i+1}_B", weight=50, type='stair')
        # G.add_edge(f"ELEVATOR_{i}", f"ELEVATOR_{i+1}", weight=10, type='elevator')
    
    return G


def draw_dashed_line(draw, p1, p2, dash_len=20, gap_len=15, fill="red", width=10):
    """Vẽ đường nét đứt giữa 2 điểm."""
    x1, y1 = p1
    x2, y2 = p2
    
    dx = x2 - x1
    dy = y2 - y1
    dist = math.hypot(dx, dy)
    
    if dist == 0:
        return
    
    vx = dx / dist
    vy = dy / dist
    
    pos = 0
    while pos < dist:
        start = pos
        end = min(pos + dash_len, dist)
        
        sx = x1 + vx * start
        sy = y1 + vy * start
        ex = x1 + vx * end
        ey = y1 + vy * end
        
        draw.line([(sx, sy), (ex, ey)], fill=fill, width=width)
        pos += dash_len + gap_len


def draw_path_on_floor(path, floor_name):
    """Vẽ đường đi lên bản đồ tầng."""
    try:
        img = Image.open(FLOOR_PLANS[floor_name]).convert("RGB")
        draw = ImageDraw.Draw(img)
        coord = ALL_FLOORS[floor_name]
        
        nodes_on_floor = [n for n in path if n in coord]
        
        # Vẽ đường nối
        for i in range(len(path) - 1):
            u, v = path[i], path[i + 1]
            if u in coord and v in coord:
                draw_dashed_line(
                    draw, coord[u], coord[v],
                    dash_len=25, gap_len=15,
                    fill="#FF4757", width=12
                )
        
        # Vẽ các điểm quan trọng
        for node in nodes_on_floor:
            x, y = coord[node]
            
            is_start = (node == path[0])
            is_end = (node == path[-1])
            # is_stair = "STAIRS" in node
            # is_elev = "ELEVATOR" in node
            
            if is_start or is_end:
                # Chọn màu và kích thước
                if is_start:
                    fill_color = "#2ED573"  # Xanh lá sáng
                    text_label = ""
                    size = 19
                    outline_color = "#1e8449"
                elif is_end:
                    fill_color = "#FF4757"  # Đỏ sáng
                    text_label = ""
                    size = 19
                    outline_color = "#c0392b"
                # elif is_elev:
                #     fill_color = "#9B59B6"  # Tím
                #     text_label = node
                #     size = 18
                #     outline_color = "#6c3483"
                # else:
                #     fill_color = "#F39C12"  # Cam
                #     text_label = node
                #     size = 18
                #     outline_color = "#d68910"
                
                # Vẽ shadow
                draw.ellipse(
                    (x - size + 3, y - size + 3, x + size + 3, y + size + 3),
                    fill="#00000040"
                )
                
                # Vẽ chấm tròn
                draw.ellipse(
                    (x - size, y - size, x + size, y + size),
                    fill=fill_color, outline="white", width=4
                )
                
                # Vẽ text
                if text_label:
                    draw.text(
                        (x - 80, y - 55), text_label,
                        fill="black", font_size=28,
                        stroke_width=3, stroke_fill="white"
                    )
        
        buf = io.BytesIO()
        img.save(buf, format="PNG")
        return f"data:image/png;base64,{base64.b64encode(buf.getvalue()).decode('utf-8')}"
    
    except Exception as e:
        print(f"Error drawing path: {e}")
        return ""


# ============================================================================
# PAGE DEFINITIONS
# ============================================================================

@ui.page('/campus')
def campus_page():
    """Trang bản đồ Campus."""
    ui.add_head_html(CUSTOM_CSS)
    
    with ui.column().classes('w-full min-h-screen items-center justify-center p-8'):
        with ui.card().classes('glass-card p-8 text-center'):
            ui.label("🗺️ BẢN ĐỒ KHUÔN VIÊN CAMPUS").classes(
                'text-3xl font-bold main-title mb-4'
            )
            ui.label("Đang phát triển...").classes('text-gray-500 mb-6')
            ui.button(
                "⬅ Quay lại Tòa nhà",
                on_click=lambda: ui.navigate.to('/')
            ).classes('btn-primary')


def create_page():
    """Trang chính - Bản đồ tòa Beta."""
    global count
    
    # Inject CSS
    ui.add_head_html(CUSTOM_CSS)
    
    # Build graph
    G = build_graph()
    
    # State
    elevator_state = {'current_floor': 'Floor 1'}
    floor_list = list(ROOMS_DATABASE.keys())
    
    # ========== HEADER ==========
    with ui.column().classes('w-full p-2 gap-2'):
        
        # Elevator Status Card (Fixed position)
        # with ui.card().classes(
        #     'fixed top-2 right-2 z-50 elevator-card p-2 floating'
        # ):
        #     with ui.row().classes('items-center gap-2'):
        #         ui.label('🛗').classes('text-lg')
        #         with ui.column().classes('gap-0'):
        #             ui.label('Thang máy:').classes(
        #                 'text-[10px] text-gray-600 font-medium'
        #             )
        #             lbl_elev_floor = ui.label(
        #                 elevator_state['current_floor']
        #             ).classes('font-bold text-orange-700 text-sm')
        
        # Back Button & Title
        with ui.row().classes('w-full items-center gap-2'):
            ui.button(
                "⬅ Menu",
                on_click=lambda: ui.navigate.to('/')
            ).classes('btn-back text-xs py-1 px-2')
            
            ui.label("🏢 TÒA BETA").classes(
                'text-base font-bold main-title'
            )
        
        # ========== SELECTION PANEL ==========
        with ui.card().classes('w-full glass-card p-3'):
            with ui.row().classes('w-full gap-2 justify-center items-start flex-nowrap'):
                
                # Start Point Selection
                with ui.card().classes('selection-card p-2 flex-1 min-w-0'):
                    with ui.column().classes('items-center gap-1'):
                        ui.label("📍 ĐI").classes(
                            'font-bold text-xs'
                        ).style('color: #11998e;')
                        
                        s_floor = ui.select(
                            floor_list, value="Floor 1", label="Tầng"
                        ).classes('w-full').props(
                            'outlined dense options-dense '
                            'popup-content-class="text-xs"'
                        ).style('font-size: 11px;')

                        s_room = ui.select(
                            options={k: display_name(k) for k in ROOMS_DATABASE["Floor 1"]},
                            value="EXTRA FRONT",
                            label="Phòng"
                        ).classes('w-full').props(
                            'outlined dense options-dense '
                            'popup-content-class="text-xs"'
                        ).style('font-size: 11px;')
                
                # End Point Selection
                with ui.card().classes('selection-card p-2 flex-1 min-w-0'):
                    with ui.column().classes('items-center gap-1'):
                        ui.label("🏁 ĐẾN").classes(
                            'font-bold text-xs'
                        ).style('color: #eb3349;')
                        
                        e_floor = ui.select(
                            floor_list, value="Floor 1", label="Tầng"
                        ).classes('w-full').props(
                            'outlined dense options-dense '
                            'popup-content-class="text-xs"'
                        ).style('font-size: 11px;')

                        e_room = ui.select(
                            options={k: display_name(k) for k in ROOMS_DATABASE["Floor 1"]},
                            value="EXTRA FRONT",
                            label="Phòng"
                        ).classes('w-full').props(
                            'outlined dense options-dense '
                            'popup-content-class="text-xs"'
                        ).style('font-size: 11px;')

        # ========== CAMPUS BUTTON ==========
        ui.button(
            "🌍 RA KHỎI TÒA NHÀ",
            on_click=lambda: ui.navigate.to('/campus')
        ).classes('w-full btn-campus text-xs py-2 pulse-glow')
        
        # ========== LEGEND ==========
        with ui.card().classes('legend-card p-2 w-full'):
            ui.label("📝 Chú thích").classes('font-bold text-gray-700 mb-1 text-xs')
            
            with ui.row().classes('gap-3 flex-wrap'):
                with ui.row().classes('items-center gap-1'):
                    ui.element('div').classes(
                        'w-3 h-3 rounded-full'
                    ).style('background: linear-gradient(135deg, #11998e, #38ef7d);')
                    ui.label("Đi").classes('text-[10px] font-medium')
                
                with ui.row().classes('items-center gap-1'):
                    ui.element('div').classes(
                        'w-3 h-3 rounded-full'
                    ).style('background: linear-gradient(135deg, #eb3349, #f45c43);')
                    ui.label("Đến").classes('text-[10px] font-medium')
                
                # with ui.row().classes('items-center gap-1'):
                #     ui.element('div').classes(
                #         'w-3 h-3 rounded-full bg-orange-500'
                #     )
                #     ui.label("Thang bộ").classes('text-[10px] font-medium')
                #
                # with ui.row().classes('items-center gap-1'):
                #     ui.element('div').classes(
                #         'w-3 h-3 rounded-full bg-purple-500'
                #     )
                #     ui.label("Thang máy").classes('text-[10px] font-medium')
        
        # ========== MAP DISPLAY ==========
        image_container = ui.column().classes(
            'w-full items-center gap-2 mt-2 map-container'
        )
    
    # ========== LOGIC FUNCTIONS ==========
    
    # def random_route():
    #     """Random vị trí thang máy."""
    #     elevator_state['current_floor'] = random.choice(floor_list)
    #     lbl_elev_floor.text = elevator_state['current_floor']
    #     ui.notify(
    #         f"🛗 Thang máy đã di chuyển đến {elevator_state['current_floor']}",
    #         type='positive',
    #         position='top-right'
    #     )
    
    def calculate_time(path, graph_source):
        """Tính thời gian di chuyển."""
        time = 0
        floors_vertical = 0
        used_elevator = False
        
        for i in range(len(path) - 1):
            u, v = path[i], path[i + 1]
            edge = graph_source.get_edge_data(u, v)
            etype = edge.get('type', 'walk')
            dist = edge.get('weight', 0)
            
            if etype == 'walk':
                time += dist / 150
            elif etype == 'stair':
                time += 20
            elif etype == 'elevator':
                """ penaty thang máy"""
                time += 10000
                # floors_vertical += 1
                # used_elevator = True
        
        # if used_elevator and floors_vertical > 0:
        #     elev_f_num = int(elevator_state['current_floor'].split()[-1])
        #     user_f_num = int(s_floor.value.split()[-1])
        #     wait_time = (abs(elev_f_num - user_f_num) * 5) + 10
        #     time += (floors_vertical * 5) + wait_time

        return time
    
    def update():
        """Cập nhật bản đồ khi thay đổi lựa chọn."""
        global count
        
        if not s_room.value or not e_room.value:
            return
        
        start, end = s_room.value, e_room.value
        
        try:
            # Tính đường đi bằng thang bộ
            G_stair = G.copy()
            G_stair.remove_edges_from([
                (u, v) for u, v, d in G.edges(data=True)
                if d.get('type') == 'elevator'
            ])
            try:
                p_stair = nx.shortest_path(G_stair, start, end, weight='weight')
                # t_stair = calculate_time(p_stair, G_stair)
            except Exception:
                G_stair.remove_edges_from([
    (u, v) for u, v, d in G.edges(data=True)
    if d.get('type') == 'elevator'
])

                p_stair = None
                t_stair = float('inf')
            
            # Tính đường đi bằng thang máy
            # G_elev = G.copy()
            # G_elev.remove_edges_from([
            #     (u, v) for u, v, d in G.edges(data=True)
            #     if d.get('type') == 'stair'
            # ])
            # try:
            #     p_elev = nx.shortest_path(G_elev, start, end, weight='weight')
            #     t_elev = calculate_time(p_elev, G_elev)
            # except Exception:
            #     p_elev = None
            #     t_elev = float('inf')
            
            # Chọn đường đi tối ưu
            # final_path = p_elev if t_elev < t_stair else p_stair
            final_path = p_stair
            # Random thang máy sau mỗi 5 lần
            # if count == 4:
            #     count = 0
            #     random_route()
            # else:
            #     count += 1
            
            # Hiển thị bản đồ
            image_container.clear()
            
            if final_path:
                with image_container:
                    if s_floor.value == e_floor.value:
                        # Cùng tầng
                        with ui.column().classes('items-center w-full'):
                            ui.label(f"📍 {s_floor.value}").classes(
                                'floor-label-start mb-2 text-xs py-1 px-3'
                            )
                            ui.image(
                                draw_path_on_floor(final_path, s_floor.value)
                            ).classes('map-image w-full').style('max-width: 100%; width: 100%;')
                    else:
                        # Khác tầng
                        with ui.column().classes('items-center w-full'):
                            ui.label(f"📍 Đi: {s_floor.value}").classes(
                                'floor-label-start mb-2 text-xs py-1 px-3'
                            )
                            ui.image(
                                draw_path_on_floor(final_path, s_floor.value)
                            ).classes('map-image w-full').style('max-width: 100%; width: 100%;')
                        
                        with ui.column().classes('items-center w-full mt-2'):
                            ui.label(f"🏁 Đến: {e_floor.value}").classes(
                                'floor-label-end mb-2 text-xs py-1 px-3'
                            )
                            ui.image(
                                draw_path_on_floor(final_path, e_floor.value)
                            ).classes('map-image w-full').style('max-width: 100%; width: 100%;')
        
        except Exception as e:
            ui.notify(f"⚠️ Lỗi: {str(e)}", type='negative')
    
    def update_start_rooms():
        """Cập nhật danh sách phòng khi đổi tầng đi."""
        s_room.options = {
            k: display_name(k) for k in ROOMS_DATABASE[s_floor.value]
        }
        s_room.value = list(s_room.options.keys())[0]
        update()
    
    def update_end_rooms():
        """Cập nhật danh sách phòng khi đổi tầng đến."""
        e_room.options = {
            k: display_name(k) for k in ROOMS_DATABASE[e_floor.value]
        }
        e_room.value = list(e_room.options.keys())[0]
        update()
    
    # Event bindings
    s_floor.on_value_change(update_start_rooms)
    e_floor.on_value_change(update_end_rooms)
    s_room.on_value_change(update)
    e_room.on_value_change(update)
    
    # Initial render
    update()