"""World events. Effects are abstract (budget, trust, a lost prototype), not procedures."""

from __future__ import annotations

from typing import Any

from rms.data import events as event_table
from rms.dice import pick_weighted


def available(state: dict[str, Any]) -> list[tuple[str, float]]:
    table = event_table()
    found = []
    for event_id, row in table.items():
        if _open(state, row["requires"]):
            found.append((event_id, float(row["weight"])))
    return found


def _open(state: dict[str, Any], requires: str) -> bool:
    if requires in {"always", "researching_or_always"}:
        return True
    if requires == "no_second_source":
        return not state.get("second_source")
    if requires == "closed_sky_angry":
        return state["factions"]["closed_sky"]["hostility"] >= 30
    if requires == "has_mole":
        return bool(state.get("secrets", {}).get("mole"))
    if requires == "high_dissent":
        return state["dissent"] >= 40 or state.get("suppressed")
    if requires == "has_analog":
        return "analog_habitat" in state["facilities"]
    if requires == "mars_assets":
        mars = state["sites"]["mars"]
        return mars["robots"] > 0 or mars["habitat"] or mars["population"] > 0
    if requires == "has_farm":
        return any(site["farms_m2"] > 0 for site in state["sites"].values())
    if requires == "people_under_pressure":
        return state["eclss"]["closed_habitat_days_record"] > 0 or any(site["population"] > 0 for site in state["sites"].values())
    if requires == "crew_exposed":
        return any(site["population"] > 0 or site["crew_missions"] > 0 for site in state["sites"].values())
    if requires == "offworld_hardware":
        return any(site["robots"] or site["habitat"] for site in state["sites"].values())
    if requires == "biology_work":
        return state["biology"]["simulant_days"] > 0 or bool(state["biology"]["levels"])
    if requires == "low_safety":
        return state["safety_culture"] < 40
    if requires == "superheavy_tech":
        return "reusable_super_heavy" in state["tech"]
    return False


def choose_event(state: dict[str, Any], *, force: str | None, seed: int, turn: int) -> str | None:
    if force == "none":
        return None
    if force:
        return force
    weights = available(state)
    if not weights:
        return None
    return pick_weighted(seed, turn, "event", weights)


def apply_event(state: dict[str, Any], event_id: str | None, roll: int) -> dict[str, Any] | None:
    if not event_id:
        return None
    text = _TEXTS.get(event_id, {"zh": event_id, "en": event_id})
    effect = _apply(state, event_id, roll)
    return {"id": event_id, "roll": roll, "zh": text["zh"], "en": text["en"], "effect": effect}


def _clamp(state: dict[str, Any], key: str, low: float = 0, high: float = 100) -> None:
    state[key] = max(low, min(high, state[key]))


