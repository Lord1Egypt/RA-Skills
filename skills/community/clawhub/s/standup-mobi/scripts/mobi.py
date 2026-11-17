#!/usr/bin/env python3
"""mobi.py — absence coverage planner: duty inventory, owner solver,
tribal-knowledge extraction checklist, graded ramp plans, paper checklists.

Subcommands:
  init      create team.json + duties.json (example data)
  duty      add a duty interactively via flags
  solve     assign owners under capacity + 1.5x fairness cap
  extract   12-question knowledge-extraction checklist for tribal duties
  ramp      graded watch->shadow->assist->solo plan for an owner
  checklist printable daily/weekly checklist for a substitute

Stdlib only. State lives in --dir (default ./cover).
"""
import argparse
import json
import sys
from pathlib import Path

RISK_W = {"high": 3, "med": 2, "low": 1}
CADENCE_PER_WEEK = {"daily": 7, "weekly": 1, "monthly": 0.25, "adhoc": 0.3}


def load(path, default):
    p = Path(path)
    if p.exists():
        return json.loads(p.read_text())
    return default


def save(path, data):
    Path(path).write_text(json.dumps(data, indent=2) + "\n")


def wmin(m):
    return "~%d min/week" % round(m)


# ---------------------------------------------------------------- init

TEAM_EX = [
    {"name": "jordan", "capacity_min_per_day": 240, "skills": ["ops", "linux", "deploy"]},
    {"name": "sam", "capacity_min_per_day": 300, "skills": ["finance", "reporting"]},
    {"name": "kim", "capacity_min_per_day": 180, "skills": ["ops", "support"]},
]

DUTIES_EX = [
    {"name": "morning deploy check", "cadence": "daily", "skill": "ops",
     "minutes": 15, "tribal": False, "risk": "med",
     "notes": "dashboard green + rollback if red"},
    {"name": "invoicing run", "cadence": "weekly", "skill": "finance",
     "minutes": 45, "tribal": True, "risk": "high",
     "notes": "Xero + spreadsheet recon; supplier codes in Alex's head"},
    {"name": "weekly metrics report", "cadence": "weekly", "skill": "reporting",
     "minutes": 60, "tribal": False, "risk": "med",
     "notes": "pull from BI, paste template, email list"},
    {"name": "support inbox triage", "cadence": "daily", "skill": "support",
     "minutes": 30, "tribal": False, "risk": "med",
     "notes": "first-response SLA 4h"},
    {"name": "SSL cert renewal check", "cadence": "monthly", "skill": "ops",
     "minutes": 10, "tribal": True, "risk": "high",
     "notes": "expires in 3 weeks! renewal flow undocumented"},
    {"name": "partner file drop", "cadence": "weekly", "skill": "ops",
     "minutes": 20, "tribal": True, "risk": "med",
     "notes": "sftp upload; only Alex knows the folder naming"},
]


def cmd_init(args):
    d = Path(args.dir)
    d.mkdir(parents=True, exist_ok=True)
    save(d / "team.json", TEAM_EX)
    save(d / "duties.json", DUTIES_EX)
    print("Initialized %s" % d.resolve())
    print("  team.json   — who's available (edit capacities/skills)")
    print("  duties.json — the absentee's duties (add yours)")
    print("Then: python3 %s solve --dir %s" % (sys.argv[0], args.dir))
    return 0


# ---------------------------------------------------------------- duty

def cmd_duty(args):
    d = Path(args.dir)
    duties = load(d / "duties.json", [])
    duties.append({
        "name": args.name,
        "cadence": args.cadence,
        "skill": args.skill,
        "minutes": args.minutes,
        "tribal": args.tribal,
        "risk": args.risk,
        "notes": args.notes or "",
    })
    save(d / "duties.json", duties)
    tribal = " [TRIBAL]" if args.tribal else ""
    print("Added duty: %s (%s, %s, %d min, risk=%s)%s"
          % (args.name, args.cadence, args.skill, args.minutes, args.risk, tribal))
    return 0


