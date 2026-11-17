"""参数化设施图块库：DXF BLOCK + INSERT + PNG 同源图形，图例与块名一一对应。

图块只表达“设施类型”，不表达厂家尺寸。所有图块以 1000×1000 为基准
（坐标 -500..500），插入时按设施建议尺寸缩放；真实尺寸由项目确认后覆盖。

图形用纯 Python 图元描述（line/poly/rect/circle/arc/text），由本模块同时
渲染到 DXF 图块和 PNG 像素图，保证图面、图例、PNG 三处图形一致：

- 塔吊 `SLP_CRANE`：基础节、标准节、附着撑杆、回转总成、驾驶室、分节起重臂、
  小车、双倍率吊钩、平衡臂配重、塔尖拉杆与幅度标注线。
- 施工电梯 `SLP_ELEV`：底座、双导轨、腹杆、附墙架、层门、吊笼门、电缆滑车、
  地面围栏与防护棚。
- 地磅 `SLP_WEIGHBRIDGE`：分节秤台、称重传感器、限位挡块、两端引坡与坡度箭头、
  称重房和行车方向。
- 洗车台 `SLP_WASH`：洗车平台、引坡、喷淋拱、三级沉淀池（1/2/3）、排水沟和减速带。
- 办公区 `SLP_OFFICE`：两层箱房排、外走廊、楼梯、停车位、旗杆和宣传栏。
- 员工宿舍 `SLP_STAFFDORM`：箱房排、空调外机、晾晒区和疏散楼梯。
- 工人生活区 `SLP_LIVING`：宿舍排、食堂、淋浴/厕所、晾晒区和活动场，分区虚线。

图元全部自绘，不复制第三方图块；若改用开源图块，必须在
`references/draw.md` 记录来源 URL、许可证、版本与 SHA-256。
"""
from __future__ import annotations

import math
from typing import Any, Dict, Iterable, List, Optional, Sequence, Tuple

BASE = 1000.0

SYMBOLS: Dict[str, Dict[str, Any]] = {
    "site_access": {"block": "SLP_GATE", "size_mm": 6000.0, "zh": "大门"},
    "construction_elevator": {"block": "SLP_ELEV", "size_mm": 7000.0, "zh": "施工电梯", "layer": "FAC-施工电梯", "stages": ("structure", "finish"), "showcase": "elev", "note": "底座/双导轨/腹杆/附墙架/层门/吊笼门/电缆滑车/围栏/防护棚"},
    "tower_crane": {"block": "SLP_CRANE", "size_mm": 12000.0, "zh": "塔吊", "layer": "CRANE-塔吊", "stages": ("structure",), "showcase": "crane", "note": "基础节/标准节/附着/回转/驾驶室/分节起重臂/小车/双倍率吊钩/平衡重/幅度线"},
    "fire_hydrant": {"block": "SLP_HYDRANT", "size_mm": 1600.0, "zh": "消火栓"},
    "distribution_room": {"block": "SLP_POWER", "size_mm": 5000.0, "zh": "配电室"},
    "primary_distribution_box": {"block": "SLP_BOX", "size_mm": 2200.0, "zh": "一级箱"},
    "processing_zone": {"block": "SLP_PROCESS", "size_mm": 8000.0, "zh": "加工区"},
    "steel_processing": {"block": "SLP_STEEL", "size_mm": 8000.0, "zh": "钢筋加工"},
    "wood_processing": {"block": "SLP_WOOD", "size_mm": 7000.0, "zh": "木工加工"},
    "mortar_processing": {"block": "SLP_MORTAR", "size_mm": 6000.0, "zh": "砂浆加工"},
    "material_yard": {"block": "SLP_MATERIAL", "size_mm": 7000.0, "zh": "材料堆场"},
    "transformer": {"block": "SLP_TRANSFORMER", "size_mm": 4500.0, "zh": "变压器"},
    "fire_pump_room": {"block": "SLP_FIREPUMP", "size_mm": 5000.0, "zh": "消防泵房"},
    "fire_water_tank": {"block": "SLP_FIRETANK", "size_mm": 6000.0, "zh": "消防水池"},
    "drainage_ditch": {"block": "SLP_DITCH", "size_mm": 3000.0, "zh": "排水沟"},
    "temporary_dormitory": {"block": "SLP_DORM", "size_mm": 7000.0, "zh": "宿舍"},
    "staff_dormitory": {"block": "SLP_STAFFDORM", "size_mm": 7000.0, "zh": "员工宿舍区", "layer": "FAC-员工宿舍", "stages": ("earthwork", "structure", "finish"), "showcase": "dorm", "note": "箱房排/空调外机/床位/晾晒/两端疏散楼梯"},
    "worker_living_zone": {"block": "SLP_LIVING", "size_mm": 9000.0, "zh": "工人生活区", "layer": "FAC-工人生活区", "stages": ("earthwork", "structure", "finish"), "showcase": "living", "note": "宿舍/食堂/淋浴厕所/晾晒/活动场，虚线分区"},
    "canteen": {"block": "SLP_CANTEEN", "size_mm": 6000.0, "zh": "食堂"},
    "toilet_shower": {"block": "SLP_TOILET", "size_mm": 4500.0, "zh": "卫生间/淋浴"},
    "drying_area": {"block": "SLP_DRYING", "size_mm": 5000.0, "zh": "晾晒区"},
    "site_office": {"block": "SLP_OFFICE", "size_mm": 7000.0, "zh": "办公区", "layer": "FAC-办公区", "stages": ("earthwork", "structure", "finish"), "showcase": "office", "note": "两层箱房排/外走廊/楼梯/停车位/旗杆/宣传栏"},
    "parking": {"block": "SLP_PARK", "size_mm": 6000.0, "zh": "停车场"},
    "notice_board": {"block": "SLP_NOTICE", "size_mm": 3000.0, "zh": "九牌一图"},
    "safety_podium": {"block": "SLP_PODIUM", "size_mm": 4000.0, "zh": "宣讲台"},
    "waste_pool": {"block": "SLP_WASTE", "size_mm": 3500.0, "zh": "垃圾池"},
    "wheel_wash": {"block": "SLP_WASH", "size_mm": 4000.0, "zh": "洗车台", "layer": "FAC-洗车池", "stages": ("earthwork", "structure", "finish"), "showcase": "wash", "note": "洗车平台/引坡/喷淋拱/三级沉淀池1-2-3/排水沟/减速带"},
    "weighbridge": {"block": "SLP_WEIGHBRIDGE", "size_mm": 12000.0, "zh": "地磅", "layer": "FAC-地磅", "stages": ("earthwork", "structure", "finish"), "showcase": "weighbridge", "note": "分节秤台/传感器/限位挡块/引坡坡度/称重房/行车方向"},
    "temporary_building": {"block": "SLP_TEMP", "size_mm": 5000.0, "zh": "临建"},
    "site_boundary_neighbor": {"block": "SLP_NEIGHBOR", "size_mm": 3000.0, "zh": "相邻地貌"},
}


