#!/usr/bin/env python3
"""
visualizer.py — 終端視覺化引擎
支援：ASCII 熱力圖、柱狀圖、環形圖、 streaks 視覺化
"""

import sys
import json
import argparse
from pathlib import Path
from datetime import date, timedelta
from collections import defaultdict

DATA_DIR = Path.home() / ".bookshelf-plus" / "habit_tracker"

# ═══════════════════════════════════════════════════════════════════════════════
# 數據載入
# ═══════════════════════════════════════════════════════════════════════════════

def _sessions():
    f = DATA_DIR / "sessions.json"
    if f.exists():
        return json.loads(f.read_text(encoding="utf-8")).get("sessions", [])
    return []


# ═══════════════════════════════════════════════════════════════════════════════
# 熱力圖
# ═══════════════════════════════════════════════════════════════════════════════

def _color(pages: int) -> str:
    """終端 ANSI 顏色"""
    if pages == 0:   return "\033[90m"   # 灰色
    if pages < 10:   return "\033[38;5;255m"  # 淡綠
    if pages < 30:   return "\033[32m"   # 綠
    if pages < 60:   return "\033[38;5;28m"  # 深綠
    return "\033[38;5;22m"             # 墨綠


RESET = "\033[0m"


def heatmap(days: int = 365) -> str:
    """ASCII 年度熱力圖（GitHub 風格）"""
    today = date.today()
    start = today - timedelta(days=days - 1)
    # 對齊週一
    start -= timedelta(days=start.weekday())

    sessions = _sessions()
    by_date: dict[str, int] = defaultdict(int)
    for s in sessions:
        by_date[s.get("date", "")] += s.get("pages_read", 0)

    lines = ["\n  🔥 年度閱讀熱力圖（過去 " + str(days) + " 天）"]
    lines.append("     " + " ".join(
        ["Mon", "", "Wed", "", "Fri", "", "Sun"][i]
        for i in range(7)
    ))

    week_cells: list[str] = []
    cur = start
    row_days: list[str] = []
    row_labels: list[str] = []

    for i in range(days + 7):
        if cur > today:
            break
        pages = by_date.get(cur.isoformat(), 0)
        color = _color(pages)
        # 隱藏零值：空格（0）或 block（>0）
        if pages == 0:
            cell = color + "░" + RESET
        else:
            cell = color + "█" + RESET
        row_days.append(cell)

        if cur.weekday() == 6 or cur == today:  # 週日或今天換行
            # 週標籤
            week_num = (cur - start).days // 7
            label = str(cur.month) if cur.day == 1 or (row_days and cur.day <= 7) else ""
            lines.append(
                f"  {label:>3} " + "".join(row_days)
            )
            row_days = []
        cur += timedelta(days=1)

    # 月份圖例
    lines.append("")
    lines.append("     " + " ".join(
        f"{_color(v)}{'░' if v==0 else '█'}" + RESET
        for v in [0, 5, 15, 35, 65]
    ) + "  0  10  30  60+ 頁/天")

    return "\n".join(lines)


# ═══════════════════════════════════════════════════════════════════════════════
# 柱狀圖
# ═══════════════════════════════════════════════════════════════════════════════

def bar_chart(data: list[tuple[str, float]], title: str = "",
              max_width: int = 30, show_value: bool = True) -> str:
    """終端柱狀圖（ASCII）"""
    if not data:
        return "(無數據)"
    max_val = max(v for _, v in data)
    if max_val == 0: max_val = 1

    lines = []
    if title:
        lines.append(title)

    for label, value in data:
        bar_len = int(value / max_val * max_width)
        bar     = "▓" * bar_len
        val_str = f"{value:.0f}" if value == int(value) else f"{value:.1f}"
        lines.append(f"  {label:<15} │{bar:<{max_width}}│ {val_str}")

    return "\n".join(lines)


# ═══════════════════════════════════════════════════════════════════════════════
# 環形圖（ASCII 近似）
# ═══════════════════════════════════════════════════════════════════════════════

