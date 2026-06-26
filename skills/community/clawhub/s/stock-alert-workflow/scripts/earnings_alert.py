#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "yfinance>=0.2.40",
#     "pandas>=2.0.0",
# ]
# ///
"""
Earnings Surprise Alert Workflow

Scans a list of tickers (or a watchlist file) for EPS surprises > 10%.
For each qualifying stock, fetches recent analyst ratings (last 30 days)
and outputs a structured alert payload suitable for WhatsApp push.

Usage:
    uv run earnings_alert.py AAPL MSFT GOOGL
    uv run earnings_alert.py --watchlist ~/.clawdbot/skills/stock-analysis/watchlist.txt
    uv run earnings_alert.py AAPL --output json
    uv run earnings_alert.py AAPL --threshold 15
"""

import argparse
import json
import sys
from datetime import datetime, timedelta
from pathlib import Path

import pandas as pd
import yfinance as yf


DEFAULT_THRESHOLD = 10.0
WATCHLIST_PATH = Path("~/.clawdbot/skills/stock-analysis/watchlist.txt").expanduser()


def fetch_earnings_surprise(ticker: str) -> dict | None:
    """Fetch the most recent EPS surprise for a ticker."""
    try:
        stock = yf.Ticker(ticker)
        eh = stock.earnings_history
        if eh is None or eh.empty:
            return None

        recent = eh.sort_index(ascending=False).head(10)
        for idx, row in recent.iterrows():
            reported = row.get("Reported EPS")
            estimate = row.get("EPS Estimate")
            if pd.notna(reported) and pd.notna(estimate):
                actual = float(reported)
                expected = float(estimate)
                if expected == 0:
                    continue
                surprise_pct = ((actual - expected) / abs(expected)) * 100
                return {
                    "ticker": ticker,
                    "actual_eps": round(actual, 4),
                    "expected_eps": round(expected, 4),
                    "surprise_pct": round(surprise_pct, 2),
                    "report_date": str(idx.date()) if hasattr(idx, "date") else str(idx),
                }
        return None
    except Exception as e:
        print(f"  ⚠ Error fetching earnings for {ticker}: {e}", file=sys.stderr)
        return None


def fetch_analyst_ratings(ticker: str, days: int = 30) -> dict | None:
    """Fetch analyst ratings from the last N days."""
    try:
        stock = yf.Ticker(ticker)

        # Get recommendation trends
        recs = stock.recommendations
        recent_recs = []
        if recs is not None and not recs.empty:
            cutoff = pd.Timestamp.now(tz="UTC") - timedelta(days=days)
            if recs.index.tz is None:
                cutoff = cutoff.tz_localize(None)
            recent = recs[recs.index >= cutoff]
            for idx, row in recent.iterrows():
                recent_recs.append({
                    "date": str(idx.date()) if hasattr(idx, "date") else str(idx),
                    "firm": row.get("Firm", "N/A"),
                    "grade": row.get("To Grade", "N/A"),
                    "action": row.get("Action", "N/A"),
                })

        # Get consensus summary
        info = stock.info or {}
        consensus = {
            "recommendation": info.get("recommendationKey", "N/A"),
            "target_mean": info.get("targetMeanPrice"),
            "current_price": info.get("regularMarketPrice") or info.get("currentPrice"),
            "num_analysts": info.get("numberOfAnalystOpinions"),
        }

        # Calculate upside if data available
        if consensus["target_mean"] and consensus["current_price"]:
            consensus["upside_pct"] = round(
                ((consensus["target_mean"] - consensus["current_price"]) / consensus["current_price"]) * 100, 2
            )
        else:
            consensus["upside_pct"] = None

        return {
            "consensus": consensus,
            "recent_ratings": recent_recs[-10:],  # cap at 10 most recent
        }
    except Exception as e:
        print(f"  ⚠ Error fetching analyst ratings for {ticker}: {e}", file=sys.stderr)
        return None


