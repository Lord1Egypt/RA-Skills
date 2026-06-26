from __future__ import annotations

import argparse

from .commands import run_export, run_init_config, run_sanitize, run_scan


def _add_common_repo_arguments(parser: argparse.ArgumentParser) -> None:
    parser.add_argument(
        "--root",
        default=".",
        help="Repository root or any path inside the repository. Defaults to the current directory.",
    )
    parser.add_argument(
        "--config",
        help="Optional path to a .vibe-sanitizer.yml config file.",
    )
    parser.add_argument(
        "--color",
        choices=("auto", "always", "never"),
        default="auto",
        help="Colorize terminal output. Defaults to auto.",
    )


def _add_scope_arguments(parser: argparse.ArgumentParser, *, default_scope: str) -> None:
    parser.add_argument(
        "--scope",
        choices=("working-tree", "tracked", "staged", "commit"),
        default=default_scope,
        help="Git-aware file scope to scan.",
    )
    parser.add_argument(
        "--commit",
        help="Commit SHA to scan when --scope=commit.",
    )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="vibe_sanitizer",
        description="Make AI-generated repos safe to share with Git-aware secret and path sanitization.",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    scan = subparsers.add_parser("scan", help="Scan repository content for sensitive data.")
    _add_common_repo_arguments(scan)
    _add_scope_arguments(scan, default_scope="working-tree")
    scan.add_argument(
        "--format",
        choices=("text", "json"),
        default="text",
        help="Output format.",
    )
    scan.set_defaults(handler=run_scan)

    sanitize = subparsers.add_parser(
        "sanitize",
        help="Apply safe in-place redactions for pre-commit cleanup.",
    )
    _add_common_repo_arguments(sanitize)
    _add_scope_arguments(sanitize, default_scope="working-tree")
    sanitize.add_argument(
        "--mode",
        choices=("in-place", "stdout"),
        default="in-place",
        help="Apply edits in-place or print the sanitized content to stdout.",
    )
    sanitize.set_defaults(handler=run_sanitize)

    export = subparsers.add_parser(
        "export",
        help="Create a separate sanitized shareable copy of the repository.",
    )
    _add_common_repo_arguments(export)
    _add_scope_arguments(export, default_scope="working-tree")
    export.add_argument(
        "--output",
        required=True,
        help="Destination directory for the sanitized copy.",
    )
    export.add_argument(
        "--init-git",
        action="store_true",
        help="Initialize a fresh Git repository in the exported copy.",
    )
    export.set_defaults(handler=run_export)

    init_config = subparsers.add_parser(
        "init-config",
        help="Create a starter .vibe-sanitizer.yml file.",
    )
    init_config.add_argument(
        "--path",
        default=".vibe-sanitizer.yml",
        help="Output path for the config file. Defaults to ./.vibe-sanitizer.yml.",
    )
    init_config.add_argument(
        "--force",
        action="store_true",
        help="Overwrite an existing config file.",
    )
    init_config.add_argument(
        "--color",
        choices=("auto", "always", "never"),
        default="auto",
        help="Colorize terminal output. Defaults to auto.",
    )
    init_config.set_defaults(handler=run_init_config)

    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    return int(args.handler(args))


if __name__ == "__main__":
    raise SystemExit(main())
