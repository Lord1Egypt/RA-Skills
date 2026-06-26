import csv
import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
SCRIPT = ROOT / "scripts" / "run-late-context-evals.py"
MANIFEST = ROOT / "evals" / "report-cases.csv"


def load_manifest() -> list[dict[str, str]]:
    with MANIFEST.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def test_late_context_eval_artifacts_exist():
    assert SCRIPT.exists()
    assert MANIFEST.exists()


def test_manifest_context_paths_resolve():
    rows = load_manifest()
    assert len(rows) >= 3
    for row in rows:
        assert row["context_path"], row
        assert (ROOT / row["context_path"]).exists(), row


def test_late_context_eval_runner_passes(tmp_path: Path):
    json_out = tmp_path / "late-context-evals.json"
    result = subprocess.run(
        [
            sys.executable,
            str(SCRIPT),
            "--root",
            str(ROOT),
            "--format",
            "json",
            "--json-out",
            str(json_out),
        ],
        capture_output=True,
        text=True,
        timeout=20,
    )
    assert result.returncode == 0, result.stdout + result.stderr

    payload = json.loads(result.stdout)
    assert payload["summary"]["total"] >= 3
    assert payload["summary"]["failed"] == 0
    assert payload["summary"]["isolated_cases_with_drift"] == 0
    assert payload["summary"]["baseline_cases_with_drift"] >= 2
    assert payload["summary"]["drift_reduction"] > 0
    assert payload["summary"]["avg_extraction_ms"] >= 0

    written = json.loads(json_out.read_text(encoding="utf-8"))
    assert written["summary"]["failed"] == 0
