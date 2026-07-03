"""Runtime field inference for bundled component data.

The bundled YAML stays close to imported facts. These helpers add conservative
derived fields from model text and existing connector fields so query and
compatibility scripts do not disagree when source fields are incomplete.
"""

import re


RGB_TERMS = ("ARGB", "RGB", "幻彩", "炫彩", "彩色", "彩光", "灯效", "灯光", "发光")
NO_RGB_TERMS = ("无光", "不发光")
WATER_TERMS = ("水冷", "一体式", "冷排", "AIO", "LIQUID", "WATER")
GPU_LIQUID_TERMS = (
    "水冷", "水神", "水雕", "水超龙", "水夜神", "NEPTUNE",
    "WATERFORCE", "LIQUID", "ASTRAL LC", "SUPRIM LIQUID",
)
GPU_VRAM_PATTERN = re.compile(
    r"(?<!\d)(?:O)?(96|48|32|24|20|16|12|10|8|6|4)\s*G(?:B)?(?!\d)"
)
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
    total_match = re.search(r"(?<!\d)(\d{1,3})\s*GB\s*(?:\(|DDR|D[45]|$)", text)
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


def infer_memory_module_count(item):
    """Infer memory module count from common kit notation such as 32Gx2."""
    text = _upper(item).replace("×", "X")
    kit_match = re.search(r"(?<!\d)\d{1,3}\s*G(?:B)?\s*[X*]\s*(\d)(?!\d)", text)
    if kit_match:
        count = int(kit_match.group(1))
        if 1 <= count <= 8:
            return count
    return item.get("module_count")


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


def infer_cooler_type(item):
    """Infer air/liquid cooler type from model text."""
    text = _upper(item)
    if any(term.upper() in text for term in WATER_TERMS):
        return "liquid"
    if (
        re.search(r"(?<!\d)(240|280|360|420)(?!\d)", text)
        and any(term in text for term in ("屏", "CPU", "ARGB", "幻彩"))
    ):
        return "liquid"
    return item.get("type") or "air"


def infer_radiator_mm(item):
    """Infer AIO radiator size from model text."""
    value = item.get("radiator_mm")
    if value:
        return value
    if infer_cooler_type(item) != "liquid":
        return value
    text = _upper(item)
    for size in (420, 360, 280, 240, 120):
        if re.search(rf"(?<!\d){size}(?!\d)", text):
            return size
    return value


def enrich_item(section, item):
    """Return a shallow enriched copy for query/compatibility scripts."""
    enriched = dict(item)
    if section == "memory":
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
        radiator = infer_radiator_mm(enriched)
        if radiator:
            enriched["radiator_mm"] = radiator
        enriched["rgb"] = infer_rgb(enriched)
    elif section == "psus":
        native = infer_native_16pin_psu(enriched)
        if native is not None:
            enriched["native_16pin_gpu_power"] = native
        modular = infer_modular(enriched)
        if modular is not None:
            enriched["modular"] = modular
    return enriched
