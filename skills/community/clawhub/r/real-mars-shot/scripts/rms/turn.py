"""Apply one player action. Mutates the state dict. Does not narrate."""

from __future__ import annotations

from typing import Any

from rms.data import V, tech_tree
from rms.dice import roll_d100
from rms.epoch import apply_epoch
from rms.events import apply_event, choose_event
from rms.missions import PROFILES, apply_success, assign_crew, plan_mission, settle_flown_crew
from rms.physics import add_months, annual_imleo_t, people_export
from rms.settlement import apply_month
from rms.state import migrate, ready_crew
from rms.win import any_ember, consider_footholds, consider_seed, earth_alive_for_foothold, living_independent_seed

FACILITIES: dict[str, dict[str, Any]] = {
    "analog_habitat": {"cost": 0.35, "months": 6, "prereq_tech": []},
    "vacuum_lab": {"cost": 0.25, "months": 5, "prereq_tech": ["vacuum_thermal_lab"]},
    "biosphere_module": {"cost": 0.9, "months": 12, "prereq_tech": ["closed_water_93"]},
    "training_center": {"cost": 0.3, "months": 6, "prereq_tech": []},
    "pad": {"cost": 0.8, "months": 10, "prereq_tech": []},
    "superheavy_pad": {"cost": 1.6, "months": 16, "prereq_tech": ["reusable_super_heavy"]},
    "genome_archive": {"cost": 0.55, "months": 8, "prereq_tech": ["genome_bank"]},
    "plant_lab": {"cost": 0.4, "months": 8, "prereq_tech": ["crop_lab"]},
}

ALIASES = {
    "等待": "wait",
    "研究": "research",
    "发射": "mission",
    "任务": "mission",
    "建造": "facility",
    "模拟": "analog",
    "游说": "lobby",
    "外交": "diplomacy",
    "训练": "train",
    "生物": "biology",
    "治理": "govern",
    "断供": "independence",
    "计算": "compute",
    "状态": "status",
    "纪元": "epoch",
    "快进": "epoch",
}


def resolve(
    state: dict[str, Any],
    action: dict[str, Any],
    *,
    force_roll: int | None = None,
    force_event: str | None = None,
    force_earth_roll: int | None = None,
) -> dict[str, Any]:
    migrate(state)
    if state.get("outcome"):
        return _result(state, {"ok": False, "ended": True, "reason": state["outcome_reason"]}, mutated=False)
    kind = ALIASES.get(str(action.get("type", "")).strip(), str(action.get("type", "")).strip())
    action = dict(action)
    action["type"] = kind
    if kind in {"status", "compute", "schema"}:
        return _result(state, _info(state, action), mutated=False)
    if kind == "meta":
        _meta(state, action)
        state["clock"]["turn"] += 1
        return _result(state, {"ok": True, "action": "meta"}, mutated=True)

    handler = {
        "wait": _wait,
        "research": _research,
        "facility": _facility,
        "analog": _analog,
        "lobby": _lobby,
        "diplomacy": _diplomacy,
        "govern": _govern,
        "train": _train,
        "biology": _biology,
        "independence": _independence,
        "mission": _mission,
        "epoch": _epoch,
    }.get(kind)
    if handler is None:
        return _result(state, {"ok": False, "error": f"unknown action {kind}"}, mutated=False)

    if kind == "epoch":
        payload = _epoch(state, action, force_roll=force_roll, force_earth_roll=force_earth_roll)
    else:
        payload = handler(state, action, force_roll=force_roll)
    if not payload.get("mutated"):
        return _result(state, payload, mutated=False)

    event_roll = force_roll if force_roll is not None else roll_d100(state["rng_seed"], state["clock"]["turn"], "event")
    event_id = choose_event(state, force=force_event, seed=state["rng_seed"], turn=state["clock"]["turn"])
    event = apply_event(state, event_id, event_roll)
    state["last_event"] = event
    _check_outcome(state, payload.get("outcome_hint"))
    state["clock"]["turn"] += 1
    payload["event"] = event
    payload["ok"] = True
    return _result(state, payload, mutated=True)


