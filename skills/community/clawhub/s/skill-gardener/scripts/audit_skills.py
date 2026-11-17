#!/usr/bin/env python3
"""Read-only structural audit of a skill directory or a bounded skill collection."""

from __future__ import annotations

import argparse
import ast
from datetime import date
import json
import os
import re
import stat
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    yaml = None

NAME_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
MAX_FILE_BYTES = 1024 * 1024
MAX_YAML_DEPTH = 32
MAX_ENTRIES = 10000
DEFAULT_DEPTH = 6
MAX_DEPTH = 64
IGNORED_DIRS = frozenset({".git", ".hg", ".svn", ".venv", "venv", "node_modules", "__pycache__"})


class FrontmatterError(ValueError):
    """Invalid or unsupported YAML in the audit's portable subset."""


def strip_comment(value: str) -> str:
    """Remove a YAML comment while preserving quoted scalar content."""
    quote = None
    escaped = False
    for index, char in enumerate(value):
        if quote == '"' and char == "\\" and not escaped:
            escaped = True
            continue
        if char in "\"'" and not escaped:
            quote = None if quote == char else (char if quote is None else quote)
        elif char == "#" and quote is None and (index == 0 or value[index - 1].isspace()):
            return value[:index].rstrip()
        escaped = False
    if quote is not None:
        raise FrontmatterError("unterminated quoted scalar")
    return value.rstrip()


def split_flow(value: str, delimiter: str = ",") -> list[str]:
    """Split a flow collection without interpreting quotes or nested brackets."""
    parts, start, depth, quote, escaped = [], 0, 0, None, False
    for index, char in enumerate(value):
        if quote == '"' and char == "\\" and not escaped:
            escaped = True
            continue
        if char in "\"'" and not escaped:
            quote = None if quote == char else (char if quote is None else quote)
        elif quote is None:
            if char in "[{":
                depth += 1
            elif char in "]}":
                depth -= 1
                if depth < 0:
                    raise FrontmatterError("unbalanced flow collection")
            elif char == delimiter and depth == 0:
                parts.append(value[start:index].strip())
                start = index + 1
        escaped = False
    if quote is not None or depth != 0:
        raise FrontmatterError("unterminated flow collection")
    parts.append(value[start:].strip())
    return parts


def parse_scalar(value: str, depth: int) -> object:
    value = strip_comment(value).strip()
    if depth > MAX_YAML_DEPTH:
        raise FrontmatterError("YAML nesting limit exceeded")
    if not value:
        return None
    if value.startswith(("&", "*", "!")) or value.startswith("<<:"):
        raise FrontmatterError("YAML aliases, merge keys, and tags are not supported")
    if value[0] == "'":
        if len(value) < 2 or value[-1] != "'":
            raise FrontmatterError("unterminated quoted scalar")
        return value[1:-1].replace("''", "'")
    if value[0] == '"':
        try:
            return json.loads(value)
        except json.JSONDecodeError as exc:
            raise FrontmatterError("invalid double-quoted scalar") from exc
    if value.startswith("["):
        if not value.endswith("]"):
            raise FrontmatterError("unterminated flow sequence")
        inner = value[1:-1].strip()
        return [] if not inner else [parse_scalar(part, depth + 1) for part in split_flow(inner)]
    if value.startswith("{"):
        if not value.endswith("}"):
            raise FrontmatterError("unterminated flow mapping")
        result = {}
        inner = value[1:-1].strip()
        for item in ([] if not inner else split_flow(inner)):
            key_value = split_flow(item, ":")
            if len(key_value) != 2:
                raise FrontmatterError("invalid flow mapping")
            key = parse_scalar(key_value[0], depth + 1)
            if not isinstance(key, str) or key == "<<" or key in result:
                raise FrontmatterError("mapping keys must be unique strings")
            result[key] = parse_scalar(key_value[1], depth + 1)
        return result
    if value in ("null", "Null", "NULL", "~"):
        return None
    if value in ("true", "True", "TRUE"):
        return True
    if value in ("false", "False", "FALSE"):
        return False
    if re.fullmatch(r"[0-9]{4}-[0-9]{2}-[0-9]{2}", value):
        try:
            return date.fromisoformat(value)
        except ValueError as exc:
            raise FrontmatterError("invalid date scalar") from exc
    try:
        return ast.literal_eval(value)
    except (ValueError, SyntaxError):
        return value


