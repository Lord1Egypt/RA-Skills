#!/usr/bin/env python3
"""Render scratch-json into boxed ASCII art with stream-based v4 connectors."""
from __future__ import annotations

import argparse
import json
import os
import sys
from dataclasses import dataclass
from pathlib import Path

LVL_PREFIX = "│ "
BLOCK_CATALOG_PATH = Path(__file__).resolve().parents[1] / "data" / "BLOCK_CATALOG.json"


def load_block_catalog() -> dict[str, dict]:
    with BLOCK_CATALOG_PATH.open(encoding="utf-8") as f:
        blocks = json.load(f)
    return {
        block["opcode"]: block
        for block in blocks
        if isinstance(block, dict) and isinstance(block.get("opcode"), str)
    }


BLOCK_CATALOG = load_block_catalog()


@dataclass
class Item:
    width: int
    level: int
    content: str = ""


@dataclass
class RenderTarget:
    owner_name: str
    display_name: str
    scripts: list[list[dict]]


def parse_args():
    parser = argparse.ArgumentParser(prog="render_ascii.py")
    parser.add_argument("file", nargs="?", default="-", help="scratch-json file path or - for stdin")
    parser.add_argument("--json", help="scratch-json text to render directly")
    parser.add_argument("--targets", nargs="+", metavar="NAME", help="only render these target names")
    return parser.parse_args()


def read_input(path: str, json_text: str | None = None) -> str:
    if json_text is not None:
        return json_text
    if path != "-":
        if not os.path.isfile(path):
            raise SystemExit(f"Error: file not found: {path}")
        with open(path, encoding="utf-8") as f:
            return f.read()
    if not sys.stdin.isatty():
        return sys.stdin.read()
    raise SystemExit(
        "Usage: python3 render_ascii.py [blocks.json|-] [--json TEXT] [--targets NAME ...]\n"
        "Input must be scratch-json, not raw Scratch project.json/sprite.json."
    )


def load_scratch_json(text: str, source: str = "scratch-json"):
    try:
        return json.loads(text)
    except json.JSONDecodeError as err:
        raise SystemExit(
            f"Invalid {source} at line {err.lineno}, column {err.colno}. "
            "Check JSON syntax like commas, quotes, and brackets."
        ) from None


def validate_block(block) -> dict:
    if not isinstance(block, dict) or not isinstance(block.get("opcode"), str):
        raise SystemExit(
            "Invalid scratch-json structure. Expected each block to be an object with an 'opcode' field."
        )

    nested_blocks = block.get("blocks")
    if nested_blocks is None:
        return block
    if not isinstance(nested_blocks, list):
        raise SystemExit(
            "Invalid scratch-json structure. Expected nested 'blocks' to be a list of branches."
        )
    for branch in nested_blocks:
        if not isinstance(branch, list):
            raise SystemExit(
                "Invalid scratch-json structure. Expected each branch in nested 'blocks' to be a list of block objects."
            )
        for nested in branch:
            validate_block(nested)
    return block


def validate_script_blocks(value) -> list[dict]:
    if value is None or not isinstance(value, list):
        raise SystemExit(
            "Invalid scratch-json structure. Expected 'blocks' in a script object to be a list of block objects."
        )

    blocks = []
    for block in value:
        blocks.append(validate_block(block))
    return blocks


def pad_text(vals: list, min_width: int = 10) -> list[str]:
    max_length = max((len(str(val)) for val in vals), default=0)
    max_length = max(max_length, min_width)
    return [str(val).ljust(max_length) for val in vals]


def to_variable_scripts(variables: list[dict]) -> list[list[dict]]:
    scripts = []
    for item in variables:
        pairs = pad_text([item["name"], item["value"]])
        blocks = []
        for val in pairs:
            blocks.append({"opcode": "custom_text", "params": [val]})
        scripts.append(blocks)
    return scripts


def to_list_scripts(lists: list[dict]) -> list[list[dict]]:
    scripts = []
    for item in lists:
        list_items = item.get("items") or []
        list_items = [f"• {entry}" for entry in list_items]
        padded_values = pad_text([item.get("name", "Unnamed"), *list_items])
        script = []
        for value in padded_values:
            script.append({"opcode": "custom_text", "params": [value]})
        scripts.append(script)
    return scripts


