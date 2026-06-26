#!/usr/bin/env python3
"""SQLite 状态存储模块 - 替代 seen_announcements.json

数据库表:
  announcements: 存储已抓取公告的完整信息
  - ann_id (TEXT PRIMARY KEY): MD5 唯一标识
  - stock_code, stock_name: 股票信息
  - title, ann_date, ann_type: 公告摘要
  - url, art_code, notice_id: 完整数据
  - full_text: 公告全文（原始，来自 PDF 提取）
  - clean_text: 公告全文（经清洗，移除模板套话）
  - attach_url: PDF 附件链接
  - first_seen_at: 首次发现时间戳
"""

import hashlib
import json
import logging
import os
import sqlite3
from datetime import datetime

logger = logging.getLogger(__name__)

SKILL_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STATE_DIR = os.path.join(SKILL_DIR, ".stock-tracker-state")
DB_PATH = os.path.join(STATE_DIR, "announcements.db")

CREATE_TABLE_SQL = """
CREATE TABLE IF NOT EXISTS announcements (
    ann_id      TEXT PRIMARY KEY,
    stock_code  TEXT NOT NULL,
    stock_name  TEXT,
    title       TEXT,
    ann_date    TEXT,
    ann_type    TEXT,
    url         TEXT,
    art_code    TEXT,
    notice_id   TEXT,    -- 注意：实际存储的是公告日期（兼容旧数据，非 ID）
    full_text   TEXT,
    clean_text  TEXT,
    attach_url  TEXT,
    first_seen_at TEXT DEFAULT (datetime('now', 'localtime'))
)
"""

CREATE_INDEXES_SQL = [
    "CREATE INDEX IF NOT EXISTS idx_stock_code ON announcements(stock_code)",
    "CREATE INDEX IF NOT EXISTS idx_ann_date ON announcements(ann_date)",
    "CREATE INDEX IF NOT EXISTS idx_first_seen ON announcements(first_seen_at)",
    "CREATE INDEX IF NOT EXISTS idx_ann_type ON announcements(ann_type)",
]

INSERT_SQL = """
INSERT INTO announcements
    (ann_id, stock_code, stock_name, title, ann_date, ann_type,
     url, art_code, notice_id, full_text, clean_text, attach_url, status, ann_type_tag, ann_type_category, clean_text_length)
VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
ON CONFLICT(ann_id) DO UPDATE SET
    stock_code = excluded.stock_code,
    stock_name = CASE WHEN excluded.stock_name != '' THEN excluded.stock_name ELSE announcements.stock_name END,
    title = excluded.title,
    ann_date = excluded.ann_date,
    ann_type = excluded.ann_type,
    url = excluded.url,
    art_code = excluded.art_code,
    notice_id = excluded.notice_id,
    full_text = CASE WHEN excluded.full_text != '' THEN excluded.full_text ELSE announcements.full_text END,
    clean_text = CASE WHEN excluded.clean_text != '' THEN excluded.clean_text ELSE announcements.clean_text END,
    attach_url = CASE WHEN excluded.attach_url != '' THEN excluded.attach_url ELSE announcements.attach_url END,
    status = CASE WHEN excluded.status != '' THEN excluded.status ELSE announcements.status END,
    ann_type_tag = CASE WHEN excluded.ann_type_tag != '' THEN excluded.ann_type_tag ELSE announcements.ann_type_tag END,
    ann_type_category = CASE WHEN excluded.ann_type_category != '' THEN excluded.ann_type_category ELSE announcements.ann_type_category END,
    clean_text_length = CASE WHEN excluded.clean_text_length > 0 THEN excluded.clean_text_length ELSE announcements.clean_text_length END
"""

UPDATE_CONTENT_SQL = """
UPDATE announcements SET full_text = ?, clean_text = ?, clean_text_length = ?, attach_url = ?, status = 'valuable' WHERE ann_id = ?
"""

UPDATE_CLEAN_SQL = """
UPDATE announcements SET clean_text = ?, clean_text_length = ? WHERE ann_id = ?
"""

UPDATE_SUMMARY_SQL = """
UPDATE announcements SET summary = ? WHERE ann_id = ?
"""


