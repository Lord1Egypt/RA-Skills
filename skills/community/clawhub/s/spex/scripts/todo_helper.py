#!/usr/bin/env python3
"""Unified CRUD operations for todo files (JSON and XML)."""

from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
import textwrap
import xml.etree.ElementTree as ET
from pathlib import Path

from cli import ArgumentParser
from common import (
    atomic_write_json,
    escape_xml_text,
    load_and_validate_todo_json,
    local_iso_timestamp,
    logger,
    resolve_spec_dir,
    validate_unique_ids,
)

REQUIRED_FIELDS = ("id", "name", "details", "completed_at", "commit_title")


def _resolve_completed_at(value):
    """Resolve the special value 'now' to a local ISO timestamp."""
    if isinstance(value, str) and value.lower() == "now":
        return local_iso_timestamp()
    return value


# ---------------------------------------------------------------------------
# Load / write dispatchers
# ---------------------------------------------------------------------------

_XML_TO_DICT = {
    "step-id": "id",
    "step-name": "name",
    "step-details": "details",
    "completed-at": "completed_at",
    "commit-title": "commit_title",
}
_DICT_TO_XML = {v: k for k, v in _XML_TO_DICT.items()}


def load_todo_xml(path):
    """Load todo entries from an XML file."""
    path = Path(path)
    if not path.is_file():
        return []
    content = path.read_text(encoding="utf-8").strip()
    if not content:
        return []
    try:
        root = ET.fromstring(content)
    except ET.ParseError as exc:
        logger.error(
            "Error: failed to parse XML '%s': %s", path, exc,
        )
        sys.exit(1)
    if root.tag != "todo":
        logger.error(
            "Error: expected root element <todo>,"
            " got <%s>.", root.tag,
        )
        sys.exit(1)
    entries = []
    for step in root.findall("step"):
        entry = {}
        for xml_name, dict_key in _XML_TO_DICT.items():
            elem = step.find(xml_name)
            entry[dict_key] = (
                elem.text if elem is not None and elem.text
                else ""
            )
        entries.append(entry)
    return entries


def write_todo_xml(path, data):
    """Write todo entries to an XML file."""
    path = Path(path)
    lines = ["<todo>"]
    for item in data:
        lines.append("  <step>")
        for dict_key in (
            "id", "name", "details",
            "completed_at", "commit_title",
        ):
            xml_name = _DICT_TO_XML[dict_key]
            value = escape_xml_text(str(item.get(dict_key, "")))
            lines.append(
                f"    <{xml_name}>{value}</{xml_name}>",
            )
        lines.append("  </step>")
    lines.append("</todo>\n")
    content = "\n".join(lines)
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp_fd = tempfile.NamedTemporaryFile(
        mode="w",
        encoding="utf-8",
        dir=path.parent,
        suffix=".tmp",
        delete=False,
    )
    try:
        tmp_fd.write(content)
        tmp_fd.close()
        os.replace(tmp_fd.name, str(path))
    except BaseException:
        tmp_fd.close()
        if os.path.exists(tmp_fd.name):
            os.unlink(tmp_fd.name)


def load_todo_json(path):
    """Load todo entries from a JSON file.

    Returns an empty list when the file does not exist or is empty.
    """
    path = Path(path)
    if not path.is_file():
        return []
    content = path.read_text(encoding="utf-8").strip()
    if not content:
        return []
    return load_and_validate_todo_json(path, allow_empty=True)


def load_todo_file(path, is_xml=False):
    """Dispatch to the appropriate loader based on format."""
    if is_xml:
        return load_todo_xml(path)
    return load_todo_json(path)


def write_todo_file(path, data, is_xml=False):
    """Dispatch to the appropriate writer based on format."""
    if is_xml:
        write_todo_xml(path, data)
    else:
        atomic_write_json(Path(path), data)


# ---------------------------------------------------------------------------
# Subcommands
# ---------------------------------------------------------------------------

def cmd_validate(todo_path, is_xml):
    """Validate todo file format and check for duplicate IDs."""
    data = load_todo_file(todo_path, is_xml)
    validate_unique_ids(data)
    for i, item in enumerate(data):
        for field in REQUIRED_FIELDS:
            if field not in item:
                logger.error(
                    "Error: item[%d]: missing required field"
                    " '%s'.", i, field,
                )
                sys.exit(1)
    logger.info("OK")


