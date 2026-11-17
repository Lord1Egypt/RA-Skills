#!/usr/bin/env python3
"""Rec League Scheduler — fixtures, absence-aware rotation, fairness audit, standings.

Circle-method round-robin (single/double), match-night re-flow for real
attendance, bye distribution to least-benched players, standings with
head-to-head tiebreak, printable match-day sheet. Local state in league.json.
"""
import argparse
import datetime as dt
import itertools
import json
import sys
from pathlib import Path

DB = Path("league.json")


def load(db=None):
    p = Path(db) if db else DB
    if p.exists():
        try:
            data = json.loads(p.read_text())
            for k in ("players", "absences", "results", "byes", "played_pairs"):
                data.setdefault(k, [] if k != "played_pairs" else [])
            if "bye_count" not in data:
                data["bye_count"] = {}
            return data
        except Exception:
            pass
    return {"players": [], "absences": [], "results": [], "byes": [],
            "played_pairs": [], "bye_count": {}}


def save(data, db=None):
    p = Path(db) if db else DB
    p.write_text(json.dumps(data, ensure_ascii=False, indent=2))


def now_iso():
    return dt.datetime.now().isoformat(timespec="minutes")


# ---------------------------------------------------------------- players
def cmd_player(a):
    data = load(a.db)
    if a.action == "list":
        if not data["players"]:
            print("No players. Add: league.py player add \"Alex\" --level 4")
            return 0
        print(f"{'name':16}{'level':>5}  games  byes")
        for p in sorted(data["players"], key=lambda p: -p.get("level", 3)):
            g = sum(1 for r in data["results"] if r["a"] == p["name"] or r["b"] == p["name"])
            b = data["bye_count"].get(p["name"], 0)
            print(f"{p['name'][:15]:16}{p.get('level', 3):>5}  {g:>5}  {b:>4}")
        return 0
    if not a.name:
        print("[!] player name required")
        return 1
    if any(p["name"].lower() == a.name.lower() for p in data["players"]):
        print(f"[!] {a.name} already on roster")
        return 1
    lvl = a.level if (a.level and 1 <= a.level <= 5) else 3
    data["players"].append({"name": a.name, "level": lvl, "added": now_iso()})
    save(data, a.db)
    print(f"added {a.name} (level {lvl}) — roster: {len(data['players'])}")
    return 0


