#!/usr/bin/env python3
"""Resolve explicit user catalog overlays without mutating the bundled catalog."""

from __future__ import annotations

import copy
import json
import math
import re
import unicodedata
from dataclasses import dataclass
from datetime import date
from pathlib import Path

import yaml

from component_inference import (
    USER_CONFIRMED_SPEC_FIELDS,
    enrich_item,
    infer_cpu_integrated_graphics,
    infer_storage_form_factor,
    normalize_explicit_storage_form_factor,
    storage_interface_form_factor_consistent,
    storage_model_form_factor_consistent,
)
from motherboard_capabilities import (
    THUNDERBOLT_STATUSES,
    USB4_STATUSES,
    validate_m2_slot_layout,
    validate_motherboard_capabilities,
    validate_pcie_slot_layout,
)


SUPPORTED_CURRENCIES = {"CNY", "USD", "EUR", "GBP", "JPY", "TWD"}


@dataclass(frozen=True)
class CategoryContract:
    section: str
    critical: tuple[str, ...]
    specs: frozenset[str]


@dataclass(frozen=True)
class FieldContract:
    kind: str
    minimum: float | None = None
    maximum: float | None = None
    choices: tuple[str, ...] = ()
    pattern: str | None = None


def _fields(*names):
    return frozenset(names)


# One tested source of truth retains category-specific facts instead of flattening
# CPUs, boards, GPUs and enclosures into one generic component shape.
CATEGORY_CONTRACTS = {
    "cpu": CategoryContract("cpus", ("socket", "power_w"), _fields(
        "platform", "socket", "power_w", "integrated_graphics", "cores_threads", "cores", "threads")),
    "mb": CategoryContract("motherboards", ("socket", "memory_generations", "form_factor"), _fields(
        "platform", "socket", "chipset", "memory_generations", "memory_slots", "memory_freq_max",
        "memory_max_gb", "m2_slots", "sata_ports", "display_outputs", "form_factor", "color",
        "pcie_slot_layout", "m2_slot_layout", "usb4_status", "usb4_rear_ports", "usb4_speed_gbps",
        "usb4_shares_with", "usb4_disable_conditions", "thunderbolt_status",
        "thunderbolt_rear_ports", "thunderbolt_version", "thunderbolt_header",
        "sata_port_conditions")),
    "memory": CategoryContract("memory", ("generation", "capacity_gb", "module_count"), _fields(
        "generation", "capacity_gb", "module_count", "frequency_mt", "timing", "color", "rgb")),
    "storage": CategoryContract("storage", ("interface", "capacity_gb"), _fields(
        "capacity_gb", "capacity_tb", "form_factor", "interface", "pcie_generation", "storage_type",
        "dram_cache", "dram_cache_mb", "series")),
    "gpu": CategoryContract("gpus", ("chip", "length_mm", "power_w"), _fields(
        "chip", "gpu_vendor", "vram_gb", "memory_type", "memory_bus_bit", "memory_bandwidth_gbps",
        "gpu_cooling", "gpu_radiator_required", "length_mm", "power_w", "power_connectors",
        "requires_16pin_psu", "color", "rgb")),
    "cooler": CategoryContract("coolers", ("type", "socket_support"), _fields(
        "type", "height_mm", "radiator_mm", "socket_support", "air_cooler_layout",
        "heatpipe_count", "color", "rgb")),
    "psu": CategoryContract("psus", ("wattage_w", "form_factor"), _fields(
        "wattage_w", "form_factor", "length_mm", "efficiency", "modular", "native_16pin_gpu_power", "color")),
    "case": CategoryContract("cases", ("motherboard_support", "gpu_length_mm", "cpu_cooler_height_mm", "psu_support"), _fields(
        "colors", "color", "motherboard_support", "gpu_length_mm", "cpu_cooler_height_mm",
        "radiator_support", "fan_mounts", "fan_slots_count", "psu_support", "psu_length_mm",
        "psu_length_recommended_mm", "psu_length_condition", "air_flow_type", "has_dust_filter", "is_showcase")),
    "display": CategoryContract("displays", ("resolution", "refresh_rate_hz"), _fields(
        "resolution", "size_inch", "refresh_rate_hz", "color")),
    "fan": CategoryContract("fans", ("size_mm",), _fields(
        "size_mm", "pack_count", "blade_direction", "color", "rgb", "is_linkable", "has_screen",
        "radiator_fan_bundle_mm", "fan_type", "default_recommend")),
}
CATEGORY_SECTIONS = {name: contract.section for name, contract in CATEGORY_CONTRACTS.items()}
ALLOWED_SPEC_FIELDS = frozenset().union(*(contract.specs for contract in CATEGORY_CONTRACTS.values()))
MINIMUM_NUMBER = 0.000001
GPU_POWER_EVIDENCE_FIELD = "power_connectors/requires_16pin_psu"
GPU_CATALOG_CONFLICT_FIELDS = (
    "chip", "vram_gb", "memory_type", "length_mm", "power_w",
    "power_connectors", "requires_16pin_psu",
)
NON_BLANK_PATTERN = r"\S"
GPU_POWER_CONNECTOR_SCHEMA_PATTERN = (
    r"^(?:(?:[1-4][xX])?(?:6|8|16)[pP][iI][nN]|"
    r"12[Vv](?:[hH][pP][wW][rR]|-?2[xX]6))$"
)
GPU_POWER_CONNECTOR_PATTERN = re.compile(GPU_POWER_CONNECTOR_SCHEMA_PATTERN)
DISPLAY_OUTPUT_SCHEMA_PATTERN = r"^(?:HDMI|DisplayPort|VGA|DVI|USB-C|Thunderbolt)$"


