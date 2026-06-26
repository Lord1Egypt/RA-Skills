#!/usr/bin/env python3
"""
Package and publish research archive query skill to ClawHub.
"""

from __future__ import annotations

import argparse
import os
import shutil
import subprocess
import sys
from pathlib import Path


SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR))

from package_skill import SKILL_DIR


DEFAULT_DIST = SKILL_DIR.parent / "dist" / "research-archive-query"


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Publish research archive query skill to ClawHub")
    parser.add_argument("--slug", default="research-archive-query")
    parser.add_argument("--name", default="本地研究资料查询")
    parser.add_argument("--version", default="0.1.0")
    parser.add_argument("--changelog", default="Initial public release")
    parser.add_argument(
        "--dist-dir",
        default=str(DEFAULT_DIST),
        help="Publish-safe dist directory",
    )
    parser.add_argument(
        "--skip-package",
        action="store_true",
        help="Reuse existing dist directory",
    )
    return parser


def run_command(cmd: list[str]) -> None:
    subprocess.run(cmd, check=True)


def resolve_clawhub_bin() -> str | None:
    env_value = os.environ.get("CLAWHUB_BIN")
    if env_value:
        path = Path(env_value).expanduser()
        if path.exists():
            return str(path)

    for candidate in [
        shutil.which("clawhub"),
        str(Path.home() / ".npm-global" / "bin" / "clawhub"),
        str(Path.home() / ".npm-global" / "node_modules" / ".bin" / "clawhub"),
    ]:
        if candidate and Path(candidate).exists():
            return candidate
    return None


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    clawhub = resolve_clawhub_bin()
    if not clawhub:
        print("未找到 clawhub CLI，请先安装并登录，或设置 CLAWHUB_BIN。")
        return 1

    dist_dir = Path(args.dist_dir).expanduser().resolve()
    if not args.skip_package:
        run_command(
            [
                sys.executable,
                str(SCRIPT_DIR / "package_skill.py"),
                "--dest",
                str(dist_dir),
            ]
        )

    run_command(
        [
            clawhub,
            "publish",
            str(dist_dir),
            "--slug",
            args.slug,
            "--name",
            args.name,
            "--version",
            args.version,
            "--changelog",
            args.changelog,
        ]
    )
    print("发布完成")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
