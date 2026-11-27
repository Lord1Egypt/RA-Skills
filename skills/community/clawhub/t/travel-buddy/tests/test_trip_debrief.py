"""After a trip: one question round, lessons into the fields the intake form pre-fills, files aside."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import trip_debrief as D  # noqa: E402
from serve_trip_intake import load_profile_defaults  # noqa: E402


def _workspace(tmp_path: Path) -> tuple[Path, Path]:
    ws = tmp_path / "ws"
    for folder in ("plans", "html", "profiles"):
        (ws / folder).mkdir(parents=True)
    for stem, dest, start, end in (("2026-09-09-tokyo", "东京", "2026-09-09", "2026-09-13"),
                                   ("2026-10-25-shenzhen", "深圳", "2026-10-25", "2026-10-28"),
                                   ("2027-03-12-porto", "波尔图", "2027-03-12", "2027-03-15")):
        plan = {"trip": {"destination": dest, "start_date": start, "end_date": end}, "days": []}
        (ws / "plans" / f"{stem}.json").write_text(json.dumps(plan, ensure_ascii=False), encoding="utf-8")
        (ws / "plans" / f"{stem}.ics").write_text("BEGIN:VCALENDAR", encoding="utf-8")
        (ws / "html" / f"{stem}.html").write_text("<html>", encoding="utf-8")
    (ws / "plans" / "intake-20260901-x.json").write_text("{}", encoding="utf-8")
    profile = json.loads((ROOT / "templates" / "personal-travel-profile.json").read_text(encoding="utf-8"))
    profile.update(profile_id="t", storage_consent={"personal_profile": True, "confirmed_at": "2026-01-01",
                                                    "purpose": "x"})
    profile["travel_history"].update(visited_places=[], wish_list=[], excluded_places=[])
    profile["recurring_preferences"].update(pace="适中", avoid_list=["红眼航班"])
    path = ws / "profiles" / "t-profile.json"
    path.write_text(json.dumps(profile, ensure_ascii=False), encoding="utf-8")
    return ws, path


def test_asks_about_the_most_recent_finished_trip_only(tmp_path, capsys) -> None:
    ws, _ = _workspace(tmp_path)
    D.main(["list", "--workspace", str(ws), "--today", "2026-11-26"])
    out = capsys.readouterr().out
    assert out.count("ASK:") == 1 and "2026-10-25-shenzhen" in out
    assert "OLDER: 1 more" in out and "porto" not in out, "an upcoming trip is not asked about"


def test_record_reaches_the_next_intake_and_moves_the_files(tmp_path, capsys) -> None:
    ws, profile = _workspace(tmp_path)
    answers = tmp_path / "answers.json"
    answers.write_text(json.dumps({"went": "yes", "revisit": "no", "did_not_work": "每天走太多",
                                   "new_avoid": ["单段步行超过 20 分钟"], "pace": "慢游/深度"},
                                  ensure_ascii=False), encoding="utf-8")
    assert D.main(["record", str(ws / "plans" / "2026-10-25-shenzhen.json"), "--profile", str(profile),
                   "--answers", str(answers), "--today", "2026-11-26"]) == 0
    prefill = load_profile_defaults(profile)
    assert prefill["pace"] == "慢游/深度"
    assert prefill["avoid_list"] == ["红眼航班", "单段步行超过 20 分钟"]
    assert prefill["do_not_revisit_places"] == ["深圳"]
    assert sorted(p.name for p in (ws / "plans" / "past").iterdir()) == ["2026-10-25-shenzhen.ics",
                                                                        "2026-10-25-shenzhen.json"]
    assert (ws / "html" / "past" / "2026-10-25-shenzhen.html").exists()
    capsys.readouterr()
    D.main(["list", "--workspace", str(ws), "--today", "2026-11-26"])
    assert "2026-09-09-tokyo" in capsys.readouterr().out, "the next one up is the older trip"


def test_skip_the_rest_and_refusals(tmp_path, capsys) -> None:
    ws, profile = _workspace(tmp_path)
    assert D.main(["skip", "--workspace", str(ws), "--profile", str(profile), "--today", "2026-11-26"]) == 0
    capsys.readouterr()
    D.main(["list", "--workspace", str(ws), "--today", "2026-11-26"])
    out = capsys.readouterr().out
    assert "2026-10-25-shenzhen" in out and "OLDER" not in out, "skip leaves the trip being asked about"
    assert (ws / "plans" / "2026-09-09-tokyo.json").exists(), "a skipped trip's files stay where they were"

    bad = tmp_path / "bad.json"
    bad.write_text(json.dumps({"went": "yes", "pace": "fast"}), encoding="utf-8")
    before = profile.read_text(encoding="utf-8")
    assert D.main(["record", str(ws / "plans" / "2026-10-25-shenzhen.json"), "--profile", str(profile),
                   "--answers", str(bad)]) == 2
    assert profile.read_text(encoding="utf-8") == before, "a refused debrief writes nothing"