def _apply(state: dict[str, Any], event_id: str, roll: int) -> dict[str, Any]:
    if event_id == "quiet_quarter":
        return {"note": "quiet"}
    if event_id == "public_inspiration":
        state["public_opinion"] += 6
        state["political_capital"] += 3
    elif event_id == "budget_cut":
        state["annual_budget_busd"] = max(1.0, state["annual_budget_busd"] * 0.85)
        state["political_capital"] -= 6
    elif event_id == "hearthbound_protest":
        state["public_opinion"] -= 4
        state["dissent"] += 6
        state["factions"]["hearthbound"]["hostility"] += 4
    elif event_id == "ember_pressure":
        state["flags"]["pressure_crew_mars"] = True
        state["factions"]["ember_covenant"]["support"] += 5
        state["political_capital"] += 2
    elif event_id == "science_grant":
        state["treasury_busd"] += 0.4
        state["knowledge"] += 1
    elif event_id == "price_hike":
        state["launch"]["price_factor"] = round(float(state["launch"]["price_factor"]) * 1.15, 3)
    elif event_id == "partner_offer":
        state["factions"]["meridian"]["support"] += 6
        state["factions"]["concord"]["support"] += 4
    elif event_id == "climate_shock":
        state["earth_stability"] -= 8
        state["public_opinion"] -= 3
    elif event_id == "sabotage":
        state["treasury_busd"] -= 0.35
        state["dissent"] += 8
        state["factions"]["closed_sky"]["hostility"] += 5
        state["safety_culture"] -= 4
    elif event_id == "mole_exposed":
        mole = state.get("secrets", {}).get("mole")
        if mole and not any(item.get("mole") == mole for item in state["revelations"]):
            state["revelations"].append({"type": "mole", "mole": mole})
            state["dissent"] += 10
            state["political_capital"] -= 8
            state["factions"]["closed_sky"]["hostility"] += 10
    elif event_id == "whistleblower":
        state["public_opinion"] -= 8
        state["dissent"] += 5
        state["suppressed"] = False
    elif event_id == "analog_incident":
        state["safety_culture"] -= 3
        state["knowledge"] += 1
        state["eclss"]["biosphere_lesson"] = True
    elif event_id == "breakthrough":
        state["knowledge"] += 2
        state["public_opinion"] += 3
    elif event_id == "dust_storm":
        mars = state["sites"]["mars"]
        mars["dust_storm_months_left"] = max(int(mars["dust_storm_months_left"]), 4)
    elif event_id == "crop_blight":
        for site in state["sites"].values():
            if site["farms_m2"] > 0:
                site["farms_m2"] = round(site["farms_m2"] * 0.7, 1)
    elif event_id == "psych_incident":
        state["crew"]["psych"] = max(0, state["crew"]["psych"] - 8)
        state["dissent"] += 4
    elif event_id == "spe_watch":
        # The mission resolver owns acute dose. This event is the warning and a small political tremor.
        state["public_opinion"] -= 2
    elif event_id == "micrometeoroid":
        for site in state["sites"].values():
            if site["solar_kwe_clear"] > 0:
                site["solar_kwe_clear"] = round(site["solar_kwe_clear"] * 0.85, 2)
                break
    elif event_id == "perchlorate_lesson":
        state["knowledge"] += 2
        state["biology"]["levels"]["perchlorate_respected"] = True
    elif event_id == "crew_guild_standdown":
        state["safety_culture"] += 5
        state["launch"]["busy_until_abs"] = max(state["launch"]["busy_until_abs"], state["clock"]["abs_month"] + 3)
    elif event_id == "treaty_opening":
        state["factions"]["concord"]["support"] += 8
        state["political_capital"] += 4
    elif event_id == "commercial_surge":
        state["launch"]["heavy_per_year"] += 1
    for key in ("public_opinion", "political_capital", "dissent", "safety_culture", "earth_stability"):
        _clamp(state, key)
    state["crew"]["psych"] = max(0, min(100, state["crew"]["psych"]))
    return {"roll": roll}