def _info(state: dict[str, Any], action: dict[str, Any]) -> dict[str, Any]:
    if action["type"] == "compute" and action.get("topic") == "mission":
        plan = plan_mission(state, action)
        return {"ok": True, "compute": True, "plan": plan}
    from rms.present import compute_answer

    return {"ok": True, "compute": True, "answer": compute_answer(state, action)}


def _meta(state: dict[str, Any], action: dict[str, Any]) -> None:
    if action.get("language") in {"zh", "en"}:
        state["language"] = action["language"]
    if "tts" in action:
        state["tts"]["enabled"] = bool(action["tts"])
    if action.get("director"):
        state["director"] = str(action["director"])[:80]
    if action.get("program"):
        state["program"] = str(action["program"])[:80]


def _advance(state: dict[str, Any], months: int, resupply_site: str | None = None) -> None:
    for index in range(months):
        state["treasury_busd"] += state["annual_budget_busd"] / 12.0
        year, month = add_months(state["clock"]["year"], state["clock"]["month"], 1)
        state["clock"]["year"] = year
        state["clock"]["month"] = month
        state["clock"]["abs_month"] += 1
        if state["crew"]["started_year"] != year:
            state["crew"]["started_year"] = year
            state["crew"]["started_this_year"] = 0
        still = []
        for cadet in state["crew"]["in_training"]:
            cadet["months_left"] -= 1
            if cadet["months_left"] <= 0:
                number = len(state["crew"]["roster"]) + 1
                state["crew"]["roster"].append({
                    "id": f"crew-{number:02d}",
                    "name": cadet.get("name") or f"crew-{number:02d}",
                    "dose_mSv": 0.0,
                    "status": "available",
                })
            else:
                still.append(cadet)
        state["crew"]["in_training"] = still
        resupply = resupply_site if index == months - 1 else None
        for site_name in ("moon", "mars", "freespace"):
            apply_month(state, site_name, resupply=resupply == site_name)
        if state["clock"]["month"] == 1:
            _births(state)
        if state["treasury_busd"] < 0:
            state["deficit_months"] += 1
            state["political_capital"] = max(0, state["political_capital"] - 2)
        else:
            state["deficit_months"] = 0


def _births(state: dict[str, Any]) -> None:
    if "offworld_obstetrics" not in state["tech"]:
        return
    roll = roll_d100(state["rng_seed"], state["clock"]["year"], "birth")
    for site_name in ("moon", "mars", "freespace"):
        site = state["sites"][site_name]
        if int(site["population"]) < 8:
            continue
        from rms.physics import annual_habitat_dose_mSv
        from rms.settlement import evaluate_month

        month = evaluate_month(site_name, site)
        dose = annual_habitat_dose_mSv(site_name, float(site.get("shielding_g_cm2", 0.0)))
        if float(month.get("food_ratio", 0)) < 0.5 or not dose["meets_target"]:
            continue
        if state["crew"]["psych"] < 45:
            continue
        if roll >= 40:
            site["births"] += 1
            site["population"] += 1


def _pay(state: dict[str, Any], cost: float) -> bool:
    if state["treasury_busd"] + 1e-9 < cost:
        return False
    state["treasury_busd"] -= cost
    return True


def _epoch(
    state: dict[str, Any],
    action: dict[str, Any],
    *,
    force_roll: int | None,
    force_earth_roll: int | None = None,
) -> dict[str, Any]:
    return apply_epoch(state, action, force_roll=force_roll, force_earth_roll=force_earth_roll)


def _wait(state: dict[str, Any], action: dict[str, Any], *, force_roll: int | None) -> dict[str, Any]:
    months = int(action.get("months", 3))
    if months < 1 or months > 60:
        return {"ok": False, "error": "months must be 1..60", "mutated": False}
    _advance(state, months)
    return {"mutated": True, "action": "wait", "months": months}


