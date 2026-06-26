#!/usr/bin/env python3
"""Cross-platform skill installer for Weekend Scout.

Copies the generated skill files to the user's global skill directory for one
or more agent platforms, then optionally installs the Python package and
pre-downloads GeoNames data.

Usage:
    python install/install_skill.py                        # advanced: copy only, requires existing package install
    python install/install_skill.py --platform claude-code # advanced: copy only for one platform
    python install/install_skill.py --platform all         # advanced: copy only for all platforms
    python install/install_skill.py --with-pip             # recommended bootstrap install
    python install/install_skill.py --with-pip --runtime-only  # install/update runtime only, skip skill-copy side effects
    python install/install_skill.py --with-pip --break-system-packages  # explicit PEP 668 override
    python install/install_skill.py --with-pip --dev       # developer install (editable)
    python install/install_skill.py --uninstall            # remove installed skill files and package
"""

from __future__ import annotations

import argparse
import os
import shutil
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

# Allow the bootstrap installer to import repo-local helpers before pip install.
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from weekend_scout.skill_install import copy_skill_tree

# Source directories inside the repo (relative to repo root)
SOURCE_DIRS: dict[str, str] = {
    "claude-code": ".claude/skills/weekend-scout",
    "codex": ".agents/skills/weekend-scout",
    "openclaw": ".openclaw/skills/weekend-scout",
}

# User-scoped global installation directories
INSTALL_TARGETS: dict[str, Path] = {
    "claude-code": Path.home() / ".claude" / "skills" / "weekend-scout",
    "codex": Path.home() / ".agents" / "skills" / "weekend-scout",
    "openclaw": Path.home() / ".openclaw" / "skills" / "weekend-scout",
}

# Directories used only for platform auto-detection.
PLATFORM_DETECTION_DIRS: dict[str, tuple[Path, ...]] = {
    "claude-code": (Path.home() / ".claude",),
    # Codex installs skills into ~/.agents/skills, but installations may expose
    # either ~/.codex or ~/.agents as a platform marker on disk.
    "codex": (Path.home() / ".codex", Path.home() / ".agents"),
    "openclaw": (Path.home() / ".openclaw",),
}

INVOKE_CMDS: dict[str, str] = {
    "claude-code": "/weekend-scout",
    "codex": "$weekend-scout",
    "openclaw": "weekend-scout",
}

_RUNTIME_CHECK_CODE = (
    "import importlib.metadata as metadata; "
    "metadata.version('weekend-scout'); "
    "import requests; "
    "import yaml"
)
SYSTEM_PIP_RECOVERY_COMMANDS: tuple[tuple[str, str], ...] = (
    ("apt-get", "sudo apt update && sudo apt install python3-venv python3-pip"),
    ("dnf", "sudo dnf install python3-pip python3-wheel"),
    ("yum", "sudo yum install python3-pip"),
    ("zypper", "sudo zypper install python3-pip python3-setuptools python3-wheel"),
    ("pacman", "sudo pacman -S python-pip"),
)
PEP_668_MARKERS: tuple[str, ...] = (
    "externally-managed-environment",
    "externally managed",
    "pep 668",
)


def detect_platforms() -> list[str]:
    """Auto-detect which platforms are installed based on detection dirs."""
    detected = [p for p, dirs in PLATFORM_DETECTION_DIRS.items() if any(d.exists() for d in dirs)]
    # OpenClaw creates ~/.agents for Plugin Bundles; don't also install the Codex skill there.
    if "openclaw" in detected and "codex" in detected:
        detected.remove("codex")
        print("OpenClaw detected: skipping Codex install (~/.agents is used by OpenClaw Plugin Bundles).")
    if not detected:
        print("No platform home directories found; defaulting to claude-code.")
        return ["claude-code"]
    if len(detected) > 1:
        names = ", ".join(detected)
        print(f"Multiple platforms detected: {names}; installing to all detected platforms.")
    return detected


def resolve_install_platforms(platform_arg: str | None) -> list[str]:
    """Resolve platform targets for install mode."""
    if platform_arg == "all":
        return list(SOURCE_DIRS.keys())
    if platform_arg:
        if platform_arg not in SOURCE_DIRS:
            print(f"Error: unknown platform '{platform_arg}'.", file=sys.stderr)
            print(f"Available: {', '.join(SOURCE_DIRS)} or 'all'", file=sys.stderr)
            sys.exit(1)
        return [platform_arg]
    return detect_platforms()


