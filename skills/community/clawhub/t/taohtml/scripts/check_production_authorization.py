#!/usr/bin/env python3
"""Validate TaoHtml confirmation state before previews or formal HTML production."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path
from typing import Any

SCRIPT_ROOT = Path(__file__).resolve().parent
if str(SCRIPT_ROOT) not in sys.path:
    sys.path.insert(0, str(SCRIPT_ROOT))

SCHEMA_VERSION = "1.3"
LEGACY_SCHEMA_VERSIONS = {"1.1", "1.2"}
ROUTES = {"idea_only", "word_pdf", "existing_ppt_html"}
VISUAL_ROUTES = {"unresolved", "built_in", "static_reference", "profile_reuse"}
BUILT_IN_THEME_IDS = {
    "black-white-fluorescent-cards",
    "rigorous-consulting-report",
    "corporate-annual-report",
    "editorial-collage",
    "deep-data-dashboard",
    "warm-brand-narrative",
    "minimal-product-whitespace",
    "formal-government-bluewhite",
}
MOTION_DENSITIES = {"minimal", "moderate", "rich"}
DECIDED_SELECTION_STATUSES = {"user_selected", "delegated_to_taohtml"}
ACTIONS = {
    "status",
    "material-summary-preview",
    "visual-route-decision",
    "reference-vi-preview",
    "project-theme-compile",
    "profile-use-bind",
    "built-in-theme-selection",
    "motion-density-selection",
    "design-brief-preview",
    "formal-html",
    "browser-qa",
    "deliver-formal-html",
}
TOP_LEVEL_KEYS = {
    "schema_version",
    "task_id",
    "route",
    "visual_route",
    "material_summary",
    "reference_vi",
    "profile_use",
    "project_theme_compiled",
    "built_in_theme",
    "motion_density",
    "design_brief",
}
V1_2_TOP_LEVEL_KEYS = TOP_LEVEL_KEYS - {
    "built_in_theme",
    "motion_density",
}
V1_1_TOP_LEVEL_KEYS = V1_2_TOP_LEVEL_KEYS - {"profile_use"}
GATE_KEYS = {
    "status",
    "artifact_path",
    "artifact_sha256",
    "confirmation_ref",
}
DESIGN_BRIEF_KEYS = GATE_KEYS | {"design_decisions_sha256"}
SHA256 = re.compile(r"^[0-9a-f]{64}$")
PROFILE_USE_KEYS = {"status", "artifact_path", "artifact_sha256"}
BUILT_IN_THEME_KEYS = {"theme_id", "selection_status", "decision_ref"}
MOTION_DENSITY_KEYS = {"density", "selection_status", "decision_ref"}


def _exact_object(raw: object, keys: set[str], label: str) -> dict[str, Any]:
    if not isinstance(raw, dict):
        raise ValueError(f"{label} must be an object")
    actual = set(raw)
    if actual != keys:
        missing = ", ".join(sorted(keys - actual)) or "none"
        extra = ", ".join(sorted(actual - keys)) or "none"
        raise ValueError(f"{label} fields drifted; missing={missing}; extra={extra}")
    return raw


def _short_text(value: object, label: str) -> str:
    if not isinstance(value, str) or not value.strip() or len(value) > 160:
        raise ValueError(f"{label} must be a non-empty string of at most 160 characters")
    return value.strip()


def _optional_text(value: object, label: str) -> str | None:
    if value is None:
        return None
    return _short_text(value, label)


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _current_artifact(
    artifact_root: Path,
    value: object,
    expected_sha256: object,
    label: str,
) -> tuple[str, str]:
    relative_text = _short_text(value, f"{label}.artifact_path")
    relative = Path(relative_text)
    if relative.is_absolute() or ".." in relative.parts:
        raise ValueError(
            f"{label}.artifact_path must be a safe task-local relative path"
        )
    if not isinstance(expected_sha256, str) or not SHA256.fullmatch(expected_sha256):
        raise ValueError(
            f"{label}.artifact_sha256 must be a lowercase SHA-256 digest"
        )
    supplied = artifact_root / relative
    cursor = artifact_root
    for part in relative.parts:
        cursor = cursor / part
        if cursor.is_symlink():
            raise ValueError(f"{label}.artifact_path must not use symlinks")
    try:
        current = supplied.resolve(strict=True)
    except FileNotFoundError as exc:
        raise ValueError(f"{label}.artifact_path does not exist: {relative_text}") from exc
    try:
        current.relative_to(artifact_root)
    except ValueError as exc:
        raise ValueError(
            f"{label}.artifact_path escapes the task artifact root: {relative_text}"
        ) from exc
    if not current.is_file():
        raise ValueError(f"{label}.artifact_path is not a file: {relative_text}")
    current_sha256 = _sha256(current)
    if current_sha256 != expected_sha256:
        raise ValueError(
            f"{label}.artifact_sha256 does not match the current file"
        )
    return relative.as_posix(), current_sha256


def _profile_use_gate(
    raw: object,
    artifact_root: Path,
) -> dict[str, Any]:
    gate = _exact_object(raw, PROFILE_USE_KEYS, "profile_use")
    status = gate["status"]
    if status not in {"not_required", "pending", "bound"}:
        raise ValueError("profile_use.status must be not_required, pending, or bound")
    artifact_path = _optional_text(gate["artifact_path"], "profile_use.artifact_path")
    artifact_sha256 = _optional_text(
        gate["artifact_sha256"], "profile_use.artifact_sha256"
    )
    validation_status = None
    temporary_override = None
    if status == "bound":
        import profile_store

        if artifact_path is None or artifact_sha256 is None:
            raise ValueError(
                "profile_use bound state requires artifact_path and artifact_sha256"
            )
        artifact_path, artifact_sha256 = _current_artifact(
            artifact_root,
            artifact_path,
            artifact_sha256,
            "profile_use",
        )
        current = artifact_root / artifact_path
        validated = profile_store.validate_binding(current)
        validation_status = validated["status"]
        temporary_override = bool(validated["binding"]["temporary_override"])
    elif status == "pending":
        if artifact_sha256 is not None:
            raise ValueError("profile_use pending state cannot contain artifact_sha256")
    elif artifact_path is not None or artifact_sha256 is not None:
        raise ValueError("profile_use not_required state cannot bind an artifact")
    return {
        "status": status,
        "artifact_path": artifact_path,
        "artifact_sha256": artifact_sha256,
        "validation_status": validation_status,
        "temporary_override": temporary_override,
    }


def _confirmation_gate(
    raw: object,
    label: str,
    artifact_root: Path,
    *,
    allowed_statuses: set[str],
) -> dict[str, str | None]:
    gate = _exact_object(raw, GATE_KEYS, label)
    status = gate["status"]
    if status not in allowed_statuses:
        raise ValueError(
            f"{label}.status must be one of: {', '.join(sorted(allowed_statuses))}"
        )
    artifact_path = _optional_text(gate["artifact_path"], f"{label}.artifact_path")
    artifact_sha256 = _optional_text(
        gate["artifact_sha256"], f"{label}.artifact_sha256"
    )
    confirmation_ref = _optional_text(
        gate["confirmation_ref"], f"{label}.confirmation_ref"
    )
    if status == "confirmed":
        if artifact_path is None or artifact_sha256 is None or confirmation_ref is None:
            raise ValueError(
                f"{label} confirmed state requires artifact_path, artifact_sha256, and confirmation_ref"
            )
        artifact_path, artifact_sha256 = _current_artifact(
            artifact_root,
            artifact_path,
            artifact_sha256,
            label,
        )
    elif status == "pending":
        if artifact_sha256 is not None or confirmation_ref is not None:
            raise ValueError(
                f"{label} pending state cannot contain artifact_sha256 or confirmation_ref"
            )
    elif (
        artifact_path is not None
        or artifact_sha256 is not None
        or confirmation_ref is not None
    ):
        raise ValueError(f"{label} not_required state cannot bind an artifact or confirmation")
    return {
        "status": status,
        "artifact_path": artifact_path,
        "artifact_sha256": artifact_sha256,
        "confirmation_ref": confirmation_ref,
    }


def _design_brief_gate(
    raw: object,
    artifact_root: Path,
) -> dict[str, str | None]:
    gate = _exact_object(raw, DESIGN_BRIEF_KEYS, "design_brief")
    confirmed_artifact = _confirmation_gate(
        {key: gate[key] for key in GATE_KEYS},
        "design_brief",
        artifact_root,
        allowed_statuses={"pending", "confirmed"},
    )
    decisions_sha256 = _optional_text(
        gate["design_decisions_sha256"],
        "design_brief.design_decisions_sha256",
    )
    if decisions_sha256 is not None and not SHA256.fullmatch(decisions_sha256):
        raise ValueError(
            "design_brief.design_decisions_sha256 must be a lowercase SHA-256 digest"
        )
    if confirmed_artifact["status"] == "confirmed":
        if decisions_sha256 is None:
            raise ValueError(
                "design_brief confirmed state requires design_decisions_sha256"
            )
    elif decisions_sha256 is not None:
        raise ValueError(
            "design_brief pending state cannot contain design_decisions_sha256"
        )
    return {
        **confirmed_artifact,
        "design_decisions_sha256": decisions_sha256,
    }


def _selection_decision(
    raw: object,
    *,
    label: str,
    keys: set[str],
    value_key: str,
    allowed_values: set[str],
    allow_not_required: bool,
) -> dict[str, str | None]:
    decision = _exact_object(raw, keys, label)
    selection_status = decision["selection_status"]
    allowed_statuses = {"pending", *DECIDED_SELECTION_STATUSES}
    if allow_not_required:
        allowed_statuses.add("not_required")
    if selection_status not in allowed_statuses:
        raise ValueError(
            f"{label}.selection_status must be one of: "
            + ", ".join(sorted(allowed_statuses))
        )
    value = _optional_text(decision[value_key], f"{label}.{value_key}")
    decision_ref = _optional_text(decision["decision_ref"], f"{label}.decision_ref")
    if selection_status in DECIDED_SELECTION_STATUSES:
        if value is None or decision_ref is None:
            raise ValueError(
                f"{label} {selection_status} requires {value_key} and decision_ref"
            )
        if value not in allowed_values:
            raise ValueError(
                f"{label}.{value_key} must be one of: "
                + ", ".join(sorted(allowed_values))
            )
    elif value is not None or decision_ref is not None:
        raise ValueError(
            f"{label} {selection_status} state cannot contain {value_key} or decision_ref"
        )
    return {
        value_key: value,
        "selection_status": selection_status,
        "decision_ref": decision_ref,
    }


def _legacy_pending_decisions(
    visual_route: str,
) -> tuple[dict[str, None | str], dict[str, None | str]]:
    built_in_status = "pending" if visual_route == "built_in" else "not_required"
    return (
        {
            "theme_id": None,
            "selection_status": built_in_status,
            "decision_ref": None,
        },
        {
            "density": None,
            "selection_status": "pending",
            "decision_ref": None,
        },
    )


def design_decisions_sha256(
    built_in_theme: dict[str, str | None],
    motion_density: dict[str, str | None],
) -> str:
    """Return the canonical digest bound by a confirmed Report Design Brief."""
    snapshot = {
        "built_in_theme": {
            key: built_in_theme[key] for key in sorted(BUILT_IN_THEME_KEYS)
        },
        "motion_density": {
            key: motion_density[key] for key in sorted(MOTION_DENSITY_KEYS)
        },
    }
    canonical = json.dumps(
        snapshot,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
    return hashlib.sha256(canonical).hexdigest()


def validate_state(raw: object, artifact_root: Path) -> dict[str, Any]:
    try:
        resolved_artifact_root = artifact_root.expanduser().resolve(strict=True)
    except FileNotFoundError as exc:
        raise ValueError(f"artifact_root does not exist: {artifact_root}") from exc
    if not resolved_artifact_root.is_dir():
        raise ValueError(f"artifact_root is not a directory: {resolved_artifact_root}")
    if not isinstance(raw, dict):
        raise ValueError("state must be an object")
    source_schema_version = raw.get("schema_version")
    legacy_migration_required = source_schema_version in LEGACY_SCHEMA_VERSIONS
    if source_schema_version == "1.1":
        state = dict(_exact_object(raw, V1_1_TOP_LEVEL_KEYS, "state"))
        state["profile_use"] = {
            "status": "not_required",
            "artifact_path": None,
            "artifact_sha256": None,
        }
    elif source_schema_version == "1.2":
        state = dict(_exact_object(raw, V1_2_TOP_LEVEL_KEYS, "state"))
    else:
        state = _exact_object(raw, TOP_LEVEL_KEYS, "state")
        if source_schema_version != SCHEMA_VERSION:
            raise ValueError(
                f"schema_version must be {SCHEMA_VERSION} "
                f"(or legacy {', '.join(sorted(LEGACY_SCHEMA_VERSIONS))})"
            )
    if legacy_migration_required:
        built_in_theme, motion_density = _legacy_pending_decisions(
            str(state["visual_route"])
        )
        state = {
            **state,
            "schema_version": SCHEMA_VERSION,
            "built_in_theme": built_in_theme,
            "motion_density": motion_density,
        }
        legacy_brief = state["design_brief"]
        if isinstance(legacy_brief, dict) and legacy_brief.get("status") == "confirmed":
            state["design_brief"] = {
                "status": "pending",
                "artifact_path": legacy_brief.get("artifact_path"),
                "artifact_sha256": None,
                "confirmation_ref": None,
                "design_decisions_sha256": None,
            }
        elif isinstance(legacy_brief, dict):
            state["design_brief"] = {
                **legacy_brief,
                "design_decisions_sha256": None,
            }
    task_id = _short_text(state["task_id"], "task_id")
    route = state["route"]
    if route not in ROUTES:
        raise ValueError(f"route must be one of: {', '.join(sorted(ROUTES))}")
    visual_route = state["visual_route"]
    if visual_route not in VISUAL_ROUTES:
        raise ValueError(
            f"visual_route must be one of: {', '.join(sorted(VISUAL_ROUTES))}"
        )
    material = _confirmation_gate(
        state["material_summary"],
        "material_summary",
        resolved_artifact_root,
        allowed_statuses={"not_required", "pending", "confirmed"},
    )
    reference_vi = _confirmation_gate(
        state["reference_vi"],
        "reference_vi",
        resolved_artifact_root,
        allowed_statuses={"not_required", "pending", "confirmed"},
    )
    brief = _design_brief_gate(
        state["design_brief"],
        resolved_artifact_root,
    )
    profile_use = _profile_use_gate(state["profile_use"], resolved_artifact_root)
    built_in_theme = _selection_decision(
        state["built_in_theme"],
        label="built_in_theme",
        keys=BUILT_IN_THEME_KEYS,
        value_key="theme_id",
        allowed_values=BUILT_IN_THEME_IDS,
        allow_not_required=True,
    )
    motion_density = _selection_decision(
        state["motion_density"],
        label="motion_density",
        keys=MOTION_DENSITY_KEYS,
        value_key="density",
        allowed_values=MOTION_DENSITIES,
        allow_not_required=False,
    )
    project_theme_compiled = state["project_theme_compiled"]
    if not isinstance(project_theme_compiled, bool):
        raise ValueError("project_theme_compiled must be a boolean")

    source_backed_route = route in {"word_pdf", "existing_ppt_html"}
    if source_backed_route:
        if material["status"] == "not_required":
            raise ValueError(
                f"{route} requires a pending or confirmed material summary"
            )
    elif material["status"] != "not_required":
        raise ValueError(f"{route} requires material_summary.status=not_required")

    if visual_route == "static_reference":
        if reference_vi["status"] == "not_required":
            raise ValueError(
                "static_reference requires a pending or confirmed reference VI"
            )
    else:
        if reference_vi["status"] != "not_required":
            raise ValueError(
                f"{visual_route} requires reference_vi.status=not_required"
            )
        if project_theme_compiled and visual_route not in {"profile_reuse"}:
            raise ValueError(
                "project_theme_compiled can be true only for static_reference or profile_reuse"
            )

    if visual_route == "profile_reuse":
        if profile_use["status"] == "bound" and profile_use["temporary_override"]:
            raise ValueError("profile_reuse cannot use a temporary-override binding")
    elif profile_use["status"] == "pending":
        raise ValueError("profile_use pending state is valid only for profile_reuse")
    elif profile_use["status"] == "bound" and not profile_use["temporary_override"]:
        raise ValueError(
            "A reusable profile binding requires visual_route=profile_reuse"
        )

    if visual_route == "built_in":
        if built_in_theme["selection_status"] == "not_required":
            raise ValueError("built_in visual route requires a built-in theme decision")
    elif built_in_theme["selection_status"] != "not_required":
        raise ValueError(
            f"{visual_route} requires built_in_theme.selection_status=not_required"
        )

    source_ready = not source_backed_route or material["status"] == "confirmed"
    vi_ready = (
        visual_route != "static_reference"
        or reference_vi["status"] == "confirmed"
    )
    profile_ready = (
        visual_route != "profile_reuse"
        or (
            profile_use["status"] == "bound"
            and profile_use["validation_status"] == "valid_reuse"
        )
    )
    built_in_theme_ready = (
        visual_route != "built_in"
        or built_in_theme["selection_status"] in DECIDED_SELECTION_STATUSES
    )
    motion_density_ready = (
        motion_density["selection_status"] in DECIDED_SELECTION_STATUSES
    )
    if reference_vi["status"] == "confirmed" and not source_ready:
        raise ValueError("reference VI cannot be confirmed before source grounding")
    if project_theme_compiled and not (vi_ready and profile_ready):
        raise ValueError("project theme cannot be compiled before reference VI confirmation")
    upstream_ready = (
        source_ready
        and visual_route != "unresolved"
        and vi_ready
        and profile_ready
        and built_in_theme_ready
        and motion_density_ready
        and (
            visual_route not in {"static_reference", "profile_reuse"}
            or project_theme_compiled
        )
    )
    if brief["status"] == "confirmed" and not upstream_ready:
        raise ValueError(
            "design brief cannot be confirmed before all applicable upstream gates"
        )
    current_design_decisions_sha256 = design_decisions_sha256(
        built_in_theme,
        motion_density,
    )
    if (
        brief["status"] == "confirmed"
        and brief["design_decisions_sha256"] != current_design_decisions_sha256
    ):
        raise ValueError(
            "design_brief.design_decisions_sha256 does not match the current "
            "built-in theme and motion decisions; update and reconfirm the brief"
        )

    return {
        "schema_version": SCHEMA_VERSION,
        "task_id": task_id,
        "route": route,
        "visual_route": visual_route,
        "material_summary": material,
        "reference_vi": reference_vi,
        "profile_use": profile_use,
        "project_theme_compiled": project_theme_compiled,
        "built_in_theme": built_in_theme,
        "motion_density": motion_density,
        "design_brief": brief,
        "current_design_decisions_sha256": current_design_decisions_sha256,
        "migration": {
            "source_schema_version": source_schema_version,
            "required": legacy_migration_required,
            "brief_reconfirmation_required": legacy_migration_required,
        },
        "artifact_root": str(resolved_artifact_root),
    }


def evaluate_state(state: dict[str, Any]) -> dict[str, object]:
    source_backed_route = state["route"] in {"word_pdf", "existing_ppt_html"}
    material_ready = (
        not source_backed_route
        or state["material_summary"]["status"] == "confirmed"
    )
    visual_ready = state["visual_route"] != "unresolved"
    vi_ready = (
        state["visual_route"] != "static_reference"
        or state["reference_vi"]["status"] == "confirmed"
    )
    profile_ready = (
        state["visual_route"] != "profile_reuse"
        or (
            state["profile_use"]["status"] == "bound"
            and state["profile_use"]["validation_status"] == "valid_reuse"
        )
    )
    project_theme_ready = (
        state["visual_route"] not in {"static_reference", "profile_reuse"}
        or state["project_theme_compiled"]
    )
    built_in_theme_ready = (
        state["visual_route"] != "built_in"
        or state["built_in_theme"]["selection_status"]
        in DECIDED_SELECTION_STATUSES
    )
    motion_density_ready = (
        state["motion_density"]["selection_status"]
        in DECIDED_SELECTION_STATUSES
    )
    brief_ready = state["design_brief"]["status"] == "confirmed"

    blocking_gates: list[str] = []
    if not material_ready:
        blocking_gates.append("material_summary_confirmation")
    if not visual_ready:
        blocking_gates.append("visual_route_selection")
    if visual_ready and not vi_ready:
        blocking_gates.append("reference_vi_confirmation")
    if visual_ready and vi_ready and not profile_ready:
        blocking_gates.append("profile_use_binding")
    if visual_ready and vi_ready and profile_ready and not project_theme_ready:
        blocking_gates.append("project_theme_compilation")
    if visual_ready and vi_ready and profile_ready and project_theme_ready:
        if not built_in_theme_ready:
            blocking_gates.append("built_in_theme_selection")
        if not motion_density_ready:
            blocking_gates.append("motion_density_selection")
    if (
        material_ready
        and visual_ready
        and vi_ready
        and profile_ready
        and project_theme_ready
        and built_in_theme_ready
        and motion_density_ready
        and not brief_ready
    ):
        blocking_gates.append("design_brief_confirmation")

    allowed = {"status"}
    if not material_ready:
        allowed.add("material-summary-preview")
    else:
        if not visual_ready:
            allowed.add("visual-route-decision")
        elif not vi_ready:
            allowed.add("reference-vi-preview")
        elif not profile_ready:
            allowed.add("profile-use-bind")
        elif not project_theme_ready:
            allowed.add("project-theme-compile")
        elif not (built_in_theme_ready and motion_density_ready):
            if not built_in_theme_ready:
                allowed.add("built-in-theme-selection")
            if not motion_density_ready:
                allowed.add("motion-density-selection")
        elif not brief_ready:
            allowed.add("design-brief-preview")
        else:
            allowed.update({"formal-html", "browser-qa", "deliver-formal-html"})

    authorized = not blocking_gates and brief_ready
    verified_artifacts = [
        {
            "gate": name,
            "artifact_path": state[name]["artifact_path"],
            "artifact_sha256": state[name]["artifact_sha256"],
        }
        for name in ("material_summary", "reference_vi", "design_brief")
        if state[name]["status"] == "confirmed"
    ]
    if state["profile_use"]["status"] == "bound":
        verified_artifacts.append(
            {
                "gate": "profile_use",
                "artifact_path": state["profile_use"]["artifact_path"],
                "artifact_sha256": state["profile_use"]["artifact_sha256"],
            }
        )
    verified_decisions = [
        {
            "gate": "built_in_theme",
            "value": state["built_in_theme"]["theme_id"],
            "selection_status": state["built_in_theme"]["selection_status"],
            "decision_ref": state["built_in_theme"]["decision_ref"],
        },
        {
            "gate": "motion_density",
            "value": state["motion_density"]["density"],
            "selection_status": state["motion_density"]["selection_status"],
            "decision_ref": state["motion_density"]["decision_ref"],
        },
    ]
    return {
        "schema_version": SCHEMA_VERSION,
        "task_id": state["task_id"],
        "status": "authorized" if authorized else "blocked",
        "authorized_for_formal_html": authorized,
        "blocking_gates": blocking_gates,
        "allowed_actions": sorted(allowed),
        "verified_artifacts": verified_artifacts,
        "verified_design_decisions": verified_decisions,
        "current_design_decisions_sha256": state[
            "current_design_decisions_sha256"
        ],
        "migration": state["migration"],
        "forbidden_formal_actions": (
            [] if authorized else ["formal-html", "browser-qa", "deliver-formal-html"]
        ),
    }


def load_state(path: Path, artifact_root: Path) -> dict[str, Any]:
    return validate_state(json.loads(path.read_text(encoding="utf-8")), artifact_root)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Check TaoHtml confirmation state before a requested action."
    )
    parser.add_argument("--state", type=Path, required=True)
    parser.add_argument(
        "--artifact-root",
        type=Path,
        required=True,
        help="Task-local root containing every bound gate artifact.",
    )
    parser.add_argument("--action", choices=sorted(ACTIONS), default="status")
    args = parser.parse_args()
    try:
        result = evaluate_state(
            load_state(args.state.resolve(), args.artifact_root)
        )
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        print(
            json.dumps(
                {
                    "schema_version": SCHEMA_VERSION,
                    "status": "invalid",
                    "error": f"{type(exc).__name__}: {exc}",
                },
                ensure_ascii=False,
                indent=2,
            )
        )
        return 2
    allowed = args.action in result["allowed_actions"]
    result["requested_action"] = {"name": args.action, "allowed": allowed}
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if allowed else 1


if __name__ == "__main__":
    raise SystemExit(main())
