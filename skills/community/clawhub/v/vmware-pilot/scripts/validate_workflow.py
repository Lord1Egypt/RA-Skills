#!/usr/bin/env python3
"""Validate a workflow YAML file before execution.

Checks:
  - Required fields (name, steps) are present
  - All referenced skills are known
  - Tool names are recognized (warns if unknown, may still be valid)
  - Approval gates are present before destructive steps
  - Step structure is well-formed

Usage:
    python3 validate_workflow.py <workflow.yaml>
    python3 validate_workflow.py ~/.vmware/workflows/*.yaml
"""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Any

VALID_SKILLS: frozenset[str] = frozenset({
    "aiops", "monitor", "nsx", "nsx-security", "aria", "vks", "storage", "pilot",
})

# Key tools per skill (not exhaustive — warns if unknown, does not error)
SKILL_TOOLS: dict[str, frozenset[str]] = {
    "aiops": frozenset({
        "vm_power_on", "vm_power_off", "deploy_linked_clone",
        "vm_create_plan", "vm_apply_plan", "vm_rollback_plan",
        "vm_guest_exec", "vm_guest_exec_output", "vm_guest_upload",
        "vm_guest_provision", "batch_clone_vms", "vm_clean_slate",
        "acknowledge_vcenter_alarm", "reset_vcenter_alarm",
        "cluster_create", "deploy_vm_from_ova", "deploy_vm_from_template",
    }),
    "monitor": frozenset({
        "list_virtual_machines", "list_esxi_hosts", "list_all_datastores",
        "list_all_clusters", "get_alarms", "get_events", "vm_info",
    }),
    "nsx": frozenset({
        "list_segments", "create_segment", "delete_segment",
        "create_tier1_gateway", "create_nat_rule", "list_nat_rules",
    }),
    "nsx-security": frozenset({
        "list_dfw_policies", "create_dfw_policy", "create_dfw_rule",
        "delete_dfw_rule", "create_group", "run_traceflow",
    }),
    "aria": frozenset({
        "list_alerts", "acknowledge_alert", "get_capacity_overview",
        "get_remaining_capacity", "get_time_remaining",
        "list_anomalies", "list_rightsizing_recommendations", "generate_report",
    }),
    "vks": frozenset({
        "create_namespace", "delete_namespace",
        "create_tkc_cluster", "scale_tkc_cluster", "delete_tkc_cluster",
        "get_tkc_kubeconfig",
    }),
    "storage": frozenset({
        "list_all_datastores", "storage_iscsi_enable",
        "storage_iscsi_add_target", "storage_rescan",
        "vsan_health", "vsan_capacity",
    }),
    "pilot": frozenset({
        "approve",
    }),
}

# Tools considered destructive — should have an approval gate before them
DESTRUCTIVE_TOOLS: frozenset[str] = frozenset({
    "vm_power_off", "vm_clean_slate", "vm_apply_plan",
    "delete_segment", "delete_dfw_rule", "delete_namespace",
    "delete_tkc_cluster", "batch_clone_vms",
})


