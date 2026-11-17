"""Mission profiles, rocket-equation mass, and ordering (impossible vs reckless)."""

from __future__ import annotations

import math
from typing import Any

from rms.data import V
from rms.gates import gates
from rms.physics import (
    add_months,
    annual_imleo_t,
    campaign_imleo_t,
    conjunction_dose_mSv,
    consumables,
    lunar_cargo_imleo_t,
    lunar_sortie_dose_mSv,
    mars_cargo_imleo_t,
    month_in_window,
    slip_to_window,
)
from rms.state import ready_crew

# Costs are program-scale estimates in billion USD, not a quote for a named rocket.
PROFILES: dict[str, dict[str, Any]] = {
    "lunar_probe": {
        "destination": "moon",
        "crew": 0,
        "payload_t": 0.4,
        "cost_busd": 0.15,
        "base_months": 8,
        "vehicle": "medium",
        "mass_model": "lunar_cargo",
    },
    "lunar_isru_demo": {
        "destination": "moon",
        "crew": 0,
        "payload_t": 1.8,
        "cost_busd": 0.7,
        "base_months": 14,
        "vehicle": "medium",
        "mass_model": "lunar_cargo",
        "requires_tech": ["lunar_isru_pilot"],
        "requires_flag": "moon.ice_confirmed",
    },
    "lunar_cargo": {
        "destination": "moon",
        "crew": 0,
        "payload_t": 4.0,
        "cost_busd": 1.1,
        "base_months": 12,
        "vehicle": "heavy",
        "mass_model": "lunar_cargo",
    },
    "lunar_crew_sortie": {
        "destination": "moon",
        "crew": 2,
        "payload_t": 0.0,
        "cost_busd": 2.6,
        "base_months": 10,
        "vehicle": "heavy",
        "mass_model": "lunar_sortie",
    },
    "lunar_outpost": {
        "destination": "moon",
        "crew": 4,
        "payload_t": 0.0,
        "cost_busd": 3.8,
        "base_months": 14,
        "vehicle": "heavy",
        "mass_model": "lunar_sortie_stay",
        "stay": True,
    },
    "greenhouse": {
        "destination": "moon",
        "crew": 0,
        "payload_t": 2.0,
        "cost_busd": 0.6,
        "base_months": 12,
        "vehicle": "medium",
        "mass_model": "auto",
        "farms_m2": 800,
    },
    "kilopower_unit": {
        "destination": "moon",
        "crew": 0,
        "payload_t": 1.5,
        "cost_busd": 0.9,
        "base_months": 14,
        "vehicle": "medium",
        "mass_model": "auto",
        "requires_tech": ["kilopower"],
        "fission_kwe": 10,
    },
    "reactor_module": {
        "destination": "moon",
        "crew": 0,
        "payload_t": 8.0,
        "cost_busd": 2.4,
        "base_months": 20,
        "vehicle": "heavy",
        "mass_model": "auto",
        "requires_tech": ["kilopower", "local_manufacturing"],
        "fission_kwe": 500,
        "fission_is_estimate": True,
    },
    "mars_relay": {
        "destination": "mars_orbit",
        "crew": 0,
        "payload_t": 0.6,
        "cost_busd": 0.35,
        "base_months": 12,
        "vehicle": "medium",
        "mass_model": "tmi_only",
        "needs_window": True,
    },
    "mars_robot": {
        "destination": "mars",
        "crew": 0,
        "payload_t": 0.8,
        "cost_busd": 0.55,
        "base_months": 18,
        "vehicle": "medium",
        "mass_model": "mars_cargo",
        "needs_window": True,
    },
    "mars_cargo": {
        "destination": "mars",
        "crew": 0,
        "payload_t": 8.0,
        "cost_busd": 2.2,
        "base_months": 22,
        "vehicle": "heavy",
        "mass_model": "mars_cargo",
        "needs_window": True,
        "requires_tech": ["heavy_edl"],
    },
    "mars_isru": {
        "destination": "mars",
        "crew": 0,
        "payload_t": 4.0,
        "cost_busd": 1.6,
        "base_months": 22,
        "vehicle": "heavy",
        "mass_model": "mars_cargo",
        "needs_window": True,
        "requires_tech": ["moxie_scale"],
    },
    "mars_crew_conjunction": {
        "destination": "mars",
        "crew": 6,
        "payload_t": 0.0,
        "cost_busd": 18.0,
        "base_months": 36,
        "vehicle": "heavy",
        "mass_model": "mars_campaign",
        "needs_window": True,
        "requires_tech": ["heavy_edl"],
    },
    "mars_outpost": {
        "destination": "mars",
        "crew": 6,
        "payload_t": 0.0,
        "cost_busd": 20.0,
        "base_months": 36,
        "vehicle": "heavy",
        "mass_model": "mars_campaign",
        "needs_window": True,
        "requires_tech": ["heavy_edl"],
        "stay": True,
    },
    "industrial_plant": {
        "destination": "moon",
        "crew": 0,
        "payload_t": 6.0,
        "cost_busd": 1.8,
        "base_months": 18,
        "vehicle": "heavy",
        "mass_model": "auto",
        "requires_tech": ["local_manufacturing"],
    },
    "replicator_seed": {
        "destination": "moon",
        "crew": 0,
        "payload_t": 0.9,
        "cost_busd": 1.6,
        "base_months": 18,
        "vehicle": "medium",
        "mass_model": "auto",
        "requires_tech": ["self_replicating_factory"],
    },
    "archive_cache": {
        "destination": "moon",
        "crew": 0,
        "payload_t": 1.2,
        "cost_busd": 0.4,
        "base_months": 10,
        "vehicle": "medium",
        "mass_model": "auto",
    },
}


