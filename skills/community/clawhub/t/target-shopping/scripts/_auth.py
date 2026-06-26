"""Anonymous guest token + carts.target.com cart helpers.

Mints a 24h `MI6` bearer token on demand and caches it locally.
The token is bound to a server-side guest session — sharing the token
in a `https://www.target.com/cart?access_token=<TOKEN>` URL lets the
recipient's browser merge our items into their cart via Target's
public `external_cart_merges` flow (no login required).

NOTE: tokens grant the holder access to mutate the bound cart. Treat
them like one-time-use share links: do not commit to source control,
do not log to long-lived stores. They expire in ~24h.
"""

from __future__ import annotations

import base64
import json
import os
import tempfile
import time
from pathlib import Path
from typing import Any

from . import _common as c

GSP_TOKEN_URL = "https://gsp.target.com/gsp/oauth_tokens/v2/client_tokens"
CARTS_BASE = "https://carts.target.com/web_checkouts/v1"
CART_TRANSFER_BASE = "https://www.target.com/cart"

CLIENT_ID = "ecom-web-1.0.0"
GRANT_TYPE = "anonymous"

# Refresh tokens that expire within this many seconds.
EXPIRY_SKEW_S = 600


def _cache_path() -> Path:
    base = os.environ.get("TARGET_TOKEN_CACHE_DIR")
    if base:
        d = Path(base)
    else:
        d = Path(tempfile.gettempdir()) / "target-com-shopper"
    d.mkdir(parents=True, exist_ok=True)
    return d / "anonymous-token.json"


def _decode_jwt_payload(jwt: str) -> dict[str, Any]:
    payload_b64 = jwt.split(".")[1]
    payload_b64 += "=" * (-len(payload_b64) % 4)
    return json.loads(base64.urlsafe_b64decode(payload_b64))


def _post_json(url: str, body: dict[str, Any], *, bearer: str | None = None) -> dict[str, Any]:
    """POST JSON via stdlib urllib, return parsed JSON.

    Accepts 200/201/206 as success. Raises RuntimeError otherwise.
    """
    import urllib.error
    import urllib.request
    import ssl

    headers = {
        "User-Agent": c.get_user_agent(),
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Origin": "https://www.target.com",
        "Referer": "https://www.target.com/",
    }
    if bearer:
        headers["Authorization"] = f"Bearer {bearer}"

    data = json.dumps(body).encode("utf-8")
    req = urllib.request.Request(url, data=data, headers=headers, method="POST")
    ctx = ssl.create_default_context()
    try:
        with urllib.request.urlopen(req, timeout=c.get_timeout(), context=ctx) as resp:
            status = resp.status
            raw = resp.read()
            if status in (200, 201, 206):
                return json.loads(raw.decode("utf-8"))
            raise RuntimeError(
                f"HTTP {status} from {url}: {raw[:300].decode('utf-8', 'replace')}"
            )
    except urllib.error.HTTPError as e:
        body_b = e.read() if hasattr(e, "read") else b""
        raise RuntimeError(
            f"HTTP {e.code} from {url}: {body_b[:300].decode('utf-8', 'replace')}"
        ) from e


def mint_token() -> dict[str, Any]:
    """Mint a fresh anonymous guest token. Includes `access_token`, `expires_in`,
    decoded `_payload`, and `_minted_at` (epoch seconds)."""
    body = {"client_id": CLIENT_ID, "grant_type": GRANT_TYPE}
    qs_url = f"{GSP_TOKEN_URL}?key={c.get_key()}"
    c._throttle()
    resp = _post_json(qs_url, body)
    if "access_token" not in resp:
        raise RuntimeError(f"unexpected token response: {resp}")
    resp["_minted_at"] = int(time.time())
    resp["_payload"] = _decode_jwt_payload(resp["access_token"])
    return resp


def get_token(*, force_refresh: bool = False) -> dict[str, Any]:
    """Return a cached token if still valid, otherwise mint and cache a new one.

    The cache is a plain JSON file under TARGET_TOKEN_CACHE_DIR (or a temp dir).
    """
    path = _cache_path()
    if not force_refresh and path.exists():
        try:
            cached = json.loads(path.read_text())
            exp = cached.get("_payload", {}).get("exp", 0)
            if exp - time.time() > EXPIRY_SKEW_S:
                return cached
        except (ValueError, KeyError, OSError):
            pass

    fresh = mint_token()
    try:
        path.write_text(json.dumps(fresh))
        # Tighten perms — token grants cart write access.
        os.chmod(path, 0o600)
    except OSError:
        pass
    return fresh


def add_cart_item(
    *,
    tcin: str,
    quantity: int,
    bearer: str,
    cart_id: str | None = None,
    cart_type: str = "REGULAR",
    channel: str = "WEB",
) -> dict[str, Any]:
    """Add one TCIN to the cart bound to the bearer token.

    Pass cart_id=None for the first item; reuse the returned `cart_id` for
    subsequent items so they all land in the same cart.
    """
    body: dict[str, Any] = {
        "cart_type": cart_type,
        "cart_item": {"tcin": str(tcin), "quantity": int(quantity), "channel": channel},
    }
    if cart_id:
        body["cart_id"] = cart_id
    url = f"{CARTS_BASE}/cart_items?key={c.get_key()}"
    c._throttle()
    return _post_json(url, body, bearer=bearer)


def transfer_url(token: str) -> str:
    """Build the browser handoff URL the user opens to receive the cart."""
    import urllib.parse
    return f"{CART_TRANSFER_BASE}?{urllib.parse.urlencode({'access_token': token})}"