# ---------------------------------------------------------------- solve

def weekly_minutes(duty):
    per_occurrence = duty["minutes"]
    return per_occurrence * CADENCE_PER_WEEK.get(duty.get("cadence", "adhoc"), 0.3)


def cmd_solve(args):
    d = Path(args.dir)
    team = load(d / "team.json", [])
    duties = load(d / "duties.json", [])
    if not team or not duties:
        print("Missing team.json or duties.json — run init first.")
        return 2

    people = {m["name"]: {"member": m, "load": 0.0, "duties": []} for m in team}
    total = sum(weekly_minutes(x) for x in duties)
    cap_avg = 1.5 * (total / len(people)) if people else 0

    ranked = sorted(duties, key=lambda x: -(RISK_W.get(x.get("risk", "med"), 2) * weekly_minutes(x)))
    uncovered = []

    for duty in ranked:
        wmin_d = weekly_minutes(duty)
        skill = duty.get("skill", "")
        # eligible: has the skill, or duty is low-risk and small
        eligible = [p for p in people.values()
                    if skill in p["member"].get("skills", [])
                    or (duty.get("risk") == "low" and wmin_d <= 30)]
        if not eligible:
            uncovered.append((duty, "no skill match on team"))
            continue
        # pick most remaining capacity among eligible
        def spare(p):
            cap_day = p["member"].get("capacity_min_per_day", 240)
            # convert weekly duty load to per-day share vs weekly capacity
            return cap_day * 5 - p["load"]
        pick = min(eligible, key=lambda p: p["load"] / max(spare(p), 1e-9))
        if pick["load"] + wmin_d > max(spare(pick), 0) or pick["load"] + wmin_d > cap_avg:
            uncovered.append((duty, "would overload %s past cap" % pick["member"]["name"]))
            continue
        pick["load"] += wmin_d
        pick["duties"].append(duty)

    print("== COVERAGE PLAN (added load, min/week) ==\n")
    grand = 0.0
    for name, p in sorted(people.items()):
        cap_day = p["member"].get("coverage_cap", p["member"].get("capacity_min_per_day", 240))
        print("%-10s +%d min/wk  (%d duties)" % (name, round(p["load"]), len(p["duties"])))
        for duty in p["duties"]:
            tribal = "  [TRIBAL]" if duty.get("tribal") else ""
            print("   - %s (%s, %d min, risk=%s)%s" %
                  (duty["name"], duty.get("cadence"), duty["minutes"], duty.get("risk"), tribal))
        grand += p["load"]
    print("\nTotal coverage load: %d min/week across %d people" % (round(grand), len(people)))
    if uncovered:
        print("\n== UNCOVERED (plan holes — decide explicitly) ==")
        for duty, why in uncovered:
            print("  ! %s — %s" % (duty["name"], why))
    else:
        print("\nAll duties covered; no fairness-cap violations.")
    tribal_n = sum(1 for x in duties if x.get("tribal"))
    print("Tribal duties: %d/%d — run 'extract' before the absence starts." % (tribal_n, len(duties)))
    return 0


# ---------------------------------------------------------------- extract

QUESTIONS = [
    "What do you do that nobody else on the team could do today?",
    "Walk me through <duty> end to end — where do you click first?",
    "What credentials/access does it need? (name the system + vault entry only — never write secrets in notes)",
    "What usually goes wrong, and how do you fix it?",
    "What looks scary but is actually safe to ignore?",
    "What looks harmless but must NEVER be touched?",
    "Who do you contact when stuck (name + channel)?",
    "If you had 15 minutes to write a runbook for this, what would page one say?",
    "What can be skipped entirely for one week with zero damage?",
    "What has a hard deadline in the next 14 days, and what's the penalty for missing it?",
    "Where are the files this needs? (for keys/credentials: vault entry name only)",
    "What question should I have asked that I didn't?",
]

