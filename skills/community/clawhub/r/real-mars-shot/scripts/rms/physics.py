"""Rocket equation, radiation, consumables, calendars, fleet capacity.

Published rates are reproduced when extra shielding is zero. Estimates are
flagged by the science file and must stay flagged in tool output.
"""

from __future__ import annotations

import datetime as dt
import math
from typing import Any

from rms.data import V, meta, sci

G0 = V("constants", "g0_m_s2")


def mass_ratio(delta_v_m_s: float, isp_s: float, g0: float = G0) -> float:
    """Tsiolkovsky mass ratio m0/mf."""
    if isp_s <= 0:
        raise ValueError("Isp must be positive")
    if delta_v_m_s < 0:
        raise ValueError("delta-v must be non-negative")
    return math.exp(delta_v_m_s / (isp_s * g0))


def delta_v(isp_s: float, mass_ratio_value: float, g0: float = G0) -> float:
    if mass_ratio_value <= 0:
        raise ValueError("mass ratio must be positive")
    return isp_s * g0 * math.log(mass_ratio_value)


def propellant_kg(payload_kg: float, delta_v_m_s: float, isp_s: float, dry_fraction: float = 0.0) -> dict[str, Any]:
    """Single-stage propellant for a payload plus optional inert mass fraction of propellant.

    dry_fraction is unused structure mass as a fraction of propellant. Default 0
    is the ideal rocket around a payload that is itself the burnout mass.
    """
    ratio = mass_ratio(delta_v_m_s, isp_s)
    # m0 = ratio * mf, mf = payload + dry, dry = dry_fraction * propellant
    # m0 = mf + propellant = ratio * mf
    # propellant = mf * (ratio - 1)
    # mf = payload + dry_fraction * propellant
    # propellant = (payload + dry_fraction * propellant) * (ratio - 1)
    # propellant = payload * (ratio - 1) / (1 - dry_fraction * (ratio - 1))
    gain = ratio - 1.0
    denom = 1.0 - dry_fraction * gain
    if denom <= 0:
        raise ValueError("dry fraction too high for this delta-v")
    prop = payload_kg * gain / denom
    mf = payload_kg + dry_fraction * prop
    return {
        "formula": "delta_v = Isp * g0 * ln(m0/mf)",
        "g0_m_s2": G0,
        "isp_s": isp_s,
        "delta_v_m_s": delta_v_m_s,
        "mass_ratio": ratio,
        "payload_kg": payload_kg,
        "burnout_kg": mf,
        "propellant_kg": prop,
        "initial_kg": mf + prop,
        "estimate": True,
        "source_id": "tsiolkovsky",
    }


def stack_imleo_kg(payload_kg: float, burns: list[dict[str, float]]) -> dict[str, Any]:
    """Apply burns from the last one back to LEO. Each burn: dv_m_s, isp_s, optional factor."""
    mass = float(payload_kg)
    steps = []
    for burn in reversed(burns):
        before = mass
        factor = float(burn.get("factor", 1.0))
        mass *= mass_ratio(float(burn["dv_m_s"]), float(burn["isp_s"]))
        mass *= factor
        steps.append({"burn": burn, "mass_after_kg": mass, "mass_before_kg": before})
    steps.reverse()
    return {
        "payload_kg": payload_kg,
        "imleo_kg": mass,
        "imleo_t": mass / 1000.0,
        "steps": steps,
        "estimate": True,
        "source_id": "tsiolkovsky",
    }


def lunar_cargo_imleo_t(surface_t: float, transfer_isp_s: float | None = None) -> dict[str, Any]:
    isp_transfer = V("propulsion", "hydrolox_vacuum_isp_s") if transfer_isp_s is None else transfer_isp_s
    isp_land = V("propulsion", "storable_isp_s")
    result = stack_imleo_kg(
        surface_t * 1000.0,
        [
            {"name": "leo_to_tli", "dv_m_s": V("delta_v_m_s", "leo_to_tli"), "isp_s": isp_transfer},
            {"name": "tli_to_llo", "dv_m_s": V("delta_v_m_s", "tli_to_llo"), "isp_s": isp_land},
            {"name": "llo_to_surface", "dv_m_s": V("delta_v_m_s", "llo_to_surface"), "isp_s": isp_land},
        ],
    )
    result["destination"] = "moon"
    result["note"] = "One-way cargo. No return propellant. Planning delta-v, estimate."
    return result


