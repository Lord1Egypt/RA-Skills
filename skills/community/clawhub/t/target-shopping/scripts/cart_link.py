"""Build a real, pre-populated guest cart on target.com and emit a handoff URL.

Flow:
  1. Mint (or reuse) a 24-hour anonymous bearer token via gsp.target.com.
  2. POST each TCIN to carts.target.com/web_checkouts/v1/cart_items, all
     bound to the same server-side guest cart.
  3. Write a local HTML redirect file (cart_file) that opens the cart, and
     try to launch it in the user's default browser. Emit the file path
     plus a markdown shopping list as the primary handoff surface.

When the user opens the cart URL their browser:
  - reads the access_token from the query string,
  - mints its OWN session token,
  - decodes our token's `sub` to use as `external_guest_id`,
  - calls /web_checkouts/v1/external_cart_merges,
  - drops them on /cart with the items pre-populated, ready to check out.

The token grants cart-write access for ~24h. Treat the URL like a one-time
share link: don't paste it into long-lived chat history or commit it.

IMPORTANT FOR THE ASSISTANT: the URL is ~600 chars (mostly JWT). Many chat
UIs truncate it, which silently breaks the handoff. Refer the user to
`cart_file` or the auto-opened browser tab. Never inline the raw `url`.
"""

from __future__ import annotations

import argparse
import html
import os
import sys
import tempfile
import time
import webbrowser
from pathlib import Path

from . import _auth, _common as c


def parse_items(tcins: list[str], quantities: list[int] | None) -> list[tuple[str, int]]:
    if quantities and len(quantities) not in (1, len(tcins)):
        raise ValueError(
            "--quantities must have either 1 value (applies to all) "
            "or the same count as TCINs"
        )
    if not quantities:
        qs = [1] * len(tcins)
    elif len(quantities) == 1:
        qs = quantities * len(tcins)
    else:
        qs = quantities
    for tcin, q in zip(tcins, qs, strict=True):
        if q < 1:
            raise ValueError(f"quantity must be >= 1 (got {q} for {tcin})")
    return list(zip(tcins, qs, strict=True))


def _default_cart_file(cart_id: str | None) -> Path:
    base = Path(tempfile.gettempdir()) / "target-com-shopper"
    base.mkdir(parents=True, exist_ok=True)
    suffix = cart_id or f"unknown-{int(time.time())}"
    return base / f"cart-{suffix}.html"


def _write_redirect_html(path: Path, url: str, items: list[dict]) -> None:
    """Write a self-contained HTML page that auto-redirects to the cart URL.

    Includes a clickable fallback link and a visible shopping summary so
    the file is useful even if the redirect is blocked.
    """
    rows = "".join(
        f"<li>{html.escape(str(it.get('qty', 1)))}x "
        f"{html.escape(it.get('title') or it.get('tcin') or 'item')}</li>"
        for it in items
    )
    body = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta http-equiv="refresh" content="0; url={html.escape(url, quote=True)}">