def block_name(category: str) -> Optional[str]:
    item = SYMBOLS.get(category)
    return item["block"] if item else None


def symbol_size(category: str) -> float:
    return float(SYMBOLS.get(category, {}).get("size_mm") or 3000.0)


def _rect(x0: float, y0: float, x1: float, y1: float) -> Tuple:
    return ("poly", [(x0, y0), (x1, y0), (x1, y1), (x0, y1)], True)


def _text(value: str, height: float = 230.0, x: float = 0.0, y: float = -115.0) -> Tuple:
    return ("text", value, height, x, y)


def _dash_line(x0: float, y0: float, x1: float, y1: float,
               dash: float = 26.0, gap: float = 16.0) -> List[Tuple]:
    """把虚线拆成短线段，DXF 与 PNG 都按普通 line 绘制，不新增图元类型。"""
    dx, dy = x1 - x0, y1 - y0
    length = math.hypot(dx, dy)
    if length <= 0:
        return []
    ux, uy = dx / length, dy / length
    out: List[Tuple] = []
    pos = 0.0
    while pos < length - 1e-6:
        end = min(pos + dash, length)
        out.append(("line", x0 + ux * pos, y0 + uy * pos,
                    x0 + ux * end, y0 + uy * end))
        pos = end + gap
    return out


def _dashed_rect(x0: float, y0: float, x1: float, y1: float,
                 dash: float = 24.0, gap: float = 14.0) -> List[Tuple]:
    return (_dash_line(x0, y0, x1, y0, dash, gap)
            + _dash_line(x1, y0, x1, y1, dash, gap)
            + _dash_line(x1, y1, x0, y1, dash, gap)
            + _dash_line(x0, y1, x0, y0, dash, gap))


def _arrow(x0: float, y0: float, x1: float, y1: float,
           head: float = 28.0) -> List[Tuple]:
    dx, dy = x1 - x0, y1 - y0
    angle = math.atan2(dy, dx)
    left = (x1 - head * math.cos(angle - 0.46), y1 - head * math.sin(angle - 0.46))
    right = (x1 - head * math.cos(angle + 0.46), y1 - head * math.sin(angle + 0.46))
    return [("line", x0, y0, x1, y1),
            ("poly", [(x1, y1), left, right], True)]


def _numeral(value: int, x: float, y: float, height: float = 60.0) -> List[Tuple]:
    """用线段画 1/2/3，保证 DXF 和 PNG 都能看到沉淀池编号。"""
    width = height * 0.52
    top, mid, bot = y + height, y + height / 2.0, y
    right = x + width
    if value == 1:
        return [("line", right, top, right, bot)]
    if value == 2:
        return [("line", x, top, right, top), ("line", right, top, right, mid),
                ("line", x, mid, right, mid), ("line", x, mid, x, bot),
                ("line", x, bot, right, bot)]
    return [("line", x, top, right, top), ("line", right, top, right, bot),
            ("line", x, mid, right, mid), ("line", x, bot, right, bot)]


def _fan_unit(x: float, y: float, w: float = 74.0, h: float = 34.0) -> List[Tuple]:
    """空调外机：机身 + 风扇圆 + 风叶线。"""
    cx, cy = x + w / 2.0, y + h / 2.0
    radius = min(w, h) * 0.30
    return [_rect(x, y, x + w, y + h),
            ("circle", cx, cy, radius),
            ("line", cx, cy - radius, cx, cy + radius),
            ("line", cx - radius, cy, cx + radius, cy)]


def _stairs(x0: float, y0: float, x1: float, y1: float,
            steps: int = 6) -> List[Tuple]:
    """平面楼梯：外框 + 踏步线 + 上行箭头。"""
    prims: List[Tuple] = [_rect(x0, y0, x1, y1)]
    for index in range(1, steps):
        yy = y0 + (y1 - y0) * index / steps
        prims.append(("line", x0, yy, x1, yy))
    prims.append(("line", (x0 + x1) / 2.0, y0 + 8, (x0 + x1) / 2.0, y1 - 8))
    prims.extend(_arrow((x0 + x1) / 2.0, y0 + 14, (x0 + x1) / 2.0, y1 - 14, 22))
    return prims


