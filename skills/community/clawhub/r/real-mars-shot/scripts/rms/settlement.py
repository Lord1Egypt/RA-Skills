"""Monthly resource balance for an off-world site.

The independence clock advances only on a month that meets the ember
thresholds with local production. Stores can keep people alive and still
not count. A resupply resets that clock.

Foothold clocks are separate from the ember.

Human days: 30-day months in which a crew stays alive and local food, oxygen,
and water cover a real share. Stores may fill the gap. They cannot, alone,
advance the clock. A death resets it. Earth cargo does not.

Human years: the same month also counts toward a century only when the
settlement is multi-generational (enough people, and at least one birth).

Biology years: a reproducing Earth species in a sheltered niche, with local
water and power, and no Earth arrival. Open sky does not count. A tardigrade
exposure does not count. Ten years is the established tier. The deep tier
uses the same clock.

Machines do not need oxygen. A replicator month needs ore, metal, electric
power, radiators, repair, and copy fidelity. Tended years advance only when
that replicator is also keeping a living, reproducing culture and an archive.
"""

from __future__ import annotations

from typing import Any

from rms.data import V, organisms
from rms.physics import (
    annual_habitat_dose_mSv,
    local_food_kg_per_day,
    power_demand_kwe,
    power_worst_kwe,
    wastewater_kg_per_cm_d,
)


def _o2_and_water(site: dict[str, Any], crew: int, days: float) -> dict[str, float]:
    o2_need = crew * V("human", "o2_kg_per_cm_d") * days
    food_dry = local_food_kg_per_day(site) * days
    plants = min(o2_need, food_dry * V("human", "o2_from_plants_kg_per_kg_dry_food"))
    o2_isru = float(site.get("isru_o2_kg_year", 0.0)) * days / 365.25
    renew_water = float(site.get("isru_water_kg_year", 0.0)) * days / 365.25
    recovery = float(site.get("water_recovery", 0.0))
    makeup = crew * wastewater_kg_per_cm_d() * days * (1.0 - recovery)
    water_left = renew_water - makeup
    extra_o2 = 0.0
    if site.get("electrolysis") and water_left > 0:
        sab = float(site.get("sabatier_fraction", 0.0))
        water_per_o2 = (18.0 / 16.0) * (1.0 - sab if sab > 0 else 1.0)
        extra_o2 = water_left / water_per_o2
    return {
        "o2_need": o2_need,
        "o2_renew": o2_isru + plants + extra_o2,
        "food_dry": food_dry,
        "food_need": crew * V("human", "food_solids_kg_per_cm_d") * days,
        "makeup": makeup,
        "renew_water": renew_water,
        "water_left_after_makeup": water_left,
    }


def evaluate_month(site_name: str, site: dict[str, Any]) -> dict[str, Any]:
    crew = int(site.get("population", 0))
    demand = power_demand_kwe(site)
    worst = power_worst_kwe(site_name, site)
    power_ratio = (worst / demand) if demand > 0 else (1.0 if crew == 0 else 0.0)
    if crew <= 0:
        return {
            "crew": 0,
            "power_ratio": power_ratio,
            "survival": True,
            "win_month": False,
            "reason": "uncrewed",
        }
    flows = _o2_and_water(site, crew, 30.0)
    food_ratio = flows["food_dry"] / flows["food_need"] if flows["food_need"] else 1.0
    o2_ratio = flows["o2_renew"] / flows["o2_need"] if flows["o2_need"] else 1.0
    water_ok = flows["water_left_after_makeup"] >= -1e-9
    dose = annual_habitat_dose_mSv(site_name, float(site.get("shielding_g_cm2", 0.0)))
    survival = (
        food_ratio >= 1.0 - 1e-9
        and o2_ratio >= 1.0 - 1e-9
        and water_ok
        and power_ratio >= 1.0 - 1e-9
    )
    win_month = (
        food_ratio >= V("win", "food_local_fraction") - 1e-9
        and o2_ratio >= V("win", "o2_margin") - 1e-9
        and water_ok
        and power_ratio >= V("win", "power_margin_worst_case") - 1e-9
        and dose["meets_target"]
        and float(site.get("water_recovery", 0.0)) >= V("win", "water_recovery_min") - 1e-9
    )
    return {
        "crew": crew,
        "power_ratio": power_ratio,
        "power_worst_kwe": worst,
        "power_demand_kwe": demand,
        "food_ratio": food_ratio,
        "o2_ratio": o2_ratio,
        "water_covered_by_isru": water_ok,
        "dose": dose,
        "survival": survival and True,
        "win_month": win_month,
        "flows": flows,
    }


