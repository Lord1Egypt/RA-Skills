#!/usr/bin/env python3
"""
session-wrap-up-premium — flush, commit, push, PARA update
"""

import json
import sys
import os
import subprocess
from pathlib import Path
from datetime import datetime

WORKSPACE = Path.cwd()
MEMORY_DIR = WORKSPACE / "memory"
NOTES_DIR = WORKSPACE / "notes" / "areas"
TODAY = datetime.now().strftime("%Y-%m-%d")
DAILY_LOG = MEMORY_DIR / f"{TODAY}.md"
MEMORY_FILE = WORKSPACE / "MEMORY.md"
OPEN_LOOPS = NOTES_DIR / "open-loops.md"

def run(cmd):
    res = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    return res.returncode, res.stdout, res.stderr

def ensure_dirs():
    MEMORY_DIR.mkdir(exist_ok=True)
    NOTES_DIR.mkdir(parents=True, exist_ok=True)

def read_recent_daily_log(lines=200):
    if not DAILY_LOG.exists():
        return ""
    with open(DAILY_LOG) as f:
        all_lines = f.readlines()
    return "".join(all_lines[-lines:])

def flush_to_daily_log(summary_text: str):
    ensure_dirs()
    if not DAILY_LOG.exists():
        with open(DAILY_LOG, "w") as f:
            f.write(f"# {TODAY} — Session Log\n\n")
    with open(DAILY_LOG, "a") as f:
        f.write(f"\n## Session Wrap-Up — {datetime.now().strftime('%H:%M')}\n\n{summary_text}\n")
    return True

def update_memory(highlights: list):
    if not MEMORY_FILE.exists():
        with open(MEMORY_FILE, "w") as f:
            f.write("# MEMORY.md — Curated Long-term Memory\n\n")
    with open(MEMORY_FILE, "a") as f:
        f.write(f"\n## {TODAY}\n")
        for item in highlights:
            f.write(f"- **{item['type']}**: {item['content']}\n")
    return True

def update_open_loops(loops: list):
    ensure_dirs()
    if not OPEN_LOOPS.exists():
        OPEN_LOOPS.write_text("# Open Loops\n\nUnfinished items from sessions.\n\n")
    # Mark any completed loops if mentioned in loops with ✅ prefix
    new_content = []
    with open(OPEN_LOOPS) as f:
        for line in f:
            new_content.append(line)
    for loop in loops:
        status = "✅ " if loop.get("done") else "- "
        new_content.append(f"{status}{loop['content']}\n")
    with open(OPEN_LOOPS, "w") as f:
        f.writelines(new_content)
    return True

def git_commit_push(message: str):
    # Check if git repo
    if not (WORKSPACE / ".git").exists():
        return False, "not a git repo"
    # Add all
    code, out, err = run("git add -A")
    if code != 0:
        return False, f"git add failed: {err}"
    # Commit
    code, out, err = run(f'git commit -m "{message}"')
    if code not in (0, 1):  # 1 means nothing to commit
        return False, f"git commit failed: {err}"
    # Push
    code, out, err = run("git push")
    if code != 0 and "Everything up-to-date" not in err:
        return False, f"git push failed: {err}"
    return True, "ok"

def generate_summary_from_recent():
    # Simple summary from last hour of daily log (simulate)
    recent = read_recent_daily_log(lines=100)
    # Extract sections by regex (very basic)
    topics = []
    decisions = []
    problems = []
    lessons = []
    loops = []
    for line in recent.split("\n"):
        if "**Key topics:**" in line or line.startswith("Topics:"):
            topics.append(recent.split("**Key topics:**")[1].split("\n")[0])
        if "**Decisions:**" in line:
            decisions.append(line.split("**Decisions:**")[1].strip())
        if "**Problems solved:**" in line:
            problems.append(line.split("**Problems solved:**")[1].strip())
        if "**Lessons learned:**" in line:
            lessons.append(line.split("**Lessons learned:**")[1].strip())
        if "**Open loops:**" in line:
            loops.append(line.split("**Open loops:**")[1].strip())
    # Fallback: if empty, just capture last few lines
    if not any([topics, decisions, problems, lessons, loops]):
        # Take last 5 non-empty lines as topics
        lines = [l.strip() for l in recent.split("\n") if l.strip()][-5:]
        topics = lines
    return {
        "topics": topics[:5],
        "decisions": decisions[:5],
        "problems": problems[:5],
        "lessons": lessons[:5],
        "loops": loops[:10]
    }

def main():
    if len(sys.argv) < 2:
        print("Usage: run.py [wrap_up|generate_summary|para_update] [json_input]")
        sys.exit(1)

    action = sys.argv[1]
    input_data = json.loads(sys.argv[2]) if len(sys.argv) > 2 else {}

    if action == "wrap_up":
        # 1. Generate summary from recent daily log (or create one if empty)
        summary = generate_summary_from_recent()
        summary_text = f"""**Key topics:** {', '.join(summary['topics'])}\n\n**Decisions:** {', '.join(summary['decisions'])}\n\n**Problems solved:** {', '.join(summary['problems'])}\n\n**Lessons learned:** {', '.join(summary['lessons'])}\n\n**Open loops:**\n"""
        for loop in summary['loops']:
            summary_text += f"- {loop}\n"

        # 2. Flush to daily log
        flush_to_daily_log(summary_text)

        # 3. Update MEMORY with highlights (convert)
        highlights = []
        for t in summary['topics']:
            highlights.append({"type": "topic", "content": t})
        for d in summary['decisions']:
            highlights.append({"type": "decision", "content": d})
        for l in summary['lessons']:
            highlights.append({"type": "lesson", "content": l})
        if highlights:
            update_memory(highlights)

        # 4. Update open-loops
        loops = [{"content": l, "done": False} for l in summary['loops']]
        if loops:
            update_open_loops(loops)

        # 5. Git commit + push
        commit_msg = input_data.get("commit_message") or f"wrap-up: {TODAY} session summary"
        success, msg = git_commit_push(commit_msg)

        # 6. Report
        report = f"""## Session Wrap-Up Complete ✅

**Captured to daily log:** ({len(summary['topics'])} topics, {len(decisions)} decisions)
**Updated:** MEMORY.md (added {len(highlights)} items)
**PARA:** open-loops.md ({len(loops)} items)
**Committed:** {commit_msg}
**Pushed:** {"✅" if success else "❌ " + msg}

Ready for new session! ⚡"""
        print(report)

    elif action == "generate_summary":
        source = input_data.get("source", "today")
        summary = generate_summary_from_recent()
        print(json.dumps(summary))
    elif action == "para_update":
        section = input_data["section"]
        content = input_data["content"]
        mode = input_data.get("mode", "append")
        success = update_open_loops([{"content": content, "done": False}])
        print(json.dumps({"status": "ok" if success else "error"}))
    else:
        print(json.dumps({"error": f"unknown action: {action}"}))
        sys.exit(1)

if __name__ == "__main__":
    main()