#!/usr/bin/env python3
"""Render an isolated prompt package for the Twin Reply workflow."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


REQUIRED_PERSONA_FILES = [
    "profile.md",
    "persona_examples.md",
    "guardrails.md",
]

OPTIONAL_PERSONA_FILES = [
    "state.md",
]

TEMPLATE_FILE_NAME = "clone_prompt_template.md"


def default_persona_dir() -> Path:
    return Path(__file__).resolve().parent.parent.parent.parent / "ai_twin"


def default_template_path() -> Path:
    return Path(__file__).resolve().parent.parent / "assets" / TEMPLATE_FILE_NAME


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Combine persona markdown and runtime context into one prompt.",
    )
    parser.add_argument(
        "--persona-dir",
        default=str(default_persona_dir()),
        help="Directory containing persona markdown files (default: repo-root/ai_twin)",
    )
    parser.add_argument(
        "--scene",
        required=True,
        help="Markdown or text file describing the current scene",
    )
    parser.add_argument(
        "--dialogue",
        required=True,
        help="Markdown or text file containing the active dialogue window",
    )
    parser.add_argument(
        "--extra-context",
        action="append",
        default=[],
        help="Additional markdown or text files to append as runtime context",
    )
    parser.add_argument(
        "--output",
        help="Write the rendered prompt to this path instead of stdout",
    )
    parser.add_argument(
        "--template",
        default=str(default_template_path()),
        help="Markdown template for the isolated prompt",
    )
    return parser.parse_args()


def read_text(path_str: str) -> str:
    path = Path(path_str).expanduser().resolve()
    if not path.is_file():
        raise FileNotFoundError(f"File not found: {path}")
    return path.read_text(encoding="utf-8").strip()


def load_persona_sections(
    persona_dir: Path,
    excluded_names: set[str],
) -> list[tuple[str, str]]:
    sections: list[tuple[str, str]] = []

    for name in ["profile.md", "state.md", "persona_examples.md", "guardrails.md"]:
        path = persona_dir / name
        if name in REQUIRED_PERSONA_FILES and not path.is_file():
            raise FileNotFoundError(f"Missing required persona file: {path}")
        if path.is_file():
            sections.append((name, path.read_text(encoding="utf-8").strip()))

    known_names = set(REQUIRED_PERSONA_FILES) | set(OPTIONAL_PERSONA_FILES)
    extras = sorted(
        path
        for path in persona_dir.glob("*.md")
        if path.name not in known_names and path.name not in excluded_names
    )
    for path in extras:
        sections.append((path.name, path.read_text(encoding="utf-8").strip()))

    return sections


def format_section(title: str, body: str) -> str:
    return f"## {title}\n\n{body}".strip()


def render_template(template_text: str, replacements: dict[str, str]) -> str:
    rendered = template_text
    for key, value in replacements.items():
        rendered = rendered.replace(f"{{{{{key}}}}}", value)
    return rendered


def build_prompt(
    template_text: str,
    persona_sections: list[tuple[str, str]],
    scene_text: str,
    dialogue_text: str,
    extra_sections: list[tuple[str, str]],
) -> str:
    persona_text = "\n\n".join(
        format_section(f"Persona File: {name}", body)
        for name, body in persona_sections
    ).strip()
    extra_text = "\n\n".join(
        format_section(f"Extra Context: {name}", body)
        for name, body in extra_sections
    ).strip()

    prompt = render_template(
        template_text,
        {
            "PERSONA_SECTIONS": persona_text,
            "SCENE_TEXT": scene_text,
            "DIALOGUE_TEXT": dialogue_text,
            "EXTRA_SECTIONS": extra_text,
        },
    )
    return re.sub(r"\n{3,}", "\n\n", prompt).strip() + "\n"


def main() -> int:
    args = parse_args()
    persona_dir = Path(args.persona_dir).expanduser().resolve()
    template_path = Path(args.template).expanduser().resolve()
    if not persona_dir.is_dir():
        print(f"[ERROR] Persona directory not found: {persona_dir}", file=sys.stderr)
        return 1
    if not template_path.is_file():
        print(f"[ERROR] Template file not found: {template_path}", file=sys.stderr)
        return 1

    try:
        excluded_names = {
            Path(args.scene).name,
            Path(args.dialogue).name,
            *(Path(item).name for item in args.extra_context),
        }
        template_text = template_path.read_text(encoding="utf-8").strip()
        persona_sections = load_persona_sections(persona_dir, excluded_names)
        scene_text = read_text(args.scene)
        dialogue_text = read_text(args.dialogue)
        extra_sections = []
        for item in args.extra_context:
            path = Path(item).expanduser().resolve()
            extra_sections.append((path.name, read_text(item)))
    except FileNotFoundError as exc:
        print(f"[ERROR] {exc}", file=sys.stderr)
        return 1

    prompt = build_prompt(
        template_text,
        persona_sections,
        scene_text,
        dialogue_text,
        extra_sections,
    )

    if args.output:
        target = Path(args.output).expanduser().resolve()
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(prompt, encoding="utf-8")
    else:
        sys.stdout.write(prompt)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
