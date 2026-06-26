#!/usr/bin/env python3
"""
Questrade CLI - Interact with the Questrade API via OpenClaw skill.

Supports: server time, accounts, balances, positions, orders, executions,
          activities, symbol search/info, Level 1 quotes, historical candles,
          markets, and order placement/cancellation.

Authentication uses OAuth 2.0 refresh tokens.  The refresh token rotates on
every use — this script automatically saves the new token back to the
credentials file.
"""

import argparse
import json
import os
import sys
import warnings
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Optional
from zoneinfo import ZoneInfo

warnings.filterwarnings("ignore", message=".*NotOpenSSLWarning.*")
warnings.filterwarnings("ignore", category=Warning, module="urllib3")

try:
    import requests
except ImportError:
    print("Error: 'requests' package not installed.")
    print("Run: pip install requests")
    sys.exit(1)


# ─── Paths ────────────────────────────────────────────────────────────────────
CREDENTIALS_FILE = Path.home() / ".openclaw" / "credentials" / "questrade.json"
TOKEN_CACHE_FILE  = Path.home() / ".openclaw" / "data" / "questrade-token-cache.json"

# ─── Login endpoints ──────────────────────────────────────────────────────────
LOGIN_URL          = "https://login.questrade.com/oauth2/token"
PRACTICE_LOGIN_URL = "https://practicelogin.questrade.com/oauth2/token"

# ─── Eastern timezone (handles EST/EDT automatically) ─────────────────────────
_EASTERN = ZoneInfo("America/Toronto")

# ─── Credentials file cache (avoid reading the file multiple times per run) ───
_config_cache: Optional[dict] = None


def _load_config() -> dict:
    """Read credentials file once and cache the result for the process lifetime."""
    global _config_cache
    if _config_cache is None:
        if CREDENTIALS_FILE.exists():
            with open(CREDENTIALS_FILE) as f:
                _config_cache = json.load(f)
        else:
            _config_cache = {}
    return _config_cache


def _invalidate_config_cache() -> None:
    """Clear the config cache after a write so the next read is fresh."""
    global _config_cache
    _config_cache = None


def is_read_only() -> bool:
    """
    Return True if read-only mode is active.

    Set via environment variable:
        export QUESTRADE_READ_ONLY="true"

    Or in ~/.openclaw/credentials/questrade.json:
        { "readOnly": true, ... }

    When enabled, the 'order' and 'cancel-order' commands are blocked.
    """
    if os.environ.get("QUESTRADE_READ_ONLY", "").lower() == "true":
        return True
    return _load_config().get("readOnly", False)


def _eastern_iso(date_str: str, end_of_day: bool = False) -> str:
    """
    Convert a YYYY-MM-DD string to an ISO 8601 datetime with the correct
    Eastern timezone offset, respecting DST (EST = -05:00, EDT = -04:00).
    """
    time_part = "23:59:59" if end_of_day else "00:00:00"
    naive = datetime.fromisoformat(f"{date_str}T{time_part}")
    return naive.replace(tzinfo=_EASTERN).isoformat()


# ══════════════════════════════════════════════════════════════════════════════
# Authentication helpers
# ══════════════════════════════════════════════════════════════════════════════

