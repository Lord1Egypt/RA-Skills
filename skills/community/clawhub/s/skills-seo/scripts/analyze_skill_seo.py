#!/usr/bin/env python3
"""Static discoverability audit for skills listed in public skill directories."""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Any


STOPWORDS = {
    "a",
    "an",
    "and",
    "are",
    "as",
    "at",
    "be",
    "by",
    "for",
    "from",
    "in",
    "into",
    "is",
    "it",
    "of",
    "on",
    "or",
    "that",
    "the",
    "this",
    "to",
    "use",
    "when",
    "with",
}


@dataclass
class Finding:
    severity: str
    area: str
    message: str
    recommendation: str


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Audit a skill folder for ClawHub and skills.sh discoverability."
    )
    parser.add_argument("skill_path", help="Path to the skill folder")
    parser.add_argument(
        "--keywords",
        default="",
        help="Comma-separated keywords or phrases to require in the analysis",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Emit JSON instead of a text report",
    )
    return parser.parse_args()


def strip_wrapping_quotes(value: str) -> str:
    if len(value) >= 2 and value[0] == value[-1] and value[0] in {"'", '"'}:
        return value[1:-1]
    return value


def coerce_text(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, str):
        return value
    if isinstance(value, list):
        return " ".join(coerce_text(item) for item in value if coerce_text(item))
    if isinstance(value, dict):
        return json.dumps(value, ensure_ascii=False, sort_keys=True)
    return str(value)


def fold_block_lines(lines: list[str], style: str) -> str:
    if style == "|":
        return "\n".join(lines).rstrip()

    folded: list[str] = []
    paragraph: list[str] = []
    for line in lines:
        if line.strip():
            paragraph.append(line.strip())
            continue
        if paragraph:
            folded.append(" ".join(paragraph))
            paragraph = []
        folded.append("")
    if paragraph:
        folded.append(" ".join(paragraph))
    return "\n".join(folded).rstrip()


def parse_frontmatter(text: str) -> tuple[dict[str, Any], str]:
    match = re.match(r"^---\n(.*?)\n---\n?(.*)$", text, re.DOTALL)
    if not match:
        raise ValueError("SKILL.md is missing valid YAML frontmatter delimited by ---")
    raw_frontmatter = match.group(1)
    body = match.group(2)
    data: dict[str, Any] = {}
    lines = raw_frontmatter.splitlines()
    i = 0
    while i < len(lines):
        line = lines[i]
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            i += 1
            continue
        if line.startswith((" ", "\t")):
            raise ValueError(f"Unsupported frontmatter indentation at top level: {line}")

        key, sep, remainder = line.partition(":")
        if not sep:
            raise ValueError(f"Unsupported frontmatter line: {line}")
        key = key.strip()
        remainder = remainder.strip()

        if remainder in {"|", ">"}:
            style = remainder
            i += 1
            block_indent = None
            block_lines: list[str] = []
            while i < len(lines):
                current = lines[i]
                if not current.strip():
                    block_lines.append("")
                    i += 1
                    continue
                current_indent = len(current) - len(current.lstrip(" "))
                if block_indent is None:
                    if current_indent == 0:
                        break
                    block_indent = current_indent
                if current_indent < block_indent:
                    break
                block_lines.append(current[block_indent:])
                i += 1
            data[key] = fold_block_lines(block_lines, style)
            continue

        if remainder == "":
            i += 1
            nested_values: list[str] = []
            nested_indent = None
            while i < len(lines):
                current = lines[i]
                if not current.strip():
                    i += 1
                    continue
                current_indent = len(current) - len(current.lstrip(" "))
                if nested_indent is None:
                    if current_indent == 0:
                        break
                    nested_indent = current_indent
                if current_indent < nested_indent:
                    break
                nested_values.append(current[nested_indent:])
                i += 1
            if nested_values and all(item.lstrip().startswith("- ") for item in nested_values):
                data[key] = [item.lstrip()[2:].strip() for item in nested_values]
            else:
                data[key] = "\n".join(nested_values).rstrip()
            continue

        data[key] = strip_wrapping_quotes(remainder)
        i += 1
    return data, body


def tokenize(text: str) -> list[str]:
    return re.findall(r"[a-z0-9][a-z0-9+-]{1,}", text.lower())


