"""
Trade Analyzer — 交易绩效分析

Compute performance metrics and generate reports for any date range.

Usage:
    python trade_analyzer.py --range <start> <end>          # Analyze date range
    python trade_analyzer.py --today                        # Analyze today
    python trade_analyzer.py --month YYYY-MM                # Analyze a month
    python trade_analyzer.py --symbol <code> [--range ...]  # Filter by symbol
    python trade_analyzer.py --summary                      # Quick summary of all data
"""

import json
import sys
import os
from datetime import date, timedelta, datetime
from math import sqrt
from typing import Optional

JOURNALS_DIR = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "journals"
)


# ── Data Loading ──

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


# ── Analysis ──

def analyze(trades: list) -> dict:
    """Compute all performance metrics for a list of trades."""
    # Only analyze closed trades (not open positions)
    closed = [t for t in trades if not t.get("open", False) and t.get("pnl") is not None]
    winning = [t for t in closed if t["pnl"] > 0]
    losing = [t for t in closed if t["pnl"] < 0]

    result = {
        "total_trades": len(trades),
        "closed_trades": len(closed),
        "open_positions": len([t for t in trades if t.get("open", True)]),
        "winning_trades": len(winning),
        "losing_trades": len(losing),
    }

    if not closed:
        result["status"] = "no_closed_trades"
        return result

    result["status"] = "ok"

    # Win Rate
    result["win_rate_pct"] = round(len(winning) / len(closed) * 100, 2)

    # Total P&L
    total_pnl = sum(t["pnl"] for t in closed)
    result["total_pnl"] = round(total_pnl, 2)

    # Gross Profit / Loss
    gross_profit = sum(t["pnl"] for t in winning) if winning else 0
    gross_loss = abs(sum(t["pnl"] for t in losing)) if losing else 0
    result["gross_profit"] = round(gross_profit, 2)
    result["gross_loss"] = round(gross_loss, 2)

    # Profit Factor
    result["profit_factor"] = round(gross_profit / gross_loss, 2) if gross_loss > 0 else float("inf")

    # Average Win / Loss
    result["avg_win"] = round(gross_profit / len(winning), 2) if winning else 0
    result["avg_loss"] = round(-gross_loss / len(losing), 2) if losing else 0

    # Payoff Ratio
    result["payoff_ratio"] = round(result["avg_win"] / abs(result["avg_loss"]), 2) if result["avg_loss"] != 0 else float("inf")

    # Best / Worst Trade
    result["best_trade"] = max(closed, key=lambda t: t["pnl"]) if closed else None
    result["worst_trade"] = min(closed, key=lambda t: t["pnl"]) if closed else None

    # Max Consecutive Wins/Losses
    max_consec_wins = 0
    max_consec_losses = 0
    cur_wins = 0
    cur_losses = 0
    for t in closed:
        if t["pnl"] > 0:
            cur_wins += 1
            cur_losses = 0
            max_consec_wins = max(max_consec_wins, cur_wins)
        else:
            cur_losses += 1
            cur_wins = 0
            max_consec_losses = max(max_consec_losses, cur_losses)
    result["max_consecutive_wins"] = max_consec_wins
    result["max_consecutive_losses"] = max_consec_losses

    # Expectancy
    loss_rate = len(losing) / len(closed)
    result["expectancy"] = round(
        result["win_rate_pct"] / 100 * result["avg_win"] - loss_rate * abs(result["avg_loss"]), 2
    )

    # Max Drawdown (cumulative P&L)
    cumulative = 0
    peak = 0
    max_dd = 0
    for t in closed:
        cumulative += t["pnl"]
        if cumulative > peak:
            peak = cumulative
        dd = peak - cumulative
        if dd > max_dd:
            max_dd = dd
    result["max_drawdown"] = round(max_dd, 2)
    result["max_drawdown_pct"] = round(max_dd / peak * 100, 2) if peak > 0 else 0

    # Daily aggregation for Sharpe
    daily_pnls = {}
    for t in closed:
        d = t.get("_date", t.get("date", "unknown"))
        daily_pnls[d] = daily_pnls.get(d, 0) + t["pnl"]
    daily_returns = list(daily_pnls.values())
    if len(daily_returns) > 1:
        avg_daily = sum(daily_returns) / len(daily_returns)
        var_daily = sum((r - avg_daily) ** 2 for r in daily_returns) / len(daily_returns)
        std_daily = sqrt(var_daily) if var_daily > 0 else 0.01
        rf_daily = 0.02 / 252  # 2% annual risk-free rate → daily
        result["sharpe_ratio"] = round((avg_daily - rf_daily) / std_daily * sqrt(252), 2)
        result["daily_avg_return"] = round(avg_daily, 2)
        result["daily_std_return"] = round(std_daily, 2)
    else:
        result["sharpe_ratio"] = None

    # Date range
    dates = [t.get("_date", t.get("date")) for t in closed]
    if dates:
        result["range"] = {"start": min(dates), "end": max(dates)}
        result["trading_days"] = len(set(dates))

    return result


