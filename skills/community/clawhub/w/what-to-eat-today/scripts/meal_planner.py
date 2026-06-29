#!/usr/bin/env python3
"""
今天吃什么 — 智能三餐规划引擎

职责（程序负责，确定性计算）：
  1. 日期感知：星期几、节日、节气、季节、日期尾数
  2. 主力蛋白周历 + 烹饪方式日期轮换
  3. 历史记录持久化 + 多维排重
  4. 从菜库智能组合候选菜
  5. 输出结构化 JSON 给 LLM

LLM / SKILL.md 负责（柔性、人性化）：
  - 做法要点、预处理建议、便当打包建议、出餐顺序
  - 宝宝注意事项、节日文案
  - 用户额外要求的柔性调整
  - 最终格式化成用户友好的输出

用法：
  python meal_planner.py                    # 今天
  python meal_planner.py --date 2026-06-20  # 指定日期
  python meal_planner.py --no-save          # 不写历史
  python meal_planner.py --reset-history    # 清空历史
"""

import json
import os
import random
import sys
from datetime import date, datetime, timedelta
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
SKILL_ROOT = SCRIPT_DIR.parent
DISH_LIBRARY_PATH = SCRIPT_DIR / "dish_library.json"
HISTORY_PATH = SKILL_ROOT / "history.json"

# ============================================================
# 1. 农历/节日/节气 数据
# ============================================================

# 二十四节气近似日期（公历月日范围） — 与 SKILL.md 保持一致
SOLAR_TERMS = [
    ("立春", (2, 3),  (2, 5),  "春饼、萝卜",   "春饼卷菜，清爽开胃"),
    ("雨水", (2, 18), (2, 20), None,           "春天湿气重，推荐薏米粥、山药"),
    ("惊蛰", (3, 5),  (3, 7),  "梨",           "雪梨银耳汤、冰糖炖梨"),
    ("春分", (3, 20), (3, 22), "春菜",         "春笋、荠菜正当季"),
    ("清明", (4, 4),  (4, 6),  "青团",         "超市买现成青团当早饭或加餐"),
    ("谷雨", (4, 19), (4, 21), "香椿",         "香椿炒蛋，谷雨前后最嫩"),
    ("立夏", (5, 5),  (5, 7),  "鸡蛋",         "早饭煮鸡蛋"),
    ("小满", (5, 20), (5, 22), "苦菜",         "苦瓜炒蛋、凉拌苦菊"),
    ("芒种", (6, 5),  (6, 7),  "梅子",         "酸梅汤，解暑开胃"),
    ("夏至", (6, 20), (6, 22), "面条",         "中午/晚上吃凉面/打卤面"),
    ("小暑", (7, 6),  (7, 8),  "饺子",         "头伏饺子"),
    ("大暑", (7, 22), (7, 24), "伏茶",         "绿豆汤、冬瓜茶消暑"),
    ("立秋", (8, 7),  (8, 9),  "吃肉",         "红烧肉、炖牛肉"),
    ("处暑", (8, 22), (8, 24), "鸭子",         "啤酒鸭、冬瓜鸭汤"),
    ("白露", (9, 7),  (9, 9),  "龙眼",         "龙眼正当季"),
    ("秋分", (9, 22), (9, 24), "秋菜",         "秋葵、南瓜、莲藕正当时"),
    ("寒露", (10, 8), (10, 9), "芝麻",         "芝麻酱拌面、芝麻糊"),
    ("霜降", (10, 23),(10, 24),"柿子",         "柿子当水果；炖牛肉加番茄"),
    ("立冬", (11, 7), (11, 8), "饺子",         "立冬吃饺子"),
    ("小雪", (11, 22),(11, 23),"糍粑",         "糯米糍粑当加餐"),
    ("大雪", (12, 6), (12, 8), "腌肉",         "腊肉炒菜、腊味蒸饭"),
    ("冬至", (12, 21),(12, 23),"饺子/汤圆",    "晚饭全家包饺子"),
    ("小寒", (1, 5),  (1, 7),  "腊八粥",       "电饭锅预约各种粥"),
    ("大寒", (1, 20), (1, 21), None,           "一年最冷，多推荐炖菜、汤锅暖身"),
]