FIELD_CONTRACTS = {
    **{name: FieldContract("string", pattern=NON_BLANK_PATTERN) for name in (
        "platform", "socket", "chipset", "form_factor", "color", "generation", "timing", "interface",
        "storage_type", "series", "chip", "gpu_vendor", "memory_type", "gpu_cooling", "type", "efficiency",
        "blade_direction", "fan_type", "resolution", "psu_length_condition", "cores_threads", "fan_mounts",
        "air_flow_type")},
    **{name: FieldContract("number", MINIMUM_NUMBER) for name in (
        "power_w", "cores", "threads", "memory_slots", "memory_freq_max", "memory_max_gb",
        "m2_slots", "sata_ports", "capacity_gb", "capacity_tb", "module_count", "frequency_mt",
        "pcie_generation", "dram_cache_mb", "vram_gb", "memory_bus_bit",
        "memory_bandwidth_gbps", "length_mm", "height_mm", "radiator_mm", "wattage_w",
        "gpu_length_mm", "cpu_cooler_height_mm", "fan_slots_count", "psu_length_mm",
        "psu_length_recommended_mm", "size_inch", "refresh_rate_hz", "size_mm",
        "pack_count", "radiator_fan_bundle_mm",
    )},
    **{name: FieldContract("boolean") for name in (
        "integrated_graphics", "rgb", "dram_cache", "gpu_radiator_required", "requires_16pin_psu", "modular",
        "native_16pin_gpu_power", "has_dust_filter", "is_showcase", "is_linkable", "has_screen", "default_recommend",
        "thunderbolt_header")},
    **{name: FieldContract("string_list", pattern=NON_BLANK_PATTERN) for name in (
        "memory_generations", "colors", "socket_support",
        "motherboard_support", "psu_support", "usb4_shares_with",
        "usb4_disable_conditions", "sata_port_conditions")},
    "display_outputs": FieldContract(
        "string_list", pattern=DISPLAY_OUTPUT_SCHEMA_PATTERN
    ),
    "power_connectors": FieldContract(
        "string_list", pattern=GPU_POWER_CONNECTOR_SCHEMA_PATTERN
    ),
    "radiator_support": FieldContract("number_list", MINIMUM_NUMBER),
    "air_cooler_layout": FieldContract(
        "string",
        choices=("low_profile", "down_draft", "single_tower", "dual_tower"),
        pattern=NON_BLANK_PATTERN,
    ),
    "heatpipe_count": FieldContract("integer", minimum=1, maximum=16),
    "pcie_slot_layout": FieldContract("pcie_slot_list"),
    "m2_slot_layout": FieldContract("m2_slot_list"),
    "usb4_status": FieldContract("string", choices=tuple(sorted(USB4_STATUSES)), pattern=NON_BLANK_PATTERN),
    "thunderbolt_status": FieldContract(
        "string", choices=tuple(sorted(THUNDERBOLT_STATUSES)), pattern=NON_BLANK_PATTERN
    ),
    "usb4_rear_ports": FieldContract("integer", minimum=0, maximum=8),
    "usb4_speed_gbps": FieldContract("integer", minimum=20, maximum=120),
    "thunderbolt_rear_ports": FieldContract("integer", minimum=0, maximum=8),
    "thunderbolt_version": FieldContract("integer", minimum=3, maximum=5),
}


class OverlayError(ValueError):
    """Machine-readable overlay failure."""

    def __init__(self, code: str, message: str, path: str = "$"):
        super().__init__(message)
        self.code, self.message, self.path = code, message, path

    def as_dict(self):
        return {"code": self.code, "path": self.path, "message": self.message}


