#!/usr/bin/env python3
"""
Mine patterns from unified memory sources.
"""

import json
import re
from pathlib import Path
from collections import defaultdict
from datetime import datetime

MEMORY_DIR = Path(__file__).parent.parent / "memory"
PATTERNS_DIR = MEMORY_DIR / "patterns"
PATTERNS_DIR.mkdir(parents=True, exist_ok=True)


def mine_error_patterns():
    """Extract error patterns from all sources."""
    errors = []
    error_keywords = ["error", "failed", "exception", "crash", "timeout"]

    for source_dir in (MEMORY_DIR / "sources").iterdir():
        if not source_dir.is_dir():
            continue
        for f in source_dir.glob("*.jsonl"):
            with open(f) as fp:
                for line in fp:
                    if any(kw in line.lower() for kw in error_keywords):
                        errors.append(line.strip())

    pattern_file = PATTERNS_DIR / "errors" / f"{datetime.now().strftime('%Y-%m-%d')}.md"
    pattern_file.parent.mkdir(parents=True, exist_ok=True)

    with open(pattern_file, "w") as f:
        f.write(f"# Error Patterns - {datetime.now().date()}\n\n")
        f.write(f"Total errors found: {len(errors)}\n\n")
        for err in errors[:100]:  # Limit to 100
            f.write(f"- {err}\n")

    print(f"Mined {len(errors)} error patterns")


def mine_workflow_patterns():
    """Extract workflow patterns from Claude Code sessions."""
    workflows = []

    cc_dir = MEMORY_DIR / "sources" / "claude-code"
    if not cc_dir.exists():
        return

    for f in cc_dir.glob("*.jsonl"):
        with open(f) as fp:
            content = fp.read()
            # Look for tool sequences
            tools = re.findall(r'"tool":"(\w+)"', content)
            if len(tools) > 3:
                seq = " -> ".join(tools[:5])
                workflows.append(seq)

    pattern_file = PATTERNS_DIR / "workflows" / f"{datetime.now().strftime('%Y-%m-%d')}.md"
    pattern_file.parent.mkdir(parents=True, exist_ok=True)

    with open(pattern_file, "w") as f:
        f.write(f"# Workflow Patterns - {datetime.now().date()}\n\n")
        seen = set()
        for wf in workflows:
            if wf not in seen:
                seen.add(wf)
                f.write(f"- {wf}\n")

    print(f"Mined {len(seen)} workflow patterns")


def generate_index():
    """Generate unified memory index."""
    index_file = MEMORY_DIR / "index.md"

    with open(index_file, "w") as f:
        f.write("# Unified Memory Lake Index\n\n")
        f.write(f"Last updated: {datetime.now().isoformat()}\n\n")

        f.write("## Sources\n\n")
        for d in (MEMORY_DIR / "sources").iterdir():
            count = len(list(d.glob("*"))) - 1  # exclude .sync_state.json
            f.write(f"- {d.name}: {count} files\n")

        f.write("\n## Patterns\n\n")
        for d in PATTERNS_DIR.iterdir():
            count = len(list(d.glob("*")))
            f.write(f"- {d.name}: {count} entries\n")


if __name__ == "__main__":
    mine_error_patterns()
    mine_workflow_patterns()
    generate_index()
    print("Pattern mining complete")
