"""Doctrine gates. They describe the honest order; missions may still be attempted."""

from __future__ import annotations

from typing import Any

from rms.data import V


def gates(state: dict[str, Any]) -> dict[str, bool]:
    eclss = state["eclss"]
    moon = state["sites"]["moon"]
    mars = state["sites"]["mars"]
    bio = state["biology"]
    independence_months = max(
        int(moon.get("independent_months", 0)),
        int(mars.get("independent_months", 0)),
        int(state["sites"]["freespace"].get("independent_months", 0)),
    )
    return {
        "analog_30": int(eclss["closed_habitat_days_record"]) >= 30,
        "analog_365": int(eclss["closed_habitat_days_record"]) >= 365 and float(eclss["water_recovery_demonstrated"]) >= 0.93,
        "water_98": float(eclss["water_recovery_demonstrated"]) >= 0.98 and int(eclss["water_recovery_duration_days"]) >= 180,
        "moon_robot": int(moon["landings_success"]) >= 1,
        "moon_isru": float(moon["isru_water_kg_year"]) > 0 or float(moon["isru_o2_kg_year"]) > 0,
        "bio_simulant": int(bio["simulant_days"]) >= 90,
        "moon_crew_return": int(moon["crew_returned"]) >= 1,
        "mars_robot": int(mars["landings_success"]) >= 1,
        "mars_cargo": int(mars["cargo_landings"]) >= 1 and bool(mars["survived_dust_season"]),
        "mars_isru": float(mars["isru_o2_kg_year"]) >= V("bodies", "mars", "isru_pilot_o2_kg_per_year"),
        "mars_crew_return": int(mars["crew_returned"]) >= 1,
        "archive_on_earth": int(state["genome_archive_donors"]) >= int(V("win", "genome_archive_donors")),
        "independence": independence_months >= int(V("win", "independence_years") * 12),
    }


PHASE_ORDER = [
    ("analog_30", "earth_analog"),
    ("analog_365", "earth_analog"),
    ("moon_robot", "machines"),
    ("moon_isru", "moon"),
    ("bio_simulant", "biology"),
    ("moon_crew_return", "cislunar_crew"),
    ("mars_cargo", "mars_cargo"),
    ("mars_isru", "mars_cargo"),
    ("mars_crew_return", "mars_outpost"),
    ("independence", "independence"),
]


def current_phase(state: dict[str, Any]) -> str:
    if state.get("outcome") == "win":
        return "ember"
    snapshot = gates(state)
    phase = "independence"
    for gate_id, phase_name in PHASE_ORDER:
        if not snapshot[gate_id]:
            return phase_name
    return phase
