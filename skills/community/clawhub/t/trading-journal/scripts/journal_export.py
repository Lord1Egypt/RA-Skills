"""
Journal Export — 交易日志导出

Export trading journals to Markdown, CSV, or JSON format.

Usage:
    python journal_export.py --format md --output report.md [--range <start> <end>]
    python journal_export.py --format csv --output trades.csv [--range <start> <end>]
    python journal_export.py --format json --output trades.json
    python journal_export.py --format md --output report.md --symbol IF
"""

import json
import sys
import os
import csv
from datetime import date, timedelta, datetime
from typing import Optional

JOURNALS_DIR = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "journals"
)


def _load_all_trades(start_date: str = None, end_date: str = None,
                     symbol: str = None) -> list:
    """Load trades from date range, optionally filtered by symbol."""
    all_trades = []
    if not os.path.exists(JOURNALS_DIR):
        return all_trades

    for fname in sorted(os.listdir(JOURNALS_DIR)):
        if not fname.endswith(".json"):
            continue
        fdate = fname.replace(".json", "")
        try:
            dt = date.fromisoformat(fdate)
        except ValueError:
            continue

        if start_date and dt < date.fromisoformat(start_date):
            continue
        if end_date and dt > date.fromisoformat(end_date):
            continue

        with open(os.path.join(JOURNALS_DIR, fname), "r", encoding="utf-8") as f:
            data = json.load(f)
        for t in data.get("trades", []):
            t["_date"] = fdate
            if symbol and t.get("symbol", "").upper() != symbol.upper():
                continue
            all_trades.append(t)

    return all_trades


def _export_md(trades: list, output_path: str):
    """Export to Markdown format."""
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("# 交易日志\n\n")
        f.write(f"_导出时间: {datetime.now().strftime('%Y-%m-%d %H:%M')}_\n\n")

        if not trades:
            f.write("暂无交易记录。\n")
            return

        # Group by date
        by_date = {}
        for t in trades:
            d = t.get("_date", t.get("date", "unknown"))
            by_date.setdefault(d, []).append(t)

        total_pnl = 0
        for date_key in sorted(by_date.keys()):
            day_trades = by_date[date_key]
            f.write(f"## {date_key}\n\n")
            f.write(f"| # | 品种 | 方向 | 入场 | 出场 | 数量 | 盈亏 | 策略 |\n")
            f.write(f"|---|:----|:----|:----:|:----:|:---:|:----:|:----:|\n")
            for i, t in enumerate(day_trades, 1):
                sym = t.get("symbol", "?")
                direction = "📈多" if t.get("direction") == "long" else ("📉空" if t.get("direction") == "short" else "?")
                entry = str(t.get("entry_price", "?"))
                exit_ = str(t.get("exit_price", "持仓中")) if t.get("exit_price") else "持仓中"
                qty = t.get("quantity", "?")
                pnl = t.get("pnl")
                if pnl is not None:
                    total_pnl += pnl
                    pnl_str = f"+¥{pnl:,.2f}" if pnl > 0 else f"-¥{abs(pnl):,.2f}" if pnl < 0 else "¥0"
                else:
                    pnl_str = "持仓中"
                strat = t.get("strategy", t.get("notes", "")[:10])
                f.write(f"| {i} | {sym} | {direction} | {entry} | {exit_} | {qty} | {pnl_str} | {strat} |\n")

            f.write("\n")
            day_pnl = sum(t.get("pnl") or 0 for t in day_trades)
            emoji = "🟢" if day_pnl > 0 else ("🔴" if day_pnl < 0 else "⚪")
            f.write(f"  本日合计: {'+¥{:,.2f}' if day_pnl >= 0 else '-¥{:,.2f}'} {emoji}\n\n".format(abs(day_pnl)))

        # Summary
        f.write("---\n")
        f.write(f"### 总计\n\n")
        closed = [t for t in trades if t.get("pnl") is not None]
        wins = sum(1 for t in closed if t["pnl"] > 0)
        emoji_total = "🟢" if total_pnl > 0 else ("🔴" if total_pnl < 0 else "⚪")
        f.write(f"- 总交易数: {len(trades)}\n")
        f.write(f"- 已平仓: {len(closed)}\n")
        f.write(f"- 胜率: {wins / len(closed) * 100:.1f}% ({wins}/{len(closed)})\n" if closed else "- 胜率: N/A\n")
        f.write(f"- 总盈亏: {'+¥{:,.2f}' if total_pnl >= 0 else '-¥{:,.2f}'} {emoji_total}\n".format(abs(total_pnl)))

    print(f"Exported to {output_path}")


def _export_csv(trades: list, output_path: str):
    """Export to CSV format."""
    fieldnames = ["date", "symbol", "type", "direction", "entry_price", "exit_price",
                   "quantity", "multiplier", "entry_time", "exit_time", "fees",
                   "stamp_duty", "strategy", "notes", "tags", "open", "pnl"]

    with open(output_path, "w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        for t in trades:
            row = {}
            row["date"] = t.get("_date", t.get("date", ""))
            for fn in fieldnames:
                if fn == "date":
                    continue
                val = t.get(fn, "")
                if isinstance(val, list):
                    val = "; ".join(str(v) for v in val)
                row[fn] = val
            writer.writerow(row)

    print(f"Exported to {output_path}")


def _export_json(trades: list, output_path: str):
    """Export to JSON format."""
    export = {
        "exported_at": datetime.now().isoformat(),
        "trade_count": len(trades),
        "trades": trades
    }
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(export, f, ensure_ascii=False, indent=2)

    print(f"Exported to {output_path} ({len(trades)} trades)")


def main():
    import argparse

    parser = argparse.ArgumentParser(description="Export trading journals")
    parser.add_argument("--format", choices=["md", "csv", "json"], required=True,
                        help="Output format")
    parser.add_argument("--output", "-o", required=True, help="Output file path")
    parser.add_argument("--range", nargs=2, metavar=("START", "END"),
                        help="Date range (YYYY-MM-DD YYYY-MM-DD)")
    parser.add_argument("--symbol", help="Filter by symbol")

    args = parser.parse_args()

    trades = _load_all_trades(
        start_date=args.range[0] if args.range else None,
        end_date=args.range[1] if args.range else None,
        symbol=args.symbol
    )

    if args.format == "md":
        _export_md(trades, args.output)
    elif args.format == "csv":
        _export_csv(trades, args.output)
    elif args.format == "json":
        _export_json(trades, args.output)


if __name__ == "__main__":
    main()
