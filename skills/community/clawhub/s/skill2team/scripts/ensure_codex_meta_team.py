#!/usr/bin/env python3
"""Generate/check Skill2Team's fixed Codex meta-team package and optionally register it for Codex preflight.

This script is the deterministic package/preflight helper for:

    Execution path: meta-team-first
    Target runtime: codex

It intentionally affects only team_id `s2t-meta`. It does not register any
generated target team from the user's source material and does not create a new Skill2Team delivery mode. For Codex `meta-team-first`, fallback role-play is not allowed: this helper must either confirm a usable registered meta-team or return a blocker reason.
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path
from typing import Any


SKILL_ROOT = Path(__file__).resolve().parents[1]
GENERATE_SCRIPT = SKILL_ROOT / "scripts" / "generate_deployment_package.py"
REGISTER_SCRIPT = SKILL_ROOT / "scripts" / "register_codex_agents.py"
META_REGISTRY_REL = Path(".codex") / "s2t-agent-registrations" / "s2t-meta.json"


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def runtime_files_exist(codex_root: Path, manifest: dict[str, Any]) -> bool:
    files = manifest.get("registered_files") or []
    return bool(files) and all((codex_root / rel).exists() for rel in files)


def entry_artifact_registered(manifest: dict[str, Any]) -> bool:
    entry = str(manifest.get("entry_agent_id") or "")
    files = [str(rel) for rel in manifest.get("registered_files") or []]
    return bool(entry and any(Path(rel).stem == entry for rel in files))


def usable_existing_registration(codex_root: Path, manifest: dict[str, Any]) -> bool:
    return (
        manifest.get("managed_by") == "skill2team"
        and manifest.get("team_id") == "s2t-meta"
        and manifest.get("team_kind") == "meta"
        and manifest.get("target_runtime") == "codex"
        and manifest.get("registration_status") == "registered"
        and manifest.get("entry_agent_runnable") is True
        and manifest.get("entry_agent_id") == "s2t-meta-entry"
        and entry_artifact_registered(manifest)
        and runtime_files_exist(codex_root, manifest)
    )


def meta_contract_signature() -> tuple[str, str, str]:
    contract = read_json(SKILL_ROOT / "data" / "meta_team_contract.json")
    return (
        str(contract.get("skill2team_version") or ""),
        str(contract.get("contract_version") or ""),
        _computed_meta_signature(),
    )


def _computed_meta_signature() -> str:
    # Import the canonical function from the package generator so this preflight
    # cannot drift from generated registry manifests.
    import importlib.util

    spec = importlib.util.spec_from_file_location("s2t_generate_deployment_package", GENERATE_SCRIPT)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Could not load {GENERATE_SCRIPT}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    contract = module.load_meta_team_contract()
    return module.meta_team_signature(contract)


def check_existing(codex_root: Path) -> dict[str, Any]:
    manifest_path = codex_root / META_REGISTRY_REL
    if not manifest_path.exists():
        return {
            "status": "missing",
            "usable": False,
            "manifest_path": str(manifest_path),
        }

    manifest = read_json(manifest_path)
    skill_version, contract_version, signature = meta_contract_signature()
    same_contract = (
        manifest.get("skill2team_version") == skill_version
        and manifest.get("meta_team_contract_version") == contract_version
        and manifest.get("meta_team_signature") == signature
    )
    usable = same_contract and usable_existing_registration(codex_root, manifest)
    return {
        "status": "already_registered" if usable else "mismatch_or_incomplete",
        "usable": usable,
        "manifest_path": str(manifest_path),
        "existing_skill2team_version": manifest.get("skill2team_version"),
        "expected_skill2team_version": skill_version,
        "existing_meta_team_contract_version": manifest.get("meta_team_contract_version"),
        "expected_meta_team_contract_version": contract_version,
        "existing_meta_team_signature": manifest.get("meta_team_signature"),
        "expected_meta_team_signature": signature,
        "registered_files": manifest.get("registered_files", []),
    }


def run(cmd: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(cmd, text=True, capture_output=True, check=False)


def generate_meta_package(package_dir: Path, *, route: str, current_run_fanout_status: str) -> None:
    package_dir.mkdir(parents=True, exist_ok=True)
    cmd = [
        sys.executable,
        str(GENERATE_SCRIPT),
        "--meta-team",
        str(package_dir),
        "--target",
        "codex",
        "--execution-path",
        "direct-skill",
        "--route",
        route,
        "--delivery",
        "package",
        "--current-run-fanout-status",
        current_run_fanout_status,
    ]
    result = run(cmd)
    if result.returncode != 0:
        raise SystemExit(
            "Failed to generate Skill2Team meta-team package.\n"
            f"Command: {' '.join(cmd)}\n"
            f"stdout:\n{result.stdout}\n"
            f"stderr:\n{result.stderr}"
        )


def register_meta_package(package_dir: Path, codex_root: Path, *, force_regenerate: bool, runtime_smoke_test_passed: bool) -> dict[str, Any]:
    cmd = [
        sys.executable,
        str(REGISTER_SCRIPT),
        "--package-dir",
        str(package_dir),
        "--codex-root",
        str(codex_root),
    ]
    if force_regenerate:
        cmd.append("--force-regenerate")
    if runtime_smoke_test_passed:
        cmd.append("--runtime-smoke-test-passed")
    result = run(cmd)
    if result.returncode != 0:
        raise SystemExit(
            "Failed to register Skill2Team meta-team package.\n"
            f"Command: {' '.join(cmd)}\n"
            f"stdout:\n{result.stdout}\n"
            f"stderr:\n{result.stderr}"
        )
    try:
        return json.loads(result.stdout)
    except json.JSONDecodeError:
        return {"status": "registered_unknown_output", "stdout": result.stdout}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--codex-root", default=".", help="Codex project root that contains or will contain .codex/.")
    parser.add_argument(
        "--package-dir",
        default=".skill2team/s2t-meta-codex-package",
        help="Where to generate the fixed s2t-meta Codex package before registration.",
    )
    parser.add_argument("--route", default="source-to-team", choices=[
        "source-to-team",
        "brief-to-team",
        "guided-to-team",
    ])
    parser.add_argument(
        "--current-run-fanout-status",
        default="blocked_no_real_codex_meta_team",
        choices=[
            "real_subagents",
            "real_session_subagents",
            "blocked_no_real_codex_meta_team",
            "direct-skill-not-requested",
            "not_needed_for_bare_startup",
        ],
        help="Current Skill2Team run fan-out status to record in generated meta-team package metadata. Use real_subagents only when registered s2t-meta agents actually ran. Use real_session_subagents only when the active Codex thread delegated fixed S2T work orders to real subagents while registered custom-agent smoke tests remain pending.",
    )
    parser.add_argument("--check-only", action="store_true", help="Only inspect existing s2t-meta registration.")
    parser.add_argument("--register", action="store_true", help="Explicitly register the generated fixed s2t-meta package into the given Codex project root. Not a Skill2Team delivery mode.")
    parser.add_argument(
        "--temporary-only",
        action="store_true",
        help="Explicitly bypass registration; report that Codex meta-team-first remains blocked. This never enables simulation.",
    )
    parser.add_argument(
        "--force-regenerate",
        action="store_true",
        help="Replace a different-version s2t-meta registration using manifest-scoped unregister first.",
    )
    parser.add_argument(
        "--runtime-smoke-test-passed",
        action="store_true",
        help="Set only after the Codex runtime has actually invoked s2t-meta-entry and confirmed specialist handoffs. Required before meta-team-first may claim real meta-team execution.",
    )
    args = parser.parse_args()

    codex_root = Path(args.codex_root).resolve()
    package_dir = Path(args.package_dir)
    if not package_dir.is_absolute():
        package_dir = codex_root / package_dir

    existing = check_existing(codex_root)

    if args.temporary_only:
        print(json.dumps({
            "status": "meta_team_first_blocked",
            "meta_team_registration_status": "deferred",
            "reason": "Codex meta-team-first requires registered and smoke-tested s2t-meta agents; temporary-only mode cannot satisfy this and fallback role-play is not permitted.",
            "recovery": "Register and smoke-test the fixed s2t-meta package, or rerun with Execution path: direct-skill if the user changes the execution path.",
            "existing": existing,
        }, ensure_ascii=False, indent=2))
        return 2

    if args.check_only:
        print(json.dumps(existing, ensure_ascii=False, indent=2))
        return 0 if existing.get("usable") else 1

    if existing.get("usable"):
        print(json.dumps({
            "status": "already_registered",
            "meta_team_registration_status": "already_registered",
            "entry_agent_id": "s2t-meta-entry",
            "manifest_path": existing.get("manifest_path"),
            "registered_files": existing.get("registered_files", []),
        }, ensure_ascii=False, indent=2))
        return 0

    generate_meta_package(
        package_dir,
        route=args.route,
        current_run_fanout_status="direct-skill-not-requested",
    )
    if not args.register:
        print(json.dumps({
            "status": "meta_team_first_blocked",
            "meta_team_registration_status": "not_registered",
            "package_dir": str(package_dir),
            "entry_agent_id": "s2t-meta-entry",
            "architecture_method": "framework-neutral agent architecture relationship graph with profile-based agents",
            "model_invocation_policy": "OpenAI Codex by default; API-service follow-up must be explicitly labeled",
            "reason": "The fixed s2t-meta Codex package was generated, but it is not registered and smoke-tested, so Codex meta-team-first cannot run.",
            "recovery": "Use docs/post-package-prompt-templates.md from the generated package for manifest-scoped Codex registration/use guidance, then rerun this helper with --register and record smoke-test evidence. Do not continue with a fallback run.",
            "existing": existing,
        }, ensure_ascii=False, indent=2))
        return 2

    result = register_meta_package(
        package_dir,
        codex_root,
        force_regenerate=args.force_regenerate,
        runtime_smoke_test_passed=args.runtime_smoke_test_passed,
    )
    if result.get("status") == "registered" and result.get("entry_agent_runnable") is True:
        result["meta_team_registration_status"] = "newly_registered_and_runtime_verified"
        exit_code = 0
    else:
        result.setdefault("meta_team_registration_status", "registered_but_runtime_smoke_test_required")
        result.setdefault(
            "hard_requirement",
            "meta-team-first must not claim real meta-team execution until s2t-meta-entry and specialist handoffs have passed runtime smoke tests.",
        )
        result.setdefault(
            "reason",
            "s2t-meta files may be installed, but real Codex entry invocation and specialist handoff smoke-test evidence is missing. In Codex desktop, newly written .codex/config.toml agent entries may not be hot-loaded into the current running thread. Fallback role-play is not permitted.",
        )
        result.setdefault(
            "recovery",
            "Start a fresh Codex thread or reload the workspace so registered s2t-meta agents are loaded, then run smoke tests for s2t-meta-entry, specialist handoffs, reviewer gate blocking, and state/artifact handoff. If the active thread already supports real subagent delegation, route fixed S2T work orders through those real subagents and record current_run_fanout_status=real_session_subagents while keeping registered smoke tests pending. Otherwise rerun with Execution path: direct-skill if the user changes the execution path.",
        )
        exit_code = 1
    result.setdefault("package_dir", str(package_dir))
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())