def _flag(state: dict[str, Any], path: str) -> bool:
    node: Any = state
    for part in path.split("."):
        if not isinstance(node, dict) or part not in node:
            return False
        node = node[part]
    return bool(node)


def _imleo(profile: dict[str, Any], state: dict[str, Any], destination: str, payload_t: float, crew: int) -> dict[str, Any]:
    model = profile["mass_model"]
    if destination == "mars" and model == "auto":
        model = "mars_cargo"
    if destination == "moon" and model == "auto":
        model = "lunar_cargo"
    if model == "lunar_cargo":
        calc = lunar_cargo_imleo_t(max(payload_t, 0.2))
        return {"imleo_t": calc["imleo_t"], "detail": calc, "estimate": True}
    if model == "mars_cargo":
        calc = mars_cargo_imleo_t(max(payload_t, 0.2))
        return {"imleo_t": calc["imleo_t"], "detail": calc, "estimate": True}
    if model == "tmi_only":
        from rms.physics import mass_ratio

        ratio = mass_ratio(V("delta_v_m_s", "leo_to_tmi_min_energy"), V("propulsion", "hydrolox_vacuum_isp_s"))
        imleo = max(payload_t, 0.3) * ratio
        return {"imleo_t": imleo, "mass_ratio": ratio, "estimate": True, "source_id": "tsiolkovsky"}
    if model == "lunar_sortie":
        return {"imleo_t": V("campaign", "lunar_sortie_imleo_t"), "estimate": True, "source_id": "game_calibration"}
    if model == "lunar_sortie_stay":
        # Stay-behind habitat is extra one-way cargo plus the sortie stack.
        cargo = lunar_cargo_imleo_t(6.0)
        return {
            "imleo_t": V("campaign", "lunar_sortie_imleo_t") * (crew / 2.0) + cargo["imleo_t"],
            "estimate": True,
            "source_id": "game_calibration",
        }
    if model == "mars_campaign":
        days = (
            V("campaign", "reference_outbound_days")
            + V("campaign", "reference_surface_days")
            + V("campaign", "reference_return_days")
        )
        recovery = float(state["eclss"]["water_recovery_demonstrated"])
        o2_mode = "sabatier" if "sabatier" in state["tech"] else ("electrolysis" if recovery > 0 else "open")
        cons = consumables(crew, days, water_recovery=recovery, food_closure=0.0, o2_mode=o2_mode)
        ntr = "ntr_stage" in state["tech"]
        campaign = campaign_imleo_t(crew, ntr=ntr, consumables_t=cons["shipped_life_support_t"])
        campaign["consumables"] = cons
        return campaign
    raise KeyError(model)