def resolve_uninstall_platforms(platform_arg: str | None) -> list[str]:
    """Resolve platform targets for uninstall mode."""
    if platform_arg == "all":
        return list(INSTALL_TARGETS.keys())
    if platform_arg:
        if platform_arg not in INSTALL_TARGETS:
            print(f"Error: unknown platform '{platform_arg}'.", file=sys.stderr)
            print(f"Available: {', '.join(INSTALL_TARGETS)} or 'all'", file=sys.stderr)
            sys.exit(1)
        return [platform_arg]
    return [name for name, target in INSTALL_TARGETS.items() if target.exists()]


def install_platform(platform: str, repo_root: Path) -> bool:
    """Copy skill files from repo to the user's global skill directory."""
    source = repo_root / SOURCE_DIRS[platform]
    target = INSTALL_TARGETS[platform]

    if not source.exists():
        print(f"  ERROR: source directory not found: {source}")
        print(f"  Run: python skill_template/generate.py --platform {platform}")
        return False

    copy_skill_tree(source, target, executable=sys.executable)

    print(f"  Installed to: {target}")
    return True


def uninstall_platform(platform: str) -> dict[str, str]:
    """Remove one installed global skill directory."""
    target = INSTALL_TARGETS[platform]
    if not target.exists():
        return {"platform": platform, "status": "not_found", "path": str(target)}

    try:
        shutil.rmtree(target)
    except OSError as exc:
        return {
            "platform": platform,
            "status": "failed",
            "path": str(target),
            "detail": str(exc),
        }
    return {"platform": platform, "status": "removed", "path": str(target)}


def check_existing_runtime(executable: str) -> tuple[bool, str]:
    """Verify that one interpreter already has the installed runtime needed by the skill."""
    result = subprocess.run(
        [executable, "-c", _RUNTIME_CHECK_CODE],
        check=False,
        capture_output=True,
        text=True,
        cwd=Path.home(),
    )
    if result.returncode == 0:
        return True, ""

    detail = (result.stderr or result.stdout).strip()
    message = (
        "This direct-copy path requires the same Python interpreter to already have "
        "the installed Weekend Scout package and runtime dependencies available."
    )
    if detail:
        message = f"{message} Details: {detail.splitlines()[-1]}"
    return False, message


def suggest_system_pip_install_command() -> str | None:
    """Return a distro-aware pip recovery command when a known package manager exists."""
    for tool, command in SYSTEM_PIP_RECOVERY_COMMANDS:
        if shutil.which(tool):
            return command
    return None


def _ensure_python_symlink() -> None:
    """On POSIX, create ~/.local/bin/python -> python3 if 'python' is not in PATH."""
    if os.name != "posix":
        return
    if shutil.which("python"):
        return
    py3 = shutil.which("python3")
    if not py3:
        return
    local_bin = Path.home() / ".local" / "bin"
    local_bin.mkdir(parents=True, exist_ok=True)
    link = local_bin / "python"
    if link.exists():
        return
    try:
        link.symlink_to(py3)
        print(f"  Created python -> {py3} in {local_bin}")
        print(
            f"  Ensure {local_bin} is in your PATH (e.g. add to ~/.bashrc: "
            'export PATH="$HOME/.local/bin:$PATH")'
        )
    except OSError as e:
        print(f"  Note: Could not create python symlink ({e}).", file=sys.stderr)
        print(f"  If needed, run: sudo ln -s {py3} /usr/local/bin/python", file=sys.stderr)


def format_retry_command(argv: list[str]) -> str:
    """Return the exact installer command the user should rerun."""
    parts = ["python", "install/install_skill.py", *argv[1:]]
    return " ".join(parts)


def emit_pip_recovery_guidance(*, detail: str, argv: list[str]) -> None:
    """Print platform-aware manual recovery guidance after failed ensurepip bootstrap."""
    print("ERROR: pip is unavailable for this Python interpreter.", file=sys.stderr)
    print(
        "Tried `python -m ensurepip --upgrade --default-pip`, but this Python build may omit ensurepip.",
        file=sys.stderr,
    )
    if detail:
        print(f"Details: {detail.splitlines()[-1]}", file=sys.stderr)

    if os.name == "nt":
        print(
            "Repair or reinstall this Python installation so `pip` is included for that interpreter.",
            file=sys.stderr,
        )
    elif os.name == "posix":
        suggested_fix = suggest_system_pip_install_command()
        if suggested_fix:
            print("Suggested fix for this system:", file=sys.stderr)
            print(f"  {suggested_fix}", file=sys.stderr)
        else:
            print(
                "Install pip for this interpreter with your Linux distribution package manager.",
                file=sys.stderr,
            )
    else:
        print(
            "Install pip for this interpreter manually, then rerun the installer.",
            file=sys.stderr,
        )

    print(f"Then rerun: `{format_retry_command(argv)}`", file=sys.stderr)