def foothold_month(site_name: str, site: dict[str, Any], month: dict[str, Any] | None = None) -> dict[str, Any]:
    """Whether this month counts toward a 500-day foothold. Does not mutate."""
    month = evaluate_month(site_name, site) if month is None else month
    crew = int(site.get("population", 0))
    min_people = int(V("win", "foothold_min_population"))
    reasons: list[str] = []
    if not site.get("habitat"):
        reasons.append("no_habitat")
    if crew < min_people:
        reasons.append("population")
    flows = month.get("flows")
    if crew <= 0 or not isinstance(flows, dict):
        reasons.append("uncrewed")
        return {"ok": False, "reasons": reasons, "checks": {}, "gaps": {}, "month": month}
    food_gap = max(0.0, float(flows["food_need"]) - float(flows["food_dry"]))
    o2_gap = max(0.0, float(flows["o2_need"]) - float(flows["o2_renew"]))
    water_gap = max(0.0, float(flows["makeup"]) - float(flows["renew_water"]))
    stores = site.get("stores") or {}
    checks = {
        "food_local": float(month.get("food_ratio", 0.0)) + 1e-9 >= V("win", "foothold_food_local_fraction"),
        "o2_local": float(month.get("o2_ratio", 0.0)) + 1e-9 >= V("win", "foothold_o2_local_fraction"),
        "water_local": float(flows["renew_water"]) + 1e-9 >= V("win", "foothold_water_local_fraction") * float(flows["makeup"]),
        "food_alive": float(stores.get("food_kg", 0.0)) + 1e-9 >= food_gap,
        "o2_alive": float(stores.get("o2_kg", 0.0)) + 1e-9 >= o2_gap,
        "water_alive": float(stores.get("water_kg", 0.0)) + 1e-9 >= water_gap,
        "power": float(month.get("power_ratio", 0.0)) + 1e-9 >= V("win", "foothold_power_margin"),
        "dose": float(month["dose"]["mSv_per_year"]) <= V("win", "foothold_dose_mSv_per_year") + 1e-9,
    }
    failed = [name for name, ok in checks.items() if not ok]
    return {
        "ok": not reasons and not failed,
        "reasons": reasons + failed,
        "checks": checks,
        "gaps": {"food_kg": food_gap, "o2_kg": o2_gap, "water_kg": water_gap},
        "month": {key: month[key] for key in month if key != "flows"},
    }


def reproducing_level(site: dict[str, Any]) -> int:
    """Highest culture level on this world, ignoring survival-only organisms."""
    cards = organisms()
    best = 0
    for name, level in (site.get("organisms") or {}).items():
        card = cards.get(name) or {}
        if card.get("survival_only"):
            continue
        best = max(best, int(level))
    return best


def sheltered_niche(site: dict[str, Any]) -> bool:
    """A greenhouse, or a buried habitat. Open regolith is not a niche."""
    if site.get("greenhouse"):
        return True
    shield = float(site.get("shielding_g_cm2", 0.0))
    return bool(site.get("habitat")) and shield + 1e-9 >= V("win", "foothold_bio_shield_g_cm2")


def biology_month(site_name: str, site: dict[str, Any]) -> dict[str, Any]:
    """Closed, reproducing Earth life. Does not mutate."""
    reasons: list[str] = []
    if not sheltered_niche(site):
        reasons.append("open_surface")
    if reproducing_level(site) < int(V("win", "foothold_biology_min_level")):
        reasons.append("not_reproducing")
    if float(site.get("isru_water_kg_year", 0.0)) + 1e-9 < V("win", "foothold_bio_water_kg_year"):
        reasons.append("water")
    if power_worst_kwe(site_name, site) + 1e-9 < V("win", "foothold_bio_power_kwe"):
        reasons.append("power")
    return {"ok": not reasons, "reasons": reasons}


def heat_required_kwe(site: dict[str, Any]) -> float:
    """Radiators must cover a floor, and fission waste heat above that."""
    floor = float(V("win", "foothold_machine_heat_floor_kwe"))
    per_kwe = float(V("win", "foothold_machine_heat_per_kwe"))
    fission = float(site.get("fission_kwe", 0.0))
    return max(floor, fission * per_kwe)


