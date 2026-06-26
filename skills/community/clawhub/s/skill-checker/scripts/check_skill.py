from __future__ import annotations

import argparse
import html
import re
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


TOP_LEVEL_FIELDS = {
    "name",
    "description",
    "description_en",
    "description_zh",
    "license",
    "compatibility",
    "metadata",
    "allowed-tools",
}
NAME_PATTERN = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
USE_MARKERS = (
    "use when",
    "when ",
    "用于",
    "适用于",
    "当",
    "needs to",
    "for tasks",
    "for ",
)
GUIDANCE_MARKERS = (
    "step",
    "steps",
    "workflow",
    "output",
    "example",
    "examples",
    "run ",
    "must",
    "should",
    "步骤",
    "流程",
    "输出",
    "示例",
    "运行",
    "必须",
    "应该",
    "检查",
)


@dataclass
class Finding:
    rule_id: str
    severity: str
    message: str
    evidence: str
    suggestion: str


@dataclass
class AuditResult:
    target_path: Path
    skill_path: Path | None
    report_path: Path | None
    resolved_from: str
    status: str
    severe_count: int
    warning_count: int
    findings: list[Finding]
    checked_at: str


class ParseError(ValueError):
    pass


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Check whether a SKILL.md file follows Agent Skills specification."
    )
    parser.add_argument("target", help="Path to a SKILL.md file or a skill directory")
    parser.add_argument(
        "--out",
        help="Path to the HTML report file. Defaults to a timestamped file in the current directory.",
    )
    parser.add_argument(
        "--fail-on-audit",
        action="store_true",
        help="Return exit code 1 when the audit result is fail (severe findings >= 2).",
    )
    return parser.parse_args()


def resolve_target(target: str) -> tuple[Path, Path, str]:
    raw_path = Path(target).expanduser()
    path = raw_path.resolve(strict=False)
    if not path.exists():
        raise FileNotFoundError(f"找不到目标路径: {path}")
    if path.is_dir():
        skill_path = path / "SKILL.md"
        if not skill_path.exists():
            raise FileNotFoundError(f"目标目录中不存在 SKILL.md: {path}")
        return skill_path, path, "directory"
    if path.name != "SKILL.md":
        raise FileNotFoundError(f"目标文件不是 SKILL.md: {path}")
    return path, path.parent, "file"


def extract_frontmatter(text: str) -> tuple[str, str]:
    normalized = text.replace("\r\n", "\n")
    if not normalized.startswith("---\n"):
        raise ParseError("文件缺少 YAML frontmatter 起始分隔符 `---`。")
    closing_index = normalized.find("\n---\n", 4)
    if closing_index == -1:
        raise ParseError("文件缺少 YAML frontmatter 结束分隔符 `---`。")
    frontmatter = normalized[4:closing_index]
    body = normalized[closing_index + 5 :]
    return frontmatter, body


def parse_scalar(raw_value: str) -> str:
    value = raw_value.strip()
    if not value:
        return ""
    if (value.startswith('"') and value.endswith('"')) or (
        value.startswith("'") and value.endswith("'")
    ):
        return value[1:-1]
    return value


def parse_frontmatter(frontmatter: str) -> dict[str, Any]:
    data: dict[str, Any] = {}
    lines = frontmatter.splitlines()
    index = 0
    while index < len(lines):
        line = lines[index]
        if not line.strip() or line.lstrip().startswith("#"):
            index += 1
            continue
        if line.startswith((" ", "\t")):
            raise ParseError(f"顶层字段缩进非法: `{line}`")
        match = re.match(r"^([A-Za-z0-9_-]+):(.*)$", line)
        if not match:
            raise ParseError(f"frontmatter 行格式非法: `{line}`")
        key = match.group(1)
        if key in data:
            raise ParseError(f"frontmatter 中存在重复字段: `{key}`")
        remainder = match.group(2).strip()
        if remainder:
            data[key] = parse_scalar(remainder)
            index += 1
            continue
        index += 1
        block: list[str] = []
        while index < len(lines):
            next_line = lines[index]
            if not next_line.strip():
                index += 1
                continue
            if next_line.startswith((" ", "\t")):
                block.append(next_line)
                index += 1
                continue
            break
        if key != "metadata":
            raise ParseError(f"字段 `{key}` 不支持嵌套结构。")
        nested: dict[str, str] = {}
        if not block:
            data[key] = nested
            continue
        for entry in block:
            nested_match = re.match(r"^\s{2,}([A-Za-z0-9_-]+):(.*)$", entry)
            if not nested_match:
                raise ParseError(f"metadata 子字段格式非法: `{entry}`")
            nested_key = nested_match.group(1)
            nested_value = nested_match.group(2)
            if not nested_value.strip():
                raise ParseError(f"metadata 子字段 `{nested_key}` 不能为空。")
            nested[nested_key] = parse_scalar(nested_value)
        data[key] = nested
    return data


