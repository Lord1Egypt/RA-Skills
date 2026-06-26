#!/usr/bin/env python3
"""模拟交易系统 - 投资组合管理"""

import sys
import uuid
from datetime import datetime
from db import get_conn, init_db, row_to_dict, rows_to_list, output_json, output_error
from refresh_prices import refresh_portfolio_prices as _refresh_prices


def create_portfolio(name, initial_cash, description=""):
    if initial_cash <= 0:
        output_error("初始资金必须大于0")

    conn = get_conn()
    pid = "PTF" + uuid.uuid4().hex[:8].upper()
    conn.execute(
        "INSERT INTO portfolios (id, name, description, initial_cash, cash) VALUES (?,?,?,?,?)",
        (pid, name, description, initial_cash, initial_cash),
    )
    conn.commit()
    row = conn.execute("SELECT * FROM portfolios WHERE id=?", (pid,)).fetchone()
    conn.close()
    output_json({"status": "ok", "portfolio": row_to_dict(row)})


def list_portfolios():
    conn = get_conn()
    rows = conn.execute(
        "SELECT * FROM portfolios ORDER BY created_at DESC"
    ).fetchall()
    # add holdings summary
    portfolios = rows_to_list(rows)
    for p in portfolios:
        holdings = conn.execute(
            "SELECT COUNT(*) as cnt FROM holdings WHERE portfolio_id=? AND quantity>0",
            (p["id"],),
        ).fetchone()
        p["holding_count"] = holdings["cnt"]
    conn.close()
    output_json({"status": "ok", "portfolios": portfolios, "count": len(portfolios)})


def show_portfolio(pid, no_refresh=False):
    """查看组合详情，默认先刷新实时行情"""
    if not no_refresh:
        try:
            _refresh_prices(pid)
        except Exception:
            pass  # 刷新失败不影响后续查询

    conn = get_conn()
    p = conn.execute("SELECT * FROM portfolios WHERE id=?", (pid,)).fetchone()
    if not p:
        conn.close()
        output_error(f"组合不存在: {pid}")
    portfolio = row_to_dict(p)

    # holdings with current prices
    holdings = conn.execute(
        """SELECT h.*, COALESCE(m.price, 0) as current_price
           FROM holdings h LEFT JOIN market_prices m ON h.symbol=m.symbol
           WHERE h.portfolio_id=? AND h.quantity>0""",
        (pid,),
    ).fetchall()
    holdings_list = rows_to_list(holdings)

    positions_value = 0
    for h in holdings_list:
        h["market_value"] = h["quantity"] * h["current_price"]
        h["profit"] = h["market_value"] - h["quantity"] * h["avg_cost"]
        h["profit_pct"] = (
            round((h["current_price"] - h["avg_cost"]) / h["avg_cost"] * 100, 2)
            if h["avg_cost"] > 0
            else 0
        )
        positions_value += h["market_value"]

    total_value = portfolio["cash"] + positions_value
    total_return = total_value - portfolio["initial_cash"]
    total_return_pct = (
        round(total_return / portfolio["initial_cash"] * 100, 2)
        if portfolio["initial_cash"] > 0
        else 0
    )

    portfolio["positions_value"] = round(positions_value, 2)
    portfolio["total_value"] = round(total_value, 2)
    portfolio["total_return"] = round(total_return, 2)
    portfolio["total_return_pct"] = total_return_pct
    portfolio["holdings"] = holdings_list

    # pending orders
    orders = conn.execute(
        "SELECT * FROM orders WHERE portfolio_id=? AND status IN ('pending','partial')",
        (pid,),
    ).fetchall()
    portfolio["pending_orders"] = rows_to_list(orders)

    # recent trades
    trades = conn.execute(
        "SELECT * FROM trades WHERE portfolio_id=? ORDER BY trade_time DESC LIMIT 20",
        (pid,),
    ).fetchall()
    portfolio["recent_trades"] = rows_to_list(trades)

    conn.close()
    output_json({"status": "ok", "portfolio": portfolio})


