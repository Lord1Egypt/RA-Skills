#!/usr/bin/env python3
"""模拟交易系统 - 净值计算与绩效分析"""

import sys
from datetime import datetime, timedelta
from db import get_conn, init_db, row_to_dict, rows_to_list, output_json, output_error
from refresh_prices import refresh_portfolio_prices as _refresh_prices


def _ensure_fresh_prices(portfolio_id, no_refresh=False):
    """确保持仓行情为最新"""
    if not no_refresh:
        try:
            _refresh_prices(portfolio_id)
        except Exception:
            pass


def calculate_nav(portfolio_id, date=None, no_refresh=False):
    """计算指定日期的净值，默认先刷新实时行情"""
    _ensure_fresh_prices(portfolio_id, no_refresh)

    if date is None:
        date = datetime.now().strftime("%Y-%m-%d")

    conn = get_conn()
    p = conn.execute(
        "SELECT * FROM portfolios WHERE id=?", (portfolio_id,)
    ).fetchone()
    if not p:
        conn.close()
        output_error(f"组合不存在: {portfolio_id}")

    holdings = conn.execute(
        """SELECT h.*, COALESCE(m.price, 0) as current_price
           FROM holdings h LEFT JOIN market_prices m ON h.symbol=m.symbol
           WHERE h.portfolio_id=?""",
        (portfolio_id,),
    ).fetchall()

    positions_value = sum(
        (h["quantity"] or 0) * (h["current_price"] or 0) for h in holdings
    )
    total_value = p["cash"] + positions_value
    nav = total_value / p["initial_cash"] if p["initial_cash"] > 0 else 0

    conn.close()

    result = {
        "portfolio_id": portfolio_id,
        "portfolio_name": p["name"],
        "date": date,
        "nav": round(nav, 6),
        "total_value": round(total_value, 2),
        "cash": round(p["cash"], 2),
        "positions_value": round(positions_value, 2),
        "initial_cash": p["initial_cash"],
        "total_return": round(total_value - p["initial_cash"], 2),
        "total_return_pct": round(
            (total_value - p["initial_cash"]) / p["initial_cash"] * 100, 2
        ),
        "holdings_detail": [
            {
                "symbol": h["symbol"],
                "name": h["name"],
                "quantity": h["quantity"],
                "avg_cost": h["avg_cost"],
                "current_price": h["current_price"],
                "market_value": round(h["quantity"] * h["current_price"], 2),
                "pnl": round(
                    h["quantity"] * (h["current_price"] - h["avg_cost"]), 2
                ),
                "pnl_pct": round(
                    (h["current_price"] - h["avg_cost"]) / h["avg_cost"] * 100, 2
                )
                if h["avg_cost"] > 0
                else 0,
            }
            for h in holdings
        ],
    }
    output_json({"status": "ok", "data": result})


def take_snapshot(portfolio_id, date=None, no_refresh=False):
    """记录净值快照，默认先刷新实时行情"""
    _ensure_fresh_prices(portfolio_id, no_refresh)

    if date is None:
        date = datetime.now().strftime("%Y-%m-%d")

    conn = get_conn()
    p = conn.execute(
        "SELECT * FROM portfolios WHERE id=?", (portfolio_id,)
    ).fetchone()
    if not p:
        conn.close()
        output_error(f"组合不存在: {portfolio_id}")

    holdings = conn.execute(
        """SELECT h.*, COALESCE(m.price, 0) as current_price
           FROM holdings h LEFT JOIN market_prices m ON h.symbol=m.symbol
           WHERE h.portfolio_id=?""",
        (portfolio_id,),
    ).fetchall()

    positions_value = sum(
        (h["quantity"] or 0) * (h["current_price"] or 0) for h in holdings
    )
    total_value = p["cash"] + positions_value
    nav = total_value / p["initial_cash"] if p["initial_cash"] > 0 else 0

    # upsert
    conn.execute(
        """INSERT INTO nav_history (portfolio_id, date, nav, total_value, cash, positions_value)
           VALUES (?,?,?,?,?,?)
           ON CONFLICT(portfolio_id, date) DO UPDATE SET
           nav=excluded.nav, total_value=excluded.total_value,
           cash=excluded.cash, positions_value=excluded.positions_value""",
        (portfolio_id, date, round(nav, 6), round(total_value, 2),
         round(p["cash"], 2), round(positions_value, 2)),
    )
    conn.commit()
    conn.close()
    output_json(
        {
            "status": "ok",
            "message": f"净值快照已记录",
            "portfolio_id": portfolio_id,
            "date": date,
            "nav": round(nav, 6),
            "total_value": round(total_value, 2),
        }
    )


