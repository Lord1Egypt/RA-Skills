#!/usr/bin/env python3
"""Smoke-check Research Mode skill and documentation contracts."""
from __future__ import annotations

import argparse
import json
import re
import shlex
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
SKILL_DIR = SCRIPT_DIR.parent
REPO_ROOT = SKILL_DIR.parent.parent

if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from research_mode import build_parser  # noqa: E402

REQUIRED_DOC_PATHS = [
    SKILL_DIR / "SKILL.md",
    SKILL_DIR / "README.md",
    SKILL_DIR / "TROUBLESHOOTING.md",
    SKILL_DIR / "ARCHITECTURE.md",
    SKILL_DIR / "docs" / "CLI.md",
    SKILL_DIR / "docs" / "STATE_VERSIONING.md",
    SKILL_DIR / "RELEASING.md",
    SKILL_DIR / "RELEASE_NOTES.md",
    SKILL_DIR / "LICENSE",
    SKILL_DIR / "SECURITY.md",
    SKILL_DIR / "ROADMAP.md",
    SKILL_DIR / "CONTRIBUTING.md",
    SKILL_DIR / "AGENTS.md",
    SKILL_DIR / "examples" / "README.md",
    SKILL_DIR / "assets" / "README.md",
    SKILL_DIR / ".github" / "ISSUE_TEMPLATE" / "bug_report.yml",
    SKILL_DIR / ".github" / "ISSUE_TEMPLATE" / "feature_request.yml",
    SKILL_DIR / ".github" / "ISSUE_TEMPLATE" / "security_hardening.yml",
]

REQUIRED_SCHEMA_PATHS = [
    SKILL_DIR / "schemas" / "state.v2.schema.json",
    SKILL_DIR / "schemas" / "worker-result.v1.schema.json",
    SKILL_DIR / "schemas" / "adequacy.v1.schema.json",
    SKILL_DIR / "schemas" / "finalization.v1.schema.json",
    SKILL_DIR / "schemas" / "delivery-intent.v1.schema.json",
]

OPTIONAL_ASSET_PATHS = [
    SKILL_DIR / "assets" / "social-preview.png",
]

OPTIONAL_DOC_PATHS: list[Path] = []

FORBIDDEN_PATTERNS = {
    r"request-changes[^\n]*--feedback": "request-changes uses positional feedback text",
    r"Important v1\.2": "current docs should not lead with v1.2-era labels",
    r"Дата: 2026-04-0[45]": "current canonical docs should carry the refreshed date",
    r"MVP-движок": "current docs should not frame the baseline as MVP",
    r"Create a manual demo task": "README should be chat-first, not CLI-first",
    r"Acquire one worker lease": "README should not present worker lease acquisition as user quickstart",
    r"Создать demo-задачу": "README should be chat-first, not CLI-first",
    r"Взять одну рабочую блокировку": "README should not present worker lease acquisition as user quickstart",
}

PUBLIC_PRIVATE_MARKER_PATTERNS = {
    r"/home/clawdbot": "public files must not expose the maintainer host path",
    r"/Users/[A-Za-z0-9_.-]+": "public files must not expose macOS home paths",
    r"C:\\\\Users\\\\": "public files must not expose Windows home paths",
    r"channel:[A-Za-z0-9_-]+": "public files must not expose messaging target ids",
    r"ghp_[A-Za-z0-9_]+": "public files must not expose GitHub tokens",
    r"xox[baprs]-[A-Za-z0-9-]+": "public files must not expose Slack tokens",
    r"OPENAI_API_KEY=": "public files must not expose API keys",
    r"ANTHROPIC_API_KEY=": "public files must not expose API keys",
}

PUBLIC_PRIVATE_MARKER_GLOBS = [
    "README.md",
    "SECURITY.md",
    "ROADMAP.md",
    "CONTRIBUTING.md",
    "RELEASE_NOTES.md",
    "docs/**/*.md",
    "schemas/*.json",
    "examples/**/*.md",
    "examples/**/*.json",
    "examples/**/*.jsonl",
    "examples/**/*.py",
    ".github/ISSUE_TEMPLATE/*.yml",
]

