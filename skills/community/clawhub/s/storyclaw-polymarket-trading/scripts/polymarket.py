#!/usr/bin/env python3
"""
Polymarket Trading Bot
Fast-loop near-expiry conviction trading for Polymarket CLOB markets.

Commands:
  check                          - Check credentials and connectivity
  fast [coin] [5m|15m]           - List current fast-loop markets (BTC/ETH/SOL/XRP, computed from time)
  markets [keyword]              - Search active markets by keyword
  book <token_id>                - Show orderbook for a token
  signal <token_id>              - Score conviction signal (imbalance + spread)
  trade <token_id> <side> <size> [price] - Place a limit or market order
  positions                      - Show open positions
  orders                         - Show open orders
  cancel <order_id>              - Cancel an order
  cancel-all                     - Cancel all open orders
  history                        - Recent trade history
  pnl                            - Realized P&L summary by market
  settle                         - Check pending dry-run orders, resolve settled markets, update P&L
  setup                          - Interactive API key setup
"""

import sys
import os
import json
import time
import math

# ─── Config Loader ───────────────────────────────────────────────────────────

SKILL_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CREDENTIALS_DIR = os.path.join(SKILL_DIR, "credentials")
STATE_DIR = os.path.join(SKILL_DIR, "state")

os.makedirs(CREDENTIALS_DIR, exist_ok=True)
os.makedirs(STATE_DIR, exist_ok=True)


def load_config(exit_on_missing=True):
    user_id = os.environ.get("USER_ID") or os.environ.get("TELEGRAM_USER_ID")
    if not user_id:
        if exit_on_missing:
            print("❌ USER_ID or TELEGRAM_USER_ID environment variable required")
            print("   Set it: USER_ID=1234567890 python3 polymarket.py ...")
            sys.exit(1)
        return None, None

    cred_path = os.path.join(CREDENTIALS_DIR, f"{user_id}.json")
    if not os.path.exists(cred_path):
        if exit_on_missing:
            print(f"❌ No config found for user {user_id}")
            print(f"   Run: python3 polymarket.py setup")
            sys.exit(1)
        return None, user_id

    with open(cred_path) as f:
        config = json.load(f)
    return config, user_id


def save_config(user_id, config):
    cred_path = os.path.join(CREDENTIALS_DIR, f"{user_id}.json")
    with open(cred_path, "w") as f:
        json.dump(config, f, indent=2)
    os.chmod(cred_path, 0o600)
    print(f"✅ Config saved to {cred_path}")


def get_state_path(user_id):
    return os.path.join(STATE_DIR, f"{user_id}.state.json")


def load_state(user_id):
    p = get_state_path(user_id)
    if os.path.exists(p):
        with open(p) as f:
            return json.load(f)
    return {}


def save_state(user_id, state):
    with open(get_state_path(user_id), "w") as f:
        json.dump(state, f, indent=2)


# ─── Client Setup ─────────────────────────────────────────────────────────────

HOST = "https://clob.polymarket.com"
CHAIN_ID = 137  # Polygon mainnet


def get_client(level=2):
    """Build py-clob-client. level=0: public only, 1: L1 auth, 2: full trading."""
    try:
        from py_clob_client.client import ClobClient
        from py_clob_client.clob_types import ApiCreds
    except ImportError:
        print("❌ py-clob-client not installed")
        print("   Run: pip3 install py-clob-client --break-system-packages")
        sys.exit(1)

    config, user_id = load_config(exit_on_missing=(level > 0))

    if level == 0:
        return ClobClient(HOST), None

    private_key = config.get("private_key")
    if not private_key:
        print("❌ private_key not in config")
        sys.exit(1)

    if level == 1 or not config.get("api_key"):
        client = ClobClient(HOST, chain_id=CHAIN_ID, key=private_key)
        return client, user_id

    # Level 2: full trading
    creds = ApiCreds(
        api_key=config["api_key"],
        api_secret=config["api_secret"],
        api_passphrase=config["api_passphrase"],
    )
    funder = config.get("funder_address")
    client = ClobClient(
        HOST,
        chain_id=CHAIN_ID,
        key=private_key,
        creds=creds,
        funder=funder,
    )
    return client, user_id


