#!/usr/bin/env python3
"""Get or set key/value in a spec's meta.json.

Usage: spex meta-helper <spec_name> [key] [value] [--stdin]

When no key is given, display all meta.json contents.
When key is given without value, display that key's value.
When key + value is given, set the key.
When key + --stdin is given, read value from stdin and set.
When key is 'prompts', the value is appended to the prompts array.
"""

from __future__ import annotations

import json
import sys
from dataclasses import fields

from cli import ArgumentParser
from common import (
    SpecMeta,
    atomic_write_json,
    logger,
    normalize_prompt_entry,
    resolve_spec_dir,
)


def _format_value(key, value, indent=""):
    """Format a single key-value pair for display."""
    if isinstance(value, list):
        lines = [f"{indent}{key}:"]
        for item in value:
            if isinstance(item, dict):
                first = True
                for k, v in item.items():
                    prefix = "- " if first else "  "
                    lines.append(f"{indent}{prefix}{k}: {v}")
                    first = False
            else:
                lines.append(f"{indent}- {item}")
        return "\n".join(lines)
    return f"{indent}{key}: {value}"


def _display_all(data):
    """Display all meta.json contents in config-like format."""
    for key, value in data.items():
        print(_format_value(key, value))


def _display_key(data, key):
    """Display a specific key's value."""
    if key not in data:
        logger.error("Error: key '%s' not found in meta.json", key)
        sys.exit(1)
    value = data[key]
    if isinstance(value, (dict, list)):
        print(json.dumps(value, indent=2, ensure_ascii=False))
    else:
        print(value)


def _add_images_only(meta, images, meta_path):
    """Append images to the last prompt entry (no new text)."""
    if not isinstance(meta.prompts, list) or not meta.prompts:
        logger.error("Error: no prompt entries to attach images to.")
        sys.exit(1)

    meta.prompts[-1] = normalize_prompt_entry(meta.prompts[-1])
    last_entry = meta.prompts[-1]
    existing = last_entry.get("images", [])
    for img in images:
        if img not in existing:
            existing.append(img)
    last_entry["images"] = existing

    data = meta.to_dict()
    atomic_write_json(meta_path, data)
    content = json.dumps(data, indent=2, ensure_ascii=False) + "\n"
    print(content, end="")


def _set_key(meta, key, value, meta_path, images=None):
    """Set a key in SpecMeta and write back."""
    if key == "prompts":
        from common import local_iso_timestamp
        if not isinstance(meta.prompts, list):
            meta.prompts = []
        entry = {"text": value, "timestamp": local_iso_timestamp()}
        if images:
            entry["images"] = list(images)
        meta.prompts.append(entry)
    else:
        known = {f.name for f in fields(SpecMeta)} - {"extras"}
        if key in known:
            setattr(meta, key, value)
        else:
            meta.extras[key] = value

    data = meta.to_dict()
    atomic_write_json(meta_path, data)
    content = json.dumps(data, indent=2, ensure_ascii=False) + "\n"
    print(content, end="")


def _build_parser() -> ArgumentParser:
    """Build the argument parser for ``spex meta-helper``."""
    parser = ArgumentParser(
        prog="spex meta-helper",
        description="Get or set key/value in a spec's meta.json.",
    )
    parser.add_argument(
        "spec_name",
        help="Spec name to look up",
    )
    parser.add_argument(
        "key",
        nargs="?",
        default=None,
        help="Meta key to get or set",
    )
    parser.add_argument(
        "value",
        nargs="?",
        default=None,
        help="Value to set for the key",
    )
    parser.add_argument(
        "--stdin",
        action="store_true",
        dest="stdin_flag",
        help="Read value from stdin instead of positional argument",
    )
    parser.add_argument(
        "--add-images",
        nargs="+",
        default=None,
        metavar="IMAGE",
        help="Add image paths to the prompt entry",
    )
    parser.add_argument(
        "--pre-action",
        default=None,
        metavar="EVENT_TYPE",
        help="Run pre-action hook with this event type before writing",
    )
    return parser


def main(argv=None):
    parser = _build_parser()
    args = parser.parse(argv)

    spec_name = args.spec_name
    key = args.key
    value = args.value
    stdin_flag = args.stdin_flag
    add_images = args.add_images
    pre_action = args.pre_action

    spec_dir = resolve_spec_dir(spec_name)
    meta_path = spec_dir / "meta.json"

    if not meta_path.is_file():
        logger.error("Error: file not found: %s", meta_path)
        sys.exit(1)

    try:
        data = json.loads(meta_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        logger.error("Error: invalid JSON: %s", e)
        sys.exit(1)

    meta = SpecMeta.from_dict(data)

    if pre_action:
        import hooks
        from config import get_project_context

        ctx = get_project_context()
        workdir = meta.workdir or (
            str(ctx.top_workdir) if ctx.in_git_workdir() else None
        )
        hooks.run_pre_action(
            pre_action,
            {"spex_branch": meta.spex_branch or ""},
            workdir=workdir,
            spec_name=spec_dir.name,
        )

    if key is None:
        _display_all(meta.to_dict())
    elif value is not None:
        if key == "prompts" and add_images:
            _set_key(meta, key, value, meta_path, images=add_images)
        else:
            _set_key(meta, key, value, meta_path)
    elif stdin_flag:
        value = sys.stdin.read()
        if key == "prompts" and add_images:
            _set_key(meta, key, value, meta_path, images=add_images)
        else:
            _set_key(meta, key, value, meta_path)
    elif key == "prompts" and add_images:
        _add_images_only(meta, add_images, meta_path)
    else:
        _display_key(meta.to_dict(), key)


if __name__ == "__main__":
    from common import setup_logging
    setup_logging()
    main()