REQUIRED_SNIPPETS = {
    "SKILL.md": [
        "Do **not** use this skill for:",
        "Do not install dangerous or suspicious packages",
        "request-changes --id <research-id> \"what to change\"",
        "Research adequacy gate",
        "phase=verify",
        "result.adequacy",
        "delivery.review_ready=true",
        "scripts/check_research_mode.sh",
    ],
    "README.md": [
        "[English](#english) | [Русский](#русский)",
        "## English",
        "## Русский",
        "OpenClaw cron-based skill",
        "OpenClaw cron architecture",
        "### Installation",
        "### Установка",
        "clawhub install research-mode",
        "ClawHub skill installs are text-only",
        "### User Guide",
        "### Руководство пользователя",
        "#### How A Task Is Started",
        "#### Как запускается задача",
        "#### Launch Parameters",
        "#### Параметры запуска",
        "### Operations",
        "### Операции",
        "personal OpenClaw workflow",
        "поставляется как есть",
        "OPENCLAW_SKILLS_DIR",
        "openclaw skills check",
        'git clone https://github.com/VKambulov/research-mode.git "$OPENCLAW_SKILLS_DIR/research-mode"',
        "reject symlinks",
        "git init",
        "normal user entrypoint",
        "обычная пользовательская точка входа",
        "Launch Parameters",
        "Параметры запуска",
        "Depth Selection",
        "Выбор глубины",
        "During The Task",
        "Работа во время задачи",
        "Review And Delivery",
        "Ревью и доставка",
        "Research Adequacy Gate",
        "Проверка достаточности исследования",
        "phase=verify",
        "result.adequacy",
        "Common Work Patterns",
        "Частые рабочие сценарии",
        "Launch Mode 1: Chat-First Start",
        "Вариант запуска 1: через чат",
        "Launch Mode 2: Create And Schedule In One Step",
        "Вариант запуска 2: создать и запланировать одной командой",
        "Launch Mode 3: Create, Attach, Then Schedule",
        "Вариант запуска 3: создать, прикрепить материалы, затем запланировать",
        "Launch Mode 4: Manual Worker Iteration",
        "Вариант запуска 4: ручная рабочая итерация",
        "Review And Delivery Commands",
        "Команды ревью и доставки",
        "Quality Gates",
        "Проверки качества",
        "bash scripts/check_research_mode.sh",
        "`attach-url-as-md` accepts only `http://` and `https://` URLs and blocks local",
        "including redirect targets",
        "attach-url-as-md` принимает только URL с `http://` и `https://` и блокирует",
        "включая redirect targets",
        "ARCHITECTURE.md",
        "docs/CLI.md",
        "docs/STATE_VERSIONING.md",
        "schemas/",
        "TROUBLESHOOTING.md",
        "RELEASING.md",
        "RELEASE_NOTES.md",
        "SECURITY.md",
        "ROADMAP.md",
        "CONTRIBUTING.md",
        "recovery-log.jsonl",
        "AGENTS.md",
        ".github/ISSUE_TEMPLATE/",
        "examples/",
        "At A Glance",
        "Why It Stands Out",
        "Showcase",
        "Apache License, Version 2.0",
        "LICENSE",
        "check_research_mode_docs.py",
        "check_research_mode.sh",
        "CodeQL is not enabled in the baseline",
        "`prepare-runtime` may create a task-local virtual",
    ],
    "ROADMAP.md": [
        "[English](#english) | [Русский](#русский)",
        "## English",
        "## Русский",
        "OpenClaw-first",
        "not a standalone Python package",
        "### Now",
        "### Сейчас",
        "health",
        "reconcile",
        "private workspace",
        "task-local package",
        "Not planned",
        "Не планируется",
    ],
    "CONTRIBUTING.md": [
        "[English](#english) | [Русский](#русский)",
        "## English",
        "## Русский",
        "scripts/check_research_mode.sh",
        "uvx --from bandit bandit -q -r scripts -x scripts/selftest",
        "Public Contracts",
        "Публичные контракты",
        "Security-Sensitive Areas",
        "Зоны повышенного внимания",
        "sanitized traces",
        "живые task roots",
        "private security",
    ],
    "ARCHITECTURE.md": [
        "[English](#english) | [Русский](#русский)",
        "## English",
        "## Русский",
        "```mermaid",
        "distributed as an OpenClaw skill package",
        "state.json",
        "operator_next_action",
        "Why This Architecture Is Better For Durable Research",
        "Почему эта архитектура лучше для длительных исследований",
        "not as a standalone Python daemon",
        "Review before delivery",
        "Research Adequacy Gate",
        "result.adequacy",
        "Проверка достаточности исследования",
    ],
    "docs/CLI.md": [
        "[English](#english) | [Русский](#русский)",
        "Stable Operator Surface",
        "Стабильная операторская поверхность",
        "begin`, `finish`, and `fail`",
        "`health` is read-only",
        "fresh_continuation_recommended",
        "recover --refresh-derived",
        "`render-prompt`",
        "prepare-runtime --package",
        "not the normal user entrypoint",
    ],
    "docs/STATE_VERSIONING.md": [
        "[English](#english) | [Русский](#русский)",
        "Current public task state uses `version: 2`",
        "state_version",
        "lazy normalization",
        "scripts/selftest/test_state_compatibility.py",
        "Текущее публичное состояние задачи использует `version: 2`",
    ],
    "TROUBLESHOOTING.md": [
        "[English](#english) | [Русский](#русский)",
        "## English",
        "## Русский",
        "Diagnosis Order",
        "Порядок диагностики",
        "Task Does Not Progress",
        "Задача не продвигается",
        "Completion Was Rejected",
        "Завершение отклонено",
        "adequacy.operator_next_action",
        "проверка достаточности исследования",
        "Documentation Smoke Fails",
        "Не прошёл docs smoke",
        "Full Gate Fails",
        "Не прошла полная проверка",
        "health --id <research-id> --format text",
        "reconcile --id <research-id> --format text",
        "recover --id <research-id> --refresh-derived",
        "`health` is read-only",
        "fresh_continuation_recommended",
        "`reconcile` is the same read-only diagnostic surface",
        "`health` ничего не исправляет",
        "`reconcile` — такой же read-only диагностический интерфейс",
        "recovery-log.jsonl",
        "manual edits to `state.json`",
        "Ручное редактирование файлов",
    ],
    "RELEASING.md": [
        "[English](#english) | [Русский](#русский)",
        "## English",
        "## Русский",
        "OpenClaw cron-based skill package",
        "## Package boundary",
        "## Граница пакета",
        "Include in the public package",
        "Включать в публичный пакет",
        "Exclude from the public package",
        "Исключать из публичного пакета",
        "## Release gate",
        "## Контур релиза",
        "## Release safety review",
        "## Проверка безопасности релиза",
        "## Finalization contract",
        "README explains installation",
        "README объясняет установку",
        "TROUBLESHOOTING.md",
        "operator_next_action",
        "scripts/release_smoke.py",
        "scripts/check_research_mode.sh",
        "ARCHITECTURE.md",
        "RELEASE_NOTES.md",
        "SECURITY.md",
        "AGENTS.md",
        "ROADMAP.md",
        "CONTRIBUTING.md",
        "docs/",
        "schemas/",
        "examples/",
        "assets/",
        "ClawHub skill publishing currently uploads text-like files only",
        "Apache License, Version 2.0",
    ],
    "examples/README.md": [
        "Research Mode Examples",
        "web-capture-evaluation/",
        "rag-eval-tooling-matrix/",
        "research-trace/",
        "Showcase",
        "ClawHub installs only text-like files",
        "sanitized copy",
        "private workspace paths",
        "chat identifiers",
    ],
    "assets/README.md": [
        "Research Mode Assets",
        "social-preview.png",
        "1280x640 GitHub social preview image",
        "ClawHub skill installs are text-only",
        "generated visual background",
        "deterministic text",
    ],
    "RELEASE_NOTES.md": [
        "[English](#english) | [Русский](#русский)",
        "## English",
        "## Русский",
        "v0.1.0",
        "GitHub Actions CI",
        "OpenClaw cron-based skill",
        "Known limitations",
        "Известные ограничения",
        "Apache License, Version 2.0",
        "LICENSE",
        "scripts/release_smoke.py",
    ],
    "LICENSE": [
        "Apache License",
        "Version 2.0",
        "Copyright 2026 Vladislav Kambulov and Research Mode contributors",
        "Grant of Patent License",
        "END OF TERMS AND CONDITIONS",
    ],
    "SECURITY.md": [
        "[English](#english) | [Русский](#русский)",
        "## English",
        "## Русский",
        "tokens, webhooks, chat ids",
        "URL capture accepts only `http://` and `https://` and blocks local",
        "task-local",
        "prepare-runtime --package",
        "public/package-facing summaries",
        "untrusted data",
        "CodeQL is not enabled by default",
        "private security advisory",
    ],
    ".github/ISSUE_TEMPLATE/bug_report.yml": [
        "name: Bug report",
        "Version or commit",
        "OpenClaw version",
        "Sanitized state or logs",
        "I removed secrets, tokens, webhooks, chat identifiers",
    ],
    ".github/ISSUE_TEMPLATE/feature_request.yml": [
        "name: Feature request",
        "Public contract impact",
        "Security and privacy implications",
        "Research Mode is OpenClaw-first",
    ],
    ".github/ISSUE_TEMPLATE/security_hardening.yml": [
        "name: Security hardening",
        "Do not use this public form for an exploitable vulnerability",
        "prepare-runtime / package installs",
        "Disclosure safety",
    ],
    "AGENTS.md": [
        "Human-facing project documentation",
        "Keep The Boundary Clear",
        "Do not mix hidden prompts or agent-only instructions into human-facing docs",
        "Research Mode is an OpenClaw skill",
        "scripts/check_research_mode.sh",
    ],
}

