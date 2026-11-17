#!/usr/bin/env python3
"""scan_skills.py — Deterministic scan of an agent's skills directory.

Reads every SKILL.md frontmatter (name + description), extracts trigger
phrases and keywords, flags description-fitness issues, and pre-screens
keyword overlap between skill pairs. Semantic overlap judgment stays with
the agent — this script only provides the deterministic facts.

Usage:
  python3 scan_skills.py --dir ~/.openclaw/skills [--json]
Zero dependencies (stdlib only).
"""
import argparse
import json
import os
import re
import sys

STOP = set("""a an the use when user asks to for of in on with and or your you my
is are was were be being been it its this that these those all any some
what which who how why where can could should would will shall may might
do does did done not no yes if then else from by as at into out about
more most less least very just also only than then them they their there
here get got make made need needs want wants like""".split())


def parse_frontmatter(path):
    """Extract name/description from SKILL.md frontmatter (tolerant parser)."""
    try:
        text = open(path, encoding="utf-8", errors="replace").read(20000)
    except OSError:
        return None
    m = re.match(r"^---\s*\n(.*?)\n---\s*\n", text, re.S)
    if not m:
        return None
    fm = m.group(1)
    def field(key):
        mm = re.search(r"^%s:\s*[\"']?(.*?)[\"']?\s*$" % key, fm, re.M | re.I)
        return mm.group(1).strip() if mm else ""
    name = field("name") or os.path.basename(os.path.dirname(path))
    desc = field("description")
    # multi-line quoted description fallback: grab everything until closing quote
    if not desc:
        mm = re.search(r"description:\s*[\"'](.*?)[\"']", fm, re.S)
        desc = mm.group(1).strip() if mm else ""
    return {"name": name, "description": desc, "dir": os.path.dirname(path)}


def keywords(desc):
    words = re.findall(r"[a-zA-Z][a-zA-Z-]{2,}", desc.lower())
    return {w for w in words if w not in STOP}


def trigger_phrases(desc):
    """Sentences that look like activation rules."""
    parts = re.split(r"(?<=[.!?;])\s+|\s*[|;]\s*", desc)
    return [p.strip() for p in parts if re.search(r"\b(use|when|activate|trigger)\b", p, re.I)] or []


def fitness(desc):
    """Deterministic description-fitness flags."""
    issues = []
    if len(desc) < 60:
        issues.append("RED: description shorter than 60 chars — trigger accuracy at risk")
    if not trigger_phrases(desc):
        issues.append("YELLOW: no 'Use when'-style trigger phrase — the model must guess when to fire")
    if desc and not re.search(r"\b(use|when|for|after)\b", desc, re.I):
        issues.append("YELLOW: describes features, not scenarios — propose a rewrite")
    return issues


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dir", required=True, help="skills directory")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    skills = []
    for entry in sorted(os.listdir(args.dir)):
        p = os.path.join(args.dir, entry, "SKILL.md")
        if not os.path.isfile(p):
            continue
        fm = parse_frontmatter(p)
        if not fm:
            continue
        kw = keywords(fm["description"])
        skills.append({
            "name": fm["name"],
            "dir": entry,
            "description_chars": len(fm["description"]),
            "trigger_phrases": trigger_phrases(fm["description"]),
            "keywords": sorted(kw),
            "fitness_issues": fitness(fm["description"]),
        })

    # deterministic keyword-overlap pre-screen (agent does the semantic verdict)
    overlaps = []
    for i in range(len(skills)):
        for j in range(i + 1, len(skills)):
            a, b = set(skills[i]["keywords"]), set(skills[j]["keywords"])
            inter = a & b
            denom = min(len(a), len(b)) or 1
            ratio = len(inter) / denom
            if inter and ratio >= 0.4:
                overlaps.append({
                    "pair": [skills[i]["name"], skills[j]["name"]],
                    "shared_keywords": sorted(inter)[:12],
                    "overlap_ratio": round(ratio, 2),
                    "screen": "candidate-conflict" if ratio >= 0.6 else "watch",
                })

    out = {
        "scanned_dir": args.dir,
        "skills_found": len(skills),
        "skills": skills,
        "overlap_prescreen": overlaps,
        "notes": "keyword overlap is a pre-screen only; the agent makes the RED/YELLOW/GREEN semantic verdict",
    }
    print(json.dumps(out, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
