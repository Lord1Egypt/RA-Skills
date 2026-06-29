"""Format listing output labels by language."""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from format_listing import format_listing


def test_tiktok_en_section_labels():
    listing = {
        "title": "Cool Earbuds",
        "bullet_points": ["Point 1"],
        "description": "Great sound",
        "keywords": ["earbuds"],
        "hashtags": ["#audio"],
        "hook": "You need these!",
    }
    text = format_listing(listing, "tiktok", "en")
    assert "[Title]" in text
    assert "[Selling Points]" in text
    assert "【标题】" not in text