def delete_portfolio(pid):
    conn = get_conn()
    p = conn.execute("SELECT * FROM portfolios WHERE id=?", (pid,)).fetchone()
    if not p:
        conn.close()
        output_error(f"组合不存在: {pid}")
    conn.execute("DELETE FROM portfolios WHERE id=?", (pid,))
    conn.commit()
    conn.close()
    output_json({"status": "ok", "message": f"组合 {pid} 已删除"})


def deposit(pid, amount):
    if amount <= 0:
        output_error("入金金额必须大于0")
    conn = get_conn()
    p = conn.execute("SELECT * FROM portfolios WHERE id=?", (pid,)).fetchone()
    if not p:
        conn.close()
        output_error(f"组合不存在: {pid}")
    new_cash = p["cash"] + amount
    conn.execute(
        "UPDATE portfolios SET cash=?, updated_at=datetime('now','localtime') WHERE id=?",
        (new_cash, pid),
    )
    conn.commit()
    p = conn.execute("SELECT * FROM portfolios WHERE id=?", (pid,)).fetchone()
    conn.close()
    output_json(
        {
            "status": "ok",
            "message": f"入金 {amount} 成功",
            "portfolio": row_to_dict(p),
        }
    )


def withdraw(pid, amount):
    if amount <= 0:
        output_error("出金金额必须大于0")
    conn = get_conn()
    p = conn.execute("SELECT * FROM portfolios WHERE id=?", (pid,)).fetchone()
    if not p:
        conn.close()
        output_error(f"组合不存在: {pid}")
    if amount > p["cash"]:
        conn.close()
        output_error(f"现金不足，当前现金: {p['cash']}")
    new_cash = p["cash"] - amount
    conn.execute(
        "UPDATE portfolios SET cash=?, updated_at=datetime('now','localtime') WHERE id=?",
        (new_cash, pid),
    )
    conn.commit()
    p = conn.execute("SELECT * FROM portfolios WHERE id=?", (pid,)).fetchone()
    conn.close()
    output_json(
        {
            "status": "ok",
            "message": f"出金 {amount} 成功",
            "portfolio": row_to_dict(p),
        }
    )


def main():
    if len(sys.argv) < 2:
        output_error(
            "用法: portfolio.py <action> [args...]\n"
            "  create <name> <initial_cash> [description]\n"
            "  list\n"
            "  show <portfolio_id> [--no-refresh]\n"
            "  delete <portfolio_id>\n"
            "  deposit <portfolio_id> <amount>\n"
            "  withdraw <portfolio_id> <amount>"
        )

    init_db()
    action = sys.argv[1]

    if action == "create":
        if len(sys.argv) < 4:
            output_error("用法: create <name> <initial_cash> [description]")
        name = sys.argv[2]
        initial_cash = float(sys.argv[3])
        desc = sys.argv[4] if len(sys.argv) > 4 else ""
        create_portfolio(name, initial_cash, desc)
    elif action == "list":
        list_portfolios()
    elif action == "show":
        if len(sys.argv) < 3:
            output_error("用法: show <portfolio_id> [--no-refresh]")
        no_refresh = "--no-refresh" in sys.argv
        show_portfolio(sys.argv[2], no_refresh=no_refresh)
    elif action == "delete":
        if len(sys.argv) < 3:
            output_error("用法: delete <portfolio_id>")
        delete_portfolio(sys.argv[2])
    elif action == "deposit":
        if len(sys.argv) < 4:
            output_error("用法: deposit <portfolio_id> <amount>")
        deposit(sys.argv[2], float(sys.argv[3]))
    elif action == "withdraw":
        if len(sys.argv) < 4:
            output_error("用法: withdraw <portfolio_id> <amount>")
        withdraw(sys.argv[2], float(sys.argv[3]))
    else:
        output_error(f"未知操作: {action}")


if __name__ == "__main__":
    main()
