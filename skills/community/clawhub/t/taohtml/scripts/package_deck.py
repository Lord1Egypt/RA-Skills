#!/usr/bin/env python3
"""Zip an HTML deck folder for portable delivery."""

from __future__ import annotations

import argparse
import os
import stat
import tempfile
import zipfile
from pathlib import Path


class PackageDeckError(ValueError):
    """Raised when a deck cannot be packaged safely."""


def _is_within(path: Path, root: Path) -> bool:
    try:
        path.relative_to(root)
    except ValueError:
        return False
    return True


def _file_type(mode: int) -> str:
    if stat.S_ISDIR(mode):
        return "directory"
    if stat.S_ISFIFO(mode):
        return "FIFO"
    if stat.S_ISSOCK(mode):
        return "socket"
    if stat.S_ISCHR(mode):
        return "character device"
    if stat.S_ISBLK(mode):
        return "block device"
    return "special file"


def _is_link_like(path: Path, entry_stat: os.stat_result) -> bool:
    if stat.S_ISLNK(entry_stat.st_mode):
        return True
    reparse_point = getattr(stat, "FILE_ATTRIBUTE_REPARSE_POINT", 0)
    file_attributes = getattr(entry_stat, "st_file_attributes", 0)
    if reparse_point and file_attributes & reparse_point:
        return True
    is_junction = getattr(path, "is_junction", None)
    return bool(is_junction and is_junction())


def _inspect_entry(path: Path, deck_root: Path) -> tuple[str, os.stat_result]:
    try:
        entry_stat = path.lstat()
    except OSError as exc:
        raise PackageDeckError(f"Cannot inspect deck entry '{path}': {exc}") from exc

    if _is_link_like(path, entry_stat):
        raise PackageDeckError(
            f"Unsafe deck entry '{path}': symbolic links and junctions are not allowed"
        )

    try:
        resolved = path.resolve(strict=True)
    except (OSError, RuntimeError) as exc:
        raise PackageDeckError(f"Cannot resolve deck entry '{path}': {exc}") from exc
    if not _is_within(resolved, deck_root):
        raise PackageDeckError(
            f"Unsafe deck entry '{path}': resolves outside deck root '{deck_root}'"
        )

    if stat.S_ISDIR(entry_stat.st_mode):
        return "directory", entry_stat
    if stat.S_ISREG(entry_stat.st_mode):
        return "file", entry_stat
    raise PackageDeckError(
        f"Unsafe deck entry '{path}': {_file_type(entry_stat.st_mode)} is not "
        "a regular file or directory"
    )


def _resolve_deck_root(deck_dir: Path) -> tuple[Path, os.stat_result]:
    try:
        deck_stat = deck_dir.lstat()
    except OSError as exc:
        raise PackageDeckError(f"Cannot inspect deck directory '{deck_dir}': {exc}") from exc
    if _is_link_like(deck_dir, deck_stat):
        raise PackageDeckError(
            f"Unsafe deck directory '{deck_dir}': symbolic links and junctions are not allowed"
        )
    if not stat.S_ISDIR(deck_stat.st_mode):
        raise PackageDeckError(f"Not a directory: {deck_dir}")
    try:
        return deck_dir.resolve(strict=True), deck_stat
    except (OSError, RuntimeError) as exc:
        raise PackageDeckError(f"Cannot resolve deck directory '{deck_dir}': {exc}") from exc


def _validate_output_path(
    zip_path: Path, deck_root: Path
) -> tuple[Path, os.stat_result | None]:
    try:
        output_stat = zip_path.lstat()
    except FileNotFoundError:
        output_stat = None
    except OSError as exc:
        raise PackageDeckError(f"Cannot inspect output archive '{zip_path}': {exc}") from exc
    if output_stat is not None:
        if _is_link_like(zip_path, output_stat):
            raise PackageDeckError(
                f"Unsafe output archive '{zip_path}': symbolic links and junctions are not allowed"
            )
        if not stat.S_ISREG(output_stat.st_mode):
            raise PackageDeckError(
                f"Unsafe output archive '{zip_path}': {_file_type(output_stat.st_mode)} "
                "is not a regular file"
            )
    try:
        resolved_output = zip_path.resolve(strict=False)
    except (OSError, RuntimeError) as exc:
        raise PackageDeckError(f"Cannot resolve output archive '{zip_path}': {exc}") from exc
    if _is_within(resolved_output, deck_root):
        raise PackageDeckError(
            f"Unsafe output archive '{zip_path}': output resolves inside deck root "
            f"'{deck_root}'; choose a path outside the deck directory"
        )
    return resolved_output, output_stat


