#!/usr/bin/env python3
"""
Shared workflow matching, capture, and rendering helpers.
"""

from __future__ import annotations

import json
import re
import unicodedata
from collections import Counter
from pathlib import Path

STOPWORDS = {
    "a",
    "an",
    "and",
    "are",
    "as",
    "at",
    "be",
    "build",
    "by",
    "can",
    "do",
    "for",
    "from",
    "help",
    "how",
    "i",
    "in",
    "into",
    "is",
    "it",
    "make",
    "me",
    "my",
    "need",
    "of",
    "on",
    "or",
    "please",
    "should",
    "something",
    "task",
    "that",
    "the",
    "this",
    "to",
    "use",
    "want",
    "we",
    "with",
}


def slugify(value: str) -> str:
    normalized = unicodedata.normalize("NFKC", value).strip().lower()
    slug = re.sub(r"[\s/]+", "-", normalized)
    slug = re.sub(r"[^\w-]+", "", slug, flags=re.UNICODE)
    slug = re.sub(r"-{2,}", "-", slug)
    slug = slug.strip("-_")
    return slug or "new-workflow"


def tokenize(text: str) -> list[str]:
    normalized = unicodedata.normalize("NFKC", text).lower()
    return re.findall(r"[^\W_]+", normalized, flags=re.UNICODE)


def normalize_tools(tools: list[str] | None) -> list[str]:
    if not tools:
        return []
    return [tool.strip().lower() for tool in tools if tool and tool.strip()]


def extract_keywords(text: str, limit: int = 6) -> list[str]:
    tokens = [token for token in tokenize(text) if token not in STOPWORDS and len(token) > 1]
    if not tokens:
        return []
    counts = Counter(tokens)
    first_index: dict[str, int] = {}
    for index, token in enumerate(tokens):
        first_index.setdefault(token, index)
    ranked = sorted(tokens, key=lambda token: (-counts[token], first_index[token]))
    deduped: list[str] = []
    for token in ranked:
        if token not in deduped:
            deduped.append(token)
        if len(deduped) >= limit:
            break
    return deduped


def parse_step_lines(raw_steps: list[str] | str | None) -> list[dict]:
    if raw_steps is None:
        return []
    if isinstance(raw_steps, str):
        lines = [line.strip() for line in raw_steps.splitlines() if line.strip()]
    else:
        lines = [str(line).strip() for line in raw_steps if str(line).strip()]

    steps: list[dict] = []
    for index, line in enumerate(lines, start=1):
        if "|" in line:
            title, instruction = [part.strip() for part in line.split("|", 1)]
        elif ":" in line:
            title, instruction = [part.strip() for part in line.split(":", 1)]
        else:
            title = f"Step {index}"
            instruction = line
        steps.append(
            {
                "id": f"step-{index}",
                "title": title or f"Step {index}",
                "instruction": instruction or title or f"Step {index}",
            }
        )
    return steps


def suggest_name(task: str, keywords: list[str]) -> str:
    if keywords:
        return " ".join(keyword.capitalize() for keyword in keywords[:3])
    tokens = [token.capitalize() for token in tokenize(task)[:3]]
    return " ".join(tokens) or "New Workflow"


def summarize_task(task: str) -> str:
    task = " ".join(task.split())
    if not task:
        return "Describe the repeated task this workflow should handle."
    if len(task) <= 120:
        return task[0].upper() + task[1:]
    return task[:117].rstrip() + "..."


def workflow_tools(workflow: dict) -> list[str]:
    return normalize_tools(
        [item.get("tool", "") for item in workflow.get("tool_preferences", []) if isinstance(item, dict)]
    )


