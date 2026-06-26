import json
from pathlib import Path

from rss_brew.compat import run_pipeline_v2 as rp


def test_list_committed_manifests_filters_current_non_committed_and_bad_payloads(tmp_path: Path):
    day_dir = tmp_path / "2026-03-09"
    day_dir.mkdir(parents=True)

    (day_dir / "CURRENT.json").write_text("{}", encoding="utf-8")
    (day_dir / "good.json").write_text(json.dumps({"status": "committed", "run_id": "good"}), encoding="utf-8")
    (day_dir / "failed.json").write_text(json.dumps({"status": "failed", "run_id": "failed"}), encoding="utf-8")
    (day_dir / "list_payload.json").write_text(json.dumps([1, 2, 3]), encoding="utf-8")
    (day_dir / "broken.json").write_text("{not json", encoding="utf-8")

    rows = rp.list_committed_manifests(day_dir)
    assert [row["run_id"] for row in rows] == ["good"]
    assert rows[0]["_path"].endswith("good.json")


def test_select_winner_works_with_legacy_committed_rows_missing_new_fields():
    committed = [
        {"run_id": "legacy", "status": "committed"},
        {"run_id": "modern", "status": "committed", "new_articles": 1, "deep_set_count": 0},
    ]

    winner = rp.select_winner(committed)
    assert winner is not None
    assert winner["run_id"] == "modern"
