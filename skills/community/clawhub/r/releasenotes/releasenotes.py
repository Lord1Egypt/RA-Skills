#!/usr/bin/env python3
"""releasenotes — Generate release notes from git log. Zero dependencies."""
import subprocess, sys, argparse, re
from datetime import datetime
from collections import defaultdict

# Conventional Commits categories
CATEGORIES = {
    "feat": "✨ Features",
    "fix": "🐛 Bug Fixes",
    "perf": "⚡ Performance",
    "refactor": "♻️ Refactoring",
    "docs": "📚 Documentation",
    "test": "🧪 Tests",
    "build": "📦 Build",
    "ci": "🔧 CI/CD",
    "chore": "🔨 Chores",
    "style": "🎨 Style",
    "revert": "⏪ Reverts",
    "breaking": "💥 Breaking Changes",
}

def git_log(since=None, until=None, path="."):
    cmd = ["git", "-C", path, "log", "--pretty=format:%H|%s|%an|%aI", "--no-merges"]
    if since:
        cmd.append(f"--since={since}")
    if until:
        cmd.append(f"--until={until}")
    out = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
    if out.returncode != 0:
        print(f"Error: {out.stderr.strip()}", file=sys.stderr)
        sys.exit(1)
    commits = []
    for line in out.stdout.strip().split("\n"):
        if not line:
            continue
        parts = line.split("|", 3)
        if len(parts) >= 4:
            commits.append({"hash": parts[0][:8], "msg": parts[1], "author": parts[2], "date": parts[3][:10]})
    return commits

def categorize(commits):
    groups = defaultdict(list)
    for c in commits:
        msg = c["msg"]
        matched = False
        for prefix, label in CATEGORIES.items():
            pattern = rf'^{prefix}(\(.+?\))?[!:]?\s*'
            m = re.match(pattern, msg, re.IGNORECASE)
            if m:
                clean_msg = msg[m.end():].strip()
                scope = m.group(1) or ""
                if "!" in msg[:m.end()]:
                    groups["💥 Breaking Changes"].append({**c, "msg": f"{scope} {clean_msg}".strip()})
                groups[label].append({**c, "msg": f"{scope} {clean_msg}".strip()})
                matched = True
                break
        if not matched:
            groups["📝 Other"].append(c)
    return groups

def format_markdown(groups, title="Release Notes", version=None):
    lines = []
    header = f"# {title}"
    if version:
        header += f" — {version}"
    lines.append(header)
    lines.append(f"*Generated {datetime.now().strftime('%Y-%m-%d %H:%M')}*\n")
    
    for label in list(CATEGORIES.values()) + ["📝 Other"]:
        if label in groups:
            lines.append(f"## {label}\n")
            for c in groups[label]:
                lines.append(f"- {c['msg']} (`{c['hash']}` by {c['author']})")
            lines.append("")
    
    total = sum(len(v) for v in groups.values())
    lines.append(f"---\n*{total} commits*")
    return "\n".join(lines)

def main():
    p = argparse.ArgumentParser(prog="releasenotes", description="Generate release notes from git log")
    p.add_argument("--since", help="Start date (YYYY-MM-DD) or tag")
    p.add_argument("--until", help="End date")
    p.add_argument("--version", help="Version label")
    p.add_argument("--path", default=".", help="Git repo path")
    p.add_argument("-o", "--output", help="Output file")
    args = p.parse_args()

    commits = git_log(since=args.since, until=args.until, path=args.path)
    if not commits:
        print("No commits found.")
        return
    
    groups = categorize(commits)
    md = format_markdown(groups, version=args.version)
    
    if args.output:
        with open(args.output, "w") as f:
            f.write(md)
        print(f"✅ Written to {args.output} ({len(commits)} commits)")
    else:
        print(md)

if __name__ == "__main__":
    main()
