#!/usr/bin/env python3
"""Manage explicit, portable TaoHtml corporate-template profiles."""

from __future__ import annotations

import argparse
from contextlib import contextmanager
import errno
import hashlib
import json
import os
import re
import shutil
import stat
import sys
import tempfile
import threading
import time
import unicodedata
import uuid
import zipfile
from pathlib import Path, PurePosixPath
from typing import Any, Iterator


SCRIPT_ROOT = Path(__file__).resolve().parent
if str(SCRIPT_ROOT) not in sys.path:
    sys.path.insert(0, str(SCRIPT_ROOT))

import compile_project_theme
import render_reference_vi
import theme_runtime


STORE_SCHEMA_VERSION = "1.0"
PROFILE_SCHEMA_VERSION = "1.0"
VERSION_SCHEMA_VERSION = "1.1"
LEGACY_VERSION_SCHEMA_VERSION = "1.0"
BINDING_SCHEMA_VERSION = "1.0"
PACKAGE_SCHEMA_VERSION = "1.0"
PROFILE_ID = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
SHA256 = re.compile(r"^[0-9a-f]{64}$")
WINDOWS_ABSOLUTE = re.compile(r"^[A-Za-z]:[\\/]")
WINDOWS_RESERVED = {
    "con",
    "prn",
    "aux",
    "nul",
    *(f"com{index}" for index in range(1, 10)),
    *(f"lpt{index}" for index in range(1, 10)),
}
MAX_PACKAGE_FILES = 2048
MAX_PACKAGE_BYTES = 512 * 1024 * 1024
LOCK_TIMEOUT_SECONDS = 30.0
LEGACY_LOCK_STALE_SECONDS = 300.0
TRANSACTION_SCHEMA_VERSION = "1.0"
TRANSACTION_KEYS = {
    "schema_version",
    "operation",
    "profile_id",
    "version",
    "old_profile_sha256",
    "new_profile_sha256",
}
_THREAD_LOCKS_GUARD = threading.Lock()
_THREAD_LOCKS: dict[str, threading.Lock] = {}
PROFILE_KEYS = {
    "schema_version",
    "profile_id",
    "display_name",
    "aliases",
    "status",
    "active_version",
    "created_at",
    "updated_at",
    "activation",
    "versions",
}
ACTIVATION_KEYS = {"version", "activated_at", "reason", "sequence"}
VERSION_ENTRY_KEYS = {"version", "manifest", "manifest_sha256"}
VERSION_KEYS = {
    "schema_version",
    "profile_id",
    "version",
    "display_name",
    "aliases",
    "lifecycle",
    "confirmation_source",
    "boundaries",
    "creation_context",
    "hashes",
    "assets",
}
LEGACY_VERSION_KEYS = VERSION_KEYS - {"creation_context"}
LIFECYCLE_KEYS = {
    "created_state",
    "created_at",
    "initial_activation_state",
    "initial_activated_at",
}
CONFIRMATION_KEYS = {
    "source_handoff_sha256",
    "method",
    "reference",
    "vi_contract_sha256",
    "reference_images_sha256",
    "source_theme_fingerprint",
}
BOUNDARY_KEYS = {
    "reference_mode",
    "screenshot_visible_only",
    "excluded_content",
}
CREATION_CONTEXT_KEYS = {"source_target_mode"}
LEGACY_BOUNDARY_KEYS = BOUNDARY_KEYS | {"target_mode"}
HASH_KEYS = {
    "vi_contract_sha256",
    "reference_images_sha256",
    "theme_fingerprint",
}
ASSET_KEYS = {"path", "role", "sha256", "size"}
BINDING_KEYS = {
    "schema_version",
    "task_id",
    "profile_id",
    "profile_display_name",
    "version",
    "active_version_at_bind",
    "target_mode",
    "theme_home_path",
    "theme_fingerprint",
    "vi_contract_sha256",
    "reference_images_sha256",
    "profile_record_sha256",
    "version_manifest_sha256",
    "resolution",
    "temporary_override",
    "customer_notice",
    "bound_at",
}
RESOLUTION_KEYS = {"identities", "basis"}
PACKAGE_KEYS = {
    "schema_version",
    "profile_id",
    "exported_at",
    "files",
}
PACKAGE_FILE_KEYS = {"path", "sha256", "size"}
THEME_FILES = tuple(sorted(theme_runtime.PROJECT_THEME_FILES))
EXCLUDED_CONTENT = [
    "report_body",
    "project_goal",
    "audience",
    "evidence",
    "customer_report_data",
    "user_preferences_outside_corporate_brand",
]


def _now() -> str:
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())


def _json_bytes(value: object) -> bytes:
    return (json.dumps(value, ensure_ascii=False, indent=2) + "\n").encode("utf-8")


def _exact_object(raw: object, keys: set[str], label: str) -> dict[str, Any]:
    if not isinstance(raw, dict):
        raise ValueError(f"{label} must be an object")
    actual = set(raw)
    if actual != keys:
        missing = ", ".join(sorted(keys - actual)) or "none"
        extra = ", ".join(sorted(actual - keys)) or "none"
        raise ValueError(
            f"{label} fields drifted; missing={missing}; extra={extra}"
        )
    return raw


def _text(value: object, label: str, maximum: int = 160) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{label} must be a non-empty string")
    normalized = value.strip()
    if len(normalized) > maximum:
        raise ValueError(f"{label} exceeds {maximum} characters")
    return normalized


