#!/usr/bin/env python3
"""模拟交易系统 - 数据库模块"""

import os
import sqlite3
import json
import sys

DB_PATH = os.environ.get(
    "SIMTRADE_DB_PATH",
    os.path.expanduser("~/.openclaw/workspace/data/simulated-trading.db"),
)


def get_db_path():
    return DB_PATH


def ensure_dir():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)


def get_conn():
    ensure_dir()
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA foreign_keys=ON")
    return conn


def init_db():
    conn = get_conn()
    conn.executescript("""
    CREATE TABLE IF NOT EXISTS portfolios (
        id TEXT PRIMARY KEY,
        name TEXT NOT NULL,
        description TEXT DEFAULT '',
        initial_cash REAL NOT NULL,
        cash REAL NOT NULL,
        created_at TEXT DEFAULT (datetime('now','localtime')),
        updated_at TEXT DEFAULT (datetime('now','localtime'))
    );

    CREATE TABLE IF NOT EXISTS holdings (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        portfolio_id TEXT NOT NULL,
        symbol TEXT NOT NULL,
        name TEXT DEFAULT '',
        quantity INTEGER NOT NULL DEFAULT 0,
        avg_cost REAL NOT NULL DEFAULT 0,
        market TEXT DEFAULT 'A',
        UNIQUE(portfolio_id, symbol),
        FOREIGN KEY (portfolio_id) REFERENCES portfolios(id) ON DELETE CASCADE
    );

    CREATE TABLE IF NOT EXISTS orders (
        id TEXT PRIMARY KEY,
        portfolio_id TEXT NOT NULL,
        symbol TEXT NOT NULL,
        name TEXT DEFAULT '',
        side TEXT NOT NULL CHECK(side IN ('buy','sell')),
        type TEXT NOT NULL CHECK(type IN ('limit','market')),
        price REAL,
        quantity INTEGER NOT NULL,
        filled_quantity INTEGER NOT NULL DEFAULT 0,
        status TEXT NOT NULL DEFAULT 'pending'
            CHECK(status IN ('pending','partial','filled','cancelled','rejected')),
        created_at TEXT DEFAULT (datetime('now','localtime')),
        updated_at TEXT DEFAULT (datetime('now','localtime')),
        FOREIGN KEY (portfolio_id) REFERENCES portfolios(id) ON DELETE CASCADE
    );

    CREATE TABLE IF NOT EXISTS trades (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        order_id TEXT NOT NULL,
        portfolio_id TEXT NOT NULL,
        symbol TEXT NOT NULL,
        name TEXT DEFAULT '',
        side TEXT NOT NULL,
        price REAL NOT NULL,
        quantity INTEGER NOT NULL,
        trade_time TEXT DEFAULT (datetime('now','localtime')),
        FOREIGN KEY (order_id) REFERENCES orders(id),
        FOREIGN KEY (portfolio_id) REFERENCES portfolios(id) ON DELETE CASCADE
    );

    CREATE TABLE IF NOT EXISTS market_prices (
        symbol TEXT PRIMARY KEY,
        name TEXT DEFAULT '',
        price REAL NOT NULL,
        updated_at TEXT DEFAULT (datetime('now','localtime'))
    );

    CREATE TABLE IF NOT EXISTS nav_history (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        portfolio_id TEXT NOT NULL,
        date TEXT NOT NULL,
        nav REAL NOT NULL,
        total_value REAL NOT NULL,
        cash REAL NOT NULL,
        positions_value REAL NOT NULL,
        UNIQUE(portfolio_id, date),
        FOREIGN KEY (portfolio_id) REFERENCES portfolios(id) ON DELETE CASCADE
    );
    """)
    conn.commit()
    conn.close()
    return True


def row_to_dict(row):
    if row is None:
        return None
    return dict(row)


def rows_to_list(rows):
    return [dict(r) for r in rows]


def output_json(data):
    print(json.dumps(data, ensure_ascii=False, indent=2))


def output_error(msg):
    output_json({"error": msg})
    sys.exit(1)


if __name__ == "__main__":
    action = sys.argv[1] if len(sys.argv) > 1 else "init"
    if action == "init":
        init_db()
        output_json({"status": "ok", "message": "数据库初始化完成", "path": DB_PATH})
    elif action == "path":
        output_json({"path": DB_PATH})
    else:
        output_error(f"未知操作: {action}")