def load_credentials():
    """
    Load Questrade credentials.

    Priority order:
    1. Credentials file (~/.openclaw/credentials/questrade.json) — always
       up-to-date because _save_refresh_token() writes the rotated token here.
    2. Environment variables — used only when the credentials file is absent
       or lacks a refreshToken.

    This ordering ensures that after token rotation the new refresh token
    (written to the credentials file) is used, even if the original token
    was provided via an env var.
    """
    refresh_token: Optional[str] = None
    practice = False

    # Prefer credentials file (always reflects latest rotated token)
    config        = _load_config()
    if config:
        refresh_token = config.get("refreshToken")
        practice      = config.get("practice", False)

    # Fall back to env vars
    if not refresh_token:
        refresh_token = os.environ.get("QUESTRADE_REFRESH_TOKEN")

    # Let env var override practice flag if explicitly set
    if os.environ.get("QUESTRADE_PRACTICE"):
        practice = os.environ["QUESTRADE_PRACTICE"].lower() == "true"

    if not refresh_token:
        print("Error: Questrade credentials not found.")
        print()
        print("Option 1 — environment variables:")
        print("  export QUESTRADE_REFRESH_TOKEN='your-refresh-token'")
        print("  export QUESTRADE_PRACTICE='false'   # or 'true' for practice account")
        print()
        print("Option 2 — credentials file (~/.openclaw/credentials/questrade.json):")
        print('  { "refreshToken": "your-refresh-token", "practice": false }')
        print()
        print("Generate a refresh token at: Questrade → App Hub → API Centre")
        sys.exit(1)

    return refresh_token, practice


def _save_refresh_token(new_token: str, practice: bool):
    """Persist a rotated refresh token back to the credentials file."""
    CREDENTIALS_FILE.parent.mkdir(parents=True, exist_ok=True)
    config = _load_config().copy()
    config["refreshToken"] = new_token
    config["practice"]     = practice
    if "readOnly" not in config:
        config["readOnly"] = False
    with open(CREDENTIALS_FILE, "w") as f:
        json.dump(config, f, indent=2)
    # Invalidate cache so the next _load_config() reads the updated file
    _invalidate_config_cache()
    # Keep in-process env in sync so subsequent calls don't re-read stale token
    os.environ["QUESTRADE_REFRESH_TOKEN"] = new_token


def get_access_token() -> tuple[str, str]:
    """
    Return (access_token, api_server).

    Uses a file-backed cache so we only call the token endpoint when the
    current access token has expired (they last ~30 minutes).
    """
    # ── Check cache ───────────────────────────────────────────────────────────
    if TOKEN_CACHE_FILE.exists():
        with open(TOKEN_CACHE_FILE) as f:
            cache = json.load(f)
        expires_at = datetime.fromisoformat(cache.get("expires_at", "2000-01-01T00:00:00+00:00"))
        if datetime.now(timezone.utc) < expires_at:
            return cache["access_token"], cache["api_server"]

    # ── Refresh ───────────────────────────────────────────────────────────────
    refresh_token, practice = load_credentials()
    login_url = PRACTICE_LOGIN_URL if practice else LOGIN_URL

    # Questrade docs show this as a GET with query params; POST with params= is
    # equivalent (params become the query string either way) and aligns with
    # RFC 6749 which recommends POST for token endpoints.
    resp = requests.post(
        login_url,
        params={"grant_type": "refresh_token", "refresh_token": refresh_token},
        timeout=15,
    )
    if not resp.ok:
        print(f"❌ Token refresh failed: {resp.status_code} — {resp.text}")
        sys.exit(1)

    data         = resp.json()
    access_token = data["access_token"]
    api_server   = data["api_server"].rstrip("/")
    expires_in   = data.get("expires_in", 1800)
    new_refresh  = data.get("refresh_token", refresh_token)

    # Questrade refresh tokens rotate — save the new one
    _save_refresh_token(new_refresh, practice)

    # Cache access token (subtract 60 s as buffer)
    TOKEN_CACHE_FILE.parent.mkdir(parents=True, exist_ok=True)
    expires_at = datetime.now(timezone.utc) + timedelta(seconds=max(expires_in - 60, 0))
    with open(TOKEN_CACHE_FILE, "w") as f:
        json.dump(
            {"access_token": access_token, "api_server": api_server,
             "expires_at": expires_at.isoformat()},
            f, indent=2,
        )

    return access_token, api_server


# ══════════════════════════════════════════════════════════════════════════════
# Low-level HTTP helpers
# ══════════════════════════════════════════════════════════════════════════════

def _auth() -> tuple:
    """Return (base_url, headers) with a single get_access_token() call."""
    access_token, api_server = get_access_token()
    return f"{api_server}/v1", {"Authorization": f"Bearer {access_token}"}


