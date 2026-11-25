#!/usr/bin/env python3
"""Inventory approved local evidence folders for Resume Intelligence.

The helper only records source coverage. It does not decide final resume claims.
"""

import argparse
import os
from dataclasses import dataclass
from pathlib import Path


TEXT_EXTENSIONS = {
    ".adoc",
    ".csv",
    ".html",
    ".json",
    ".log",
    ".md",
    ".rst",
    ".txt",
    ".xml",
    ".yaml",
    ".yml",
}

DOCUMENT_EXTENSIONS = {".docx", ".pdf"}

BINARY_EXTENSIONS = {
    ".avif",
    ".bin",
    ".gif",
    ".heic",
    ".ico",
    ".jpeg",
    ".jpg",
    ".mov",
    ".mp4",
    ".pages",
    ".png",
    ".ppt",
    ".pptx",
    ".webp",
    ".xls",
    ".xlsx",
    ".zip",
}

SKIPPED_DIRECTORIES = {".git", ".hg", ".svn", "__pycache__"}


@dataclass(frozen=True)
class InventoryRow:
    relative_path: str
    extension: str
    status: str
    extraction_method: str
    size_bytes: int
    modified_time: str
    notes: str


def format_mtime(path: Path) -> str:
    return str(int(path.stat().st_mtime))


def has_binary_marker(path: Path) -> bool:
    try:
        with path.open("rb") as source:
            return b"\x00" in source.read(4096)
    except OSError:
        return False


def relative_inventory_path(root: Path, path: Path) -> str:
    try:
        return path.relative_to(Path.cwd().resolve()).as_posix()
    except ValueError:
        return path.relative_to(root).as_posix()


def classify_file(root: Path, path: Path) -> InventoryRow:
    relative_path = relative_inventory_path(root, path)
    extension = path.suffix.lower()

    try:
        size_bytes = path.stat().st_size
        modified_time = format_mtime(path)
    except OSError as exc:
        return InventoryRow(
            relative_path=relative_path,
            extension=extension,
            status="skipped-permission",
            extraction_method="none",
            size_bytes=0,
            modified_time="unknown",
            notes=f"stat failed: {exc.__class__.__name__}",
        )

    if extension in BINARY_EXTENSIONS or has_binary_marker(path):
        return InventoryRow(
            relative_path=relative_path,
            extension=extension,
            status="skipped-binary",
            extraction_method="none",
            size_bytes=size_bytes,
            modified_time=modified_time,
            notes="binary or media file",
        )

    if extension in TEXT_EXTENSIONS:
        return InventoryRow(
            relative_path=relative_path,
            extension=extension,
            status="scanned",
            extraction_method="direct-read",
            size_bytes=size_bytes,
            modified_time=modified_time,
            notes="text-oriented file ready for evidence review",
        )

    if extension in DOCUMENT_EXTENSIONS:
        return InventoryRow(
            relative_path=relative_path,
            extension=extension,
            status="needs-user-input",
            extraction_method="external-parser-required",
            size_bytes=size_bytes,
            modified_time=modified_time,
            notes="use DOCX/PDF tooling or ask user for converted text",
        )

    return InventoryRow(
        relative_path=relative_path,
        extension=extension,
        status="skipped-unsupported-format",
        extraction_method="none",
        size_bytes=size_bytes,
        modified_time=modified_time,
        notes="unsupported extension for first-pass inventory",
    )


def inventory_root(root: Path) -> list[InventoryRow]:
    root = root.expanduser().resolve()
    if not root.exists():
        raise FileNotFoundError(f"approved root does not exist: {root}")
    if not root.is_dir():
        raise NotADirectoryError(f"approved root is not a directory: {root}")

    rows: list[InventoryRow] = []
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = sorted(name for name in dirnames if name not in SKIPPED_DIRECTORIES)
        for filename in sorted(filenames):
            path = Path(dirpath) / filename
            rows.append(classify_file(root, path))
    return rows


def markdown_escape(value: object) -> str:
    return str(value).replace("|", "\\|").replace("\n", " ")


def render_markdown(root: Path, rows: list[InventoryRow], command: str) -> str:
    counts: dict[str, int] = {}
    for row in rows:
        counts[row.status] = counts.get(row.status, 0) + 1

    lines = [
        "# Source Inventory",
        "",
        "## Inventory Summary",
        "",
        f"- Approved root: `{root.expanduser().resolve()}`",
        f"- Inventory command: `{command}`",
        f"- Total files: {len(rows)}",
    ]
    for status in sorted(counts):
        lines.append(f"- {status}: {counts[status]}")

    lines.extend(
        [
            "",
            "## Files",
            "",
            "| Relative Path | Extension | Status | Extraction Method | Size Bytes | Modified Time | Notes |",
            "| --- | --- | --- | --- | ---: | --- | --- |",
        ]
    )
    for row in rows:
        lines.append(
            "| "
            + " | ".join(
                [
                    markdown_escape(row.relative_path),
                    markdown_escape(row.extension),
                    markdown_escape(row.status),
                    markdown_escape(row.extraction_method),
                    markdown_escape(row.size_bytes),
                    markdown_escape(row.modified_time),
                    markdown_escape(row.notes),
                ]
            )
            + " |"
        )
    lines.append("")
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(description="Create a recursive source inventory markdown file.")
    parser.add_argument("root", help="Approved local evidence folder to inventory.")
    parser.add_argument("--output", help="Markdown output path. Prints to stdout when omitted.")
    args = parser.parse_args()

    root = Path(args.root)
    command_parts = ["inventory_sources.py", args.root]
    if args.output:
        command_parts.extend(["--output", args.output])

    rows = inventory_root(root)
    markdown = render_markdown(root, rows, command=" ".join(command_parts))

    if args.output:
        output = Path(args.output)
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(markdown, encoding="utf-8")
    else:
        print(markdown)


if __name__ == "__main__":
    main()