# 2026 年传统节日（农历→公历对照）
# 注：农历转换使用简单算法，2027+ 需更新或引入 zhdate 库
LUNAR_FESTIVALS_2026 = {
    "2026-01-26": {"name": "腊八节", "food": "腊八粥", "tip": "早饭电饭锅预约腊八粥"},
    "2026-02-10": {"name": "小年(北方)", "food": "饺子", "tip": "晚饭吃饺子"},
    "2026-02-17": {"name": "春节", "food": "饺子、年糕、鱼", "tip": "晚饭包饺子/蒸年糕，鱼清蒸"},
    "2026-03-03": {"name": "元宵节", "food": "元宵/汤圆", "tip": "早饭或晚饭后煮汤圆当甜品"},
    "2026-03-20": {"name": "龙抬头", "food": "春饼", "tip": "春饼卷菜，全家动手卷着吃"},
    "2026-04-05": {"name": "清明节", "food": "青团", "tip": "超市买现成青团当早饭"},
    "2026-06-19": {"name": "端午节", "food": "粽子", "tip": "早饭蒸粽子，宝宝少吃（糯米不易消化）"},
    "2026-08-19": {"name": "七夕", "food": "巧果", "tip": "可当晚间小点心"},
    "2026-09-25": {"name": "中秋节", "food": "月饼、柚子", "tip": "月饼当饭后点心，柚子当水果"},
    "2026-10-19": {"name": "重阳节", "food": "重阳糕", "tip": "重阳糕当早饭，寓意敬老"},
    "2026-12-22": {"name": "冬至", "food": "饺子/汤圆", "tip": "晚饭全家包饺子"},
}

# ============================================================
# 2. 日期感知引擎
# ============================================================

def _in_range(d: date, start_md: tuple, end_md: tuple) -> bool:
    """判断日期是否在月日范围内（跨年友好）"""
    val = (d.month, d.day)
    s = start_md
    e = end_md
    if s <= e:
        return s <= val <= e
    else:  # 跨年范围，如 12/21 ~ 1/7
        return val >= s or val <= e

def detect_date_info(target_date: date) -> dict:
    """根据日期返回完整的上下文信息"""
    weekday_cn = ["周一", "周二", "周三", "周四", "周五", "周六", "周日"]
    wd = target_date.weekday()  # 0=Mon
    date_str = target_date.isoformat()

    info = {
        "date": date_str,
        "weekday": wd,
        "weekday_cn": weekday_cn[wd],
        "is_weekend": wd >= 5,
        "date_digit": target_date.day % 10,
        "month": target_date.month,
        "day": target_date.day,
        "festival": None,
        "solar_term": None,
        "season": get_season(target_date.month),
        "primary_protein": None,
        "cooking_preference": [],
    }

    # 检测传统节日（优先级最高）
    if date_str in LUNAR_FESTIVALS_2026:
        f = LUNAR_FESTIVALS_2026[date_str]
        info["festival"] = {"name": f["name"], "food": f["food"], "tip": f["tip"]}
        # 冬至也是节气，但仍以节日为准

    # 检测节气
    for term_name, start, end, food, tip in SOLAR_TERMS:
        if _in_range(target_date, start, end):
            info["solar_term"] = {"name": term_name, "food": food, "tip": tip}
            break

    # 主力蛋白（节日可覆盖，见 combine 阶段）
    info["primary_protein"] = get_primary_protein(wd)

    # 烹饪方式偏好
    info["cooking_preference"] = get_cooking_preference(target_date.day % 10)

    return info

def get_season(month: int) -> str:
    if month in (3, 4, 5):  return "春"
    if month in (6, 7, 8):  return "夏"
    if month in (9, 10, 11): return "秋"
    return "冬"

def get_primary_protein(weekday: int) -> dict:
    """主力蛋白周历"""
    table = {
        0: ("鸡", "禽类（鸡/鸭）"),
        1: ("猪", "猪肉"),
        2: ("鱼", "水产（鱼/虾）"),
        3: ("牛", "牛羊"),
        4: ("蛋", "豆蛋"),
        5: ("*", "自由日"),  # 周六
        6: ("*", "硬菜日"),  # 周日, * 表示不限
    }
    code, label = table[weekday]
    return {"code": code, "label": label}

