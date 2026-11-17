#!/usr/bin/env python3
"""
skill-benchmark.py - composite quality score for an OpenClaw/Hermes skill.

Runs skill-lint + prompt-lint style checks and returns a 0-100 benchmark with a
letter grade. Reuses the same heuristics as the standalone linters. Stdlib only.

Usage:
  python skill-benchmark.py score <folder> [--json]
  python skill-benchmark.py self-test
"""
import argparse
import json
import os
import re
import sys

REQUIRED = ["name", "version", "description"]
ROLE = re.compile(r'(?i)(you are|act as|your role)', re.I)
GOAL = re.compile(r'(?i)(goal|objective|task is|your job)', re.I)
OUTFMT = re.compile(r'(?i)(output|format|return|json|markdown)', re.I)
VAGUE = re.compile(r'\b(help|somehow|as needed|appropriately)\b', re.I)


def score(folder, as_json):
    issues = []
    skill = os.path.join(folder, "SKILL.md")
    if not os.path.isfile(skill):
        issues.append("missing SKILL.md")
    else:
        txt = open(skill, encoding="utf-8").read()
        m = re.match(r"^---\s*\n(.*?)\n---\s*\n", txt, re.S)
        if not m:
            issues.append("missing frontmatter")
        else:
            fm = m.group(1)
            for k in REQUIRED:
                if not re.search(rf"^{k}\s*:", fm, re.M):
                    issues.append(f"missing {k}")
        body = txt
        if not ROLE.search(body): issues.append("no role stated")
        if not GOAL.search(body): issues.append("no goal stated")
        if not OUTFMT.search(body): issues.append("no output format")
        issues += [f"vague: {v.group(0)}" for v in VAGUE.finditer(body)]
    # tool presence
    if not any(f.endswith(".py") for f in os.listdir(folder)):
        issues.append("no tool file (.py) present")
    score_val = max(0, 100 - len(issues) * 10)
    grade = "A" if score_val >= 90 else "B" if score_val >= 75 else "C" if score_val >= 60 else "D"
    res = {"folder": os.path.basename(folder), "score": score_val, "grade": grade, "issues": issues}
    if as_json:
        print(json.dumps(res, indent=2))
    else:
        print(f"{grade} ({score_val}/100)" + (" - clean" if not issues else " - " + "; ".join(issues)))
    return res


def self_test():
    import tempfile, shutil
    d = tempfile.mkdtemp()
    open(os.path.join(d, "SKILL.md"), "w").write(
        "---\nname: x\nversion: 1.0.0\ndescription: y\n---\nYou are a helper. Goal: assist. Output: markdown.\n")
    open(os.path.join(d, "tool.py"), "w").write("print(1)\n")
    good = score(d, False)
    shutil.rmtree(d)
    bad_d = tempfile.mkdtemp()
    open(os.path.join(bad_d, "README.md"), "w").write("no skill")
    bad = score(bad_d, False)
    shutil.rmtree(bad_d)
    ok = good["grade"] in ("A", "B") and bad["score"] < good["score"]
    print("self-test:", "PASS" if ok else "FAIL", f"(good={good['score']} bad={bad['score']})")
    return 0 if ok else 1


def main():
    p = argparse.ArgumentParser(description="skill-benchmark")
    sub = p.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("score"); s.add_argument("folder"); s.add_argument("--json", action="store_true")
    sub.add_parser("self-test")
    a = p.parse_args()
    if a.cmd == "self-test": return self_test()
    if a.cmd == "score": score(a.folder, a.json); return 0


if __name__ == "__main__":
    sys.exit(main())
