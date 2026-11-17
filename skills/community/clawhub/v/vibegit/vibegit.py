#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
vibegit — how much of this repository looks AI-assisted (and how sloppy is it)?

Read-only analysis of git history. Zero dependencies, no network, no file
contents: only commit metadata and numstat are read.

Outputs a 0-100 slop score, an AI-assistance estimate (confirmed vs likely),
top signals, a Markdown/JSON report, a shareable card, and an SVG badge.

Exit codes: 0 ok, 1 score gate failed (--max-score), 2 not a git repo, 4 git error.
"""

import argparse
import json
import os
import re
import subprocess
import sys

__version__ = "1.0.3"

AI_TOOLS = [
    "claude", "copilot", "cursor", "codex", "aider", "devin", "gemini",
    "codeium", "tabnine", "sweep", "windsurf", "qodo", "openhands", "cline",
    "continue", "amazon q", "sourcegraph cody", "roo code", "zed ai",
]

BOT_RE = re.compile(
    r"(\[bot\]|dependabot|renovate|github-actions|gitlab-ci|pre-commit-ci|snyk-bot|greenkeeper)",
    re.IGNORECASE)

TRAILER_RE = re.compile(
    r"(?im)^(co-authored-by|assisted-by|generated-by|ai-assisted-by)\s*:\s*(.+)$")

GENERATED_RE = re.compile(
    r"(?i)(generated|written|assisted|powered)\s+(with|by)\s+\[?("
    + "|".join(re.escape(t) for t in AI_TOOLS) + r")\b")

SHORT_MSG_RE = re.compile(
    r"(?i)^(wip|fix|fixes|update|updates|changes?|stuff|misc|tmp|temp|test|tests|"
    r"typo|oops|cleanup)\.{0,3}$")

TEST_PATH_RE = re.compile(
    r"(^|/)(tests?|spec|__tests__|__snapshots__)(/|$)|"
    r"(^|/)(test_[^/]+|[^/]+_test\.[a-z]+|[^/]+\.(test|spec)\.[a-z]+)$",
    re.IGNORECASE)

LOCKFILES = {
    "package-lock.json", "yarn.lock", "pnpm-lock.yaml", "bun.lockb",
    "poetry.lock", "pipfile.lock", "uv.lock", "cargo.lock", "go.sum",
    "composer.lock", "gemfile.lock", "mix.lock", "flake.lock",
}

VERDICTS = [
    (14, "Clean", "green"),
    (34, "Mild slop", "yellow"),
    (59, "Slop", "orange"),
    (100, "Heavy slop", "red"),
]


# ---------------------------------------------------------------- git access
def run_git(repo, args, timeout=180):
    proc = subprocess.run(
        ["git", "-C", repo] + list(args),
        stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        text=True, encoding="utf-8", errors="replace", timeout=timeout,
    )
    return proc


def git_ok(repo, args):
    proc = run_git(repo, args)
    if proc.returncode != 0:
        detail = (proc.stderr or proc.stdout).strip().splitlines()
        return None, detail[0] if detail else "git failed"
    return proc.stdout, None


def repo_info(repo):
    top, err = git_ok(repo, ["rev-parse", "--show-toplevel"])
    if err:
        return None
    branch, _ = git_ok(repo, ["rev-parse", "--abbrev-ref", "HEAD"])
    return {"root": top.strip(), "branch": (branch or "").strip() or "HEAD"}


def range_args(since, until, include_merges):
    args = []
    if not include_merges:
        args.append("--no-merges")
    if since:
        args += ["--since", since]
    if until:
        args += ["--until", until]
    return args


def load_commits(repo, since=None, until=None, include_merges=False):
    """Return a list of commit dicts (metadata + numstat totals)."""
    rng = range_args(since, until, include_merges)
    fmt = "%x1e%H%x1f%an%x1f%ae%x1f%ad%x1f%P%x1f%B"
    meta_out, err = git_ok(repo, ["log", "--date=short", "--format=" + fmt] + rng)
    if err:
        raise RuntimeError(err)

    commits = []
    for record in meta_out.split("\x1e"):
        record = record.strip("\n")
        if not record.strip():
            continue
        parts = record.split("\x1f", 5)
        if len(parts) < 6:
            continue
        h, an, ae, ad, parents, body = parts
        commits.append({
            "hash": h.strip(), "author": an.strip(), "email": ae.strip(),
            "date": ad.strip(), "parents": parents.split(),
            "body": body, "subject": body.strip().splitlines()[0] if body.strip() else "",
            "files": [], "insertions": 0, "deletions": 0,
        })

    num_out, err = git_ok(repo, ["log", "--numstat", "--format=%x1e%H"] + rng)
    if err:
        raise RuntimeError(err)

    stats = {}
    current = None
    for line in num_out.split("\n"):
        if line.startswith("\x1e"):
            current = line[1:].strip()
            stats[current] = {"files": [], "insertions": 0, "deletions": 0}
            continue
        if not current or not line.strip():
            continue
        cells = line.split("\t")
        if len(cells) < 3:
            continue
        add, dele, path = cells[0], cells[1], cells[2]
        if add == "-" or dele == "-":
            continue
        stats[current]["files"].append(path)
        stats[current]["insertions"] += int(add)
        stats[current]["deletions"] += int(dele)

    for commit in commits:
        s = stats.get(commit["hash"])
        if s:
            commit.update(s)
    return commits


# ---------------------------------------------------------------- analysis
def ai_tool_in(text):
    low = (text or "").lower()
    for tool in AI_TOOLS:
        if re.search(r"(?<![a-z0-9])" + re.escape(tool) + r"(?![a-z0-9])", low):
            return tool
    return None


def classify(commit):
    """Return (level, tool) where level in {bot, confirmed, likely, none}."""
    who = "%s <%s>" % (commit["author"], commit["email"])
    if BOT_RE.search(who):
        return "bot", None
    tool = ai_tool_in(who)
    if tool:
        return "confirmed", tool
    body = commit["body"] or ""
    for m in TRAILER_RE.finditer(body):
        tool = ai_tool_in(m.group(2))
        if tool:
            return "confirmed", tool
    m = GENERATED_RE.search(body) or GENERATED_RE.search(commit["subject"])
    if m:
        return "confirmed", m.group(3).lower()
    if body.lstrip().lower().startswith("aider:"):
        return "confirmed", "aider"
    if "🤖" in body:
        return "confirmed", "ai"
    tool = ai_tool_in(body)
    if tool:
        return "likely", tool
    return "none", None


def verdict_for(score):
    for limit, label, color in VERDICTS:
        if score <= limit:
            return label, color
    return VERDICTS[-1][1], VERDICTS[-1][2]


def analyze(commits):
    total = len(commits)
    confirmed = likely = bots = 0
    tools = {}
    authors = {}
    giant = short = testdel = lock_only = 0
    file_edits = {}
    unique_files = set()
    monthly = {}

    for c in commits:
        level, tool = classify(c)
        if level == "bot":
            bots += 1
            continue
        if level == "confirmed":
            confirmed += 1
            tools[tool] = tools.get(tool, 0) + 1
        elif level == "likely":
            likely += 1
            tools[tool] = tools.get(tool, 0) + 1

        authors[c["author"]] = authors.get(c["author"], 0) + 1
        changed = c["insertions"] + c["deletions"]
        if changed > 400:
            giant += 1
        if SHORT_MSG_RE.match(c["subject"].strip()) or len(c["subject"].strip()) < 15:
            short += 1

        files = c["files"]
        if files:
            names = {os.path.basename(f).lower() for f in files}
            if names and names.issubset(LOCKFILES):
                lock_only += 1
            for f in files:
                unique_files.add(f)
                file_edits[f] = file_edits.get(f, 0) + 1

        for f in files:
            if TEST_PATH_RE.search(f) and c["deletions"] > 0 and c["insertions"] == 0 and not os.path.basename(f).lower() in LOCKFILES:
                testdel += 1
                break

        month = (c["date"] or "")[:7]
        if month:
            m = monthly.setdefault(month, {"commits": 0, "ai": 0})
            m["commits"] += 1
            if level in ("confirmed", "likely"):
                m["ai"] += 1

    human = max(total - bots, 1)
    confirmed_pct = confirmed / human * 100
    likely_pct = likely / human * 100
    ai_estimate = confirmed_pct + likely_pct * 0.5
    giant_pct = giant / human * 100
    short_pct = short / human * 100
    lock_pct = lock_only / human * 100
    churn_files = sum(1 for n in file_edits.values() if n > 5)
    churn_pct = (churn_files / len(unique_files) * 100) if unique_files else 0.0

    parts = {
        "ai_assistance": min(ai_estimate, 60) / 60 * 30,
        "giant_commits": min(giant_pct, 40) / 40 * 10,
        "short_messages": min(short_pct, 40) / 40 * 10,
        "test_deletions": min(testdel * 4, 20),
        "file_churn": min(churn_pct, 30) / 30 * 15,
        "lockfile_only": min(lock_pct, 15) / 15 * 15,
    }
    score = int(round(min(100, max(0, sum(parts.values())))))
    label, color = verdict_for(score)

    return {
        "total_commits": total,
        "bot_commits": bots,
        "ai": {
            "confirmed": confirmed, "likely": likely,
            "confirmed_pct": round(confirmed_pct, 1),
            "likely_pct": round(likely_pct, 1),
            "estimate_pct": round(ai_estimate, 1),
            "confidence": "high" if human >= 50 else ("medium" if human >= 15 else "low"),
            "tools": dict(sorted(tools.items(), key=lambda kv: -kv[1])),
        },
        "signals": {
            "giant_commits": huge_count(giant, giant_pct),
            "short_messages": huge_count(short, short_pct),
            "test_deletions": testdel,
            "churn_files": churn_files,
            "churn_pct": round(churn_pct, 1),
            "lockfile_only": lock_only,
            "unique_files": len(unique_files),
        },
        "score_parts": {k: round(v, 1) for k, v in parts.items()},
        "score": score,
        "verdict": label,
        "color": color,
        "authors": dict(sorted(authors.items(), key=lambda kv: -kv[1])[:10]),
        "monthly": dict(sorted(monthly.items())[-12:]),
    }


def huge_count(n, pct):
    return {"count": n, "pct": round(pct, 1)}


# ---------------------------------------------------------------- rendering
def fmt_pct(v):
    return ("%.1f" % v).rstrip("0").rstrip(".")


def card(report, info):
    s = report["signals"]
    ai = report["ai"]
    lines = []
    lines.append("+-- vibegit " + "-" * 52)
    lines.append("| repo      %s (%s)" % (os.path.basename(info["root"]), info["branch"]))
    lines.append("| commits   %d%s" % (report["total_commits"],
                                      "  [%d bot]" % report["bot_commits"] if report["bot_commits"] else ""))
    lines.append("| slop      %d/100  %s" % (report["score"], report["verdict"]))
    lines.append("| AI-assist ~%s%%  (confirmed %s%% / likely %s%%, %s confidence)" % (
        fmt_pct(ai["estimate_pct"]), fmt_pct(ai["confirmed_pct"]),
        fmt_pct(ai["likely_pct"]), ai["confidence"]))
    lines.append("+-- top signals " + "-" * 46)
    rows = [
        ("AI assistance", "%.1f pts" % report["score_parts"]["ai_assistance"]),
        ("giant commits", "%s%% (%d) -> %.1f pts" % (fmt_pct(s["giant_commits"]["pct"]),
                                                     s["giant_commits"]["count"],
                                                     report["score_parts"]["giant_commits"])),
        ("short messages", "%s%% (%d) -> %.1f pts" % (fmt_pct(s["short_messages"]["pct"]),
                                                      s["short_messages"]["count"],
                                                      report["score_parts"]["short_messages"])),
        ("test deletions", "%d commits -> %.1f pts" % (s["test_deletions"],
                                                       report["score_parts"]["test_deletions"])),
        ("file churn", "%s%% of files (>5 edits) -> %.1f pts" % (fmt_pct(s["churn_pct"]),
                                                                 report["score_parts"]["file_churn"])),
        ("lockfile-only", "%d commits -> %.1f pts" % (s["lockfile_only"],
                                                      report["score_parts"]["lockfile_only"])),
    ]
    for name, detail in rows:
        lines.append("| %-16s %s" % (name, detail))
    if ai["tools"]:
        lines.append("+-- AI tools " + "-" * 48)
        lines.append("| " + ", ".join("%s x%d" % (k, v) for k, v in ai["tools"].items()))
    lines.append("+-- share " + "-" * 50)
    lines.append("| " + share_line(report, info))
    lines.append("+" + "-" * 62)
    return "\n".join(lines)


def share_line(report, info):
    ai = report["ai"]
    return "vibegit · %s: slop %d/100 (%s) · AI-assisted ~%s%%" % (
        os.path.basename(info["root"]), report["score"], report["verdict"],
        fmt_pct(ai["estimate_pct"]))


def markdown(report, info):
    s, ai = report["signals"], report["ai"]
    out = ["# vibegit report", "",
           "**Repository:** `%s` (%s)  " % (os.path.basename(info["root"]), info["branch"]),
           "**Slop score:** **%d/100** — %s  " % (report["score"], report["verdict"]),
           "**AI-assisted estimate:** ~%s%% (confirmed %s%%, likely %s%%, %s confidence)  " % (
               fmt_pct(ai["estimate_pct"]), fmt_pct(ai["confirmed_pct"]),
               fmt_pct(ai["likely_pct"]), ai["confidence"]),
           "**Commits:** %d (%d bot/automation)" % (report["total_commits"], report["bot_commits"]),
           "", "| Signal | Value | Points |", "|---|---|---|"]
    out.append("| AI assistance | ~%s%% | %.1f |" % (fmt_pct(ai["estimate_pct"]),
                                                   report["score_parts"]["ai_assistance"]))
    out.append("| Giant commits | %s%% (%d) | %.1f |" % (fmt_pct(s["giant_commits"]["pct"]),
                                                        s["giant_commits"]["count"],
                                                        report["score_parts"]["giant_commits"]))
    out.append("| Short messages | %s%% (%d) | %.1f |" % (fmt_pct(s["short_messages"]["pct"]),
                                                         s["short_messages"]["count"],
                                                         report["score_parts"]["short_messages"]))
    out.append("| Test deletions | %d | %.1f |" % (s["test_deletions"],
                                                  report["score_parts"]["test_deletions"]))
    out.append("| File churn | %s%% of files | %.1f |" % (fmt_pct(s["churn_pct"]),
                                                        report["score_parts"]["file_churn"]))
    out.append("| Lockfile-only commits | %d | %.1f |" % (s["lockfile_only"],
                                                         report["score_parts"]["lockfile_only"]))
    if ai["tools"]:
        out += ["", "**AI tools detected:** " + ", ".join("%s (%d)" % (k, v) for k, v in ai["tools"].items())]
    out += ["", "> " + share_line(report, info), "",
            "_Estimate only: vibegit reads commit metadata, not file contents. "
            "It does not prove authorship._"]
    return "\n".join(out)


def svg_badge(report):
    color = {"green": "#2ea043", "yellow": "#d29922", "orange": "#db6d28", "red": "#da3633"}[report["color"]]
    label = "vibegit"
    value = "%d/100 %s" % (report["score"], report["verdict"])
    lw, vw = 58, 18 + len(value) * 7
    width = lw + vw
    return (
        '<svg xmlns="http://www.w3.org/2000/svg" width="%d" height="20" role="img" '
        'aria-label="%s: %s">\n'
        '  <title>%s: %s</title>\n'
        '  <rect width="%d" height="20" rx="3" fill="#1f2328"/>\n'
        '  <rect x="%d" width="%d" height="20" rx="3" fill="%s"/>\n'
        '  <g fill="#fff" font-family="Verdana,Geneva,DejaVu Sans,sans-serif" font-size="11">\n'
        '    <text x="8" y="14">%s</text>\n'
        '    <text x="%d" y="14">%s</text>\n'
        '  </g>\n'
        '</svg>\n'
    ) % (width, label, value, label, value, width, lw, vw, color, label, lw + 8, value)


# ---------------------------------------------------------------- main
def main(argv=None):
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8", errors="replace")
        except (AttributeError, OSError):
            pass

    ap = argparse.ArgumentParser(
        prog="vibegit",
        description="Estimate AI-assisted commits and slop signals from git history. "
                    "Read-only: commit metadata only, never file contents.")
    ap.add_argument("path", nargs="?", default=".", help="repository path (default: .)")
    ap.add_argument("--since", help="git --since value (e.g. '90 days ago', '2025-01-01')")
    ap.add_argument("--until", help="git --until value")
    ap.add_argument("--include-merges", action="store_true", help="count merge commits too")
    ap.add_argument("--format", choices=["text", "card", "md", "json", "badge"], default="text")
    ap.add_argument("--badge", metavar="FILE", help="write an SVG badge to FILE")
    ap.add_argument("--share", action="store_true", help="print only the shareable one-liner")
    ap.add_argument("--max-score", type=int, metavar="N",
                    help="exit 1 when the slop score is greater than N (CI gate)")
    ap.add_argument("--top", type=int, default=10, help="number of authors to show (default 10)")
    ap.add_argument("--version", action="version", version="vibegit %s" % __version__)
    args = ap.parse_args(argv)

    info = repo_info(args.path)
    if not info:
        print("vibegit: not a git repository: %s" % args.path, file=sys.stderr)
        return 2
    try:
        commits = load_commits(info["root"], args.since, args.until, args.include_merges)
    except (RuntimeError, subprocess.SubprocessError, OSError) as exc:
        print("vibegit: git error: %s" % exc, file=sys.stderr)
        return 4
    if not commits:
        print("vibegit: no commits found in range", file=sys.stderr)
        return 2

    report = analyze(commits)
    report["authors"] = dict(list(report["authors"].items())[:max(1, args.top)])

    if args.share:
        print(share_line(report, info))
    elif args.format == "json":
        out = {"tool": "vibegit", "version": __version__,
               "repo": os.path.basename(info["root"]), "branch": info["branch"],
               "since": args.since, "until": args.until, **report}
        print(json.dumps(out, indent=2, ensure_ascii=False))
    elif args.format == "md":
        print(markdown(report, info))
    elif args.format == "badge":
        print(svg_badge(report).rstrip("\n"))
    elif args.format == "card":
        print(card(report, info))
    else:
        print(card(report, info))

    if args.badge:
        with open(args.badge, "w", encoding="utf-8") as fh:
            fh.write(svg_badge(report))

    if args.max_score is not None and report["score"] > args.max_score:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