def api_get(path: str, params: Optional[dict] = None) -> dict:
    base, headers = _auth()
    resp = requests.get(f"{base}{path}", headers=headers, params=params, timeout=15)
    resp.raise_for_status()
    return resp.json()


def api_post(path: str, body: Optional[dict] = None) -> dict:
    base, headers = _auth()
    resp = requests.post(
        f"{base}{path}",
        headers={**headers, "Content-Type": "application/json"},
        json=body,
        timeout=15,
    )
    resp.raise_for_status()
    return resp.json()


def api_delete(path: str) -> dict:
    base, headers = _auth()
    resp = requests.delete(f"{base}{path}", headers=headers, timeout=15)
    resp.raise_for_status()
    return resp.json() if resp.content else {}


# ══════════════════════════════════════════════════════════════════════════════
# Command handlers
# ══════════════════════════════════════════════════════════════════════════════

def cmd_time(args):
    """Print current Questrade server time."""
    data = api_get("/time")
    print(f"Server Time: {data['time']}")


def cmd_accounts(args):
    """List all accounts linked to the token."""
    data     = api_get("/accounts")
    accounts = data.get("accounts", [])
    if not accounts:
        print("No accounts found.")
        return
    print(f"{'Number':<12} {'Type':<20} {'Status':<12} {'Primary'}")
    print("─" * 52)
    for a in accounts:
        primary = "✓" if a.get("isPrimary") else ""
        print(f"{a['number']:<12} {a['type']:<20} {a['status']:<12} {primary}")


def cmd_balances(args):
    """Display combined and per-currency balances for an account."""
    data      = api_get(f"/accounts/{args.account_id}/balances")
    combined  = data.get("combinedBalances", [])
    per_curr  = data.get("perCurrencyBalances", [])

    print("=== Combined Balances ===")
    for b in combined:
        print(f"  Currency        : {b['currency']}")
        print(f"  Cash            : ${b.get('cash', 0):>14,.2f}")
        print(f"  Market Value    : ${b.get('marketValue', 0):>14,.2f}")
        print(f"  Total Equity    : ${b.get('totalEquity', 0):>14,.2f}")
        print(f"  Buying Power    : ${b.get('buyingPower', 0):>14,.2f}")
        print(f"  Maintenance Exc : ${b.get('maintenanceExcess', 0):>14,.2f}")
        print()

    print("=== Per-Currency Balances ===")
    for b in per_curr:
        print(
            f"  {b['currency']:>4}  Cash ${b.get('cash', 0):>12,.2f} | "
            f"MV ${b.get('marketValue', 0):>12,.2f} | "
            f"Equity ${b.get('totalEquity', 0):>12,.2f}"
        )


def cmd_positions(args):
    """List all open positions in an account."""
    data      = api_get(f"/accounts/{args.account_id}/positions")
    positions = data.get("positions", [])
    if not positions:
        print("No open positions.")
        return

    print(
        f"{'Symbol':<12} {'Qty':>8} {'Avg Entry':>12} {'Current':>12} "
        f"{'Mkt Value':>12} {'Open P/L':>12} {'P/L %':>8}"
    )
    print("─" * 80)
    for p in positions:
        pl      = p.get("openPnl") or 0
        avg     = p.get("averageEntryPrice") or 0
        qty     = p.get("openQuantity") or 0
        current = p.get("currentPrice") or 0
        mv      = p.get("currentMarketValue") or 0
        pct     = (pl / (qty * avg) * 100) if qty and avg else 0
        pl_str  = f"${pl:,.2f}" if pl >= 0 else f"-${abs(pl):,.2f}"
        print(
            f"{p['symbol']:<12} {qty:>8.2f} ${avg:>10.2f} ${current:>10.2f} "
            f"${mv:>10,.2f} {pl_str:>12} {pct:>7.2f}%"
        )


