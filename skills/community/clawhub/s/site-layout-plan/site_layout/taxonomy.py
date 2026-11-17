"""施工平面布置设施分类表（单一事实来源）。

分类只描述"这是什么设施"，不代表已识别成功；识图证据由 cad-file-reader
的 site-layout-facility 包给出，本表负责中英文名、图层、默认阶段与必备性。
"""
from __future__ import annotations

from typing import Any, Dict, Tuple

STAGES: Tuple[str, ...] = ("earthwork", "structure", "finish")
STAGE_NAMES: Dict[str, str] = {
    "earthwork": "土石方阶段",
    "structure": "主体结构阶段",
    "finish": "装饰装修阶段",
}
STAGE_ORDER = {name: index for index, name in enumerate(STAGES)}

# kind: point 点状设施 / line 线状设施 / area 区域设施
FACILITIES: Dict[str, Dict[str, Any]] = {
    "tower_crane": {
        "zh": "塔吊", "layer": "CRANE-塔吊", "color": 1, "kind": "point",
        # 默认只服务主体结构；如需装饰阶段继续使用，在 active_stages 显式加 finish
        "stages": ("structure",),
    },
    "construction_elevator": {
        "zh": "施工电梯", "layer": "FAC-施工电梯", "color": 30, "kind": "line",
        "stages": ("structure", "finish"),
    },
    "site_access": {
        "zh": "大门/出入口", "layer": "FAC-出入口", "color": 2, "kind": "point",
        "stages": STAGES,
    },
    "permanent_road": {
        "zh": "永久道路", "layer": "FAC-永久道路", "color": 8, "kind": "line",
        "stages": STAGES,
    },
    "temporary_road": {
        "zh": "临时道路", "layer": "FAC-临时道路", "color": 3, "kind": "line",
        "stages": STAGES,
    },
    "fire_access": {
        "zh": "消防车道", "layer": "FAC-消防车道", "color": 6, "kind": "line",
        "stages": STAGES,
    },
    "temporary_power": {
        "zh": "临时用电线路", "layer": "FAC-临时用电", "color": 5, "kind": "line",
        "stages": STAGES,
    },
    "distribution_room": {
        "zh": "配电室", "layer": "FAC-配电室", "color": 5, "kind": "area",
        "stages": STAGES,
    },
    "transformer": {
        "zh": "变压器/箱变", "layer": "FAC-变压器", "color": 5, "kind": "area",
        "stages": STAGES,
    },
    "primary_distribution_box": {
        "zh": "一级配电箱", "layer": "FAC-一级箱", "color": 5, "kind": "point",
        "stages": STAGES,
    },
    "temporary_water": {
        "zh": "临时给水", "layer": "FAC-临时给水", "color": 4, "kind": "line",
        "stages": STAGES,
    },
    "drainage_ditch": {
        "zh": "排水沟", "layer": "FAC-排水沟", "color": 4, "kind": "line",
        "stages": STAGES,
    },
    "fire_water": {
        "zh": "临时消防给水", "layer": "FAC-消防给水", "color": 6, "kind": "line",
        "stages": STAGES,
    },
    "fire_hydrant": {
        "zh": "消火栓", "layer": "FAC-消火栓", "color": 6, "kind": "point",
        "stages": STAGES,
    },
    "fire_pump_room": {
        "zh": "消防泵房", "layer": "FAC-消防泵房", "color": 6, "kind": "area",
        "stages": STAGES,
    },
    "fire_water_tank": {
        "zh": "消防水池", "layer": "FAC-消防水池", "color": 6, "kind": "area",
        "stages": STAGES,
    },
    "processing_zone": {
        "zh": "加工区", "layer": "FAC-加工区", "color": 30, "kind": "area",
        "stages": ("structure", "finish"),
    },
    # 0.6.0 起加工区拆分：钢筋/木工/砂浆砌体各自建类、各自隔离规则。
    # processing_zone 保留为旧数据/识图通用别名，不主动生成。
    "steel_processing": {
        "zh": "钢筋加工区", "layer": "FAC-钢筋加工区", "color": 30, "kind": "area",
        "stages": ("structure",),
    },
    "wood_processing": {
        "zh": "木工加工区", "layer": "FAC-木工加工区", "color": 30, "kind": "area",
        "stages": ("structure", "finish"),
    },
    "mortar_processing": {
        "zh": "砂浆/砌体加工区", "layer": "FAC-砂浆加工区", "color": 30, "kind": "area",
        "stages": ("structure", "finish"),
    },
    "material_yard": {
        "zh": "材料堆场", "layer": "FAC-材料堆场", "color": 30, "kind": "area",
        "stages": ("structure", "finish"),
    },
    "temporary_dormitory": {
        "zh": "临时宿舍", "layer": "FAC-宿舍", "color": 40, "kind": "area",
        "stages": STAGES,
    },
    "site_office": {
        "zh": "办公区", "layer": "FAC-办公区", "color": 40, "kind": "area",
        "stages": STAGES,
    },
    # 0.7.0 生活区分设：员工宿舍与工人生活区分开建模，不再用一个“临时宿舍”
    # 混指管理人员宿舍和工人生活区。生活区类默认全阶段保留。
    "staff_dormitory": {
        "zh": "员工宿舍区", "layer": "FAC-员工宿舍", "color": 40, "kind": "area",
        "stages": STAGES,
    },
    "worker_living_zone": {
        "zh": "工人生活区", "layer": "FAC-工人生活区", "color": 40, "kind": "area",
        "stages": STAGES,
    },
    "canteen": {
        "zh": "食堂", "layer": "FAC-食堂", "color": 40, "kind": "area",
        "stages": STAGES,
    },
    "toilet_shower": {
        "zh": "卫生间/淋浴间", "layer": "FAC-卫生间淋浴", "color": 40, "kind": "area",
        "stages": STAGES,
    },
    "drying_area": {
        "zh": "晾晒区", "layer": "FAC-晾晒区", "color": 40, "kind": "area",
        "stages": STAGES,
    },
    "parking": {
        "zh": "停车场", "layer": "FAC-停车场", "color": 8, "kind": "area",
        "stages": STAGES,
    },
    "notice_board": {
        # 9 块板沿围挡/道路直线排布，平面按长条区域表达，不再用单点图块。
        "zh": "九牌一图", "layer": "FAC-九牌一图", "color": 2, "kind": "area",
        "stages": STAGES,
    },
    "safety_podium": {
        "zh": "安全宣讲台", "layer": "FAC-宣讲台", "color": 2, "kind": "area",
        "stages": STAGES,
    },
    "waste_pool": {
        "zh": "垃圾池", "layer": "FAC-垃圾池", "color": 32, "kind": "area",
        "stages": STAGES,
    },
    "wheel_wash": {
        "zh": "洗车池/沉淀池", "layer": "FAC-洗车池", "color": 4, "kind": "area",
        # 施工全过程车辆冲洗：默认全阶段保留；仅土方阶段设置须显式改 active_stages
        "stages": STAGES,
    },
    "weighbridge": {
        # 地磅：平台 + 两端引坡 + 称重房；按项目是否需称重设置，不列为阶段硬性必备。
        "zh": "地磅", "layer": "FAC-地磅", "color": 3, "kind": "area",
        "stages": STAGES,
    },
    "hoarding": {
        "zh": "围挡", "layer": "FAC-围挡", "color": 32, "kind": "line",
        "stages": STAGES,
    },
    "site_boundary_neighbor": {
        "zh": "相邻地貌/周边", "layer": "FAC-相邻地貌", "color": 8, "kind": "area",
        "stages": STAGES,
    },
    "temporary_building": {
        "zh": "临时建筑（食堂/厕所等）", "layer": "FAC-临建", "color": 40, "kind": "area",
        "stages": STAGES,
    },
}

