#!/usr/bin/env python3
"""
session_logger.py — 閱讀 Session 記錄器
記錄每次閱讀：書名、頁數、時長、章節、備註
"""

import sys
import json
import argparse
from pathlib import Path
from datetime import datetime, date, timedelta

DATA_DIR    = Path.home() / ".bookshelf-plus" / "habit_tracker"
SESSIONS_F  = DATA_DIR / "sessions.json"
BOOKLIST_F  = DATA_DIR / "booklist.json"


def _load_sessions() -> dict:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    if SESSIONS_F.exists():
        return json.loads(SESSIONS_F.read_text(encoding="utf-8"))
    return {"sessions": [], "last_updated": ""}


def _save(data: dict):
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    SESSIONS_F.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def _load_booklist() -> dict:
    if BOOKLIST_F.exists():
        return json.loads(BOOKLIST_F.read_text(encoding="utf-8"))
    return {"books": []}


def _save_booklist(data: dict):
    BOOKLIST_F.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def _book_status(title: str) -> str:
    books = _load_booklist().get("books", [])
    for b in books:
        if b.get("title") == title:
            return b.get("status", "unknown")
    return "unknown"


def _update_book_status(title: str, status: str):
    data = _load_booklist()
    books = data.get("books", [])
    for b in books:
        if b.get("title") == title:
            b["status"] = status
            b["updated"] = date.today().isoformat()
            break
    else:
        books.append({
            "title":   title,
            "status":  status,
            "added":   date.today().isoformat(),
            "updated": date.today().isoformat(),
        })
    data["books"] = books
    _save_booklist(data)


def _estimate_speed(pages: int, minutes: int) -> float:
    if minutes <= 0: return 0
    return pages / minutes * 60  # 頁/小時


# ── log ──────────────────────────────────────────────────────────────────────

def log_session(args) -> dict:
    data     = _load_sessions()
    today    = date.today().isoformat()
    sessions = data.get("sessions", [])

    session = {
        "id":           len(sessions) + 1,
        "date":         today,
        "book":         args.title,
        "pages_read":   args.pages,
        "from_page":    args.from_page or 0,
        "to_page":      args.to_page or 0,
        "duration_minutes": args.minutes,
        "chapter":      args.chapter or "",
        "note":         args.note or "",
        "speed":        _estimate_speed(args.pages, args.minutes),
        "created_at":   datetime.now().isoformat(),
    }
    sessions.append(session)
    data["sessions"] = sessions
    data["last_updated"] = today
    _save(data)

    # 自動更新書單狀態
    current_status = _book_status(args.title)
    if current_status in ("to-read", "unknown"):
        _update_book_status(args.title, "reading")

    # 自動標記已完成
    if args.finished:
        _update_book_status(args.title, "finished")
        session["finished"] = True

    return session


def _print_session(s: dict, verbose: bool = False) -> str:
    icon = "✅" if s.get("finished") else "📖"
    lines = [
        f"  {icon} [{s['date']}] {s['book']}",
        f"     📄 {s['pages_read']} 頁"
    ]
    if s.get("duration_minutes"):
        lines.append(f"     ⏱️  {s['duration_minutes']} 分鐘")
    if s.get("chapter"):
        lines.append(f"     📑 {s['chapter']}")
    if s.get("note"):
        lines.append(f"     📝 {s['note']}")
    if s.get("speed"):
        lines.append(f"     🚀 閱讀速度：{s['speed']:.0f} 頁/小時")
    return "\n".join(lines)


# ── view ─────────────────────────────────────────────────────────────────────

