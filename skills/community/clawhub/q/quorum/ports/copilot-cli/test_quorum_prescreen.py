"""Tests for the Copilot CLI quorum-prescreen.py — batch link scanning."""

from __future__ import annotations

import importlib
import sys
from pathlib import Path

import pytest

# Add the copilot-cli directory to sys.path so we can import the module
_CLI_DIR = str(Path(__file__).resolve().parent)
if _CLI_DIR not in sys.path:
    sys.path.insert(0, _CLI_DIR)

# Import from the hyphenated filename
quorum_prescreen = importlib.import_module("quorum-prescreen")


class TestScanAllLinks:
    """Tests for the scan_all_links batch scanning function."""

    def test_clean_repo_returns_zero_broken(self, tmp_path):
        (tmp_path / ".git").mkdir()
        (tmp_path / "README.md").write_text("# Hello\n[other](other.md)\n")
        (tmp_path / "other.md").write_text("# Other\n")
        result = quorum_prescreen.scan_all_links(tmp_path)
        assert result["total_broken"] == 0
        assert result["files_with_broken_links"] == 0

    def test_broken_link_detected_across_files(self, tmp_path):
        (tmp_path / ".git").mkdir()
        (tmp_path / "README.md").write_text("[missing](NONEXISTENT.md)\n")
        (tmp_path / "docs").mkdir()
        (tmp_path / "docs" / "guide.md").write_text("[also missing](nope.md)\n")
        result = quorum_prescreen.scan_all_links(tmp_path)
        assert result["files_with_broken_links"] == 2
        assert result["total_broken"] >= 2

    def test_skips_hidden_dirs(self, tmp_path):
        (tmp_path / ".git").mkdir()
        git_md = tmp_path / ".git" / "description.md"
        git_md.write_text("[broken](nope.md)\n")
        (tmp_path / "README.md").write_text("# Clean\n")
        result = quorum_prescreen.scan_all_links(tmp_path)
        assert result["files_with_broken_links"] == 0

    def test_upward_links_within_repo_not_false_positive(self, tmp_path):
        (tmp_path / ".git").mkdir()
        (tmp_path / "SPEC.md").write_text("# Spec\n")
        sub = tmp_path / "docs" / "guides"
        sub.mkdir(parents=True)
        (sub / "tutorial.md").write_text("[spec](../../SPEC.md)\n")
        result = quorum_prescreen.scan_all_links(tmp_path)
        assert result["total_broken"] == 0

    def test_non_directory_returns_error(self, tmp_path):
        f = tmp_path / "file.txt"
        f.write_text("hi")
        result = quorum_prescreen.scan_all_links(f)
        assert "error" in result
