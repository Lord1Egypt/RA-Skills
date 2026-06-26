"""Offline tests: load raw fixtures, run trim() functions, assert shape.

These do not hit the network. They guard against schema-path regressions
in the trim layer.
"""

from __future__ import annotations

from scripts import fulfillment, pdp, reviews, search, stores, summary


def test_search_trim_shape(fixture):
    raw = fixture("search.json")
    out = search.trim(raw, query_label="milk")

    assert out["query"] == "milk"
    assert out["count_returned"] == 3
    assert out["total_results"] == 76
    assert out["current_page"] == 1
    assert out["total_pages"] == 26
    assert len(out["results"]) == 3

    first = out["results"][0]
    # Required keys exist on every result, even if value is None.
    for key in (
        "tcin",
        "title",
        "brand",
        "price",
        "reg_price",
        "save_percent",
        "rating",
        "review_count",
        "buy_url",
        "image",
    ):
        assert key in first, f"missing key: {key}"

    # At least the first result has real data we know is in the fixture.
    assert first["tcin"]
    assert first["price"] and first["price"].startswith("$")


def test_pdp_trim_shape(fixture):
    raw = fixture("pdp.json")
    out = pdp.trim(raw)

    assert out["tcin"] == "89827259"
    assert out["title"] == "Apple EarPods (USB-C)"
    assert out["brand"]  # primary_brand.name
    assert out["price"]["formatted"]
    assert out["price"]["current"] is not None
    assert isinstance(out["bullets"], list)
    assert "primary" in out["images"]
    assert isinstance(out["images"]["alternates"], list)
    assert isinstance(out["promotions"], list)
    assert isinstance(out["variants"], list)
    assert out["rating"]["average"] is not None
    assert out["rating"]["count"] is not None


def test_summary_trim_shape(fixture):
    raw = fixture("summary.json")
    out = summary.trim(raw)

    assert out["count"] >= 1
    assert len(out["items"]) == out["count"]
    item = out["items"][0]
    for key in (
        "tcin",
        "title",
        "buy_url",
        "sold_out",
        "shipping_status",
        "primary_store_id",
    ):
        assert key in item


def test_fulfillment_trim_shape(fixture):
    raw = fixture("fulfillment.json")
    out = fulfillment.trim(raw)

    assert out["tcin"] == "89827259"
    assert out["stores_checked"] >= 1
    s = out["stores"][0]
    for key in (
        "store_id",
        "name",
        "city",
        "state",
        "zip",
        "distance_mi",
        "available_qty",
        "pickup",
    ):
        assert key in s
    assert s["store_id"]


def test_stores_trim_shape(fixture):
    raw = fixture("stores.json")
    out = stores.trim(raw)

    assert out["count"] >= 1
    s = out["stores"][0]
    for key in (
        "store_id",
        "name",
        "address",
        "city",
        "state",
        "zip",
        "phone",
        "distance_mi",
        "timezone",
    ):
        assert key in s
    # state should fall back to two-letter region.
    assert s["state"] in ("MN", "Minnesota") or len(s["state"]) >= 2


def test_reviews_trim_shape(fixture):
    raw = fixture("reviews.json")
    out = reviews.trim(raw)

    assert out["tcin"] == "89827259"
    assert "review_count" in out
    assert "average_rating" in out
    assert "note" in out
    assert "not returned" in out["note"].lower()
