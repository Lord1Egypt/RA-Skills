#!/usr/bin/env python3
"""Plan and gate AI-assisted maintenance candidates for a large ClawHub skill portfolio.

This script is intentionally conservative. By default it only selects the next
skills worth maintaining, inspects local source packages, writes an evidence
report, and creates one prompt file per candidate for an AI maintainer. It does
not publish, hide, merge, delete, or edit source files unless explicitly asked
with --apply-safe.
"""

from __future__ import annotations

import argparse
import csv
import json
import re
import shutil
import subprocess
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


PRIORITY_RANK = {
    "P0_feedback": 0,
    "P1_maintain": 1,
    "P2_upgrade": 2,
    "P3_watch": 3,
    "P4_low_priority": 4,
    "P5_data_unavailable": 5,
}

DATA_UNAVAILABLE = "data_unavailable"

FORBIDDEN_PACKAGE_NAMES = {
    ".env",
    ".DS_Store",
    "node_modules",
    "dist",
    "build",
    "logs",
    "tmp",
    "secrets",
    "credentials",
}

IGNORED_SCAN_NAMES = {
    ".git",
    "__pycache__",
}

SENSITIVE_PATTERNS = {
    "health": re.compile(r"health|medical|doctor|symptom|lab|blood|pain|recovery|medicine", re.I),
    "legal": re.compile(r"legal|law|contract|dispute|tenant|landlord|labor|compliance", re.I),
    "finance": re.compile(r"finance|financial|tax|invest|budget|cash|invoice|credit|loan", re.I),
    "shopping": re.compile(r"shopping|commerce|merchant|taobao|jd|pdd|alibaba|amazon|price", re.I),
}


def utc_stamp() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).strftime("%Y%m%dT%H%M%SZ")


def read_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    try:
        data = json.loads(path.read_text("utf-8"))
    except Exception:
        return {}
    return data if isinstance(data, dict) else {}


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2), encoding="utf-8")


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        path.write_text("", encoding="utf-8")
        return
    fieldnames: list[str] = []
    seen: set[str] = set()
    for row in rows:
        for key in row.keys():
            if key not in seen:
                seen.add(key)
                fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def to_int(value: Any) -> int:
    try:
        if value in (None, ""):
            return 0
        return int(float(value))
    except Exception:
        return 0


def to_float(value: Any) -> float:
    try:
        if value in (None, ""):
            return 0.0
        return float(value)
    except Exception:
        return 0.0


def compact_text(value: Any, limit: int = 240) -> str:
    text = re.sub(r"\s+", " ", str(value or "")).strip()
    return text[:limit]


def unique_existing_roots(paths: list[Path]) -> list[Path]:
    roots: list[Path] = []
    seen: set[str] = set()
    for path in paths:
        expanded = path.expanduser()
        key = str(expanded)
        if key in seen or not expanded.exists():
            continue
        seen.add(key)
        roots.append(expanded)
    return roots


def default_source_roots(primary_root: Path, extra_roots: list[Path]) -> list[Path]:
    home = Path.home()
    script_repo_root = Path(__file__).resolve().parents[1]
    roots = [
        primary_root,
        home / ".openclaw" / "workspace" / "agents" / "main" / "skills",
        home / ".openclaw" / "workspace" / "skills",
        script_repo_root.parent,
        script_repo_root.parent / "skills",
        script_repo_root.parent / "hermes-skills" / "skills",
        script_repo_root.parent / "openclaw-edit-staging",
        *extra_roots,
    ]
    return unique_existing_roots(roots)


def package_candidates(root: Path, slug: str) -> list[Path]:
    return [
        root / slug,
        root / "skills" / slug,
        root / "hermes-skills" / "skills" / slug,
        root / "openclaw-edit-staging" / slug,
    ]


@dataclass
class SourceResult:
    path: Path | None
    source_kind: str
    note: str
    acquisition_commands: list[str]
    errors: list[str]
    rate_limited: bool = False


