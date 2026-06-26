#!/usr/bin/env python3
"""Static quality evaluator for agent skills (SKILL.md packages)."""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass, asdict, field
from pathlib import Path
from typing import Any


# ---------------------------------------------------------------------------
# Frontmatter parsing
# ---------------------------------------------------------------------------

def parse_frontmatter(text: str) -> tuple[dict[str, str], str]:
    match = re.match(r"^---\n(.*?)\n---\n?(.*)$", text, re.DOTALL)
    if not match:
        raise ValueError("SKILL.md is missing valid YAML frontmatter delimited by ---")
    raw = match.group(1)
    body = match.group(2)
    data: dict[str, str] = {}
    for line in raw.splitlines():
        if not line.strip():
            continue
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        data[key.strip()] = value.strip().strip("'\"")
    return data, body


# ---------------------------------------------------------------------------
# Data structures
# ---------------------------------------------------------------------------

@dataclass
class Check:
    name: str
    passed: bool
    message: str
    severity: str = "medium"


@dataclass
class DimensionResult:
    name: str
    weight: float
    score: int
    checks: list[Check] = field(default_factory=list)


@dataclass
class EvalReport:
    skill_path: str
    slug: str
    overall_score: int
    dimensions: list[DimensionResult] = field(default_factory=list)
    findings: list[dict[str, str]] = field(default_factory=list)
    recommendations: list[str] = field(default_factory=list)
    baseline_platform_compatibility: dict[str, bool] = field(default_factory=dict)


# ---------------------------------------------------------------------------
# Dimension evaluators
# ---------------------------------------------------------------------------

def eval_trigger_quality(frontmatter: dict[str, str], body: str, slug: str) -> DimensionResult:
    """Evaluate how well the skill's metadata supports correct triggering."""
    checks: list[Check] = []
    name = frontmatter.get("name", "")
    description = frontmatter.get("description", "")

    checks.append(Check(
        "name-present", bool(name),
        "name field present" if name else "name field missing from frontmatter",
        "critical",
    ))
    checks.append(Check(
        "name-matches-slug", name == slug,
        "name matches directory slug" if name == slug else f"name '{name}' != slug '{slug}'",
        "high",
    ))
    name_pattern = re.compile(r"^[a-z0-9]([a-z0-9-]*[a-z0-9])?$")
    checks.append(Check(
        "name-valid-format", bool(name_pattern.match(name)) if name else False,
        "name uses lowercase-hyphen format" if name and name_pattern.match(name) else "name must be lowercase letters, digits, hyphens; no leading/trailing hyphens",
        "high",
    ))
    checks.append(Check(
        "description-present", bool(description.strip()),
        "description present" if description.strip() else "description missing",
        "critical",
    ))
    desc_len = len(description)
    good_len = 110 <= desc_len <= 1024
    checks.append(Check(
        "description-length", good_len,
        f"description length {desc_len} chars (optimal: 110-420, max: 1024)" if good_len else f"description length {desc_len} chars; aim for 110-420",
        "medium",
    ))
    has_trigger = "use when" in description.lower()
    checks.append(Check(
        "description-trigger-phrasing", has_trigger,
        "description includes 'Use when...' trigger" if has_trigger else "description lacks 'Use when...' trigger phrasing",
        "high",
    ))
    action_words = re.findall(r"\b(create|generate|analyze|build|fix|test|deploy|audit|optimize|review|convert|transform|run|check|validate|scaffold|evaluate|grade|benchmark)\b", description.lower())
    has_actions = len(set(action_words)) >= 2
    checks.append(Check(
        "description-action-density", has_actions,
        f"description contains action verbs: {', '.join(sorted(set(action_words)))}" if has_actions else "description needs more concrete action verbs",
        "medium",
    ))

    example_patterns = re.findall(
        r"(^-\s+`|^\d+\.\s+`|^##?\s+Example|example prompts)",
        body, re.MULTILINE | re.IGNORECASE,
    )
    has_examples = len(example_patterns) >= 3
    checks.append(Check(
        "example-prompts", has_examples,
        f"found {len(example_patterns)} example prompts" if has_examples else f"only {len(example_patterns)} examples; need at least 3",
        "high",
    ))

    passed = sum(1 for c in checks if c.passed)
    score = round((passed / len(checks)) * 100) if checks else 0
    return DimensionResult("trigger_accuracy", 0.25, score, checks)


