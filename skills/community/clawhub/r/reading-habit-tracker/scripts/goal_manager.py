#!/usr/bin/env python3
"""
goal_manager.py — 閱讀目標管理
支援：年度/月度/單書目標，設定/查看/刪除
"""

import sys
import json
import argparse
from pathlib import Path
from datetime import datetime, date

DATA_DIR = Path.home() / ".bookshelf-plus" / "habit_tracker"
GOALS_FILE = DATA_DIR / "goals.json"


def _load() -> dict:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    if GOALS_FILE.exists():
        return json.loads(GOALS_FILE.read_text(encoding="utf-8"))
    return {"yearly": {}, "monthly": {}, "per_book": {}}


def _save(data: dict):
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    GOALS_FILE.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def _fmt_delta(days: int) -> str:
    if days == 0:   return "今天"
    if days == 1:   return "明天"
    if days == -1:  return "昨天"
    if days > 0:    return f"{days} 天落後"
    return f"{-days} 天超前"


def _pct(done: float, target: float) -> float:
    if target <= 0: return 0.0
    return min(done / target * 100, 999.9)


def set_goal(args) -> dict:
    data = _load()
    today = date.today()
    year  = today.year
    month = today.month

    if args.type == "yearly":
        data["yearly"][str(year)] = {
            "books":    args.books,
            "pages":    args.pages,
            "hours":    args.hours,
            "created":  today.isoformat(),
        }

    elif args.type == "monthly":
        key = f"{year}-{month:02d}"
        data["monthly"][key] = {
            "books":  args.books,
            "pages":  args.pages,
            "hours":  args.hours,
            "created": today.isoformat(),
        }

    elif args.type == "per-book":
        title = args.title
        data["per_book"][title] = {
            "target_pages":   args.pages,
            "target_hours":   args.hours or 0,
            "deadline":       args.deadline or "",
            "category":       args.category or "",
            "created":        today.isoformat(),
        }

    _save(data)
    return data


def view_goals(sessions_file: Path = None) -> str:
    data    = _load()
    today   = date.today()
    year    = today.year
    month   = today.month

    sessions_data = {}
    if sessions_file and sessions_file.exists():
        sessions_data = json.loads(sessions_file.read_text(encoding="utf-8"))

    # 計算已完成的量
    year_sessions = [s for s in sessions_data.get("sessions", [])
                    if s.get("date", "").startswith(str(year))]
    month_sessions = [s for s in sessions_data.get("sessions", [])
                      if s.get("date", "").startswith(f"{year}-{month:02d}")]

    done_books_year  = len(set(s.get("book") for s in year_sessions
                                if s.get("finished")))
    done_pages_year  = sum(s.get("pages_read", 0) for s in year_sessions)
    done_hours_year  = sum(s.get("duration_minutes", 0) for s in year_sessions) / 60
    done_books_month = len(set(s.get("book") for s in month_sessions
                                if s.get("finished")))
    done_pages_month = sum(s.get("pages_read", 0) for s in month_sessions)
    done_hours_month = sum(s.get("duration_minutes", 0) for s in month_sessions) / 60

    lines = ["\n📌 閱讀目標追蹤"]
    lines.append(f"   查詢日期：{today.isoformat()}\n")

    # ── 年度目標 ─────────────────────────────────────────────────────────────
    y_goal = data.get("yearly", {}).get(str(year), {})
    if y_goal:
        b_pct = _pct(done_books_year, y_goal.get("books", 1))
        p_pct = _pct(done_pages_year, y_goal.get("pages", 1))
        h_pct = _pct(done_hours_year, y_goal.get("hours", 1))
        days_left = (date(year, 12, 31) - today).days
        lines += [
            f"  【{year} 年度目標】",
            f"  📚 書籍：{done_books_year} / {y_goal.get('books', 0)} 本 ({b_pct:.0f}%)",
            f"  📄 頁數：{done_pages_year:,} / {y_goal.get('pages', 0):,} 頁 ({p_pct:.0f}%)",
            f"  ⏱️  時長：{done_hours_year:.1f} / {y_goal.get('hours', 0)}h ({h_pct:.0f}%)",
            f"  📅 剩餘：{days_left} 天",
        ]
    else:
        lines.append(f"  【{year} 年度目標】尚未設定（使用 set 指令設定）")

    lines.append("")

    # ── 月度目標 ─────────────────────────────────────────────────────────────
    m_key  = f"{year}-{month:02d}"
    m_goal = data.get("monthly", {}).get(m_key, {})
    if m_goal:
        days_in_month = (date(year, month, 1) - date(year, month + 1, 1)).days if month < 12 \
                        else (date(year, 12, 31) - date(year, month, 1)).days + 1
        days_passed   = today.day
        b_pct = _pct(done_books_month, m_goal.get("books", 1))
        p_pct = _pct(done_pages_month, m_goal.get("pages", 1))
        lines += [
            f"  【{year}-{month:02d} 月度目標】",
            f"  📚 書籍：{done_books_month} / {m_goal.get('books', 0)} 本 ({b_pct:.0f}%)",
            f"  📄 頁數：{done_pages_month:,} / {m_goal.get('pages', 0):,} 頁 ({p_pct:.0f}%)",
            f"  📅 進度：{days_passed}/{days_in_month} 天（{days_passed/days_in_month*100:.0f}%）",
        ]
    else:
        lines.append(f"  【{year}-{month:02d} 月度目標】尚未設定")

    lines.append("")

    # ── 單書目標 ─────────────────────────────────────────────────────────────
    pb_goals = data.get("per_book", {})
    if pb_goals:
        lines.append("  【單書目標】")
        for title, g in list(pb_goals.items())[:5]:
            book_sessions = [s for s in sessions_data.get("sessions", [])
                            if s.get("book") == title]
            done_pages = sum(s.get("pages_read", 0) for s in book_sessions)
            target     = g.get("target_pages", 0)
            pct = _pct(done_pages, target)
            deadline = g.get("deadline", "未設期限")
            lines.append(f"  《{title[:20]}》")
            lines.append(f"    頁數：{done_pages:,} / {target:,} ({pct:.0f}%)  "
                         f"截止：{deadline}")
        if len(pb_goals) > 5:
            lines.append(f"  ... 還有 {len(pb_goals)-5} 本")
    else:
        lines.append("  【單書目標】尚無設定")

    return "\n".join(lines)