def _pairs_no_duplicates(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise OverlayError("duplicate_key", f"duplicate JSON key: {key}")
        result[key] = value
    return result


def _reject_constant(value):
    raise OverlayError("invalid_number", f"non-finite number is forbidden: {value}")


def _reject_unpaired_surrogates(value):
    """Reject JSON strings that UTF-8 terminals and files cannot represent."""
    stack = [value]
    while stack:
        current = stack.pop()
        if isinstance(current, str):
            if any(0xD800 <= ord(character) <= 0xDFFF for character in current):
                raise OverlayError(
                    "invalid_encoding", "overlay JSON contains an unpaired Unicode surrogate"
                )
        elif isinstance(current, dict):
            for key, item in current.items():
                stack.append(key)
                stack.append(item)
        elif isinstance(current, (list, tuple)):
            stack.extend(current)


def load_json_strict(source, *, max_bytes=5_000_000):
    try:
        if hasattr(source, "read"):
            payload = source.read(max_bytes + 1)
        else:
            with Path(source).open("rb") as handle:
                payload = handle.read(max_bytes + 1)
    except (OSError, UnicodeError) as exc:
        raise OverlayError("file_read_error", "unable to read overlay JSON") from exc
    if isinstance(payload, bytes):
        try:
            text = payload.decode("utf-8")
        except UnicodeDecodeError as exc:
            raise OverlayError("invalid_encoding", "overlay JSON must be UTF-8") from exc
    elif isinstance(payload, str):
        text = payload
    else:
        raise OverlayError("file_read_error", "overlay source must provide text or bytes")
    try:
        encoded_size = len(text.encode("utf-8"))
    except UnicodeEncodeError as exc:
        raise OverlayError("invalid_encoding", "overlay JSON must contain valid Unicode") from exc
    if encoded_size > max_bytes:
        raise OverlayError("file_too_large", f"overlay exceeds {max_bytes} bytes")
    try:
        document = json.loads(
            text,
            object_pairs_hook=_pairs_no_duplicates,
            parse_constant=_reject_constant,
        )
    except OverlayError:
        raise
    except (ValueError, UnicodeError, RecursionError) as exc:
        raise OverlayError("invalid_json", str(exc)) from exc
    _reject_unpaired_surrogates(document)
    return document


def _keys(obj, allowed, path):
    if not isinstance(obj, dict):
        raise OverlayError("wrong_type", "expected object", path)
    extra = sorted(set(obj) - set(allowed))
    if extra:
        raise OverlayError("unknown_field", f"unknown field(s): {', '.join(extra)}", path)


def _iso_date(value, path):
    if not isinstance(value, str) or not re.fullmatch(r"\d{4}-\d{2}-\d{2}", value):
        raise OverlayError("invalid_date", "expected ISO date YYYY-MM-DD", path)
    try:
        parsed = date.fromisoformat(value)
    except ValueError as exc:
        raise OverlayError("invalid_date", "expected ISO date YYYY-MM-DD", path) from exc
    if parsed > date.today():
        raise OverlayError("invalid_date", "price date cannot be in the future", path)


def _price(value, path):
    if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value) or value < MINIMUM_NUMBER:
        raise OverlayError("invalid_price", f"price must be a finite number of at least {MINIMUM_NUMBER}", path)


def _validate_spec_value(field, value, path):
    contract = FIELD_CONTRACTS.get(field)
    if contract is None:
        return
    if contract.kind == "string":
        valid = (
            isinstance(value, str)
            and contract.pattern is not None
            and re.search(contract.pattern, value) is not None
            and (not contract.choices or value in contract.choices)
        )
    elif contract.kind == "number":
        valid = (
            not isinstance(value, bool)
            and isinstance(value, (int, float))
            and math.isfinite(value)
            and value >= contract.minimum
            and (contract.maximum is None or value <= contract.maximum)
        )
    elif contract.kind == "integer":
        valid = (
            not isinstance(value, bool)
            and isinstance(value, int)
            and value >= contract.minimum
            and (contract.maximum is None or value <= contract.maximum)
        )
    elif contract.kind == "boolean":
        valid = isinstance(value, bool)
    elif contract.kind == "string_list":
        valid = (
            isinstance(value, list)
            and bool(value)
            and contract.pattern is not None
            and all(
                isinstance(x, str) and re.search(contract.pattern, x) is not None
                for x in value
            )
        )
    elif contract.kind == "number_list":
        minimum = contract.minimum if contract.minimum is not None else MINIMUM_NUMBER
        valid = (
            isinstance(value, list)
            and bool(value)
            and all(
                not isinstance(x, bool)
                and isinstance(x, (int, float))
                and math.isfinite(x)
                and x >= minimum
                for x in value
            )
        )
    elif contract.kind == "pcie_slot_list":
        valid = not validate_pcie_slot_layout(value)
    elif contract.kind == "m2_slot_list":
        valid = not validate_m2_slot_layout(value)
    else:
        valid = False
    if not valid:
        raise OverlayError("invalid_spec", f"invalid {field} value", path)