def _research(state: dict[str, Any], action: dict[str, Any], *, force_roll: int | None) -> dict[str, Any]:
    tech_id = action.get("tech_id")
    tree = tech_tree()
    if tech_id not in tree:
        return {"ok": False, "error": "unknown tech", "mutated": False}
    if tech_id in state["tech"]:
        return {"ok": False, "error": "already unlocked", "mutated": False, "tech_id": tech_id}
    missing = [item for item in tree[tech_id]["prereq"] if item not in state["tech"]]
    if missing:
        return {"ok": False, "error": "missing prereq", "missing": missing, "mutated": False, "class": "impossible"}
    cost = float(tree[tech_id]["cost_busd"])
    months = int(tree[tech_id]["months"])
    if not _pay(state, cost):
        return {"ok": False, "error": "money", "cost_busd": cost, "mutated": False, "class": "impossible"}
    _advance(state, months)
    roll = force_roll if force_roll is not None else roll_d100(state["rng_seed"], state["clock"]["turn"], "research")
    if roll <= 8:
        state["knowledge"] += 1
        return {"mutated": True, "action": "research", "tech_id": tech_id, "unlocked": False, "setback": True, "roll": roll, "months": months}
    state["tech"].append(tech_id)
    _apply_tech(state, tech_id)
    state["knowledge"] += 2
    return {"mutated": True, "action": "research", "tech_id": tech_id, "unlocked": True, "roll": roll, "months": months, "card": tree[tech_id]}


def _apply_tech(state: dict[str, Any], tech_id: str) -> None:
    eclss = state["eclss"]
    if tech_id == "closed_water_93":
        eclss["water_recovery_demonstrated"] = max(float(eclss["water_recovery_demonstrated"]), 0.93)
    elif tech_id == "closed_water_98":
        eclss["water_recovery_demonstrated"] = max(float(eclss["water_recovery_demonstrated"]), 0.98)
    elif tech_id == "sabatier":
        eclss["o2_recovery_from_co2"] = max(float(eclss["o2_recovery_from_co2"]), V("human", "o2_recovery_from_co2_current"))
    elif tech_id == "crop_lab":
        eclss["food_closure_demonstrated"] = max(float(eclss["food_closure_demonstrated"]), 0.15)


def _facility(state: dict[str, Any], action: dict[str, Any], *, force_roll: int | None) -> dict[str, Any]:
    facility = action.get("facility")
    if facility not in FACILITIES:
        return {"ok": False, "error": "unknown facility", "mutated": False}
    if facility in state["facilities"]:
        return {"ok": False, "error": "already built", "mutated": False}
    spec = FACILITIES[facility]
    missing = [item for item in spec["prereq_tech"] if item not in state["tech"]]
    if missing:
        return {"ok": False, "error": "missing prereq", "missing": missing, "mutated": False, "class": "impossible"}
    if not _pay(state, spec["cost"]):
        return {"ok": False, "error": "money", "cost_busd": spec["cost"], "mutated": False, "class": "impossible"}
    _advance(state, spec["months"])
    state["facilities"][facility] = {"year": state["clock"]["year"], "month": state["clock"]["month"]}
    _apply_facility(state, facility)
    return {"mutated": True, "action": "facility", "facility": facility, "months": spec["months"]}


def _apply_facility(state: dict[str, Any], facility: str) -> None:
    if facility == "training_center":
        state["crew"]["pipeline_per_year"] += 4
    elif facility == "pad":
        state["launch"]["heavy_per_year"] += 1
    elif facility == "superheavy_pad":
        state["launch"]["heavy_per_year"] += 2
        state["launch"]["heavy_leo_t"] = max(float(state["launch"]["heavy_leo_t"]), 100.0)
        state["launch"]["reliability_heavy"] = min(float(state["launch"]["reliability_heavy"]), 0.9)
    elif facility == "genome_archive":
        state["genome_archive_donors"] = int(V("win", "genome_archive_donors"))