def mars_cargo_imleo_t(surface_t: float, transfer_isp_s: float | None = None) -> dict[str, Any]:
    isp_transfer = V("propulsion", "hydrolox_vacuum_isp_s") if transfer_isp_s is None else transfer_isp_s
    isp_land = V("propulsion", "storable_isp_s")
    result = stack_imleo_kg(
        surface_t * 1000.0,
        [
            {"name": "leo_to_tmi", "dv_m_s": V("delta_v_m_s", "leo_to_tmi_min_energy"), "isp_s": isp_transfer},
            {
                "name": "aeroshell",
                "dv_m_s": 0.0,
                "isp_s": isp_transfer,
                "factor": V("delta_v_m_s", "mars_aeroshell_mass_factor"),
            },
            {
                "name": "edl_overhead",
                "dv_m_s": 0.0,
                "isp_s": isp_transfer,
                "factor": V("delta_v_m_s", "mars_edl_systems_overhead"),
            },
            {"name": "terminal_descent", "dv_m_s": V("delta_v_m_s", "mars_terminal_descent"), "isp_s": isp_land},
        ],
    )
    result["destination"] = "mars"
    result["note"] = (
        "One-way cargo with aerocapture-class entry, an aeroshell factor, and an EDL overhead. "
        "Estimate. Heritage landed mass is about 1 t until heavy EDL is in hand."
    )
    return result


def shield_transmission(extra_g_cm2: float) -> float:
    """Additional shielding on top of the published reference environment.

    extra = 0 reproduces MSL cruise or MSL surface rates. This curve is an
    estimate, not a radiation-transport code.
    """
    if extra_g_cm2 < 0:
        raise ValueError("shielding cannot be negative")
    scale = V("radiation", "shield_scale_g_cm2")
    return 1.0 / (1.0 + extra_g_cm2 / scale)


def dose_mSv(rate_mSv_per_day: float, days: float, extra_g_cm2: float = 0.0) -> float:
    return rate_mSv_per_day * days * shield_transmission(extra_g_cm2)


def conjunction_dose_mSv(
    transit_extra_g_cm2: float = 0.0,
    surface_extra_g_cm2: float = 0.0,
    outbound_days: float | None = None,
    surface_days: float | None = None,
    return_days: float | None = None,
) -> dict[str, Any]:
    out_days = V("campaign", "reference_outbound_days") if outbound_days is None else outbound_days
    stay = V("campaign", "reference_surface_days") if surface_days is None else surface_days
    back = V("campaign", "reference_return_days") if return_days is None else return_days
    cruise_rate = V("radiation", "cruise_mSv_per_day")
    surface_rate = V("radiation", "mars_surface_mSv_per_day")
    transit = dose_mSv(cruise_rate, out_days + back, transit_extra_g_cm2)
    surface = dose_mSv(surface_rate, stay, surface_extra_g_cm2)
    total = transit + surface
    return {
        "transit_mSv": transit,
        "surface_mSv": surface,
        "total_mSv": total,
        "total_Sv": total / 1000.0,
        "outbound_days": out_days,
        "surface_days": stay,
        "return_days": back,
        "transit_extra_g_cm2": transit_extra_g_cm2,
        "surface_extra_g_cm2": surface_extra_g_cm2,
        "cruise_rate_note": meta(sci("radiation", "cruise_mSv_per_day")),
        "surface_rate_note": meta(sci("radiation", "mars_surface_mSv_per_day")),
        "shield_model_estimate": True,
        "career_cap_mSv": V("radiation", "career_planning_cap_mSv"),
        "career_cap_is_estimate": True,
        "exceeds_planning_cap": total > V("radiation", "career_planning_cap_mSv"),
    }


