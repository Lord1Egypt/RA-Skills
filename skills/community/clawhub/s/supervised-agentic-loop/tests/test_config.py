"""Tests for sal.config — EvolveConfig validation."""

import os
import tempfile

import pytest

from sal.config import EvolveConfig


@pytest.fixture
def tmp_work_dir():
    """Create a temp dir with a target file."""
    d = tempfile.mkdtemp()
    target = os.path.join(d, "train.py")
    with open(target, "w") as f:
        f.write("print('hello')\n")
    yield d


def test_valid_config(tmp_work_dir):
    """should create config with valid defaults."""
    cfg = EvolveConfig(
        target_file="train.py",
        metric_command="python train.py",
        metric_parser="last_line_float",
        work_dir=tmp_work_dir,
    )
    assert cfg.target_file == "train.py"
    assert cfg.minimize is True
    assert cfg.time_budget == 300
    assert cfg.max_iterations == 100
    assert cfg.run_tag  # auto-generated


def test_auto_run_tag(tmp_work_dir):
    """should auto-generate run_tag when not provided."""
    cfg = EvolveConfig(
        target_file="train.py",
        metric_command="python train.py",
        metric_parser="last_line_float",
        work_dir=tmp_work_dir,
    )
    assert len(cfg.run_tag) == 15  # YYYYMMDD_HHMMSS


def test_missing_target_file():
    """should raise FileNotFoundError for non-existent target."""
    with pytest.raises(FileNotFoundError, match="not found"):
        EvolveConfig(
            target_file="nonexistent.py",
            metric_command="echo 1",
            metric_parser="last_line_float",
            work_dir="/tmp",
        )


def test_invalid_metric_parser(tmp_work_dir):
    """should raise ValueError for bad metric_parser spec."""
    with pytest.raises(ValueError, match="not a named strategy"):
        EvolveConfig(
            target_file="train.py",
            metric_command="echo 1",
            metric_parser="(invalid[regex",
            work_dir=tmp_work_dir,
        )


def test_negative_time_budget(tmp_work_dir):
    """should raise ValueError for time_budget <= 0."""
    with pytest.raises(ValueError, match="time_budget must be > 0"):
        EvolveConfig(
            target_file="train.py",
            metric_command="echo 1",
            metric_parser="last_line_float",
            time_budget=-1,
            work_dir=tmp_work_dir,
        )


def test_target_in_readonly(tmp_work_dir):
    """should raise ValueError if target_file is in readonly_files."""
    with pytest.raises(ValueError, match="cannot be in readonly_files"):
        EvolveConfig(
            target_file="train.py",
            metric_command="echo 1",
            metric_parser="last_line_float",
            readonly_files=["train.py"],
            work_dir=tmp_work_dir,
        )