def get_cooking_preference(date_digit: int) -> list:
    """烹饪方式日期权重"""
    if date_digit in (0, 1, 2):
        return ["蒸", "炖"]
    elif date_digit in (3, 4, 5):
        return ["炒"]
    elif date_digit in (6, 7):
        return ["炖", "煮"]
    else:
        return ["蒸", "炒"]


# ============================================================
# 3. 历史记录管理
# ============================================================

def load_history() -> list:
    """加载历史记录，返回 entry 列表"""
    if not HISTORY_PATH.exists():
        return []
    try:
        with open(HISTORY_PATH) as f:
            data = json.load(f)
        return data.get("entries", [])
    except (json.JSONDecodeError, KeyError):
        return []

def save_history(entries: list):
    """保存历史记录（保留最近 60 条）"""
    entries = entries[-60:]
    with open(HISTORY_PATH, "w") as f:
        json.dump({"last_updated": date.today().isoformat(), "entries": entries},
                  f, ensure_ascii=False, indent=2)

def get_recent_dish_names(entries: list, days: int = 7) -> set:
    """获取最近 N 天内出现过的菜名"""
    cutoff = date.today() - timedelta(days=days)
    names = set()
    for entry in entries:
        entry_date = date.fromisoformat(entry["date"])
        if entry_date >= cutoff:
            for meal_type in ("breakfast", "lunch", "dinner"):
                for dish in entry.get(meal_type, []):
                    names.add(dish["name"])
    return names

def get_recent_main_ingredients(entries: list, days: int = 3) -> dict:
    """获取最近 N 天内出现的主食材及次数"""
    cutoff = date.today() - timedelta(days=days)
    ingredients = {}
    for entry in entries:
        entry_date = date.fromisoformat(entry["date"])
        if entry_date >= cutoff:
            for meal_type in ("lunch", "dinner"):
                for dish in entry.get(meal_type, []):
                    ing = dish.get("main_ingredient", "")
                    if ing:
                        ingredients[ing] = ingredients.get(ing, 0) + 1
    return ingredients


# ============================================================
# 4. 菜库加载 & 候选池构建
# ============================================================

def load_dish_library() -> dict:
    with open(DISH_LIBRARY_PATH) as f:
        return json.load(f)

def _match_protein(dish: dict, target_code: str) -> bool:
    """检查菜的蛋白分类是否匹配"""
    p = dish.get("protein", "")
    if target_code == "鸡":
        return p == "鸡"
    if target_code == "猪":
        return p == "猪" and dish.get("main_ingredient", "") not in ("牛腩",)
    if target_code == "鱼":
        return p == "鱼"
    if target_code == "牛":
        return p == "牛"
    if target_code == "蛋":
        return p in ("蛋", "豆")
    if target_code == "*":
        return True  # 自由日/硬菜日
    return True

def _match_cooking(dish: dict, preference: list) -> bool:
    """检查烹饪方式是否匹配偏好（宽松匹配）"""
    method = dish.get("method", "")
    if method in preference:
        return True
    # 炖菜也匹配"炖"偏好
    if "炖" in preference and method == "炖":
        return True
    if "煮" in preference and method == "煮":
        return True
    return False

def _match_season(dish: dict, season: str) -> bool:
    """当季食材加分"""
    seasons = dish.get("season", [])
    if not seasons:
        return True  # 无季节标注的默认可用
    return season in seasons

def filter_candidates(
    dishes: list,
    date_info: dict,
    history: list,
    method_filter: str,
    target_count: int = 5,
) -> list:
    """
    从菜品列表中筛选候选菜。
    排序优先级：非黑名单 > 蛋白匹配 > 烹饪偏好匹配 > 季节匹配 > 随机
    """
    recent_names = get_recent_dish_names(history, days=7)
    recent_ingredients = get_recent_main_ingredients(history, days=3)
    primary_code = date_info["primary_protein"]["code"]
    cooking_pref = date_info["cooking_preference"]
    season = date_info["season"]

    scored = []
    for dish in dishes:
        name = dish["name"]

        # 黑名单：7天内同名菜直接排除
        if name in recent_names:
            continue

        # 黑名单：3天内主食材超过2次降权但不排除
        ing = dish.get("main_ingredient", "")
        ing_count = recent_ingredients.get(ing, 0)

        score = 10.0  # 基础分

        # 惩罚：近期主食材出现次数
        score -= ing_count * 3.0

        # 奖励：匹配主力蛋白
        if _match_protein(dish, primary_code):
            score += 5.0

        # 奖励：匹配烹饪偏好
        if _match_cooking(dish, cooking_pref):
            score += 3.0

        # 奖励：当季
        if _match_season(dish, season):
            score += 2.0

        # 奖励：带饭评分高
        score += dish.get("lunch_score", 0) * 1.0

        # 微随机扰动（同日期同种子，保证可复现）
        rng = random.Random(f"{date_info['date']}_{name}")
        score += rng.uniform(-0.5, 0.5)

        scored.append((score, dish))

    # 按分数降序排列
    scored.sort(key=lambda x: x[0], reverse=True)

    return [dish for _, dish in scored[:target_count]]


