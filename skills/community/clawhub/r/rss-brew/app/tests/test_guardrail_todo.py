import json
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

from rss_brew.compat import run_pipeline_v2 as rp


def test_scoring_v2_phase_script_fallback_resolves_missing_local_files():
    rule = rp.phase_script("phase_rule_filter_score.py")
    model = rp.phase_script("phase_model_score.py")

    assert rule.exists()
    assert model.exists()
    assert "scripts" in str(rule)
    assert "scripts" in str(model)


def _run_orchestrator(monkeypatch, data_root: Path, new_count: int, deep_count: int) -> int:
    def fake_run_cmd(cmd: list[str]) -> int:
        cmd_s = [str(c) for c in cmd]

        def arg(name: str) -> str:
            return cmd_s[cmd_s.index(name) + 1]

        if any("phase_a_score.py" in c for c in cmd_s):
            src = Path(arg("--input"))
            out = Path(arg("--output"))
            payload = rp.read_json(src, {})
            out.parent.mkdir(parents=True, exist_ok=True)
            out.write_text(json.dumps({"article_count": int(payload.get("article_count", 0) or 0), "articles": []}), encoding="utf-8")
            return 0

        if any("phase_b_analyze.py" in c for c in cmd_s):
            out = Path(arg("--output"))
            out.parent.mkdir(parents=True, exist_ok=True)
            out.write_text(json.dumps({"article_count": deep_count, "articles": []}), encoding="utf-8")
            return 0

        if any("digest_writer.py" in c for c in cmd_s):
            out = Path(arg("--output"))
            out.parent.mkdir(parents=True, exist_ok=True)
            out.write_text(f"digest for new={new_count} deep={deep_count}\n", encoding="utf-8")
            return 0

        if any("core_pipeline.py" in c for c in cmd_s):
            out = Path(arg("--output"))
            out.parent.mkdir(parents=True, exist_ok=True)
            out.write_text(json.dumps({"article_count": new_count, "articles": []}), encoding="utf-8")
            return 0

        raise AssertionError(f"Unexpected command: {cmd}")

    monkeypatch.setattr(rp, "run_cmd", fake_run_cmd)

    incoming_new = data_root / "new-articles.json"
    incoming_new.parent.mkdir(parents=True, exist_ok=True)
    incoming_new.write_text(json.dumps({"article_count": new_count, "articles": []}), encoding="utf-8")

    argv = [
        "run_pipeline_v2.py",
        "--data-root",
        str(data_root),
        "--skip-core",
        "--mock",
    ]

    old_argv = sys.argv
    sys.argv = argv
    try:
        rp.main()
    finally:
        sys.argv = old_argv
    return 0


def test_current_pointer_written_and_kept_on_same_day_zero_new_retry(monkeypatch, tmp_path: Path):
    data_root = tmp_path / "data"

    _run_orchestrator(monkeypatch, data_root, new_count=5, deep_count=2)
    time.sleep(1.1)
    _run_orchestrator(monkeypatch, data_root, new_count=0, deep_count=0)

    day = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    day_records = data_root / "run-records" / day
    daily_day = data_root / "daily" / day

    manifests = sorted(p for p in day_records.glob("*.json") if p.name != "CURRENT.json")
    assert len(manifests) == 2

    first = json.loads(manifests[0].read_text(encoding="utf-8"))
    second = json.loads(manifests[1].read_text(encoding="utf-8"))

    assert first["status"] == "committed"
    assert first["new_articles"] == 5

    assert second["status"] == "committed"
    assert second["new_articles"] == 0
    assert second["failure_reason"] == "guardrail_nonzero_committed_winner_preserved"
    assert second["deep_set_count"] == first["deep_set_count"]

    current_run_id = first["run_id"]

    current_records = json.loads((day_records / "CURRENT.json").read_text(encoding="utf-8"))
    current_daily_json = json.loads((daily_day / "CURRENT.json").read_text(encoding="utf-8"))
    current_daily_txt = (daily_day / "CURRENT").read_text(encoding="utf-8").strip()

    assert current_records["winner_run_id"] == current_run_id
    assert current_daily_json["winner_run_id"] == current_run_id
    assert current_daily_txt == current_run_id


