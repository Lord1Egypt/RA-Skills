#!/usr/bin/env python3
from __future__ import annotations

import argparse
import os
import subprocess
import sys
from pathlib import Path


SCRIPT_DIR = Path(__file__).resolve().parent
CLI_BY_LANG = {
    "zh": SCRIPT_DIR / "ZipCracker.py",
    "en": SCRIPT_DIR / "ZipCracker_en.py",
}
INSPECTOR_PATH = SCRIPT_DIR / "zipcracker_inspect.py"


def default_lang() -> str:
    for env_name in ("ZIPCRACKER_SKILL_LANG", "LC_ALL", "LC_MESSAGES", "LANG"):
        value = os.environ.get(env_name, "").strip().lower()
        if value.startswith("en"):
            return "en"
        if value.startswith("zh"):
            return "zh"
    return "zh"


def parse_args(argv: list[str]) -> tuple[argparse.Namespace, list[str]]:
    parser = argparse.ArgumentParser(
        description="OpenClaw-friendly wrapper around the bundled ZipCracker skill."
    )
    parser.add_argument(
        "--lang",
        choices=("zh", "en"),
        default=default_lang(),
        help="Choose the bundled Chinese or English CLI.",
    )
    parser.add_argument(
        "--profile",
        action="store_true",
        help="Inspect the ZIP first and print a human-readable strategy summary.",
    )
    parser.add_argument(
        "--profile-json",
        action="store_true",
        help="Inspect the ZIP first and emit structured JSON.",
    )
    parser.add_argument(
        "--auto-crc",
        action="store_true",
        help="Auto-confirm short-plaintext CRC32 enumeration prompts.",
    )
    parser.add_argument(
        "--auto-large-mask",
        action="store_true",
        help="Auto-confirm huge mask warnings.",
    )
    parser.add_argument(
        "--auto-template-kpa",
        action="store_true",
        help="Auto-confirm built-in template KPA suggestions after default attacks fail.",
    )
    parser.add_argument(
        "--skip-dict-count",
        action="store_true",
        help="Skip upfront line counting for large dictionaries.",
    )
    parser.add_argument(
        "--skip-orig-password-recovery",
        action="store_true",
        help="Skip original password recovery after bkcrack-based extraction succeeds.",
    )
    parser.add_argument(
        "--allow-install-prompts",
        action="store_true",
        help="Allow pyzipper/bkcrack install prompts instead of forcing non-interactive skip.",
    )
    return parser.parse_known_args(argv)


def build_env(args: argparse.Namespace) -> dict[str, str]:
    env = os.environ.copy()
    if not args.allow_install_prompts:
        env.setdefault("ZIPCRACKER_AUTO_INSTALL_PYZIPPER", "0")
        env.setdefault("ZIPCRACKER_AUTO_INSTALL_BKCRACK", "0")
    if args.auto_crc:
        env["ZIPCRACKER_ASSUME_CRC_RECOVERY"] = "1"
    if args.auto_large_mask:
        env["ZIPCRACKER_ASSUME_LARGE_MASK"] = "1"
    if args.auto_template_kpa:
        env["ZIPCRACKER_ASSUME_TEMPLATE_KPA"] = "1"
    if args.skip_dict_count:
        env["ZIPCRACKER_SKIP_DICT_COUNT"] = "1"
    if args.skip_orig_password_recovery:
        env["ZIPCRACKER_SKIP_ORIG_PW_RECOVERY"] = "1"
    return env


def main(argv: list[str] | None = None) -> int:
    args, inner_args = parse_args(argv or sys.argv[1:])
    if inner_args and inner_args[0] == "--":
        inner_args = inner_args[1:]
    if not inner_args:
        inner_args = ["--help"]

    if args.profile or args.profile_json:
        inspect_args = [str(INSPECTOR_PATH), "--lang", args.lang]
        if args.profile_json:
            inspect_args.append("--json")
        inspect_args.extend(inner_args)
        completed = subprocess.run([sys.executable, *inspect_args], check=False)
        return completed.returncode

    cli_path = CLI_BY_LANG[args.lang]
    env = build_env(args)
    command = [sys.executable, str(cli_path), *inner_args]
    completed = subprocess.run(command, env=env, check=False)
    return completed.returncode


if __name__ == "__main__":
    raise SystemExit(main())
