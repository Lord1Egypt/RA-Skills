"""Tests for CSV audit report generation."""

from __future__ import annotations

import csv
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from quorum.audit import (
    DETAIL_COLUMNS,
    SUMMARY_COLUMNS,
    _build_detail_row,
    _build_summary_row,
    _parse_duration,
    generate_audit_reports,
    generate_batch_audit_reports,
)
from quorum.cost import CostTracker
from quorum.models import FileResult, Verdict, VerdictStatus


# ── Helpers ───────────────────────────────────────────────────────────────────

def _make_run_dir(
    tmp_path: Path,
    file_path: str = "/project/foo.py",
    verdict_status: str = "PASS",
    finding_count: int = 0,
    started_at: str = "2026-03-09T10:00:00+00:00",
    completed_at: str = "2026-03-09T10:00:05+00:00",
    artifact_text: str = "def foo():\n    pass\n",
) -> Path:
    """Create a minimal run directory matching what the pipeline writes."""
    run_dir = tmp_path / "run"
    run_dir.mkdir(exist_ok=True)

    (run_dir / "artifact.txt").write_text(artifact_text, encoding="utf-8")

    manifest = {
        "target": file_path,
        "started_at": started_at,
        "completed_at": completed_at,
        "verdict": verdict_status,
    }
    (run_dir / "run-manifest.json").write_text(json.dumps(manifest), encoding="utf-8")

    findings = [
        {
            "id": f"F-{i:08x}",
            "severity": "HIGH",
            "description": f"issue {i}",
            "evidence": {"tool": "test", "result": "test"},
        }
        for i in range(finding_count)
    ]
    verdict_data = {
        "status": verdict_status,
        "reasoning": "test reasoning",
        "confidence": 0.9,
        "report": {
            "findings": findings,
            "confidence": 0.9,
            "conflicts_resolved": 0,
            "critic_results": [],
        },
    }
    (run_dir / "verdict.json").write_text(json.dumps(verdict_data), encoding="utf-8")

    return run_dir


def _make_tracker(file_path: str, calls: list[tuple] | None = None) -> CostTracker:
    """Create a CostTracker with pre-loaded records for a file."""
    tracker = CostTracker()
    tracker.set_current_file(file_path)
    if calls is None:
        calls = [
            ("critic.correctness", "claude-sonnet-4", 500, 200, 0.001),
            ("critic.security", "claude-opus-4", 600, 300, 0.003),
        ]
    for call_name, model, prompt_t, completion_t, cost in calls:
        tracker.track(call_name, model, prompt_t, completion_t, cost)
    return tracker


_T0 = datetime(2026, 3, 9, 10, 0, 0, tzinfo=timezone.utc)
_T1 = datetime(2026, 3, 9, 10, 1, 0, tzinfo=timezone.utc)  # 60s later


# ── _parse_duration ───────────────────────────────────────────────────────────


class TestParseDuration:
    def test_basic(self):
        assert _parse_duration("2026-03-09T10:00:00+00:00", "2026-03-09T10:00:05+00:00") == pytest.approx(5.0)

    def test_empty_strings_return_zero(self):
        assert _parse_duration("", "") == 0.0
        assert _parse_duration("2026-03-09T10:00:00+00:00", "") == 0.0

    def test_invalid_strings_return_zero(self):
        assert _parse_duration("not-a-date", "also-not") == 0.0

    def test_negative_clamped_to_zero(self):
        # end before start → should return 0.0
        result = _parse_duration("2026-03-09T10:00:05+00:00", "2026-03-09T10:00:00+00:00")
        assert result == 0.0


# ── _build_detail_row ─────────────────────────────────────────────────────────


