#!/usr/bin/env python3
"""Research helpers for the content-strategy skill. Standard library only.

Commands
  suggest     expand seed topics through search autocomplete (Google or YouTube)
              -> relative demand signals with an intent tag
  trends-csv  summarize Google Trends "interest over time" CSV exports
              (growth, year-over-year, seasonality, spikiness)
  gap         compare demand keywords against competitor/niche titles
              -> gap / thin / contested
  calendar    lay out a content calendar from a JSON plan so pillar ratios
              and posting cadence match the plan exactly

Honesty note: autocomplete rank and Google Trends values are RELATIVE signals,
not search volume. Do not present them as volumes.
"""
import argparse
import csv
import json
import os
import re
import statistics
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from collections import defaultdict
from datetime import date, datetime, timedelta

SUGGEST_URL = "https://suggestqueries.google.com/complete/search"
QUESTION_WORDS = {"how", "what", "why", "when", "where", "who", "which", "can", "does", "do",
                  "is", "are", "should", "will"}
COMPARE_WORDS = {"vs", "versus", "alternative", "alternatives", "compare", "comparison"}
COMMERCIAL_WORDS = {"best", "top", "review", "reviews", "price", "pricing", "cost", "cheap",
                    "cheapest", "buy", "discount", "coupon", "hire", "agency", "service", "services"}
FUNNEL_HINT = {"question": "awareness", "informational": "engagement",
               "comparison": "conversion", "commercial": "conversion"}