def validate_overlay(doc):
    _keys(doc, ("schema_version", "currency", "quote_patches", "components", "aliases"), "$")
    if doc.get("schema_version") != "1.0":
        raise OverlayError("unsupported_schema", "schema_version must be 1.0", "$.schema_version")
    currency = doc.get("currency")
    if currency not in SUPPORTED_CURRENCIES:
        raise OverlayError("invalid_currency", f"currency must be one of {sorted(SUPPORTED_CURRENCIES)}", "$.currency")
    for field in ("quote_patches", "components", "aliases"):
        if field in doc and not isinstance(doc[field], list):
            raise OverlayError("wrong_type", "expected array", f"$.{field}")
        if len(doc.get(field, [])) > 5000:
            raise OverlayError("too_many_items", "array limit is 5000", f"$.{field}")

    for i, patch in enumerate(doc.get("quote_patches", [])):
        p = f"$.quote_patches[{i}]"
        _keys(patch, ("target_id", "price", "price_date", "note"), p)
        if not isinstance(patch.get("target_id"), str) or not patch["target_id"].strip():
            raise OverlayError("invalid_id", "target_id is required", p + ".target_id")
        _price(patch.get("price"), p + ".price")
        _iso_date(patch.get("price_date"), p + ".price_date")
        if "note" in patch and (not isinstance(patch["note"], str) or len(patch["note"]) > 1000):
            raise OverlayError("wrong_type", "note must be a string of at most 1000 characters", p + ".note")

    ids = set()
    for i, component in enumerate(doc.get("components", [])):
        p = f"$.components[{i}]"
        _keys(component, ("id", "category", "brand", "model", "brand_en", "model_en", "base_component_id", "specs", "price", "price_date", "note"), p)
        category, item_id = component.get("category"), component.get("id")
        if category not in CATEGORY_CONTRACTS:
            raise OverlayError("invalid_category", f"unknown category: {category}", p + ".category")
        if not isinstance(item_id, str) or not re.fullmatch(rf"user-{re.escape(category)}-[a-z0-9][a-z0-9._-]*", item_id):
            raise OverlayError("invalid_id", f"id must start with user-{category}-", p + ".id")
        if item_id in ids:
            raise OverlayError("duplicate_id", f"duplicate component id: {item_id}", p + ".id")
        ids.add(item_id)
        for field in ("brand", "model"):
            if not isinstance(component.get(field), str) or not component[field].strip():
                raise OverlayError("missing_identity", f"{field} is required", p + f".{field}")
        for field in ("brand_en", "model_en"):
            if field in component and (not isinstance(component[field], str) or not component[field].strip()):
                raise OverlayError("wrong_type", f"{field} must be a non-empty string", p + f".{field}")
        if "note" in component and (not isinstance(component["note"], str) or len(component["note"]) > 1000):
            raise OverlayError("wrong_type", "note must be a string of at most 1000 characters", p + ".note")
        if "base_component_id" in component and (
            not isinstance(component["base_component_id"], str) or not component["base_component_id"].strip()
        ):
            raise OverlayError("invalid_id", "base_component_id must be a non-empty exact ID", p + ".base_component_id")
        specs = component.get("specs", {})
        _keys(specs, CATEGORY_CONTRACTS[category].specs, p + ".specs")
        for field, value in specs.items():
            _validate_spec_value(field, value, p + f".specs.{field}")
        if category == "cpu" and specs.get("integrated_graphics") is True:
            model_fact = infer_cpu_integrated_graphics({
                "brand": component["brand"],
                "model": component["model"],
            })
            if model_fact is False:
                raise OverlayError(
                    "spec_conflict",
                    "integrated_graphics=true conflicts with a CPU model whose F/KF suffix disables integrated graphics",
                    p + ".specs.integrated_graphics",
                )
        if category == "mb":
            capability_errors = validate_motherboard_capabilities(specs)
            if capability_errors:
                raise OverlayError(
                    "invalid_spec",
                    "; ".join(capability_errors),
                    p + ".specs",
                )
        if (
            category == "storage"
            and "form_factor" in specs
            and normalize_explicit_storage_form_factor(specs["form_factor"]) is None
        ):
            raise OverlayError(
                "invalid_spec",
                "storage form_factor must be M.2/NGFF with an optional supported size, mSATA, 2.5 SATA, or 3.5 SATA",
                p + ".specs.form_factor",
            )
        if (
            category == "storage"
            and "interface" in specs
            and "form_factor" in specs
            and storage_interface_form_factor_consistent(
                specs["interface"], specs["form_factor"]
            ) is not True
        ):
            raise OverlayError(
                "invalid_spec",
                "storage interface and form_factor are not a supported semantic pair",
                p + ".specs",
            )
        if (
            category == "storage"
            and "form_factor" in specs
            and storage_model_form_factor_consistent(
                component["model"], specs["form_factor"]
            ) is False
        ):
            raise OverlayError(
                "spec_conflict",
                "storage form_factor conflicts with explicit physical-shape evidence in model",
                p + ".specs.form_factor",
            )
        if "price" in component:
            _price(component["price"], p + ".price")
            _iso_date(component.get("price_date"), p + ".price_date")
        elif "price_date" in component:
            raise OverlayError("orphan_price_date", "price_date requires price", p + ".price_date")

    for i, alias in enumerate(doc.get("aliases", [])):
        p = f"$.aliases[{i}]"
        _keys(alias, ("alias", "target_id"), p)
        if not all(isinstance(alias.get(k), str) and alias[k].strip() for k in ("alias", "target_id")):
            raise OverlayError("invalid_alias", "alias and target_id are required", p)
    return doc


def normalize_overlay(doc):
    validate_overlay(doc)
    result = copy.deepcopy(doc)
    result.setdefault("quote_patches", [])
    result.setdefault("components", [])
    result.setdefault("aliases", [])
    return result


def _compact(value):
    text = unicodedata.normalize("NFKC", str(value or ""))
    return "".join(ch for ch in text.upper() if ch.isalnum())


def _identity_keys(item, alias_data, category, *, include_explicit):
    """Return raw-derived SKU keys, optionally including stored official identity."""
    raw_identity = {"brand": item.get("brand"), "model": item.get("model")}
    normalized = normalize_item_names(raw_identity, alias_data, category)
    keys = set()
    for brand_field, model_field in (("brand", "model"), ("brand_en", "model_en")):
        brand = _compact(normalized.get(brand_field))
        model = _compact(normalized.get(model_field))
        if brand and model:
            keys.add((brand, model))
    if include_explicit:
        brand = _compact(item.get("brand_en"))
        model = _compact(item.get("model_en"))
        if brand and model:
            keys.add((brand, model))
    return keys