def lunar_sortie_dose_mSv(transit_extra_g_cm2: float = 0.0, surface_extra_g_cm2: float = 0.0) -> dict[str, Any]:
    # DRA comparison: ~4 days out, ~7 days on the surface, ~4 days back, ~18 days total.
    transit_days = 8.0
    surface_days = 7.0
    transit = dose_mSv(V("radiation", "cruise_mSv_per_day"), transit_days, transit_extra_g_cm2)
    surface = dose_mSv(V("radiation", "lunar_surface_mSv_per_day"), surface_days, surface_extra_g_cm2)
    total = transit + surface
    return {
        "transit_mSv": transit,
        "surface_mSv": surface,
        "total_mSv": total,
        "transit_days": transit_days,
        "surface_days": surface_days,
        "lunar_rate_is_estimate": True,
        "source_id": "nasa_dra5_2009",
    }


def annual_habitat_dose_mSv(site: str, extra_g_cm2: float) -> dict[str, Any]:
    if site == "moon":
        rate = V("radiation", "lunar_surface_mSv_per_day")
        estimate = True
        source = "game_calibration"
    elif site == "mars":
        rate = V("radiation", "mars_surface_mSv_per_day")
        estimate = False
        source = "zeitlin2014_surface"
    elif site == "freespace":
        rate = V("radiation", "cruise_mSv_per_day")
        estimate = False
        source = "zeitlin2013_cruise"
    else:
        raise ValueError(site)
    annual = dose_mSv(rate, 365.25, extra_g_cm2)
    target = V("radiation", "settlement_design_target_mSv_per_year")
    return {
        "site": site,
        "extra_g_cm2": extra_g_cm2,
        "mSv_per_year": annual,
        "target_mSv_per_year": target,
        "meets_target": annual <= target,
        "rate_is_estimate": estimate or extra_g_cm2 != 0.0,
        "source_id": source if extra_g_cm2 == 0.0 else "game_calibration",
    }


def wastewater_kg_per_cm_d() -> float:
    return (
        V("human", "fecal_water_kg_per_cm_d")
        + V("human", "respiration_perspiration_water_kg_per_cm_d")
        + V("human", "urine_water_kg_per_cm_d")
    )


def consumables(
    crew: int,
    days: float,
    water_recovery: float = 0.0,
    food_closure: float = 0.0,
    o2_mode: str = "open",
    sabatier_fraction: float | None = None,
) -> dict[str, Any]:
    """Life-support logistics for `crew` people over `days`.

    o2_mode:
      open — ship oxygen tanks
      electrolysis — split water, vent the hydrogen, no CO2 recovery
      sabatier — recover a fraction of oxygen from CO2; ship the rest as water
    """
    if crew < 0 or days < 0:
        raise ValueError("crew and days must be non-negative")
    if not 0.0 <= water_recovery <= 1.0:
        raise ValueError("water recovery must be in [0, 1]")
    if not 0.0 <= food_closure <= 1.0:
        raise ValueError("food closure must be in [0, 1]")
    person_days = crew * days
    food_kg = person_days * V("human", "food_logistics_kg_per_cm_d") * (1.0 - food_closure)
    food_dry_need = person_days * V("human", "food_solids_kg_per_cm_d")
    water_loss = person_days * wastewater_kg_per_cm_d() * (1.0 - water_recovery)
    o2_need = person_days * V("human", "o2_kg_per_cm_d")
    co2_kg = person_days * V("human", "co2_kg_per_cm_d")
    water_for_o2 = 0.0
    o2_tanks = 0.0
    if o2_mode == "open":
        o2_tanks = o2_need
    elif o2_mode == "electrolysis":
        water_for_o2 = o2_need * (18.0 / 16.0)
    elif o2_mode == "sabatier":
        fraction = V("human", "o2_recovery_from_co2_current") if sabatier_fraction is None else sabatier_fraction
        water_for_o2 = o2_need * (18.0 / 16.0) * (1.0 - fraction)
    else:
        raise ValueError(o2_mode)
    shipped = food_kg + water_loss + water_for_o2 + o2_tanks
    return {
        "crew": crew,
        "days": days,
        "food_shipped_kg": food_kg,
        "food_dry_need_kg": food_dry_need,
        "water_makeup_kg": water_loss,
        "water_for_oxygen_kg": water_for_o2,
        "oxygen_tanks_kg": o2_tanks,
        "oxygen_need_kg": o2_need,
        "co2_produced_kg": co2_kg,
        "shipped_life_support_kg": shipped,
        "shipped_life_support_t": shipped / 1000.0,
        "water_recovery": water_recovery,
        "food_closure": food_closure,
        "o2_mode": o2_mode,
        "wastewater_kg_per_cm_d": wastewater_kg_per_cm_d(),
        "sources": ["nasa_bvad_2022", "nasa_iss_water_2023", "nasa_eclss_o2_2021"],
    }


