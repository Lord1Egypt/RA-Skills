"""Save files, new games, and the public view (secrets stripped)."""

from __future__ import annotations

import json
import os
import random
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from rms.data import ROOT, advisors, factions

CREW_NAMES = [
    ("周晚舟", "Zhou Wanzhou"),
    ("阿米拉·哈达德", "Amira Haddad"),
    ("冈田健司", "Kenji Okada"),
    ("伊利亚·莫罗佐夫", "Ilya Morozov"),
    ("唐小禾", "Tang Xiaohe"),
    ("马特奥·伊瓦拉", "Mateo Ibarra"),
    ("妮娅·门萨", "Nia Mensah"),
    ("韩砺", "Han Li"),
    ("萨拉·林霍尔姆", "Sara Lindholm"),
    ("奥马尔·法鲁克", "Omar Farouk"),
    ("普丽娅·拉曼", "Priya Raman"),
    ("乔纳斯·贝尔格", "Jonas Berg"),
]


def save_dir() -> Path:
    override = os.environ.get("REALMARSSHOT_SAVE_DIR")
    if override:
        return Path(override)
    return Path.home() / ".realmarsshot" / "saves"


def safe_user_id(user_id: str) -> str:
    cleaned = re.sub(r"[^A-Za-z0-9_-]", "", user_id or "")
    if not cleaned or cleaned != (user_id or ""):
        raise ValueError("user id may contain only letters, numbers, underscore, and hyphen")
    return cleaned


def save_path(user_id: str) -> Path:
    return save_dir() / f"user-{safe_user_id(user_id)}.json"


def _blank_foothold(reason: str) -> dict[str, Any]:
    return {
        "achieved": False,
        "announced": False,
        "just_announced": False,
        "reason": reason,
        "site": None,
        "progress": 0,
    }


def blank_site() -> dict[str, Any]:
    return {
        "population": 0,
        "births": 0,
        "robots": 0,
        "landings_success": 0,
        "landings_fail": 0,
        "crew_returned": 0,
        "crew_missions": 0,
        "cargo_landings": 0,
        "survived_dust_season": False,
        "trial": False,
        "independent_months": 0,
        "evacuated": False,
        "extinct": False,
        "fatalities": 0,
        "inhabited_days": 0,
        "inhabited_years": 0.0,
        "biology_closed_months": 0,
        "biology_years": 0.0,
        "machine_tended_months": 0,
        "machine_replicator_months": 0,
        "machine_years": 0.0,
        "tended_years": 0.0,
        "epoch_paths": {},
        "organisms": {},
        "life_archive_accessions": 0,
        "ore_reserve_t": 0.0,
        "isru_metal_t_year": 0.0,
        "heat_reject_kwe": 0.0,
        "repair_fraction": 0.0,
        "replication_fidelity": 0.0,
        "replication_improvement": False,
        "stores": {"food_kg": 0.0, "water_kg": 0.0, "o2_kg": 0.0},
        "farms_m2": 0.0,
        "solar_kwe_clear": 0.0,
        "fission_kwe": 0.0,
        "battery_kwe": 0.0,
        "polar": False,
        "shielding_g_cm2": 0.0,
        "spe_shelter": False,
        "water_recovery": 0.0,
        "sabatier_fraction": 0.0,
        "electrolysis": False,
        "industrial_closure": 0.0,
        "knowledge_archive": False,
        "genome_archive_donors": 0,
        "isru_water_kg_year": 0.0,
        "isru_o2_kg_year": 0.0,
        "isru_ch4_kg_year": 0.0,
        "dust_storm_months_left": 0,
        "habitat": False,
        "greenhouse": False,
        "rtg": False,
        "relay": False,
        "ice_confirmed": False,
    }


def assign_secrets(seed: int, advisor_ids: list[str]) -> dict[str, Any]:
    rng = random.Random(seed)
    if advisor_ids and rng.randrange(100) < 45:
        mole = advisor_ids[rng.randrange(len(advisor_ids))]
    else:
        mole = None
    return {"mole": mole}


