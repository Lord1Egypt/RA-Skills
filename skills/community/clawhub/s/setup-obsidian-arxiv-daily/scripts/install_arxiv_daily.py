import argparse
import os
import re
import shutil
import stat
import sys
from dataclasses import dataclass
from pathlib import Path


RUNTIME_DIRECTORIES = ("papers", "daily", "archive", "logs")
INVALID_PROJECT_NAME = re.compile(r'[<>:"/\\|?*\x00-\x1f]')


@dataclass(frozen=True)
class InstallResult:
    destination: Path
    files: tuple[Path, ...]
    runtime_directories: tuple[Path, ...]
    dry_run: bool


def _is_redirect(path: Path) -> bool:
    if path.is_symlink():
        return True
    try:
        return bool(
            getattr(os.lstat(path), "st_file_attributes", 0)
            & stat.FILE_ATTRIBUTE_REPARSE_POINT
        )
    except (FileNotFoundError, OSError):
        return False


def _validate_project_name(project_name: str) -> str:
    if (
        not project_name
        or project_name != project_name.strip()
        or project_name in {".", ".."}
        or INVALID_PROJECT_NAME.search(project_name)
        or Path(project_name).name != project_name
    ):
        raise ValueError(f"Invalid project name: {project_name!r}")
    return project_name


def _asset_root() -> Path:
    return Path(__file__).resolve().parent.parent / "assets" / "arxiv-daily"


def _asset_files(source_root: Path) -> tuple[Path, ...]:
    resolved_root = source_root.resolve(strict=True)
    files: list[Path] = []
    for current_dir, dirnames, filenames in os.walk(
        source_root,
        topdown=True,
        followlinks=False,
    ):
        current_path = Path(current_dir)
        dirnames[:] = [
            dirname
            for dirname in dirnames
            if dirname != "__pycache__"
            and not (
                current_path == source_root
                and dirname in RUNTIME_DIRECTORIES
            )
        ]
        for dirname in dirnames:
            child = current_path / dirname
            if _is_redirect(child):
                raise ValueError(f"Redirected asset directory is not allowed: {child}")
        for filename in filenames:
            if filename.lower().endswith(".pyc"):
                continue
            child = current_path / filename
            if _is_redirect(child):
                raise ValueError(f"Redirected asset file is not allowed: {child}")
            if not child.resolve(strict=True).is_relative_to(resolved_root):
                raise ValueError(f"Asset escapes package root: {child}")
            files.append(child.relative_to(source_root))
    return tuple(sorted(files, key=lambda path: path.as_posix()))


def _write_asset(source: Path, destination: Path, project_name: str) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    if source.suffix.lower() == ".md":
        text = source.read_text(encoding="utf-8")
        text = text.replace("arxiv-daily/", f"{project_name}/")
        text = text.replace(
            ".\\arxiv-daily\\",
            f".\\{project_name}\\",
        )
        destination.write_text(text, encoding="utf-8", newline="\n")
        return
    shutil.copy2(source, destination)


def install(
    vault: Path,
    project_name: str = "arxiv-daily",
    dry_run: bool = False,
    force: bool = False,
) -> InstallResult:
    project_name = _validate_project_name(project_name)
    vault = Path(vault)
    if not vault.exists():
        raise FileNotFoundError(f"Vault does not exist: {vault}")
    if not vault.is_dir():
        raise NotADirectoryError(f"Vault is not a directory: {vault}")

    vault = vault.resolve(strict=True)
    source_root = _asset_root()
    if not source_root.is_dir():
        raise FileNotFoundError(f"Packaged assets are missing: {source_root}")
    files = _asset_files(source_root)

    destination = vault / project_name
    if destination.exists() and _is_redirect(destination):
        raise ValueError(f"Destination is a redirected directory: {destination}")
    if not destination.resolve(strict=False).is_relative_to(vault):
        raise ValueError(f"Destination escapes Vault: {destination}")
    if destination.exists() and not destination.is_dir():
        raise FileExistsError(f"Destination is not a directory: {destination}")
    if destination.exists() and not force:
        raise FileExistsError(
            f"Destination already exists: {destination}. Use --force to update it."
        )

    runtime_paths = tuple(Path(name) for name in RUNTIME_DIRECTORIES)
    result = InstallResult(
        destination=destination.resolve(strict=False),
        files=files,
        runtime_directories=runtime_paths,
        dry_run=dry_run,
    )
    if dry_run:
        return result

    destination.mkdir(parents=True, exist_ok=True)
    for relative_path in files:
        target = destination / relative_path
        if not target.resolve(strict=False).is_relative_to(destination.resolve()):
            raise ValueError(f"Asset destination escapes project: {target}")
        _write_asset(source_root / relative_path, target, project_name)
    for relative_path in runtime_paths:
        (destination / relative_path).mkdir(parents=True, exist_ok=True)
    return result


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Install the packaged Obsidian arXiv daily workflow.",
    )
    parser.add_argument("--vault", required=True, type=Path)
    parser.add_argument("--project-name", default="arxiv-daily")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--force", action="store_true")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    try:
        result = install(
            vault=args.vault,
            project_name=args.project_name,
            dry_run=args.dry_run,
            force=args.force,
        )
    except Exception as exc:
        print(f"Install failed: {exc}", file=sys.stderr)
        return 1

    mode = "Preview" if result.dry_run else "Installed"
    print(f"{mode}: {result.destination}")
    for path in result.files:
        print(f"- file: {path.as_posix()}")
    for path in result.runtime_directories:
        print(f"- runtime directory: {path.as_posix()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