def _collect_deck_files(deck_root: Path, root_stat: os.stat_result) -> list[Path]:
    files: list[Path] = []
    pending = [deck_root]
    seen_directories = {(root_stat.st_dev, root_stat.st_ino)}

    while pending:
        directory = pending.pop()
        try:
            with os.scandir(directory) as entries:
                children = sorted(entries, key=lambda entry: entry.name, reverse=True)
        except OSError as exc:
            raise PackageDeckError(f"Cannot scan deck directory '{directory}': {exc}") from exc

        for entry in children:
            path = Path(entry.path)
            kind, entry_stat = _inspect_entry(path, deck_root)
            if kind == "directory":
                identity = (entry_stat.st_dev, entry_stat.st_ino)
                if identity in seen_directories:
                    raise PackageDeckError(
                        f"Unsafe deck entry '{path}': repeated directory or directory cycle"
                    )
                seen_directories.add(identity)
                pending.append(path)
            else:
                files.append(path)

    return sorted(files, key=lambda path: path.relative_to(deck_root).as_posix())


def _revalidate_file(path: Path, deck_root: Path) -> None:
    kind, _ = _inspect_entry(path, deck_root)
    if kind != "file":
        raise PackageDeckError(
            f"Unsafe deck entry '{path}': file changed after the preflight scan"
        )


def _write_archive(files: list[Path], deck_root: Path, output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temporary_name = tempfile.mkstemp(
        prefix=f".{output_path.name}.",
        suffix=".tmp",
        dir=output_path.parent,
    )
    temporary_path = Path(temporary_name)

    try:
        with os.fdopen(descriptor, "w+b") as temporary_file:
            with zipfile.ZipFile(
                temporary_file, "w", compression=zipfile.ZIP_DEFLATED
            ) as archive:
                for path in files:
                    _revalidate_file(path, deck_root)
                    relative = path.relative_to(deck_root)
                    archive.write(path, (Path(deck_root.name) / relative).as_posix())
        os.replace(temporary_path, output_path)
    finally:
        try:
            temporary_path.unlink()
        except FileNotFoundError:
            pass


def package_deck(deck_dir: Path, zip_path: Path) -> Path:
    deck_root, root_stat = _resolve_deck_root(deck_dir)
    output_path, output_stat = _validate_output_path(zip_path, deck_root)
    files = _collect_deck_files(deck_root, root_stat)
    index_path = deck_root / "index.html"
    if index_path not in files:
        raise PackageDeckError(f"index.html not found as a regular file in: {deck_root}")
    if output_stat is not None:
        output_identity = (output_stat.st_dev, output_stat.st_ino)
        for path in files:
            source_stat = path.lstat()
            if (source_stat.st_dev, source_stat.st_ino) == output_identity:
                raise PackageDeckError(
                    f"Unsafe output archive '{zip_path}': aliases deck file '{path}'"
                )

    _write_archive(files, deck_root, output_path)
    return output_path


def main() -> int:
    parser = argparse.ArgumentParser(description="Create a portable zip for an HTML deck folder.")
    parser.add_argument("deck_dir", type=Path, help="Folder containing index.html and assets.")
    parser.add_argument("zip_path", type=Path, help="Output zip path.")
    args = parser.parse_args()

    try:
        package_deck(args.deck_dir, args.zip_path)
    except (OSError, PackageDeckError, zipfile.BadZipFile) as exc:
        raise SystemExit(str(exc)) from None

    print(args.zip_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
