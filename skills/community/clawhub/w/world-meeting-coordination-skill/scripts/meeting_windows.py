#!/usr/bin/env python3
import argparse
import json
from dataclasses import dataclass
from datetime import datetime, timedelta
from pathlib import Path
from zoneinfo import ZoneInfo

CONFIG_PATH = Path.home() / ".openclaw" / "skills" / "world-meeting-coordination-skill" / "config.json"


@dataclass
class Participant:
    name: str
    tz: ZoneInfo


def load_config():
    if CONFIG_PATH.exists():
        return json.loads(CONFIG_PATH.read_text())
    return {}


def save_config(cfg: dict):
    CONFIG_PATH.parent.mkdir(parents=True, exist_ok=True)
    CONFIG_PATH.write_text(json.dumps(cfg, indent=2))


def run_onboarding_interactive():
    print("First-time setup for World Meeting Coordination Skill")
    tz = input("1) Your timezone (e.g. America/Chicago): ").strip() or "America/Chicago"
    hours = input('2) Preferred meeting hours (e.g. 09:00-17:00): ').strip() or "09:00-17:00"
    flex = input("3) Flexibility [strict|balanced|flexible] (default balanced): ").strip().lower() or "balanced"
    if flex not in {"strict", "balanced", "flexible"}:
        flex = "balanced"
    cfg = {"me": {"timezone": tz, "working_hours": hours, "flexibility": flex}}
    save_config(cfg)
    return cfg


def parse_zones(raw: str):
    out = []
    for part in raw.split(","):
        name, tz = part.split("=", 1)
        out.append(Participant(name.strip(), ZoneInfo(tz.strip())))
    return out


def parse_hhmm(s: str) -> int:
    h, m = s.split(":", 1)
    return int(h) * 60 + int(m)


def parse_hours_range(rng: str):
    a, b = rng.split("-", 1)
    return parse_hhmm(a.strip()), parse_hhmm(b.strip())


def parse_hours_map(raw: str | None):
    out = {}
    if not raw:
        return out
    for part in raw.split(","):
        if not part.strip():
            continue
        name, rng = part.split("=", 1)
        out[name.strip()] = parse_hours_range(rng.strip())
    return out


def in_range(minutes: int, start: int, end: int) -> bool:
    return start <= minutes < end


def penalty(local_dt: datetime, pref_start: int, pref_end: int, flexibility: str) -> int:
    mins = local_dt.hour * 60 + local_dt.minute
    if in_range(mins, pref_start, pref_end):
        return 0

    d = min(abs(mins - pref_start), abs(mins - pref_end))

    if flexibility == "strict":
        if d <= 30:
            return 2
        if d <= 120:
            return 4
        return 6
    if flexibility == "flexible":
        if d <= 60:
            return 1
        if d <= 180:
            return 2
        return 4

    # balanced
    if d <= 60:
        return 1
    if d <= 180:
        return 3
    return 5


def reason_for_penalty(name: str, p: int, local_dt: datetime) -> str | None:
    h = local_dt.hour
    if p >= 5 and (h >= 22 or h < 7):
        return f"{name} overnight"
    if p >= 3:
        return f"{name} outside preferred hours"
    return None


def fmt(dt: datetime):
    return dt.strftime("%H:%M"), dt.strftime("%-I:%M %p")


