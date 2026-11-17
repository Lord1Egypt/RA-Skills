#!/usr/bin/env python3
from __future__ import annotations

import json
import shutil
import zipfile
from datetime import date
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PROJECT_ROOT = ROOT.parent
DIST = PROJECT_ROOT / "dist"
SKILL_NAME = ROOT.name
VERSION = "v1.2.1"


def should_include(path: Path) -> bool:
    rel = path.relative_to(ROOT)
    parts = set(rel.parts)
    if "__pycache__" in parts:
        return False
    if path.name in {".DS_Store"}:
        return False
    return path.is_file()


def build_zip(target: Path) -> None:
    if target.exists():
        target.unlink()
    with zipfile.ZipFile(target, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        for path in sorted(ROOT.rglob("*")):
            if should_include(path):
                zf.write(path, Path(SKILL_NAME) / path.relative_to(ROOT))


def main() -> None:
    DIST.mkdir(exist_ok=True)
    stamp = date.today().strftime("%Y%m%d")
    versioned = DIST / f"{SKILL_NAME}-{VERSION}-{stamp}.zip"
    latest = DIST / f"{SKILL_NAME}-latest.zip"
    manifest_path = DIST / f"{SKILL_NAME}-{VERSION}-{stamp}.manifest.json"

    build_zip(versioned)
    shutil.copyfile(versioned, latest)

    files = []
    with zipfile.ZipFile(versioned) as zf:
        for item in sorted(zf.infolist(), key=lambda info: info.filename):
            files.append({"path": item.filename, "size": item.file_size})

    manifest = {
        "skill": SKILL_NAME,
        "version": VERSION,
        "date": stamp,
        "zip": versioned.name,
        "latest": latest.name,
        "file_count": len(files),
        "files": files,
    }
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(json.dumps({
        "zip": str(versioned),
        "latest": str(latest),
        "manifest": str(manifest_path),
        "file_count": len(files),
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
