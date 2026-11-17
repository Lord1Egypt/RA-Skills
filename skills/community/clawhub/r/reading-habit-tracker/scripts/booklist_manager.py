#!/usr/bin/env python3
"""
booklist_manager.py — 書單管理
想讀 / 在讀 / 已讀 / 放棄 四象限管理
"""

import sys
import json
import argparse
from pathlib import Path
from datetime import date

DATA_DIR   = Path.home() / ".bookshelf-plus" / "habit_tracker"
BOOKLIST_F = DATA_DIR / "booklist.json"


def _load() -> dict:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    if BOOKLIST_F.exists():
        return json.loads(BOOKLIST_F.read_text(encoding="utf-8"))
    return {"books": []}


def _save(data: dict):
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    BOOKLIST_F.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


STATUS_META = {
    "to-read":   ("📋 想讀", "想讀"),
    "reading":   ("📖 在讀", "在讀"),
    "finished":  ("✅ 已讀", "已讀"),
    "paused":    ("⏸  暫停", "暫停"),
    "abandoned": ("🗑 放棄", "放棄"),
}

STATUS_ORDER = ["reading", "to-read", "finished", "paused", "abandoned"]


def _render_book(b: dict) -> str:
    title   = b.get("title", "未知")
    status  = b.get("status", "unknown")
    meta    = STATUS_META.get(status, ("❓ 未知", "未知"))
    pages   = b.get("total_pages", 0) or 0
    added   = b.get("added", "")
    finished = b.get("finished_date", "")

    lines = [
        f"  {meta[0]} 《{title}》"
    ]
    if pages:
        lines.append(f"       📄 {pages} 頁")
    if added:
        lines.append(f"       📅 新增：{added}")
    if finished:
        lines.append(f"       🎉 讀完：{finished}")
    note = b.get("note", "")
    if note:
        lines.append(f"       📝 {note}")
    rating = b.get("rating", 0)
    if rating:
        stars = "⭐" * int(rating)
        lines.append(f"       {stars}")
    return "\n".join(lines)


def add_book(args) -> str:
    data  = _load()
    books = data.get("books", [])

    # 檢查是否已存在
    for b in books:
        if b.get("title") == args.title:
            old = b.get("status", "")
            b["status"]   = args.status
            b["updated"]  = date.today().isoformat()
            b["note"]     = args.note or b.get("note", "")
            if args.pages: b["total_pages"] = args.pages
            _save(data)
            return f"✅ 「{args.title}」狀態已更新：{old} → {args.status}"

    books.append({
        "title":       args.title,
        "status":      args.status,
        "total_pages": args.pages or 0,
        "author":      args.author or "",
        "category":    args.category or "",
        "note":        args.note or "",
        "rating":      0,
        "added":       date.today().isoformat(),
        "updated":     date.today().isoformat(),
    })
    data["books"] = books
    _save(data)
    return f"✅ 已加入「{args.title}」（📋 {args.status}）"


def list_books(args) -> str:
    data  = _load()
    books = data.get("books", [])

    if args.status:
        books = [b for b in books if b.get("status") == args.status]
    elif args.category:
        books = [b for b in books if b.get("category") == args.category]
    elif args.search:
        books = [b for b in books
                if args.search.lower() in b.get("title", "").lower()
                or args.search.lower() in b.get("author", "").lower()]

    if not books:
        return "📭 書單為空，或找不到符合條件的書籍"

    # 按狀態分組
    by_status: dict[str, list] = {}
    for b in books:
        by_status.setdefault(b.get("status", "unknown"), []).append(b)

    lines = [f"\n📚 書單（共 {len(books)} 本）"]
    lines.append("─" * 44)

    for status in STATUS_ORDER:
        bs = by_status.get(status, [])
        if not bs:
            continue
        meta = STATUS_META.get(status, ("❓", "未知"))
        lines.append(f"\n  {meta[0]}（{len(bs)} 本）")
        for b in bs:
            lines.append(_render_book(b))

    return "\n".join(lines)


def update_status(title_frag: str, new_status: str) -> str:
    data  = _load()
    books = data.get("books", [])
    found = False

    for b in books:
        if title_frag.lower() in b.get("title", "").lower():
            old = b.get("status", "")
            b["status"]      = new_status
            b["updated"]     = date.today().isoformat()
            if new_status == "finished":
                b["finished_date"] = date.today().isoformat()
            found = True

    if not found:
        return f"❌ 找不到包含「{title_frag}」的書籍"

    _save(data)
    return f"✅ 「{title_frag}」已更新：{old} → {new_status}"


def rate_book(title_frag: str, rating: int) -> str:
    data  = _load()
    books = data.get("books", [])
    for b in books:
        if title_frag.lower() in b.get("title", "").lower():
            b["rating"]  = rating
            b["updated"] = date.today().isoformat()
            _save(data)
            return f"✅ 《{b['title']}》評分：{'⭐' * rating}"
    return f"❌ 找不到書籍"


def remove_book(title_frag: str) -> str:
    data  = _load()
    books = data.get("books", [])
    before = len(books)
    books = [b for b in books if title_frag.lower() not in b.get("title", "").lower()]
    if len(books) == before:
        return f"❌ 找不到包含「{title_frag}」的書籍"
    data["books"] = books
    _save(data)
    return f"✅ 已移除（含「{title_frag}」）的書籍"


def export_json() -> str:
    return json.dumps(_load(), ensure_ascii=False, indent=2)


# ── CLI ───────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="書單管理器")
    sub = parser.add_subparsers(dest="cmd")

    p_add = sub.add_parser("add", help="新增書籍")
    p_add.add_argument("--title",    "-t", required=True)
    p_add.add_argument("--status",  choices=list(STATUS_META.keys()),
                       default="to-read")
    p_add.add_argument("--pages",    type=int, default=0)
    p_add.add_argument("--author",   default="")
    p_add.add_argument("--category", default="")
    p_add.add_argument("--note",     default="")

    p_list = sub.add_parser("list", help="列出書單")
    p_list.add_argument("--status",   choices=list(STATUS_META.keys()))
    p_list.add_argument("--category")
    p_list.add_argument("--search")

    p_move = sub.add_parser("move", help="移動書籍狀態")
    p_move.add_argument("title",  help="書名關鍵字")
    p_move.add_argument("status", choices=list(STATUS_META.keys()))

    p_rate = sub.add_parser("rate", help="評分書籍")
    p_rate.add_argument("title",  help="書名關鍵字")
    p_rate.add_argument("rating", type=int, choices=[1,2,3,4,5])

    p_rm = sub.add_parser("remove", help="移除書籍")
    p_rm.add_argument("title", help="書名關鍵字")

    args = parser.parse_args(sys.argv[2:] if len(sys.argv) > 2 else [""])

    if args.cmd == "add":
        print(add_book(args))
    elif args.cmd == "list":
        print(list_books(args))
    elif args.cmd == "move":
        print(update_status(args.title, args.status))
    elif args.cmd == "rate":
        print(rate_book(args.title, args.rating))
    elif args.cmd == "remove":
        print(remove_book(args.title))
    else:
        print(list_books(args))


if __name__ == "__main__":
    main()