def light_time_s(distance_m: float) -> float:
    return distance_m / V("constants", "c_m_s")


def comms_delay() -> dict[str, Any]:
    moon = light_time_s(V("bodies", "moon", "mean_distance_m"))
    mars_min = light_time_s(V("bodies", "mars", "distance_min_m"))
    mars_max = light_time_s(V("bodies", "mars", "distance_max_m"))
    return {
        "moon_one_way_s": moon,
        "mars_one_way_min_s": mars_min,
        "mars_one_way_max_s": mars_max,
        "mars_two_way_min_min": 2 * mars_min / 60.0,
        "mars_two_way_max_min": 2 * mars_max / 60.0,
        "source_id": "nasa_dra5_2009",
    }


def _parse_date(text: str) -> dt.date:
    year, month, day = (int(part) for part in text.split("-"))
    return dt.date(year, month, day)


def window_center(index: int) -> dt.date:
    ref = _parse_date(str(sci("bodies", "mars", "window_reference_date")["value"]))
    period = V("bodies", "mars", "synodic_days")
    ordinal = ref.toordinal() + int(round(index * period))
    return dt.date.fromordinal(ordinal)


def nearest_window(day: dt.date) -> tuple[dt.date, int]:
    ref = _parse_date(str(sci("bodies", "mars", "window_reference_date")["value"]))
    period = V("bodies", "mars", "synodic_days")
    delta = day.toordinal() - ref.toordinal()
    index = int(round(delta / period))
    return window_center(index), index


def in_mars_window(day: dt.date, half_width: float | None = None) -> bool:
    center, _index = nearest_window(day)
    width = V("bodies", "mars", "window_half_width_days") if half_width is None else half_width
    return abs(day.toordinal() - center.toordinal()) <= width


def month_in_window(year: int, month: int) -> bool:
    last = 28 if month == 2 else 30
    return any(in_mars_window(dt.date(year, month, day)) for day in (1, 15, last))


def add_months(year: int, month: int, months: int) -> tuple[int, int]:
    index = year * 12 + (month - 1) + months
    return index // 12, index % 12 + 1


def slip_to_window(year: int, month: int, max_slip: int = 40) -> tuple[int, int, int]:
    """Return year, month, months slipped so the departure month meets a window."""
    slipped = 0
    y, m = year, month
    while not month_in_window(y, m):
        if slipped >= max_slip:
            break
        y, m = add_months(y, m, 1)
        slipped += 1
    return y, m, slipped


def next_window_label(year: int, month: int) -> str:
    y, m, _slipped = slip_to_window(year, month)
    return f"{y:04d}-{m:02d}"


def campaign_imleo_t(crew: int, *, ntr: bool, consumables_t: float) -> dict[str, Any]:
    """IMLEO for a conjunction-class crewed Mars campaign, including cargo preposition.

    Chemical result is intended to sit above the DRA 800–1200 t band.
    NTR multiplies the stack so a 6-person reference case sits inside that band.
    Both the split and the multiplier are estimates anchored to DRA 5.0.
    """
    overhead = V("campaign", "mars_preposition_imleo_t")
    per = V("campaign", "mars_stack_imleo_t_per_crew_chemical")
    chemical = overhead + per * crew + consumables_t
    multiplier = V("propulsion", "ntr_imleo_multiplier") if ntr else 1.0
    total = chemical * multiplier
    return {
        "crew": crew,
        "ntr": ntr,
        "consumables_t": consumables_t,
        "chemical_imleo_t": chemical,
        "imleo_t": total,
        "multiplier": multiplier,
        "estimate": True,
        "source_id": "nasa_dra5_2009",
        "dra_band_t": [V("delta_v_m_s", "dra_campaign_imleo_t_low"), V("delta_v_m_s", "dra_campaign_imleo_t_high")],
    }


