#!/usr/bin/env python3
"""
memory_access_log.py - 记忆访问日志，记录每次记忆读取以计算重要性评分

用法:
  python scripts/memory_access_log.py --uid pupper --chunk-id xxx    # 记录访问
  python scripts/memory_access_log.py --uid pupper --report          # 打印评分报告
  python scripts/memory_access_log.py --uid pupper --get-importance  # 输出 JSON（供其他脚本调用）

重要性评分公式:
  score = 50 + (access_count_normalized × 0.4 + recency_normalized × 0.4 + importance_manual × 0.2) × 50

依赖:
  pip install openai numpy
"""

import os
import sys
import sqlite3
import argparse
import json
from datetime import datetime, timezone

ACCESS_DB = ".memory_access_log.db"

# 全局默认重要性（来自手动标记）
MANUAL_IMPORTANCE = {
    "L3": 100,  # 永久记忆默认最高
    "L2": 60,   # 长期记忆
    "L1": 40,   # 临时记忆
}


def get_db_path(base_dir):
    return os.path.join(os.path.abspath(base_dir), ACCESS_DB)


def init_access_db(db_path):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute("PRAGMA journal_mode=WAL")
    c.execute("""
        CREATE TABLE IF NOT EXISTS memory_access_log (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            chunk_id    TEXT    NOT NULL,
            uid         TEXT    NOT NULL,
            access_time REAL    NOT NULL,  -- Unix timestamp
            access_type TEXT    NOT NULL,  -- 'read' | 'search' | 'write' | 'manual_pin'
            extra       TEXT    DEFAULT '{}'  -- JSON extra info
        )
    """)
    # 手动重要性标记表（用户可手动 pin 重要记忆）
    c.execute("""
        CREATE TABLE IF NOT EXISTS manual_importance (
            chunk_id    TEXT PRIMARY KEY,
            uid         TEXT    NOT NULL,
            score       REAL    NOT NULL,  -- 0-100
            note        TEXT    DEFAULT '',
            updated_at  REAL    NOT NULL
        )
    """)
    c.execute("""
        CREATE INDEX IF NOT EXISTS idx_chunk_time
        ON memory_access_log(chunk_id, access_time DESC)
    """)
    conn.commit()
    return conn


def log_access(db_path, chunk_id, uid, access_type="read", extra=None):
    """记录一次记忆访问"""
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute(
        "INSERT INTO memory_access_log (chunk_id, uid, access_time, access_type, extra) VALUES (?, ?, ?, ?, ?)",
        (chunk_id, uid, datetime.now(timezone.utc).timestamp(), access_type, json.dumps(extra or {}))
    )
    conn.commit()
    conn.close()


def get_access_stats(db_path, uid, chunk_ids=None):
    """
    获取 chunk_ids 的访问统计。
    返回: {chunk_id: {"access_count": N, "last_accessed": ts, "access_types": [...]}}
    """
    conn = sqlite3.connect(db_path)
    c = conn.cursor()

    result = {}
    target_ids = chunk_ids or []

    if target_ids:
        placeholders = ",".join(["?"] * len(target_ids))
        rows = c.execute(f"""
            SELECT chunk_id, COUNT(*), MAX(access_time),
                   GROUP_CONCAT(DISTINCT access_type) as types
            FROM memory_access_log
            WHERE uid = ? AND chunk_id IN ({placeholders})
            GROUP BY chunk_id
        """, [uid] + target_ids).fetchall()

        for chunk_id, count, last_ts, types in rows:
            result[chunk_id] = {
                "access_count": count,
                "last_accessed": last_ts,
                "access_types": types.split(",") if types else [],
            }

    conn.close()
    return result


def get_manual_importance(db_path, uid, chunk_ids=None):
    """获取手动重要性评分"""
    conn = sqlite3.connect(db_path)
    c = conn.cursor()

    result = {}
    target_ids = chunk_ids or []

    if target_ids:
        placeholders = ",".join(["?"] * len(target_ids))
        rows = c.execute(f"""
            SELECT chunk_id, score FROM manual_importance
            WHERE uid = ? AND chunk_id IN ({placeholders})
        """, [uid] + target_ids).fetchall()
        result = {cid: score for cid, score in rows}

    conn.close()
    return result