# ---------------------------------------------------------------- fixtures
def circle_rounds(names):
    """Circle method: returns list of rounds; each round = list of pairs, plus bye."""
    n = len(names)
    lst = list(names)
    if n % 2 == 1:
        lst.append(None)  # None = bye marker
        n += 1
    rounds = []
    fixed = lst[0]
    rot = lst[1:]
    for _ in range(n - 1):
        ring = [fixed] + rot
        pairs, bye = [], None
        for i in range(n // 2):
            x, y = ring[i], ring[n - 1 - i]
            if x is None:
                bye = y
            elif y is None:
                bye = x
            else:
                pairs.append((x, y))
        rounds.append((pairs, bye))
        rot = [rot[-1]] + rot[:-1]  # rotate
    return rounds


def cmd_fixtures(a):
    data = load(a.db)
    names = [p["name"] for p in data["players"]]
    if len(names) < 4:
        print(f"[!] need ≥4 players for fixtures (have {len(names)})")
        return 1
    rounds = circle_rounds(names)
    if a.double:
        second = [([(y, x) for x, y in pairs], bye) for pairs, bye in circle_rounds(names)]
        rounds = rounds + second
    label = "double" if a.double else "single"
    print(f"FIXTURES — {label} round-robin, {len(names)} players, "
          f"{len(rounds)} rounds, {a.courts} court(s)\n" + "=" * 56)
    for rn, (pairs, bye) in enumerate(rounds, 1):
        print(f"Round {rn}{'  (bye: ' + bye + ')' if bye else ''}")
        for ci, (x, y) in enumerate(pairs[:a.courts], 1):
            print(f"  court {ci}: {x} vs {y}")
        if len(pairs) > a.courts:
            print(f"  (slots full: {len(pairs) - a.courts} more pair(s) waitlisted this round)")
        print()
    return 0


# ---------------------------------------------------------------- absences
def cmd_absent(a):
    data = load(a.db)
    if not a.name:
        if not data["absences"]:
            print("No absences recorded.")
        else:
            for ab in data["absences"]:
                print(f"  {ab['date']}  {ab['name']}")
        return 0
    data["absences"].append({"name": a.name, "date": a.date})
    save(data, a.db)
    print(f"absence recorded: {a.name} on {a.date}")
    return 0


# ---------------------------------------------------------------- night
def cmd_night(a):
    data = load(a.db)
    roster = [p["name"] for p in data["players"]]
    absent_today = {ab["name"] for ab in data["absences"] if ab["date"] == a.date}
    if a.absent:
        absent_today |= set(x.strip() for x in a.absent.split(",") if x.strip())
    present = [n for n in roster if n not in absent_today]
    if a.present is not None and a.present != len(present):
        print(f"[!] --present {a.present} but roster-minus-absent = {len(present)}: {', '.join(present)}")
        print("    fix with --absent or adjust --present")
        return 1
    slots = a.courts * 2
    byes_needed = len(present) - slots
    if byes_needed < 0:
        print(f"[!] {len(present)} present but {slots} slots ({a.courts} courts × 2) — short by {-byes_needed}. Call-ups needed:")
        avail = [n for n in roster if n in absent_today]
        print("    call-up candidates (marked absent today): " + (", ".join(avail) or "none — recruit outside roster"))
        return 2
    # bye assignment: fewest byes so far; tie → alphabetical
    order = sorted(present, key=lambda n: (data["bye_count"].get(n, 0), n))
    byes_tonight = order[:byes_needed] if byes_needed > 0 else []
    playing = [n for n in present if n not in byes_tonight]
    # pairing: prefer pairs that haven't met (by played_pairs), balance skill
    met = {frozenset(p) for p in data["played_pairs"]}
    lvl = {p["name"]: p.get("level", 3) for p in data["players"]}
    pairs, rest = [], list(playing)
    # greedy: for each strongest remaining player, pick partner they've met least
    while len(rest) >= 2:
        rest.sort(key=lambda n: (-lvl.get(n, 3), n))
        x = rest.pop(0)
        best = min(rest, key=lambda n: (frozenset((x, n)) in met, abs(lvl.get(x, 3) - lvl.get(n, 3)), n))
        rest.remove(best)
        pairs.append((x, best))
    print(f"MATCH NIGHT {a.date} — {len(present)} present, {a.courts} court(s)\n" + "=" * 56)
    for ci in range(a.courts):
        if ci < len(pairs):
            x, y = pairs[ci]
            print(f"court {ci+1}: {x} vs {y}      score ____ : ____")
        else:
            print(f"court {ci+1}: (open — skills/warmup)")
    if byes_tonight:
        print(f"byes: {', '.join(byes_tonight)}")
        for b in byes_tonight:
            data["bye_count"][b] = data["bye_count"].get(b, 0) + 1
            data["byes"].append({"name": b, "date": a.date})
    for x, y in pairs[:a.courts]:
        data["played_pairs"].append([x, y])
    save(data, a.db)
    print("\n(fixture order balanced by: unmet pairs first, then close skill levels)")
    print("Record: league.py result \"Alex\" 21 15 \"Sam\"")
    return 0


# ---------------------------------------------------------------- results
def cmd_result(a):
    data = load(a.db)
    names = {p["name"].lower(): p["name"] for p in data["players"]}
    if a.a.lower() not in names or a.b.lower() not in names:
        print("[!] both players must be on the roster")
        return 1
    A, B = names[a.a.lower()], names[a.b.lower()]
    data["results"].append({"a": A, "ascore": a.ascore, "b": B, "bscore": a.bscore,
                            "date": a.date or now_iso()[:10]})
    save(data, a.db)
    w = A if a.ascore > a.bscore else B
    print(f"recorded: {A} {a.ascore} : {a.bscore} {B} — winner {w}")
    return 0


def standings_rows(data):
    rows = []
    for p in data["players"]:
        n = p["name"]
        w = l = gw = gl = 0
        h2h = {}
        for r in data["results"]:
            if r["a"] == n or r["b"] == n:
                mine, theirs = (r["ascore"], r["bscore"]) if r["a"] == n else (r["bscore"], r["ascore"])
                opp = r["b"] if r["a"] == n else r["a"]
                gw += mine; gl += theirs
                if mine > theirs:
                    w += 1; h2h[opp] = h2h.get(opp, 0) + 1
                else:
                    l += 1; h2h[opp] = h2h.get(opp, 0) - 1
        rows.append({"name": n, "w": w, "l": l, "diff": gw - gl, "pts": 2 * w, "h2h": h2h})
    return rows


def cmd_standings(a):
    data = load(a.db)
    rows = standings_rows(data)
    if not any(r["w"] or r["l"] for r in rows):
        print("No results yet. Record: league.py result \"Alex\" 21 15 \"Sam\"")
        return 0
    # sort: points, diff, then head-to-head between tied groups
    rows.sort(key=lambda r: (-r["pts"], -r["diff"], r["name"]))
    # apply h2h within (pts, diff) ties
    i = 0
    while i < len(rows):
        j = i
        while j + 1 < len(rows) and rows[j + 1]["pts"] == rows[i]["pts"] and rows[j + 1]["diff"] == rows[i]["diff"]:
            j += 1
        if j > i:
            group = rows[i:j + 1]
            group.sort(key=lambda r: (-sum(r["h2h"].get(o["name"], 0) for o in group if o is not r), r["name"]))
            rows[i:j + 1] = group
        i = j + 1
    print(f"STANDINGS — {len(data['results'])} games\n" + "=" * 46)
    print(f"{'#':>2} {'player':16}{'W':>3}{'L':>3}{'diff':>6}{'pts':>5}")
    for i, r in enumerate(rows, 1):
        print(f"{i:>2} {r['name'][:15]:16}{r['w']:>3}{r['l']:>3}{r['diff']:>6}{r['pts']:>5}")
    print("\n(ties broken by game difference, then head-to-head)")
    return 0


# ---------------------------------------------------------------- audit
def cmd_audit(a):
    data = load(a.db)
    rows = standings_rows(data)
    n = len(rows)
    if not n:
        print("No players yet.")
        return 0
    games = [r["w"] + r["l"] for r in rows]
    byes = [data["bye_count"].get(r["name"], 0) for r in rows]
    gm, bm = sum(games) / n, sum(byes) / n
    print("FAIRNESS AUDIT\n" + "=" * 46)
    print(f"{'player':16}{'games':>6}{'byes':>6}")
    for r, g, b in sorted(zip(rows, games, byes), key=lambda t: -t[1]):
        flag = ""
        if games and abs(g - gm) > 1:
            flag += " ← game spread"
        if byes and abs(b - bm) > 1:
            flag += " ← bye spread"
        print(f"{r['name'][:15]:16}{g:>6}{b:>6}{flag}")
    issues = []
    if max(games) - min(games) > 1 and len(data["results"]) >= n:
        issues.append(f"game spread {max(games)}-{min(games)} exceeds ±1")
    if byes and max(byes) - min(byes) > 1 and sum(byes) >= n:
        issues.append(f"bye spread {max(byes)}-{min(byes)} exceeds ±1")
    # consecutive byes
    bydate = {}
    for b in data["byes"]:
        bydate.setdefault(b["name"], []).append(b["date"])
    for name, ds in bydate.items():
        ds = sorted(ds)
        for x, y in zip(ds, ds[1:]):
            dd = (dt.date.fromisoformat(y) - dt.date.fromisoformat(x)).days
            if 0 < dd <= 7:
                issues.append(f"{name}: byes on {x} and {y} back-to-back")
    # duplicate pair meetings
    from collections import Counter
    c = Counter(frozenset(p) for p in data["played_pairs"])
    dups = [(tuple(sorted(k)), v) for k, v in c.items() if v > 1]
    if dups:
        issues.append(f"{len(dups)} pair(s) met more than once: " +
                      ", ".join(f"{x[0]}×{x[1]}({v})" for x, v in dups[:5]))
    print()
    if issues:
        print("ISSUES:")
        for i in issues:
            print(f"  - {i}")
        return 2
    print("Fair: games and byes within ±1, no back-to-back byes" +
          (", no repeated pairs" if data["played_pairs"] else ""))
    return 0


# ----------------------------------------------------------------
def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--db", default=None)
    sub = ap.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("player", help="add/list players")
    p.add_argument("action", nargs="?", default="list", choices=["add", "list"])
    p.add_argument("name", nargs="?", default=None)
    p.add_argument("--level", type=int, default=None, help="1-5 skill (optional)")
    p.set_defaults(fn=cmd_player)

    p = sub.add_parser("fixtures", help="round-robin fixture list")
    p.add_argument("--courts", type=int, default=2)
    p.add_argument("--double", action="store_true", help="home-and-away (2×)")
    p.set_defaults(fn=cmd_fixtures)

    p = sub.add_parser("absent", help="record/list absences")
    p.add_argument("name", nargs="?", default=None)
    p.add_argument("--date", default=dt.date.today().isoformat())
    p.set_defaults(fn=cmd_absent)

    p = sub.add_parser("night", help="match-night sheet for real attendance")
    p.add_argument("--date", default=dt.date.today().isoformat())
    p.add_argument("--courts", type=int, default=2)
    p.add_argument("--present", type=int, default=None, help="expected count (sanity check)")
    p.add_argument("--absent", default=None, help="comma-separated names also out today")
    p.set_defaults(fn=cmd_night)

    p = sub.add_parser("result", help="record a score")
    p.add_argument("a")
    p.add_argument("ascore", type=int)
    p.add_argument("bscore", type=int)
    p.add_argument("b")
    p.add_argument("--date", default=None)
    p.set_defaults(fn=cmd_result)

    p = sub.add_parser("standings", help="points table with h2h tiebreak")
    p.set_defaults(fn=cmd_standings)

    p = sub.add_parser("audit", help="fairness report")
    p.set_defaults(fn=cmd_audit)

    a = ap.parse_args()
    sys.exit(a.fn(a) or 0)


if __name__ == "__main__":
    main()
