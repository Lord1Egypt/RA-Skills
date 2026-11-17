#!/usr/bin/env python3
"""Validate, package and install-check Workday Companion v1."""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import shutil
import subprocess
import sys
import tempfile
from datetime import date, datetime
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile, ZipInfo


ROOT = Path(__file__).resolve().parents[1]
WORKSPACE = ROOT.parent
DEFAULT_DIST = WORKSPACE / "dist"
EXCLUDED_NAMES = {".DS_Store", "__pycache__"}
EXCLUDED_SUFFIXES = {".pyc", ".pyo"}


def load_module(relative: str, name: str):
    path = ROOT / relative
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {relative}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def package_files() -> list[Path]:
    files: list[Path] = []
    for path in ROOT.rglob("*"):
        if not path.is_file():
            continue
        if any(part in EXCLUDED_NAMES for part in path.parts) or path.suffix in EXCLUDED_SUFFIXES:
            continue
        files.append(path)
    return sorted(files, key=lambda item: item.relative_to(ROOT).as_posix())


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def validate_source() -> dict[str, str]:
    validator = load_module("scripts/validate_skill.py", "validate_skill_module")
    results = validator.validate_all()
    rendered = load_module("scripts/validate_rendered_cards.py", "validate_rendered_cards_module")
    rendered.validate_all()
    return results


def write_deterministic_zip(output: Path, files: list[Path], release_date: str) -> None:
    stamp = datetime.strptime(release_date, "%Y-%m-%d")
    zip_stamp = (max(1980, stamp.year), stamp.month, stamp.day, 0, 0, 0)
    with ZipFile(output, "w", compression=ZIP_DEFLATED, compresslevel=9) as archive:
        for path in files:
            relative = path.relative_to(ROOT).as_posix()
            info = ZipInfo(f"{ROOT.name}/{relative}", date_time=zip_stamp)
            info.compress_type = ZIP_DEFLATED
            info.external_attr = (0o755 if path.suffix == ".py" else 0o644) << 16
            archive.writestr(info, path.read_bytes())


def validate_zip_members(archive_path: Path, files: list[Path]) -> None:
    expected = {f"{ROOT.name}/{path.relative_to(ROOT).as_posix()}" for path in files}
    with ZipFile(archive_path) as archive:
        actual = set(archive.namelist())
        if actual != expected:
            missing = sorted(expected - actual)
            extra = sorted(actual - expected)
            raise RuntimeError(f"archive members drifted; missing={missing} extra={extra}")
        for member in actual:
            target = Path(member)
            if target.is_absolute() or ".." in target.parts:
                raise RuntimeError(f"unsafe archive member: {member}")


def validate_install(archive_path: Path) -> None:
    with tempfile.TemporaryDirectory(prefix="workday-install-") as raw:
        temp = Path(raw)
        with ZipFile(archive_path) as archive:
            archive.extractall(temp)
        installed = temp / ROOT.name
        subprocess.run(
            [sys.executable, str(installed / "scripts/validate_skill.py"), "--quiet"],
            cwd=installed,
            check=True,
        )
        subprocess.run(
            [sys.executable, str(installed / "scripts/validate_rendered_cards.py")],
            cwd=installed,
            check=True,
        )


def manifest_payload(version: str, release_date: str, archive: Path, latest: Path, files: list[Path], gates: dict[str, str]) -> dict[str, object]:
    return {
        "skill": ROOT.name,
        "version": version,
        "date": release_date,
        "zip": archive.name,
        "latest": latest.name,
        "sha256": sha256(archive),
        "file_count": len(files),
        "gate_count": len(gates) + 2,
        "external_evidence_state": "evidence_pending",
        "files": [
            {
                "path": path.relative_to(ROOT).as_posix(),
                "size": path.stat().st_size,
                "sha256": sha256(path),
            }
            for path in files
        ],
    }


def prune_old_workday_artifacts(dist: Path, keep: set[Path]) -> list[str]:
    removed: list[str] = []
    patterns = ("workday-companion-v1-*.zip", "workday-companion-v1-*.manifest.json")
    for pattern in patterns:
        for path in dist.glob(pattern):
            if path.resolve() in keep:
                continue
            path.unlink()
            removed.append(path.name)
    return sorted(removed)


def build(version: str, release_date: str, dist: Path) -> tuple[Path, Path, Path]:
    datetime.strptime(release_date, "%Y-%m-%d")
    if version != "v1":
        raise ValueError("public release version must remain v1")
    gates = validate_source()
    files = package_files()
    dist.mkdir(parents=True, exist_ok=True)
    compact_date = release_date.replace("-", "")
    archive = dist / f"workday-companion-{version}-{compact_date}.zip"
    latest = dist / "workday-companion-latest.zip"
    manifest = dist / f"workday-companion-{version}-{compact_date}.manifest.json"
    temp_archive = dist / f".{archive.name}.tmp"
    if temp_archive.exists():
        temp_archive.unlink()
    write_deterministic_zip(temp_archive, files, release_date)
    validate_zip_members(temp_archive, files)
    validate_install(temp_archive)
    temp_archive.replace(archive)
    shutil.copy2(archive, latest)
    payload = manifest_payload(version, release_date, archive, latest, files, gates)
    manifest.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    removed = prune_old_workday_artifacts(dist, {archive.resolve(), manifest.resolve()})
    print(f"OK package {archive} files={len(files)} sha256={payload['sha256']}")
    print(f"OK latest {latest} identical={sha256(latest) == payload['sha256']}")
    print(f"OK manifest {manifest} gates={payload['gate_count']} evidence=evidence_pending")
    if removed:
        print(f"OK pruned old artifacts count={len(removed)}")
    return archive, latest, manifest


def main() -> None:
    parser = argparse.ArgumentParser(description="Build the Workday Companion public v1 package.")
    parser.add_argument("--version", default="v1")
    parser.add_argument("--date", default=date.today().isoformat())
    parser.add_argument("--out-dir", default=str(DEFAULT_DIST))
    args = parser.parse_args()
    try:
        build(args.version, args.date, Path(args.out_dir).resolve())
    except (OSError, RuntimeError, ValueError, subprocess.CalledProcessError) as exc:
        print(f"FAIL {exc}")
        raise SystemExit(1) from exc


if __name__ == "__main__":
    main()