# ─── Commands ─────────────────────────────────────────────────────────────────


def cmd_check():
    """Check credentials and connectivity."""
    config, user_id = load_config(exit_on_missing=False)

    if config is None:
        print("⚠️  No credentials configured")
        print("   Run: python3 polymarket.py setup")
        return

    print(f"👤 User: {user_id}")
    print(f"   Private key: {'✅ configured' if config.get('private_key') else '❌ missing'}")
    print(f"   API key:     {'✅ configured' if config.get('api_key') else '❌ missing (run setup --derive-api-key)'}")
    print(f"   Funder:      {config.get('funder_address', '(not set)')}")
    print(f"   Dry run:     {config.get('dry_run', True)}")

    # Test public connectivity
    try:
        client, _ = get_client(level=0)
        resp = client.get_ok()
        print(f"\n🌐 CLOB API: ✅ reachable ({resp})")
    except Exception as e:
        print(f"\n🌐 CLOB API: ❌ {e}")

    # Test auth if available
    if config.get("api_key"):
        try:
            client, _ = get_client(level=2)
            balance = client.get_balance_allowance(params={"asset_type": "COLLATERAL"})
            print(f"💰 USDC Balance: {balance.get('balance', '?')}")
        except Exception as e:
            print(f"🔐 Auth test: ❌ {e}")


def _parse_gamma_market(m):
    """Parse a Gamma API market dict into (question, slug, end_date, token_ids, outcomes)."""
    q = m.get("question", "") or ""
    slug = m.get("slug", "") or ""
    end_date = m.get("endDate", "?")

    clob_raw = m.get("clobTokenIds", "[]")
    clob_token_ids = json.loads(clob_raw) if isinstance(clob_raw, str) else clob_raw

    out_raw = m.get("outcomes", '["Up","Down"]')
    outcomes = json.loads(out_raw) if isinstance(out_raw, str) else out_raw

    return q, slug, end_date, clob_token_ids, outcomes


def _gamma_fetch(slug):
    """Fetch a single market from Gamma API by exact slug. Returns market dict or None."""
    import urllib.request
    url = f"https://gamma-api.polymarket.com/markets?slug={slug}&limit=1"
    headers = {
        "Accept": "application/json",
        "User-Agent": "Mozilla/5.0 (compatible; polymarket-bot)",
        "Origin": "https://polymarket.com",
    }
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=8) as r:
            data = json.loads(r.read())
        if data:
            return data[0]
    except Exception:
        pass
    return None