RUNBOOK_TMPL = """# Runbook: {name}

Cadence: {cadence} | minutes: {minutes} | risk: {risk}

> SECURITY: never write passwords, keys, or tokens here. Reference the
> vault/secret-manager entry by name only. Runbooks get shared — treat
> them as public.

## Steps (from interview)
1.
2.
3.

## Credentials / access needed
- (system + vault entry name only — no secrets)

## If it breaks
-

## STOP — ask before touching
-

## Can be skipped for one week?
[ ] yes  [ ] no — why:
"""


def cmd_extract(args):
    d = Path(args.dir)
    duties = load(d / "duties.json", [])
    tribal = [x for x in duties if x.get("tribal")]
    if not tribal:
        print("No tribal duties flagged. Set \"tribal\": true on duties without runbooks.")
        return 0
    print("== KNOWLEDGE EXTRACTION — %d tribal dut%s ==\n" % (len(tribal), "y" if len(tribal) == 1 else "ies"))
    print("Run one 15-min session per duty. You ask, you write. Never assign the absentee homework.\n")
    for i, q in enumerate(QUESTIONS, 1):
        print("%2d. %s" % (i, q))
    outdir = d / "runbooks"
    outdir.mkdir(exist_ok=True)
    for duty in tribal:
        f = outdir / ("%s.md" % duty["name"].lower().replace(" ", "-").replace("/", "-"))
        f.write_text(RUNBOOK_TMPL.format(**{**duty, **{"cadence": duty.get("cadence", ""), "minutes": duty.get("minutes", ""), "risk": duty.get("risk", "")}}))
        print("  runbook seed -> %s" % f)
    print("\nAfter each session: fill the runbook, set \"tribal\": false in duties.json.")
    return 0


# ---------------------------------------------------------------- ramp

RAMP_LEVELS = [
    ("Day 1 — WATCH", "Observe %s doing the duty (live or recording); read the runbook end to end.",
     "Any step not in the runbook"),
    ("Day 2 — SHADOW", "Do the duty alongside %s; your hands, their call on each step.",
     "Any divergence from the runbook"),
    ("Day 3 — ASSIST", "You do it; %s reviews the result before it counts as done.",
     "Output looks different from usual"),
    ("Day 4 — SOLO", "You do it alone; log any deviation in the runbook.",
     "Anything the runbook marks STOP"),
    ("Day 5 — AUDIT", "%s (or the lead) reviews the week's deviations; patch the runbook.",
     "More than 2 deviations in one run"),
]

RAMP_HEADER = """# Ramp plan: {owner} covering {absentee}

One level per duty per day. Do not skip levels on high-risk duties.
Buddy: {absentee} (or the duty's usual receiver if unreachable).
"""


def cmd_ramp(args):
    d = Path(args.dir)
    duties = load(d / "duties.json", [])
    team = load(d / "team.json", [])
    # duties assigned to owner: we don't persist solve output; select by skill match + risk
    skills = set()
    for m in team:
        if m["name"] == args.owner:
            skills = set(m.get("skills", []))
    mine = [x for x in duties if x.get("skill") in skills or x.get("risk") == "low"]
    if args.only:
        mine = [x for x in duties if x["name"] == args.only]
    if not mine:
        print("No duties match owner '%s' (skills=%s). Use --only <duty>." % (args.owner, sorted(skills) or None))
        return 1
    hdr = RAMP_HEADER.format(owner=args.owner, absentee=args.absentee)
    print(hdr)
    byday = {}
    for duty in mine:
        for lvl, act, stop in RAMP_LEVELS:
            byday.setdefault(lvl, []).append((duty, act, stop))
    for lvl, act, stop in RAMP_LEVELS:
        print("== %s ==" % lvl)
        for duty, a, s in byday.get(lvl, []):
            print("  * %s: %s" % (duty["name"], a.replace("%s", args.absentee)))
            print("      STOP-AND-ASK: %s" % s)
        print()
    return 0