BASH_BLOCK_PATTERN = re.compile(r"```(?:bash|sh|shell)\n(.*?)```", re.DOTALL)


def _command_names() -> set[str]:
    parser = build_parser()
    commands: set[str] = set()
    for action in parser._actions:
        if isinstance(action, argparse._SubParsersAction):
            commands.update(action.choices)
    return commands


def _command_options() -> dict[str, set[str]]:
    parser = build_parser()
    options: dict[str, set[str]] = {}
    for action in parser._actions:
        if not isinstance(action, argparse._SubParsersAction):
            continue
        for command, subparser in action.choices.items():
            command_options = {"--help", "-h"}
            for sub_action in subparser._actions:
                command_options.update(sub_action.option_strings)
            options[command] = command_options
    return options


def _relative(path: Path) -> str:
    try:
        return str(path.relative_to(REPO_ROOT))
    except ValueError:
        return str(path)


def _doc_key(path: Path) -> str:
    try:
        return str(path.relative_to(SKILL_DIR))
    except ValueError:
        return _relative(path)


def _read_docs() -> dict[Path, str]:
    docs: dict[Path, str] = {}
    for path in REQUIRED_DOC_PATHS:
        if not path.exists():
            raise AssertionError(f"missing documented file: {_relative(path)}")
        docs[path] = path.read_text(encoding="utf-8")
    for path in OPTIONAL_DOC_PATHS:
        if path.exists():
            docs[path] = path.read_text(encoding="utf-8")
    return docs