def validate(path: Path) -> tuple[list[str], list[str]]:
    """Validate a workflow YAML file.

    Returns (errors, warnings) lists.
    """
    try:
        import yaml
    except ImportError:
        return (["pyyaml is not installed — run: pip install pyyaml"], [])

    errors: list[str] = []
    warnings: list[str] = []

    try:
        with open(path) as f:
            spec: Any = yaml.safe_load(f)
    except Exception as exc:
        return ([f"Failed to parse YAML: {exc}"], [])

    if not isinstance(spec, dict):
        return ([f"Expected a YAML mapping, got {type(spec).__name__}"], [])

    # Required fields
    if "name" not in spec:
        errors.append("Missing required field: 'name'")

    if "steps" not in spec:
        errors.append("Missing required field: 'steps'")
        return (errors, warnings)

    steps = spec["steps"]
    if not isinstance(steps, list):
        errors.append(f"'steps' must be a list, got {type(steps).__name__}")
        return (errors, warnings)

    if len(steps) == 0:
        errors.append("'steps' list is empty")
        return (errors, warnings)

    if len(steps) > 20:
        warnings.append(
            f"Workflow has {len(steps)} steps — consider splitting into "
            f"multiple workflows (recommended max: 15)"
        )

    # Track whether we have seen an approval gate
    has_approval = False
    approval_indices: list[int] = []
    destructive_before_approval: list[tuple[int, str]] = []

    for i, step in enumerate(steps):
        if not isinstance(step, dict):
            errors.append(f"Step {i}: expected a mapping, got {type(step).__name__}")
            continue

        # Check required step fields
        if "action" not in step:
            errors.append(f"Step {i}: missing 'action' field")
        if "skill" not in step:
            errors.append(f"Step {i}: missing 'skill' field")
        if "tool" not in step:
            errors.append(f"Step {i}: missing 'tool' field")

        skill = step.get("skill", "")
        tool = step.get("tool", "")
        action = step.get("action", "")

        # Validate skill
        if skill and skill not in VALID_SKILLS:
            errors.append(f"Step {i}: unknown skill '{skill}' (valid: {', '.join(sorted(VALID_SKILLS))})")

        # Validate tool (warn only — tool list may not be exhaustive)
        if skill and tool and skill in SKILL_TOOLS:
            if tool not in SKILL_TOOLS[skill]:
                warnings.append(
                    f"Step {i}: tool '{tool}' not in known tools for '{skill}' "
                    f"(may still be valid if recently added)"
                )

        # Track approval gates
        if action == "require_approval":
            has_approval = True
            approval_indices.append(i)

        # Track destructive steps before any approval gate
        if tool in DESTRUCTIVE_TOOLS and not has_approval:
            destructive_before_approval.append((i, tool))

        # Validate rollback references
        rollback_tool = step.get("rollback_tool", "")
        if rollback_tool and skill in SKILL_TOOLS:
            if rollback_tool not in SKILL_TOOLS.get(skill, frozenset()):
                warnings.append(
                    f"Step {i}: rollback_tool '{rollback_tool}' not in known "
                    f"tools for '{skill}'"
                )

        # Check params is a dict
        params = step.get("params")
        if params is not None and not isinstance(params, dict):
            errors.append(f"Step {i}: 'params' must be a mapping, got {type(params).__name__}")

        rollback_params = step.get("rollback_params")
        if rollback_params is not None and not isinstance(rollback_params, dict):
            errors.append(
                f"Step {i}: 'rollback_params' must be a mapping, "
                f"got {type(rollback_params).__name__}"
            )

    # Warn about missing approval gate
    if not has_approval:
        warnings.append(
            "No approval gate found — consider adding one before destructive steps"
        )

    # Warn about destructive steps before any approval gate
    for idx, tool_name in destructive_before_approval:
        warnings.append(
            f"Step {idx}: destructive tool '{tool_name}' appears before "
            f"any approval gate"
        )

    return (errors, warnings)


def main() -> int:
    if len(sys.argv) < 2:
        print("Usage: python3 validate_workflow.py <workflow.yaml> [workflow2.yaml ...]")
        print()
        print("Validates workflow YAML files for vmware-pilot.")
        print("Checks skills, tools, approval gates, and step structure.")
        return 1

    exit_code = 0

    for arg in sys.argv[1:]:
        path = Path(arg)
        if not path.exists():
            print(f"File not found: {path}")
            exit_code = 1
            continue

        if len(sys.argv) > 2:
            print(f"\n--- {path.name} ---")

        errors, warnings = validate(path)

        if errors:
            print(f"ERRORS ({len(errors)}):")
            for e in errors:
                print(f"  x {e}")
            exit_code = 1

        if warnings:
            print(f"WARNINGS ({len(warnings)}):")
            for w in warnings:
                print(f"  ! {w}")

        if not errors and not warnings:
            print(f"OK: {path.name} is valid")

    return exit_code


if __name__ == "__main__":
    sys.exit(main())
