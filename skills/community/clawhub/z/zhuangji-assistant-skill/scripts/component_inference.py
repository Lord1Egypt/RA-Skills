"""Runtime field inference for bundled component data.

The bundled YAML stays close to imported facts. These helpers add conservative
derived fields from model text and existing connector fields so query and
compatibility scripts do not disagree when source fields are incomplete.
"""

import re
import unicodedata
from dataclasses import dataclass


RGB_TERMS = ("ARGB", "RGB", "幻彩", "炫彩", "彩色", "彩光", "灯效", "灯光", "发光")
NO_RGB_TERMS = ("无光", "不发光")
WATER_TERMS = ("水冷", "一体式", "冷排", "AIO", "LIQUID", "WATER")
COOLER_LIQUID_FAMILY_TERMS = (
    "FROZEN PRISM", "冰封棱镜", "冰霜护甲", "FROZEN INFINITY", "冰封无限",
    "LG600", "LG700", "LX800", "A080", "A090", "冰封幻境", "龙神3",
    "冰神", "冰魔方", "冰雕", "PA 420", "CORE MATRIX", "M25黑旋风", "冰刃A13",
    "冰暴", "凌霜", "寒冰I", "山河S360", "风擎视界", "木语360",
    "星凰X360", "星渊", "C240 VALKYRIE", "C480", "酷凛 FX120", "巨浪120", "寒战120",
)
COOLER_RADIATOR_PATTERN = re.compile(r"(?<!\d)(120|240|280|360|420|480)(?!\d)")
COOLER_EXCLUSIVE_PLATFORM_PATTERN = re.compile(
    r"(?P<platform>AMD|INTEL|英特尔)\s*(?:平台)?(?:专用|版本|可用|适用)"
    r"|(?:专用|版本|可用|适用|仅支持)\s*(?P<reverse>AMD|INTEL|英特尔)",
    re.IGNORECASE,
)
COOLER_LIQUID_SERIES_RADIATOR_PATTERNS = (
    (re.compile(r"(?<![A-Z0-9])(?:V36|GL36)(?![A-Z0-9])", re.IGNORECASE), 360),
    (re.compile(r"(?<![A-Z0-9])XW36(?:SD|S)?(?!\d)", re.IGNORECASE), 360),
    (re.compile(r"(?<![A-Z0-9])H150(?![A-Z0-9])", re.IGNORECASE), 360),
    (re.compile(r"(?<![A-Z0-9])H100(?![A-Z0-9])", re.IGNORECASE), 240),
    (re.compile(r"龙王4代", re.IGNORECASE), 360),
)
AXP90_TOTAL_HEIGHT_PATTERN = re.compile(r"(?<![A-Z0-9])AXP90[- ]?X(36|47|53)(?!\d)", re.IGNORECASE)
LOW_PROFILE_COOLER_PATTERN = re.compile(
    r"(?<![A-Z0-9])AXP90|LOW\s*PROFILE|TOP[- ]?DOWN|DOWN[- ]?DRAFT|下压",
    re.IGNORECASE,
)
AIR_COOLER_LAYOUT_PATTERNS = (
    ("dual_tower", re.compile(r"DUAL\s*TOWER|双塔", re.IGNORECASE)),
    ("single_tower", re.compile(r"SINGLE\s*TOWER|单塔", re.IGNORECASE)),
)
HEATPIPE_COUNT_PATTERN = re.compile(r"(?<!\d)(\d{1,2})\s*(?:热管|铜管|HEAT\s*PIPES?)", re.IGNORECASE)
CHINESE_HEATPIPE_COUNT_PATTERN = re.compile(r"([一二三四五六七八九十])\s*(?:热管|铜管)")
CHINESE_HEATPIPE_COUNTS = {
    "一": 1, "二": 2, "三": 3, "四": 4, "五": 5,
    "六": 6, "七": 7, "八": 8, "九": 9, "十": 10,
}

THERMAL_LOW = 0
THERMAL_MAINSTREAM = 1
THERMAL_STRONG = 2
THERMAL_HIGH = 3


@dataclass(frozen=True)
class CoolerThermalProfile:
    """Conservative structural evidence used by query and compatibility gates."""

    rank: int | None
    label: str
    evidence: tuple[str, ...] = ()


def infer_cooler_exclusive_platform(item):
    """Read an explicit single-platform SKU label; ordinary support claims are not exclusive."""
    model = unicodedata.normalize("NFKC", str((item or {}).get("model") or ""))
    platforms = {
        "intel" if (match.group("platform") or match.group("reverse")).lower() == "英特尔"
        else (match.group("platform") or match.group("reverse")).lower()
        for match in COOLER_EXCLUSIVE_PLATFORM_PATTERN.finditer(model)
    }
    return next(iter(platforms)) if len(platforms) == 1 else None


