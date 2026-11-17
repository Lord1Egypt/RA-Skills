#!/usr/bin/env python3
"""wedding-toast-architect: build and safety-scan a wedding speech.

Pure-stdlib. Three tools:
  build   — questionnaire answers -> structured 5-part outline with word
            budgets per section (tuned by role), timing at 3 speaking paces.
  scan    — draft text -> red-flag report: cut/soften/check findings
            (ex mentions, drunk stories, profanity, inside jokes density,
            divorce/money jokes, negative openers), length vs target,
            long-sentence and readability checks.
  time    — words -> minutes at 120/135/150 wpm with verdict.

Usage:
  python3 toast_architect.py build --role best-man --couple "Alex & Sam" \
      --years-known 9 --stories "rafting capsize; chili cook-off disaster" \
      --qualities "loyal, calm in chaos" --partner "Sam" --minutes 3
  python3 toast_architect.py scan --draft draft.txt --protected "Jordan,Riley" --minutes 3
  python3 toast_architect.py time --words 720
"""
from __future__ import annotations

import argparse
import json
import re
import sys

WPM_SLOW, WPM_NORMAL, WPM_FAST = 110, 135, 150

ROLE_BUDGETS = {  # section -> share of total words (sums to 1.0), by role
    "best-man":       {"hook": 0.12, "who": 0.10, "story1": 0.30, "story2": 0.22, "partner": 0.14, "toast": 0.12},
    "maid-of-honor":  {"hook": 0.10, "who": 0.10, "story1": 0.28, "story2": 0.22, "partner": 0.18, "toast": 0.12},
    "parent":         {"hook": 0.10, "who": 0.06, "story1": 0.26, "story2": 0.22, "partner": 0.24, "toast": 0.12},
    "friend":         {"hook": 0.14, "who": 0.16, "story1": 0.28, "story2": 0.20, "partner": 0.10, "toast": 0.12},
    "sibling":        {"hook": 0.12, "who": 0.10, "story1": 0.28, "story2": 0.22, "partner": 0.16, "toast": 0.12},
}

SECTION_PROMPTS = {
    "hook":    "One line that lands. A tiny image, not a joke from the internet. "
               "E.g. 'Nine years ago Alex talked me into a rafting trip that went very wrong.'",
    "who":     "Who you are in one sentence + your credential to speak "
               "(relationship, years known). Nobody wants your resume.",
    "story1":  "THE story: 60-90 second arc (scene -> complication -> payoff) that shows a "
               "quality of the person. One story, told well, beats three told fast.",
    "story2":  "Short second beat OR the how-they-met/how-partner-changed-them moment. "
               "This is where the partner enters properly - warm, specific, generous.",
    "partner": "Welcome the partner by name: what they bring, one observed detail. "
               "Never 'we never thought X would settle down' - that insults both.",
    "toast":   "The ask: glasses up, one sentence of wish for their future, names said. "
               "End on 'to Alex and Sam' - not on a punchline.",
}

# (label, compiled regex, severity, advice)  severity: CUT | SOFTEN | CHECK
FLAGS = [
    ("ex-partner reference", re.compile(r"\bex[- ](?:wife|husband|girl|boy|partner|es)?\b", re.I),
     "CUT", "Exes never belong in a toast. No exceptions, even funny ones."),
    ("drunk/intoxication story", re.compile(r"\b(?:drunk|wasted|hammered|blackout|blacked out|vomit|threw up|passed out|buzzed)\b", re.I),
     "CUT", "Family weddings, all ages. Kill the drinking story — or compress to 'a memorable night' with no detail."),
    ("strip club / vegas reference", re.compile(r"\b(?:strip|gentleman'?s club|lap dance|vegas)\b", re.I),
     "CUT", "Bachelor-party content bombs with half the room. Replace with a story that includes the couple."),
    ("divorce / pessimism joke", re.compile(r"\b(?:divorce|half of marriages|ball and chain|chain|game over|end of freedom|last free day)\b", re.I),
     "CUT", "Divorce/entrapment jokes read as doubt about the marriage. Cut entirely."),
    ("'finally settled' framing", re.compile(r"\b(?:finally settled|took you long enough|last person i expected|never thought (?:you'?d|he'?d|she'?d) (?:get married|settle)|didn'?t think it was possible)\b", re.I),
     "CUT", "Backhanded compliment — implies the couple is lucky anyone married them. Reframe as delight, not surprise."),
    ("pregnancy mention", re.compile(r"\b(?:pregnan\w*|baby on the way|shotgun)\b", re.I),
     "CUT", "Not your news to announce. Ever."),
    ("profanity", re.compile(r"\b(?:damn|hell|crap|sucks|screw(?:ed)?|ass\w*|bitch\w*|sh\*t|shit)\b", re.I),
     "SOFTEN", "Swears shrink the room. One mild word can pass; more than one, soften."),
    ("money/finance joke", re.compile(r"\b(?:prenup|her money|his money|dowry|sugar|meal ticket)\b", re.I),
     "SOFTEN", "Money jokes divide the room into who laughed and who cringed. Rework."),
    ("looks-focused compliment", re.compile(r"\b(?:hot|sexy|smoking|gorgeous body|trophy (?:wife|husband))\b", re.I),
     "SOFTEN", "Compliment character and choices, not just looks — grandparents present."),
    ("dating-app swipe joke", re.compile(r"\b(?:swipe(?:d|right|left)|tinder|bumble|hinge (?:match|date))\b", re.I),
     "CHECK", "Mild, but make sure the couple is happy for the meeting story to be told. Ask."),
    ("inside-joke marker", re.compile(r"[\(\[].{0,40}?[\)\]]"),
     "CHECK", "Parentheticals usually signal an inside joke only two people get. Translate or cut."),
    ("religion/faith assumption", re.compile(r"\b(?:god(?:'s plan| willing)|blessed by|prayers)\b", re.I),
     "CHECK", "Only if it matches the couple's faith and tone of the day."),
    ("negative opener 'but'", re.compile(r"^\s*.{0,60}\bhowever\b", re.I | re.M),
     "CHECK", "'However' early in a sentence usually introduces a dig. Read aloud."),
    ("cliche opener", re.compile(r"^\s*(?:good (?:evening|afternoon)|for those who don'?t know me|when i was asked to give this speech)", re.I | re.M),
     "SOFTEN", "Stock openings waste your best 10 seconds. Start inside the story instead."),
    ("reading-off-phone marker", re.compile(r"\b(?:um+|uh+|like, i guess|sort of like)\b", re.I),
     "SOFTEN", "Filler words on paper mean filler words out loud. Tighten."),
]