def _same_component_identity(component, base, alias_data, category):
    component_keys = _identity_keys(component, alias_data, category, include_explicit=False)
    base_keys = _identity_keys(base, alias_data, category, include_explicit=True)
    if not (component_keys & base_keys):
        return False
    normalized_base = normalize_item_names(base, alias_data, category)
    for field, raw_field in (("brand_en", "brand"), ("model_en", "model")):
        if field not in component:
            continue
        allowed = {_compact(normalized_base.get(field)), _compact(normalized_base.get(raw_field))} - {""}
        if _compact(component[field]) not in allowed:
            return False
    return True


CATALOGUE_FILES = (
    (("components.yaml", "components.txt"), ("cpus", "motherboards", "memory", "storage", "gpus", "coolers", "psus", "fans")),
    (("cases.yaml", "cases.txt"), ("cases",)),
    (("displays.yaml", "displays.txt"), ("displays",)),
)


def load_catalog_sections(data_dir):
    """Load the bundled YAML catalogue, including Red package .txt adapters."""
    data_dir = Path(data_dir)
    sections = {}
    for filenames, section_names in CATALOGUE_FILES:
        path = next((data_dir / name for name in filenames if (data_dir / name).is_file()), None)
        if path is None:
            continue
        try:
            with path.open("r", encoding="utf-8") as handle:
                document = yaml.safe_load(handle) or {}
        except (OSError, UnicodeError, yaml.YAMLError) as exc:
            raise OverlayError("catalog_read_error", f"unable to read bundled catalog: {path.name}") from exc
        if not isinstance(document, dict):
            raise OverlayError("catalog_read_error", f"bundled catalog root must be an object: {path.name}")
        for section in section_names:
            items = document.get(section, [])
            if not isinstance(items, list):
                raise OverlayError("catalog_read_error", f"catalog section must be an array: {section}")
            sections[section] = items
    return sections


def load_name_aliases(data_dir):
    path = Path(data_dir) / "hardware_name_aliases.json"
    if not path.exists():
        return {"schema_version": "1.0", "brands": [], "series": []}
    doc = load_json_strict(path)
    _keys(doc, ("schema_version", "brands", "series"), "$")
    if doc.get("schema_version") != "1.0":
        raise OverlayError("unsupported_alias_schema", "alias schema_version must be 1.0")
    if not isinstance(doc.get("brands"), list) or not isinstance(doc.get("series"), list):
        raise OverlayError("invalid_alias_catalog", "brands and series must be arrays")
    officials, seen_aliases, series_keys = set(), {}, set()
    for index, entry in enumerate(doc["brands"]):
        p = f"$.brands[{index}]"
        _keys(entry, ("official", "aliases"), p)
        official, aliases = entry.get("official"), entry.get("aliases")
        if not isinstance(official, str) or not official.strip() or official in officials:
            raise OverlayError("duplicate_official_name", f"invalid or duplicate official name: {official}", p)
        if not isinstance(aliases, list) or not aliases or not all(isinstance(x, str) and x.strip() for x in aliases):
            raise OverlayError("invalid_alias_catalog", "aliases must be a non-empty string array", p)
        officials.add(official)
        for alias in aliases:
            key = _compact(alias)
            if key in seen_aliases and seen_aliases[key] != official:
                raise OverlayError("overlapping_alias", f"alias {alias} maps to multiple official names", p)
            seen_aliases[key] = official
    for index, rule in enumerate(doc["series"]):
        p = f"$.series[{index}]"
        _keys(rule, ("brand", "official", "categories", "patterns"), p)
        key = (rule.get("brand"), rule.get("official"))
        patterns, categories = rule.get("patterns"), rule.get("categories")
        if key in series_keys or rule.get("brand") not in officials:
            raise OverlayError("invalid_series_alias", f"invalid or duplicate series rule: {key}", p)
        if not isinstance(patterns, list) or not patterns or not isinstance(categories, list) or not categories:
            raise OverlayError("invalid_series_alias", "patterns and categories must be non-empty arrays", p)
        if any(category not in CATEGORY_CONTRACTS for category in categories):
            raise OverlayError("invalid_series_alias", "series rule contains an unknown category", p)
        try:
            for pattern in patterns:
                re.compile(pattern)
        except (TypeError, re.error) as exc:
            raise OverlayError("invalid_series_alias", f"invalid regex pattern: {exc}", p) from exc
        series_keys.add(key)
    return doc