def format_whatsapp_message(alerts: list[dict]) -> str:
    """Format alerts into a WhatsApp-friendly message."""
    if not alerts:
        return ""

    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    lines = [
        f"📈 *超预期盈利提醒* _{now}_",
        "━━━━━━━━━━━━━━━━━━",
    ]

    for a in alerts:
        s = a["surprise"]
        lines.append(f"\n🎯 *{s['ticker']}*  EPS超预期 *{s['surprise_pct']}%*")
        lines.append(f"   实际: ${s['actual_eps']}  预期: ${s['expected_eps']}")
        lines.append(f"   报告日期: {s['report_date']}")

        r = a["ratings"]
        if r:
            c = r["consensus"]
            rec = c.get("recommendation", "N/A")
            if isinstance(rec, str):
                rec = rec.replace("_", " ").title()
            lines.append(f"   📊 共识评级: {rec}")

            if c.get("num_analysts"):
                lines.append(f"   👥 分析师数量: {c['num_analysts']}")

            if c.get("upside_pct") is not None:
                direction = "↑" if c["upside_pct"] > 0 else "↓"
                lines.append(f"   💰 目标价空间: {direction}{abs(c['upside_pct'])}%")

            if c.get("target_mean") and c.get("current_price"):
                lines.append(f"   💵 目标价: ${c['target_mean']:.2f} (现价 ${c['current_price']:.2f})")

            recent = r.get("recent_ratings", [])
            if recent:
                lines.append("   📝 近期评级变动:")
                for rating in recent[:5]:
                    lines.append(f"     • {rating['date']} {rating['firm']}: {rating['grade']}")

        lines.append("───────────────────")

    lines.append("\n_⚠️ 以上信息仅供参考，不构成投资建议_")
    return "\n".join(lines)


def run_alert(tickers: list[str], threshold: float = DEFAULT_THRESHOLD, days: int = 30) -> list[dict]:
    """Main alert logic: scan tickers, filter by threshold, enrich with analyst ratings."""
    alerts = []

    for ticker in tickers:
        ticker = ticker.strip().upper()
        if not ticker:
            continue
        print(f"  🔍 Scanning {ticker}...", file=sys.stderr)
        surprise = fetch_earnings_surprise(ticker)
        if surprise is None:
            continue
        if surprise["surprise_pct"] > threshold:
            print(f"  ✅ {ticker}: EPS surprise {surprise['surprise_pct']}% > {threshold}%  — fetching analyst ratings", file=sys.stderr)
            ratings = fetch_analyst_ratings(ticker, days=days)
            alerts.append({"surprise": surprise, "ratings": ratings})
        else:
            print(f"  ⏭ {ticker}: surprise {surprise['surprise_pct']}% ≤ {threshold}%, skipping", file=sys.stderr)

    return alerts


def load_watchlist(path: Path) -> list[str]:
    """Load tickers from a watchlist file (one per line, # comments)."""
    if not path.exists():
        print(f"Watchlist not found: {path}", file=sys.stderr)
        return []
    tickers = []
    for line in path.read_text().splitlines():
        line = line.strip().upper()
        if line and not line.startswith("#"):
            tickers.append(line)
    return tickers


def main():
    parser = argparse.ArgumentParser(description="Earnings Surprise Alert Workflow")
    parser.add_argument("tickers", nargs="*", help="Ticker symbols to scan")
    parser.add_argument("--watchlist", type=str, help="Path to watchlist file (one ticker per line)")
    parser.add_argument("--threshold", type=float, default=DEFAULT_THRESHOLD,
                        help=f"EPS surprise %% threshold (default: {DEFAULT_THRESHOLD})")
    parser.add_argument("--days", type=int, default=30, help="Analyst rating lookback days (default: 30)")
    parser.add_argument("--output", choices=["text", "json"], default="text", help="Output format")

    args = parser.parse_args()

    # Resolve tickers
    tickers = list(args.tickers)
    if args.watchlist:
        tickers.extend(load_watchlist(Path(args.watchlist)))
    if not tickers:
        if WATCHLIST_PATH.exists():
            tickers = load_watchlist(WATCHLIST_PATH)
        if not tickers:
            print("No tickers provided. Use positional args or --watchlist.", file=sys.stderr)
            sys.exit(1)

    tickers = list(dict.fromkeys(tickers))  # dedupe preserving order
    print(f"Scanning {len(tickers)} ticker(s) for EPS surprise > {args.threshold}%...", file=sys.stderr)

    alerts = run_alert(tickers, threshold=args.threshold, days=args.days)

    if not alerts:
        print("No earnings surprises exceeding threshold found.", file=sys.stderr)
        if args.output == "json":
            print(json.dumps({"alerts": [], "count": 0}, indent=2))
        else:
            print("📭 No alerts to send.")
        return

    if args.output == "json":
        print(json.dumps({"alerts": alerts, "count": len(alerts)}, indent=2, default=str))
    else:
        msg = format_whatsapp_message(alerts)
        print(msg)


if __name__ == "__main__":
    main()