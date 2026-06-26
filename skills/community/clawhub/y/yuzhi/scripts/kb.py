#!/usr/bin/env python3
"""御知库 CLI - 知识库管理工具"""
import sys
import os
import re
import json
import sqlite3
import argparse
from pathlib import Path
from datetime import datetime

YUZHI_DIR = Path.home() / ".yuzhi"
DB_PATH = YUZHI_DIR / "index.db"
TAGS = ["制度", "项目", "决策", "人物", "技术", "笔记", "其他"]

YUZHI_DIR.mkdir(exist_ok=True)

def get_db():
    conn = sqlite3.connect(str(DB_PATH))
    conn.execute("PRAGMA journal_mode=WAL")
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    conn.execute("""CREATE TABLE IF NOT EXISTS kb (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        path TEXT UNIQUE NOT NULL,
        tag TEXT DEFAULT '其他',
        title TEXT,
        summary TEXT,
        content TEXT,
        created_at TEXT,
        updated_at TEXT
    )""")
    conn.commit()
    conn.close()

def safe_tag(tag):
    return tag if tag in TAGS else "其他"

ALLOWED_ROOTS = [
    Path.home() / ".yuzhi",
    Path.home() / "Desktop",
    Path.home() / "Documents",
    Path.home() / "Downloads",
]

def _is_allowed_path(file_path):
    """防止读取敏感目录，限制在白名单目录内"""
    try:
        abs_path = Path(file_path).resolve()
        for root in ALLOWED_ROOTS:
            if abs_path.is_relative_to(root.resolve()):
                return True
        for ws in Path.home().iterdir():
            if ws.is_dir() and (".openclaw" in str(ws) or "workspaces" in str(ws)):
                if abs_path.is_relative_to(ws.resolve()):
                    return True
    except Exception:
        pass
    return False

def extract_text_from_file(file_path):
    """从文件提取文本"""
    path = Path(file_path)
    try:
        if path.suffix in (".md", ".txt"):
            return path.read_text(encoding="utf-8", errors="ignore")
        elif path.suffix == ".pdf":
            import subprocess
            script = f"import pdfplumber; p=pdfplumber.open({str(path)!r}); print('\\n'.join([x.extract_text() or '' for x in p.pages]))"
            result = subprocess.run(
                ["python3", "-c", script],
                capture_output=True, text=True, timeout=30
            )
            if result.returncode == 0:
                return result.stdout.strip()
        else:
            return path.read_text(encoding="utf-8", errors="ignore")
    except Exception:
        pass
    return ""

def extract_summary(text, max_len=200):
    text = re.sub(r'#+\s+', '', text)
    text = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', text)
    text = re.sub(r'\n+', ' ', text).strip()
    return text[:max_len] + ("..." if len(text) > max_len else "")

def cmd_add(file_path, tag="其他", title=None):
    if not Path(file_path).exists():
        print(f"❌ 文件不存在: {file_path}")
        return
    if not _is_allowed_path(file_path):
        print(f"❌ 不允许添加该路径（仅允许 ~/.yuzhi、桌面、文档、Downloads、workspaces）：{file_path}")
        return
    content = extract_text_from_file(file_path)
    if not content.strip():
        print(f"⚠️ 无法提取文本: {file_path}")
        return
    title = title or Path(file_path).stem
    summary = extract_summary(content)
    tag = safe_tag(tag)
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT id FROM kb WHERE path=?", (str(file_path),))
    existing = cur.fetchone()
    if existing:
        cur.execute("UPDATE kb SET title=?,summary=?,content=?,tag=?,updated_at=? WHERE id=?",
                    (title, summary, content, tag, now, existing["id"]))
        print(f"✅ 更新: {title}")
    else:
        cur.execute("INSERT INTO kb (path,tag,title,summary,content,created_at,updated_at) VALUES (?,?,?,?,?,?,?)",
                    (str(file_path), tag, title, summary, content, now, now))
        print(f"✅ 添加: {title}")
    conn.commit()
    conn.close()

def simple_search(query, limit=5):
    """基于字符重叠的简单语义搜索"""
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT id, title, summary, content, tag, path FROM kb")
    rows = cur.fetchall()
    conn.close()
    query_words = set(re.findall(r'[\w\u4e00-\u9fff]{2,}', query.lower()))
    scored = []
    for r in rows:
        text = ((r["content"] or "") + " " + (r["summary"] or "")).lower()
        text_words = set(re.findall(r'[\w\u4e00-\u9fff]{2,}', text))
        if not query_words:
            continue
        score = len(query_words & text_words) / len(query_words)
        if score >= 0.05:
            scored.append((score, dict(r)))
    scored.sort(key=lambda x: -x[0])
    return [r for _, r in scored[:limit]]