def cmd_orders(args):
    """List orders for an account with optional state/date filtering."""
    params = {"stateFilter": args.state}
    if args.start:
        params["startTime"] = _eastern_iso(args.start)
    if args.end:
        params["endTime"]   = _eastern_iso(args.end, end_of_day=True)

    data   = api_get(f"/accounts/{args.account_id}/orders", params=params)
    orders = data.get("orders", [])
    if not orders:
        print("No orders found.")
        return

    print(
        f"{'ID':<10} {'Symbol':<12} {'Side':<6} {'Type':<12} "
        f"{'Qty':>8} {'Limit':>10} {'State':<14} {'TIF':<20}"
    )
    print("─" * 96)
    for o in orders:
        limit   = f"${o['limitPrice']:.4f}" if o.get("limitPrice") else "Market"
        print(
            f"{o['id']:<10} {o.get('symbol',''):<12} {o.get('side',''):<6} "
            f"{o.get('orderType',''):<12} {o.get('totalQuantity',0):>8.0f} "
            f"{limit:>10} {o.get('state',''):<14} {o.get('timeInForce',''):<20}"
        )


def cmd_order_detail(args):
    """Print full JSON detail for a single order."""
    data   = api_get(f"/accounts/{args.account_id}/orders/{args.order_id}")
    orders = data.get("orders", [])
    if not orders:
        print(f"Order {args.order_id} not found.")
        return
    print(json.dumps(orders[0], indent=2))


def cmd_executions(args):
    """List trade executions for an account."""
    params = {}
    if args.start:
        params["startTime"] = _eastern_iso(args.start)
    if args.end:
        params["endTime"]   = _eastern_iso(args.end, end_of_day=True)

    data       = api_get(f"/accounts/{args.account_id}/executions", params=params)
    executions = data.get("executions", [])
    if not executions:
        print("No executions found.")
        return

    print(f"{'Symbol':<12} {'Side':<6} {'Qty':>8} {'Price':>10} {'Timestamp':<22} {'OrderID':<10}")
    print("─" * 72)
    for e in executions:
        ts = (e.get("timestamp") or "")[:19].replace("T", " ")
        print(
            f"{e.get('symbol',''):<12} {e.get('side',''):<6} "
            f"{e.get('quantity',0):>8.0f} ${e.get('price',0):>8.2f} "
            f"{ts:<22} {e.get('orderId',''):<10}"
        )


def cmd_activities(args):
    """List account activities (dividends, deposits, trades, etc.)."""
    # Activities endpoint requires both startTime and endTime, max 30-day window.
    start_date = args.start
    end_date   = args.end or datetime.now(_EASTERN).strftime("%Y-%m-%d")

    start_dt = datetime.fromisoformat(start_date)
    end_dt   = datetime.fromisoformat(end_date)
    if (end_dt - start_dt).days > 30:
        print("❌ Activities endpoint maximum range is 30 days.")
        print(f"   Requested: {start_date} → {end_date} ({(end_dt - start_dt).days} days)")
        print("   Use --end to narrow the window.")
        sys.exit(1)

    params = {
        "startTime": _eastern_iso(start_date),
        "endTime"  : _eastern_iso(end_date, end_of_day=True),
    }

    data       = api_get(f"/accounts/{args.account_id}/activities", params=params)
    activities = data.get("activities", [])
    if not activities:
        print("No activities found.")
        return

    for a in activities:
        date = (a.get("tradeDate") or "")[:10]
        print(
            f"[{date}] {a.get('type',''):<16} {a.get('symbol',''):<10} "
            f"Qty:{a.get('quantity',0):>8.2f}  "
            f"Price:${a.get('price',0):>8.2f}  "
            f"Net:${a.get('netAmount',0):>10.2f}"
        )