MEMORY_DDR_FREQUENCY_PATTERN = re.compile(
    r"(?<![A-Z0-9])DDR\s*([45])\s*[-_/]?\s*(\d{4,5})(?:\s*(?:MHZ|MT/S|MTPS|频))?(?!\d)",
    re.IGNORECASE,
)
MEMORY_FREQUENCY_SUFFIX_PATTERN = re.compile(
    r"(?<!\d)(\d{4,5})\s*(?:MHZ|MT/S|MTPS|频率|频)(?![A-Z0-9])",
    re.IGNORECASE,
)
MEMORY_DDR_MULTI_FREQUENCY_PATTERN = re.compile(
    r"(?<![A-Z0-9])DDR\s*([45])(?:\s*[-_])?\s*((?:\d{4,5})(?:\s*[/|,，、~～至-]\s*\d{4,5})+)",
    re.IGNORECASE,
)
INTEL_UNLOCKED_CPU_PATTERN = re.compile(
    r"(?<![A-Z0-9])(?:INTEL\s+)?(?:CORE\s+)?I[579][ -]?(12600|12700|12900|13600|13700|13900|14600|14700|14900)(?:K|KF|KS)(?![A-Z0-9])",
    re.IGNORECASE,
)
# Combined storefront titles such as ``14400K/KF`` and ``7500X/F`` are
# ambiguous physical SKUs.  If any listed alternative is an F/KF variant, the
# title cannot prove that an iGPU is present and must stay out of no-GPU builds.
CPU_NO_IGPU_ALTERNATIVE_PATTERN = re.compile(
    r"(?<![A-Z0-9])\d{3,5}(?:[A-Z0-9]\s*)*(?:[/|、]|OR|或)\s*"
    r"(?:\d{3,5}\s*)?(?:[A-Z]\s*)*F(?=$|[^A-Z0-9])",
    re.IGNORECASE,
)
CPU_NO_IGPU_SUFFIX_PATTERN = re.compile(
    r"(?<![A-Z0-9])\d{3,5}\s*(?:[KX]\s*)?F(?=$|[^A-Z0-9])",
    re.IGNORECASE,
)
# Intel Maximum Turbo Power values used as conservative runtime floors when a
# market snapshot has accidentally copied the lower Processor Base Power.
INTEL_UNLOCKED_CPU_POWER_FLOORS_W = {
    "12600": 150,
    "12700": 190,
    "12900": 241,
    "13600": 181,
    "13700": 253,
    "13900": 253,
    "14600": 181,
    "14700": 253,
    "14900": 253,
}
GPU_RTX_3060_12GB_PATTERN = re.compile(
    r"(?<!\d)(?:RTX\s*)?3060\s*[- ]?\s*12\s*G(?:B)?(?!\d)",
    re.IGNORECASE,
)
GPU_LIQUID_TERMS = (
    "水冷", "水神", "水雕", "水超龙", "水夜神", "NEPTUNE",
    "WATERFORCE", "LIQUID", "ASTRAL LC", "SUPRIM LIQUID",
)
GPU_VRAM_PATTERN = re.compile(
    r"(?<!\d)(?:O)?(96|48|32|24|20|16|12|10|8|6|4)\s*G(?:B)?(?!\d)"
)
MEMORY_GENERATION_TOKEN_PATTERN = re.compile(
    r"(?<![A-Z0-9])DDR\s*([345])(?![0-9])", re.IGNORECASE
)
STORAGE_M2_FORM_PATTERN = re.compile(
    r"(?<![A-Z0-9])(?:M\s*[.\-]?\s*2|NGFF)(?![A-Z0-9])",
    re.IGNORECASE,
)
STORAGE_M2_SIZE_PATTERN = re.compile(
    r"(?<![A-Z0-9])(?:M\s*[.\-]?\s*2|NGFF)\s*[-/]?\s*(2230|2242|2260|2280|22110)(?![A-Z0-9])",
    re.IGNORECASE,
)
STORAGE_MSATA_FORM_PATTERN = re.compile(
    r"(?<![A-Z0-9])M\s*[-.]?\s*SATA(?![A-Z0-9])", re.IGNORECASE
)
STORAGE_ROTATIONAL_PATTERN = re.compile(
    r"(?<!\d)(?:5400|7200)\s*(?:转|RPM)(?![A-Z0-9])|机械硬盘", re.IGNORECASE
)
STORAGE_SATA_SSD_SPEED_PATTERN = re.compile(
    r"(?<!\d)(?:4\d{2}|5\d{2}|6[0-5]\d)\s*MB/S", re.IGNORECASE
)
STORAGE_BAY_FORM_PATTERN = re.compile(
    r"(?<!\d)(2\.5|3\.5)\s*[-/]?\s*"
    r"(?:(?:IN(?:CH)?|英寸|[\"'])|SATA|SSD|HDD|DRIVE|硬盘|固态)",
    re.IGNORECASE,
)
STORAGE_U2_FORM_PATTERN = re.compile(
    r"(?<![A-Z0-9])U\s*[.\-]?\s*2(?![A-Z0-9])", re.IGNORECASE
)
STORAGE_SOLID_STATE_TYPES = {"SSD", "TLC", "QLC"}
USER_CONFIRMED_SPEC_FIELDS = "_user_confirmed_spec_fields"
PSU_NATIVE_16PIN_TERMS = (
    "ATX3.0", "ATX 3.0", "ATX3.1", "ATX 3.1",
    "PCIE5", "PCI-E5", "PCI-E 5", "PCIe5", "PCIe 5",
    "12VHPWR", "12V-2X6", "12V2X6", "16PIN", "16 PIN", "原生16",
)
PSU_NATIVE_NEGATIVE_TERMS = ("转接线", "转接", "不带16", "无16")