def add_finding(
    findings: list[Finding],
    rule_id: str,
    severity: str,
    message: str,
    evidence: str,
    suggestion: str,
) -> None:
    findings.append(
        Finding(
            rule_id=rule_id,
            severity=severity,
            message=message,
            evidence=evidence,
            suggestion=suggestion,
        )
    )


def validate_frontmatter(
    data: dict[str, Any],
    body: str,
    skill_file: Path,
    skill_dir: Path,
) -> list[Finding]:
    findings: list[Finding] = []

    for key in data:
        if key not in TOP_LEVEL_FIELDS:
            add_finding(
                findings,
                "spec.unknown-field",
                "severe",
                f"frontmatter 包含 specification 未定义的字段 `{key}`。",
                key,
                "删除该字段，或改用 specification 支持的顶层字段。",
            )

    name = data.get("name")
    if not isinstance(name, str) or not name.strip():
        add_finding(
            findings,
            "spec.required-name",
            "severe",
            "frontmatter 缺少必填字段 `name`，或其值为空。",
            str(name),
            "补充合法的 skill 名称，并确保只使用小写字母、数字和连字符。",
        )
    else:
        if not NAME_PATTERN.match(name):
            add_finding(
                findings,
                "spec.name-format",
                "severe",
                "`name` 不符合规范命名格式。",
                name,
                "将 `name` 改为小写字母、数字和连字符组成的名称，例如 `skill-checker`。",
            )
        if skill_dir.name and name != skill_dir.name:
            add_finding(
                findings,
                "spec.name-directory-match",
                "severe",
                "`name` 与技能目录名不一致。",
                f"name={name}, directory={skill_dir.name}",
                "保持目录名与 `name` 完全一致，避免触发和引用混乱。",
            )

    description = data.get("description")
    if not isinstance(description, str) or not description.strip():
        add_finding(
            findings,
            "spec.required-description",
            "severe",
            "frontmatter 缺少必填字段 `description`，或其值为空。",
            str(description),
            "补充描述，明确说明 skill 做什么以及何时使用它。",
        )
        description_text = ""
    else:
        description_text = description.strip()
        if len(description_text) > 1024:
            add_finding(
                findings,
                "spec.description-length",
                "severe",
                "`description` 超过 1024 个字符。",
                f"length={len(description_text)}",
                "压缩描述，只保留能力概述和触发场景。",
            )
        if len(description_text) < 24:
            add_finding(
                findings,
                "semantics.description-too-short",
                "severe",
                "`description` 过短，难以表达 skill 能力和触发场景。",
                description_text,
                "扩展描述，至少同时说明它解决什么问题，以及何时应触发该 skill。",
            )
        lowered = description_text.lower()
        if not any(marker in lowered for marker in USE_MARKERS):
            add_finding(
                findings,
                "semantics.description-trigger-context",
                "severe",
                "`description` 没有清晰说明何时使用这个 skill。",
                description_text,
                "在描述中加入触发语句，例如 `Use when ...` 或中文的 `当需要...时使用`。",
            )

    for recommended_field in ("description_en", "description_zh"):
        recommended_value = data.get(recommended_field)
        if recommended_value is None or (
            isinstance(recommended_value, str) and not recommended_value.strip()
        ):
            add_finding(
                findings,
                f"semantics.recommended-{recommended_field}",
                "warning",
                f"推荐字段 `{recommended_field}` 缺失或为空。",
                str(recommended_value),
                f"补充 `{recommended_field}`，用于提供双语描述，提升跨语言可读性。",
            )
        elif not isinstance(recommended_value, str):
            add_finding(
                findings,
                f"spec.{recommended_field}-type",
                "severe",
                f"`{recommended_field}` 必须是字符串。",
                repr(recommended_value),
                f"将 `{recommended_field}` 改为单行字符串。",
            )

    license_value = data.get("license")
    if not isinstance(license_value, str) or not license_value.strip():
        add_finding(
            findings,
            "spec.required-license",
            "severe",
            "frontmatter 缺少必填字段 `license`，或其值为空。",
            str(license_value),
            "补充 `license`，并使用单行字符串，例如 `MIT` 或 `Apache-2.0`。",
        )

    for optional_field in ("compatibility", "allowed-tools"):
        if optional_field in data and not isinstance(data[optional_field], str):
            add_finding(
                findings,
                f"spec.{optional_field}-type",
                "severe",
                f"`{optional_field}` 必须是字符串。",
                repr(data[optional_field]),
                f"将 `{optional_field}` 改为单行字符串。",
            )
    if "license" in data and not isinstance(data["license"], str):
        add_finding(
            findings,
            "spec.license-type",
            "severe",
            "`license` 必须是字符串。",
            repr(data["license"]),
            "将 `license` 改为单行字符串。",
        )

    metadata = data.get("metadata")
    if metadata is None:
        add_finding(
            findings,
            "spec.required-metadata",
            "severe",
            "frontmatter 缺少必填字段 `metadata`。",
            str(metadata),
            "补充 `metadata` 映射，并至少包含 `author` 与 `version` 字段。",
        )
    elif not isinstance(metadata, dict):
        add_finding(
            findings,
            "spec.metadata-type",
            "severe",
            "`metadata` 必须是键值对映射。",
            repr(metadata),
            "将 `metadata` 改为简单映射，且所有键和值都使用字符串。",
        )
    else:
        for metadata_key, metadata_value in metadata.items():
            if not isinstance(metadata_key, str) or not isinstance(metadata_value, str):
                add_finding(
                    findings,
                    "spec.metadata-values",
                    "severe",
                    "`metadata` 中的键和值都必须是字符串。",
                    f"{metadata_key}={metadata_value}",
                    "仅保留字符串类型的 metadata 键值对。",
                )
        author = metadata.get("author")
        if not isinstance(author, str) or not author.strip():
            add_finding(
                findings,
                "spec.required-metadata-author",
                "severe",
                "`metadata.author` 为必填字段，且必须是非空字符串。",
                str(author),
                "补充 `metadata.author`，例如组织名或维护者标识。",
            )
        version = metadata.get("version")
        if not isinstance(version, str) or not version.strip():
            add_finding(
                findings,
                "spec.required-metadata-version",
                "severe",
                "`metadata.version` 为必填字段，且必须是非空字符串。",
                str(version),
                "补充 `metadata.version`，建议使用语义化版本号字符串，如 `1.0.0`。",
            )

    body_text = body.strip()
    body_lines = [line.strip() for line in body.splitlines() if line.strip()]
    if not body_text:
        add_finding(
            findings,
            "semantics.empty-body",
            "severe",
            "SKILL.md 正文为空，无法指导另一个 agent 执行任务。",
            str(skill_file),
            "补充工作流、关键约束和输出要求等执行指引。",
        )
    elif len(body_text) < 120 or len(body_lines) < 4:
        add_finding(
            findings,
            "semantics.body-too-thin",
            "severe",
            "SKILL.md 正文过薄，难以形成可执行的技能说明。",
            f"chars={len(body_text)}, lines={len(body_lines)}",
            "增加阶段化流程、关键原则、产出要求或示例，让 skill 能真正指导执行。",
        )
    else:
        lowered_body = body_text.lower()
        guidance_hits = sum(1 for marker in GUIDANCE_MARKERS if marker in lowered_body)
        heading_hits = sum(1 for line in body_lines if line.startswith("#"))
        if guidance_hits < 2:
            add_finding(
                findings,
                "semantics.body-guidance-thin",
                "warning",
                "正文存在，但执行指导信号偏弱。",
                f"guidance_hits={guidance_hits}",
                "增加步骤、输出预期、命令示例或约束说明，让使用者更容易照着执行。",
            )
        if heading_hits == 0:
            add_finding(
                findings,
                "semantics.body-structure",
                "warning",
                "正文缺少明显结构，阅读和查找重点会比较吃力。",
                "未发现 Markdown 标题",
                "使用标题或短小分段组织内容，让工作流和规则更容易扫描。",
            )
    return findings


