#!/usr/bin/env python3
import argparse
import json
import subprocess
from collections import defaultdict

BASE = "https://data-api.polymarket.com/v1/leaderboard"
PERIODS = ["DAY", "WEEK", "MONTH", "ALL"]


def fetch_board(category: str, period: str, limit: int = 100):
    url = f"{BASE}?category={category}&timePeriod={period}&orderBy=PNL&limit={limit}&offset=0"
    out = subprocess.check_output(
        ["curl", "-sS", "-L", "--retry", "3", "--retry-delay", "1", "--max-time", "20", url],
        text=True,
    )
    rows = json.loads(out)
    idx = {}
    for i, r in enumerate(rows, start=1):
        w = (r.get("proxyWallet") or "").lower()
        if not w:
            continue
        idx[w] = {
            "rank": i,
            "pnl": float(r.get("pnl", 0) or 0),
            "vol": float(r.get("vol", 0) or 0),
            "userName": r.get("userName") or "",
        }
    return idx


def status_label(ranks):
    day = ranks.get("DAY", 999)
    week = ranks.get("WEEK", 999)
    month = ranks.get("MONTH", 999)
    if day <= 10 and week <= 10 and month <= 20:
        return "巅峰"
    if week <= 15 and month <= 30:
        return "强势"
    if month <= 20 and day > 30:
        return "观察"
    return "普通"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--categories", default="OVERALL,POLITICS,CRYPTO")
    ap.add_argument("--top", type=int, default=5)
    ap.add_argument("--limit", type=int, default=100)
    args = ap.parse_args()

    categories = [c.strip().upper() for c in args.categories.split(",") if c.strip()]
    boards = {(c, p): fetch_board(c, p, args.limit) for c in categories for p in PERIODS}

    stats = defaultdict(lambda: {
        "wallet": "",
        "userName": "",
        "score": 0,
        "hits": 0,
        "per": defaultdict(dict),
    })

    for (c, p), board in boards.items():
        for w, r in board.items():
            st = stats[w]
            st["wallet"] = w
            if r["userName"]:
                st["userName"] = r["userName"]
            st["hits"] += 1
            st["score"] += max(0, 101 - r["rank"])  # higher rank => higher score
            st["per"][c][p] = r

    ranked = sorted(stats.values(), key=lambda x: (x["hits"], x["score"]), reverse=True)[: args.top]

    out = []
    for t in ranked:
        # choose best category by avg rank in week/month
        best_cat, best_avg = None, 999.0
        for c, per in t["per"].items():
            wk = per.get("WEEK", {}).get("rank", 999)
            mo = per.get("MONTH", {}).get("rank", 999)
            avg = (wk + mo) / 2
            if avg < best_avg:
                best_avg, best_cat = avg, c

        ranks = {p: t["per"].get(best_cat, {}).get(p, {}).get("rank", 999) for p in PERIODS}
        out.append({
            "userName": t["userName"] or t["wallet"],
            "wallet": t["wallet"],
            "focusCategory": best_cat,
            "status": status_label(ranks),
            "score": t["score"],
            "hits": t["hits"],
            "ranks": ranks,
        })

    print(json.dumps(out, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
