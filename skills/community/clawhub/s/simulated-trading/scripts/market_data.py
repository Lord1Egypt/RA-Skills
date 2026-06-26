#!/usr/bin/env python3
"""模拟交易系统 - 行情数据管理"""

import sys
import json
from datetime import datetime
from db import get_conn, init_db, row_to_dict, rows_to_list, output_json, output_error


def update_price(symbol, price, name=""):
    """更新单个标的价格"""
    if price <= 0:
        output_error("价格必须大于0")

    conn = get_conn()
    existing = conn.execute(
        "SELECT * FROM market_prices WHERE symbol=?", (symbol,)
    ).fetchone()

    if existing:
        old_price = existing["price"]
        conn.execute(
            """UPDATE market_prices
               SET price=?, name=?, updated_at=datetime('now','localtime')
               WHERE symbol=?""",
            (price, name if name else existing["name"], symbol),
        )
    else:
        conn.execute(
            "INSERT INTO market_prices (symbol,name,price) VALUES (?,?,?)",
            (symbol, name if name else symbol, price),
        )
        old_price = None

    conn.commit()
    row = conn.execute(
        "SELECT * FROM market_prices WHERE symbol=?", (symbol,)
    ).fetchone()
    conn.close()

    change = None
    if old_price and old_price > 0:
        change = round((price - old_price) / old_price * 100, 2)

    output_json(
        {
            "status": "ok",
            "symbol": symbol,
            "price": price,
            "old_price": old_price,
            "change_pct": change,
            "data": row_to_dict(row),
        }
    )


def batch_update(json_str):
    """批量更新价格，JSON 格式: [{"symbol":"000001","price":12.5,"name":"平安银行"}, ...]"""
    try:
        items = json.loads(json_str) if isinstance(json_str, str) else json_str
    except json.JSONDecodeError as e:
        output_error(f"JSON 解析错误: {e}")

    if not isinstance(items, list):
        output_error("需要 JSON 数组格式")

    conn = get_conn()
    results = []
    for item in items:
        symbol = item["symbol"]
        price = item["price"]
        name = item.get("name", "")
        existing = conn.execute(
            "SELECT * FROM market_prices WHERE symbol=?", (symbol,)
        ).fetchone()
        old_price = existing["price"] if existing else None
        if existing:
            conn.execute(
                "UPDATE market_prices SET price=?, name=?, updated_at=datetime('now','localtime') WHERE symbol=?",
                (price, name if name else existing["name"], symbol),
            )
        else:
            conn.execute(
                "INSERT INTO market_prices (symbol,name,price) VALUES (?,?,?)",
                (symbol, name if name else symbol, price),
            )
        change = None
        if old_price and old_price > 0:
            change = round((price - old_price) / old_price * 100, 2)
        results.append(
            {"symbol": symbol, "price": price, "old_price": old_price, "change_pct": change}
        )

    conn.commit()
    conn.close()
    output_json(
        {
            "status": "ok",
            "updated": len(results),
            "results": results,
        }
    )


def get_price(symbol):
    """查询单个标的价格"""
    conn = get_conn()
    row = conn.execute(
        "SELECT * FROM market_prices WHERE symbol=?", (symbol,)
    ).fetchone()
    conn.close()
    if row:
        output_json({"status": "ok", "data": row_to_dict(row)})
    else:
        output_error(f"未找到标的: {symbol}")


def list_prices(search=None):
    """列出所有行情"""
    conn = get_conn()
    if search:
        rows = conn.execute(
            "SELECT * FROM market_prices WHERE symbol LIKE ? OR name LIKE ? ORDER BY symbol",
            (f"%{search}%", f"%{search}%"),
        ).fetchall()
    else:
        rows = conn.execute(
            "SELECT * FROM market_prices ORDER BY symbol"
        ).fetchall()
    conn.close()
    output_json(
        {
            "status": "ok",
            "prices": rows_to_list(rows),
            "count": len(rows),
        }
    )


def delete_price(symbol):
    """删除标的价格数据"""
    conn = get_conn()
    conn.execute("DELETE FROM market_prices WHERE symbol=?", (symbol,))
    conn.commit()
    conn.close()
    output_json({"status": "ok", "message": f"已删除 {symbol} 的行情数据"})


def main():
    if len(sys.argv) < 2:
        output_error(
            "用法: market_data.py <action> [args...]\n"
            "  update <symbol> <price> [name]\n"
            "  batch <json_array>\n"
            "  price <symbol>\n"
            "  list [search]\n"
            "  delete <symbol>"
        )

    init_db()
    action = sys.argv[1]

    if action == "update":
        if len(sys.argv) < 4:
            output_error("用法: update <symbol> <price> [name]")
        symbol = sys.argv[2]
        price = float(sys.argv[3])
        name = sys.argv[4] if len(sys.argv) > 4 else ""
        update_price(symbol, price, name)
    elif action == "batch":
        if len(sys.argv) < 3:
            output_error("用法: batch <json_array>")
        batch_update(sys.argv[2])
    elif action == "price":
        if len(sys.argv) < 3:
            output_error("用法: price <symbol>")
        get_price(sys.argv[2])
    elif action == "list":
        search = sys.argv[2] if len(sys.argv) > 2 else None
        list_prices(search)
    elif action == "delete":
        if len(sys.argv) < 3:
            output_error("用法: delete <symbol>")
        delete_price(sys.argv[2])
    else:
        output_error(f"未知操作: {action}")


if __name__ == "__main__":
    main()
