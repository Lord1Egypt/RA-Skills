"""
Authentication for TradingView.

Two modes:
  1. Anonymous  — No account needed. Works immediately.
                  Free-tier bar limits apply (6.5k 1min, 10.8k 1h, full daily).
  2. Token      — Provide your auth token from the browser.
                  Unlocks more bars if you have a paid plan (Essential/Plus/Premium).

To get your token:
  Option A (cookies):
    1. Log in to tradingview.com
    2. Open DevTools (F12) -> Console
    3. Run: document.cookie.split('; ').find(c=>c.startsWith('auth_token=')).split('=').slice(1).join('=')
    4. Copy the JWT string

  Option B (WebSocket traffic):
    1. Open tradingview.com/chart in browser
    2. DevTools -> Network -> WS filter -> click the data.tradingview.com connection
    3. Find the set_auth_token message -> copy the token
"""

from __future__ import annotations

import json as _json
import logging

import httpx

from tvfetch.exceptions import TvAuthError

log = logging.getLogger(__name__)

ANONYMOUS_TOKEN = "unauthorized_user_token"
_SIGNIN_URL = "https://www.tradingview.com/accounts/signin/"
_SIGNIN_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    "Referer": "https://www.tradingview.com/",
    "Content-Type": "application/x-www-form-urlencoded",
    "X-Language": "en",
}


def anonymous_token() -> str:
    """Return the anonymous access token. No account required."""
    return ANONYMOUS_TOKEN


def is_anonymous(token: str) -> bool:
    return token == ANONYMOUS_TOKEN


def login(username: str, password: str) -> str:
    """
    Log in to TradingView and return a JWT auth token.

    Raises TvAuthError if credentials are wrong or CAPTCHA is required.
    Note: If CAPTCHA is triggered, use the browser method instead.
    """
    log.debug("Attempting login for user: %s", username)
    try:
        resp = httpx.post(
            _SIGNIN_URL,
            data={"username": username, "password": password, "remember": "on"},
            headers=_SIGNIN_HEADERS,
            timeout=15,
            follow_redirects=True,
        )
    except httpx.RequestError as exc:
        raise TvAuthError(f"Login request failed: {exc}") from exc

    if resp.status_code != 200:
        raise TvAuthError(f"Login returned HTTP {resp.status_code}")

    try:
        data = resp.json()
    except _json.JSONDecodeError:
        raise TvAuthError("Login returned non-JSON response. TradingView may have changed their API.")

    # CAPTCHA challenge
    if "challenge" in data or data.get("error") == "captcha_required":
        raise TvAuthError(
            "TradingView requires CAPTCHA verification. "
            "Please use the browser method to get your auth token instead:\n"
            "  1. Log in at tradingview.com\n"
            "  2. Open DevTools -> Console\n"
            "  3. Run: document.cookie.split('; ').find(c=>c.startsWith('auth_token=')).split('=').slice(1).join('=')\n"
            "  4. Pass the result with --token or TvClient(auth_token='...')"
        )

    # Wrong credentials
    if "error" in data:
        raise TvAuthError(f"Login failed: {data['error']}")

    token = data.get("user", {}).get("auth_token")
    if not token:
        raise TvAuthError(
            "Login succeeded but auth_token not found in response. "
            "TradingView may have changed their API format."
        )

    log.debug("Login successful, token acquired")
    return token
