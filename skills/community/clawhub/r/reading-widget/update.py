#!/usr/bin/env python3
"""Fetch WeRead stats and regenerate widget.html."""
import os, json, time, datetime, pathlib, urllib.request, urllib.error, html as htmllib

API = "https://i.weread.qq.com/api/agent/gateway"
SKILL_VERSION = "1.1.0"
ROOT = pathlib.Path(__file__).parent
CONFIG = json.loads((ROOT / "config.json").read_text())

def _load_key():
    k = os.environ.get("WEREAD_API_KEY") or CONFIG.get("api_key")
    if k: return k
    # fallback: read settings.json env.WEREAD_API_KEY (~/.claw, then ~/.claude)
    for base in (".claw", ".claude"):
        try:
            settings = json.loads((pathlib.Path.home() / base / "settings.json").read_text())
            v = settings.get("env", {}).get("WEREAD_API_KEY")
            if v: return v
        except Exception:
            pass
    return None

KEY = _load_key()

# Crude terms to keep out of the rotating desktop quote.
QUOTE_BLOCKLIST = ("鸡巴", "屌", "傻逼", "煞笔", "草泥马", "卧槽", "妈的", "婊", "贱人", "fuck", "shit")


def call(api_name, **params):
    body = {"api_name": api_name, "skill_version": SKILL_VERSION, **params}
    req = urllib.request.Request(
        API,
        data=json.dumps(body).encode(),
        headers={"Authorization": f"Bearer {KEY}", "Content-Type": "application/json"},
    )
    with urllib.request.urlopen(req, timeout=20) as resp:
        return json.loads(resp.read())