def _analog(state: dict[str, Any], action: dict[str, Any], *, force_roll: int | None) -> dict[str, Any]:
    if "analog_habitat" not in state["facilities"]:
        return {"ok": False, "error": "no analog habitat", "mutated": False, "class": "impossible"}
    days = int(action.get("days", 30))
    if days < 7 or days > 800:
        return {"ok": False, "error": "days must be 7..800", "mutated": False}
    record = int(state["eclss"]["closed_habitat_days_record"])
    reckless = days > max(30, record + 90)
    if reckless and not action.get("confirm_reckless"):
        return {
            "ok": False,
            "needs_confirmation": True,
            "class": "reckless",
            "mutated": False,
            "zh": "你要把封闭时间一下拉得比记录长很多。生物圈二号的氧气不是在第 7 天掉下去的。",
            "en": "You want a sealed run far longer than the record. Biosphere 2 did not lose its oxygen on day 7.",
        }
    cost = 0.05 + 0.0015 * days
    if not _pay(state, cost):
        return {"ok": False, "error": "money", "mutated": False, "class": "impossible"}
    months = max(1, round(days / 30))
    _advance(state, months)
    roll = force_roll if force_roll is not None else roll_d100(state["rng_seed"], state["clock"]["turn"], "analog")
    failure_p = 0.15
    if "analog_operations" not in state["tech"]:
        failure_p += 0.15
    if days > 180 and "closed_water_93" not in state["tech"]:
        failure_p += 0.35
    if reckless:
        failure_p += 0.2
    failure_p = min(0.9, failure_p)
    success = (roll / 100.0) > failure_p
    facts: dict[str, Any] = {"mutated": True, "action": "analog", "days": days, "roll": roll, "failure_p": round(failure_p, 3), "success": success}
    if success:
        eclss = state["eclss"]
        eclss["closed_habitat_days_record"] = max(record, days)
        eclss["water_recovery_duration_days"] = int(eclss["water_recovery_duration_days"]) + days
        if "closed_water_98" in state["tech"] and days >= 180:
            eclss["water_recovery_demonstrated"] = max(float(eclss["water_recovery_demonstrated"]), 0.98)
        elif "closed_water_93" in state["tech"]:
            eclss["water_recovery_demonstrated"] = max(float(eclss["water_recovery_demonstrated"]), 0.93)
        if "crop_lab" in state["tech"] and days >= 90:
            eclss["food_closure_demonstrated"] = max(float(eclss["food_closure_demonstrated"]), 0.3)
        state["crew"]["psych"] = max(0, state["crew"]["psych"] - (4 if days > 180 else 1))
        state["knowledge"] += 1
        state["public_opinion"] = min(100, state["public_opinion"] + 2)
    else:
        state["eclss"]["biosphere_lesson"] = True
        state["knowledge"] += 2
        state["public_opinion"] = max(0, state["public_opinion"] - 5)
        state["safety_culture"] = min(100, state["safety_culture"] + 3)
        facts["evacuated"] = True
        facts["lesson"] = "biosphere"
    return facts


def _lobby(state: dict[str, Any], action: dict[str, Any], *, force_roll: int | None) -> dict[str, Any]:
    if not _pay(state, 0.15):
        return {"ok": False, "error": "money", "mutated": False, "class": "impossible"}
    _advance(state, 6)
    roll = force_roll if force_roll is not None else roll_d100(state["rng_seed"], state["clock"]["turn"], "lobby")
    ok = state["political_capital"] > 30 and roll > 35
    if ok:
        state["annual_budget_busd"] = round(state["annual_budget_busd"] + 0.8, 3)
        state["political_capital"] = max(0, state["political_capital"] - 4)
    else:
        state["political_capital"] = max(0, state["political_capital"] - 8)
        state["public_opinion"] = max(0, state["public_opinion"] - 3)
    return {"mutated": True, "action": "lobby", "won": ok, "roll": roll, "months": 6}


