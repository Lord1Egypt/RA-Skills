#!/usr/bin/env python3
"""Validate a custom workflow YAML file before pilot loads it.

Checks:
  - Required fields (name, steps) are present and well-formed
  - Every step has action / skill / tool, and params is a mapping
  - Approval gates: every destructive or unclassifiable step has a
    ``require_approval`` step somewhere before it. This is an ERROR, not a
    warning — ``create_workflow_from_template`` refuses such a file, and so does this script.
  - Skill / tool names the skill catalog does not list (warning only — the
    catalog is a curated subset, not a whitelist)

The classification is not kept here. It is vmware-pilot's own
(``vmware_pilot.approval_gate`` over ``vmware_pilot.review``), run by building
the workflow exactly as ``create_workflow_from_template`` does, so this script cannot pass a
file that pilot will refuse. It therefore needs vmware-pilot importable:

    # with vmware-pilot installed via `uv tool install vmware-pilot`
    "$(uv tool dir)/vmware-pilot/bin/python" validate_workflow.py <file.yaml>
    # or, resolving the package on the fly
    uvx --from 'vmware-pilot>=1.9.0' python validate_workflow.py <file.yaml>

Usage:
    validate_workflow.py <workflow.yaml> [workflow2.yaml ...]
"""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Any

_NOT_IMPORTABLE = (
    "vmware-pilot is not importable from this Python ({exe}). The approval-gate "
    "check is pilot's own code, so this script runs it rather than a copy. Run it "
    "with the interpreter pilot is installed in, e.g.\n"
    "  \"$(uv tool dir)/vmware-pilot/bin/python\" {script} <file.yaml>\n"
    "  uvx --from 'vmware-pilot>=1.9.0' python {script} <file.yaml>"
)


def _structure_errors(spec: Any) -> list[str]:
    """Shape checks that must pass before the workflow can be built at all."""
    if not isinstance(spec, dict):
        return [f"Expected a YAML mapping, got {type(spec).__name__}"]
    errors = []
    if "name" not in spec:
        errors.append("Missing required field: 'name'")
    steps = spec.get("steps")
    if steps is None:
        return errors + ["Missing required field: 'steps'"]
    if not isinstance(steps, list):
        return errors + [f"'steps' must be a list, got {type(steps).__name__}"]
    if not steps:
        return errors + ["'steps' list is empty"]
    for i, step in enumerate(steps):
        if not isinstance(step, dict):
            errors.append(f"Step {i}: expected a mapping, got {type(step).__name__}")
            continue
        errors.extend(f"Step {i}: missing '{k}' field" for k in ("action", "skill", "tool")
                      if k not in step)
        for key in ("params", "rollback_params"):
            value = step.get(key)
            if value is not None and not isinstance(value, dict):
                errors.append(f"Step {i}: '{key}' must be a mapping, got {type(value).__name__}")
    return errors


def _current_tool_name(skill: Any, tool: Any) -> Any:
    """The 2.0 name Pilot will run ``tool`` as (unchanged on a Pilot older than 1.13.0)."""
    try:
        from vmware_pilot.renames import current_tool_name
    except ImportError:
        return tool
    return current_tool_name(skill, tool)


def _catalog_warnings(steps: list[dict[str, Any]]) -> list[str]:
    from vmware_pilot.mcp_server._catalog import SKILL_CATALOG

    warnings = []
    for i, step in enumerate(steps):
        skill, tool = step.get("skill", ""), step.get("tool", "")
        if step.get("action") == "require_approval" or skill == "pilot":
            continue
        current = _current_tool_name(skill, tool)
        if current != tool:
            warnings.append(
                f"Step {i}: '{tool}' is the pre-2.0 name of {skill}'s '{current}'; it "
                f"runs as '{current}' — rename it in the file"
            )
            tool = current
        if skill not in SKILL_CATALOG:
            warnings.append(
                f"Step {i}: skill '{skill}' is not in pilot's skill catalog "
                "(fine if it is a real companion skill; its steps are gated as unknown)"
            )
        elif tool not in SKILL_CATALOG[skill]["tools"]:
            warnings.append(
                f"Step {i}: tool '{tool}' is not in the catalog for '{skill}' "
                "(may still be valid if recently added)"
            )
    return warnings


def validate(path: Path) -> tuple[list[str], list[str]]:
    """Validate a workflow YAML file. Returns (errors, warnings)."""
    try:
        import yaml
    except ImportError:
        return (["pyyaml is not installed — run: pip install pyyaml"], [])
    try:
        import vmware_pilot
    except ImportError:
        return ([_NOT_IMPORTABLE.format(exe=sys.executable, script=Path(__file__).name)], [])
    try:
        from vmware_pilot.approval_gate import ApprovalGateError
        from vmware_pilot.custom_loader import _make_loader
    except ImportError:
        return ([
            f"vmware-pilot {vmware_pilot.__version__} predates the enforced approval-gate "
            "check this script runs. Upgrade it (uv tool upgrade vmware-pilot) and re-run."
        ], [])

    try:
        with open(path, encoding="utf-8") as f:
            spec: Any = yaml.safe_load(f)
    except Exception as exc:  # noqa: BLE001 — any parse failure is the answer
        return ([f"Failed to parse YAML: {exc}"], [])

    errors = _structure_errors(spec)
    if errors:
        return (errors, [])

    steps = spec["steps"]
    warnings = _catalog_warnings(steps)
    if len(steps) > 20:
        warnings.append(
            f"Workflow has {len(steps)} steps — consider splitting into "
            "multiple workflows (recommended max: 15)"
        )

    # Build it exactly the way create_workflow_from_template will. Placeholders stay unfilled;
    # the gate verdict does not depend on them (only params are substituted).
    try:
        _make_loader(spec, path)()
    except ApprovalGateError as exc:
        errors.append(str(exc))
    return (errors, warnings)


def main() -> int:
    if len(sys.argv) < 2:
        print("Usage: validate_workflow.py <workflow.yaml> [workflow2.yaml ...]")
        print()
        print("Validates custom workflow YAML files for vmware-pilot.")
        print("Checks structure and approval gates; ungated destructive steps are errors.")
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
