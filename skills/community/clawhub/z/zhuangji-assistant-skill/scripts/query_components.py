#!/usr/bin/env python3
"""配件查询工具 — 按品类、预算、平台、颜色筛选配件。

渐进式披露: 默认只返回 summary (id+model+price)，用 --detail 看完整属性。

用法:
  python query_components.py --category gpu --budget 5000
  python query_components.py --category cpu --platform intel --limit 5
  python query_components.py --category case --color white --summary
  python query_components.py --category all --budget 8000 --json
"""

import argparse
import json
import re
import sys
from statistics import median
from pathlib import Path

import yaml

from component_inference import enrich_item, infer_gpu_cooling, infer_gpu_vram

try:
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
except Exception:
    pass

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"

CATEGORIES = {
    "cpu": "cpus",
    "mb": "motherboards",
    "memory": "memory",
    "storage": "storage",
    "gpu": "gpus",
    "cooler": "coolers",
    "psu": "psus",
    "case": "cases",  # from cases.yaml
}

DISPLAY_NAMES = {
    "cpu": "CPU",
    "mb": "主板",
    "memory": "内存",
    "storage": "硬盘",
    "gpu": "显卡",
    "cooler": "散热",
    "psu": "电源",
    "case": "机箱",
}

# Summary fields per category — minimal fields needed for first-pass narrowing.
SUMMARY_BASE_FIELDS = ["id", "brand", "model", "price_cny", "price_status", "price_date"]
SUMMARY_FIELDS_BY_CATEGORY = {
    "cpu": SUMMARY_BASE_FIELDS + ["platform", "socket", "cores", "threads", "power_w"],
    "mb": SUMMARY_BASE_FIELDS + [
        "platform", "socket", "chipset", "memory_generations", "memory_slots",
        "memory_freq_max", "m2_slots", "sata_ports", "form_factor", "color",
    ],
    "memory": SUMMARY_BASE_FIELDS + [
        "generation", "capacity_gb", "module_count", "frequency_mt", "timing", "color", "rgb",
    ],
    "storage": SUMMARY_BASE_FIELDS + [
        "capacity_tb", "capacity_gb", "form_factor", "interface", "pcie_generation", "storage_type", "series",
    ],
    "gpu": SUMMARY_BASE_FIELDS + [
        "chip", "gpu_vendor", "vram_gb", "memory_type", "memory_bus_bit",
        "memory_bandwidth_gbps", "gpu_cooling", "gpu_radiator_required",
        "length_mm", "power_w", "power_connectors", "requires_16pin_psu", "color", "rgb",
    ],
    "cooler": SUMMARY_BASE_FIELDS + ["type", "height_mm", "radiator_mm", "color", "rgb"],
    "psu": SUMMARY_BASE_FIELDS + [
        "wattage_w", "form_factor", "length_mm", "efficiency", "modular", "native_16pin_gpu_power", "color",
    ],
    "case": SUMMARY_BASE_FIELDS + [
        "colors", "motherboard_support", "gpu_length_mm", "cpu_cooler_height_mm",
        "radiator_support", "fan_mounts", "fan_slots_count", "psu_support", "psu_length_mm", "is_showcase",
    ],
}

COLOR_ALIASES = {
    "white": {"white", "白", "白色"},
    "black": {"black", "黑", "黑色"},
}

RGB_TERMS = ("ARGB", "RGB", "幻彩", "炫彩", "彩色", "彩光", "灯效", "灯光", "发光")
NO_RGB_TERMS = ("无光", "不发光")

# 以下排序只按芯片/芯片组定位辅助筛选，不包含品牌优劣判断。
# 若后续加入品牌/系列候选池权重，应仅基于公开电商销量、装机采用率、
# 渠道覆盖和规格完整度等可观察信号，并保持非品牌倾向、非品牌贬损。
GPU_TIERS = (
    ("RTXPRO6000", 10.0),
    ("RTX5090DV2", 7.8), ("RTX5090D", 8.0), ("RTX5090", 8.2),
    ("RTX5080", 7),
    ("RTX5070TI", 6),
    ("RTX5070", 5), ("RX9070XT", 5),
    ("RTX5060TI", 4),
    ("RX9070GRE", 3), ("RX9070", 3),
    ("RTX5060", 2), ("ARCB580", 2), ("A770", 2), ("RX9060XT", 2), ("RTX3060TI", 2),
    ("RTX5050", 1), ("ARCB570", 1), ("A750", 1),
)

MOTHERBOARD_TIERS = (
    ("Z890", 70), ("X870", 70),
    ("Z790", 65), ("X670", 65),
    ("B860", 55), ("B850", 55),
    ("B760", 50), ("B650", 50),
    ("H810", 10), ("H610", 10), ("A820", 10), ("A620", 10),
)

# Positive candidate-pool signals derived from public adoption, channel coverage,
# visible specifications and common DIY usage. This is not a brand endorsement
# or a negative judgment against brands outside the list.
MOTHERBOARD_PRIMARY_SIGNALS = (
    "华硕", "ASUS", "技嘉", "GIGABYTE", "微星", "MSI",
)

MOTHERBOARD_SERIES_SIGNALS = (
    "AYW", "TUF", "PRIME", "AORUS", "GAMINGX", "GAMING X",
    "迫击炮", "MORTAR", "MAG", "GAMINGPRO", "GAMING PRO", "小雕",
)

MOTHERBOARD_COMMON_SIGNALS = (
    "华擎", "ASROCK", "七彩虹", "COLORFUL", "BATTLEAX",
)

STORAGE_PRIMARY_SIGNALS = (
    "SAMSUNG", "三星", "致态", "TIPLUS", "TIPLUS", "ZHITAI",
    "宏碁掠夺者", "PREDATOR", "ACER",
    "WD", "西数", "SN850", "SN770", "BLACK",
    "KIOXIA", "铠侠", "SOLIDIGM", "海力士", "HYNIX",
    "LEXAR", "雷克沙", "CRUCIAL", "英睿达",
    "ADATA", "威刚", "XPG",
)

STORAGE_COMMON_SIGNALS = (
    "金百达", "KINGBANK", "梵想", "光威",
)