def set_manual_importance(db_path, chunk_id, uid, score, note=""):
    """手动设置/更新记忆的重要性"""
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute("""
        INSERT INTO manual_importance (chunk_id, uid, score, note, updated_at)
        VALUES (?, ?, ?, ?, ?)
        ON CONFLICT(chunk_id) DO UPDATE SET score=excluded.score, note=excluded.note, updated_at=excluded.updated_at
    """, (chunk_id, uid, score, note, datetime.now(timezone.utc).timestamp()))
    conn.commit()
    conn.close()


def calculate_importance_score(db_path, uid, chunk_id, level, base_score=50):
    """
    计算单条记忆的重要性评分（0-100）。

    公式:
      score = base + (freq_w × 0.4 + recency_w × 0.4 + manual_w × 0.2) × 50

    其中:
      - freq_w: 访问频率标准化 (min-max, 0-1)
      - recency_w: 最近访问时间标准化 (指数衰减, 0-1)
      - manual_w: 手动标记分数 (0-1, 来自 manual_importance 表)
    """
    import math

    conn = sqlite3.connect(db_path)
    c = conn.cursor()

    now = datetime.now(timezone.utc).timestamp()

    # 获取该用户所有 chunk 的访问情况（用于标准化）
    rows = c.execute("""
        SELECT chunk_id, COUNT(*), MAX(access_time)
        FROM memory_access_log
        WHERE uid = ?
        GROUP BY chunk_id
    """, (uid,)).fetchall()

    if not rows:
        conn.close()
        return base_score + MANUAL_IMPORTANCE.get(level, 50) * 0.2

    counts = {cid: cnt for cid, cnt, _ in rows}
    last_times = {cid: ts for cid, _, ts in rows}

    all_counts = list(counts.values())
    max_count = max(all_counts) if all_counts else 1
    min_count = min(all_counts) if all_counts else 0

    count_range = max(max_count - min_count, 1)

    # 访问频率标准化
    freq_w = (counts.get(chunk_id, 0) - min_count) / count_range

    # 最近访问时间：指数衰减，半衰期 7 天
    last_ts = last_times.get(chunk_id, 0)
    if last_ts > 0:
        age_days = (now - last_ts) / 86400
        recency_w = math.exp(-age_days / 7)  # 0-1, 越新越接近 1
    else:
        recency_w = 0

    # 手动重要性
    row = c.execute(
        "SELECT score FROM manual_importance WHERE chunk_id = ? AND uid = ?",
        (chunk_id, uid)
    ).fetchone()
    manual_w = (row[0] / 100) if row else (MANUAL_IMPORTANCE.get(level, 50) / 100)

    conn.close()

    score = base_score + (freq_w * 0.4 + recency_w * 0.4 + manual_w * 0.2) * 50
    return min(100.0, max(0.0, score))


def get_all_importance_scores(db_path, uid):
    """
    返回该用户所有 chunk 的重要性评分字典。
    {chunk_id: {"score": float, "access_count": int, "last_accessed": float}}
    """
    conn = sqlite3.connect(db_path)
    c = conn.cursor()

    rows = c.execute("""
        SELECT chunk_id, COUNT(*) as cnt, MAX(access_time) as last_ts
        FROM memory_access_log
        WHERE uid = ?
        GROUP BY chunk_id
    """, (uid,)).fetchall()

    manual_rows = dict(c.execute(
        "SELECT chunk_id, score FROM manual_importance WHERE uid = ?", (uid,)
    ).fetchall())

    conn.close()

    result = {}
    for chunk_id, cnt, last_ts in rows:
        # 从 vector DB 获取 level（需要传入 base_dir）
        result[chunk_id] = {
            "access_count": cnt,
            "last_accessed": last_ts,
            "manual_score": manual_rows.get(chunk_id),
        }

    return result


