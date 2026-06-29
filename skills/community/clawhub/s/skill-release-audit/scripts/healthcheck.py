#!/usr/bin/env python3
"""
skill-healthcheck — Skill Complete Inspection Tool
Usage:
    python healthcheck.py <skill-dir>                          # report only (default)
    python healthcheck.py <skill-dir> --auto-install           # also pip-install missing deps
    python healthcheck.py <skill-dir> --auto-install --install-timeout 120
    python healthcheck.py <skill-dir> --modules 1,2,3          # run specific modules only

Note: auto-install is OFF by default — the auditor reports without modifying the
environment. --no-auto-install is kept as a deprecated no-op for backward compat.
"""

import argparse
import sys
from pathlib import Path

# Ensure sibling scripts are importable
sys.path.insert(0, str(Path(__file__).parent))

import check_logic
import check_features
import check_edges
import check_data_safety
import check_deps
from _common import load_profile, list_profiles, DEFAULT_PROFILE
from i18n import t, set_lang
import check_docs

# ---------------------------------------------------------------------------
# ANSI colors
# ---------------------------------------------------------------------------
RED = "\033[91m"
YELLOW = "\033[93m"
GREEN = "\033[92m"
CYAN = "\033[96m"
BOLD = "\033[1m"
DIM = "\033[2m"
RESET = "\033[0m"


def _status_icon(status: str) -> str:
    return {
        "PASS": f"{GREEN}✅ PASS{RESET}",
        "WARN": f"{YELLOW}⚠️  WARN{RESET}",
        "FAIL": f"{RED}❌ FAIL{RESET}",
    }.get(status, status)


def _severity_prefix(sev: str) -> str:
    return {
        "ERROR": f"{RED}[ERROR]{RESET}",
        "WARN": f"{YELLOW}[WARN] {RESET}",
        "INFO": f"{CYAN}[INFO] {RESET}",
    }.get(sev, f"[{sev}]")


def print_header(skill_name: str):
    width = 60
    print()
    print(f"{BOLD}{'─' * width}{RESET}")
    print(f"{BOLD}  🔍 skill-healthcheck: {skill_name}{RESET}")
    print(f"{BOLD}{'─' * width}{RESET}")


def print_module_result(result: dict):
    module_name = result.get("module", "?")
    status = result.get("status", "?")
    issues = result.get("issues", [])

    print(f"\n  {_status_icon(status)}  {BOLD}{module_name}{RESET}")

    # Special annotations
    if "auto_installed" in result and result["auto_installed"]:
        pkgs = ", ".join(result["auto_installed"])
        print(f"    {GREEN}{t('report.auto_installed', pkgs=pkgs)}{RESET}")

    if "tip" in result:
        print(f"    {DIM}↳ {result['tip']}{RESET}")

    if not issues:
        print(f"    {DIM}{t('report.no_issues')}{RESET}")
        return

    for issue in issues:
        prefix = _severity_prefix(issue["severity"])
        file_info = f"{DIM}{issue['file']}"
        if issue.get("line"):
            file_info += f":{issue['line']}"
        file_info += RESET

        print(f"    {prefix} {file_info}")
        # Wrap long messages
        msg = issue["message"]
        for line in msg.splitlines():
            print(f"           {line}")

        if "install_cmd" in issue:
            print(f"           {CYAN}$ {issue['install_cmd']}{RESET}")
        if "docs_url" in issue:
            print(f"           {DIM}📖 {issue['docs_url']}{RESET}")


def print_summary(results: list[dict], skill_name: str):
    total_errors = sum(
        len([i for i in r.get("issues", []) if i["severity"] == "ERROR"])
        for r in results
    )
    total_warns = sum(
        len([i for i in r.get("issues", []) if i["severity"] == "WARN"])
        for r in results
    )
    fail_modules = [r["module"] for r in results if r["status"] == "FAIL"]
    warn_modules = [r["module"] for r in results if r["status"] == "WARN"]
    pass_count = sum(1 for r in results if r["status"] == "PASS")

    print(f"\n{'─' * 60}")
    print(f"{BOLD}  {t('report.summary', name=skill_name)}{RESET}")
    print(f"{'─' * 60}")
    print(f"  {t('report.pass', n=pass_count)}")
    if warn_modules:
        print(f"  {t('report.warn', n=len(warn_modules), mods=', '.join(warn_modules))}")
    if fail_modules:
        print(f"  {t('report.fail', n=len(fail_modules), mods=', '.join(fail_modules))}")
    print()

    if total_errors == 0 and total_warns == 0:
        print(f"  {GREEN}{BOLD}{t('report.all_pass')}{RESET}")
    elif total_errors == 0:
        print(f"  {YELLOW}{t('report.warns_only', w=total_warns)}{RESET}")
    else:
        print(f"  {RED}{t('report.errors', e=total_errors, w=total_warns)}{RESET}")

    print(f"{'─' * 60}\n")

    return total_errors, total_warns


