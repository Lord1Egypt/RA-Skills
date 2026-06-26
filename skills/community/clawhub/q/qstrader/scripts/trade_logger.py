#!/usr/bin/env python3
"""
QStrader — Trade Logger
Логирует сделки в Qdrant через mcporter.
"""
import subprocess, json, sys, os
from datetime import datetime


def mcporter_call(args):
    """Call mcporter CLI and return parsed JSON."""
    mcp_config = os.environ.get("MCP_CONFIG", "")
    if not mcp_config:
        for p in [os.path.expanduser("~/.openclaw/workspace/config/mcporter.json"), "./config/mcporter.json"]:
            if os.path.exists(p):
                mcp_config = p
                break
    cmd = ["mcporter", "call"] + args
    os.chdir(os.path.expanduser("~/.openclaw/workspace"))
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
    if result.returncode != 0:
        return {"error": result.stderr.strip()}
    try:
        return json.loads(result.stdout)
    except json.JSONDecodeError:
        return {"raw": result.stdout.strip()}


def log_trade(ticker, side, entry_price, volume, setup_description,
              strategy="manual", tags=None):
    """Залогировать сделку в Qdrant."""
    if tags is None:
        tags = []

    args = [
        "qdrant-trading.journal_add_trade",
        f"ticker={ticker}",
        f"side={side}",
        f"entry_price={entry_price}",
        f"volume={volume}",
        f"setup_description={setup_description}",
        f"strategy={strategy}",
        f"tags={json.dumps(tags)}",
    ]

    result = mcporter_call(args)
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"📝 [{timestamp}] Trade logged: {ticker} {side} @ {entry_price} x{volume}")
    if "error" in result:
        print(f"   ⚠️ {result['error']}")
    return result


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="QStrader Trade Logger")
    parser.add_argument("ticker", help="Тикер (например US500)")
    parser.add_argument("side", choices=["buy", "sell"], help="Направление")
    parser.add_argument("entry_price", type=float, help="Цена входа")
    parser.add_argument("volume", type=float, help="Объём")
    parser.add_argument("setup", help="Описание сетапа")
    parser.add_argument("--strategy", default="manual", help="Стратегия (default: manual)")
    parser.add_argument("--tags", default="", help="Теги через запятую (например: indices,trend)")
    args = parser.parse_args()

    tags = [t.strip() for t in args.tags.split(",") if t.strip()] if args.tags else []
    log_trade(args.ticker, args.side, args.entry_price, args.volume,
              args.setup, args.strategy, tags)