def group_objects(data: list[dict]) -> list[RenderTarget]:
    if not isinstance(data, list):
        if isinstance(data, dict) and "targets" in data:
            raise SystemExit(
                "Expected scratch-json: a top-level list of objects. "
                "Got raw Scratch project.json instead. Run extract.py first."
            )
        if isinstance(data, dict) and "blocks" in data:
            raise SystemExit(
                "Expected scratch-json: a top-level list of objects. "
                "Got raw Scratch sprite/project target JSON instead. Run extract.py first."
            )
        raise SystemExit("Expected scratch-json: a top-level list of objects.")

    grouped: dict[str, dict[str, list]] = {}
    target_order: list[str] = []
    seen_variables: set[tuple[str, str]] = set()
    seen_lists: set[tuple[str, str]] = set()

    for obj in data:
        if not isinstance(obj, dict):
            raise SystemExit("Expected scratch-json top-level list items to be objects")

        obj_type = obj.get("type")
        target = obj.get("target")
        if not isinstance(obj_type, str):
            raise SystemExit("Invalid scratch-json structure. Expected each object to include a string 'type' field.")
        if not isinstance(target, str):
            raise SystemExit("Invalid scratch-json structure. Expected each object to include a string 'target' field.")

        if target not in grouped:
            grouped[target] = {"variables": [], "lists": [], "scripts": []}
            target_order.append(target)

        if obj_type == "script":
            grouped[target]["scripts"].append(validate_script_blocks(obj.get("blocks")))
            continue

        name = obj.get("name")
        if not isinstance(name, str):
            raise SystemExit("Invalid scratch-json structure. Expected variable/list objects to include a string 'name' field.")

        if obj_type == "variable":
            key = (target, name)
            if key in seen_variables:
                raise SystemExit(
                    f"Invalid scratch-json structure. Duplicate variable '{name}' for target '{target}'."
                )
            seen_variables.add(key)
            grouped[target]["variables"].append({"name": name, "value": obj.get("value")})
            continue

        if obj_type == "list":
            items = obj.get("items")
            if not isinstance(items, list):
                raise SystemExit(
                    "Invalid scratch-json structure. Expected list objects to include an 'items' array."
                )
            key = (target, name)
            if key in seen_lists:
                raise SystemExit(
                    f"Invalid scratch-json structure. Duplicate list '{name}' for target '{target}'."
                )
            seen_lists.add(key)
            grouped[target]["lists"].append({"name": name, "items": items})
            continue

        raise SystemExit(f"Invalid scratch-json structure. Unsupported object type '{obj_type}'.")

    targets: list[RenderTarget] = []
    for target in target_order:
        entry = grouped[target]
        if entry["variables"]:
            targets.append(RenderTarget(target, f"{target} Variables", to_variable_scripts(entry["variables"])))
        if entry["lists"]:
            targets.append(RenderTarget(target, f"{target} Lists", to_list_scripts(entry["lists"])))
        targets.append(RenderTarget(target, target, entry["scripts"]))
    return targets


def parse_targets(text: str) -> list[RenderTarget]:
    data = load_scratch_json(text)
    return group_objects(data)


def humanize(opcode: str, params: list | None = None) -> str:
    params = params or []
    if opcode == "custom_text":
        return str(params[0]) if params else ""

    block = BLOCK_CATALOG.get(opcode)
    if not isinstance(block, dict):
        if not params:
            return opcode
        formatted = ", ".join(format_param_value(param) for param in params)
        return f"{opcode} ({formatted})"

    texts = block.get("text")
    if not isinstance(texts, list):
        texts = [opcode]
    param_specs = block.get("params")
    if not isinstance(param_specs, list):
        param_specs = []

    parts: list[str] = []
    count = max(len(texts), len(params), len(param_specs))
    for i in range(count):
        if i < len(texts) and isinstance(texts[i], str) and texts[i]:
            parts.append(texts[i])
        if i < len(params) or i < len(param_specs):
            raw_value = params[i] if i < len(params) else None
            param_spec = param_specs[i] if i < len(param_specs) and isinstance(param_specs[i], dict) else {}
            param_type = str(param_spec.get("type", ""))
            if raw_value is None:
                if "value" in param_spec:
                    raw_value = param_spec["value"]
                elif param_type == "boolean":
                    parts.append("<>")
                    continue
                elif param_type.startswith("dropdown"):
                    parts.append("[ ▼]")
                    continue
                else:
                    parts.append("()")
                    continue
            value = format_param_value(raw_value)
            if isinstance(raw_value, bool) or param_type == "boolean":
                parts.append(f"<{value}>")
            elif param_type.startswith("dropdown"):
                parts.append(f"[{value} ▼]")
            else:
                parts.append(f"({value})")

    return " ".join(parts) if parts else opcode


def format_param_value(value) -> str:
    if isinstance(value, dict) and "opcode" in value:
        return humanize(value["opcode"], value.get("params", []))
    if isinstance(value, dict) and value.get("type") in {"variable", "list", "broadcast"}:
        return str(value["name"])
    return "true" if value is True else "false" if value is False else str(value)


