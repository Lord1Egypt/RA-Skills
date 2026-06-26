from __future__ import annotations

from collections import defaultdict
from datetime import datetime, timezone

from smart_home.models import AnalysisResult, AreaAnalysis, Device

POWER_UNITS = {"W", "kW"}
ENERGY_UNITS = {"Wh", "kWh"}

ATTR_POWER_KEYS = ("power", "current_power", "power_consumption")


def normalize_power(value: float, unit: str) -> float | None:
    """Convert power value to watts. Returns None for energy (cumulative) units."""
    if unit in ENERGY_UNITS:
        return None
    if unit == "kW":
        return value * 1000
    return value  # W


def extract_power_value(entity: dict) -> float | None:
    """Extract power in watts from an entity, auto-detecting source."""
    attrs = entity.get("attributes", {})
    unit = attrs.get("unit_of_measurement", "")

    # Try state first
    try:
        raw = float(entity["state"])
        watts = normalize_power(raw, unit)
        if watts is not None:
            return watts
    except (ValueError, TypeError):
        pass

    # Fallback to attribute-based power
    for key in ATTR_POWER_KEYS:
        if key in attrs:
            try:
                raw = float(attrs[key])
                watts = normalize_power(raw, unit)
                if watts is not None:
                    return watts
            except (ValueError, TypeError):
                continue

    return None


def analyze(
    entities: list[dict],
    entity_area_map: dict[str, str],
) -> AnalysisResult:
    """Analyze filtered entities: normalize, group by area, rank."""
    devices_by_area: dict[str, list[Device]] = defaultdict(list)
    all_devices: list[Device] = []

    for entity in entities:
        watts = extract_power_value(entity)
        if watts is None:
            continue

        entity_id = entity["entity_id"]
        name = entity.get("attributes", {}).get("friendly_name", entity_id)
        area = entity_area_map.get(entity_id, "Unassigned")

        device = Device(entity_id=entity_id, name=name, watts=watts, area=area)
        devices_by_area[area].append(device)
        all_devices.append(device)

    areas = [
        AreaAnalysis(name=name, devices=sorted(devs, key=lambda d: d.watts, reverse=True))
        for name, devs in sorted(
            devices_by_area.items(),
            key=lambda item: sum(d.watts for d in item[1]),
            reverse=True,
        )
    ]

    total = sum(d.watts for d in all_devices)
    highest = max(all_devices, key=lambda d: d.watts) if all_devices else None

    return AnalysisResult(
        timestamp=datetime.now(timezone.utc).isoformat(),
        total_consumption_w=total,
        highest_consumer=highest,
        areas=areas,
    )