def cmd_append(todo_path, is_xml, args):
    """Append a new entry to the todo file."""
    if args.details_from_stdin:
        details = sys.stdin.read()
    elif args.details is not None:
        details = args.details
    else:
        logger.error(
            "Error: --details or --details-from-stdin required.",
        )
        sys.exit(1)

    data = load_todo_file(todo_path, is_xml)

    for item in data:
        if isinstance(item, dict) and item.get("id") == args.id:
            logger.error(
                "Error: duplicate id '%s'.", args.id,
            )
            sys.exit(1)

    entry = {
        "id": args.id,
        "name": args.step_name,
        "details": details,
        "completed_at": _resolve_completed_at(args.completed_at),
        "commit_title": args.commit_title,
    }
    data.append(entry)
    write_todo_file(todo_path, data, is_xml)
    logger.info("Appended '%s'.", args.id)


def _short_head_sha() -> str:
    """Return short HEAD sha, or empty string when unavailable."""
    try:
        result = subprocess.run(
            ["git", "rev-parse", "--short", "HEAD"],
            capture_output=True,
            text=True,
            check=False,
        )
    except OSError:
        return ""
    if result.returncode != 0:
        return ""
    return (result.stdout or "").strip()


def _sha_from_commit_title(commit_title) -> str:
    """Extract leading short sha from persisted ``%h: %s`` commit_title."""
    prefix = str(commit_title).split(":", 1)[0].strip()
    if (
        4 <= len(prefix) <= 40
        and all(c in "0123456789abcdef" for c in prefix.lower())
    ):
        return prefix
    return ""


def _emit_todo_edit_apply_anchor(todo_path, args, item) -> None:
    """Emit APPLY anchors for commit-title / completed_at edits."""
    from debug_log import emit_apply_anchor

    # todo.json / todo.xml live directly under the spec directory.
    spec_dir = Path(todo_path).parent

    if args.completed_at is not None and item.get("completed_at"):
        emit_apply_anchor(
            spec_dir,
            f"===== APPLY task done id={args.id} =====",
        )
        return

    if (
        args.commit_title is not None
        and str(args.commit_title).strip()
        and not item.get("completed_at")
    ):
        # Prefer sha already persisted in commit_title over probing HEAD.
        sha = (
            _sha_from_commit_title(args.commit_title)
            or _short_head_sha()
        )
        emit_apply_anchor(
            spec_dir,
            f"===== APPLY task committed id={args.id} sha={sha} =====",
        )


def cmd_edit(todo_path, is_xml, args):
    """Edit an existing entry by ID."""
    details = args.details
    if args.details_from_stdin:
        details = sys.stdin.read()

    if args.completed_at is not None:
        args.completed_at = _resolve_completed_at(args.completed_at)

    data = load_todo_file(todo_path, is_xml)

    found = False
    updated_item = None
    for item in data:
        if isinstance(item, dict) and item.get("id") == args.id:
            if args.step_name is not None:
                item["name"] = args.step_name
            if details is not None:
                item["details"] = details
            if args.completed_at is not None:
                item["completed_at"] = args.completed_at
            if args.commit_title is not None:
                item["commit_title"] = args.commit_title
            found = True
            updated_item = item
            break

    if not found:
        logger.error(
            "Error: id '%s' not found.", args.id,
        )
        sys.exit(1)

    write_todo_file(todo_path, data, is_xml)
    logger.info("Updated '%s'.", args.id)
    if updated_item is not None:
        _emit_todo_edit_apply_anchor(todo_path, args, updated_item)


def cmd_remove(todo_path, is_xml, args):
    """Remove an entry by ID."""
    data = load_todo_file(todo_path, is_xml)

    new_data = [
        item for item in data
        if not (isinstance(item, dict) and item.get("id") == args.id)
    ]

    if len(new_data) == len(data):
        logger.error(
            "Error: id '%s' not found.", args.id,
        )
        sys.exit(1)

    write_todo_file(todo_path, new_data, is_xml)
    logger.info("Removed '%s'.", args.id)