# ============================================================
# 5. 三餐组合引擎
# ============================================================

def _is_baby_friendly(dish: dict) -> bool:
    bf = dish.get("baby_friendly", True)
    return bf is True or bf == "warn"  # warn 也可选，但有注意事项

def _dish_flavors(dishes: list) -> set:
    return {d.get("flavor", "") for d in dishes if d.get("flavor")}

def select_breakfast(library: dict, date_info: dict, history: list, festival_food: str = None) -> list:
    """早饭：1粥/主食 + 1配菜 + 1饮品"""
    bf = library["breakfast"]
    rng = random.Random(date_info["date"] + "_breakfast")

    # 节日覆盖
    if festival_food in ("腊八粥",):
        return [
            {"name": "腊八粥", "subtype": "粥", "prep": "电饭锅预约"},
            {"name": "煮鸡蛋", "subtype": "配菜", "prep": "前一晚煮好放冰箱"},
            {"name": "牛奶", "subtype": "饮品", "prep": "加热即饮"},
        ]

    if festival_food and "粽子" in str(festival_food):
        return [
            {"name": "粽子", "subtype": "主食", "prep": "早上蒸10分钟", "note": "宝宝少吃，糯米不易消化"},
            {"name": "牛奶", "subtype": "饮品", "prep": "加热即饮"},
        ]

    if festival_food and "青团" in str(festival_food):
        return [
            {"name": "青团", "subtype": "主食", "prep": "即食（超市买现成）"},
            {"name": "煮鸡蛋", "subtype": "配菜", "prep": "前一晚煮好放冰箱"},
            {"name": "豆浆", "subtype": "饮品", "prep": "加热即饮"},
        ]

    if festival_food and "汤圆" in str(festival_food):
        return [
            {"name": "汤圆", "subtype": "主食", "prep": "早上煮5分钟", "note": "宝宝少吃，糯米不易消化"},
            {"name": "煮鸡蛋", "subtype": "配菜", "prep": "前一晚煮好放冰箱"},
            {"name": "牛奶", "subtype": "饮品", "prep": "加热即饮"},
        ]

    # 节气食物
    solar_term = date_info.get("solar_term")
    if solar_term and solar_term.get("food") == "鸡蛋":
        bf_eggs = [d for d in bf if "蛋" in d.get("name", "")]
    else:
        bf_eggs = [d for d in bf if d.get("subtype") == "配菜"]

    # 分类
    porridges = [d for d in bf if d["subtype"] == "粥"]
    staples = [d for d in bf if d["subtype"] == "主食"]
    sides = [d for d in bf if d["subtype"] == "配菜"]
    drinks = [d for d in bf if d["subtype"] == "饮品"]

    # 工作日：粥为主，周末可以选主食
    if date_info["is_weekend"]:
        main_candidates = porridges + staples
    else:
        main_candidates = porridges  # 工作日电饭锅预约粥最省时

    # 季节过滤
    season = date_info["season"]
    main_candidates = [d for d in main_candidates if _match_season(d, season)] or main_candidates

    # 随机选（种子基于日期保证可复现）
    rng.shuffle(main_candidates)
    rng.shuffle(sides)
    rng.shuffle(drinks)

    main = main_candidates[:1] if main_candidates else [{"name": "小米粥", "subtype": "粥", "prep": "电饭锅预约"}]
    side = sides[:1] if sides else [{"name": "煮鸡蛋", "subtype": "配菜", "prep": "前一晚煮好放冰箱"}]
    drink = drinks[:1] if drinks else [{"name": "牛奶", "subtype": "饮品", "prep": "加热即饮"}]

    return main + side + drink