def _text(item):
    return " ".join(str(item.get(k, "")) for k in ("brand", "model", "id", "series"))


def _upper(item):
    return _text(item).upper().replace("－", "-")


_DISPLAY_OUTPUT_PATTERNS = (
    ("HDMI", re.compile(r"^(?:\d+\s*[X×]\s*)?HDMI(?:\s*(?:PORT)?\s*\d+(?:\.\d+)?)?$", re.IGNORECASE)),
    ("DisplayPort", re.compile(r"^(?:\d+\s*[X×]\s*)?(?:DISPLAYPORT|DP)(?:\s*\d+(?:\.\d+)?)?$", re.IGNORECASE)),
    ("VGA", re.compile(r"^(?:\d+\s*[X×]\s*)?(?:VGA|D[- ]?SUB)$", re.IGNORECASE)),
    ("DVI", re.compile(r"^(?:\d+\s*[X×]\s*)?DVI(?:-[DIA])?$", re.IGNORECASE)),
    ("USB-C", re.compile(r"^(?:\d+\s*[X×]\s*)?USB(?:\s*TYPE)?[- ]?C(?:\s*(?:DISPLAYPORT|DP)\s*ALT\s*MODE)?$", re.IGNORECASE)),
    ("Thunderbolt", re.compile(r"^(?:\d+\s*[X×]\s*)?THUNDERBOLT(?:\s*[1-5])?$", re.IGNORECASE)),
)


def normalize_display_output(value):
    """Return a canonical motherboard display connector or None."""
    text = str(value or "").strip()
    for canonical, pattern in _DISPLAY_OUTPUT_PATTERNS:
        if pattern.fullmatch(text):
            return canonical
    return None


def normalize_display_outputs(values):
    """Normalize a display-output list, rejecting the whole field if any value is invalid."""
    if not isinstance(values, list) or not values:
        return []
    normalized = [normalize_display_output(value) for value in values]
    if any(value is None for value in normalized):
        return []
    return normalized


def infer_cpu_integrated_graphics(item):
    """Return True/False when a desktop CPU's integrated graphics are known.

    Explicit data wins. Model inference is deliberately conservative so an
    unknown SKU cannot satisfy a no-discrete-GPU build by accident.
    """
    for field in ("integrated_graphics", "has_integrated_graphics", "igpu"):
        if field not in item or item.get(field) is None:
            continue
        value = item.get(field)
        if isinstance(value, bool):
            return value
        text = str(value).strip().lower()
        if text in ("true", "yes", "y", "1", "有", "支持", "核显", "集显"):
            return True
        if text in ("false", "no", "n", "0", "无", "不支持", "none", "no igpu"):
            return False

    text = unicodedata.normalize("NFKC", _upper(item))
    compact = re.sub(r"[^A-Z0-9\u4e00-\u9fff]+", "", text)
    if "INTEL" in text or "CORE" in text or compact.startswith(("I3", "I5", "I7", "I9", "U5", "U7", "U9")):
        # Intel desktop F/KF suffix SKUs disable integrated graphics.
        if CPU_NO_IGPU_ALTERNATIVE_PATTERN.search(text) or CPU_NO_IGPU_SUFFIX_PATTERN.search(text):
            return False
        return True

    if "AMD" in text or "RYZEN" in text:
        if CPU_NO_IGPU_ALTERNATIVE_PATTERN.search(text) or CPU_NO_IGPU_SUFFIX_PATTERN.search(text):
            return False
        if re.search(r"(?<![A-Z0-9])\d{4,5}\s*(?:GE|GT|G)(?=$|[^A-Z0-9])", text):
            return True
        match = re.search(
            r"(?<![A-Z0-9])(?:RYZEN\s+\d\s*)?(\d{4,5})\s*(?:X3D|X)?(?=$|[^A-Z0-9])",
            text,
        )
        if match:
            return int(match.group(1)) >= 7000
    return None


