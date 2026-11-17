#!/usr/bin/env python3
"""sleep-shift-survivor — circadian planner for shift workers.

Rotation patterns (2D,2E,2N,4off) -> dated sleep plans with anchor sleep,
per-block main windows, strategic naps, caffeine cutoffs, light/dark
choreography, transition sequences, drowsy-drive commute cards, and
shift-work-disorder screening flags from sleep logs. 100% local, stdlib.

Informational planning only — persistent symptoms belong with occupational
health or sleep medicine, not with software.
"""
import argparse
import json
import sys
from datetime import date, datetime, timedelta
from pathlib import Path

DB = Path("shift_sleep.json")
ANCHOR = ("04:00", "08:00")          # default anchor window
CAFFEINE_BUFFER_H = 6.0              # half-life clearance before sleep
NAP_BEFORE_FIRST_NIGHT_MIN = 90
DRIVE_MIN_SLEEP_H = 4.0


def load() -> dict:
    if DB.exists():
        return json.loads(DB.read_text())
    return {"schedules": {}, "logs": {}}


def save(db: dict) -> None:
    DB.write_text(json.dumps(db, indent=2, ensure_ascii=False))


def hm(s: str):
    return datetime.strptime(s, "%H:%M").time()


def add_min(t: datetime.time, minutes: int):
    base = datetime(2000, 1, 1, t.hour, t.minute) + timedelta(minutes=minutes)
    return base.time()


def fmt(t) -> str:
    return t.strftime("%H:%M") if t else "?"


def span_h(start, end) -> float:
    """Length of a shift window possibly crossing midnight."""
    s = start.hour * 60 + start.minute
    e = end.hour * 60 + end.minute
    if e <= s:
        e += 24 * 60
    return (e - s) / 60.0


# ---------- schedules ----------

def parse_pattern(p: str):
    """'2D,2E,2N,4off' -> ['D','D','E','E','N','N','off','off','off','off']"""
    out = []
    for part in p.split(","):
        part = part.strip()
        count = int("".join(ch for ch in part if ch.isdigit()) or 1)
        kind = "".join(ch for ch in part if ch.isalpha())
        out.extend([kind] * count)
    if not out:
        sys.exit("pattern empty")
    return out


def cmd_schedule(args, db):
    if args.action == "add":
        shifts = {
            "D": (args.day.split("-")[0], args.day.split("-")[1]),
            "E": (args.evening.split("-")[0], args.evening.split("-")[1]),
            "N": (args.night.split("-")[0], args.night.split("-")[1]),
        }
        db["schedules"][args.name] = {
            "pattern": args.pattern,
            "shifts": shifts,
            "anchor": list(ANCHOR),
            "added": date.today().isoformat(),
        }
        save(db)
        cyc = "".join(parse_pattern(args.pattern))
        print(f"added '{args.name}': {args.pattern} ({len(parse_pattern(args.pattern))}-day cycle)")
        print(f"shifts: D {args.day} | E {args.evening} | N {args.night}")
        print(f"anchor sleep window: {ANCHOR[0]}-{ANCHOR[1]} (present in every block)")
        fast = all(parse_pattern(args.pattern).count(k) <= 3
                   for k in "DEN" if parse_pattern(args.pattern).count(k))
        if "N" in cyc and parse_pattern(args.pattern).count("N") <= 3:
            print("rotation is FAST (night blocks ≤3 days) — anchor strategy, do not fully adapt")
    elif args.action == "list":
        for name, s in db["schedules"].items():
            print(f"{name:<16} {s['pattern']:<14} anchor {s['anchor'][0]}-{s['anchor'][1]}")


def block_seq(sched: dict, start_index: int = 0):
    return parse_pattern(sched["pattern"])[start_index:] + parse_pattern(sched["pattern"])[:start_index]


# ---------- plan ----------