def cmd_fast_markets(coin=None, timeframe=None):
    """
    Fetch currently active fast-loop markets by computing their slugs from current time.

    Slug pattern: {coin}-updown-{5m|15m}-{unix_timestamp_of_interval_start}
    The timestamp is floored to the nearest interval boundary (5min or 15min).

    Supported coins: btc, eth, sol, xrp
    """
    now = int(time.time())

    coins = [coin.lower()] if coin else ["btc", "eth", "sol", "xrp"]
    timeframes = [timeframe] if timeframe else ["5m", "15m"]

    results = []
    print(f"⏰ Current UTC time: {time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(now))}\n")

    for tf in timeframes:
        interval = 300 if tf == "5m" else 900  # seconds
        # Current interval start
        t_current = (now // interval) * interval
        # Next interval start
        t_next = t_current + interval
        seconds_remaining = t_next - now

        print(f"── {tf.upper()} markets ──────────────────────────────")
        print(f"   Current interval: T+{seconds_remaining}s remaining")

        for c in coins:
            # Try current interval first, then next (in case current just expired)
            for t in [t_current, t_next]:
                slug = f"{c}-updown-{tf}-{t}"
                m = _gamma_fetch(slug)
                if m:
                    q, _, end_date, token_ids, outcomes = _parse_gamma_market(m)
                    label = "CURRENT" if t == t_current else "NEXT"
                    print(f"\n   📌 [{label}] {q[:60]}")
                    print(f"      Slug:  {slug}")
                    print(f"      Ends:  {end_date}")
                    for i, tid in enumerate(token_ids):
                        out = outcomes[i] if i < len(outcomes) else f"Outcome {i}"
                        print(f"      [{out}] token_id={tid}")
                    results.append({"slug": slug, "token_ids": token_ids, "outcomes": outcomes, "question": q})
                    break  # found a valid one, don't try next timestamp
                # else: slug not found (market may not have been created yet)

    if not results:
        print("\n⚠️  No fast markets found. They may not be live yet or slug pattern changed.")

    return results


def cmd_markets(keyword=None):
    """
    Search active markets via Gamma REST API by keyword.
    For fast-loop 5m/15m markets, use: python3 polymarket.py fast [coin] [timeframe]
    """
    import urllib.request

    if not keyword:
        # Default to fast markets if no keyword given
        print("No keyword given — showing fast-loop markets instead.")
        print("Tip: use 'python3 polymarket.py fast' for 5m/15m crypto markets\n")
        return cmd_fast_markets()

    base_url = "https://gamma-api.polymarket.com/markets"
    params = f"limit=30&active=true&closed=false&keyword={urllib.request.quote(keyword)}"
    headers = {
        "Accept": "application/json",
        "User-Agent": "Mozilla/5.0 (compatible; polymarket-bot)",
        "Origin": "https://polymarket.com",
    }

    results = []
    try:
        req = urllib.request.Request(f"{base_url}?{params}", headers=headers)
        with urllib.request.urlopen(req, timeout=10) as r:
            markets = json.loads(r.read())
    except Exception as e:
        print(f"❌ Gamma API failed: {e}")
        return results

    for m in (markets or []):
        q, slug, end_date, clob_token_ids, outcomes = _parse_gamma_market(m)
        print(f"\n📌 {q[:75]}")
        print(f"   Slug:    {slug[:60]}")
        print(f"   Ends:    {end_date}")
        for i, tid in enumerate(clob_token_ids):
            outcome = outcomes[i] if i < len(outcomes) else f"Outcome {i}"
            print(f"   [{outcome}] token_id={tid}")
        results.append(m)

    if not results:
        print(f"\nNo active markets found for: {keyword}")

    return results


def cmd_book(token_id):
    """Show current orderbook for a token."""
    client, _ = get_client(level=0)
    try:
        book = client.get_order_book(token_id)
    except Exception as e:
        print(f"❌ Failed to get orderbook: {e}")
        return

    bids = book.bids or []
    asks = book.asks or []

    print(f"\n📖 Orderbook for {token_id[:12]}...")
    print(f"   Token: {token_id}")

    if asks:
        print(f"\n   ASKS (sell orders):")
        for a in sorted(asks, key=lambda x: float(x.price))[:5]:
            print(f"     {float(a.price):.4f}  x  {float(a.size):.2f}")

    spread = None
    if bids and asks:
        best_bid = max(float(b.price) for b in bids)
        best_ask = min(float(a.price) for a in asks)
        spread = best_ask - best_bid
        mid = (best_bid + best_ask) / 2
        print(f"\n   ─── spread={spread:.4f}  mid={mid:.4f} ───")

    if bids:
        print(f"\n   BIDS (buy orders):")
        for b in sorted(bids, key=lambda x: float(x.price), reverse=True)[:5]:
            print(f"     {float(b.price):.4f}  x  {float(b.size):.2f}")

    return book


def cmd_signal(token_id):
    """
    Score conviction signal for a token.
    Uses orderbook imbalance + spread dynamics.
    Returns: BUY / SELL / PASS with score and reasoning.
    """
    client, _ = get_client(level=0)
    try:
        book = client.get_order_book(token_id)
        mid_resp = client.get_midpoint(token_id)
        spread_resp = client.get_spread(token_id)
    except Exception as e:
        print(f"❌ Failed to fetch data: {e}")
        return

    bids = book.bids or []
    asks = book.asks or []

    if not bids or not asks:
        print("⚠️  Thin market - insufficient liquidity for signal")
        return

    # ── Imbalance Score ──────────────────────────────────────────
    bid_vol = sum(float(b.size) for b in bids)
    ask_vol = sum(float(a.size) for a in asks)
    total_vol = bid_vol + ask_vol
    imbalance = (bid_vol - ask_vol) / total_vol if total_vol > 0 else 0
    # +1.0 = all bids (bullish), -1.0 = all asks (bearish)

    # ── Spread Score ─────────────────────────────────────────────
    # Both mid and spread return dicts: {"mid": "0.5"}, {"spread": "0.02"}
    try:
        if isinstance(spread_resp, dict):
            spread_val = float(spread_resp.get("spread", 0))
        else:
            spread_val = float(getattr(spread_resp, "spread", 0))
    except Exception:
        spread_val = 0.0

    try:
        if isinstance(mid_resp, dict):
            mid_val = float(mid_resp.get("mid", 0.5))
        else:
            mid_val = float(getattr(mid_resp, "mid", 0.5))
    except Exception:
        mid_val = 0.5

    # Tight spread = liquid = better edge
    spread_score = max(0, 1 - spread_val / 0.05)  # normalize: 0.05 = "wide"

    # ── Near-expiry time decay ────────────────────────────────────
    # For near-expiry markets: high conviction + price near 0 or 1 is better
    edge_to_extreme = max(abs(mid_val - 0.0), abs(mid_val - 1.0))
    # price near 0 or 1 → higher conviction
    conviction_score = edge_to_extreme if edge_to_extreme > 0.7 else 0.0

    # ── Final Score ───────────────────────────────────────────────
    final = (imbalance * 0.5) + (spread_score * 0.3) + (conviction_score * 0.2)

    print(f"\n🎯 Signal Analysis for {token_id[:16]}...")
    print(f"   Mid price:      {mid_val:.4f}")
    print(f"   Spread:         {spread_val:.4f}")
    print(f"   Bid vol:        {bid_vol:.2f}")
    print(f"   Ask vol:        {ask_vol:.2f}")
    print(f"   Imbalance:      {imbalance:+.3f}  (>0 = buy pressure)")
    print(f"   Spread score:   {spread_score:.3f}  (1=tight, 0=wide)")
    print(f"   Conviction:     {conviction_score:.3f}  (price near 0/1)")
    print(f"   Final score:    {final:+.3f}")
    print()

    THRESHOLD = 0.15
    if final > THRESHOLD:
        print(f"   ✅ SIGNAL: BUY  (score {final:+.3f} > threshold {THRESHOLD})")
    elif final < -THRESHOLD:
        print(f"   ✅ SIGNAL: SELL (score {final:+.3f} < -{THRESHOLD})")
    else:
        print(f"   ⏸  SIGNAL: PASS (score {final:+.3f} within ±{THRESHOLD})")

    return {
        "token_id": token_id,
        "mid": mid_val,
        "spread": spread_val,
        "imbalance": imbalance,
        "final_score": final,
        "signal": "BUY" if final > THRESHOLD else ("SELL" if final < -THRESHOLD else "PASS"),
    }


def cmd_trade(token_id, side, size, price=None):
    """
    Place an order. side=BUY|SELL, size=USDC notional.
    If price is omitted → market order.
    """
    config, user_id = load_config()
    dry_run = config.get("dry_run", True)

    from py_clob_client.clob_types import OrderArgs, MarketOrderArgs
    from py_clob_client.order_builder.builder import BUY, SELL

    side_const = BUY if side.upper() == "BUY" else SELL
    size = float(size)

    if dry_run:
        print(f"🧪 DRY RUN - Would place order:")
        print(f"   Side:     {side.upper()}")
        print(f"   Token:    {token_id[:20]}...")
        print(f"   Size:     {size}")
        print(f"   Price:    {price or 'market'}")
        print(f"\n   To execute for real: set dry_run=false in credentials/{user_id}.json")
        return

    client, _ = get_client(level=2)

    try:
        if price is None:
            # Market order
            order_args = MarketOrderArgs(
                token_id=token_id,
                amount=size,
                price=None,
            )
            resp = client.create_market_order(order_args)
        else:
            price = float(price)
            # Get tick size first
            tick_size = client.get_tick_size(token_id)
            neg_risk = client.get_neg_risk(token_id)

            order_args = OrderArgs(
                token_id=token_id,
                price=price,
                size=size,
                side=side_const,
            )
            signed_order = client.create_order(order_args)
            resp = client.post_order(signed_order, orderType="GTC")

        print(f"✅ Order placed!")
        print(f"   Order ID: {resp.get('orderID', resp.get('id', '?'))}")
        print(f"   Status:   {resp.get('status', '?')}")

        # Save to state
        state = load_state(user_id)
        orders = state.get("orders", [])
        orders.append({
            "ts": int(time.time()),
            "token_id": token_id,
            "side": side.upper(),
            "size": size,
            "price": price,
            "resp": resp,
        })
        state["orders"] = orders[-50:]  # keep last 50
        save_state(user_id, state)

        return resp

    except Exception as e:
        print(f"❌ Order failed: {e}")
        sys.exit(1)


def cmd_positions():
    """Show open positions (token holdings)."""
    client, user_id = get_client(level=2)
    try:
        resp = client.get_orders(params={"status": "LIVE"})
        if not resp:
            print("📦 No open positions")
            return

        print("📦 Open Positions:")
        for pos in resp:
            print(f"  Token: {pos.get('asset_id', '?')[:20]}...")
            print(f"    Side:  {pos.get('side', '?')}")
            print(f"    Size:  {pos.get('size', '?')}")
            print(f"    Price: {pos.get('price', '?')}")
            print(f"    ID:    {pos.get('id', '?')}")
            print()
    except Exception as e:
        print(f"❌ Failed: {e}")


def cmd_orders():
    """Show open orders."""
    client, user_id = get_client(level=2)
    try:
        resp = client.get_orders(params={"status": "LIVE"})
        if not resp:
            print("📋 No open orders")
            return

        print("📋 Open Orders:")
        for o in resp:
            print(f"  [{o.get('side', '?')}] token={o.get('asset_id', '?')[:16]}...")
            print(f"    size={o.get('size', '?')}  price={o.get('price', '?')}")
            print(f"    id={o.get('id', '?')}")
            print()
    except Exception as e:
        print(f"❌ Failed: {e}")


def cmd_cancel(order_id):
    """Cancel a specific order."""
    client, _ = get_client(level=2)
    try:
        resp = client.cancel(order_id=order_id)
        print(f"✅ Cancelled: {order_id}")
        return resp
    except Exception as e:
        print(f"❌ Cancel failed: {e}")


def cmd_cancel_all():
    """Cancel all open orders."""
    client, _ = get_client(level=2)
    try:
        resp = client.cancel_all()
        print(f"✅ All orders cancelled")
        return resp
    except Exception as e:
        print(f"❌ Cancel-all failed: {e}")


def cmd_history():
    """Show recent trade history."""
    client, user_id = get_client(level=2)
    try:
        from py_clob_client.clob_types import TradeParams
        trades = client.get_trades(params=TradeParams(maker_address=client.get_address()))
        if not trades:
            print("📜 No trade history")
            return

        print("📜 Recent Trades:")
        for t in (trades or [])[:10]:
            ts = t.get("created_at", "?")[:16]
            side = t.get("side", "?")
            size = t.get("size", "?")
            price = t.get("price", "?")
            market = t.get("asset_id", "?")[:16]
            print(f"  [{ts}] {side} {size} @ {price} | {market}...")
    except Exception as e:
        print(f"❌ Failed: {e}")


def cmd_pnl():
    """
    Show realized P&L summary from trade history.
    Groups trades by token (market), computes per-market net P&L:
      - BUY trades: cost = size * price
      - SELL trades: revenue = size * price
      - Net P&L = revenue - cost  (positive = profit)
    For binary markets that settled at 1.0 (win) or 0.0 (loss),
    this accurately reflects what you made or lost.
    """
    client, user_id = get_client(level=2)
    try:
        from py_clob_client.clob_types import TradeParams
        trades = client.get_trades(params=TradeParams(maker_address=client.get_address()))
    except Exception as e:
        print(f"❌ Failed to fetch trades: {e}")
        return

    if not trades:
        print("📊 No trades found")
        return

    # Group by asset_id (token)
    markets = {}
    for t in trades:
        token = t.get("asset_id", "unknown")
        side = t.get("side", "").upper()
        try:
            size = float(t.get("size", 0))
            price = float(t.get("price", 0))
        except (ValueError, TypeError):
            continue
        notional = size * price

        if token not in markets:
            markets[token] = {"buy_cost": 0.0, "sell_revenue": 0.0, "trades": 0, "last_ts": ""}
        m = markets[token]
        m["trades"] += 1
        m["last_ts"] = max(m["last_ts"], t.get("created_at", ""))
        if side == "BUY":
            m["buy_cost"] += notional
        else:
            m["sell_revenue"] += notional

    # Compute P&L per market
    rows = []
    for token, m in markets.items():
        net = m["sell_revenue"] - m["buy_cost"]
        rows.append((token, m["buy_cost"], m["sell_revenue"], net, m["trades"], m["last_ts"]))

    # Sort by most recent activity
    rows.sort(key=lambda r: r[5], reverse=True)

    total_cost = sum(r[1] for r in rows)
    total_rev = sum(r[2] for r in rows)
    total_net = total_rev - total_cost
    open_cost = sum(r[1] - r[2] for r in rows if r[1] > r[2])  # positions not fully sold

    print(f"\n📊 Polymarket P&L Summary ({len(rows)} markets, {sum(r[4] for r in rows)} trades)")
    print("─" * 70)
    print(f"  {'Token':<20}  {'Bought':>10}  {'Sold':>10}  {'Net P&L':>10}  Trades")
    print("─" * 70)

    for token, cost, rev, net, n_trades, ts in rows[:20]:
        sign = "+" if net >= 0 else ""
        emoji = "🟢" if net > 0 else ("🔴" if net < 0 else "⚪")
        date = ts[:10] if ts else "?"
        print(f"  {emoji} {token[:18]:<18}  ${cost:>8.2f}  ${rev:>8.2f}  {sign}${net:>8.2f}  {n_trades}  [{date}]")

    print("─" * 70)
    total_sign = "+" if total_net >= 0 else ""
    print(f"  {'TOTAL':<20}  ${total_cost:>8.2f}  ${total_rev:>8.2f}  {total_sign}${total_net:>8.2f}")
    print()
    if open_cost > 0:
        print(f"  ⚠️  ~${open_cost:.2f} in open/unsettled positions (buy > sell)")
    print(f"  Realized P&L: {total_sign}${total_net:.2f} USDC")

    return rows


def cmd_settle():
    """
    Check all pending dry-run orders and settle ones whose market has resolved.

    Resolution detection: after end_ts, query the token's midpoint.
      - mid > 0.95  → resolved YES/Up  (winner)
      - mid < 0.05  → resolved NO/Down (loser)
      - otherwise   → still pending or not yet resolved

    P&L calculation:
      BUY at entry_price, resolves to 1.0 → profit = (1.0 - entry_price) * size
      BUY at entry_price, resolves to 0.0 → loss   = entry_price * size
    """
    perf_path_template = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        "state", "{user_id}.performance.json"
    )

    # Load config to find user_id
    config, user_id = load_config(exit_on_missing=False)
    if not user_id:
        user_id = os.environ.get("USER_ID") or os.environ.get("TELEGRAM_USER_ID")
    if not user_id:
        print("❌ USER_ID required")
        return

    perf_path = perf_path_template.format(user_id=user_id)
    if not os.path.exists(perf_path):
        print("📊 No performance file found — no dry-run orders recorded yet")
        return

    with open(perf_path) as f:
        perf = json.load(f)

    # migrate old format
    if "trades" in perf and "pending" not in perf:
        perf["pending"] = []
        perf["settled"] = perf.pop("trades", [])
    perf.setdefault("pending", [])
    perf.setdefault("settled", [])
    perf.setdefault("stats", {"total_trades": 0, "winning_trades": 0, "losing_trades": 0, "total_pnl": 0.0, "win_rate": 0.0})

    pending = perf["pending"]
    now = int(time.time())
    newly_settled = []
    still_pending = []

    client, _ = get_client(level=0)

    for order in pending:
        end_ts = order.get("end_ts")
        token_id = order.get("token_id")

        # Not yet expired
        if end_ts and now < end_ts:
            remaining = end_ts - now
            print(f"⏳ {order['name']} [{order['id']}] — {remaining//60}m {remaining%60}s remaining")
            still_pending.append(order)
            continue

        # Expired — check resolution via midpoint first, fall back to Gamma API
        resolution = None
        try:
            mid_resp = client.get_midpoint(token_id)
            mid = float(mid_resp.get("mid", 0.5) if isinstance(mid_resp, dict) else getattr(mid_resp, "mid", 0.5))
            if mid > 0.95:
                resolution = 1.0
            elif mid < 0.05:
                resolution = 0.0
        except Exception:
            pass

        # Gamma API fallback: outcomePrices has final settlement values
        if resolution is None:
            try:
                import urllib.request
                url = f"https://gamma-api.polymarket.com/markets?clob_token_ids={token_id}"
                req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
                with urllib.request.urlopen(req, timeout=8) as resp:
                    gamma_data = json.loads(resp.read())
                if gamma_data:
                    gm = gamma_data[0]
                    outcome_prices = json.loads(gm.get("outcomePrices", "[]"))
                    clob_ids = json.loads(gm.get("clobTokenIds", "[]"))
                    if token_id in clob_ids and outcome_prices:
                        idx = clob_ids.index(token_id)
                        price = float(outcome_prices[idx])
                        if price > 0.95:
                            resolution = 1.0
                        elif price < 0.05:
                            resolution = 0.0
            except Exception:
                pass

        if resolution is None:
            print(f"⏳ {order['name']} [{order['id']}] — expired but resolution unclear, will retry next run")
            still_pending.append(order)
            continue

        # Calculate P&L
        entry = order.get("entry_price", 0.5)
        size = order.get("size", 10)
        side = order.get("side", "BUY")

        if side == "BUY":
            pnl = (resolution - entry) * size
        else:  # SELL
            pnl = (entry - resolution) * size

        won = pnl > 0
        settled_order = {**order, "resolved": True, "resolution": resolution, "exit_price": resolution, "pnl": round(pnl, 4)}
        newly_settled.append(settled_order)
        perf["settled"].append(settled_order)

        emoji = "🟢" if won else "🔴"
        sign = "+" if pnl >= 0 else ""
        print(f"{emoji} {order['name']} [{order['id']}]  entry={entry:.4f} → resolution={resolution:.1f}  P&L: {sign}{pnl:.2f} USDC")

    perf["pending"] = still_pending

    # Recompute stats from all settled orders
    settled = perf["settled"]
    total = len(settled)
    wins = sum(1 for o in settled if o.get("pnl", 0) > 0)
    total_pnl = sum(o.get("pnl", 0) for o in settled)
    perf["stats"] = {
        "total_trades": total,
        "winning_trades": wins,
        "losing_trades": total - wins,
        "total_pnl": round(total_pnl, 4),
        "win_rate": round(wins / total, 4) if total > 0 else 0.0,
    }

    with open(perf_path, "w") as f:
        json.dump(perf, f, indent=2)

    print(f"\n📊 Settlement complete: {len(newly_settled)} settled, {len(still_pending)} still pending")
    print(f"   All-time: {total} trades | {wins}W {total-wins}L | win rate {perf['stats']['win_rate']*100:.0f}%")
    sign = "+" if total_pnl >= 0 else ""
    print(f"   Total P&L: {sign}{total_pnl:.2f} USDC")


