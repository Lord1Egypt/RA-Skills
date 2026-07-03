#!/usr/bin/env python3
"""主库结构校验 — 验证 components.yaml 和 cases.yaml 的基本完整性。

用法:
  python validate_library.py
"""

import re
import sys
from pathlib import Path

import yaml

from component_inference import enrich_item, infer_gpu_vram

try:
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
except Exception:
    pass

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"

REQUIRED_SECTIONS = ["cpus", "motherboards", "memory", "storage", "gpus", "coolers", "psus"]

REQUIRED_FIELDS = {
    "cpus": {"id", "brand", "model", "platform", "socket"},
    "motherboards": {"id", "brand", "model", "socket", "memory_generations", "form_factor"},
    "memory": {"id", "brand", "model", "generation", "capacity_gb"},
    "storage": {"id", "brand", "model", "capacity_tb", "form_factor"},
    "gpus": {"id", "brand", "model"},
    "coolers": {"id", "brand", "model", "type"},
    "psus": {"id", "brand", "model", "wattage_w"},
}

# Fields that trigger warning (not error) when missing.
# Motherboard M.2/SATA omissions are tracked separately as non-blocking notes:
# current mainstream boards usually have at least one M.2 slot, and SATA is
# only critical for multi-drive / editing / workstation workflows.
WARN_FIELDS = {
    "cpus": {"power_w"},
    "gpus": {"power_w", "length_mm"},
    "motherboards": {"color", "memory_freq_max"},
    "psus": {"length_mm"},
}

NOTE_FIELDS = {
    "motherboards": {"m2_slots", "sata_ports"},
}

VALID_PRICE_STATUSES = {"scraped", "verified_manual", "channel_quote", "needs_market_quote"}

COVERAGE_FIELDS = {
    "gpus": ["length_mm", "requires_16pin_psu"],
    "motherboards": ["m2_slots", "sata_ports", "memory_freq_max"],
    "memory": ["timing"],
    "storage": ["pcie_generation"],
    "coolers": ["type", "radiator_mm", "rgb"],
    "psus": ["wattage_w", "form_factor", "length_mm", "modular", "native_16pin_gpu_power"],
    "cases": ["gpu_length_mm", "cpu_cooler_height_mm", "radiator_support", "fan_mounts", "psu_length_mm"],
}


def _valid_fan_mounts(value):
    if value in (None, "", [], {}):
        return True
    text = str(value).upper().strip().replace("×", "X")
    if re.fullmatch(r"\d{1,2}", text):
        return 1 <= int(text) <= 20
    if re.fullmatch(r"\d{2,3}(?:\.\d+)?\s*(?:MM|CM)", text):
        return False
    if re.search(r"\d{1,2}\s*个(?:以上)?", text):
        return True
    if re.search(r"\d{1,2}\s*X\s*(?:120|140|200)", text):
        return True
    if re.search(r"(?:120|140|160|200)\s*MM?\s*(?:风扇|FAN)", text):
        return True
    if re.search(r"风扇|FAN|TOP|FRONT|REAR|BOTTOM|SIDE|前|顶|后|底|侧", text):
        return True
    return not bool(re.fullmatch(r"\d+(?:\.\d+)?\s*(?:MM|CM)?", text))