def performance(portfolio_id, from_date=None, to_date=None, no_refresh=False):
    """计算组合绩效指标，默认先刷新实时行情"""
    _ensure_fresh_prices(portfolio_id, no_refresh)

    if from_date is None:
        from_date = (datetime.now() - timedelta(days=365)).strftime("%Y-%m-%d")
    if to_date is None:
        to_date = datetime.now().strftime("%Y-%m-%d")

    conn = get_conn()
    p = conn.execute(
        "SELECT * FROM portfolios WHERE id=?", (portfolio_id,)
    ).fetchone()
    if not p:
        conn.close()
        output_error(f"组合不存在: {portfolio_id}")

    # 获取净值历史
    rows = conn.execute(
        """SELECT * FROM nav_history
           WHERE portfolio_id=? AND date BETWEEN ? AND ?
           ORDER BY date ASC""",
        (portfolio_id, from_date, to_date),
    ).fetchall()
    nav_list = rows_to_list(rows)

    # 如果没有历史快照，计算当前的
    if not nav_list:
        conn.close()
        output_error(
            f"没有找到 {from_date} 到 {to_date} 的净值快照。请先执行 snapshot 命令。"
        )

    # 计算指标
    n = len(nav_list)
    navs = [r["nav"] for r in nav_list]
    start_nav = navs[0]
    end_nav = navs[-1]

    total_return = (end_nav - start_nav) / start_nav if start_nav > 0 else 0

    # 日收益率
    daily_returns = []
    for i in range(1, n):
        r = (navs[i] - navs[i - 1]) / navs[i - 1] if navs[i - 1] > 0 else 0
        daily_returns.append(r)

    # 年化收益率（假设每个快照是一天，简化为252交易日/年）
    avg_daily = sum(daily_returns) / len(daily_returns) if daily_returns else 0
    annualized_return = round(((1 + avg_daily) ** 252 - 1) * 100, 2)

    # 年化波动率
    if len(daily_returns) > 1:
        avg_r = sum(daily_returns) / len(daily_returns)
        variance = sum((r - avg_r) ** 2 for r in daily_returns) / (len(daily_returns) - 1)
        daily_vol = variance ** 0.5
        annualized_vol = round(daily_vol * (252 ** 0.5) * 100, 2)
    else:
        annualized_vol = 0

    # 夏普比率（假设无风险利率 2%）
    risk_free = 0.02
    sharpe = round(
        (annualized_return / 100 - risk_free) / (annualized_vol / 100), 2
    ) if annualized_vol > 0 else 0

    # 最大回撤
    max_drawdown = 0
    peak = navs[0]
    for nav in navs:
        if nav > peak:
            peak = nav
        dd = (peak - nav) / peak if peak > 0 else 0
        if dd > max_drawdown:
            max_drawdown = dd

    # 胜率
    win_days = sum(1 for r in daily_returns if r > 0)
    win_rate = round(win_days / len(daily_returns) * 100, 2) if daily_returns else 0

    # 总成交统计
    trades = conn.execute(
        "SELECT COUNT(*) as cnt, SUM(quantity*price) as total_amount FROM trades WHERE portfolio_id=?",
        (portfolio_id,),
    ).fetchone()

    # 当前持仓数量和市值
    holdings_count = conn.execute(
        "SELECT COUNT(*) as cnt FROM holdings WHERE portfolio_id=? AND quantity>0",
        (portfolio_id,),
    ).fetchone()

    current_holdings = conn.execute(
        """SELECT h.*, COALESCE(m.price, 0) as current_price
           FROM holdings h LEFT JOIN market_prices m ON h.symbol=m.symbol
           WHERE h.portfolio_id=? AND h.quantity>0""",
        (portfolio_id,),
    ).fetchall()

    positions_val = sum(
        (h["quantity"] or 0) * (h["current_price"] or 0) for h in current_holdings
    )

    conn.close()

    result = {
        "portfolio_id": portfolio_id,
        "portfolio_name": p["name"],
        "period": f"{from_date} ~ {to_date}",
        "data_points": n,
        "start_nav": round(start_nav, 4),
        "end_nav": round(end_nav, 4),
        "total_return_pct": round(total_return * 100, 2),
        "annualized_return_pct": annualized_return,
        "annualized_volatility_pct": annualized_vol,
        "sharpe_ratio": sharpe,
        "max_drawdown_pct": round(max_drawdown * 100, 2),
        "win_rate_pct": win_rate,
        "trades_count": trades["cnt"] if trades else 0,
        "trades_total_amount": round(trades["total_amount"] or 0, 2),
        "current_holdings_count": holdings_count["cnt"] if holdings_count else 0,
        "initial_cash": p["initial_cash"],
        "current_cash": round(p["cash"], 2),
        "current_total_value": round(p["cash"] + positions_val, 2),
    }
    output_json({"status": "ok", "data": result})