def cmd_symbol_search(args):
    """Search for symbols by ticker prefix or company name."""
    params = {"prefix": args.query}
    if args.offset:
        params["offset"] = args.offset

    data    = api_get("/symbols/search", params=params)
    # API may return "symbols" (v2 behaviour) or "symbol" (documented v1 key)
    symbols = data.get("symbols") or data.get("symbol", [])
    if not symbols:
        print("No symbols found.")
        return

    print(f"{'Symbol':<12} {'ID':>10} {'Description':<38} {'Type':<12} {'Exchange'}")
    print("─" * 84)
    for s in symbols:
        desc = (s.get("description") or "")[:36]
        print(
            f"{s.get('symbol',''):<12} {s.get('symbolId',0):>10} "
            f"{desc:<38} {s.get('securityType',''):<12} "
            f"{s.get('listingExchange','')}"
        )


def cmd_symbol_info(args):
    """Get detailed info for a symbol by its Questrade integer ID."""
    data    = api_get(f"/symbols/{args.symbol_id}")
    symbols = data.get("symbols", [])
    if not symbols:
        print("Symbol not found.")
        return
    for s in symbols:
        print(json.dumps(s, indent=2))


def cmd_quote(args):
    """Get Level 1 market data for one or more Questrade symbol IDs."""
    ids_str = args.ids
    if "," in ids_str:
        # Multiple IDs: Questrade expects ?ids=ID1,ID2,... query parameter
        data = api_get("/markets/quotes", params={"ids": ids_str})
    else:
        # Single ID: use path parameter
        data = api_get(f"/markets/quotes/{ids_str}")
    quotes  = data.get("quotes", [])
    if not quotes:
        print("No quotes found.")
        return

    print(
        f"{'Symbol':<12} {'Bid':>10} {'Ask':>10} {'Last':>10} "
        f"{'Volume':>12} {'Open':>10} {'High':>10} {'Low':>10}"
    )
    print("─" * 88)
    for q in quotes:
        bid  = q.get("bidPrice")  or 0
        ask  = q.get("askPrice")  or 0
        last = q.get("lastTradePriceTrHrs") or q.get("lastTradePrice") or 0
        vol  = q.get("volume")    or 0
        o    = q.get("openPrice") or 0
        h    = q.get("highPrice") or 0
        lo   = q.get("lowPrice")  or 0
        print(
            f"{q.get('symbol',''):<12} ${bid:>8.2f} ${ask:>8.2f} "
            f"${last:>8.2f} {vol:>12,} ${o:>8.2f} ${h:>8.2f} ${lo:>8.2f}"
        )


def cmd_candles(args):
    """Fetch historical OHLCV candles for a symbol."""
    end_date = args.end or datetime.now().strftime("%Y-%m-%d")
    params   = {
        "startTime": f"{args.start}T00:00:00-05:00",
        "endTime"  : f"{end_date}T23:59:59-05:00",
        "interval" : args.interval,
    }

    data    = api_get(f"/markets/candles/{args.symbol_id}", params=params)
    candles = data.get("candles", [])
    if not candles:
        print("No candles found.")
        return

    print(f"{'Start':<20} {'Open':>10} {'High':>10} {'Low':>10} {'Close':>10} {'Volume':>12} {'VWAP':>10}")
    print("─" * 84)
    for c in candles:
        ts   = (c.get("start") or "")[:16].replace("T", " ")
        vwap = c.get("VWAP") or 0
        print(
            f"{ts:<20} ${c.get('open',0):>8.4f} ${c.get('high',0):>8.4f} "
            f"${c.get('low',0):>8.4f} ${c.get('close',0):>8.4f} "
            f"{c.get('volume',0):>12,} ${vwap:>8.4f}"
        )


def cmd_markets(args):
    """List all markets available through Questrade."""
    data    = api_get("/markets")
    markets = data.get("markets", [])
    if not markets:
        print("No markets found.")
        return

    def _time(iso: str) -> str:
        """Extract HH:MM from a full ISO timestamp."""
        return iso[11:16] if iso and len(iso) >= 16 else "—"

    print(f"{'Name':<8} {'Open (ET)':<12} {'Close (ET)':<12} {'Ext Start':<12} {'Ext End'}")
    print("─" * 60)
    for m in markets:
        print(
            f"{m.get('name',''):<8} "
            f"{_time(m.get('startTime','')):<12} "
            f"{_time(m.get('endTime','')):<12} "
            f"{_time(m.get('extendedStartTime','')):<12} "
            f"{_time(m.get('extendedEndTime',''))}"
        )


