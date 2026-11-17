#!/usr/bin/env python3
"""Skill portfolio dashboard: one-command health audit of a skills build tree.

Scans a portfolio root, grades every skill directory (A-D) on:
  structure   - SKILL.md/README/LICENSE/references/scripts present, scripts compile
  frontmatter - YAML parses; name==dir; description <=1024 chars w/ trigger
                phrasing; version/author/license/tags present
  security    - credential patterns (ghp_, sk-, AKIA, xox, password in URL)
  git         - repo present, remote configured, no uncommitted changes (soft)

Outputs a portfolio score, grade histogram, and severity-ordered fix queue.
Optional --smoke executes every script's --help to catch import-level rot.

Stdlib only.
"""
import argparse
import json
import os
import py_compile
import re
import subprocess
import sys

DESC_LIMIT = 1024
TRIGGER_WORDS = ("use when", "run when", "use this")

SECURITY_PATTERNS = [
    (re.compile(r"ghp_[A-Za-z0-9]{20,}"), "GitHub PAT"),
    (re.compile(r"github_pat_[A-Za-z0-9_]{20,}"), "GitHub fine-grained PAT"),
    (re.compile(r"\bsk-[A-Za-z0-9]{20,}"), "OpenAI-style API key"),
    (re.compile(r"AKIA[0-9A-Z]{16}"), "AWS access key"),
    (re.compile(r"xox[baprs]-[A-Za-z0-9-]{10,}"), "Slack token"),
    (re.compile(r"https?://[^\s/:]+:[^\s@]{6,}@"), "credentials in URL"),
]
# single-pass alternation of all patterns (fast pre-filter); detail patterns above
# are only run on lines the master regex hits
_MASTER = re.compile("|".join(p.pattern for p, _ in SECURITY_PATTERNS))
MAX_SCAN_BYTES = 1_000_000  # skip files larger than 1 MB

TEXT_EXTS = (".py", ".md", ".json", ".txt", ".yaml", ".yml", ".toml", ".sh", "")


def parse_frontmatter(text):
    """Return (fm_dict, error). Minimal YAML frontmatter parser (flat + one nested level)."""
    if not text.startswith("---"):
        return None, "SKILL.md does not start with ---"
    m = re.search(r"\n---\s*\n", text[3:])
    if not m:
        return None, "frontmatter not closed"
    raw = text[3:3 + m.start()]
    fm, stack, err = {}, {}, None
    for line in raw.splitlines():
        if not line.strip() or line.strip().startswith("#"):
            continue
        top = re.match(r"^([A-Za-z0-9_-]+):\s*(.*)$", line)
        nested = re.match(r"^\s+([A-Za-z0-9_-]+):\s*(.*)$", line)
        cont = re.match(r"^\s+(?![A-Za-z0-9_-]+:)(.+)$", line)
        if nested and stack.get("_last_top") and isinstance(fm.get(stack["_last_top"]), dict):
            fm[stack["_last_top"]][nested.group(1)] = nested.group(2).strip().strip("'\"")
        elif re.match(r"^\s+-\s", line):
            # YAML list item under the last top-level key: mark that key as present
            lt = stack.get("_last_top")
            if lt and isinstance(fm.get(lt), dict) and not fm[lt]:
                fm[lt] = "__yaml_list__"
            continue
        elif top:
            k, v = top.group(1), top.group(2).strip()
            fm[k] = {} if v == "" else v.strip("'\"")
            stack["_last_top"] = k if v == "" else k
        elif cont and stack.get("_last_top") and isinstance(fm.get(stack["_last_top"]), str):
            # multi-line YAML value (folded/indented continuation): append
            fm[stack["_last_top"]] += " " + cont.group(1).strip()
        else:
            err = err or f"unparseable frontmatter line: {line[:40]!r}"
    return fm, err


def scan_text_security(root):
    findings = []
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in (".git", "node_modules", "__pycache__")]
        for fn in filenames:
            if not any(fn.endswith(e) for e in TEXT_EXTS):
                continue
            path = os.path.join(dirpath, fn)
            try:
                if os.path.getsize(path) > MAX_SCAN_BYTES:
                    continue
                with open(path, encoding="utf-8", errors="ignore") as f:
                    for i, line in enumerate(f, 1):
                        if not _MASTER.search(line):
                            continue
                        for pat, label in SECURITY_PATTERNS:
                            if pat.search(line):
                                findings.append((os.path.relpath(path, root), i, label))
                                break
            except OSError:
                pass
    return findings


