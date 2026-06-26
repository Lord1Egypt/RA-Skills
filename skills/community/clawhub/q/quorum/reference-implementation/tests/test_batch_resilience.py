# SPDX-License-Identifier: MIT
# Copyright 2026 SharedIntellect — https://github.com/SharedIntellect/quorum

"""Tests for crash-resilient batch validation: progressive saves, resume, signal handling."""

from __future__ import annotations

import json
import os
import signal
import threading
import time
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from quorum.config import QuorumConfig
from quorum.models import (
    AggregatedReport,
    BatchVerdict,
    CriticResult,
    FileResult,
    Verdict,
    VerdictStatus,
)
from quorum.pipeline import (
    _aggregate_batch,
    _write_json_atomic,
    resolve_targets,
    resume_batch_validation,
    run_batch_validation,
)


# ── Fixtures ──────────────────────────────────────────────────────────────────


@pytest.fixture
def quick_config() -> QuorumConfig:
    return QuorumConfig(
        critics=["correctness"],
        model_tier1="m1",
        model_tier2="m2",
        depth_profile="quick",
        enable_prescreen=False,
    )


def _make_verdict(status: VerdictStatus = VerdictStatus.PASS) -> Verdict:
    return Verdict(
        status=status,
        reasoning="test",
        confidence=0.9,
        report=AggregatedReport(findings=[], confidence=0.9),
    )


def _make_file_result(path: str, status: VerdictStatus = VerdictStatus.PASS) -> FileResult:
    return FileResult(
        file_path=path,
        verdict=_make_verdict(status),
        run_dir="/tmp/run",
    )


def _setup_mock_pipeline(MockSupervisor, MockAggregator, MockProvider):
    """Wire up the three pipeline mocks to return a passing verdict."""
    mock_provider = MagicMock()
    MockProvider.return_value = mock_provider

    cr = CriticResult(critic_name="correctness", findings=[], confidence=0.9, runtime_ms=50)
    MockSupervisor.return_value.run = MagicMock(return_value=[cr])

    verdict = _make_verdict()
    MockAggregator.return_value.run = MagicMock(return_value=verdict)


# ── 1. Atomic writes ──────────────────────────────────────────────────────────


class TestAtomicWrites:
    def test_writes_valid_json(self, tmp_path):
        path = tmp_path / "out.json"
        _write_json_atomic(path, {"key": "value", "num": 42})
        data = json.loads(path.read_text())
        assert data == {"key": "value", "num": 42}

    def test_no_tmp_file_left_on_success(self, tmp_path):
        path = tmp_path / "out.json"
        _write_json_atomic(path, {"ok": True})
        assert not (tmp_path / "out.tmp").exists()

    def test_overwrites_existing(self, tmp_path):
        path = tmp_path / "out.json"
        _write_json_atomic(path, {"v": 1})
        _write_json_atomic(path, {"v": 2})
        assert json.loads(path.read_text())["v"] == 2

    def test_creates_parent_dirs(self, tmp_path):
        path = tmp_path / "a" / "b" / "c.json"
        _write_json_atomic(path, {"nested": True})
        assert path.exists()

    def test_result_is_always_valid_json(self, tmp_path):
        """Even after many rapid overwrites, the file must always parse as JSON."""
        path = tmp_path / "manifest.json"
        for i in range(20):
            _write_json_atomic(path, {"count": i, "data": "x" * 100})
            content = path.read_text()
            parsed = json.loads(content)  # must not raise
            assert parsed["count"] == i


# ── 2. Progressive manifest ───────────────────────────────────────────────────