# ---------------------------------------------------------------- checklist

def cmd_checklist(args):
    d = Path(args.dir)
    duties = load(d / "duties.json", [])
    team = load(d / "team.json", [])
    skills = set()
    for m in team:
        if m["name"] == args.owner:
            skills = set(m.get("skills", []))
    mine = [x for x in duties if x.get("skill") in skills or x.get("risk") == "low"]
    if args.only:
        mine = [x for x in duties if x["name"] == args.only]
    if not mine:
        print("No duties match owner '%s'. Use --only <duty> or fix skills in team.json." % args.owner)
        return 1

    lines = ["# Coverage checklist — %s" % args.owner, ""]
    lines += ["Grouped by cadence. Tape next to the monitor. Mark [x] when DONE.", ""]
    for cadence in ["daily", "weekly", "monthly", "adhoc"]:
        grp = [x for x in mine if x.get("cadence") == cadence]
        if not grp:
            continue
        lines.append("## %s" % cadence.upper())
        for duty in grp:
            lines.append("- [ ] %s (%d min, risk=%s)%s" %
                         (duty["name"], duty["minutes"], duty.get("risk"),
                          " — TRIBAL, read runbook first" if duty.get("tribal") else ""))
            if duty.get("notes"):
                lines.append("      %s" % duty["notes"])
        lines.append("")
    lines += ["Stop-and-ask: anything marked STOP in a runbook; anything the runbook doesn't cover.", ""]
    if args.out:
        Path(args.out).write_text("\n".join(lines) + "\n")
        print("Wrote %d-duty checklist -> %s" % (len(mine), args.out))
    else:
        print("\n".join(lines))
    return 0


# ---------------------------------------------------------------- main

def main():
    ap = argparse.ArgumentParser(
        description="Absence coverage planner: init, duty, solve, extract, ramp, checklist.")
    sub = ap.add_subparsers(dest="cmd", required=True)

    i = sub.add_parser("init", help="create team.json + duties.json")
    i.add_argument("--dir", default="cover")
    i.set_defaults(func=cmd_init)

    du = sub.add_parser("duty", help="add a duty")
    du.add_argument("--dir", default="cover")
    du.add_argument("--name", required=True)
    du.add_argument("--cadence", default="weekly",
                    choices=["daily", "weekly", "monthly", "adhoc"])
    du.add_argument("--skill", default="ops")
    du.add_argument("--minutes", type=int, default=15)
    du.add_argument("--risk", default="med", choices=["low", "med", "high"])
    du.add_argument("--tribal", action="store_true")
    du.add_argument("--notes", default="")
    du.set_defaults(func=cmd_duty)

    s = sub.add_parser("solve", help="assign owners under constraints")
    s.add_argument("--dir", default="cover")
    s.set_defaults(func=cmd_solve)

    e = sub.add_parser("extract", help="tribal-knowledge extraction kit")
    e.add_argument("--dir", default="cover")
    e.set_defaults(func=cmd_extract)

    r = sub.add_parser("ramp", help="graded ramp plan for an owner")
    r.add_argument("--dir", default="cover")
    r.add_argument("--owner", required=True)
    r.add_argument("--absentee", default="the absentee")
    r.add_argument("--only", help="limit to one duty name")
    r.set_defaults(func=cmd_ramp)

    c = sub.add_parser("checklist", help="printable substitute checklist")
    c.add_argument("--dir", default="cover")
    c.add_argument("--owner", required=True)
    c.add_argument("--only", help="limit to one duty name")
    c.add_argument("--out", help="write to file instead of stdout")
    c.set_defaults(func=cmd_checklist)

    args = ap.parse_args()
    return args.func(args)


if __name__ == "__main__":
    try:
        sys.exit(main())
    except BrokenPipeError:
        sys.exit(0)