def phrase_present(text: str, phrase: str) -> bool:
    escaped = re.escape(phrase.strip().lower())
    return bool(re.search(rf"\b{escaped}\b", text.lower()))


def collect_candidate_keywords(
    slug: str,
    frontmatter: dict[str, Any],
    body: str,
    explicit_keywords: list[str],
) -> list[str]:
    phrases: list[str] = []
    if explicit_keywords:
        phrases.extend(explicit_keywords)
    name = coerce_text(frontmatter.get("name", ""))
    description = coerce_text(frontmatter.get("description", ""))
    first_sentence = description.split(".")[0].strip()
    if first_sentence:
        phrases.append(first_sentence)
    for part in re.split(r",| or | and | when the user asks", description, flags=re.IGNORECASE):
        part = " ".join(part.split())
        if 3 <= len(part) <= 80:
            phrases.append(part)
    for phrase in [slug.replace("-", " "), name.replace("-", " ")]:
        cleaned = " ".join(phrase.split())
        if cleaned:
            phrases.append(cleaned)
    tokens = []
    for token in tokenize(f"{slug} {name} {description}"):
        if token not in STOPWORDS and len(token) > 2:
            tokens.append(token)
    top_tokens = []
    for token in tokens:
        if token not in top_tokens:
            top_tokens.append(token)
    headings = re.findall(r"^##?\s+(.+)$", body, re.MULTILINE)
    for heading in headings[:5]:
        phrases.append(heading.strip())
    phrases.extend(top_tokens[:8])
    deduped = []
    seen = set()
    for item in phrases:
        normalized = item.lower().strip()
        if not normalized or normalized in seen:
            continue
        seen.add(normalized)
        deduped.append(item.strip())
    return deduped


def score_ratio(passed: int, total: int) -> int:
    if total == 0:
        return 0
    return round((passed / total) * 100)


def detect_compatibility(skill_dir: Path, frontmatter: dict[str, Any]) -> dict[str, str]:
    skill_exists = (skill_dir / "SKILL.md").exists()
    cursor_hints = any(path.exists() for path in [skill_dir / ".cursor" / "rules"])
    claude_hints = any(
        path.exists()
        for path in [skill_dir / ".claude" / "agents", skill_dir / ".claude" / "commands"]
    )
    codex_hints = any(path.exists() for path in [skill_dir / "AGENTS.md"])
    has_core_skill = skill_exists and bool(coerce_text(frontmatter.get("name"))) and bool(
        coerce_text(frontmatter.get("description"))
    )
    return {
        "openclaw": "verified" if has_core_skill else "missing",
        "codex": "verified" if codex_hints else ("unverified" if has_core_skill else "missing"),
        "claude_code": "verified" if claude_hints else ("unverified" if has_core_skill else "missing"),
        "cursor": "verified" if cursor_hints else ("unverified" if has_core_skill else "missing"),
    }