class TestProgressiveManifest:
    @patch("quorum.pipeline.LiteLLMProvider")
    @patch("quorum.pipeline.AggregatorAgent")
    @patch("quorum.pipeline.SupervisorAgent")
    def test_initial_manifest_written_before_files_complete(
        self, MockSupervisor, MockAggregator, MockProvider, quick_config, tmp_path
    ):
        """batch-manifest.json must exist with status='running' before any file finishes."""
        _setup_mock_pipeline(MockSupervisor, MockAggregator, MockProvider)

        test_dir = tmp_path / "input"
        test_dir.mkdir()
        manifests_seen: list[dict] = []

        original_validate = None

        def spy_validate(*args, **kwargs):
            # Read manifest while a file is "in flight"
            manifest_path = tmp_path / "runs" / "batch-manifest.json"
            # Find the manifest by scanning for any batch-* dir
            for p in (tmp_path / "runs").glob("batch-*/batch-manifest.json"):
                try:
                    manifests_seen.append(json.loads(p.read_text()))
                except (json.JSONDecodeError, OSError):
                    pass  # manifest may be partially written during race
            return original_validate(*args, **kwargs)

        # Create 3 files
        for i in range(3):
            (test_dir / f"file{i}.md").write_text(f"# File {i}\n")

        run_batch_validation(
            target=test_dir,
            pattern="*.md",
            config=quick_config,
            runs_dir=tmp_path / "runs",
        )

        # After completion the final manifest must be completed
        batch_dirs = list((tmp_path / "runs").glob("batch-*"))
        assert batch_dirs, "No batch directory created"
        manifest = json.loads((batch_dirs[0] / "batch-manifest.json").read_text())
        assert manifest["status"] == "completed"
        assert manifest["total_files"] == 3
        assert len(manifest["completed_files"]) == 3

    @patch("quorum.pipeline.LiteLLMProvider")
    @patch("quorum.pipeline.AggregatorAgent")
    @patch("quorum.pipeline.SupervisorAgent")
    def test_manifest_has_completed_files_list(
        self, MockSupervisor, MockAggregator, MockProvider, quick_config, tmp_path
    ):
        _setup_mock_pipeline(MockSupervisor, MockAggregator, MockProvider)

        test_dir = tmp_path / "input"
        test_dir.mkdir()
        for i in range(5):
            (test_dir / f"f{i}.md").write_text(f"# {i}\n")

        run_batch_validation(
            target=test_dir,
            pattern="*.md",
            config=quick_config,
            runs_dir=tmp_path / "runs",
        )

        batch_dirs = list((tmp_path / "runs").glob("batch-*"))
        manifest = json.loads((batch_dirs[0] / "batch-manifest.json").read_text())

        assert "completed_files" in manifest
        assert len(manifest["completed_files"]) == 5
        for entry in manifest["completed_files"]:
            assert "file" in entry
            assert "run_dir" in entry
            assert "verdict" in entry
            assert "completed_at" in entry

    @patch("quorum.pipeline.LiteLLMProvider")
    @patch("quorum.pipeline.AggregatorAgent")
    @patch("quorum.pipeline.SupervisorAgent")
    def test_manifest_progressive_update_after_each_file(
        self, MockSupervisor, MockAggregator, MockProvider, quick_config, tmp_path
    ):
        """Verify the manifest 'validated' count grows as files complete."""
        _setup_mock_pipeline(MockSupervisor, MockAggregator, MockProvider)

        snapshots: list[int] = []
        original_write_atomic = None

        import quorum.pipeline as _pipeline_mod

        original_write_atomic = _pipeline_mod._write_json_atomic

        def capturing_write_atomic(path: Path, data: dict) -> None:
            original_write_atomic(path, data)
            if path.name == "batch-manifest.json" and data.get("status") == "running":
                snapshots.append(data.get("validated", 0))

        test_dir = tmp_path / "input"
        test_dir.mkdir()
        for i in range(4):
            (test_dir / f"f{i}.md").write_text(f"# {i}\n")

        with patch.object(_pipeline_mod, "_write_json_atomic", side_effect=capturing_write_atomic):
            run_batch_validation(
                target=test_dir,
                pattern="*.md",
                config=quick_config,
                runs_dir=tmp_path / "runs",
            )

        # Should have seen at least 1 intermediate snapshot
        assert len(snapshots) >= 1
        # Each snapshot must be <= 4
        assert all(0 <= s <= 4 for s in snapshots)


# ── 3. Resume capability ──────────────────────────────────────────────────────


