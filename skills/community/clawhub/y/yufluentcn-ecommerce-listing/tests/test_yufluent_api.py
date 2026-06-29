"""Tests for Yufluent cloud skill client."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SHARED = ROOT.parent / "_shared"
sys.path.insert(0, str(SHARED))

from yufluent_api import normalize_api_root, skill_run_url  # noqa: E402


def test_normalize_api_root_with_v1_suffix():
    assert normalize_api_root("http://localhost:8080/v1") == "http://localhost:8080/v1"


def test_normalize_api_root_without_v1():
    assert normalize_api_root("http://localhost:8080") == "http://localhost:8080/v1"


def test_skill_run_url():
    url = skill_run_url("https://example.com/api/v1", "listing")
    assert url == "https://example.com/api/v1/skills/listing/run"
