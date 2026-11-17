"""数据管理展示元数据校验（模板开发自检，不依赖宿主）。"""

from __future__ import annotations

import os
import re
import sqlite3
from dataclasses import dataclass, field

from db.display_metadata import (
    DATETIME_UNIX_SECONDS,
    METADATA_TABLES,
    STANDARD_TIMESTAMP_COLUMNS,
    TASK_LOGS_COLUMN_METADATA,
    TASK_LOGS_TABLE,
    iter_user_tables,
    list_physical_column_names,
)
from db.timestamp_columns import has_updated_at_trigger
from util.constants import SKILL_SLUG
from util.slug_naming import LEGACY_EXEMPT_SLUGS, validate_slug_semantics

_TEMPLATE_PLACEHOLDER_SLUGS = frozenset({"your-skill-slug", "your_skill_slug"})
_ENGLISH_PLACEHOLDER_NAME_PATTERNS = (
    re.compile(r"^my\s+skill$", re.I),
    re.compile(r"^your[-_\s]?skill", re.I),
    re.compile(r"^skill[-_\s]?template$", re.I),
    re.compile(r"^[a-z0-9_-]+$"),
)
_KEBAB_SLUG = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
_CJK_RE = re.compile(r"[\u4e00-\u9fff]")


@dataclass
class ValidationReport:
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)

    @property
    def ok(self) -> bool:
        return not self.errors


def _has_cjk(text: str) -> bool:
    return bool(_CJK_RE.search(text))


def _looks_like_raw_physical_name(display_name: str, physical_name: str) -> bool:
    if not display_name.strip():
        return True
    if display_name.strip().lower() == physical_name.strip().lower():
        return True
    compact = display_name.replace(" ", "").replace("_", "").lower()
    if compact == physical_name.replace("_", "").lower():
        return True
    return False


def _parse_frontmatter_field(text: str, field_name: str) -> str:
    parts = text.split("---", 2)
    if len(parts) < 2:
        return ""
    for line in parts[1].splitlines():
        match = re.match(rf"^{re.escape(field_name)}:\s*(.+)\s*$", line.strip())
        if match:
            return match.group(1).strip().strip("\"'")
    return ""


def _parse_openclaw_slug(text: str) -> str:
    parts = text.split("---", 2)
    if len(parts) < 2:
        return ""
    lines = parts[1].splitlines()
    for index, line in enumerate(lines):
        if re.match(r"^\s+openclaw:\s*$", line):
            for inner in lines[index + 1 :]:
                if inner.strip() and inner[0] not in (" ", "\t"):
                    break
                match = re.match(r"^(\s+)slug:\s*(.+)\s*$", inner)
                if match:
                    return match.group(2).strip().strip("\"'")
    return ""


def parse_skill_frontmatter(skill_root: str) -> dict[str, str]:
    path = os.path.join(skill_root, "SKILL.md")
    with open(path, encoding="utf-8") as f:
        text = f.read()
    return {
        "name": _parse_frontmatter_field(text, "name"),
        "slug": _parse_openclaw_slug(text),
    }


def validate_skill_frontmatter(skill_root: str, *, allow_template_placeholders: bool = True) -> ValidationReport:
    report = ValidationReport()
    data = parse_skill_frontmatter(skill_root)
    name = str(data.get("name") or "").strip()
    slug = str(data.get("slug") or "").strip()

    if not name:
        report.errors.append("SKILL.md frontmatter.name 缺失")
    elif not _has_cjk(name):
        if allow_template_placeholders and slug in _TEMPLATE_PLACEHOLDER_SLUGS:
            report.warnings.append("SKILL.md frontmatter.name 建议使用清晰的中文业务名称（模板占位可暂保留）")
        else:
            report.errors.append("SKILL.md frontmatter.name 应使用用户可见的中文业务名称")
    else:
        for pattern in _ENGLISH_PLACEHOLDER_NAME_PATTERNS:
            if pattern.fullmatch(name):
                if allow_template_placeholders and slug in _TEMPLATE_PLACEHOLDER_SLUGS:
                    report.warnings.append(f"SKILL.md frontmatter.name 仍为占位风格：{name!r}")
                else:
                    report.errors.append(f"SKILL.md frontmatter.name 不应为英文占位名：{name!r}")
                break

    if not slug:
        report.errors.append("SKILL.md metadata.openclaw.slug 缺失")
    elif not _KEBAB_SLUG.fullmatch(slug):
        report.errors.append(f"metadata.openclaw.slug 必须为 kebab-case：{slug!r}")
    elif slug in _TEMPLATE_PLACEHOLDER_SLUGS and not allow_template_placeholders:
        report.errors.append(f"metadata.openclaw.slug 仍为模板占位：{slug!r}")

    constants_slug = SKILL_SLUG.strip()
    if slug and constants_slug and slug != constants_slug:
        report.warnings.append(
            f"SKILL.md slug ({slug!r}) 与 util.constants.SKILL_SLUG ({constants_slug!r}) 不一致"
        )

    if slug and slug not in LEGACY_EXEMPT_SLUGS and _KEBAB_SLUG.fullmatch(slug):
        naming_errors, naming_warnings = validate_slug_semantics(
            slug,
            strict=not allow_template_placeholders,
        )
        report.errors.extend(naming_errors)
        report.warnings.extend(naming_warnings)

    return report