def _container_row(x0: float, y0: float, x1: float, y1: float,
                   modules: int = 5) -> List[Tuple]:
    """箱房排：外框 + 等分房间线 + 每间门洞短划。"""
    prims: List[Tuple] = [_rect(x0, y0, x1, y1)]
    width = (x1 - x0) / modules
    for index in range(1, modules):
        xx = x0 + width * index
        prims.append(("line", xx, y0, xx, y1))
    for index in range(modules):
        cx = x0 + width * (index + 0.5)
        prims.append(("line", cx - 12, y0, cx + 12, y0))
        prims.append(("line", cx - 10, y1, cx + 10, y1))
    return prims


def _bed(x: float, y: float, w: float = 52.0, h: float = 40.0) -> List[Tuple]:
    """宿舍床位：床框 + 枕头 + 被面折线。"""
    return [_rect(x, y, x + w, y + h),
            ("line", x + 7, y + h - 9, x + 20, y + h - 9),
            ("line", x + 10, y + 6, x + w - 8, y + 15)]


def _crane() -> List[Tuple]:
    """塔吊类型示意：基础节、标准节、附着、回转、驾驶室、分节起重臂、
    小车、双倍率吊钩、平衡臂配重、塔尖拉杆与幅度标注线。"""
    prims: List[Tuple] = [
        # 混凝土基础与基础节
        ("solid", [(-185, -370), (185, -370), (185, -330), (-185, -330)]),
        ("line", -185, -330, 185, -330),
        ("line", -120, -330, -120, -250),
        ("line", 120, -330, 120, -250),
        ("line", -120, -330, 120, -250),
        ("line", 120, -330, -120, -250),
        ("line", -120, -250, 120, -250),
        # 标准节塔身：双弦杆 + 水平系杆 + 交叉腹杆
        ("line", -82, -250, -82, 150),
        ("line", 82, -250, 82, 150),
        ("line", -82, -250, 82, 150),
        ("line", -82, 150, 82, -250),
        # 回转总成：外圈 + 齿圈刻线
        ("circle", 0, 150, 50),
        ("circle", 0, 150, 34),
        # 驾驶室
        _rect(86, -30, 214, 90),
        ("solid", [(100, -16), (200, -16), (200, 76), (100, 76)]),
        ("line", 100, 68, 200, 68),
        ("line", 150, -16, 150, 76),
        # 塔尖与拉杆（两组，表达四根拉杆）
        ("line", 0, 150, 0, 330),
        ("line", 0, 330, 360, 55),
        ("line", 0, 330, -330, 55),
        ("line", 0, 330, 250, 39),
        ("line", 0, 330, -250, 31),
        # 起重臂上下弦与端部
        ("line", 82, 62, 500, 26),
        ("line", 82, -18, 500, -8),
        ("line", 500, 26, 500, -8),
        # 平衡臂上下弦
        ("line", -82, 62, -390, 32),
        ("line", -82, -18, -390, -20),
        ("line", -390, 32, -390, -20),
        # 平衡重：外框 + 填实 + 分块
        _rect(-472, -95, -392, 95),
        ("solid", [(-458, -78), (-406, -78), (-406, 78), (-458, 78)]),
        ("line", -444, -78, -444, 78),
        ("line", -428, -78, -428, 78),
        ("line", -472, -95, -472, 95),
        ("line", -472, 0, -392, 0),
        # 小车与双倍率吊钩
        _rect(306, -24, 372, 8),
        ("circle", 322, -8, 9),
        ("circle", 356, -8, 9),
        ("line", 334, -24, 340, -188),
        ("line", 352, -24, 346, -180),
        ("circle", 344, -190, 16),
        ("line", 328, -204, 360, -204),
        ("poly", [(344, -206), (330, -218), (322, -238), (332, -256),
                  (352, -254), (360, -238), (352, -224)], False),
        _text("塔", 150, 250, -335),
        # 附着撑杆：塔身到结构侧，端部带连接板
        ("line", 82, 60, 320, 130),
        ("line", 82, -10, 320, 60),
        ("line", 320, 48, 320, 142),
        ("line", 308, 130, 332, 130),
        ("line", 308, 60, 332, 60),
    ]
    # 标准节水平系杆与交叉腹杆
    for y in (-230, -170, -110, -50, 10, 70, 130):
        prims.append(("line", -82, y, 82, y))
    for y0 in (-250, -190, -130, -70, -10, 50, 110):
        prims.append(("line", -82, y0, 82, y0 + 60))
    # 起重臂分节竖杆与 X 形腹杆
    xs = (82, 150, 230, 310, 390, 460, 500)
    tops = [62 - 36 * (x - 82) / 418.0 for x in xs]
    bots = [-18 + 10 * (x - 82) / 418.0 for x in xs]
    for index in range(1, len(xs) - 1):
        prims.append(("line", xs[index], bots[index], xs[index], tops[index]))
    for index in range(len(xs) - 1):
        prims.append(("line", xs[index], tops[index], xs[index + 1], bots[index + 1]))
        prims.append(("line", xs[index], bots[index], xs[index + 1], tops[index + 1]))
    # 平衡臂栏杆
    for x0 in (-120, -175, -230, -285, -340):
        prims.append(("line", x0, 42, x0, -30))
    # 幅度标注线：起重臂端到回转中心
    prims.extend(_dash_line(500, 14, 500, -420, 24, 14))
    prims += [
        ("line", 0, -445, 500, -445),
        ("line", 0, -470, 0, -420),
        ("line", 500, -470, 500, -420),
        ("poly", [(500, -445), (482, -433), (482, -457)], True),
        ("poly", [(0, -445), (18, -433), (18, -457)], True),
        _text("R", 100, 250, -430),
    ]
    return prims


