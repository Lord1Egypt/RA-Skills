"""
release_gate.py — Logging helper for the release-gate skill.

No framework dependencies. Pure Python stdlib.

Usage:
    from scripts.release_gate import log_gate_decision, GateResult

    log_gate_decision(
        log_file="/opt/myapp/logs/deployments.log",
        feature="Stripe checkout v1",
        roles={"Dev": "PASS", "Product": "PASS"},
        result="APPROVED",
        deployer="Pods",
        notes="systemctl restart myapp"
    )
"""

import os
from datetime import datetime, timezone
from enum import Enum
from typing import Optional


class GateResult(str, Enum):
    APPROVED = "APPROVED"
    BLOCKED = "BLOCKED"


def log_gate_decision(
    log_file: str,
    feature: str,
    roles: dict[str, str],           # {"Dev": "PASS", "Product": "BLOCKED (reason)"}
    result: GateResult | str,
    deployer: str = "Pods",
    notes: Optional[str] = None,
) -> None:
    """
    Append a gate decision to the deploy log.

    Args:
        log_file: Path to the deployments log file.
        feature: Short description of the feature/change being deployed.
        roles: Dict of role name → "PASS" or "BLOCKED (reason)".
        result: GateResult.APPROVED or GateResult.BLOCKED (or plain string).
        deployer: Name of the agent or human running the gate.
        notes: Optional extra context (command run, rollback plan, etc.).
    """
    ts = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    result_str = result.value if isinstance(result, GateResult) else str(result).upper()

    role_lines = " | ".join(f"{role}: {status}" for role, status in roles.items())

    lines = [
        f"[{ts}] {result_str}: {feature}",
        f"  Roles: {role_lines}",
        f"  Deployer: {deployer}",
    ]
    if notes:
        lines.append(f"  Notes: {notes}")
    lines.append("")  # blank line separator

    os.makedirs(os.path.dirname(os.path.abspath(log_file)), exist_ok=True)
    with open(log_file, "a") as f:
        f.write("\n".join(lines) + "\n")


def check_gate(checklist: dict[str, list[bool]]) -> tuple[bool, list[str]]:
    """
    Evaluate a checklist and return (all_passed, list_of_failures).

    Args:
        checklist: {"Role": [True, True, False], ...}
                   True = item checked/passed, False = item blocked.

    Returns:
        (True, []) if all pass.
        (False, ["Role: item index 2 not checked", ...]) if any fail.
    """
    failures = []
    for role, items in checklist.items():
        for i, passed in enumerate(items):
            if not passed:
                failures.append(f"{role}: item {i + 1} not cleared")
    return len(failures) == 0, failures


def run_release_gate(
    feature: str,
    required_roles: list[str],
    checklist: dict[str, list[dict]],
    log_file: Optional[str] = None,
    deployer: str = "agent",
) -> bool:
    """
    Gate runner for programmatic use in agent pipelines.

    Validates that:
    1. All required roles are present in the checklist.
    2. Every checklist item for each role has passed=True.

    BLOCKED if any role is missing OR any item has passed=False or is empty.
    APPROVED only when every item for every required role explicitly passes.

    Args:
        feature: Name of the feature/change being gated.
        required_roles: Roles that must sign off (e.g. ["Dev", "Product"]).
        checklist: {
            "Dev": [
                {"item": "Tests pass", "passed": True},
                {"item": "No hardcoded secrets", "passed": True},
            ],
            ...
        }
        log_file: Optional path to log the decision.
        deployer: Name of the agent or human running the gate.

    Returns:
        True if ALL required roles present and ALL items passed.
        False (and logs BLOCKED) if any role missing or any item not passed.
    """
    failures = []

    # Check all required roles are present
    missing_roles = [r for r in required_roles if r not in checklist]
    for r in missing_roles:
        failures.append(f"{r}: no sign-off provided")

    # Validate each item in present roles
    for role in required_roles:
        if role not in checklist:
            continue
        items = checklist[role]
        if not items:
            failures.append(f"{role}: checklist is empty")
            continue
        for entry in items:
            if not isinstance(entry, dict) or not entry.get("passed", False):
                label = entry.get("item", "unknown item") if isinstance(entry, dict) else str(entry)
                failures.append(f"{role}: '{label}' not cleared")

    roles_log = {}
    for r in required_roles:
        role_failures = [f for f in failures if f.startswith(f"{r}:")]
        roles_log[r] = "PASS" if not role_failures else f"BLOCKED ({'; '.join(role_failures)})"

    if failures:
        print(f"[release-gate] BLOCKED: {feature}")
        for f in failures:
            print(f"  ✗ {f}")
        if log_file:
            log_gate_decision(
                log_file=log_file,
                feature=feature,
                roles=roles_log,
                result=GateResult.BLOCKED,
                deployer=deployer,
                notes=f"Failures: {'; '.join(failures)}"
            )
        return False

    print(f"[release-gate] APPROVED: {feature}")
    if log_file:
        log_gate_decision(
            log_file=log_file,
            feature=feature,
            roles=roles_log,
            result=GateResult.APPROVED,
            deployer=deployer,
        )
    return True


# ── CLI demo ──────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    import tempfile, os

    print("=== Release Gate Demo ===\n")

    with tempfile.NamedTemporaryFile(mode="r", suffix=".log", delete=False) as f:
        log_path = f.name

    # Simulate a passing gate
    log_gate_decision(
        log_file=log_path,
        feature="Add Stripe checkout",
        roles={"Dev": "PASS", "Product": "PASS", "Legal": "PASS"},
        result=GateResult.APPROVED,
        deployer="Pods",
        notes="systemctl restart myapp"
    )

    # Simulate a blocked gate
    log_gate_decision(
        log_file=log_path,
        feature="Update pricing page",
        roles={"Dev": "PASS", "Product": "BLOCKED (pricing table not updated)"},
        result=GateResult.BLOCKED,
        deployer="Pods",
        notes="Holding until Sloane updates /pricing"
    )

    print("Log output:\n")
    with open(log_path) as f:
        print(f.read())

    os.unlink(log_path)

    # Demonstrate run_release_gate with explicit pass/fail items
    result = run_release_gate(
        feature="Add Stripe checkout",
        required_roles=["Dev", "Product"],
        checklist={
            "Dev": [
                {"item": "Tests pass", "passed": True},
                {"item": "No hardcoded secrets", "passed": True},
            ],
            "Product": [
                {"item": "Pricing page updated", "passed": True},
                {"item": "Copy accurate", "passed": False},  # blocked
            ],
        },
        log_file=log_path,
        deployer="agent",
    )
    print(f"Gate passed: {result}")  # False — Product item not cleared
