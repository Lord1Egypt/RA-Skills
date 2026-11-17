#!/usr/bin/env python3
"""Toddler meltdown triage + pattern log.

triage: score 7 trigger classes from observed cues, print the
top classes with a de-escalation script + NEVER list + parent
check + red-flag scan. log: record episodes (full or averted).
stats: hour-of-day hotspots, class frequency, intervention
effectiveness. Pure stdlib; state in scripts/data/meltdowns.json.
"""
import argparse
import json
import re
import sys
import time
from collections import Counter, defaultdict
from pathlib import Path

DATA = Path(__file__).parent / "data" / "meltdowns.json"

CLASSES = ["hungry", "tired", "overstimulated", "frustrated",
           "sensory", "connection", "pain"]

CUES = {
    "hungry": {
        "pre-meal": 2, "hangry-aggression": 2, "bites-then-eats": 2,
        "demands-food": 1, "fast-ramp": 1,
    },
    "tired": {
        "eye-rub": 2, "yawning": 2, "clumsy": 2, "fights-nap": 2,
        "melts-at-minor": 1, "slow-burn": 1, "late-afternoon": 1,
        "wakes-night": 1,
    },
    "overstimulated": {
        "covers-ears": 2, "avoids-eyes": 2, "wants-alone": 2,
        "post-playdate": 2, "post-store": 2, "busy-before": 1,
        "escape-seeking": 2, "hard-transitions": 1,
    },
    "frustrated": {
        "task-linked": 2, "me-do-it": 2, "throws-at-problem": 2,
        "tower-collapse": 1, "clothes-struggle": 1,
    },
    "sensory": {
        "tag": 2, "seams": 2, "sock-refusal": 2, "sound-cover": 2,
        "light-squint": 2, "texture-transition": 1, "specific-stimulus": 2,
    },
    "connection": {
        "bid-then-boom": 2, "parent-on-phone": 2, "follows-then-hits": 2,
        "calms-fast-with-attention": 2, "sibling-attention": 1,
    },
    "pain": {
        "ear-grab": 2, "chewing": 2, "drooling": 2, "night-waking": 1,
        "fever": 2, "nothing-works": 2, "falls-on-food": 1,
    },
}

TIME_PRIORS = {  # hour -> class -> bonus
    17: {"hungry": 2, "tired": 1}, 18: {"hungry": 2, "tired": 1},
    16: {"hungry": 1}, 19: {"tired": 2},
    11: {"hungry": 1}, 12: {"hungry": 1, "tired": 1},
    13: {"tired": 2}, 14: {"tired": 2},
}

RED_FLAGS = {
    "self-injury": "self-injury (head banging beyond brief frustration, "
                   "biting self hard) -> pediatrician conversation",
    "breath-holding": "breath-holding with fainting -> pediatrician "
                      "conversation",
    "inconsolable": "total inconsolability, nothing works EVERY time -> "
                    "pediatrician conversation",
    "no-joint-attention": "no pointing/joint attention alongside behavior "
                          "-> developmental screening conversation",
    "language-regression": "language regression -> pediatrician promptly",
    "nightly-45min": "nightly 45+ min episodes with aggression -> "
                     "pediatrician conversation",
}