def normalize_item_names(item, alias_data, category=None):
    result = dict(item)
    if result.get("brand_en") and result.get("model_en"):
        result["normalization_status"] = "explicit"
        return result
    brand_text = _compact(result.get("brand"))
    brand_en = result.get("brand_en")
    for entry in alias_data.get("brands", []):
        if brand_text in {_compact(x) for x in entry.get("aliases", [])}:
            brand_en = entry["official"]
            break
    model = str(result.get("model") or "")
    model_en = result.get("model_en")
    matched = None
    for rule in alias_data.get("series", []):
        if rule.get("brand") != brand_en:
            continue
        if category not in rule.get("categories", []):
            continue
        if any(re.search(pattern, model, flags=re.IGNORECASE) for pattern in rule.get("patterns", [])):
            matched = rule["official"]
            break
    if brand_en:
        result["brand_en"] = brand_en
    if matched:
        model_en = model
        for entry in alias_data.get("brands", []):
            if entry.get("official") == brand_en:
                for alias in sorted(entry.get("aliases", []), key=len, reverse=True):
                    model_en = re.sub(re.escape(alias), brand_en, model_en, flags=re.IGNORECASE)
        rule = next(rule for rule in alias_data["series"] if rule["brand"] == brand_en and rule["official"] == matched and category in rule["categories"])
        for pattern in rule["patterns"]:
            match = re.search(pattern, model_en, flags=re.IGNORECASE)
            if not match:
                continue
            replacement = matched
            if _compact(matched) in _compact(model_en) and _compact(match.group(0)) != _compact(matched):
                replacement = ""
            model_en = re.sub(pattern, replacement, model_en, flags=re.IGNORECASE)
        model_en = re.sub(r"[^\x20-\x7E]+", " ", model_en)
        model_en = re.sub(r"\s+", " ", model_en).strip()
        if model_en and _compact(model_en) != _compact(brand_en):
            result["model_en"] = model_en
            result["normalization_status"] = "official_alias_partial"
        else:
            result["normalization_status"] = "brand_only"
    elif model_en:
        result["model_en"] = model_en
        result["normalization_status"] = "explicit"
    elif brand_en:
        result["normalization_status"] = "brand_only"
    else:
        result["normalization_status"] = "unverified"
    return result


def _apply_user_quote(item, quote, currency):
    """Attach one active user quote while retaining the base CNY quote object."""
    if item.get("price_cny") is not None:
        item.setdefault("base_price_cny", item.get("price_cny"))
        item.setdefault("base_price_status", item.get("price_status"))
        item.setdefault("base_price_date", item.get("price_date"))
    item.update({
        "user_price": quote["price"],
        "user_price_currency": currency,
        "user_price_date": quote["price_date"],
        "user_quote_note": quote.get("note"),
        # Compatibility aliases for callers written before the quote object split.
        "active_price": quote["price"],
        "price_currency": currency,
        "price_status": "user_quote",
        "price_date": quote["price_date"],
    })


def _has_gpu_power_evidence(item):
    connectors = item.get("power_connectors")
    recognized_connectors = (
        isinstance(connectors, list)
        and bool(connectors)
        and all(
            isinstance(value, str)
            and GPU_POWER_CONNECTOR_PATTERN.fullmatch(value.strip())
            for value in connectors
        )
    )
    # False without a connector is indistinguishable from a weak-model guess.
    # A positive 16-pin requirement is actionable on its own; a negative claim
    # must be backed by a canonical connector such as 8pin.
    return recognized_connectors or item.get("requires_16pin_psu") is True


def _missing_critical_fields(category, item, *, gpu_power_evidence=True):
    missing = [
        field
        for field in CATEGORY_CONTRACTS[category].critical
        if item.get(field) in (None, "", [])
    ]
    if category == "gpu" and not gpu_power_evidence:
        missing.append(GPU_POWER_EVIDENCE_FIELD)
    return missing


def enrich_resolved_item(section, item):
    """Apply runtime inference without turning an explicit overlay unknown into False."""
    enriched = enrich_item(section, item)
    if GPU_POWER_EVIDENCE_FIELD in enriched.get("_overlay_incomplete_fields", []):
        enriched.pop("requires_16pin_psu", None)
    conflicts = enriched.get("_catalog_conflict_fields")
    if conflicts:
        enriched["spec_conflicts"] = list(conflicts)
    return enriched


def _canonical_spec_value(field, value):
    """Return a stable comparison key without rewriting the stored fact."""
    if field == "radiator_support":
        if isinstance(value, bool):
            return value
        try:
            number = float(str(value).strip())
        except (TypeError, ValueError):
            pass
        else:
            return int(number) if number.is_integer() else number
    if not isinstance(value, str):
        return value
    if field == "form_factor":
        storage_shape = normalize_explicit_storage_form_factor(value)
        if storage_shape is not None:
            return _compact(storage_shape)
    if field == "socket_support":
        text = unicodedata.normalize("NFKC", value)
        sockets = []
        for part in re.split(r"[/,|，、;；&+]|\bAND\b|和|及|与", text, flags=re.IGNORECASE):
            key = re.sub(r"[^0-9A-Z]", "", part.upper())
            previous = None
            while key and key != previous:
                previous = key
                for prefix in ("SOCKET", "INTEL", "AMD"):
                    if key.startswith(prefix):
                        key = key[len(prefix):]
                        break
            if key in {
                "775", "1150", "1151", "1155", "1156", "115X", "1200",
                "1366", "1700", "1851", "2011", "20113", "2066",
            }:
                key = "LGA" + key
            if key:
                sockets.append(key)
        if sockets:
            return tuple(sockets)
    key = _compact(value)
    if field == "power_connectors":
        counted = re.fullmatch(r"([1-4])X((?:6|8|16)PIN)", key)
        if counted:
            return tuple([counted.group(2)] * int(counted.group(1)))
    if field in {"type", "gpu_cooling"}:
        aliases = {
            "LIQUID": "LIQUID",
            "WATER": "LIQUID",
            "水冷": "LIQUID",
            "一体式": "LIQUID",
            "AIR": "AIR",
            "风冷": "AIR",
        }
        key = aliases.get(key, key)
    return key


