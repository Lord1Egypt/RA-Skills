from __future__ import annotations

from urllib.parse import urlencode

CARS_CATEGORY = "cars"
DEFAULT_SEARCH_LOCATION = "uk"

# ── 排序选项 ──────────────────────────────────────────────────────────────────
SORT_OPTIONS = [
    "relevance",            # 相关性（默认）
    "date",                 # 最新发布
    "price_lowest_first",   # 价格从低到高
    "price_highest_first",  # 价格从高到低
    "distance",             # 距离由近到远
    "year_newest_first",    # 生产年份从新到旧
    "year_oldest_first",    # 生产年份从旧到新
    "mileage_lowest_first", # 行驶里程从低到高
    "mileage_highest_first", # 行驶里程从高到低
]

# 需要本地二次排序的 sort 值（Gumtree 服务端对这些排序不稳定）
CLIENT_SORT_VALUES = frozenset([
    "year_newest_first",
    "year_oldest_first",
    "mileage_lowest_first",
    "mileage_highest_first",
])

# ── 燃油类型 ──────────────────────────────────────────────────────────────────
FUEL_TYPES = [
    "petrol",         # 汽油
    "diesel",         # 柴油
    "electric",       # 纯电动
    "hybrid_electric", # 混合动力
    "gas_bi_fuel",    # 气油两用
]

# ── 变速箱类型 ────────────────────────────────────────────────────────────────
TRANSMISSION_TYPES = [
    "manual",    # 手动
    "automatic", # 自动
]

# ── 车身类型 ──────────────────────────────────────────────────────────────────
BODY_TYPES = [
    "hatchback",        # 两厢车
    "saloon",           # 三厢轿车
    "estate",           # 旅行车
    "suv",              # SUV
    "coupe",            # 跑车/轿跑
    "convertible",      # 敞篷车
    "mpv",              # 多用途车
    "car_derived_van",  # 商用两厢
    "light_4x4_utility", # 轻型四驱
    "sports",           # 运动型
    "other",            # 其他
]

# ── 座位数 ────────────────────────────────────────────────────────────────────
SEAT_OPTIONS = [2, 3, 4, 5, 6, 7, 8, 9]

# ── 平均油耗（MPG） ───────────────────────────────────────────────────────────
MPG_OPTIONS = [
    "over_30",  # 30+ mpg（百公里约 9.4L 以内）
    "over_40",  # 40+ mpg（百公里约 7.1L 以内）
    "over_50",  # 50+ mpg（百公里约 5.6L 以内）
    "over_60",  # 60+ mpg（百公里约 4.7L 以内）
]

# ── 里程筛选 ──────────────────────────────────────────────────────────────────
MILEAGE_OPTIONS = [
    "up_to_15000",  # 1.5 万英里以内
    "up_to_30000",  # 3 万英里以内
    "up_to_60000",  # 6 万英里以内
    "up_to_80000",  # 8 万英里以内
    "over_80000",   # 超过 8 万英里
]

# ── 车龄筛选（注册年限） ──────────────────────────────────────────────────────
YEAR_OPTIONS = [
    "up_to_1",  "up_to_2",  "up_to_3",  "up_to_4",  "up_to_5",
    "up_to_6",  "up_to_7",  "up_to_8",  "up_to_9",  "up_to_10",
    "over_10",
]

# ── 发动机排量 ────────────────────────────────────────────────────────────────
ENGINE_SIZE_OPTIONS = [
    "up_to_999",    # 999cc 以内
    "1000_to_1999", # 1.0L - 2.0L
    "2000_to_2999", # 2.0L - 3.0L
    "3000_to_3999", # 3.0L - 4.0L
    "4000_to_4999", # 4.0L - 5.0L
    "over_4999",    # 超过 5.0L
]

# ── 车门数量 ──────────────────────────────────────────────────────────────────
DOOR_OPTIONS = [2, 3, 4, 5]

# ── 卖家类型 ──────────────────────────────────────────────────────────────────
SELLER_TYPE_OPTIONS = ["trade", "private"]

# ── 常见颜色（Gumtree URL 参数值） ───────────────────────────────────────────
COLOUR_OPTIONS = [
    "white", "black", "silver", "grey", "blue", "red", "green",
    "yellow", "orange", "purple", "brown", "gold", "bronze",
    "beige", "multi_coloured", "other",
]


def _join_values(values: list[str] | None) -> str | None:
    if not values:
        return None
    cleaned = [v.strip() for v in values if v.strip()]
    return ",".join(cleaned) if cleaned else None


def build_car_search_url(
    keyword: str = "",
    search_location: str = DEFAULT_SEARCH_LOCATION,
    sort: str | None = None,
    distance: int | None = None,
    min_price: int | None = None,
    max_price: int | None = None,
    make: str | None = None,
    model: str | None = None,
    fuel_type: str | None = None,
    transmission: str | None = None,
    body_type: str | None = None,
    mileage: str | None = None,
    year: str | None = None,
    engine_size: str | None = None,
    colour: str | None = None,
    doors: int | None = None,
    seats: int | None = None,
    avg_mpg: str | None = None,
    seller_types: list[str] | None = None,
) -> str:
    """构建 Gumtree 二手车搜索 URL，包含所有支持的筛选参数。"""
    params: dict[str, str | int] = {
        "search_category": CARS_CATEGORY,
        "q": keyword or "",
        "search_term_populated_by": "input",
        "keyword_correction": "suggest",
        "search_location": search_location,
    }
    optional_params: dict[str, str | int | None] = {
        "sort": sort,
        "distance": distance,
        "min_price": min_price,
        "max_price": max_price,
        "vehicle_make": make,
        "vehicle_model": model,
        "vehicle_fuel_type": fuel_type,
        "vehicle_transmission": transmission,
        "vehicle_body_type": body_type,
        "vehicle_mileage": mileage,
        "vehicle_registration_year": year,
        "vehicle_engine_size": engine_size,
        "vehicle_colour": colour,
        "vehicle_doors": doors,
        "vehicle_seats": seats,
        "vehicle_average_mpg": avg_mpg,
        "seller_type": _join_values(seller_types),
    }
    for key, value in optional_params.items():
        if value not in (None, ""):
            params[key] = value  # type: ignore[assignment]

    return f"https://www.gumtree.com/search?{urlencode(params)}"
