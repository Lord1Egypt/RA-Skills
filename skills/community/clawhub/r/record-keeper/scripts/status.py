#!/usr/bin/env python3
"""
记录状态更新工具
根据状态流转规范，更新 records 表中指定记录的状态。
"""

import sys
import sqlite3
from pathlib import Path
from datetime import datetime

# =====================================================================
# 配置
# =====================================================================
DB_PATH = Path.cwd() / "vectors" / "embeddings.db"

# =====================================================================
# 合法流转矩阵：当前状态 → 允许流转的目标状态
# =====================================================================
VALID_TRANSITIONS = {
    "open":         {"pending", "in_progress", "done", "deferred"},
    "pending":      {"in_progress", "done", "deferred"},
    "in_progress":  {"pending", "done", "deferred"},
    "done":         set(),  # done 不可逆
    "deferred":     {"open", "in_progress", "done"},
}

# =====================================================================
# 原文到状态值的归一化映射
# =====================================================================
STATUS_NORMALIZE = {
    # done 类（精确匹配）
    "done": "done",
    "已完成": "done",
    "✅ 已完成": "done",
    "已交付": "done",
    "已上线": "done",
    "已归档": "done",
    "fixed": "done",
    "✅ 已修复": "done",
    "✅ 已修复（线上环境）": "done",
    "已修复": "done",
    "verified": "done",
    "验证通过": "done",
    "✅ done": "done",
    # pending 类
    "pending": "pending",
    "待评审": "pending",
    "待分配": "pending",
    "待确认": "pending",
    "已建档": "pending",
    # in_progress 类
    "in_progress": "in_progress",
    "进行中": "in_progress",
    "处理中": "in_progress",
    "调查中": "in_progress",
    "已分配": "in_progress",
    "转交排查": "in_progress",
    "联调中": "in_progress",
    # open 类
    "open": "open",
    "未开始": "open",
    "待处理": "open",
    "待启动": "open",
    "新建": "open",
    # deferred 类
    "deferred": "deferred",
    "已延期": "deferred",
    "已挂起": "deferred",
    "搁置": "deferred",
}

# =====================================================================
# 各类别可用状态（严格封闭）
# =====================================================================
CATEGORY_ALLOWED = {
    "badcase":     {"open", "in_progress", "done", "deferred"},
    "task":        {"open", "in_progress", "done", "deferred"},
    "plan":        {"open", "pending", "in_progress", "done", "deferred"},
    "requirement": {"open", "pending", "in_progress", "done", "deferred"},
    "meeting":     {"open", "done"},
    "report":      {"open", "in_progress", "done"},
    "sop":         {"open", "pending", "done"},
    "weekly":      {"open", "done"},
    "monthly":     {"open", "done"},
    "quarterly":   {"open", "done"},
    "yearly":      {"open", "done"},
    "admin":       {"open", "in_progress", "done", "deferred"},
    "memo":        {"open", "done"},
    "adjust":      {"open", "done"},
    "sql":         {"open", "done"},
}


def get_db() -> sqlite3.Connection:
    """打开 SQLite 数据库"""
    if not DB_PATH.exists():
        raise FileNotFoundError(f"数据库不存在: {DB_PATH}")
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    return conn


def ensure_status_column(conn: sqlite3.Connection):
    """确保 status 列存在（首次运行自动添加）"""
    try:
        conn.execute("ALTER TABLE records ADD COLUMN status TEXT DEFAULT 'open'")
        conn.commit()
        print("  ✅ 已添加 status 列")
    except sqlite3.OperationalError:
        pass  # 列已存在


def normalize_status(text: str) -> str | None:
    """将原文表述归一化为标准状态值"""
    if text in STATUS_NORMALIZE:
        return STATUS_NORMALIZE[text]
    
    # 预处理：去掉括号后缀（如 "已完成（2026-06-11 上线）" → "已完成"）
    import re
    cleaned = re.sub(r"[（(][^）)]*[）)]", "", text).strip()
    if cleaned in STATUS_NORMALIZE:
        return STATUS_NORMALIZE[cleaned]
    
    # 尝试模糊匹配（去掉 ✅ 等前缀）
    for key, val in STATUS_NORMALIZE.items():
        if key.replace("✅", "").replace(" ", "").strip() == text.replace("✅", "").replace(" ", "").strip():
            return val
        if key.replace("✅", "").replace(" ", "").strip() == cleaned.replace("✅", "").replace(" ", "").strip():
            return val
    return None


def cmd_set(record_id: str, new_status: str):
    """设置指定记录的状态"""
    if not DB_PATH.exists():
        print("❌ 数据库不存在，请先运行 embed.py init")
        return

    conn = get_db()
    ensure_status_column(conn)

    # 查询当前记录
    row = conn.execute(
        "SELECT id, filename, category, status FROM records WHERE id = ?",
        (record_id,)
    ).fetchone()

    if not row:
        print(f"❌ 未找到记录: {record_id}")
        conn.close()
        return

    current = row["status"] or "open"
    category = row["category"]
    filename = row["filename"]

    # 校验目标状态值
    allowed = CATEGORY_ALLOWED.get(category, set())
    if new_status not in {"open", "pending", "in_progress", "done", "deferred"}:
        print(f"❌ 无效状态值: {new_status}")
        print(f"  允许的值: open, pending, in_progress, done, deferred")
        conn.close()
        return

    # 校验类别是否允许该状态
    if new_status not in allowed:
        print(f"❌ 类别 '{category}' 不允许状态 '{new_status}'")
        print(f"  允许的状态: {', '.join(sorted(allowed))}")
        conn.close()
        return

    # 校验流转合法性
    if new_status not in VALID_TRANSITIONS.get(current, set()):
        print(f"❌ 非法流转: {current} → {new_status}")
        print(f"  当前状态: {current}")
        print(f"  允许流转至: {', '.join(sorted(VALID_TRANSITIONS.get(current, set()))) or '（已终止，不可流转）'}")
        conn.close()
        return

    # 执行更新
    now = datetime.now().isoformat()
    conn.execute(
        "UPDATE records SET status = ?, updated_at = ? WHERE id = ?",
        (new_status, now, record_id)
    )
    conn.commit()
    conn.close()

    print(f"✅ {filename}")
    print(f"   {category} | {current} → {new_status}")


