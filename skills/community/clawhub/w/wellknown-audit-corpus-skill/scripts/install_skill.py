#!/usr/bin/env python3
"""Install this ClawMart skill/starter-pack into an OpenClaw skills directory."""
import argparse
import json
import os
import pathlib
import shutil
import subprocess
import sys
import time

PACKAGE_DIR = pathlib.Path(__file__).resolve().parents[1]
DEFAULT_TARGET = pathlib.Path(os.environ.get("OPENCLAW_SKILLS_DIR", "~/.openclaw/skills")).expanduser()


def copytree(src: pathlib.Path, dst: pathlib.Path, force: bool):
    if dst.exists():
        if not force:
            raise SystemExit(f"target exists: {dst} (pass --force to overwrite)")
        shutil.rmtree(dst)
    ignore = shutil.ignore_patterns("__pycache__", "*.pyc", ".DS_Store")
    shutil.copytree(src, dst, ignore=ignore)


def run_package_verify(package_dir: pathlib.Path):
    verifier = package_dir / "scripts" / "verify_package.py"
    if not verifier.exists():
        raise SystemExit("missing scripts/verify_package.py; refusing install without package integrity check")
    return subprocess.call([sys.executable, str(verifier)])


def write_lock(dest: pathlib.Path):
    checksums_path = dest / "checksums.json"
    checksums = json.loads(checksums_path.read_text()) if checksums_path.exists() else {}
    lock = {
        "source": "clawmart",
        "slug": checksums.get("slug", dest.name),
        "version": checksums.get("version", "1.0.0"),
        "installed_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "checksums_file": "checksums.json",
        "pinning": "Do not auto-update this skill. Reinstall only after reviewing a new ClawMart version and re-running scripts/verify_package.py.",
    }
    (dest / ".clawmart-lock.json").write_text(json.dumps(lock, indent=2) + "\n")


def main():
    parser = argparse.ArgumentParser(description="Install this package into an OpenClaw skills directory.")
    parser.add_argument("--target", default=str(DEFAULT_TARGET), help="Skills directory, default: OPENCLAW_SKILLS_DIR or ~/.openclaw/skills")
    parser.add_argument("--name", default=PACKAGE_DIR.name, help="Installed directory name")
    parser.add_argument("--force", action="store_true", help="Overwrite an existing installed copy")
    parser.add_argument("--skip-package-verify", action="store_true", help="Skip bundled checksum verification before install")
    parser.add_argument("--verify-backend", action="store_true", help="Run scripts/verify_backend.py after install when present")
    args = parser.parse_args()

    if not args.skip_package_verify:
        code = run_package_verify(PACKAGE_DIR)
        if code != 0:
            return code

    target = pathlib.Path(args.target).expanduser().resolve()
    dest = target / args.name
    target.mkdir(parents=True, exist_ok=True)
    copytree(PACKAGE_DIR, dest, args.force)
    write_lock(dest)
    print(f"INSTALLED {PACKAGE_DIR.name} -> {dest}")
    print(f"LOCKED {dest / '.clawmart-lock.json'}")
    print(f"NEXT: ask your agent to read {dest / 'SKILL.md'} before use")

    if args.verify_backend:
        verifier = dest / "scripts" / "verify_backend.py"
        if not verifier.exists():
            print("VERIFY_SKIPPED no scripts/verify_backend.py in package")
            return 0
        return subprocess.call([sys.executable, str(verifier)])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