def _validate_no_forbidden(docs: dict[Path, str]) -> list[str]:
    errors: list[str] = []
    for path, text in docs.items():
        for pattern, reason in FORBIDDEN_PATTERNS.items():
            match = re.search(pattern, text)
            if match:
                errors.append(
                    f"{_relative(path)}: forbidden pattern {pattern!r}: {reason}"
                )
    return errors


def _validate_required_snippets(docs: dict[Path, str]) -> list[str]:
    errors: list[str] = []
    by_relative = {_doc_key(path): text for path, text in docs.items()}
    optional_rel_paths = {_relative(path) for path in OPTIONAL_DOC_PATHS}
    for rel_path, snippets in REQUIRED_SNIPPETS.items():
        text = by_relative.get(rel_path)
        if text is None:
            if rel_path in optional_rel_paths:
                continue
            errors.append(f"required snippet target missing: {rel_path}")
            continue
        for snippet in snippets:
            if snippet not in text:
                errors.append(f"{rel_path}: missing required snippet: {snippet!r}")
    return errors


def _validate_no_private_markers() -> list[str]:
    errors: list[str] = []
    paths: set[Path] = set()
    for pattern in PUBLIC_PRIVATE_MARKER_GLOBS:
        paths.update(SKILL_DIR.glob(pattern))
    for path in sorted(paths):
        if not path.is_file():
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        for pattern, reason in PUBLIC_PRIVATE_MARKER_PATTERNS.items():
            if re.search(pattern, text):
                errors.append(
                    f"{_relative(path)}: private marker pattern {pattern!r}: {reason}"
                )
    return errors


