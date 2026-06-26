#!/usr/bin/env python3
"""Skill template generator for Weekend Scout.

Generates platform-specific SKILL.md files from a single template.
Uses #@IF / #@ENDIF directives for conditional blocks and %%VAR%% for substitution.

Usage:
    python skill_template/generate.py                    # all platforms
    python skill_template/generate.py --platform claude-code
    python skill_template/generate.py --dry-run
    python skill_template/generate.py --check
"""

from __future__ import annotations

import argparse
import re
import shutil
import sys
from pathlib import Path

import yaml


SCRIPT_DIR = Path(__file__).resolve().parent
REPO_ROOT = SCRIPT_DIR.parent
PLATFORMS_FILE = SCRIPT_DIR / "platforms.yaml"
TEMPLATE_FILE = SCRIPT_DIR / "weekend-scout.template.md"
RESOURCES_DIR = SCRIPT_DIR / "resources"
TEXT_RESOURCE_EXTENSIONS = {
    ".md",
    ".markdown",
    ".yaml",
    ".yml",
    ".json",
    ".txt",
    ".py",
    ".ps1",
    ".sh",
}

# skill_data/ mirror mapping: platform_id -> subdir inside weekend_scout/skill_data/
SKILL_DATA_TARGETS: dict[str, str] = {
    "claude-code": "weekend_scout/skill_data/claude-code",
    "codex":       "weekend_scout/skill_data/codex",
    "openclaw":    "weekend_scout/skill_data/openclaw",
}


def load_config() -> dict:
    """Load platforms.yaml."""
    with PLATFORMS_FILE.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def load_template() -> str:
    """Load the template file and reject common encoding corruption."""
    template_bytes = TEMPLATE_FILE.read_bytes()
    if template_bytes.startswith(b"\xef\xbb\xbf"):
        raise ValueError(f"{TEMPLATE_FILE} must not start with a UTF-8 BOM")

    template = template_bytes.decode("utf-8")
    mojibake_markers = ("\u0432\u0402", "\u0432\u2020", "\u0413\u2014", "\u0415\u0403")
    found_markers = [marker for marker in mojibake_markers if marker in template]
    if found_markers:
        markers = ", ".join(repr(marker) for marker in found_markers)
        raise ValueError(f"{TEMPLATE_FILE} contains mojibake markers: {markers}")

    return template


def process_directives(template: str, platform_id: str) -> str:
    """Process #@IF / #@ENDIF directives for a given platform.

    Supported forms:
      #@IF platform-id          — include only for this platform
      #@IF platform-a,platform-b — include for either (OR)
      #@IF !platform-id         — include for all platforms EXCEPT this one

    The #@IF and #@ENDIF lines themselves are consumed (not in output).
    Nested #@IF is not supported.

    Args:
        template: Raw template string.
        platform_id: Target platform identifier.

    Returns:
        Template with conditional blocks resolved.
    """
    lines = template.splitlines(keepends=True)
    output: list[str] = []
    inside_block = False
    include_block = False

    for line in lines:
        stripped = line.strip()

        if stripped.startswith("#@IF "):
            condition = stripped[5:].strip()
            if condition.startswith("!"):
                # NOT condition
                excluded = [p.strip() for p in condition[1:].split(",")]
                include_block = platform_id not in excluded
            else:
                # OR condition
                included = [p.strip() for p in condition.split(",")]
                include_block = platform_id in included
            inside_block = True
            # Consume the #@IF line itself
            continue

        if stripped == "#@ENDIF":
            inside_block = False
            include_block = False
            # Consume the #@ENDIF line itself
            continue

        if inside_block:
            if include_block:
                output.append(line)
            # else: drop line (excluded block)
        else:
            output.append(line)

    return "".join(output)


def substitute_vars(text: str, variables: dict[str, str]) -> str:
    """Replace %%VAR_NAME%% placeholders with values from variables dict.

    Args:
        text: Text with %%VAR%% placeholders.
        variables: Mapping of variable name to value.

    Returns:
        Text with all placeholders substituted.

    Raises:
        KeyError: If a %%VAR%% has no matching key in variables.
    """
    def replacer(match: re.Match) -> str:
        name = match.group(1)
        if name not in variables:
            raise KeyError(f"Template variable '%%{name}%%' has no value defined in platforms.yaml")
        return variables[name]

    return re.sub(r"%%([A-Z0-9_]+)%%", replacer, text)