def cmd_setup():
    """
    Interactive setup: collect private key, derive API credentials.
    """
    user_id = os.environ.get("USER_ID") or os.environ.get("TELEGRAM_USER_ID")
    if not user_id:
        user_id = input("Enter your User ID (Telegram ID or any identifier): ").strip()
        if not user_id:
            print("❌ User ID is required")
            sys.exit(1)

    print("\n🔑 Polymarket Setup")
    print("=" * 50)
    print("\nYou need your Polymarket wallet private key.")
    print("Get it from: https://polymarket.com/settings → 'Export Key'")
    print()

    private_key = input("Private key (0x...): ").strip()
    if not private_key:
        print("❌ Private key is required")
        sys.exit(1)

    funder = input("Funder address (leave blank to derive from key): ").strip() or None

    dry_run_input = input("Enable dry run mode? [Y/n]: ").strip().lower()
    dry_run = dry_run_input != "n"

    config = {
        "private_key": private_key,
        "funder_address": funder,
        "dry_run": dry_run,
    }

    # Try to derive/create API creds
    print("\n📡 Connecting to derive API credentials...")
    try:
        from py_clob_client.client import ClobClient
        client = ClobClient(HOST, chain_id=CHAIN_ID, key=private_key)
        creds = client.create_or_derive_api_creds()
        config["api_key"] = creds.api_key
        config["api_secret"] = creds.api_secret
        config["api_passphrase"] = creds.api_passphrase
        print(f"✅ API credentials derived!")
        print(f"   API Key: {creds.api_key}")
    except Exception as e:
        print(f"⚠️  Could not derive API creds: {e}")
        print("   You can add them manually later in the credentials file")

    save_config(user_id, config)
    print(f"\n✅ Setup complete! Config saved.")
    print(f"   File: {os.path.join(CREDENTIALS_DIR, user_id + '.json')}")
    if dry_run:
        print(f"\n⚠️  DRY RUN is enabled. No real trades will be placed.")
        print(f"   To enable live trading: set dry_run=false in the config file")