def _quote_identifier(name: str) -> str:
    return '"' + name.replace('"', '""') + '"'


def _table_column_info(cursor, table_name: str) -> dict[str, dict[str, object]]:
    cursor.execute(f"PRAGMA table_info({_quote_identifier(table_name)})")
    info: dict[str, dict[str, object]] = {}
    for row in cursor.fetchall():
        info[str(row[1])] = {
            "cid": int(row[0]),
            "name": str(row[1]),
            "type": str(row[2] or ""),
            "notnull": int(row[3] or 0),
            "dflt_value": row[4],
            "pk": int(row[5] or 0),
        }
    return info


def _default_uses_unixepoch(default_value: object) -> bool:
    if default_value is None:
        return False
    text = str(default_value).strip().lower()
    return "unixepoch" in text


def _expected_timestamp_display_name(column_name: str) -> str:
    if column_name == "created_at":
        return "创建时间"
    if column_name == "updated_at":
        return "更新时间"
    return ""


def validate_standard_timestamp_columns(
    cursor,
    table_name: str,
    *,
    physical_columns: list[str] | None = None,
) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []
    ordered = physical_columns or list_physical_column_names(cursor, table_name)
    column_info = _table_column_info(cursor, table_name)

    for column_name in STANDARD_TIMESTAMP_COLUMNS:
        if column_name not in ordered:
            continue

        physical = column_info.get(column_name)
        if not physical:
            errors.append(f"{table_name}.{column_name} 缺少物理字段定义")
            continue

        if "INT" not in str(physical["type"]).upper():
            errors.append(
                f"{table_name}.{column_name} 字段类型应为 INTEGER（Unix 秒级时间戳），当前为 {physical['type']!r}"
            )

        if column_name == "created_at" and not _default_uses_unixepoch(physical["dflt_value"]):
            errors.append(
                f"{table_name}.created_at 应设置数据库默认值 DEFAULT (unixepoch())，当前默认值为 {physical['dflt_value']!r}"
            )
        if column_name == "updated_at" and not _default_uses_unixepoch(physical["dflt_value"]):
            errors.append(
                f"{table_name}.updated_at 应设置数据库初始默认值 DEFAULT (unixepoch())，当前默认值为 {physical['dflt_value']!r}"
            )

        cursor.execute(
            """
            SELECT display_name, display_type, editable, searchable, display_order
            FROM _jiangchang_columns
            WHERE table_name = ? AND column_name = ?
            """,
            (table_name, column_name),
        )
        meta_row = cursor.fetchone()
        if not meta_row:
            errors.append(f"{table_name}.{column_name} 缺少 _jiangchang_columns 元数据")
            continue

        display_name, display_type, editable, searchable, display_order = meta_row
        expected_name = _expected_timestamp_display_name(column_name)
        if str(display_name or "").strip() != expected_name:
            errors.append(
                f"{table_name}.{column_name} 的 display_name 应为 {expected_name!r}，当前为 {display_name!r}"
            )
        if str(display_type or "").strip() != DATETIME_UNIX_SECONDS:
            errors.append(
                f"{table_name}.{column_name} 的 display_type 应为 {DATETIME_UNIX_SECONDS!r}，当前为 {display_type!r}"
            )
        if editable is None or int(editable) != 0:
            errors.append(f"{table_name}.{column_name} 的 editable 应为 0（系统时间字段不可编辑）")
        if display_order is not None:
            errors.append(f"{table_name}.{column_name} 的 display_order 应为 NULL")
        if searchable is not None and int(searchable) != 0:
            warnings.append(f"{table_name}.{column_name} 的时间字段通常不必开启 searchable")

    if "created_at" in ordered and "updated_at" in ordered:
        if ordered.index("updated_at") < ordered.index("created_at"):
            warnings.append(f"{table_name}: updated_at 不应出现在 created_at 之前")

    if "updated_at" in ordered and not has_updated_at_trigger(cursor, table_name):
        errors.append(
            f"{table_name}.updated_at 缺少自动维护 trigger（期望 {table_name}_set_updated_at）"
        )

    return errors, warnings