def cmd_place_order(args):
    """
    Place a new order.

    NOTE: Order placement requires Questrade *partner* API access.
    Read-only personal tokens will receive a 403 error.
    """
    if is_read_only():
        print("🔒 Read-only mode is enabled — order placement is blocked.")
        print("   To allow trades, set QUESTRADE_READ_ONLY=false or remove")
        print('   "readOnly": true from ~/.openclaw/credentials/questrade.json')
        sys.exit(1)

    side    = args.side.capitalize()   # "Buy" / "Sell"
    qty     = int(args.qty)
    o_type  = args.order_type          # "Market", "Limit", "Stop", "StopLimit"

    # ── Fetch live quote for guardrails ───────────────────────────────────────
    ask = bid = 0
    symbol_label = str(args.symbol_id)
    try:
        qdata  = api_get(f"/markets/quotes/{args.symbol_id}")
        quotes = qdata.get("quotes", [])
        if quotes:
            q            = quotes[0]
            ask          = q.get("askPrice") or 0
            bid          = q.get("bidPrice") or 0
            symbol_label = q.get("symbol", symbol_label)
    except Exception:
        pass  # Guardrails skipped if quote unavailable

    # ── Price sanity checks ───────────────────────────────────────────────────
    if o_type in ("Limit", "StopLimit") and args.limit_price:
        if side == "Buy" and ask > 0 and args.limit_price > ask and not args.force:
            print(f"⚠️  Warning: Buy limit ${args.limit_price:.4f} is ABOVE current ask ${ask:.4f}")
            if input("   Proceed anyway? (y/n): ").strip().lower() != "y":
                print("Order cancelled.")
                return
        elif side == "Sell" and bid > 0 and args.limit_price < bid and not args.force:
            print(f"⚠️  Warning: Sell limit ${args.limit_price:.4f} is BELOW current bid ${bid:.4f}")
            if input("   Proceed anyway? (y/n): ").strip().lower() != "y":
                print("Order cancelled.")
                return

    # ── Order summary + confirmation ──────────────────────────────────────────
    ref_price   = args.limit_price or ask or 0
    estimated   = qty * ref_price
    price_label = f"@ ${args.limit_price:.4f} limit" if args.limit_price else "@ MARKET"
    if args.stop_price:
        price_label += f"  stop ${args.stop_price:.4f}"

    print(f"\n📋 Order Summary:")
    print(f"   {side} {qty} × {symbol_label} (ID: {args.symbol_id}) {price_label}")
    print(f"   Type: {o_type}  |  TIF: {args.tif}  |  Account: {args.account_id}")
    if estimated:
        print(f"   Estimated notional: ${estimated:,.2f} {args.currency}")

    if not args.force:
        if input("   Confirm order? (y/n): ").strip().lower() != "y":
            print("Order cancelled.")
            return

    # ── Build request body ────────────────────────────────────────────────────
    body = {
        "accountNumber" : args.account_id,
        "symbolId"      : int(args.symbol_id),
        "quantity"      : qty,
        "icebergQuantity": qty,
        "action"        : side,
        "orderType"     : o_type,
        "timeInForce"   : args.tif,
        "primaryRoute"  : "AUTO",
        "secondaryRoute": "AUTO",
    }
    if args.limit_price:
        body["limitPrice"] = args.limit_price
    if args.stop_price:
        body["stopPrice"]  = args.stop_price

    result = api_post(f"/accounts/{args.account_id}/orders", body=body)
    orders = result.get("orders", [result])

    if orders:
        o = orders[0]
        print(f"\n✅ Order Placed!")
        print(f"   ID     : {o.get('id', 'N/A')}")
        print(f"   Symbol : {o.get('symbol', symbol_label)}")
        print(f"   State  : {o.get('state', 'N/A')}")
        print(f"   Qty    : {o.get('totalQuantity', qty)}")
    else:
        print("✅ Order submitted (no detail returned).")


