"""
events.py — Step 7: Fetch macro events and annotate known calendar milestones.

API note: news_economic_baidu() typically lags 4–8 weeks behind today.
If the API window returns nothing, we fall back to a hardcoded China macro
calendar so the output is never silently empty.

Usage:
    from events import fetch_events
    ev_lines = fetch_events()
    for line in ev_lines:
        print(line)
"""

from __future__ import annotations

from datetime import date, timedelta
import akshare as ak
import pandas as pd


# ── Hardcoded annual China macro calendar (month, day, label) ────────────────
_CHINA_MACRO_CALENDAR = [
    # PMI: first business day of each month — approximated as 1st
    (1,  1,  "PMI releases (Jan)"),
    (2,  1,  "PMI releases (Feb)"),
    (3,  1,  "PMI releases (Mar)"),
    (3,  5,  "NPC/CPPCC Two Sessions open (approx)"),
    (3, 15,  "NPC/CPPCC Two Sessions close (approx)"),
    (3, 31,  "Annual report disclosure deadline"),
    (4,  1,  "PMI releases (Apr)"),
    (4, 30,  "Q1 earnings window closes"),
    (5,  1,  "PMI releases (May)"),
    (6,  1,  "PMI releases (Jun)"),
    (7,  1,  "PMI releases (Jul)"),
    (8,  1,  "PMI releases (Aug)"),
    (8, 31,  "H1 / Q2 earnings window closes"),
    (9,  1,  "PMI releases (Sep)"),
    (10, 1,  "PMI releases (Oct)"),
    (10,31,  "Q3 earnings window closes"),
    (11, 1,  "PMI releases (Nov)"),
    (12, 1,  "PMI releases (Dec)"),
    (12,31,  "Year-end / annual settlement"),
]

# Earnings season windows keyed by (start_month, end_month)
_EARNINGS_WINDOWS = [
    (4,  4,  "Q1 earnings season (Apr)"),
    (8,  8,  "H1/Q2 earnings season (Aug)"),
    (10, 10, "Q3 earnings season (Oct)"),
    (1,  3,  "Q4/Annual earnings season (Jan–Mar)"),
]


def _earnings_flag(today: date) -> str | None:
    """Return a label if today falls inside an earnings window."""
    m = today.month
    for start, end, label in _EARNINGS_WINDOWS:
        if start <= m <= end:
            return label
    return None


def fetch_events(
    lookback_days: int = 30,
    lookahead_days: int = 14,
    min_importance: int = 2,
) -> list[str]:
    """
    Return a list of annotated event strings covering ±window around today.

    First tries the live API; falls back to hardcoded calendar if empty.
    """
    today = date.today()
    lo    = today - timedelta(days=lookback_days)
    hi    = today + timedelta(days=lookahead_days)
    lines: list[str] = []

    # ── ① Try live API ───────────────────────────────────────────────────────
    api_ok = False
    try:
        ev_df = ak.news_economic_baidu()
        # Date column contains datetime.date objects
        window = ev_df[ev_df["日期"].apply(lambda d: lo <= d <= hi)]
        if min_importance and "重要性" in window.columns:
            window = window[window["重要性"] >= min_importance]
        if not window.empty:
            api_ok = True
            for _, row in window.iterrows():
                lines.append(
                    f"- {row['日期']} [{row.get('地区','')}] {row['事件']}"
                    + (f"  (重要性={row['重要性']})" if "重要性" in row else "")
                )
    except Exception as e:
        print(f"[events] news_economic_baidu failed: {e}")

    if not api_ok:
        lines.append(
            "- *API data unavailable or stale (news_economic_baidu lags ~4–8 weeks).*"
            "  Key dates annotated from hardcoded calendar:"
        )

    # ── ② Always annotate hardcoded China macro calendar ────────────────────
    year = today.year
    for month, day, label in _CHINA_MACRO_CALENDAR:
        for yr in (year - 1, year, year + 1):
            try:
                d = date(yr, month, day)
            except ValueError:
                continue
            if lo <= d <= hi:
                lines.append(f"- {d}  📅 {label}")

    # ── ③ Earnings season flag ───────────────────────────────────────────────
    flag = _earnings_flag(today)
    if flag:
        lines.append(f"- ⚠️  Currently in **{flag}** — watch for earnings surprises")

    if not lines:
        lines.append("- No notable events in the ±30/14 day window.")

    return lines


# ── Quick smoke-test ─────────────────────────────────────────────────────────
if __name__ == "__main__":
    for line in fetch_events():
        print(line)
