#!/usr/bin/env python3
"""Create a reusable campaign scaffold for a SOTA-oriented CV or DS effort."""

from __future__ import annotations

import argparse
import re
from datetime import datetime, timezone
from pathlib import Path


def slugify(value: str) -> str:
    cleaned = re.sub(r"[^A-Za-z0-9._-]+", "-", value.strip())
    return cleaned.strip("-") or "sota-campaign"


def write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", required=True, help="Directory under which the campaign folder will be created.")
    parser.add_argument("--campaign-id", required=True, help="Stable campaign identifier.")
    parser.add_argument("--title", required=True, help="Human-readable title.")
    args = parser.parse_args()

    campaign_id = slugify(args.campaign_id)
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%SZ")
    root = Path(args.root).expanduser().resolve() / campaign_id
    root.mkdir(parents=True, exist_ok=True)

    files = {
        "README.md": f"""# {args.title}

- campaign_id: `{campaign_id}`
- created_utc: `{now}`

## Benchmark Contract

- task:
- dataset:
- metric:
- split:
- target score:
- trusted baseline:

## Claim Threshold

- what qualifies as "match"
- what qualifies as "beat"
- what blocks a SOTA claim

## Runtime Contract

- local helpers and public artifacts
- no paid API keys by default

## Agent Roles

- main thread owns the benchmark contract
- bounded subagents for scouting, reproduction, and review
""",
        "program.md": """# Program

## Benchmark Contract

- task
- dataset
- metric
- split
- claim threshold
- minimum meaningful delta

## Baselines

- name / score / trust level

## Frontier Sources

- source / why it matters

## Rerun Rule

- small-delta threshold
- minimum reruns
- seed strategy
""",
        "agents.md": """# Agents

## Main Thread

- benchmark contract
- stop conditions
- final claim wording

## Bounded Subagents

- scout: paper, repo, and leaderboard triage
- reproducer: baseline and reference inspection
- reviewer: contamination, regressions, and evidence completeness

## Runtime Rule

- prefer local helpers and user-supplied artifacts
- treat paid API-key frameworks as reference-only by default
""",
        "research.md": """# Research

## Field Snapshot

- strongest references
- leaderboard notes
- benchmark caveats

## Reproduction Targets

- baseline
- public reference
""",
        "leaderboard.md": """# Leaderboard

## Contract

- task
- dataset
- metric
- split

## Current Table

- model / score / source / notes
""",
        "paper-triage.md": """# Paper Triage

## Must Read

- title / why it matters

## Worth Stealing

- trick / likely value / cheapest test

## Skip

- why it does not match the campaign
""",
        "plan.md": """# Plan

## Hypothesis Backlog

1. hypothesis

## Execution Order

1. reproduce baseline
2. reproduce strong reference
3. narrow ablations
4. stress best candidate
5. claim or hold
""",
        "journal.md": """# Journal

## Timeline

- timestamp / action / result / next step
""",
        "evidence.md": """# Evidence

## Benchmark Artifacts

- paths

## Browser Evidence

- urls
- screenshots

## Failure Cases

- notes
""",
        "claim.md": """# Claim

## Candidate

- id
- score
- delta vs baseline

## Review

- valid comparison?
- reproducible enough?
- regressions?

## Decision

- promote / hold / reject
""",
        "ablation-matrix.csv": "candidate_id,question,change_set,baseline_ref,score,delta,status,notes\n",
    }

    for name, content in files.items():
        write(root / name, content)

    print(root)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