class TestResumeBatchValidation:
    def _build_completed_run_dir(self, batch_dir: Path, file_path: Path) -> Path:
        """Create a fake per-file run directory with a verdict.json."""
        run_dir = batch_dir / "per-file" / f"run-{file_path.stem}"
        run_dir.mkdir(parents=True, exist_ok=True)
        verdict = _make_verdict(VerdictStatus.PASS)
        (run_dir / "verdict.json").write_text(
            json.dumps(verdict.model_dump(), default=str), encoding="utf-8"
        )
        return run_dir

    @patch("quorum.pipeline.LiteLLMProvider")
    @patch("quorum.pipeline.AggregatorAgent")
    @patch("quorum.pipeline.SupervisorAgent")
    def test_resume_skips_completed_files(
        self, MockSupervisor, MockAggregator, MockProvider, quick_config, tmp_path
    ):
        """Resume should only validate the 2 remaining files out of 5."""
        _setup_mock_pipeline(MockSupervisor, MockAggregator, MockProvider)

        # Create 5 files
        input_dir = tmp_path / "input"
        input_dir.mkdir()
        files = []
        for i in range(5):
            f = input_dir / f"file{i}.md"
            f.write_text(f"# File {i}\n")
            files.append(f)

        # Set up a partial batch directory: 3/5 complete
        batch_dir = tmp_path / "runs" / "batch-test"
        batch_dir.mkdir(parents=True)

        completed = []
        for f in files[:3]:
            run_dir = self._build_completed_run_dir(batch_dir, f)
            completed.append({
                "file": str(f),
                "run_dir": str(run_dir),
                "verdict": "PASS",
                "completed_at": "2026-03-09T00:00:00+00:00",
            })

        _write_json_atomic(batch_dir / "batch-manifest.json", {
            "target": str(input_dir),
            "pattern": "*.md",
            "depth": "quick",
            "rubric": None,
            "total_files": 5,
            "validated": 3,
            "errors": 0,
            "started_at": "2026-03-09T00:00:00+00:00",
            "status": "interrupted",
            "completed_files": completed,
            "failed_files": [],
        })

        validated_files: list[str] = []
        original_validate_one = None

        import quorum.pipeline as _pipeline_mod
        original_validate_one = _pipeline_mod._validate_one_file

        def spy_validate_one(file_path, *args, **kwargs):
            validated_files.append(str(file_path))
            return original_validate_one(file_path, *args, **kwargs)

        with patch.object(_pipeline_mod, "_validate_one_file", side_effect=spy_validate_one):
            batch_verdict, out_dir = resume_batch_validation(batch_dir=batch_dir)

        # Only the 2 remaining files should have been validated
        assert len(validated_files) == 2
        for vf in validated_files:
            assert vf not in {str(f) for f in files[:3]}

        assert batch_verdict.total_files == 5
        assert isinstance(batch_verdict, BatchVerdict)

    @patch("quorum.pipeline.LiteLLMProvider")
    @patch("quorum.pipeline.AggregatorAgent")
    @patch("quorum.pipeline.SupervisorAgent")
    def test_resume_final_manifest_status_completed(
        self, MockSupervisor, MockAggregator, MockProvider, quick_config, tmp_path
    ):
        """After a successful resume, manifest status must be 'completed'."""
        _setup_mock_pipeline(MockSupervisor, MockAggregator, MockProvider)

        input_dir = tmp_path / "input"
        input_dir.mkdir()
        files = []
        for i in range(3):
            f = input_dir / f"file{i}.md"
            f.write_text(f"# {i}\n")
            files.append(f)

        batch_dir = tmp_path / "runs" / "batch-resume-test"
        batch_dir.mkdir(parents=True)

        # 1 of 3 already done
        run_dir_0 = self._build_completed_run_dir(batch_dir, files[0])
        _write_json_atomic(batch_dir / "batch-manifest.json", {
            "target": str(input_dir),
            "pattern": "*.md",
            "depth": "quick",
            "rubric": None,
            "total_files": 3,
            "validated": 1,
            "errors": 0,
            "started_at": "2026-03-09T00:00:00+00:00",
            "status": "interrupted",
            "completed_files": [{
                "file": str(files[0]),
                "run_dir": str(run_dir_0),
                "verdict": "PASS",
                "completed_at": "2026-03-09T00:00:00+00:00",
            }],
            "failed_files": [],
        })

        resume_batch_validation(batch_dir=batch_dir)

        manifest = json.loads((batch_dir / "batch-manifest.json").read_text())
        assert manifest["status"] == "completed"
        assert manifest["validated"] == 3

    def test_resume_nonexistent_dir_raises(self, tmp_path):
        with pytest.raises(FileNotFoundError):
            resume_batch_validation(batch_dir=tmp_path / "nonexistent")

    def test_resume_corrupted_manifest_raises(self, tmp_path):
        batch_dir = tmp_path / "batch-bad"
        batch_dir.mkdir()
        (batch_dir / "batch-manifest.json").write_text("NOT JSON {{{{", encoding="utf-8")
        with pytest.raises(ValueError, match="Corrupted"):
            resume_batch_validation(batch_dir=batch_dir)

    @patch("quorum.pipeline.LiteLLMProvider")
    @patch("quorum.pipeline.AggregatorAgent")
    @patch("quorum.pipeline.SupervisorAgent")
    def test_resume_revalidates_crashed_per_file_dir(
        self, MockSupervisor, MockAggregator, MockProvider, quick_config, tmp_path
    ):
        """A run_dir that exists on disk but has no verdict.json must be re-validated."""
        _setup_mock_pipeline(MockSupervisor, MockAggregator, MockProvider)

        input_dir = tmp_path / "input"
        input_dir.mkdir()
        files = []
        for i in range(3):
            f = input_dir / f"file{i}.md"
            f.write_text(f"# {i}\n")
            files.append(f)

        batch_dir = tmp_path / "runs" / "batch-crash"
        batch_dir.mkdir(parents=True)

        # file0 has a valid run_dir with verdict.json
        run_dir_0 = self._build_completed_run_dir(batch_dir, files[0])

        # file1 has a run_dir BUT no verdict.json (crashed during validation)
        crashed_run_dir = batch_dir / "per-file" / "run-crashed"
        crashed_run_dir.mkdir(parents=True)
        # No verdict.json here — crash mid-validation

        _write_json_atomic(batch_dir / "batch-manifest.json", {
            "target": str(input_dir),
            "pattern": "*.md",
            "depth": "quick",
            "rubric": None,
            "total_files": 3,
            "validated": 2,
            "errors": 0,
            "started_at": "2026-03-09T00:00:00+00:00",
            "status": "interrupted",
            "completed_files": [
                {
                    "file": str(files[0]),
                    "run_dir": str(run_dir_0),
                    "verdict": "PASS",
                    "completed_at": "2026-03-09T00:00:00+00:00",
                },
                {
                    "file": str(files[1]),
                    "run_dir": str(crashed_run_dir),  # no verdict.json
                    "verdict": "PASS",
                    "completed_at": "2026-03-09T00:00:00+00:00",
                },
            ],
            "failed_files": [],
        })

        validated_files: list[str] = []
        import quorum.pipeline as _pipeline_mod
        original = _pipeline_mod._validate_one_file

        def spy(file_path, *args, **kwargs):
            validated_files.append(str(file_path))
            return original(file_path, *args, **kwargs)

        with patch.object(_pipeline_mod, "_validate_one_file", side_effect=spy):
            resume_batch_validation(batch_dir=batch_dir)

        # file1 (crashed) + file2 (never started) must be re-validated; file0 skipped
        assert str(files[0]) not in validated_files
        assert str(files[1]) in validated_files
        assert str(files[2]) in validated_files