_TEXTS = {
    "quiet_quarter": {
        "zh": "这个季度没有灾难。试验日志按页增加，这本身就是消息。",
        "en": "The quarter produced no disaster. The log simply got longer, which is itself the news.",
    },
    "public_inspiration": {
        "zh": "一次干净的试验被拍进了晚间新闻。舆论短暂地站到了你这边。",
        "en": "A clean test made the evening news. Opinion stands with you for a while.",
    },
    "budget_cut": {
        "zh": "拨款委员会砍了年度预算。他们没有取消计划，他们让计划变慢。",
        "en": "The appropriation committee cut the annual budget. They did not cancel the plan. They slowed it.",
    },
    "hearthbound_protest": {
        "zh": "守炉派堵住了试验场的路。他们的句子很简单：地球上的人还没活好。",
        "en": "Hearthbound blocked the test range road. Their sentence is simple: people on Earth are not yet secure.",
    },
    "ember_pressure": {
        "zh": "火种盟在内部会议上拍桌子。他们要一个载人火星日期，越早越好。",
        "en": "The Ember Covenant pounds the table. They want a crewed Mars date, and they want it early.",
    },
    "science_grant": {
        "zh": "一笔科学拨款到账，指定给封闭舱和星壤，不许拿去买一次壮丽的发射。",
        "en": "A science grant arrives, earmarked for chambers and regolith, not for a glorious launch.",
    },
    "price_hike": {
        "zh": "发射行会上调了价格。你没有第二来源。",
        "en": "The Launch Guild raises prices. You have no second source.",
    },
    "partner_offer": {
        "zh": "子午线局提议分享一次发射窗口。条件写在微笑后面。",
        "en": "The Meridian Directorate offers to share a launch window. The conditions sit behind the smile.",
    },
    "climate_shock": {
        "zh": "地球这边先出了事。洪水、热浪、电网。稳定度下降。计划突然显得像奢侈品。",
        "en": "Earth breaks first. Flood, heat, a grid. Stability drops. The plan suddenly looks like a luxury.",
    },
    "sabotage": {
        "zh": "一套地面原型在夜间失火。调查称之为电气故障。闭天会没有留下名字。",
        "en": "A ground prototype burns at night. The inquiry calls it electrical. Closed Sky leaves no name.",
    },
    "mole_exposed": {
        "zh": "账本对不上。有人把试验日程交给了闭天会。名字现在公开了。",
        "en": "The books do not match. Someone handed the test schedule to Closed Sky. The name is public now.",
    },
    "whistleblower": {
        "zh": "有人把你们压下去的事故报告寄给了记者。掩盖比事故更贵。",
        "en": "Someone mails the buried incident report to a reporter. The cover-up costs more than the incident.",
    },
    "analog_incident": {
        "zh": "模拟舱的氧气往下掉，像生物圈二号那样。人被撤出来了。你们获得的是一课，不是一座坟。",
        "en": "Oxygen in the analog drifts down, Biosphere 2 fashion. The crew walks out. You bought a lesson, not a grave.",
    },
    "breakthrough": {
        "zh": "一组讨厌的数据忽然连成了线。知识增加，欢呼很少。",
        "en": "An ugly data set suddenly lines up. Knowledge goes up. There is little cheering.",
    },
    "dust_storm": {
        "zh": "火星进入尘暴季。只靠太阳电池的资产会在几个月里挨饿。",
        "en": "Mars enters a dust-storm season. Assets that live on solar power will starve for months.",
    },
    "crop_blight": {
        "zh": "温室里的一种作物倒了。卡路里比照片脆弱。",
        "en": "A greenhouse crop fails. Calories are more fragile than the photograph.",
    },
    "psych_incident": {
        "zh": "封闭环境里的一次冲突升级。乘员公会要求休息，不是动员演讲。",
        "en": "A conflict inside the sealed volume escalates. The Crew Guild wants rest, not a speech.",
    },
    "spe_watch": {
        "zh": "太阳监测网发出粒子事件警报。有掩体的人进去。没有掩体的人只能计算剂量。",
        "en": "The solar watch issues a particle-event alert. People with a shelter go inside. People without one can only integrate the dose.",
    },
    "micrometeoroid": {
        "zh": "一块很小的石头打中了太阳能电池。功率永久地少了一截。",
        "en": "A very small rock hits a solar array. The power is permanently a little lower.",
    },
    "perchlorate_lesson": {
        "zh": "模拟星壤里的高氯酸盐再次毁掉一批幼苗。凤凰号当年的测量不是历史 trivia。",
        "en": "Perchlorate in the simulant kills another tray of seedlings. The Phoenix measurement is not trivia.",
    },
    "crew_guild_standdown": {
        "zh": "乘员公会停飞三个月。安全文化太低的时候，这是他们仅有的投票方式。",
        "en": "The Crew Guild stands down for three months. When safety culture is low, this is the vote they have.",
    },
    "treaty_opening": {
        "zh": "协和框架出现一个可以签字的窗口。第二发射来源通常是这么来的。",
        "en": "A signature window opens in the Concord frame. Second launch sources usually arrive this way.",
    },
    "commercial_surge": {
        "zh": "超重型运载的试飞统计终于好看到能多买一个班次。",
        "en": "The super-heavy test record is finally good enough to buy one more flight a year.",
    },
}