# --------------------------------------------------------------------------
# shared output helpers
# --------------------------------------------------------------------------
def save_rows(rows, meta, base):
    if not base:
        return
    parent = os.path.dirname(base)
    if parent:
        os.makedirs(parent, exist_ok=True)
    with open(base + ".json", "w", encoding="utf-8") as f:
        json.dump({"meta": meta, "rows": rows}, f, ensure_ascii=False, indent=2)
    if rows:
        with open(base + ".csv", "w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
            w.writeheader()
            w.writerows(rows)
    print(f"\nSaved {base}.json and {base}.csv", file=sys.stderr)


def fnum(x, nd=1):
    return "-" if x is None else f"{x:.{nd}f}"


# --------------------------------------------------------------------------
# suggest
# --------------------------------------------------------------------------
class HelperError(RuntimeError):
    pass


def fetch_suggest(q, source, hl, gl, timeout=15):
    params = {"client": "firefox", "q": q}
    if hl:
        params["hl"] = hl
    if gl:
        params["gl"] = gl
    if source == "youtube":
        params["ds"] = "yt"
    req = urllib.request.Request(
        SUGGEST_URL + "?" + urllib.parse.urlencode(params),
        headers={"User-Agent": "Mozilla/5.0 (content-strategy skill)"},
    )
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            data = json.loads(r.read().decode("utf-8", "replace"))
    except urllib.error.URLError as e:
        raise HelperError(
            f"Could not reach the autocomplete endpoint ({getattr(e, 'reason', e)}). In a sandbox this "
            "host may be blocked; run the command on your own machine, or use WebSearch instead."
        ) from None
    except ValueError:
        raise HelperError("Autocomplete returned something that is not JSON (endpoint changed or throttled).") from None
    return [s for s in (data[1] if len(data) > 1 else []) if isinstance(s, str)]


def expansions(seed, modes):
    out = [seed]
    if "questions" in modes:
        out += [f"{w} {seed}" for w in ("how to", "what is", "why", "when to", "can", "should", "is", "how much")]
    if "modifiers" in modes:
        out += [f"{seed} {m}" for m in ("for beginners", "for small business", "vs", "alternative",
                                        "best", "tools", "examples", "mistakes", "cost", "review",
                                        "template", "tips")]
    if "alpha" in modes:
        out += [f"{seed} {c}" for c in "abcdefghijklmnopqrstuvwxyz"]
    return list(dict.fromkeys(out))


def intent_of(kw):
    toks = re.findall(r"\w+", kw.lower())
    if any(t in COMPARE_WORDS for t in toks):
        return "comparison"
    if any(t in COMMERCIAL_WORDS for t in toks) or "near me" in " ".join(toks):
        return "commercial"
    if toks and toks[0] in QUESTION_WORDS:
        return "question"
    return "informational"


def cmd_suggest(a):
    modes = {m.strip() for m in a.expand.split(",") if m.strip()}
    plan = [(seed, q) for seed in a.seeds for q in expansions(seed, modes)]
    if len(plan) > a.max_requests:
        raise HelperError(f"{len(plan)} requests planned, above --max-requests {a.max_requests}. "
                          "Use fewer seeds/expansions or raise the limit.")
    print(f"{len(plan)} autocomplete requests...", file=sys.stderr)
    agg = {}
    for seed, q in plan:
        for rank, s in enumerate(fetch_suggest(q, a.source, a.hl, a.gl)):
            e = agg.setdefault(s.lower(), {"keyword": s.lower(), "seed": seed, "demand_score": 0,
                                           "appearances": 0, "best_rank": rank + 1, "queries": set()})
            if q not in e["queries"]:
                e["queries"].add(q)
                e["appearances"] += 1
                e["demand_score"] += max(10 - rank, 1)
            e["best_rank"] = min(e["best_rank"], rank + 1)
        if a.sleep:
            time.sleep(a.sleep)
    rows = []
    for e in agg.values():
        e.pop("queries")
        e["intent"] = intent_of(e["keyword"])
        e["funnel_hint"] = FUNNEL_HINT[e["intent"]]
        rows.append(e)
    rows.sort(key=lambda r: (-r["demand_score"], r["keyword"]))
    print(f"{'score':>5} {'seen':>4} {'rank':>4}  {'intent':<13} keyword")
    for r in rows[:a.limit]:
        print(f"{r['demand_score']:>5} {r['appearances']:>4} {r['best_rank']:>4}  {r['intent']:<13} {r['keyword']}")
    if len(rows) > a.limit:
        print(f"... {len(rows) - a.limit} more (see saved files or raise --limit)")
    meta = {"command": "suggest", "source": a.source, "seeds": a.seeds, "expand": sorted(modes),
            "requests": len(plan), "generated": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "note": "demand_score is a relative autocomplete signal, NOT search volume. "
                    "funnel_hint is a keyword-pattern heuristic."}
    save_rows(rows, meta, a.out)


# --------------------------------------------------------------------------
# trends-csv
# --------------------------------------------------------------------------
HEADER_FIRST = {"week", "day", "month", "time", "date"}


def parse_date(s):
    s = s.strip()
    for n, fmt in ((10, "%Y-%m-%d"), (7, "%Y-%m")):
        try:
            return datetime.strptime(s[:n], fmt).date()
        except ValueError:
            continue
    return None


def parse_val(v):
    v = v.strip()
    if not v:
        return None
    if v.startswith("<"):
        return 0.5
    try:
        return float(v)
    except ValueError:
        return None


def read_trends(path):
    with open(path, encoding="utf-8-sig", newline="") as f:
        rows = list(csv.reader(f))
    start = next((i for i, r in enumerate(rows) if len(r) >= 2 and r[0].strip().lower() in HEADER_FIRST), None)
    if start is None:
        raise HelperError(f"{path}: no 'Week/Day/Month,term' header found. Export 'interest over time' from "
                          "Google Trends (Download button on the chart).")
    terms = [re.sub(r":\s*\(.*\)\s*$", "", h).strip() for h in rows[start][1:]]
    series = {t: [] for t in terms}
    for r in rows[start + 1:]:
        if not r or not r[0].strip():
            break
        d = parse_date(r[0])
        if not d:
            break
        for t, v in zip(terms, r[1:]):
            series[t].append((d, parse_val(v)))
    return series


def mean(xs):
    return statistics.fmean(xs) if xs else None


def analyze_series(pts):
    pts = sorted((d, v) for d, v in pts if v is not None)
    if len(pts) < 8:
        return None
    last = pts[-1][0]
    vals = [v for _, v in pts]
    overall = mean(vals)

    def window(lo, hi):
        return [v for d, v in pts if last - timedelta(days=hi) < d <= last - timedelta(days=lo)]

    span = (last - pts[0][0]).days
    recent, prior, year_ago = window(0, 90), window(90, 180), window(365, 455)
    growth = yoy = None
    if span >= 180 and recent and prior and mean(prior) > 0:
        growth = (mean(recent) / mean(prior) - 1) * 100
    if span >= 455 and recent and year_ago and mean(year_ago) > 0:
        yoy = (mean(recent) / mean(year_ago) - 1) * 100
    peak_d, peak_v = max(pts, key=lambda p: p[1])
    p2m = peak_v / overall if overall else None
    if growth is None:
        trend = "insufficient history"
    elif growth >= 15:
        trend = "rising"
    elif growth <= -15:
        trend = "declining"
    else:
        trend = "stable"
    if p2m and p2m > 4:
        trend += " (spiky: check if news-driven)"
    season_peak = season_trough = season_range = None
    if span >= 700 and overall:
        by_month = defaultdict(list)
        for d, v in pts:
            by_month[d.month].append(v)
        idx = {m: mean(v) / overall for m, v in by_month.items()}
        if len(idx) >= 6:
            pm, tm = max(idx, key=idx.get), min(idx, key=idx.get)
            season_peak, season_trough = date(2000, pm, 1).strftime("%b"), date(2000, tm, 1).strftime("%b")
            season_range = round(idx[pm] - idx[tm], 2)
    return {
        "points": len(pts), "span_days": span, "mean": round(overall, 1),
        "latest_4pt_mean": round(mean(vals[-4:]), 1),
        "growth_90d_pct": None if growth is None else round(growth, 1),
        "yoy_pct": None if yoy is None else round(yoy, 1),
        "trend": trend, "peak_date": peak_d.isoformat(),
        "peak_to_mean": None if p2m is None else round(p2m, 1),
        "season_peak": season_peak, "season_trough": season_trough, "season_range": season_range,
    }


def cmd_trends(a):
    rows = []
    for path in a.files:
        for term, pts in read_trends(path).items():
            res = analyze_series(pts)
            if res is None:
                print(f"skipped '{term}' in {path}: fewer than 8 usable points", file=sys.stderr)
                continue
            rows.append({"file": os.path.basename(path), "term": term, **res})
    if not rows:
        print("No analyzable series.")
        return
    print(f"{'term':<28} {'mean':>5} {'now':>5} {'90d%':>7} {'yoy%':>7}  {'peak':<10} {'season':<11} trend")
    for r in rows:
        season = f"{r['season_peak']}/{r['season_trough']}" if r["season_peak"] else "-"
        print(f"{r['term'][:28]:<28} {r['mean']:>5} {r['latest_4pt_mean']:>5} {fnum(r['growth_90d_pct']):>7} "
              f"{fnum(r['yoy_pct']):>7}  {r['peak_date']:<10} {season:<11} {r['trend']}")
    print("\nValues are relative (0-100 inside one export). Terms are comparable only within the same file.")
    save_rows(rows, {"command": "trends-csv", "files": a.files,
                     "note": "relative Google Trends index; not search volume"}, a.out)


# --------------------------------------------------------------------------
# gap
# --------------------------------------------------------------------------
STOP = {"the", "a", "an", "to", "of", "for", "in", "on", "and", "or", "is", "are", "it", "your", "you",
        "my", "with", "i", "best", "top", "vs", "versus"} | QUESTION_WORDS
# DATA, not prose: Roman Urdu / Hinglish function words (equivalents of "of", "how", "do", "is", "method"...).
# Search phrases and video titles in South Asian niches are often written in Roman Urdu or Hinglish. Without this
# list a phrase only matched titles that repeated every small word, so real competitors were missed and gaps were
# overstated. Keep it so the gap matrix works for those audiences.
STOP_ROMAN = {"ka", "ki", "ke", "ko", "se", "me", "mein", "main", "par", "pe", "hai", "hain", "ho", "hota", "hoti",
              "kaise", "kese", "kaisay", "kesay", "kya", "kyun", "kyu", "aur", "ya", "bhi", "ye", "yeh", "wo", "woh",
              "kar", "kare", "karen", "karein", "kre", "kren", "karo", "karna", "karne", "karte", "kiya", "wala",
              "wali", "wale", "liye", "lie", "tarika", "tareeqa", "tareeka", "tarike"}
# DATA: spelling variants and Roman Urdu terms mapped to one English word, so "electricity", "electric" and the
# Roman Urdu word for electricity count as the same keyword. Add entries for your own niche as needed.
VARIANTS = {"electric": "electricity", "bijli": "electricity", "bijlee": "electricity", "bijly": "electricity",
            "bachat": "saving", "bachao": "saving", "bachaye": "saving", "bachayein": "saving", "savings": "saving",
            "kam": "reduce", "kum": "reduce", "lower": "reduce", "cut": "reduce"}


def tokens(text):
    out = set()
    for t in re.findall(r"[^\W_]+", text.lower()):
        if t in STOP or t in STOP_ROMAN:
            continue
        if len(t) > 3 and t.endswith("s") and not t.endswith("ss"):
            t = t[:-1]
        out.add(VARIANTS.get(t, t))
    return out


def read_demand(path):
    items = []
    if path.lower().endswith(".csv"):
        with open(path, encoding="utf-8-sig", newline="") as f:
            rd = csv.DictReader(f)
            kcol = "keyword" if "keyword" in (rd.fieldnames or []) else (rd.fieldnames or [None])[0]
            scol = next((c for c in ("demand_score", "score") if c in (rd.fieldnames or [])), None)
            for r in rd:
                kw = (r.get(kcol) or "").strip()
                if kw:
                    try:
                        sc = float(r[scol]) if scol and r.get(scol) not in (None, "") else 1.0
                    except ValueError:
                        sc = 1.0
                    items.append((kw, sc))
    else:
        with open(path, encoding="utf-8-sig") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#"):
                    items.append((line, 1.0))
    return items


def read_supply(paths):
    out = []
    for p in paths:
        with open(p, encoding="utf-8-sig", newline="") as f:
            rd = csv.DictReader(f)
            if "title" not in (rd.fieldnames or []):
                raise HelperError(f"{p}: no 'title' column (use output of yt_research.py / yt_competitors.py).")
            for r in rd:
                title = (r.get("title") or "").strip()
                if not title:
                    continue
                try:
                    views = int(float(r["views"])) if r.get("views") not in (None, "") else None
                except (ValueError, KeyError):
                    views = None
                out.append({"title": title, "views": views, "tokens": tokens(title)})
    return out


def classify_gap(demand, supply, thin):
    rows = []
    for kw, score in demand:
        kt = tokens(kw)
        if not kt:
            continue
        full, partial = [], 0
        for s in supply:
            inter = len(kt & s["tokens"])
            if inter == len(kt):
                full.append(s)
            elif len(kt) >= 3 and inter / len(kt) >= 0.6:
                partial += 1
        views = [s["views"] for s in full if s["views"] is not None]
        top = max(full, key=lambda s: s["views"] or 0) if full else None
        cls = "gap" if not full else ("thin" if len(full) <= thin else "contested")
        rows.append({
            "class": cls, "keyword": kw, "demand_score": score, "full_matches": len(full),
            "partial_matches": partial,
            "top_match_views": max(views) if views else None,
            "median_match_views": int(statistics.median(views)) if views else None,
            "top_match_title": top["title"] if top else "",
        })
    order = {"gap": 0, "thin": 1, "contested": 2}
    rows.sort(key=lambda r: (order[r["class"]], -r["demand_score"], r["keyword"]))
    return rows


def cmd_gap(a):
    demand = read_demand(a.demand)
    supply = read_supply(a.supply)
    if not demand:
        raise HelperError("Demand file is empty.")
    if not supply:
        raise HelperError("Supply files contain no titles.")
    rows = classify_gap(demand, supply, a.thin)
    counts = {c: sum(1 for r in rows if r["class"] == c) for c in ("gap", "thin", "contested")}
    print(f"{len(demand)} demand items vs {len(supply)} supply titles -> {counts}")
    print(f"{'class':<10} {'score':>6} {'full':>4} {'part':>4} {'top_views':>10}  keyword")
    for r in rows[:a.limit]:
        tv = r["top_match_views"]
        print(f"{r['class']:<10} {r['demand_score']:>6.0f} {r['full_matches']:>4} {r['partial_matches']:>4} "
              f"{(str(tv) if tv is not None else '-'):>10}  {r['keyword']}")
    if len(rows) > a.limit:
        print(f"... {len(rows) - a.limit} more (see saved files or raise --limit)")
    print("\nA gap is only as reliable as the supply sample: judge it against how many titles were compared.")
    save_rows(rows, {"command": "gap", "demand_items": len(demand), "supply_titles": len(supply),
                     "thin_threshold": a.thin, "counts": counts}, a.out)


# --------------------------------------------------------------------------
# calendar
# --------------------------------------------------------------------------
DAYS = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
EXAMPLE_PLAN = {
    "start": "2026-12-01", "weeks": 4,
    "pillars": [
        {"name": "Education", "weight": 50, "stage": "awareness"},
        {"name": "Proof and case studies", "weight": 30, "stage": "conversion"},
        {"name": "Community and behind the scenes", "weight": 20, "stage": "engagement"},
    ],
    "platforms": [
        {"name": "YouTube", "per_week": 2, "days": ["Tue", "Fri"]},
        {"name": "Instagram", "per_week": 4},
    ],
}


def norm_day(d):
    d = str(d).strip()[:3].title()
    if d not in DAYS:
        raise HelperError(f"Unknown weekday '{d}'. Use Mon..Sun.")
    return d


def pick_days(per_week, days):
    if days:
        return sorted({DAYS.index(norm_day(d)) for d in days})
    if per_week > 7:
        raise HelperError("per_week above 7: add a second entry for the same platform instead.")
    chosen = []
    for i in range(per_week):
        d = round(i * 7 / per_week) % 7
        while d in chosen:
            d = (d + 1) % 7
        chosen.append(d)
    return sorted(chosen)


def assign_pillars(pillars, n):
    total = sum(p["weight"] for p in pillars)
    counts = {p["name"]: 0 for p in pillars}
    out, prev = [], None
    for i in range(n):
        def key(p):
            deficit = p["weight"] / total * (i + 1) - counts[p["name"]]
            return (deficit - (0.5 if p["name"] == prev else 0.0), p["weight"])
        best = max(pillars, key=key)
        counts[best["name"]] += 1
        out.append(best)
        prev = best["name"]
    return out


def build_calendar(plan):
    pillars, platforms = plan.get("pillars") or [], plan.get("platforms") or []
    if not pillars or not platforms:
        raise HelperError("Plan needs non-empty 'pillars' and 'platforms'.")
    for p in pillars:
        if not p.get("name") or float(p.get("weight", 0)) <= 0:
            raise HelperError("Every pillar needs a name and a positive weight.")
    start = datetime.strptime(plan["start"], "%Y-%m-%d").date()
    weeks = int(plan.get("weeks", 4))
    monday = start - timedelta(days=start.weekday())
    rows = []
    for pf in platforms:
        days = pick_days(int(pf["per_week"]), pf.get("days"))
        slots = []
        for w in range(weeks):
            for d in days:
                dt = monday + timedelta(days=w * 7 + d)
                if dt >= start:
                    slots.append(dt)
        for dt, pillar in zip(slots, assign_pillars(pillars, len(slots))):
            rows.append({
                "date": dt.isoformat(), "weekday": DAYS[dt.weekday()],
                "week": (dt - monday).days // 7 + 1, "platform": pf["name"],
                "pillar": pillar["name"], "funnel_stage": pillar.get("stage", ""),
                "format": "", "topic": "", "hook": "", "evidence_id": "", "cta": "", "status": "to fill",
            })
    rows.sort(key=lambda r: (r["date"], r["platform"]))
    return rows


def cmd_calendar(a):
    if a.example:
        print(json.dumps(EXAMPLE_PLAN, indent=2))
        return
    if not a.plan:
        raise HelperError("Pass --plan plan.json (use --example to print a template).")
    with open(a.plan, encoding="utf-8") as f:
        plan = json.load(f)
    rows = build_calendar(plan)
    cur = None
    for r in rows:
        if r["week"] != cur:
            cur = r["week"]
            print(f"\nWeek {cur}")
        print(f"  {r['date']} {r['weekday']}  {r['platform']:<12} {r['pillar']}  [{r['funnel_stage'] or '-'}]")
    total = len(rows)
    print("\nPillar mix (actual vs target):")
    wsum = sum(float(p["weight"]) for p in plan["pillars"])
    for p in plan["pillars"]:
        n = sum(1 for r in rows if r["pillar"] == p["name"])
        print(f"  {p['name']:<34} {100 * n / total:5.1f}%  target {100 * float(p['weight']) / wsum:5.1f}%")
    save_rows(rows, {"command": "calendar", "plan": plan}, a.out)


# --------------------------------------------------------------------------
def build_parser():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="cmd", required=True)

    s = sub.add_parser("suggest", help="autocomplete keyword expansion")
    s.add_argument("seeds", nargs="+", help="seed topics, e.g. 'ai chatbot' 'whatsapp automation'")
    s.add_argument("--source", choices=["google", "youtube"], default="google")
    s.add_argument("--hl", help="interface language, e.g. en, ur, hi")
    s.add_argument("--gl", help="country code, e.g. PK, IN, AE, US")
    s.add_argument("--expand", default="questions,modifiers", help="comma list: questions, modifiers, alpha")
    s.add_argument("--sleep", type=float, default=0.3, help="seconds between requests")
    s.add_argument("--max-requests", type=int, default=150)
    s.add_argument("--limit", type=int, default=40)
    s.add_argument("--out")
    s.set_defaults(fn=cmd_suggest)

    t = sub.add_parser("trends-csv", help="summarize Google Trends CSV exports")
    t.add_argument("files", nargs="+")
    t.add_argument("--out")
    t.set_defaults(fn=cmd_trends)

    g = sub.add_parser("gap", help="demand keywords vs competitor titles")
    g.add_argument("--demand", required=True, help="txt (one keyword per line) or csv with a keyword column")
    g.add_argument("--supply", nargs="+", required=True, help="csv file(s) with a title column (and views)")
    g.add_argument("--thin", type=int, default=2, help="max matching titles still counted as thin")
    g.add_argument("--limit", type=int, default=40)
    g.add_argument("--out")
    g.set_defaults(fn=cmd_gap)

    c = sub.add_parser("calendar", help="lay out a calendar from a JSON plan")
    c.add_argument("--plan", help="plan JSON file")
    c.add_argument("--example", action="store_true", help="print an example plan and exit")
    c.add_argument("--out")
    c.set_defaults(fn=cmd_calendar)
    return p


def main(argv=None):
    a = build_parser().parse_args(argv)
    try:
        a.fn(a)
    except (HelperError, ValueError, KeyError, OSError) as e:
        print(f"error: {e}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