def machine_replicator(site_name: str, site: dict[str, Any]) -> dict[str, Any]:
    """Ore, energy, heat, repair, fidelity. Oxygen is not a machine need."""
    reasons: list[str] = []
    repair = float(site.get("repair_fraction", 0.0))
    failure = float(V("win", "foothold_machine_failure_fraction"))
    repair_floor = float(V("win", "foothold_machine_repair_fraction"))
    industry = float(site.get("industrial_closure", 0.0))
    repair_ok = repair + 1e-9 >= max(failure, repair_floor) or industry + 1e-9 >= float(V("win", "foothold_machine_industry"))
    if int(site.get("robots", 0)) < int(V("win", "foothold_machine_robots")):
        reasons.append("robots")
    if float(site.get("isru_metal_t_year", 0.0)) + 1e-9 < float(V("win", "foothold_machine_metal_t_year")):
        reasons.append("metal")
    if float(site.get("ore_reserve_t", 0.0)) + 1e-9 < float(V("win", "foothold_machine_ore_t")):
        reasons.append("ore")
    if power_worst_kwe(site_name, site) + 1e-9 < float(V("win", "foothold_machine_power_kwe")):
        reasons.append("power")
    if float(site.get("heat_reject_kwe", 0.0)) + 1e-9 < heat_required_kwe(site):
        reasons.append("heat")
    if not repair_ok:
        reasons.append("repair")
    if float(site.get("replication_fidelity", 0.0)) + 1e-9 < float(V("win", "foothold_machine_fidelity_min")):
        reasons.append("fidelity")
    return {"ok": not reasons, "reasons": reasons, "heat_required_kwe": heat_required_kwe(site)}


def tended_life(site_name: str, site: dict[str, Any]) -> dict[str, Any]:
    """A replicator that is also keeping a living culture it can re-seed."""
    machines = machine_replicator(site_name, site)
    life = biology_month(site_name, site)
    reasons = list(machines["reasons"]) + [item for item in life["reasons"] if item not in machines["reasons"]]
    if int(site.get("life_archive_accessions", 0)) < int(V("win", "foothold_machine_archive_accessions")):
        reasons.append("archive")
    return {"ok": not reasons, "reasons": reasons, "life": life["ok"], "replicator": machines["ok"]}


def machine_month(site_name: str, site: dict[str, Any]) -> dict[str, Any]:
    """Backward-compatible name. This is the replicator, not tended life."""
    report = machine_replicator(site_name, site)
    report["life"] = biology_month(site_name, site)["ok"]
    return report


def _tick_months(site: dict[str, Any], field: str, ok: bool, *, resupply: bool) -> str:
    if resupply or not ok:
        site[field] = 0
        return "reset_resupply" if resupply else "reset"
    site[field] = int(site.get(field, 0)) + 1
    return "advanced"


def _tick_years(site: dict[str, Any], field: str, ok: bool, *, resupply: bool, independent: bool) -> str:
    """Month-scale progress. An Earth landing wipes the clock.

    Before the path has entered an epoch, a failed month wipes it too.
    After that, one bad month holds the deep clock instead of erasing it.
    """
    if resupply:
        site[field] = 0.0
        return "reset_resupply"
    if not ok:
        if independent:
            return "held"
        site[field] = 0.0
        return "reset"
    step = float(V("win", "foothold_month_days")) / 365.25
    site[field] = float(site.get(field, 0.0)) + step
    return "advanced"


def _advance_foothold(
    site_name: str,
    site: dict[str, Any],
    month: dict[str, Any],
    *,
    population_before: int,
    fatalities_before: int,
) -> dict[str, Any]:
    qualifying = foothold_month(site_name, site, month)
    population = int(site.get("population", 0))
    fatalities = int(site.get("fatalities", 0))
    min_people = int(V("win", "foothold_min_population"))
    broken = fatalities > fatalities_before or population < population_before or population < min_people
    independent = bool((site.get("epoch_paths") or {}).get("human"))
    century = (
        qualifying["ok"]
        and not broken
        and population >= int(V("win", "foothold_century_min_population"))
        and int(site.get("births", 0)) >= int(V("win", "foothold_century_min_births"))
    )
    if century:
        step = float(V("win", "foothold_month_days")) / 365.25
        site["inhabited_years"] = float(site.get("inhabited_years", 0.0)) + step
    elif broken or not independent:
        site["inhabited_years"] = 0.0
    if qualifying["ok"] and not broken:
        for kind, gap in qualifying["gaps"].items():
            if gap > 0:
                site["stores"][kind] = float(site["stores"][kind]) - float(gap)
        site["inhabited_days"] = int(site.get("inhabited_days", 0)) + int(V("win", "foothold_month_days"))
        qualifying["clock"] = "advanced"
    else:
        site["inhabited_days"] = 0
        qualifying["clock"] = "reset"
        if broken:
            qualifying["reasons"] = list(qualifying.get("reasons", [])) + ["death_or_population"]
    qualifying["inhabited_days"] = int(site.get("inhabited_days", 0))
    return qualifying