def _dose(profile_id: str, state: dict[str, Any], crew: int) -> dict[str, Any] | None:
    if crew <= 0:
        return None
    shelter = "storm_shelter" in state["tech"]
    buried = "buried_habitat" in state["tech"]
    transit_extra = V("radiation", "storm_shelter_extra_g_cm2") if shelter else 0.0
    surface_extra = V("radiation", "buried_habitat_extra_g_cm2") if buried else 0.0
    if profile_id in {"mars_crew_conjunction", "mars_outpost"}:
        shielded = conjunction_dose_mSv(transit_extra, surface_extra)
        bare = conjunction_dose_mSv(0.0, 0.0)
        return {"applied": shielded, "unshielded_reference": bare, "transit_extra_g_cm2": transit_extra, "surface_extra_g_cm2": surface_extra}
    if profile_id in {"lunar_crew_sortie", "lunar_outpost"}:
        return {"applied": lunar_sortie_dose_mSv(transit_extra, surface_extra), "transit_extra_g_cm2": transit_extra, "surface_extra_g_cm2": surface_extra}
    return None


def plan_mission(state: dict[str, Any], spec: dict[str, Any]) -> dict[str, Any]:
    profile_id = spec.get("profile")
    if profile_id not in PROFILES:
        raise ValueError(f"unknown profile {profile_id}")
    profile = dict(PROFILES[profile_id])
    destination = spec.get("destination", profile["destination"])
    if destination not in {"moon", "mars", "mars_orbit", "freespace"}:
        raise ValueError("destination must be moon, mars, mars_orbit, or freespace")
    profile["destination"] = destination
    crew = int(spec.get("crew", profile["crew"]))
    payload_t = float(spec.get("payload_t", profile["payload_t"]))
    reasons: list[dict[str, Any]] = []
    impossible: list[dict[str, Any]] = []
    failure_p = 0.08
    gate = gates(state)

    for tech_id in profile.get("requires_tech", []):
        if tech_id not in state["tech"]:
            impossible.append({
                "id": "missing_tech",
                "tech": tech_id,
                "zh": f"缺少技术：{tech_id}。这不是勇气问题，是还没有这个能力。",
                "en": f"Missing tech: {tech_id}. This is not a question of nerve. The capability is not in hand.",
            })
    flag = profile.get("requires_flag")
    if flag and not _flag(state, flag):
        impossible.append({
            "id": "missing_flag",
            "flag": flag,
            "zh": "前置探测还没有给出必须的事实。",
            "en": "A required prior measurement is not in hand.",
        })

    resolved_model = profile["mass_model"]
    if resolved_model == "auto":
        resolved_model = "mars_cargo" if destination == "mars" else "lunar_cargo"
    if destination == "mars" and payload_t > V("bodies", "mars", "heritage_landed_mass_t") and "heavy_edl" not in state["tech"] and resolved_model == "mars_cargo":
        impossible.append({
            "id": "edl_mass",
            "zh": "继承下来的火星着陆能力大约是一吨。更重的东西在进入、减速、着陆上还没有被证明。",
            "en": "Heritage Mars landing is about one tonne. Heavier payloads are not demonstrated through entry, descent, and landing.",
            "source_id": "braun_manning_2007",
        })
    if profile_id in {"mars_crew_conjunction", "mars_outpost"} and "heavy_edl" not in state["tech"]:
        # already added via requires_tech, keep a specific sentence
        pass

    if crew > 0:
        available = ready_crew(state)
        if len(available) < crew:
            impossible.append({
                "id": "crew_pool",
                "have": len(available),
                "need": crew,
                "zh": "合格且未超过剂量规划上限的乘员不够。地球并不能随意派人。",
                "en": "Not enough qualified crew still under the dose planning cap. Earth cannot send people at will.",
            })
        if profile_id in {"lunar_crew_sortie", "lunar_outpost"} and not gate["analog_30"]:
            reasons.append({
                "id": "skip_analog",
                "zh": "封闭舱还没有连续运行满 30 天。生命保障和心理问题会在飞行中第一次出现。",
                "en": "No closed habitat has run 30 days. Life support and psychology would meet the crew for the first time in flight.",
            })
            failure_p += 0.45
        if profile_id in {"mars_crew_conjunction", "mars_outpost"}:
            if not gate["analog_365"]:
                reasons.append({
                    "id": "skip_year_analog",
                    "zh": "没有一年的封闭栖息地记录，也没有 93% 的水循环演示。DRA 式的会合任务要在外面待两年以上。",
                    "en": "No one-year closed habitat, and no 93% water loop. A conjunction mission keeps the crew away for more than two years.",
                })
                failure_p += 0.5
            elif float(state["eclss"]["water_recovery_demonstrated"]) < 0.98:
                reasons.append({
                    "id": "water_short_of_98",
                    "zh": "水循环还没有到 98%。任务也许回得来，但质量账会很难看。",
                    "en": "Water recovery is not yet 98%. The mission may still be flyable, but the mass budget is ugly.",
                    "estimate": False,
                    "source_id": "nasa_iss_water_2023",
                })
                failure_p += 0.1
            if "storm_shelter" not in state["tech"]:
                reasons.append({
                    "id": "no_shelter",
                    "zh": "转移飞行器上没有风暴掩体。银河宇宙线已经很重，太阳粒子事件会变成急性剂量。",
                    "en": "No storm shelter on the transfer vehicle. Galactic cosmic rays are already heavy; a solar particle event becomes an acute dose.",
                })
                failure_p += 0.15
            if not gate["mars_cargo"]:
                reasons.append({
                    "id": "no_preposition",
                    "zh": "货物还没有在火星上降落并熬过一个尘暴季。DRA 5.0 把货物提前一个窗口送出去。",
                    "en": "Cargo has not landed and lived through a dust-storm season. DRA 5.0 sends cargo one window ahead.",
                    "source_id": "nasa_dra5_2009",
                })
                failure_p += 0.25
            if not gate["mars_isru"] and profile_id == "mars_crew_conjunction":
                reasons.append({
                    "id": "return_propellant",
                    "zh": "返回用的氧还停留在 MOXIE 的克级演示，没有试点级的吨每年。可以从地球带氧化剂，但你现在的方案里没有这笔质量。",
                    "en": "Return oxygen is still at MOXIE's grams, not a pilot in tonnes per year. Oxidizer can be shipped from Earth, and this profile does not carry that mass.",
                })
                failure_p += 0.2
            if not gate["moon_crew_return"]:
                reasons.append({
                    "id": "skip_moon_crew",
                    "zh": "月球载人往返还没做过。物理上不禁止直飞火星，但尘埃、辐射和延迟操作都没有在有人的情况下演练过。",
                    "en": "No crewed lunar round trip yet. Physics does not forbid a direct Mars shot. Dust, radiation, and delayed operations have not been rehearsed with a crew.",
                })
                failure_p += 0.12
            if profile_id == "mars_outpost" and not gate["mars_crew_return"]:
                reasons.append({
                    "id": "stay_before_return",
                    "zh": "第一次载人就留下不回来。没有中止能力的居住不是前哨，是赌注。",
                    "en": "The first crew stays with no return. A habitation without an abort is a wager, not an outpost.",
                })
                failure_p += 0.25

    if destination == "mars" and profile_id == "greenhouse" and not gate["bio_simulant"]:
        reasons.append({
            "id": "biology_outdoors",
            "zh": "模拟星壤里还没有 90 天的生长记录。高氯酸盐不会因为你已经发射就消失。",
            "en": "No 90-day simulant grow-out. Perchlorates do not vanish because the launcher lit.",
            "source_id": "hecht2009",
        })
        failure_p += 0.35

    if profile_id == "mars_robot" and "precision_robotics" not in state["tech"]:
        failure_p += 0.18
        reasons.append({
            "id": "immature_robot",
            "zh": "精确着陆还在纸面上。机器人任务可以飞，失败率按早期着陆器计算。",
            "en": "Precision landing is still on paper. A robot can fly. The failure rate is an early-lander rate.",
        })

    mass = _imleo(profile, state, "mars" if destination == "mars_orbit" else destination, payload_t, crew)
    imleo = float(mass["imleo_t"])
    per_year = annual_imleo_t(state["launch"])
    if per_year <= 0:
        impossible.append({"id": "no_launch", "zh": "没有发射能力。", "en": "No launch capacity."})
        years_needed = 99
    else:
        years_needed = max(1, math.ceil(imleo / per_year - 1e-9))
    if years_needed > 12:
        impossible.append({
            "id": "cadence",
            "imleo_t": round(imleo, 2),
            "per_year_t": round(per_year, 2),
            "zh": "以现在的发射班次，十二年也堆不出这次任务的近地轨道质量。",
            "en": "At the current cadence, twelve years cannot assemble this mission's mass in low Earth orbit.",
        })

    year, month = state["clock"]["year"], state["clock"]["month"]
    prep = max(int(profile["base_months"]), years_needed * 12)
    depart_year, depart_month = add_months(year, month, prep)
    slipped = 0
    if profile.get("needs_window") and "high_energy_transfer" not in state["tech"]:
        depart_year, depart_month, slipped = slip_to_window(depart_year, depart_month)
        prep += slipped
    elif profile.get("needs_window") and not month_in_window(depart_year, depart_month):
        reasons.append({
            "id": "off_window",
            "zh": "不在窗口里。高能转移买得起时间，火箭方程会收质量税。",
            "en": "Off window. High-energy transfer buys the calendar. The rocket equation taxes the mass.",
        })
        failure_p += 0.08
        imleo *= 1.8
        mass["imleo_t"] = imleo
        mass["off_window_multiplier"] = 1.8

    reliability = state["launch"]["reliability_heavy" if profile["vehicle"] == "heavy" else "reliability_medium"]
    failure_p = 1.0 - (1.0 - failure_p) * reliability
    failure_p = min(0.95, failure_p)
    # Hostile quiet opposition nudges the failure of crewed flights.
    hostility = state["factions"]["closed_sky"]["hostility"]
    if crew > 0:
        failure_p = min(0.95, failure_p + 0.05 * (hostility / 100.0))

    dose = _dose(profile_id, state, crew)
    if dose and dose["applied"].get("exceeds_planning_cap"):
        reasons.append({
            "id": "dose_cap",
            "total_mSv": round(dose["applied"]["total_mSv"], 1),
            "cap_mSv": dose["applied"]["career_cap_mSv"],
            "zh": "按规划，这次任务的剂量当量会超过 600 毫希沃特的保守上限。这是估计用的筛子，不是 NASA 标准里的那个单一数字。不加屏蔽的会合任务，光是银河宇宙线就大约 1 希沃特。",
            "en": "As planned, dose equivalent on this mission exceeds the conservative 600 mSv screen. That screen is an estimate, not NASA's single number. An unshielded conjunction is about a sievert of galactic cosmic rays alone.",
            "estimate": True,
            "source_id": "zeitlin2013_cruise",
        })

    cost = float(profile["cost_busd"]) * float(state["launch"].get("price_factor", 1.0))
    if crew:
        cost += 0.15 * crew
    if state["treasury_busd"] < cost:
        impossible.append({
            "id": "money",
            "cost_busd": round(cost, 2),
            "treasury_busd": round(state["treasury_busd"], 2),
            "zh": "国库不够。先游说预算，或等年度拨款累积。",
            "en": "The treasury cannot cover this. Lobby for the budget, or let the annual appropriation accumulate.",
        })

    classification = "impossible" if impossible else ("reckless" if reasons else "ok")
    return {
        "profile": profile_id,
        "destination": destination,
        "crew": crew,
        "payload_t": payload_t,
        "class": classification,
        "failure_p": round(failure_p, 4),
        "impossible": impossible,
        "risks": reasons,
        "imleo_t": round(imleo, 3),
        "mass": {key: mass[key] for key in mass if key != "consumables"},
        "consumables": mass.get("consumables"),
        "cost_busd": round(cost, 3),
        "months": prep,
        "departure": f"{depart_year:04d}-{depart_month:02d}",
        "window_slip_months": slipped,
        "dose": dose,
        "needs_confirmation": classification == "reckless",
        "estimate_mass": True,
    }


