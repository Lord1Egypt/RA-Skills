#!/usr/bin/env python3
"""
analytics.py — 閱讀數據分析引擎
Dashboard / 每週報告 / 落後預警 / 預測
"""

import sys
import json
import argparse
from pathlib import Path
from datetime import datetime, date, timedelta
from collections import defaultdict

DATA_DIR = Path.home() / ".bookshelf-plus" / "habit_tracker"

# ═══════════════════════════════════════════════════════════════════════════════
# 數據載入
# ═══════════════════════════════════════════════════════════════════════════════

def _load(file_name: str) -> dict:
    f = DATA_DIR / file_name
    if f.exists():
        return json.loads(f.read_text(encoding="utf-8"))
    return {}


def _sessions() -> list:
    return _load("sessions.json").get("sessions", [])


def _goals() -> dict:
    return _load("goals.json")


def _booklist() -> list:
    return _load("booklist.json").get("books", [])


# ═══════════════════════════════════════════════════════════════════════════════
# 時間工具
# ═══════════════════════════════════════════════════════════════════════════════

def _week_range(dt: date) -> tuple[date, date]:
    monday = dt - timedelta(days=dt.weekday())
    return monday, monday + timedelta(days=6)


def _month_range(year: int, month: int) -> tuple[date, date]:
    first = date(year, month, 1)
    if month == 12:
        last = date(year + 1, 1, 1) - timedelta(days=1)
    else:
        last = date(year, month + 1, 1) - timedelta(days=1)
    return first, last


# ═══════════════════════════════════════════════════════════════════════════════
# 核心計算
# ═══════════════════════════════════════════════════════════════════════════════

def calc_stats(sessions: list, start: date, end: date) -> dict:
    """計算指定時間範圍的閱讀統計"""
    filtered = [
        s for s in sessions
        if start.isoformat() <= s.get("date", "") <= end.isoformat()
    ]

    total_pages  = sum(s.get("pages_read", 0) for s in filtered)
    total_mins   = sum(s.get("duration_minutes", 0) for s in filtered)
    unique_books = len(set(s.get("book", "") for s in filtered))
    finished_books = len(set(s.get("book", "") for s in filtered if s.get("finished")))
    avg_speed    = total_pages / (total_mins / 60) if total_mins > 0 else 0

    # 每日分組
    by_date: dict[str, int] = defaultdict(int)
    for s in filtered:
        by_date[s["date"]] += s.get("pages_read", 0)

    # 讀最多的一天
    best_day = max(by_date.items(), key=lambda x: x[1]) if by_date else ("—", 0)

    return {
        "sessions":     len(filtered),
        "pages":        total_pages,
        "minutes":      total_mins,
        "hours":        total_mins / 60,
        "books":        unique_books,
        "finished":     finished_books,
        "avg_speed":    avg_speed,
        "days_active":  len(by_date),
        "best_day":     best_day[0],
        "best_pages":   best_day[1],
        "by_date":      dict(by_date),
    }


def pace_analysis(goal: dict, stats: dict, days_total: int,
                   days_passed: int) -> dict:
    """計算進度/落後分析"""
    def safe(key: str) -> float:
        return float(goal.get(key, 0) or 0)

    results = {}

    for key, label in [("books","書籍"), ("pages","頁數"), ("hours","時長")]:
        target = safe(key)
        if target <= 0:
            continue
        if key == "books":
            done = float(stats.get("books", 0))
        elif key == "pages":
            done = float(stats.get("pages", 0))
        else:
            done = stats.get("hours", 0)

        pace     = done / max(days_passed, 1)          # 目前每日速度
        needed   = (target - done) / max(days_total - days_passed, 1)  # 剩餘每日需達成
        pct      = done / target * 100
        behind   = (target / days_total * days_passed) - done  # 落後多少

        # 預測能否完成
        projected = done + needed * (days_total - days_passed)
        on_track  = projected >= target

        results[key] = {
            "target":   target,
            "done":     done,
            "pct":      pct,
            "pace":     pace,
            "needed_daily": needed,
            "behind":   behind,
            "on_track": on_track,
            "label":    label,
        }

    return results


# ═══════════════════════════════════════════════════════════════════════════════
# 文字報告生成
# ═══════════════════════════════════════════════════════════════════════════════