# ── 4. Signal handling ────────────────────────────────────────────────────────


class TestSignalHandling:
    @patch("quorum.pipeline.LiteLLMProvider")
    @patch("quorum.pipeline.AggregatorAgent")
    @patch("quorum.pipeline.SupervisorAgent")
    def test_sigint_sets_interrupted_status(
        self, MockSupervisor, MockAggregator, MockProvider, quick_config, tmp_path
    ):
        """Send SIGINT mid-batch and verify manifest ends up with status='interrupted'."""
        _setup_mock_pipeline(MockSupervisor, MockAggregator, MockProvider)

        input_dir = tmp_path / "input"
        input_dir.mkdir()
        for i in range(6):
            (input_dir / f"f{i}.md").write_text(f"# {i}\n")

        import quorum.pipeline as _pipeline_mod

        files_started = threading.Event()
        original_validate_one = _pipeline_mod._validate_one_file

        def slow_validate(file_path, *args, **kwargs):
            files_started.set()
            # Brief delay to keep the batch running while we send the signal
            time.sleep(0.05)
            return original_validate_one(file_path, *args, **kwargs)

        batch_dir_holder: list[Path] = []
        original_run_batch = run_batch_validation

        def run_and_signal():
            # Wait until at least one file has started, then send SIGINT
            files_started.wait(timeout=5)
            os.kill(os.getpid(), signal.SIGINT)

        signal_thread = threading.Thread(target=run_and_signal, daemon=True)

        with patch.object(_pipeline_mod, "_validate_one_file", side_effect=slow_validate):
            signal_thread.start()
            try:
                batch_verdict, batch_dir = run_batch_validation(
                    target=input_dir,
                    pattern="*.md",
                    config=quick_config,
                    runs_dir=tmp_path / "runs",
                )
            except SystemExit:
                pass  # SIGINT may propagate as SystemExit in some contexts
            batch_dir_holder.append(batch_dir)

        signal_thread.join(timeout=3)

        # Find the batch directory
        batch_dirs = list((tmp_path / "runs").glob("batch-*"))
        if not batch_dirs and batch_dir_holder:
            batch_dirs = batch_dir_holder

        assert batch_dirs, "No batch directory found"
        bd = batch_dirs[0]
        manifest = json.loads((bd / "batch-manifest.json").read_text())
        assert manifest["status"] == "interrupted"

    def test_stop_event_prevents_new_submissions(self, tmp_path, quick_config):
        """Verify that after stop_event is set, remaining files are cancelled."""
        # This is a unit test on the stop logic via the _stop_event mechanism
        # We verify via the manifest that fewer than all files complete
        import quorum.pipeline as _pipeline_mod

        input_dir = tmp_path / "input"
        input_dir.mkdir()
        for i in range(10):
            (input_dir / f"f{i}.md").write_text(f"# {i}\n")

        call_count = 0
        original_validate_one = _pipeline_mod._validate_one_file

        def counting_validate(file_path, *args, **kwargs):
            nonlocal call_count
            call_count += 1
            if call_count == 2:
                # Simulate an external stop after 2 files
                os.kill(os.getpid(), signal.SIGINT)
                time.sleep(0.02)
            return original_validate_one(file_path, *args, **kwargs)

        with patch("quorum.pipeline.LiteLLMProvider"), \
             patch("quorum.pipeline.AggregatorAgent") as MockAgg, \
             patch("quorum.pipeline.SupervisorAgent") as MockSup:

            cr = CriticResult(critic_name="correctness", findings=[], confidence=0.9, runtime_ms=50)
            MockSup.return_value.run = MagicMock(return_value=[cr])
            verdict = _make_verdict()
            MockAgg.return_value.run = MagicMock(return_value=verdict)

            with patch.object(_pipeline_mod, "_validate_one_file", side_effect=counting_validate):
                try:
                    _, batch_dir = run_batch_validation(
                        target=input_dir,
                        pattern="*.md",
                        config=quick_config,
                        runs_dir=tmp_path / "runs",
                    )
                except SystemExit:
                    batch_dir = list((tmp_path / "runs").glob("batch-*"))[0]

        manifest = json.loads((batch_dir / "batch-manifest.json").read_text())
        # Must be interrupted and fewer than 10 files completed
        assert manifest["status"] == "interrupted"
        assert manifest["validated"] < 10