def donut(data: list[tuple[str, float]], title: str = "") -> str:
    """ASCII 環形圖"""
    if not data:
        return "(無數據)"
    total = sum(v for _, v in data)
    if total == 0:
        return "(無數據)"

    chars = ["▏", "▎", "▍", "▌", "▋", "▊", "▉", "█"]
    colors_ansi = [
        "\033[31m", "\033[32m", "\033[34m",
        "\033[33m", "\033[36m", "\033[35m",
        "\033[91m", "\033[92m",
    ]
    R = RESET

    # 簡化：只畫前6個
    segments = data[:6]
    n = len(segments)

    lines = []
    if title:
        lines.append(title)

    legend_lines = []
    for i, (label, value) in enumerate(segments):
        pct = value / total * 100
        color = colors_ansi[i % len(colors_ansi)]
        legend_lines.append(
            f"  {color}██{R} {label:<12} {pct:5.1f}%  ({value:.0f})"
        )

    # 上下半圓（用基本字符湊合）
    half = n // 2
    top    = "  ┌─ " + " ".join(f"{colors_ansi[i]}██{R}" for i in range(half))
    bottom = "  └─ " + " ".join(f"{colors_ansi[i+half]}██{R}" for i in range(n - half))

    lines.append(top)
    for ln in legend_lines:
        lines.append(ln)
    lines.append(bottom)
    lines.append(f"  合計：{total:.0f}")

    return "\n".join(lines)


# ═══════════════════════════════════════════════════════════════════════════════
# Streak 火焰圖
# ═══════════════════════════════════════════════════════════════════════════════

def streak_fire() -> str:
    """終端火焰 streak 可視化"""
    sessions = _sessions()
    today    = date.today()

    # 計算連續天數
    dates = sorted(set(s.get("date", "") for s in sessions), reverse=True)
    if not dates:
        return "  🔥 Streak：尚未開始記錄 📖"

    # 找當前 streak
    current = 0
    expected = today.isoformat()
    for d in dates:
        if d == expected:
            current += 1
            expected = (today - timedelta(days=current)).isoformat()
        else:
            break

    # 最長 streak
    longest = 0
    streak  = 0
    prev    = None
    for d in sorted(dates):
        if prev is None or (date.fromisoformat(d) - date.fromisoformat(prev)).days == 1:
            streak += 1
        else:
            longest = max(longest, streak)
            streak  = 1
        prev = d
    longest = max(longest, streak)

    fire = "🔥" * min(current, 10)
    empty = "⚪" * max(0, 10 - current)

    lines = [
        "",
        "  ┌─────────────────────────────────────┐",
        f"  │  {fire}{empty}  │",
        f"  │  當前連續：{current:>3} 天     最長：{longest:>3} 天  │",
        "  └─────────────────────────────────────┘",
    ]

    # 里程碑
    milestones = [7, 14, 30, 60, 100, 365]
    next_mile = next((m for m in milestones if m > current), None)
    if next_mile:
        lines.append(f"  🎯 下一個里程碑：{next_mile} 天（還差 {next_mile - current} 天）")
    else:
        lines.append("  🎉 恭喜！你已超越所有里程碑！")

    return "\n".join(lines)


# ═══════════════════════════════════════════════════════════════════════════════
# 月度日曆視圖
# ═══════════════════════════════════════════════════════════════════════════════

