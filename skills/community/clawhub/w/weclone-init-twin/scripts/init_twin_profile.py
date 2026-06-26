#!/usr/bin/env python3
"""Initialize a persona directory from bundled markdown templates."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path


TEMPLATE_NAMES = [
    "profile.md",
    "state.md",
    "persona_examples.md",
    "guardrails.md",
]

LANGUAGE_ALIASES = {
    "en": "en",
    "english": "en",
    "zh": "zh",
    "zh-cn": "zh",
    "zh-hans": "zh",
    "chinese": "zh",
}


def default_persona_dir() -> Path:
    return Path(__file__).resolve().parent.parent.parent.parent / "ai_twin"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Create a persona directory for weclone-init-twin.",
    )
    parser.add_argument(
        "output_dir",
        nargs="?",
        default=str(default_persona_dir()),
        help="Directory to create or populate (default: repo-root/ai_twin)",
    )
    parser.add_argument(
        "--user-name",
        default="User",
        help="Replace the template placeholder with this name",
    )
    parser.add_argument(
        "--language",
        default="en",
        help="Template language: en or zh (default: en)",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Overwrite existing target files",
    )
    return parser.parse_args()


def template_dir() -> Path:
    return Path(__file__).resolve().parent.parent / "assets" / "persona-pack"


def normalize_language(language: str) -> str:
    normalized = LANGUAGE_ALIASES.get(language.strip().lower())
    if normalized is None:
        supported = ", ".join(sorted(set(LANGUAGE_ALIASES.values())))
        raise ValueError(
            f"Unsupported language '{language}'. Supported values: {supported}"
        )
    return normalized


def template_path(base_dir: Path, template_name: str, language: str) -> Path:
    if language == "en":
        return base_dir / template_name

    localized_name = template_name.replace(".md", f".{language}.md")
    return base_dir / localized_name


def render_template(source: Path, user_name: str) -> str:
    return source.read_text(encoding="utf-8").replace("{{USER_NAME}}", user_name)


def validate_targets(output_dir: Path, force: bool) -> None:
    conflicts = []
    for name in TEMPLATE_NAMES:
        target = output_dir / name
        if target.exists() and not force:
            conflicts.append(str(target))
    if conflicts:
        joined = "\n".join(f"- {item}" for item in conflicts)
        raise FileExistsError(
            "Refusing to overwrite existing files without --force:\n"
            f"{joined}"
        )


def main() -> int:
    args = parse_args()
    out_dir = Path(args.output_dir).expanduser().resolve()
    source_dir = template_dir()
    try:
        language = normalize_language(args.language)
    except ValueError as exc:
        print(f"[ERROR] {exc}", file=sys.stderr)
        return 1

    if not source_dir.is_dir():
        print(f"[ERROR] Template directory not found: {source_dir}", file=sys.stderr)
        return 1

    out_dir.mkdir(parents=True, exist_ok=True)

    try:
        validate_targets(out_dir, args.force)
    except FileExistsError as exc:
        print(f"[ERROR] {exc}", file=sys.stderr)
        return 1

    for name in TEMPLATE_NAMES:
        source = template_path(source_dir, name, language)
        if not source.is_file():
            print(f"[ERROR] Missing template: {source}", file=sys.stderr)
            return 1
        target = out_dir / name
        target.write_text(render_template(source, args.user_name), encoding="utf-8")
        print(f"[OK] Wrote {target}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