def eval_structural_integrity(skill_dir: Path, body: str) -> DimensionResult:
    """Check that the skill's file structure is sound."""
    checks: list[Check] = []

    ref_links = re.findall(r"\[.*?\]\(((?!https?://).*?)\)", body)
    broken = []
    for link in ref_links:
        clean = link.split("#")[0].strip()
        if clean and not (skill_dir / clean).exists():
            broken.append(clean)
    checks.append(Check(
        "no-dead-links", len(broken) == 0,
        "all internal links resolve" if not broken else f"broken links: {', '.join(broken)}",
        "high",
    ))

    has_basedir = "{baseDir}" in body
    has_hardcoded = bool(re.search(r"(/usr/local|/home/|/Users/|~/|C:\\)", body))
    checks.append(Check(
        "portable-paths", has_basedir and not has_hardcoded,
        "commands use {baseDir} without hardcoded paths" if (has_basedir and not has_hardcoded) else "use {baseDir} for portable command paths; avoid hardcoded absolute paths",
        "medium" if has_basedir else "high",
    ))

    refs_dir = skill_dir / "references"
    has_refs = refs_dir.is_dir() and any(refs_dir.iterdir())
    checks.append(Check(
        "references-present", has_refs,
        "references/ directory with content" if has_refs else "no references/ directory or it is empty",
        "low",
    ))

    scripts_or_bin = (skill_dir / "scripts").is_dir() or (skill_dir / "bin").is_dir()
    checks.append(Check(
        "executable-assets", scripts_or_bin,
        "scripts/ or bin/ directory present" if scripts_or_bin else "no scripts/ or bin/ found; add executable tools if the skill uses commands",
        "low",
    ))

    passed = sum(1 for c in checks if c.passed)
    score = round((passed / len(checks)) * 100) if checks else 0
    return DimensionResult("structural_integrity", 0.20, score, checks)


def eval_content_quality(body: str) -> DimensionResult:
    """Evaluate the documentation quality of SKILL.md body."""
    checks: list[Check] = []

    headings = re.findall(r"^##?\s+(.+)$", body, re.MULTILINE)
    heading_names = [h.lower().strip() for h in headings]
    checks.append(Check(
        "has-workflow", any("workflow" in h or "steps" in h or "how" in h for h in heading_names),
        "workflow/steps section found" if any("workflow" in h or "steps" in h or "how" in h for h in heading_names) else "add a Workflow or Steps section documenting the process",
        "high",
    ))
    checks.append(Check(
        "has-commands", any("command" in h or "usage" in h or "cli" in h for h in heading_names),
        "commands/usage section found" if any("command" in h or "usage" in h or "cli" in h for h in heading_names) else "add a Commands section with runnable examples",
        "medium",
    ))

    has_prereqs = bool(re.search(r"prerequisite|require|must be set|must have|need|depends on", body, re.IGNORECASE))
    checks.append(Check(
        "prerequisites-stated", has_prereqs,
        "prerequisites documented" if has_prereqs else "document prerequisites (env vars, tools, dependencies)",
        "high",
    ))

    has_done = bool(re.search(r"definition of done|done when|success.*criter|completion|verify|✅", body, re.IGNORECASE))
    checks.append(Check(
        "definition-of-done", has_done,
        "completion criteria found" if has_done else "add a 'Definition of done' with measurable success criteria",
        "high",
    ))

    code_blocks = re.findall(r"```[\s\S]*?```", body)
    has_code = len(code_blocks) >= 1
    checks.append(Check(
        "code-examples", has_code,
        f"{len(code_blocks)} code block(s) found" if has_code else "add at least one code block with runnable commands",
        "medium",
    ))

    has_output = bool(re.search(r"output|report|result|produce|generate|return|emit", body, re.IGNORECASE))
    checks.append(Check(
        "output-described", has_output,
        "output format described" if has_output else "describe what the skill produces and in what format",
        "medium",
    ))

    word_count = len(body.split())
    good_length = 200 <= word_count <= 3000
    checks.append(Check(
        "body-length", good_length,
        f"body length {word_count} words" if good_length else f"body is {word_count} words; aim for 200-3000",
        "low",
    ))

    passed = sum(1 for c in checks if c.passed)
    score = round((passed / len(checks)) * 100) if checks else 0
    return DimensionResult("content_quality", 0.25, score, checks)