def test_same_day_retry_preserves_winner_digest_and_current_pointer(monkeypatch, tmp_path: Path):
    data_root = tmp_path / "data"

    _run_orchestrator(monkeypatch, data_root, new_count=3, deep_count=1)
    day = datetime.now(timezone.utc).strftime("%Y-%m-%d")

    day_records = data_root / "run-records" / day
    daily_day = data_root / "daily" / day

    first_manifest = next(p for p in sorted(day_records.glob("*.json")) if p.name != "CURRENT.json")
    first = json.loads(first_manifest.read_text(encoding="utf-8"))
    first_digest = Path(first["published_path"]) / f"daily-digest-{day}.md"
    assert first_digest.exists()
    first_digest_text = first_digest.read_text(encoding="utf-8")

    time.sleep(1.1)
    _run_orchestrator(monkeypatch, data_root, new_count=0, deep_count=0)

    manifests = sorted(p for p in day_records.glob("*.json") if p.name != "CURRENT.json")
    second = json.loads(manifests[-1].read_text(encoding="utf-8"))
    assert second["failure_reason"] == "guardrail_nonzero_committed_winner_preserved"

    top_level_digest = (data_root / "digests" / f"daily-digest-{day}.md").read_text(encoding="utf-8")
    assert top_level_digest == first_digest_text

    current_run_id = json.loads((day_records / "CURRENT.json").read_text(encoding="utf-8"))["winner_run_id"]
    assert current_run_id == first["run_id"]
    assert (daily_day / "CURRENT").read_text(encoding="utf-8").strip() == first["run_id"]


def test_legacy_winner_without_published_path_still_promotes_canonical_outputs(monkeypatch, tmp_path: Path):
    data_root = tmp_path / "data"
    day = datetime.now(timezone.utc).strftime("%Y-%m-%d")

    legacy_run_id = "legacy-winner"
    legacy_publish = data_root / "daily" / day / legacy_run_id
    legacy_publish.mkdir(parents=True, exist_ok=True)
    (legacy_publish / "deep-set.json").write_text('{"article_count": 2, "marker": "winner"}\n', encoding="utf-8")
    (legacy_publish / f"daily-digest-{day}.md").write_text("winner digest\n", encoding="utf-8")

    run_records_day = data_root / "run-records" / day
    run_records_day.mkdir(parents=True, exist_ok=True)
    (run_records_day / "20260101T000000Z-1.json").write_text(
        json.dumps(
            {
                "day": day,
                "run_id": legacy_run_id,
                "status": "committed",
                "new_articles": 5,
                "deep_set_count": 2,
                # intentionally no published_path (legacy manifest shape)
                "finalize_finished_at": "2026-01-01T00:00:00+00:00",
            }
        ),
        encoding="utf-8",
    )

    # Seed stale top-level canonical outputs that should be overwritten from winner publish dir.
    (data_root / "deep-set.json").parent.mkdir(parents=True, exist_ok=True)
    (data_root / "deep-set.json").write_text('{"article_count": 1, "marker": "stale"}\n', encoding="utf-8")
    (data_root / "digests" / f"daily-digest-{day}.md").parent.mkdir(parents=True, exist_ok=True)
    (data_root / "digests" / f"daily-digest-{day}.md").write_text("stale digest\n", encoding="utf-8")

    _run_orchestrator(monkeypatch, data_root, new_count=0, deep_count=0)

    assert (data_root / "deep-set.json").read_text(encoding="utf-8") == (legacy_publish / "deep-set.json").read_text(encoding="utf-8")
    assert (data_root / "digests" / f"daily-digest-{day}.md").read_text(encoding="utf-8") == (
        legacy_publish / f"daily-digest-{day}.md"
    ).read_text(encoding="utf-8")

    current_run_id = json.loads((run_records_day / "CURRENT.json").read_text(encoding="utf-8"))["winner_run_id"]
    assert current_run_id == legacy_run_id
