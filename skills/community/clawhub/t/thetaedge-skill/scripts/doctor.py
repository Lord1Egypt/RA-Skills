#!/usr/bin/env python3
"""
Health check for the thetaedge-skill (thetix) installation.

Verifies skill files, credentials, API connectivity, and permissions.

Usage:
    python3 scripts/doctor.py
    python3 scripts/doctor.py --target claude-code
    python3 scripts/doctor.py --json
"""

import argparse
import json
import os
import stat
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lib.common import (
    DEFAULT_API_BASE,
    config_path_for_target,
    detect_os,
    detect_targets,
    get_credentials,
    git_available,
    is_windows,
    print_status,
    run_git,
    skill_dir_for_target,
    test_api_connection,
    validate_api_key,
)


class CheckResult:
    def __init__(self, name: str, status: str, message: str, detail: str = ""):
        self.name = name
        self.status = status  # "pass", "warn", "fail"
        self.message = message
        self.detail = detail

    def to_dict(self) -> dict:
        d = {"name": self.name, "status": self.status, "message": self.message}
        if self.detail:
            d["detail"] = self.detail
        return d


def check_python_version() -> CheckResult:
    v = sys.version_info
    ver_str = f"Python {v.major}.{v.minor}.{v.micro}"
    if v >= (3, 7):
        return CheckResult("python_version", "pass", ver_str)
    return CheckResult(
        "python_version", "fail", f"{ver_str} (need 3.7+)",
        "Download from https://www.python.org/downloads/",
    )


def check_git() -> CheckResult:
    if git_available():
        return CheckResult("git", "pass", "git found on PATH")
    return CheckResult(
        "git", "fail", "git not found",
        "Install: brew install git / sudo apt install git / https://git-scm.com",
    )


def check_skill_installed(target: str) -> CheckResult:
    sdir = skill_dir_for_target(target)
    if not sdir or target == "generic":
        return CheckResult(
            f"skill_installed_{target}", "pass",
            f"No skill directory needed for {target}",
        )
    if sdir.is_dir() and (sdir / "SKILL.md").is_file():
        return CheckResult(
            f"skill_installed_{target}", "pass",
            f"Skill installed at {sdir}",
        )
    return CheckResult(
        f"skill_installed_{target}", "fail",
        f"Skill not found at {sdir}",
        "Run: python3 scripts/install.py",
    )


def check_skill_up_to_date(target: str) -> CheckResult:
    sdir = skill_dir_for_target(target)
    name = f"skill_up_to_date_{target}"
    if not sdir or target == "generic":
        return CheckResult(name, "pass", "N/A for generic")

    # Resolve through symlinks
    real = sdir.resolve() if sdir.is_symlink() else sdir
    if not (real / ".git").is_dir():
        return CheckResult(name, "warn", "Not a git repo, cannot check for updates")

    # Fetch to see if remote has newer commits
    fetch = run_git("fetch", "--dry-run", cwd=real)
    if fetch.returncode != 0:
        return CheckResult(name, "warn", "Could not fetch remote (offline?)")

    run_git("fetch", cwd=real)
    status = run_git("status", "-sb", cwd=real)
    if status.returncode != 0:
        return CheckResult(name, "warn", "Could not determine git status")

    output = status.stdout.strip()
    if "behind" in output:
        # Extract count
        behind = ""
        for part in output.split():
            if part.startswith("behind"):
                idx = output.find("behind")
                behind = output[idx:]
                break
        return CheckResult(
            name, "warn", f"Skill is {behind}",
            "Run: python3 scripts/install.py --update",
        )
    return CheckResult(name, "pass", "Skill is up to date")


def check_credentials(target: str) -> CheckResult:
    api_key, api_base = get_credentials(target)
    cfg = config_path_for_target(target)
    name = f"credentials_{target}"

    if not api_key:
        label = target.replace("-", " ").title()
        return CheckResult(
            name, "fail", f"No API key in {cfg}",
            f"Run: python3 scripts/install.py --target {target}",
        )
    # Mask key for display
    masked = api_key[:6] + "..." if len(api_key) > 6 else api_key
    return CheckResult(name, "pass", f"API key configured ({masked}) in {cfg}")