MEMORY_ADOPTION_SIGNALS = (
    "芝奇", "GSKILL", "G.SKILL", "TRIDENT", "幻锋",
    "金百达", "KINGBANK", "阿斯加特", "ASGARD",
    "ADATA", "威刚", "XPG", "光威", "GLOWAY", "玖合",
    "宏碁掠夺者", "PREDATOR", "ACER", "KINGSTON", "金士顿",
    "CORSAIR", "海盗船", "CRUCIAL", "英睿达",
)

COOLER_ADOPTION_SIGNALS = (
    "利民", "THERMALRIGHT", "九州风神", "DEEPCOOL", "酷冷至尊", "COOLERMASTER",
    "雅浚", "乔思伯", "JONSBO", "瓦尔基里", "VALKYRIE", "华硕", "ASUS",
)

PSU_PRIMARY_SIGNALS = (
    "海韵", "SEASONIC", "振华", "SUPERFLOWER", "SUPER FLOWER",
    "海盗船", "CORSAIR", "全汉", "FSP",
)

PSU_COMMON_SIGNALS = (
    "微星", "MSI", "酷冷至尊", "COOLERMASTER", "长城", "GREATWALL",
    "安钛克", "ANTEC", "鑫谷", "SEGOTEP", "华硕", "ASUS",
)


def load_components():
    """Load components.yaml."""
    with (DATA / "components.yaml").open("r", encoding="utf-8") as f:
        lib = yaml.safe_load(f)
    for section, items in list(lib.items()):
        if isinstance(items, list):
            lib[section] = [enrich_item(section, item) for item in items]
    return lib


def load_cases():
    """Load cases.yaml."""
    with (DATA / "cases.yaml").open("r", encoding="utf-8") as f:
        return yaml.safe_load(f)


_PRICE_FLOORS = None


def load_price_floors():
    """Load optional lower-bound market reference floors."""
    global _PRICE_FLOORS
    if _PRICE_FLOORS is not None:
        return _PRICE_FLOORS
    path = DATA / "price_floors.yaml"
    if not path.exists():
        _PRICE_FLOORS = {}
        return _PRICE_FLOORS
    with path.open("r", encoding="utf-8") as f:
        _PRICE_FLOORS = yaml.safe_load(f) or {}
    return _PRICE_FLOORS


def normalize_color(value):
    """Normalize common Chinese/English color names."""
    if value is None:
        return ""
    text = str(value).strip().lower()
    for normalized, aliases in COLOR_ALIASES.items():
        if text in aliases:
            return normalized
    return text


def compact_text(value):
    """Normalize model/spec text for simple scope checks."""
    return "".join(ch for ch in str(value or "").upper() if ch.isalnum())


def item_text(item):
    """Join searchable fields for positive candidate-pool scoring."""
    return " ".join(str(item.get(k, "")) for k in ("brand", "model", "series", "id"))


def has_candidate_signal(item, signals):
    """Return whether an item matches a positive public-adoption signal."""
    text = compact_text(item_text(item))
    return any(compact_text(signal) in text for signal in signals)


def candidate_signal_score(item, primary=(), secondary=(), common=()):
    """Score visible public-adoption signals without using negative brand labels."""
    score = 0
    if primary and has_candidate_signal(item, primary):
        score += 12
    if secondary and has_candidate_signal(item, secondary):
        score += 6
    if common and has_candidate_signal(item, common):
        score += 4
    return score


def parse_rated_wattage(item):
    """Prefer rated wattage in the model text over noisy imported fields."""
    text = str(item.get("model", ""))
    match = re.search(r"额定\s*(\d{3,4})\s*W", text, flags=re.IGNORECASE)
    if match:
        return int(match.group(1))
    match = re.search(r"(\d{3,4})\s*W", text, flags=re.IGNORECASE)
    if match:
        return int(match.group(1))
    return int(item.get("wattage_w") or 0)


def _extract_cpu_model_token(item):
    text = compact_text(item_text(item))
    ultra = re.search(r"ULTRA[579](?:2[235678]\d)(?:K|KF|F)?(?:PLUS)?", text)
    if ultra:
        return ultra.group(0)
    core = re.search(r"I[3579](?:12|13|14)\d{3}(?:KF|K|F)?", text)
    if core:
        return core.group(0)
    for token in (
        "9950X3D", "9900X3D", "9800X3D", "7800X3D",
        "9950X", "9900X", "9700X", "9600X", "7500F",
    ):
        if token in text:
            return token
    return ""


def _cpu_price_floor_tokens(value):
    """Return compact aliases used by public daily CPU price-floor rows."""
    text = compact_text(value)
    tokens = {text} if text else set()
    ultra = re.fullmatch(r"U([579])(\d{3})(K|KF|F)?(PLUS)?", text)
    if ultra:
        suffix = ultra.group(3) or ""
        plus = ultra.group(4) or ""
        tokens.add(f"ULTRA{ultra.group(1)}{ultra.group(2)}{suffix}{plus}")
        tokens.add(f"COREULTRA{ultra.group(1)}{ultra.group(2)}{suffix}{plus}")
    ryzen = re.fullmatch(r"R([579])(\d{4}(?:X3D|X|F)?)", text)
    if ryzen:
        tokens.add(f"RYZEN{ryzen.group(1)}{ryzen.group(2)}")
        tokens.add(f"AMDRYZEN{ryzen.group(1)}{ryzen.group(2)}")
    return tokens