def apply_success(state: dict[str, Any], plan: dict[str, Any]) -> list[str]:
    profile_id = plan["profile"]
    destination = plan["destination"]
    site_name = "mars" if destination == "mars_orbit" else destination
    site = state["sites"][site_name]
    notes = [f"success:{profile_id}"]
    if profile_id == "lunar_probe":
        site["robots"] += 1
        site["landings_success"] += 1
        site["ice_confirmed"] = True
        site["rtg"] = True
    elif profile_id == "lunar_isru_demo":
        site["isru_water_kg_year"] += 3000
        site["isru_o2_kg_year"] += 800
        site["robots"] += 1
    elif profile_id == "lunar_cargo":
        site["habitat"] = True
        site["polar"] = True
        site["solar_kwe_clear"] += 40
        site["battery_kwe"] += 10
        extra = V("radiation", "buried_habitat_extra_g_cm2") if "buried_habitat" in state["tech"] else 30
        site["shielding_g_cm2"] = max(float(site["shielding_g_cm2"]), extra)
        site["cargo_landings"] += 1
        _maybe_archive(state, site)
    elif profile_id == "lunar_crew_sortie":
        site["crew_returned"] += plan["crew"]
        site["crew_missions"] += 1
    elif profile_id == "lunar_outpost":
        _deliver_crew(state, site, plan["crew"])
        site["habitat"] = True
        site["polar"] = True
        _copy_eclss(state, site)
        site["stores"]["food_kg"] += plan["crew"] * 180 * 2.39
        site["stores"]["water_kg"] += plan["crew"] * 200
    elif profile_id == "greenhouse":
        site["greenhouse"] = True
        site["farms_m2"] += 800
    elif profile_id == "kilopower_unit":
        site["fission_kwe"] += 10
        site["heat_reject_kwe"] = float(site.get("heat_reject_kwe", 0.0)) + 10 * float(V("win", "foothold_machine_heat_per_kwe"))
    elif profile_id == "reactor_module":
        added = 500
        site["fission_kwe"] += added
        site["heat_reject_kwe"] = float(site.get("heat_reject_kwe", 0.0)) + added * float(V("win", "foothold_machine_heat_per_kwe"))
    elif profile_id == "replicator_seed":
        site["robots"] += int(V("win", "foothold_machine_robots"))
        site["isru_metal_t_year"] = max(float(site.get("isru_metal_t_year", 0.0)), float(V("win", "replicator_metal_t_year")))
        site["ore_reserve_t"] = max(float(site.get("ore_reserve_t", 0.0)), float(V("win", "replicator_ore_reserve_t")))
        site["heat_reject_kwe"] = max(float(site.get("heat_reject_kwe", 0.0)), float(V("win", "replicator_heat_reject_kwe")))
        site["repair_fraction"] = max(float(site.get("repair_fraction", 0.0)), float(V("win", "replicator_repair_fraction")))
        site["replication_fidelity"] = max(float(site.get("replication_fidelity", 0.0)), float(V("win", "replicator_fidelity")))
        notes.append("replicator_seed_no_procedure")
    elif profile_id == "mars_relay":
        site["relay"] = True
    elif profile_id == "mars_robot":
        site["robots"] += 1
        site["landings_success"] += 1
        site["rtg"] = True
    elif profile_id == "mars_cargo":
        site["habitat"] = True
        site["solar_kwe_clear"] += 30
        site["battery_kwe"] += 8
        extra = 80 if "buried_habitat" in state["tech"] else 15
        site["shielding_g_cm2"] = max(float(site["shielding_g_cm2"]), extra)
        site["cargo_landings"] += 1
        _maybe_archive(state, site)
    elif profile_id == "mars_isru":
        added = 40000 if "industrial_isru" in state["tech"] else 5000
        site["isru_o2_kg_year"] += added
        site["robots"] += 1
    elif profile_id == "mars_crew_conjunction":
        site["crew_returned"] += plan["crew"]
        site["crew_missions"] += 1
        site["habitat"] = True
    elif profile_id == "mars_outpost":
        _deliver_crew(state, site, plan["crew"])
        site["habitat"] = True
        _copy_eclss(state, site)
        site["stores"]["food_kg"] += plan["crew"] * 500 * 2.39
    elif profile_id == "industrial_plant":
        site["industrial_closure"] = max(float(site["industrial_closure"]), 0.85)
    elif profile_id == "archive_cache":
        _maybe_archive(state, site)
        if int(site["genome_archive_donors"]) <= 0:
            notes.append("archive_not_ready_on_earth")
    else:
        raise KeyError(profile_id)
    return notes