def _get_conn() -> sqlite3.Connection:
    os.makedirs(STATE_DIR, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA foreign_keys=ON")
    return conn


def _migrate_schema(conn: sqlite3.Connection):
    for col, col_def in [("full_text", "TEXT"), ("clean_text", "TEXT"), ("attach_url", "TEXT"), ("summary", "TEXT"), ("status", "TEXT DEFAULT 'valuable'"), ("ann_type_tag", "TEXT DEFAULT ''"), ("ann_type_category", "TEXT DEFAULT ''"), ("clean_text_length", "INTEGER DEFAULT 0")]:
        try:
            conn.execute(f"ALTER TABLE announcements ADD COLUMN {col} {col_def}")
            logger.info("数据库迁移: 新增字段 %s", col)
        except sqlite3.OperationalError:
            pass


def init_db():
    conn = _get_conn()
    try:
        conn.execute(CREATE_TABLE_SQL)
        _migrate_schema(conn)
        for idx in CREATE_INDEXES_SQL:
            conn.execute(idx)
        conn.commit()

        old_json = os.path.join(STATE_DIR, "seen_announcements.json")
        if os.path.exists(old_json):
            _migrate_from_json(conn, old_json)
    finally:
        conn.close()


def _migrate_from_json(conn: sqlite3.Connection, json_path: str):
    cursor = conn.execute("SELECT COUNT(*) FROM announcements")
    if cursor.fetchone()[0] > 0:
        logger.info("数据库已有数据，跳过 JSON 迁移")
        return

    try:
        with open(json_path, "r") as f:
            hashes = json.load(f)
        if not hashes:
            return

        for h in hashes:
            conn.execute(
                INSERT_SQL,
                (h, "", "", "", "", "", "", "", "", "", "", "", "filtered", "", "", 0),
            )
        conn.commit()
        backup = json_path + ".bak"
        os.rename(json_path, backup)
        logger.info("已从 %s 迁移 %d 条记录到 SQLite", json_path, len(hashes))
        logger.info("原 JSON 文件已备份为 %s", backup)
    except Exception as e:
        logger.warning("JSON 迁移失败: %s", e)


def make_ann_id(ann: dict) -> str:
    raw = f"{ann['stock_code']}_{ann.get('art_code', '')}_{ann.get('notice_id', '')}_{ann['title']}"
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()


def get_seen_ids() -> set:
    conn = _get_conn()
    try:
        rows = conn.execute("SELECT ann_id FROM announcements").fetchall()
        return {row[0] for row in rows}
    finally:
        conn.close()


def record_announcements(announcements: list[dict]):
    if not announcements:
        return
    conn = _get_conn()
    try:
        count = 0
        for ann in announcements:
            ann_id = make_ann_id(ann)
            conn.execute(
                INSERT_SQL,
                (
                    ann_id,
                    ann["stock_code"],
                    ann["stock_name"],
                    ann["title"],
                    ann["ann_date"],
                    ann.get("ann_type", ""),
                    ann["url"],
                    ann.get("art_code", ""),
                    ann.get("notice_id", ""),
                    ann.get("full_text", ""),
                    ann.get("clean_text", ""),
                    ann.get("attach_url", ""),
                    ann.get("status", "filtered"),
                    ann.get("ann_type_tag", ""),
                    ann.get("ann_type_category", ""),
                    len(ann.get("clean_text", "")),
                ),
            )
            count += 1
        conn.commit()
        logger.info("已记录 %d 条公告到数据库", count)
    finally:
        conn.close()


def update_content(announcements: list[dict]):
    conn = _get_conn()
    try:
        count = 0
        for ann in announcements:
            full_text = ann.get("full_text", "")
            clean_text = ann.get("clean_text", "")
            attach_url = ann.get("attach_url", "")
            if not full_text and not attach_url:
                continue
            ann_id = make_ann_id(ann)
            conn.execute(UPDATE_CONTENT_SQL, (full_text, clean_text, len(clean_text), attach_url, ann_id))
            count += 1
        conn.commit()
        if count:
            logger.info("已更新 %d 条公告正文", count)
    finally:
        conn.close()


def update_clean_text(announcements: list[dict]):
    """批量更新清洗后的文本"""
    conn = _get_conn()
    try:
        count = 0
        for ann in announcements:
            clean_text = ann.get("clean_text", "")
            if not clean_text:
                continue
            ann_id = make_ann_id(ann)
            conn.execute(UPDATE_CLEAN_SQL, (clean_text, len(clean_text), ann_id))
            count += 1
        conn.commit()
        if count:
            logger.info("已清洗 %d 条公告", count)
    finally:
        conn.close()


def update_summary(ann_id: str, summary: str):
    """更新单条公告的摘要"""
    if not summary:
        return
    conn = _get_conn()
    try:
        conn.execute(UPDATE_SUMMARY_SQL, (summary, ann_id))
        conn.commit()
    finally:
        conn.close()


def get_stock_overview() -> list[dict]:
    """获取所有股票的概览统计（供 Web 仪表盘使用）"""
    conn = _get_conn()
    try:
        rows = conn.execute("""
            SELECT stock_code, stock_name,
                   COUNT(*) as total,
                   SUM(CASE WHEN status = 'valuable' THEN 1 ELSE 0 END) as valuable_total,
                   SUM(CASE WHEN ann_date >= date('now', '-7 days') THEN 1 ELSE 0 END) as total_7d,
                   SUM(CASE WHEN ann_date >= date('now', '-7 days') AND status = 'valuable' THEN 1 ELSE 0 END) as valuable_7d,
                   SUM(CASE WHEN ann_date >= date('now', '-15 days') THEN 1 ELSE 0 END) as total_15d,
                   SUM(CASE WHEN ann_date >= date('now', '-15 days') AND status = 'valuable' THEN 1 ELSE 0 END) as valuable_15d,
                   SUM(CASE WHEN ann_date >= date('now', '-30 days') THEN 1 ELSE 0 END) as total_30d,
                   SUM(CASE WHEN ann_date >= date('now', '-30 days') AND status = 'valuable' THEN 1 ELSE 0 END) as valuable_30d
            FROM announcements
            GROUP BY stock_code
            ORDER BY stock_name
        """).fetchall()
        return [
            {
                "stock_code": r[0], "stock_name": r[1],
                "valuable_7d": r[5], "total_7d": r[4],
                "valuable_15d": r[7], "total_15d": r[6],
                "valuable_30d": r[9], "total_30d": r[8],
                "valuable_total": r[3], "total": r[2],
            }
            for r in rows
        ]
    finally:
        conn.close()


def get_announcements_for_stock(stock_code: str, days: int = 30) -> list[dict]:
    """获取指定股票的公告列表（供 Web 仪表盘使用）"""
    conn = _get_conn()
    try:
        rows = conn.execute("""
            SELECT ann_id, stock_code, stock_name, title, ann_date,
                   clean_text, summary, url, attach_url, first_seen_at, ann_type_tag, ann_type_category
            FROM announcements
            WHERE stock_code = ? AND ann_date >= date('now', ? || ' days')
              AND status = 'valuable'
            ORDER BY ann_date DESC
        """, (stock_code, f"-{days}")).fetchall()
        return [
            {
                "ann_id": r[0], "stock_code": r[1], "stock_name": r[2],
                "title": r[3], "ann_date": r[4], "clean_text": r[5],
                "summary": r[6], "url": r[7], "attach_url": r[8],
                "first_seen_at": r[9], "ann_type_tag": r[10] if len(r) > 10 else "",
                "ann_type_category": r[11] if len(r) > 11 else "",
            }
            for r in rows
        ]
    finally:
        conn.close()


def get_records_needing_clean() -> list[dict]:
    """获取有原始全文但尚无清洗文本的记录"""
    conn = _get_conn()
    try:
        rows = conn.execute(
            "SELECT ann_id, stock_code, stock_name, title, art_code, notice_id, url, ann_date, full_text "
            "FROM announcements WHERE full_text IS NOT NULL AND full_text != '' "
            "AND (clean_text IS NULL OR clean_text = '')"
        ).fetchall()
        return [
            {
                "ann_id": r[0], "stock_code": r[1], "stock_name": r[2],
                "title": r[3], "art_code": r[4], "notice_id": r[5],
                "url": r[6], "ann_date": r[7], "full_text": r[8],
            }
            for r in rows
        ]
    finally:
        conn.close()


def get_pending_content() -> list[dict]:
    conn = _get_conn()
    try:
        rows = conn.execute(
            "SELECT ann_id, stock_code, stock_name, title, art_code, notice_id, url, ann_date "
            "FROM announcements WHERE (full_text IS NULL OR full_text = '') AND art_code != ''"
        ).fetchall()
        return [
            {
                "ann_id": r[0], "stock_code": r[1], "stock_name": r[2],
                "title": r[3], "art_code": r[4], "notice_id": r[5],
                "url": r[6], "ann_date": r[7],
            }
            for r in rows
        ]
    finally:
        conn.close()


def prune_empty():
    """删除被过滤的无效记录（status='filtered' 且无正文）"""
    conn = _get_conn()
    try:
        deleted = conn.execute(
            "DELETE FROM announcements WHERE status = 'filtered' AND (full_text IS NULL OR full_text = '')"
        ).rowcount
        conn.commit()
        if deleted:
            logger.info("已清理 %d 条被过滤的记录", deleted)
        return deleted
    finally:
        conn.close()


def _count_by_source(keyword: str) -> int:
    conn = _get_conn()
    try:
        return conn.execute(
            "SELECT COUNT(*) FROM announcements WHERE url LIKE ?", (f"%{keyword}%",)
        ).fetchone()[0]
    finally:
        conn.close()


def get_stats() -> dict:
    conn = _get_conn()
    try:
        total = conn.execute("SELECT COUNT(*) FROM announcements").fetchone()[0]
        with_text = conn.execute(
            "SELECT COUNT(*) FROM announcements WHERE full_text IS NOT NULL AND full_text != ''"
        ).fetchone()[0]
        stocks = conn.execute(
            "SELECT COUNT(DISTINCT stock_code) FROM announcements WHERE stock_code != ''"
        ).fetchone()[0]
        latest = conn.execute(
            "SELECT MAX(first_seen_at) FROM announcements"
        ).fetchone()[0] or "无"
        return {
            "total": total,
            "with_content": with_text,
            "stocks_tracked": stocks,
            "latest_update": latest,
        }
    finally:
        conn.close()


def list_announcements(stock_code: str = None, stock_codes: list[str] = None, days: int = None, limit: int = 100) -> list[dict]:
    conn = _get_conn()
    try:
        sql = (
            "SELECT ann_id, stock_code, stock_name, title, ann_date, ann_type, "
            "url, art_code, full_text, attach_url, first_seen_at FROM announcements"
        )
        conditions = []
        params = []

        if stock_code:
            conditions.append("stock_code = ?")
            params.append(stock_code)
        elif stock_codes:
            placeholders = ",".join("?" for _ in stock_codes)
            conditions.append(f"stock_code IN ({placeholders})")
            params.extend(stock_codes)

        if days:
            conditions.append("ann_date >= date('now', ? || ' days')")
            params.append(f"-{days}")

        if conditions:
            sql += " WHERE " + " AND ".join(conditions)

        sql += " ORDER BY first_seen_at DESC LIMIT ?"
        params.append(limit)

        rows = conn.execute(sql, params).fetchall()
        return [
            {
                "ann_id": r[0], "stock_code": r[1], "stock_name": r[2],
                "title": r[3], "ann_date": r[4], "ann_type": r[5],
                "url": r[6], "art_code": r[7],
                "full_text": r[8], "attach_url": r[9],
                "first_seen_at": r[10],
            }
            for r in rows
        ]
    finally:
        conn.close()


def get_announcements_with_summary(stock_codes: list[str] = None, days: int = 1) -> list[dict]:
    """获取有摘要的有价值公告（供 digest 输出使用）"""
    conn = _get_conn()
    try:
        sql = (
            "SELECT stock_code, stock_name, title, ann_date, summary, ann_type_tag, ann_type_category "
            "FROM announcements "
            "WHERE status = 'valuable' AND summary IS NOT NULL AND summary != '' "
            "AND ann_date >= date('now', ? || ' days') "
            "ORDER BY ann_date DESC, stock_code"
        )
        params = [f"-{days}"]

        if stock_codes:
            placeholders = ",".join("?" for _ in stock_codes)
            sql = sql.replace(
                "AND ann_date >= date('now', ? || ' days') ",
                f"AND stock_code IN ({placeholders}) AND ann_date >= date('now', ? || ' days') ",
            )
            params = stock_codes + params

        rows = conn.execute(sql, params).fetchall()
        return [
            {
                "stock_code": r[0], "stock_name": r[1],
                "title": r[2], "ann_date": r[3], "summary": r[4],
                "ann_type_tag": r[5] if len(r) > 5 else "",
                "ann_type_category": r[6] if len(r) > 6 else "",
            }
            for r in rows
        ]
    finally:
        conn.close()


init_db()