def keyword_search(query, limit=5):
    """关键词 LIKE 搜索"""
    conn = get_db()
    cur = conn.cursor()
    pattern = f"%{query}%"
    cur.execute("""SELECT id, title, summary, tag, path, content FROM kb
                  WHERE title LIKE ? OR summary LIKE ? OR content LIKE ? OR tag LIKE ?
                  LIMIT ?""",
                (pattern, pattern, pattern, pattern, limit))
    rows = [dict(r) for r in cur.fetchall()]
    conn.close()
    return rows

def cmd_search(query, mode="all", limit=5):
    results_map = {}
    seen_ids = set()
    if mode in ("keyword", "all"):
        kws = keyword_search(query, limit)
        for r in kws:
            if r["id"] not in seen_ids:
                r["match"] = "keyword"
                results_map[r["id"]] = r
                seen_ids.add(r["id"])
    if mode in ("semantic", "all"):
        sems = simple_search(query, limit)
        for r in sems:
            if r["id"] not in seen_ids:
                r["match"] = "semantic"
                results_map[r["id"]] = r
                seen_ids.add(r["id"])
    results = list(results_map.values())[:limit]
    if not results:
        print("🔍 未找到相关结果")
        return []
    print(f"🔍 找到 {len(results)} 条结果：")
    for i, r in enumerate(results, 1):
        icon = "🔑" if r["match"] == "keyword" else "📖"
        snippet = r.get("summary", "")[:100]
        print(f"\n{icon} [{i}] {r['title']} ({r['tag']})")
        print(f"   {snippet}...")
        print(f"   📁 {r['path']}")
    return results

def cmd_list(tag=None, limit=20):
    conn = get_db()
    cur = conn.cursor()
    if tag:
        cur.execute("SELECT id, title, tag, path, summary, created_at FROM kb WHERE tag=? ORDER BY id DESC LIMIT ?", (tag, limit))
    else:
        cur.execute("SELECT id, title, tag, path, summary, created_at FROM kb ORDER BY id DESC LIMIT ?", (limit,))
    rows = cur.fetchall()
    conn.close()
    if not rows:
        print("📂 知识库为空")
        return
    print(f"📂 知识库（共 {len(rows)} 条）：")
    for r in rows:
        print(f"\n  [{r['id']}] {r['title']} — {r['tag']}")
        print(f"     {str(r['summary'] or '')[:80]}...")
        print(f"     📁 {r['path']} | {r['created_at']}")

def cmd_stats():
    total_size = sum(f.stat().st_size for f in YUZHI_DIR.rglob("*") if f.is_file()) / 1024
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) as cnt FROM kb")
    total = cur.fetchone()["cnt"]
    cur.execute("SELECT tag, COUNT(*) as cnt FROM kb GROUP BY tag ORDER BY cnt DESC")
    tags = cur.fetchall()
    conn.close()
    print(f"📊 御知库统计：")
    print(f"   总文件：{total} 条")
    print(f"   存储大小：{total_size:.1f} KB")
    print(f"   标签分布：")
    for t in tags:
        print(f"   - {t['tag']}: {t['cnt']} 条")

def cmd_delete(doc_id):
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT id, title FROM kb WHERE id=?", (doc_id,))
    r = cur.fetchone()
    if not r:
        print(f"❌ 条目 {doc_id} 不存在")
        conn.close()
        return
    cur.execute("DELETE FROM kb WHERE id=?", (doc_id,))
    conn.commit()
    conn.close()
    print(f"✅ 已删除: {r['title']}")

if __name__ == "__main__":
    init_db()
    parser = argparse.ArgumentParser(description="御知库 CLI", prog="yuzhi")
    sub = parser.add_subparsers(dest="cmd")

    p_add = sub.add_parser("add", help="添加文件")
    p_add.add_argument("file")
    p_add.add_argument("--tag", default="其他", choices=TAGS)
    p_add.add_argument("--title")

    p_search = sub.add_parser("search", help="搜索")
    p_search.add_argument("query")
    p_search.add_argument("--mode", default="all", choices=["semantic","keyword","all"])
    p_search.add_argument("--limit", type=int, default=5)

    p_list = sub.add_parser("list", help="列出文件")
    p_list.add_argument("--tag", default=None, choices=TAGS)
    p_list.add_argument("--limit", type=int, default=20)

    p_stats = sub.add_parser("stats", help="统计")
    p_del = sub.add_parser("delete", help="删除")
    p_del.add_argument("id", type=int)

    args = parser.parse_args()

    if args.cmd == "add":
        cmd_add(args.file, args.tag, args.title)
    elif args.cmd == "search":
        cmd_search(args.query, args.mode, args.limit)
    elif args.cmd == "list":
        cmd_list(args.tag, args.limit)
    elif args.cmd == "stats":
        cmd_stats()
    elif args.cmd == "delete":
        cmd_delete(args.id)
    else:
        parser.print_help()