class TestBuildDetailRow:
    def test_correct_columns(self, tmp_path):
        run_dir = _make_run_dir(tmp_path, file_path="/p/foo.py")
        tracker = _make_tracker("/p/foo.py")
        row = _build_detail_row(run_dir, "/p/foo.py", tracker.summary().records)
        assert set(row.keys()) == set(DETAIL_COLUMNS)

    def test_sha256_matches_artifact(self, tmp_path):
        artifact_text = "def foo():\n    return 42\n"
        run_dir = _make_run_dir(tmp_path, file_path="/p/foo.py", artifact_text=artifact_text)
        tracker = _make_tracker("/p/foo.py")
        row = _build_detail_row(run_dir, "/p/foo.py", tracker.summary().records)
        expected_sha256 = hashlib.sha256(artifact_text.encode("utf-8")).hexdigest()
        assert row["sha256"] == expected_sha256

    def test_file_size_bytes(self, tmp_path):
        artifact_text = "hello"
        run_dir = _make_run_dir(tmp_path, file_path="/p/foo.py", artifact_text=artifact_text)
        tracker = _make_tracker("/p/foo.py")
        row = _build_detail_row(run_dir, "/p/foo.py", tracker.summary().records)
        assert row["file_size_bytes"] == len(artifact_text.encode("utf-8"))

    def test_file_token_estimate(self, tmp_path):
        artifact_text = "x" * 400  # 400 chars → 100 tokens
        run_dir = _make_run_dir(tmp_path, file_path="/p/foo.py", artifact_text=artifact_text)
        tracker = _make_tracker("/p/foo.py")
        row = _build_detail_row(run_dir, "/p/foo.py", tracker.summary().records)
        assert row["file_token_estimate"] == 100

    def test_duration_computed(self, tmp_path):
        run_dir = _make_run_dir(
            tmp_path,
            started_at="2026-03-09T10:00:00+00:00",
            completed_at="2026-03-09T10:00:10+00:00",
        )
        tracker = _make_tracker("/p/foo.py")
        row = _build_detail_row(run_dir, "/p/foo.py", tracker.summary().records)
        assert row["duration_seconds"] == pytest.approx(10.0)

    def test_token_counts_from_tracker(self, tmp_path):
        run_dir = _make_run_dir(tmp_path, file_path="/p/foo.py")
        tracker = _make_tracker("/p/foo.py", calls=[
            ("critic.correctness", "claude-sonnet-4", 100, 50, 0.001),
        ])
        row = _build_detail_row(run_dir, "/p/foo.py", tracker.summary().records)
        assert row["input_tokens"] == 100
        assert row["output_tokens"] == 50

    def test_cost_from_tracker(self, tmp_path):
        run_dir = _make_run_dir(tmp_path, file_path="/p/foo.py")
        tracker = _make_tracker("/p/foo.py", calls=[
            ("critic.correctness", "claude-sonnet-4", 100, 50, 0.005),
            ("critic.security", "claude-opus-4", 200, 100, 0.010),
        ])
        row = _build_detail_row(run_dir, "/p/foo.py", tracker.summary().records)
        assert row["cost_usd"] == pytest.approx(0.015)

    def test_models_used_sorted(self, tmp_path):
        run_dir = _make_run_dir(tmp_path, file_path="/p/foo.py")
        tracker = _make_tracker("/p/foo.py", calls=[
            ("c1", "zmodel", 100, 50, 0.001),
            ("c2", "amodel", 200, 100, 0.002),
        ])
        row = _build_detail_row(run_dir, "/p/foo.py", tracker.summary().records)
        assert row["models_used"] == "amodel,zmodel"

    def test_verdict_and_finding_count(self, tmp_path):
        run_dir = _make_run_dir(tmp_path, verdict_status="REJECT", finding_count=3)
        tracker = _make_tracker("/p/foo.py")
        row = _build_detail_row(run_dir, "/p/foo.py", tracker.summary().records)
        assert row["verdict"] == "REJECT"
        assert row["finding_count"] == 3

    def test_zero_findings(self, tmp_path):
        run_dir = _make_run_dir(tmp_path, verdict_status="PASS", finding_count=0)
        tracker = _make_tracker("/p/foo.py")
        row = _build_detail_row(run_dir, "/p/foo.py", tracker.summary().records)
        assert row["finding_count"] == 0
        assert row["verdict"] == "PASS"

    def test_many_findings(self, tmp_path):
        run_dir = _make_run_dir(tmp_path, verdict_status="REJECT", finding_count=25)
        tracker = _make_tracker("/p/foo.py")
        row = _build_detail_row(run_dir, "/p/foo.py", tracker.summary().records)
        assert row["finding_count"] == 25

    def test_tokens_per_second_computed(self, tmp_path):
        run_dir = _make_run_dir(
            tmp_path,
            file_path="/p/foo.py",
            started_at="2026-03-09T10:00:00+00:00",
            completed_at="2026-03-09T10:00:02+00:00",  # 2 seconds
        )
        tracker = _make_tracker("/p/foo.py", calls=[
            ("c", "m", 0, 200, 0.001),  # 200 output tokens
        ])
        row = _build_detail_row(run_dir, "/p/foo.py", tracker.summary().records)
        assert row["tokens_per_second"] == pytest.approx(100.0)  # 200/2

    def test_zero_duration_no_divide_by_zero(self, tmp_path):
        run_dir = _make_run_dir(
            tmp_path,
            started_at="2026-03-09T10:00:00+00:00",
            completed_at="2026-03-09T10:00:00+00:00",  # same time
        )
        tracker = _make_tracker("/p/foo.py")
        row = _build_detail_row(run_dir, "/p/foo.py", tracker.summary().records)
        assert row["tokens_per_second"] == 0.0

    def test_only_counts_records_for_this_file(self, tmp_path):
        """Records for other files must not contaminate this row."""
        run_dir = _make_run_dir(tmp_path, file_path="/p/foo.py")
        tracker = CostTracker()
        tracker.set_current_file("/p/foo.py")
        tracker.track("c", "m", 100, 50, 0.001)
        tracker.set_current_file("/p/bar.py")
        tracker.track("c", "m", 9000, 5000, 9.999)  # should not appear in foo.py's row
        row = _build_detail_row(run_dir, "/p/foo.py", tracker.summary().records)
        assert row["input_tokens"] == 100
        assert row["output_tokens"] == 50
        assert row["cost_usd"] == pytest.approx(0.001)

    def test_missing_artifact_gracefully(self, tmp_path):
        """If artifact.txt is missing, row is returned without crashing."""
        run_dir = _make_run_dir(tmp_path, file_path="/p/foo.py")
        (run_dir / "artifact.txt").unlink()
        tracker = _make_tracker("/p/foo.py")
        row = _build_detail_row(run_dir, "/p/foo.py", tracker.summary().records)
        assert row["sha256"] == hashlib.sha256(b"").hexdigest()
        assert row["file_size_bytes"] == 0