def run_healthcheck(skill_dir: Path, auto_install: bool = False,
                    modules: list[int] | None = None, install_timeout: int = 60,
                    profile: dict | None = None):
    skill_name = skill_dir.name
    profile = profile or load_profile(DEFAULT_PROFILE)
    print_header(skill_name)
    print(f"  {DIM}{t('report.target_profile', name=profile.get('name', DEFAULT_PROFILE))}{RESET}")

    all_modules = [
        (1, check_logic.run),
        (2, check_features.run),
        (3, check_edges.run),
        (4, check_data_safety.run),
        (5, lambda d: check_deps.run(d, auto_install=auto_install, install_timeout=install_timeout, profile=profile)),
        (6, lambda d: check_docs.run(d, profile=profile)),
    ]

    selected = all_modules if not modules else [m for m in all_modules if m[0] in modules]

    results = []
    for _, fn in selected:
        try:
            result = fn(skill_dir)
        except Exception as e:
            result = {
                "module": t("module.crashed"),
                "status": "FAIL",
                "issues": [{
                    "file": "healthcheck",
                    "line": None,
                    "message": t("report.module_crashed", err=e),
                    "severity": "ERROR",
                }],
            }
        print_module_result(result)
        results.append(result)

    total_errors, total_warns = print_summary(results, skill_name)
    return total_errors


def main():
    parser = argparse.ArgumentParser(
        description="skill-healthcheck: Comprehensive skill quality & safety inspector"
    )
    parser.add_argument("skill_dir", help="Path to the skill directory")
    parser.add_argument(
        "--auto-install",
        action="store_true",
        help="Automatically pip install missing Python packages "
             "(default: OFF — auditor only reports, does not modify the environment)",
    )
    parser.add_argument(
        "--no-auto-install",
        action="store_true",
        help="(deprecated, kept for backward compat — auto-install is already OFF by default)",
    )
    parser.add_argument(
        "--install-timeout",
        type=int,
        default=60,
        help="Per-package pip install timeout in seconds (only used with --auto-install; default 60)",
    )
    parser.add_argument(
        "--modules",
        help="Comma-separated list of module numbers to run (e.g. 1,3,5)",
        default=None,
    )
    parser.add_argument(
        "--target",
        default=DEFAULT_PROFILE,
        help=(
            "Publishing target to validate against (tunes checks/severity; does NOT publish). "
            f"Available: {', '.join(list_profiles())}. Default: {DEFAULT_PROFILE}"
        ),
    )
    parser.add_argument(
        "--lang",
        choices=["zh", "en"],
        default=None,
        help="Report output language (zh|en). Default: zh (or $SKILL_AUDIT_LANG).",
    )
    args = parser.parse_args()

    # Resolve language before any user-facing output.
    set_lang(args.lang)

    try:
        profile = load_profile(args.target)
    except ValueError:
        print(
            f"{RED}[ERROR] {t('cli.unknown_target', t=args.target, avail=', '.join(list_profiles()))}{RESET}",
            file=sys.stderr,
        )
        sys.exit(2)

    skill_dir = Path(args.skill_dir).resolve()
    if not skill_dir.exists():
        print(f"{RED}[ERROR] {t('cli.dir_not_found', path=skill_dir)}{RESET}", file=sys.stderr)
        sys.exit(2)

    if not (skill_dir / "SKILL.md").exists():
        print(f"{RED}[ERROR] {t('cli.not_a_skill', path=skill_dir)}{RESET}", file=sys.stderr)
        sys.exit(2)

    modules = None
    if args.modules:
        try:
            modules = [int(x.strip()) for x in args.modules.split(",")]
        except ValueError:
            print(f"{RED}[ERROR] {t('cli.bad_modules')}{RESET}", file=sys.stderr)
            sys.exit(2)

    # Auto-install is OFF by default (auditor must not silently change the env).
    # --auto-install opts in; --no-auto-install is a no-op kept for backward compat.
    auto_install = bool(args.auto_install) and not args.no_auto_install

    error_count = run_healthcheck(
        skill_dir,
        auto_install=auto_install,
        modules=modules,
        install_timeout=args.install_timeout,
        profile=profile,
    )

    # Exit code: 0 = all pass/warn, 1 = has errors
    sys.exit(1 if error_count > 0 else 0)


if __name__ == "__main__":
    main()
