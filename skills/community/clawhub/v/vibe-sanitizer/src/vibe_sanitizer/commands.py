from __future__ import annotations

import shutil
import sys
from pathlib import Path

from .colors import BOLD, CYAN, GREEN, RED, YELLOW, colorize, use_color
from .config import load_config, write_default_config
from .constants import EXIT_ERROR, EXIT_FINDINGS, EXIT_OK
from .errors import VibeSanitizerError
from .filesystem import read_text_candidate
from .formatters import format_scan_report
from .git import initialize_new_repo, resolve_repo_root, resolve_scope_files
from .redaction import apply_replacements, findings_by_path
from .scanner import ScanEngine


def run_scan(args: object) -> int:
    colored = use_color(getattr(args, "color", "auto"))
    try:
        report = _scan_from_args(args)
    except VibeSanitizerError as exc:
        print(_error_text(str(exc), enabled=colored), file=sys.stderr)
        return EXIT_ERROR

    print(
        format_scan_report(
            report,
            getattr(args, "format", "text"),
            color_mode=getattr(args, "color", "auto"),
        )
    )
    return EXIT_FINDINGS if report.findings else EXIT_OK


def run_sanitize(args: object) -> int:
    colored = use_color(getattr(args, "color", "auto"))
    try:
        report = _scan_from_args(args)
    except VibeSanitizerError as exc:
        print(_error_text(str(exc), enabled=colored), file=sys.stderr)
        return EXIT_ERROR

    if not report.findings:
        print(colorize("No findings detected. Nothing to sanitize.", GREEN, enabled=colored))
        return EXIT_OK

    root = report.root
    grouped = findings_by_path(report.findings)

    if args.mode == "stdout":
        for relative_path in sorted(grouped):
            source_path = root / relative_path
            original = read_text_candidate(source_path)
            if original is None:
                continue
            sanitized = apply_replacements(original, grouped[relative_path], in_place_only=True)
            print(colorize(f"===== {relative_path} =====", BOLD, CYAN, enabled=colored))
            print(sanitized)
        return EXIT_FINDINGS if report.review_required_findings else EXIT_OK

    modified_files = 0
    for relative_path, path_findings in grouped.items():
        if not any(finding.editable_in_place for finding in path_findings):
            continue
        source_path = root / relative_path
        original = read_text_candidate(source_path)
        if original is None:
            continue
        sanitized = apply_replacements(original, path_findings, in_place_only=True)
        if sanitized == original:
            continue
        source_path.write_text(sanitized, encoding="utf-8")
        modified_files += 1

    print(f"{colorize('Modified files:', BOLD, CYAN, enabled=colored)} {colorize(str(modified_files), GREEN, enabled=colored)}")
    print(
        f"{colorize('Review-required findings left unchanged:', BOLD, CYAN, enabled=colored)} "
        f"{colorize(str(report.review_required_findings), YELLOW, enabled=colored)}"
    )
    if getattr(args, "scope", "") == "staged" and modified_files:
        print(colorize("Note: re-stage modified files before committing.", YELLOW, enabled=colored))

    return EXIT_FINDINGS if report.review_required_findings else EXIT_OK


def run_export(args: object) -> int:
    colored = use_color(getattr(args, "color", "auto"))
    try:
        report = _scan_from_args(args)
        output_dir = Path(args.output).expanduser().resolve()
        _validate_export_destination(report.root, output_dir)
    except VibeSanitizerError as exc:
        print(_error_text(str(exc), enabled=colored), file=sys.stderr)
        return EXIT_ERROR

    grouped = findings_by_path(report.findings)
    selected_paths = resolve_scope_files(report.root, args.scope, getattr(args, "commit", None))

    output_dir.mkdir(parents=True, exist_ok=False)
    for source_path in selected_paths:
        relative_path = source_path.relative_to(report.root)
        destination = output_dir / relative_path
        destination.parent.mkdir(parents=True, exist_ok=True)

        original = read_text_candidate(source_path)
        if original is None:
            shutil.copy2(source_path, destination)
            continue

        if str(relative_path) in grouped:
            shutil.copy2(source_path, destination)
            destination.write_text(
                apply_replacements(original, grouped[str(relative_path)], in_place_only=False),
                encoding="utf-8",
            )
        else:
            shutil.copy2(source_path, destination)

    if args.init_git:
        initialize_new_repo(output_dir)

    print(
        f"{colorize('Exported sanitized copy to', BOLD, GREEN, enabled=colored)} "
        f"{output_dir}"
    )
    print(f"{colorize('Files scanned:', BOLD, CYAN, enabled=colored)} {report.files_scanned}")
    print(
        f"{colorize('Findings redacted in export:', BOLD, CYAN, enabled=colored)} "
        f"{colorize(str(report.total_findings), GREEN, enabled=colored)}"
    )
    if args.init_git:
        print(colorize("Initialized a fresh Git repository in the export.", GREEN, enabled=colored))
    return EXIT_OK


def run_init_config(args: object) -> int:
    colored = use_color(getattr(args, "color", "auto"))
    try:
        created = write_default_config(Path(args.path).expanduser(), force=bool(args.force))
    except VibeSanitizerError as exc:
        print(_error_text(str(exc), enabled=colored), file=sys.stderr)
        return EXIT_ERROR

    print(f"{colorize('Created config at', BOLD, GREEN, enabled=colored)} {created}")
    return EXIT_OK


def _scan_from_args(args: object):
    repo_root = resolve_repo_root(Path(args.root))
    config = load_config(repo_root, getattr(args, "config", None))
    selected_paths = resolve_scope_files(repo_root, args.scope, getattr(args, "commit", None))
    engine = ScanEngine(repo_root, config)
    return engine.scan_paths(selected_paths, args.scope)


def _validate_export_destination(repo_root: Path, output_dir: Path) -> None:
    if output_dir.exists():
        raise VibeSanitizerError(f"Export destination already exists: {output_dir}")
    try:
        output_dir.relative_to(repo_root)
    except ValueError:
        return
    raise VibeSanitizerError(
        "Export destination must be outside the source repository. Use a sibling path such as ../safe-share."
    )


def _error_text(message: str, *, enabled: bool) -> str:
    return f"{colorize('Error:', BOLD, RED, enabled=enabled)} {message}"
