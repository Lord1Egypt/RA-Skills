#!/usr/bin/env python3
"""模拟交易系统 - 订单管理（下单/撤单/查单）"""

import sys
import uuid
from db import get_conn, init_db, row_to_dict, rows_to_list, output_json, output_error


def place_order(portfolio_id, symbol, side, order_type, quantity, price=None, name=""):
    if side not in ("buy", "sell"):
        output_error("side 必须是 buy 或 sell")
    if order_type not in ("limit", "market"):
        output_error("type 必须是 limit 或 market")
    if quantity <= 0:
        output_error("数量必须大于0")
    if order_type == "limit" and (price is None or price <= 0):
        output_error("限价单必须指定有效的价格")

    conn = get_conn()
    p = conn.execute(
        "SELECT * FROM portfolios WHERE id=?", (portfolio_id,)
    ).fetchone()
    if not p:
        conn.close()
        output_error(f"组合不存在: {portfolio_id}")

    # 获取股票名称
    mp = conn.execute(
        "SELECT name,price FROM market_prices WHERE symbol=?", (symbol,)
    ).fetchone()
    if mp and name == "":
        name = mp["name"]
    market_price = mp["price"] if mp else None

    order_id = "ORD" + uuid.uuid4().hex[:8].upper()

    if order_type == "market":
        # 市价单立即成交
        if market_price is None:
            conn.close()
            output_error(f"没有 {symbol} 的行情数据，无法执行市价单")
        conn.execute(
            """INSERT INTO orders (id,portfolio_id,symbol,name,side,type,price,quantity)
               VALUES (?,?,?,?,?,?,?,?)""",
            (order_id, portfolio_id, symbol, name, side, "market", None, quantity),
        )
        _execute_order(conn, order_id, portfolio_id, symbol, name, side, quantity,
                       market_price)
        conn.commit()
        result_order = conn.execute(
            "SELECT * FROM orders WHERE id=?", (order_id,)
        ).fetchone()
        conn.close()
        output_json(
            {
                "status": "ok",
                "message": f"市价单 {order_id} 已成交",
                "execution_price": market_price,
                "order": row_to_dict(result_order),
            }
        )
    else:
        # 限价单挂单
        conn.execute(
            """INSERT INTO orders (id,portfolio_id,symbol,name,side,type,price,quantity)
               VALUES (?,?,?,?,?,?,?,?)""",
            (order_id, portfolio_id, symbol, name, side, "limit", price, quantity),
        )
        conn.commit()
        result_order = conn.execute(
            "SELECT * FROM orders WHERE id=?", (order_id,)
        ).fetchone()
        conn.close()
        output_json(
            {
                "status": "ok",
                "message": f"限价单 {order_id} 已挂单",
                "order": row_to_dict(result_order),
            }
        )


def _execute_order(conn, order_id, portfolio_id, symbol, name, side, quantity, price):
    """执行成交：更新现金、持仓、订单状态、生成成交记录"""
    if side == "buy":
        # 检查现金
        p = conn.execute(
            "SELECT cash FROM portfolios WHERE id=?", (portfolio_id,)
        ).fetchone()
        cost = quantity * price
        if p["cash"] < cost:
            conn.execute(
                "UPDATE orders SET status='rejected',updated_at=datetime('now','localtime') WHERE id=?",
                (order_id,),
            )
            conn.commit()
            conn.close()
            output_error(
                f"现金不足：需要 {cost:.2f}，可用 {p['cash']:.2f}"
            )
        # 扣现金
        conn.execute(
            "UPDATE portfolios SET cash=cash-?, updated_at=datetime('now','localtime') WHERE id=?",
            (cost, portfolio_id),
        )
        # 更新持仓
        holding = conn.execute(
            "SELECT * FROM holdings WHERE portfolio_id=? AND symbol=?",
            (portfolio_id, symbol),
        ).fetchone()
        if holding:
            total_qty = holding["quantity"] + quantity
            avg_cost = (
                (holding["quantity"] * holding["avg_cost"] + cost) / total_qty
            )
            conn.execute(
                "UPDATE holdings SET quantity=?, avg_cost=? WHERE id=?",
                (total_qty, avg_cost, holding["id"]),
            )
        else:
            conn.execute(
                "INSERT INTO holdings (portfolio_id,symbol,name,quantity,avg_cost,market) VALUES (?,?,?,?,?,?)",
                (portfolio_id, symbol, name, quantity, price, "A"),
            )
    else:  # sell
        # 检查持仓
        holding = conn.execute(
            "SELECT * FROM holdings WHERE portfolio_id=? AND symbol=?",
            (portfolio_id, symbol),
        ).fetchone()
        if not holding or holding["quantity"] < quantity:
            conn.execute(
                "UPDATE orders SET status='rejected',updated_at=datetime('now','localtime') WHERE id=?",
                (order_id,),
            )
            conn.commit()
            conn.close()
            output_error(
                f"持仓不足：需要 {quantity} 股，持有 {holding['quantity'] if holding else 0} 股"
            )
        # 加现金
        revenue = quantity * price
        conn.execute(
            "UPDATE portfolios SET cash=cash+?, updated_at=datetime('now','localtime') WHERE id=?",
            (revenue, portfolio_id),
        )
        # 更新持仓
        new_qty = holding["quantity"] - quantity
        if new_qty == 0:
            conn.execute("DELETE FROM holdings WHERE id=?", (holding["id"],))
        else:
            conn.execute(
                "UPDATE holdings SET quantity=? WHERE id=?", (new_qty, holding["id"])
            )

    # 更新订单状态
    conn.execute(
        "UPDATE orders SET status='filled', filled_quantity=?, updated_at=datetime('now','localtime') WHERE id=?",
        (quantity, order_id),
    )
    # 生成成交记录
    conn.execute(
        "INSERT INTO trades (order_id,portfolio_id,symbol,name,side,price,quantity) VALUES (?,?,?,?,?,?,?)",
        (order_id, portfolio_id, symbol, name, side, price, quantity),
    )


