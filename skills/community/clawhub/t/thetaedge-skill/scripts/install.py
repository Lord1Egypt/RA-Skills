#!/usr/bin/env python3
"""
Cross-platform installer for the thetaedge-skill (thetix) skill.

Supports Claude Code, OpenClaw, and generic agent configurations
on Windows, macOS, and Linux.

Usage:
    python3 scripts/install.py
    python3 scripts/install.py --target claude-code --api-key te_...
    python3 scripts/install.py --update
"""

import argparse
import getpass
import os
import shutil
import sys
from pathlib import Path

# Ensure the scripts/ package is importable regardless of cwd.
sys.path.insert(0, str(Path(__file__).resolve().parent))
from lib.common import (
    DEFAULT_API_BASE,
    DEFAULT_CLONE_URL,
    deep_merge,
    detect_os,
    detect_targets,
    fatal,
    get_credentials,
    git_available,
    info,
    is_windows,
    run_git,
    set_credentials,
    skill_dir_for_target,
    test_api_connection,
    validate_api_key,
    warn,
)


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(
        description="Install the thetix skill for Claude Code, OpenClaw, or other agents.",
    )
    p.add_argument(
        "--target",
        choices=["auto", "claude-code", "openclaw", "generic"],
        default="auto",
        help="Agent platform to install for (default: auto-detect)",
    )
    p.add_argument("--api-key", help="ThetaEdge API key (prompted if omitted)")
    p.add_argument("--api-base", default=DEFAULT_API_BASE, help=f"API base URL (default: {DEFAULT_API_BASE})")
    p.add_argument("--update", action="store_true", help="Update an existing installation")
    p.add_argument("--non-interactive", action="store_true", help="Skip all prompts")
    p.add_argument("--clone-url", default=DEFAULT_CLONE_URL, help="Git clone URL")
    return p.parse_args()


# ---------------------------------------------------------------------------
# Skill source detection
# ---------------------------------------------------------------------------

def find_skill_source() -> Path:
    """Return the repo root if this script lives inside a clone."""
    script_dir = Path(__file__).resolve().parent
    repo_root = script_dir.parent
    if (repo_root / "SKILL.md").is_file():
        return repo_root
    return Path("")


# ---------------------------------------------------------------------------
# Skill installation
# ---------------------------------------------------------------------------

def install_claude_code(source: Path, clone_url: str, update: bool) -> Path:
    target = skill_dir_for_target("claude-code")
    if target.is_dir() and (target / "SKILL.md").is_file():
        if update and (target / ".git").is_dir():
            info("Updating skill at " + str(target))
            result = run_git("pull", cwd=target)
            if result.returncode != 0:
                warn(f"git pull failed: {result.stderr.strip()}")
            else:
                info("Updated successfully.")
        else:
            info(f"Skill already installed at {target}")
        return target

    info(f"Installing skill to {target}")
    target.parent.mkdir(parents=True, exist_ok=True)

    # If running from inside a clone, clone from the same remote
    if source and (source / ".git").is_dir():
        result = run_git("remote", "get-url", "origin", cwd=source)
        if result.returncode == 0 and result.stdout.strip():
            clone_url = result.stdout.strip()

    result = run_git("clone", clone_url, str(target))
    if result.returncode != 0:
        fatal(f"git clone failed: {result.stderr.strip()}")
    info("Cloned successfully.")
    return target


def install_openclaw(source: Path, clone_url: str, update: bool) -> Path:
    target = skill_dir_for_target("openclaw")

    if target.is_dir() and (target / "SKILL.md").is_file():
        if update:
            if target.is_symlink():
                real = Path(os.readlink(target))
                if (real / ".git").is_dir():
                    info("Updating skill source at " + str(real))
                    result = run_git("pull", cwd=real)
                    if result.returncode != 0:
                        warn(f"git pull failed: {result.stderr.strip()}")
                    else:
                        info("Updated successfully.")
            elif (target / ".git").is_dir():
                info("Updating skill at " + str(target))
                result = run_git("pull", cwd=target)
                if result.returncode != 0:
                    warn(f"git pull failed: {result.stderr.strip()}")
                else:
                    info("Updated successfully.")
            elif source:
                # Copied dir on Windows — re-copy from source
                info("Re-copying skill files from source...")
                shutil.rmtree(target)
                shutil.copytree(source, target)
                info("Updated successfully.")
        else:
            info(f"Skill already installed at {target}")
        return target

    info(f"Installing skill to {target}")
    target.parent.mkdir(parents=True, exist_ok=True)

    if source and source.is_dir():
        # We have a local source — symlink or copy
        if is_windows():
            try:
                os.symlink(source, target, target_is_directory=True)
                info(f"Symlink created: {target} -> {source}")
            except OSError:
                info("Symlinks not available, copying files instead...")
                shutil.copytree(source, target)
                info("Copied successfully.")
        else:
            os.symlink(source, target)
            info(f"Symlink created: {target} -> {source}")
    else:
        # No local source — clone directly
        result = run_git("clone", clone_url, str(target))
        if result.returncode != 0:
            fatal(f"git clone failed: {result.stderr.strip()}")
        info("Cloned successfully.")

    return target