def nav_history(portfolio_id, limit=30):
    """查询净值历史"""
    conn = get_conn()
    rows = conn.execute(
        "SELECT * FROM nav_history WHERE portfolio_id=? ORDER BY date DESC LIMIT ?",
        (portfolio_id, limit),
    ).fetchall()
    conn.close()
    output_json(
        {
            "status": "ok",
            "portfolio_id": portfolio_id,
            "history": rows_to_list(rows),
            "count": len(rows),
        }
    )


def _parse_no_refresh():
    return "--no-refresh" in sys.argv


def main():
    if len(sys.argv) < 2:
        output_error(
            "用法: performance.py <action> [args...]\n"
            "  nav <portfolio_id> [date] [--no-refresh]\n"
            "  snapshot <portfolio_id> [date] [--no-refresh]\n"
            "  perf <portfolio_id> [from_date] [to_date] [--no-refresh]\n"
            "  history <portfolio_id> [limit]"
        )

    init_db()
    action = sys.argv[1]
    no_refresh = "--no-refresh" in sys.argv

    if action == "nav":
        if len(sys.argv) < 3:
            output_error("用法: nav <portfolio_id> [date] [--no-refresh]")
        pid = sys.argv[2]
        date = sys.argv[3] if len(sys.argv) > 3 and sys.argv[3] != "--no-refresh" else None
        calculate_nav(pid, date, no_refresh=no_refresh)
    elif action == "snapshot":
        if len(sys.argv) < 3:
            output_error("用法: snapshot <portfolio_id> [date] [--no-refresh]")
        pid = sys.argv[2]
        date = sys.argv[3] if len(sys.argv) > 3 and sys.argv[3] != "--no-refresh" else None
        take_snapshot(pid, date, no_refresh=no_refresh)
    elif action == "perf":
        if len(sys.argv) < 3:
            output_error("用法: perf <portfolio_id> [from_date] [to_date] [--no-refresh]")
        pid = sys.argv[2]
        args = [a for a in sys.argv[3:] if a != "--no-refresh"]
        from_date = args[0] if len(args) > 0 else None
        to_date = args[1] if len(args) > 1 else None
        performance(pid, from_date, to_date, no_refresh=no_refresh)
    elif action == "history":
        if len(sys.argv) < 3:
            output_error("用法: history <portfolio_id> [limit]")
        pid = sys.argv[2]
        limit = int(sys.argv[3]) if len(sys.argv) > 3 else 30
        nav_history(pid, limit)
    else:
        output_error(f"未知操作: {action}")


if __name__ == "__main__":
    main()
