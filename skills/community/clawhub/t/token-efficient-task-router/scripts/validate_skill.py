#!/usr/bin/env python3
"""Validate the token-efficient-task-router skill package."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


REQUIRED_DIRS = [
    "references",
    "templates",
    "examples",
    "tests",
    "scripts",
]

REQUIRED_FILES = [
    ".gitignore",
    "SKILL.md",
    "LICENSE",
    "README.md",
    "README.en.md",
    "GUIDE.md",
    "GUIDE.en.md",
    "VERSION",
    "CHANGELOG.md",
    "references/chat_confirmation_affordances.md",
    "references/codebuddy_adaptation.md",
    "references/focus_activation_rules.md",
    "references/need_calibration.md",
    "references/mode_router.md",
    "references/platform_quick_commands.md",
    "references/ask_mode.md",
    "references/plan_mode.md",
    "references/craft_mode.md",
    "references/expert_mode.md",
    "references/risk_levels.md",
    "references/token_budget_modes.md",
    "references/file_safety_rules.md",
    "references/ambiguity_handling.md",
    "references/interactive_routing.md",
    "references/progressive_delivery_rules.md",
    "references/workbuddy_adaptation.md",
    "references/ima_copilot_adaptation.md",
    "references/ima_copilot_runtime_protocol.md",
    "templates/ask_mode_template.md",
    "templates/button_ready_confirmation_template.md",
    "templates/codebuddy_scope_confirmation_template.md",
    "templates/plan_mode_template.md",
    "templates/craft_mode_template.md",
    "templates/expert_mode_template.md",
    "templates/focus_selection_template.md",
    "templates/need_calibration_template.md",
    "templates/risk_assessment_template.md",
    "templates/confirmation_request_template.md",
    "templates/token_saving_report_template.md",
    "templates/interactive_routing_prompt_template.md",
    "templates/ima_copilot_lite_response_template.md",
    "examples/example_button_guided_chat.md",
    "examples/example_codebuddy_bugfix.md",
    "examples/example_codebuddy_refactor.md",
    "examples/example_focus_activation.md",
    "examples/example_khazix_pairing.md",
    "examples/example_need_calibration.md",
    "examples/example_simple_craft_task.md",
    "examples/example_complex_plan_task.md",
    "examples/example_error_ask_task.md",
    "examples/example_expert_escalation.md",
    "examples/example_workbuddy_file_task.md",
    "examples/example_ima_knowledge_task.md",
    "examples/example_interactive_routing.md",
    "examples/example_ima_lite_session.md",
    "tests/sample_inputs.md",
    "tests/expected_output_checklist.md",
    "scripts/validate_skill.py",
    "scripts/package_skill.py",
]

SKILL_SECTIONS = [
    "## Purpose",
    "## When to use this skill",
    "## When not to use this skill",
    "## Core principles",
    "## Focus activation rules",
    "## Need calibration rules",
    "## Progressive delivery rules",
    "## Chat confirmation affordances",
    "## Quick-start command prompts",
    "## Task classification",
    "## Mode routing rules",
    "## Interactive Routing Prompt",
    "## Ask Mode",
    "## Plan Mode",
    "## Craft Mode",
    "## Expert Mode",
    "## Risk levels",
    "## Token budget modes",
    "## Token saving protocol",
    "## File safety rules",
    "## Ambiguity handling rules",
    "## WorkBuddy adaptation",
    "## CodeBuddy adaptation",
    "## iMA Copilot adaptation",
    "## Confirmation gates",
    "## Examples",
]

FRONTMATTER_KEY_RE = re.compile(r"^[a-z][a-z0-9_-]*:\s*.+$")
KEBAB_CASE_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
TEXT_SUFFIXES = {".md", ".py", ".txt", ".json", ".yaml", ".yml", ".toml", ".ini"}

DANGEROUS_CONTENT_PATTERNS = {
    "api_key_assignment": re.compile(r"api[_ -]?key\s*[:=]\s*['\"][^'\"]+['\"]", re.IGNORECASE),
    "secret_assignment": re.compile(r"(secret|client_secret)\s*[:=]\s*['\"][^'\"]+['\"]", re.IGNORECASE),
    "token_assignment": re.compile(r"(access_token|refresh_token|auth_token)\s*[:=]\s*['\"][^'\"]+['\"]", re.IGNORECASE),
    "cookie_assignment": re.compile(r"cookie\s*[:=]\s*['\"][^'\"]+['\"]", re.IGNORECASE),
    "bearer_token": re.compile(r"bearer\s+[a-z0-9._-]{16,}", re.IGNORECASE),
    "sk_token": re.compile(r"sk-[a-z0-9]{16,}", re.IGNORECASE),
}

AUTO_UPLOAD_PATTERNS = {
    "scp_upload": re.compile(r"\bscp\b", re.IGNORECASE),
    "rsync_upload": re.compile(r"\brsync\b", re.IGNORECASE),
    "s3_upload": re.compile(r"\baws\s+s3\s+(cp|sync)\b", re.IGNORECASE),
    "curl_upload": re.compile(r"\bcurl\b[^\n]*\s-T\s", re.IGNORECASE),
    "requests_post": re.compile(r"requests\.post\s*\(", re.IGNORECASE),
    "boto3_upload": re.compile(r"upload_file|upload_fileobj", re.IGNORECASE),
}

DANGEROUS_COMMAND_PATTERNS = {
    "remote_pipe_shell": re.compile(r"(curl|wget)[^\n]*\|\s*(sh|bash)", re.IGNORECASE),
    "rm_rf": re.compile(r"\brm\s+-rf\b"),
    "chmod_777": re.compile(r"\bchmod\s+777\b"),
    "os_system": re.compile(r"\bos\.system\s*\("),
    "eval_call": re.compile(r"\beval\s*\("),
    "exec_call": re.compile(r"\bexec\s*\("),
    "shell_true": re.compile(r"shell\s*=\s*True"),
}

REQUIRED_TEXT_SNIPPETS = {
    "guide_overview": ("GUIDE.md", "## 这个 Skill 是做什么的"),
    "guide_language_switch_zh": ("GUIDE.md", "GUIDE.en.md"),
    "guide_language_switch_en": ("GUIDE.en.md", "GUIDE.md"),
    "guide_en_overview": ("GUIDE.en.md", "## What This Skill Does"),
    "license_text": ("LICENSE", "MIT License"),
    "readme_language_switch_zh": ("README.md", "README.en.md"),
    "readme_language_switch_en": ("README.en.md", "README.md"),
    "chat_confirmation": ("references/chat_confirmation_affordances.md", "button-ready confirmation block"),
    "codebuddy": ("references/codebuddy_adaptation.md", "CodeBuddy scope gate"),
    "focus_activation": ("references/focus_activation_rules.md", "smallest useful focus bundle"),
    "need_calibration": ("references/need_calibration.md", "Necessary-only token logic"),
    "mode_router": ("references/mode_router.md", "Interactive Routing Prompt"),
    "ask_mode": ("references/ask_mode.md", "Ask Mode"),
    "plan_mode": ("references/plan_mode.md", "Plan Mode"),
    "craft_mode": ("references/craft_mode.md", "Craft Mode"),
    "expert_mode": ("references/expert_mode.md", "Expert Mode"),
    "workbuddy": ("references/workbuddy_adaptation.md", "WorkBuddy"),
    "ima": ("references/ima_copilot_adaptation.md", "iMA Copilot"),
    "ima_runtime": ("references/ima_copilot_runtime_protocol.md", "Understanding lock sentence"),
    "progressive_delivery": ("references/progressive_delivery_rules.md", "Delivery levels"),
    "platform_quick_commands": ("references/platform_quick_commands.md", "Platform Quick Commands"),
    "token_saving": ("SKILL.md", "Always optimize for ROI per token."),
    "interactive_prompt": ("templates/interactive_routing_prompt_template.md", "任务路由确认"),
    "button_ready_template": ("templates/button_ready_confirmation_template.md", "按钮友好型确认"),
    "codebuddy_template": ("templates/codebuddy_scope_confirmation_template.md", "CodeBuddy 范围确认"),
    "focus_template": ("templates/focus_selection_template.md", "Focus Selection"),
    "need_calibration_template": ("templates/need_calibration_template.md", "真实需求校准"),
    "ima_lite_template": ("templates/ima_copilot_lite_response_template.md", "iMA 理解锁定句"),
    "readme_version": ("README.md", "当前版本"),
    "readme_en_version": ("README.en.md", "## Repository Structure"),
}

SEMVER_RE = re.compile(r"^\d+\.\d+\.\d+$")


def parse_frontmatter(skill_file: Path) -> tuple[dict[str, str], list[str]]:
    errors: list[str] = []
    lines = skill_file.read_text(encoding="utf-8").splitlines()
    if len(lines) < 3 or lines[0].strip() != "---":
        return {}, ["SKILL.md is missing YAML frontmatter."]

    closing_index = None
    for index in range(1, len(lines)):
        if lines[index].strip() == "---":
            closing_index = index
            break
    if closing_index is None:
        return {}, ["SKILL.md frontmatter is not closed with '---'."]

    frontmatter_lines = lines[1:closing_index]
    if not frontmatter_lines:
        return {}, ["SKILL.md frontmatter is empty."]

    data: dict[str, str] = {}
    for line in frontmatter_lines:
        if not FRONTMATTER_KEY_RE.match(line):
            errors.append(f"Invalid frontmatter line: {line}")
            continue
        key, value = line.split(":", 1)
        data[key.strip()] = value.strip()

    allowed_keys = {"name", "description"}
    actual_keys = set(data)
    missing = allowed_keys - actual_keys
    extra = actual_keys - allowed_keys
    if missing:
        errors.append(f"Frontmatter missing required keys: {', '.join(sorted(missing))}")
    if extra:
        errors.append(f"Frontmatter contains unsupported keys: {', '.join(sorted(extra))}")
    return data, errors


def iter_text_files(root: Path):
    for path in root.rglob("*"):
        if path.is_dir():
            continue
        if path.suffix.lower() in TEXT_SUFFIXES or path.name in {"SKILL.md", "README.md"}:
            yield path


def read_version(root: Path) -> tuple[str | None, list[str]]:
    errors: list[str] = []
    version_file = root / "VERSION"
    if not version_file.is_file():
        return None, ["Missing VERSION file."]

    version = version_file.read_text(encoding="utf-8").strip()
    if not version:
        return None, ["VERSION file is empty."]
    if not SEMVER_RE.fullmatch(version):
        return version, ["VERSION file must use semver like 0.1.0."]
    return version, errors


def validate_skill_root(root: Path) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []

    if not root.exists():
        return [f"Skill root does not exist: {root}"], warnings
    if not root.is_dir():
        return [f"Skill root is not a directory: {root}"], warnings

    for required_dir in REQUIRED_DIRS:
        if not (root / required_dir).is_dir():
            errors.append(f"Missing required directory: {required_dir}")

    for required_file in REQUIRED_FILES:
        if not (root / required_file).is_file():
            errors.append(f"Missing required file: {required_file}")

    version, version_errors = read_version(root)
    errors.extend(version_errors)

    skill_file = root / "SKILL.md"
    if skill_file.is_file():
        frontmatter, frontmatter_errors = parse_frontmatter(skill_file)
        errors.extend(frontmatter_errors)
        if frontmatter:
            name = frontmatter.get("name", "")
            if name and not KEBAB_CASE_RE.fullmatch(name):
                errors.append("Frontmatter name is not valid kebab-case.")
            if name and name != "token-efficient-task-router":
                warnings.append("Frontmatter name differs from the requested canonical skill name.")
            description = frontmatter.get("description", "")
            if not description:
                errors.append("Frontmatter description is empty.")

        skill_content = skill_file.read_text(encoding="utf-8")
        for section in SKILL_SECTIONS:
            if section not in skill_content:
                errors.append(f"Missing SKILL.md section: {section}")

    for path in root.rglob("*"):
        if path.is_symlink():
            errors.append(f"Symlink is not allowed: {path.relative_to(root)}")

    for label, (relative_path, snippet) in REQUIRED_TEXT_SNIPPETS.items():
        path = root / relative_path
        if not path.is_file():
            continue
        content = path.read_text(encoding="utf-8", errors="ignore")
        if snippet not in content:
            errors.append(f"Required content for {label} not found in {relative_path}")

    changelog_file = root / "CHANGELOG.md"
    if version and changelog_file.is_file():
        changelog_content = changelog_file.read_text(encoding="utf-8", errors="ignore")
        if f"## v{version}" not in changelog_content:
            errors.append(f"CHANGELOG.md does not contain an entry for v{version}.")

    readme_file = root / "README.md"
    if version and readme_file.is_file():
        readme_content = readme_file.read_text(encoding="utf-8", errors="ignore")
        if (
            f"Current version: `v{version}`" not in readme_content
            and f"当前版本：`v{version}`" not in readme_content
        ):
            errors.append(f"README.md does not declare the current version as v{version}.")

    for text_file in iter_text_files(root):
        content = text_file.read_text(encoding="utf-8", errors="ignore")
        relative = text_file.relative_to(root)
        for label, pattern in DANGEROUS_CONTENT_PATTERNS.items():
            if pattern.search(content):
                errors.append(f"Suspicious credential-like content ({label}) found in {relative}")
        if relative.as_posix() == "scripts/validate_skill.py":
            continue
        for label, pattern in AUTO_UPLOAD_PATTERNS.items():
            if pattern.search(content):
                errors.append(f"Auto-upload pattern ({label}) found in {relative}")
        for label, pattern in DANGEROUS_COMMAND_PATTERNS.items():
            if pattern.search(content):
                errors.append(f"Dangerous command pattern ({label}) found in {relative}")

    safety_phrases = [
        "Without user confirmation",
        "未经确认",
        "确认执行",
    ]
    combined = "\n".join(
        (root / rel).read_text(encoding="utf-8", errors="ignore")
        for rel in ["SKILL.md", "README.md", "references/file_safety_rules.md"]
        if (root / rel).is_file()
    )
    if not any(phrase in combined for phrase in safety_phrases):
        errors.append("Missing confirmation-gate language for file safety.")

    return errors, warnings


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate the token-efficient-task-router skill.")
    parser.add_argument(
        "path",
        nargs="?",
        default=Path(__file__).resolve().parents[1],
        type=Path,
        help="Path to the skill root. Defaults to the parent folder of this script.",
    )
    args = parser.parse_args()
    root = args.path.resolve()

    errors, warnings = validate_skill_root(root)
    print(f"Validating: {root}")
    if errors:
        print("[FAIL] Blocking issues found:")
        for item in errors:
            print(f"  - {item}")
    else:
        print("[OK] No blocking issues found.")

    if warnings:
        print("[WARN] Non-blocking notes:")
        for item in warnings:
            print(f"  - {item}")

    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
