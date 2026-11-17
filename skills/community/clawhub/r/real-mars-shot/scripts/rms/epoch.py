"""Fast-forward a self-sustaining path. One action, one risk roll, one Earth roll.

Monthly turns are not a way to reach ten thousand years. An epoch is.
Dice stay deterministic: sha256(seed:turn:salt).
"""

from __future__ import annotations

from typing import Any

from rms.data import V
from rms.dice import roll_d100
from rms.physics import add_months
from rms.settlement import biology_month, foothold_month, machine_replicator, tended_life

SCALES = {
    "decade": "epoch_decade_years",
    "century": "epoch_century_years",
    "millennium": "epoch_millennium_years",
}

EARTH_P = {
    "decade": "epoch_earth_end_decade",
    "century": "epoch_earth_end_century",
    "millennium": "epoch_earth_end_millennium",
}

HAZARDS = {
    "human": ("asteroid_impact", "solar_particle_event", "equipment_entropy", "ecosystem_collapse"),
    "biology": ("asteroid_impact", "solar_particle_event", "mutation_load", "ecosystem_collapse"),
    "machine": ("equipment_entropy", "replication_drift", "solar_particle_event", "thermal_rejection_fault"),
}

_TEXT = {
    "bad_site": {
        "zh": "纪元只能发生在月球、火星或自由空间。",
        "en": "An epoch can run on the Moon, Mars, or in free space.",
    },
    "bad_path": {
        "zh": "路径只能是人、生物或机器。",
        "en": "The path has to be human, biology, or machine.",
    },
    "bad_scale": {
        "zh": "尺度只能是十年、百年或千年。",
        "en": "The scale has to be a decade, a century, or a millennium.",
    },
    "scale_too_long": {
        "zh": "人的纪元只走到百年。千年是生命和机器的尺度。",
        "en": "A human epoch stops at a century. A millennium is for life and for machines.",
    },
    "not_self_sustaining": {
        "zh": "这套系统眼下还不能自己维持，不能快进。",
        "en": "This system is not self-sustaining right now, so it cannot fast-forward.",
    },
    "not_multigenerational": {
        "zh": "百年这一档要已经有地外出生，并且当地人够组成一户。两个人熬时间不算下一代。",
        "en": "The century tier needs an off-world birth and enough people for a household. Two people aging in place are not a next generation.",
    },
    "stay_too_short": {
        "zh": "先把五百天的停留站住，才能把人的时间快进到百年。",
        "en": "The 500-day stay has to be in hand before a human epoch can run toward a century.",
    },
    "not_demonstrated": {
        "zh": "先用普通月份证明它能连续运转一年，再快进。生物圈二号在大约两年里就失控了。十二个月是估计，比那次失败短。",
        "en": "Show a year of ordinary months before fast-forwarding. Biosphere 2 lost control in about two years. Twelve months is an estimate, and shorter than that failure.",
    },
    "deep_locked": {
        "zh": "千年纪元要等这一档的短目标已经成立：生物十年，或机器五十年。",
        "en": "A millennium waits until the shorter tier is real: ten years of life, or fifty years of machines.",
    },
}


def _fail(reasons: list[str]) -> dict[str, Any]:
    text = _TEXT.get(reasons[0], _TEXT["not_self_sustaining"]) if reasons else _TEXT["not_self_sustaining"]
    return {"ok": False, "error": "epoch refused", "reasons": reasons, "zh": text["zh"], "en": text["en"], "mutated": False}


def _demonstrated(site: dict[str, Any], field: str) -> bool:
    return int(site.get(field, 0)) >= int(V("win", "epoch_demo_months"))