def score_workflow(task: str, workflow: dict, tools: list[str] | None = None) -> dict:
    task_tokens = set(extract_keywords(task, limit=12))
    workflow_keywords = {
        token.lower()
        for token in workflow.get("match", {}).get("keywords", [])
        if isinstance(token, str) and token.strip()
    }
    name_tokens = set(extract_keywords(workflow.get("name", ""), limit=6))
    summary_tokens = set(extract_keywords(workflow.get("summary", ""), limit=6))
    tool_set = set(normalize_tools(tools))
    workflow_tool_set = set(workflow_tools(workflow))

    keyword_overlap = sorted(task_tokens & workflow_keywords)
    name_overlap = sorted(task_tokens & name_tokens)
    summary_overlap = sorted(task_tokens & summary_tokens)
    tool_overlap = sorted(tool_set & workflow_tool_set)

    keyword_score = len(keyword_overlap) / max(1, len(workflow_keywords))
    name_score = len(name_overlap) / max(1, len(name_tokens)) if name_tokens else 0.0
    summary_score = len(summary_overlap) / max(1, len(summary_tokens)) if summary_tokens else 0.0
    tool_score = len(tool_overlap) / max(1, len(workflow_tool_set)) if workflow_tool_set and tool_set else 0.0

    total = (0.55 * keyword_score) + (0.20 * name_score) + (0.10 * summary_score) + (0.15 * tool_score)
    reasons: list[str] = []
    if keyword_overlap:
        reasons.append("keyword overlap: " + ", ".join(keyword_overlap))
    if tool_overlap:
        reasons.append("tool overlap: " + ", ".join(tool_overlap))
    if name_overlap and not keyword_overlap:
        reasons.append("name overlap: " + ", ".join(name_overlap))

    return {
        "workflow_id": workflow.get("id"),
        "name": workflow.get("name", workflow.get("id", "Unnamed Workflow")),
        "score": round(total, 3),
        "keyword_overlap": keyword_overlap,
        "tool_overlap": tool_overlap,
        "reasons": reasons,
    }


def find_matches(task: str, workflows: list[dict], tools: list[str] | None = None, limit: int = 3) -> list[dict]:
    if not task.strip():
        return []
    scored = [score_workflow(task, workflow, tools) for workflow in workflows]
    scored = [item for item in scored if item["score"] > 0]
    scored.sort(key=lambda item: (-item["score"], item["name"].lower()))
    return scored[:limit]


def render_execution_brief(workflow: dict, task: str = "") -> str:
    keywords = workflow.get("match", {}).get("keywords", [])
    tools = workflow_tools(workflow)
    steps = workflow.get("steps", [])

    def format_list(items: list[str]) -> str:
        return "\n".join(f"- {item}" for item in items) if items else "- None"

    lines = [
        f"Workflow: {workflow.get('name', workflow.get('id', 'Unnamed Workflow'))}",
        "",
        "Current Goal",
        f"- {task.strip() or workflow.get('summary', 'No summary provided.')}",
        "",
        "Workflow Summary",
        f"- {workflow.get('summary', 'No summary provided.')}",
        "",
        "Trigger Keywords",
        format_list([str(item) for item in keywords]),
        "",
        "Preferred Tools",
        format_list([str(item) for item in tools]),
        "",
        "Ordered Steps",
        format_list(
            [
                f"{step.get('title', step.get('id', 'step'))}: {step.get('instruction', '').strip()}"
                for step in steps
            ]
        ),
    ]
    return "\n".join(lines).strip() + "\n"


def capture_workflow(task: str, raw_steps: list[str] | str | None = None, tools: list[str] | None = None) -> dict:
    keywords = extract_keywords(task, limit=6)
    name = suggest_name(task, keywords)
    steps = parse_step_lines(raw_steps)
    tool_preferences = [{"tool": tool, "purpose": ""} for tool in normalize_tools(tools)]

    if not steps and task.strip():
        steps = [
            {
                "id": "step-1",
                "title": "Core task",
                "instruction": task.strip(),
            }
        ]

    return {
        "id": slugify(name),
        "name": name,
        "summary": summarize_task(task),
        "match": {
            "keywords": keywords,
        },
        "steps": steps,
        "tool_preferences": tool_preferences,
        "version": 1,
    }


def load_workflow(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def load_workflows(workflows_dir: Path) -> list[dict]:
    workflows: list[dict] = []
    for path in sorted(workflows_dir.glob("*.json")):
        try:
            workflows.append(load_workflow(path))
        except (OSError, json.JSONDecodeError):
            continue
    return workflows