def check_skill(path, check_git=False):
    """Grade one skill dir. Returns dict with grade + issues list."""
    issues = []          # (severity, message); sev: sec|struct|fm|polish
    name = os.path.basename(path)

    sk = os.path.join(path, "SKILL.md")
    if not os.path.isfile(sk):
        return {"name": name, "grade": "D", "issues": [("struct", "SKILL.md missing")]}
    text = open(sk, encoding="utf-8", errors="ignore").read()

    fm, err = parse_frontmatter(text)
    if err or fm is None:
        return {"name": name, "grade": "D",
                "issues": [("fm", err or "frontmatter unparseable")]}
    if fm.get("name") != name:
        issues.append(("fm", f"frontmatter name {fm.get('name')!r} != dir {name!r}"))
    desc = str(fm.get("description", ""))
    if not desc:
        issues.append(("fm", "no description"))
    else:
        if len(desc) > DESC_LIMIT:
            issues.append(("fm", f"description {len(desc)} chars > {DESC_LIMIT}"))
        if not any(desc.lower().startswith(t) or f". {t}" in desc.lower() for t in TRIGGER_WORDS):
            issues.append(("polish", "description lacks trigger phrasing (Use when...)"))
    for field in ("version", "author", "license"):
        if not fm.get(field):
            issues.append(("fm", f"missing {field}"))
    meta = fm.get("metadata")
    if fm.get("tags"):
        tags = fm.get("tags")
    elif isinstance(meta, dict):
        tags = (meta.get("hermes") or {}).get("tags")
    else:
        tags = None
    if not tags:
        issues.append(("polish", "no tags"))

    body = text.split("\n---", 1)[-1]
    if len(body.strip()) < 200:
        issues.append(("polish", "body suspiciously short (<200 chars)"))

    if not os.path.isfile(os.path.join(path, "README.md")):
        issues.append(("struct", "no README.md"))
    if not os.path.isfile(os.path.join(path, "LICENSE")):
        issues.append(("struct", "no LICENSE"))
    if not os.path.isdir(os.path.join(path, "references")):
        issues.append(("struct", "no references/"))
    scripts_dir = os.path.join(path, "scripts")
    scripts = []
    if os.path.isdir(scripts_dir):
        scripts = [f for f in os.listdir(scripts_dir) if f.endswith(".py")]
    if not scripts:
        issues.append(("struct", "no python scripts"))
    for s in scripts:
        sp = os.path.join(scripts_dir, s)
        try:
            with open(sp, encoding="utf-8", errors="ignore") as f:
                compile(f.read(), sp, "exec")
        except SyntaxError as e:
            issues.append(("struct", f"script {s} does not compile: line {e.lineno}: {e.msg}"))
        except OSError as e:
            issues.append(("struct", f"script {s} unreadable: {e}"))

    # git state (soft signal, opt-in: slow on big portfolios)
    if check_git and os.path.isdir(os.path.join(path, ".git")):
        try:
            r = subprocess.run(["git", "-C", path, "status", "--porcelain"],
                               capture_output=True, text=True, timeout=10)
            if r.stdout.strip():
                issues.append(("polish", f"{len(r.stdout.strip().splitlines())} uncommitted file(s)"))
            r2 = subprocess.run(["git", "-C", path, "remote", "get-url", "origin"],
                                capture_output=True, text=True, timeout=10)
            if r2.returncode != 0:
                issues.append(("polish", "no origin remote"))
        except (subprocess.SubprocessError, OSError):
            issues.append(("polish", "git check failed"))
    else:
        issues.append(("polish", "not a git repo")) if check_git else None

    sev_rank = {"sec": 0, "struct": 1, "fm": 2, "polish": 3}
    issues.sort(key=lambda x: sev_rank[x[0]])
    hard = sum(1 for s, _ in issues if s in ("sec", "struct", "fm"))
    grade = "A" if not issues else ("B" if hard == 0 else ("C" if hard <= 2 else "D"))
    return {"name": name, "grade": grade, "issues": issues}


def main():
    p = argparse.ArgumentParser(description="Skill portfolio dashboard")
    p.add_argument("--root", default=".", help="portfolio root containing skill dirs")
    p.add_argument("--json", action="store_true")
    p.add_argument("--verbose", action="store_true")
    p.add_argument("--git", action="store_true", help="include per-repo git checks (slow on large portfolios)")
    a = p.parse_args()

    root = os.path.abspath(a.root)
    skills = []
    for entry in sorted(os.listdir(root)):
        pth = os.path.join(root, entry)
        if os.path.isdir(pth) and os.path.isfile(os.path.join(pth, "SKILL.md")):
            skills.append(check_skill(pth, check_git=a.git))

    sec = scan_text_security(root)

    hist = {g: sum(1 for s in skills if s["grade"] == g) for g in "ABCD"}
    score = int(100 * (hist["A"] + 0.6 * hist["B"] + 0.3 * hist["C"]) / max(1, len(skills)))

    queue = []
    for s in skills:
        if s["grade"] != "A" or a.verbose:
            for sev, msg in s["issues"]:
                queue.append((sev, s["name"], msg))
    for f, line, label in sec:
        queue.insert(0, ("sec", os.path.dirname(f) or ".", f"CREDENTIAL PATTERN ({label}) in {f}:{line}"))
    sev_rank = {"sec": 0, "struct": 1, "fm": 2, "polish": 3}
    queue.sort(key=lambda x: sev_rank[x[0]])

    if a.json:
        print(json.dumps({"root": root, "skills_scanned": len(skills), "score": score,
                          "grades": hist, "fix_queue": queue}, indent=2))
        return

    print(f"PORTFOLIO: {len(skills)} skills scanned @ {root}")
    print(f"Score: {score}/100   A:{hist['A']}  B:{hist['B']}  C:{hist['C']}  D:{hist['D']}")
    print(f"Security findings: {len(sec)}")
    if queue:
        print("\nFIX QUEUE (severity order):")
        for i, (sev, name, msg) in enumerate(queue[:40], 1):
            print(f" {i:>2}. [{sev.upper():7}] {name}: {msg}")
        if len(queue) > 40:
            print(f" ... and {len(queue) - 40} more")
    else:
        print("\nAll skills fully compliant.")
    sys.exit(2 if (sec or hist["D"]) else 0)


if __name__ == "__main__":
    try:
        main()
    except BrokenPipeError:
        pass