def eligible(state: dict[str, Any], site_name: str, path: str, scale: str) -> dict[str, Any]:
    if site_name not in state["sites"]:
        return _fail(["bad_site"])
    if path not in {"human", "biology", "machine"}:
        return _fail(["bad_path"])
    if scale not in SCALES:
        return _fail(["bad_scale"])
    site = state["sites"][site_name]
    paths = site.get("epoch_paths") or {}
    if path == "human":
        if scale == "millennium":
            return _fail(["scale_too_long"])
        month = foothold_month(site_name, site)
        if not month["ok"]:
            return _fail(["not_self_sustaining"] + list(month.get("reasons") or []))
        if int(site.get("inhabited_days", 0)) < int(V("win", "foothold_days")):
            return _fail(["stay_too_short"])
        if int(site.get("population", 0)) < int(V("win", "foothold_century_min_population")) or int(site.get("births", 0)) < int(V("win", "foothold_century_min_births")):
            return _fail(["not_multigenerational"])
        return {"ok": True}
    if path == "biology":
        life = biology_month(site_name, site)
        if not life["ok"]:
            return _fail(["not_self_sustaining"] + life["reasons"])
        started = bool(paths.get("biology")) or float(site.get("biology_years", 0.0)) + 1e-9 >= float(V("win", "foothold_biology_years"))
        if not started and not _demonstrated(site, "biology_closed_months"):
            return _fail(["not_demonstrated"])
        if scale == "millennium" and float(site.get("biology_years", 0.0)) + 1e-9 < float(V("win", "foothold_biology_years")) and not (state.get("footholds") or {}).get("biology", {}).get("achieved"):
            return _fail(["deep_locked"])
        return {"ok": True}
    machines = machine_replicator(site_name, site)
    if not machines["ok"]:
        return _fail(["not_self_sustaining"] + machines["reasons"])
    started = bool(paths.get("machine")) or float(site.get("machine_years", 0.0)) + 1e-9 >= float(V("win", "foothold_machine_years"))
    if not started and not _demonstrated(site, "machine_replicator_months"):
        return _fail(["not_demonstrated"])
    if scale == "millennium" and float(site.get("machine_years", 0.0)) + 1e-9 < float(V("win", "foothold_machine_years")) and not (state.get("footholds") or {}).get("machine", {}).get("achieved"):
        return _fail(["deep_locked"])
    return {"ok": True}


def _band(roll: int) -> str:
    if roll >= int(V("win", "epoch_stable_roll")):
        return "stable"
    if roll >= int(V("win", "epoch_strained_roll")):
        return "strained"
    if roll >= int(V("win", "epoch_setback_roll")):
        return "setback"
    return "collapse"