def _bar(value: float, target: float, width: int = 12) -> str:
    """ASCII 進度條"""
    if target <= 0:
        return "░" * width
    filled = min(int(value / target * width), width)
    return "█" * filled + "░" * (width - filled)


def _emoji_pace(pace: float, needed: float) -> str:
    if pace >= needed * 1.2: return "🚀"
    if pace >= needed * 0.9: return "✅"
    if pace >= needed * 0.6: return "⚠️"
    return "🔴"


def dashboard_text() -> str:
    today    = date.today()
    year     = today.year
    month    = today.month

    sessions = _sessions()
    goals    = _goals()

    # 年度 stats
    yr_start, yr_end = date(year, 1, 1), date(year, 12, 31)
    yr_stats  = calc_stats(sessions, yr_start, today)
    yr_goal   = goals.get("yearly", {}).get(str(year), {})

    # 月度 stats
    mo_start, mo_end = _month_range(year, month)
    mo_stats  = calc_stats(sessions, mo_start, today)
    mo_goal   = goals.get("monthly", {}).get(f"{year}-{month:02d}", {})

    # 本週 stats
    wk_start, wk_end = _week_range(today)
    wk_stats   = calc_stats(sessions, wk_start, today)

    days_in_month = (mo_end - mo_start).days + 1
    days_passed_month = today.day
    days_left_month   = max(days_in_month - days_passed_month, 0)

    yr_days_passed = (today - yr_start).days + 1
    yr_days_total  = 365 + (1 if (year % 4 == 0 and year % 100 != 0) or year % 400 == 0 else 0)

    lines = []

    # 標題
    lines.append(f"""
╔══════════════════════════════════════════════════════╗
║     📊  閱讀習慣追蹤 Dashboard  —  {today.isoformat()}     ║
╚══════════════════════════════════════════════════════╝
""".strip())

    # 本週摘要
    lines.append(f"  📅 本週（{wk_start.isoformat()} ~ {wk_end.isoformat()}）")
    lines.append(f"     📄 {wk_stats['pages']} 頁  "
                 f"  ⏱️  {wk_stats['hours']:.1f}h  "
                 f"  📚 {wk_stats['books']} 本  "
                 f"  📆 {wk_stats['days_active']} 天")
    if wk_stats['best_day'] != "—":
        lines.append(f"     🏆 本週最佳：{wk_stats['best_day']} ({wk_stats['best_pages']} 頁)")
    lines.append("")

    # 月度目標
    lines.append(f"  ── {year}-{month:02d} 月 ─────────────────────────────")
    if mo_goal:
        mo_pace = pace_analysis(mo_goal, mo_stats, days_in_month, days_passed_month)
        lines.append(f"     進度：{_bar(mo_stats['pages'], mo_goal.get('pages', 1), 16)}  "
                     f"{mo_stats['pages']}/{mo_goal.get('pages', 0)} 頁")
        lines.append(f"     📚 {mo_stats['books']} 本  ⏱️  {mo_stats['hours']:.1f}h")
        for k, v in mo_pace.items():
            emoji = _emoji_pace(v["pace"], v["needed_daily"])
            status = "✅ 達標中" if v["on_track"] else (f"🔴 落後 {v['behind']:.0f}" if v['behind'] > 0 else "🚀 超前")
            lines.append(f"     {emoji} {v['label']}：{v['done']:.0f}/{v['target']:.0f} "
                         f"({v['pct']:.0f}%)  {status}")
    else:
        lines.append(f"     ⚠️  月度目標未設定（使用 goal set --type monthly 設定）")
        lines.append(f"     實際：📄 {mo_stats['pages']} 頁  📚 {mo_stats['books']} 本  ⏱️  {mo_stats['hours']:.1f}h")
    lines.append("")

    # 年度目標
    lines.append(f"  ── {year} 年度 ─────────────────────────────────────")
    if yr_goal:
        yr_pace = pace_analysis(yr_goal, yr_stats, yr_days_total, yr_days_passed)
        lines.append(f"     進度：{_bar(yr_stats['pages'], yr_goal.get('pages', 1), 16)}  "
                     f"{yr_stats['pages']}/{yr_goal.get('pages', 0)} 頁")
        lines.append(f"     📚 {yr_stats['books']} 本  ⏱️  {yr_stats['hours']:.1f}h  "
                     f"  剩 {365 - yr_days_passed + 1} 天")
        for k, v in yr_pace.items():
            emoji = _emoji_pace(v["pace"], v["needed_daily"])
            status = "✅ 達標中" if v["on_track"] else (f"🔴 落後 {v['behind']:.0f}" if v['behind'] > 0 else "🚀 超前")
            lines.append(f"     {emoji} {v['label']}：{v['done']:.0f}/{v['target']:.0f} "
                         f"({v['pct']:.0f}%)  {status}")
    else:
        lines.append(f"     ⚠️  年度目標未設定（使用 goal set --type yearly 設定）")
        lines.append(f"     實際：📄 {yr_stats['pages']:,} 頁  📚 {yr_stats['books']} 本  "
                     f"  ⏱️  {yr_stats['hours']:.1f}h")

    # 書單狀態
    books = _booklist()
    by_status = defaultdict(int)
    for b in books:
        by_status[b.get("status", "unknown")] += 1

    lines.append("")
    lines.append("  ── 書單狀態 ─────────────────────────────────────────")
    status_labels = {
        "reading":   "在讀",
        "finished":  "已讀",
        "to-read":   "想讀",
        "paused":    "暫停",
        "abandoned": "放棄",
    }
    for status, label in status_labels.items():
        count = by_status.get(status, 0)
        icon = "📖" if status == "reading" else "✅" if status == "finished" else "📋"
        lines.append(f"     {icon} {label}：{count} 本")

    return "\n".join(lines)