def _diplomacy(state: dict[str, Any], action: dict[str, Any], *, force_roll: int | None) -> dict[str, Any]:
    faction = action.get("faction")
    if faction not in state["factions"]:
        return {"ok": False, "error": "unknown faction", "mutated": False}
    if not _pay(state, 0.1):
        return {"ok": False, "error": "money", "mutated": False, "class": "impossible"}
    _advance(state, 3)
    row = state["factions"][faction]
    row["support"] = min(100, row["support"] + 8)
    row["hostility"] = max(0, row["hostility"] - 5)
    granted = False
    if faction == "meridian" and row["support"] >= 60 and not state["second_source"]:
        state["second_source"] = True
        state["launch"]["heavy_per_year"] += 1
        granted = True
    return {"mutated": True, "action": "diplomacy", "faction": faction, "second_source": granted, "months": 3}


def _govern(state: dict[str, Any], action: dict[str, Any], *, force_roll: int | None) -> dict[str, Any]:
    style = action.get("style", "open")
    if style not in {"open", "suppress"}:
        return {"ok": False, "error": "style must be open or suppress", "mutated": False}
    _advance(state, 3 if style == "open" else 2)
    if style == "open":
        state["dissent"] = max(0, state["dissent"] - 8)
        state["political_capital"] = max(0, state["political_capital"] - 2)
        state["safety_culture"] = min(100, state["safety_culture"] + 2)
        state["suppressed"] = False
    else:
        state["dissent"] = min(100, state["dissent"] + 5)
        state["safety_culture"] = max(0, state["safety_culture"] - 8)
        state["suppressed"] = True
    return {"mutated": True, "action": "govern", "style": style}


def _train(state: dict[str, Any], action: dict[str, Any], *, force_roll: int | None) -> dict[str, Any]:
    cohort = int(action.get("cohort", 4))
    if cohort < 1 or cohort > 20:
        return {"ok": False, "error": "cohort must be 1..20", "mutated": False}
    room = state["crew"]["pipeline_per_year"] - state["crew"]["started_this_year"]
    if cohort > room:
        return {"ok": False, "error": "pipeline full", "room": room, "mutated": False, "class": "impossible"}
    cost = 0.04 * cohort
    if not _pay(state, cost):
        return {"ok": False, "error": "money", "mutated": False, "class": "impossible"}
    state["crew"]["started_this_year"] += cohort
    for index in range(cohort):
        state["crew"]["in_training"].append({"months_left": 48, "name": f"cadet-{state['clock']['year']}-{index + 1}"})
    _advance(state, 1)
    return {"mutated": True, "action": "train", "cohort": cohort, "graduates_in_months": 48}


def _biology(state: dict[str, Any], action: dict[str, Any], *, force_roll: int | None) -> dict[str, Any]:
    organism = action.get("organism", "cyanobacteria")
    site = action.get("site", "earth_lab")
    from rms.data import organisms

    if organism not in organisms():
        return {"ok": False, "error": "unknown organism", "mutated": False}
    if site == "earth_open":
        if not action.get("confirm_reckless"):
            return {
                "ok": False,
                "needs_confirmation": True,
                "class": "reckless",
                "mutated": False,
                "zh": "在地球上无约束释放试验生物会终结计划。没有第二种结局。",
                "en": "An uncontained release on Earth ends the program. There is not a second outcome.",
            }
        state["biology"]["uncontained"] = True
        state["outcome_hint_local"] = "biosafety"
        _advance(state, 1)
        return {"mutated": True, "action": "biology", "site": site, "outcome_hint": "biosafety"}
    if site == "earth_simulant" and "simulant_biology" not in state["tech"]:
        return {"ok": False, "error": "missing tech", "missing": ["simulant_biology"], "mutated": False, "class": "impossible"}
    if site in {"moon", "mars", "freespace"} and not state["sites"][site]["greenhouse"] and not (
        state["sites"][site]["habitat"] and float(state["sites"][site]["shielding_g_cm2"]) + 1e-9 >= V("win", "foothold_bio_shield_g_cm2")
    ):
        return {
            "ok": False,
            "error": "no sheltered niche",
            "mutated": False,
            "class": "impossible",
            "zh": "开放的月面或火星地表留不住液态水和可生长的地球生物。先要温室，或有覆土的栖息地。",
            "en": "Open regolith does not hold liquid water or a growing Earth organism. A greenhouse, or a buried habitat, has to come first.",
        }
    if not _pay(state, 0.08):
        return {"ok": False, "error": "money", "mutated": False, "class": "impossible"}
    months = 3 if organism == "tardigrade" else 6
    _advance(state, months)
    card = organisms()[organism]
    if organism == "tardigrade":
        state["biology"]["tardigrade_exposure"] = True
        protection = _planetary_protection(state, site)
        return {
            "mutated": True,
            "action": "biology",
            "organism": organism,
            "established": False,
            "survival_is_not_habitation": True,
            "planetary_protection": protection,
            "zh": "缓步动物在暴露试验里活了下来。这不计入建立，也不产生氧气或粮食。",
            "en": "The tardigrades survived the exposure test. That does not count as establishment, and it makes neither oxygen nor food.",
        }
    if site == "earth_simulant":
        state["biology"]["simulant_days"] += 90
    levels = state["biology"]["levels"]
    levels[organism] = min(5, int(levels.get(organism, 0)) + 1)
    protection = None
    if site in state["sites"] and not card.get("survival_only"):
        slot = state["sites"][site].setdefault("organisms", {})
        slot[organism] = min(5, int(slot.get(organism, 0)) + 1)
        state["sites"][site]["life_archive_accessions"] = int(state["sites"][site].get("life_archive_accessions", 0)) + int(V("win", "foothold_culture_accessions"))
        if organism == "food_crop":
            state["sites"][site]["farms_m2"] += 200
        protection = _planetary_protection(state, site)
    return {
        "mutated": True,
        "action": "biology",
        "organism": organism,
        "site": site,
        "established": bool(card.get("establishes_ecosystem")) and site in {"moon", "mars"} and levels[organism] >= 3,
        "survival_is_not_habitation": bool(card.get("survival_only", False)),
        "planetary_protection": protection,
        "note_zh": card["note_zh"],
        "note_en": card["note_en"],
    }