def _elevator() -> List[Tuple]:
    """施工电梯类型示意：底座、双导轨、腹杆、附墙架、层门、吊笼门、
    电缆滑车、地面围栏与防护棚。"""
    prims: List[Tuple] = [
        # 底座与地脚螺栓
        ("solid", [(-215, -355), (-25, -355), (-25, -315), (-215, -315)]),
        ("line", -215, -315, -25, -315),
        ("circle", -195, -335, 7),
        ("circle", -45, -335, 7),
        # 双立柱导轨架
        ("line", -170, -315, -170, 300),
        ("line", -70, -315, -70, 300),
        # 顶部驱动/牵引轮与牵引绳
        _rect(-195, 300, -45, 338),
        ("circle", -120, 338, 20),
        ("line", -120, 338, -120, 186),
        _text("SC", 160, 220, -350),
    ]
    # 导轨腹杆与水平系杆
    for index in range(6):
        y0 = -315 + index * 102.5
        y1 = y0 + 102.5
        prims.append(("line", -170, y0, -70, y1) if index % 2 == 0 else
                     ("line", -70, y0, -170, y1))
    for y in (-270, -167.5, -65, 37.5, 140, 242.5):
        prims.append(("line", -170, y, -70, y))
    # 内侧短导靴，不增加“第三根通高导轨”
    for y0 in (-300, -120, 60, 180):
        prims.append(("line", -150, y0, -150, y0 + 80))
        prims.append(("line", -90, y0, -90, y0 + 80))
        prims.append(("line", -150, y0 + 40, -90, y0 + 40))
    # 吊笼（带门缝、吊顶、导靴）
    prims += [
        _rect(-48, -96, 112, 186),
        ("line", -48, 150, 112, 150),
        ("line", 28, -96, 28, 150),
        ("line", -48, 186, 112, 186),
        ("line", 28, 150, 28, 186),
        ("solid", [(-44, -90), (108, -90), (108, -84), (-44, -84)]),
        ("solid", [(-44, 180), (108, 180), (108, 186), (-44, 186)]),
        ("line", -170, 150, -48, 150),
        ("line", -170, -96, -48, -96),
        # 吊笼门：门扇 + 开启弧 + 把手
        ("line", 28, -90, 28, 146),
        ("arc", 28, -90, 56, 0, 82),
        ("line", 24, 40, 32, 40),
        # 停靠层（楼层线 + 端部栏杆 + 层门）
        ("line", 112, 186, 360, 186),
        ("line", 112, 60, 360, 60),
        ("line", 112, -96, 360, -96),
        ("line", 112, -250, 360, -250),
        ("line", 360, 186, 360, 60),
        ("line", 360, -96, 360, -250),
        ("line", 360, 186, 360, 210),
        ("line", 340, 210, 380, 210),
    ]
    for floor in (186, 60, -96):
        prims.append(_rect(130, floor + 12, 192, floor + 70))
        prims.append(("line", 130, floor + 41, 192, floor + 41))
    # 附墙架（三层）
    for level in (-20, 120, 250):
        prims += [
            ("line", 180, level, 330, level),
            ("line", 330, level - 24, 330, level + 24),
            ("line", 300, level, 300, level + 26),
        ]
    # 电缆滑车与电缆
    prims += [
        _rect(-8, 255, 62, 290),
        ("circle", 4, 272, 8),
        ("circle", 50, 272, 8),
        ("line", 50, 255, 50, 186),
        ("line", 50, 186, 60, 150),
    ]
    # 地面围栏与防护棚
    prims += [
        ("line", -250, -392, 170, -392),
        ("line", -250, -355, 170, -355),
    ]
    for x in (-250, -170, -90, -10, 70, 170):
        prims.append(("line", x, -392, x, -355))
    prims += [
        ("poly", [(-30, 235), (195, 235), (180, 252), (-15, 252)], True),
        ("line", -15, 186, -15, 235),
        ("line", 180, 186, 180, 235),
        ("line", -15, 186, 40, 235),
        ("line", 180, 186, 125, 235),
    ]
    return prims


def _weighbridge_block() -> List[Tuple]:
    """地磅：分节秤台、传感器、限位挡块、引坡坡度箭头、称重房、行车方向。"""
    prims: List[Tuple] = [
        # 分节秤台
        _rect(-360, -95, 360, 95),
        ("line", -240, -95, -240, 95),
        ("line", -120, -95, -120, 95),
        ("line", 0, -95, 0, 95),
        ("line", 120, -95, 120, 95),
        ("line", 240, -95, 240, 95),
        # 两端引坡
        ("poly", [(-500, -170), (-360, -95), (-360, 95), (-500, 170)], True),
        ("poly", [(360, -95), (500, -170), (500, 170), (360, 95)], True),
        ("line", -500, -170, -500, 170),
        ("line", 500, -170, 500, 170),
        # 四角称重传感器与限位挡块
    ]
    for x in (-300, 300):
        for y in (-65, 65):
            prims.append(_rect(x - 20, y - 14, x + 20, y + 14))
            prims.append(("circle", x, y, 6))
    for x in (-350, 350):
        for y in (-78, 78):
            prims.append(_rect(x - 8, y - 22, x + 8, y + 22))
    # 坡度箭头：布置在引坡两侧，避开中间行车方向线
    for y in (-120, 120):
        prims.extend(_arrow(-470, y, -390, y, 20))
        prims.extend(_arrow(470, y, 390, y, 20))
    # 行车方向箭头
    prims += [
        ("line", -320, 0, 300, 0),
        ("poly", [(320, 0), (286, 18), (286, -18)], True),
        # 称重房：门、窗、屋顶分缝
        _rect(-80, 115, 80, 270),
        ("line", -80, 160, 80, 160),
        ("line", -26, 160, -26, 270),
        ("line", 26, 160, 26, 270),
        ("line", 0, 115, 0, 160),
        ("line", -18, 224, -18, 252),
        ("line", 18, 224, 18, 252),
        _text("磅", 130, 0, -345),
    ]
    return prims