def format_report(analysis: dict) -> str:
    """Format analysis results into a human-readable report."""
    if analysis["status"] == "no_closed_trades":
        return "📊 没有已平仓的交易记录。"

    lines = []
    r = analysis
    lines.append("📊 交易绩效报告")
    lines.append("━" * 35)

    if "range" in r:
        lines.append(f"  日期范围:  {r['range']['start']} ~ {r['range']['end']}")
        lines.append(f"  交易日数:  {r.get('trading_days', 'N/A')}")
    lines.append(f"  总交易数:  {r['total_trades']}")
    lines.append(f"  已平仓:    {r['closed_trades']}")
    if r.get("open_positions", 0) > 0:
        lines.append(f"  持仓中:    {r['open_positions']}")
    lines.append("")

    total_pnl = r["total_pnl"]
    emoji = "🟢" if total_pnl > 0 else ("🔴" if total_pnl < 0 else "⚪")
    lines.append(f"  胜率:      {r['win_rate_pct']}% ({r['winning_trades']}/{r['closed_trades']})")
    lines.append(f"  总盈亏:    {'+¥{:,.2f}' if total_pnl >= 0 else '-¥{:,.2f}'} {emoji}".format(abs(total_pnl)))
    lines.append(f"  盈亏比:    {r['profit_factor']}")
    lines.append(f"  平均盈利:  +¥{r['avg_win']:,.2f}")
    lines.append(f"  平均亏损:  -¥{abs(r['avg_loss']):,.2f}")
    lines.append(f"  盈亏比:    {r['payoff_ratio']}")
    lines.append(f"  期望值:    ¥{r['expectancy']:,.2f}/笔")
    lines.append("")

    if r.get("sharpe_ratio"):
        lines.append(f"  夏普比率:  {r['sharpe_ratio']}")
    lines.append(f"  最大回撤:  -¥{r['max_drawdown']:,.2f} ({r['max_drawdown_pct']}%)")
    lines.append(f"  连胜:      {r['max_consecutive_wins']}")
    lines.append(f"  连败:      {r['max_consecutive_losses']}")

    if r.get("best_trade"):
        bt = r["best_trade"]
        lines.append(f"  最佳交易:  +¥{bt['pnl']:,.2f} ({bt.get('symbol','?')}, {bt.get('_date','?')})")
    if r.get("worst_trade"):
        wt = r["worst_trade"]
        lines.append(f"  最差交易:  {wt['pnl']:,.2f} ({wt.get('symbol','?')}, {wt.get('_date','?')})")

    return "\n".join(lines)


# ── Main ──

def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    start_date = None
    end_date = None
    symbol = None

    if "--range" in sys.argv:
        idx = sys.argv.index("--range") + 1
        start_date = sys.argv[idx]
        end_date = sys.argv[idx + 1] if idx + 1 < len(sys.argv) else start_date
    elif "--today" in sys.argv:
        today_str = date.today().isoformat()
        start_date = today_str
        end_date = today_str
    elif "--month" in sys.argv:
        idx = sys.argv.index("--month") + 1
        ym = sys.argv[idx]
        start_date = f"{ym}-01"
        # Last day of month
        y, m = int(ym[:4]), int(ym[5:7])
        if m == 12:
            end_date = f"{y+1}-01-01"
        else:
            end_date = f"{y}-{m+1:02d}-01"
        # Subtract 1 day
        end_date = (date.fromisoformat(end_date) - timedelta(days=1)).isoformat()
    elif "--summary" in sys.argv:
        pass  # leave None = all data

    if "--symbol" in sys.argv:
        idx = sys.argv.index("--symbol") + 1
        symbol = sys.argv[idx]

    trades = _load_all_trades(start_date, end_date, symbol)
    analysis = analyze(trades)

    if "--json" in sys.argv:
        print(json.dumps(analysis, ensure_ascii=False, indent=2,
                         default=str))
    else:
        print(format_report(analysis))


if __name__ == "__main__":
    main()