def infer_cpu_conservative_power_w(item):
    """Return the higher of recorded power and a controlled unlocked-CPU floor."""
    raw = item.get("power_w")
    if isinstance(raw, bool):
        recorded = 0
    else:
        try:
            recorded = float(raw or 0)
        except (TypeError, ValueError):
            recorded = 0
    model = str(item.get("model") or "")
    match = INTEL_UNLOCKED_CPU_PATTERN.search(model)
    floor = INTEL_UNLOCKED_CPU_POWER_FLOORS_W.get(match.group(1), 0) if match else 0
    effective = max(recorded, floor)
    if effective <= 0:
        return None
    return int(effective) if float(effective).is_integer() else effective


def infer_cpu_required_thermal_rank(item):
    """Return a conservative cooler tier without treating every boost ceiling as a K-SKU."""
    power_w = infer_cpu_conservative_power_w(item)
    if power_w is None:
        return None
    if power_w <= 65:
        return THERMAL_LOW
    model = str(item.get("model") or "")
    if INTEL_UNLOCKED_CPU_PATTERN.search(model):
        return THERMAL_STRONG if power_w <= 150 else THERMAL_HIGH
    if power_w <= 150:
        return THERMAL_MAINSTREAM
    return THERMAL_HIGH


def infer_rgb(item):
    """Infer RGB from explicit field and common model keywords."""
    text = _upper(item)
    if any(term.upper() in text for term in NO_RGB_TERMS):
        return False
    if any(term.upper() in text for term in RGB_TERMS):
        return True
    value = item.get("rgb")
    return value if value is not None else False


def infer_timing(item):
    """Infer memory timing like C30/CL30 from model text."""
    value = str(item.get("timing") or "").strip()
    if value:
        return value
    match = re.search(r"\bC(?:L)?\s*([1-4]\d)\b", _upper(item))
    return f"C{match.group(1)}" if match else value


def infer_pcie_generation(item):
    """Infer PCIe generation from interface/model text."""
    value = item.get("pcie_generation")
    if value:
        return value
    text = _upper(item)
    match = re.search(r"PCIE\s*([345])(?:\.0)?|PCI-E\s*([345])(?:\.0)?|GEN\s*([345])", text)
    if match:
        for group in match.groups():
            if group:
                return int(group)
    return value


def infer_capacity_gb(item):
    """Infer storage capacity in GB, preferring explicit model text over noisy fields."""
    text = _upper(item)
    match = re.search(r"(?<![A-Z0-9])(\d+(?:\.\d+)?)\s*T(?:B)?(?![A-Z0-9])", text)
    if match:
        return int(float(match.group(1)) * 1024)
    match = re.search(r"(?<![A-Z0-9])(\d{3,4})\s*G(?:B)?(?![A-Z0-9])", text)
    if match:
        return int(match.group(1))
    value = item.get("capacity_gb")
    if value:
        return value
    tb = item.get("capacity_tb")
    if tb:
        try:
            return int(float(tb) * 1024)
        except (TypeError, ValueError):
            pass
    return value


def infer_memory_capacity_gb(item):
    """Infer memory kit total capacity from model text before trusting noisy fields."""
    text = _upper(item).replace("×", "X")
    total_match = re.search(r"(?<!\d)(\d{1,3})\s*G(?:B)?\s*(?:\(|DDR|D[45]|$)", text)
    if total_match:
        total = int(total_match.group(1))
        if 4 <= total <= 256:
            return total
    kit_match = re.search(r"(?<!\d)(\d{1,3})\s*G(?:B)?\s*[X*]\s*(\d)(?!\d)", text)
    if kit_match:
        total = int(kit_match.group(1)) * int(kit_match.group(2))
        if 4 <= total <= 256:
            return total
    return item.get("capacity_gb")


def normalize_memory_generation(value):
    """Canonicalize one memory generation without hiding conflicting values."""
    text = unicodedata.normalize("NFKC", str(value or "")).strip().upper()
    matches = {
        f"DDR{match.group(1)}"
        for match in MEMORY_GENERATION_TOKEN_PATTERN.finditer(text)
    }
    if len(matches) == 1:
        return matches.pop()
    return re.sub(r"\s+", " ", text)


def normalize_memory_generations(values):
    """Expand a board's DDR support list and canonicalize common labels."""
    if values in (None, "", [], (), {}):
        return []
    raw_values = list(values) if isinstance(values, (list, tuple, set)) else [values]
    result = []
    for value in raw_values:
        text = unicodedata.normalize("NFKC", str(value or "")).strip().upper()
        matches = [
            f"DDR{match.group(1)}"
            for match in MEMORY_GENERATION_TOKEN_PATTERN.finditer(text)
        ]
        normalized = matches or ([re.sub(r"\s+", " ", text)] if text else [])
        for generation in normalized:
            if generation not in result:
                result.append(generation)
    return result


def infer_memory_module_count(item):
    """Infer memory module count from common kit notation such as 32Gx2."""
    text = _upper(item).replace("×", "X")
    kit_match = re.search(r"(?<!\d)\d{1,3}\s*G(?:B)?\s*[X*]\s*(\d)(?!\d)", text)
    if kit_match:
        count = int(kit_match.group(1))
        if 1 <= count <= 8:
            return count
    return item.get("module_count")


