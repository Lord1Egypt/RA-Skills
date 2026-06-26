from __future__ import annotations

import json
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile

from _paths import DIST_DIR, SKILL_DIR

EXCLUDE_DIRS = {"__pycache__", ".pytest_cache", "dist", "data"}
EXCLUDE_SUFFIXES = {".pyc", ".pyo"}


def should_include(path: Path) -> bool:
    rel = path.relative_to(SKILL_DIR)
    if any(part in EXCLUDE_DIRS for part in rel.parts):
        return False
    if path.suffix.lower() in EXCLUDE_SUFFIXES:
        return False
    return path.is_file()


def main() -> int:
    DIST_DIR.mkdir(parents=True, exist_ok=True)
    out_path = DIST_DIR / "used-market-watch.skill"
    manifest = {
        "name": "used-market-watch",
        "version": "0.4.0",
        "entry": "SKILL.md",
    }
    with ZipFile(out_path, "w", compression=ZIP_DEFLATED) as zf:
        zf.writestr("manifest.json", json.dumps(manifest, ensure_ascii=False, indent=2))
        for path in sorted(SKILL_DIR.rglob("*")):
            if should_include(path):
                zf.write(path, arcname=str(path.relative_to(SKILL_DIR)).replace('\\', '/'))
    print(str(out_path))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