# ─── Main ─────────────────────────────────────────────────────────────────────


def main():
    args = sys.argv[1:]
    if not args:
        print(__doc__)
        sys.exit(0)

    cmd = args[0]
    rest = args[1:]

    dispatch = {
        "check": (cmd_check, 0),
        "fast": (lambda: cmd_fast_markets(rest[0] if rest else None, rest[1] if len(rest) > 1 else None), 0),
        "markets": (lambda: cmd_markets(rest[0] if rest else None), 0),
        "book": (lambda: cmd_book(rest[0]), 1),
        "signal": (lambda: cmd_signal(rest[0]), 1),
        "trade": (lambda: cmd_trade(*rest), 1),
        "positions": (cmd_positions, 0),
        "orders": (cmd_orders, 0),
        "cancel": (lambda: cmd_cancel(rest[0]), 1),
        "cancel-all": (cmd_cancel_all, 0),
        "history": (cmd_history, 0),
        "pnl": (cmd_pnl, 0),
        "settle": (cmd_settle, 0),
        "setup": (cmd_setup, 0),
    }

    if cmd not in dispatch:
        print(f"❌ Unknown command: {cmd}")
        print(__doc__)
        sys.exit(1)

    fn, _ = dispatch[cmd]
    fn()


if __name__ == "__main__":
    main()