def infer_explicit_memory_frequency_mt(item):
    """Return one unambiguous DDR frequency written in the model, or None."""
    text = str(item.get("model") or "").upper().replace("－", "-")
    ddr_matches = list(MEMORY_DDR_FREQUENCY_PATTERN.finditer(text))
    declared_generation = normalize_memory_generation(item.get("generation")).replace(" ", "")
    if declared_generation and any(
        declared_generation != f"DDR{match.group(1)}" for match in ddr_matches
    ):
        return None
    candidates = {int(match.group(2)) for match in ddr_matches}
    candidates.update(int(match.group(1)) for match in MEMORY_FREQUENCY_SUFFIX_PATTERN.finditer(text))
    for match in MEMORY_DDR_MULTI_FREQUENCY_PATTERN.finditer(text):
        if declared_generation and declared_generation != f"DDR{match.group(1)}":
            return None
        candidates.update(int(value) for value in re.findall(r"\d{4,5}", match.group(2)))
    if len(candidates) != 1:
        return None
    value = candidates.pop()
    return value if 1600 <= value <= 12000 else None


def infer_requires_16pin_gpu(item):
    """Infer whether a GPU needs a 16pin/12VHPWR style connector."""
    connectors = item.get("power_connectors") or []
    connector_text = " ".join(str(c).upper() for c in connectors)
    if any(term in connector_text for term in ("16PIN", "12VHPWR", "12V-2X6", "12V2X6")):
        return True
    value = item.get("requires_16pin_psu")
    return value if value is not None else False


def infer_gpu_cooling(item):
    """Infer GPU cooler style. Only explicit water/liquid model terms become liquid."""
    value = item.get("gpu_cooling")
    if value:
        return value
    text = _upper(item)
    if any(term.upper() in text for term in GPU_LIQUID_TERMS):
        return "liquid"
    return "air"


def infer_gpu_vram(item):
    """Infer explicit GPU VRAM from model text, including O16G/O8G vendor naming."""
    text = _upper(item)
    matches = [int(match.group(1)) for match in GPU_VRAM_PATTERN.finditer(text)]
    if matches:
        return max(matches)
    return item.get("vram_gb")


def infer_explicit_gpu_chip(item):
    """Infer only a model token that is incompatible with the current chip label."""
    text = str(item.get("model") or "").upper()
    if GPU_RTX_3060_12GB_PATTERN.search(text) and not re.search(r"3060\s*TI", text):
        return "RTX 3060"
    return None


def infer_native_16pin_psu(item):
    """Infer PSU native 16pin support.

    Returns True/False/None. None means source data and model text are
    insufficient, so compatibility should be a复核项 rather than a hard warning.
    """
    if "native_16pin_gpu_power" in item and item.get("native_16pin_gpu_power") is not None:
        explicit = item.get("native_16pin_gpu_power")
        if explicit in (True, "true", "True", 1):
            return True
        if explicit in (False, "false", "False", 0):
            return False
    text = _upper(item)
    if any(term.upper() in text for term in PSU_NATIVE_NEGATIVE_TERMS):
        return False
    if any(term.upper() in text for term in PSU_NATIVE_16PIN_TERMS):
        return True
    return None


def infer_modular(item):
    """Infer PSU modular cable design from model text when explicit text exists."""
    text = _text(item)
    if "非模组" in text:
        return False
    if "全模组" in text or "全模" in text or "半模组" in text or "半模" in text:
        return True
    return item.get("modular")


def infer_psu_form_factor(item):
    """Prefer an explicit small-form-factor token over a conflicting imported field."""
    text = _upper(item)
    if re.search(r"(?<![A-Z0-9])SFX[- ]?L(?![A-Z0-9])", text):
        return "SFX-L"
    if re.search(r"(?<![A-Z0-9])SFX(?![A-Z0-9])", text):
        return "SFX"
    if re.search(r"(?<![A-Z0-9])FLEX(?![A-Z0-9])", text):
        return "FLEX"
    if re.search(r"(?<![A-Z0-9])TFX(?![A-Z0-9])", text):
        return "TFX"
    return normalize_psu_form_factor(item.get("form_factor"))


def normalize_psu_form_factor(value):
    """Canonicalize a PSU enclosure form while ignoring ATX revision suffixes."""
    text = unicodedata.normalize("NFKC", str(value or "")).strip()
    compact = re.sub(r"[\s._-]+", "", text.upper())
    if re.fullmatch(r"ATX(?:3(?:\d+)?)?", compact):
        return "ATX"
    if re.fullmatch(r"SFX(L)?(?:4(?:\d+)?)?", compact):
        return "SFX-L" if re.fullmatch(r"SFXL.*", compact) else "SFX"
    if compact in {"TFX", "FLEX"}:
        return compact
    return text