def new_state(
    *,
    user_id: str,
    language: str = "zh",
    director: str = "",
    program: str = "",
    seed: int = 20260101,
    difficulty: str = "realistic",
    tts: bool = True,
) -> dict[str, Any]:
    if language not in {"zh", "en"}:
        raise ValueError("language must be zh or en")
    if difficulty not in {"realistic", "hard"}:
        raise ValueError("difficulty must be realistic or hard")
    user_id = safe_user_id(user_id)
    advisor_ids = list(advisors().keys())
    roster = []
    for index in range(36):
        if index < len(CREW_NAMES):
            name = CREW_NAMES[index][0 if language == "zh" else 1]
        else:
            name = f"crew-{index + 1:02d}"
        roster.append({"id": f"crew-{index + 1:02d}", "name": name, "dose_mSv": 0.0, "status": "available"})
    hard = difficulty == "hard"
    faction_state = {}
    for key, row in factions().items():
        faction_state[key] = {
            "support": row["support"] - (5 if hard and key == "concord" else 0),
            "hostility": row["hostility"] + (15 if hard and key == "closed_sky" else 0),
        }
    now = datetime.now(timezone.utc).isoformat()
    state: dict[str, Any] = {
        "version": 2,
        "game": "realmarsshot",
        "language": language,
        "user_id": user_id,
        "director": director or ("指挥官" if language == "zh" else "Director"),
        "program": program or ("火种计划" if language == "zh" else "Ember Program"),
        "difficulty": difficulty,
        "created_at": now,
        "last_saved": now,
        "clock": {"year": 2026, "month": 1, "turn": 0, "abs_month": 0},
        "rng_seed": int(seed),
        "outcome": None,
        "outcome_reason": None,
        "outcome_site": None,
        "footholds": _blank_footholds(),
        "earth_program_ended": False,
        "treasury_busd": 1.5,
        "annual_budget_busd": 4.0 if hard else 6.0,
        "political_capital": 48 if hard else 55,
        "public_opinion": 42 if hard else 50,
        "earth_stability": 78 if hard else 82,
        "dissent": 18 if hard else 12,
        "safety_culture": 62,
        "deficit_months": 0,
        "suppressed": False,
        "second_source": False,
        "knowledge": 4,
        "crew": {
            "roster": roster,
            "in_training": [],
            "pipeline_per_year": 6 if hard else 8,
            "started_this_year": 0,
            "started_year": 2026,
            "psych": 70,
            "fatalities": 0,
        },
        "eclss": {
            "water_recovery_demonstrated": 0.0,
            "water_recovery_duration_days": 0,
            "o2_recovery_from_co2": 0.0,
            "food_closure_demonstrated": 0.0,
            "closed_habitat_days_record": 0,
            "biosphere_lesson": False,
        },
        "biology": {
            "simulant_days": 0,
            "levels": {},
            "tardigrade_exposure": False,
            "uncontained": False,
        },
        "sites": {"moon": blank_site(), "mars": blank_site(), "freespace": blank_site()},
        "facilities": {},
        "tech": [],
        "factions": faction_state,
        "advisors": {key: {"trust": row["trust"]} for key, row in advisors().items()},
        "genome_archive_donors": 0,
        "launch": {
            "heavy_per_year": 2,
            "heavy_leo_t": 40.0 if hard else 45.0,
            "medium_per_year": 6 if hard else 8,
            "medium_leo_t": 18.0,
            "busy_until_abs": 0,
            "reliability_heavy": 0.93 if hard else 0.96,
            "reliability_medium": 0.95 if hard else 0.97,
            "price_factor": 1.0,
        },
        "tts": {
            "enabled": bool(tts),
            "provider": "edge-tts",
            "voices": {"zh": "zh-CN-XiaoxiaoNeural", "en": "en-US-AriaNeural"},
        },
        "images": True,
        "log": [],
        "revelations": [],
        "secrets": assign_secrets(int(seed), advisor_ids),
        "last_event": None,
        "flags": {"pressure_crew_mars": False},
    }
    return state


def public_view(state: dict[str, Any]) -> dict[str, Any]:
    view = json.loads(json.dumps(state))
    view.pop("secrets", None)
    return view


def ready_crew(state: dict[str, Any], cap_mSv: float = 600.0) -> list[dict[str, Any]]:
    return [
        person
        for person in state["crew"]["roster"]
        if person["status"] == "available" and float(person["dose_mSv"]) < cap_mSv
    ]