# ---------------------------------------------------------------------------
# Credential prompting
# ---------------------------------------------------------------------------

def prompt_credentials(args: argparse.Namespace, targets: list) -> tuple:
    api_key = args.api_key or ""
    api_base = args.api_base

    # Check if credentials already exist for any target
    existing_key = ""
    for t in targets:
        ek, _ = get_credentials(t)
        if ek:
            existing_key = ek
            break

    if not api_key and not args.non_interactive:
        if existing_key:
            masked = existing_key[:6] + "..." if len(existing_key) > 6 else existing_key
            print(f"\nExisting API key found: {masked}")
            answer = input("Keep existing key? [Y/n] ").strip().lower()
            if answer in ("", "y", "yes"):
                return "", api_base  # empty key = skip credential writing
            print()
        api_key = getpass.getpass("ThetaEdge API key (input is hidden): ")

    if not api_key:
        if args.non_interactive and existing_key:
            info("Existing credentials preserved.")
            return "", api_base
        elif args.non_interactive:
            warn("No API key provided. Configure credentials manually later.")
        else:
            warn("No API key entered. You can configure it later.")

    if api_key:
        ok, msg = validate_api_key(api_key)
        if not ok:
            warn(f"API key validation: {msg}")

    return api_key, api_base


# ---------------------------------------------------------------------------
# Verification
# ---------------------------------------------------------------------------

def verify_installation(target: str, api_key: str, api_base: str, non_interactive: bool) -> None:
    sdir = skill_dir_for_target(target)
    if target != "generic":
        if sdir.is_dir() and (sdir / "SKILL.md").is_file():
            info(f"Skill files verified at {sdir}")
        else:
            warn(f"Skill files not found at {sdir}")

    if api_key and not non_interactive:
        info("Testing API connectivity...")
        ok, msg = test_api_connection(api_base, api_key)
        if ok:
            info(msg)
        else:
            warn(msg)


# ---------------------------------------------------------------------------
# Summary
# ---------------------------------------------------------------------------

def print_summary(targets: list, api_base: str) -> None:
    print()
    print("=" * 44)
    print("  thetix skill installed successfully")
    print("=" * 44)
    print()
    for t in targets:
        sdir = skill_dir_for_target(t)
        label = t.replace("-", " ").title()
        if t != "generic":
            print(f"  {label}:")
            print(f"    Skill:  {sdir}")
        else:
            print(f"  {label}:")
        from lib.common import config_path_for_target
        print(f"    Config: {config_path_for_target(t)}")
    print(f"  API base: {api_base}")
    print()
    print("Next steps:")
    print("  1. Start Claude Code or OpenClaw")
    print("  2. Test the skill: /thetix")
    print()
    print("Health check:  python3 scripts/doctor.py")
    print("Update:        python3 scripts/install.py --update")
    print()
    print("=" * 44)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    args = parse_args()

    # Check prerequisites
    if not git_available():
        fatal(
            "git is not installed.\n"
            "  macOS:   brew install git\n"
            "  Ubuntu:  sudo apt install git\n"
            "  Windows: https://git-scm.com/download/win"
        )

    # Resolve targets
    if args.target == "auto":
        targets = detect_targets()
        info(f"Detected platforms: {', '.join(targets)}")
    else:
        targets = [args.target]

    # Find skill source (if running from inside the repo)
    source = find_skill_source()
    if source:
        info(f"Skill source: {source}")

    # Install skill files per target
    for t in targets:
        if t == "claude-code":
            install_claude_code(source, args.clone_url, args.update)
        elif t == "openclaw":
            install_openclaw(source, args.clone_url, args.update)
        # generic needs no file installation

    # Credentials
    api_key, api_base = prompt_credentials(args, targets)

    if api_key:
        for t in targets:
            path = set_credentials(t, api_key, api_base)
            info(f"Credentials saved to {path}")

    # Verify
    for t in targets:
        verify_installation(t, api_key, api_base, args.non_interactive)

    print_summary(targets, api_base)


if __name__ == "__main__":
    main()