def _wash_block() -> List[Tuple]:
    """洗车台：平台、引坡、喷淋拱、三级沉淀池、排水沟、减速带。"""
    prims: List[Tuple] = [
        # 洗车平台与两端引坡
        _rect(-420, -230, 420, 200),
        ("poly", [(-500, -280), (-420, -230), (-420, 200), (-500, 250)], True),
        ("poly", [(420, -230), (500, -280), (500, 250), (420, 200)], True),
        ("line", -500, -280, -500, 250),
        ("line", 500, -280, 500, 250),
        # 轮胎轨迹
        ("line", -400, -85, 400, -85),
        ("line", -400, 45, 400, 45),
        # 喷淋拱：横跨车道的喷淋杆 + 两端立柱 + 喷嘴
        ("line", 40, -210, 40, 180),
        _rect(28, -226, 52, -194),
        _rect(28, 164, 52, 196),
    ]
    for y in (-170, -100, -30, 40, 110, 150):
        prims.append(("circle", 40, y, 7))
    # 三级沉淀池与编号 1/2/3
    prims += [
        _rect(-460, -365, -160, -265),
        _rect(-150, -365, 150, -265),
        _rect(160, -365, 460, -265),
    ]
    prims += _numeral(1, -326, -350, 65)
    prims += _numeral(2, -17, -350, 65)
    prims += _numeral(3, 292, -350, 65)
    # 排水沟与沟篦短划
    for y in (-252, 218):
        prims.append(("line", -420, y, 420, y))
        for x in range(-400, 401, 80):
            prims.append(("line", x, y - 6, x, y + 6))
    # 减速带：横跨车道的短虚线
    prims.extend(_dash_line(-330, -190, -330, 160, 22, 12))
    prims.extend(_dash_line(330, -190, 330, 160, 22, 12))
    # 单向行驶方向：入口到出口
    prims.extend(_arrow(-400, 0, 400, 0, 24))
    prims.append(_text("洗", 150, 400, 210))
    return prims


def _office_block() -> List[Tuple]:
    """办公区组合块：两层箱房排、外走廊、楼梯、停车位、旗杆、宣传栏。"""
    prims: List[Tuple] = [
        _rect(-480, -380, 480, 380),
        # 两层箱房排（上下两排 + 中间外走廊）
        *_container_row(-430, 210, 300, 320, 5),
        *_container_row(-430, 40, 300, 150, 5),
        _rect(-430, 150, 300, 210),
        ("line", -430, 180, 300, 180),
        # 外走廊栏杆短划
    ]
    for x in range(-410, 300, 60):
        prims.append(("line", x, 193, x, 207))
    # 楼梯
    prims.extend(_stairs(315, 40, 415, 210, 7))
    # 停车位与车位线
    prims += [
        _rect(-430, -350, -150, -245),
        ("line", -337, -350, -337, -245),
        ("line", -244, -350, -244, -245),
        _rect(-420, -335, -355, -270),
        _rect(-325, -335, -260, -270),
        _rect(-225, -335, -160, -270),
    ]
    # 旗杆与旗帜
    prims += [
        ("circle", 430, 300, 12),
        ("line", 430, 300, 430, 360),
        ("poly", [(430, 360), (478, 344), (430, 326)], False),
    ]
    # 宣传栏
    prims += [_rect(-430, -175, -160, -125),
              ("line", -340, -175, -340, -125),
              ("line", -250, -175, -250, -125),
              ("line", -430, -150, -160, -150)]
    prims += _numeral(2, 350, 330, 40)
    prims.append(_text("办", 190, 0, -210))
    return prims


def _staff_dorm_block() -> List[Tuple]:
    """员工宿舍组合块：箱房排、空调外机、晾晒、疏散楼梯。"""
    prims: List[Tuple] = [
        _rect(-480, -380, 480, 380),
        *_container_row(-370, 190, 300, 310, 5),
        *_container_row(-370, 20, 300, 140, 5),
        _rect(-370, 140, 300, 190),
        ("line", -370, 165, 300, 165),
    ]
    for x in range(-350, 300, 60):
        prims.append(("line", x, 147, x, 158))
    # 空调外机
    for x in (-350, -230, -110, 10, 130, 250):
        prims.extend(_fan_unit(x, 326, 76, 36))
    # 疏散楼梯（两端）
    prims.extend(_stairs(-465, 20, -385, 190, 7))
    prims.extend(_stairs(315, 20, 395, 190, 7))
    # 房间内床位
    for row_y in (215, 45):
        for x in (-350, -220, -90, 40, 170):
            prims.extend(_bed(x, row_y, 52, 40))
    # 晾晒区
    prims += [
        _rect(-370, -330, 300, -225),
        ("line", -340, -250, 270, -250),
        ("line", -340, -300, 270, -300),
        ("poly", [(-300, -250), (-300, -292), (-270, -310), (-240, -292), (-240, -250)], False),
        ("poly", [(-130, -250), (-130, -292), (-100, -310), (-70, -292), (-70, -250)], False),
        ("poly", [(40, -250), (40, -292), (70, -310), (100, -292), (100, -250)], False),
    ]
    prims.append(_text("员", 190, 0, -165))
    return prims