def classify(score: int):
    if score <= 1:
        return "Optimal"
    if score <= 5:
        return "Stretch"
    return "Avoid"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--date", help="Anchor date, e.g. 2026-03-06")
    ap.add_argument("--anchor", default="America/Chicago")
    ap.add_argument("--zones", help='"Chicago=America/Chicago,London=Europe/London"')
    ap.add_argument("--duration", type=int, default=60)
    ap.add_argument("--step", type=int, default=60)
    ap.add_argument("--top", type=int, default=3)
    ap.add_argument("--hours", default="", help='Per-person preferred hours map, e.g. "Chicago=09:00-17:00,London=08:30-17:30"')
    ap.add_argument("--my-hours", default="", help='Your preferred hours range, e.g. "09:00-17:00"')
    ap.add_argument("--setup", action="store_true", help="Run/update onboarding settings")
    ap.add_argument("--show-settings", action="store_true")
    args = ap.parse_args()

    cfg = load_config()

    if args.setup or (not cfg and __import__("sys").stdin.isatty()):
        cfg = run_onboarding_interactive()

    if args.show_settings:
        print(json.dumps(cfg or {"me": {}}, indent=2))
        return

    if not args.date or not args.zones:
        print("Missing required args: --date and --zones")
        print("Tip: run with --setup once to save your defaults.")
        return

    # Me defaults from saved onboarding
    me = (cfg or {}).get("me", {})
    me_hours = args.my_hours or me.get("working_hours", "")
    me_tz = me.get("timezone", args.anchor)
    me_flex = me.get("flexibility", "balanced")

    anchor_tz = ZoneInfo(args.anchor)
    participants = parse_zones(args.zones)

    hours_map = parse_hours_map(args.hours)
    # Apply "me" settings to participant that matches anchor timezone first, otherwise first participant
    if me_hours:
        target_name = None
        for p in participants:
            if str(p.tz) == me_tz or str(p.tz) == str(anchor_tz):
                target_name = p.name
                break
        if target_name is None:
            target_name = participants[0].name
        hours_map[target_name] = parse_hours_range(me_hours)

    default_hours = (8 * 60, 18 * 60)

    start_day = datetime.fromisoformat(args.date).replace(hour=0, minute=0, second=0, microsecond=0, tzinfo=anchor_tz)

    slots = []
    t = start_day
    end_day = start_day + timedelta(days=1)
    while t < end_day:
        t2 = t + timedelta(minutes=args.duration)
        score = 0
        reasons = []
        rows = []
        for p in participants:
            ls, le = t.astimezone(p.tz), t2.astimezone(p.tz)
            pref_start, pref_end = hours_map.get(p.name, default_hours)
            flex = me_flex if p.name in hours_map and (pref_start, pref_end) == hours_map.get(p.name) else "balanced"
            pen = penalty(ls, pref_start, pref_end, flex)
            score += pen
            r = reason_for_penalty(p.name, pen, ls)
            if r:
                reasons.append(r)
            rows.append((p.name, ls, le))
        slots.append((classify(score), score, t, t2, rows, sorted(set(reasons))))
        t += timedelta(minutes=args.step)

    buckets = {"Optimal": [], "Stretch": [], "Avoid": []}
    for s in slots:
        buckets[s[0]].append(s)

    for k in buckets:
        buckets[k] = sorted(buckets[k], key=lambda x: x[1])[: args.top]

    for category in ["Optimal", "Stretch", "Avoid"]:
        icon = {"Optimal": "✅", "Stretch": "🟨", "Avoid": "🟥"}[category]
        print(f"{icon} **{category}**\n")
        if not buckets[category]:
            print("No windows found.\n")
            continue

        for i, (_, score, s, e, rows, reasons) in enumerate(buckets[category], start=1):
            a24s, a12s = fmt(s)
            a24e, a12e = fmt(e)
            print(f"{i}. **{a24s}–{a24e} {s.tzname()} ({a12s}–{a12e})**")

            for name, ls, le in rows[1:]:
                s24, s12 = fmt(ls)
                e24, e12 = fmt(le)
                plus = " +1 day" if ls.date() > s.date() else ""
                print(f"{name} {s24}–{e24} ({s12}–{e12}){plus}")

            if category in ("Stretch", "Avoid") and reasons:
                print(f"*Reason: {', '.join(reasons)}.*")

            if i != len(buckets[category]):
                print("⠀")
        print()


if __name__ == "__main__":
    main()