def eval_platform_readiness(skill_dir: Path, frontmatter: dict[str, str]) -> DimensionResult:
    """Check baseline platform compatibility, not full platform-specific support."""
    checks: list[Check] = []

    skill_md = (skill_dir / "SKILL.md").exists()
    checks.append(Check(
        "openclaw-ready", skill_md and bool(frontmatter.get("name")) and bool(frontmatter.get("description")),
        "OpenClaw compatible (SKILL.md + name + description)" if skill_md else "SKILL.md with name and description required for OpenClaw",
        "critical",
    ))

    metadata_raw = frontmatter.get("metadata", "")
    has_openclaw_meta = "openclaw" in metadata_raw.lower() if metadata_raw else False
    checks.append(Check(
        "openclaw-metadata", has_openclaw_meta,
        "metadata.openclaw present" if has_openclaw_meta else "add metadata.openclaw for emoji, requires, and gating",
        "medium",
    ))

    checks.append(Check(
        "codex-ready", skill_md or (skill_dir / "AGENTS.md").exists(),
        "Codex compatible" if skill_md or (skill_dir / "AGENTS.md").exists() else "add SKILL.md or AGENTS.md for Codex",
        "high",
    ))

    checks.append(Check(
        "claude-code-ready", skill_md,
        "Claude Code compatible (SKILL.md)" if skill_md else "SKILL.md required for Claude Code",
        "high",
    ))

    cursor_ready = any(p.exists() for p in [
        skill_dir / ".cursor" / "rules",
        skill_dir / "AGENTS.md",
    ])
    checks.append(Check(
        "cursor-ready", cursor_ready or skill_md,
        "Cursor compatible" if cursor_ready or skill_md else "add .cursor/rules/ or AGENTS.md for Cursor",
        "medium",
    ))

    passed = sum(1 for c in checks if c.passed)
    score = round((passed / len(checks)) * 100) if checks else 0
    return DimensionResult("baseline_platform_compatibility", 0.15, score, checks)


def eval_testability(body: str, skill_dir: Path) -> DimensionResult:
    """Evaluate how easy it is to write automated tests for this skill."""
    checks: list[Check] = []

    has_eval = (skill_dir / "eval.yaml").exists()
    checks.append(Check(
        "eval-suite-exists", has_eval,
        "eval.yaml test suite found" if has_eval else "no eval.yaml; add one only if you need repeatable regression testing",
        "low",
    ))

    has_measurable = bool(re.search(
        r"(file.*exist|npm run|pytest|build.*success|start.*success|create|generat|produc|exit.*code|return|output)",
        body, re.IGNORECASE,
    ))
    checks.append(Check(
        "measurable-outcomes", has_measurable,
        "outcomes are measurable (file checks, build commands, etc.)" if has_measurable else "add measurable success criteria that automated graders can verify",
        "high",
    ))

    has_constraints = bool(re.search(r"(must not|do not|avoid|only|never|no extra|without)", body, re.IGNORECASE))
    checks.append(Check(
        "boundary-constraints", has_constraints,
        "boundary constraints documented" if has_constraints else "add explicit constraints (what the skill should NOT do) for negative testing",
        "medium",
    ))

    has_idempotent = bool(re.search(r"(idempotent|re-run|repeat|already exist|overwrite|skip if)", body, re.IGNORECASE))
    checks.append(Check(
        "idempotency-noted", has_idempotent,
        "idempotency behavior documented" if has_idempotent else "document behavior when re-run (overwrite? skip? error?)",
        "low",
    ))

    passed = sum(1 for c in checks if c.passed)
    score = round((passed / len(checks)) * 100) if checks else 0
    return DimensionResult("testability", 0.15, score, checks)