def cmd_cancel_order(args):
    """Cancel an open order."""
    if is_read_only():
        print("🔒 Read-only mode is enabled — order cancellation is blocked.")
        print("   To allow trades, set QUESTRADE_READ_ONLY=false or remove")
        print('   "readOnly": true from ~/.openclaw/credentials/questrade.json')
        sys.exit(1)

    try:
        result = api_delete(f"/accounts/{args.account_id}/orders/{args.order_id}")
        print(f"✅ Order {args.order_id} cancelled.")
        if result:
            print(json.dumps(result, indent=2))
    except requests.exceptions.HTTPError as e:
        print(f"❌ Cancel failed: {e.response.status_code} — {e.response.text}")


# ══════════════════════════════════════════════════════════════════════════════
# Argument parser
# ══════════════════════════════════════════════════════════════════════════════

def main():
    parser     = argparse.ArgumentParser(
        prog="questrade_cli.py",
        description="Questrade OpenClaw CLI — query accounts, market data, and manage orders.",
    )
    subparsers = parser.add_subparsers(dest="command", metavar="COMMAND")

    # ── time ──────────────────────────────────────────────────────────────────
    subparsers.add_parser("time", help="Get Questrade server time")

    # ── accounts ──────────────────────────────────────────────────────────────
    subparsers.add_parser("accounts", help="List all linked accounts")

    # ── balances ──────────────────────────────────────────────────────────────
    p = subparsers.add_parser("balances", help="Show account balances")
    p.add_argument("account_id", help="Account number (e.g. 12345678)")

    # ── positions ─────────────────────────────────────────────────────────────
    p = subparsers.add_parser("positions", help="List open positions")
    p.add_argument("account_id", help="Account number")

    # ── orders ────────────────────────────────────────────────────────────────
    p = subparsers.add_parser("orders", help="List orders")
    p.add_argument("account_id", help="Account number")
    p.add_argument(
        "--state", default="Open",
        choices=["Open", "Closed", "All"],
        help="Filter by order state (default: Open)",
    )
    p.add_argument("--start", metavar="YYYY-MM-DD", help="Start date")
    p.add_argument("--end",   metavar="YYYY-MM-DD", help="End date")

    # ── order-detail ──────────────────────────────────────────────────────────
    p = subparsers.add_parser("order-detail", help="Get full detail for one order")
    p.add_argument("account_id", help="Account number")
    p.add_argument("order_id",   help="Order ID")

    # ── executions ────────────────────────────────────────────────────────────
    p = subparsers.add_parser("executions", help="List trade executions")
    p.add_argument("account_id", help="Account number")
    p.add_argument("--start", metavar="YYYY-MM-DD", help="Start date")
    p.add_argument("--end",   metavar="YYYY-MM-DD", help="End date")

    # ── activities ────────────────────────────────────────────────────────────
    p = subparsers.add_parser("activities", help="List account activities")
    p.add_argument("account_id", help="Account number")
    p.add_argument("--start", metavar="YYYY-MM-DD", help="Start date")
    p.add_argument("--end",   metavar="YYYY-MM-DD", help="End date")

    # ── symbol-search ─────────────────────────────────────────────────────────
    p = subparsers.add_parser("symbol-search", help="Search symbols by ticker prefix or name")
    p.add_argument("query",  help="Ticker prefix or company name (e.g. AAPL, Royal Bank)")
    p.add_argument("--offset", type=int, default=0, help="Pagination offset")

    # ── symbol-info ───────────────────────────────────────────────────────────
    p = subparsers.add_parser("symbol-info", help="Get full symbol details by Questrade symbol ID")
    p.add_argument("symbol_id", help="Questrade integer symbol ID")

    # ── quote ─────────────────────────────────────────────────────────────────
    p = subparsers.add_parser("quote", help="Get Level 1 quote(s) by symbol ID(s)")
    p.add_argument("ids", help="One or more comma-separated Questrade symbol IDs (e.g. 8049,38738)")

    # ── candles ───────────────────────────────────────────────────────────────
    INTERVALS = [
        "OneMinute", "TwoMinutes", "ThreeMinutes", "FourMinutes", "FiveMinutes",
        "TenMinutes", "FifteenMinutes", "TwentyMinutes", "HalfHour",
        "OneHour", "TwoHours", "FourHours",
        "OneDay", "OneWeek", "OneMonth", "OneYear",
    ]
    p = subparsers.add_parser("candles", help="Get historical OHLCV candles")
    p.add_argument("symbol_id",          help="Questrade symbol ID")
    p.add_argument("--start", required=True, metavar="YYYY-MM-DD", help="Start date")
    p.add_argument("--end",   metavar="YYYY-MM-DD", help="End date (default: today)")
    p.add_argument("--interval", default="OneDay", choices=INTERVALS,
                   help="Candle interval (default: OneDay)")

    # ── markets ───────────────────────────────────────────────────────────────
    subparsers.add_parser("markets", help="List available markets and their hours")

    # ── order (place) ─────────────────────────────────────────────────────────
    p = subparsers.add_parser(
        "order",
        help="Place an order (requires Questrade partner API access)",
    )
    p.add_argument("side",       choices=["buy", "sell"])
    p.add_argument("account_id", help="Account number")
    p.add_argument("symbol_id",  help="Questrade integer symbol ID")
    p.add_argument("qty",        type=int, help="Number of shares/units")
    p.add_argument("order_type", metavar="type",
                   choices=["Market", "Limit", "Stop", "StopLimit"])
    p.add_argument("--limit-price", type=float, dest="limit_price", help="Limit price")
    p.add_argument("--stop-price",  type=float, dest="stop_price",  help="Stop price")
    p.add_argument("--tif", default="Day",
                   choices=["Day", "GoodTillCanceled", "ImmediateOrCancel", "FillOrKill"],
                   help="Time-in-force (default: Day)")
    p.add_argument("--currency", default="CAD", choices=["CAD", "USD"],
                   help="Display currency for cost estimate (default: CAD)")
    p.add_argument("--force", action="store_true",
                   help="Skip price-sanity warnings and confirmation prompt")

    # ── cancel-order ─────────────────────────────────────────────────────────
    p = subparsers.add_parser("cancel-order", help="Cancel an open order")
    p.add_argument("account_id", help="Account number")
    p.add_argument("order_id",   help="Order ID to cancel")

    # ── Dispatch ──────────────────────────────────────────────────────────────
    args = parser.parse_args()
    if not args.command:
        parser.print_help()
        return

    COMMANDS = {
        "time"         : cmd_time,
        "accounts"     : cmd_accounts,
        "balances"     : cmd_balances,
        "positions"    : cmd_positions,
        "orders"       : cmd_orders,
        "order-detail" : cmd_order_detail,
        "executions"   : cmd_executions,
        "activities"   : cmd_activities,
        "symbol-search": cmd_symbol_search,
        "symbol-info"  : cmd_symbol_info,
        "quote"        : cmd_quote,
        "candles"      : cmd_candles,
        "markets"      : cmd_markets,
        "order"        : cmd_place_order,
        "cancel-order" : cmd_cancel_order,
    }

    try:
        COMMANDS[args.command](args)
    except requests.exceptions.HTTPError as e:
        code = e.response.status_code
        body = e.response.text
        print(f"❌ API Error {code}: {body}")
        if code == 401:
            print("   Hint: delete ~/.openclaw/data/questrade-token-cache.json to force a token refresh.")
        elif code == 403:
            print("   Hint: if calling quotes/candles — your token may lack market data scope.")
            print("         Check your Questrade API Centre for enabled scopes.")
            print("         If placing orders — partner API access is required.")
        sys.exit(1)
    except requests.exceptions.ConnectionError:
        print("❌ Connection error. Check your internet connection.")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\nCancelled.")
        sys.exit(0)


if __name__ == "__main__":
    main()

