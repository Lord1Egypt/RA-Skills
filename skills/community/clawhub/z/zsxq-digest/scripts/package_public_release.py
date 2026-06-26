#!/usr/bin/env python3
import argparse
import shutil
import subprocess
import sys
import tempfile
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DEFAULT_OUTPUT_DIR = ROOT / "dist"
DEFAULT_PACKAGE_SCRIPT = Path("/opt/homebrew/lib/node_modules/openclaw/skills/skill-creator/scripts/package_skill.py")
SKIP_DIR_NAMES = {"state", "__pycache__", ".tmp", "tmp", ".git"}
SKIP_FILE_NAMES = {".DS_Store"}
SKIP_SUFFIXES = (".pyc", ".pyo", ".skill", ".bak")


def should_skip(rel_path: Path) -> bool:
    if any(part in SKIP_DIR_NAMES for part in rel_path.parts):
        return True
    name = rel_path.name
    if name in SKIP_FILE_NAMES:
        return True
    if ".bak-" in name or ".bak." in name or name.endswith(".bak"):
        return True
    if name.endswith(SKIP_SUFFIXES):
        return True
    return False


def copy_sanitized_tree(src_root: Path, dst_root: Path) -> None:
    for src_path in src_root.rglob("*"):
        rel_path = src_path.relative_to(src_root)
        if should_skip(rel_path):
            continue
        dst_path = dst_root / rel_path
        if src_path.is_dir():
            dst_path.mkdir(parents=True, exist_ok=True)
            continue
        dst_path.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src_path, dst_path)


def verify_artifact(artifact_path: Path) -> None:
    with zipfile.ZipFile(artifact_path) as zf:
        bad_entries = [
            name for name in zf.namelist()
            if "/state/" in f"/{name}" or name.endswith("session.token.json") or name.endswith("captured-cookies.json")
        ]
    if bad_entries:
        raise SystemExit(f"artifact still contains private runtime files: {bad_entries}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Package zsxq-digest without private runtime state")
    parser.add_argument("--output-dir", default=str(DEFAULT_OUTPUT_DIR))
    parser.add_argument("--package-script", default=str(DEFAULT_PACKAGE_SCRIPT))
    args = parser.parse_args()

    output_dir = Path(args.output_dir).expanduser().resolve()
    package_script = Path(args.package_script).expanduser().resolve()
    output_dir.mkdir(parents=True, exist_ok=True)

    with tempfile.TemporaryDirectory() as td:
        staged_root = Path(td) / ROOT.name
        staged_root.mkdir(parents=True, exist_ok=True)
        copy_sanitized_tree(ROOT, staged_root)
        subprocess.run(
            [sys.executable, str(package_script), str(staged_root), str(output_dir)],
            check=True,
        )

    artifact_path = output_dir / f"{ROOT.name}.skill"
    verify_artifact(artifact_path)
    print(artifact_path)


if __name__ == "__main__":
    main()
