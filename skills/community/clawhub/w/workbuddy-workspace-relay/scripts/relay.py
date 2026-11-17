#!/usr/bin/env python3
"""Deterministic pack/restore engine for the WorkBuddy Workspace Relay skill.

The script owns file selection, archive validation, hashing, and the age
encryption boundary. WorkBuddy owns the semantic HANDOFF content and invokes
this script with an explicit mode.
"""

from __future__ import annotations

import argparse
import getpass
import hashlib
import json
import os
import platform
import re
import select
import shutil
import stat
import subprocess
import sys
import tarfile
import tempfile
import time
from pathlib import Path, PurePosixPath
from typing import Any, Iterable


FORMAT_VERSION = "0.1"
PACKAGE_SUFFIX = ".wbpack"
METADATA_DIR = ".workbuddy-relay"
CHUNK_SIZE = 1024 * 1024
AGE_TIMEOUT_SECONDS = 300

EXCLUDED_DIRS = frozenset(
    {
        ".cache",
        ".pytest_cache",
        ".mypy_cache",
        ".ruff_cache",
        "__pycache__",
        ".venv",
        "venv",
        "node_modules",
        "dist",
        "build",
        "target",
        "coverage",
        ".workbuddy-relay",
    }
)
EXCLUDED_FILENAMES = frozenset({".DS_Store", "Thumbs.db"})
EXCLUDED_SUFFIXES = (".log", ".tmp", ".temp", ".wbpack", ".wbpack.part")


class RelayError(RuntimeError):
    """Expected user-facing failure without a traceback or secret material."""