def main():
    errors = []
    warnings = []
    notes = []
    counts = {}
    coverage_rows = []

    # Load components.yaml
    comp_path = DATA / "components.yaml"
    if not comp_path.exists():
        print(f"FAIL: {comp_path} not found")
        return 1

    with comp_path.open("r", encoding="utf-8") as f:
        lib = yaml.safe_load(f)

    for section in REQUIRED_SECTIONS:
        items = lib.get(section, [])
        counts[section] = len(items)
        required = REQUIRED_FIELDS.get(section, set())

        for item in items:
            item_id = item.get("id", "<no-id>")
            if str(item_id).startswith("cat-") or "--" in str(item_id):
                errors.append(f"{section}.{item_id}: imported id was not normalized")
            missing = required - set(item.keys())
            if missing:
                errors.append(f"{section}.{item_id}: missing fields {missing}")

            price_status = item.get("price_status", "")
            if price_status and price_status not in VALID_PRICE_STATUSES:
                errors.append(f"{section}.{item_id}: invalid price_status '{price_status}'")

            price_cny = item.get("price_cny")
            if price_status == "needs_market_quote" and price_cny is not None:
                warnings.append(f"{section}.{item_id}: needs_market_quote but has price_cny={price_cny}")
            if price_status != "needs_market_quote" and price_cny is None:
                warnings.append(f"{section}.{item_id}: has price_status={price_status} but price_cny is None")
            if section == "gpus" and item.get("length_mm"):
                try:
                    gpu_length = int(item.get("length_mm"))
                    if gpu_length > 450 or gpu_length < 120:
                        errors.append(f"{section}.{item_id}: impossible length_mm={item.get('length_mm')}")
                except (TypeError, ValueError):
                    errors.append(f"{section}.{item_id}: invalid length_mm={item.get('length_mm')}")
            if section == "gpus":
                inferred_vram = infer_gpu_vram(item)
                current_vram = item.get("vram_gb")
                if inferred_vram and current_vram:
                    try:
                        if int(current_vram) != int(inferred_vram):
                            errors.append(
                                f"{section}.{item_id}: vram_gb={current_vram} conflicts with model token {inferred_vram}GB"
                            )
                    except (TypeError, ValueError):
                        errors.append(f"{section}.{item_id}: invalid vram_gb={current_vram}")

        for field in sorted(WARN_FIELDS.get(section, set())):
            missing_items = [item.get("id", "<no-id>") for item in items if not item.get(field)]
            if missing_items:
                sample = ", ".join(missing_items[:5])
                warnings.append(
                    f"{section}: {len(missing_items)}/{len(items)} missing or empty {field}"
                    + (f" (sample: {sample})" if sample else "")
                )
        for field in sorted(NOTE_FIELDS.get(section, set())):
            missing_items = [item.get("id", "<no-id>") for item in items if not item.get(field)]
            if missing_items:
                sample = ", ".join(missing_items[:5])
                notes.append(
                    f"{section}: {len(missing_items)}/{len(items)} missing or empty {field}"
                    + (f" (sample: {sample})" if sample else "")
                )
        coverage_rows.extend(_coverage_rows(section, items))

    # Load cases.yaml
    cases_path = DATA / "cases.yaml"
    if not cases_path.exists():
        print(f"FAIL: {cases_path} not found")
        return 1

    with cases_path.open("r", encoding="utf-8") as f:
        cases = yaml.safe_load(f)

    case_items = cases.get("cases", [])
    counts["cases"] = len(case_items)

    for case in case_items:
        case_id = case.get("id", "<no-id>")
        if str(case_id).startswith("cat-") or "--" in str(case_id):
            errors.append(f"cases.{case_id}: imported id was not normalized")
        if not case.get("brand"):
            errors.append(f"cases.{case_id}: missing brand")
        if not case.get("motherboard_support"):
            warnings.append(f"cases.{case_id}: no motherboard_support")
        if not case.get("gpu_length_mm"):
            warnings.append(f"cases.{case_id}: no gpu_length_mm")
        if not _valid_fan_mounts(case.get("fan_mounts")):
            errors.append(f"cases.{case_id}: invalid fan_mounts={case.get('fan_mounts')}")
    missing_case_prices = [case.get("id", "<no-id>") for case in case_items if case.get("price_cny") is None]
    if missing_case_prices:
        sample = ", ".join(missing_case_prices[:5])
        warnings.append(
            f"cases: {len(missing_case_prices)}/{len(case_items)} missing price_cny"
            + (f" (sample: {sample})" if sample else "")
        )
    coverage_rows.extend(_coverage_rows("cases", case_items))

    # Report
    if errors:
        print("VALIDATION FAILED")
        for e in errors:
            print(f"  ❌ {e}")
        for w in warnings:
            print(f"  ⚠️ {w}")
        return 1

    print("component library validation OK")
    print(f"sections: {', '.join(REQUIRED_SECTIONS)} + cases")
    for sec, count in counts.items():
        print(f"  {sec}: {count} items")

    status_counts = {}
    for section in REQUIRED_SECTIONS:
        for item in lib.get(section, []):
            ps = item.get("price_status", "unknown")
            status_counts[ps] = status_counts.get(ps, 0) + 1
    print(f"price status counts: {status_counts}")

    if coverage_rows:
        print("\nfield coverage (raw/effective):")
        for row in coverage_rows:
            print(f"  {row}")

    if warnings:
        print(f"\nwarnings ({len(warnings)}):")
        for w in warnings:
            print(f"  ⚠️ {w}")
    if notes:
        print(f"\nnon-blocking notes ({len(notes)}):")
        for n in notes:
            print(f"  ℹ️ {n}")

    return 0


def _has_value(item, field):
    value = item.get(field)
    if field in {"length_mm", "gpu_length_mm", "cpu_cooler_height_mm", "height_mm"} and value == 0:
        return False
    if field == "fan_mounts" and not _valid_fan_mounts(value):
        return False
    return value not in (None, "", [], {})


def _coverage_rows(section, items):
    rows = []
    fields = COVERAGE_FIELDS.get(section, [])
    if not fields:
        return rows
    enriched_items = [enrich_item(section, item) for item in items]
    total = len(items) or 1
    for field in fields:
        raw = sum(1 for item in items if _has_value(item, field))
        effective = sum(1 for item in enriched_items if _has_value(item, field))
        if raw != total or effective != total:
            rows.append(f"{section}.{field}: raw {raw}/{total}, effective {effective}/{total}")
    return rows


if __name__ == "__main__":
    sys.exit(main())