def audit_target(target: str) -> AuditResult:
    checked_at = datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds")
    try:
        skill_file, skill_dir, resolved_from = resolve_target(target)
    except FileNotFoundError as exc:
        findings = [
            Finding(
                rule_id="input.target-not-found",
                severity="severe",
                message="目标路径不可用，无法开始检查。",
                evidence=str(exc),
                suggestion="传入存在的 SKILL.md 绝对路径，或包含 SKILL.md 的技能目录路径。",
            ),
            Finding(
                rule_id="input.audit-blocked",
                severity="severe",
                message="由于输入目标不可解析，本次检查直接判定为不通过。",
                evidence=target,
                suggestion="修正目标路径后重新运行检查。",
            ),
        ]
        return finalize_result(
            target_path=Path(target),
            skill_path=None,
            resolved_from="invalid",
            findings=findings,
            checked_at=checked_at,
        )

    try:
        raw_text = skill_file.read_text(encoding="utf-8")
    except OSError as exc:
        findings = [
            Finding(
                rule_id="input.read-failed",
                severity="severe",
                message="无法读取目标 SKILL.md。",
                evidence=str(exc),
                suggestion="确认文件存在、编码为 UTF-8，且当前环境具有读取权限。",
            ),
            Finding(
                rule_id="input.audit-blocked",
                severity="severe",
                message="由于文件不可读，本次检查直接判定为不通过。",
                evidence=str(skill_file),
                suggestion="修复读取问题后重新运行检查。",
            ),
        ]
        return finalize_result(
            target_path=Path(target),
            skill_path=skill_file,
            resolved_from=resolved_from,
            findings=findings,
            checked_at=checked_at,
        )

    findings: list[Finding] = []
    try:
        frontmatter, body = extract_frontmatter(raw_text)
    except ParseError as exc:
        add_finding(
            findings,
            "spec.frontmatter-missing",
            "severe",
            "SKILL.md 缺少合法的 YAML frontmatter。",
            str(exc),
            "在文件顶部加入 `---` 包裹的 frontmatter，并至少提供 `name` 与 `description`。",
        )
        add_finding(
            findings,
            "input.audit-blocked",
            "severe",
            "无法继续执行字段级检查，本次检查直接判定为不通过。",
            str(skill_file),
            "修复 frontmatter 结构后重新运行检查。",
        )
        return finalize_result(
            target_path=Path(target),
            skill_path=skill_file,
            resolved_from=resolved_from,
            findings=findings,
            checked_at=checked_at,
        )

    try:
        data = parse_frontmatter(frontmatter)
    except ParseError as exc:
        add_finding(
            findings,
            "spec.frontmatter-invalid",
            "severe",
            "frontmatter 存在 YAML 结构问题，无法可靠解析。",
            str(exc),
            "检查缩进、重复字段、嵌套格式和字段写法，确保 frontmatter 是简单合法的 YAML。",
        )
        add_finding(
            findings,
            "input.audit-blocked",
            "severe",
            "无法继续执行字段级检查，本次检查直接判定为不通过。",
            frontmatter,
            "修复 frontmatter 结构后重新运行检查。",
        )
        return finalize_result(
            target_path=Path(target),
            skill_path=skill_file,
            resolved_from=resolved_from,
            findings=findings,
            checked_at=checked_at,
        )

    findings.extend(validate_frontmatter(data, body, skill_file, skill_dir))
    return finalize_result(
        target_path=Path(target),
        skill_path=skill_file,
        resolved_from=resolved_from,
        findings=findings,
        checked_at=checked_at,
    )