def _outlier_group_key(category, item):
    """Group near-identical specs so default tier sort can ignore low-price outliers."""
    if category == "gpu":
        chip = compact_text(item.get("chip") or "")
        if not chip:
            chip = compact_text(item.get("model") or "")
            for key, _ in GPU_TIERS:
                if key in chip:
                    chip = key
                    break
        vram = int(infer_gpu_vram(item) or 0)
        return ("gpu", chip, vram) if chip and vram else None
    if category == "storage":
        capacity = int(item.get("capacity_gb") or 0)
        gen = int(item.get("pcie_generation") or 0)
        speed = _storage_read_speed(item)
        speed_bucket = (speed // 1000) if speed else 0
        return ("storage", capacity, gen, speed_bucket) if capacity and gen else None
    if category == "memory":
        generation = str(item.get("generation") or "").upper()
        capacity = int(item.get("capacity_gb") or 0)
        freq = int(item.get("frequency_mt") or 0)
        timing = _memory_timing_value(item)
        modules = int(item.get("module_count") or 0)
        return ("memory", generation, capacity, freq, timing, modules) if generation and capacity and freq else None
    return None


def _near_capacity(value, target):
    if not value or not target:
        return False
    value = int(value)
    target = int(target)
    return abs(value - target) <= 96


def _same_capacity(value, target):
    if not value or not target:
        return False
    return int(value) == int(target)


def _trusted_price_floor(category, item):
    """Return a trusted lower price bound for categories with market floor data."""
    floors = load_price_floors()
    if category == "cpu":
        text = compact_text(" ".join(str(item.get(k, "")) for k in ("brand", "model", "id")))
        rows = sorted(floors.get("cpus", []), key=lambda row: len(compact_text(row.get("model"))), reverse=True)
        for row in rows:
            tokens = _cpu_price_floor_tokens(row.get("model"))
            if tokens and any(token in text for token in tokens):
                return int(row.get("floor_cny") or 0) or None
    if category == "gpu":
        chip_text = compact_text(" ".join(str(item.get(k, "")) for k in ("chip", "model", "id")))
        vram = int(infer_gpu_vram(item) or 0)
        rows = sorted(floors.get("gpus", []), key=lambda row: len(compact_text(row.get("chip"))), reverse=True)
        for row in rows:
            target = compact_text(row.get("chip"))
            if not target or target not in chip_text:
                continue
            min_vram = int(row.get("min_vram_gb") or 0)
            max_vram = int(row.get("max_vram_gb") or 0)
            if min_vram and vram and vram < min_vram:
                continue
            if max_vram and vram and vram > max_vram:
                continue
            return int(row.get("floor_cny") or 0) or None
    if category == "memory":
        generation = str(item.get("generation") or "").upper()
        capacity = int(item.get("capacity_gb") or 0)
        modules = int(item.get("module_count") or 0)
        for row in floors.get("memory", []):
            if generation != str(row.get("generation") or "").upper():
                continue
            if not _same_capacity(capacity, row.get("capacity_gb")):
                continue
            row_modules = int(row.get("module_count") or 0)
            if row_modules and modules and modules != row_modules:
                continue
            return int(row.get("floor_cny") or 0) or None
    if category == "storage":
        gen = int(item.get("pcie_generation") or 0)
        capacity = int(item.get("capacity_gb") or 0)
        if not capacity and item.get("capacity_tb"):
            capacity = int(float(item.get("capacity_tb")) * 1000)
        for row in floors.get("storage", []):
            if gen != int(row.get("pcie_generation") or 0):
                continue
            if not _near_capacity(capacity, row.get("capacity_gb")):
                continue
            return int(row.get("floor_cny") or 0) or None
    return None


def _low_price_floor(category, group_key, group_prices):
    """Return a conservative lower bound for default candidate ranking."""
    if len(group_prices) < 4:
        return None
    mid = median(group_prices)
    if category == "memory":
        ratio = 0.65
    elif category == "gpu":
        chip = str(group_key[1]) if len(group_key) > 1 else ""
        if "RTX5090" in chip:
            ratio = 0.90
        elif "RTX5080" in chip:
            ratio = 0.85
        else:
            ratio = 0.80
    else:
        ratio = 0.60
    return mid * ratio


def filter_low_price_outliers(category, results):
    """Remove low-price outliers from default tier results without setting an upper cap."""
    if category not in {"cpu", "gpu", "storage", "memory"}:
        return results
    groups = {}
    if category != "cpu":
        for item in results:
            price = item.get("price_cny")
            key = _outlier_group_key(category, item)
            if key and price:
                groups.setdefault(key, []).append(float(price))
    floors = {
        key: floor for key, prices in groups.items()
        if (floor := _low_price_floor(category, key, prices)) is not None
    }
    kept = []
    for item in results:
        key = _outlier_group_key(category, item)
        price = float(item.get("price_cny") or 0)
        trusted_floor = _trusted_price_floor(category, item)
        if trusted_floor and price and price < trusted_floor:
            continue
        if key in floors and price and price < floors[key]:
            continue
        kept.append(item)
    return kept


def color_matches(item, requested):
    """Return whether an item matches the requested color."""
    requested = normalize_color(requested)
    raw_colors = item.get("colors")
    if raw_colors is None:
        raw_colors = item.get("color", "")
    if not isinstance(raw_colors, list):
        raw_colors = [raw_colors]
    normalized = {normalize_color(c) for c in raw_colors if c}
    model_text = str(item.get("model", "")).lower()
    if normalized:
        if (requested == "white" and requested in normalized
                and ("白牌" in model_text or "白金牌" in model_text)
                and not actual_white_in_model(model_text)):
            return False
        return requested in normalized
    if requested == "white":
        model_text = model_text.replace("白牌", "")
    aliases = COLOR_ALIASES.get(requested, {requested})
    return any(alias.lower() in model_text for alias in aliases)


def actual_white_in_model(model_text):
    """Treat PSU efficiency words like 白牌/白金牌 as not being chassis color."""
    cleaned = str(model_text or "").lower().replace("白金牌", "").replace("白牌", "")
    return "white" in cleaned or "白" in cleaned or "雪" in cleaned


def rgb_matches(item, requested):
    """Return whether an item matches the requested RGB preference."""
    if requested is None:
        return True
    model_text = str(item.get("model", "")).upper()
    explicit = item.get("rgb")
    has_no_rgb_text = any(term.upper() in model_text for term in NO_RGB_TERMS)
    has_rgb_text = any(term.upper() in model_text for term in RGB_TERMS)
    if requested is True:
        return bool(explicit) or (has_rgb_text and not has_no_rgb_text)
    if explicit or (has_rgb_text and not has_no_rgb_text):
        return False
    return True


def in_current_scope(section, item, include_workstation_gpu=False):
    """Filter out legacy/irrelevant parts unless caller explicitly opts in."""
    model = compact_text(" ".join(str(item.get(k, "")) for k in ("brand", "model", "chip", "gpu_vendor")))
    socket = compact_text(item.get("socket"))

    if section == "cpus":
        if "CELERON" in model or "PENTIUM" in model or "XEON" in model or "至强" in str(item.get("model", "")):
            return False
        if "RYZEN" in model:
            return socket in {"AM5", "SOCKETAM5"}
        if "COREULTRA" in model or "ULTRA" in model:
            return socket in {"LGA1851", "1851"} or any(term in model for term in ("245", "250", "265", "270", "285"))
        return any(f"COREI{tier}1{gen}" in model or f"I{tier}1{gen}" in model
                   for tier in "3579" for gen in "234")

    if section == "motherboards":
        memory = " ".join(str(v) for v in item.get("memory_generations", []))
        return socket in {"LGA1700", "1700", "LGA1851", "1851", "AM5", "SOCKETAM5"} and "DDR3" not in memory.upper()

    if section == "memory":
        # Keep low-budget fallback candidates visible; recommendation rules still prefer 16GB+.
        return str(item.get("generation", "")).upper() in {"DDR4", "DDR5"} and int(item.get("capacity_gb") or 0) >= 8

    if section == "storage":
        form = str(item.get("form_factor", "")).upper()
        interface = str(item.get("interface", "")).upper()
        generation = item.get("pcie_generation") or 0
        capacity_tb = float(item.get("capacity_tb") or 0)
        capacity_gb = int(item.get("capacity_gb") or 0)
        return (
            "M.2" in form
            and ("PCIE" in interface or "NVME" in interface or int(generation or 0) >= 4)
            and int(generation or 0) >= 4
            and (capacity_tb >= 0.48 or capacity_gb >= 480)
        )

    if section == "gpus":
        if "RTXPRO" in model:
            return bool(include_workstation_gpu and "RTXPRO6000" in model)
        return any(term in model for term in (
            "RTX50", "RTX5050", "RTX5060", "RTX5070", "RTX5080", "RTX5090",
            "RTX3060TI", "RX9060", "RX9070", "ARCB570", "ARCB580",
        ))

    if section == "coolers":
        height = item.get("height_mm") or 0
        radiator = item.get("radiator_mm") or 0
        price = item.get("price_cny") or 0
        return (bool(radiator) or float(height or 0) >= 120) and int(price or 0) >= 50

    if section == "psus":
        return parse_rated_wattage(item) >= 450

    return True


def _matches_socket(item, requested):
    item_socket = compact_text(item.get("socket"))
    wanted = compact_text(requested)
    return not wanted or wanted in item_socket or item_socket in wanted


def _matches_memory_gen(section, item, requested):
    wanted = str(requested or "").upper()
    if not wanted:
        return True
    if section == "motherboards":
        return wanted in [str(g).upper() for g in item.get("memory_generations", [])]
    if section == "memory":
        return wanted == str(item.get("generation", "")).upper()
    return True


def _normalize_form_factor(ff):
    text = compact_text(ff)
    mapping = {"MICROATX": "MATX", "M-ATX": "MATX", "MINIITX": "ITX"}
    return mapping.get(text, text)


def _matches_form_factor(section, item, requested):
    wanted = _normalize_form_factor(requested)
    if not wanted:
        return True
    if section == "motherboards":
        return _normalize_form_factor(item.get("form_factor")) == wanted
    if section == "cases":
        supported = [_normalize_form_factor(v) for v in item.get("motherboard_support", [])]
        return wanted in supported
    return True


def _matches_max_length(section, item, max_length):
    if not max_length:
        return True
    if section == "gpus":
        length = item.get("length_mm") or 0
        return bool(length) and length <= max_length
    if section == "cases":
        limit = item.get("gpu_length_mm") or 0
        return bool(limit) and limit >= max_length
    return True


def parse_fan_slots_count(value):
    """Best-effort total fan slot count from compact case fan_mounts text."""
    if value in (None, "", [], {}):
        return None
    if isinstance(value, (int, float)):
        number = int(value)
        return number if 1 <= number <= 20 else None
    text = str(value).upper().replace("×", "X")
    if re.fullmatch(r"\s*\d{1,2}\s*", text):
        number = int(text)
        return number if 1 <= number <= 20 else None
    if re.fullmatch(r"\s*\d{2,3}(?:\.\d+)?\s*(?:MM|CM)\s*", text):
        return None
    match = re.search(r"(\d{1,2})\s*个(?:以上)?\s*(?:E-?ATX|ATX|M-?ATX|MATX|ITX|≤|<|$)", text)
    if match:
        return int(match.group(1))
    match = re.search(r"(\d{1,2})\s*(?:风扇位|风扇安装位)", text)
    if match:
        return int(match.group(1))
    match = re.search(r"(?:风扇位|风扇安装位)\s*(\d{1,2})", text)
    if match:
        return int(match.group(1))
    total = 0
    found = False
    for segment in re.split(r"[;；。]\s*", text):
        counts = []
        counts.extend(int(m.group(1)) for m in re.finditer(r"(\d{1,2})\s*X\s*(?:120|140|200)", segment))
        counts.extend(int(m.group(1)) for m in re.finditer(r"(?:120|140|200)\s*MM?\s*FAN\s*X\s*(\d{1,2})", segment))
        counts.extend(int(m.group(1)) for m in re.finditer(r"(?:120|140|200)\s*风扇\s*X\s*(\d{1,2})", segment))
        if counts:
            total += max(counts)
            found = True
    return total if found else None


def should_display_fan_mounts(value):
    """Only show raw fan_mounts when it looks like fan placement text, not dimensions."""
    if value in (None, "", [], {}):
        return False
    text = str(value).upper().replace("×", "X")
    if parse_fan_slots_count(text):
        return True
    if re.fullmatch(r"\s*\d{2,3}(?:\.\d+)?\s*(?:MM|CM)\s*", text):
        return False
    return bool(re.search(r"风扇|FAN|TOP|FRONT|REAR|BOTTOM|SIDE|前|顶|后|底|侧", text))


def radiator_fan_slots(radiator_mm):
    """Common AIO radiator fan occupancy: 240/280=2, 360/420=3."""
    try:
        size = int(radiator_mm or 0)
    except (TypeError, ValueError):
        return None
    if size in (360, 420):
        return 3
    if size in (240, 280):
        return 2
    if size in (120, 140):
        return 1
    return None


GPU_CHIP_SUFFIXES = ("DV2", "V2", "SUPER", "GRE", "TI", "XT", "D")


def _gpu_chip_suffix_conflicts(wanted, rest):
    """Avoid fuzzy chip matches such as RTX5070 matching RTX5070Ti."""
    for suffix in GPU_CHIP_SUFFIXES:
        if rest.startswith(suffix) and not wanted.endswith(suffix):
            return True
    return False


def _matches_gpu_chip(item, requested):
    """Match GPU chip tokens while preserving Ti/D/V2/XT/GRE distinctions."""
    wanted = compact_text(requested)
    if not wanted:
        return True
    if compact_text(item.get("chip")) == wanted:
        return True
    for field in ("chip", "model", "id"):
        text = compact_text(item.get(field))
        start = 0
        while True:
            pos = text.find(wanted, start)
            if pos < 0:
                break
            rest = text[pos + len(wanted):]
            if not _gpu_chip_suffix_conflicts(wanted, rest):
                return True
            start = pos + 1
    return False


def _sort_results(results, sort, category=None):
    """Sort with missing prices last and keep case sorting consistent."""
    if sort == "tier":
        results.sort(key=lambda x: _tier_sort_key(category, x))
    elif sort in ("desc", "price-desc"):
        results.sort(key=lambda x: (x.get("price_cny") is None, -(x.get("price_cny") or 0), x.get("id", "")))
    else:
        results.sort(key=lambda x: (x.get("price_cny") is None, x.get("price_cny") or 0, x.get("id", "")))


def query(category=None, budget=None, platform=None, color=None,
          rgb=None, limit=20, has_price_only=True, showcase=None,
          include_legacy=False, sort="asc", socket=None, chipset=None,
          memory_gen=None, form_factor=None, max_length=None, gpu_cooling="air",
          gpu_chip=None, min_vram=None, min_capacity=None, include_workstation_gpu=False):
    """查询配件。返回匹配的配件列表。"""
    if gpu_cooling == "any":
        gpu_cooling = None
    results = []

    if category == "case":
        # Query cases.yaml
        cases_data = load_cases()
        for item in cases_data.get("cases", []):
            if has_price_only and item.get("price_status") == "needs_market_quote":
                continue
            if not include_legacy and not item.get("motherboard_support"):
                continue
            if budget and item.get("price_cny") and item["price_cny"] > budget:
                continue
            if not _matches_form_factor("cases", item, form_factor):
                continue
            if not _matches_max_length("cases", item, max_length):
                continue
            if color and not color_matches(item, color):
                continue
            if showcase is True:
                case_type = str(item.get("is_showcase", False))
                if case_type != "True" and not item.get("is_showcase"):
                    continue
            results.append(_summarize_case(item))
        _sort_results(results, sort, "case")
        return results[:limit]

    # Query components.yaml
    lib = load_components()
    categories_to_search = [CATEGORIES[category]] if category and category in CATEGORIES \
        else [v for k, v in CATEGORIES.items() if k != "case"]

    for sec in categories_to_search:
        for item in lib.get(sec, []):
            if has_price_only and item.get("price_status") == "needs_market_quote":
                continue
            if not include_legacy and not in_current_scope(
                sec, item, include_workstation_gpu=include_workstation_gpu
            ):
                continue
            if budget and item.get("price_cny") and item["price_cny"] > budget:
                continue
            if platform:
                item_platform = item.get("platform", "").lower()
                if item_platform and platform.lower() not in item_platform:
                    continue
            if socket and sec in ("cpus", "motherboards") and not _matches_socket(item, socket):
                continue
            if chipset and sec == "motherboards" and compact_text(chipset) not in compact_text(item.get("chipset")):
                continue
            if memory_gen and not _matches_memory_gen(sec, item, memory_gen):
                continue
            if form_factor and not _matches_form_factor(sec, item, form_factor):
                continue
            if not _matches_max_length(sec, item, max_length):
                continue
            if sec == "gpus":
                if gpu_chip and not _matches_gpu_chip(item, gpu_chip):
                    continue
                if min_vram and int(infer_gpu_vram(item) or 0) < int(min_vram):
                    continue
                if gpu_cooling and infer_gpu_cooling(item) != gpu_cooling:
                    continue
            if sec == "memory" and min_capacity and int(item.get("capacity_gb") or 0) < int(min_capacity):
                continue
            if sec == "storage" and min_capacity and int(item.get("capacity_gb") or 0) < int(min_capacity):
                continue
            if color and not color_matches(item, color):
                continue
            if not rgb_matches(item, rgb):
                continue

            results.append(item)

    if category:
        results = filter_low_price_outliers(category, results)
    _sort_results(results, sort, category)
    return results[:limit]


def _gpu_tier(item):
    """Return GPU chip tier rank (higher = better). 0 for non-GPU or unknown."""
    chip = compact_text(" ".join(str(item.get(k, "")) for k in ("chip", "model", "id")))
    for key, tier in GPU_TIERS:
        if key in chip:
            return tier
    return 0


def _cpu_tier(item):
    """Return CPU tier rank for budget-near choices. Higher is better."""
    text = compact_text(" ".join(str(item.get(k, "")) for k in ("brand", "model", "id")))
    if "ULTRA9270" in text:
        return 820
    if "ULTRA9285" in text:
        return 810
    if "ULTRA7270" in text:
        return 830
    if "ULTRA7265" in text:
        return 780
    if "ULTRA5250" in text:
        return 735
    if "ULTRA5245" in text:
        return 700
    if "ULTRA5235" in text:
        return 680
    if "ULTRA5230" in text or "ULTRA5225" in text:
        return 610

    amd_scores = (
        ("9950X3D", 900), ("9800X3D", 880), ("7800X3D", 760),
        ("9950X", 830), ("9700X", 760), ("9900X", 730),
        ("9600X", 660), ("7500F", 450),
    )
    for key, score in amd_scores:
        if key in text:
            return score

    intel_scores = (
        ("I914900", 900), ("I914700", 860), ("I714700", 820),
        ("I714900", 820), ("I714700K", 835),
        ("I514600", 760), ("I512600K", 725), ("I512600", 710),
        ("I514490", 705), ("I514400", 690),
        ("I513490", 680), ("I513400", 670),
        ("I512490", 625), ("I512400", 600),
        ("I314100", 420), ("I313100", 380), ("I312100", 320),
    )
    for key, score in intel_scores:
        if key in text:
            return score
    return 0


def _motherboard_tier(item):
    """Return motherboard chipset tier rank (higher = better)."""
    text = compact_text(" ".join(str(item.get(k, "")) for k in ("chipset", "model", "id")))
    score = candidate_signal_score(
        item,
        primary=MOTHERBOARD_PRIMARY_SIGNALS,
        secondary=MOTHERBOARD_SERIES_SIGNALS,
        common=MOTHERBOARD_COMMON_SIGNALS,
    )
    for key, tier in MOTHERBOARD_TIERS:
        if key in text:
            return tier * 100 + score
    return score


def _storage_read_speed(item):
    """Infer advertised sequential read speed from common model text."""
    text = str(item.get("model", "")).upper()
    patterns = (
        r"读速\s*(\d{3,5})\s*MB",
        r"读取\s*(\d{3,5})\s*MB",
        r"(\d{3,5})\s*MB/S",
    )
    for pattern in patterns:
        match = re.search(pattern, text)
        if match:
            return int(match.group(1))
    return 0


def _storage_tier(item):
    """Score SSDs by positive adoption and visible specification signals."""
    score = 0
    score += candidate_signal_score(
        item,
        primary=STORAGE_PRIMARY_SIGNALS,
        common=STORAGE_COMMON_SIGNALS,
    )
    generation = int(item.get("pcie_generation") or 0)
    if generation >= 5:
        score += 5
    elif generation >= 4:
        score += 3
    speed = _storage_read_speed(item)
    if speed >= 7000:
        score += 4
    elif speed >= 5000:
        score += 2
    elif speed >= 3500:
        score += 1
    if "TLC" in compact_text(item_text(item)):
        score += 3
    capacity_gb = int(item.get("capacity_gb") or 0)
    if capacity_gb >= 4000:
        score += 2
    elif capacity_gb >= 2000:
        score += 1
    if item.get("price_cny") and item.get("price_date"):
        score += 1
    return score


def _memory_timing_value(item):
    """Infer CL/timing headline value from structured timing or model text."""
    text = str(item.get("timing") or item.get("model", "")).upper()
    match = re.search(r"(?:CL|C)\s*(\d{2})", text)
    return int(match.group(1)) if match else 0


def _memory_tier(item):
    """Score memory by positive adoption and balanced DDR4/DDR5 parameters."""
    score = 0
    if has_candidate_signal(item, MEMORY_ADOPTION_SIGNALS):
        score += 8
    freq = int(item.get("frequency_mt") or 0)
    if 6000 <= freq <= 6400:
        score += 4
    elif freq >= 6800:
        score += 3
    elif freq >= 5600:
        score += 2
    elif freq >= 3200:
        score += 1
    timing = _memory_timing_value(item)
    if timing and timing <= 30:
        score += 3
    elif timing and timing <= 36:
        score += 2
    module_count = int(item.get("module_count") or 0)
    if module_count == 2:
        score += 4
    elif module_count > 2:
        score -= 3
    price = int(item.get("price_cny") or 0)
    generation = str(item.get("generation", "")).upper()
    capacity_gb = int(item.get("capacity_gb") or 0)
    if generation == "DDR5" and freq >= 5600 and capacity_gb >= 32 and 0 < price < 1300:
        score -= 8
    if generation == "DDR5" and freq >= 5600 and capacity_gb >= 64 and 0 < price < 2500:
        score -= 8
    if item.get("price_cny") and item.get("price_date"):
        score += 1
    return score


def _cooler_tier(item):
    """Score coolers by heat capacity and visible adoption signals."""
    score = candidate_signal_score(item, primary=COOLER_ADOPTION_SIGNALS)
    radiator = int(item.get("radiator_mm") or 0)
    if radiator >= 420:
        score += 24
    elif radiator >= 360:
        score += 22
    elif radiator >= 240:
        score += 14
    text = compact_text(item_text(item))
    if "双塔" in str(item.get("model", "")) or "DUALTOWER" in text:
        score += 8
    heat_pipe_match = re.search(r"(\d)\s*热管", str(item.get("model", "")))
    if heat_pipe_match:
        pipes = int(heat_pipe_match.group(1))
        if pipes >= 7:
            score += 7
        elif pipes >= 6:
            score += 5
        elif pipes <= 4:
            score -= 3
    height = float(item.get("height_mm") or 0)
    if 145 <= height <= 165:
        score += 2
    if any(token in text for token in ("LCD", "数显", "屏")):
        score += 2
    if item.get("price_cny") and item.get("price_date"):
        score += 1
    return score


def _psu_tier(item):
    """Score PSUs by platform, wattage, efficiency and visible adoption signals."""
    score = candidate_signal_score(
        item,
        primary=PSU_PRIMARY_SIGNALS,
        common=PSU_COMMON_SIGNALS,
    )
    wattage = parse_rated_wattage(item)
    if wattage >= 1200:
        score += 8
    elif wattage >= 1000:
        score += 7
    elif wattage >= 850:
        score += 6
    elif wattage >= 750:
        score += 4
    elif wattage >= 650:
        score += 2
    text = compact_text(item_text(item))
    if any(token in text for token in ("ATX31", "ATX30", "PCIE5", "PCIE50", "12V2X6", "12VHPWR")):
        score += 5
    if item.get("native_16pin_gpu_power"):
        score += 4
    if any(token in text for token in ("钛金", "TITANIUM")):
        score += 4
    elif any(token in text for token in ("白金", "PLATINUM")):
        score += 3
    elif any(token in text for token in ("金牌", "GOLD")):
        score += 2
    if any(token in text for token in ("全模", "全模组", "FULLMODULAR")):
        score += 2
    if any(token in text for token in ("白牌", "WHITE牌".upper())):
        score -= 4
    if item.get("price_cny") and item.get("price_date"):
        score += 1
    return score


def _tier_sort_key(category, item):
    """Category-aware tier sort used by the progressive query helper."""
    price = item.get("price_cny") or 0
    if category == "cpu":
        return (-_cpu_tier(item), price)
    if category == "gpu":
        return (-_gpu_tier(item), price)
    if category == "mb":
        return (-_motherboard_tier(item), price)
    if category == "storage":
        return (-_storage_tier(item), price)
    if category == "memory":
        return (-_memory_tier(item), price)
    if category == "cooler":
        return (-_cooler_tier(item), price)
    if category == "psu":
        return (-_psu_tier(item), price)
    return (0, price)


def query_all(budget=None, platform=None, color=None, rgb=None, limit=5,
              has_price_only=True, include_legacy=False, sort="asc", socket=None,
              chipset=None, memory_gen=None, form_factor=None, max_length=None,
              gpu_cooling="air", gpu_chip=None, min_vram=None, min_capacity=None,
              include_workstation_gpu=False, showcase=None):
    """Return candidates grouped by category for smoke/progressive disclosure."""
    grouped = {}
    for category in CATEGORIES:
        grouped[category] = query(
            category=category,
            budget=budget,
            platform=platform,
            color=color,
            rgb=rgb,
            limit=limit,
            has_price_only=has_price_only,
            include_legacy=include_legacy,
            sort=sort,
            socket=socket,
            chipset=chipset,
            memory_gen=memory_gen,
            form_factor=form_factor,
            max_length=max_length,
            gpu_cooling=gpu_cooling,
            gpu_chip=gpu_chip,
            min_vram=min_vram,
            min_capacity=min_capacity,
            include_workstation_gpu=include_workstation_gpu,
            showcase=showcase if category == "case" else None,
        )
    return grouped


def _summarize_case(case):
    """Extract summary fields from a case record."""
    fan_mounts = case.get("fan_mounts")
    return {
        "id": case.get("id", ""),
        "brand": case.get("brand", ""),
        "model": case.get("model", ""),
        "price_cny": case.get("price_cny"),
        "price_status": case.get("price_status"),
        "price_date": case.get("price_date"),
        "colors": case.get("colors", case.get("color", "")),
        "motherboard_support": case.get("motherboard_support", []),
        "gpu_length_mm": case.get("gpu_length_mm", 0),
        "cpu_cooler_height_mm": case.get("cpu_cooler_height_mm", 0),
        "radiator_support": case.get("radiator_support", []),
        "fan_mounts": fan_mounts,
        "fan_slots_count": parse_fan_slots_count(fan_mounts),
        "psu_support": case.get("psu_support", ["ATX"]),
        "psu_length_mm": case.get("psu_length_mm", 0),
        "is_showcase": case.get("is_showcase", False),
    }


def summarize(item, category=None):
    """Extract only summary fields for progressive disclosure."""
    fields = SUMMARY_FIELDS_BY_CATEGORY.get(category, SUMMARY_BASE_FIELDS)
    summary = {k: item.get(k) for k in fields if item.get(k) is not None}
    if category == "gpu" and infer_gpu_cooling(item) == "liquid":
        summary["gpu_cooling"] = "liquid"
        summary["gpu_radiator_required"] = True
    return summary


def display_extra(category, item):
    """Keep plain-text summaries compact while exposing the key routing field."""
    if category == "mb" and item.get("chipset"):
        return f"chipset={item.get('chipset')}"
    if category == "gpu" and item.get("chip"):
        parts = [f"chip={item.get('chip')}"]
        if item.get("vram_gb"):
            parts.append(f"{item.get('vram_gb')}GB")
        if item.get("memory_bus_bit"):
            parts.append(f"{item.get('memory_bus_bit')}-bit")
        if infer_gpu_cooling(item) == "liquid":
            parts.append("liquid-gpu")
        return " ".join(parts)
    if category == "psu" and item.get("wattage_w"):
        connector = " native16pin" if item.get("native_16pin_gpu_power") else ""
        form = f" {item.get('form_factor')}" if item.get("form_factor") else ""
        length = f" {item.get('length_mm')}mm" if item.get("length_mm") else ""
        return f"{item.get('wattage_w')}W{form}{length}{connector}"
    if category == "memory" and item.get("frequency_mt"):
        timing = f" {item.get('timing')}" if item.get("timing") else ""
        return f"{item.get('generation','')} {item.get('frequency_mt')}MT/s{timing}"
    if category == "storage" and item.get("capacity_tb"):
        return f"{item.get('capacity_tb')}TB {item.get('interface','')}"
    if category == "cooler":
        if item.get("type") == "liquid" and item.get("radiator_mm"):
            return f"liquid {item.get('radiator_mm')}mm"
        if item.get("height_mm"):
            return f"{item.get('type','air')} {item.get('height_mm')}mm"
    if category == "case":
        parts = []
        if item.get("gpu_length_mm"):
            parts.append(f"GPU≤{item.get('gpu_length_mm')}mm")
        if item.get("cpu_cooler_height_mm"):
            parts.append(f"CPU≤{item.get('cpu_cooler_height_mm')}mm")
        if item.get("radiator_support"):
            parts.append("rad=" + "/".join(str(x) for x in item.get("radiator_support")))
        if item.get("fan_slots_count"):
            parts.append(f"fans={item.get('fan_slots_count')}")
        elif should_display_fan_mounts(item.get("fan_mounts")):
            parts.append(f"fans={item.get('fan_mounts')}")
        if item.get("psu_support"):
            parts.append("PSU=" + "/".join(str(x) for x in item.get("psu_support")))
        if item.get("psu_length_mm"):
            parts.append(f"PSU≤{item.get('psu_length_mm')}mm")
        return " ".join(parts)
    return ""


def main():
    parser = argparse.ArgumentParser(description="配件查询工具 (渐进式披露)", allow_abbrev=False)
    parser.add_argument("--category", choices=list(CATEGORIES.keys()) + ["all"],
                        default="all", help="配件品类")
    parser.add_argument("--budget", type=int, help="单品价格上限 (元)，不是整机预算")
    parser.add_argument("--platform", help="平台过滤 (intel/amd)")
    parser.add_argument("--socket", help="CPU/主板 socket 过滤 (LGA1700/AM5/LGA1851)")
    parser.add_argument("--chipset", help="主板芯片组过滤 (B760/B850/X870/Z890 等)")
    parser.add_argument("--memory-gen", help="内存代际过滤 (DDR4/DDR5)，作用于主板和内存")
    parser.add_argument("--form-factor", help="主板/机箱版型过滤 (ATX/M-ATX/ITX)")
    parser.add_argument("--max-length", type=int,
                        help="显卡长度上限；查询机箱时表示需要容纳的显卡长度 (mm)")
    parser.add_argument("--gpu-cooling", choices=["air", "liquid", "any"], default="air",
                        help="显卡散热形态过滤；默认 air，用户明确要水冷显卡时使用 liquid，排查全量候选时使用 any")
    parser.add_argument("--gpu-chip", "--chip", dest="gpu_chip",
                        help="显卡芯片过滤 (RTX5060Ti/RTX5080/RTX5090D V2 等)；--chip 是兼容别名")
    parser.add_argument("--min-vram", type=int,
                        help="显卡最低显存容量 (GB)，例如明确要 RTX 5060 Ti 16GB 时用 --min-vram 16")
    parser.add_argument("--min-capacity", type=int,
                        help="内存最低总容量 (GB)，例如本地 AI/剪辑 64GB 用 --min-capacity 64")
    parser.add_argument("--color", help="颜色过滤 (black/white)")
    parser.add_argument("--rgb", choices=["yes", "no"], help="RGB 过滤")
    parser.add_argument("--showcase", action="store_true", help="只返回海景房机箱")
    parser.add_argument("--sort", choices=["asc", "desc", "tier"], default="asc",
                        help="排序: asc=价格升序(默认), desc=价格降序, tier=显卡芯片/主板芯片组等级优先,同等级按价格升序")
    parser.add_argument("--limit", type=int, default=20, help="最大返回数")
    parser.add_argument("--detail", action="store_true", help="返回完整属性 (默认只返回摘要)")
    parser.add_argument("--json", action="store_true", help="输出 JSON 格式")
    parser.add_argument("--include-legacy", action="store_true", help="包含旧平台/非当前推荐范围条目")
    parser.add_argument("--include-workstation-gpu", action="store_true",
                        help="包含 RTX PRO 6000 等工作站显卡；仅本地大模型/工作站超高预算场景使用")
    args = parser.parse_args()

    if args.category == "all":
        grouped = query_all(
            budget=args.budget,
            platform=args.platform,
            color=args.color,
            rgb=(True if args.rgb == "yes" else False) if args.rgb else None,
            limit=args.limit,
            include_legacy=args.include_legacy,
            sort=args.sort,
            socket=args.socket,
            chipset=args.chipset,
            memory_gen=args.memory_gen,
            form_factor=args.form_factor,
            max_length=args.max_length,
            gpu_cooling=args.gpu_cooling,
            gpu_chip=args.gpu_chip,
            min_vram=args.min_vram,
            min_capacity=args.min_capacity,
            include_workstation_gpu=args.include_workstation_gpu,
            showcase=args.showcase,
        )
        if not args.detail:
            output = {
                category: (items if category == "case" else [summarize(r, category) for r in items])
                for category, items in grouped.items()
            }
        else:
            output = grouped

        if args.json:
            print(json.dumps(output, ensure_ascii=False, indent=2))
        else:
            total = sum(len(items) for items in output.values())
            print(f"查询结果: {total} 条，按品类分组" + (" (摘要模式, 用 --detail 看完整属性)" if not args.detail else ""))
            for category, items in output.items():
                print(f"[{DISPLAY_NAMES.get(category, category)}] {len(items)} 条")
                for r in items:
                    price = f"¥{r.get('price_cny','')}" if r.get("price_cny") else "待补价"
                    color = r.get("colors", r.get("color", ""))
                    showcase_tag = " [海景房]" if r.get("is_showcase") else ""
                    extra = display_extra(category, r)
                    print(f"  {r.get('id',''):45s} {r.get('brand',''):10s} {r.get('model',''):35s} {price:>8s} {color} {extra} {showcase_tag}")
        return

    results = query(
        category=args.category,
        budget=args.budget,
        platform=args.platform,
        color=args.color,
        rgb=(True if args.rgb == "yes" else False) if args.rgb else None,
        limit=args.limit,
        showcase=args.showcase if args.category == "case" else None,
        include_legacy=args.include_legacy,
        sort=args.sort,
        socket=args.socket,
        chipset=args.chipset,
        memory_gen=args.memory_gen,
        form_factor=args.form_factor,
        max_length=args.max_length,
        gpu_cooling=args.gpu_cooling,
        gpu_chip=args.gpu_chip,
        min_vram=args.min_vram,
        min_capacity=args.min_capacity,
        include_workstation_gpu=args.include_workstation_gpu,
    )

    # Progressive disclosure: summary by default, detail only with --detail
    if not args.detail:
        if args.category == "case":
            output = results  # cases already summarized
        else:
            output = [summarize(r, args.category) for r in results]
    else:
        output = results

    if args.json:
        print(json.dumps(output, ensure_ascii=False, indent=2))
    else:
        print(f"查询结果: {len(output)} 条" + (" (摘要模式, 用 --detail 看完整属性)" if not args.detail else ""))
        for r in output:
            if args.category == "case" or not args.detail:
                price = f"¥{r.get('price_cny','')}" if r.get("price_cny") else ""
                color = r.get("colors", r.get("color", ""))
                showcase_tag = " [海景房]" if r.get("is_showcase") else ""
                extra = display_extra(args.category, r)
                print(f"  {r.get('id',''):45s} {r.get('brand',''):10s} {r.get('model',''):35s} {price:>8s} {color} {extra} {showcase_tag}")
            else:
                price = f"¥{r['price_cny']}" if r.get("price_cny") else "待补价"
                print(f"  {r['id']:45s} {r.get('brand',''):12s} {r.get('model',''):40s} {price:>8s}")


if __name__ == "__main__":
    main()
