#!/usr/bin/env python3
"""myth_analyzer.py - urban myth / chain message / superstition analyzer.

Modes:
  analyze - score a claim against the folklore-pattern catalog
  list    - show the pattern catalog (families -> patterns)
  stats   - running stats of analyzed claims (JSON log)

Not a fact-checker: it detects the *rhetorical structure* that myths,
chain letters, and old wives' tales share, and points at what evidence
WOULD settle the claim. Educational triage, not a verdict on truth.

Zero dependencies (Python 3.8+ stdlib). Log: ./data/myth_log.json
"""
import argparse
import json
import os
import re
import sys
from datetime import date

DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")

# --------------------------------------------------------- pattern catalog
# family -> list of (pattern_name, regex, weight, tell_tale_question)
PATTERNS = {
    "authority mimicry": [
        ("named-expert vagueness", r"\b(according to|per)\s+(a|an|some)?\s*(doctor|professor|scientist|researcher|study|harvard|mit|nasa|fda)", 2,
         "Which doctor/study? Named institutions publish named people."),
        ("big-institution flex", r"\b(harvard|mit|nasa|fda|cdc|who|mayo clinic)\b.{0,60}\b(proved|confirms|found|says|warns)\b", 2,
         "Institutions publish press releases with URLs - where is it?"),
        ("military/secret research", r"\b(army|military|navy|cia|secret(ly)?|classified)\b.{0,50}\b(study|research|experiment|program)\b", 2,
         "Classified research is uncheckable by design - a red flag, not proof."),
    ],
    "urgency & suppression": [
        ("they don't want you to know", r"(don'?t|doesn'?t|never)\s+(want|let)\s+(you|us|people)\s+(to\s+)?(know|see|hear|find)", 3,
         "Who is 'they'? Vague suppression claims need a named actor."),
        ("censorship imminent", r"(they'?re|they are|get)\s+(trying\s+to\s+)?(take|remove|ban|censor|delete|suppress)\w*\s+(this|it|down)", 3,
         "Reposts of 'about to be deleted' content exist for decades."),
        ("share immediately", r"(forward|share|send|pass)\s+(this\s+)?(to|with)\s+(\d+|everyone|all|every)", 3,
         "Genuine information doesn't come with forwarding quotas."),
        ("act before you think", r"(before\s+(it'?s\s+)?too\s+late|hurry|act\s+now|time\s+is\s+running)", 2,
         "Deadlines disable verification - that's their function."),
    ],
    "unfalsifiable structure": [
        ("no-testable-mechanism vibe", r"\b(energy|vibrations|aura|quantum|frequencies|toxins)\b", 2,
         "Ask for the mechanism in one sentence with measurable quantities."),
        ("convenient immunity", r"(only|just)\s+(works|happens)\s+(if|when)\s+(you\s+(believe|don'?t\s+test)|no\s+one\s+(is\s+)?(watching|measuring|looking))", 3,
         "A claim that fails when measured is not a claim."),
        ("ancient wisdom appeal", r"\b(ancients?|for\s+(thousands|centuries)|traditional|our\s+grandmothers|old\s+wive)", 1,
         "Age of a belief is not evidence - longitude of belief is."),
    ],
    "causal sleight of hand": [
        ("correlation-as-cause", r"\b(because\s+of|caused|linked\s+to|due\s+to|after)\b.{0,60}\b(they|people|he|she|it)\b.{0,40}\b(died|got\s+sick|happened)", 2,
         "Was a controlled comparison done, or did two events merely co-occur?"),
        ("single-case proof", r"\b(my|a|one)\s+(friend|neighbor|cousin|aunt|uncle|guy|woman|man)\b.{0,80}\b(died|collapsed|was\s+cured|swears)", 2,
         "One vivid case is an anecdote; ask for the base rate."),
        ("post-hoc timing", r"\b(hours?|days?|minutes?)\s+(later|after)\b.{0,50}\b(doctors|scientists|experts)\s+(found|discovered|confirmed)", 2,
         "Sequence is not causation; ask what the comparison group showed."),
    ],
    "numeric theater": [
        ("precise-sounding stat, no source", r"\b\d{2,3}\s?%.{0,60}\b(of\s+(people|americans|doctors|users)|die|fail|are\s+affected)", 2,
         "Percentages need denominators and sources."),
        ("suspicious round numbers", r"\b(9[05]|[1-9]0|[1-9],?000|100)\s?(out\s+of\s+\d+)?\s?(doctors|scientists|experts)", 2,
         "'9 out of 10 experts' - which ten, polled by whom?"),
        ("micro-dose scare", r"\b(\d+(\.\d+)?)\s?(mg|g|micrograms?|ppm|percent)\b.{0,50}\b(poison|toxic|kill|deadly|dangerous)", 2,
         "The dose makes the poison - what's the reference dose for comparison?"),
    ],
    "emotional amplifiers": [
        ("children at risk", r"\b(children|kids|child|baby|babies|infant)\b.{0,60}\b(danger|dying|at\s+risk|hurt|kidnapp|threat)", 3,
         "Child-safety framing spikes sharing; ask for the incident reports."),
        ("gruesome detail", r"\b(bleeding|convulsion|paralyzed|organ\s+failure|melted|rotting)\b", 2,
         "Graphic imagery is not data."),
        ("fortune/curse chain", r"\b(good\s+luck|bad\s+luck|curse|blessing|fortune|wish)\b.{0,60}\b(send|forward|share|copy|delete|ignore)", 3,
         "Luck mechanics are the oldest chain-letter engine."),
    ],
}

