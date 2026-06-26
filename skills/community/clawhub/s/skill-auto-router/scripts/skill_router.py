#!/usr/bin/env python3
"""Skill Router

Purpose:
- Rank installed skills against a task text (pre-task routing)
- Run daily audit of skill descriptions/trigger quality

Usage:
  python scripts/skill_router.py --task "build azure function and deploy"
  python scripts/skill_router.py --daily
"""

from __future__ import annotations

import argparse
import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, List, Tuple


FRONTMATTER_RE = re.compile(r"^---\n(.*?)\n---\n", re.DOTALL)
KV_RE = re.compile(r"^([a-zA-Z0-9_\-]+):\s*(.*)$")
TOKEN_RE = re.compile(r"[a-zA-Z0-9_\-]{3,}")


@dataclass
class SkillMeta:
    name: str
    description: str
    path: Path


def tokenize(text: str) -> set[str]:
    return {t.lower() for t in TOKEN_RE.findall(text or "")}


def parse_skill_md(path: Path) -> SkillMeta | None:
    try:
        raw = path.read_text(encoding="utf-8", errors="ignore")
    except Exception:
        return None

    m = FRONTMATTER_RE.match(raw)
    if not m:
        return None

    frontmatter = m.group(1)
    data = {}
    for line in frontmatter.splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        km = KV_RE.match(line)
        if km:
            data[km.group(1).strip()] = km.group(2).strip().strip('"')

    name = data.get("name", "").strip()
    description = data.get("description", "").strip()
    if not name or not description:
        return None

    return SkillMeta(name=name, description=description, path=path)


def default_skill_roots() -> List[Path]:
    home = Path.home()
    return [
        Path("E:/AI/openclaw/.openclaw/workspace/skills"),
        home / "AppData/Roaming/npm/node_modules/openclaw/skills",
        home / ".agents/skills",
    ]


def discover_skills(roots: Iterable[Path]) -> List[SkillMeta]:
    out: List[SkillMeta] = []
    seen = set()
    for root in roots:
        if not root.exists() or not root.is_dir():
            continue
        for skill_md in root.rglob("SKILL.md"):
            meta = parse_skill_md(skill_md)
            if not meta:
                continue
            key = (meta.name.lower(), str(skill_md.resolve()).lower())
            if key in seen:
                continue
            seen.add(key)
            out.append(meta)
    return out


def score_skill(task_tokens: set[str], skill: SkillMeta) -> Tuple[float, List[str]]:
    desc_tokens = tokenize(skill.description)
    name_tokens = tokenize(skill.name)

    overlap_desc = sorted(task_tokens & desc_tokens)
    overlap_name = sorted(task_tokens & name_tokens)

    score = (len(overlap_desc) * 2.0) + (len(overlap_name) * 3.0)

    reasons = []
    if overlap_name:
        reasons.append(f"name overlap: {', '.join(overlap_name[:6])}")
    if overlap_desc:
        reasons.append(f"description overlap: {', '.join(overlap_desc[:8])}")

    # slight boost for explicit trigger phrasing
    desc_lower = skill.description.lower()
    if "use when" in desc_lower or "when:" in desc_lower:
        score += 0.5

    return score, reasons


def route_task(task: str, skills: List[SkillMeta], top_n: int = 5) -> dict:
    task_tokens = tokenize(task)
    ranked = []
    for s in skills:
        score, reasons = score_skill(task_tokens, s)
        if score > 0:
            ranked.append({
                "name": s.name,
                "score": round(score, 2),
                "path": str(s.path),
                "reasons": reasons,
            })

    ranked.sort(key=lambda x: x["score"], reverse=True)
    return {
        "task": task,
        "candidates": ranked[:top_n],
        "total_matches": len(ranked),
        "advice": "Load top 1-3 skills only unless task is clearly multi-domain.",
    }


def daily_audit(skills: List[SkillMeta]) -> dict:
    weak = []
    token_index = {}

    for s in skills:
        d = s.description.strip()
        if len(d) < 60 or "[todo" in d.lower() or "todo" in d.lower():
            weak.append({"name": s.name, "path": str(s.path), "issue": "description too weak or placeholder"})

        for t in tokenize(d):
            token_index.setdefault(t, set()).add(s.name)

    overlaps = []
    for tok, names in token_index.items():
        if len(names) >= 6 and tok not in {"use", "when", "with", "for", "and", "the", "that"}:
            overlaps.append({"token": tok, "skills": sorted(names)[:8], "count": len(names)})

    overlaps.sort(key=lambda x: x["count"], reverse=True)

    return {
        "skills_discovered": len(skills),
        "weak_descriptions": weak[:25],
        "high_overlap_tokens": overlaps[:25],
        "recommendation": "Tighten vague descriptions and reduce generic overlap words to improve auto-routing precision.",
    }


def main() -> None:
    ap = argparse.ArgumentParser(description="Auto route skills by task text and run daily audits")
    ap.add_argument("--task", type=str, help="Task text to route")
    ap.add_argument("--daily", action="store_true", help="Run daily audit")
    ap.add_argument("--skills-root", action="append", default=[], help="Additional skills root (repeatable)")
    ap.add_argument("--top", type=int, default=5, help="Top candidates for --task")
    args = ap.parse_args()

    roots = default_skill_roots() + [Path(p) for p in args.skills_root]
    skills = discover_skills(roots)

    if args.daily:
        print(json.dumps(daily_audit(skills), indent=2))
        return

    if args.task:
        print(json.dumps(route_task(args.task, skills, top_n=max(1, args.top)), indent=2))
        return

    ap.error("Provide either --task or --daily")


if __name__ == "__main__":
    main()
