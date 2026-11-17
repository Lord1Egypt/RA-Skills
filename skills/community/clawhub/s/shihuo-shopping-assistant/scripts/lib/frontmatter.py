"""Skill frontmatter 的解析工具。

优先使用 PyYAML 解析完整 YAML；本地没有 PyYAML 时使用一个只读的最小
解析器，覆盖本项目需要的顶层标量、块字符串、列表和嵌套映射。
"""

from __future__ import annotations

from pathlib import Path
from typing import Any


class FrontmatterError(ValueError):
    """frontmatter 不是可解析的 YAML 文档。"""


def split_frontmatter(text: str) -> tuple[str, str]:
    """返回 ``(yaml_text, markdown_body)``，并校验包裹线。"""
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        raise FrontmatterError("SKILL.md 必须以 --- 开头声明 YAML frontmatter")
    for index in range(1, len(lines)):
        if lines[index].strip() == "---":
            return "\n".join(lines[1:index]), "\n".join(lines[index + 1 :])
    raise FrontmatterError("frontmatter 缺少结束的 ---")


def _fallback_scalar(value: str) -> Any:
    value = value.strip()
    if not value:
        return None
    if (value.startswith("\"") and value.endswith("\"")) or (
        value.startswith("'") and value.endswith("'")
    ):
        return value[1:-1]
    if value in {"true", "True"}:
        return True
    if value in {"false", "False"}:
        return False
    if value in {"null", "Null", "~"}:
        return None
    if value.startswith("[") and value.endswith("]"):
        return [_fallback_scalar(item) for item in value[1:-1].split(",") if item.strip()]
    return value


def _fallback_parse(yaml_text: str) -> dict[str, Any]:
    """无第三方依赖时的有限 YAML 解析器。"""
    lines = yaml_text.splitlines()
    result: dict[str, Any] = {}
    index = 0
    while index < len(lines):
        raw = lines[index]
        index += 1
        if not raw.strip() or raw.lstrip().startswith("#") or raw.startswith((" ", "\t")):
            continue
        if ":" not in raw:
            raise FrontmatterError(f"无法解析 frontmatter 行：{raw}")
        key, value = raw.split(":", 1)
        key, value = key.strip(), value.strip()
        if value in {">", ">-", ">+", "|", "|-", "|+"}:
            block: list[str] = []
            while index < len(lines) and (not lines[index].strip() or lines[index].startswith((" ", "\t"))):
                block.append(lines[index].strip())
                index += 1
            result[key] = " ".join(item for item in block if item)
            continue
        if value:
            result[key] = _fallback_scalar(value)
            continue
        # 空值后面可以是列表或嵌套 map。
        children: list[str] = []
        while index < len(lines) and (not lines[index].strip() or lines[index].startswith((" ", "\t"))):
            children.append(lines[index])
            index += 1
        nonempty = [line.strip() for line in children if line.strip()]
        if nonempty and all(line.startswith("-") for line in nonempty):
            result[key] = [_fallback_scalar(line[1:].strip()) for line in nonempty]
        elif nonempty:
            nested: dict[str, Any] = {}
            for child in nonempty:
                if ":" in child:
                    child_key, child_value = child.split(":", 1)
                    nested[child_key.strip()] = _fallback_scalar(child_value)
            result[key] = nested
        else:
            result[key] = None
    return result


def parse_frontmatter(yaml_text: str) -> dict[str, Any]:
    """解析 YAML frontmatter 内容，结果必须是映射。"""
    try:
        import yaml  # type: ignore
    except ImportError:
        return _fallback_parse(yaml_text)

    try:
        value = yaml.safe_load(yaml_text) or {}
    except Exception as exc:  # PyYAML 的异常类型不应泄露给调用方
        raise FrontmatterError(f"frontmatter YAML 解析失败：{exc}") from exc
    if not isinstance(value, dict):
        raise FrontmatterError("frontmatter 顶层必须是 YAML 映射")
    return value


def load_frontmatter(skill_md: str | Path) -> tuple[dict[str, Any], str]:
    """读取 ``SKILL.md`` 并返回 ``(frontmatter, body)``。"""
    path = Path(skill_md)
    try:
        text = path.read_text(encoding="utf-8")
    except OSError as exc:
        raise FrontmatterError(f"无法读取 {path}：{exc}") from exc
    yaml_text, body = split_frontmatter(text)
    return parse_frontmatter(yaml_text), body


__all__ = [
    "FrontmatterError",
    "load_frontmatter",
    "parse_frontmatter",
    "split_frontmatter",
]