def finalize_result(
    target_path: Path,
    skill_path: Path | None,
    resolved_from: str,
    findings: list[Finding],
    checked_at: str,
) -> AuditResult:
    severe_count = sum(1 for finding in findings if finding.severity == "severe")
    warning_count = sum(1 for finding in findings if finding.severity != "severe")
    status = "不通过" if severe_count >= 2 else "通过"
    return AuditResult(
        target_path=target_path,
        skill_path=skill_path,
        report_path=None,
        resolved_from=resolved_from,
        status=status,
        severe_count=severe_count,
        warning_count=warning_count,
        findings=findings,
        checked_at=checked_at,
    )


RULE_TRANSLATIONS: dict[str, tuple[str, str]] = {
    "input.target-not-found": (
        "Target path is unavailable, so the audit cannot start.",
        "Provide an existing SKILL.md absolute path or a skill directory path that contains SKILL.md.",
    ),
    "input.audit-blocked": (
        "The audit is blocked and marked as fail due to an input or parsing issue.",
        "Fix the blocking issue and run the check again.",
    ),
    "input.read-failed": (
        "Failed to read the target SKILL.md.",
        "Ensure the file exists, uses UTF-8 encoding, and is readable in the current environment.",
    ),
    "spec.frontmatter-missing": (
        "SKILL.md is missing a valid YAML frontmatter block.",
        "Add a frontmatter block wrapped by `---` and include at least `name` and `description`.",
    ),
    "spec.frontmatter-invalid": (
        "The frontmatter has structural YAML errors and cannot be parsed reliably.",
        "Fix indentation, duplicate keys, nested formats, and field syntax.",
    ),
    "spec.unknown-field": (
        "Frontmatter contains a field not defined by the specification.",
        "Remove the field or replace it with a supported top-level field.",
    ),
    "spec.required-name": (
        "Frontmatter is missing required field `name`, or it is empty.",
        "Add a valid skill name using lowercase letters, digits, and hyphens.",
    ),
    "spec.name-format": (
        "`name` does not match the required naming pattern.",
        "Use lowercase letters, digits, and hyphens, for example `skill-checker`.",
    ),
    "spec.name-directory-match": (
        "`name` does not match the skill directory name.",
        "Keep the directory name exactly aligned with `name`.",
    ),
    "spec.required-description": (
        "Frontmatter is missing required field `description`, or it is empty.",
        "Add a description that explains what the skill does and when to use it.",
    ),
    "spec.description_en-type": (
        "`description_en` must be a string.",
        "Change `description_en` to a single-line string value.",
    ),
    "spec.description_zh-type": (
        "`description_zh` must be a string.",
        "Change `description_zh` to a single-line string value.",
    ),
    "spec.required-license": (
        "Frontmatter is missing required field `license`, or it is empty.",
        "Add a single-line `license` string such as `MIT` or `Apache-2.0`.",
    ),
    "spec.description-length": (
        "`description` exceeds 1024 characters.",
        "Shorten it to capability summary and trigger context only.",
    ),
    "spec.license-type": (
        "`license` must be a string.",
        "Change `license` to a single-line string value.",
    ),
    "spec.compatibility-type": (
        "`compatibility` must be a string.",
        "Change `compatibility` to a single-line string value.",
    ),
    "spec.allowed-tools-type": (
        "`allowed-tools` must be a string.",
        "Change `allowed-tools` to a single-line string value.",
    ),
    "spec.metadata-type": (
        "`metadata` must be a key-value mapping.",
        "Change `metadata` to a simple mapping with string keys and values.",
    ),
    "spec.metadata-values": (
        "All `metadata` keys and values must be strings.",
        "Keep only string key-value pairs in `metadata`.",
    ),
    "spec.required-metadata": (
        "Frontmatter is missing required field `metadata`.",
        "Add a `metadata` mapping and include at least `author` and `version`.",
    ),
    "spec.required-metadata-author": (
        "`metadata.author` is required and must be a non-empty string.",
        "Add `metadata.author` with the maintainer or organization identifier.",
    ),
    "spec.required-metadata-version": (
        "`metadata.version` is required and must be a non-empty string.",
        "Add `metadata.version` as a version string, for example `1.0.0`.",
    ),
    "semantics.description-too-short": (
        "`description` is too short to express capability and trigger context.",
        "Expand it to explain what problem the skill solves and when to trigger it.",
    ),
    "semantics.description-trigger-context": (
        "`description` does not clearly state when this skill should be used.",
        "Add trigger wording such as `Use when ...`.",
    ),
    "semantics.recommended-description_en": (
        "Recommended field `description_en` is missing or empty.",
        "Add `description_en` to provide an English description for bilingual readability.",
    ),
    "semantics.recommended-description_zh": (
        "Recommended field `description_zh` is missing or empty.",
        "Add `description_zh` to provide a Chinese description for bilingual readability.",
    ),
    "semantics.empty-body": (
        "SKILL.md body is empty and cannot guide another agent.",
        "Add workflow, constraints, and expected output guidance.",
    ),
    "semantics.body-too-thin": (
        "SKILL.md body is too thin to be practically executable.",
        "Add phased workflow, key principles, and concrete output expectations.",
    ),
    "semantics.body-guidance-thin": (
        "The body exists, but execution guidance is weak.",
        "Add step-by-step instructions, expected outputs, examples, or constraints.",
    ),
    "semantics.body-structure": (
        "The body has weak structure and is hard to scan.",
        "Use headings and short sections to organize workflow and rules.",
    ),
}


