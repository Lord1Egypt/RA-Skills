"""Integration tests for platform scrapers.

These tests make real network requests. Run with:
    pytest tests/test_platforms.py -v -k "bilibili"

Skip slow browser-based tests:
    pytest tests/test_platforms.py -v -k "not browser"
"""
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))

from platforms.bilibili import BilibiliPlatform


@pytest.mark.asyncio
async def test_bilibili_fetch_by_url():
    """Test Bilibili API with a known public account."""
    platform = BilibiliPlatform()
    result = await platform.fetch_by_url("https://space.bilibili.com/946974")
    assert result.success, f"Expected success but got error: {result.error}"
    assert result.platform == "bilibili"
    assert result.uid == "946974"
    assert result.metrics.get("followers") is not None
    assert isinstance(result.metrics["followers"], int)
    assert result.metrics["followers"] > 0


@pytest.mark.asyncio
async def test_bilibili_fetch_by_nickname():
    """Test Bilibili nickname search (may fail due to API rate limiting)."""
    platform = BilibiliPlatform()
    result = await platform.fetch_by_nickname("影视飓风")
    assert result.platform == "bilibili"
    if result.success:
        assert result.metrics.get("followers") is not None


@pytest.mark.asyncio
async def test_bilibili_invalid_uid():
    """Test Bilibili with invalid URL."""
    platform = BilibiliPlatform()
    result = await platform.fetch_by_url("https://space.bilibili.com/invalid")
    assert not result.success