def _integer(value: object, label: str, minimum: int = 1) -> int:
    if not isinstance(value, int) or isinstance(value, bool) or value < minimum:
        raise ValueError(f"{label} must be an integer >= {minimum}")
    return value


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _bytes_sha256(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def _load_json(path: Path, label: str) -> dict[str, Any]:
    try:
        raw = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise ValueError(f"{label} is missing: {path}") from exc
    except json.JSONDecodeError as exc:
        raise ValueError(f"{label} is not valid JSON: {path}: {exc}") from exc
    if not isinstance(raw, dict):
        raise ValueError(f"{label} must be a JSON object: {path}")
    return raw


def _atomic_write(path: Path, payload: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(f".{path.name}.tmp-{uuid.uuid4().hex}")
    try:
        with temporary.open("xb") as handle:
            handle.write(payload)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary, path)
        try:
            descriptor = os.open(path.parent, os.O_RDONLY)
        except OSError:
            return
        try:
            os.fsync(descriptor)
        finally:
            os.close(descriptor)
    finally:
        if temporary.exists():
            temporary.unlink()


def _atomic_json(path: Path, value: object) -> None:
    _atomic_write(path, _json_bytes(value))


def _normalize_identity(value: str) -> str:
    return " ".join(unicodedata.normalize("NFKC", value).split()).casefold()


def _profile_id(value: object) -> str:
    result = _text(value, "profile_id", 48)
    if not PROFILE_ID.fullmatch(result):
        raise ValueError("profile_id must be a lowercase hyphenated slug")
    return result


def _aliases(values: object, display_name: str) -> list[str]:
    if not isinstance(values, list) or len(values) > 20:
        raise ValueError("aliases must be a list of at most 20 explicit aliases")
    normalized: set[str] = {_normalize_identity(display_name)}
    result: list[str] = []
    for index, value in enumerate(values):
        alias = _text(value, f"aliases[{index}]", 80)
        key = _normalize_identity(alias)
        if key in normalized:
            raise ValueError("aliases must be unique and must not repeat display_name")
        normalized.add(key)
        result.append(alias)
    return result


def _safe_package_path(value: object, label: str = "path") -> PurePosixPath:
    text = _text(value, label, 320)
    if (
        "\\" in text
        or text.startswith("/")
        or WINDOWS_ABSOLUTE.match(text)
        or text.startswith("//")
    ):
        raise ValueError(f"{label} must be a portable relative POSIX path")
    path = PurePosixPath(text)
    if path.is_absolute() or not path.parts or any(part in {"", ".", ".."} for part in path.parts):
        raise ValueError(f"{label} must be a portable relative POSIX path")
    if any(
        ":" in part
        or part.rstrip(" .") != part
        or part.split(".", 1)[0].casefold() in WINDOWS_RESERVED
        or any(ord(character) < 32 for character in part)
        for part in path.parts
    ):
        raise ValueError(f"{label} contains a non-portable path component")
    return path


def _regular_file(path: Path, label: str) -> Path:
    supplied = path.expanduser()
    if supplied.is_symlink():
        raise ValueError(f"{label} must not be a symlink: {supplied}")
    try:
        resolved = supplied.resolve(strict=True)
    except FileNotFoundError as exc:
        raise ValueError(f"{label} does not exist: {path}") from exc
    if not resolved.is_file():
        raise ValueError(f"{label} must be a regular file: {resolved}")
    return resolved


def _home_candidate(home: Path | None = None) -> Path:
    if home is None:
        environment = os.environ.get("TAOHTML_HOME")
        supplied = Path(environment).expanduser() if environment else Path.home() / ".taohtml"
    else:
        supplied = home.expanduser()
    if not supplied.is_absolute():
        raise ValueError("TAOHTML_HOME must be an absolute path")
    if supplied.is_symlink():
        raise ValueError(f"TAOHTML_HOME must not be a symlink: {supplied}")
    return supplied


def resolve_home(home: Path | None = None, *, create: bool = False) -> Path:
    supplied = _home_candidate(home)
    if create:
        supplied.mkdir(parents=True, exist_ok=True)
        (supplied / "profiles").mkdir(exist_ok=True)
    try:
        resolved = supplied.resolve(strict=True)
    except FileNotFoundError as exc:
        raise ValueError(f"TAOHTML_HOME does not exist: {supplied}") from exc
    if not resolved.is_dir():
        raise ValueError(f"TAOHTML_HOME is not a directory: {resolved}")
    profiles = resolved / "profiles"
    if profiles.is_symlink():
        raise ValueError(f"TAOHTML_HOME/profiles must not be a symlink: {profiles}")
    if create:
        profiles.mkdir(exist_ok=True)
    elif not profiles.is_dir():
        raise ValueError(f"TAOHTML_HOME profile store is missing: {profiles}")
    return resolved


def _local_store_lock(home: Path) -> threading.Lock:
    key = str(home)
    with _THREAD_LOCKS_GUARD:
        return _THREAD_LOCKS.setdefault(key, threading.Lock())


def _recover_legacy_lock_directory(lock_path: Path, deadline: float) -> None:
    while lock_path.is_dir() and not lock_path.is_symlink():
        entries = list(lock_path.iterdir())
        age = max(0.0, time.time() - lock_path.stat().st_mtime)
        if not entries and age >= LEGACY_LOCK_STALE_SECONDS:
            try:
                lock_path.rmdir()
                return
            except FileNotFoundError:
                return
        if time.monotonic() >= deadline:
            raise ValueError(
                "Profile store is busy; a recent or non-empty legacy lock directory "
                "cannot be recovered safely"
            )
        time.sleep(0.05)


def _open_lock_file(lock_path: Path) -> int:
    if lock_path.is_symlink():
        raise ValueError(f"Profile store lock path is unsafe: {lock_path}")
    flags = os.O_RDWR | os.O_CREAT | getattr(os, "O_BINARY", 0)
    if hasattr(os, "O_NOFOLLOW"):
        flags |= os.O_NOFOLLOW
    try:
        descriptor = os.open(lock_path, flags, 0o600)
    except OSError as exc:
        raise ValueError(f"Profile store lock path is unsafe: {lock_path}") from exc
    if not stat.S_ISREG(os.fstat(descriptor).st_mode):
        os.close(descriptor)
        raise ValueError(f"Profile store lock must be a regular file: {lock_path}")
    if os.fstat(descriptor).st_size == 0:
        os.write(descriptor, b"\0")
        os.fsync(descriptor)
    return descriptor


def _try_os_lock(descriptor: int) -> bool:
    try:
        if os.name == "nt":
            import msvcrt

            os.lseek(descriptor, 0, os.SEEK_SET)
            msvcrt.locking(descriptor, msvcrt.LK_NBLCK, 1)
        else:
            import fcntl

            fcntl.flock(descriptor, fcntl.LOCK_EX | fcntl.LOCK_NB)
    except OSError as exc:
        if exc.errno in {errno.EACCES, errno.EAGAIN}:
            return False
        raise
    return True


def _release_os_lock(descriptor: int) -> None:
    if os.name == "nt":
        import msvcrt

        os.lseek(descriptor, 0, os.SEEK_SET)
        msvcrt.locking(descriptor, msvcrt.LK_UNLCK, 1)
    else:
        import fcntl

        fcntl.flock(descriptor, fcntl.LOCK_UN)


def _remove_managed_directory(path: Path, label: str) -> None:
    if path.is_symlink() or not path.is_dir():
        raise ValueError(f"{label} is unsafe: {path}")
    shutil.rmtree(path)


def _recover_abandoned_stages(home: Path) -> None:
    profiles_root = home / "profiles"
    if not profiles_root.is_dir():
        return
    for path in list(profiles_root.iterdir()):
        if path.name.startswith((".stage-create-", ".stage-import-")):
            _remove_managed_directory(path, "Abandoned profile transaction")
            continue
        if path.name.startswith(".") or path.is_symlink() or not path.is_dir():
            continue
        versions = path / "versions"
        if versions.is_symlink() or not versions.is_dir():
            continue
        for candidate in list(versions.iterdir()):
            if candidate.name.startswith(".stage-v"):
                _remove_managed_directory(candidate, "Abandoned version transaction")


def _recover_update_transactions(home: Path) -> None:
    root = home / ".profile-store-transactions"
    if not root.exists():
        return
    if root.is_symlink() or not root.is_dir():
        raise ValueError(f"Profile transaction root is unsafe: {root}")
    for transaction in sorted(root.iterdir()):
        if transaction.is_symlink() or not transaction.is_dir():
            raise ValueError(f"Profile transaction entry is unsafe: {transaction}")
        journal_path = transaction / "journal.json"
        if not journal_path.exists():
            _remove_managed_directory(transaction, "Incomplete profile transaction")
            continue
        if journal_path.is_symlink() or not journal_path.is_file():
            raise ValueError("Profile update journal is unsafe")
        journal = _exact_object(
            _load_json(journal_path, "Profile update journal"),
            TRANSACTION_KEYS,
            "profile update journal",
        )
        if (
            journal["schema_version"] != TRANSACTION_SCHEMA_VERSION
            or journal["operation"] != "update"
        ):
            raise ValueError("Profile update journal schema or operation is invalid")
        profile_id = _profile_id(journal["profile_id"])
        version = _integer(journal["version"], "profile update journal.version")
        old_path = transaction / "old-profile.json"
        new_path = transaction / "new-profile.json"
        if any(path.is_symlink() or not path.is_file() for path in (old_path, new_path)):
            raise ValueError("Profile update journal snapshots are missing or unsafe")
        old_payload = old_path.read_bytes()
        new_payload = new_path.read_bytes()
        if (
            journal["old_profile_sha256"] != _bytes_sha256(old_payload)
            or journal["new_profile_sha256"] != _bytes_sha256(new_payload)
        ):
            raise ValueError("Profile update journal snapshot hashes drifted")
        profile_root = home / "profiles" / profile_id
        profile_path = profile_root / "profile.json"
        if profile_path.is_symlink() or not profile_path.is_file():
            raise ValueError("Profile update target is missing or unsafe")
        current_payload = profile_path.read_bytes()
        current_hash = _bytes_sha256(current_payload)
        final_version = profile_root / "versions" / f"v{version}"
        committed = transaction / "committed"
        if committed.is_symlink():
            raise ValueError("Profile update commit marker is unsafe")
        if committed.exists():
            if (
                not committed.is_file()
                or current_hash != journal["new_profile_sha256"]
                or final_version.is_symlink()
                or not final_version.is_dir()
            ):
                raise ValueError("Committed profile transaction is incomplete")
            validate_profile(profile_root)
            _remove_managed_directory(transaction, "Committed profile transaction")
            continue
        if current_hash == journal["new_profile_sha256"]:
            _atomic_write(profile_path, old_payload)
        elif current_hash != journal["old_profile_sha256"]:
            raise ValueError("Profile changed outside an incomplete update transaction")
        if final_version.exists():
            _remove_managed_directory(final_version, "Uncommitted profile version")
        validate_profile(profile_root)
        _remove_managed_directory(transaction, "Rolled-back profile transaction")
    try:
        root.rmdir()
    except OSError:
        pass


def _recover_store(home: Path) -> None:
    _recover_abandoned_stages(home)
    _recover_update_transactions(home)


@contextmanager
def _store_lock(
    home: Path, timeout: float = LOCK_TIMEOUT_SECONDS
) -> Iterator[None]:
    deadline = time.monotonic() + timeout
    local_lock = _local_store_lock(home)
    if not local_lock.acquire(timeout=max(0.0, timeout)):
        raise ValueError("Profile store is busy; retry after the active operation finishes")
    descriptor: int | None = None
    locked = False
    try:
        lock_path = home / ".profile-store.lock"
        if lock_path.is_symlink():
            raise ValueError(f"Profile store lock path is unsafe: {lock_path}")
        if lock_path.is_dir():
            _recover_legacy_lock_directory(lock_path, deadline)
        descriptor = _open_lock_file(lock_path)
        while not _try_os_lock(descriptor):
            if time.monotonic() >= deadline:
                raise ValueError(
                    "Profile store is busy; retry after the active operation finishes"
                )
            time.sleep(0.05)
        locked = True
        _recover_store(home)
        yield
    finally:
        if descriptor is not None:
            if locked:
                _release_os_lock(descriptor)
            os.close(descriptor)
        local_lock.release()


def _theme_fingerprint(theme_dir: Path) -> str:
    records = [
        {"path": name, "sha256": _sha256(theme_dir / name)}
        for name in THEME_FILES
    ]
    return _bytes_sha256(
        json.dumps(records, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    )


def _asset_records(assets_root: Path) -> list[dict[str, object]]:
    records: list[dict[str, object]] = []
    for path in sorted(assets_root.rglob("*")):
        if path.is_symlink():
            raise ValueError(f"Profile assets must not contain symlinks: {path}")
        if path.is_dir():
            continue
        if not path.is_file():
            raise ValueError(f"Profile asset is not a regular file: {path}")
        relative = path.relative_to(assets_root).as_posix()
        if relative == "vi-contract.json":
            role = "vi_contract"
        elif relative.startswith("references/reference-"):
            role = "reference_image"
        elif relative.startswith("project-theme/"):
            role = "project_theme"
        else:
            raise ValueError(f"Unexpected profile asset path: {relative}")
        records.append(
            {
                "path": f"assets/{relative}",
                "role": role,
                "sha256": _sha256(path),
                "size": path.stat().st_size,
            }
        )
    return records


def _source_theme_matches_handoff(
    bundle: theme_runtime.ThemeBundle,
    request: dict[str, Any],
) -> None:
    project = bundle.manifest.get("project")
    compilation = bundle.manifest.get("compilation")
    if not isinstance(project, dict) or project.get("reference_mode") != "corporate_fidelity":
        raise ValueError("Only a validated corporate_fidelity project theme can enter a profile")
    if project.get("target_mode") != request["target_mode"]:
        raise ValueError("Project theme target_mode does not match the confirmed handoff")
    if not isinstance(compilation, dict):
        raise ValueError("Project theme compilation record is missing")
    if compilation.get("vi_contract_sha256") != request["confirmation"]["vi_contract_sha256"]:
        raise ValueError("Project theme VI hash does not match the confirmed handoff")
    expected_references = request["confirmation"].get("reference_images_sha256")
    if expected_references is None:
        expected_references = [request["confirmation"].get("reference_image_sha256")]
    actual_references = compilation.get("reference_images_sha256")
    if actual_references is None:
        actual_references = [compilation.get("reference_image_sha256")]
    if actual_references != expected_references:
        raise ValueError("Project theme reference hashes do not match the confirmed handoff")


def _assert_profile_theme_equivalent(
    source: theme_runtime.ThemeBundle,
    archived: theme_runtime.ThemeBundle,
) -> None:
    for key in (
        "identity",
        "tokens",
        "token_sources",
        "executable_layout",
        "structure_sources",
        "canvas",
        "layout_variants",
        "components",
        "preserve",
        "forbidden",
        "motion",
        "corporate_shell",
        "corporate_template_family",
    ):
        if source.manifest.get(key) != archived.manifest.get(key):
            raise ValueError(f"Archived profile theme drifted from the validated source theme: {key}")
    normalized_source_css = source.css.replace(source.theme_id, archived.theme_id)
    if normalized_source_css != archived.css or source.templates != archived.templates:
        raise ValueError("Archived profile theme CSS/templates drifted from the validated source theme")


def _portable_reference_name(index: int, path: Path) -> str:
    suffix = path.suffix.lower()
    if suffix not in {".png", ".jpg", ".jpeg", ".webp"}:
        raise ValueError("Corporate profile references must be PNG, JPEG, or WebP raster files")
    return f"reference-{index:02d}{suffix}"


def _reject_handoff_input_symlinks(handoff: Path) -> None:
    raw = _load_json(handoff, "Confirmed VI handoff")
    inputs = raw.get("inputs")
    if not isinstance(inputs, dict):
        return
    values: list[object] = []
    if "vi_contract" in inputs:
        values.append(inputs["vi_contract"])
    if "reference_image" in inputs:
        values.append(inputs["reference_image"])
    references = inputs.get("reference_images")
    if isinstance(references, list):
        values.extend(references)
    for index, value in enumerate(values):
        if not isinstance(value, str):
            continue
        relative = Path(value)
        cursor = handoff.parent
        for part in relative.parts:
            cursor = cursor / part
            if cursor.is_symlink():
                raise ValueError(
                    f"Confirmed handoff input must not use symlinks: inputs[{index}]"
                )


def _build_version(
    version_root: Path,
    *,
    profile_id: str,
    display_name: str,
    aliases: list[str],
    version: int,
    handoff_path: Path,
    source_theme_dir: Path,
    created_at: str,
) -> dict[str, Any]:
    handoff = _regular_file(handoff_path, "Confirmed VI handoff")
    if handoff.suffix.lower() != ".json":
        raise ValueError("Confirmed VI handoff must be JSON")
    _reject_handoff_input_symlinks(handoff)
    request, contract, vi_path, reference_input = compile_project_theme.load_handoff(handoff)
    if request["schema_version"] not in compile_project_theme.CURRENT_HANDOFF_SCHEMA_VERSIONS:
        raise ValueError("Corporate profiles require the current conversation-bound handoff schema")
    if contract.get("reference_mode") != "corporate_fidelity":
        raise ValueError("Only corporate_fidelity VI contracts can be saved as corporate profiles")
    reference_paths = [reference_input] if isinstance(reference_input, Path) else reference_input
    source_theme = theme_runtime.load_project_theme(source_theme_dir)
    _source_theme_matches_handoff(source_theme, request)
    source_theme_fingerprint = _theme_fingerprint(source_theme.root)

    assets_root = version_root / "assets"
    references_root = assets_root / "references"
    references_root.mkdir(parents=True)
    shutil.copyfile(vi_path, assets_root / "vi-contract.json")
    stored_references: list[Path] = []
    for index, reference in enumerate(reference_paths, 1):
        target = references_root / _portable_reference_name(index, reference)
        shutil.copyfile(reference, target)
        stored_references.append(target)

    with tempfile.TemporaryDirectory(prefix="profile-compile-") as temp_dir:
        compile_root = Path(temp_dir)
        shutil.copyfile(assets_root / "vi-contract.json", compile_root / "vi-contract.json")
        portable_reference_names: list[str] = []
        for stored in stored_references:
            target = compile_root / stored.name
            shutil.copyfile(stored, target)
            portable_reference_names.append(target.name)
        confirmation: dict[str, object] = {
            "status": "confirmed",
            "confirmation_ref": request["confirmation"]["confirmation_ref"],
            "vi_contract_sha256": request["confirmation"]["vi_contract_sha256"],
        }
        if len(stored_references) == 1 and request["schema_version"] == compile_project_theme.CURRENT_SINGLE_HANDOFF_SCHEMA_VERSION:
            confirmation["reference_image_sha256"] = request["confirmation"]["reference_image_sha256"]
            inputs: dict[str, object] = {
                "vi_contract": "vi-contract.json",
                "reference_image": portable_reference_names[0],
            }
        else:
            confirmation["reference_images_sha256"] = request["confirmation"]["reference_images_sha256"]
            inputs = {
                "vi_contract": "vi-contract.json",
                "reference_images": portable_reference_names,
            }
        archive_request = {
            "schema_version": request["schema_version"],
            "project": {
                "id": f"profile-{profile_id[:30]}-v{version}",
                "display_name": f"{display_name} 企业模板 v{version}",
            },
            "confirmation": confirmation,
            "inputs": inputs,
            "target_mode": request["target_mode"],
            "customer_corrections": [],
        }
        archive_handoff = compile_root / "handoff.json"
        archive_handoff.write_bytes(_json_bytes(archive_request))
        archive_theme_root = assets_root / "project-theme"
        compile_project_theme.compile_theme(archive_handoff, archive_theme_root)

    archived_theme = theme_runtime.load_project_theme(assets_root / "project-theme")
    _assert_profile_theme_equivalent(source_theme, archived_theme)
    reference_hashes = [_sha256(path) for path in stored_references]
    vi_hash = _sha256(assets_root / "vi-contract.json")
    if vi_hash != request["confirmation"]["vi_contract_sha256"]:
        raise ValueError("Stored VI contract hash drifted during profile creation")
    expected_reference_hashes = request["confirmation"].get("reference_images_sha256")
    if expected_reference_hashes is None:
        expected_reference_hashes = [request["confirmation"]["reference_image_sha256"]]
    if reference_hashes != expected_reference_hashes:
        raise ValueError("Stored reference hashes drifted during profile creation")
    theme_fingerprint = _theme_fingerprint(archived_theme.root)
    assets = _asset_records(assets_root)
    manifest: dict[str, Any] = {
        "schema_version": VERSION_SCHEMA_VERSION,
        "profile_id": profile_id,
        "version": version,
        "display_name": display_name,
        "aliases": aliases,
        "lifecycle": {
            "created_state": "created",
            "created_at": created_at,
            "initial_activation_state": "activated",
            "initial_activated_at": created_at,
        },
        "confirmation_source": {
            "source_handoff_sha256": _sha256(handoff),
            "method": request["confirmation"]["confirmation_method"],
            "reference": request["confirmation"]["confirmation_ref"],
            "vi_contract_sha256": vi_hash,
            "reference_images_sha256": reference_hashes,
            "source_theme_fingerprint": source_theme_fingerprint,
        },
        "boundaries": {
            "reference_mode": "corporate_fidelity",
            "screenshot_visible_only": True,
            "excluded_content": EXCLUDED_CONTENT,
        },
        "creation_context": {
            "source_target_mode": request["target_mode"],
        },
        "hashes": {
            "vi_contract_sha256": vi_hash,
            "reference_images_sha256": reference_hashes,
            "theme_fingerprint": theme_fingerprint,
        },
        "assets": assets,
    }
    _atomic_json(version_root / "version.json", manifest)
    return manifest


def _version_entry(version_root: Path, manifest: dict[str, Any]) -> dict[str, object]:
    return {
        "version": manifest["version"],
        "manifest": f"versions/v{manifest['version']}/version.json",
        "manifest_sha256": _sha256(version_root / "version.json"),
    }


def _validate_asset_manifest(version_root: Path, manifest: dict[str, Any]) -> None:
    raw_assets = manifest["assets"]
    if not isinstance(raw_assets, list) or not raw_assets:
        raise ValueError("version.assets must be a non-empty complete file list")
    expected: dict[str, dict[str, Any]] = {}
    for index, raw in enumerate(raw_assets):
        asset = _exact_object(raw, ASSET_KEYS, f"version.assets[{index}]")
        relative = _safe_package_path(asset["path"], f"version.assets[{index}].path")
        if relative.parts[0] != "assets":
            raise ValueError("Every version asset must live under assets/")
        relative_text = relative.as_posix()
        if relative_text in expected:
            raise ValueError("version.assets contains duplicate paths")
        role = asset["role"]
        if role not in {"vi_contract", "reference_image", "project_theme"}:
            raise ValueError("version.assets role is invalid")
        digest = asset["sha256"]
        if not isinstance(digest, str) or not SHA256.fullmatch(digest):
            raise ValueError("version.assets sha256 is invalid")
        _integer(asset["size"], f"version.assets[{index}].size", 0)
        expected[relative_text] = asset
    actual: set[str] = set()
    for path in version_root.rglob("*"):
        if path.is_symlink():
            raise ValueError(f"Profile version contains a symlink: {path}")
        if path.is_dir():
            continue
        if not path.is_file():
            raise ValueError(f"Profile version contains a non-regular file: {path}")
        relative = path.relative_to(version_root).as_posix()
        if relative != "version.json":
            actual.add(relative)
    if actual != set(expected):
        missing = ", ".join(sorted(set(expected) - actual)) or "none"
        extra = ", ".join(sorted(actual - set(expected))) or "none"
        raise ValueError(f"Profile version file list drifted; missing={missing}; extra={extra}")
    for relative, asset in expected.items():
        path = version_root / Path(*PurePosixPath(relative).parts)
        if _sha256(path) != asset["sha256"] or path.stat().st_size != asset["size"]:
            raise ValueError(f"Profile asset hash or size drifted: {relative}")


def validate_version(
    version_root: Path,
    *,
    expected_profile_id: str | None = None,
    expected_display_name: str | None = None,
    expected_aliases: list[str] | None = None,
) -> dict[str, Any]:
    if version_root.is_symlink() or not version_root.is_dir():
        raise ValueError(f"Profile version must be a regular directory: {version_root}")
    raw_manifest = _load_json(version_root / "version.json", "Profile version manifest")
    schema_version = raw_manifest.get("schema_version")
    if schema_version == VERSION_SCHEMA_VERSION:
        manifest = _exact_object(raw_manifest, VERSION_KEYS, "version")
    elif schema_version == LEGACY_VERSION_SCHEMA_VERSION:
        manifest = _exact_object(raw_manifest, LEGACY_VERSION_KEYS, "legacy version")
    else:
        raise ValueError(
            "version.schema_version must be 1.1 or the compatible legacy 1.0"
        )
    profile_id = _profile_id(manifest["profile_id"])
    version = _integer(manifest["version"], "version.version")
    display_name = _text(manifest["display_name"], "version.display_name", 80)
    aliases = _aliases(manifest["aliases"], display_name)
    if expected_profile_id is not None and profile_id != expected_profile_id:
        raise ValueError("Version profile_id does not match its profile")
    if expected_display_name is not None and display_name != expected_display_name:
        raise ValueError("Version display_name snapshot drifted from its profile")
    if expected_aliases is not None and aliases != expected_aliases:
        raise ValueError("Version aliases snapshot drifted from its profile")
    lifecycle = _exact_object(manifest["lifecycle"], LIFECYCLE_KEYS, "version.lifecycle")
    if lifecycle["created_state"] != "created" or lifecycle["initial_activation_state"] != "activated":
        raise ValueError("Version lifecycle must preserve created and initial activated states")
    _text(lifecycle["created_at"], "version.lifecycle.created_at")
    _text(lifecycle["initial_activated_at"], "version.lifecycle.initial_activated_at")
    confirmation = _exact_object(
        manifest["confirmation_source"], CONFIRMATION_KEYS, "version.confirmation_source"
    )
    for field in ("source_handoff_sha256", "vi_contract_sha256", "source_theme_fingerprint"):
        value = confirmation[field]
        if not isinstance(value, str) or not SHA256.fullmatch(value):
            raise ValueError(f"version.confirmation_source.{field} must be SHA-256")
    if confirmation["method"] != "conversation_ref":
        raise ValueError("Corporate profile confirmation must be conversation-bound")
    _text(confirmation["reference"], "version.confirmation_source.reference")
    if schema_version == LEGACY_VERSION_SCHEMA_VERSION:
        boundaries = _exact_object(
            manifest["boundaries"], LEGACY_BOUNDARY_KEYS, "legacy version.boundaries"
        )
        source_target_mode = boundaries.get("target_mode")
        expected_boundaries = {
            "reference_mode": "corporate_fidelity",
            "screenshot_visible_only": True,
            "target_mode": source_target_mode,
            "excluded_content": EXCLUDED_CONTENT,
        }
    else:
        boundaries = _exact_object(
            manifest["boundaries"], BOUNDARY_KEYS, "version.boundaries"
        )
        creation_context = _exact_object(
            manifest["creation_context"],
            CREATION_CONTEXT_KEYS,
            "version.creation_context",
        )
        source_target_mode = creation_context["source_target_mode"]
        expected_boundaries = {
            "reference_mode": "corporate_fidelity",
            "screenshot_visible_only": True,
            "excluded_content": EXCLUDED_CONTENT,
        }
    if boundaries != expected_boundaries:
        raise ValueError("Version boundaries drifted from the corporate profile contract")
    if source_target_mode not in {"reading", "presentation"}:
        raise ValueError("Version source_target_mode is invalid")
    hashes = _exact_object(manifest["hashes"], HASH_KEYS, "version.hashes")
    _validate_asset_manifest(version_root, manifest)
    vi_path = version_root / "assets" / "vi-contract.json"
    references = sorted((version_root / "assets" / "references").glob("reference-*"))
    if not references:
        raise ValueError("Profile version has no reference images")
    vi_hash = _sha256(vi_path)
    reference_hashes = [_sha256(path) for path in references]
    if hashes["vi_contract_sha256"] != vi_hash or confirmation["vi_contract_sha256"] != vi_hash:
        raise ValueError("Profile VI contract hash drifted")
    if hashes["reference_images_sha256"] != reference_hashes or confirmation["reference_images_sha256"] != reference_hashes:
        raise ValueError("Profile reference image hashes drifted")
    contract = render_reference_vi.load_contract(vi_path)
    if contract.get("reference_mode") != "corporate_fidelity":
        raise ValueError("Profile VI contract is not corporate_fidelity")
    render_reference_vi.validate_source_bindings(contract, references)
    theme_dir = version_root / "assets" / "project-theme"
    bundle = theme_runtime.load_project_theme(theme_dir)
    fingerprint = _theme_fingerprint(theme_dir)
    if hashes["theme_fingerprint"] != fingerprint:
        raise ValueError("Profile theme fingerprint drifted")
    project = bundle.manifest.get("project")
    compilation = bundle.manifest.get("compilation")
    if not isinstance(project, dict) or project.get("reference_mode") != "corporate_fidelity":
        raise ValueError("Profile theme is not corporate_fidelity")
    if project.get("target_mode") != source_target_mode:
        raise ValueError("Profile theme source target_mode provenance drifted")
    if not isinstance(compilation, dict) or compilation.get("vi_contract_sha256") != vi_hash:
        raise ValueError("Profile theme VI provenance drifted")
    compiled_references = compilation.get("reference_images_sha256")
    if compiled_references is None:
        compiled_references = [compilation.get("reference_image_sha256")]
    if compiled_references != reference_hashes:
        raise ValueError("Profile theme reference provenance drifted")
    if version_root.name != f"v{version}":
        raise ValueError("Profile version directory does not match its version number")
    return manifest


def validate_profile(profile_root: Path) -> dict[str, Any]:
    if profile_root.is_symlink() or not profile_root.is_dir():
        raise ValueError(f"Profile must be a regular directory: {profile_root}")
    actual_root = {path.name for path in profile_root.iterdir()}
    if actual_root != {"profile.json", "versions"}:
        raise ValueError("Profile root must contain exactly profile.json and versions/")
    if (profile_root / "profile.json").is_symlink() or (profile_root / "versions").is_symlink():
        raise ValueError("Profile metadata and versions must not be symlinks")
    profile = _exact_object(
        _load_json(profile_root / "profile.json", "Corporate profile"),
        PROFILE_KEYS,
        "profile",
    )
    if profile["schema_version"] != PROFILE_SCHEMA_VERSION:
        raise ValueError(f"profile.schema_version must be {PROFILE_SCHEMA_VERSION}")
    profile_id = _profile_id(profile["profile_id"])
    if profile_root.name != profile_id:
        raise ValueError("Profile directory does not match profile_id")
    display_name = _text(profile["display_name"], "profile.display_name", 80)
    aliases = _aliases(profile["aliases"], display_name)
    if profile["status"] not in {"active", "archived"}:
        raise ValueError("profile.status must be active or archived")
    active_version = _integer(profile["active_version"], "profile.active_version")
    _text(profile["created_at"], "profile.created_at")
    _text(profile["updated_at"], "profile.updated_at")
    activation = _exact_object(profile["activation"], ACTIVATION_KEYS, "profile.activation")
    if _integer(activation["version"], "profile.activation.version") != active_version:
        raise ValueError("Profile activation pointer does not match active_version")
    _text(activation["activated_at"], "profile.activation.activated_at")
    if activation["reason"] not in {"created", "updated", "manual", "rollback"}:
        raise ValueError("Profile activation reason is invalid")
    _integer(activation["sequence"], "profile.activation.sequence")
    entries = profile["versions"]
    if not isinstance(entries, list) or not entries:
        raise ValueError("profile.versions must be non-empty")
    expected_directories: set[str] = set()
    version_numbers: list[int] = []
    for index, raw in enumerate(entries):
        entry = _exact_object(raw, VERSION_ENTRY_KEYS, f"profile.versions[{index}]")
        version = _integer(entry["version"], f"profile.versions[{index}].version")
        if version in version_numbers:
            raise ValueError("profile.versions contains duplicate versions")
        version_numbers.append(version)
        expected_manifest = f"versions/v{version}/version.json"
        if entry["manifest"] != expected_manifest:
            raise ValueError("Profile version manifest path drifted")
        digest = entry["manifest_sha256"]
        if not isinstance(digest, str) or not SHA256.fullmatch(digest):
            raise ValueError("Profile version manifest digest is invalid")
        version_root = profile_root / "versions" / f"v{version}"
        manifest = validate_version(
            version_root,
            expected_profile_id=profile_id,
            expected_display_name=display_name,
            expected_aliases=aliases,
        )
        if _sha256(version_root / "version.json") != digest or manifest["version"] != version:
            raise ValueError("Profile version manifest hash drifted")
        expected_directories.add(f"v{version}")
    actual_versions = {path.name for path in (profile_root / "versions").iterdir()}
    if actual_versions != expected_directories:
        raise ValueError("Profile versions directory has missing or extra entries")
    if version_numbers != sorted(version_numbers) or version_numbers != list(range(1, max(version_numbers) + 1)):
        raise ValueError("Profile versions must be contiguous and ordered from v1")
    if active_version not in version_numbers:
        raise ValueError("Profile active_version does not exist")
    return profile


def _profile_roots(home: Path) -> list[Path]:
    profiles_root = home / "profiles"
    roots: list[Path] = []
    for path in sorted(profiles_root.iterdir()):
        if path.name.startswith(".stage-"):
            raise ValueError(f"Incomplete profile transaction requires inspection: {path}")
        if path.is_symlink() or not path.is_dir():
            raise ValueError(f"Unexpected profile-store entry: {path}")
        roots.append(path)
    return roots


def _identity_keys(profile: dict[str, Any]) -> dict[str, str]:
    values = {
        profile["profile_id"]: "profile_id",
        profile["display_name"]: "display_name",
        **{alias: "alias" for alias in profile["aliases"]},
    }
    return {_normalize_identity(value): basis for value, basis in values.items()}


def _validated_profiles(home: Path) -> list[tuple[Path, dict[str, Any]]]:
    profiles: list[tuple[Path, dict[str, Any]]] = []
    identities: dict[str, str] = {}
    for root in _profile_roots(home):
        profile = validate_profile(root)
        for key in _identity_keys(profile):
            previous = identities.get(key)
            if previous is not None and previous != profile["profile_id"]:
                raise ValueError(
                    f"Stored corporate identity collision between {previous} and {profile['profile_id']}"
                )
            identities[key] = profile["profile_id"]
        profiles.append((root, profile))
    return profiles


def _assert_identity_available(
    profiles: list[tuple[Path, dict[str, Any]]],
    *,
    profile_id: str,
    display_name: str,
    aliases: list[str],
) -> None:
    requested = {
        _normalize_identity(profile_id),
        _normalize_identity(display_name),
        *(_normalize_identity(alias) for alias in aliases),
    }
    for _, profile in profiles:
        overlap = requested & set(_identity_keys(profile))
        if overlap:
            raise ValueError(
                f"Corporate identity or alias conflicts with profile {profile['profile_id']}"
            )


def create_profile(
    *,
    home: Path | None,
    profile_id: str,
    display_name: str,
    aliases: list[str],
    handoff: Path,
    theme: Path,
) -> dict[str, Any]:
    store = resolve_home(home, create=True)
    normalized_id = _profile_id(profile_id)
    normalized_name = _text(display_name, "display_name", 80)
    normalized_aliases = _aliases(aliases, normalized_name)
    with _store_lock(store):
        profiles = _validated_profiles(store)
        _assert_identity_available(
            profiles,
            profile_id=normalized_id,
            display_name=normalized_name,
            aliases=normalized_aliases,
        )
        final = store / "profiles" / normalized_id
        if final.exists():
            raise ValueError(f"Profile already exists: {normalized_id}")
        transaction = Path(
            tempfile.mkdtemp(prefix=".stage-create-", dir=store / "profiles")
        )
        stage = transaction / normalized_id
        moved = False
        try:
            stage.mkdir()
            (stage / "versions").mkdir()
            timestamp = _now()
            version_root = stage / "versions" / "v1"
            version_root.mkdir()
            version_manifest = _build_version(
                version_root,
                profile_id=normalized_id,
                display_name=normalized_name,
                aliases=normalized_aliases,
                version=1,
                handoff_path=handoff,
                source_theme_dir=theme,
                created_at=timestamp,
            )
            profile = {
                "schema_version": PROFILE_SCHEMA_VERSION,
                "profile_id": normalized_id,
                "display_name": normalized_name,
                "aliases": normalized_aliases,
                "status": "active",
                "active_version": 1,
                "created_at": timestamp,
                "updated_at": timestamp,
                "activation": {
                    "version": 1,
                    "activated_at": timestamp,
                    "reason": "created",
                    "sequence": 1,
                },
                "versions": [_version_entry(version_root, version_manifest)],
            }
            _atomic_json(stage / "profile.json", profile)
            validate_profile(stage)
            os.replace(stage, final)
            transaction.rmdir()
            moved = True
        finally:
            if transaction.exists():
                shutil.rmtree(transaction)
    return {
        "schema_version": STORE_SCHEMA_VERSION,
        "status": "created",
        "profile_id": normalized_id,
        "active_version": 1,
        "home_path": f"profiles/{normalized_id}",
    }


def update_profile(
    *,
    home: Path | None,
    profile_id: str,
    handoff: Path,
    theme: Path,
) -> dict[str, Any]:
    store = resolve_home(home)
    normalized_id = _profile_id(profile_id)
    with _store_lock(store):
        profile_root = store / "profiles" / normalized_id
        profile = validate_profile(profile_root)
        if profile["status"] != "active":
            raise ValueError("Archived profiles cannot receive new versions")
        old_profile_payload = (profile_root / "profile.json").read_bytes()
        version = max(entry["version"] for entry in profile["versions"]) + 1
        final_version = profile_root / "versions" / f"v{version}"
        transactions_root = store / ".profile-store-transactions"
        if transactions_root.is_symlink():
            raise ValueError("Profile transaction root must not be a symlink")
        transactions_root.mkdir(exist_ok=True)
        transaction = Path(
            tempfile.mkdtemp(
                prefix=f"update-{normalized_id}-v{version}-", dir=transactions_root
            )
        )
        stage = transaction / f"v{version}"
        try:
            stage.mkdir()
            timestamp = _now()
            manifest = _build_version(
                stage,
                profile_id=normalized_id,
                display_name=profile["display_name"],
                aliases=profile["aliases"],
                version=version,
                handoff_path=handoff,
                source_theme_dir=theme,
                created_at=timestamp,
            )
            active_manifest = _load_json(
                profile_root / "versions" / f"v{profile['active_version']}" / "version.json",
                "Active profile version",
            )
            if (
                manifest["hashes"]["vi_contract_sha256"]
                == active_manifest["hashes"]["vi_contract_sha256"]
                and manifest["hashes"]["reference_images_sha256"]
                == active_manifest["hashes"]["reference_images_sha256"]
            ):
                raise ValueError("Permanent update must change the confirmed corporate VI or references")
            validate_version(
                stage,
                expected_profile_id=normalized_id,
                expected_display_name=profile["display_name"],
                expected_aliases=profile["aliases"],
            )
            profile["versions"].append(_version_entry(stage, manifest))
            profile["active_version"] = version
            profile["updated_at"] = timestamp
            profile["activation"] = {
                "version": version,
                "activated_at": timestamp,
                "reason": "updated",
                "sequence": profile["activation"]["sequence"] + 1,
            }
            new_profile_payload = _json_bytes(profile)
            _atomic_write(transaction / "old-profile.json", old_profile_payload)
            _atomic_write(transaction / "new-profile.json", new_profile_payload)
            _atomic_json(
                transaction / "journal.json",
                {
                    "schema_version": TRANSACTION_SCHEMA_VERSION,
                    "operation": "update",
                    "profile_id": normalized_id,
                    "version": version,
                    "old_profile_sha256": _bytes_sha256(old_profile_payload),
                    "new_profile_sha256": _bytes_sha256(new_profile_payload),
                },
            )
            os.replace(stage, final_version)
            _atomic_json(profile_root / "profile.json", profile)
            validate_profile(profile_root)
            _atomic_write(transaction / "committed", b"committed\n")
            _remove_managed_directory(transaction, "Completed profile transaction")
            try:
                transactions_root.rmdir()
            except OSError:
                pass
        except BaseException:
            try:
                _recover_update_transactions(store)
            except BaseException as recovery_error:
                raise RuntimeError(
                    "Profile update failed and automatic rollback could not complete; "
                    "the recovery journal was preserved"
                ) from recovery_error
            raise
    return {
        "schema_version": STORE_SCHEMA_VERSION,
        "status": "updated",
        "profile_id": normalized_id,
        "active_version": version,
        "previous_version": version - 1,
    }


def list_profiles(home: Path | None = None, *, include_archived: bool = False) -> dict[str, Any]:
    candidate = _home_candidate(home)
    if not candidate.exists() or not (candidate / "profiles").exists():
        return {"schema_version": STORE_SCHEMA_VERSION, "status": "ok", "profiles": []}
    store = resolve_home(home)
    with _store_lock(store):
        profiles = []
        for _, profile in _validated_profiles(store):
            if profile["status"] == "archived" and not include_archived:
                continue
            profiles.append(
                {
                    "profile_id": profile["profile_id"],
                    "display_name": profile["display_name"],
                    "aliases": profile["aliases"],
                    "status": profile["status"],
                    "active_version": profile["active_version"],
                    "versions": [entry["version"] for entry in profile["versions"]],
                }
            )
    return {"schema_version": STORE_SCHEMA_VERSION, "status": "ok", "profiles": profiles}


def show_profile(home: Path | None, profile_id: str) -> dict[str, Any]:
    store = resolve_home(home)
    normalized_id = _profile_id(profile_id)
    with _store_lock(store):
        root = store / "profiles" / normalized_id
        profile = validate_profile(root)
        versions = [
            _load_json(
                root / "versions" / f"v{entry['version']}" / "version.json",
                "Profile version",
            )
            for entry in profile["versions"]
        ]
    return {
        "schema_version": STORE_SCHEMA_VERSION,
        "status": "ok",
        "profile": profile,
        "version_manifests": versions,
    }


def _resolve_profiles_unlocked(
    home: Path,
    identities: list[str],
    *,
    include_archived: bool = False,
) -> dict[str, Any]:
    if not identities or len(identities) > 12:
        raise ValueError("resolve requires one to twelve explicit identity candidates")
    normalized = [_normalize_identity(_text(value, "identity", 80)) for value in identities]
    matches: dict[str, dict[str, Any]] = {}
    for _, profile in _validated_profiles(home):
        if profile["status"] == "archived" and not include_archived:
            continue
        keys = _identity_keys(profile)
        bases: list[str] = []
        matched_identities: list[str] = []
        for raw, key in zip(identities, normalized, strict=True):
            basis = keys.get(key)
            if basis is not None:
                bases.append(basis)
                matched_identities.append(raw)
        if bases:
            matches[profile["profile_id"]] = {
                "profile_id": profile["profile_id"],
                "display_name": profile["display_name"],
                "active_version": profile["active_version"],
                "matched_identities": matched_identities,
                "basis": sorted(set(bases)),
            }
    candidates = list(matches.values())
    if not candidates:
        status = "not_found"
    elif len(candidates) == 1:
        status = "resolved"
    else:
        status = "ambiguous"
    return {
        "schema_version": STORE_SCHEMA_VERSION,
        "status": status,
        "identities": identities,
        "candidates": candidates,
        "requires_single_selection_question": status == "ambiguous",
    }


def resolve_profiles(
    home: Path | None,
    identities: list[str],
    *,
    include_archived: bool = False,
) -> dict[str, Any]:
    if not identities or len(identities) > 12:
        raise ValueError("resolve requires one to twelve explicit identity candidates")
    candidate = _home_candidate(home)
    if not candidate.exists() or not (candidate / "profiles").exists():
        return {
            "schema_version": STORE_SCHEMA_VERSION,
            "status": "not_found",
            "identities": identities,
            "candidates": [],
            "requires_single_selection_question": False,
        }
    store = resolve_home(home)
    with _store_lock(store):
        return _resolve_profiles_unlocked(
            store, identities, include_archived=include_archived
        )


def _selected_profile(
    home: Path,
    *,
    identities: list[str] | None,
    profile_id: str | None,
) -> tuple[Path, dict[str, Any], dict[str, Any]]:
    if profile_id is not None:
        normalized_id = _profile_id(profile_id)
        root = home / "profiles" / normalized_id
        profile = validate_profile(root)
        resolution = {"identities": identities or [], "basis": ["explicit_selection"]}
        return root, profile, resolution
    result = _resolve_profiles_unlocked(home, identities or [])
    if result["status"] != "resolved":
        raise ValueError(
            "Corporate identity did not resolve uniquely; ask one selection question when candidates are ambiguous"
        )
    candidate = result["candidates"][0]
    root = home / "profiles" / candidate["profile_id"]
    profile = validate_profile(root)
    resolution = {
        "identities": identities or [],
        "basis": candidate["basis"],
    }
    return root, profile, resolution


def bind_profile(
    *,
    home: Path | None,
    output: Path,
    task_id: str,
    target_mode: str,
    identities: list[str] | None = None,
    profile_id: str | None = None,
    temporary_override: bool = False,
    replace: bool = False,
) -> dict[str, Any]:
    store = resolve_home(home)
    if (identities is None) == (profile_id is None):
        raise ValueError("bind requires exactly one of identities or profile_id")
    if target_mode not in {"reading", "presentation"}:
        raise ValueError("target_mode must be reading or presentation")
    destination = output.expanduser()
    if destination.resolve().is_relative_to(store):
        raise ValueError("Binding output must stay outside TAOHTML_HOME")
    with _store_lock(store):
        root, profile, resolution = _selected_profile(
            store, identities=identities, profile_id=profile_id
        )
        if profile["status"] != "active":
            raise ValueError("Archived profiles cannot be bound")
        version = profile["active_version"]
        version_root = root / "versions" / f"v{version}"
        manifest = validate_version(
            version_root,
            expected_profile_id=profile["profile_id"],
            expected_display_name=profile["display_name"],
            expected_aliases=profile["aliases"],
        )
        customer_notice = (
            f"本次不沿用【{profile['display_name']} 企业模板 v{version}】；默认档案保持不变。"
            if temporary_override
            else f"本次沿用【{profile['display_name']} 企业模板 v{version}】；如需更换请直接说明。"
        )
        binding = {
            "schema_version": BINDING_SCHEMA_VERSION,
            "task_id": _text(task_id, "task_id", 160),
            "profile_id": profile["profile_id"],
            "profile_display_name": profile["display_name"],
            "version": version,
            "active_version_at_bind": version,
            "target_mode": target_mode,
            "theme_home_path": f"profiles/{profile['profile_id']}/versions/v{version}/assets/project-theme",
            "theme_fingerprint": manifest["hashes"]["theme_fingerprint"],
            "vi_contract_sha256": manifest["hashes"]["vi_contract_sha256"],
            "reference_images_sha256": manifest["hashes"]["reference_images_sha256"],
            "profile_record_sha256": _sha256(root / "profile.json"),
            "version_manifest_sha256": _sha256(version_root / "version.json"),
            "resolution": resolution,
            "temporary_override": bool(temporary_override),
            "customer_notice": customer_notice,
            "bound_at": _now(),
        }
        if destination.exists() and not replace:
            raise ValueError(f"Binding output already exists: {destination}")
        if destination.is_symlink():
            raise ValueError(f"Binding output must not be a symlink: {destination}")
        _atomic_json(destination, binding)
    return {
        "schema_version": STORE_SCHEMA_VERSION,
        "status": "bound",
        "binding": binding,
        "binding_path": str(destination.resolve()),
    }


def validate_binding(
    binding_path: Path,
    *,
    home: Path | None = None,
) -> dict[str, Any]:
    store = resolve_home(home)
    with _store_lock(store):
        path = _regular_file(binding_path, "Profile-use binding")
        binding = _exact_object(
            _load_json(path, "Profile-use binding"), BINDING_KEYS, "binding"
        )
        if binding["schema_version"] != BINDING_SCHEMA_VERSION:
            raise ValueError(f"binding.schema_version must be {BINDING_SCHEMA_VERSION}")
        profile_id = _profile_id(binding["profile_id"])
        root = store / "profiles" / profile_id
        profile = validate_profile(root)
        version = _integer(binding["version"], "binding.version")
        if profile["status"] != "active":
            raise ValueError("Bound profile is no longer active")
        if binding["active_version_at_bind"] != version or profile["active_version"] != version:
            raise ValueError("Bound profile active version changed after binding")
        if binding["profile_display_name"] != profile["display_name"]:
            raise ValueError("Bound corporate identity drifted")
        if binding["profile_record_sha256"] != _sha256(root / "profile.json"):
            raise ValueError("Bound profile record changed after binding")
        version_root = root / "versions" / f"v{version}"
        manifest = validate_version(
            version_root,
            expected_profile_id=profile_id,
            expected_display_name=profile["display_name"],
            expected_aliases=profile["aliases"],
        )
        if binding["version_manifest_sha256"] != _sha256(version_root / "version.json"):
            raise ValueError("Bound version manifest changed after binding")
        if binding["theme_fingerprint"] != manifest["hashes"]["theme_fingerprint"]:
            raise ValueError("Bound theme fingerprint changed after binding")
        if binding["vi_contract_sha256"] != manifest["hashes"]["vi_contract_sha256"]:
            raise ValueError("Bound VI hash changed after binding")
        if binding["reference_images_sha256"] != manifest["hashes"]["reference_images_sha256"]:
            raise ValueError("Bound reference hashes changed after binding")
        expected_home_path = f"profiles/{profile_id}/versions/v{version}/assets/project-theme"
        if binding["theme_home_path"] != expected_home_path:
            raise ValueError("Bound theme path drifted")
        if binding["target_mode"] not in {"reading", "presentation"}:
            raise ValueError("Binding target_mode is invalid")
        resolution = _exact_object(binding["resolution"], RESOLUTION_KEYS, "binding.resolution")
        if not isinstance(resolution["identities"], list) or not isinstance(resolution["basis"], list) or not resolution["basis"]:
            raise ValueError("Binding resolution basis is incomplete")
        _text(binding["task_id"], "binding.task_id")
        _text(binding["customer_notice"], "binding.customer_notice", 240)
        _text(binding["bound_at"], "binding.bound_at")
        theme_path = root / "versions" / f"v{version}" / "assets" / "project-theme"
    return {
        "schema_version": STORE_SCHEMA_VERSION,
        "status": "valid_override" if binding["temporary_override"] else "valid_reuse",
        "binding": binding,
        "theme_path": theme_path,
    }


def _activate_version_unlocked(
    store: Path, normalized_id: str, target: int, reason: str
) -> dict[str, Any]:
    root = store / "profiles" / normalized_id
    profile = validate_profile(root)
    if profile["status"] != "active":
        raise ValueError("Archived profiles cannot change active version")
    validate_version(
        root / "versions" / f"v{target}",
        expected_profile_id=normalized_id,
        expected_display_name=profile["display_name"],
        expected_aliases=profile["aliases"],
    )
    previous = profile["active_version"]
    timestamp = _now()
    profile["active_version"] = target
    profile["updated_at"] = timestamp
    profile["activation"] = {
        "version": target,
        "activated_at": timestamp,
        "reason": reason,
        "sequence": profile["activation"]["sequence"] + 1,
    }
    _atomic_json(root / "profile.json", profile)
    validate_profile(root)
    return {
        "schema_version": STORE_SCHEMA_VERSION,
        "status": "activated",
        "profile_id": normalized_id,
        "previous_version": previous,
        "active_version": target,
        "reason": reason,
    }


def activate_version(
    home: Path | None,
    profile_id: str,
    version: int,
    *,
    reason: str = "manual",
) -> dict[str, Any]:
    store = resolve_home(home)
    normalized_id = _profile_id(profile_id)
    target = _integer(version, "version")
    if reason not in {"manual", "rollback"}:
        raise ValueError("Activation reason must be manual or rollback")
    with _store_lock(store):
        return _activate_version_unlocked(store, normalized_id, target, reason)


def rollback_profile(
    home: Path | None,
    profile_id: str,
    version: int | None = None,
) -> dict[str, Any]:
    store = resolve_home(home)
    normalized_id = _profile_id(profile_id)
    with _store_lock(store):
        profile = validate_profile(store / "profiles" / normalized_id)
        if version is None:
            candidates = [
                entry["version"]
                for entry in profile["versions"]
                if entry["version"] < profile["active_version"]
            ]
            if not candidates:
                raise ValueError("No earlier corporate profile version is available")
            version = max(candidates)
        target = _integer(version, "version")
        if target == profile["active_version"]:
            raise ValueError("Rollback target must differ from the active version")
        return _activate_version_unlocked(store, normalized_id, target, "rollback")


def archive_profile(home: Path | None, profile_id: str) -> dict[str, Any]:
    store = resolve_home(home)
    normalized_id = _profile_id(profile_id)
    with _store_lock(store):
        root = store / "profiles" / normalized_id
        profile = validate_profile(root)
        if profile["status"] == "archived":
            raise ValueError("Profile is already archived")
        profile["status"] = "archived"
        profile["updated_at"] = _now()
        _atomic_json(root / "profile.json", profile)
        validate_profile(root)
    return {
        "schema_version": STORE_SCHEMA_VERSION,
        "status": "archived",
        "profile_id": normalized_id,
        "recoverable": True,
    }


def restore_profile(home: Path | None, profile_id: str) -> dict[str, Any]:
    store = resolve_home(home)
    normalized_id = _profile_id(profile_id)
    with _store_lock(store):
        root = store / "profiles" / normalized_id
        profile = validate_profile(root)
        if profile["status"] != "archived":
            raise ValueError("Only an archived profile can be restored")
        profile["status"] = "active"
        profile["updated_at"] = _now()
        _atomic_json(root / "profile.json", profile)
        validate_profile(root)
    return {
        "schema_version": STORE_SCHEMA_VERSION,
        "status": "restored",
        "profile_id": normalized_id,
        "active_version": profile["active_version"],
    }


def _zip_info(name: str) -> zipfile.ZipInfo:
    info = zipfile.ZipInfo(name, date_time=(1980, 1, 1, 0, 0, 0))
    info.compress_type = zipfile.ZIP_DEFLATED
    info.create_system = 3
    info.external_attr = (0o100644 & 0xFFFF) << 16
    return info


def export_profile(home: Path | None, profile_id: str, output: Path) -> dict[str, Any]:
    store = resolve_home(home)
    normalized_id = _profile_id(profile_id)
    destination = output.expanduser()
    if destination.resolve().is_relative_to(store):
        raise ValueError("Export output must stay outside TAOHTML_HOME")
    with _store_lock(store):
        root = store / "profiles" / normalized_id
        validate_profile(root)
        if destination.exists() or destination.is_symlink():
            raise ValueError(f"Export output already exists: {destination}")
        destination.parent.mkdir(parents=True, exist_ok=True)
        records: list[dict[str, object]] = []
        payloads: dict[str, bytes] = {}
        for path in sorted(root.rglob("*")):
            if path.is_symlink():
                raise ValueError(f"Profile export refuses symlinks: {path}")
            if not path.is_file():
                continue
            name = f"profile/{path.relative_to(root).as_posix()}"
            payload = path.read_bytes()
            payloads[name] = payload
            records.append(
                {"path": name, "sha256": _bytes_sha256(payload), "size": len(payload)}
            )
        package = {
            "schema_version": PACKAGE_SCHEMA_VERSION,
            "profile_id": normalized_id,
            "exported_at": _now(),
            "files": records,
        }
        temporary = destination.with_name(f".{destination.name}.tmp-{uuid.uuid4().hex}")
        try:
            with zipfile.ZipFile(temporary, "x") as archive:
                archive.writestr(
                    _zip_info("taohtml-profile-package.json"), _json_bytes(package)
                )
                for name in sorted(payloads):
                    archive.writestr(_zip_info(name), payloads[name])
            os.replace(temporary, destination)
        finally:
            if temporary.exists():
                temporary.unlink()
    return {
        "schema_version": STORE_SCHEMA_VERSION,
        "status": "exported",
        "profile_id": normalized_id,
        "output": str(destination.resolve()),
        "files": len(records),
    }


def _zip_member_is_symlink(info: zipfile.ZipInfo) -> bool:
    mode = (info.external_attr >> 16) & 0xFFFF
    return stat.S_IFMT(mode) == stat.S_IFLNK


def import_profile(home: Path | None, package_path: Path) -> dict[str, Any]:
    store = resolve_home(home, create=True)
    package_file = _regular_file(package_path, "Profile package")
    with _store_lock(store), zipfile.ZipFile(package_file) as archive:
        infos = archive.infolist()
        if len(infos) > MAX_PACKAGE_FILES or sum(info.file_size for info in infos) > MAX_PACKAGE_BYTES:
            raise ValueError("Profile package exceeds the safe file-count or uncompressed-size limit")
        names = [info.filename for info in infos]
        if len(names) != len(set(names)):
            raise ValueError("Profile package contains duplicate archive entries")
        if len({name.casefold() for name in names}) != len(names):
            raise ValueError("Profile package contains case-colliding archive entries")
        for info in infos:
            _safe_package_path(info.filename, "archive entry")
            if info.is_dir():
                raise ValueError("Profile package must contain files only, not directory entries")
            if _zip_member_is_symlink(info):
                raise ValueError(f"Profile package contains a symlink: {info.filename}")
            if info.flag_bits & 0x1:
                raise ValueError(f"Profile package contains an encrypted entry: {info.filename}")
        if "taohtml-profile-package.json" not in names:
            raise ValueError("Profile package manifest is missing")
        package = _exact_object(
            json.loads(archive.read("taohtml-profile-package.json").decode("utf-8")),
            PACKAGE_KEYS,
            "package",
        )
        if package["schema_version"] != PACKAGE_SCHEMA_VERSION:
            raise ValueError(f"package.schema_version must be {PACKAGE_SCHEMA_VERSION}")
        profile_id = _profile_id(package["profile_id"])
        _text(package["exported_at"], "package.exported_at")
        raw_files = package["files"]
        if not isinstance(raw_files, list) or not raw_files:
            raise ValueError("package.files must be a non-empty complete file list")
        expected: dict[str, dict[str, Any]] = {}
        for index, raw in enumerate(raw_files):
            record = _exact_object(raw, PACKAGE_FILE_KEYS, f"package.files[{index}]")
            relative = _safe_package_path(record["path"], f"package.files[{index}].path")
            if len(relative.parts) < 2 or relative.parts[0] != "profile":
                raise ValueError("Every imported file must live below profile/")
            name = relative.as_posix()
            if name in expected:
                raise ValueError("package.files contains duplicate paths")
            digest = record["sha256"]
            if not isinstance(digest, str) or not SHA256.fullmatch(digest):
                raise ValueError("package.files sha256 is invalid")
            _integer(record["size"], f"package.files[{index}].size", 0)
            expected[name] = record
        actual = set(names) - {"taohtml-profile-package.json"}
        if actual != set(expected):
            missing = ", ".join(sorted(set(expected) - actual)) or "none"
            extra = ", ".join(sorted(actual - set(expected))) or "none"
            raise ValueError(f"Profile package file list drifted; missing={missing}; extra={extra}")
        final = store / "profiles" / profile_id
        if final.exists():
            raise ValueError(f"Profile already exists: {profile_id}")
        profiles = _validated_profiles(store)
        transaction = Path(
            tempfile.mkdtemp(prefix=".stage-import-", dir=store / "profiles")
        )
        stage = transaction / profile_id
        moved = False
        try:
            stage.mkdir()
            for name, record in expected.items():
                payload = archive.read(name)
                if len(payload) != record["size"] or _bytes_sha256(payload) != record["sha256"]:
                    raise ValueError(f"Imported file hash or size drifted: {name}")
                relative = PurePosixPath(name)
                target = stage.joinpath(*relative.parts[1:])
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_bytes(payload)
            profile = validate_profile(stage)
            _assert_identity_available(
                profiles,
                profile_id=profile_id,
                display_name=profile["display_name"],
                aliases=profile["aliases"],
            )
            os.replace(stage, final)
            transaction.rmdir()
            moved = True
        finally:
            if transaction.exists():
                shutil.rmtree(transaction)
    return {
        "schema_version": STORE_SCHEMA_VERSION,
        "status": "imported",
        "profile_id": profile_id,
        "active_version": profile["active_version"],
    }


def _emit(result: object) -> None:
    print(json.dumps(result, ensure_ascii=False, indent=2, default=str))


def _add_home(parser: argparse.ArgumentParser) -> None:
    parser.add_argument(
        "--home",
        type=Path,
        help="Override TAOHTML_HOME; defaults to the environment variable, then ~/.taohtml.",
    )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Manage explicit TaoHtml corporate-template profiles."
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    create = subparsers.add_parser("create", help="Create v1 from a confirmed corporate VI and validated theme.")
    _add_home(create)
    create.add_argument("--profile-id", required=True)
    create.add_argument("--display-name", required=True)
    create.add_argument("--alias", action="append", default=[])
    create.add_argument("--handoff", type=Path, required=True)
    create.add_argument("--theme", type=Path, required=True)

    update = subparsers.add_parser("update", help="Create an immutable next version and atomically activate it.")
    _add_home(update)
    update.add_argument("--profile-id", required=True)
    update.add_argument("--handoff", type=Path, required=True)
    update.add_argument("--theme", type=Path, required=True)

    listing = subparsers.add_parser("list", help="List validated corporate profiles.")
    _add_home(listing)
    listing.add_argument("--include-archived", action="store_true")

    show = subparsers.add_parser("show", help="Show one validated profile and all version manifests.")
    _add_home(show)
    show.add_argument("--profile-id", required=True)

    resolve = subparsers.add_parser("resolve", help="Resolve exact enterprise identity candidates without guessing.")
    _add_home(resolve)
    resolve.add_argument("--identity", action="append", required=True)

    bind = subparsers.add_parser("bind", help="Write a task-local, live-validated profile-use binding.")
    _add_home(bind)
    selector = bind.add_mutually_exclusive_group(required=True)
    selector.add_argument("--identity", action="append")
    selector.add_argument("--profile-id")
    bind.add_argument("--task-id", required=True)
    bind.add_argument("--target-mode", choices=("reading", "presentation"), required=True)
    bind.add_argument("--output", type=Path, required=True)
    bind.add_argument("--temporary-override", action="store_true")
    bind.add_argument("--replace", action="store_true")

    validate = subparsers.add_parser("validate-binding", help="Revalidate a binding against the live profile and theme.")
    _add_home(validate)
    validate.add_argument("--binding", type=Path, required=True)

    activate = subparsers.add_parser("activate", help="Atomically activate an existing immutable version.")
    _add_home(activate)
    activate.add_argument("--profile-id", required=True)
    activate.add_argument("--version", type=int, required=True)

    rollback = subparsers.add_parser("rollback", help="Rollback to an earlier retained version.")
    _add_home(rollback)
    rollback.add_argument("--profile-id", required=True)
    rollback.add_argument("--version", type=int)

    archive = subparsers.add_parser("archive", help="Archive without deleting profile assets.")
    _add_home(archive)
    archive.add_argument("--profile-id", required=True)

    restore = subparsers.add_parser("restore", help="Restore an archived profile without changing its active version.")
    _add_home(restore)
    restore.add_argument("--profile-id", required=True)

    export = subparsers.add_parser("export", help="Export a complete portable profile package.")
    _add_home(export)
    export.add_argument("--profile-id", required=True)
    export.add_argument("--output", type=Path, required=True)

    import_command = subparsers.add_parser("import", help="Strictly validate and import a portable profile package.")
    _add_home(import_command)
    import_command.add_argument("--package", type=Path, required=True)
    return parser


def main() -> int:
    args = build_parser().parse_args()
    try:
        if args.command == "create":
            result = create_profile(
                home=args.home,
                profile_id=args.profile_id,
                display_name=args.display_name,
                aliases=args.alias,
                handoff=args.handoff,
                theme=args.theme,
            )
        elif args.command == "update":
            result = update_profile(
                home=args.home,
                profile_id=args.profile_id,
                handoff=args.handoff,
                theme=args.theme,
            )
        elif args.command == "list":
            result = list_profiles(args.home, include_archived=args.include_archived)
        elif args.command == "show":
            result = show_profile(args.home, args.profile_id)
        elif args.command == "resolve":
            result = resolve_profiles(args.home, args.identity)
        elif args.command == "bind":
            result = bind_profile(
                home=args.home,
                output=args.output,
                task_id=args.task_id,
                target_mode=args.target_mode,
                identities=args.identity,
                profile_id=args.profile_id,
                temporary_override=args.temporary_override,
                replace=args.replace,
            )
        elif args.command == "validate-binding":
            result = validate_binding(args.binding, home=args.home)
        elif args.command == "activate":
            result = activate_version(args.home, args.profile_id, args.version)
        elif args.command == "rollback":
            result = rollback_profile(args.home, args.profile_id, args.version)
        elif args.command == "archive":
            result = archive_profile(args.home, args.profile_id)
        elif args.command == "restore":
            result = restore_profile(args.home, args.profile_id)
        elif args.command == "export":
            result = export_profile(args.home, args.profile_id, args.output)
        elif args.command == "import":
            result = import_profile(args.home, args.package)
        else:
            raise AssertionError(args.command)
    except (OSError, ValueError, zipfile.BadZipFile) as exc:
        _emit(
            {
                "schema_version": STORE_SCHEMA_VERSION,
                "status": "invalid",
                "error": f"{type(exc).__name__}: {exc}",
            }
        )
        return 2
    _emit(result)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