def select_lunch(library: dict, date_info: dict, history: list, festival_food: str = None) -> tuple:
    """午饭便当：1道蒸菜（带饭友好）。返回 (dishes, used_proteins)"""
    steamed = library["steamed"]
    rng = random.Random(date_info["date"] + "_lunch")
    primary_code = date_info["primary_protein"]["code"]

    # 过滤：适合带饭（lunch_score >= 2）
    candidates = [d for d in steamed if d.get("lunch_score", 0) >= 2]

    # 节日食物优先
    if festival_food and "饺子" in str(festival_food):
        dish = {"name": "蒸饺", "main_ingredient": "饺子", "protein": "猪", "method": "蒸", "baby_friendly": True, "steam_time": "10-15分钟"}
        return [dish], {"猪"}

    # 应用排重 + 偏好过滤
    candidates = filter_candidates(candidates, date_info, history, "蒸", 5)

    # 优先选匹配主力蛋白的（提高蛋白匹配权重）
    protein_match = [d for d in candidates if _match_protein(d, primary_code)]
    if protein_match:
        selected = rng.choice(protein_match)
    elif candidates:
        selected = rng.choice(candidates)
    else:
        selected = steamed[0]  # fallback

    used_proteins = {selected.get("protein", "")}
    return [selected], used_proteins

