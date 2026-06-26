"""Live smoke tests against Target's real public-facing API.

Disabled by default. Run explicitly with:

    TARGET_LIVE_TESTS=1 uv run pytest -m live -v

These tests verify the public key + URL shapes still work.
They do not assert on volatile content (price, stock) — only structure.
"""

from __future__ import annotations

import os

import pytest

from scripts import fulfillment, pdp, reviews, search, stores, summary

LIVE = os.environ.get("TARGET_LIVE_TESTS") == "1"
pytestmark = [
    pytest.mark.live,
    pytest.mark.skipif(not LIVE, reason="set TARGET_LIVE_TESTS=1 to run"),
]

# Evergreen test product: Apple EarPods (USB-C). Stable for years.
TCIN = "89827259"
ZIP = "55403"


def test_live_search():
    raw = search.fetch(
        keyword="milk",
        category=None,
        count=3,
        offset=0,
        store_id="2281",
        pricing_store_id="2281",
        visitor_id="0000000000000000000000000000000000",
    )
    out = search.trim(raw, query_label="milk")
    assert out["count_returned"] >= 1
    assert out["results"][0]["tcin"]


def test_live_pdp():
    raw = pdp.fetch(
        tcin=TCIN,
        store_id="2281",
        pricing_store_id="2281",
        visitor_id="0000000000000000000000000000000000",
    )
    out = pdp.trim(raw)
    assert out["tcin"] == TCIN
    assert out["title"]


def test_live_summary():
    raw = summary.fetch(
        tcins=[TCIN],
        store_id="2281",
        pricing_store_id="2281",
        zip_code=ZIP,
        state=None,
        latitude=None,
        longitude=None,
    )
    out = summary.trim(raw)
    assert out["count"] == 1
    assert out["items"][0]["tcin"] == TCIN


def test_live_fulfillment():
    raw = fulfillment.fetch(
        tcin=TCIN,
        nearby=ZIP,
        radius=50,
        limit=3,
        requested_quantity=1,
        only_available=False,
        visitor_id="0000000000000000000000000000000000",
    )
    out = fulfillment.trim(raw)
    assert out["tcin"] == TCIN
    assert out["stores_checked"] >= 1


def test_live_stores():
    raw = stores.fetch(place=ZIP, limit=3, within=50)
    out = stores.trim(raw)
    assert out["count"] >= 1
    assert out["stores"][0]["store_id"]


def test_live_reviews():
    raw = reviews.fetch(tcin=TCIN)
    out = reviews.trim(raw)
    assert out["tcin"] == TCIN