def _json_dump(path: Path, value: Any) -> None:
    path.write_text(
        json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        while True:
            chunk = handle.read(CHUNK_SIZE)
            if not chunk:
                break
            digest.update(chunk)
    return digest.hexdigest()


def _is_within(path: Path, parent: Path) -> bool:
    try:
        path.resolve(strict=False).relative_to(parent.resolve(strict=False))
        return True
    except ValueError:
        return False


def _lexists(path: Path) -> bool:
    return os.path.lexists(os.fspath(path))


def _safe_project_name(name: str) -> str:
    cleaned = re.sub(r"[^\w.\-\u4e00-\u9fff]+", "-", name, flags=re.UNICODE)
    cleaned = cleaned.strip(".-")
    return cleaned or "workspace"


def _workspace_name(workspace: Path) -> str:
    return _safe_project_name(workspace.name or "workspace")


def _is_excluded(relative: Path) -> bool:
    parts = relative.parts
    if any(part in EXCLUDED_DIRS for part in parts):
        return True
    filename = relative.name
    if filename in EXCLUDED_FILENAMES:
        return True
    if filename.endswith(EXCLUDED_SUFFIXES):
        return True
    if filename.startswith("~$"):
        return True
    return False


def _scan_workspace(workspace: Path) -> tuple[list[Path], list[Path], int]:
    files: list[Path] = []
    directories: list[Path] = []
    skipped_symlinks = 0

    for root, dirnames, filenames in os.walk(
        workspace, topdown=True, followlinks=False
    ):
        root_path = Path(root)
        kept_dirs: list[str] = []
        for dirname in sorted(dirnames):
            candidate = root_path / dirname
            relative = candidate.relative_to(workspace)
            if candidate.is_symlink():
                skipped_symlinks += 1
                continue
            if _is_excluded(relative):
                continue
            kept_dirs.append(dirname)
            directories.append(relative)
        dirnames[:] = kept_dirs

        for filename in sorted(filenames):
            candidate = root_path / filename
            relative = candidate.relative_to(workspace)
            if candidate.is_symlink():
                skipped_symlinks += 1
                continue
            if _is_excluded(relative):
                continue
            if not candidate.is_file():
                continue
            files.append(candidate)

    return files, directories, skipped_symlinks


def _copy_file(src: Path, dst: Path) -> None:
    dst.parent.mkdir(parents=True, exist_ok=True)
    with src.open("rb") as source, dst.open("wb") as target:
        while True:
            chunk = source.read(CHUNK_SIZE)
            if not chunk:
                break
            target.write(chunk)
    try:
        shutil.copystat(src, dst, follow_symlinks=False)
    except OSError:
        # Windows can reject some source metadata. Content remains authoritative.
        pass


def _git_branch(workspace: Path) -> str | None:
    try:
        result = subprocess.run(
            ["git", "-C", os.fspath(workspace), "branch", "--show-current"],
            check=False,
            capture_output=True,
            text=True,
            timeout=5,
        )
    except (OSError, subprocess.SubprocessError):
        return None
    branch = result.stdout.strip()
    return branch or None


def _runtime_info(workspace: Path) -> dict[str, Any]:
    available_tools = [
        tool
        for tool in ("python", "node", "npm", "pnpm", "yarn", "uv", "cargo", "go")
        if shutil.which(tool)
    ]
    return {
        "source_os": platform.system(),
        "source_arch": platform.machine(),
        "python": platform.python_version(),
        "git_branch": _git_branch(workspace),
        "available_runtime_tools": available_tools,
    }


def _default_handoff(workspace: Path) -> str:
    return """# WorkBuddy Workspace Handoff

## Project goal

The project goal was not supplied to the deterministic packer. The WorkBuddy
agent should read the project rules and source files before continuing.

## Current phase

The workspace was packaged without a semantic handoff supplied by the agent.

## Confirmed decisions

- Preserve the restored files and existing project rules.
- Do not execute restored scripts automatically.

## Current constraints

- Treat this file as a machine-generated fallback, not as a complete project brief.
- Do not treat missing information as confirmed.

## Next action

Read this file, then inspect the restored project rules and continue only after
reconstructing the current task context.
"""


def _read_handoff(workspace: Path, handoff_file: Path | None) -> str:
    source = handoff_file
    if source is None:
        candidate = workspace / "HANDOFF.md"
        if candidate.is_file() and not candidate.is_symlink():
            source = candidate
    if source is None:
        return _default_handoff(workspace)
    if not source.is_file() or source.is_symlink():
        raise RelayError(f"handoff file is not a regular file: {source}")
    try:
        content = source.read_text(encoding="utf-8")
    except UnicodeDecodeError as exc:
        raise RelayError("handoff file must be UTF-8 text") from exc
    if not content.strip():
        raise RelayError("handoff file must not be empty")
    return content


def _add_tree(tar: tarfile.TarFile, path: Path, archive_name: str) -> None:
    """Add only regular files and directories from a symlink-free staging tree."""
    if path.is_symlink():
        raise RelayError("internal staging tree unexpectedly contains a symlink")
    if path.is_dir():
        tar.add(path, arcname=archive_name, recursive=False)
        for child in sorted(path.iterdir(), key=lambda item: item.name):
            _add_tree(tar, child, f"{archive_name}/{child.name}")
        return
    if path.is_file():
        tar.add(path, arcname=archive_name, recursive=False)
        return
    raise RelayError(f"unsupported file type in staging tree: {path}")


def _platform_key() -> tuple[str, str]:
    system = platform.system().lower()
    if system == "darwin":
        system = "darwin"
    elif system == "windows":
        system = "windows"
    elif system == "linux":
        system = "linux"
    machine = platform.machine().lower()
    if machine in {"aarch64", "arm64"}:
        machine = "arm64"
    elif machine in {"x86_64", "amd64"}:
        machine = "amd64"
    return system, machine


def _resolve_age(explicit: str | None) -> Path:
    if explicit:
        candidate = Path(explicit).expanduser()
        if not candidate.is_file():
            raise RelayError(f"age executable was not found: {candidate}")
        return candidate

    root = Path(__file__).resolve().parents[1]
    system, machine = _platform_key()
    executable = "age.exe" if system == "windows" else "age"
    candidates = [
        root / "bin" / f"{system}-{machine}" / executable,
        root / "bin" / system / machine / executable,
        root / "bin" / executable,
    ]
    on_path = shutil.which("age")
    if on_path:
        candidates.append(Path(on_path))
    for candidate in candidates:
        if candidate.is_file():
            return candidate
    raise RelayError(
        "age executable is unavailable; install age or place the approved "
        f"binary at bin/{system}-{machine}/{executable}"
    )


def _write_password(master: int, password: str) -> None:
    if "\n" in password or "\r" in password:
        raise RelayError("password may not contain a line break")
    data = bytearray(password.encode("utf-8") + b"\n")
    try:
        offset = 0
        while offset < len(data):
            offset += os.write(master, data[offset:])
    finally:
        for index in range(len(data)):
            data[index] = 0


def _run_age_posix(command: list[str], password: str, expect_confirmation: bool) -> None:
    import pty

    master, slave = pty.openpty()
    process = subprocess.Popen(
        command,
        stdin=slave,
        stdout=slave,
        stderr=slave,
        close_fds=True,
    )
    os.close(slave)
    sent_first = False
    sent_second = False
    started = time.monotonic()
    output = bytearray()
    try:
        while True:
            if time.monotonic() - started > AGE_TIMEOUT_SECONDS:
                process.kill()
                raise RelayError("age operation timed out")
            readable, _, _ = select.select([master], [], [], 0.5)
            if readable:
                try:
                    data = os.read(master, 4096)
                except OSError:
                    data = b""
                if data:
                    output.extend(data)
                    if not sent_first and b"Enter passphrase" in output:
                        _write_password(master, password)
                        sent_first = True
                    if (
                        expect_confirmation
                        and sent_first
                        and not sent_second
                        and b"Confirm passphrase" in output
                    ):
                        _write_password(master, password)
                        sent_second = True
                elif process.poll() is not None:
                    break
            if process.poll() is not None and not readable:
                break
        return_code = process.wait(timeout=5)
    finally:
        try:
            os.close(master)
        except OSError:
            pass
    if return_code != 0:
        raise RelayError("age could not encrypt or decrypt the migration package")
    if not sent_first or (expect_confirmation and not sent_second):
        raise RelayError("age did not request the expected local password input")


def _run_age_windows(command: list[str], password: str) -> None:
    """Run age in a local console on Windows; the password never enters chat or args."""
    del password
    creation_flags = getattr(subprocess, "CREATE_NEW_CONSOLE", 0)
    try:
        result = subprocess.run(
            command,
            check=False,
            creationflags=creation_flags,
            timeout=AGE_TIMEOUT_SECONDS,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
    except subprocess.TimeoutExpired as exc:
        raise RelayError("age operation timed out") from exc
    if result.returncode != 0:
        raise RelayError("age could not encrypt or decrypt the migration package")


def _run_age(command: list[str], password: str, expect_confirmation: bool) -> None:
    if os.name == "nt":
        _run_age_windows(command, password)
    else:
        _run_age_posix(command, password, expect_confirmation)


def _prompt_passwords(mode: str, use_stdin: bool) -> tuple[str, str | None]:
    if use_stdin:
        first = sys.stdin.buffer.readline()
        if not first:
            raise RelayError("password input was empty")
        password = first.rstrip(b"\r\n").decode("utf-8")
        confirmation: str | None = None
        if mode == "pack":
            second = sys.stdin.buffer.readline()
            if not second:
                raise RelayError("pack mode requires password confirmation")
            confirmation = second.rstrip(b"\r\n").decode("utf-8")
    else:
        if os.name == "nt":
            # The bundled Windows age binary owns its local console prompt.
            # Do not collect a second password in a Tk window that cannot be
            # passed to age without exposing it through an unsupported channel.
            return "__local_console_prompt__", None
        try:
            import tkinter as tk
            root = tk.Tk()
            root.title("WorkBuddy Workspace Relay")
            root.resizable(False, False)
            root.attributes("-topmost", True)
            result: dict[str, str | None] = {"password": None, "confirmation": None}
            frame = tk.Frame(root, padx=18, pady=16)
            frame.pack()
            label = "设置迁移密码" if mode == "pack" else "输入迁移密码"
            tk.Label(frame, text=label).grid(row=0, column=0, columnspan=2, pady=(0, 8))
            tk.Label(frame, text="密码").grid(row=1, column=0, sticky="e", padx=(0, 8))
            first_entry = tk.Entry(frame, show="•", width=28)
            first_entry.grid(row=1, column=1)
            second_entry = None
            if mode == "pack":
                tk.Label(frame, text="再次输入").grid(row=2, column=0, sticky="e", padx=(0, 8))
                second_entry = tk.Entry(frame, show="•", width=28)
                second_entry.grid(row=2, column=1)

            def submit() -> None:
                result["password"] = first_entry.get()
                result["confirmation"] = second_entry.get() if second_entry else None
                root.destroy()

            def cancel() -> None:
                root.destroy()

            row = 3 if mode == "pack" else 2
            tk.Button(frame, text="继续", command=submit, width=10).grid(
                row=row, column=1, sticky="e", pady=(12, 0)
            )
            root.protocol("WM_DELETE_WINDOW", cancel)
            first_entry.focus_set()
            root.mainloop()
            password = result["password"] or ""
            confirmation = result["confirmation"]
        except Exception:
            password = getpass.getpass("Migration password: ")
            confirmation = getpass.getpass("Confirm migration password: ") if mode == "pack" else None

    if not password:
        raise RelayError("password must not be empty")
    if mode == "pack" and password != confirmation:
        raise RelayError("password confirmation did not match")
    return password, confirmation


def _validate_archive_name(name: str) -> PurePosixPath:
    if not name or name.startswith("/") or "\\" in name:
        raise RelayError("migration package contains an unsafe path")
    parts = name.split("/")
    if any(part in {"", ".", ".."} for part in parts):
        raise RelayError("migration package contains a path traversal")
    path = PurePosixPath(name)
    if path.parts[0] != "payload":
        raise RelayError("migration package contains an unexpected root")
    return path


def _extract_archive(tar_path: Path, destination: Path) -> None:
    seen: set[str] = set()
    with tarfile.open(tar_path, mode="r:gz") as archive:
        members = archive.getmembers()
        if not members:
            raise RelayError("migration package archive is empty")
        for member in members:
            safe_name = _validate_archive_name(member.name)
            if member.name in seen:
                raise RelayError("migration package contains duplicate paths")
            seen.add(member.name)
            if not (member.isdir() or member.isreg()):
                raise RelayError("migration package contains a link or special file")
            target = destination.joinpath(*safe_name.parts)
            if not _is_within(target, destination):
                raise RelayError("migration package escapes the extraction directory")
            if member.isdir():
                target.mkdir(parents=True, exist_ok=True)
                continue
            target.parent.mkdir(parents=True, exist_ok=True)
            source = archive.extractfile(member)
            if source is None:
                raise RelayError("migration package contains an unreadable file")
            with source, target.open("wb") as output:
                shutil.copyfileobj(source, output, length=CHUNK_SIZE)
            try:
                os.chmod(target, stat.S_IMODE(member.mode))
            except OSError:
                pass


def _validate_manifest(extracted: Path) -> tuple[dict[str, Any], dict[str, Any], str]:
    payload = extracted / "payload"
    manifest_path = payload / "manifest.json"
    runtime_path = payload / "runtime.json"
    handoff_path = payload / "HANDOFF.md"
    workspace_path = payload / "workspace"
    if not all(path.is_file() for path in (manifest_path, runtime_path, handoff_path)):
        raise RelayError("migration package is missing required metadata")
    if not workspace_path.is_dir() or workspace_path.is_symlink():
        raise RelayError("migration package is missing its workspace payload")
    top_level = {path.name for path in payload.iterdir()}
    if top_level != {"workspace", "HANDOFF.md", "manifest.json", "runtime.json"}:
        raise RelayError("migration package has unexpected top-level content")
    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        runtime = json.loads(runtime_path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise RelayError("migration package metadata is not valid UTF-8 JSON") from exc
    if manifest.get("format_version") != FORMAT_VERSION:
        raise RelayError("unsupported migration package format version")
    project_name = manifest.get("project_name")
    if not isinstance(project_name, str) or not project_name:
        raise RelayError("migration package has no project name")
    files = manifest.get("files")
    if not isinstance(files, list):
        raise RelayError("migration package manifest has no file list")
    file_count = manifest.get("file_count")
    total_bytes = manifest.get("total_bytes")
    if not isinstance(file_count, int) or file_count < 0:
        raise RelayError("migration package manifest has an invalid file count")
    if not isinstance(total_bytes, int) or total_bytes < 0:
        raise RelayError("migration package manifest has an invalid byte count")
    expected: set[str] = set()
    for entry in files:
        if not isinstance(entry, dict):
            raise RelayError("migration package manifest contains an invalid file record")
        relative = entry.get("path")
        digest = entry.get("sha256")
        size = entry.get("size")
        if (
            not isinstance(relative, str)
            or not relative.startswith("workspace/")
            or not isinstance(digest, str)
            or not re.fullmatch(r"[0-9a-f]{64}", digest)
            or not isinstance(size, int)
            or size < 0
        ):
            raise RelayError("migration package manifest contains an invalid file record")
        relative_path = relative[len("workspace/") :]
        _validate_archive_name(f"payload/workspace/{relative_path}")
        if relative in expected:
            raise RelayError("migration package manifest contains duplicate files")
        expected.add(relative)
    if file_count != len(files) or total_bytes != sum(entry["size"] for entry in files):
        raise RelayError("migration package manifest totals do not match its file list")

    actual: set[str] = set()
    for path in workspace_path.rglob("*"):
        if path.is_symlink():
            raise RelayError("migration package workspace contains a symlink")
        if path.is_file():
            relative = path.relative_to(workspace_path).as_posix()
            actual.add(f"workspace/{relative}")
    if actual != expected:
        raise RelayError("migration package contents do not match its manifest")
    for entry in files:
        relative = entry["path"][len("workspace/") :]
        file_path = workspace_path.joinpath(*PurePosixPath(relative).parts)
        if file_path.stat().st_size != entry["size"] or _sha256(file_path) != entry["sha256"]:
            raise RelayError(f"integrity check failed for {entry['path']}")
    return manifest, runtime, project_name


def _unique_restore_target(destination_root: Path, project_name: str) -> Path:
    if not any(destination_root.iterdir()):
        return destination_root
    base = destination_root / f"{_safe_project_name(project_name)}-已恢复"
    candidate = base
    index = 2
    while _lexists(candidate):
        candidate = destination_root / f"{_safe_project_name(project_name)}-已恢复-{index}"
        index += 1
    return candidate


def _prepare_restore_root(extracted: Path, destination: Path) -> None:
    payload = extracted / "payload"
    workspace = payload / "workspace"
    shutil.copytree(workspace, destination, symlinks=False)
    metadata = destination / METADATA_DIR
    metadata.mkdir(parents=True, exist_ok=True)
    for name in ("HANDOFF.md", "manifest.json", "runtime.json"):
        _copy_file(payload / name, metadata / name)


def pack_workspace(
    workspace: Path,
    output: Path | None,
    output_dir: Path | None,
    handoff_file: Path | None,
    age_bin: str | None,
    password_stdin: bool,
    json_output: bool,
) -> int:
    workspace = workspace.expanduser().resolve()
    if not workspace.is_dir() or workspace.is_symlink():
        raise RelayError(f"workspace is not a regular directory: {workspace}")
    if output and output_dir:
        raise RelayError("use either --output or --output-dir, not both")
    if output is None:
        if output_dir is None:
            desktop = Path.home() / "Desktop"
            output_dir = desktop if desktop.is_dir() and not _is_within(desktop, workspace) else workspace.parent
        output_dir = output_dir.expanduser().resolve()
        output_dir.mkdir(parents=True, exist_ok=True)
        timestamp = time.strftime("%Y%m%d-%H%M%S")
        output = output_dir / f"{_workspace_name(workspace)}-WorkBuddy-{timestamp}{PACKAGE_SUFFIX}"
    else:
        output = output.expanduser().resolve()
    if _is_within(output, workspace):
        raise RelayError("migration package output must be outside the source workspace")
    if _lexists(output):
        raise RelayError(f"output file already exists: {output}")
    output.parent.mkdir(parents=True, exist_ok=True)
    age = _resolve_age(age_bin)
    password, _ = _prompt_passwords("pack", password_stdin)

    files, directories, skipped_symlinks = _scan_workspace(workspace)
    handoff = _read_handoff(workspace, handoff_file.expanduser().resolve() if handoff_file else None)
    staging_parent = Path(tempfile.mkdtemp(prefix="workbuddy-relay-pack-"))
    partial = output.with_name(output.name + ".part")
    try:
        staging = staging_parent / "package"
        payload = staging / "payload"
        staged_workspace = payload / "workspace"
        staged_workspace.mkdir(parents=True)
        for directory in directories:
            (staged_workspace / directory).mkdir(parents=True, exist_ok=True)

        records: list[dict[str, Any]] = []
        total_bytes = 0
        for source in files:
            relative = source.relative_to(workspace)
            target = staged_workspace / relative
            _copy_file(source, target)
            size = target.stat().st_size
            total_bytes += size
            records.append(
                {
                    "path": f"workspace/{relative.as_posix()}",
                    "size": size,
                    "sha256": _sha256(target),
                    "mode": stat.S_IMODE(target.stat().st_mode),
                }
            )

        payload.mkdir(exist_ok=True)
        (payload / "HANDOFF.md").write_text(handoff, encoding="utf-8")
        manifest = {
            "format": "workbuddy-workspace-relay",
            "format_version": FORMAT_VERSION,
            "project_name": _workspace_name(workspace),
            "created_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "source_os": platform.system(),
            "source_arch": platform.machine(),
            "workspace_folder": "workspace",
            "file_count": len(records),
            "total_bytes": total_bytes,
            "directories": [f"workspace/{path.as_posix()}" for path in directories],
            "files": records,
            "excluded_rules": {
                "directories": sorted(EXCLUDED_DIRS),
                "filenames": sorted(EXCLUDED_FILENAMES),
                "suffixes": list(EXCLUDED_SUFFIXES),
                "symlinks": "skipped",
            },
            "skipped_symlink_count": skipped_symlinks,
        }
        runtime = _runtime_info(workspace)
        _json_dump(payload / "manifest.json", manifest)
        _json_dump(payload / "runtime.json", runtime)

        tar_path = staging_parent / "payload.tar.gz"
        with tarfile.open(tar_path, mode="w:gz", format=tarfile.PAX_FORMAT) as archive:
            _add_tree(archive, payload, "payload")
        command = [os.fspath(age), "-p", "-o", os.fspath(partial), os.fspath(tar_path)]
        _run_age(command, password, expect_confirmation=True)
        password = ""
        if not partial.is_file() or partial.stat().st_size == 0:
            raise RelayError("age did not produce a migration package")
        os.replace(partial, output)
        try:
            os.chmod(output, 0o600)
        except OSError:
            pass
    finally:
        password = ""
        if partial.exists():
            partial.unlink(missing_ok=True)
        shutil.rmtree(staging_parent, ignore_errors=True)

    result = {
        "package": os.fspath(output),
        "format_version": FORMAT_VERSION,
        "file_count": len(records),
        "total_bytes": total_bytes,
    }
    print(json.dumps(result, ensure_ascii=False) if json_output else os.fspath(output))
    return 0


def restore_workspace(
    package: Path,
    destination_root: Path,
    age_bin: str | None,
    password_stdin: bool,
    json_output: bool,
) -> int:
    package = package.expanduser().resolve()
    destination_root = destination_root.expanduser().resolve()
    if not package.is_file() or package.is_symlink():
        raise RelayError(f"migration package is not a regular file: {package}")
    if package.suffix != PACKAGE_SUFFIX:
        raise RelayError(f"migration package must use the {PACKAGE_SUFFIX} extension")
    destination_root.mkdir(parents=True, exist_ok=True)
    age = _resolve_age(age_bin)
    password, _ = _prompt_passwords("restore", password_stdin)
    staging_parent = Path(tempfile.mkdtemp(prefix="workbuddy-relay-restore-"))
    try:
        decrypted = staging_parent / "payload.tar.gz"
        command = [os.fspath(age), "-d", "-o", os.fspath(decrypted), os.fspath(package)]
        _run_age(command, password, expect_confirmation=False)
        password = ""
        extracted = staging_parent / "extracted"
        extracted.mkdir()
        _extract_archive(decrypted, extracted)
        manifest, _, project_name = _validate_manifest(extracted)
        target = _unique_restore_target(destination_root, project_name)
        if target != destination_root:
            target.parent.mkdir(parents=True, exist_ok=True)
            target_staging = staging_parent / "restored"
            _prepare_restore_root(extracted, target_staging)
            os.replace(target_staging, target)
        else:
            target_staging = staging_parent / "restored"
            _prepare_restore_root(extracted, target_staging)
            for child in sorted(target_staging.iterdir(), key=lambda item: item.name):
                os.replace(child, destination_root / child.name)
        result = {
            "restored_to": os.fspath(target),
            "project_name": project_name,
            "format_version": FORMAT_VERSION,
            "file_count": manifest["file_count"],
            "verified": True,
        }
    finally:
        password = ""
        shutil.rmtree(staging_parent, ignore_errors=True)
    print(json.dumps(result, ensure_ascii=False) if json_output else os.fspath(target))
    return 0


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="WorkBuddy Workspace Relay file engine")
    subparsers = parser.add_subparsers(dest="command", required=True)

    pack = subparsers.add_parser("pack", help="pack a workspace into an encrypted .wbpack")
    pack.add_argument("--workspace", type=Path, default=Path.cwd())
    pack.add_argument("--output", type=Path)
    pack.add_argument("--output-dir", type=Path)
    pack.add_argument("--handoff-file", type=Path)
    pack.add_argument("--age-bin")
    pack.add_argument("--password-stdin", action="store_true")
    pack.add_argument("--json", action="store_true", dest="json_output")

    restore = subparsers.add_parser("restore", help="restore an encrypted .wbpack")
    restore.add_argument("package", type=Path)
    restore.add_argument("--destination-root", type=Path, default=Path.cwd())
    restore.add_argument("--age-bin")
    restore.add_argument("--password-stdin", action="store_true")
    restore.add_argument("--json", action="store_true", dest="json_output")
    return parser


def main(argv: Iterable[str] | None = None) -> int:
    args = _build_parser().parse_args(list(argv) if argv is not None else None)
    try:
        if args.command == "pack":
            return pack_workspace(
                args.workspace,
                args.output,
                args.output_dir,
                args.handoff_file,
                args.age_bin,
                args.password_stdin,
                args.json_output,
            )
        return restore_workspace(
            args.package,
            args.destination_root,
            args.age_bin,
            args.password_stdin,
            args.json_output,
        )
    except RelayError as exc:
        print(f"workbuddy-relay: {exc}", file=sys.stderr)
        return 2
    except (OSError, tarfile.TarError, json.JSONDecodeError) as exc:
        print(f"workbuddy-relay: operation failed safely: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
