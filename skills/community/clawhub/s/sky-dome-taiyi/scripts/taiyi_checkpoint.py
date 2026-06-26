#!/usr/bin/env python3
"""Create a compact SkyDome Taiyi checkpoint markdown file."""
from __future__ import annotations
import argparse, datetime, re
from pathlib import Path

TEMPLATE = """# Checkpoint: {title}\n\nCreated: {created}\n\n## Goal\n\n- TODO\n\n## Current state\n\n- TODO\n\n## Decisions\n\n- TODO\n\n## Files changed\n\n- TODO\n\n## Evidence / tests\n\n- TODO\n\n## Open questions\n\n- TODO\n\n## Next actions\n\n- TODO\n\n## Risks\n\n- TODO\n"""

def slugify(text: str) -> str:
    text = re.sub(r"[^\w\u4e00-\u9fff-]+", "-", text.strip().lower())
    text = re.sub(r"-+", "-", text).strip("-")
    return text or "checkpoint"

parser = argparse.ArgumentParser()
parser.add_argument("title", nargs="?", default="taiyi")
parser.add_argument("--dir", default="context-checkpoints")
args = parser.parse_args()

out_dir = Path(args.dir)
out_dir.mkdir(parents=True, exist_ok=True)
now = datetime.datetime.now().strftime("%Y-%m-%d-%H%M%S")
path = out_dir / f"{now}-{slugify(args.title)}.md"
path.write_text(TEMPLATE.format(title=args.title, created=datetime.datetime.now().isoformat(timespec="seconds")), encoding="utf-8")
print(path)
