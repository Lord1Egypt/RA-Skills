"""The draft page: real prices or none, a total the script adds up, and the questions first."""

from __future__ import annotations

import copy
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import render_draft as R  # noqa: E402

DRAFT = {
    "language": "en", "title": "Porto, 3 nights", "origin": "Amsterdam", "destination": "Porto",
    "start_date": "2027-03-12", "end_date": "2027-03-15", "travellers": 2, "rooms": 1, "currency": "EUR",
    "getting_there": [{"label": "HV6007 / HV6002", "outbound": "AMS 06:30 → OPO 08:15", "stops": 0,
                       "per_person_low": 298, "per_person_high": 298, "source": "Kiwi.com",
                       "checked_at": "2026-11-26",
                       "url": "https://www.kiwi.com/en/search/results/amsterdam-netherlands/porto-portugal/2027-03-12/2027-03-15?adults=2"}],
    "stay_areas": [{"name": "Centro", "why": "walkable", "nightly_low": 80, "nightly_high": 110,
                    "source": "Booking.com", "checked_at": "2026-11-26"}],
    "daily_spend": {"per_person_low": 40, "per_person_high": 70, "basis": "estimate"},
    "outline": ["Day 1: old town"], "decisions": ["Which flight?"],
}


def test_total_is_added_up_from_the_parts() -> None:
    parts = R.cost_range(DRAFT)
    assert parts["getting_there"] == (298, 298)
    assert parts["stay"] == (80 * 3 / 2, 110 * 3 / 2), "a shared room is split between the party"
    assert parts["daily"] == (40 * 4, 70 * 4)
    assert parts["total"] == (298 + 120 + 160, 298 + 165 + 280)


def test_a_price_without_source_or_date_is_refused() -> None:
    assert R.validate(DRAFT) == []
    no_source = copy.deepcopy(DRAFT)
    del no_source["stay_areas"][0]["source"]
    assert any("source and checked_at" in e for e in R.validate(no_source))
    unsourced_spend = copy.deepcopy(DRAFT)
    unsourced_spend["daily_spend"]["basis"] = "researched"
    assert any("daily_spend" in e for e in R.validate(unsourced_spend)), "only a labelled estimate needs no source"
    no_questions = dict(DRAFT, decisions=[])
    assert any("checkpoint" in e for e in R.validate(no_questions))
    backwards = dict(DRAFT, end_date="2027-03-10")
    assert any("after start_date" in e for e in R.validate(backwards))


def test_page_says_draft_and_labels_searches(tmp_path, capsys) -> None:
    page = R.render(DRAFT)
    assert "Not fact-checked yet" in page and "About EUR 578–743 per person, all in" in page
    assert page.index("To build the full plan") < page.index("<h2>Getting there"), "the questions come first"
    assert "Search Kiwi.com (pick from the results)" in page
    zh = R.render(dict(DRAFT, language="zh"))
    assert "草稿" in zh and "Not fact-checked" not in zh

    path = tmp_path / "draft.json"
    path.write_text(json.dumps(DRAFT), encoding="utf-8")
    assert R.main([str(path), "--workspace", str(tmp_path / "ws")]) == 0
    out = capsys.readouterr().out
    assert "ASK: Which flight?" in out and "Draft HTML:" in out
    assert R.main([str(path), "--workspace", str(tmp_path / "ws")]) == 1, "no silent overwrite"