def _wrap_field(label, text, indent, width=10**9):
    """Wrap a sub-bullet field."""
    prefix = f"{indent}- {label}: "
    cont = " " * len(prefix)
    result = []
    for i, paragraph in enumerate(text.split("\n")):
        if i == 0:
            result.append(textwrap.fill(
                paragraph, width=width,
                initial_indent=prefix,
                subsequent_indent=cont,
            ))
        else:
            result.append(textwrap.fill(
                paragraph, width=width,
                initial_indent=cont,
                subsequent_indent=cont,
            ) if paragraph.strip() else cont.rstrip())
    return "\n".join(result)


def _format_block_details(text, indent, width=10**9):
    """Format multi-line details using block scalar syntax."""
    content_indent = " " * (len(indent) + 4)
    lines = [f"{indent}- details: |"]
    for paragraph in text.split("\n"):
        if paragraph.strip():
            lines.append(textwrap.fill(
                paragraph, width=width,
                initial_indent=content_indent,
                subsequent_indent=content_indent,
            ))
        else:
            lines.append("")
    return "\n".join(lines)


def _format_markdown(data, width=0):
    """Format todo entries as markdown.

    width=0 disables wrapping (lines may exceed 80 chars).
    """
    w = width if width > 0 else 10**9
    lines = []
    for idx, item in enumerate(data, 1):
        step_id = item.get("id", "")
        completed = bool(item.get("completed_at"))
        icon = "✅" if completed else "🔲"
        prefix = f"{idx}. "
        indent = " " * len(prefix)
        lines.append(f"{prefix}{icon} {step_id}")

        name = item.get("name", "")
        if name:
            lines.append(f"{indent}- name: {name}")

        details = item.get("details", "")
        if details:
            if "\n" in details:
                lines.append(
                    _format_block_details(details, indent, w),
                )
            else:
                lines.append(
                    _wrap_field("details", details, indent, w),
                )

        completed_at = item.get("completed_at", "")
        if completed_at:
            lines.append(f"{indent}- completed_at: {completed_at}")

        commit_title = item.get("commit_title", "")
        if commit_title:
            lines.append(
                _wrap_field("commit_title", commit_title, indent, w),
            )

    return "\n".join(lines)


def cmd_show(todo_path, is_xml, args):
    """Display entries with optional filtering and format."""
    data = load_todo_file(todo_path, is_xml)

    if args.step_id:
        data = [
            item for item in data
            if isinstance(item, dict) and item.get("id") == args.step_id
        ]
        if not data:
            logger.error(
                "Error: id '%s' not found.", args.step_id,
            )
            sys.exit(1)
    elif args.done:
        data = [
            item for item in data
            if isinstance(item, dict) and item.get("completed_at")
        ]
    elif args.undone:
        data = [
            item for item in data
            if isinstance(item, dict) and not item.get("completed_at")
        ]

    if args.fmt == "markdown":
        print(_format_markdown(data, width=80 if args.wrap else 0))
    else:
        print(json.dumps(data, indent=2, ensure_ascii=False))


def cmd_xml2json(todo_path, is_xml, args):
    """Convert an XML todo file to JSON format."""
    data = load_todo_xml(todo_path)
    output_path = todo_path.with_suffix(".json")
    atomic_write_json(output_path, data)
    if args.rm:
        todo_path.unlink()
    logger.info("Converted %s -> %s", todo_path, output_path)


def cmd_json2xml(todo_path, is_xml, args):
    """Convert a JSON todo file to XML format."""
    data = load_todo_json(todo_path)
    output_path = todo_path.with_suffix(".xml")
    write_todo_xml(output_path, data)
    if args.rm:
        todo_path.unlink()
    logger.info("Converted %s -> %s", todo_path, output_path)


# ---------------------------------------------------------------------------
# Main entry point
# ---------------------------------------------------------------------------

