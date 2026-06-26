#!/usr/bin/env python3
"""
Solana Token Monitor — Core monitoring script
Built by ShepDog (shepdogcoin.com)
Uses DexScreener public API (no key required)
Telegram alerts via Bot API (optional — configure with setup --telegram-token and --chat-id)
"""

import json
import sys
import urllib.request
import urllib.parse
import os
from datetime import datetime, timezone

DEXSCREENER_URL = "https://api.dexscreener.com/tokens/v1/solana/{}"
TELEGRAM_API_URL = "https://api.telegram.org/bot{}/sendMessage"
DATA_DIR = os.path.expanduser("~/.openclaw/workspace/data/token-monitors")


def fetch_token_data(contract_address: str):
    """Fetch token data from DexScreener API."""
    url = DEXSCREENER_URL.format(contract_address)
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "SolanaTokenMonitor/1.0"})
        with urllib.request.urlopen(req, timeout=10) as response:
            data = json.loads(response.read().decode())
            pairs = data if isinstance(data, list) else data.get("pairs", [])
            if not pairs:
                return None
            return max(pairs, key=lambda p: float(p.get("liquidity", {}).get("usd", 0) or 0))
    except Exception as e:
        print(f"Error fetching data: {e}", file=sys.stderr)
        return None


def send_telegram(bot_token: str, chat_id: str, text: str) -> bool:
    """Send a Telegram message via Bot API."""
    if not bot_token or not chat_id:
        return False
    try:
        payload = json.dumps({"chat_id": chat_id, "text": text, "parse_mode": "HTML"}).encode()
        req = urllib.request.Request(
            TELEGRAM_API_URL.format(bot_token),
            data=payload,
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        with urllib.request.urlopen(req, timeout=10) as resp:
            result = json.loads(resp.read().decode())
            return result.get("ok", False)
    except Exception as e:
        print(f"Telegram delivery error: {e}", file=sys.stderr)
        return False


def load_config(symbol: str):
    """Load token monitor config."""
    path = os.path.join(DATA_DIR, f"{symbol.upper()}.json")
    if not os.path.exists(path):
        return None
    with open(path) as f:
        return json.load(f)


def save_config(symbol: str, config: dict):
    """Save token monitor config."""
    os.makedirs(DATA_DIR, exist_ok=True)
    path = os.path.join(DATA_DIR, f"{symbol.upper()}.json")
    with open(path, "w") as f:
        json.dump(config, f, indent=2)


def setup_monitor(contract_address: str, symbol: str, telegram_token: str = None, chat_id: str = None):
    """Set up monitoring for a token."""
    print(f"Setting up monitor for ${symbol.upper()} ({contract_address})...")
    data = fetch_token_data(contract_address)
    if not data:
        print(f"❌ Could not fetch data for {contract_address}.")
        print("   Check the contract address is correct and has an active liquidity pool on DexScreener.")
        sys.exit(1)

    price = float(data.get("priceUsd", 0) or 0)
    market_cap = float(data.get("marketCap", 0) or 0)
    volume_24h = float(data.get("volume", {}).get("h24", 0) or 0)
    liquidity = float(data.get("liquidity", {}).get("usd", 0) or 0)

    config = {
        "symbol": symbol.upper(),
        "contract": contract_address,
        "chain": "solana",
        "telegram_bot_token": telegram_token or "",
        "telegram_chat_id": chat_id or "",
        "thresholds": {
            "price_change_pct": 5.0,
            "volume_spike_multiplier": 2.0,
            "liquidity_drop_pct": 20.0,
        },
        "milestones": [10000, 50000, 100000, 500000, 1000000],
        "milestones_hit": [],
        "last_check": {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "price_usd": price,
            "market_cap": market_cap,
            "volume_24h": volume_24h,
            "liquidity_usd": liquidity,
        },
        "created_at": datetime.now(timezone.utc).isoformat(),
        "enabled": True,
    }

    save_config(symbol, config)

    telegram_status = "✅ Configured" if (telegram_token and chat_id) else "⚠️  Not configured (alerts printed to stdout only)"

    print(f"""
✅ Monitor configured for ${symbol.upper()}!

Current stats:
  Price:      ${price:.8f}
  Market Cap: ${market_cap:,.0f}
  Volume 24h: ${volume_24h:,.2f}
  Liquidity:  ${liquidity:,.2f}

Alerts:
  Telegram:   {telegram_status}
  Thresholds: price >{config['thresholds']['price_change_pct']}%, volume >{config['thresholds']['volume_spike_multiplier']}x, liquidity drop >{config['thresholds']['liquidity_drop_pct']}%
  Milestones: $10K, $50K, $100K, $500K, $1M

Config saved to: {DATA_DIR}/{symbol.upper()}.json
""")

    if telegram_token and chat_id:
        msg = f"🐕 Solana Token Monitor activated for ${symbol.upper()}!\n\nPrice: ${price:.8f}\nMarket Cap: ${market_cap:,.0f}\nLiquidity: ${liquidity:,.2f}\n\nI'll alert you on:\n• Price moves &gt;5%\n• Volume spikes &gt;2x\n• Liquidity drops &gt;20%\n• Market cap milestones"
        if send_telegram(telegram_token, chat_id, msg):
            print("✅ Test alert sent to Telegram successfully.")
        else:
            print("⚠️  Could not send test Telegram alert. Check your bot token and chat ID.")


def check_monitor(symbol: str) -> list:
    """Check a token and return any alerts. Also delivers them via Telegram if configured."""
    config = load_config(symbol)
    if not config or not config.get("enabled"):
        return []

    data = fetch_token_data(config["contract"])
    if not data:
        return [{"urgency": "grey", "message": f"⚠️ Could not fetch data for ${symbol.upper()}"}]

    alerts = []
    now = datetime.now(timezone.utc).isoformat()

    current_price = float(data.get("priceUsd", 0) or 0)
    current_mcap = float(data.get("marketCap", 0) or 0)
    current_volume = float(data.get("volume", {}).get("h24", 0) or 0)
    current_liquidity = float(data.get("liquidity", {}).get("usd", 0) or 0)
    price_change_1h = float(data.get("priceChange", {}).get("h1", 0) or 0)

    last = config.get("last_check", {})
    last_liquidity = float(last.get("liquidity_usd", current_liquidity) or current_liquidity)
    last_volume = float(last.get("volume_24h", current_volume) or current_volume)
    thresholds = config.get("thresholds", {})

    # Price change alert
    if abs(price_change_1h) >= thresholds.get("price_change_pct", 5.0):
        direction = "🚀" if price_change_1h > 0 else "📉"
        urgency = "yellow" if abs(price_change_1h) < 15 else "red"
        alerts.append({
            "urgency": urgency,
            "message": f"{direction} ${symbol.upper()} price {price_change_1h:+.1f}% in 1h | Now: ${current_price:.8f}"
        })

    # Liquidity drop alert
    if last_liquidity > 0:
        liq_change_pct = ((current_liquidity - last_liquidity) / last_liquidity) * 100
        if liq_change_pct <= -thresholds.get("liquidity_drop_pct", 20.0):
            alerts.append({
                "urgency": "red",
                "message": f"⚠️ ${symbol.upper()} LIQUIDITY DROP {liq_change_pct:.1f}% | Now: ${current_liquidity:,.0f}"
            })

    # Volume spike alert
    if last_volume > 0 and current_volume >= last_volume * thresholds.get("volume_spike_multiplier", 2.0):
        ratio = current_volume / last_volume
        alerts.append({
            "urgency": "yellow",
            "message": f"📊 ${symbol.upper()} volume spike {ratio:.1f}x | 24h: ${current_volume:,.2f}"
        })

    # Milestone alerts
    milestones = config.get("milestones", [])
    milestones_hit = set(config.get("milestones_hit", []))
    for milestone in milestones:
        if current_mcap >= milestone and milestone not in milestones_hit:
            milestones_hit.add(milestone)
            label = f"${milestone/1000:.0f}K" if milestone < 1000000 else f"${milestone/1000000:.0f}M"
            alerts.append({
                "urgency": "yellow",
                "message": f"🎯 ${symbol.upper()} hit {label} market cap! Now: ${current_mcap:,.0f}"
            })

    # Update stored state
    config["last_check"] = {
        "timestamp": now,
        "price_usd": current_price,
        "market_cap": current_mcap,
        "volume_24h": current_volume,
        "liquidity_usd": current_liquidity,
    }
    config["milestones_hit"] = list(milestones_hit)
    save_config(symbol, config)

    # Deliver alerts via Telegram if configured
    bot_token = config.get("telegram_bot_token", "")
    chat_id = config.get("telegram_chat_id", "")
    if alerts and bot_token and chat_id:
        lines = [f"🐕 <b>${symbol.upper()} Alert</b>"]
        for a in alerts:
            prefix = "🔴" if a["urgency"] == "red" else "🟡"
            lines.append(f"{prefix} {a['message']}")
        send_telegram(bot_token, chat_id, "\n".join(lines))

    return alerts


def report(symbol: str) -> str:
    """Generate a formatted status report."""
    config = load_config(symbol)
    if not config:
        return f"❌ No monitor found for ${symbol.upper()}. Run: monitor.py setup <CONTRACT> {symbol.upper()}"

    data = fetch_token_data(config["contract"])
    if not data:
        return f"❌ Could not fetch data for ${symbol.upper()}. Token may have no active liquidity pool."

    price = float(data.get("priceUsd", 0) or 0)
    mcap = float(data.get("marketCap", 0) or 0)
    volume = float(data.get("volume", {}).get("h24", 0) or 0)
    liquidity = float(data.get("liquidity", {}).get("usd", 0) or 0)
    change_24h = float(data.get("priceChange", {}).get("h24", 0) or 0)
    change_1h = float(data.get("priceChange", {}).get("h1", 0) or 0)
    txns_24h = data.get("txns", {}).get("h24", {})
    buys = txns_24h.get("buys", 0)
    sells = txns_24h.get("sells", 0)

    arrow_24h = "▲" if change_24h >= 0 else "▼"
    arrow_1h = "▲" if change_1h >= 0 else "▼"
    telegram_status = "✅" if config.get("telegram_bot_token") and config.get("telegram_chat_id") else "⚠️  not configured"

    return f"""🐕 Solana Token Monitor — Status Report
{'─' * 40}
Token:      ${symbol.upper()}
Chain:      Solana

Price:      ${price:.8f}
  1h:       {arrow_1h} {abs(change_1h):.1f}%
  24h:      {arrow_24h} {abs(change_24h):.1f}%

Market Cap: ${mcap:,.0f}
Volume 24h: ${volume:,.2f}
Liquidity:  ${liquidity:,.2f}

Txns 24h:   {buys} buys / {sells} sells
Telegram:   {telegram_status}

Contract:   {config['contract'][:20]}...
{'─' * 40}
Built by ShepDog 🐕 shepdogcoin.com"""


def list_monitors() -> list:
    """List all configured monitors."""
    if not os.path.exists(DATA_DIR):
        return []
    return [f.replace(".json", "") for f in os.listdir(DATA_DIR) if f.endswith(".json")]


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "help"

    if cmd == "setup" and len(sys.argv) >= 4:
        # Optional: --telegram-token TOKEN --chat-id ID
        args = sys.argv[4:]
        tg_token = None
        chat_id = None
        for i, a in enumerate(args):
            if a == "--telegram-token" and i + 1 < len(args):
                tg_token = args[i + 1]
            if a == "--chat-id" and i + 1 < len(args):
                chat_id = args[i + 1]
        setup_monitor(sys.argv[2], sys.argv[3], tg_token, chat_id)

    elif cmd == "check" and len(sys.argv) >= 3:
        alerts = check_monitor(sys.argv[2])
        for a in alerts:
            print(f"[{a['urgency'].upper()}] {a['message']}")
        if not alerts:
            print(f"✅ No alerts for ${sys.argv[2].upper()}")

    elif cmd == "report" and len(sys.argv) >= 3:
        print(report(sys.argv[2]))

    elif cmd == "list":
        monitors = list_monitors()
        print(f"Active monitors: {', '.join(monitors) if monitors else 'None'}")

    else:
        print("""
Solana Token Monitor — Built by ShepDog 🐕

Usage:
  monitor.py setup <CONTRACT_ADDRESS> <SYMBOL> [--telegram-token TOKEN --chat-id ID]
  monitor.py check <SYMBOL>
  monitor.py report <SYMBOL>
  monitor.py list

Examples:
  # Basic setup (alerts printed to stdout, for use inside OpenClaw heartbeat)
  monitor.py setup DezXAZ8z7PnrnRJjz3wXBoRgixCa6xjnB7YaB1pPB263 BONK

  # With Telegram bot alerts
  monitor.py setup DezXAZ8z7PnrnRJjz3wXBoRgixCa6xjnB7YaB1pPB263 BONK --telegram-token 123:ABC --chat-id 456789

  monitor.py report BONK
  monitor.py check BONK
""")