def cmd_set_by_file(filename: str, new_status: str):
    """通过文件名设置状态（模糊匹配）"""
    if not DB_PATH.exists():
        print("❌ 数据库不存在，请先运行 embed.py init")
        return

    conn = get_db()
    ensure_status_column(conn)

    # 多级匹配：精确 → 包含 → 前缀
    for pattern, label in [
        (filename, "精确匹配"),
        (f"%{filename}%", "包含匹配"),
        (filename + "%", "前缀匹配"),
    ]:
        row = conn.execute(
            "SELECT id, filename, category, status FROM records WHERE filename LIKE ?",
            (pattern,)
        ).fetchone()
        if row:
            break

    if not row:
        print(f"❌ 未找到匹配文件: {filename}")
        conn.close()
        return

    record_id = row["id"]
    conn.close()
    cmd_set(record_id, new_status)


def cmd_list(category: str = None, status: list = None, since: str = None):
    """列出记录的状态
    
    since: 按 updated_at 过滤。支持 'today'（今天）、'7d'（最近7天）、或 YYYYMMDD 格式。
    """
    """列出记录的状态"""
    if not DB_PATH.exists():
        print("❌ 数据库不存在，请先运行 embed.py init")
        return

    conn = get_db()
    ensure_status_column(conn)

    sql = "SELECT filename, category, status FROM records WHERE 1=1"
    params = []

    if category:
        sql += " AND category = ?"
        params.append(category)
    if status:
        placeholders = ",".join(["?"] * len(status))
        sql += f" AND status IN ({placeholders})"
        params.extend(status)

    if since:
        if since == "today":
            sql += " AND date(updated_at) = date('now', 'localtime')"
        elif since == "7d":
            sql += " AND updated_at >= datetime('now', 'localtime', '-7 days')"
        else:
            # 按 YYYYMMDD 过滤（updated_at >= 指定日期的 00:00:00）
            sql += " AND date(updated_at) >= ?"
            params.append(since)

    sql += " ORDER BY date DESC"

    rows = conn.execute(sql, params).fetchall()
    conn.close()

    if not rows:
        print("  未找到匹配记录")
        return

    print(f"\n{'状态':<14} {'类别':<14} 文件名")
    print("-" * 80)
    for row in rows:
        s = row["status"] or "open"
        print(f"{s:<14} {row['category']:<14} {row['filename']}")
    print(f"\n共 {len(rows)} 条")


def cmd_normalize(text: str):
    """测试归一化：将原文表述转为标准状态值"""
    result = normalize_status(text)
    if result:
        print(f"  \"{text}\" → \"{result}\"")
    else:
        print(f"  ❌ 无法归一化: \"{text}\"")
        print(f"  可用原文值: {', '.join(STATUS_NORMALIZE.keys())}")


# =====================================================================
# CLI 入口
# =====================================================================
def main():
    if len(sys.argv) < 2:
        print("用法：")
        print("  python3 status.py set <record_id> <status>      # 按记录 ID 设置状态")
        print("  python3 status.py set-file <文件名> <status>    # 按文件名设置状态")
        print("  python3 status.py list [--category badcase] [--status done]  # 列出状态")
        print("  python3 status.py normalize \"已完成\"            # 测试归一化")
        print()
        print("状态值: open, pending, in_progress, done, deferred")
        return

    cmd = sys.argv[1]

    if cmd == "set":
        if len(sys.argv) < 4:
            print("用法: python3 status.py set <record_id> <status>")
            return
        cmd_set(sys.argv[2], sys.argv[3])

    elif cmd == "set-file":
        if len(sys.argv) < 4:
            print("用法: python3 status.py set-file <文件名> <status>")
            return
        cmd_set_by_file(sys.argv[2], sys.argv[3])

    elif cmd == "list":
        category = None
        status = []
        since = None
        i = 2
        while i < len(sys.argv):
            if sys.argv[i] == "--category" and i + 1 < len(sys.argv):
                category = sys.argv[i + 1]
                i += 2
            elif sys.argv[i] == "--status" and i + 1 < len(sys.argv):
                status.append(sys.argv[i + 1])
                i += 2
            elif sys.argv[i] == "--since" and i + 1 < len(sys.argv):
                since = sys.argv[i + 1]
                i += 2
            else:
                i += 1
        cmd_list(category=category, status=status, since=since)

    elif cmd == "normalize":
        if len(sys.argv) < 3:
            print("用法: python3 status.py normalize \"原文表述\"")
            return
        cmd_normalize(sys.argv[2])

    else:
        print(f"❌ 未知命令: {cmd}")
        print("可用命令: set, set-file, list, normalize")


if __name__ == "__main__":
    main()
