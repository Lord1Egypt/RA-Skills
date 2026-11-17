#!/usr/bin/env python3
"""Check a micro drama season grid (the Markdown table from assets/templates/episode-grid.md).

Usage:
  python3 grid_check.py grid.md [--json]

Reads the first Markdown table whose header has an "Ep" column. Columns are matched by name, in any order:
  Ep, Title, Spring (COMPRESS or RELEASE), Open, Hook, Reversal (or Turn), Payoff, Cliffhanger type, Cliffhanger beat
  (or one "Cliffhanger" column written as "type: beat"), Cast, Places, Rung, Secrets, Pay (PAYWALL or HOOK).
Checks:
  - every row has a hook, a reversal, a payoff and a cliffhanger;
  - no cliffhanger type twice in a row, none on more than about a third of the rows, types from the library;
  - no more than two COMPRESS rows in a row, a RELEASE at least every three rows;
  - one PAYWALL row for seasons of 20 episodes or more, usually between episodes 8 and 12;
  - four cast members or fewer per row, two places per row (three at most), about ten speaking characters and six
    places for the season;
  - each secret goes teased, partial, revealed in that order, and is revealed once.
Standard library only. Exit code 1 when any ERROR is found.
"""
import argparse
import json
import re
import sys

TYPES = {"reveal", "arrival", "evidence", "threat", "danger", "decision", "betrayal", "exposure", "interruption",
         "withheld-answer", "power-entrance", "strike", "countdown", "contradiction-clue", "mistaken-identity", "return",
         "pregnancy", "overheard", "call", "power-flash", "question-line", "offer", "villain-wins", "reframe", "vanish",
         "transformation", "cut-off", "impossible-fact", "trap"}
STAGES = ["teased", "partial", "revealed"]


def norm(h):
    h = h.strip().lower()
    h = re.sub(r"\(.*?\)", "", h).strip()
    if h in ("ep", "ep.", "episode", "#", "no", "no."):
        return "ep"
    for key, words in [("cliff_type", ["cliffhanger type", "cliff type", "type"]),
                       ("cliff_beat", ["cliffhanger beat", "cliff beat", "final beat"]),
                       ("cliff", ["cliffhanger", "cliff"]), ("spring", ["spring"]), ("open", ["open"]),
                       ("hook", ["hook"]), ("reversal", ["reversal", "turn", "twist"]), ("payoff", ["payoff"]),
                       ("cast", ["cast", "characters"]), ("places", ["places", "locations", "place"]),
                       ("rung", ["rung", "villain"]), ("secrets", ["secrets", "secret"]), ("pay", ["pay"]),
                       ("title", ["title"])]:
        if any(h == w or h.startswith(w) for w in words):
            return key
    return h


def parse_table(text):
    lines = text.split("\n")
    for i, line in enumerate(lines):
        if not line.strip().startswith("|"):
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        keys = [norm(c) for c in cells]
        if "ep" not in keys or i + 1 >= len(lines) or not re.match(r"^\s*\|?\s*:?-{2,}", lines[i + 1]):
            continue
        rows = []
        for raw in lines[i + 2:]:
            if not raw.strip().startswith("|"):
                break
            vals = [c.strip() for c in raw.strip().strip("|").split("|")]
            vals += [""] * (len(keys) - len(vals))
            row = dict(zip(keys, vals))
            m = re.match(r"^\D*(\d+)", row.get("ep", ""))
            if not m:
                continue
            row["ep_n"] = int(m.group(1))
            rows.append(row)
        return keys, rows
    return None, []


def split_list(v):
    v = re.sub(r"<[^>]*>", "", v or "")
    return [x.strip() for x in re.split(r"[,;/]| and ", v) if x.strip() and x.strip() not in ("-", "—")]