def emit_pip_missing_pep668_guidance(argv: list[str]) -> None:
    """Print two-step guidance when pip is absent and PEP 668 blocked ensurepip bootstrap."""
    retry_args = argv[1:]
    if "--break-system-packages" not in retry_args:
        retry_args = [*retry_args, "--break-system-packages"]
    retry_command = format_retry_command(["install/install_skill.py", *retry_args])

    print(
        "ERROR: pip is not installed, and its bootstrap was blocked by an"
        " externally managed Python environment (PEP 668).",
        file=sys.stderr,
    )
    if os.name == "posix":
        suggested_fix = suggest_system_pip_install_command()
        if suggested_fix:
            print("Step 1 — Install pip via your system package manager:", file=sys.stderr)
            print(f"  {suggested_fix}", file=sys.stderr)
        else:
            print(
                "Step 1 — Install pip via your Linux distribution package manager.",
                file=sys.stderr,
            )
        print(
            "Step 2 — Rerun with --break-system-packages to allow the weekend-scout install:",
            file=sys.stderr,
        )
        print(f"  {retry_command}", file=sys.stderr)
    else:
        # Unexpected: PEP 668 is a Linux-only concern, but handle gracefully
        print(
            "Reinstall Python so that pip is available, then rerun:", file=sys.stderr
        )
        print(f"  {retry_command}", file=sys.stderr)


def is_pep_668_error(output: str) -> bool:
    """Return True when pip output indicates an externally managed environment."""
    lowered = output.lower()
    return any(marker in lowered for marker in PEP_668_MARKERS)


def emit_pep_668_guidance(argv: list[str]) -> None:
    """Print targeted guidance for externally managed system Python installs."""
    retry_args = argv[1:]
    if "--break-system-packages" not in retry_args:
        retry_args = [*retry_args, "--break-system-packages"]
    retry_command = format_retry_command(["install/install_skill.py", *retry_args])

    print(
        "ERROR: pip install was blocked because this Python interpreter is externally managed (PEP 668).",
        file=sys.stderr,
    )
    print("Recommended one-shot retry:", file=sys.stderr)
    print(f"  {retry_command}", file=sys.stderr)
    print("Optional persistent workaround:", file=sys.stderr)
    print("  pip config set global.break-system-packages true", file=sys.stderr)
    print(
        "The flag is safer than the global pip config because it only affects this installation command.",
        file=sys.stderr,
    )


def emit_uninstall_pep_668_guidance(argv: list[str]) -> None:
    """Print targeted guidance for uninstall in externally managed system Python installs."""
    retry_args = argv[1:]
    if "--break-system-packages" not in retry_args:
        retry_args = [*retry_args, "--break-system-packages"]
    retry_command = format_retry_command(["install/install_skill.py", *retry_args])

    print(
        "ERROR: pip uninstall was blocked because this Python interpreter is externally managed (PEP 668).",
        file=sys.stderr,
    )
    print("Recommended one-shot retry:", file=sys.stderr)
    print(f"  {retry_command}", file=sys.stderr)
    print("Optional persistent workaround:", file=sys.stderr)
    print("  pip config set global.break-system-packages true", file=sys.stderr)
    print(
        "The flag is safer than the global pip config because it only affects this uninstall command.",
        file=sys.stderr,
    )


def ensure_pip_available(executable: str) -> None:
    """Bootstrap pip from the stdlib when the chosen interpreter does not have it."""
    result = subprocess.run(
        [executable, "-m", "pip", "--version"],
        check=False,
        capture_output=True,
        text=True,
    )
    if result.returncode == 0:
        return

    print("pip is missing; bootstrapping with ensurepip...")
    ensurepip_result = subprocess.run(
        [executable, "-m", "ensurepip", "--upgrade", "--default-pip"],
        check=False,
        capture_output=True,
        text=True,
    )
    retry = subprocess.run(
        [executable, "-m", "pip", "--version"],
        check=False,
        capture_output=True,
        text=True,
    )
    if retry.returncode == 0:
        return

    detail = (
        ensurepip_result.stderr
        or ensurepip_result.stdout
        or retry.stderr
        or retry.stdout
    ).strip()

    # If ensurepip was blocked by PEP 668 (externally managed environment) or
    # disabled by Debian/Ubuntu for system Python, show two-step guidance.
    # Otherwise, show generic pip installation guidance.
    is_system_restriction = is_pep_668_error(detail) or "ensurepip is disabled" in detail.lower()
    if is_system_restriction:
        emit_pip_missing_pep668_guidance(argv=sys.argv)
    else:
        emit_pip_recovery_guidance(detail=detail, argv=sys.argv)
    sys.exit(1)