def annual_imleo_t(launch: dict[str, Any]) -> float:
    return (
        launch["heavy_per_year"] * launch["heavy_leo_t"]
        + launch["medium_per_year"] * launch["medium_leo_t"]
    )


def people_export(launch: dict[str, Any], *, qualified: int, pipeline_per_year: int, years: int = 10, ntr: bool = False) -> dict[str, Any]:
    """How many people Earth can send to Mars if the whole fleet is spent on crew campaigns.

    This is a ceiling, not a plan. Spending the fleet this way leaves no cargo,
    no ISRU, and no Earth-orbit logistics, and the ordering rules will punish it.
    """
    reference_crew = int(V("campaign", "reference_crew_mars"))
    # Closed-loop-ish water, open food: the reference logistics case.
    cons = consumables(reference_crew, V("campaign", "reference_outbound_days") + V("campaign", "reference_surface_days") + V("campaign", "reference_return_days"), water_recovery=0.98, food_closure=0.0, o2_mode="sabatier")
    campaign = campaign_imleo_t(reference_crew, ntr=ntr, consumables_t=cons["shipped_life_support_t"])
    imleo_year = annual_imleo_t(launch)
    mass_campaigns = (imleo_year * years) / campaign["imleo_t"] if campaign["imleo_t"] else 0.0
    windows = years * 365.25 / V("bodies", "mars", "synodic_days")
    campaigns = min(mass_campaigns, windows)
    by_mass = int(campaigns * reference_crew)
    by_people = qualified + pipeline_per_year * years
    sent = max(0, min(by_mass, by_people))
    return {
        "years": years,
        "imleo_t_per_year": imleo_year,
        "campaign_imleo_t": campaign["imleo_t"],
        "windows": windows,
        "people_by_mass_and_windows": by_mass,
        "people_by_training": by_people,
        "people": sent,
        "binding": "mass_and_windows" if by_mass <= by_people else "training",
        "ntr": ntr,
        "estimate": True,
        "note": "Ceiling if every launch of the decade flies crewed Mars campaigns and nothing else.",
        "source_id": "nasa_dra5_2009",
    }


def food_area_m2(crew: int, local_fraction: float | None = None) -> dict[str, Any]:
    fraction = V("win", "food_local_fraction") if local_fraction is None else local_fraction
    dry_per_day = crew * V("human", "food_solids_kg_per_cm_d") * fraction
    rate = V("human", "farm_dry_edible_kg_per_m2_d")
    area = dry_per_day / rate if rate else float("inf")
    power = area * V("human", "farm_light_kwe_per_m2")
    return {
        "crew": crew,
        "local_fraction": fraction,
        "area_m2": area,
        "light_kwe": power,
        "estimate": True,
        "source_id": "game_calibration",
    }


def power_demand_kwe(site: dict[str, Any]) -> float:
    crew = int(site.get("population", 0))
    habitat = 0.0
    if site.get("habitat") and crew:
        habitat = V("human", "habitat_base_kwe") + crew * V("human", "habitat_kwe_per_person")
    elif site.get("robots"):
        habitat = 0.2
    lights = float(site.get("farms_m2", 0.0)) * V("human", "farm_light_kwe_per_m2")
    isru = float(site.get("isru_o2_kg_year", 0.0)) * V("human", "electrolysis_kwh_per_kg_o2") / 8760.0
    return habitat + lights + isru


def power_worst_kwe(site_name: str, site: dict[str, Any]) -> float:
    solar = float(site.get("solar_kwe_clear", 0.0))
    if site_name == "moon":
        if site.get("polar"):
            solar *= V("bodies", "moon", "polar_illumination_fraction")
        else:
            solar = float(site.get("battery_kwe", 0.0))
    if site_name == "mars" and int(site.get("dust_storm_months_left", 0)) > 0:
        solar *= V("bodies", "mars", "dust_storm_solar_fraction")
    return solar + float(site.get("fission_kwe", 0.0))


def local_food_kg_per_day(site: dict[str, Any]) -> float:
    if float(site.get("farms_m2", 0.0)) <= 0:
        return 0.0
    return float(site["farms_m2"]) * V("human", "farm_dry_edible_kg_per_m2_d")