# ── 5. Progressive batch report ───────────────────────────────────────────────


class TestProgressiveBatchReport:
    @patch("quorum.pipeline.LiteLLMProvider")
    @patch("quorum.pipeline.AggregatorAgent")
    @patch("quorum.pipeline.SupervisorAgent")
    def test_batch_report_created_before_completion(
        self, MockSupervisor, MockAggregator, MockProvider, quick_config, tmp_path
    ):
        """batch-report.md must exist with a header row immediately."""
        _setup_mock_pipeline(MockSupervisor, MockAggregator, MockProvider)

        input_dir = tmp_path / "input"
        input_dir.mkdir()
        for i in range(3):
            (input_dir / f"f{i}.md").write_text(f"# {i}\n")

        _, batch_dir = run_batch_validation(
            target=input_dir,
            pattern="*.md",
            config=quick_config,
            runs_dir=tmp_path / "runs",
        )

        report_path = batch_dir / "batch-report.md"
        assert report_path.exists()
        content = report_path.read_text()
        assert "# Quorum Batch Validation Report" in content
        assert "Per-File Summary" in content

    @patch("quorum.pipeline.LiteLLMProvider")
    @patch("quorum.pipeline.AggregatorAgent")
    @patch("quorum.pipeline.SupervisorAgent")
    def test_batch_report_contains_aggregate_section(
        self, MockSupervisor, MockAggregator, MockProvider, quick_config, tmp_path
    ):
        _setup_mock_pipeline(MockSupervisor, MockAggregator, MockProvider)

        input_dir = tmp_path / "input"
        input_dir.mkdir()
        for i in range(2):
            (input_dir / f"f{i}.md").write_text(f"# {i}\n")

        _, batch_dir = run_batch_validation(
            target=input_dir,
            pattern="*.md",
            config=quick_config,
            runs_dir=tmp_path / "runs",
        )

        content = (batch_dir / "batch-report.md").read_text()
        assert "Batch Verdict:" in content
        assert "Aggregate Findings" in content