def cancel_order(order_id):
    conn = get_conn()
    order = conn.execute("SELECT * FROM orders WHERE id=?", (order_id,)).fetchone()
    if not order:
        conn.close()
        output_error(f"订单不存在: {order_id}")
    if order["status"] not in ("pending", "partial"):
        conn.close()
        output_error(f"订单状态为 {order['status']}，无法撤销")
    conn.execute(
        "UPDATE orders SET status='cancelled', updated_at=datetime('now','localtime') WHERE id=?",
        (order_id,),
    )
    conn.commit()
    updated = conn.execute("SELECT * FROM orders WHERE id=?", (order_id,)).fetchone()
    conn.close()
    output_json(
        {
            "status": "ok",
            "message": f"订单 {order_id} 已撤销",
            "order": row_to_dict(updated),
        }
    )


def query_orders(portfolio_id=None, status=None):
    conn = get_conn()
    sql = "SELECT * FROM orders WHERE 1=1"
    params = []
    if portfolio_id:
        sql += " AND portfolio_id=?"
        params.append(portfolio_id)
    if status:
        sql += " AND status=?"
        params.append(status)
    sql += " ORDER BY created_at DESC LIMIT 100"
    rows = conn.execute(sql, params).fetchall()
    conn.close()
    output_json(
        {
            "status": "ok",
            "orders": rows_to_list(rows),
            "count": len(rows),
        }
    )


def show_order(order_id):
    conn = get_conn()
    order = conn.execute("SELECT * FROM orders WHERE id=?", (order_id,)).fetchone()
    if not order:
        conn.close()
        output_error(f"订单不存在: {order_id}")
    trades = conn.execute(
        "SELECT * FROM trades WHERE order_id=?", (order_id,)
    ).fetchall()
    result = row_to_dict(order)
    result["trades"] = rows_to_list(trades)
    conn.close()
    output_json({"status": "ok", "order": result})


def main():
    if len(sys.argv) < 2:
        output_error(
            "用法: order.py <action> [args...]\n"
            "  place <portfolio_id> <symbol> <side> <type> <quantity> [price] [name]\n"
            "  cancel <order_id>\n"
            "  query [portfolio_id] [status]\n"
            "  show <order_id>"
        )

    init_db()
    action = sys.argv[1]

    if action == "place":
        if len(sys.argv) < 7:
            output_error(
                "用法: place <portfolio_id> <symbol> <side> <type> <quantity> [price] [name]"
            )
        pid = sys.argv[2]
        symbol = sys.argv[3]
        side = sys.argv[4]
        otype = sys.argv[5]
        qty = int(sys.argv[6])
        price = float(sys.argv[7]) if len(sys.argv) > 7 and sys.argv[7] else None
        name = sys.argv[8] if len(sys.argv) > 8 else ""
        place_order(pid, symbol, side, otype, qty, price, name)
    elif action == "cancel":
        if len(sys.argv) < 3:
            output_error("用法: cancel <order_id>")
        cancel_order(sys.argv[2])
    elif action == "query":
        pid = sys.argv[2] if len(sys.argv) > 2 else None
        status = sys.argv[3] if len(sys.argv) > 3 else None
        query_orders(pid, status)
    elif action == "show":
        if len(sys.argv) < 3:
            output_error("用法: show <order_id>")
        show_order(sys.argv[2])
    else:
        output_error(f"未知操作: {action}")


if __name__ == "__main__":
    main()
