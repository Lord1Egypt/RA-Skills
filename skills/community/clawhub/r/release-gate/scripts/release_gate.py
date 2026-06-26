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
    checklist: dict[str, list[str]],
    log_file: Optional[str] = None,
    deployer: str = "Pods",
) -> bool:
    """
    Interactive-style gate runner (for programmatic use in agent pipelines).

    This function is intentionally simple: it takes a pre-filled checklist
    (all items as strings), assumes the agent has already verified each one,
    and logs the result.

    In practice, agents should call this AFTER verifying each checklist item
    through their own tooling (running tests, reading files, etc.).

    Args:
        feature: Name of the feature/change.
        required_roles: Roles that must sign off (e.g. ["Dev", "Product"]).
        checklist: {"Dev": ["Tests pass", "No hardcoded secrets"], ...}
                   All items are assumed PASSED when passed to this function.
                   To indicate a failure, raise before calling this function.
        log_file: Optional path to log the decision.
        deployer: Name of the agent or human running the gate.

    Returns:
        True if gate passes, False if any role is missing from checklist.
    """
    missing_roles = [r for r in required_roles if r not in checklist]
    if missing_roles:
        print(f"[release-gate] BLOCKED: Missing sign-off from: {', '.join(missing_roles)}")
        if log_file:
            roles = {r: "PASS" for r in checklist}
            for r in missing_roles:
                roles[r] = "BLOCKED (no sign-off)"
            log_gate_decision(
                log_file=log_file,
                feature=feature,
                roles=roles,
                result=GateResult.BLOCKED,
                deployer=deployer,
                notes=f"Missing roles: {', '.join(missing_roles)}"
            )
        return False

    roles = {r: "PASS" for r in required_roles}
    if log_file:
        log_gate_decision(
            log_file=log_file,
            feature=feature,
            roles=roles,
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

    # Demonstrate check_gate
    all_pass, failures = check_gate({
        "Dev": [True, True, True],
        "Product": [True, False],   # one item not cleared
    })
    print(f"Gate passed: {all_pass}")
    if failures:
        print(f"Failures: {failures}")
