"""Tests for cart_link.

Offline tests cover argument parsing and the local-side handoff plumbing
(HTML file write, shopping list rendering, browser-open opt-out) by
patching the network calls. The actual cart build hits gsp.target.com
plus carts.target.com — gated behind TARGET_LIVE_TESTS.
"""

from __future__ import annotations

import os
import urllib.parse
from pathlib import Path

import pytest

from scripts import _auth, cart_link

LIVE = os.environ.get("TARGET_LIVE_TESTS") == "1"


# ---------- Offline: argument parsing ----------

def test_parse_items_default_qty_is_one():
    assert cart_link.parse_items(["111", "222"], None) == [("111", 1), ("222", 1)]


def test_parse_items_single_qty_broadcasts():
    assert cart_link.parse_items(["111", "222", "333"], [4]) == [
        ("111", 4),
        ("222", 4),
        ("333", 4),
    ]


def test_parse_items_per_tcin_quantities():
    assert cart_link.parse_items(["111", "222"], [2, 5]) == [("111", 2), ("222", 5)]


def test_parse_items_length_mismatch_raises():
    with pytest.raises(ValueError):
        cart_link.parse_items(["111", "222", "333"], [1, 2])


def test_parse_items_rejects_zero_quantity():
    with pytest.raises(ValueError):
        cart_link.parse_items(["111"], [0])


def test_transfer_url_shape():
    url = _auth.transfer_url("abc.def.ghi")
    parts = urllib.parse.urlparse(url)
    assert parts.scheme == "https"
    assert parts.netloc == "www.target.com"
    assert parts.path == "/cart"
    qs = dict(urllib.parse.parse_qsl(parts.query))
    assert qs == {"access_token": "abc.def.ghi"}


# ---------- Offline: rendering helpers ----------

def test_shopping_list_markdown_renders_items():
    md = cart_link._shopping_list_markdown(
        [
            {"tcin": "111", "qty": 2, "title": "Basmati Rice 32oz", "current_price": 4.29},
            {"tcin": "222", "qty": 1, "title": "Garlic Powder", "current_price": 1.19},
        ]
    )
    assert "## Target shopping list (2 items)" in md
    assert "[Basmati Rice 32oz](https://www.target.com/p/-/A-111) x2 - $4.29" in md
    assert "[Garlic Powder](https://www.target.com/p/-/A-222) x1 - $1.19" in md


def test_shopping_list_markdown_handles_missing_title_and_price():
    md = cart_link._shopping_list_markdown([{"tcin": "999", "qty": 1}])
    assert "[TCIN 999](https://www.target.com/p/-/A-999) x1" in md
    assert "$" not in md  # no price -> no $ formatting


def test_shopping_list_markdown_empty():
    assert cart_link._shopping_list_markdown([]) == ""


def test_shopping_list_text_renders_one_per_line():
    out = cart_link._shopping_list_text(
        [{"tcin": "111", "qty": 2}, {"tcin": "222", "qty": 1}]
    )
    assert out.splitlines() == [
        "2x https://www.target.com/p/-/A-111",
        "1x https://www.target.com/p/-/A-222",
    ]


def test_url_preview_short_url_is_unchanged():
    short = "https://www.target.com/cart?access_token=abc"
    assert cart_link._url_preview(short) == short


def test_url_preview_long_url_is_elided():
    long = "https://www.target.com/cart?access_token=" + ("y" * 800)
    out = cart_link._url_preview(long)
    assert out.startswith("https://www.target.com/cart?access_token=")
    assert "..." in out
    assert len(out) < len(long)
    assert out.endswith("y" * 20)


def test_write_redirect_html_contains_url_and_items(tmp_path: Path):
    target = tmp_path / "cart.html"
    cart_link._write_redirect_html(
        target,
        "https://www.target.com/cart?access_token=TOK",
        [{"tcin": "111", "qty": 2, "title": "Test Item"}],
    )
    body = target.read_text(encoding="utf-8")
    assert "https://www.target.com/cart?access_token=TOK" in body
    assert 'http-equiv="refresh"' in body
    assert "2x Test Item" in body


def test_write_redirect_html_escapes_user_data(tmp_path: Path):
    target = tmp_path / "cart.html"
    cart_link._write_redirect_html(
        target,
        "https://www.target.com/cart?access_token=tok&x=1",
        [{"tcin": "111", "qty": 1, "title": "Risky <script>alert('x')</script>"}],
    )
    body = target.read_text(encoding="utf-8")
    assert "<script>alert" not in body
    assert "&lt;script&gt;" in body
    # The ampersand in the URL must also be escaped inside HTML attributes.
    assert "access_token=tok&amp;x=1" in body


# ---------- Offline: build_cart with mocked HTTP ----------

class _StubResp:
    def __init__(self, **kw):
        self.kw = kw

    def get(self, k, default=None):
        return self.kw.get(k, default)