def _validate_documented_commands(docs: dict[Path, str]) -> list[str]:
    commands = _command_names()
    errors: list[str] = []
    command_pattern = re.compile(r"research_mode\.py\s+([a-z][a-z0-9-]+)")
    for path, text in docs.items():
        for command in command_pattern.findall(text):
            if command not in commands:
                errors.append(
                    f"{_relative(path)}: documented unknown command: {command}"
                )
    return errors


def _logical_shell_lines(block: str) -> list[str]:
    lines: list[str] = []
    current = ""
    for raw_line in block.splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        if current:
            current = f"{current} {line}"
        else:
            current = line
        if current.endswith("\\"):
            current = current[:-1].rstrip()
            continue
        lines.append(current)
        current = ""
    if current:
        lines.append(current)
    return lines


def _research_mode_invocations(line: str) -> list[list[str]]:
    try:
        tokens = shlex.split(line)
    except ValueError:
        return []

    invocations: list[list[str]] = []
    for index, token in enumerate(tokens):
        if Path(token).name != "research_mode.py":
            continue
        invocation: list[str] = []
        for part in tokens[index + 1 :]:
            if part in {"&&", ";", "||", "|"}:
                break
            invocation.append(part)
        if invocation:
            invocations.append(invocation)
    return invocations


def _normalize_option(token: str) -> str | None:
    if token.startswith("[--"):
        token = token[1:]
    if token.endswith("]"):
        token = token[:-1]
    if not token.startswith("-"):
        return None
    return token.split("=", 1)[0]


def _validate_documented_bash_blocks(docs: dict[Path, str]) -> list[str]:
    commands = _command_names()
    command_options = _command_options()
    errors: list[str] = []

    for path, text in docs.items():
        for block in BASH_BLOCK_PATTERN.findall(text):
            for line in _logical_shell_lines(block):
                for invocation in _research_mode_invocations(line):
                    command = invocation[0]
                    if command not in commands:
                        continue
                    valid_options = command_options[command]
                    for token in invocation[1:]:
                        option = _normalize_option(token)
                        if option and option not in valid_options:
                            errors.append(
                                f"{_relative(path)}: documented unknown option "
                                f"for {command}: {option}"
                            )
    return errors


def _json_type_matches(value: object, expected: object) -> bool:
    if isinstance(expected, list):
        return any(_json_type_matches(value, item) for item in expected)
    if expected == "object":
        return isinstance(value, dict)
    if expected == "array":
        return isinstance(value, list)
    if expected == "string":
        return isinstance(value, str)
    if expected == "integer":
        return isinstance(value, int) and not isinstance(value, bool)
    if expected == "number":
        return isinstance(value, int | float) and not isinstance(value, bool)
    if expected == "boolean":
        return isinstance(value, bool)
    if expected == "null":
        return value is None
    return True


def _validate_object_contract(
    schema: dict[str, object], data: object, data_path: Path
) -> list[str]:
    if not isinstance(data, dict):
        return [f"{_relative(data_path)}: expected JSON object"]

    errors: list[str] = []
    required = schema.get("required", [])
    if not isinstance(required, list):
        errors.append(f"{_relative(data_path)}: schema required must be a list")
        required = []
    for field in required:
        if isinstance(field, str) and field not in data:
            errors.append(f"{_relative(data_path)}: missing required field {field!r}")

    properties = schema.get("properties", {})
    if not isinstance(properties, dict):
        return errors

    for field, property_schema in properties.items():
        if field not in data or not isinstance(property_schema, dict):
            continue
        expected_type = property_schema.get("type")
        if expected_type and not _json_type_matches(data[field], expected_type):
            errors.append(
                f"{_relative(data_path)}: field {field!r} does not match "
                f"schema type {expected_type!r}"
            )
    return errors


