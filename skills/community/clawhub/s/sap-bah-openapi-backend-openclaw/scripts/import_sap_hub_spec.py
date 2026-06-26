#!/usr/bin/env python3
"""Import a downloaded SAP Business Accelerator Hub API spec into APIConnectionToSAP.

This script is intentionally simple and deterministic:
- Find a downloaded file (explicit path, latest by pattern, or latest supported file)
- Resolve target category folder style used by this repo
- Copy or move file into APIConnectionToSAP/<Category>[/Connection]
- Normalize filename to reduce duplicates like "(1)"
"""

from __future__ import annotations

import argparse
import re
import shutil
from pathlib import Path
from typing import Iterable

SUPPORTED_EXTENSIONS = {".json", ".yaml", ".yml", ".edmx", ".xml", ".wsdl"}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Import SAP Hub spec into APIConnectionToSAP")
    parser.add_argument("--category", required=True, help="Category folder name under APIConnectionToSAP, e.g. PurchaseOrder, OSC2.0")
    parser.add_argument("--file", help="Exact file path of downloaded spec")
    parser.add_argument("--downloads-dir", default=str(Path.home() / "Downloads"), help="Directory to search downloaded files")
    parser.add_argument("--pattern", help="Case-insensitive keyword used to pick the latest matching file, e.g. warehouseorder")
    parser.add_argument("--name", help="Override output file base name without extension")
    parser.add_argument("--mode", choices=["copy", "move"], default="copy", help="Copy or move source file")
    parser.add_argument("--project-root", default=str(Path(__file__).resolve().parents[3]), help="Project root containing APIConnectionToSAP")
    parser.add_argument("--dry-run", action="store_true", help="Only print action")
    return parser.parse_args()


def normalize_base_name(raw: str) -> str:
    base = raw.strip()
    base = re.sub(r"\s*\(\d+\)$", "", base)
    base = base.replace("-", "_")
    base = re.sub(r"\s+", "_", base)
    base = re.sub(r"[^A-Za-z0-9_.]+", "_", base)
    base = re.sub(r"_+", "_", base)
    return base.strip("_") or "sap_api_spec"


def iter_candidate_files(downloads_dir: Path) -> Iterable[Path]:
    for p in downloads_dir.iterdir():
        if p.is_file() and p.suffix.lower() in SUPPORTED_EXTENSIONS:
            yield p


def pick_source_file(explicit_file: str | None, downloads_dir: Path, pattern: str | None) -> Path:
    if explicit_file:
        p = Path(explicit_file).expanduser().resolve()
        if not p.exists() or not p.is_file():
            raise FileNotFoundError(f"File not found: {p}")
        if p.suffix.lower() not in SUPPORTED_EXTENSIONS:
            raise ValueError(f"Unsupported file extension: {p.suffix}")
        return p

    if not downloads_dir.exists() or not downloads_dir.is_dir():
        raise FileNotFoundError(f"Downloads directory not found: {downloads_dir}")

    files = list(iter_candidate_files(downloads_dir))
    if pattern:
        pat = pattern.lower()
        files = [p for p in files if pat in p.name.lower()]

    if not files:
        hint = f" matching pattern '{pattern}'" if pattern else ""
        raise FileNotFoundError(f"No supported file found in {downloads_dir}{hint}")

    files.sort(key=lambda p: p.stat().st_mtime, reverse=True)
    return files[0]


def resolve_target_dir(api_root: Path, category: str) -> Path:
    category_dir = api_root / category
    connection_dir = category_dir / "Connection"

    if category_dir.exists():
        if connection_dir.exists() and connection_dir.is_dir():
            return connection_dir
        return category_dir

    connection_dir.mkdir(parents=True, exist_ok=True)
    return connection_dir


def dedupe_target_path(target: Path) -> Path:
    if not target.exists():
        return target
    stem = target.stem
    suffix = target.suffix
    parent = target.parent
    idx = 1
    while True:
        candidate = parent / f"{stem}_{idx}{suffix}"
        if not candidate.exists():
            return candidate
        idx += 1


def main() -> None:
    args = parse_args()

    project_root = Path(args.project_root).expanduser().resolve()
    api_root = project_root / "APIConnectionToSAP"
    if not api_root.exists():
        raise FileNotFoundError(f"APIConnectionToSAP not found under {project_root}")

    source_file = pick_source_file(args.file, Path(args.downloads_dir).expanduser().resolve(), args.pattern)
    target_dir = resolve_target_dir(api_root, args.category)

    out_base = normalize_base_name(args.name) if args.name else normalize_base_name(source_file.stem)
    target_file = dedupe_target_path(target_dir / f"{out_base}{source_file.suffix.lower()}")

    print(f"[INFO] Source: {source_file}")
    print(f"[INFO] Target: {target_file}")
    print(f"[INFO] Mode:   {args.mode}")

    if args.dry_run:
        print("[DRY-RUN] No file changes were made.")
        return

    if args.mode == "copy":
        shutil.copy2(source_file, target_file)
    else:
        shutil.move(str(source_file), str(target_file))

    print("[OK] Spec imported successfully.")


if __name__ == "__main__":
    main()
