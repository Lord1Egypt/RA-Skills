#!/usr/bin/env python3
"""模拟交易系统 - 撮合引擎（价格优先、时间优先）"""

import sys
from db import get_conn, init_db, rows_to_list, output_json, output_error


def match_orders(portfolio_id=None):
    """撮合所有待成交的限价单

    逻辑：对每只股票，检查买单价 >= 当前行情，卖单价 <= 当前行情
    价格优先、时间优先（按挂单时间排序）
    """
    conn = get_conn()

    sql = """SELECT o.*, COALESCE(m.price, 0) as market_price
             FROM orders o
             LEFT JOIN market_prices m ON o.symbol=m.symbol
             WHERE o.status='pending' AND o.type='limit'"""
    params = []
    if portfolio_id:
        sql += " AND o.portfolio_id=?"
        params.append(portfolio_id)
    sql += " ORDER BY o.created_at ASC"

    orders = conn.execute(sql, params).fetchall()
    if not orders:
        conn.close()
        output_json({"status": "ok", "message": "没有待撮合的订单", "matched": 0})

    matched_count = 0
    matched_details = []

    for order in orders:
        mp = order["market_price"]
        if mp == 0:
            continue

        od = dict(order)
        should_match = False
        match_price = 0

        if od["side"] == "buy" and mp <= od["price"]:
            should_match = True
            match_price = mp
        elif od["side"] == "sell" and mp >= od["price"]:
            should_match = True
            match_price = mp

        if should_match:
            result = _execute_single(conn, od, match_price)
            matched_details.append(result)
            if result["status"] == "filled":
                matched_count += 1

    conn.close()
    output_json(
        {
            "status": "ok",
            "matched": matched_count,
            "details": matched_details,
        }
    )


def _execute_single(conn, order, price):
    """执行单笔成交"""
    oid = order["id"]
    pid = order["portfolio_id"]
    symbol = order["symbol"]
    name = order["name"]
    side = order["side"]
    qty = order["quantity"]

    if side == "buy":
        p = conn.execute("SELECT cash FROM portfolios WHERE id=?", (pid,)).fetchone()
        cost = qty * price
        if p["cash"] < cost:
            conn.execute(
                "UPDATE orders SET status='rejected',updated_at=datetime('now','localtime') WHERE id=?",
                (oid,),
            )
            conn.commit()
            return {
                "order_id": oid, "symbol": symbol, "side": side,
                "quantity": qty, "limit_price": order["price"],
                "status": "rejected", "reason": f"现金不足：需{cost:.2f}，可用{p['cash']:.2f}",
            }
        conn.execute(
            "UPDATE portfolios SET cash=cash-?, updated_at=datetime('now','localtime') WHERE id=?",
            (cost, pid),
        )
        holding = conn.execute(
            "SELECT * FROM holdings WHERE portfolio_id=? AND symbol=?",
            (pid, symbol),
        ).fetchone()
        if holding:
            total_qty = holding["quantity"] + qty
            avg_cost = (holding["quantity"] * holding["avg_cost"] + cost) / total_qty
            conn.execute(
                "UPDATE holdings SET quantity=?, avg_cost=? WHERE id=?",
                (total_qty, avg_cost, holding["id"]),
            )
        else:
            conn.execute(
                "INSERT INTO holdings (portfolio_id,symbol,name,quantity,avg_cost,market) VALUES (?,?,?,?,?,?)",
                (pid, symbol, name, qty, price, "A"),
            )
    else:
        holding = conn.execute(
            "SELECT * FROM holdings WHERE portfolio_id=? AND symbol=?",
            (pid, symbol),
        ).fetchone()
        if not holding or holding["quantity"] < qty:
            conn.execute(
                "UPDATE orders SET status='rejected',updated_at=datetime('now','localtime') WHERE id=?",
                (oid,),
            )
            conn.commit()
            return {
                "order_id": oid, "symbol": symbol, "side": side,
                "quantity": qty, "limit_price": order["price"],
                "status": "rejected",
                "reason": f"持仓不足：需{qty}股，持{holding['quantity'] if holding else 0}股",
            }
        revenue = qty * price
        conn.execute(
            "UPDATE portfolios SET cash=cash+?, updated_at=datetime('now','localtime') WHERE id=?",
            (revenue, pid),
        )
        new_qty = holding["quantity"] - qty
        if new_qty == 0:
            conn.execute("DELETE FROM holdings WHERE id=?", (holding["id"],))
        else:
            conn.execute(
                "UPDATE holdings SET quantity=? WHERE id=?", (new_qty, holding["id"])
            )

    conn.execute(
        "UPDATE orders SET status='filled', filled_quantity=?, updated_at=datetime('now','localtime') WHERE id=?",
        (qty, oid),
    )
    conn.execute(
        "INSERT INTO trades (order_id,portfolio_id,symbol,name,side,price,quantity) VALUES (?,?,?,?,?,?,?)",
        (oid, pid, symbol, name, side, price, qty),
    )
    conn.commit()
    return {
        "order_id": oid, "symbol": symbol, "side": side,
        "quantity": qty, "limit_price": order["price"],
        "execution_price": price, "status": "filled",
    }


def main():
    init_db()
    pid = sys.argv[1] if len(sys.argv) > 1 else None
    match_orders(pid)


if __name__ == "__main__":
    main()