def install_via_package_cli(platforms: list[str]) -> None:
    """Copy bundled skill files from the installed package for the resolved platforms."""
    for platform in platforms:
        print(f"\nInstalling skill via package CLI (--platform {platform})...")
        result = subprocess.run(
            [sys.executable, "-m", "weekend_scout", "install-skill", "--platform", platform],
            check=False,
            cwd=Path.home(),
        )
        if result.returncode != 0:
            print(
                f"ERROR: install-skill failed after pip install for platform '{platform}'.",
                file=sys.stderr,
            )
            sys.exit(result.returncode or 1)


def uninstall_package(executable: str, *, break_system_packages: bool) -> dict[str, str]:
    """Uninstall the weekend-scout package from the selected interpreter."""
    ensure_pip_available(executable)
    cmd = [executable, "-m", "pip", "uninstall", "-y", "weekend-scout"]
    if break_system_packages:
        cmd.append("--break-system-packages")
    result = subprocess.run(
        cmd,
        check=False,
        capture_output=True,
        text=True,
        cwd=Path.home(),
    )
    output = f"{result.stdout or ''}\n{result.stderr or ''}".strip()
    if result.returncode == 0:
        lowered = output.lower()
        if "not installed" in lowered or "skipping weekend-scout" in lowered:
            return {"status": "not_found", "detail": output}
        return {"status": "removed", "detail": output}

    if is_pep_668_error(output) and not break_system_packages:
        emit_uninstall_pep_668_guidance(sys.argv)
        sys.exit(result.returncode or 1)

    print("ERROR: pip uninstall failed.", file=sys.stderr)
    if output:
        print(output.splitlines()[-1], file=sys.stderr)
    sys.exit(result.returncode or 1)