def _living_block() -> List[Tuple]:
    """工人生活区组合块：宿舍、食堂、淋浴/厕所、晾晒、活动场，虚线分区。"""
    prims: List[Tuple] = [_rect(-480, -360, 480, 360)]
    # 虚线分区
    prims.extend(_dash_line(-90, -360, -90, 360, 26, 16))
    prims.extend(_dash_line(-480, 90, -90, 90, 26, 16))
    prims.extend(_dash_line(-90, 210, 480, 210, 26, 16))
    prims.extend(_dash_line(-90, 90, 480, 90, 26, 16))
    # 宿舍排（左上）
    prims.extend(_container_row(-455, 240, -110, 330, 3))
    prims.extend(_container_row(-455, 140, -110, 230, 3))
    for x in (-430, -315, -200):
        prims.extend(_bed(x, 260, 44, 34))
        prims.extend(_bed(x, 160, 44, 34))
    # 食堂（左下）：餐桌椅
    prims += [_rect(-455, -330, -110, 50)]
    for cx, cy in ((-380, -240), (-280, -120), (-170, -240)):
        prims.append(("circle", cx, cy, 34))
        prims.append(("line", cx - 52, cy, cx - 22, cy))
        prims.append(("line", cx + 22, cy, cx + 52, cy))
        prims.append(("line", cx, cy - 52, cx, cy - 22))
        prims.append(("line", cx, cy + 22, cx, cy + 52))
    # 淋浴/厕所（右上）
    prims += [_rect(-60, 240, 455, 330), ("line", -60, 285, 455, 285)]
    for x in (70, 170, 270, 370):
        prims.append(("line", x, 240, x, 330))
    for x in (5, 120, 220, 320, 420):
        prims.append(("circle", x, 258, 12))
        prims.append(("line", x - 8, 272, x + 8, 258))
    # 晾晒（右中）
    for y in (125, 175):
        prims.append(("line", -50, y, 440, y))
    for x in (0, 120, 240):
        prims.append(("poly", [(x, 175), (x, 140), (x + 32, 122), (x + 64, 140), (x + 64, 175)], False))
    # 活动场（右下）：篮球场
    prims += [
        _rect(-60, -330, 455, 50),
        ("line", 198, -330, 198, 50),
        ("circle", 198, -140, 55),
        _rect(110, -210, 286, -70),
        ("circle", 198, -70, 14),
        ("line", 184, -70, 212, -70),
    ]
    prims.extend(_arrow(60, -300, 60, -20, 24))
    prims.append(_text("生", 120, -300, 40))
    return prims