def generate_for_platform(
    platform_id: str,
    platform_cfg: dict,
    shared_vars: dict[str, str],
    template: str,
) -> dict[str, str]:
    """Generate all output files for a single platform.

    Args:
        platform_id: Platform identifier (e.g. 'claude-code').
        platform_cfg: Platform config dict from platforms.yaml.
        shared_vars: Shared variables dict.
        template: Raw template string.

    Returns:
        Dict mapping relative output path -> file content.
    """
    # Merge vars: shared overridden by platform-specific
    variables: dict[str, str] = dict(shared_vars)
    variables.update(platform_cfg.get("vars", {}))

    # Process directives then substitute vars
    processed = process_directives(template, platform_id)
    content = substitute_vars(processed, variables)

    files: dict[str, str] = {"SKILL.md": content}

    for resource_dir in (RESOURCES_DIR / "common", RESOURCES_DIR / platform_id):
        if not resource_dir.exists():
            continue
        for resource_path in sorted(p for p in resource_dir.rglob("*") if p.is_file()):
            rel_path = resource_path.relative_to(resource_dir).as_posix()
            if resource_path.suffix.lower() not in TEXT_RESOURCE_EXTENSIONS:
                raise ValueError(
                    f"Unsupported resource type {resource_path.suffix!r} for {resource_path}"
                )
            resource_text = resource_path.read_text(encoding="utf-8")
            resource_text = process_directives(resource_text, platform_id)
            files[rel_path] = substitute_vars(resource_text, variables)

    # Extra files (e.g. agents/openai.yaml for Codex)
    for rel_path, file_content in platform_cfg.get("extra_files", {}).items():
        files[rel_path] = substitute_vars(file_content, variables)

    return files


def write_files(
    output_dir: Path,
    files: dict[str, str],
    dry_run: bool = False,
) -> None:
    """Write generated files to the output directory.

    Args:
        output_dir: Absolute path to the output directory.
        files: Dict mapping relative path -> content.
        dry_run: If True, print content but do not write.
    """
    for rel_path, content in files.items():
        target = output_dir / rel_path
        if dry_run:
            print(f"\n--- {target} ---")
            print(content)
        else:
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(content, encoding="utf-8")
            print(f"  Written: {target}")


def check_files(
    output_dir: Path,
    files: dict[str, str],
) -> bool:
    """Check if existing files match generated content.

    Args:
        output_dir: Absolute path to the output directory.
        files: Dict mapping relative path -> expected content.

    Returns:
        True if all files are up to date, False if any differ or are missing.
    """
    up_to_date = True
    for rel_path, expected in files.items():
        target = output_dir / rel_path
        if not target.exists():
            print(f"  MISSING: {target}")
            up_to_date = False
            continue
        actual = target.read_text(encoding="utf-8")
        if actual != expected:
            print(f"  OUTDATED: {target}")
            # Show first differing line for quick diagnosis
            for i, (a, b) in enumerate(
                zip(actual.splitlines(), expected.splitlines()), start=1
            ):
                if a != b:
                    print(f"    Line {i}: got    {a!r}")
                    print(f"    Line {i}: expect {b!r}")
                    break
            up_to_date = False
    return up_to_date


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Generate platform-specific SKILL.md files from template."
    )
    parser.add_argument(
        "--platform",
        metavar="NAME",
        help="Generate only for this platform (default: all platforms).",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print generated output without writing files.",
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="Check if generated files are up to date. Exit 1 if not.",
    )
    args = parser.parse_args()

    config = load_config()
    template = load_template()
    shared_vars: dict[str, str] = config.get("shared_vars", {})
    platforms: dict[str, dict] = config.get("platforms", {})

    # Determine target platforms
    if args.platform:
        if args.platform not in platforms:
            print(f"Error: unknown platform '{args.platform}'.", file=sys.stderr)
            print(f"Available: {', '.join(platforms)}", file=sys.stderr)
            sys.exit(1)
        target_platforms = {args.platform: platforms[args.platform]}
    else:
        target_platforms = platforms

    all_ok = True

    for platform_id, platform_cfg in target_platforms.items():
        output_dir = REPO_ROOT / platform_cfg["output_dir"]
        files = generate_for_platform(platform_id, platform_cfg, shared_vars, template)

        if args.check:
            print(f"Checking {platform_id} ({output_dir})...")
            ok = check_files(output_dir, files)
            if ok:
                print("  OK")
            else:
                all_ok = False
        elif args.dry_run:
            print(f"=== Platform: {platform_id} ===")
            write_files(output_dir, files, dry_run=True)
        else:
            print(f"Generating {platform_id} -> {output_dir}")
            write_files(output_dir, files)
            # Mirror into weekend_scout/skill_data/ so the package is self-contained
            if platform_id in SKILL_DATA_TARGETS:
                skill_data_dir = REPO_ROOT / SKILL_DATA_TARGETS[platform_id]
                write_files(skill_data_dir, files)

    if args.check and not all_ok:
        print("\nSome files are out of date. Run: python skill_template/generate.py")
        sys.exit(1)
    elif args.check:
        print("\nAll generated files are up to date.")


if __name__ == "__main__":
    main()