def words(text: str) -> int:
    return len(re.findall(r"[A-Za-z0-9'’-]+", text))


def sentences(text: str):
    return [s.strip() for s in re.split(r"[.!?]+", text) if s.strip()]


def syllables(word: str) -> int:
    w = re.sub(r"[^a-z]", "", word.lower())
    if not w:
        return 0
    groups = re.findall(r"[aeiouy]+", w)
    n = len(groups)
    if w.endswith("e") and n > 1 and not w.endswith(("le", "ee", "ye")):
        n -= 1
    return max(1, n)


def flesch(text: str) -> float:
    sents = sentences(text)
    if not sents:
        return 0.0
    w = [x for x in re.findall(r"[A-Za-z'’-]+", text)]
    if not w:
        return 0.0
    syl = sum(syllables(x) for x in w)
    return 206.835 - 1.015 * (len(w) / len(sents)) - 84.6 * (syl / len(w))


def cmd_build(args):
    budget = ROLE_BUDGETS.get(args.role, ROLE_BUDGETS["friend"])
    total_words = int(args.minutes * WPM_NORMAL)
    stories = [s.strip() for s in re.split(r"[;]", args.stories or "") if s.strip()]
    qualities = [s.strip() for s in re.split(r"[;,]", args.qualities or "") if s.strip()]

    print("=" * 66)
    print(f"TOAST BLUEPRINT — {args.role.replace('-', ' ').title()} for {args.couple}")
    print(f"Target: {args.minutes} min ≈ {total_words} words at {WPM_NORMAL} wpm")
    print("=" * 66)

    fills = {
        "hook": f"Open inside a moment with {args.couple.split('&')[0].strip() or 'them'}"
                + (f" ({args.years_known} years of material to choose from)." if args.years_known else "."),
        "who": f"One sentence: your relationship + years known"
               + (f" ({args.years_known} years)." if args.years_known else "."),
        "story1": (f"Your story: {stories[0]}" if stories else "Your strongest story") +
                  (f" — told to prove: {qualities[0]}" if qualities else " — told to prove one quality"),
        "story2": f"Second beat: {stories[1]}" if len(stories) > 1 else
                  ("How they met / how the partner changed them — bring in "
                   f"{args.partner or 'the partner'} here."),
        "partner": f"Welcome {args.partner or 'the partner'}: one specific thing they bring out in your person."
                   + (f" Note the quality '{qualities[1]}' if true." if len(qualities) > 1 else ""),
        "toast": f"Raise glass: one sentence of future-wish for {args.couple}, end on their names.",
    }

    for i, sec in enumerate(["hook", "who", "story1", "story2", "partner", "toast"], 1):
        n = int(total_words * budget[sec])
        print(f"\n{i}. {sec.upper()}  —  ~{n} words ({n / WPM_NORMAL * 60:.0f}s)")
        print(f"   {SECTION_PROMPTS[sec]}")
        print(f"   Yours: {fills[sec]}")

    print("\n" + "-" * 66)
    print(f"Pacing: {total_words} words = "
          f"{total_words / WPM_SLOW:.1f}min slow / {total_words / WPM_NORMAL:.1f}min normal / "
          f"{total_words / WPM_FAST:.1f}min fast")
    print("Rehearse 3x out loud, standing, holding a (full) glass.")
    print("Print in 18pt+, one section per index card, number the cards.")
    return 0