def _copy_eclss(state: dict[str, Any], site: dict[str, Any]) -> None:
    site["water_recovery"] = max(float(site["water_recovery"]), float(state["eclss"]["water_recovery_demonstrated"]))
    if "sabatier" in state["tech"]:
        site["electrolysis"] = True
        site["sabatier_fraction"] = max(float(site["sabatier_fraction"]), V("human", "o2_recovery_from_co2_current"))
    elif site["water_recovery"] > 0:
        site["electrolysis"] = True
    if "storm_shelter" in state["tech"]:
        site["spe_shelter"] = True


def _deliver_crew(state: dict[str, Any], site: dict[str, Any], crew: int) -> None:
    site["population"] += crew


def settle_flown_crew(state: dict[str, Any], crew_ids: list[str], dose_mSv: float, *, died: bool, stay: bool) -> list[dict[str, Any]]:
    cap = V("radiation", "career_planning_cap_mSv")
    report = []
    id_set = set(crew_ids)
    for person in state["crew"]["roster"]:
        if person["id"] not in id_set:
            continue
        person["dose_mSv"] = round(float(person["dose_mSv"]) + dose_mSv, 2)
        if died:
            person["status"] = "dead"
        elif stay:
            person["status"] = "resident"
        elif person["dose_mSv"] >= cap:
            person["status"] = "grounded"
        else:
            person["status"] = "available"
        report.append({"id": person["id"], "name": person["name"], "dose_mSv": person["dose_mSv"], "status": person["status"]})
    if died:
        state["crew"]["fatalities"] += len(crew_ids)
    return report


def _maybe_archive(state: dict[str, Any], site: dict[str, Any]) -> None:
    donors = int(state.get("genome_archive_donors", 0))
    if donors >= int(V("win", "genome_archive_donors")):
        site["genome_archive_donors"] = donors
        site["knowledge_archive"] = True


def assign_crew(state: dict[str, Any], crew: int) -> list[str]:
    chosen = ready_crew(state)[:crew]
    ids = [person["id"] for person in chosen]
    id_set = set(ids)
    for person in state["crew"]["roster"]:
        if person["id"] in id_set:
            person["status"] = "assigned"
    return ids