def select_dinner(library: dict, date_info: dict, history: list, lunch_proteins: set = None, lunch_names: set = None, festival_food: str = None) -> list:
    """
    晚饭：3道菜，至少1蒸菜
    规则：
    - 如果命中了节日食物，优先安排
    - 主力蛋白至少出现在1道菜中（如果午饭还没用过）
    - 至少1道蒸菜
    - 口味至少2种
    - 不重复午饭菜名、不重复午饭蛋白
    """
    steamed = library["steamed"]
    stir_fry = library["stir_fry"]
    stew_soup = library["stew_soup"]
    rng = random.Random(date_info["date"] + "_dinner")

    primary_code = date_info["primary_protein"]["code"]
    primary_label = date_info["primary_protein"]["label"]
    cooking_pref = date_info["cooking_preference"]
    is_weekend = date_info["is_weekend"]
    season = date_info["season"]
    if lunch_proteins is None:
        lunch_proteins = set()
    if lunch_names is None:
        lunch_names = set()

    selected = []
    used_proteins = set(lunch_proteins)       # 同天不重复肉
    used_names = set(lunch_names)              # 同天不重复菜名

    # ---- 节日覆盖 ----
    if festival_food and "饺子" in str(festival_food):
        # 冬至/春节：全家包饺子
        return [
            {"name": "饺子(蒸/煮)", "main_ingredient": "饺子", "protein": "猪", "method": "蒸", "flavor": "咸香", "baby_friendly": True, "steam_time": "15-20分钟"},
            {"name": "紫菜蛋花汤",   "main_ingredient": "紫菜",   "protein": "蛋", "method": "煮", "flavor": "清淡", "baby_friendly": True, "stew_time": "5分钟"},
            {"name": "蒜蓉西兰花",   "main_ingredient": "西兰花", "protein": "素", "method": "炒", "flavor": "清淡", "baby_friendly": True},
        ]

    # ---- 组合策略 ----

    # Step A: 选蒸菜（至少1道），排除午饭已用蛋白和菜名
    steamed_candidates = filter_candidates(steamed, date_info, history, "蒸", 5)
    steamed_candidates = [d for d in steamed_candidates if d["name"] not in used_names and d.get("protein") not in used_proteins]

    # 优先选匹配主力蛋白的
    protein_steamed = [d for d in steamed_candidates if _match_protein(d, primary_code)]
    other_steamed = [d for d in steamed_candidates if not _match_protein(d, primary_code)]

    if protein_steamed:
        steam_dish = rng.choice(protein_steamed)
    elif other_steamed:
        steam_dish = rng.choice(other_steamed)
    else:
        steam_dish = rng.choice(steamed)
    selected.append(steam_dish)
    used_main_ingredients = {steam_dish.get("main_ingredient", "")}
    used_proteins.add(steam_dish.get("protein", ""))

    # Step B: 选第2道菜（炒菜为主）
    stir_candidates = filter_candidates(stir_fry, date_info, history, "炒", 6)
    stew_candidates = filter_candidates(stew_soup, date_info, history, "炖", 4)

    # 排除已用主食材 + 已用蛋白
    stir_candidates = [d for d in stir_candidates if d.get("main_ingredient") not in used_main_ingredients and d.get("protein") not in used_proteins]
    stew_candidates = [d for d in stew_candidates if d.get("main_ingredient") not in used_main_ingredients and d.get("protein") not in used_proteins]

    # 如果主力蛋白还没出现，优先从炒菜/炖菜中选
    if primary_code not in (d.get("protein", "") for d in selected):
        protein_stir = [d for d in stir_candidates if _match_protein(d, primary_code)]
        protein_stew = [d for d in stew_candidates if _match_protein(d, primary_code)]
        if protein_stir:
            dish2 = rng.choice(protein_stir)
            selected.append(dish2)
            used_main_ingredients.add(dish2.get("main_ingredient", ""))
            used_proteins.add(dish2.get("protein", ""))
        elif protein_stew:
            dish2 = rng.choice(protein_stew)
            selected.append(dish2)
            used_main_ingredients.add(dish2.get("main_ingredient", ""))
            used_proteins.add(dish2.get("protein", ""))

    # Step C: 如果还不到3道，继续选
    while len(selected) < 3:
        # 轮流从炒菜、炖菜中选
        pool = stir_candidates if len(selected) % 2 == 0 else stew_candidates
        if not pool:
            pool = stir_fry  # fallback to all
        pool = [d for d in pool if d.get("main_ingredient") not in used_main_ingredients and d.get("protein") not in used_proteins]
        if pool:
            dish = rng.choice(pool)
            selected.append(dish)
            used_main_ingredients.add(dish.get("main_ingredient", ""))
            used_proteins.add(dish.get("protein", ""))
        else:
            # 实在没合适的，从全部菜库随机补一个
            all_dishes = steamed + stir_fry + stew_soup
            available = [d for d in all_dishes if d.get("main_ingredient") not in used_main_ingredients and d.get("protein") not in used_proteins]
            if available:
                dish = rng.choice(available)
                selected.append(dish)
                used_main_ingredients.add(dish.get("main_ingredient", ""))
                used_proteins.add(dish.get("protein", ""))
            else:
                break

    # Step D: 周末硬菜日，至少有一道费时的菜
    if is_weekend and date_info["weekday_cn"] == "周日":
        hard_dishes = [
            {"name": "红烧肉",       "main_ingredient": "五花肉", "protein": "猪", "method": "炖", "flavor": "咸香", "baby_friendly": True, "stew_time": "90分钟"},
            {"name": "酱牛肉",       "main_ingredient": "牛腱子", "protein": "牛", "method": "炖", "flavor": "咸香", "baby_friendly": True, "stew_time": "90分钟"},
            {"name": "梅菜扣肉",     "main_ingredient": "五花肉", "protein": "猪", "method": "蒸", "flavor": "咸香", "baby_friendly": False, "steam_time": "60分钟"},
            {"name": "菌菇鸡汤",     "main_ingredient": "鸡",     "protein": "鸡", "method": "炖", "flavor": "清淡", "baby_friendly": True, "stew_time": "90分钟"},
            {"name": "啤酒鸭",       "main_ingredient": "鸭",     "protein": "鸡", "method": "炖", "flavor": "咸香", "baby_friendly": True, "stew_time": "60分钟"},
        ]
        hard = rng.choice(hard_dishes)
        # 替换第一道菜或追加
        if len(selected) < 3:
            selected.append(hard)
        else:
            selected[0] = hard

    # Step E: 口味校验
    flavors = _dish_flavors(selected)
    if len(flavors) < 2 and len(selected) >= 2:
        # 尝试换一道菜换取更多口味
        all_pool = [d for d in stir_fry + stew_soup if d.get("flavor") not in flavors and d.get("main_ingredient") not in used_main_ingredients]
        if all_pool and len(selected) >= 2:
            selected[-1] = rng.choice(all_pool)

    return selected[:3]

# ============================================================
# 6. 主流程
# ============================================================