# ── _build_summary_row ────────────────────────────────────────────────────────


class TestBuildSummaryRow:
    def _make_detail_rows(self, n: int = 2) -> list[dict]:
        return [
            {
                "filename": f"/p/file{i}.py",
                "sha256": "abc",
                "file_size_bytes": 100 * (i + 1),
                "file_token_estimate": 25 * (i + 1),
                "analysis_start": "2026-03-09T10:00:00+00:00",
                "analysis_end": "2026-03-09T10:00:05+00:00",
                "duration_seconds": 5.0,
                "input_tokens": 100,
                "output_tokens": 50,
                "tokens_per_second": 10.0,
                "models_used": "claude-sonnet-4",
                "verdict": "PASS" if i % 2 == 0 else "REJECT",
                "finding_count": i * 2,
                "cost_usd": 0.001 * (i + 1),
            }
            for i in range(n)
        ]

    def test_correct_columns(self):
        rows = self._make_detail_rows(2)
        tracker = _make_tracker("/p/file0.py")
        summary = _build_summary_row(rows, tracker.summary().records, _T0, _T1)
        assert set(summary.keys()) == set(SUMMARY_COLUMNS)

    def test_total_files(self):
        rows = self._make_detail_rows(3)
        tracker = _make_tracker("/p/file0.py")
        summary = _build_summary_row(rows, tracker.summary().records, _T0, _T1)
        assert summary["total_files"] == 3

    def test_total_size_bytes(self):
        rows = self._make_detail_rows(3)
        expected = sum(r["file_size_bytes"] for r in rows)
        tracker = _make_tracker("/p/file0.py")
        summary = _build_summary_row(rows, tracker.summary().records, _T0, _T1)
        assert summary["total_size_bytes"] == expected

    def test_total_token_estimate(self):
        rows = self._make_detail_rows(3)
        expected = sum(r["file_token_estimate"] for r in rows)
        tracker = _make_tracker("/p/file0.py")
        summary = _build_summary_row(rows, tracker.summary().records, _T0, _T1)
        assert summary["total_token_estimate"] == expected

    def test_run_duration_seconds(self):
        rows = self._make_detail_rows(1)
        tracker = _make_tracker("/p/file0.py")
        summary = _build_summary_row(rows, tracker.summary().records, _T0, _T1)
        assert summary["run_duration_seconds"] == pytest.approx(60.0)

    def test_total_tokens(self):
        rows = self._make_detail_rows(2)
        tracker = _make_tracker("/p/file0.py")
        summary = _build_summary_row(rows, tracker.summary().records, _T0, _T1)
        assert summary["total_input_tokens"] == 200
        assert summary["total_output_tokens"] == 100

    def test_pass_fail_counts(self):
        rows = self._make_detail_rows(4)  # indices 0,2 → PASS; 1,3 → REJECT
        tracker = _make_tracker("/p/file0.py")
        summary = _build_summary_row(rows, tracker.summary().records, _T0, _T1)
        assert summary["pass_count"] == 2
        assert summary["fail_count"] == 2

    def test_pass_with_notes_counts_as_pass(self):
        rows = [
            {**self._make_detail_rows(1)[0], "verdict": "PASS_WITH_NOTES"},
        ]
        tracker = _make_tracker("/p/file0.py")
        summary = _build_summary_row(rows, tracker.summary().records, _T0, _T1)
        assert summary["pass_count"] == 1
        assert summary["fail_count"] == 0

    def test_cost_by_model_json(self):
        tracker = CostTracker()
        tracker.set_current_file("/p/a.py")
        tracker.track("c", "model-a", 100, 50, 0.001)
        tracker.track("c", "model-b", 100, 50, 0.002)
        rows = self._make_detail_rows(1)
        summary = _build_summary_row(rows, tracker.summary().records, _T0, _T1)
        cost_by_model = json.loads(summary["cost_by_model"])
        assert "model-a" in cost_by_model
        assert "model-b" in cost_by_model
        assert cost_by_model["model-a"] == pytest.approx(0.001)
        assert cost_by_model["model-b"] == pytest.approx(0.002)

    def test_total_critic_calls(self):
        tracker = CostTracker()
        tracker.set_current_file("/p/a.py")
        for i in range(5):
            tracker.track(f"c{i}", "m", 100, 50, 0.001)
        rows = self._make_detail_rows(1)
        summary = _build_summary_row(rows, tracker.summary().records, _T0, _T1)
        assert summary["total_critic_calls"] == 5

    def test_avg_tokens_per_second(self):
        rows = [
            {**self._make_detail_rows(1)[0], "tokens_per_second": 10.0},
            {**self._make_detail_rows(1)[0], "tokens_per_second": 20.0},
        ]
        tracker = _make_tracker("/p/file0.py")
        summary = _build_summary_row(rows, tracker.summary().records, _T0, _T1)
        assert summary["avg_tokens_per_second"] == pytest.approx(15.0)

    def test_median_tokens_per_second(self):
        rows = [
            {**self._make_detail_rows(1)[0], "tokens_per_second": 10.0},
            {**self._make_detail_rows(1)[0], "tokens_per_second": 20.0},
            {**self._make_detail_rows(1)[0], "tokens_per_second": 30.0},
        ]
        tracker = _make_tracker("/p/file0.py")
        summary = _build_summary_row(rows, tracker.summary().records, _T0, _T1)
        assert summary["median_tokens_per_second"] == pytest.approx(20.0)

    def test_models_used_all_unique(self):
        tracker = CostTracker()
        tracker.set_current_file("/p/a.py")
        tracker.track("c1", "model-x", 100, 50, 0.001)
        tracker.track("c2", "model-x", 100, 50, 0.001)  # duplicate
        tracker.track("c3", "model-y", 100, 50, 0.001)
        rows = self._make_detail_rows(1)
        summary = _build_summary_row(rows, tracker.summary().records, _T0, _T1)
        models = summary["models_used"].split(",")
        assert sorted(models) == ["model-x", "model-y"]

    def test_empty_files_zero_values(self):
        tracker = _make_tracker("/p/a.py", calls=[])
        summary = _build_summary_row([], tracker.summary().records, _T0, _T1)
        assert summary["total_files"] == 0
        assert summary["total_size_bytes"] == 0
        assert summary["total_input_tokens"] == 0
        assert summary["pass_count"] == 0
        assert summary["fail_count"] == 0
        assert summary["avg_tokens_per_second"] == 0.0
        assert summary["median_tokens_per_second"] == 0.0


