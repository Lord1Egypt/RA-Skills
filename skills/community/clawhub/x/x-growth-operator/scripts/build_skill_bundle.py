from __future__ import annotations

from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile


ROOT = Path(__file__).resolve().parent.parent
DIST = ROOT / "dist"
OUTPUT = DIST / "x-growth-operator-skill.zip"

INCLUDE_PREFIXES = (
    "SKILL.md",
    "README.md",
    "ROADMAP.md",
    "LICENSE",
    "agents/openai.yaml",
    "app/",
    "core/",
    "references/",
    "examples/",
    "scripts/",
    "data/.gitkeep",
)

EXCLUDE_PATHS = {
    "scripts/.env",
    "scripts/package-lock.json",
}

EXCLUDE_PARTS = {
    "node_modules",
    "__pycache__",
    ".DS_Store",
}


def should_include(relative_path: str) -> bool:
    if relative_path in EXCLUDE_PATHS:
        return False
    if any(part in EXCLUDE_PARTS for part in Path(relative_path).parts):
        return False
    return any(
        relative_path == prefix or relative_path.startswith(prefix)
        for prefix in INCLUDE_PREFIXES
    )


def main() -> int:
    DIST.mkdir(parents=True, exist_ok=True)
    with ZipFile(OUTPUT, "w", compression=ZIP_DEFLATED) as archive:
        for path in sorted(ROOT.rglob("*")):
            if not path.is_file():
                continue
            relative = path.relative_to(ROOT).as_posix()
            if not should_include(relative):
                continue
            archive.write(path, arcname=relative)

    print(f"Wrote {OUTPUT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