def infer_explicit_cooler_radiator_mm(item):
    """Return a radiator size only from structured data or controlled AIO model evidence."""
    text = _upper(item)
    try:
        explicit_radiator = int(item.get("radiator_mm") or 0)
    except (TypeError, ValueError):
        explicit_radiator = 0
    if explicit_radiator in {120, 240, 280, 360, 420, 480}:
        return explicit_radiator
    radiator_match = COOLER_RADIATOR_PATTERN.search(text)
    if radiator_match and any(
        term.upper() in text for term in WATER_TERMS + COOLER_LIQUID_FAMILY_TERMS
    ):
        return int(radiator_match.group(1))
    for pattern, size in COOLER_LIQUID_SERIES_RADIATOR_PATTERNS:
        if pattern.search(text):
            return size
    return None


def infer_cooler_type(item):
    """Infer air/liquid cooler type from model text and structured radiator data."""
    text = _upper(item)
    if infer_explicit_cooler_radiator_mm(item) is not None:
        return "liquid"
    if any(term.upper() in text for term in WATER_TERMS):
        return "liquid"
    return item.get("type") or "air"


def _positive_number(value):
    if isinstance(value, bool):
        return None
    try:
        number = float(value)
    except (TypeError, ValueError):
        return None
    return number if number > 0 else None


def infer_air_cooler_layout(item):
    """Return a controlled air-cooler layout from explicit data or model text."""
    explicit = str(item.get("air_cooler_layout") or "").strip().lower().replace("-", "_")
    if explicit in {"low_profile", "down_draft", "single_tower", "dual_tower"}:
        return explicit
    text = _text(item)
    if LOW_PROFILE_COOLER_PATTERN.search(text):
        return "low_profile"
    for layout, pattern in AIR_COOLER_LAYOUT_PATTERNS:
        if pattern.search(text):
            return layout
    return None


def infer_heatpipe_count(item):
    """Return a plausible heat-pipe count without treating unrelated numbers as evidence."""
    explicit = _positive_number(item.get("heatpipe_count"))
    if explicit is not None and explicit.is_integer() and explicit <= 16:
        return int(explicit)
    text = _text(item)
    match = HEATPIPE_COUNT_PATTERN.search(text)
    if match:
        count = int(match.group(1))
        return count if 1 <= count <= 16 else None
    match = CHINESE_HEATPIPE_COUNT_PATTERN.search(text)
    return CHINESE_HEATPIPE_COUNTS.get(match.group(1)) if match else None


def infer_cooler_thermal_profile(item):
    """Classify only evidenced cooler structure; unknown facts remain unknown."""
    cooler_type = infer_cooler_type(item)
    if cooler_type == "liquid":
        radiator = infer_explicit_cooler_radiator_mm(item)
        if radiator is None:
            return CoolerThermalProfile(None, "水冷冷排尺寸未知")
        if radiator >= 360:
            return CoolerThermalProfile(THERMAL_HIGH, f"{radiator}mm水冷", (f"radiator_mm={radiator}",))
        if radiator >= 240:
            return CoolerThermalProfile(THERMAL_STRONG, f"{radiator}mm水冷", (f"radiator_mm={radiator}",))
        return CoolerThermalProfile(THERMAL_MAINSTREAM, f"{radiator}mm水冷", (f"radiator_mm={radiator}",))

    if cooler_type != "air":
        return CoolerThermalProfile(None, "散热类型未知")

    layout = infer_air_cooler_layout(item)
    height = _positive_number(item.get("height_mm"))
    if layout in {"low_profile", "down_draft"} or (height is not None and height <= 80):
        evidence = tuple(
            value for value in (
                f"layout={layout}" if layout else None,
                f"height_mm={height:g}" if height is not None else None,
            ) if value
        )
        return CoolerThermalProfile(THERMAL_LOW, "低矮/下压风冷", evidence)

    heatpipes = infer_heatpipe_count(item)
    evidence = tuple(
        value for value in (
            f"layout={layout}" if layout else None,
            f"heatpipe_count={heatpipes}" if heatpipes else None,
        ) if value
    )
    if layout == "dual_tower" and heatpipes is not None and heatpipes >= 6:
        return CoolerThermalProfile(THERMAL_STRONG, "双塔六热管级风冷", evidence)
    if layout in {"single_tower", "dual_tower"} and heatpipes is not None and heatpipes >= 4:
        return CoolerThermalProfile(THERMAL_MAINSTREAM, "塔式四热管级风冷", evidence)
    return CoolerThermalProfile(None, "风冷结构证据不足", evidence)


def infer_explicit_cooler_height_mm(item):
    """Return the installed AXP90-X cooler height encoded by the exact SKU."""
    text = " ".join(str(item.get(key, "")) for key in ("model", "id"))
    match = AXP90_TOTAL_HEIGHT_PATTERN.search(text)
    return int(match.group(1)) if match else None