# ── generate_audit_reports ────────────────────────────────────────────────────


class TestGenerateAuditReports:
    def test_files_are_created(self, tmp_path):
        run_dir = _make_run_dir(tmp_path, file_path="/p/foo.py")
        tracker = _make_tracker("/p/foo.py")
        detail, summary = generate_audit_reports(run_dir, "/p/foo.py", tracker, _T0, _T1)
        assert detail.exists()
        assert summary.exists()

    def test_detail_csv_has_header_and_one_data_row(self, tmp_path):
        run_dir = _make_run_dir(tmp_path, file_path="/p/foo.py")
        tracker = _make_tracker("/p/foo.py")
        detail, _ = generate_audit_reports(run_dir, "/p/foo.py", tracker, _T0, _T1)
        with open(detail, newline="", encoding="utf-8") as f:
            reader = list(csv.DictReader(f))
        assert len(reader) == 1

    def test_detail_csv_all_columns_present(self, tmp_path):
        run_dir = _make_run_dir(tmp_path, file_path="/p/foo.py")
        tracker = _make_tracker("/p/foo.py")
        detail, _ = generate_audit_reports(run_dir, "/p/foo.py", tracker, _T0, _T1)
        with open(detail, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            assert list(reader.fieldnames) == DETAIL_COLUMNS

    def test_summary_csv_has_header_and_one_data_row(self, tmp_path):
        run_dir = _make_run_dir(tmp_path, file_path="/p/foo.py")
        tracker = _make_tracker("/p/foo.py")
        _, summary = generate_audit_reports(run_dir, "/p/foo.py", tracker, _T0, _T1)
        with open(summary, newline="", encoding="utf-8") as f:
            reader = list(csv.DictReader(f))
        assert len(reader) == 1

    def test_summary_csv_all_columns_present(self, tmp_path):
        run_dir = _make_run_dir(tmp_path, file_path="/p/foo.py")
        tracker = _make_tracker("/p/foo.py")
        _, summary = generate_audit_reports(run_dir, "/p/foo.py", tracker, _T0, _T1)
        with open(summary, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            assert list(reader.fieldnames) == SUMMARY_COLUMNS

    def test_sha256_round_trip(self, tmp_path):
        artifact_text = "content to hash\n"
        run_dir = _make_run_dir(tmp_path, file_path="/p/foo.py", artifact_text=artifact_text)
        tracker = _make_tracker("/p/foo.py")
        detail, _ = generate_audit_reports(run_dir, "/p/foo.py", tracker, _T0, _T1)
        with open(detail, newline="", encoding="utf-8") as f:
            row = next(csv.DictReader(f))
        expected = hashlib.sha256(artifact_text.encode("utf-8")).hexdigest()
        assert row["sha256"] == expected

    def test_csv_round_trip_parseable(self, tmp_path):
        run_dir = _make_run_dir(tmp_path, file_path="/p/foo.py", finding_count=3)
        tracker = _make_tracker("/p/foo.py")
        detail, summary = generate_audit_reports(run_dir, "/p/foo.py", tracker, _T0, _T1)

        # Detail round-trip
        with open(detail, newline="", encoding="utf-8") as f:
            rows = list(csv.DictReader(f))
        assert len(rows) == 1
        assert rows[0]["verdict"] == "PASS"
        assert rows[0]["finding_count"] == "3"

        # Summary round-trip
        with open(summary, newline="", encoding="utf-8") as f:
            srows = list(csv.DictReader(f))
        assert len(srows) == 1
        assert srows[0]["total_files"] == "1"

    def test_numeric_fields_not_quoted(self, tmp_path):
        """Numeric values in CSVs must not be quoted."""
        run_dir = _make_run_dir(tmp_path, file_path="/p/foo.py")
        tracker = _make_tracker("/p/foo.py", calls=[
            ("c", "m", 500, 200, 0.005),
        ])
        detail, summary = generate_audit_reports(run_dir, "/p/foo.py", tracker, _T0, _T1)

        raw_detail = detail.read_text(encoding="utf-8")
        # file_size_bytes value should appear unquoted
        lines = raw_detail.splitlines()
        data_line = lines[1]
        # Numeric values should not be surrounded by quotes
        # Split by comma and check that size/token fields look like plain numbers
        fields = data_line.split(",")
        # file_size_bytes is column index 2 (0-indexed): filename, sha256, file_size_bytes
        file_size_field = fields[2]
        assert not file_size_field.startswith('"'), f"file_size_bytes was quoted: {file_size_field!r}"

    def test_cost_by_model_json_is_quoted(self, tmp_path):
        """cost_by_model JSON string with commas must be quoted in the CSV."""
        run_dir = _make_run_dir(tmp_path, file_path="/p/foo.py")
        tracker = CostTracker()
        tracker.set_current_file("/p/foo.py")
        tracker.track("c1", "model-a", 100, 50, 0.001)
        tracker.track("c2", "model-b", 100, 50, 0.002)
        _, summary = generate_audit_reports(run_dir, "/p/foo.py", tracker, _T0, _T1)

        raw = summary.read_text(encoding="utf-8")
        # cost_by_model JSON must be parseable after round-trip
        with open(summary, newline="", encoding="utf-8") as f:
            srow = next(csv.DictReader(f))
        cost_by_model = json.loads(srow["cost_by_model"])
        assert isinstance(cost_by_model, dict)
        assert len(cost_by_model) == 2

    def test_zero_findings(self, tmp_path):
        run_dir = _make_run_dir(tmp_path, file_path="/p/foo.py", finding_count=0, verdict_status="PASS")
        tracker = _make_tracker("/p/foo.py")
        detail, summary = generate_audit_reports(run_dir, "/p/foo.py", tracker, _T0, _T1)
        with open(detail, newline="", encoding="utf-8") as f:
            row = next(csv.DictReader(f))
        assert row["finding_count"] == "0"
        assert row["verdict"] == "PASS"
        with open(summary, newline="", encoding="utf-8") as f:
            srow = next(csv.DictReader(f))
        assert srow["pass_count"] == "1"
        assert srow["fail_count"] == "0"

    def test_many_findings(self, tmp_path):
        run_dir = _make_run_dir(tmp_path, file_path="/p/foo.py", finding_count=42, verdict_status="REJECT")
        tracker = _make_tracker("/p/foo.py")
        detail, _ = generate_audit_reports(run_dir, "/p/foo.py", tracker, _T0, _T1)
        with open(detail, newline="", encoding="utf-8") as f:
            row = next(csv.DictReader(f))
        assert row["finding_count"] == "42"
        assert row["verdict"] == "REJECT"

    def test_summary_aggregates_correct_single_file(self, tmp_path):
        run_dir = _make_run_dir(
            tmp_path, file_path="/p/foo.py",
            started_at="2026-03-09T10:00:00+00:00",
            completed_at="2026-03-09T10:00:10+00:00",
        )
        tracker = _make_tracker("/p/foo.py", calls=[
            ("c1", "model-x", 400, 100, 0.002),
            ("c2", "model-x", 600, 200, 0.004),
        ])
        _, summary = generate_audit_reports(run_dir, "/p/foo.py", tracker, _T0, _T1)
        with open(summary, newline="", encoding="utf-8") as f:
            srow = next(csv.DictReader(f))
        assert srow["total_files"] == "1"
        assert srow["total_input_tokens"] == "1000"  # 400 + 600
        assert srow["total_output_tokens"] == "300"  # 100 + 200
        assert float(srow["total_cost_usd"]) == pytest.approx(0.006)
        assert srow["total_critic_calls"] == "2"


# ── generate_batch_audit_reports ─────────────────────────────────────────────


class TestGenerateBatchAuditReports:
    def _make_file_result(self, tmp_path: Path, name: str, verdict: str = "PASS", findings: int = 0) -> FileResult:
        file_path = f"/project/{name}"
        sub = tmp_path / name.replace("/", "_").replace(".", "_")
        sub.mkdir(exist_ok=True)
        run_dir = _make_run_dir(sub, file_path=file_path, verdict_status=verdict, finding_count=findings)
        return FileResult(
            file_path=file_path,
            verdict=Verdict(
                status=VerdictStatus(verdict),
                reasoning="test",
                confidence=0.9,
            ),
            run_dir=str(run_dir),
        )

    def test_files_are_created(self, tmp_path):
        batch_dir = tmp_path / "batch"
        batch_dir.mkdir()
        fr1 = self._make_file_result(tmp_path, "a.py", "PASS")
        fr2 = self._make_file_result(tmp_path, "b.py", "REJECT", findings=2)
        tracker = CostTracker()
        tracker.set_current_file("/project/a.py")
        tracker.track("c", "m", 100, 50, 0.001)
        tracker.set_current_file("/project/b.py")
        tracker.track("c", "m", 200, 100, 0.002)
        detail, summary = generate_batch_audit_reports(batch_dir, [fr1, fr2], tracker, _T0, _T1)
        assert detail.exists()
        assert summary.exists()

    def test_detail_row_count_matches_files(self, tmp_path):
        batch_dir = tmp_path / "batch"
        batch_dir.mkdir()
        results = [self._make_file_result(tmp_path, f"f{i}.py") for i in range(4)]
        tracker = CostTracker()
        detail, _ = generate_batch_audit_reports(batch_dir, results, tracker, _T0, _T1)
        with open(detail, newline="", encoding="utf-8") as f:
            rows = list(csv.DictReader(f))
        assert len(rows) == 4

    def test_summary_aggregates_across_files(self, tmp_path):
        batch_dir = tmp_path / "batch"
        batch_dir.mkdir()
        fr1 = self._make_file_result(tmp_path, "a.py", "PASS")
        fr2 = self._make_file_result(tmp_path, "b.py", "REJECT", findings=5)
        tracker = CostTracker()
        tracker.set_current_file("/project/a.py")
        tracker.track("c", "model-a", 300, 100, 0.001)
        tracker.set_current_file("/project/b.py")
        tracker.track("c", "model-b", 700, 300, 0.003)
        _, summary = generate_batch_audit_reports(batch_dir, [fr1, fr2], tracker, _T0, _T1)
        with open(summary, newline="", encoding="utf-8") as f:
            srow = next(csv.DictReader(f))
        assert srow["total_files"] == "2"
        assert srow["total_input_tokens"] == "1000"
        assert srow["total_output_tokens"] == "400"
        assert float(srow["total_cost_usd"]) == pytest.approx(0.004)
        assert srow["pass_count"] == "1"
        assert srow["fail_count"] == "1"
        assert srow["total_critic_calls"] == "2"

    def test_csv_parseable_round_trip(self, tmp_path):
        batch_dir = tmp_path / "batch"
        batch_dir.mkdir()
        fr = self._make_file_result(tmp_path, "x.py", "PASS_WITH_NOTES", findings=1)
        tracker = _make_tracker("/project/x.py")
        detail, summary = generate_batch_audit_reports(batch_dir, [fr], tracker, _T0, _T1)
        with open(detail, newline="", encoding="utf-8") as f:
            rows = list(csv.DictReader(f))
        assert rows[0]["verdict"] == "PASS_WITH_NOTES"
        with open(summary, newline="", encoding="utf-8") as f:
            srows = list(csv.DictReader(f))
        assert srows[0]["pass_count"] == "1"

    def test_empty_results(self, tmp_path):
        batch_dir = tmp_path / "batch"
        batch_dir.mkdir()
        tracker = CostTracker()
        detail, summary = generate_batch_audit_reports(batch_dir, [], tracker, _T0, _T1)
        with open(detail, newline="", encoding="utf-8") as f:
            rows = list(csv.DictReader(f))
        assert len(rows) == 0
        with open(summary, newline="", encoding="utf-8") as f:
            srow = next(csv.DictReader(f))
        assert srow["total_files"] == "0"


# ── CLI --audit-report flag ───────────────────────────────────────────────────


class TestCLIAuditReportFlag:
    def test_flag_in_help(self):
        from click.testing import CliRunner
        from quorum.cli import cli
        runner = CliRunner()
        result = runner.invoke(cli, ["run", "--help"])
        assert result.exit_code == 0
        assert "audit-report" in result.output

    def _invoke_run(self, runner, cli, artifact, extra_args=None):
        """Invoke 'quorum run' with all side-effect functions mocked out."""
        mock_verdict = MagicMock()
        mock_verdict.status.value = "PASS"
        mock_verdict.is_actionable = False
        mock_verdict.report = None
        run_dir = artifact.parent

        # run_validation and print_verdict are imported inside run_cmd body,
        # so patch at their source modules.
        with patch("quorum.pipeline.run_validation", return_value=(mock_verdict, run_dir)) as mock_run, \
             patch("quorum.cli._has_api_key", return_value=True), \
             patch("quorum.output.print_verdict"), \
             patch("quorum.cli._print_run_cost_summary"), \
             patch("quorum.cli._print_fix_loop_summary"), \
             patch("quorum.cli._print_learning_summary"), \
             patch("quorum.cli._print_audit_report_path"):
            args = ["run", "--target", str(artifact)] + (extra_args or [])
            runner.invoke(cli, args)
        return mock_run

    def test_auto_enable_at_thorough_depth(self, tmp_path):
        """run_validation should be called with audit_report=True when depth=thorough."""
        from click.testing import CliRunner
        from quorum.cli import cli

        artifact = tmp_path / "test.py"
        artifact.write_text("x = 1\n", encoding="utf-8")

        runner = CliRunner()
        mock_run = self._invoke_run(runner, cli, artifact, ["--depth", "thorough"])
        call_kwargs = mock_run.call_args[1]
        assert call_kwargs.get("audit_report") is True

    def test_explicit_flag_passes_through(self, tmp_path):
        """--audit-report flag should enable audit_report=True even at quick depth."""
        from click.testing import CliRunner
        from quorum.cli import cli

        artifact = tmp_path / "test.py"
        artifact.write_text("x = 1\n", encoding="utf-8")

        runner = CliRunner()
        mock_run = self._invoke_run(runner, cli, artifact, ["--depth", "quick", "--audit-report"])
        call_kwargs = mock_run.call_args[1]
        assert call_kwargs.get("audit_report") is True

    def test_no_flag_at_quick_depth_disabled(self, tmp_path):
        """Without --audit-report and not at thorough depth, audit_report should be False."""
        from click.testing import CliRunner
        from quorum.cli import cli

        artifact = tmp_path / "test.py"
        artifact.write_text("x = 1\n", encoding="utf-8")

        runner = CliRunner()
        mock_run = self._invoke_run(runner, cli, artifact, ["--depth", "quick"])
        call_kwargs = mock_run.call_args[1]
        assert call_kwargs.get("audit_report") is False


# ── pipeline integration (mocked) ────────────────────────────────────────────


class TestPipelineAuditIntegration:
    def test_run_validation_generates_audit_files(self, tmp_path):
        """run_validation with audit_report=True should produce CSV files."""
        from quorum.config import QuorumConfig
        from quorum.models import AggregatedReport, CriticResult, Verdict, VerdictStatus
        from quorum.pipeline import run_validation

        artifact = tmp_path / "test.py"
        artifact.write_text("def foo(): pass\n", encoding="utf-8")

        config = QuorumConfig(
            critics=["correctness"],
            model_tier1="claude-sonnet-4",
            model_tier2="claude-sonnet-4",
        )

        mock_critic_result = CriticResult(
            critic_name="correctness", findings=[], confidence=0.9, runtime_ms=10
        )
        mock_verdict = Verdict(
            status=VerdictStatus.PASS,
            reasoning="All good",
            confidence=0.9,
            report=AggregatedReport(findings=[], confidence=0.9),
        )

        with patch("quorum.pipeline.SupervisorAgent") as MockSupervisor, \
             patch("quorum.pipeline.AggregatorAgent") as MockAggregator, \
             patch("quorum.pipeline.LiteLLMProvider"), \
             patch("quorum.pipeline.LearningMemory"):
            MockSupervisor.return_value.run.return_value = [mock_critic_result]
            MockSupervisor.return_value.classify_domain.return_value = "python"
            MockAggregator.return_value.run.return_value = mock_verdict

            _, run_dir = run_validation(
                target_path=artifact,
                config=config,
                runs_dir=tmp_path / "runs",
                enable_learning=False,
                audit_report=True,
            )

        assert (run_dir / "audit-detail.csv").exists()
        assert (run_dir / "audit-summary.csv").exists()

    def test_run_validation_no_audit_by_default(self, tmp_path):
        """run_validation without audit_report should NOT produce CSV files."""
        from quorum.config import QuorumConfig
        from quorum.models import AggregatedReport, CriticResult, Verdict, VerdictStatus
        from quorum.pipeline import run_validation

        artifact = tmp_path / "test.py"
        artifact.write_text("def foo(): pass\n", encoding="utf-8")

        config = QuorumConfig(
            critics=["correctness"],
            model_tier1="claude-sonnet-4",
            model_tier2="claude-sonnet-4",
        )

        mock_critic_result = CriticResult(
            critic_name="correctness", findings=[], confidence=0.9, runtime_ms=10
        )
        mock_verdict = Verdict(
            status=VerdictStatus.PASS,
            reasoning="All good",
            confidence=0.9,
            report=AggregatedReport(findings=[], confidence=0.9),
        )

        with patch("quorum.pipeline.SupervisorAgent") as MockSupervisor, \
             patch("quorum.pipeline.AggregatorAgent") as MockAggregator, \
             patch("quorum.pipeline.LiteLLMProvider"), \
             patch("quorum.pipeline.LearningMemory"):
            MockSupervisor.return_value.run.return_value = [mock_critic_result]
            MockSupervisor.return_value.classify_domain.return_value = "python"
            MockAggregator.return_value.run.return_value = mock_verdict

            _, run_dir = run_validation(
                target_path=artifact,
                config=config,
                runs_dir=tmp_path / "runs",
                enable_learning=False,
                audit_report=False,
            )

        assert not (run_dir / "audit-detail.csv").exists()
        assert not (run_dir / "audit-summary.csv").exists()

    def test_artifact_sha256_in_manifest(self, tmp_path):
        """run_validation should write artifact_sha256 to run-manifest.json."""
        from quorum.config import QuorumConfig
        from quorum.models import AggregatedReport, CriticResult, Verdict, VerdictStatus
        from quorum.pipeline import run_validation

        content = "def bar(): return 42\n"
        artifact = tmp_path / "bar.py"
        artifact.write_text(content, encoding="utf-8")

        config = QuorumConfig(
            critics=["correctness"],
            model_tier1="claude-sonnet-4",
            model_tier2="claude-sonnet-4",
        )

        mock_critic_result = CriticResult(
            critic_name="correctness", findings=[], confidence=0.9, runtime_ms=10
        )
        mock_verdict = Verdict(
            status=VerdictStatus.PASS,
            reasoning="All good",
            confidence=0.9,
            report=AggregatedReport(findings=[], confidence=0.9),
        )

        with patch("quorum.pipeline.SupervisorAgent") as MockSupervisor, \
             patch("quorum.pipeline.AggregatorAgent") as MockAggregator, \
             patch("quorum.pipeline.LiteLLMProvider"), \
             patch("quorum.pipeline.LearningMemory"):
            MockSupervisor.return_value.run.return_value = [mock_critic_result]
            MockSupervisor.return_value.classify_domain.return_value = "python"
            MockAggregator.return_value.run.return_value = mock_verdict

            _, run_dir = run_validation(
                target_path=artifact,
                config=config,
                runs_dir=tmp_path / "runs",
                enable_learning=False,
            )

        manifest = json.loads((run_dir / "run-manifest.json").read_text())
        expected_sha256 = hashlib.sha256(content.encode("utf-8")).hexdigest()
        assert manifest.get("artifact_sha256") == expected_sha256