def _shapes() -> Dict[str, List[Tuple]]:
    shapes: Dict[str, List[Tuple]] = {
        "SLP_GATE": [
            # 门柱（填实）+ 双扇门 + 开启方向箭头
            ("solid", [(-430, -330), (-370, -330), (-370, 330), (-430, 330)]),
            ("solid", [(370, -330), (430, -330), (430, 330), (370, 330)]),
            ("line", -370, 0, 370, 0),
            ("line", -370, 250, 0, 120),
            ("line", -370, -250, 0, -120),
            ("line", 370, 250, 0, 120),
            ("line", 370, -250, 0, -120),
            ("line", -430, 330, 430, 330),
            ("line", -430, -330, 430, -330),
            _text("门", 200, 0, -250),
        ],
        "SLP_CRANE": _crane(),
        "SLP_ELEV": _elevator(),
        "SLP_HYDRANT": [
            # 室外消火栓：底座、栓体、阀盖、双侧出水口、顶部操作杆
            ("solid", [(-95, -230), (95, -230), (95, -185), (-95, -185)]),
            _rect(-58, -185, 58, 95),
            ("solid", [(-58, -30), (58, -30), (58, 35), (-58, 35)]),
            ("poly", [(-78, 95), (78, 95), (58, 140), (-58, 140)], True),
            ("line", 0, 140, 0, 205),
            ("line", -42, 205, 42, 205),
            ("line", -58, 40, -128, 40),
            ("line", -128, 18, -128, 62),
            ("line", 58, 40, 128, 40),
            ("line", 128, 18, 128, 62),
            ("circle", 0, 60, 20),
            _text("消", 190, 0, -300),
        ],
        "SLP_POWER": [
            _rect(-480, -380, 480, 380),
            ("poly", [(70, 300), (-110, 20), (10, 20), (-70, -300), (150, -10), (30, -10)], True),
            _text("配", 180, 0, -330),
        ],
        "SLP_BOX": [
            _rect(-360, -500, 360, 500),
            ("line", -360, 250, 360, 250),
            ("line", -360, -250, 360, -250),
            ("circle", -180, 0, 55),
            ("circle", 0, 0, 55),
            ("circle", 180, 0, 55),
            _text("一", 180, 0, -400),
        ],
        "SLP_PROCESS": [
            _rect(-480, -380, 480, 380),
            ("line", -480, -380, -120, 380),
            ("line", -260, -380, 100, 380),
            ("line", -40, -380, 320, 380),
            ("line", 180, -380, 480, 300),
            _text("加", 190, 0, -110),
        ],
        "SLP_STEEL": [
            _rect(-480, -380, 480, 380),
        ] + [
            ("line", -400, y, 400, y) for y in (-220, -90, 40, 170)
        ] + [
            ("line", -400, y + 30, -400, y - 30) for y in (-220, -90, 40, 170)
        ] + [
            ("line", 400, y + 30, 400, y - 30) for y in (-220, -90, 40, 170)
        ] + [_text("钢", 190, 0, -330)],
        "SLP_WOOD": [
            _rect(-480, -380, 480, 380),
            ("circle", 0, 30, 250),
            ("circle", 0, 30, 60),
            ("line", -300, -300, 300, 300),
            _text("木", 190, 0, -330),
        ],
        "SLP_MORTAR": [
            _rect(-480, -380, 480, 380),
            ("poly", [(-260, 220), (260, 220), (180, -80), (-180, -80)], True),
            ("circle", 0, -160, 90),
            ("line", -330, 220, -330, 340),
            ("line", -330, 340, -180, 340),
            _text("砂", 190, 0, -320),
        ],
        "SLP_MATERIAL": [
            _rect(-480, -380, 480, 380),
        ] + [
            _rect(-420 + col * 220, -300 + row * 150, -300 + col * 220, -180 + row * 150)
            for row in range(4) for col in range(4)
        ] + [_text("堆", 190, 0, -420)],
        "SLP_TRANSFORMER": [
            _rect(-420, -380, 420, 380),
            ("circle", -110, 60, 180),
            ("circle", 110, 60, 180),
            ("line", -260, -240, 260, -240),
            ("line", -260, -320, 260, -320),
            _text("变", 190, 0, -400),
        ],
        "SLP_FIREPUMP": [
            _rect(-480, -380, 480, 380),
            ("circle", 0, 40, 240),
            ("line", -120, 40, 120, 40),
            ("line", 0, -80, 0, 160),
            ("arc", 0, 40, 130, 200, 340),
            _text("泵", 190, 0, -330),
        ],
        "SLP_FIRETANK": [
            _rect(-480, -380, 480, 380),
            ("line", -340, 250, 340, 250),
            ("arc", -170, 150, 170, 180, 360),
            ("arc", 170, 150, 170, 180, 360),
            ("arc", -170, 40, 170, 180, 360),
            ("arc", 170, 40, 170, 180, 360),
            _text("池", 190, 0, -330),
        ],
        "SLP_DITCH": [
            _rect(-480, -200, 480, 200),
            ("line", -480, 0, 480, 0),
            _text("沟", 170, 0, -95),
        ],
        "SLP_DORM": [
            _rect(-480, -380, 480, 380),
            ("line", -480, 100, 480, 100),
        ] + [
            ("line", x, 100, x, 380) for x in (-240, 0, 240)
        ] + [
            ("line", x, -380, x, 100) for x in (-320, -160, 0, 160, 320)
        ] + [_text("宿", 190, 0, -140)],
        "SLP_STAFFDORM": _staff_dorm_block(),
        "SLP_LIVING": _living_block(),
        "SLP_CANTEEN": [
            # 食堂：取餐台 + 餐桌椅
            _rect(-480, -380, 480, 380),
            _rect(-420, 180, 420, 280),
            ("line", -420, 180, 420, 280),
        ] + [
            ("circle", x, -40, 85) for x in (-250, 0, 250)
        ] + [
            ("line", x - 115, -40, x - 55, -40) for x in (-250, 0, 250)
        ] + [
            ("line", x + 55, -40, x + 115, -40) for x in (-250, 0, 250)
        ] + [_text("食", 190, 0, -300)],
        "SLP_TOILET": [
            # 卫生间/淋浴间：隔间 + 洗手/淋浴位
            _rect(-480, -380, 480, 380),
            ("line", -480, 120, 480, 120),
            ("line", -480, -80, 480, -80),
        ] + [
            ("line", x, 120, x, 380) for x in (-240, 0, 240)
        ] + [
            ("circle", x, -180, 55) for x in (-330, -110, 110, 330)
        ] + [_text("卫", 170, 0, -310)],
        "SLP_DRYING": [
            # 晾晒区：双排晾衣绳 + 衣物示意
            _rect(-480, -380, 480, 380),
            ("line", -400, 180, 400, 180),
            ("line", -400, -20, 400, -20),
            ("poly", [(-320, 180), (-320, 80), (-250, 50), (-180, 80), (-180, 180)], False),
            ("poly", [(20, 180), (20, 80), (90, 50), (160, 80), (160, 180)], False),
            ("poly", [(-250, -20), (-250, -120), (-180, -150), (-110, -120), (-110, -20)], False),
            ("poly", [(100, -20), (100, -120), (170, -150), (240, -120), (240, -20)], False),
            _text("晾", 190, 0, -310),
        ],
        "SLP_OFFICE": _office_block(),
        "SLP_PARK": [
            _rect(-480, -380, 480, 380),
            ("line", -240, -380, -240, 100),
            ("line", 0, -380, 0, 100),
            ("line", 240, -380, 240, 100),
            _text("P", 300, 0, -250),
        ],
        "SLP_NOTICE": [
            # 九牌一图：9 块 1.2m 板直线连续排布，不是 3×3 方阵
            ("line", -480, -250, 480, -250),
            ("line", -480, 250, 480, 250),
            ("solid", [(-500, -300), (-460, -300), (-460, 300), (-500, 300)]),
            ("solid", [(460, -300), (500, -300), (500, 300), (460, 300)]),
        ] + [
            _rect(-456 + index * 101, -220, -456 + index * 101 + 96, 220)
            for index in range(9)
        ] + [_text("九", 170, 0, -345)],
        "SLP_PODIUM": [
            _rect(-480, -320, 480, 320),
            ("poly", [(-300, -80), (300, -80), (300, 240), (-300, 240)], True),
            ("line", 0, -80, 0, -320),
            ("line", -300, 130, 300, 130),
            _text("讲", 170, 0, -420),
        ],
        "SLP_WASTE": [
            _rect(-420, -380, 420, 380),
            ("line", -300, -260, 300, 260),
            ("line", -300, 260, 300, -260),
            _text("垃", 190, 0, -110),
        ],
        "SLP_WEIGHBRIDGE": _weighbridge_block(),
        "SLP_WASH": _wash_block(),
        "SLP_TEMP": [
            _rect(-480, -360, 480, 360),
            ("poly", [(-520, 360), (0, 620), (520, 360)], False),
            ("line", -300, -360, -300, 360),
            ("line", 300, -360, 300, 360),
            _text("临", 190, 0, -110),
        ],
        "SLP_NEIGHBOR": [
            _rect(-480, -380, 480, 380),
        ] + [
            ("line", -480, y, 480, y) for y in (-240, -80, 80, 240)
        ] + [_text("邻", 190, 0, -110)],
    }
    return shapes