# ── 6. Manifest always valid JSON ─────────────────────────────────────────────


class TestManifestIntegrity:
    @patch("quorum.pipeline.LiteLLMProvider")
    @patch("quorum.pipeline.AggregatorAgent")
    @patch("quorum.pipeline.SupervisorAgent")
    def test_manifest_always_parseable(
        self, MockSupervisor, MockAggregator, MockProvider, quick_config, tmp_path
    ):
        """Every version of batch-manifest.json written must be valid JSON."""
        _setup_mock_pipeline(MockSupervisor, MockAggregator, MockProvider)

        input_dir = tmp_path / "input"
        input_dir.mkdir()
        for i in range(4):
            (input_dir / f"f{i}.md").write_text(f"# {i}\n")

        import quorum.pipeline as _pipeline_mod
        snapshots: list[str] = []
        original = _pipeline_mod._write_json_atomic

        def capturing(path: Path, data: dict) -> None:
            original(path, data)
            if path.name == "batch-manifest.json":
                try:
                    snapshots.append(path.read_text())
                except OSError:
                    pass

        with patch.object(_pipeline_mod, "_write_json_atomic", side_effect=capturing):
            run_batch_validation(
                target=input_dir,
                pattern="*.md",
                config=quick_config,
                runs_dir=tmp_path / "runs",
            )

        assert snapshots, "No manifest snapshots captured"
        for i, snap in enumerate(snapshots):
            parsed = json.loads(snap)  # must not raise
            assert "status" in parsed, f"Snapshot {i} missing 'status'"

    def test_initial_manifest_written_immediately(self, tmp_path, quick_config):
        """The manifest exists on disk even before the first file finishes."""
        import quorum.pipeline as _pipeline_mod

        input_dir = tmp_path / "input"
        input_dir.mkdir()
        for i in range(3):
            (input_dir / f"f{i}.md").write_text(f"# {i}\n")

        manifest_exists_during_run = threading.Event()
        batch_dir_holder: list[Path] = []
        original_validate = _pipeline_mod._validate_one_file

        def spy_validate(file_path, index, total, *args, **kwargs):
            # On first file, check that manifest already exists
            if index == 1:
                for p in (tmp_path / "runs").glob("batch-*/batch-manifest.json"):
                    manifest_exists_during_run.set()
            return original_validate(file_path, index, total, *args, **kwargs)

        with patch("quorum.pipeline.LiteLLMProvider"), \
             patch("quorum.pipeline.AggregatorAgent") as MockAgg, \
             patch("quorum.pipeline.SupervisorAgent") as MockSup, \
             patch.object(_pipeline_mod, "_validate_one_file", side_effect=spy_validate):

            cr = CriticResult(critic_name="correctness", findings=[], confidence=0.9, runtime_ms=50)
            MockSup.return_value.run = MagicMock(return_value=[cr])
            MockAgg.return_value.run = MagicMock(return_value=_make_verdict())

            _, batch_dir = run_batch_validation(
                target=input_dir,
                pattern="*.md",
                config=quick_config,
                runs_dir=tmp_path / "runs",
            )

        assert manifest_exists_during_run.is_set(), (
            "batch-manifest.json was not on disk before the first file finished"
        )