def build_entry(date_info: dict, breakfast: list, lunch: list, dinner: list) -> dict:
    """构建历史记录条目"""
    return {
        "date": date_info["date"],
        "weekday_cn": date_info["weekday_cn"],
        "protein": date_info["primary_protein"]["code"],
        "festival": date_info["festival"]["name"] if date_info["festival"] else None,
        "solar_term": date_info["solar_term"]["name"] if date_info["solar_term"] else None,
        "breakfast": [{"name": d["name"], "main_ingredient": d.get("main_ingredient", "")} for d in breakfast],
        "lunch": [{"name": d["name"], "main_ingredient": d.get("main_ingredient", "")} for d in lunch],
        "dinner": [{"name": d["name"], "main_ingredient": d.get("main_ingredient", "")} for d in dinner],
    }

def plan_meals(target_date: date = None, save: bool = True) -> dict:
    """
    主入口：为指定日期规划三餐。
    返回结构化 JSON（供 LLM 读取后格式化输出）。
    """
    if target_date is None:
        target_date = date.today()

    date_info = detect_date_info(target_date)
    library = load_dish_library()
    history = load_history()

    festival_food = date_info["festival"]["food"] if date_info["festival"] else None
    solar_term = date_info.get("solar_term")

    # 节日/节气的食物提示
    date_messages = []
    if date_info["festival"]:
        date_messages.append({
            "type": "festival",
            "name": date_info["festival"]["name"],
            "food": date_info["festival"]["food"],
            "tip": date_info["festival"]["tip"],
        })
    if solar_term and solar_term.get("food"):
        if not date_info["festival"] or date_info["festival"]["name"] != solar_term["name"]:
            date_messages.append({
                "type": "solar_term",
                "name": solar_term["name"],
                "food": solar_term["food"],
                "tip": solar_term["tip"],
            })

    # 组合三餐
    breakfast = select_breakfast(library, date_info, history, festival_food)
    lunch, lunch_proteins = select_lunch(library, date_info, history, festival_food)
    lunch_names = {d["name"] for d in lunch}
    dinner = select_dinner(library, date_info, history, lunch_proteins, lunch_names, festival_food)

    # 构建结果
    result = {
        "meta": {
            "engine": "meal_planner v1.0",
            "generated_at": datetime.now().isoformat(),
        },
        "date_context": {
            "date": date_info["date"],
            "weekday_cn": date_info["weekday_cn"],
            "is_weekend": date_info["is_weekend"],
            "season": date_info["season"],
            "date_digit": date_info["date_digit"],
            "primary_protein": date_info["primary_protein"],
            "cooking_preference": date_info["cooking_preference"],
            "date_messages": date_messages,
        },
        "meals": {
            "breakfast": breakfast,
            "lunch": lunch,
            "dinner": dinner,
        },
        "dedup": {
            "recent_dish_count": len(get_recent_dish_names(history, days=7)),
            "recent_ingredient_count": len(get_recent_main_ingredients(history, days=3)),
            "history_entries": len(history),
        },
    }

    # 保存历史
    if save:
        entry = build_entry(date_info, breakfast, lunch, dinner)
        history.append(entry)
        save_history(history)
        result["meta"]["history_saved"] = True

    return result


# ============================================================
# CLI
# ============================================================

def main():
    import argparse

    parser = argparse.ArgumentParser(description="今天吃什么 - 智能三餐规划引擎")
    parser.add_argument("--date", type=str, default=None, help="指定日期 YYYY-MM-DD")
    parser.add_argument("--no-save", action="store_true", help="不写入历史记录")
    parser.add_argument("--reset-history", action="store_true", help="清空历史记录")
    parser.add_argument("--json", action="store_true", default=True, help="JSON 输出（默认）")
    args = parser.parse_args()

    if args.reset_history:
        if HISTORY_PATH.exists():
            HISTORY_PATH.unlink()
        print(json.dumps({"status": "ok", "message": "历史记录已清空"}, ensure_ascii=False))
        return

    target_date = date.today()
    if args.date:
        try:
            target_date = date.fromisoformat(args.date)
        except ValueError:
            print(json.dumps({"error": f"无效日期: {args.date}，格式应为 YYYY-MM-DD"}, ensure_ascii=False), file=sys.stderr)
            sys.exit(2)

    result = plan_meals(target_date, save=not args.no_save)
    print(json.dumps(result, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