# ---------------------------------------------------------------------------
# Scaffold generator
# ---------------------------------------------------------------------------

def generate_scaffold(skill_dir: Path, frontmatter: dict[str, str], body: str) -> str:
    name = frontmatter.get("name", skill_dir.name)
    examples = re.findall(r"^-\s+`(.+?)`", body, re.MULTILINE)
    trigger_prompts = examples[:3] if examples else [f"Use the ${name} skill to do X"]

    scaffold = {
        "version": "1",
        "defaults": {
            "trials": 5,
            "timeout": 300,
            "threshold": 0.8,
        },
        "trigger_tests": [],
        "outcome_tests": [],
    }

    for i, prompt in enumerate(trigger_prompts):
        scaffold["trigger_tests"].append({
            "id": f"trigger-positive-{i+1}",
            "should_trigger": True,
            "prompt": prompt,
        })
    scaffold["trigger_tests"].append({
        "id": "trigger-negative-1",
        "should_trigger": False,
        "prompt": f"Do something unrelated to {name}",
    })

    scaffold["outcome_tests"].append({
        "id": "basic-outcome",
        "type": "deterministic",
        "checks": [
            {"description": "TODO: add file_exists, command_ran, or build_success checks"},
        ],
    })
    scaffold["outcome_tests"].append({
        "id": "style-check",
        "type": "llm_rubric",
        "rubric": "TODO: define qualitative criteria for this skill's output",
    })

    return json.dumps(scaffold, indent=2, ensure_ascii=False)


# ---------------------------------------------------------------------------
# Report assembly
# ---------------------------------------------------------------------------

def build_report(skill_dir: Path, explicit_keywords: list[str]) -> EvalReport:
    skill_file = skill_dir / "SKILL.md"
    if not skill_file.exists():
        raise FileNotFoundError(f"Missing file: {skill_file}")

    text = skill_file.read_text(encoding="utf-8")
    frontmatter, body = parse_frontmatter(text)
    slug = skill_dir.name

    dimensions = [
        eval_trigger_quality(frontmatter, body, slug),
        eval_structural_integrity(skill_dir, body),
        eval_content_quality(body),
        eval_platform_readiness(skill_dir, frontmatter),
        eval_testability(body, skill_dir),
    ]

    weighted_sum = sum(d.score * d.weight for d in dimensions)
    total_weight = sum(d.weight for d in dimensions)
    overall = round(weighted_sum / total_weight) if total_weight > 0 else 0

    findings: list[dict[str, str]] = []
    recommendations: list[str] = []
    for dim in dimensions:
        for check in dim.checks:
            if not check.passed:
                findings.append({
                    "severity": check.severity,
                    "dimension": dim.name,
                    "check": check.name,
                    "message": check.message,
                })
                if check.severity in ("critical", "high"):
                    recommendations.append(check.message)

    baseline_platform_compatibility = {}
    for dim in dimensions:
        if dim.name == "baseline_platform_compatibility":
            for check in dim.checks:
                baseline_platform_compatibility[check.name] = check.passed

    return EvalReport(
        skill_path=str(skill_dir),
        slug=slug,
        overall_score=overall,
        dimensions=dimensions,
        findings=findings,
        recommendations=recommendations,
        baseline_platform_compatibility=baseline_platform_compatibility,
    )


# ---------------------------------------------------------------------------
# Output formatters
# ---------------------------------------------------------------------------

def report_to_dict(report: EvalReport) -> dict[str, Any]:
    return {
        "skill_path": report.skill_path,
        "slug": report.slug,
        "overall_score": report.overall_score,
        "dimensions": [
            {
                "name": d.name,
                "weight": d.weight,
                "score": d.score,
                "checks": [asdict(c) for c in d.checks],
            }
            for d in report.dimensions
        ],
        "findings": report.findings,
        "recommendations": report.recommendations,
        "baseline_platform_compatibility": report.baseline_platform_compatibility,
    }