def map_status_text(result: AuditResult) -> tuple[str, str]:
    is_fail = result.severe_count >= 2
    return ("Fail", "不通过") if is_fail else ("Pass", "通过")


def map_resolved_from_text(value: str) -> tuple[str, str]:
    mapping = {
        "file": ("File", "文件"),
        "directory": ("Directory", "目录"),
        "invalid": ("Invalid", "无效"),
    }
    return mapping.get(value, (value, value))


def get_finding_localized_text(finding: Finding) -> tuple[str, str]:
    fallback_en_message = finding.message
    fallback_en_suggestion = finding.suggestion
    if finding.rule_id in RULE_TRANSLATIONS:
        return RULE_TRANSLATIONS[finding.rule_id]
    return fallback_en_message, fallback_en_suggestion


def build_html_report(result: AuditResult) -> str:
    title_en = "Skill Checker Report"
    title_zh = "Skill Checker 报告"
    status_en, status_zh = map_status_text(result)
    resolved_en, resolved_zh = map_resolved_from_text(result.resolved_from)

    summary_items = [
        ("Target Path", "目标路径", str(result.target_path), str(result.target_path)),
        ("Resolved From", "解析来源", resolved_en, resolved_zh),
        (
            "Checked File",
            "检查文件",
            str(result.skill_path) if result.skill_path else "Unresolved",
            str(result.skill_path) if result.skill_path else "未解析",
        ),
        ("Checked At", "检查时间", result.checked_at, result.checked_at),
        ("Final Result", "最终结论", status_en, status_zh),
        ("Severe Findings", "严重问题", str(result.severe_count), str(result.severe_count)),
        ("Warnings", "一般问题", str(result.warning_count), str(result.warning_count)),
    ]
    summary_html = "".join(
        "<li>"
        f"<strong><span class='lang lang-en'>{html.escape(label_en)}:</span>"
        f"<span class='lang lang-zh'>{html.escape(label_zh)}:</span></strong> "
        f"<span class='lang lang-en'>{html.escape(value_en)}</span>"
        f"<span class='lang lang-zh'>{html.escape(value_zh)}</span>"
        "</li>"
        for label_en, label_zh, value_en, value_zh in summary_items
    )

    findings_html = ""
    if result.findings:
        cards: list[str] = []
        for finding in result.findings:
            message_en, suggestion_en = get_finding_localized_text(finding)
            severity_en = "severe" if finding.severity == "severe" else "warning"
            severity_zh = "严重" if finding.severity == "severe" else "一般"
            cards.append(
                "<article class='finding'>"
                "<div class='finding-head'>"
                f"<span class='badge {html.escape(finding.severity)}'>"
                f"<span class='lang lang-en'>{html.escape(severity_en)}</span>"
                f"<span class='lang lang-zh'>{html.escape(severity_zh)}</span>"
                "</span>"
                f"<code>{html.escape(finding.rule_id)}</code>"
                "</div>"
                "<h3>"
                f"<span class='lang lang-en'>{html.escape(message_en)}</span>"
                f"<span class='lang lang-zh'>{html.escape(finding.message)}</span>"
                "</h3>"
                "<p>"
                "<strong><span class='lang lang-en'>Evidence:</span><span class='lang lang-zh'>证据:</span></strong> "
                f"{html.escape(finding.evidence)}"
                "</p>"
                "<p>"
                "<strong><span class='lang lang-en'>Suggestion:</span><span class='lang lang-zh'>建议:</span></strong> "
                f"<span class='lang lang-en'>{html.escape(suggestion_en)}</span>"
                f"<span class='lang lang-zh'>{html.escape(finding.suggestion)}</span>"
                "</p>"
                "</article>"
            )
        findings_html = "".join(cards)
    else:
        findings_html = (
            "<p class='empty'><span class='lang lang-en'>No findings.</span>"
            "<span class='lang lang-zh'>未发现问题。</span></p>"
        )

    return f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{html.escape(title_en)}</title>
  <style>
    :root {{
      color-scheme: light;
      --bg: #f5efe4;
      --panel: #fffdf8;
      --ink: #1f1a14;
      --muted: #6e6458;
      --border: #d6c9b7;
      --accent: #1f6f78;
      --accent-soft: #d7ece8;
      --success: #217346;
      --success-soft: #dcf4e4;
      --danger: #a13232;
      --danger-soft: #f8dddd;
      --pill-neutral-bg: #efe6d8;
      --pill-neutral-text: #5f5347;
      --warn: #8c5f12;
      --warn-soft: #fdecc8;
      --shadow: 0 18px 40px rgba(31, 26, 20, 0.08);
    }}
    * {{ box-sizing: border-box; }}
    body {{
      margin: 0;
      font-family: "Segoe UI", "PingFang SC", "Microsoft YaHei", sans-serif;
      background:
        radial-gradient(circle at top left, rgba(31, 111, 120, 0.18), transparent 28%),
        linear-gradient(180deg, #fcf8ef 0%, var(--bg) 100%);
      color: var(--ink);
    }}
    .shell {{
      max-width: 1080px;
      margin: 0 auto;
      padding: 40px 20px 72px;
    }}
    .hero, .panel {{
      background: var(--panel);
      border: 1px solid var(--border);
      border-radius: 24px;
      box-shadow: var(--shadow);
    }}
    .hero {{
      padding: 28px;
      margin-bottom: 24px;
      position: relative;
    }}
    .lang-switch {{
      position: absolute;
      top: 18px;
      right: 18px;
      display: inline-flex;
      border: 1px solid var(--border);
      border-radius: 999px;
      background: #fff8ec;
      overflow: hidden;
    }}
    .lang-switch button {{
      border: 0;
      background: transparent;
      padding: 6px 12px;
      font-size: 12px;
      font-weight: 700;
      cursor: pointer;
      color: var(--muted);
    }}
    .lang-switch button.active {{
      background: var(--accent);
      color: #ffffff;
    }}
    .lang {{
      display: none;
    }}
    html[data-lang="en"] .lang-en {{
      display: inline;
    }}
    html[data-lang="zh"] .lang-zh {{
      display: inline;
    }}
    h1 {{
      margin: 0 0 8px;
      font-size: 32px;
      line-height: 1.15;
    }}
    .hero p {{
      margin: 0;
      color: var(--muted);
      font-size: 16px;
    }}
    .status-row {{
      display: flex;
      gap: 12px;
      flex-wrap: wrap;
      margin-top: 18px;
    }}
    .status-pill {{
      display: inline-flex;
      align-items: center;
      gap: 8px;
      border-radius: 999px;
      padding: 10px 14px;
      font-weight: 700;
      background: var(--pill-neutral-bg);
      color: var(--pill-neutral-text);
    }}
    .status-pill.pass {{
      background: var(--success-soft);
      color: var(--success);
    }}
    .status-pill.fail {{
      background: var(--danger-soft);
      color: var(--danger);
    }}
    .grid {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
      gap: 24px;
    }}
    .panel {{
      padding: 24px;
    }}
    .panel h2 {{
      margin: 0 0 16px;
      font-size: 20px;
    }}
    ul {{
      margin: 0;
      padding-left: 18px;
    }}
    li + li {{
      margin-top: 10px;
    }}
    .finding {{
      border: 1px solid var(--border);
      border-radius: 18px;
      padding: 18px;
      background: #fffaf1;
    }}
    .finding + .finding {{
      margin-top: 16px;
    }}
    .finding-head {{
      display: flex;
      align-items: center;
      gap: 10px;
      margin-bottom: 10px;
      flex-wrap: wrap;
    }}
    .badge {{
      display: inline-block;
      border-radius: 999px;
      padding: 4px 10px;
      font-size: 12px;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: 0.04em;
    }}
    .badge.severe {{
      background: var(--danger-soft);
      color: var(--danger);
    }}
    .badge.warning {{
      background: var(--warn-soft);
      color: var(--warn);
    }}
    code {{
      background: #f3ebe0;
      padding: 2px 6px;
      border-radius: 6px;
      font-family: "Cascadia Code", "Consolas", monospace;
    }}
    .empty {{
      color: var(--muted);
      margin: 0;
    }}
  </style>