SCRIPTS = {
    "hungry": ("NOW: protein+fat snack (cheese/yogurt/nut butter), not "
               "juice/sweets. Words: 'Food. Let's eat.'\n"
               "NEVER: negotiate eating; make food contingent on calm.\n"
               "PREVENT: snack at 17:00 sharp; watch the dinner gap."),
    "tired": ("NOW: zero demands. 'We're going home.' Carry, don't walk-"
              "and-argue. Dim, slow, quiet.\n"
              "NEVER: 'one more thing'; fight the nap with activity.\n"
              "PREVENT: protect nap window; bedtime 20 min earlier for a "
              "week - count meltdowns in the log."),
    "overstimulated": ("NOW: REMOVE stimulus (leave/dim/quiet). Fewer "
                       "words. Sit nearby; touch only if invited. Words: "
                       "'Quiet now.'\n"
                       "NEVER: choices, questions, distraction-"
                       "entertainment - all more input.\n"
                       "PREVENT: 20-min decompression buffer after group "
                       "settings; warn before transitions."),
    "frustrated": ("NOW: break the task invisibly; offer TWO tiny choices "
                   "(red cup or blue?) to restore control.\n"
                   "NEVER: take over and finish it for them.\n"
                   "PREVENT: scaffold hard steps; tools at the edge of "
                   "ability."),
    "sensory": ("NOW: remove/replace the stimulus (tag, seams, sound, "
                "light). Words: 'Tag gone. Better?'\n"
                "NEVER: 'it's just a sock' - the perception is real.\n"
                "PREVENT: pre-check new clothes; familiar items for "
                "transitions; offer firm pressure, don't impose."),
    "connection": ("NOW: 5 min FULL attention, phone away, child-led "
                   "play. Stops fast - that speed is the signature.\n"
                   "NEVER: punish the bid delivered as a hit. Set the "
                   "limit AND meet the need: 'I won't let you hit. I'm "
                   "here NOW.'\n"
                   "PREVENT: daily 10-min named special time, child-led."),
    "pain": ("NOW: check mouth/ears/fever; cold chew thing; weight-based "
             "analgesic per pediatrician dosing if indicated.\n"
             "NEVER: assume 'phase' 3+ days without checking - ear "
             "infections present as tantrums.\n"
             "PREVENT: log night-wakings next to meltdowns."),
}

PARENT_CHECK = ("PARENT CHECK: voice up? jaw tight? rushing? -> tag out "
                "if any adult available; 60s swap is engineering, not "
                "abandonment. Alone: floor sit, slow exhale: 'You're "
                "safe. I'm here.' Your calm IS the intervention.")


def load():
    if DATA.exists():
        return json.loads(DATA.read_text())
    return {"episodes": []}


def save(s):
    DATA.parent.mkdir(parents=True, exist_ok=True)
    DATA.write_text(json.dumps(s, indent=2))


def norm(cue):
    return re.sub(r"\s+", "-", cue.strip().lower())


def hour_of(text):
    m = re.search(r"(\d{1,2})[:.](\d{2})", text or "")
    if m:
        return int(m.group(1)) % 24
    m = re.search(r"\b(\d{1,2})\s*(am|pm)?\b", text or "")
    if m:
        h = int(m.group(1)) % 12
        if m.group(2) == "pm":
            h += 12
        return h % 24
    return None


def score(cues, hour):
    sc = {c: 0.0 for c in CLASSES}
    matched = []
    for cue in cues:
        c = norm(cue)
        hit = False
        for cls, d in CUES.items():
            for key, w in d.items():
                if key in c or c in key or (len(c) > 3 and
                                            key.split("-")[0] in c):
                    sc[cls] += w
                    hit = True
        if c in RED_FLAGS or any(f in c for f in RED_FLAGS):
            matched.append(c)
        if not hit and len(c) > 2:
            matched_unknown = c  # fall through: time prior still applies
    if hour is not None:
        for cls, bonus in TIME_PRIORS.get(hour, {}).items():
            sc[cls] += bonus
    return sc, matched


def cmd_triage(a):
    cues = [c for c in re.split(r"[,;]", a.cues or "") if c.strip()]
    hour = a.hour if a.hour is not None else hour_of(a.cues or "")
    if not cues:
        sys.exit("pass --cues comma-separated observed cues "
                 "(e.g. eye-rub,clumsy,17:40)")
    sc, flagged = score(cues, hour)
    ranked = sorted(sc.items(), key=lambda kv: kv[1], reverse=True)
    top, second = ranked[0], ranked[1]
    total = sum(v for _, v in ranked) or 1
    conf = top[1] / total * 100

    print(f"\nTRIAGE (age {a.age}, hour {hour if hour is not None else '?'})"
          f"  cues: {', '.join(norm(c) for c in cues)}")
    print("=" * 70)
    print(f"1. {top[0].upper():<14} score {top[1]:.0f}  ({conf:.0f}% share)"
          + ("   [weak signal - treat as guess]" if top[1] < 3 else ""))
    if second[1] >= top[1] * 0.5 and second[1] > 0:
        print(f"2. {second[0].upper():<14} score {second[1]:.0f}  "
              "(stacked class - address both)")
    print("-" * 70)
    print(SCRIPTS[top[0]])
    if second[1] >= top[1] * 0.5 and second[1] > 0:
        print(f"\nAlso, for the stacked {second[0]} class:")
        print(SCRIPTS[second[0]])
    print("-" * 70)
    if flagged:
        print("RED FLAGS RAISED:")
        for f in flagged:
            for k, v in RED_FLAGS.items():
                if k in f:
                    print(f"  ! {v}")
    else:
        print("Red flags: none from these cues.")
    print("-" * 70)
    print("UNIVERSAL: get low, 3-5 words max, fewer stimuli, no teaching "
          "mid-meltdown, time-IN not time-out under ~4.")
    print(PARENT_CHECK)
    print("=" * 70 + "\n")
    if a.log:
        cmd_log_args(a, top[0], hour)
        print("(episode logged)")