def calendar_view(year: int = None, month: int = None) -> str:
    """月度日曆視圖"""
    today = date.today()
    year  = year  or today.year
    month = month or today.month

    first = date(year, month, 1)
    if month == 12:
        next_m = date(year + 1, 1, 1)
    else:
        next_m = date(year, month + 1, 1)
    last = next_m - timedelta(days=1)

    sessions = _sessions()
    by_date: dict[str, int] = defaultdict(int)
    for s in sessions:
        by_date[s.get("date", "")] += s.get("pages_read", 0)

    day_names = ["一", "二", "三", "四", "五", "六", "日"]
    lines = [
        "",
        f"  ┌─ {year} 年 {month:02d} 月 ───────────────────────┐",
        "  │  " + "  ".join(f"{d:^4}" for d in day_names) + "  │",
        "  │  " + " " * 0,
    ]

    # 第一天前的空白
    offset = first.weekday()  # 週一=0
    cells = ["    "] * offset

    for day in range(1, last.day + 1):
        d = date(year, month, day)
        pages = by_date.get(d.isoformat(), 0)
        if pages == 0:
            cell = f"{day:>4}"
        elif pages < 10:
            cell = f"{day:>2}·"
        elif pages < 100:
            cell = f"{day:>2}+"
        else:
            cell = f"{day:>2}*"
        cells.append(cell)

        if d.weekday() == 6:  # 週日換行
            row = "".join(cells)
            lines.append("  │  " + row + "  │")
            cells = []

    # 補足最後一行
    if cells:
        cells += ["    "] * (7 - len(cells))
        lines.append("  │  " + "".join(cells) + "  │")

    lines.append("  └──────────────────────────────────────────────┘")
    lines.append("     ·=1-9頁  +=10-99頁  *=100+頁")
    return "\n".join(lines)


# ═══════════════════════════════════════════════════════════════════════════════
# 綜合儀表板
# ═══════════════════════════════════════════════════════════════════════════════

def full_dashboard() -> str:
    sessions = _sessions()
    today    = date.today()
    year     = today.year

    # 月度柱狀圖
    month_data: dict[str, int] = defaultdict(int)
    for s in sessions:
        key = s.get("date", "")[:7]  # "YYYY-MM"
        month_data[key] += s.get("pages_read", 0)

    recent_months = sorted(month_data.items())[-6:]
    bar_viz = bar_chart(
        [(m, v) for m, v in recent_months],
        title="  📅 近月閱讀頁數",
        max_width=25,
    )

    # 書本柱狀圖
    book_data: dict[str, int] = defaultdict(int)
    for s in sessions:
        book_data[s.get("book", "")[:15]] += s.get("pages_read", 0)
    top_books = sorted(book_data.items(), key=lambda x: x[1], reverse=True)[:5]
    book_viz  = bar_chart(
        top_books,
        title="  📚 Top 5 閱讀書籍",
        max_width=20,
    )

    return (
        heatmap(90) +
        "\n" +
        bar_viz +
        "\n" +
        book_viz +
        "\n" +
        streak_fire() +
        "\n" +
        calendar_view()
    )


# ═══════════════════════════════════════════════════════════════════════════════
# CLI
# ═══════════════════════════════════════════════════════════════════════════════

def main():
    parser = argparse.ArgumentParser(description="閱讀視覺化工具")
    sub = parser.add_subparsers(dest="cmd")

    sub.add_parser("heatmap",   help="年度熱力圖")
    sub.add_parser("dashboard", help="完整儀表板")
    sub.add_parser("streak",    help="Streak 火焰圖")
    sub.add_parser("calendar",  help="月度日曆")

    p_bar = sub.add_parser("bar", help="柱狀圖")
    p_bar.add_argument("--data", nargs="+", help="標籤:數值 對，例如：--data 甲:30 乙:45")

    args = parser.parse_args(sys.argv[2:] if len(sys.argv) > 2 else ["dashboard"])

    if args.cmd == "heatmap":
        print(heatmap(365))
    elif args.cmd == "dashboard":
        print(full_dashboard())
    elif args.cmd == "streak":
        print(streak_fire())
    elif args.cmd == "calendar":
        print(calendar_view(args.year, args.month))
    elif args.cmd == "bar" and args.data:
        pairs = []
        for item in args.data:
            if ":" in item:
                label, val = item.rsplit(":", 1)
                try:
                    pairs.append((label, float(val)))
                except ValueError:
                    pass
        if pairs:
            print(bar_chart(pairs, max_width=25))
    else:
        print(full_dashboard())

if __name__ == "__main__":
    main()