def _load_schema(path: Path) -> tuple[dict[str, object] | None, list[str]]:
    errors: list[str] = []
    if not path.exists():
        return None, [f"missing schema file: {_relative(path)}"]
    try:
        schema = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        return None, [f"{_relative(path)}: invalid JSON: {exc}"]
    if not isinstance(schema, dict):
        return None, [f"{_relative(path)}: schema root must be an object"]
    for key in ("$schema", "title", "type", "properties"):
        if key not in schema:
            errors.append(f"{_relative(path)}: missing schema metadata {key!r}")
    if schema.get("type") != "object":
        errors.append(f"{_relative(path)}: top-level schema type must be object")
    return schema, errors


def _validate_json_contracts() -> list[str]:
    errors: list[str] = []
    schemas: dict[str, dict[str, object]] = {}
    for path in REQUIRED_SCHEMA_PATHS:
        schema, schema_errors = _load_schema(path)
        errors.extend(schema_errors)
        if schema is not None:
            schemas[path.name] = schema

    state_schema = schemas.get("state.v2.schema.json")
    worker_schema = schemas.get("worker-result.v1.schema.json")
    adequacy_schema = schemas.get("adequacy.v1.schema.json")
    finalization_schema = schemas.get("finalization.v1.schema.json")
    delivery_schema = schemas.get("delivery-intent.v1.schema.json")

    for path in sorted((SKILL_DIR / "examples").glob("*/research-trace/state.json")):
        try:
            state = json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            errors.append(f"{_relative(path)}: invalid JSON: {exc}")
            continue
        if state_schema is not None:
            errors.extend(_validate_object_contract(state_schema, state, path))
        if isinstance(state, dict):
            for intent in state.get("delivery_intents", []) or []:
                if delivery_schema is not None:
                    errors.extend(_validate_object_contract(delivery_schema, intent, path))
            if isinstance(state.get("adequacy"), dict) and adequacy_schema is not None:
                errors.extend(
                    _validate_object_contract(adequacy_schema, state["adequacy"], path)
                )
            if isinstance(state.get("finalization"), dict) and finalization_schema is not None:
                errors.extend(
                    _validate_object_contract(
                        finalization_schema, state["finalization"], path
                    )
                )

    for path in sorted((SKILL_DIR / "examples").glob("*/research-trace/results/*.json")):
        try:
            result = json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            errors.append(f"{_relative(path)}: invalid JSON: {exc}")
            continue
        if worker_schema is not None:
            errors.extend(_validate_object_contract(worker_schema, result, path))
        if isinstance(result, dict):
            if isinstance(result.get("adequacy"), dict) and adequacy_schema is not None:
                errors.extend(
                    _validate_object_contract(adequacy_schema, result["adequacy"], path)
                )
            if (
                isinstance(result.get("finalization"), dict)
                and finalization_schema is not None
            ):
                errors.extend(
                    _validate_object_contract(
                        finalization_schema, result["finalization"], path
                    )
                )
    return errors


def _validate_optional_assets() -> list[str]:
    errors: list[str] = []
    for path in OPTIONAL_ASSET_PATHS:
        if path.exists() and path.stat().st_size == 0:
            errors.append(f"documented asset is empty: {_relative(path)}")
    return errors


def main() -> int:
    docs = _read_docs()
    errors = [
        *_validate_no_forbidden(docs),
        *_validate_required_snippets(docs),
        *_validate_no_private_markers(),
        *_validate_documented_commands(docs),
        *_validate_documented_bash_blocks(docs),
        *_validate_json_contracts(),
        *_validate_optional_assets(),
    ]
    if errors:
        for error in errors:
            print(error, file=sys.stderr)
        return 1
    print("research-mode docs smoke check passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