FAMILY_HINTS = {
    "authority mimicry": "borrows credibility instead of earning it",
    "urgency & suppression": "rushes you past verification",
    "unfalsifiable structure": "arranges to survive being wrong",
    "causal sleight of hand": "dresses sequence up as cause",
    "numeric theater": "uses numbers as costumes",
    "emotional amplifiers": "hijacks sharing instincts",
}


def analyze_text(text):
    hits = []
    score = 0
    tl = text.lower()
    for family, pats in PATTERNS.items():
        fam_hits = 0
        for name, rx, weight, question in pats:
            m = re.search(rx, tl)
            if m:
                fam_hits += 1
                score += weight
                hits.append({"family": family, "pattern": name,
                             "matched": m.group(0)[:60], "weight": weight,
                             "ask": question})
        if fam_hits >= 2:
            score += 2  # family clustering bonus
    return score, hits


def verdict_for(score, hits):
    fams = {h["family"] for h in hits}
    if score >= 10 or len(fams) >= 4:
        return "STRONG myth signatures", "Treat as folklore until primary sources appear."
    if score >= 6 or len(fams) >= 3:
        return "MODERATE myth signatures", "Verify before sharing; several rhetorical red flags."
    if score >= 3:
        return "WEAK myth signatures", "A couple of flags - could be sloppy writing or real news."
    return "NO significant myth signatures", "Structure alone doesn't judge this one; check facts normally."


def cmd_analyze(args):
    text = args.text
    if os.path.exists(text) and text.endswith(".txt"):
        with open(text) as f:
            text = f.read()
    score, hits = analyze_text(text)
    label, advice = verdict_for(score, hits)
    print("Claim analyzed (%d chars)" % len(text))
    print("Myth-signature score : %d" % score)
    print("Pattern families hit : %d" % len({h["family"] for h in hits}))
    print("Verdict              : %s" % label)
    print()
    if hits:
        print("Matched patterns:")
        for h in hits:
            print("  [%s] %s (w%d)" % (h["family"], h["pattern"], h["weight"]))
            print("     matched: %r" % h["matched"])
            print("     ask    : %s" % h["ask"])
        print()
    print("Next step: %s" % advice)
    if args.log:
        os.makedirs(DATA_DIR, exist_ok=True)
        entry = {"ts": str(date.today()), "score": score,
                 "verdict": label, "text_head": text[:120],
                 "hits": [(h["family"], h["pattern"]) for h in hits]}
        path = os.path.join(DATA_DIR, "myth_log.json")
        log = []
        if os.path.exists(path):
            try:
                with open(path) as f:
                    log = json.load(f)
            except Exception:
                log = []
        log.append(entry)
        with open(path, "w") as f:
            json.dump(log, f, indent=2)
        print("Logged: %s" % path)
    return 0


def cmd_list(args):
    for fam, pats in PATTERNS.items():
        print("%s - %s" % (fam.upper(), FAMILY_HINTS[fam]))
        for name, rx, weight, q in pats:
            print("  - %-32s w%d" % (name, weight))
        print()
    return 0


def cmd_stats(args):
    path = os.path.join(DATA_DIR, "myth_log.json")
    if not os.path.exists(path):
        sys.exit("no log yet - run analyze --log first")
    with open(path) as f:
        log = json.load(f)
    print("Analyzed claims: %d" % len(log))
    from collections import Counter
    fams = Counter()
    pats = Counter()
    for e in log:
        for fam, pat in e["hits"]:
            fams[fam] += 1
            pats[pat] += 1
    print("\nTop families:")
    for fam, n in fams.most_common():
        print("  %-26s %d" % (fam, n))
    print("\nTop patterns:")
    for pat, n in pats.most_common(8):
        print("  %-32s %d" % (pat, n))
    return 0


def main():
    p = argparse.ArgumentParser(description=__doc__)
    sub = p.add_subparsers(dest="mode", required=True)

    sp = sub.add_parser("analyze", help="score a claim's rhetoric")
    sp.add_argument("text", help="claim text (or path to a .txt file)")
    sp.add_argument("--log", action="store_true", help="append to log")
    sp.set_defaults(func=cmd_analyze)

    sp = sub.add_parser("list", help="show pattern catalog")
    sp.set_defaults(func=cmd_list)

    sp = sub.add_parser("stats", help="log statistics")
    sp.set_defaults(func=cmd_stats)

    args = p.parse_args()
    sys.exit(args.func(args))


if __name__ == "__main__":
    main()