@dataclass
class FetchResult:
    path: Path | None
    kind: str
    note: str
    errors: list[str]
    rate_limited: bool = False


def load_analysis_rows(data_dir: Path, handle: str) -> dict[str, dict[str, str]]:
    rows = read_csv(data_dir / "processed" / f"{handle}_skill_analysis.csv")
    if not rows:
        rows = read_csv(data_dir / "processed" / f"{handle}_skills.csv")
    return {row.get("slug", ""): row for row in rows if row.get("slug")}


def select_candidates(
    *,
    data_dir: Path,
    handle: str,
    limit: int,
    only_slugs: set[str],
    skip_recent_manifest: Path | None,
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    summary = read_json(data_dir / "processed" / f"{handle}_summary.json")
    rows_by_slug = load_analysis_rows(data_dir, handle)
    recent_slugs = load_recent_slugs(skip_recent_manifest) if skip_recent_manifest else set()

    raw_queue = summary.get("quality_maintenance_queue")
    if isinstance(raw_queue, list) and raw_queue:
        candidates = [dict(item) for item in raw_queue if isinstance(item, dict)]
    else:
        candidates = fallback_quality_queue(rows_by_slug.values())

    enriched: list[dict[str, Any]] = []
    for item in candidates:
        slug = str(item.get("slug", "")).strip()
        if not slug:
            continue
        if only_slugs and slug not in only_slugs:
            continue
        if slug in recent_slugs:
            continue
        merged = {**rows_by_slug.get(slug, {}), **item}
        if should_skip_candidate(merged):
            continue
        enriched.append(merged)

    enriched.sort(key=candidate_sort_key)
    return enriched[:limit], summary


def fallback_quality_queue(rows: Any) -> list[dict[str, Any]]:
    queue: list[dict[str, Any]] = []
    for row in rows:
        downloads = to_int(row.get("downloads"))
        installs = to_int(row.get("installs_all_time"))
        stars = to_int(row.get("stars"))
        comments = to_int(row.get("comments"))
        versions = to_int(row.get("versions"))
        quality_score = min(
            100.0,
            comments * 20.0
            + installs * 4.0
            + stars * 8.0
            + min(30.0, downloads / 40.0)
            + min(12.0, versions * 2.0),
        )
        priority = "P0_feedback" if comments else "P1_maintain" if installs >= 5 or stars else "P2_upgrade" if installs or downloads >= 300 else "P3_watch"
        copy = dict(row)
        copy["quality_score"] = round(quality_score, 1)
        copy["maintenance_priority"] = priority
        copy["quality_reason"] = "fallback_quality_score"
        queue.append(copy)
    return queue


def load_recent_slugs(path: Path) -> set[str]:
    data = read_json(path)
    slugs: set[str] = set()
    for item in data.get("candidates", []) if isinstance(data.get("candidates"), list) else []:
        slug = str(item.get("slug", "")).strip()
        if slug:
            slugs.add(slug)
    return slugs


def should_skip_candidate(row: dict[str, Any]) -> bool:
    if is_data_unavailable(row) or not is_detail_available(row):
        return True
    decision = row.get("portfolio_decision", "")
    if decision in {"delete_candidate", "move_private_or_hide", "merge_into_stronger_skill"}:
        engagement = to_int(row.get("installs_all_time")) + to_int(row.get("stars")) + to_int(row.get("comments"))
        if engagement == 0 and row.get("meaningfulness") in {"low_signal", "plausible_but_low_signal"}:
            return True
    return False


def is_data_unavailable(row: dict[str, Any]) -> bool:
    return (
        row.get("meaningfulness") == DATA_UNAVAILABLE
        or row.get("recommended_action") == DATA_UNAVAILABLE
        or row.get("portfolio_decision") == DATA_UNAVAILABLE
    )


def is_detail_available(row: dict[str, Any]) -> bool:
    value = str(row.get("detail_ok", "")).strip().lower()
    if value:
        return value in {"true", "1", "yes", "ok"}
    return not str(row.get("detail_error", "")).strip()


def candidate_sort_key(row: dict[str, Any]) -> tuple[int, float, int, int, int, str]:
    return (
        PRIORITY_RANK.get(str(row.get("maintenance_priority", "")), 9),
        -to_float(row.get("quality_score")),
        -to_int(row.get("installs_all_time")),
        -to_int(row.get("stars")),
        -to_int(row.get("downloads")),
        str(row.get("slug", "")),
    )


def resolve_source(
    slug: str,
    row: dict[str, Any],
    source_roots: list[Path],
    source_cache_dir: Path,
    github_owner: str,
    fetch_source: bool,
) -> SourceResult:
    acquisition_commands = build_acquisition_commands(slug, row, source_cache_dir, github_owner)
    if fetch_source:
        github = fetch_github_source(slug, row, source_cache_dir, github_owner)
        if github.path is not None:
            return SourceResult(path=github.path, source_kind=github.kind, note=github.note, acquisition_commands=acquisition_commands, errors=github.errors)
        if github.rate_limited:
            return SourceResult(path=None, source_kind=github.kind, note=github.note, acquisition_commands=acquisition_commands, errors=github.errors, rate_limited=True)

    candidates: list[Path] = []
    for root in source_roots:
        candidates.extend(package_candidates(root, slug))

    source_path = str(row.get("source_path", "") or "").strip()
    if source_path:
        p = Path(source_path).expanduser()
        if p.is_absolute():
            candidates.append(p)
        else:
            for root in source_roots:
                candidates.append(root / p)

    for path in candidates:
        if (path / "SKILL.md").exists():
            return SourceResult(path=path, source_kind="local", note="found SKILL.md", acquisition_commands=acquisition_commands, errors=[])

    if fetch_source:
        clawhub = fetch_clawhub_source(slug, source_cache_dir)
        if clawhub.path is not None:
            return SourceResult(path=clawhub.path, source_kind=clawhub.kind, note=clawhub.note, acquisition_commands=acquisition_commands, errors=clawhub.errors)
        return SourceResult(path=None, source_kind=clawhub.kind, note=clawhub.note, acquisition_commands=acquisition_commands, errors=clawhub.errors, rate_limited=clawhub.rate_limited)

    if row.get("source_repo"):
        return SourceResult(path=None, source_kind="repo", note=str(row.get("source_repo")), acquisition_commands=acquisition_commands, errors=[])
    return SourceResult(path=None, source_kind="missing", note="no local source found; acquire from GitHub first, then ClawHub", acquisition_commands=acquisition_commands, errors=[])


def build_acquisition_commands(slug: str, row: dict[str, Any], source_cache_dir: Path, github_owner: str) -> list[str]:
    commands: list[str] = []
    for owner, repo in github_repo_candidates(slug, row, github_owner):
        target = github_target_dir(source_cache_dir, owner, repo)
        commands.append(shell_command(["gh", "repo", "clone", f"{owner}/{repo}", str(target), "--", "--depth=1"]))
    commands.append(shell_command(["clawhub", "--workdir", str(source_cache_dir), "--dir", "clawhub", "install", slug]))
    return commands


def github_repo_candidates(slug: str, row: dict[str, Any], github_owner: str) -> list[tuple[str, str]]:
    candidates: list[tuple[str, str]] = []
    source_repo = str(row.get("source_repo", "") or "").strip()
    parsed = parse_github_repo(source_repo)
    if parsed:
        candidates.append(parsed)
    candidates.extend(
        [
            (github_owner, slug),
            (github_owner, f"{slug}-skill"),
            (github_owner, f"clawhub-{slug}"),
        ]
    )
    unique: list[tuple[str, str]] = []
    seen: set[tuple[str, str]] = set()
    for item in candidates:
        if item in seen:
            continue
        seen.add(item)
        unique.append(item)
    return unique


def parse_github_repo(value: str) -> tuple[str, str] | None:
    if not value:
        return None
    match = re.search(r"github\.com[:/](?P<owner>[^/\s]+)/(?P<repo>[^/\s#?]+)", value)
    if not match:
        return None
    repo = match.group("repo").removesuffix(".git")
    return match.group("owner"), repo


def github_target_dir(source_cache_dir: Path, owner: str, repo: str) -> Path:
    return source_cache_dir / "github" / f"{owner}__{repo}"


def fetch_github_source(slug: str, row: dict[str, Any], source_cache_dir: Path, github_owner: str) -> FetchResult:
    errors: list[str] = []
    for owner, repo in github_repo_candidates(slug, row, github_owner):
        target = github_target_dir(source_cache_dir, owner, repo)
        if (target / "SKILL.md").exists():
            return FetchResult(path=target, kind="github", note=f"cached GitHub source {owner}/{repo}", errors=errors)
        if target.exists():
            errors.append(f"{owner}/{repo}: cache exists but no SKILL.md")
            continue
        target.parent.mkdir(parents=True, exist_ok=True)
        result = run_external(["gh", "repo", "clone", f"{owner}/{repo}", str(target), "--", "--depth=1"])
        if result.returncode == 0 and (target / "SKILL.md").exists():
            return FetchResult(path=target, kind="github", note=f"cloned GitHub source {owner}/{repo}", errors=errors)
        message = compact_text((result.stderr or result.stdout or f"exit {result.returncode}"), 300)
        errors.append(f"{owner}/{repo}: {message}")
        if is_rate_limited(message):
            return FetchResult(path=None, kind="github_rate_limited", note="GitHub rate limited; do not retry now", errors=errors, rate_limited=True)
    return FetchResult(path=None, kind="github_missing", note="no GitHub source found", errors=errors)


def fetch_clawhub_source(slug: str, source_cache_dir: Path) -> FetchResult:
    target = source_cache_dir / "clawhub" / slug
    if (target / "SKILL.md").exists():
        return FetchResult(path=target, kind="clawhub", note="cached ClawHub install", errors=[])
    result = run_external(["clawhub", "--workdir", str(source_cache_dir), "--dir", "clawhub", "install", slug])
    if result.returncode == 0 and (target / "SKILL.md").exists():
        return FetchResult(path=target, kind="clawhub", note="installed from ClawHub", errors=[])
    message = compact_text((result.stderr or result.stdout or f"exit {result.returncode}"), 300)
    return FetchResult(
        path=None,
        kind="clawhub_rate_limited" if is_rate_limited(message) else "clawhub_missing",
        note="ClawHub rate limited; do not retry now" if is_rate_limited(message) else "ClawHub install did not produce source",
        errors=[message],
        rate_limited=is_rate_limited(message),
    )


def run_external(command: list[str]) -> subprocess.CompletedProcess[str]:
    try:
        return subprocess.run(command, check=False, capture_output=True, text=True, timeout=120)
    except FileNotFoundError as exc:
        return subprocess.CompletedProcess(command, 127, "", str(exc))
    except subprocess.TimeoutExpired as exc:
        return subprocess.CompletedProcess(command, 124, exc.stdout or "", exc.stderr or "command timed out")


def is_rate_limited(message: str) -> bool:
    return bool(re.search(r"rate.?limit|too many requests|secondary rate|429", message, re.I))


def analyze_source(path: Path | None, row: dict[str, Any]) -> dict[str, Any]:
    if path is None:
        return {
            "source_found": False,
            "findings": ["local source missing"],
            "recommended_edits": ["locate source via GitHub or clawhub inspect before editing"],
            "validation_commands": [],
            "package_file_count": 0,
            "forbidden_files": [],
            "safe_auto_editable": False,
        }

    skill_md = path / "SKILL.md"
    text = skill_md.read_text("utf-8", errors="replace") if skill_md.exists() else ""
    headings = extract_headings(text)
    files = list(iter_package_files(path))
    forbidden = sorted(
        str(p.relative_to(path))
        for p in files
        if any(part in FORBIDDEN_PACKAGE_NAMES for part in p.relative_to(path).parts)
    )

    findings: list[str] = []
    edits: list[str] = []
    has_frontmatter = text.lstrip().startswith("---")
    has_examples = any("example" in h.lower() or "prompt" in h.lower() or "示例" in h for h in headings)
    has_boundaries = bool(re.search(r"safety|boundary|limitation|do not|never|风险|边界|限制", text, re.I))
    has_workflow = bool(re.search(r"workflow|steps|procedure|process|流程|步骤", text, re.I))
    has_validation = bool(re.search(r"validate|verify|check|test|验收|验证|检查", text, re.I))
    description_len = len(frontmatter_description(text))
    sensitive = risk_labels(row, text)

    if not has_frontmatter:
        findings.append("missing YAML frontmatter")
        edits.append("add required name and description frontmatter")
    if description_len < 80:
        findings.append("thin trigger description")
        edits.append("clarify trigger conditions and expected user intent")
    if not has_examples:
        findings.append("missing example prompts")
        edits.append("add 2-3 realistic example prompts")
    if not has_workflow:
        findings.append("missing explicit workflow")
        edits.append("add a concise step-by-step workflow")
    if sensitive and not has_boundaries:
        findings.append("sensitive domain without clear boundaries")
        edits.append(f"add safety boundaries for {', '.join(sensitive)}")
    if not has_validation:
        findings.append("missing validation or quality check")
        edits.append("add validation checks for final output")
    if forbidden:
        findings.append("package contains forbidden files")
        edits.append("remove forbidden files before publish")
    if len(files) > 10:
        findings.append("package has more than 10 files")
        edits.append("review package surface before publish")
    if not findings:
        findings.append("source looks maintainable; consider examples, tags, and release notes polish")
        edits.append("perform small quality polish only")

    validation_commands = [
        f"test -f {quote_path(path / 'SKILL.md')}",
        f"clawhub inspect {row.get('slug', '')} --json",
        f"clawhub publish {quote_path(path)} --dry-run --json",
    ]

    return {
        "source_found": True,
        "headings": headings[:20],
        "findings": findings,
        "recommended_edits": edits,
        "validation_commands": validation_commands,
        "package_file_count": len(files),
        "forbidden_files": forbidden,
        "risk_labels": sensitive,
        "safe_auto_editable": bool(skill_md.exists() and not forbidden and len(files) <= 10),
        "has_examples": has_examples,
        "has_boundaries": has_boundaries,
        "has_workflow": has_workflow,
        "has_validation": has_validation,
    }


def iter_package_files(path: Path) -> list[Path]:
    files: list[Path] = []
    for candidate in path.rglob("*"):
        if not candidate.is_file():
            continue
        rel_parts = candidate.relative_to(path).parts
        if any(part in IGNORED_SCAN_NAMES for part in rel_parts):
            continue
        files.append(candidate)
    return files


def extract_headings(text: str) -> list[str]:
    return [line.strip("# ").strip() for line in text.splitlines() if line.startswith("#")]


def frontmatter_description(text: str) -> str:
    if not text.lstrip().startswith("---"):
        return ""
    parts = text.lstrip().split("---", 2)
    if len(parts) < 3:
        return ""
    for line in parts[1].splitlines():
        if line.strip().startswith("description:"):
            return line.split(":", 1)[1].strip().strip('"')
    return ""


def risk_labels(row: dict[str, Any], text: str) -> list[str]:
    haystack = " ".join(
        [
            str(row.get("slug", "")),
            str(row.get("display_name", "")),
            str(row.get("summary", "")),
            str(row.get("category", "")),
            text[:2000],
        ]
    )
    return [label for label, pattern in SENSITIVE_PATTERNS.items() if pattern.search(haystack)]


def quote_path(path: Path) -> str:
    return quote_arg(str(path))


def quote_arg(text: str) -> str:
    if re.search(r"\s", text):
        return "'" + text.replace("'", "'\\''") + "'"
    return text


def shell_command(parts: list[str]) -> str:
    return " ".join(quote_arg(part) for part in parts)


def build_agent_prompt(candidate: dict[str, Any]) -> str:
    slug = candidate["slug"]
    source_path = candidate.get("source_path_resolved") or ""
    findings = "\n".join(f"- {item}" for item in candidate.get("findings", []))
    edits = "\n".join(f"- {item}" for item in candidate.get("recommended_edits", []))
    validation = "\n".join(f"- `{item}`" for item in candidate.get("validation_commands", []))
    acquisition = "\n".join(f"- `{item}`" for item in candidate.get("source_acquisition_commands", []))
    source_errors = "\n".join(f"- {item}" for item in candidate.get("source_errors", []))
    return f"""Use $skillopt principles to upgrade one ClawHub skill safely.

Target skill: {slug}
Local source: {source_path or 'MISSING'}
Display name: {candidate.get('display_name', '')}
Summary: {compact_text(candidate.get('summary'), 500)}
Signals: downloads={candidate.get('downloads', '')}, installs={candidate.get('installs_all_time', '')}, stars={candidate.get('stars', '')}, comments={candidate.get('comments', '')}, quality_score={candidate.get('quality_score', '')}, priority={candidate.get('maintenance_priority', '')}
Quality reason: {candidate.get('quality_reason', '')}

Findings:
{findings}

Recommended edits:
{edits}

Source acquisition order:
1. GitHub repository source.
2. Local source roots.
3. ClawHub install/download fallback.

Source acquisition commands:
{acquisition or '- already resolved locally'}

Source errors:
{source_errors or '- none'}

Rules:
- Preserve the original public contract and slug.
- Prefer small, reviewable edits to SKILL.md and adjacent metadata only.
- Add examples, clearer trigger text, workflow, validation checks, and safety boundaries where missing.
- Do not delete, hide, merge, rename, or change ownership.
- Do not publish if data_quality.status is partial unless the user explicitly allows this run.
- Do not add secrets, executable handlers, network dependencies, or unsupported claims.
- After edits, run validation and dry-run publish. Stop on rate limits or auth errors.

Validation commands to consider:
{validation}

Expected output:
- Files changed
- Validation results
- Publish readiness
- Any item requiring user approval
"""


def apply_safe_edit(candidate: dict[str, Any], run_dir: Path) -> dict[str, Any]:
    path_text = candidate.get("source_path_resolved")
    if not path_text:
        return {"applied": False, "reason": "missing source"}
    path = Path(path_text)
    skill_md = path / "SKILL.md"
    if not skill_md.exists():
        return {"applied": False, "reason": "missing SKILL.md"}
    if not candidate.get("safe_auto_editable"):
        return {"applied": False, "reason": "package is not safe-auto-editable"}

    text = skill_md.read_text("utf-8", errors="replace")
    additions: list[str] = []
    if not candidate.get("has_examples"):
        additions.append(example_prompt_block(candidate))
    if candidate.get("risk_labels") and not candidate.get("has_boundaries"):
        additions.append(boundary_block(candidate))
    if not additions:
        return {"applied": False, "reason": "no safe deterministic edit needed"}

    backup_dir = run_dir / "backups" / candidate["slug"]
    backup_dir.mkdir(parents=True, exist_ok=True)
    shutil.copy2(skill_md, backup_dir / "SKILL.md.before")
    updated = text.rstrip() + "\n\n" + "\n\n".join(additions).rstrip() + "\n"
    skill_md.write_text(updated, encoding="utf-8")
    return {"applied": True, "reason": "appended safe maintenance sections", "backup": str(backup_dir / "SKILL.md.before")}


def example_prompt_block(candidate: dict[str, Any]) -> str:
    slug = candidate["slug"]
    display = candidate.get("display_name") or slug.replace("-", " ").title()
    summary = compact_text(candidate.get("summary"), 160).rstrip(".")
    return f"""## Example Prompts

- Use ${slug} to help me with a realistic {display} request: {summary}.
- Use ${slug} to turn my rough context into a clear checklist, decision, or next-step plan.
- Use ${slug} to review this situation, identify missing details, and produce a concise action-ready output."""


def boundary_block(candidate: dict[str, Any]) -> str:
    labels = ", ".join(candidate.get("risk_labels", []))
    return f"""## Safety Boundaries

- Treat {labels or 'sensitive'} requests as decision support, not professional advice.
- Ask for missing context before making strong recommendations.
- Flag uncertainty, assumptions, and cases where the user should consult a qualified professional.
- Do not request secrets, credentials, private identifiers, or payment details."""


def write_prompt_files(run_dir: Path, candidates: list[dict[str, Any]]) -> None:
    prompt_dir = run_dir / "agent_prompts"
    prompt_dir.mkdir(parents=True, exist_ok=True)
    for candidate in candidates:
        (prompt_dir / f"{candidate['slug']}.md").write_text(build_agent_prompt(candidate), encoding="utf-8")


def write_report(run_dir: Path, handle: str, candidates: list[dict[str, Any]], summary: dict[str, Any], source_roots: list[Path]) -> None:
    data_quality = summary.get("data_quality") if isinstance(summary.get("data_quality"), dict) else {}
    lines = [
        f"# Maintenance Candidate Plan - {handle}",
        "",
        f"Generated: {datetime.now(timezone.utc).replace(microsecond=0).isoformat()}",
        f"Data quality: `{data_quality.get('status', 'unknown')}`",
        "",
        "This report is a safe planning artifact. No publish, hide, merge, or delete action is implied.",
        "",
        "Source acquisition order for missing sources: GitHub first, local roots second, ClawHub install/download fallback last. Stop instead of retrying when a rate limit is detected.",
        "",
        "## Source Roots",
        "",
    ]
    lines.extend(f"- `{root}`" for root in source_roots)
    lines.extend(
        [
            "",
            "## Candidates",
            "",
        ]
    )
    if not candidates:
        lines.append("No candidates selected.")
    else:
        keys = ["slug", "downloads", "installs_all_time", "stars", "comments", "quality_score", "maintenance_priority", "source_kind", "safe_auto_editable"]
        lines.append("| " + " | ".join(keys) + " |")
        lines.append("| " + " | ".join("---" for _ in keys) + " |")
        for candidate in candidates:
            lines.append("| " + " | ".join(markdown_cell(candidate.get(key, "")) for key in keys) + " |")
    lines.extend(["", "## Per-Skill Findings", ""])
    for candidate in candidates:
        lines.extend(
            [
                f"### {candidate['slug']}",
                "",
                f"- source: `{candidate.get('source_path_resolved') or candidate.get('source_note', '')}`",
                f"- source kind: `{candidate.get('source_kind', '')}`",
                f"- signals: downloads `{candidate.get('downloads', '')}`, installs `{candidate.get('installs_all_time', '')}`, stars `{candidate.get('stars', '')}`, comments `{candidate.get('comments', '')}`",
                f"- quality reason: {candidate.get('quality_reason', '')}",
                "- findings:",
            ]
        )
        lines.extend(f"  - {item}" for item in candidate.get("findings", []))
        lines.append("- recommended edits:")
        lines.extend(f"  - {item}" for item in candidate.get("recommended_edits", []))
        if candidate.get("source_acquisition_commands"):
            lines.append("- source acquisition commands:")
            lines.extend(f"  - `{item}`" for item in candidate.get("source_acquisition_commands", []))
        if candidate.get("source_errors"):
            lines.append("- source errors:")
            lines.extend(f"  - {item}" for item in candidate.get("source_errors", []))
        if candidate.get("apply_result"):
            lines.append(f"- apply result: `{candidate['apply_result'].get('reason', '')}`")
        lines.append("")
    (run_dir / "report.md").write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def markdown_cell(value: Any) -> str:
    return str(value).replace("|", "\\|").replace("\n", " ")[:160]


def build_candidate_record(row: dict[str, Any], source: SourceResult, analysis: dict[str, Any]) -> dict[str, Any]:
    return {
        **row,
        "slug": row.get("slug", ""),
        "source_kind": source.source_kind,
        "source_note": source.note,
        "source_path_resolved": str(source.path) if source.path else "",
        "source_acquisition_commands": source.acquisition_commands,
        "source_errors": source.errors,
        "source_rate_limited": source.rate_limited,
        **analysis,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--handle", default="harrylabsj")
    parser.add_argument("--data-dir", default="data")
    parser.add_argument("--skills-root", default="~/.openclaw/skills")
    parser.add_argument("--extra-root", action="append", default=[])
    parser.add_argument("--source-cache-dir", default=".cache/auto_upgrade_sources")
    parser.add_argument("--github-owner", default="", help="GitHub owner to probe when source_repo is not present; defaults to --handle.")
    parser.add_argument("--fetch-source", action="store_true", help="Clone GitHub source first, then install from ClawHub if GitHub is unavailable.")
    parser.add_argument("--out-dir", default="reports/auto_upgrade")
    parser.add_argument("--limit", type=int, default=5)
    parser.add_argument("--slug", action="append", default=[], help="Restrict to one or more slugs.")
    parser.add_argument("--skip-recent-manifest", default="", help="Previous manifest whose slugs should be skipped.")
    parser.add_argument("--apply-safe", action="store_true", help="Apply only deterministic append-only SKILL.md improvements.")
    args = parser.parse_args()

    data_dir = Path(args.data_dir).expanduser()
    skills_root = Path(args.skills_root).expanduser()
    extra_roots = [Path(item).expanduser() for item in args.extra_root]
    source_roots = default_source_roots(skills_root, extra_roots)
    source_cache_dir = Path(args.source_cache_dir).expanduser()
    if not source_cache_dir.is_absolute():
        source_cache_dir = Path.cwd() / source_cache_dir
    github_owner = args.github_owner.strip() or args.handle
    out_root = Path(args.out_dir).expanduser()
    run_dir = out_root / utc_stamp()
    run_dir.mkdir(parents=True, exist_ok=True)

    candidates, summary = select_candidates(
        data_dir=data_dir,
        handle=args.handle,
        limit=args.limit,
        only_slugs={slug.strip() for slug in args.slug if slug.strip()},
        skip_recent_manifest=Path(args.skip_recent_manifest).expanduser() if args.skip_recent_manifest else None,
    )

    records: list[dict[str, Any]] = []
    for row in candidates:
        source = resolve_source(
            str(row.get("slug", "")),
            row,
            source_roots,
            source_cache_dir,
            github_owner,
            args.fetch_source,
        )
        analysis = analyze_source(source.path, row)
        record = build_candidate_record(row, source, analysis)
        if args.apply_safe:
            record["apply_result"] = apply_safe_edit(record, run_dir)
        records.append(record)

    write_prompt_files(run_dir, records)
    write_report(run_dir, args.handle, records, summary, source_roots)
    write_json(
        run_dir / "manifest.json",
        {
            "handle": args.handle,
            "generated_at_utc": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
            "mode": "apply-safe" if args.apply_safe else "plan",
            "data_quality": summary.get("data_quality", {}),
            "source_roots": [str(root) for root in source_roots],
            "source_cache_dir": str(source_cache_dir),
            "source_resolution_order": ["github", "local", "clawhub"] if args.fetch_source else ["local", "github_command", "clawhub_command"],
            "fetch_source": args.fetch_source,
            "candidates": records,
        },
    )
    write_csv(run_dir / "candidates.csv", records)
    latest = out_root / "latest"
    if latest.exists() or latest.is_symlink():
        latest.unlink()
    try:
        latest.symlink_to(run_dir.name)
    except OSError:
        pass

    print(json.dumps({"run_dir": str(run_dir), "candidate_count": len(records), "mode": "apply-safe" if args.apply_safe else "plan"}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
