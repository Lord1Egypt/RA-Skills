from typing import Any

# Emoji map for signal direction
DIRECTION_EMOJI = {
    "buy":     "🟢",
    "sell":    "🔴",
    "long":    "🟢",
    "short":   "🔴",
    "close":   "⚪",
    "neutral": "🟡",
    "alert":   "🔔",
}

# Emoji map for known symbols
SYMBOL_EMOJI = {
    "XAUUSD": "🥇",
    "EURUSD": "💶",
    "GBPUSD": "💷",
    "BTCUSD": "₿",
    "ETHUSD": "⟠",
    "USDJPY": "💴",
    "USDCHF": "🇨🇭",
}


def format_signal(payload: dict[str, Any]) -> str:
    """
    Format incoming webhook payload into a clean Telegram message.

    Supports two modes:
    - TradingView standard alert payload
    - Custom payload with flexible fields
    """
    # --- TradingView standard fields ---
    action   = str(payload.get("action",   payload.get("signal", "alert"))).lower()
    symbol   = str(payload.get("symbol",   payload.get("ticker", "UNKNOWN"))).upper()
    price    = payload.get("price",        payload.get("close", None))
    interval = payload.get("interval",     payload.get("timeframe", None))
    message  = payload.get("message",      payload.get("msg", None))
    strategy = payload.get("strategy",     payload.get("strategy_name", None))

    # Optional risk fields
    sl       = payload.get("sl",           payload.get("stop_loss", None))
    tp       = payload.get("tp",           payload.get("take_profit", None))
    lot      = payload.get("lot",          payload.get("quantity", None))

    # Resolve emojis
    dir_emoji = DIRECTION_EMOJI.get(action, "🔔")
    sym_emoji = SYMBOL_EMOJI.get(symbol, "📊")

    # Build message lines
    lines = [
        f"{dir_emoji} *{action.upper()} Signal*",
        f"",
        f"{sym_emoji} *Pair:* `{symbol}`",
    ]

    if price:
        lines.append(f"💰 *Price:* `{price}`")
    if interval:
        lines.append(f"⏱️ *Timeframe:* `{interval}`")
    if strategy:
        lines.append(f"🧠 *Strategy:* `{strategy}`")

    # Risk management block
    risk_lines = []
    if sl:
        risk_lines.append(f"🛑 *Stop Loss:* `{sl}`")
    if tp:
        risk_lines.append(f"🎯 *Take Profit:* `{tp}`")
    if lot:
        risk_lines.append(f"📦 *Lot / Qty:* `{lot}`")

    if risk_lines:
        lines.append("")
        lines.extend(risk_lines)

    # Custom message block
    if message:
        lines += ["", f"📝 _{message}_"]

    # Footer
    lines += ["", "─────────────────────", "⚡ _Powered by Webhook-to-Telegram_"]

    return "\n".join(lines)


def format_raw(payload: dict[str, Any]) -> str:
    """Fallback: format any arbitrary payload as a readable key-value list."""
    lines = ["🔔 *New Alert*", ""]
    for key, value in payload.items():
        lines.append(f"• *{key}:* `{value}`")
    lines += ["", "⚡ _Powered by Webhook-to-Telegram_"]
    return "\n".join(lines)