def fallback_load(source: str) -> dict:
    """Parse the safe, documented YAML subset without third-party packages."""
    lines = source.splitlines()

    def block(index: int, indent: int, depth: int) -> tuple[object, int]:
        if depth > MAX_YAML_DEPTH:
            raise FrontmatterError("YAML nesting limit exceeded")
        result: object | None = None
        while index < len(lines):
            raw = lines[index]
            if not raw.strip() or raw.lstrip().startswith("#"):
                index += 1
                continue
            current = len(raw) - len(raw.lstrip(" "))
            if "\t" in raw[: len(raw) - len(raw.lstrip())] or current < indent:
                break
            if current != indent:
                raise FrontmatterError("invalid indentation")
            text = strip_comment(raw.strip())
            if text.startswith("- ") or text == "-":
                if result is None:
                    result = []
                if not isinstance(result, list):
                    raise FrontmatterError("mixed mapping and sequence")
                item = text[1:].strip()
                if item:
                    result.append(parse_scalar(item, depth + 1))
                    index += 1
                else:
                    index += 1
                    child, index = block(index, indent + 2, depth + 1)
                    result.append(child)
                continue
            if ":" not in text:
                raise FrontmatterError("invalid mapping entry")
            key_text, value = text.split(":", 1)
            key = parse_scalar(key_text, depth + 1)
            if not isinstance(key, str) or key == "<<":
                raise FrontmatterError("mapping keys must be strings; YAML merge keys are unsupported")
            if result is None:
                result = {}
            if not isinstance(result, dict):
                raise FrontmatterError("mixed mapping and sequence")
            if key in result:
                raise FrontmatterError("duplicate mapping key")
            value = value.strip()
            if value in ("|", "|-", "|+", ">", ">-", ">+"):
                folded, index = [], index + 1
                while index < len(lines) and (not lines[index].strip() or len(lines[index]) - len(lines[index].lstrip(" ")) > indent):
                    content = lines[index]
                    folded.append(content[indent + 2:] if len(content) > indent + 1 else "")
                    index += 1
                text_value = (" " if value.startswith(">") else "\n").join(folded).rstrip("\n")
                result[key] = text_value if value.endswith("-") else text_value + "\n"
            elif value:
                result[key] = parse_scalar(value, depth + 1)
                index += 1
            else:
                index += 1
                child, index = block(index, indent + 2, depth + 1)
                result[key] = child
        if result is None:
            raise FrontmatterError("empty frontmatter")
        return result, index

    parsed, index = block(0, 0, 0)
    if index != len(lines) or not isinstance(parsed, dict):
        raise FrontmatterError("frontmatter must be a mapping")
    return parsed


if yaml is not None:
    class FrontmatterLoader(yaml.SafeLoader):
        """Safe YAML with unique string keys and bounded, alias-free nesting."""

        def __init__(self, stream):
            super().__init__(stream)
            self.nesting = 0

        def compose_node(self, parent, index):
            if self.check_event(yaml.AliasEvent):
                raise yaml.YAMLError("YAML aliases are not supported")
            self.nesting += 1
            try:
                if self.nesting > MAX_YAML_DEPTH:
                    raise yaml.YAMLError("YAML nesting limit exceeded")
                return super().compose_node(parent, index)
            finally:
                self.nesting -= 1

        def construct_mapping(self, node, deep=False):
            keys = set()
            for key_node, _ in node.value:
                if key_node.tag != "tag:yaml.org,2002:str":
                    raise yaml.YAMLError("mapping keys must be strings; YAML merge keys are unsupported")
                key = self.construct_object(key_node, deep=deep)
                if key in keys:
                    raise yaml.YAMLError("duplicate mapping key")
                keys.add(key)
            return super().construct_mapping(node, deep=deep)