def print_report(db_path, uid, top_n=20):
    """打印访问报告"""
    conn = sqlite3.connect(db_path)
    c = conn.cursor()

    print(f"\nfrom typing import List, Dict, Optional, Union, Any, Tuple\n📊 记忆访问报告 — {uid}")
    print("=" * 50)

    # 访问最多
    rows = c.execute("""
        SELECT chunk_id, COUNT(*) as cnt, MAX(access_time)
        FROM memory_access_log
        WHERE uid = ?
        GROUP BY chunk_id
        ORDER BY cnt DESC
        LIMIT ?
    """, (uid, top_n)).fetchall()

    print(f"\n🔥 最活跃记忆 (Top {top_n}):")
    print(f"  {'排名':<4} {'chunk_id':<20} {'访问次数':>8} {'最后访问':>12}")
    print("  " + "-" * 48)
    for i, (cid, cnt, last_ts) in enumerate(rows, 1):
        ts = datetime.fromtimestamp(last_ts, tz=timezone.utc).strftime("%m-%d %H:%M") if last_ts else "从未"
        print(f"  {i:<4} {cid:<20} {cnt:>8} {ts:>12}")

    # 总访问量
    total = c.execute(
        "SELECT COUNT(*) FROM memory_access_log WHERE uid = ?", (uid,)
    ).fetchone()[0]
    print(f"\n📈 总访问次数: {total}")

    conn.close()


def main():
    parser = argparse.ArgumentParser(description="记忆访问日志与重要性评分")
    parser.add_argument("--base-dir", default=".", help="记忆仓库根目录")
    parser.add_argument("--uid", help="用户ID")
    parser.add_argument("--chunk-id", help="记忆块 ID（记录访问时用）")
    parser.add_argument("--access-type", default="read",
                        choices=["read", "search", "write", "manual_pin"],
                        help="访问类型")
    parser.add_argument("--report", action="store_true", help="打印访问报告")
    parser.add_argument("--get-importance", action="store_true",
                        help="输出 JSON 重要性评分（供其他脚本调用）")
    parser.add_argument("--set-importance", type=float, metavar="SCORE",
                        help="手动设置重要性 (0-100)")
    parser.add_argument("--set-note", default="", help="手动设置备注")
    args = parser.parse_args()

    uid = args.uid or os.environ.get("MEMORY_USER_ID", "default")
    db_path = get_db_path(args.base_dir)

    if not os.path.exists(db_path):
        init_access_db(db_path)

    if args.report:
        print_report(db_path, uid)
        return

    if args.get_importance:
        # 输出 JSON（从向量库读取 level）
        import sqlite3 as sqlite_internal
        vec_db = os.path.join(os.path.abspath(args.base_dir), ".memory_vectors.db")
        scores = get_all_importance_scores(db_path, uid)

        if os.path.exists(vec_db):
            vconn = sqlite_internal.connect(vec_db)
            vconn.execute("PRAGMA journal_mode=WAL")
            vcur = vconn.cursor()
            for cid in scores:
                row = vcur.execute(
                    "SELECT level FROM memory_embeddings WHERE chunk_id = ? AND uid = ?",
                    (cid, uid)
                ).fetchone()
                if row:
                    scores[cid]["level"] = row[0]
                    scores[cid]["score"] = calculate_importance_score(
                        db_path, uid, cid, row[0]
                    )
            vconn.close()

        print(json.dumps(scores))
        return

    if args.set_importance is not None:
        if not args.chunk_id:
            print("❌ --set-importance 需要 --chunk-id")
            sys.exit(1)
        set_manual_importance(db_path, args.chunk_id, uid, args.set_importance, args.set_note)
        print(f"✅ 已设置 {args.chunk_id} 重要性 = {args.set_importance}")
        return

    if args.chunk_id:
        log_access(db_path, args.chunk_id, uid, args.access_type)
        print(f"✅ 记录访问: {args.chunk_id} ({args.access_type})")
        return

    print("❌ 请指定操作: --report / --get-importance / --chunk-id <id>")
    parser.print_help()


if __name__ == "__main__":
    main()