def analyze(skill_dir: Path, explicit_keywords: list[str]) -> dict[str, Any]:
    skill_file = skill_dir / "SKILL.md"
    if not skill_file.exists():
        raise FileNotFoundError(f"Missing file: {skill_file}")

    text = skill_file.read_text(encoding="utf-8")
    frontmatter, body = parse_frontmatter(text)
    slug = skill_dir.name
    candidate_keywords = collect_candidate_keywords(slug, frontmatter, body, explicit_keywords)

    findings: list[Finding] = []
    description = coerce_text(frontmatter.get("description", ""))
    name = coerce_text(frontmatter.get("name", ""))
    top_section = "\n".join(body.splitlines()[:40])
    example_count = len(
        re.findall(
            r"(^-\s+`|^\d+\.\s+`|^##\s+Example|example prompts|^-\s+.+\?$)",
            body,
            re.MULTILINE | re.IGNORECASE,
        )
    )

    metadata_checks = {
        "name_matches_slug": name == slug,
        "description_exists": bool(description.strip()),
        "description_has_use_when": "use when" in description.lower(),
        "description_reasonable_length": 110 <= len(description) <= 420,
    }
    query_hits = [kw for kw in candidate_keywords if phrase_present(text, kw)]
    concise_keywords = [
        kw for kw in candidate_keywords if len(kw) <= 40 and len(kw.split()) <= 5
    ]
    focus_keywords = concise_keywords[: min(8, len(concise_keywords))] or candidate_keywords[
        : min(8, len(candidate_keywords))
    ]
    description_hits = sum(1 for kw in focus_keywords if phrase_present(description, kw))
    top_hits = sum(1 for kw in focus_keywords if phrase_present(top_section, kw))
    query_checks = {
        "keywords_in_description": description_hits >= max(2, len(focus_keywords) // 3),
        "keywords_in_top_section": top_hits >= max(2, len(focus_keywords) // 3),
        "body_has_examples": example_count >= 3,
        "body_has_constraints": bool(re.search(r"constraint|prerequisite|important|note", body, re.IGNORECASE)),
    }
    platform_checks = {
        "slug_is_literal": bool(re.search(r"[a-z0-9]+-[a-z0-9]+", slug)),
        "clawhub_exact_match_terms": any(
            phrase_present(slug.replace("-", " "), kw) or phrase_present(name.replace("-", " "), kw)
            for kw in explicit_keywords
        )
        if explicit_keywords
        else True,
        "freshness_hooks": bool(re.search(r"update|maintain|recent|version", text, re.IGNORECASE)),
        "trust_signals": bool(re.search(r"prerequisite|cost|limit|env|tool|requires", text, re.IGNORECASE)),
    }
    compatibility = detect_compatibility(skill_dir, frontmatter)

    if not metadata_checks["description_has_use_when"]:
        findings.append(
            Finding(
                "high",
                "metadata",
                "Frontmatter description does not include an explicit 'Use when ...' trigger.",
                "Rewrite the description to include user intents, task variations, and trigger phrasing.",
            )
        )
    if not metadata_checks["description_reasonable_length"]:
        findings.append(
            Finding(
                "medium",
                "metadata",
                "Frontmatter description is either too short to cover query variants or too long for list-page scanning.",
                "Keep the description concrete and usually within roughly 110 to 420 characters.",
            )
        )
    if not query_checks["body_has_examples"]:
        findings.append(
            Finding(
                "high",
                "query-coverage",
                "SKILL.md does not show enough realistic examples near the top of the file.",
                "Add at least 3 concrete user-style example prompts covering exact tasks and close synonyms.",
            )
        )
    if not query_checks["keywords_in_description"]:
        findings.append(
            Finding(
                "high",
                "query-coverage",
                "Core task phrases are underrepresented in the frontmatter description.",
                "Move exact task words, object names, and user-intent language into the first sentence.",
            )
        )
    if not query_checks["keywords_in_top_section"]:
        findings.append(
            Finding(
                "medium",
                "query-coverage",
                "The top section of SKILL.md does not reinforce the main search phrases strongly enough.",
                "Surface examples, constraints, and commands that repeat the job-to-be-done vocabulary.",
            )
        )
    if not platform_checks["trust_signals"]:
        findings.append(
            Finding(
                "medium",
                "conversion",
                "The skill lacks strong trust or conversion signals such as prerequisites, tool requirements, or limits.",
                "Add truthful prerequisites, setup notes, constraints, and cost or rate-limit guidance.",
            )
        )
    if explicit_keywords and not platform_checks["clawhub_exact_match_terms"]:
        findings.append(
            Finding(
                "high",
                "clawhub",
                "Explicit target keywords do not appear in the slug or skill name, which weakens exact or prefix matching.",
                "Consider a more literal slug or name if the current brand term is not itself a search term.",
            )
        )
    metadata_score = score_ratio(sum(metadata_checks.values()), len(metadata_checks))
    query_score = score_ratio(sum(query_checks.values()), len(query_checks))
    platform_score = score_ratio(sum(platform_checks.values()), len(platform_checks))
    compatibility_score = round(
        (
            sum(
                1.0 if status == "verified" else 0.5 if status == "unverified" else 0.0
                for status in compatibility.values()
            )
            / len(compatibility)
        )
        * 100
    )
    overall_score = round(
        (metadata_score * 0.30) + (query_score * 0.30) + (platform_score * 0.25) + (compatibility_score * 0.15)
    )

    recommendations = []
    if not metadata_checks["description_has_use_when"] or not metadata_checks["description_reasonable_length"]:
        recommendations.append(
            "Rewrite the frontmatter description so the first sentence names the action, object, outcome, and 'Use when ...' triggers."
        )
    if not query_checks["body_has_examples"]:
        recommendations.append("Add 3 to 5 realistic user-style example prompts near the top of SKILL.md.")
    if not query_checks["keywords_in_description"] or not query_checks["keywords_in_top_section"]:
        recommendations.append(
            "Mirror the main task phrase in the slug, name, description, and first screen."
        )
    if not platform_checks["trust_signals"]:
        recommendations.append(
            "State prerequisites, constraints, and trust signals clearly to improve conversion after discovery."
        )
    if explicit_keywords and not platform_checks["clawhub_exact_match_terms"]:
        recommendations.append(
            "Consider a more literal slug or public name if exact-match search terms matter more than the current brand phrasing."
        )
    compatibility_notes = []
    if compatibility["openclaw"] != "verified":
        compatibility_notes.append("Missing `SKILL.md`; OpenClaw-style skill packaging is not valid yet.")
    if compatibility["codex"] == "unverified":
        compatibility_notes.append("Codex compatibility is unverified; no `AGENTS.md` hint was found.")
    elif compatibility["codex"] == "missing":
        compatibility_notes.append("Codex compatibility is missing because the core skill package is incomplete.")
    if compatibility["claude_code"] == "unverified":
        compatibility_notes.append("Claude Code compatibility is unverified; no `.claude/agents` or `.claude/commands` files were found.")
    elif compatibility["claude_code"] == "missing":
        compatibility_notes.append("Claude Code compatibility is missing because the core skill package is incomplete.")
    if compatibility["cursor"] == "unverified":
        compatibility_notes.append("Cursor compatibility is unverified; no `.cursor/rules` files were found.")
    elif compatibility["cursor"] == "missing":
        compatibility_notes.append("Cursor compatibility is missing because the core skill package is incomplete.")

    return {
        "skill_path": str(skill_dir),
        "slug": slug,
        "frontmatter": frontmatter,
        "candidate_keywords": candidate_keywords,
        "query_hits": query_hits,
        "scores": {
            "overall": overall_score,
            "metadata": metadata_score,
            "query_coverage": query_score,
            "platform_fit": platform_score,
            "compatibility": compatibility_score,
        },
        "checks": {
            "metadata": metadata_checks,
            "query_coverage": query_checks,
            "platform_fit": platform_checks,
        },
        "compatibility": compatibility,
        "compatibility_notes": compatibility_notes,
        "findings": [asdict(finding) for finding in findings],
        "recommendations": recommendations,
    }


def print_text_report(report: dict[str, Any]) -> None:
    scores = report["scores"]
    print(f"Skill SEO Audit: {report['slug']}")
    print(f"Path: {report['skill_path']}")
    print(
        "Scores: "
        f"overall={scores['overall']} "
        f"metadata={scores['metadata']} "
        f"query_coverage={scores['query_coverage']} "
        f"platform_fit={scores['platform_fit']} "
        f"compatibility={scores['compatibility']}"
    )
    print("")
    print("Compatibility:")
    for platform, status in report["compatibility"].items():
        print(f"- {platform}: {status}")
    if report["compatibility_notes"]:
        print("")
        print("Compatibility notes:")
        for note in report["compatibility_notes"]:
            print(f"- {note}")
    print("")
    print("Candidate keywords:")
    for keyword in report["candidate_keywords"][:12]:
        print(f"- {keyword}")
    print("")
    print("Findings:")
    if not report["findings"]:
        print("- No critical discoverability issues detected by static heuristics.")
    else:
        for finding in report["findings"]:
            print(
                f"- [{finding['severity']}] {finding['area']}: {finding['message']} "
                f"Recommendation: {finding['recommendation']}"
            )
    print("")
    print("Recommendations:")
    for item in report["recommendations"]:
        print(f"- {item}")


def main() -> int:
    args = parse_args()
    skill_dir = Path(args.skill_path).expanduser().resolve()
    explicit_keywords = [item.strip() for item in args.keywords.split(",") if item.strip()]
    try:
        report = analyze(skill_dir, explicit_keywords)
    except Exception as exc:  # pragma: no cover - CLI error path
        print(f"error: {exc}", file=sys.stderr)
        return 1
    if args.json:
        json.dump(report, sys.stdout, ensure_ascii=False, indent=2)
        print("")
    else:
        print_text_report(report)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