def read_skill(path: Path) -> str:
    """Read a bounded regular file, refusing a symlink at the file itself.

    Discovery also refuses symlink directories. This is a static audit, not a
    sandbox for trees being concurrently changed by an adversarial process.
    """
    info = path.lstat()
    if not stat.S_ISREG(info.st_mode):
        raise ValueError("SKILL.md must be a regular file, not a symlink or special file")
    flags = os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0) | getattr(os, "O_NONBLOCK", 0)
    fd = os.open(path, flags)
    with os.fdopen(fd, "rb") as source:
        opened = os.fstat(source.fileno())
        if not stat.S_ISREG(opened.st_mode):
            raise ValueError("SKILL.md must be a regular file")
        if (info.st_dev, info.st_ino) != (opened.st_dev, opened.st_ino):
            raise ValueError("SKILL.md changed during inspection; retry on a stable tree")
        if opened.st_size > MAX_FILE_BYTES:
            raise ValueError("SKILL.md exceeds the 1 MiB audit limit")
        raw = source.read(MAX_FILE_BYTES + 1)
    if len(raw) > MAX_FILE_BYTES:
        raise ValueError("SKILL.md exceeds the 1 MiB audit limit")
    return raw.decode("utf-8").replace("\r\n", "\n")


def parse_frontmatter(path: Path) -> tuple[dict, str | None]:
    try:
        text = read_skill(path)
    except (OSError, UnicodeError, ValueError) as exc:
        # Do not echo file contents or exception text containing arbitrary paths.
        if isinstance(exc, ValueError) and not isinstance(exc, UnicodeError):
            return {}, str(exc)
        return {}, "cannot read SKILL.md as a regular UTF-8 file"

    lines = text.split("\n")
    if lines[0] != "---":
        return {}, "frontmatter must start at byte zero with '---'"
    end = next((i for i in range(1, len(lines)) if lines[i] == "---"), None)
    if end is None:
        return {}, "missing closing frontmatter delimiter"
    if not "\n".join(lines[end + 1:]).strip():
        return {}, "skill body is empty"
    try:
        source = "\n".join(lines[1:end]) + "\n"
        fields = yaml.load(source, Loader=FrontmatterLoader) if yaml is not None else fallback_load(source)
    except ((yaml.YAMLError if yaml is not None else FrontmatterError), ValueError, OverflowError, RecursionError) as exc:
        mark = getattr(exc, "problem_mark", None)
        location = f" near line {mark.line + 2}, column {mark.column + 1}" if mark else ""
        return {}, "invalid or unsupported YAML frontmatter" + location
    if not isinstance(fields, dict):
        return {}, "frontmatter must be a mapping"
    return fields, None


def invalid_root(root: Path) -> bool:
    try:
        return not root.is_dir() or any(part.is_symlink() for part in (root, *root.parents))
    except OSError:
        return True