def check_api_key_format(target: str) -> CheckResult:
    api_key, _ = get_credentials(target)
    name = f"api_key_format_{target}"
    if not api_key:
        return CheckResult(name, "fail", "No API key to validate")
    ok, msg = validate_api_key(api_key)
    if ok:
        return CheckResult(name, "pass", msg)
    return CheckResult(
        name, "warn", msg,
        "Get a key at Profile > API Keys on ThetaEdge",
    )


def check_api_connection(target: str) -> CheckResult:
    api_key, api_base = get_credentials(target)
    name = f"api_connection_{target}"
    if not api_key:
        return CheckResult(name, "fail", "No API key — skipping connection test")
    ok, msg = test_api_connection(api_base, api_key)
    if ok:
        return CheckResult(name, "pass", f"{msg} by {api_base}")
    return CheckResult(name, "fail", msg)


def check_config_permissions(target: str) -> CheckResult:
    name = f"config_permissions_{target}"
    if is_windows():
        return CheckResult(name, "pass", "Permission check skipped on Windows")

    cfg = config_path_for_target(target)
    if not cfg.is_file():
        return CheckResult(name, "pass", "Config file does not exist yet")

    mode = stat.S_IMODE(os.stat(cfg).st_mode)
    if mode & (stat.S_IRGRP | stat.S_IROTH | stat.S_IWGRP | stat.S_IWOTH):
        perms = oct(mode)
        return CheckResult(
            name, "warn", f"{cfg} is too permissive ({perms})",
            f"Run: chmod 600 {cfg}",
        )
    return CheckResult(name, "pass", f"Config permissions OK ({oct(mode)})")


# ---------------------------------------------------------------------------
# Runner
# ---------------------------------------------------------------------------

def run_checks(targets: list) -> list:
    results = []

    # Global checks
    results.append(check_python_version())
    results.append(check_git())

    # Per-target checks
    for t in targets:
        results.append(check_skill_installed(t))
        results.append(check_skill_up_to_date(t))
        results.append(check_credentials(t))
        results.append(check_api_key_format(t))
        results.append(check_api_connection(t))
        results.append(check_config_permissions(t))

    return results


def print_results(results: list, as_json: bool) -> int:
    counts = {"pass": 0, "warn": 0, "fail": 0}
    for r in results:
        counts[r.status] += 1

    if as_json:
        output = {
            "checks": [r.to_dict() for r in results],
            "summary": counts,
        }
        print(json.dumps(output, indent=2))
    else:
        print()
        print("Thetix Skill Health Check")
        print("=" * 40)
        print()
        for r in results:
            print_status(r.status, r.message, r.detail)
        print()
        parts = []
        if counts["pass"]:
            parts.append(f"{counts['pass']} passed")
        if counts["warn"]:
            parts.append(f"{counts['warn']} warning{'s' if counts['warn'] != 1 else ''}")
        if counts["fail"]:
            parts.append(f"{counts['fail']} failed")
        print(f"  {', '.join(parts)}")
        print()

    return 1 if counts["fail"] > 0 else 0


def main() -> None:
    p = argparse.ArgumentParser(description="Check thetix skill installation health.")
    p.add_argument(
        "--target",
        choices=["auto", "claude-code", "openclaw", "generic"],
        default="auto",
        help="Platform to check (default: auto-detect all)",
    )
    p.add_argument("--json", action="store_true", dest="as_json", help="Output as JSON")
    p.add_argument("--verbose", action="store_true", help="Show detailed output")
    args = p.parse_args()

    if args.target == "auto":
        targets = detect_targets()
    else:
        targets = [args.target]

    results = run_checks(targets)
    exit_code = print_results(results, args.as_json)
    sys.exit(exit_code)


if __name__ == "__main__":
    main()