<title>Open Target cart</title>
<style>
body {{ font-family: -apple-system, system-ui, sans-serif; max-width: 40em; margin: 3em auto; padding: 0 1em; color: #333; }}
a.cta {{ display: inline-block; padding: 0.75em 1.5em; background: #cc0000; color: white; text-decoration: none; border-radius: 4px; font-weight: 600; }}
ul {{ background: #f6f6f6; padding: 1em 1em 1em 2.5em; border-radius: 4px; }}
</style>
</head>
<body>
<h1>Opening your Target cart...</h1>
<p>If you aren't redirected automatically, click below:</p>
<p><a class="cta" href="{html.escape(url, quote=True)}">Open Target cart</a></p>
<h2>Items in this cart</h2>
<ul>{rows}</ul>
</body>
</html>
"""
    path.write_text(body, encoding="utf-8")


def _shopping_list_markdown(items: list[dict]) -> str:
    if not items:
        return ""
    lines = [f"## Target shopping list ({len(items)} item{'s' if len(items) != 1 else ''})", ""]
    for it in items:
        tcin = it.get("tcin", "")
        title = it.get("title") or f"TCIN {tcin}"
        qty = it.get("qty", 1)
        price = it.get("current_price")
        pdp = f"https://www.target.com/p/-/A-{tcin}"
        price_str = f" - ${price:.2f}" if isinstance(price, (int, float)) else ""
        lines.append(f"- [{title}]({pdp}) x{qty}{price_str}")
    return "\n".join(lines) + "\n"


def _shopping_list_text(items: list[dict]) -> str:
    return "\n".join(
        f"{it.get('qty', 1)}x https://www.target.com/p/-/A-{it.get('tcin', '')}"
        for it in items
    ) + ("\n" if items else "")


def _url_preview(url: str) -> str:
    if len(url) <= 100:
        return url
    return f"{url[:80]}...{url[-20:]}"


def build_cart(
    items: list[tuple[str, int]],
    *,
    force_refresh_token: bool = False,
    open_browser: bool = True,
    cart_file: Path | None = None,
) -> dict:
    """Mint token, push items, write a redirect HTML file, optionally open browser."""
    if not items:
        raise ValueError("no items provided")

    tok = _auth.get_token(force_refresh=force_refresh_token)
    bearer = tok["access_token"]

    cart_id: str | None = None
    pushed: list[dict] = []
    failures: list[dict] = []
    total_qty = 0

    for tcin, qty in items:
        try:
            resp = _auth.add_cart_item(
                tcin=tcin, quantity=qty, bearer=bearer, cart_id=cart_id
            )
            cart_id = cart_id or resp.get("cart_id")
            total_qty = resp.get("total_cart_item_quantity", total_qty)
            pushed.append(
                {
                    "tcin": tcin,
                    "qty": qty,
                    "title": resp.get("item_description")
                    or c.safe_get(resp, "item", "product_description", "title"),
                    "unit_price": resp.get("unit_price"),
                    "current_price": resp.get("current_price"),
                    "cart_item_id": resp.get("cart_item_id"),
                }
            )
        except Exception as e:  # noqa: BLE001
            failures.append({"tcin": tcin, "qty": qty, "error": str(e)})

    url = _auth.transfer_url(bearer)

    file_path = cart_file or _default_cart_file(cart_id)
    file_written: str | None = None
    file_error: str | None = None
    try:
        _write_redirect_html(file_path, url, pushed)
        file_written = str(file_path.resolve())
    except OSError as e:
        file_error = str(e)

    auto_opened = False
    auto_open_error: str | None = None
    if open_browser:
        try:
            auto_opened = bool(webbrowser.open(url))
        except Exception as e:  # noqa: BLE001
            auto_open_error = str(e)

    expiry_epoch = tok.get("_payload", {}).get("exp")
    expires_in_h = (
        round((expiry_epoch - time.time()) / 3600, 1) if expiry_epoch else None
    )

    result: dict = {
        "cart_file": file_written,
        "auto_opened": auto_opened,
        "cart_id": cart_id,
        "guest_id": tok.get("_payload", {}).get("sub"),
        "total_cart_item_quantity": total_qty,
        "items_added": pushed,
        "items_failed": failures,
        "shopping_list_markdown": _shopping_list_markdown(pushed),
        "shopping_list_text": _shopping_list_text(pushed),
        "token_expires_in_hours": expires_in_h,
        "url_length": len(url),
        "url_preview": _url_preview(url),
        "url_warning": (
            "Do NOT inline the full `url` into a chat reply - the JWT is ~600 "
            "chars and chat UIs truncate it, breaking the handoff. Use "
            "`cart_file` (a short local path) or rely on `auto_opened`."
        ),
        "url": url,
        "note": (
            "Recommended: tell the user to open `cart_file` (or note that the "
            "browser already opened). The cart URL is a 24h bearer token - "
            "treat it like a one-time share link."
        ),
    }
    if file_error:
        result["cart_file_error"] = file_error
    if auto_open_error:
        result["auto_open_error"] = auto_open_error
    return result


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(
        prog="cart_link",
        description=(
            "Build a real guest cart on target.com. Writes a local HTML "
            "redirect file and tries to open it in the default browser. "
            "Avoids inlining the (long) cart URL, which chat UIs truncate."
        ),
    )
    p.add_argument("tcins", nargs="+", help="One or more TCINs")
    p.add_argument(
        "--quantities",
        nargs="+",
        type=int,
        default=None,
        help="Per-TCIN quantities (default 1). Pass 1 value to apply to all.",
    )
    p.add_argument(
        "--refresh-token",
        action="store_true",
        help="Force minting a fresh token instead of reusing the cached one.",
    )
    p.add_argument(
        "--no-open",
        action="store_true",
        help="Skip launching the default browser. Just write the cart_file.",
    )
    p.add_argument(
        "--cart-file",
        default=None,
        help=(
            "Where to write the HTML redirect file. "
            "Defaults to $TMPDIR/target-com-shopper/cart-<cart_id>.html."
        ),
    )
    args = p.parse_args(argv)

    cart_file_path: Path | None = None
    if args.cart_file:
        cart_file_path = Path(os.path.expanduser(args.cart_file)).resolve()
        cart_file_path.parent.mkdir(parents=True, exist_ok=True)

    try:
        items = parse_items(args.tcins, args.quantities)
        result = build_cart(
            items,
            force_refresh_token=args.refresh_token,
            open_browser=not args.no_open,
            cart_file=cart_file_path,
        )
    except ValueError as e:
        c.fail(str(e))
    except Exception as e:  # noqa: BLE001
        c.fail(f"cart build failed: {e}")

    c.emit(result)
    if result["items_failed"]:
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