def cmd_scan(args):
    text = open(args.draft, encoding="utf-8").read().strip() if args.draft != "-" else sys.stdin.read().strip()
    if not text:
        print("Empty draft."); return 1
    wc = words(text)
    findings = []

    for label, rx, sev, advice in FLAGS:
        hits = rx.findall(text)
        if hits:
            findings.append((sev, label, len(hits), advice))

    for name in [n.strip() for n in (args.protected or "").split(",") if n.strip()]:
        if re.search(rf"\b{re.escape(name)}\b", text, re.I):
            findings.append(("CUT", f"protected name '{name}'", 1,
                             "You flagged this name as forbidden (ex, estranged, deceased, or private). Remove."))

    n_cut = sum(1 for f in findings if f[0] == "CUT")
    n_soft = sum(1 for f in findings if f[0] == "SOFTEN")
    n_check = sum(1 for f in findings if f[0] == "CHECK")

    target = int((args.minutes or 3) * WPM_NORMAL)
    fr = flesch(text)
    long_sents = [s for s in sentences(text) if words(s) > 34]

    print("=" * 66)
    print("RED-FLAG SCAN")
    print("=" * 66)
    print(f"Words: {wc}  |  target ≈ {target}  |  est. {wc / WPM_NORMAL:.1f} min at {WPM_NORMAL} wpm")
    if wc > target * 1.25:
        print(f"!! LENGTH: {wc - target} words OVER — cut one story, not all detail.")
    elif wc < target * 0.6:
        print(f"!! LENGTH: {target - wc} words UNDER — you have room; deepen story 1, don't add story 3.")
    else:
        print("OK length.")
    print(f"Readability (Flesch): {fr:.0f} — aim 60-80 for ears; lower = harder to deliver.")
    if long_sents:
        print(f"!! {len(long_sents)} sentence(s) over 34 words — split for breath:")
        for s in long_sents[:3]:
            print(f"   - {s[:80]}...")

    if findings:
        print(f"\nFindings: {n_cut} CUT / {n_soft} SOFTEN / {n_check} CHECK")
        for sev in ("CUT", "SOFTEN", "CHECK"):
            group = [f for f in findings if f[0] == sev]
            if group:
                print(f"\n[{sev}]")
                for _, label, n, advice in group:
                    print(f"  - {label} ({n}x): {advice}")
    else:
        print("\nNo flag patterns found. Still read aloud once — scanners miss tone.")

    print("\nFinal gate: would you say this to the couple's face, with both "
          "grandmothers listening? That is the bar.")
    score = 100 - n_cut * 18 - n_soft * 7 - n_check * 3
    print(f"Safety score: {max(0, score)}/100" +
          ("  — publish-able after fixes." if score >= 85 else "  — fix CUT items first."))
    return 0


def cmd_time(args):
    w = args.words
    print(f"{w} words:")
    for label, wpm in (("slow/adrenaline", WPM_SLOW), ("normal", WPM_NORMAL), ("fast", WPM_FAST)):
        print(f"  {label:18} {w / wpm:.1f} min")
    print("Sweet spot for a toast: 2.5-3.5 minutes (340-470 words).")
    return 0


def main(argv=None):
    p = argparse.ArgumentParser(description="Wedding toast architect")
    sub = p.add_subparsers(dest="cmd", required=True)

    b = sub.add_parser("build")
    b.add_argument("--role", required=True, choices=sorted(ROLE_BUDGETS))
    b.add_argument("--couple", required=True)
    b.add_argument("--partner", default="")
    b.add_argument("--years-known", type=int, default=0)
    b.add_argument("--stories", default="", help="1-2 stories separated by ';'")
    b.add_argument("--qualities", default="", help="qualities separated by ','")
    b.add_argument("--minutes", type=float, default=3.0)

    s = sub.add_parser("scan")
    s.add_argument("--draft", required=True, help="path to draft .txt, or - for stdin")
    s.add_argument("--protected", default="", help="names that must NOT appear, comma-separated")
    s.add_argument("--minutes", type=float, default=3.0)

    t = sub.add_parser("time")
    t.add_argument("--words", type=int, required=True)

    args = p.parse_args(argv)
    return {"build": cmd_build, "scan": cmd_scan, "time": cmd_time}[args.cmd](args)


if __name__ == "__main__":
    try:
        sys.exit(main())
    except BrokenPipeError:
        sys.exit(0)  # output was piped to head/less — not an error