def print_uninstall_summary(platform_results: list[dict[str, str]], package_result: dict[str, str]) -> None:
    """Print a concise uninstall summary."""
    print("\n" + "=" * 50)
    print("Weekend Scout uninstall summary")
    if platform_results:
        for result in platform_results:
            status = result["status"]
            if status == "removed":
                print(f"  {result['platform']}: removed {result['path']}")
            elif status == "failed":
                print(f"  {result['platform']}: failed to remove {result['path']}")
            else:
                print(f"  {result['platform']}: not found ({result['path']})")
    else:
        print("  skill files: no installed platform directories found")

    if package_result["status"] == "removed":
        print("  package: removed weekend-scout from this Python interpreter")
    else:
        print("  package: weekend-scout was not installed in this Python interpreter")

    print("  runtime data: preserved in .weekend_scout/")
    print("=" * 50)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Install the Weekend Scout skill or Python runtime."
    )
    parser.add_argument(
        "--platform",
        metavar="NAME",
        help=(
            "Platform to install to: claude-code, codex, openclaw, or 'all'. "
            "Default: auto-detect for install; existing installed targets for uninstall."
        ),
    )
    parser.add_argument(
        "--with-pip",
        action="store_true",
        help="Recommended bootstrap flow: install the Python package via pip before copying the skill.",
    )
    parser.add_argument(
        "--runtime-only",
        action="store_true",
        help=(
            "Install or update the Python runtime only and skip copying any skill files. "
            "Requires --with-pip or --dev and cannot be combined with --platform."
        ),
    )
    parser.add_argument(
        "--break-system-packages",
        action="store_true",
        help="Pass pip's --break-system-packages override when installing into an externally managed Python.",
    )
    parser.add_argument(
        "--dev",
        action="store_true",
        help="Developer install: use 'pip install -e .[dev]' (editable, includes test deps). Implies --with-pip.",
    )
    parser.add_argument(
        "--uninstall",
        action="store_true",
        help="Remove installed global skill files and uninstall the weekend-scout package from this interpreter.",
    )
    args = parser.parse_args()

    if args.uninstall and args.with_pip:
        parser.error("--uninstall cannot be combined with --with-pip")
    if args.uninstall and args.dev:
        parser.error("--uninstall cannot be combined with --dev")
    if args.uninstall and args.runtime_only:
        parser.error("--uninstall cannot be combined with --runtime-only")
    if args.runtime_only and args.platform:
        parser.error("--runtime-only cannot be combined with --platform")
    if args.runtime_only and not (args.with_pip or args.dev):
        parser.error("--runtime-only requires --with-pip or --dev")

    repo_root = REPO_ROOT

    if args.uninstall:
        platforms = resolve_uninstall_platforms(args.platform)
    elif args.runtime_only:
        platforms = []
    else:
        platforms = resolve_install_platforms(args.platform)

    if args.uninstall:
        platform_results = [uninstall_platform(platform) for platform in platforms]
        package_result = uninstall_package(
            sys.executable,
            break_system_packages=args.break_system_packages,
        )
        print_uninstall_summary(platform_results, package_result)
        if any(result["status"] == "failed" for result in platform_results):
            sys.exit(1)
        return

    do_pip = args.with_pip or args.dev
    if do_pip:
        ensure_pip_available(sys.executable)
        if args.dev:
            print("Installing Python package (developer/editable mode)...")
            pip_cmd = [sys.executable, "-m", "pip", "install", "-e", ".[dev]"]
        else:
            print("Installing Python package...")
            pip_cmd = [sys.executable, "-m", "pip", "install", "."]
        if args.break_system_packages:
            pip_cmd.append("--break-system-packages")
        result = subprocess.run(pip_cmd, check=False, cwd=repo_root)
        if result.returncode != 0:
            pip_output = f"{result.stdout or ''}\n{result.stderr or ''}".strip()
            if is_pep_668_error(pip_output) and not args.break_system_packages:
                emit_pep_668_guidance(sys.argv)
                sys.exit(result.returncode or 1)
            print("ERROR: pip install failed. Aborting skill installation.", file=sys.stderr)
            sys.exit(result.returncode or 1)
        print("  Package installed.")
        _ensure_python_symlink()

        if not args.runtime_only:
            # Delegate skill copying to the installed package so it reads from
            # its own skill_data/ directory (works after the clone is deleted).
            install_via_package_cli(platforms)
    else:
        runtime_ok, runtime_message = check_existing_runtime(sys.executable)
        if not runtime_ok:
            print("ERROR: Cannot install skill files without a ready Python runtime.", file=sys.stderr)
            print(runtime_message, file=sys.stderr)
            print("Run `python install/install_skill.py --with-pip` instead.", file=sys.stderr)
            print(
                "Or install the package first, then use `python -m weekend_scout install-skill --platform ...`.",
                file=sys.stderr,
            )
            sys.exit(1)

        all_ok = True
        for platform in platforms:
            print(f"\nInstalling skill for {platform}...")
            ok = install_platform(platform, repo_root)
            if not ok:
                all_ok = False
        if not all_ok:
            print("\nSome platforms failed; see errors above.")
            sys.exit(1)

    print("\nPre-downloading GeoNames city data...")
    result = subprocess.run(
        [sys.executable, "-m", "weekend_scout", "download-data"],
        check=False,
        cwd=Path.home(),
    )
    if result.returncode != 0:
        print("WARNING: GeoNames download failed. Data will be downloaded on first run.")

    print("\n" + "=" * 50)
    if args.runtime_only:
        print("Weekend Scout runtime installed successfully!")
        if args.dev:
            print("\nDeveloper/editable runtime install complete. Keep this repo for the editable package.")
        else:
            print("\nThe Python package is installed for this interpreter from the current bundle.")
        print("Bundled skill files were not copied to any shared/global skill directory.")
        print("=" * 50)
        return

    print("Weekend Scout installed successfully!")
    if do_pip and not args.dev:
        print("\nThe package is installed for this Python interpreter. You can safely delete this folder.")
        print("To update later: re-clone and re-run this installer.")
    elif args.dev:
        print("\nDeveloper/editable install complete. Keep this repo for the editable package.")
    else:
        print("\nUsed the existing Python environment without running pip.")
        print("Keep this repo if that environment is an editable install from this checkout.")
    print("\nNext steps:")
    for platform in platforms:
        cmd = INVOKE_CMDS[platform]
        print(f"  {platform}: type '{cmd}' to start scouting")
    print("=" * 50)


if __name__ == "__main__":
    main()