def main(argv=None):
    ap = argparse.ArgumentParser(description="Check a micro drama season grid.")
    ap.add_argument("grid", help="the grid Markdown file")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args(argv)
    text = open(args.grid, encoding="utf-8").read()
    keys, rows = parse_table(text)
    issues = []

    def add(level, msg):
        issues.append({"level": level, "msg": msg})

    if not rows:
        add("ERROR", "No grid table found: it needs a header row with an Ep column and one row per episode.")
        return report(args, rows, issues)
    rows = [r for r in rows if any(v and not v.startswith("<") for k, v in r.items() if k not in ("ep", "ep_n"))]
    if not rows:
        add("ERROR", "The grid has no filled rows yet.")
        return report(args, rows, issues)
    nums = [r["ep_n"] for r in rows]
    if nums != list(range(nums[0], nums[0] + len(nums))):
        add("WARN", "Episode numbers are not consecutive: %s" % nums)

    types = []
    for r in rows:
        ep = r["ep_n"]
        ctype = (r.get("cliff_type") or "").strip().lower()
        beat = r.get("cliff_beat", "")
        if not ctype and r.get("cliff"):
            m = re.match(r"^\s*([A-Za-z][A-Za-z -]*?)\s*:\s*(.*)$", r["cliff"])
            ctype, beat = (m.group(1).lower(), m.group(2)) if m else ("", r["cliff"])
        ctype = "" if ctype.startswith("<") else re.sub(r"\s+", "-", ctype)
        types.append(ctype)
        for k, label in (("hook", "hook"), ("reversal", "reversal"), ("payoff", "payoff")):
            if k in keys and not r.get(k):
                add("ERROR", "Ep %d has no %s." % (ep, label))
        if not ctype and not beat:
            add("ERROR", "Ep %d has no cliffhanger." % ep)
        elif ctype and ctype not in TYPES:
            add("TIP", "Ep %d: cliffhanger type '%s' is not in the library (references/cliffhangers.md)." % (ep, ctype))
        cast = split_list(r.get("cast", ""))
        finale = ep >= rows[-1]["ep_n"] - 1 and len(rows) >= 10
        if len(cast) > 4:
            add("TIP" if finale else "WARN", "Ep %d has %d cast members (%s). Four is about the most a 90 second episode holds%s."
                % (ep, len(cast), ", ".join(cast), "; in a finale, keep most of them silent witnesses" if finale else ""))
        places = split_list(r.get("places", ""))
        if len(places) > 3:
            add("WARN", "Ep %d uses %d places. One or two per episode, a third only as a short insert." % (ep, len(places)))
        elif len(places) == 3:
            add("TIP", "Ep %d uses 3 places: keep the third to a short insert." % ep)

    for a in range(1, len(types)):
        if types[a] and types[a] == types[a - 1]:
            add("WARN", "Ep %d and %d both end on '%s'. Alternate the type." % (rows[a - 1]["ep_n"], rows[a]["ep_n"], types[a]))
    named = [t for t in types if t]
    if len(named) >= 6:
        for t in sorted(set(named)):
            if named.count(t) / len(named) > 0.34:
                add("WARN", "'%s' ends %d of %d episodes; mix in other types." % (t, named.count(t), len(named)))

    springs = [(r.get("spring") or "").strip().upper() for r in rows]
    if "spring" in keys:
        run = 0
        for r, sp in zip(rows, springs):
            if sp not in ("COMPRESS", "RELEASE"):
                add("TIP", "Ep %d: Spring should be COMPRESS or RELEASE." % r["ep_n"])
                continue
            run = run + 1 if sp == "COMPRESS" else 0
            if run == 3:
                add("WARN", "Ep %d is the third COMPRESS episode in a row: give the audience a release." % r["ep_n"])
        if len(springs) >= 3 and all(s == "COMPRESS" for s in springs[:3]):
            add("WARN", "Episodes 1 to 3 are all COMPRESS: the first payoff should land by episode 3.")

    pays = [r for r in rows if "PAYWALL" in (r.get("pay") or "").upper()]
    total = len(rows)
    if total >= 20 and not pays and "pay" in keys:
        add("TIP", "No PAYWALL row. For an app release mark the last free episode (usually 8 to 12).")
    for r in pays:
        if not 8 <= r["ep_n"] <= 12:
            add("TIP", "The PAYWALL is at episode %d; apps usually put it between 8 and 12." % r["ep_n"])
    if len(pays) > 1:
        add("WARN", "%d rows are marked PAYWALL; mark the first pay point PAYWALL and later ones HOOK." % len(pays))

    all_cast, all_places = [], []
    for r in rows:
        for c in split_list(r.get("cast", "")):
            if c.lower() not in [x.lower() for x in all_cast]:
                all_cast.append(c)
        for p in split_list(r.get("places", "")):
            if p.lower() not in [x.lower() for x in all_places]:
                all_places.append(p)
    if len(all_cast) > 10:
        add("WARN", "%d named characters across the season (%s). Six to ten keeps faces clear and production cheap."
            % (len(all_cast), ", ".join(all_cast)))
    if len(all_places) > 6:
        add("WARN", "%d places across the season. Three to six recurring sets is the sweet spot." % len(all_places))

    stage_of = {}
    for r in rows:
        for part in re.split(r"[;,]", r.get("secrets", "") or ""):
            m = re.match(r"^\s*(.+?)\s*:\s*(teased|partial|revealed)\b", part.strip(), re.I)
            if not m:
                continue
            name, stage = m.group(1).strip().lower(), m.group(2).lower()
            seen = stage_of.setdefault(name, [])
            if stage == "revealed" and "revealed" in [s for s, _ in seen]:
                add("WARN", "Secret '%s' is revealed twice (episodes %s and %d)."
                    % (name, [e for s, e in seen if s == "revealed"][0], r["ep_n"]))
            if seen and STAGES.index(stage) < STAGES.index(seen[-1][0]):
                add("TIP", "Secret '%s' goes back from %s to %s at episode %d." % (name, seen[-1][0], stage, r["ep_n"]))
            seen.append((stage, r["ep_n"]))
    return report(args, rows, issues, types=types, springs=springs, cast=all_cast, places=all_places)


def report(args, rows, issues, types=None, springs=None, cast=None, places=None):
    errors = sum(1 for i in issues if i["level"] == "ERROR")
    if args.json:
        print(json.dumps({"episodes": len(rows), "cliffhanger_types": types or [], "springs": springs or [],
                          "cast": cast or [], "places": places or [], "issues": issues, "errors": errors}, indent=2))
        return 1 if errors else 0
    print("%d episode row(s)." % len(rows))
    if types:
        print("Cliffhanger types: %s" % ", ".join(t or "?" for t in types))
    if springs and any(springs):
        print("Spring: %s" % " ".join({"COMPRESS": "C", "RELEASE": "R"}.get(s, "?") for s in springs))
    if cast:
        print("Cast (%d): %s" % (len(cast), ", ".join(cast)))
    if places:
        print("Places (%d): %s" % (len(places), ", ".join(places)))
    if not issues:
        print("OK: no issues found.")
    for i in issues:
        print("  %-5s %s" % (i["level"], i["msg"]))
    print("%d error(s)." % errors)
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