def _planetary_protection(state: dict[str, Any], site: str) -> dict[str, Any] | None:
    """Sealed Earth life on another world still costs a review. No release procedure."""
    if site not in {"moon", "mars", "freespace"}:
        return None
    cost = float(V("win", "foothold_pp_political_cost"))
    state["political_capital"] = max(0, state["political_capital"] - cost)
    concord = state["factions"].setdefault("concord", {"support": 0, "hostility": 0})
    concord["support"] = max(0, concord.get("support", 0) - cost)
    hearth = state["factions"].setdefault("hearthbound", {"support": 0, "hostility": 0})
    hearth["hostility"] = min(100, hearth.get("hostility", 0) + 2)
    return {
        "estimate": True,
        "source_id": "cospar_planetary_protection",
        "political_cost": cost,
        "zh": "封闭舱里的地球生物仍然是前向污染。协和要一份行星保护审查，政治资本下降。这不是向开放地表撒播。",
        "en": "Earth life in a sealed niche is still forward contamination. Concord wants a planetary-protection review, and political capital drops. This is not a release onto open ground.",
    }


def _independence(state: dict[str, Any], action: dict[str, Any], *, force_roll: int | None) -> dict[str, Any]:
    site_name = action.get("site", "moon")
    if site_name not in state["sites"]:
        return {"ok": False, "error": "unknown site", "mutated": False}
    from rms.settlement import evaluate_month

    report = evaluate_month(site_name, state["sites"][site_name])
    if int(state["sites"][site_name]["population"]) <= 0:
        return {"ok": False, "error": "nobody lives there", "mutated": False, "class": "impossible", "month": report}
    if not report["win_month"] and not action.get("confirm_reckless"):
        return {
            "ok": False,
            "needs_confirmation": True,
            "class": "reckless",
            "mutated": False,
            "month": {key: report[key] for key in report if key != "flows"},
            "zh": "这个月并不是本地盈余。现在开始断供，时钟不会走，人会先挨饿或断电。",
            "en": "This month is not a local surplus. Starting the trial now will not advance the clock. People will meet the shortfall first.",
        }
    state["sites"][site_name]["trial"] = True
    _advance(state, 1)
    return {"mutated": True, "action": "independence", "site": site_name}


