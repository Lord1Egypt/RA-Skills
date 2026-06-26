#!/usr/bin/env python3
"""Shared helpers for the responses third-party prompt-cache patch skill."""

from __future__ import annotations

import re
import shutil
import subprocess
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Iterable, Sequence

SKILL_SLUG = "responses-third-party-prompt-cache-patch"
PATCH_MARKER = "openclaw-skill:responses-third-party-prompt-cache-patch"
BACKUP_TOKEN = f"bak.{SKILL_SLUG}"
TARGET_FUNCTION_SIGNATURE = "function shouldStripResponsesPromptCache(model) {"
TARGET_RETURN = "return !isDirectOpenAIBaseUrl(model.baseUrl);"
PATCHED_RETURN = f"return false; /* {PATCH_MARKER} */"
PREFERRED_PATTERNS: Sequence[str] = ("pi-embedded-*.js",)
FALLBACK_PATTERNS: Sequence[str] = ("*.js",)
SYSTEMD_UNIT_NAME = "openclaw-gateway"
SYSTEMD_SERVICE_PATH = Path.home() / ".config" / "systemd" / "user" / f"{SYSTEMD_UNIT_NAME}.service"
DIST_INDEX_PATTERN = re.compile(r'([A-Za-z0-9_./~+-]+/dist/index\.js)')


class PatchError(RuntimeError):
    """Raised when the patch workflow cannot continue safely."""


@dataclass
class BundleInspection:
    path: Path
    text: str
    function_start: int
    function_end: int
    function_block: str
    state: str


def resolve_openclaw_root(explicit_root: str | None) -> Path:
    """Resolve the OpenClaw installation root.

    Resolution order:
    1. Explicit ``--root`` override
    2. Active gateway service command / systemd unit ExecStart
    3. ``openclaw`` executable on PATH

    When the gateway service and CLI point at different installs, prefer the
    running gateway root because that is the bundle the operator almost always
    intends to patch. Emit a clear note so the operator understands why.
    """

    if explicit_root:
        root = Path(explicit_root).expanduser().resolve()
        ensure_dist_dir(root)
        return root

    candidates: list[tuple[str, Path]] = []

    gateway_candidate = _resolve_gateway_root()
    if gateway_candidate is not None:
        candidates.append(gateway_candidate)

    executable_candidate = _resolve_root_from_openclaw_executable()
    if executable_candidate is not None:
        candidates.append(executable_candidate)

    if not candidates:
        checked_summary = ", ".join(_checked_location_hints())
        raise PatchError(
            "Could not locate the installed OpenClaw root automatically. "
            "Pass --root /path/to/openclaw. Checked: "
            f"{checked_summary}"
        )

    unique_roots: dict[Path, list[str]] = {}
    for source, root in candidates:
        unique_roots.setdefault(root, []).append(source)

    gateway_root = gateway_candidate[1] if gateway_candidate is not None else None
    if gateway_root is not None:
        if len(unique_roots) > 1:
            other_roots = [
                f"{root} ({', '.join(sources)})"
                for root, sources in unique_roots.items()
                if root != gateway_root
            ]
            print(
                "Detected multiple OpenClaw installs. "
                f"Using active gateway root {gateway_root} "
                f"({', '.join(unique_roots[gateway_root])}). "
                f"Other detected roots: {'; '.join(other_roots)}. "
                "Pass --root to override."
            )
        return gateway_root

    if len(unique_roots) == 1:
        return next(iter(unique_roots))

    candidates_summary = "; ".join(
        f"{root} ({', '.join(sources)})" for root, sources in unique_roots.items()
    )
    raise PatchError(
        "Detected multiple OpenClaw installs but could not identify the active gateway root automatically. "
        f"Pass --root /path/to/openclaw. Candidates: {candidates_summary}"
    )


def _checked_location_hints() -> list[str]:
    hints = [str(SYSTEMD_SERVICE_PATH), "systemctl --user show openclaw-gateway", "which openclaw"]
    return hints


def _resolve_gateway_root() -> tuple[str, Path] | None:
    systemctl_candidate = _resolve_root_from_systemctl()
    if systemctl_candidate is not None:
        return systemctl_candidate

    service_file_candidate = _resolve_root_from_service_file()
    if service_file_candidate is not None:
        return service_file_candidate

    return None


def _resolve_root_from_systemctl() -> tuple[str, Path] | None:
    try:
        result = subprocess.run(
            ["systemctl", "--user", "show", SYSTEMD_UNIT_NAME, "--property=ExecStart", "--value"],
            capture_output=True,
            text=True,
            check=False,
        )
    except FileNotFoundError:
        return None

    text = "\n".join(part for part in [result.stdout, result.stderr] if part)
    root = _extract_openclaw_root_from_text(text)
    if root is None:
        return None
    return ("running gateway service", root)


def _resolve_root_from_service_file() -> tuple[str, Path] | None:
    if not SYSTEMD_SERVICE_PATH.is_file():
        return None

    try:
        text = SYSTEMD_SERVICE_PATH.read_text(encoding="utf-8")
    except OSError:
        return None

    root = _extract_openclaw_root_from_text(text)
    if root is None:
        return None
    return (f"systemd unit file {SYSTEMD_SERVICE_PATH}", root)


def _resolve_root_from_openclaw_executable() -> tuple[str, Path] | None:
    executable = shutil.which("openclaw")
    if not executable:
        return None

    resolved = Path(executable).expanduser().resolve()
    candidates = [
        resolved.parent,
        resolved.parent.parent,
        resolved.parent.parent / "lib" / "node_modules" / "openclaw",
    ]
    for candidate in candidates:
        if (candidate / "dist").is_dir():
            return (f"openclaw executable {resolved}", candidate)
    return None