def infer_radiator_mm(item):
    """Infer AIO radiator size from model text."""
    if infer_cooler_type(item) != "liquid":
        return item.get("radiator_mm")
    return infer_explicit_cooler_radiator_mm(item)


def normalize_explicit_storage_form_factor(value):
    """Canonicalize a user-confirmed desktop storage shape, or return None.

    This deliberately accepts only physical form-factor evidence.  A bare
    ``SATA`` token is an interface, not a shape, and therefore cannot satisfy
    this contract.
    """
    text = unicodedata.normalize("NFKC", str(value or "")).strip()
    if not text:
        return None
    if STORAGE_MSATA_FORM_PATTERN.fullmatch(text):
        return "mSATA"
    m2_match = re.fullmatch(
        r"(?:M\s*[.\-]?\s*2|NGFF)(?:\s*[-/]?\s*(2230|2242|2260|2280|22110))?",
        text,
        flags=re.IGNORECASE,
    )
    if m2_match:
        size = m2_match.group(1)
        return f"M.2 {size}" if size else "M.2"
    sata_shape = re.fullmatch(
        r"(?:(2\.5|3\.5)(?:\s*(?:IN(?:CH)?|英寸|[\"']))?\s*SATA|"
        r"SATA\s*(2\.5|3\.5)(?:\s*(?:IN(?:CH)?|英寸|[\"']))?)",
        text,
        flags=re.IGNORECASE,
    )
    if sata_shape:
        size = sata_shape.group(1) or sata_shape.group(2)
        return f"{size} SATA"
    return None


def _explicit_storage_text_shapes(value, *, include_u2=False):
    """Return physical shapes explicitly written in storage text."""
    text = unicodedata.normalize("NFKC", str(value or ""))
    shapes = set()
    if STORAGE_MSATA_FORM_PATTERN.search(text):
        shapes.add("mSATA")
    m2_size = STORAGE_M2_SIZE_PATTERN.search(text)
    if m2_size:
        shapes.add(f"M.2 {m2_size.group(1)}")
    elif STORAGE_M2_FORM_PATTERN.search(text):
        shapes.add("M.2")
    bay = STORAGE_BAY_FORM_PATTERN.search(text)
    if bay:
        shapes.add(f"{bay.group(1)} SATA")
    if include_u2 and STORAGE_U2_FORM_PATTERN.search(text):
        shapes.add("U.2")
    return shapes


def infer_explicit_storage_model_form_factor(model):
    """Return one unambiguous physical shape stated by model text."""
    shapes = _explicit_storage_text_shapes(model, include_u2=True)
    return next(iter(shapes)) if len(shapes) == 1 else None


def _storage_shape_evidence_matches(evidence, supplied_shape):
    if evidence == "M.2":
        return supplied_shape.startswith("M.2")
    if evidence == "U.2":
        return supplied_shape == "2.5 SATA"
    return evidence == supplied_shape


def storage_model_form_factor_consistent(model, form_factor):
    """Compare user shape data with explicit model-text shape evidence."""
    if not str(form_factor or "").strip():
        return None
    model_shapes = _explicit_storage_text_shapes(model, include_u2=True)
    if not model_shapes:
        return None
    supplied_shape = normalize_explicit_storage_form_factor(form_factor)
    if supplied_shape is None:
        return False
    return all(
        _storage_shape_evidence_matches(evidence, supplied_shape)
        for evidence in model_shapes
    )


def storage_interface_form_factor_consistent(interface, form_factor):
    """Return whether two explicit storage facts describe a supported shape.

    ``None`` means one side is absent and no pair can be judged.  ``False``
    includes unknown interface families so overlay import fails closed rather
    than silently accepting an uncheckable combination.
    """
    if not str(interface or "").strip() or not str(form_factor or "").strip():
        return None
    shape = normalize_explicit_storage_form_factor(form_factor)
    if shape is None:
        return False
    text = unicodedata.normalize("NFKC", str(interface)).upper()
    interface_shapes = _explicit_storage_text_shapes(text, include_u2=True)
    if interface_shapes and not all(
        _storage_shape_evidence_matches(evidence, shape)
        for evidence in interface_shapes
    ):
        return False
    if STORAGE_MSATA_FORM_PATTERN.search(text):
        interface_family = "msata"
    elif "USB" in text:
        interface_family = "usb"
    elif STORAGE_M2_FORM_PATTERN.search(text):
        interface_family = "m2"
    elif "NVME" in text or re.search(r"PCI\s*[-.]?\s*E", text):
        interface_family = "pcie"
    elif "SATA" in text:
        interface_family = "sata"
    else:
        interface_family = "unknown"

    if shape.startswith("M.2"):
        return interface_family in {"m2", "pcie", "sata"}
    if shape == "mSATA":
        return interface_family in {"msata", "sata"}
    if shape in {"2.5 SATA", "3.5 SATA"}:
        return interface_family == "sata"
    return False