def view_history(args) -> str:
    data     = _load_sessions()
    sessions = data.get("sessions", [])
    today    = date.today()

    if args.book:
        sessions = [s for s in sessions if args.book in s.get("book", "")]

    if args.days:
        cutoff = (today - timedelta(days=args.days)).isoformat()
        sessions = [s for s in sessions if s.get("date", "") >= cutoff]

    sessions.sort(key=lambda x: x.get("date", ""), reverse=True)

    if not sessions:
        return "📭 尚無閱讀記錄，使用 log 指令新增。"

    # 摘要
    total_pages  = sum(s.get("pages_read", 0) for s in sessions)
    total_mins   = sum(s.get("duration_minutes", 0) for s in sessions)
    unique_books = len(set(s.get("book", "") for s in sessions))
    finished     = len([s for s in sessions if s.get("finished")])

    header = f"📊 閱讀記錄（共 {len(sessions)} 筆記錄）"
    summary = (
        f"  📚 {unique_books} 本書  "
        f"  📄 {total_pages:,} 頁  "
        f"  ⏱️  {total_mins//60}h {total_mins%60}min  "
        f"  ✅ {finished} 本讀完"
    )

    entries = "\n".join(
        _print_session(s)
        for s in sessions[: args.limit or 20]
    )

    return f"{header}\n{summary}\n\n{entries}"


# ── delete / edit ─────────────────────────────────────────────────────────────

def delete_session(session_id: int) -> str:
    data     = _load_sessions()
    sessions = data.get("sessions", [])
    before   = len(sessions)
    sessions = [s for s in sessions if s.get("id") != session_id]
    if len(sessions) == before:
        return f"❌ 找不到 ID={session_id} 的記錄"
    data["sessions"] = sessions
    _save(data)
    return f"✅ 已刪除 ID={session_id}（共刪除 {before - len(sessions)} 筆）"


def edit_session(session_id: int, pages: int = None, minutes: int = None,
                 note: str = None) -> str:
    data     = _load_sessions()
    sessions = data.get("sessions", [])
    for s in sessions:
        if s.get("id") == session_id:
            if pages   is not None: s["pages_read"]       = pages
            if minutes is not None: s["duration_minutes"] = minutes
            if note    is not None: s["note"]             = note
            s["speed"] = _estimate_speed(
                s.get("pages_read", 0), s.get("duration_minutes", 0))
            _save(data)
            return f"✅ 已更新 ID={session_id}"
    return f"❌ 找不到 ID={session_id}"


# ── CLI ───────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="閱讀 Session 記錄")
    sub = parser.add_subparsers(dest="cmd")

    # log
    p = sub.add_parser("log", help="記錄一次閱讀")
    p.add_argument("--title",    "-t", required=True)
    p.add_argument("--pages",    "-p", type=int, required=True)
    p.add_argument("--minutes",  "-m", type=int, default=0)
    p.add_argument("--from-page", type=int)
    p.add_argument("--to-page",  type=int)
    p.add_argument("--chapter",  "-c")
    p.add_argument("--note",     "-n")
    p.add_argument("--finished",  action="store_true",
                  help="標記此書已讀完")

    # history
    ph = sub.add_parser("history", help="查看歷史記錄")
    ph.add_argument("--book",   help="書名關鍵字篩選")
    ph.add_argument("--days",   type=int, help="最近 N 天")
    ph.add_argument("--limit",  type=int, default=20)

    # delete
    pd = sub.add_parser("delete", help="刪除記錄")
    pd.add_argument("id", type=int, help="Session ID")

    # edit
    pe = sub.add_parser("edit", help="編輯記錄")
    pe.add_argument("id",   type=int)
    pe.add_argument("--pages",   type=int)
    pe.add_argument("--minutes", type=int)
    pe.add_argument("--note",)

    parser.set_defaults(cmd='history')
    args = parser.parse_args(sys.argv[1:] if len(sys.argv) > 1 else [])

    if args.cmd == "log":
        s = log_session(args)
        print(f"\n✅ 記錄成功！\n")
        print(_print_session(s))

    elif args.cmd == "history":
        print(view_history(args))

    elif args.cmd == "delete":
        print(delete_session(args.id))

    elif args.cmd == "edit":
        print(edit_session(args.id, args.pages, args.minutes, args.note))

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
