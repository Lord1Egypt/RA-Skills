from __future__ import annotations

import json
import re

from smart_home.models import AnalysisResult, PipelineConfig


def format_summary(result: AnalysisResult) -> str:
    """Generate a 2-3 sentence human-readable summary."""
    if not result.areas:
        return "No energy data available. Check that your Home Assistant instance has entities with power units."

    if result.highest_consumer is None:
        return "No energy data available. Check that your Home Assistant instance has entities with power units."

    top = result.highest_consumer
    top_pct = (top.watts / result.total_consumption_w * 100) if result.total_consumption_w > 0 else 0
    top_area = top.area

    lines = [
        f"{top_area} is drawing {top.watts:,.0f}W — {top_pct:.0f}% of your total {result.total_consumption_w:,.1f}W.",
        f"The {top.name} is the single highest consumer at {top.watts:,.0f}W.",
        "No anomalies detected.",
    ]
    return " ".join(lines)


def format_table(result: AnalysisResult) -> str:
    """Generate a markdown table comparing Area | Device | Consumption."""
    if not result.areas:
        return "No data to display."

    lines = ["| Area | Device | Consumption (W) |", "|------|--------|-----------------|"]
    for area in result.areas:
        for device in area.devices:
            lines.append(f"| {area.name} | {device.name} | {device.watts:,.1f} |")
    return "\n".join(lines)


def _area_slug(area_name: str) -> str:
    """Convert area name to HA entity slug (lowercase, underscores)."""
    return re.sub(r"[^a-z0-9]", "_", area_name.lower()).strip("_")


def format_automation(
    result: AnalysisResult,
    config: PipelineConfig,
    known_entity_ids: set[str] | None = None,
) -> str:
    """Generate HA automation.create JSON for devices exceeding threshold."""
    automations = []
    known = known_entity_ids or set()

    for area in result.areas:
        for device in area.devices:
            if device.watts < config.threshold_watts:
                continue

            conditions = [
                {
                    "condition": "time",
                    "after": f"{config.time_after}:00",
                    "before": f"{config.time_before}:00",
                }
            ]

            # Add occupancy condition only if sensor exists
            occupancy_id = f"binary_sensor.{_area_slug(area.name)}_occupancy"
            if occupancy_id in known:
                conditions.append(
                    {
                        "condition": "state",
                        "entity_id": occupancy_id,
                        "state": config.require_occupancy,
                    }
                )

            # Derive switch entity from sensor entity
            switch_id = device.entity_id.replace("sensor.", "switch.").replace("_power", "").replace("_wattage", "")

            automations.append(
                {
                    "alias": f"High Power Alert - {area.name}",
                    "trigger": {
                        "platform": "numeric_state",
                        "entity_id": device.entity_id,
                        "above": int(config.threshold_watts),
                    },
                    "condition": conditions,
                    "action": {
                        "service": f"switch.{config.action}",
                        "target": {"entity_id": switch_id},
                    },
                }
            )

    return json.dumps(automations, indent=2)