def _resolve_todo_path(args):
    """Resolve the todo file path from parsed global arguments.

    Returns (todo_path, is_xml) tuple.
    """
    is_xml = args.xml

    if args.todo_file:
        todo_path = Path(args.todo_file)
        if not is_xml and todo_path.suffix == ".xml":
            is_xml = True
        return (todo_path, is_xml)

    # --name mode: resolve spec dir for todo file
    spec_dir = resolve_spec_dir(args.name)
    filename = "todo.xml" if is_xml else "todo.json"
    return (spec_dir / filename, is_xml)


_LOCATOR_FLAGS_WITH_VALUE = ("--name", "--todo-file")
_LOCATOR_FLAGS_BOOL = ("--xml",)
# Subcommand options that take a value. Their next argv token must
# not be classified as a hoistable locator, even when it looks like
# a flag (e.g. ``--commit-title --xml``).
_VALUE_TAKING_SUB_FLAGS = frozenset({
    "--id",
    "--step-name",
    "--details",
    "--completed-at",
    "--commit-title",
    "--format",
})


def _hoist_locator_flags(argv):
    """Move locator flags before the subcommand for argparse.

    Agents sometimes place ``--name`` / ``--todo-file`` / ``--xml``
    after the subcommand; argparse only accepts parent options before
    it. Hoisting keeps mutual exclusivity and existing parse paths.

    Value-taking subcommand flags keep their following token so a
    value that literally equals a locator flag is not stolen.
    """
    argv = list(argv)
    hoisted = []
    remaining = []
    i = 0
    n = len(argv)
    while i < n:
        arg = argv[i]
        if arg in _LOCATOR_FLAGS_WITH_VALUE:
            # Only hoist when a value token follows; leave bare
            # --name / --todo-file in place so argparse reports
            # the real missing-argument error instead of rewriting
            # the subcommand into the flag value.
            if i + 1 < n and not argv[i + 1].startswith("-"):
                hoisted.append(arg)
                hoisted.append(argv[i + 1])
                i += 2
            else:
                remaining.append(arg)
                i += 1
            continue
        if arg.startswith("--name=") or arg.startswith("--todo-file="):
            hoisted.append(arg)
            i += 1
            continue
        if arg in _LOCATOR_FLAGS_BOOL:
            hoisted.append(arg)
            i += 1
            continue
        if arg in _VALUE_TAKING_SUB_FLAGS:
            remaining.append(arg)
            i += 1
            # Consume the value even when it looks like an option
            # (argparse accepts that for unknown-to-subparser tokens).
            if i < n:
                remaining.append(argv[i])
                i += 1
            continue
        if arg.startswith("--") and "=" in arg:
            flag, _sep, _val = arg.partition("=")
            if flag in _VALUE_TAKING_SUB_FLAGS:
                remaining.append(arg)
                i += 1
                continue
        remaining.append(arg)
        i += 1
    return hoisted + remaining