def column_order_warnings(table_name: str, ordered_names: list[str]) -> list[str]:
    warnings: list[str] = []
    if "id" in ordered_names and ordered_names.index("id") != 0:
        warnings.append(f"{table_name}: 字段 id 通常应定义在 CREATE TABLE 的第一列")
    if "created_at" in ordered_names:
        idx = ordered_names.index("created_at")
        trailing = ordered_names[idx + 1 :]
        if trailing and trailing != ["updated_at"]:
            warnings.append(
                f"{table_name}: created_at 之后通常只应跟 updated_at，不应再放置其他业务字段"
            )
    if "updated_at" in ordered_names and "created_at" in ordered_names:
        if ordered_names.index("updated_at") < ordered_names.index("created_at"):
            warnings.append(f"{table_name}: updated_at 不应出现在 created_at 之前")
    return warnings


def _table_exists(cursor, table_name: str) -> bool:
    cursor.execute(
        "SELECT 1 FROM sqlite_master WHERE type = 'table' AND name = ? LIMIT 1",
        (table_name,),
    )
    return cursor.fetchone() is not None


def validate_display_metadata(conn: sqlite3.Connection, *, check_column_order: bool = True) -> ValidationReport:
    report = ValidationReport()
    cur = conn.cursor()

    has_tables_meta = _table_exists(cur, "_jiangchang_tables")
    has_columns_meta = _table_exists(cur, "_jiangchang_columns")
    if not has_tables_meta:
        report.errors.append("缺少数据管理元数据表 _jiangchang_tables")
    if not has_columns_meta:
        report.errors.append("缺少数据管理元数据表 _jiangchang_columns")
    if not has_tables_meta or not has_columns_meta:
        return report

    for table_name in iter_user_tables(cur):
        cur.execute(
            "SELECT display_name FROM _jiangchang_tables WHERE table_name = ?",
            (table_name,),
        )
        row = cur.fetchone()
        if not row or not str(row[0] or "").strip():
            report.errors.append(f"业务表 {table_name!r} 缺少 _jiangchang_tables.display_name")
        elif not _has_cjk(str(row[0])):
            report.errors.append(f"业务表 {table_name!r} 的 display_name 应使用中文业务名称")

        physical_columns = list_physical_column_names(cur, table_name)
        if check_column_order:
            report.warnings.extend(column_order_warnings(table_name, physical_columns))

        for column_name in physical_columns:
            cur.execute(
                """
                SELECT display_name, visible
                FROM _jiangchang_columns
                WHERE table_name = ? AND column_name = ?
                """,
                (table_name, column_name),
            )
            col_row = cur.fetchone()
            if not col_row:
                report.errors.append(
                    f"字段 {table_name}.{column_name} 缺少 _jiangchang_columns 元数据"
                )
                continue
            display_name = str(col_row[0] or "").strip()
            visible = col_row[1] is None or int(col_row[1]) != 0
            if visible and not display_name:
                report.errors.append(f"字段 {table_name}.{column_name} 的 display_name 为空")
            elif visible and _looks_like_raw_physical_name(display_name, column_name):
                report.errors.append(
                    f"字段 {table_name}.{column_name} 的 display_name 不应直接等于英文物理名：{display_name!r}"
                )
            elif visible and not _has_cjk(display_name):
                report.errors.append(
                    f"字段 {table_name}.{column_name} 的 display_name 应使用中文：{display_name!r}"
                )

        ts_errors, ts_warnings = validate_standard_timestamp_columns(
            cur,
            table_name,
            physical_columns=physical_columns,
        )
        report.errors.extend(ts_errors)
        report.warnings.extend(ts_warnings)

    cur.execute("SELECT table_name, column_name FROM _jiangchang_columns")
    for table_name, column_name in cur.fetchall():
        if table_name in METADATA_TABLES:
            continue
        cur.execute(
            "SELECT 1 FROM sqlite_master WHERE type='table' AND name = ?",
            (table_name,),
        )
        if not cur.fetchone():
            report.errors.append(f"元数据引用了不存在的表：{table_name!r}")
            continue
        physical = list_physical_column_names(cur, str(table_name))
        if str(column_name) not in physical:
            report.errors.append(f"元数据引用了不存在的字段：{table_name}.{column_name}")

    cur.execute("SELECT table_name FROM _jiangchang_tables")
    for (table_name,) in cur.fetchall():
        if table_name in METADATA_TABLES:
            continue
        cur.execute(
            "SELECT 1 FROM sqlite_master WHERE type='table' AND name = ?",
            (table_name,),
        )
        if not cur.fetchone():
            report.errors.append(f"元数据引用了不存在的表：{table_name!r}")

    return report


def validate_template_database(conn: sqlite3.Connection) -> ValidationReport:
    report = validate_display_metadata(conn)
    physical = list_physical_column_names(conn.cursor(), TASK_LOGS_TABLE)
    expected = [str(item["column_name"]) for item in TASK_LOGS_COLUMN_METADATA]
    if physical != expected:
        report.errors.append(
            f"task_logs 物理字段顺序应为 {expected}，当前为 {physical}"
        )
    return report