def _extract_openclaw_root_from_text(text: str) -> Path | None:
    for raw_match in DIST_INDEX_PATTERN.findall(text):
        candidate = Path(raw_match).expanduser()
        if not candidate.is_absolute():
            continue
        try:
            resolved = candidate.resolve()
        except OSError:
            continue
        if resolved.name != "index.js":
            continue
        if resolved.parent.name != "dist":
            continue
        root = resolved.parent.parent
        if (root / "dist").is_dir():
            return root
    return None


def ensure_dist_dir(root: Path) -> Path:
    dist_dir = root / "dist"
    if not dist_dir.is_dir():
        raise PatchError(f"Expected dist/ under {root}, but {dist_dir} does not exist")
    return dist_dir


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError as exc:
        raise PatchError(f"Failed to decode {path} as UTF-8: {exc}") from exc
    except OSError as exc:
        raise PatchError(f"Failed to read {path}: {exc}") from exc


def write_text(path: Path, content: str) -> None:
    try:
        path.write_text(content, encoding="utf-8")
    except OSError as exc:
        raise PatchError(f"Failed to write {path}: {exc}") from exc


def iter_candidate_bundles(dist_dir: Path) -> list[Path]:
    preferred = collect_bundles(dist_dir, PREFERRED_PATTERNS)
    preferred_matches = [path for path in preferred if bundle_contains_target(path)]
    if preferred_matches:
        return preferred_matches

    fallback = collect_bundles(dist_dir, FALLBACK_PATTERNS)
    fallback_matches = [
        path for path in fallback if path not in preferred and bundle_contains_target(path)
    ]
    return fallback_matches


def collect_bundles(dist_dir: Path, patterns: Iterable[str]) -> list[Path]:
    seen: set[Path] = set()
    bundles: list[Path] = []
    for pattern in patterns:
        for path in sorted(dist_dir.glob(pattern)):
            if not path.is_file():
                continue
            if BACKUP_TOKEN in path.name:
                continue
            if path.suffix != ".js":
                continue
            if path in seen:
                continue
            seen.add(path)
            bundles.append(path)
    return bundles


def bundle_contains_target(path: Path) -> bool:
    try:
        return TARGET_FUNCTION_SIGNATURE in read_text(path)
    except PatchError:
        return False


def inspect_bundle(path: Path) -> BundleInspection:
    text = read_text(path)
    function_start, function_end, function_block = locate_target_function(text, path)
    if PATCH_MARKER in function_block:
        state = "patched"
    elif TARGET_RETURN in function_block:
        state = "patchable"
    else:
        state = "unexpected"
    return BundleInspection(
        path=path,
        text=text,
        function_start=function_start,
        function_end=function_end,
        function_block=function_block,
        state=state,
    )


def locate_target_function(text: str, path: Path) -> tuple[int, int, str]:
    start = text.find(TARGET_FUNCTION_SIGNATURE)
    if start < 0:
        raise PatchError(f"Target function not found in {path}")

    brace_start = text.find("{", start)
    if brace_start < 0:
        raise PatchError(f"Malformed target function in {path}: missing opening brace")

    depth = 0
    for index in range(brace_start, len(text)):
        character = text[index]
        if character == "{":
            depth += 1
        elif character == "}":
            depth -= 1
            if depth == 0:
                end = index + 1
                return start, end, text[start:end]

    raise PatchError(f"Malformed target function in {path}: missing closing brace")


def build_patched_text(inspection: BundleInspection) -> str:
    if inspection.state == "patched":
        return inspection.text
    if inspection.state != "patchable":
        raise PatchError(
            f"Refusing to patch {inspection.path}: target function exists but no longer matches the expected return line"
        )

    patched_block = inspection.function_block.replace(TARGET_RETURN, PATCHED_RETURN, 1)
    if patched_block == inspection.function_block:
        raise PatchError(f"Failed to patch {inspection.path}: return line was not replaced")

    return (
        inspection.text[: inspection.function_start]
        + patched_block
        + inspection.text[inspection.function_end :]
    )


def create_backup(path: Path) -> Path:
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    base_name = f"{path.name}.{BACKUP_TOKEN}.{timestamp}"
    backup_path = path.with_name(base_name)
    counter = 1
    while backup_path.exists():
        backup_path = path.with_name(f"{base_name}.{counter}")
        counter += 1
    try:
        shutil.copy2(path, backup_path)
    except OSError as exc:
        raise PatchError(f"Failed to create backup for {path}: {exc}") from exc
    return backup_path


def list_skill_backups(dist_dir: Path) -> list[Path]:
    return sorted(dist_dir.glob(f"*.{BACKUP_TOKEN}.*"))


def list_matching_backups(bundle_path: Path) -> list[Path]:
    return sorted(bundle_path.parent.glob(f"{bundle_path.name}.{BACKUP_TOKEN}.*"))


def latest_matching_backup(bundle_path: Path) -> Path | None:
    backups = list_matching_backups(bundle_path)
    if not backups:
        return None
    return backups[-1]


def run_node_check(path: Path) -> None:
    try:
        result = subprocess.run(
            ["node", "--check", str(path)],
            capture_output=True,
            text=True,
            check=False,
        )
    except FileNotFoundError as exc:
        raise PatchError("node is required but was not found in PATH") from exc

    if result.returncode != 0:
        combined = "\n".join(part for part in [result.stdout.strip(), result.stderr.strip()] if part)
        raise PatchError(f"node --check failed for {path}\n{combined}")


def copy_file(source: Path, destination: Path) -> None:
    try:
        shutil.copy2(source, destination)
    except OSError as exc:
        raise PatchError(f"Failed to copy {source} to {destination}: {exc}") from exc


def format_paths(paths: Iterable[Path]) -> str:
    return ", ".join(str(path) for path in paths)