def _add_years(current: float, band: str, span: int) -> float:
    if band == "stable":
        return current + span
    if band == "strained":
        return current + (span // 2)
    if band == "setback":
        return current * 0.5
    return 0.0


def _spend_ore(site: dict[str, Any], years: float) -> float:
    """Return the years the ore body can actually feed. The rest is not lived."""
    rate = float(site.get("isru_metal_t_year", 0.0))
    reserve = float(site.get("ore_reserve_t", 0.0))
    if years <= 0 or rate <= 0:
        return 0.0
    affordable = reserve / rate
    lived = min(years, affordable)
    site["ore_reserve_t"] = max(0.0, reserve - rate * lived)
    return lived


def _harm_seed(site_name: str, site: dict[str, Any], path: str) -> None:
    if path == "human":
        population = int(site.get("population", 0))
        if population > 0:
            site["population"] = population - 1
            site["fatalities"] = int(site.get("fatalities", 0)) + 1
        site["inhabited_days"] = 0
        site["inhabited_years"] = 0.0
        return
    if path == "biology":
        organisms = site.get("organisms") or {}
        for name in list(organisms):
            organisms[name] = max(0, int(organisms[name]) - 1)
        return
    site["robots"] = max(0, int(site.get("robots", 0)) - 1)


def _drift(site: dict[str, Any], key: str) -> None:
    loss = float(V("win", key))
    if site.get("replication_improvement"):
        loss *= 0.5
    site["replication_fidelity"] = max(0.0, float(site.get("replication_fidelity", 0.0)) - loss)


def _seed_alive(site: dict[str, Any]) -> bool:
    from rms.settlement import reproducing_level

    if int(site.get("population", 0)) > 0 or int(site.get("robots", 0)) > 0 or reproducing_level(site) > 0:
        return True
    return False


def apply_epoch(
    state: dict[str, Any],
    action: dict[str, Any],
    *,
    force_roll: int | None = None,
    force_earth_roll: int | None = None,
) -> dict[str, Any]:
    site_name = str(action.get("site") or "mars")
    path = str(action.get("path") or "")
    scale = str(action.get("scale") or "")
    gate = eligible(state, site_name, path, scale)
    if not gate.get("ok"):
        return gate
    site = state["sites"][site_name]
    paths = site.setdefault("epoch_paths", {})
    paths[path] = True
    span = int(V("win", SCALES[scale]))
    turn = int(state["clock"]["turn"])
    roll = force_roll if force_roll is not None else roll_d100(state["rng_seed"], turn, f"epoch:{path}:{site_name}:{scale}")
    band = _band(int(roll))
    hazard = HAZARDS[path][int(roll) % len(HAZARDS[path])]
    ore_limited = False
    if band == "collapse":
        if path == "human":
            site["inhabited_years"] = 0.0
        elif path == "biology":
            site["biology_years"] = 0.0
        else:
            site["machine_years"] = 0.0
            site["tended_years"] = 0.0
            _drift(site, "epoch_fidelity_collapse")
        if int(roll) <= 5:
            _harm_seed(site_name, site, path)
            hazard = "catastrophic_" + hazard
        added = 0
    else:
        if path == "human":
            site["inhabited_years"] = _add_years(float(site.get("inhabited_years", 0.0)), band, span)
            added = span if band == "stable" else span // 2
        elif path == "biology":
            site["biology_years"] = _add_years(float(site.get("biology_years", 0.0)), band, span)
            added = span if band == "stable" else (span // 2 if band == "strained" else 0)
        else:
            proposed = _add_years(0.0, band, span)
            lived = _spend_ore(site, proposed)
            if lived + 1e-9 < proposed:
                ore_limited = True
            if band == "setback":
                site["machine_years"] = float(site.get("machine_years", 0.0)) * 0.5
                site["tended_years"] = float(site.get("tended_years", 0.0)) * 0.5
                _drift(site, "epoch_fidelity_setback")
                added = 0
            else:
                site["machine_years"] = float(site.get("machine_years", 0.0)) + lived
                if tended_life(site_name, site)["ok"]:
                    site["tended_years"] = float(site.get("tended_years", 0.0)) + lived
                if band == "strained":
                    _drift(site, "epoch_fidelity_strain")
                added = lived
            if band == "stable" and int(roll) >= int(V("win", "epoch_improvement_roll")):
                site["replication_improvement"] = True
    if not _seed_alive(site):
        paths[path] = False
        site["extinct"] = True
    earth_roll = force_earth_roll if force_earth_roll is not None else roll_d100(
        state["rng_seed"], turn, f"epoch-earth:{path}:{site_name}:{scale}"
    )
    earth_ended = int(earth_roll) <= int(V("win", EARTH_P[scale]))
    if earth_ended:
        state["earth_stability"] = 0
        state["political_capital"] = 0
        state["earth_program_ended"] = True
    months = span * 12
    year, month = add_months(state["clock"]["year"], state["clock"]["month"], months)
    state["clock"]["year"] = year
    state["clock"]["month"] = month
    state["clock"]["abs_month"] = int(state["clock"].get("abs_month", 0)) + months
    return {
        "mutated": True,
        "action": "epoch",
        "site": site_name,
        "path": path,
        "scale": scale,
        "span_years": span,
        "years_applied": added,
        "band": "ore_limited" if ore_limited and band != "collapse" else band,
        "hazard": hazard,
        "roll": int(roll),
        "earth_roll": int(earth_roll),
        "earth_program_ended": bool(state.get("earth_program_ended")),
        "estimate": True,
        "biology_years": round(float(site.get("biology_years", 0.0)), 4),
        "machine_years": round(float(site.get("machine_years", 0.0)), 4),
        "tended_years": round(float(site.get("tended_years", 0.0)), 4),
        "inhabited_years": round(float(site.get("inhabited_years", 0.0)), 4),
        "ore_reserve_t": round(float(site.get("ore_reserve_t", 0.0)), 3),
        "replication_fidelity": round(float(site.get("replication_fidelity", 0.0)), 4),
        "replication_improvement": bool(site.get("replication_improvement")),
    }