def weekly_report_text() -> str:
    today    = date.today()
    wk_start, wk_end = _week_range(today)
    sessions = _sessions()
    goals    = _goals()

    stats    = calc_stats(sessions, wk_start, today)
    month    = today.month
    mo_goal  = goals.get("monthly", {}).get(f"{today.year}-{month:02d}", {})

    lines = [f"""
📊 閱讀週報 — {wk_start.isoformat()} 至 {wk_end.isoformat()}
{'='*50}
""".strip()]

    lines.append(f"  📄 總閱讀頁數：{stats['pages']} 頁")
    lines.append(f"  ⏱️  總閱讀時長：{stats['hours']:.1f} 小時")
    lines.append(f"  📚 閱讀書籍數：{stats['books']} 本")
    lines.append(f"  📆 活躍天數：{stats['days_active']} 天")
    if stats['avg_speed'] > 0:
        lines.append(f"  🚀 平均速度：{stats['avg_speed']:.0f} 頁/小時")
    if stats['best_day'] != "—":
        lines.append(f"  🏆 本週最佳日：{stats['best_day']}（{stats['best_pages']} 頁）")

    # 每日柱狀圖
    lines.append("")
    lines.append("  📅 每日閱讀柱狀圖（頁）")
    by_date = sorted(stats["by_date"].items())
    max_pages = max((v for _, v in by_date), default=1)
    for d, pages in by_date:
        bar_len = int(pages / max_pages * 20) if max_pages > 0 else 0
        day_name = date.fromisoformat(d).strftime("%a")
        lines.append(f"     {day_name} {d}  {'█' * bar_len} {pages}")

    # 月度進度
    if mo_goal:
        mo_start, _ = _month_range(today.year, today.month)
        mo_stats = calc_stats(sessions, mo_start, today)
        lines.append("")
        lines.append(f"  📈 {today.year}-{today.month:02d} 月進度")
        for key, label in [("pages","📄 頁數"), ("books","📚 書籍")]:
            target = float(mo_goal.get(key, 0) or 0)
            if target <= 0: continue
            done = float(mo_stats.get(key, 0))
            pct  = done / target * 100
            days_in = (date(today.year, today.month, 1) - date(today.year, today.month + 1, 1)).days if today.month < 12 else 31
            expected = target / days_in * today.day
            diff = done - expected
            sign = "+" if diff >= 0 else ""
            status = f"{sign}{diff:.0f}" if diff != 0 else "=0"
            lines.append(f"     {label}：{done:.0f}/{target:.0f} ({pct:.0f}%)  "
                         f"預期：{expected:.0f}  差：{status}")

    return "\n".join(lines)