def _mission(state: dict[str, Any], action: dict[str, Any], *, force_roll: int | None) -> dict[str, Any]:
    try:
        plan = plan_mission(state, action)
    except ValueError as exc:
        return {"ok": False, "error": str(exc), "mutated": False}
    if plan["class"] == "impossible":
        return {"ok": False, "class": "impossible", "plan": plan, "mutated": False}
    if plan["class"] == "reckless" and not action.get("confirm_reckless"):
        return {
            "ok": False,
            "needs_confirmation": True,
            "class": "reckless",
            "plan": plan,
            "mutated": False,
            "zh": "顾问反对这次发射。如果你仍然要飞，请明确确认。",
            "en": "The advisors oppose this launch. If you still want to fly, say so explicitly.",
        }
    if not _pay(state, plan["cost_busd"]):
        return {"ok": False, "error": "money", "plan": plan, "mutated": False, "class": "impossible"}
    crew_ids: list[str] = []
    if plan["crew"]:
        crew_ids = assign_crew(state, plan["crew"])
    if plan["imleo_t"] > 0.5 * annual_imleo_t(state["launch"]):
        state["launch"]["busy_until_abs"] = state["clock"]["abs_month"] + plan["months"]
    resupply = None
    if plan["destination"] in {"moon", "mars"} and plan["crew"] == 0:
        resupply = plan["destination"]
    _advance(state, plan["months"], resupply_site=resupply if False else None)
    roll = force_roll if force_roll is not None else roll_d100(state["rng_seed"], state["clock"]["turn"], "mission")
    success = (roll / 100.0) > plan["failure_p"]
    spe = None
    died = False
    if plan["crew"] and plan["destination"] in {"moon", "mars"}:
        spe_roll = force_roll if force_roll is not None else roll_d100(state["rng_seed"], state["clock"]["turn"], "spe")
        threshold = int(V("radiation", "game_spe_probability_mars_mission" if plan["destination"] == "mars" else "game_spe_probability_lunar_sortie") * 100)
        if spe_roll <= threshold:
            sheltered = "storm_shelter" in state["tech"]
            acute = 25.0 if sheltered else (1600.0 if spe_roll <= max(1, threshold // 5) else 450.0)
            spe = {"acute_mSv": acute, "sheltered": sheltered, "probability_is_dramatic_compression": True}
            if acute >= V("radiation", "acute_severe_mSv"):
                success = False
                died = True
    facts: dict[str, Any] = {
        "mutated": True,
        "action": "mission",
        "plan": plan,
        "roll": roll,
        "success": success and not died,
        "spe": spe,
    }
    dose_value = 0.0
    if plan.get("dose"):
        dose_value = float(plan["dose"]["applied"].get("total_mSv", plan["dose"]["applied"].get("total_mSv", 0.0)))
        if isinstance(plan["dose"]["applied"], dict) and "total_mSv" in plan["dose"]["applied"]:
            dose_value = float(plan["dose"]["applied"]["total_mSv"])
    if spe:
        dose_value += spe["acute_mSv"]
    if success and not died:
        facts["notes"] = apply_success(state, plan)
        if crew_ids:
            stay = bool(PROFILES[plan["profile"]].get("stay"))
            facts["crew"] = settle_flown_crew(state, crew_ids, dose_value, died=False, stay=stay)
        state["public_opinion"] = min(100, state["public_opinion"] + (4 if plan["crew"] else 2))
        state["knowledge"] += 1
        if plan["destination"] in state["sites"] and state["sites"][plan["destination"]].get("trial"):
            state["sites"][plan["destination"]]["independent_months"] = 0
            facts["trial_reset"] = True
        if plan["destination"] in state["sites"]:
            landed = state["sites"][plan["destination"]]
            clocks = (
                int(landed.get("biology_closed_months", 0) or 0),
                int(landed.get("machine_tended_months", 0) or 0),
                int(landed.get("machine_replicator_months", 0) or 0),
                float(landed.get("biology_years", 0) or 0),
                float(landed.get("machine_years", 0) or 0),
                float(landed.get("tended_years", 0) or 0),
            )
            if any(clocks) or any((landed.get("epoch_paths") or {}).values()):
                facts["closure_reset"] = True
            landed["biology_closed_months"] = 0
            landed["machine_tended_months"] = 0
            landed["machine_replicator_months"] = 0
            landed["biology_years"] = 0.0
            landed["machine_years"] = 0.0
            landed["tended_years"] = 0.0
            landed["epoch_paths"] = {}
    else:
        site_name = plan["destination"] if plan["destination"] in state["sites"] else None
        if site_name:
            state["sites"][site_name]["landings_fail"] += 1
        if crew_ids:
            if not died:
                death_roll = force_roll if force_roll is not None else roll_d100(state["rng_seed"], state["clock"]["turn"], "death")
                death_p = 0.7 if plan["destination"] == "mars" else 0.35
                if "launch_abort" in state["tech"] and plan["destination"] == "moon":
                    death_p = 0.18
                died = (death_roll / 100.0) <= death_p
                facts["death_roll"] = death_roll
            facts["crew_died"] = died
            facts["crew"] = settle_flown_crew(state, crew_ids, dose_value * (1.0 if died else 0.5), died=died, stay=False)
            state["public_opinion"] = max(0, state["public_opinion"] - (25 if died else 8))
            state["political_capital"] = max(0, state["political_capital"] - (15 if died else 6))
            state["earth_stability"] = max(0, state["earth_stability"] - (6 if died else 2))
            if died and _all_in(state):
                facts["outcome_hint"] = "all_in"
        else:
            state["public_opinion"] = max(0, state["public_opinion"] - 4)
            state["knowledge"] += 1
        facts["success"] = False
    return facts


def _all_in(state: dict[str, Any]) -> bool:
    offworld_robots = state["sites"]["moon"]["robots"] + state["sites"]["mars"]["robots"]
    return (
        state["treasury_busd"] < 0.3
        and state["political_capital"] <= 10
        and len(ready_crew(state)) < 4
        and offworld_robots == 0
        and state.get("outcome") != "win"
    )


def _check_outcome(state: dict[str, Any], hint: str | None) -> None:
    if state.get("outcome"):
        return
    ember = any_ember(state)
    if ember:
        consider_footholds(state)
        state["outcome"] = "win"
        state["outcome_reason"] = f"ember:{ember['site']}"
        state["outcome_site"] = ember["site"]
        return
    if hint == "biosafety" or state["biology"].get("uncontained"):
        state["outcome"] = "game_over"
        state["outcome_reason"] = "biosafety"
        return
    independent = living_independent_seed(state)
    program_collapsed = state["deficit_months"] >= 12 and state["political_capital"] <= 0 and state["public_opinion"] <= 15
    earth_failed = state["earth_stability"] <= 0 or program_collapsed or hint == "all_in"
    if independent and earth_failed:
        state["earth_program_ended"] = True
    elif state["earth_stability"] <= 0:
        state["outcome"] = "game_over"
        state["outcome_reason"] = "earth_collapse"
        return
    elif program_collapsed:
        state["outcome"] = "game_over"
        state["outcome_reason"] = "program_collapse"
        return
    elif hint == "all_in":
        state["outcome"] = "game_over"
        state["outcome_reason"] = "all_in_disaster"
        return
    for site_name, site in state["sites"].items():
        if site.get("extinct") and state["earth_stability"] < 25:
            state["outcome"] = "game_over"
            state["outcome_reason"] = f"offworld_extinction:{site_name}"
            return
    if earth_alive_for_foothold(state):
        consider_footholds(state)
    seed = consider_seed(state)
    if seed:
        state["outcome"] = "win"
        state["outcome_reason"] = f"seed_of_life:{seed['path']}:{seed['site']}"
        state["outcome_site"] = seed["site"]


def _result(state: dict[str, Any], payload: dict[str, Any], *, mutated: bool) -> dict[str, Any]:
    from rms.present import decorate

    payload = dict(payload)
    payload["mutated"] = mutated
    return decorate(state, payload)