def _patch_network(monkeypatch, *, items_seen: list | None = None):
    """Replace _auth.get_token and _auth.add_cart_item with deterministic stubs.

    No network is touched. items_seen, if provided, collects the (tcin, qty)
    pairs that build_cart attempted to add.
    """
    monkeypatch.setattr(
        _auth,
        "get_token",
        lambda **kw: {
            "access_token": "header." + ("p" * 400) + ".sig",  # >600 chars total
            "_payload": {"sub": "guest-abc", "exp": 9_999_999_999},
        },
    )

    def fake_add(*, tcin, quantity, bearer, cart_id=None, **kw):
        if items_seen is not None:
            items_seen.append((tcin, quantity))
        return {
            "cart_id": cart_id or "cart-XYZ",
            "cart_item_id": f"item-{tcin}",
            "total_cart_item_quantity": (cart_id and 0 or 0) + quantity,
            "item_description": f"Title {tcin}",
            "unit_price": 1.99,
            "current_price": 1.99,
        }

    monkeypatch.setattr(_auth, "add_cart_item", fake_add)


def test_build_cart_writes_file_and_skips_browser_when_disabled(monkeypatch, tmp_path: Path):
    _patch_network(monkeypatch)
    opened = []
    monkeypatch.setattr(cart_link.webbrowser, "open", lambda u: opened.append(u) or True)

    cart_file = tmp_path / "out.html"
    result = cart_link.build_cart(
        [("111", 1), ("222", 1)],
        open_browser=False,
        cart_file=cart_file,
    )

    assert opened == [], "webbrowser.open must not be called when open_browser=False"
    assert result["auto_opened"] is False
    assert result["cart_file"] == str(cart_file.resolve())
    assert cart_file.exists()
    assert "access_token=" in cart_file.read_text(encoding="utf-8")
    assert result["url_length"] > 400
    assert "..." in result["url_preview"]
    assert "Do NOT inline" in result["url_warning"]
    assert "## Target shopping list" in result["shopping_list_markdown"]
    assert "[Title 111](https://www.target.com/p/-/A-111)" in result["shopping_list_markdown"]
    assert result["items_failed"] == []
    assert result["cart_id"] == "cart-XYZ"


def test_build_cart_calls_browser_open_when_enabled(monkeypatch, tmp_path: Path):
    _patch_network(monkeypatch)
    opened = []
    monkeypatch.setattr(cart_link.webbrowser, "open", lambda u: opened.append(u) or True)

    result = cart_link.build_cart(
        [("111", 1)], open_browser=True, cart_file=tmp_path / "c.html"
    )

    assert len(opened) == 1
    assert opened[0].startswith("https://www.target.com/cart?access_token=")
    assert result["auto_opened"] is True


def test_build_cart_records_per_item_failures(monkeypatch, tmp_path: Path):
    _patch_network(monkeypatch)

    def flaky(*, tcin, quantity, bearer, cart_id=None, **kw):
        if tcin == "BAD":
            raise RuntimeError("HTTP 404: not a real TCIN")
        return {
            "cart_id": cart_id or "cart-XYZ",
            "cart_item_id": f"item-{tcin}",
            "total_cart_item_quantity": quantity,
            "item_description": f"Title {tcin}",
            "unit_price": 0.99,
            "current_price": 0.99,
        }

    monkeypatch.setattr(_auth, "add_cart_item", flaky)
    monkeypatch.setattr(cart_link.webbrowser, "open", lambda u: True)

    result = cart_link.build_cart(
        [("GOOD", 1), ("BAD", 1)],
        open_browser=False,
        cart_file=tmp_path / "c.html",
    )

    assert len(result["items_added"]) == 1
    assert result["items_added"][0]["tcin"] == "GOOD"
    assert len(result["items_failed"]) == 1
    assert result["items_failed"][0]["tcin"] == "BAD"
    assert "HTTP 404" in result["items_failed"][0]["error"]
    # Shopping list reflects only successful adds.
    assert "GOOD" in result["shopping_list_markdown"]
    assert "BAD" not in result["shopping_list_markdown"]


def test_main_exits_2_on_partial_failure(monkeypatch, tmp_path: Path, capsys):
    _patch_network(monkeypatch)

    def fail_once(*, tcin, quantity, bearer, cart_id=None, **kw):
        raise RuntimeError("nope")

    monkeypatch.setattr(_auth, "add_cart_item", fail_once)
    monkeypatch.setattr(cart_link.webbrowser, "open", lambda u: True)

    rc = cart_link.main(["111", "--no-open", "--cart-file", str(tmp_path / "c.html")])
    assert rc == 2
    out = capsys.readouterr().out
    assert '"items_failed"' in out


# ---------- Live: end-to-end cart build ----------

@pytest.mark.live
@pytest.mark.skipif(not LIVE, reason="set TARGET_LIVE_TESTS=1 to run")
def test_live_mint_token():
    tok = _auth.mint_token()
    assert "access_token" in tok
    assert tok["token_type"] == "Bearer"
    assert tok["_payload"]["iss"] == "MI6"
    assert tok["_payload"]["sut"] == "G"  # guest
    assert tok["_payload"]["cli"] == "ecom-web-1.0.0"


@pytest.mark.live
@pytest.mark.skipif(not LIVE, reason="set TARGET_LIVE_TESTS=1 to run")
def test_live_build_cart_two_items():
    # Apple EarPods (USB-C) + Sony WHCH520 refurb — both evergreen.
    result = cart_link.build_cart([("89827259", 2), ("94783927", 1)])
    assert result["cart_id"]
    assert result["total_cart_item_quantity"] == 3
    assert len(result["items_added"]) == 2
    assert not result["items_failed"]
    assert result["url"].startswith("https://www.target.com/cart?access_token=")
    # token good for at most ~24h.
    assert 0 < (result["token_expires_in_hours"] or 0) <= 24