def save_game(state: dict[str, Any], *, backup: bool = True) -> dict[str, Any]:
    path = save_path(state["user_id"])
    path.parent.mkdir(parents=True, exist_ok=True)
    state["last_saved"] = datetime.now(timezone.utc).isoformat()
    backup_path = None
    if backup and path.exists():
        backup_dir = path.parent.parent / "backups"
        backup_dir.mkdir(parents=True, exist_ok=True)
        stamp = datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S")
        backup_path = backup_dir / f"user-{state['user_id']}-{stamp}.json"
        backup_path.write_text(path.read_text(encoding="utf-8"), encoding="utf-8")
    path.write_text(json.dumps(state, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return {"success": True, "save_path": str(path), "backup_path": str(backup_path) if backup_path else None}


def _blank_footholds() -> dict[str, Any]:
    return {
        "human": _blank_foothold("foothold_500"),
        "human_century": _blank_foothold("foothold_human_century"),
        "biology": _blank_foothold("foothold_biology"),
        "machine": _blank_foothold("foothold_machine"),
    }


_LEGACY_FOOTHOLDS = (
    ("human", "foothold_500"),
    ("biology", "foothold_biology"),
    ("machine", "foothold_machine"),
)


def _ensure_site(site: dict[str, Any]) -> None:
    fresh = blank_site()
    for key, value in fresh.items():
        if key not in site:
            site[key] = json.loads(json.dumps(value))
        elif key == "stores" and isinstance(site.get("stores"), dict):
            for store_key, store_value in fresh["stores"].items():
                site["stores"].setdefault(store_key, store_value)
        elif key == "organisms" and not isinstance(site.get("organisms"), dict):
            site["organisms"] = {}
        elif key == "epoch_paths" and not isinstance(site.get("epoch_paths"), dict):
            site["epoch_paths"] = {}


def migrate(data: dict[str, Any]) -> dict[str, Any]:
    """Bring a version-1 save up to the tiered clocks. Idempotent.

    An announcement that already happened stays announced and does not fire again.
    A version-1 biology or machine foothold was a shorter clock. Keeping it achieved
    is the migration, not a new deep-time win. Deep-time years are not granted.
    """
    if not isinstance(data, dict):
        return data
    previous = int(data.get("version") or 1)
    footholds = data.get("footholds")
    if not isinstance(footholds, dict):
        footholds = {}
        data["footholds"] = footholds
    for key, reason in _LEGACY_FOOTHOLDS:
        row = footholds.get(key)
        if not isinstance(row, dict) or "achieved" not in row:
            footholds[key] = _blank_foothold(reason)
            row = footholds[key]
        row.setdefault("reason", reason)
        row.setdefault("announced", bool(row.get("achieved")))
        row.setdefault("site", None)
        row.setdefault("progress", 0)
        row["just_announced"] = False
    for key, reason in _blank_footholds().items():
        row = footholds.get(key)
        if not isinstance(row, dict) or "achieved" not in row:
            footholds[key] = _blank_foothold(reason["reason"])
        else:
            row.setdefault("reason", reason["reason"])
            row.setdefault("announced", bool(row.get("achieved")))
            row.setdefault("site", None)
            row.setdefault("progress", 0)
            row["just_announced"] = False
    sites = data.get("sites")
    if not isinstance(sites, dict):
        sites = {}
        data["sites"] = sites
    for name in ("moon", "mars", "freespace"):
        site = sites.get(name)
        if not isinstance(site, dict):
            sites[name] = blank_site()
            continue
        if "biology_years" not in site:
            months = float(site.get("biology_closed_months") or 0)
            site["biology_years"] = round(months * 30.0 / 365.25, 4)
        if "inhabited_years" not in site:
            site["inhabited_years"] = round(float(site.get("inhabited_days") or 0) / 365.25, 4)
        if "machine_years" not in site:
            site["machine_years"] = 0.0
        if "tended_years" not in site:
            tended_months = float(site.get("machine_tended_months") or 0)
            site["tended_years"] = round(tended_months * 30.0 / 365.25, 4)
        if "machine_replicator_months" not in site:
            site["machine_replicator_months"] = 0
        _ensure_site(site)
    if previous < 2:
        from rms.data import V

        biology = footholds.get("biology") or {}
        if biology.get("achieved"):
            site_name = biology.get("site") if biology.get("site") in sites else "mars"
            site = sites[site_name]
            site["biology_years"] = max(float(site.get("biology_years") or 0), float(V("win", "foothold_biology_years")))
            biology["progress"] = int(site["biology_years"])
            biology["site"] = site_name
        machine = footholds.get("machine") or {}
        if machine.get("achieved"):
            site_name = machine.get("site") if machine.get("site") in sites else "mars"
            site = sites[site_name]
            site["machine_years"] = max(float(site.get("machine_years") or 0), float(V("win", "foothold_machine_years")))
            machine["progress"] = int(site["machine_years"])
            machine["site"] = site_name
    data["version"] = 2
    data.setdefault("earth_program_ended", False)
    return data


def load_game(user_id: str) -> dict[str, Any]:
    path = save_path(user_id)
    if not path.exists():
        return {"exists": False, "save_path": str(path)}
    data = migrate(json.loads(path.read_text(encoding="utf-8")))
    return {"exists": True, "save_path": str(path), "data": data}


def skill_root() -> Path:
    return ROOT