def get_num_branches(block_spec: dict) -> int:
    if not block_spec:
        return 0
    shapes = block_spec.get("shapes")
    if "c-1" in shapes:
        return 1
    elif "c-2" in shapes:
        return 2
    return 0


def flatten_sequence(blocks: list[dict], level: int = 0) -> list[Item]:
    items: list[Item] = []
    for block in blocks:
        text = humanize(block["opcode"], block.get("params", []))
        text = f" {text} "
        width = len(text)
        items.append(Item(width, level, text))

        block_spec = BLOCK_CATALOG.get(block["opcode"])
        nested_blocks = block.get("blocks")
        num_branch = get_num_branches(block_spec)
        if not nested_blocks and num_branch == 0:
            continue
        if not nested_blocks:
            nested_blocks = []
        num_missed_branches = num_branch - len(nested_blocks)
        if num_missed_branches > 0:
            nested_blocks.extend([[] for _ in range(num_missed_branches)])

        nested_level = level + 1
        branch_labels = block_spec.get("branch_labels", []) if block_spec else []
        for i, branch in enumerate(nested_blocks):
            if len(branch) == 0:
                items.append(Item(0, nested_level, ""))
            else:
                items.extend(flatten_sequence(branch, nested_level))
            branch_label = branch_labels[i] if i < len(branch_labels) else None
            label_content = None
            if branch_label:
                pos = branch_label.get("position", "left")
                label_text = branch_label["text"]
                diff = width - len(label_text) - 1
                if label_text and diff > 0:
                    if pos == "left":
                        label_content = " " + label_text + " " * diff
                    else:
                        label_content = " " * diff + label_text + " "
            items.append(Item(width, level, label_content))
    return items


def connector_line(level1: int, width1: int, level2: int, width2: int) -> str:
    if abs(level2 - level1) > 1:
        raise ValueError("levels can only stay the same or move by 1")
    if width1 < 0 or width2 < 0 or (width1 == 0 and width2 == 0):
        raise ValueError("widths must be positive")

    if level1 == 0 and width1 == 0:
        return "┌" + "─" * width2 + "┐"
    elif level2 == 0 and width2 == 0:
        return "└" + "─" * width1 + "┘"

    delta_level = level2 - level1
    num_prefix = 0
    if delta_level == 0:
        num_prefix = level1
    else:
        num_prefix = min(level1, level2) + 1
    prefix = LVL_PREFIX * num_prefix
    real_width1 = width1 + level1 * len(LVL_PREFIX)
    real_width2 = width2 + level2 * len(LVL_PREFIX)

    if delta_level == 1:
        left = "┌"
    elif delta_level == -1:
        left = "└"
    else:
        left = "├"

    if width1 != 0 and real_width1 < real_width2:
        middle = "┴"
    elif width2 != 0 and real_width1 > real_width2:
        middle = "┬"
    else:
        middle = ""

    span1 = "─" * (min(real_width1, real_width2) - len(prefix))
    span2 = "─" * (abs(real_width1 - real_width2) - len(middle))

    if real_width1 < real_width2:
        right = "┐"
    elif real_width1 > real_width2:
        right = "┘"
    else:
        right = "┤"

    return prefix + left + span1 + middle + span2 + right


def content_line(level: int, content: str) -> str:
    prefix = LVL_PREFIX * level
    if content:
        return prefix + "│" + content + "│"
    else:
        return prefix + "│"


def render_items(items: list[Item]) -> list[str]:
    if not items:
        return []
    lines = [connector_line(0, 0, 0, items[0].width)]
    for i, item in enumerate(items):
        if item.content is not None:
            inner = item.content.ljust(max(item.width, 0))
            lines.append(content_line(item.level, inner))
        next_width = (items[i + 1].width) if i + 1 < len(items) else 0
        next_level = items[i + 1].level if i + 1 < len(items) else 0
        lines.append(connector_line(item.level, item.width, next_level, next_width))
    return lines


def render(text: str, targets: list[str] | None = None) -> str:
    out = []
    for target in parse_targets(text):
        if targets and target.owner_name not in targets:
            continue
        out.append(f"# {target.display_name}")
        if not target.scripts or all(not script for script in target.scripts):
            out.extend(["(no scripts)", ""])
            continue
        for script in target.scripts:
            if not script:
                continue
            out.extend([*render_items(flatten_sequence(script)), ""])
    return "\n".join(out).rstrip() + "\n"


if __name__ == "__main__":
    args = parse_args()
    sys.stdout.write(render(read_input(args.file, args.json), args.targets))