def fmt_hm(secs):
    secs = int(secs or 0)
    h, m = divmod(secs // 60, 60)
    if h and m: return f"{h}h {m}m"
    if h: return f"{h}h"
    return f"{m}m"


def relative_time(ts):
    if not ts: return "—"
    delta = int(time.time() - ts)
    if delta < 60: return "刚刚"
    if delta < 3600: return f"{delta // 60} 分钟前"
    if delta < 86400: return f"{delta // 3600} 小时前"
    return f"{delta // 86400} 天前"


def fetch_week(date_in_week):
    base_ts = int(datetime.datetime.combine(date_in_week, datetime.time(12)).timestamp())
    return call("/readdata/detail", mode="weekly", baseTime=base_ts)


def compute_streak_and_today(threshold=60, max_weeks=10):
    """Walk back day-by-day; count consecutive days with reading >= threshold seconds.
    Today does not break the streak if 0. Returns (streak, today_minutes)."""
    today = datetime.date.today()
    today_min = 0
    streak = 0
    today_counted = False
    today_seen = False

    for w in range(max_weeks):
        week_date = today - datetime.timedelta(weeks=w)
        data = fetch_week(week_date)
        rt = data.get("readTimes", {})
        # sort day-buckets descending by timestamp
        items = sorted(((int(k), int(v)) for k, v in rt.items()), reverse=True)
        for d_ts, secs in items:
            d_date = datetime.date.fromtimestamp(d_ts)
            if d_date > today:
                continue
            if d_date == today and not today_seen:
                today_seen = True
                today_min = secs // 60
                if secs >= threshold:
                    streak += 1
                    today_counted = True
                # today with 0 doesn't break; just move on
                continue
            if d_date == today:
                continue
            # past day
            if secs >= threshold:
                streak += 1
            else:
                return streak, today_min
    return streak, today_min


def week_total_seconds(date_in_week):
    """Total reading seconds for the week containing date_in_week."""
    data = fetch_week(date_in_week)
    total = data.get("totalReadTime")
    if not total:
        total = sum(int(v) for v in data.get("readTimes", {}).values())
    return int(total or 0)


def find_current_book():
    shelf = call("/shelf/sync")
    books = shelf.get("books", [])
    candidates = [b for b in books if not b.get("finishReading")]
    if not candidates:
        return None
    candidates.sort(key=lambda b: b.get("readUpdateTime", 0), reverse=True)
    return candidates[0]


def parse_stat_count(annual, name):
    for s in annual.get("readStat", []):
        if s.get("stat") == name:
            return int("".join(c for c in s.get("counts", "") if c.isdigit()) or 0)
    return 0


def main():
    if not KEY:
        raise SystemExit("WEREAD_API_KEY not set (env or config.json)")

    monthly = call("/readdata/detail", mode="monthly")
    annual = call("/readdata/detail", mode="annually")

    today = datetime.date.today()
    first_of_month = today.replace(day=1)
    last_month_anchor = first_of_month - datetime.timedelta(days=1)
    lm_ts = int(datetime.datetime.combine(last_month_anchor.replace(day=1), datetime.time(12)).timestamp())
    last_monthly = call("/readdata/detail", mode="monthly", baseTime=lm_ts)

    streak, today_min = compute_streak_and_today()

    # this-week total + daily average (for the 今日→本周 drill-down)
    week_total_sec = week_total_seconds(today)
    days_elapsed = today.weekday() + 1
    week_hm = fmt_hm(week_total_sec)
    week_day_avg = fmt_hm(week_total_sec // days_elapsed if days_elapsed else 0)

    month_total_sec = monthly.get("totalReadTime", 0)
    month_hours = month_total_sec // 3600
    day_avg = fmt_hm(monthly.get("dayAverageReadTime", 0))
    last_month_hours = last_monthly.get("totalReadTime", 0) // 3600

    year_finished = parse_stat_count(annual, "读完")
    year_notes = parse_stat_count(annual, "笔记")
    year_total_sec = annual.get("totalReadTime", 0)
    year_total_hours = year_total_sec // 3600
    day_of_year = today.timetuple().tm_yday
    year_day_avg = fmt_hm(year_total_sec // day_of_year if day_of_year else 0)

    book = find_current_book()
    quote = ""
    if book:
        try:
            prog_resp = call("/book/getprogress", bookId=book["bookId"])
            progress = prog_resp.get("book", {}).get("progress", 0)
        except Exception:
            progress = 0
        book_title = book.get("title", "—")
        book_author = book.get("author") or "—"
        book_cover = book.get("cover", "")
        last_read = book.get("readUpdateTime", 0)
        # quote: top hot-highlight, prefer short & literary; rotate by day
        try:
            bm = call("/book/bestbookmarks", bookId=book["bookId"])
            items = bm.get("items", [])
            candidates = [
                t for t in (i.get("markText", "").strip() for i in items)
                if 15 <= len(t) <= 70 and not any(w in t.lower() for w in QUOTE_BLOCKLIST)
            ]
            if candidates:
                idx = today.toordinal() % len(candidates)
                quote = candidates[idx]
        except Exception:
            pass
    else:
        progress = 0
        book_title = "暂无在读"
        book_author = ""
        book_cover = ""
        last_read = 0

    goal_hours = int(CONFIG.get("goal_hours", 50))
    refresh_seconds = int(CONFIG.get("refresh_seconds", 300))
    goal_pct = min(100, round(month_hours / goal_hours * 100)) if goal_hours else 0

    weekday = ["一", "二", "三", "四", "五", "六", "日"][today.weekday()]
    date_str = f"{today.year}.{today.month:02d}.{today.day:02d} 周{weekday}"

    repl = {
        "DATE": date_str,
        "STREAK": str(streak),
        "TODAY_MIN": str(today_min),
        "DAY_AVG": day_avg,
        "MONTH_HOURS": str(month_hours),
        "LAST_MONTH_HOURS": str(last_month_hours),
        "GOAL_HOURS": str(goal_hours),
        "GOAL_PCT": str(goal_pct),
        "WEEK_HM": week_hm,
        "WEEK_DAY_AVG": week_day_avg,
        "BOOK_TITLE": htmllib.escape(book_title),
        "BOOK_AUTHOR": htmllib.escape(book_author),
        "BOOK_COVER": htmllib.escape(book_cover),
        "BOOK_PROGRESS": str(progress),
        "YEAR_FINISHED": str(year_finished),
        "YEAR_HOURS": str(year_total_hours),
        "YEAR_DAY_AVG": year_day_avg,
        "YEAR_NOTES": str(year_notes),
        "LAST_READ": htmllib.escape(relative_time(last_read)),
        "UPDATED_AT": datetime.datetime.now().strftime("%H:%M"),
        "REFRESH_SECONDS": str(refresh_seconds),
        "QUOTE": htmllib.escape(quote),
    }

    tpl = (ROOT / "template.html").read_text()
    for k, v in repl.items():
        tpl = tpl.replace("{{" + k + "}}", v)
    (ROOT / "widget.html").write_text(tpl)

    # Also write a fragment (style + body content) for Übersicht inline rendering.
    import re
    style_match = re.search(r"<style>(.*?)</style>", tpl, re.S)
    body_match = re.search(r"<body>(.*?)</body>", tpl, re.S)
    if style_match and body_match:
        fragment = f"<style>{style_match.group(1)}</style>\n{body_match.group(1)}"
        (ROOT / "widget-fragment.html").write_text(fragment)

    print(f"[{datetime.datetime.now():%H:%M:%S}] widget.html updated · streak={streak} today={today_min}m month={month_hours}h book={book_title!r}")


if __name__ == "__main__":
    main()