# 每阶段硬性必备：缺了就不能算"该阶段布置完整"，但只判 fail，不代做布置。
REQUIRED_BY_STAGE: Dict[str, Tuple[str, ...]] = {
    "earthwork": ("site_access", "temporary_road", "fire_access", "temporary_power",
                  "wheel_wash"),
    "structure": ("site_access", "temporary_road", "fire_access", "temporary_power",
                  "tower_crane", "construction_elevator", "processing_zone",
                  "site_office"),
    "finish": ("site_access", "temporary_road", "fire_access", "temporary_power",
               "construction_elevator", "waste_pool", "site_office"),
}

# 别名：reader/人工 JSON 可能用这些写法
ALIASES: Dict[str, str] = {
    "crane": "tower_crane",
    "towercrane": "tower_crane",
    "lift": "construction_elevator",
    "elevator": "construction_elevator",
    "gate": "site_access",
    "entrance": "site_access",
    "road": "temporary_road",
    "temp_road": "temporary_road",
    "permanent_road": "permanent_road",
    "fire_lane": "fire_access",
    "fire_road": "fire_access",
    "power": "temporary_power",
    "electric": "temporary_power",
    "water": "temporary_water",
    "hydrant": "fire_hydrant",
    "distribution_box": "primary_distribution_box",
    "first_box": "primary_distribution_box",
    "processing": "processing_zone",
    "rebar_yard": "steel_processing",
    "rebar_processing": "steel_processing",
    "steel": "steel_processing",
    "wood_yard": "wood_processing",
    "wood": "wood_processing",
    "mortar": "mortar_processing",
    "masonry": "mortar_processing",
    "fire_pump": "fire_pump_room",
    "fire_pump_house": "fire_pump_room",
    "fire_tank": "fire_water_tank",
    "water_tank": "fire_water_tank",
    "box_transformer": "transformer",
    "substation": "transformer",
    "ditch": "drainage_ditch",
    "gutter": "drainage_ditch",
    # 0.7.0：dorm/dormitory 默认指员工宿舍；旧“临时宿舍”数据仍可用
    # temporary_dormitory 或 temp_dorm 原样归一，不静默改义。
    "dormitory": "staff_dormitory",
    "dorm": "staff_dormitory",
    "staff_dorm": "staff_dormitory",
    "employee_dorm": "staff_dormitory",
    "employee_dormitory": "staff_dormitory",
    "员工宿舍": "staff_dormitory",
    "员工宿舍区": "staff_dormitory",
    "管理人员宿舍": "staff_dormitory",
    "living": "worker_living_zone",
    "living_zone": "worker_living_zone",
    "worker_living": "worker_living_zone",
    "workers_living": "worker_living_zone",
    "worker_living_area": "worker_living_zone",
    "labour_living": "worker_living_zone",
    "labor_living": "worker_living_zone",
    "生活区": "worker_living_zone",
    "工人生活区": "worker_living_zone",
    "canteen": "canteen",
    "mess": "canteen",
    "dining": "canteen",
    "dining_hall": "canteen",
    "食堂": "canteen",
    "餐厅": "canteen",
    "toilet": "toilet_shower",
    "toilets": "toilet_shower",
    "wc": "toilet_shower",
    "shower": "toilet_shower",
    "bathroom": "toilet_shower",
    "卫生间": "toilet_shower",
    "淋浴间": "toilet_shower",
    "厕所": "toilet_shower",
    "drying": "drying_area",
    "laundry": "drying_area",
    "晾晒区": "drying_area",
    "晾衣区": "drying_area",
    "temp_dorm": "temporary_dormitory",
    "temporary_dorm": "temporary_dormitory",
    "office": "site_office",
    "office_area": "site_office",
    "办公区": "site_office",
    "car_park": "parking",
    "board": "notice_board",
    "nine_boards": "notice_board",
    "podium": "safety_podium",
    "rubbish": "waste_pool",
    "garbage": "waste_pool",
    "wash": "wheel_wash",
    "weighbridge": "weighbridge",
    "weigh_bridge": "weighbridge",
    "truck_scale": "weighbridge",
    "scale": "weighbridge",
    "dibang": "weighbridge",
    "地磅": "weighbridge",
    "fence": "hoarding",
    "neighbor": "site_boundary_neighbor",
    "surroundings": "site_boundary_neighbor",
    "temporary_building": "temporary_building",
}


def canonical(category: Any) -> str:
    """把别名归一为分类键；未知分类原样返回小写键。"""
    key = str(category or "").strip().lower().replace("-", "_").replace(" ", "_")
    key = ALIASES.get(key, key)
    return key


def meta(category: Any) -> Dict[str, Any]:
    key = canonical(category)
    return FACILITIES.get(key, {
        "zh": key or "未分类", "layer": "FAC-其他", "color": 7, "kind": "point",
        "stages": STAGES,
    })


def is_known(category: Any) -> bool:
    return canonical(category) in FACILITIES
