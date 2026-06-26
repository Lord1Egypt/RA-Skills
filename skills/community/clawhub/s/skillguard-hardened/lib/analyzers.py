from __future__ import annotations

import math
import re
from typing import Any

from lib.discovery import SkillTarget

RULE_ID_ALIASES = {
    "network_exfiltration": "network_upload",
    "credential_access": "credential_reference",
}


def _clip(text: str, width: int = 220) -> str:
    text = " ".join(text.strip().split())
    if len(text) <= width:
        return text
    return text[: width - 3] + "..."


def _file_weight(policy: dict[str, Any], relative_path: str) -> float:
    multiplier = 1.0
    for override in policy.get("path_weight_overrides", []):
        if any(fragment in relative_path for fragment in override.get("path_contains", [])):
            multiplier = min(multiplier, float(override.get("multiplier", 1.0)))
    return multiplier


def _line_is_non_executing_context(relative_path: str, line: str) -> bool:
    stripped = line.strip()
    if not stripped:
        return True
    if stripped.startswith("#"):
        return True
    if stripped.startswith("echo "):
        return True
    if relative_path.endswith(".md") and stripped.startswith(("```", "|", "-", "*", ">")):
        return True
    return False


def _canonical_rule_id(rule_id: str) -> str:
    return RULE_ID_ALIASES.get(rule_id, rule_id)


def _is_placeholder_secret_line(line: str) -> bool:
    lowered = line.lower()
    placeholders = (
        "your_api_key",
        "your api key",
        "example",
        "placeholder",
        "sample",
        "dummy",
        "test_key",
        "replace_me",
        "<api_key>",
        "<token>",
        "moltbook_xxx",
        "claim_xxx",
        "sk-xxxx",
        "xxxx",
        "xxxxx",
        "***",
    )
    return any(token in lowered for token in placeholders)


def _iter_relevant_lines(relative_path: str, content: str) -> list[str]:
    if not relative_path.endswith(".md"):
        return content.splitlines()

    relevant_lines: list[str] = []
    in_code_fence = False
    for raw_line in content.splitlines():
        stripped = raw_line.strip()
        if stripped.startswith("```"):
            in_code_fence = not in_code_fence
            continue
        if in_code_fence:
            continue
        relevant_lines.append(raw_line)
    return relevant_lines


def analyze_static(target: SkillTarget, policy: dict[str, Any]) -> dict[str, Any]:
    findings: list[dict[str, Any]] = []
    capabilities: dict[str, list[str]] = {}
    max_matches = int(policy.get("size_limits", {}).get("max_matches_per_rule", 5))
    exceptions = policy.get("rule_exceptions", [])

    def is_excepted(rule_id: str, file_path: str) -> bool:
        canonical_rule_id = _canonical_rule_id(rule_id)
        for exception in exceptions:
            skill_names = set(exception.get("skill_names", []))
            rule_ids = {_canonical_rule_id(str(value)) for value in exception.get("rule_ids", [])}
            file_globs = exception.get("file_globs", [])
            if skill_names and target.name not in skill_names:
                continue
            if rule_ids and canonical_rule_id not in rule_ids:
                continue
            if file_globs and not any(file_glob in file_path for file_glob in file_globs):
                continue
            return True
        return False

    compiled_rules = []
    for rule in policy.get("rules", []):
        compiled_rules.append((rule, re.compile(rule["pattern"], re.IGNORECASE | re.MULTILINE)))

    compiled_capabilities = {
        name: [re.compile(pattern, re.IGNORECASE | re.MULTILINE) for pattern in patterns]
        for name, patterns in policy.get("capability_patterns", {}).items()
    }

    for file_info in target.files:
        file_weight = _file_weight(policy, file_info.relative_path)
        if file_info.is_symlink:
            findings.append(
                {
                    "rule_id": "symlink_entry",
                    "title": "Symlink entry detected",
                    "severity": "medium",
                    "weight": 20,
                    "file": file_info.relative_path,
                    "evidence": ["Symlinked files can escape intended directory boundaries."],
                }
            )
            continue

        if not file_info.is_text:
            if file_info.size > 0:
                findings.append(
                    {
                        "rule_id": "binary_payload",
                        "title": "Binary or opaque payload",
                        "severity": "medium",
                        "weight": 15,
                        "file": file_info.relative_path,
                        "evidence": [f"Non-text payload detected ({file_info.size} bytes)."],
                    }
                )
            continue

        content = file_info.content or ""
        for rule, compiled in compiled_rules:
            if is_excepted(rule["id"], file_info.relative_path):
                continue

            evidence = []
            seen_lines = 0
            matched_lines = 0
            for raw_line in _iter_relevant_lines(file_info.relative_path, content):
                if _line_is_non_executing_context(file_info.relative_path, raw_line):
                    continue
                if compiled.search(raw_line):
                    if rule["id"] == "hardcoded_secret" and _is_placeholder_secret_line(raw_line):
                        continue
                    evidence.append(_clip(raw_line))
                    seen_lines += 1
                    matched_lines += 1
                if seen_lines >= max_matches:
                    break

            if matched_lines == 0:
                continue

            weighted_value = max(1, int(math.ceil(int(rule["weight"]) * file_weight)))

            findings.append(
                {
                    "rule_id": rule["id"],
                    "title": rule["title"],
                    "severity": rule["severity"],
                    "weight": weighted_value,
                    "base_weight": int(rule["weight"]),
                    "weight_multiplier": file_weight,
                    "file": file_info.relative_path,
                    "evidence": evidence or [rule["description"]],
                    "category": rule["category"],
                    "description": rule["description"],
                }
            )

        for capability_name, patterns in compiled_capabilities.items():
            for compiled in patterns:
                if compiled.search(content):
                    capabilities.setdefault(capability_name, [])
                    if file_info.relative_path not in capabilities[capability_name]:
                        capabilities[capability_name].append(file_info.relative_path)
                    break

    if not any(file_info.relative_path == "SKILL.md" for file_info in target.files):
        findings.append(
            {
                "rule_id": "missing_skill_manifest",
                "title": "Missing SKILL.md",
                "severity": "medium",
                "weight": 10,
                "file": target.name,
                "evidence": ["Skill package has no SKILL.md declaration."],
            }
        )

    return {
        "findings": findings,
        "capabilities": capabilities,
        "summary": {
            "file_count": len(target.files),
            "text_file_count": sum(1 for file_info in target.files if file_info.is_text),
        },
    }