def cmd_log_args(a, cls, hour):
    st = load()
    st["episodes"].append({
        "ts": int(time.time()), "age": a.age,
        "cues": [norm(c) for c in re.split(r"[,;]", a.cues or "") if c.strip()],
        "class": cls, "hour": hour,
        "duration": a.duration, "averted": bool(a.averted),
        "intervention": a.intervention, "notes": a.notes,
    })
    save(st)


def cmd_log(a):
    if not a.cls:
        cues = [c for c in re.split(r"[,;]", a.cues or "") if c.strip()]
        if not cues:
            sys.exit("log needs --class or --cues")
        hour = a.hour if a.hour is not None else hour_of(a.cues)
        sc, _ = score(cues, hour)
        a.cls = max(sc.items(), key=lambda kv: kv[1])[0]
    hour = a.hour if a.hour is not None else hour_of(a.cues or "")
    cmd_log_args(a, a.cls, hour)
    print(f"logged episode: class={a.cls} hour={hour} "
          f"averted={bool(a.averted)}")


def cmd_stats(_a=None):
    st = load()
    eps = st.get("episodes", [])
    if not eps:
        sys.exit("no episodes logged yet - log a few first")
    print(f"\n{len(eps)} episodes logged\n" + "=" * 70)
    hrs = Counter(e["hour"] for e in eps if e["hour"] is not None)
    if hrs:
        print("HOUR-OF-DAY HOTSPOTS (one dominant spike = schedule fix)")
        peak = max(hrs.values())
        for h in sorted(hrs):
            bar = "#" * int(hrs[h] / peak * 30)
            print(f"  {h:02d}:00  {hrs[h]:>2}  {bar}")
    cls = Counter(e["class"] for e in eps)
    print("\nCLASS FREQUENCY:")
    for c, n in cls.most_common():
        print(f"  {c:<14} {n}")
    av = [e for e in eps if e.get("averted")]
    full = [e for e in eps if not e.get("averted")]
    print(f"\naverted {len(av)} / full {len(full)}")
    iv = Counter(e.get("intervention") for e in av if e.get("intervention"))
    if iv:
        print("INTERVENTIONS THAT AVERTED (keep doing these):")
        for k, n in iv.most_common():
            print(f"  {k:<24} {n}")
    freq = len(eps)
    print(f"\nrate: {freq} episodes logged total")
    print("If 3+/day every day for weeks: revisit red flags + talk to "
          "your pediatrician - that's logistics or medical, not "
          "parenting.")
    print()


def main():
    p = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.
                                 RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="cmd", required=True)
    t = sub.add_parser("triage")
    t.add_argument("--cues", required=True,
                   help="comma-separated observed cues + optional time")
    t.add_argument("--age", type=int, default=2)
    t.add_argument("--hour", type=int, default=None)
    t.add_argument("--log", action="store_true",
                   help="also log this episode with the top class")
    t.set_defaults(func=cmd_triage)
    l = sub.add_parser("log")
    l.add_argument("--cues", default="")
    l.add_argument("--class", dest="cls", default=None)
    l.add_argument("--age", type=int, default=2)
    l.add_argument("--hour", type=int, default=None)
    l.add_argument("--duration", type=int, default=None)
    l.add_argument("--averted", action="store_true")
    l.add_argument("--intervention", default=None)
    l.add_argument("--notes", default=None)
    l.set_defaults(func=cmd_log)
    s = sub.add_parser("stats")
    s.set_defaults(func=cmd_stats)
    a = p.parse_args()
    a.func(a)


if __name__ == "__main__":
    try:
        main()
    except BrokenPipeError:
        try:
            sys.stdout.close()
        except Exception:
            pass