def _canonical_list_values(field, values):
    """Canonicalize unordered list facts and expand connector/socket bundles."""
    keys = []
    for value in values:
        canonical = _canonical_spec_value(field, value)
        if field in {"socket_support", "power_connectors"} and isinstance(canonical, tuple):
            keys.extend(canonical)
        else:
            keys.append(canonical)
    return keys


def _spec_values_equivalent(field, supplied, effective):
    """Compare explicit facts semantically, including unordered set-like lists."""
    if isinstance(supplied, (list, tuple)) and isinstance(effective, (list, tuple)):
        supplied_keys = _canonical_list_values(field, supplied)
        effective_keys = _canonical_list_values(field, effective)
        return sorted(supplied_keys, key=repr) == sorted(effective_keys, key=repr)
    return _canonical_spec_value(field, supplied) == _canonical_spec_value(field, effective)


def _catalog_gpu_identity(item):
    return _compact(item.get("brand")), _compact(item.get("model"))


def _hashable_catalog_fact(field, value):
    if isinstance(value, (list, tuple, set)):
        canonical_items = _canonical_list_values(field, value)
        return tuple(sorted(canonical_items, key=repr))
    return _canonical_spec_value(field, value)


def mark_base_gpu_spec_conflicts(items):
    """Mark same-name base GPUs whose compatibility-sensitive facts disagree."""
    grouped = {}
    for item in items:
        identity = _catalog_gpu_identity(item)
        if not all(identity):
            continue
        facts = grouped.setdefault(
            identity, {field: set() for field in GPU_CATALOG_CONFLICT_FIELDS}
        )
        for field in GPU_CATALOG_CONFLICT_FIELDS:
            value = item.get(field)
            if value in (None, "", []):
                continue
            facts[field].add(_hashable_catalog_fact(field, value))
    conflicts_by_identity = {
        identity: tuple(
            field for field in GPU_CATALOG_CONFLICT_FIELDS
            if len(facts[field]) > 1
        )
        for identity, facts in grouped.items()
    }
    for item in items:
        conflicts = conflicts_by_identity.get(_catalog_gpu_identity(item), ())
        if conflicts:
            item["_catalog_conflict_fields"] = list(conflicts)
        else:
            item.pop("_catalog_conflict_fields", None)
    return conflicts_by_identity


