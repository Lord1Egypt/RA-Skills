#!/usr/bin/env python3
"""Scan feedback files and generate evolution proposals.

Usage:
    python scripts/evolution_runner.py --feedback-dir .claude/feedback

This script intentionally generates suggestions only. It never edits rule files.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import defaultdict
from dataclasses import dataclass, field
from pathlib import Path


LOW_SCORE_THRESHOLD = 2
AVG_SCORE_THRESHOLD = 3
RULE_GRADUATION_THRESHOLD = 3
NEW_SKILL_THRESHOLD = 5


@dataclass
class FeedbackItem:
    path: Path
    title: str
    description: str = ""
    occurrences: int = 1
    graduated: bool = False
    skipped: bool = False
    source_skill: str = "N/A"
    proposal_hint: str = "auto"
    scores: dict[str, int] = field(default_factory=dict)
    evidence: str = ""


def parse_bool(value: str) -> bool:
    return value.strip().lower() == "true"


def parse_frontmatter(text: str) -> tuple[dict[str, object], str]:
    if not text.startswith("---\n"):
        return {}, text

    parts = text.split("---\n", 2)
    if len(parts) < 3:
        return {}, text

    raw_frontmatter = parts[1]
    body = parts[2]
    data: dict[str, object] = {}
    current_parent: str | None = None

    for line in raw_frontmatter.splitlines():
        if not line.strip():
            continue

        nested = re.match(r"^\s{2}([A-Za-z_]+):\s*(.+)$", line)
        if nested and current_parent:
            parent = data.setdefault(current_parent, {})
            if isinstance(parent, dict):
                parent[nested.group(1)] = nested.group(2).strip().strip('"')
            continue

        top = re.match(r"^([A-Za-z_]+):\s*(.*)$", line)
        if not top:
            continue

        key, raw_value = top.group(1), top.group(2).strip()
        if raw_value == "":
            data[key] = {}
            current_parent = key
            continue

        current_parent = None
        if raw_value.isdigit():
            data[key] = int(raw_value)
        elif raw_value.lower() in {"true", "false"}:
            data[key] = parse_bool(raw_value)
        else:
            data[key] = raw_value.strip('"')

    return data, body


def parse_feedback_file(path: Path) -> FeedbackItem:
    text = path.read_text(encoding="utf-8")
    frontmatter, body = parse_frontmatter(text)

    title_match = re.search(r"^#\s+(.+)$", body, re.MULTILINE)
    title = title_match.group(1).strip() if title_match else path.stem
    scores = {}
    raw_scores = frontmatter.get("scores", {})
    if isinstance(raw_scores, dict):
        for key, value in raw_scores.items():
            if str(value).isdigit():
                scores[key] = int(str(value))

    evidence = ""
    if isinstance(raw_scores, dict):
        evidence = str(raw_scores.get("evidence", ""))

    return FeedbackItem(
        path=path,
        title=title,
        description=str(frontmatter.get("description", "")),
        occurrences=int(frontmatter.get("occurrences", 1) or 1),
        graduated=bool(frontmatter.get("graduated", False)),
        skipped=bool(frontmatter.get("skipped", False)),
        source_skill=str(frontmatter.get("source_skill", "N/A")),
        proposal_hint=str(frontmatter.get("proposal_hint", "auto")),
        scores=scores,
        evidence=evidence,
    )


def detect_rule_graduations(items: list[FeedbackItem]) -> list[dict[str, object]]:
    proposals = []
    for item in items:
        if item.proposal_hint == "new_skill":
            continue
        if item.occurrences >= RULE_GRADUATION_THRESHOLD and not item.graduated and not item.skipped:
            target = f"{item.source_skill}/SKILL.md" if item.source_skill != "N/A" else "CLAUDE.md"
            proposals.append(
                {
                    "type": "rule_graduation",
                    "title": item.title,
                    "occurrences": item.occurrences,
                    "source_skill": item.source_skill,
                    "target_file": target,
                    "summary": item.description or item.title,
                    "feedback_file": str(item.path),
                }
            )
    return proposals


def detect_skill_optimizations(items: list[FeedbackItem]) -> list[dict[str, object]]:
    grouped: dict[str, list[FeedbackItem]] = defaultdict(list)
    proposals = []

    for item in items:
        if item.source_skill and item.source_skill != "N/A":
            grouped[item.source_skill].append(item)

    for skill_name, skill_items in grouped.items():
        score_history: dict[str, list[int]] = defaultdict(list)
        occurrences_sum = 0
        evidence = []

        for item in skill_items:
            occurrences_sum += item.occurrences
            if item.evidence:
                evidence.append(item.evidence)
            for dimension, score in item.scores.items():
                score_history[dimension].append(score)

        triggered_dimensions = []
        for dimension, values in score_history.items():
            if len(values) >= 3 and all(v <= LOW_SCORE_THRESHOLD for v in values[-3:]):
                triggered_dimensions.append(
                    {
                        "dimension": dimension,
                        "reason": f"连续 3 次 <= {LOW_SCORE_THRESHOLD}",
                        "values": values[-3:],
                    }
                )
                continue

            if len(values) >= 5:
                recent = values[-5:]
                avg_score = sum(recent) / len(recent)
                if avg_score <= AVG_SCORE_THRESHOLD:
                    triggered_dimensions.append(
                        {
                            "dimension": dimension,
                            "reason": f"最近 5 次平均分 <= {AVG_SCORE_THRESHOLD}",
                            "values": recent,
                            "average": round(avg_score, 2),
                        }
                    )

        if triggered_dimensions or occurrences_sum >= 5:
            proposals.append(
                {
                    "type": "skill_optimization",
                    "skill_name": skill_name,
                    "occurrences_sum": occurrences_sum,
                    "low_score_dimensions": triggered_dimensions,
                    "evidence": evidence[:3],
                    "suggestion": (
                        "检查该 Skill 是否缺少覆盖清单、边界状态枚举、"
                        "结果校验步骤或用户确认节点。"
                    ),
                }
            )

    return proposals


def detect_new_skill_candidates(items: list[FeedbackItem]) -> list[dict[str, object]]:
    proposals = []
    for item in items:
        if item.proposal_hint == "rule":
            continue
        if item.occurrences >= NEW_SKILL_THRESHOLD and item.source_skill == "N/A" and not item.skipped:
            proposals.append(
                {
                    "type": "new_skill_proposal",
                    "title": item.title,
                    "occurrences": item.occurrences,
                    "summary": item.description or item.title,
                    "feedback_file": str(item.path),
                    "suggestion": "检查该模式是否具备稳定输入输出，并考虑新建独立 Skill。",
                }
            )
    return proposals


def scan_feedback(feedback_dir: Path) -> dict[str, list[dict[str, object]]]:
    items = []
    for path in sorted(feedback_dir.glob("*.md")):
        if path.name == "FEEDBACK-INDEX.md":
            continue
        items.append(parse_feedback_file(path))

    return {
        "rule_graduations": detect_rule_graduations(items),
        "skill_optimizations": detect_skill_optimizations(items),
        "new_skill_proposals": detect_new_skill_candidates(items),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate evolution proposals.")
    parser.add_argument("--feedback-dir", required=True, help="Directory containing feedback files")
    parser.add_argument("--rules-file", help="Optional rules file path for downstream consumers")
    args = parser.parse_args()

    feedback_dir = Path(args.feedback_dir)
    if not feedback_dir.exists():
        json.dump(
            {
                "rule_graduations": [],
                "skill_optimizations": [],
                "new_skill_proposals": [],
                "rules_file": args.rules_file or "",
                "warning": f"feedback 目录不存在: {feedback_dir}",
            },
            sys.stdout,
            ensure_ascii=False,
            indent=2,
        )
        sys.stdout.write("\n")
        return 0

    result = scan_feedback(feedback_dir)
    result["rules_file"] = args.rules_file or ""
    json.dump(result, sys.stdout, ensure_ascii=False, indent=2)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