def infer_storage_form_factor(item):
    """Infer only explicit desktop SATA/M.2 shapes from model and catalog facts.

    A historical importer assigned ``M.2 2280`` to every SATA drive.  SATA
    alone does not prove an M.2 device, so rotational desktop drives and
    ordinary SATA SSD titles are classified separately while ambiguous titles
    remain unknown instead of consuming a fictitious M.2 slot.
    """
    confirmed_fields = set(item.get(USER_CONFIRMED_SPEC_FIELDS) or ())
    if "form_factor" in confirmed_fields:
        return normalize_explicit_storage_form_factor(item.get("form_factor"))

    interface = unicodedata.normalize("NFKC", str(item.get("interface") or "")).upper()
    model = unicodedata.normalize("NFKC", str(item.get("model") or ""))
    form_factor_text = unicodedata.normalize("NFKC", str(item.get("form_factor") or ""))
    storage_type = str(item.get("storage_type") or "").strip()
    interface_is_msata = bool(STORAGE_MSATA_FORM_PATTERN.search(interface))
    interface_is_m2 = bool(STORAGE_M2_FORM_PATTERN.search(interface))
    model_is_msata = bool(STORAGE_MSATA_FORM_PATTERN.search(model))
    model_is_m2 = bool(STORAGE_M2_FORM_PATTERN.search(model))
    size_match = next(
        (
            match
            for text in (interface, form_factor_text, model)
            if (match := STORAGE_M2_SIZE_PATTERN.search(text))
        ),
        None,
    )
    if interface_is_msata or model_is_msata:
        return "mSATA"
    if interface_is_m2:
        return f"M.2 {size_match.group(1)}" if size_match else "M.2 2280"
    if "SATA" in interface:
        if model_is_m2:
            return f"M.2 {size_match.group(1)}" if size_match else "M.2 2280"
        if storage_type == "台式机硬盘" or STORAGE_ROTATIONAL_PATTERN.search(model):
            return "3.5 SATA"
        if (
            storage_type in STORAGE_SOLID_STATE_TYPES
            or "SSD" in model.upper()
            or STORAGE_SATA_SSD_SPEED_PATTERN.search(model)
        ):
            return "2.5 SATA"
        return None
    if "NVME" in interface:
        return f"M.2 {size_match.group(1)}" if size_match else "M.2 2280"
    return None


def enrich_item(section, item):
    """Return a shallow enriched copy for query/compatibility scripts."""
    enriched = dict(item)
    if section == "cpus":
        power_w = infer_cpu_conservative_power_w(enriched)
        if power_w is not None:
            enriched["power_w"] = power_w
        integrated_graphics = infer_cpu_integrated_graphics(enriched)
        if integrated_graphics is not None:
            enriched["integrated_graphics"] = integrated_graphics
    elif section == "memory":
        timing = infer_timing(enriched)
        if timing:
            enriched["timing"] = timing
        capacity_gb = infer_memory_capacity_gb(enriched)
        if capacity_gb:
            enriched["capacity_gb"] = capacity_gb
        module_count = infer_memory_module_count(enriched)
        if module_count:
            enriched["module_count"] = module_count
    elif section == "storage":
        gen = infer_pcie_generation(enriched)
        if gen:
            enriched["pcie_generation"] = gen
        capacity_gb = infer_capacity_gb(enriched)
        if capacity_gb:
            enriched["capacity_gb"] = capacity_gb
        form_factor = infer_storage_form_factor(enriched)
        if form_factor:
            enriched["form_factor"] = form_factor
        elif (
            "SATA" in str(enriched.get("interface") or "").upper()
            and "M.2" in str(enriched.get("form_factor") or "").upper()
        ):
            enriched.pop("form_factor", None)
    elif section == "gpus":
        vram = infer_gpu_vram(enriched)
        if vram:
            enriched["vram_gb"] = vram
        enriched["requires_16pin_psu"] = infer_requires_16pin_gpu(enriched)
        gpu_cooling = infer_gpu_cooling(enriched)
        if gpu_cooling == "liquid":
            enriched["gpu_cooling"] = gpu_cooling
            enriched["gpu_radiator_required"] = True
    elif section == "coolers":
        enriched["type"] = infer_cooler_type(enriched)
        height = infer_explicit_cooler_height_mm(enriched)
        if height and enriched["type"] == "air":
            enriched["height_mm"] = height
        radiator = infer_radiator_mm(enriched)
        if radiator:
            enriched["radiator_mm"] = radiator
        enriched["rgb"] = infer_rgb(enriched)
    elif section == "psus":
        form_factor = infer_psu_form_factor(enriched)
        if form_factor:
            enriched["form_factor"] = form_factor
        native = infer_native_16pin_psu(enriched)
        if native is not None:
            enriched["native_16pin_gpu_power"] = native
        modular = infer_modular(enriched)
        if modular is not None:
            enriched["modular"] = modular
    return enriched