</head>
<body>
  <main class="shell">
    <section class="hero">
      <div class="lang-switch" aria-label="Language switch">
        <button id="btn-en" class="active" type="button">EN</button>
        <button id="btn-zh" type="button">中文</button>
      </div>
      <h1><span class="lang lang-en">{html.escape(title_en)}</span><span class="lang lang-zh">{html.escape(title_zh)}</span></h1>
      <p>
        <span class="lang lang-en">Static specification and semantic checks for a target `SKILL.md` based on Agent Skills specification.</span>
        <span class="lang lang-zh">根据 Agent Skills specification 对目标 `SKILL.md` 进行静态规范与语义质量检查。</span>
      </p>
      <div class="status-row">
        <div class="status-pill {'fail' if result.severe_count >= 2 else 'pass'}">
          <span class="lang lang-en">{html.escape(status_en)}</span>
          <span class="lang lang-zh">{html.escape(status_zh)}</span>
        </div>
        <div class="status-pill">
          <span class="lang lang-en">Severe {result.severe_count}</span>
          <span class="lang lang-zh">严重问题 {result.severe_count}</span>
        </div>
        <div class="status-pill">
          <span class="lang lang-en">Warnings {result.warning_count}</span>
          <span class="lang lang-zh">一般问题 {result.warning_count}</span>
        </div>
      </div>
    </section>
    <section class="grid">
      <section class="panel">
        <h2><span class="lang lang-en">Summary</span><span class="lang lang-zh">摘要</span></h2>
        <ul>{summary_html}</ul>
      </section>
      <section class="panel">
        <h2><span class="lang lang-en">Fix Priority</span><span class="lang lang-zh">修复优先级</span></h2>
        <ul>
          <li><span class="lang lang-en">Fix all severe findings before warnings.</span><span class="lang lang-zh">先处理所有严重问题，再处理一般问题。</span></li>
          <li><span class="lang lang-en">The audit fails when severe findings reach 2 or more.</span><span class="lang lang-zh">若严重问题达到 2 个及以上，本次检查结论为不通过。</span></li>
          <li><span class="lang lang-en">Prioritize `name`, `description`, frontmatter structure, and executable body guidance.</span><span class="lang lang-zh">重点关注 `name`、`description`、frontmatter 结构和正文可执行性。</span></li>
        </ul>
      </section>
    </section>
    <section class="panel" style="margin-top: 24px;">
      <h2><span class="lang lang-en">Findings</span><span class="lang lang-zh">发现的问题</span></h2>
      {findings_html}
    </section>
  </main>
  <script>
    function setLang(lang) {{
      document.documentElement.setAttribute("data-lang", lang);
      const en = document.getElementById("btn-en");
      const zh = document.getElementById("btn-zh");
      en.classList.toggle("active", lang === "en");
      zh.classList.toggle("active", lang === "zh");
    }}
    document.getElementById("btn-en").addEventListener("click", function () {{ setLang("en"); }});
    document.getElementById("btn-zh").addEventListener("click", function () {{ setLang("zh"); }});
    setLang("en");
  </script>
</body>
</html>
"""


def write_report(result: AuditResult, output_path: str | None) -> Path:
    if output_path:
        report_path = Path(output_path).expanduser().resolve(strict=False)
    else:
        timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        report_path = Path.cwd() / f"skill-check-report-{timestamp}.html"
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(build_html_report(result), encoding="utf-8")
    result.report_path = report_path
    return report_path


def main() -> int:
    args = parse_args()
    result = audit_target(args.target)
    report_path = write_report(result, args.out)
    print(f"结论: {result.status}")
    print(f"严重问题: {result.severe_count}")
    print(f"一般问题: {result.warning_count}")
    print(f"HTML 报告: {report_path}")
    if args.fail_on_audit and result.status == "不通过":
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