def print_text_report(report: EvalReport) -> None:
    print(f"Skill Evaluation: {report.slug}")
    print(f"Path: {report.skill_path}")
    print(f"Overall Score: {report.overall_score}/100")
    print()

    for dim in report.dimensions:
        bar_len = dim.score // 5
        bar = "█" * bar_len + "░" * (20 - bar_len)
        print(f"  {dim.name:<25} {bar} {dim.score:>3}/100 (weight: {dim.weight:.0%})")
    print()

    critical = [f for f in report.findings if f["severity"] == "critical"]
    high = [f for f in report.findings if f["severity"] == "high"]
    medium = [f for f in report.findings if f["severity"] == "medium"]
    low = [f for f in report.findings if f["severity"] == "low"]

    if critical or high:
        print("Issues to fix:")
        for f in critical:
            print(f"  [CRITICAL] {f['dimension']}/{f['check']}: {f['message']}")
        for f in high:
            print(f"  [HIGH]     {f['dimension']}/{f['check']}: {f['message']}")
        print()

    if medium:
        print("Improvements:")
        for f in medium:
            print(f"  [MEDIUM]   {f['dimension']}/{f['check']}: {f['message']}")
        print()

    if low:
        print("Nice to have:")
        for f in low:
            print(f"  [LOW]      {f['dimension']}/{f['check']}: {f['message']}")
        print()

    print("Baseline platform compatibility:")
    for platform, ready in report.baseline_platform_compatibility.items():
        icon = "✓" if ready else "✗"
        print(f"  {icon} {platform}")
    print()

    if report.recommendations:
        print("Top recommendations:")
        for i, rec in enumerate(report.recommendations[:5], 1):
            print(f"  {i}. {rec}")


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Evaluate an agent skill for quality, testability, and baseline platform compatibility."
    )
    parser.add_argument("skill_path", help="Path to the skill folder containing SKILL.md")
    parser.add_argument(
        "--keywords", default="",
        help="Comma-separated keywords to check for coverage",
    )
    parser.add_argument("--json", action="store_true", help="Emit JSON instead of text")
    parser.add_argument(
        "--scaffold", action="store_true",
        help="Generate an eval.yaml scaffold for the target skill",
    )
    parser.add_argument(
        "--baseline",
        help="Path to a baseline skill version for regression comparison",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    skill_dir = Path(args.skill_path).expanduser().resolve()
    keywords = [k.strip() for k in args.keywords.split(",") if k.strip()]

    if args.scaffold:
        try:
            text = (skill_dir / "SKILL.md").read_text(encoding="utf-8")
            fm, body = parse_frontmatter(text)
            scaffold = generate_scaffold(skill_dir, fm, body)
            out_path = skill_dir / "eval.yaml"
            out_path.write_text(scaffold, encoding="utf-8")
            print(f"Generated {out_path}", file=sys.stderr)
            print(scaffold)
            return 0
        except Exception as exc:
            print(f"error: {exc}", file=sys.stderr)
            return 1

    try:
        report = build_report(skill_dir, keywords)
    except Exception as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1

    if args.baseline:
        try:
            baseline_dir = Path(args.baseline).expanduser().resolve()
            baseline = build_report(baseline_dir, keywords)
            regressions: list[str] = []
            if report.overall_score < baseline.overall_score - 5:
                regressions.append(
                    f"overall score dropped: {baseline.overall_score} → {report.overall_score}"
                )
            baseline_dims = {d.name: d.score for d in baseline.dimensions}
            for dim in report.dimensions:
                prev = baseline_dims.get(dim.name, 0)
                if dim.score < prev - 10:
                    regressions.append(
                        f"{dim.name} dropped: {prev} → {dim.score}"
                    )
            if regressions:
                report.findings.insert(0, {
                    "severity": "critical",
                    "dimension": "regression",
                    "check": "baseline-comparison",
                    "message": "; ".join(regressions),
                })
                report.recommendations.insert(0, "Regression detected: " + "; ".join(regressions))
        except Exception as exc:
            print(f"warning: baseline comparison failed: {exc}", file=sys.stderr)

    if args.json:
        json.dump(report_to_dict(report), sys.stdout, ensure_ascii=False, indent=2)
        print()
    else:
        print_text_report(report)

    return 0 if report.overall_score >= 50 else 1


if __name__ == "__main__":
    raise SystemExit(main())
