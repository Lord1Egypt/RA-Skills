#!/usr/bin/env python3
"""Create a Super SOP Node OS run folder."""

from __future__ import annotations

import argparse
import datetime as dt
import re
from pathlib import Path

CHAINS = {
    "research": ["intake", "context", "radar", "normalize", "score", "check", "sediment"],
    "implementation": ["intake", "context", "planning", "routing", "action", "test", "check", "handoff", "sediment"],
    "learning": ["intake", "context", "radar", "normalize", "learning", "test", "score", "check", "sediment"],
    "enterprise": ["intake", "context", "data", "planning", "action", "check", "handoff", "sediment"],
}

NODE_TITLES = {
    "intake": "Intake",
    "context": "Context / Memory",
    "radar": "Radar",
    "normalize": "Evidence Normalize",
    "data": "Data Modeling",
    "planning": "Planning",
    "routing": "Routing",
    "learning": "Learning",
    "action": "Action",
    "test": "Test",
    "score": "Score",
    "check": "Check",
    "handoff": "Handoff",
    "sediment": "Sediment",
}


def slugify(text: str) -> str:
    text = re.sub(r"[^a-z0-9\u4e00-\u9fff]+", "-", text.strip().lower())
    return re.sub(r"-+", "-", text).strip("-")[:80] or "node-run"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--goal", required=True)
    parser.add_argument("--type", choices=sorted(CHAINS), default="research")
    parser.add_argument("--root", default="runs")
    args = parser.parse_args()

    run_id = f"{dt.date.today().isoformat()}-{slugify(args.goal)}"
    run_dir = Path(args.root) / run_id
    run_dir.mkdir(parents=True, exist_ok=False)
    chain = CHAINS[args.type]

    (run_dir / "run.md").write_text(
        "# Node Run\n\n"
        f"**goal**: {args.goal}\n\n"
        f"**chain**: {' -> '.join(chain)}\n\n",
        encoding="utf-8",
    )

    for i, node in enumerate(chain, start=1):
        (run_dir / f"{i:02d}_{node}.md").write_text(
            f"# N{i:02d} · {NODE_TITLES[node]}\n\n"
            "## Purpose\n\n## Inputs\n\n## Work\n\n## Outputs\n\n## Check\n\n## Next\n",
            encoding="utf-8",
        )

    print(run_dir)


if __name__ == "__main__":
    main()

