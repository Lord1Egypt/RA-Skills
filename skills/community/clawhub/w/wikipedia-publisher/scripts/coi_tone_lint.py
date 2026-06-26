#!/usr/bin/env python3
import argparse
import re
import sys
from pathlib import Path

PROMO_PATTERNS = {
    "puffery": [
        r"\bleading\b", r"\bworld[ -]?class\b", r"\bpremier\b", r"\binnovative\b",
        r"\btrusted\b", r"\bpioneering\b", r"\brenowned\b", r"\bhigh[- ]quality\b",
        r"\bofficial supplier\b", r"\bindustry leader\b", r"\bcutting-edge\b",
    ],
    "sales-language": [
        r"\bcustomers?\b", r"\bsolutions\b", r"\bexcellence\b", r"\bpremium\b",
        r"\bbespoke\b", r"\bseamless\b", r"\bvalue proposition\b",
    ],
    "weak-scale-claims": [
        r"\bglobal\b", r"\bworldwide\b", r"\bmajor\b", r"\bextensive\b", r"\blarge-scale\b",
    ],
}

PRIMARY_HINTS = [
    "official website", "about", "contact", "press release", "linkedin", "facebook", "instagram",
    "youtube", "x.com", "twitter.com", "company website", "the company said"
]

CITE_PAT = re.compile(r"<ref[^>]*>(.*?)</ref>|\{\{cite [^}]+\}\}", re.I | re.S)


def load_text(path: str | None) -> str:
    if not path or path == "-":
        return sys.stdin.read()
    return Path(path).read_text(encoding="utf-8")


def count_matches(text: str):
    results = {}
    for label, patterns in PROMO_PATTERNS.items():
        hits = []
        for pat in patterns:
            hits.extend(re.findall(pat, text, flags=re.I))
        results[label] = hits
    return results


def primary_hints(text: str):
    found = []
    lower = text.lower()
    for hint in PRIMARY_HINTS:
        if hint in lower:
            found.append(hint)
    return found


def main():
    ap = argparse.ArgumentParser(description="Flag promotional tone and weak-source hints in wiki drafts")
    ap.add_argument("path", nargs="?", help="Draft file path, or omit/read stdin")
    args = ap.parse_args()
    text = load_text(args.path)

    promo = count_matches(text)
    primary = primary_hints(text)
    refs = len(CITE_PAT.findall(text))

    total_hits = sum(len(v) for v in promo.values())
    print(f"refs_detected: {refs}")
    print(f"promo_hits: {total_hits}")
    for label, hits in promo.items():
        if hits:
            uniq = sorted(set(h.lower() for h in hits))
            print(f"- {label}: {', '.join(uniq)}")
    if primary:
        print(f"primary_source_hints: {', '.join(sorted(set(primary)))}")

    if total_hits == 0 and not primary:
        print("risk: low")
    elif total_hits <= 3 and len(primary) <= 2:
        print("risk: medium")
    else:
        print("risk: high")


if __name__ == "__main__":
    main()