SHAPES: Dict[str, List[Tuple]] = _shapes()


def primitives(category: str) -> List[Tuple]:
    """返回某类设施的图元列表（只读用途）。"""
    name = block_name(category)
    return list(SHAPES.get(name or "", []))


def _add_text(block: Any, value: str, height: float = 230.0, x: float = 0.0, y: float = -115.0) -> None:
    from ezdxf.enums import TextEntityAlignment

    text = block.add_text(value, height=float(height), dxfattribs={"layer": "0"})
    text.set_placement((float(x), float(y)), align=TextEntityAlignment.CENTER)


def ensure_symbol_blocks(doc: Any) -> List[str]:
    """创建缺失图块，幂等；返回本次创建的块名。"""
    created: List[str] = []
    for category, item in SYMBOLS.items():
        name = item["block"]
        if name in doc.blocks:
            continue
        block = doc.blocks.new(name=name)
        created.append(name)
        for prim in SHAPES.get(name, []):
            kind = prim[0]
            if kind == "line":
                block.add_line((prim[1], prim[2]), (prim[3], prim[4]), dxfattribs={"layer": "0"})
            elif kind == "poly":
                block.add_lwpolyline(list(prim[1]), close=bool(prim[2]), dxfattribs={"layer": "0"})
            elif kind == "solid":
                points = [(float(x), float(y)) for x, y in prim[1]]
                for index in range(1, len(points) - 1):
                    block.add_solid([points[0], points[index], points[index + 1]],
                                    dxfattribs={"layer": "0"})
            elif kind == "circle":
                block.add_circle((prim[1], prim[2]), prim[3], dxfattribs={"layer": "0"})
            elif kind == "arc":
                block.add_arc((prim[1], prim[2]), prim[3], prim[4], prim[5],
                              dxfattribs={"layer": "0"})
            elif kind == "text":
                _add_text(block, prim[1], prim[2], prim[3], prim[4])
    return created


def insert_symbol(msp: Any, category: str, x: float, y: float, layer: str, color: int,
                  size_mm: Optional[float] = None, rotation: float = 0.0) -> bool:
    name = block_name(category)
    if not name:
        return False
    size = float(size_mm or symbol_size(category))
    msp.add_blockref(name, insert=(float(x), float(y)), dxfattribs={
        "layer": layer, "color": color,
        "xscale": size / BASE, "yscale": size / BASE, "rotation": float(rotation),
    })
    return True


def _arc_points(cx: float, cy: float, r: float, start: float, end: float,
                steps: int = 8) -> List[Tuple[float, float]]:
    if end < start:
        end += 360.0
    points = []
    for index in range(steps + 1):
        angle = math.radians(start + (end - start) * index / steps)
        points.append((cx + r * math.cos(angle), cy + r * math.sin(angle)))
    return points


def draw_pictogram(draw: Any, category: str, cx: float, cy: float, size_px: float,
                   color: Any, width: Optional[int] = None,
                   rotation: float = 0.0) -> bool:
    """把同一套图元画到 PNG（PIL ImageDraw）；像素尺寸 size_px 对应 BASE。"""
    prims = primitives(category)
    if not prims:
        return False
    scale = float(size_px) / BASE
    line_w = int(width or max(1, round(size_px / 26.0)))
    angle = math.radians(float(rotation))
    cos_a, sin_a = math.cos(angle), math.sin(angle)

    def px(x: float, y: float) -> Tuple[float, float]:
        xr = x * cos_a - y * sin_a
        yr = x * sin_a + y * cos_a
        return (cx + xr * scale, cy - yr * scale)

    for prim in prims:
        kind = prim[0]
        if kind == "line":
            draw.line((px(prim[1], prim[2]), px(prim[3], prim[4])), fill=color, width=line_w)
        elif kind == "poly":
            points = [px(x, y) for x, y in prim[1]]
            if prim[2]:
                points = points + [points[0]]
            draw.line(points, fill=color, width=line_w)
        elif kind == "solid":
            points = [px(x, y) for x, y in prim[1]]
            if len(points) >= 3:
                draw.polygon(points, fill=color)
        elif kind == "circle":
            # 旋转后圆的包围盒仍应以旋转后的圆心为中心；用两个对角点
            # 直接相减会在 90°/180° 旋转时把 x0/x1 次序颠倒。
            ccx, ccy = px(prim[1], prim[2])
            radius_px = prim[3] * scale
            draw.ellipse((ccx - radius_px, ccy - radius_px,
                          ccx + radius_px, ccy + radius_px),
                         outline=color, width=line_w)
        elif kind == "arc":
            points = [px(x, y) for x, y in _arc_points(prim[1], prim[2], prim[3], prim[4], prim[5])]
            draw.line(points, fill=color, width=line_w)
        elif kind == "text":
            # PNG 图标不重复画块内文字：尺寸小时文字变成墨点，说明放在图例名称里。
            continue
    return True


def categories_in(model: Dict[str, Any]) -> List[Dict[str, Any]]:
    counts: Dict[str, int] = {}
    names: Dict[str, str] = {}
    for row in model.get("facilities") or []:
        category = str(row.get("category") or "")
        if not block_name(category):
            continue
        counts[category] = counts.get(category, 0) + 1
        names[category] = str(row.get("category_name") or SYMBOLS[category]["zh"])
    if model.get("cranes"):
        counts["tower_crane"] = len(model["cranes"])
        names["tower_crane"] = SYMBOLS["tower_crane"]["zh"]
    order = list(SYMBOLS.keys())
    return [{"category": key, "name": names[key], "count": counts[key],
             "block": block_name(key)} for key in order if key in counts]