def apply_month(state: dict[str, Any], site_name: str, resupply: bool = False) -> dict[str, Any]:
    site = state["sites"][site_name]
    before = int(site.get("dust_storm_months_left", 0))
    population_before = int(site.get("population", 0))
    fatalities_before = int(site.get("fatalities", 0))
    report = evaluate_month(site_name, site)
    report["site"] = site_name
    if resupply and site.get("trial"):
        site["independent_months"] = 0
        report["clock"] = "reset_resupply"
    elif site.get("trial") and int(site.get("population", 0)) > 0:
        if report["win_month"] and not resupply:
            site["independent_months"] = int(site.get("independent_months", 0)) + 1
            report["clock"] = "advanced"
        elif not report["survival"]:
            site["independent_months"] = 0
            report["clock"] = "reset_shortfall"
            _harm(state, site_name, report)
        else:
            report["clock"] = "held"
    report["foothold"] = _advance_foothold(
        site_name,
        site,
        report,
        population_before=population_before,
        fatalities_before=fatalities_before,
    )
    if resupply:
        site["epoch_paths"] = {}
    paths = site.get("epoch_paths") or {}
    bio = biology_month(site_name, site)
    bio["clock"] = _tick_months(site, "biology_closed_months", bio["ok"], resupply=resupply)
    bio["years_clock"] = _tick_years(site, "biology_years", bio["ok"], resupply=resupply, independent=bool(paths.get("biology")))
    bio["months"] = int(site.get("biology_closed_months", 0))
    bio["years"] = float(site.get("biology_years", 0.0))
    machines = machine_replicator(site_name, site)
    machines["clock"] = _tick_months(site, "machine_replicator_months", machines["ok"], resupply=resupply)
    machines["years_clock"] = _tick_years(
        site, "machine_years", machines["ok"], resupply=resupply, independent=bool(paths.get("machine"))
    )
    tended = tended_life(site_name, site)
    tended["clock"] = _tick_months(site, "machine_tended_months", tended["ok"], resupply=resupply)
    tended["years_clock"] = _tick_years(
        site, "tended_years", tended["ok"], resupply=resupply, independent=bool(paths.get("machine"))
    )
    machines["months"] = int(site.get("machine_replicator_months", 0))
    machines["years"] = float(site.get("machine_years", 0.0))
    report["biology_foothold"] = bio
    report["machine_foothold"] = machines
    report["tended_life"] = tended
    if before > 0:
        site["dust_storm_months_left"] = before - 1
        if site["dust_storm_months_left"] == 0 and site.get("robots"):
            if site.get("rtg") or float(site.get("fission_kwe", 0)) > 0 or float(site.get("battery_kwe", 0)) > 0:
                site["survived_dust_season"] = True
                report["dust_season_survived"] = True
    return report


def _harm(state: dict[str, Any], site_name: str, report: dict[str, Any]) -> None:
    site = state["sites"][site_name]
    population = int(site.get("population", 0))
    if population <= 0:
        return
    power_ratio = float(report.get("power_ratio", 0))
    loss = 1 if power_ratio > 0.3 else max(1, population // 2)
    loss = min(population, loss)
    site["population"] = population - loss
    site["fatalities"] = int(site.get("fatalities", 0)) + loss
    state["public_opinion"] = max(0, state["public_opinion"] - 6)
    report["casualties"] = loss
    if site["population"] == 0 and site.get("trial"):
        can_rescue = state["earth_stability"] >= 25 and state["treasury_busd"] > 0.5
        if can_rescue:
            site["trial"] = False
            site["evacuated"] = True
            state["treasury_busd"] -= 0.4
            report["evacuated"] = True
        else:
            site["extinct"] = True
            report["extinct"] = True
