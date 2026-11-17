#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
双色球数据抓取器
自动从 cwl.gov.cn（中国福利彩票官网）拉取最新开奖数据，
增量更新到本地 SQLite 数据库。
"""
import json
import os
import sqlite3
import sys
import time
from datetime import datetime

import requests

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "ssq_data.db")
CWL_API = "https://www.cwl.gov.cn/cwl_admin/front/cwlkj/search/kjxx/findDrawNotice"
MAX_PER_PAGE = 50


def init_db():
    """初始化 SQLite 数据库表结构"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.execute("""
        CREATE TABLE IF NOT EXISTS draws (
            code TEXT PRIMARY KEY,
            red1 INTEGER, red2 INTEGER, red3 INTEGER,
            red4 INTEGER, red5 INTEGER, red6 INTEGER,
            blue INTEGER,
            draw_date TEXT,
            week TEXT,
            sales INTEGER,
            poolmoney INTEGER,
            fetched_at TEXT
        )
    """)

    c.execute("""
        CREATE TABLE IF NOT EXISTS ball_stats (
            ball_type TEXT,
            ball_number INTEGER,
            appear_count INTEGER DEFAULT 0,
            last_seen_code TEXT,
            last_seen_date TEXT,
            PRIMARY KEY (ball_type, ball_number)
        )
    """)

    c.execute("""
        CREATE TABLE IF NOT EXISTS fetch_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            fetched_at TEXT,
            new_draws INTEGER DEFAULT 0,
            total_draws INTEGER DEFAULT 0,
            status TEXT DEFAULT 'ok'
        )
    """)

    conn.commit()
    return conn


def parse_red_balls(red_str):
    """解析红球字符串 -> 排序后的整数列表"""
    return sorted([int(x) for x in red_str.split(",")])


def fetch_draws(issue_count=MAX_PER_PAGE):
    """从 cwl.gov.cn 拉取开奖数据"""
    params = {"name": "ssq", "issueCount": issue_count}
    headers = {"User-Agent": "SSQAnalyzer/1.0"}
    # 请求间隔保护，避免触发平台限流
    time.sleep(1)
    resp = requests.get(CWL_API, params=params, headers=headers, timeout=20)
    resp.raise_for_status()
    data = resp.json()

    if data.get("state") != 0:
        print(f"[ERROR] API 返回异常: {data.get('message', '未知错误')}")
        return []

    results = data.get("result", [])
    draws = []
    for item in results:
        try:
            reds = parse_red_balls(item["red"])
            draws.append({
                "code": item["code"],
                "red1": reds[0], "red2": reds[1], "red3": reds[2],
                "red4": reds[3], "red5": reds[4], "red6": reds[5],
                "blue": int(item["blue"]),
                "draw_date": item["date"],
                "week": item.get("week", ""),
                "sales": int(item.get("sales", 0)),
                "poolmoney": int(item.get("poolmoney", 0)),
            })
        except (KeyError, ValueError, IndexError) as e:
            print(f"[WARN] 解析期号 {item.get('code', 'unknown')} 失败: {e}")
            continue

    return draws


def save_new_draws(conn, draws):
    """增量存入新数据，跳过已存在的期号"""
    c = conn.cursor()
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    new_count = 0

    for draw in draws:
        c.execute("SELECT code FROM draws WHERE code = ?", (draw["code"],))
        if c.fetchone():
            continue

        c.execute("""
            INSERT INTO draws (code, red1, red2, red3, red4, red5, red6,
                              blue, draw_date, week, sales, poolmoney, fetched_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            draw["code"], draw["red1"], draw["red2"], draw["red3"],
            draw["red4"], draw["red5"], draw["red6"],
            draw["blue"], draw["draw_date"], draw["week"],
            draw["sales"], draw["poolmoney"], now
        ))
        new_count += 1

    c.execute("SELECT COUNT(*) FROM draws")
    total = c.fetchone()[0]

    c.execute("""
        INSERT INTO fetch_log (fetched_at, new_draws, total_draws, status)
        VALUES (?, ?, ?, ?)
    """, (now, new_count, total, "ok"))

    conn.commit()
    return new_count, total


def update_ball_stats(conn):
    """重新统计所有球的出现次数"""
    c = conn.cursor()
    c.execute("DELETE FROM ball_stats")

    for n in range(1, 34):
        c.execute("""
            SELECT COUNT(*), COALESCE(MAX(code), ''), COALESCE(MAX(draw_date), '')
            FROM draws WHERE red1=? OR red2=? OR red3=? OR red4=? OR red5=? OR red6=?
        """, (n, n, n, n, n, n))
        count, last_code, last_date = c.fetchone()
        c.execute("""
            INSERT INTO ball_stats (ball_type, ball_number, appear_count, last_seen_code, last_seen_date)
            VALUES ('red', ?, ?, ?, ?)
        """, (n, count, last_code, last_date))

    for n in range(1, 17):
        c.execute("""
            SELECT COUNT(*), COALESCE(MAX(code), ''), COALESCE(MAX(draw_date), '')
            FROM draws WHERE blue=?
        """, (n,))
        count, last_code, last_date = c.fetchone()
        c.execute("""
            INSERT INTO ball_stats (ball_type, ball_number, appear_count, last_seen_code, last_seen_date)
            VALUES ('blue', ?, ?, ?, ?)
        """, (n, count, last_code, last_date))

    conn.commit()


def get_db_summary(conn):
    """获取数据库摘要"""
    c = conn.cursor()
    c.execute("SELECT COUNT(*) FROM draws")
    total = c.fetchone()[0]
    if total == 0:
        return None, None

    c.execute("SELECT MIN(code), MAX(code) FROM draws")
    min_code, max_code = c.fetchone()
    c.execute("SELECT fetched_at FROM fetch_log ORDER BY id DESC LIMIT 1")
    row = c.fetchone()
    last_fetch = row[0] if row else "从未"

    return total, {"total": total, "min_code": min_code, "max_code": max_code, "last_fetch": last_fetch}


def main():
    print("=" * 50)
    print("  双色球数据抓取器")
    print(f"  {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 50)

    conn = init_db()
    summary = get_db_summary(conn)
    if summary[0]:
        print(f"\n[DB] 当前数据库: {summary[0]} 期数据")
        print(f"     最新期号: {summary[1]['max_code']}")
        print(f"     上次抓取: {summary[1]['last_fetch']}")
    else:
        print("\n[DB] 数据库为空，首次抓取")

    print("\n[FETCH] 正在从 cwl.gov.cn 抓取...")
    try:
        draws = fetch_draws()
        if not draws:
            print("[ERROR] 未抓取到数据，请检查网络连接")
            conn.close()
            return 1

        new_count, total = save_new_draws(conn, draws)
        print(f"        获取 {len(draws)} 期，新增 {new_count} 期")

        if new_count > 0:
            update_ball_stats(conn)
            print("[STATS] 球号统计已更新")

        print(f"\n[DONE] 完成！数据库总计 {total} 期数据")
        return 0

    except requests.exceptions.RequestException as e:
        print(f"\n[ERROR] 网络请求失败: {e}")
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        c = conn.cursor()
        c.execute("INSERT INTO fetch_log (fetched_at, new_draws, total_draws, status) VALUES (?, 0, ?, ?)",
                  (now, summary[0] or 0, f"error: {str(e)[:100]}"))
        conn.commit()
        return 1
    finally:
        conn.close()


if __name__ == "__main__":
    sys.exit(main())
