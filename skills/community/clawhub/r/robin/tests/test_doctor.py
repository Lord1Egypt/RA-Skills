from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import pytest

from robin.config import load_index, save_index
from robin.serializer import build_text_entry, serialize_entry
from scripts import doctor

ROOT = Path(__file__).resolve().parents[1]


def _write_entry(robin_env, filename: str = "writing.md", *, entry_id: str = "20260408-a1f3c9", media_source: str = "") -> None:
    entry = build_text_entry(
        topic="Writing",
        content="Write as if speaking to a smart friend.",
        description="Guidance on conversational clarity in writing.",
        source="",
        note="",
        tags=["writing"],
        date_added="2026-04-08",
        media_source=media_source,
        entry_id=entry_id,
    )
    (robin_env["topics_dir"] / filename).write_text(serialize_entry(entry) + "\n", encoding="utf-8")


def _doctor_json(capsys):
    with pytest.raises(SystemExit) as exc_info:
        doctor.main()
    return exc_info.value.code, json.loads(capsys.readouterr().out)


def _codes(payload: dict) -> set[str]:
    return {item["code"] for item in payload["diagnostics"]}


def test_doctor_healthy_library_returns_ok(robin_env, monkeypatch, capsys):
    robin_env["media_dir"].mkdir()
    _write_entry(robin_env)
    index = load_index()
    index["items"]["20260408-a1f3c9"] = {
        "id": "20260408-a1f3c9",
        "topic": "writing",
        "date": "2026-04-08",
        "rating": 4,
        "last_surfaced": "2026-04-09T10:00:00+00:00",
        "times_surfaced": 1,
        "_awaiting_rating": False,
    }
    save_index(index)

    monkeypatch.setattr("sys.argv", ["doctor.py", "--json"])
    code, payload = _doctor_json(capsys)

    assert code == 0
    assert payload == {"ok": True, "errors": 0, "warnings": 0, "diagnostics": []}


def test_doctor_reports_malformed_topic_entry(robin_env, monkeypatch, capsys):
    robin_env["media_dir"].mkdir()
    (robin_env["topics_dir"] / "broken.md").write_text("date_added 2026-04-08\n\nBroken entry\n", encoding="utf-8")

    monkeypatch.setattr("sys.argv", ["doctor.py", "--json"])
    code, payload = _doctor_json(capsys)

    assert code == 1
    assert "invalid_topic_entry" in _codes(payload)


def test_doctor_reports_duplicate_entry_ids(robin_env, monkeypatch, capsys):
    robin_env["media_dir"].mkdir()
    _write_entry(robin_env, "one.md", entry_id="20260408-sameid")
    _write_entry(robin_env, "two.md", entry_id="20260408-sameid")

    monkeypatch.setattr("sys.argv", ["doctor.py", "--json"])
    code, payload = _doctor_json(capsys)

    assert code == 1
    assert "duplicate_entry_id" in _codes(payload)


def test_doctor_reports_missing_local_media(robin_env, monkeypatch, capsys):
    robin_env["media_dir"].mkdir()
    _write_entry(robin_env, media_source="media/writing/missing.png")
    save_index(
        {
            "items": {
                "20260408-a1f3c9": {
                    "id": "20260408-a1f3c9",
                    "topic": "writing",
                    "date": "2026-04-08",
                    "rating": None,
                    "last_surfaced": None,
                    "times_surfaced": 0,
                }
            }
        }
    )

    monkeypatch.setattr("sys.argv", ["doctor.py", "--json"])
    code, payload = _doctor_json(capsys)

    assert code == 1
    assert "missing_media" in _codes(payload)


def test_doctor_reports_index_drift_as_warning_only(robin_env, monkeypatch, capsys):
    robin_env["media_dir"].mkdir()
    _write_entry(robin_env)
    save_index(
        {
            "items": {
                "orphan-entry": {
                    "id": "orphan-entry",
                    "topic": "old",
                    "date": "2026-04-01",
                    "rating": None,
                    "last_surfaced": None,
                    "times_surfaced": 0,
                }
            }
        }
    )

    monkeypatch.setattr("sys.argv", ["doctor.py", "--json"])
    code, payload = _doctor_json(capsys)

    assert code == 0
    assert payload["errors"] == 0
    assert {"orphan_index_item", "missing_index_item"}.issubset(_codes(payload))


def test_doctor_reports_corrupt_review_index(robin_env, monkeypatch, capsys):
    robin_env["media_dir"].mkdir()
    _write_entry(robin_env)
    (robin_env["state_dir"] / "robin-review-index.json").write_text("{invalid json", encoding="utf-8")

    monkeypatch.setattr("sys.argv", ["doctor.py", "--json"])
    code, payload = _doctor_json(capsys)

    assert code == 1
    assert "invalid_index_json" in _codes(payload)


def test_doctor_script_json_smoke(robin_env):
    robin_env["media_dir"].mkdir()
    proc = subprocess.run(
        [sys.executable, str(ROOT / "scripts" / "doctor.py"), "--state-dir", str(robin_env["state_dir"]), "--json"],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )

    assert proc.returncode == 0, proc.stdout + proc.stderr
    payload = json.loads(proc.stdout)
    assert payload["ok"] is True
    assert payload["diagnostics"] == []