def delete_goal(args) -> str:
    data = _load()
    if args.type == "yearly":
        data.get("yearly", {}).pop(str(date.today().year), None)
    elif args.type == "monthly":
        today = date.today()
        data.get("monthly", {}).pop(f"{today.year}-{today.month:02d}", None)
    elif args.type == "per-book":
        data.get("per_book", {}).pop(args.title, None)
    _save(data)
    return "✅ 目標已刪除"


# ── CLI ───────────────────────────────────────────────────────────────────────

def main():
    sessions_file = DATA_DIR / "sessions.json"
    parser = argparse.ArgumentParser(description="閱讀目標管理")
    sub = parser.add_subparsers(dest="cmd")

    # set
    p_set = sub.add_parser("set", help="設定目標")
    p_set.add_argument("--type",   choices=["yearly", "monthly", "per-book"],
                       required=True)
    p_set.add_argument("--books",  type=int, default=0)
    p_set.add_argument("--pages",  type=int, default=0)
    p_set.add_argument("--hours",  type=float, default=0)
    p_set.add_argument("--title",  help="單書目標時必填")
    p_set.add_argument("--deadline", help="截止日期 YYYY-MM-DD")
    p_set.add_argument("--category", default="")

    # view
    sub.add_parser("view", help="查看所有目標與進度")

    # delete
    p_del = sub.add_parser("delete", help="刪除目標")
    p_del.add_argument("--type", choices=["yearly", "monthly", "per-book"], required=True)
    p_del.add_argument("--title", help="單書目標時必填")

    parser.set_defaults(cmd='view')
    args = parser.parse_args(sys.argv[1:] if len(sys.argv) > 2 else [])

    if args.cmd == "set":
        set_goal(args)
        print("✅ 目標已設定")
        print(view_goals(sessions_file))
    elif args.cmd == "view":
        print(view_goals(sessions_file))
    elif args.cmd == "delete":
        print(delete_goal(args))
    else:
        print(view_goals(sessions_file))


if __name__ == "__main__":
    main()