def audit(root: Path, *, single: bool = False, max_depth: int = DEFAULT_DEPTH) -> dict:
    root = root.absolute()
    issues: list[dict[str, str]] = []
    warnings: list[dict[str, str]] = []
    files: list[Path] = []
    names: dict[str, Path] = {}
    result = {
        "root": str(root),
        "scope": "skill" if single else "collection",
        "skills": 0,
        "passed": False,
        "issues": issues,
        "warnings": warnings,
    }

    def issue(path: Path, message: str) -> None:
        issues.append({"file": str(path), "issue": message})

    if invalid_root(root):
        issue(root, "root must be an existing directory without symlink path components")
        return result
    if not 1 <= max_depth <= MAX_DEPTH:
        issue(root, "max_depth must be between 1 and 64")
        return result
    root = root.resolve()
    result["root"] = str(root)

    visited = 0

    def discover(directory: Path, depth: int) -> None:
        nonlocal visited
        skill_file = directory / "SKILL.md"
        # lexists also detects broken symlinks. Stop below a skill boundary.
        if os.path.lexists(skill_file):
            files.append(skill_file)
            return
        try:
            with os.scandir(directory) as entries:
                children = []
                for entry in entries:
                    visited += 1
                    if visited > MAX_ENTRIES:
                        raise ValueError
                    children.append(entry)
            for child in sorted(children, key=lambda entry: entry.name):
                if child.name in IGNORED_DIRS:
                    continue
                child_path = directory / child.name
                if child.is_symlink():
                    issue(child_path, "symlink skipped; collection is not fully audited")
                elif child.is_dir(follow_symlinks=False):
                    if depth >= max_depth:
                        issue(child_path, "depth limit reached; collection is not fully audited")
                    else:
                        discover(child_path, depth + 1)
        except OSError:
            issue(directory, "cannot enumerate directory; collection is not fully audited")

    if single:
        files.append(root / "SKILL.md")
    else:
        try:
            discover(root, 0)
        except ValueError:
            issue(root, "entry limit reached; collection is not fully audited")
    if not files:
        issue(root, "no SKILL.md files found in the requested scope")

    for path in files:
        fields, error = parse_frontmatter(path)
        if error:
            issue(path, error)
            continue
        name = fields.get("name")
        description = fields.get("description")
        if not isinstance(name, str) or not 1 <= len(name) <= 64 or not NAME_RE.fullmatch(name):
            issue(path, "name must be 1–64 lowercase letters/digits with single internal hyphens")
        else:
            if name in names:
                issue(path, f"duplicate skill name also used by {names[name]}")
            names[name] = path
            if path.parent.name != name:
                warnings.append({"file": str(path), "warning": "directory name differs from skill name; check target runtime compatibility"})
        if not isinstance(description, str) or not description.strip():
            issue(path, "description must be a non-empty string")
        elif len(description) > 1024:
            issue(path, "description exceeds 1024 characters")
        for field in ("compatibility", "license"):
            if field in fields and (not isinstance(fields[field], str) or not fields[field].strip()):
                issue(path, f"{field} must be a non-empty string when provided")
        if "allowed-tools" in fields:
            tools = fields["allowed-tools"]
            if isinstance(tools, str):
                valid_tools = bool(tools.strip())
            else:
                valid_tools = isinstance(tools, list) and bool(tools) and all(isinstance(tool, str) and tool.strip() for tool in tools)
            if not valid_tools:
                issue(path, "allowed-tools must be a non-empty string or list of non-empty strings when provided")
        if isinstance(fields.get("compatibility"), str) and len(fields["compatibility"]) > 500:
            issue(path, "compatibility exceeds 500 characters")
        # OpenClaw accepts nested metadata; it is not limited to flat strings.
        if "metadata" in fields and fields["metadata"] is not None and not isinstance(fields["metadata"], dict):
            issue(path, "metadata must be a mapping when provided")

    result["skills"] = len(files)
    result["passed"] = not issues
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("root", nargs="?", type=Path, help="collection root (default: ./skills)")
    parser.add_argument("--skill", type=Path, help="validate one skill directory without scanning its siblings")
    parser.add_argument("--max-depth", type=int, default=DEFAULT_DEPTH, help="collection directory depth (default: 6)")
    args = parser.parse_args()
    if args.skill is not None and args.root is not None:
        parser.error("use a collection root or --skill, not both")
    if not 1 <= args.max_depth <= MAX_DEPTH:
        parser.error("--max-depth must be between 1 and 64")
    root = args.skill if args.skill is not None else (args.root or Path("skills"))
    result = audit(root, single=args.skill is not None, max_depth=args.max_depth)
    print(json.dumps(result, indent=2))
    if invalid_root(root.absolute()):
        return 2
    return 0 if result["passed"] else 1


if __name__ == "__main__":
    sys.exit(main())