def alert_text() -> str:
    """落後預警報告"""
    today    = date.today()
    year     = today.year
    month    = today.month
    sessions = _sessions()
    goals    = _goals()

    alerts: list[str] = []
    warnings: list[str] = []

    # 月度預警
    mo_start, mo_end = _month_range(year, month)
    mo_stats = calc_stats(sessions, mo_start, today)
    mo_goal  = goals.get("monthly", {}).get(f"{year}-{month:02d}", {})
    days_in  = (mo_end - mo_start).days + 1
    days_p   = today.day

    if mo_goal:
        mo_pace = pace_analysis(mo_goal, mo_stats, days_in, days_p)
        for k, v in mo_pace.items():
            if v["behind"] > 0 and v["behind"] > v["target"] * 0.2:
                alerts.append(
                    f"🔴 本月「{v['label']}」落後 {v['behind']:.0f}，"
                    f"落後幅度 >20%，建議加把勁！"
                )
            elif v["behind"] > 0:
                warnings.append(
                    f"⚠️  本月「{v['label']}」輕微落後 {v['behind']:.0f}，"
                    f"每天需讀 {v['needed_daily']:.1f} 頁才能達標"
                )
            elif v["on_track"]:
                pass  # 良好狀態不預警

    # 零活動預警
    this_week_sessions = [
        s for s in sessions
        if _week_range(today)[0].isoformat() <= s.get("date","") <= _week_range(today)[1].isoformat()
    ]
    if not this_week_sessions:
        warnings.append("⚠️  本週尚無閱讀記錄！快開始讀書吧 📖")

    if not alerts and not warnings:
        return "✅ 目前進度良好，繼續保持！"

    if alerts:
        return "🚨 **閱讀落後預警**\n\n" + "\n\n".join(alerts) + \
               ("\n\n" + "\n".join(warnings) if warnings else "")
    return "⚠️  **閱讀提醒**\n\n" + "\n".join(warnings)


# ═══════════════════════════════════════════════════════════════════════════════
# CLI
# ═══════════════════════════════════════════════════════════════════════════════

def main():
    parser = argparse.ArgumentParser(description="閱讀數據分析")
    sub = parser.add_subparsers(dest="cmd")

    sub.add_parser("dashboard", help="進度儀表板")
    sub.add_parser("weekly",    help="本週報告")
    sub.add_parser("alert",      help="落後預警")
    sub.add_parser("monthly",   help="本月報告")

    p_stats = sub.add_parser("stats", help="指定時間統計")
    p_stats.add_argument("--start", help="起始日期 YYYY-MM-DD")
    p_stats.add_argument("--end",   help="結束日期 YYYY-MM-DD")

    parser.set_defaults(cmd='history')
    args = parser.parse_args(sys.argv[1:] if len(sys.argv) > 2 else [])

    if args.cmd == "dashboard":
        print(dashboard_text())

    elif args.cmd == "weekly":
        print(weekly_report_text())

    elif args.cmd == "alert":
        print(alert_text())

    elif args.cmd == "monthly":
        today = date.today()
        mo_start, mo_end = _month_range(today.year, today.month)
        sessions = _sessions()
        stats = calc_stats(sessions, mo_start, today)
        goals = _goals()
        mo_goal = goals.get("monthly", {}).get(f"{today.year}-{today.month:02d}", {})
        days_in = (mo_end - mo_start).days + 1
        print(f"\n📊 {today.year}-{today.month:02d} 月報告")
        print("=" * 40)
        print(f"  📄 {stats['pages']} 頁  ⏱️  {stats['hours']:.1f}h  "
              f"  📚 {stats['books']} 本  📆 {stats['days_active']} 天")
        if mo_goal:
            for key, label in [("pages","📄"), ("books","📚")]:
                target = float(mo_goal.get(key, 0) or 0)
                if target <= 0: continue
                pct = float(stats.get(key, 0)) / target * 100
                print(f"  {label} 進度：{_bar(stats.get(key,0), target, 16)} {pct:.0f}%")

    elif args.cmd == "stats":
        if args.start and args.end:
            s = calc_stats(sessions, date.fromisoformat(args.start),
                           date.fromisoformat(args.end))
        else:
            today = date.today()
            s = calc_stats(_sessions(),
                           today - timedelta(days=30), today)
        print(f"  📄 {s['pages']} 頁  ⏱️  {s['hours']:.1f}h  "
              f"  📚 {s['books']} 本  📆 {s['days_active']} 天")

    else:
        print(dashboard_text())


if __name__ == "__main__":
    main()