def _build_parser():
    """Build the top-level parser with subcommand sub-parsers."""
    parser = ArgumentParser(
        prog="spex todo-helper",
        description=(
            "Operate on todo files"
            " (validate, append, edit, remove, show)."
        ),
    )
    locator = parser.add_mutually_exclusive_group()
    locator.add_argument(
        "--name",
        help=(
            "Resolve spec dir for todo file"
            " (accepted before or after the subcommand)"
        ),
    )
    locator.add_argument(
        "--todo-file",
        help=(
            "Direct path to todo file"
            " (accepted before or after the subcommand)"
        ),
    )
    parser.add_argument(
        "--xml", action="store_true", help="Force XML format",
    )

    subs = parser.add_subparsers(dest="subcmd", title="Subcommands")

    # validate
    subs.add_parser(
        "validate",
        description=(
            "Validate todo file format and check"
            " for duplicate IDs."
        ),
        help="Validate todo file format and check duplicate IDs",
    )

    # append
    p_append = subs.add_parser(
        "append",
        description="Append a new entry to the todo file.",
        help="Append a new entry",
    )
    p_append.add_argument(
        "--id", required=True, help="Task ID",
    )
    p_append.add_argument(
        "--step-name", required=True, help="Task name",
    )
    p_append.add_argument(
        "--details", default=None, help="Task details text",
    )
    p_append.add_argument(
        "--details-from-stdin", action="store_true",
        help="Read details from stdin",
    )
    p_append.add_argument(
        "--completed-at", default="",
        help="Completion timestamp (or 'now')",
    )
    p_append.add_argument(
        "--commit-title", default="",
        help="Commit title for the task",
    )

    # edit
    p_edit = subs.add_parser(
        "edit",
        description="Edit an existing entry by ID.",
        help="Edit an existing entry by ID",
    )
    p_edit.add_argument(
        "--id", required=True, help="Task ID to edit",
    )
    p_edit.add_argument(
        "--step-name", default=None, help="New task name",
    )
    p_edit.add_argument(
        "--details", default=None, help="New details text",
    )
    p_edit.add_argument(
        "--details-from-stdin", action="store_true",
        help="Read details from stdin",
    )
    p_edit.add_argument(
        "--completed-at", default=None,
        help="Completion timestamp (or 'now')",
    )
    p_edit.add_argument(
        "--commit-title", default=None,
        help="Commit title for the task",
    )

    # remove
    p_remove = subs.add_parser(
        "remove",
        description="Remove an entry by ID.",
        help="Remove an entry by ID",
    )
    p_remove.add_argument(
        "--id", required=True, help="Task ID to remove",
    )

    # show
    p_show = subs.add_parser(
        "show",
        description=(
            "Display entries with filtering and format options."
        ),
        help="Display entries with filtering and format options",
    )
    show_filter = p_show.add_mutually_exclusive_group()
    show_filter.add_argument(
        "--done", action="store_true",
        help="Show only completed entries",
    )
    show_filter.add_argument(
        "--undone", action="store_true",
        help="Show only incomplete entries",
    )
    p_show.add_argument(
        "--id", dest="step_id", default=None,
        help=(
            "Show a single entry by ID "
            "(ignores --done/--undone if set)"
        ),
    )
    p_show.add_argument(
        "--format", dest="fmt",
        choices=["json", "markdown"], default="json",
        help="Output format (default: json)",
    )
    wrap_group = p_show.add_mutually_exclusive_group()
    wrap_group.add_argument(
        "--wrap", action="store_true", default=False,
        help="Wrap long lines at 80 columns",
    )
    wrap_group.add_argument(
        "--no-wrap", dest="wrap", action="store_false",
        help="Do not wrap lines (default)",
    )

    # xml2json
    p_xml2json = subs.add_parser(
        "xml2json",
        description="Convert an XML todo file to JSON format.",
        help="Convert XML todo file to JSON format",
    )
    p_xml2json.add_argument(
        "--rm", action="store_true",
        help="Remove the source XML file after conversion",
    )

    # json2xml
    p_json2xml = subs.add_parser(
        "json2xml",
        description="Convert a JSON todo file to XML format.",
        help="Convert JSON todo file to XML format",
    )
    p_json2xml.add_argument(
        "--rm", action="store_true",
        help="Remove the source JSON file after conversion",
    )

    return parser


def main(argv=None):
    """Parse args, resolve todo path, route to subcommand."""
    parser = _build_parser()
    if argv is None:
        argv = sys.argv[1:]
    args = parser.parse(_hoist_locator_flags(argv))

    if not args.subcmd:
        parser.print_help(sys.stderr)
        sys.exit(0)

    if not args.name and not args.todo_file:
        logger.error(
            "Error: one of the arguments --name"
            " --todo-file is required.",
        )
        sys.exit(2)

    todo_path, is_xml = _resolve_todo_path(args)

    if args.subcmd == "validate":
        cmd_validate(todo_path, is_xml)
    elif args.subcmd == "append":
        cmd_append(todo_path, is_xml, args)
    elif args.subcmd == "edit":
        cmd_edit(todo_path, is_xml, args)
    elif args.subcmd == "remove":
        cmd_remove(todo_path, is_xml, args)
    elif args.subcmd == "show":
        cmd_show(todo_path, is_xml, args)
    elif args.subcmd == "xml2json":
        cmd_xml2json(todo_path, is_xml, args)
    elif args.subcmd == "json2xml":
        cmd_json2xml(todo_path, is_xml, args)


if __name__ == "__main__":
    from common import setup_logging
    setup_logging()
    main()