def resolve_catalog_documents(sections, documents, *, data_dir, normalize_names=True):
    """Resolve already-parsed overlays; shared by import, query, and check."""
    alias_data = load_name_aliases(data_dir)
    section_categories = {contract.section: category for category, contract in CATEGORY_CONTRACTS.items()}
    resolved = {
        name: [
            normalize_item_names(item, alias_data, section_categories.get(name))
            if normalize_names else dict(item)
            for item in items
        ]
        for name, items in sections.items()
    }
    mark_base_gpu_spec_conflicts(resolved.get("gpus", []))
    by_id = {}
    category_by_id = {}
    for category, section in CATEGORY_SECTIONS.items():
        for item in resolved.get(section, []):
            if item["id"] in by_id:
                raise OverlayError("duplicate_base_id", f"duplicate base id: {item['id']}")
            by_id[item["id"]] = item
            category_by_id[item["id"]] = category
            if item.get("price_cny"):
                item.setdefault("base_price_cny", item["price_cny"])
                item.setdefault("base_price_status", item.get("price_status"))
                item.setdefault("base_price_date", item.get("price_date"))
                item.setdefault("active_price", item["price_cny"])
                item.setdefault("price_currency", "CNY")

    alias_index = {}
    for document in documents or []:
        doc = normalize_overlay(document)
        currency = doc["currency"]
        new_ids = {x["id"] for x in doc["components"]}
        collisions = sorted(new_ids & set(by_id))
        if collisions:
            raise OverlayError("duplicate_id", f"component id already exists: {collisions[0]}")
        for component_index, component in enumerate(doc["components"]):
            base = by_id.get(component.get("base_component_id")) if component.get("base_component_id") else None
            if component.get("base_component_id") and base is None:
                raise OverlayError("unknown_target", f"base component does not exist: {component['base_component_id']}")
            if base and category_by_id[component["base_component_id"]] != component["category"]:
                raise OverlayError("category_conflict", "base_component_id category does not match new component")
            if base and not _same_component_identity(component, base, alias_data, component["category"]):
                raise OverlayError(
                    "base_identity_conflict",
                    "base_component_id may inherit specifications only for the exact same bilingual SKU; use quote_patches and aliases for an existing catalog item",
                )
            item = dict(base or {})
            if base:
                for field in (
                    "user_price", "user_price_currency", "user_price_date", "active_price",
                    "price_currency", "price_status", "price_date", "user_quote_note",
                    "_overlay_incomplete_fields",
                ):
                    item.pop(field, None)
                if item.get("price_cny") is not None:
                    item["active_price"] = item["price_cny"]
                    item["price_currency"] = "CNY"
                    item["price_status"] = item.get("base_price_status")
                    item["price_date"] = item.get("base_price_date")
            supplied_specs = component.get("specs", {})
            inherited_confirmed_spec_fields = set(
                item.get(USER_CONFIRMED_SPEC_FIELDS, [])
            )
            confirmed_spec_fields = set(inherited_confirmed_spec_fields)
            confirmed_spec_fields.update(supplied_specs)
            inherited_conflicts = set(item.get("_catalog_conflict_fields", []))
            for field, value in supplied_specs.items():
                repairs_unconfirmed_storage_shape = (
                    component["category"] == "storage"
                    and field == "form_factor"
                    and "form_factor" not in inherited_confirmed_spec_fields
                    and normalize_explicit_storage_form_factor(value)
                    == infer_storage_form_factor(item)
                )
                if (
                    base
                    and base.get(field) not in (None, "", [])
                    and field not in inherited_conflicts
                    and not repairs_unconfirmed_storage_shape
                    and not _spec_values_equivalent(field, value, base.get(field))
                ):
                    raise OverlayError("spec_conflict", f"{field} conflicts with inherited base specification")
                item[field] = value
                inherited_conflicts.discard(field)
            if confirmed_spec_fields:
                item[USER_CONFIRMED_SPEC_FIELDS] = sorted(confirmed_spec_fields)
            if inherited_conflicts:
                item["_catalog_conflict_fields"] = sorted(inherited_conflicts)
            else:
                item.pop("_catalog_conflict_fields", None)
            item.update({"id": component["id"], "brand": component["brand"], "model": component["model"]})
            if base:
                item["base_component_id"] = component["base_component_id"]
            for key in ("brand_en", "model_en", "note"):
                if component.get(key) is not None:
                    item[key] = component[key]
            gpu_power_evidence = component["category"] != "gpu" or _has_gpu_power_evidence(item)
            item = normalize_item_names(item, alias_data, component["category"])
            item = enrich_item(CATEGORY_SECTIONS[component["category"]], item)
            if component["category"] == "mb":
                capability_errors = validate_motherboard_capabilities(item)
                if capability_errors:
                    raise OverlayError(
                        "invalid_spec",
                        "; ".join(capability_errors),
                        f"$.components[{component_index}].specs",
                    )
            if (
                component["category"] == "storage"
                and storage_interface_form_factor_consistent(
                    item.get("interface"), item.get("form_factor")
                ) is False
            ):
                raise OverlayError(
                    "invalid_spec",
                    "effective storage interface and form_factor are not a supported semantic pair",
                    f"$.components[{component_index}].specs",
                )
            for field, supplied_value in supplied_specs.items():
                if not _spec_values_equivalent(field, supplied_value, item.get(field)):
                    raise OverlayError(
                        "spec_conflict",
                        f"explicit {field} conflicts with deterministic model or inherited inference",
                        f"$.components[{component_index}].specs.{field}",
                    )
            if not gpu_power_evidence:
                item.pop("requires_16pin_psu", None)
            if component.get("price") is not None:
                _apply_user_quote(item, component, currency)
            missing = _missing_critical_fields(
                component["category"], item, gpu_power_evidence=gpu_power_evidence
            )
            if missing:
                item["_overlay_incomplete_fields"] = missing
            resolved.setdefault(CATEGORY_SECTIONS[component["category"]], []).append(item)
            by_id[item["id"]] = item
            category_by_id[item["id"]] = component["category"]
        for patch in doc["quote_patches"]:
            target = by_id.get(patch["target_id"])
            if target is None:
                raise OverlayError("unknown_target", f"quote target does not exist: {patch['target_id']}")
            _apply_user_quote(target, patch, currency)
        for alias in doc["aliases"]:
            if alias["target_id"] not in by_id:
                raise OverlayError("unknown_target", f"alias target does not exist: {alias['target_id']}")
            key = _compact(alias["alias"])
            targets = alias_index.setdefault(key, set())
            if targets and alias["target_id"] not in targets:
                raise OverlayError("ambiguous_alias", f"alias resolves to multiple IDs: {', '.join(sorted(targets | {alias['target_id']}))}")
            targets.add(alias["target_id"])
    return resolved, by_id, alias_index


def resolve_catalog(sections, overlay_paths, *, data_dir):
    """Return copied sections plus alias index. Later quote patches win."""
    documents = [load_json_strict(path) for path in (overlay_paths or [])]
    return resolve_catalog_documents(sections, documents, data_dir=data_dir)


def resolve_id(token, by_id, alias_index):
    if token in by_id:
        return token
    targets = sorted(alias_index.get(_compact(token), set()))
    if not targets:
        return None
    if len(targets) > 1:
        raise OverlayError("ambiguous_alias", f"alias resolves to multiple IDs: {', '.join(targets)}")
    return targets[0]