def day_plan(kind: str, sched: dict, is_first_night: bool, prev_kind: str) -> list:
    """Return instruction lines for one roster day of block kind."""
    shifts = sched["shifts"]
    lines = []
    a0, a1 = sched["anchor"]
    if kind == "off":
        lines.append("OFF — protect anchor sleep "
                     f"{a0}-{a1}; normal night sleep if recovered")
        if prev_kind == "N":
            lines.append("  transition: if ≥48h off → hard reset tonight "
                         "(stay up to normal bedtime, no late nap)")
        return lines
    if kind not in shifts:
        return [f"unknown block '{kind}' — treat as off"]
    s, e = shifts[kind]
    start, end = hm(s), hm(e)
    caffe_cutoff = add_min(end, -int((span_h(start, end)) * 0))  # placeholder
    # caffeine cutoff: 6h before intended sleep attempt
    if kind == "N":
        sleep_attempt = add_min(end, 90 // 60 + 30)  # ~1.5h after shift end
        cutoff = add_min(sleep_attempt, -int(CAFFEINE_BUFFER_H * 60))
        lines.append(f"NIGHT {s}-{e}: main sleep after shift "
                     f"({fmt(add_min(end, 60))}-{fmt(add_min(end, 60+7*60))} target)")
        lines.append(f"  anchor window {a0}-{a1}: overlap it — keep at least "
                     f"the anchor if sleep is short")
        lines.append("  BRIGHT light first half of shift; dim last 2h")
        lines.append("  DARK sunglasses on the morning commute home")
        lines.append(f"  caffeine cutoff {fmt(cutoff)} "
                     f"(clears before {fmt(sleep_attempt)} sleep attempt)")
        if is_first_night:
            lines.append(f"  prophylactic nap {NAP_BEFORE_FIRST_NIGHT_MIN} min "
                         f"before shift (alarm!)")
        lines.append("  ⚠ DROWSY-DRIVE RISK on morning commute — see `commute` card")
    elif kind == "E":
        sleep_attempt = add_min(end, 90)  # wind-down after evening shift
        cutoff = add_min(sleep_attempt, -int(CAFFEINE_BUFFER_H * 60))
        lines.append(f"EVENING {s}-{e}: sleep {fmt(add_min(end, 60))}-"
                     f"{fmt(add_min(end, 60+8*60))}")
        lines.append(f"  anchor window {a0}-{a1} sits inside this sleep — good")
        lines.append(f"  caffeine cutoff {fmt(cutoff)}")
    else:  # D
        cutoff = hm("21:00")
        lines.append(f"DAY {s}-{e}: normal night sleep 22:30-06:30 "
                     f"(anchor tail {a0}-{a1} optional)")
        lines.append(f"  caffeine cutoff {fmt(cutoff)} (evening clearance)")
        lines.append("  daylight exposure morning/midday keeps the clock day-oriented")
    return lines


def cmd_plan(args, db):
    if args.name not in db["schedules"]:
        sys.exit(f"schedule '{args.name}' not found")
    sched = db["schedules"][args.name]
    seq = block_seq(sched)
    d0 = datetime.strptime(args.from_date, "%Y-%m-%d").date()
    prev = None
    nights_seen = 0
    print(f"PLAN — {args.name} ({sched['pattern']}), {args.days} days from {d0}\n")
    for i in range(args.days):
        kind = seq[i % len(seq)]
        first_night = kind == "N" and prev != "N"
        dd = d0 + timedelta(days=i)
        print(f"{dd} [{kind}]")
        for line in day_plan(kind, sched, first_night, prev or "off"):
            print(f"   {line}")
        if prev and prev != kind and {prev, kind} == {"N", "D"}:
            print("   TRANSITION: night↔day block change — see reset note")
        prev = kind
    print("\nremember: fast rotation = anchor strategy (do not fully adapt); "
          "slow rotation = adapt per block, delay forward only")


# ---------- commute ----------

def cmd_commute(args, db):
    end = hm(args.night_ends)
    print("DROWSY-DRIVE RISK CARD — post-night-shift morning commute\n")
    print(f"shift ends {fmt(end)}")
    print("1. Sleep < 4h in last 24h OR any microsleep episode → DO NOT DRIVE.")
    print("   20-min car nap + transit/ride alternatives first.")
    print("2. Otherwise: 20-min nap + coffee 30 min before departure.")
    print("3. Dark sunglasses NOW (morning light resets the clock the wrong way).")
    print("4. Cool cabin, talking passenger, no monotone highway cruise.")
    print("5. Any eye-lid heaviness / missing mile markers → pull over immediately.")
    print("\nmicrosleeps are not survivable by willpower. The 20-minute nap is.")


# ---------- log / screen / report ----------

def cmd_log(args, db):
    sch = db["logs"].setdefault(args.name, [])
    sch.append({"date": args.date, "slept": args.slept,
                "quality": args.quality, "note": args.note or ""})
    save(db)
    print(f"logged {args.date}: slept {args.slept}, quality {args.quality}/5")


def sleep_hours(slept: str) -> float:
    try:
        a, b = slept.split("-")
        return span_h(hm(a.strip()), hm(b.strip()))
    except Exception:
        return 0.0


def cmd_screen(args, db):
    logs = db["logs"].get(args.name, [])
    if len(logs) < 14:
        print(f"screening needs ≥14 logged days (have {len(logs)}) — keep logging")
        return
    hrs = [sleep_hours(l["slept"]) for l in logs]
    q = [l["quality"] for l in logs]
    short_nights = sum(1 for h in hrs if h < 6)
    low_q = sum(1 for x in q if x <= 2)
    print(f"SCREEN — {args.name} ({len(logs)} days logged)")
    print(f"  mean sleep {sum(hrs)/len(hrs):.1f}h; nights <6h: {short_nights}; "
          f"quality ≤2: {low_q}")
    flags = []
    if short_nights >= len(logs) * 0.3:
        flags.append("≥30% of nights under 6h")
    if low_q >= len(logs) * 0.3:
        flags.append("≥30% of nights quality ≤2/5")
    if flags:
        print("\n⚠ shift-work-disorder FLAGS (informational, not diagnostic):")
        for f in flags:
            print(f"  • {f}")
        print("  persistent symptoms ≥3 months → occupational health / sleep medicine")
    else:
        print("\nno screening flags — distribution looks tolerable; keep logging")


def cmd_report(args, db):
    sched = db["schedules"].get(args.name)
    logs = db["logs"].get(args.name, [])
    print(f"REPORT — {args.name}")
    if sched:
        print(f"  pattern {sched['pattern']}, anchor {sched['anchor'][0]}-"
              f"{sched['anchor'][1]}")
    if not logs:
        print("  no sleep logs yet — `log` to start")
        return
    hrs = [sleep_hours(l["slept"]) for l in logs]
    anchor0, anchor1 = sched["anchor"] if sched else ANCHOR
    anchor_ok = 0
    for l in logs:
        try:
            a, b = l["slept"].split("-")
            # crude overlap check with anchor window
            s, e = hm(a.strip()), hm(b.strip())
            a0, a1 = hm(anchor0), hm(anchor1)
            late_night_overlap = s <= a0 and span_h(s, e) >= 6
            morning_overlap = not (e < a0 or s > a1)
            if morning_overlap or late_night_overlap:
                anchor_ok += 1
        except Exception:
            pass
    print(f"  logged {len(logs)} days; mean {sum(hrs)/len(hrs):.1f}h; "
          f"anchor-adjacent sleeps {anchor_ok}/{len(logs)}")
    debt = sum(max(0, 7 - h) for h in hrs)
    print(f"  cumulative debt vs 7h: {debt:.1f}h over the log window")


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("schedule")
    ss = p.add_subparsers(dest="action", required=True)
    pa = ss.add_parser("add")
    pa.add_argument("name"); pa.add_argument("--pattern", required=True)
    pa.add_argument("--day", default="07:00-15:00")
    pa.add_argument("--evening", default="15:00-23:00")
    pa.add_argument("--night", default="23:00-07:00")
    ss.add_parser("list")

    p = sub.add_parser("plan")
    p.add_argument("name")
    p.add_argument("--from", dest="from_date", default=date.today().isoformat())
    p.add_argument("--days", type=int, default=14)

    p = sub.add_parser("commute")
    p.add_argument("--night-ends", dest="night_ends", default="07:00")

    p = sub.add_parser("log")
    p.add_argument("name"); p.add_argument("--date", default=date.today().isoformat())
    p.add_argument("--slept", required=True, help="e.g. 08:30-14:00")
    p.add_argument("--quality", type=int, default=3, help="1-5")
    p.add_argument("--note")

    p = sub.add_parser("screen"); p.add_argument("name")
    p = sub.add_parser("report"); p.add_argument("name")

    args = ap.parse_args()
    db = load()

    if args.cmd == "schedule":
        cmd_schedule(args, db)
    elif args.cmd == "plan":
        cmd_plan(args, db)
    elif args.cmd == "commute":
        cmd_commute(args, db)
    elif args.cmd == "log":
        cmd_log(args, db)
    elif args.cmd == "screen":
        cmd_screen(args, db)
    elif args.cmd == "report":
        cmd_report(args, db)


if __name__ == "__main__":
    main()
