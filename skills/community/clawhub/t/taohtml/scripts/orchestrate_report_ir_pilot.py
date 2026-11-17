#!/usr/bin/env python3
"""Route and record an explicitly authorized TaoHtml Report IR pilot build."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

import check_production_authorization as production_authorization  # noqa: E402
import compile_report_ir  # noqa: E402
import report_ir_core  # noqa: E402
import validate_project_handoff  # noqa: E402


SCHEMA_VERSION = "1.0"
WORKFLOW = "report_ir_pilot"
PILOT_AUTHORIZATION_KEYS = {
    "schema_version",
    "authorization_type",
    "status",
    "scope",
    "task_id",
    "route",
    "authorization_ref",
}
PILOT_ONLY_ARGUMENTS = (
    "production_state",
    "report_ir",
    "output_dir",
    "project_theme_dir",
    "handoff",
)


class WorkflowError(RuntimeError):
    """Fail one named pilot stage without falling back to direct HTML."""

    def __init__(self, stage: str, code: str, message: str) -> None:
        super().__init__(message)
        self.stage = stage
        self.code = code


def _load_json(path: Path) -> object:
    return report_ir_core.strict_json_loads(path.read_text(encoding="utf-8"))


def _artifact_root(path: Path) -> Path:
    expanded = path.expanduser()
    if expanded.is_symlink():
        raise ValueError("artifact root must not be a symlink")
    resolved = expanded.resolve(strict=True)
    if not resolved.is_dir():
        raise ValueError("artifact root must be a directory")
    return resolved


def _relative_candidate(root: Path, value: Path, label: str) -> tuple[Path, Path]:
    candidate = value.expanduser()
    if not candidate.is_absolute():
        candidate = root / candidate
    try:
        relative = candidate.absolute().relative_to(root)
    except ValueError as exc:
        raise ValueError(f"{label} must stay inside the task artifact root") from exc
    if ".." in relative.parts:
        raise ValueError(f"{label} must not traverse outside the task artifact root")
    return candidate, relative


def _input_path(root: Path, value: Path, label: str) -> tuple[Path, str]:
    candidate, relative = _relative_candidate(root, value, label)
    cursor = root
    for part in relative.parts:
        cursor = cursor / part
        if cursor.is_symlink():
            raise ValueError(f"{label} must not use symlinks")
    resolved = candidate.resolve(strict=True)
    try:
        resolved.relative_to(root)
    except ValueError as exc:
        raise ValueError(f"{label} escapes the task artifact root") from exc
    if not resolved.is_file():
        raise ValueError(f"{label} must be a regular file")
    return resolved, relative.as_posix()


def _output_path(root: Path, value: Path, label: str) -> tuple[Path, str]:
    candidate, relative = _relative_candidate(root, value, label)
    cursor = root
    for part in relative.parts:
        cursor = cursor / part
        if cursor.exists() and cursor.is_symlink():
            raise ValueError(f"{label} must not use symlinks")
    existing_parent = candidate
    while not existing_parent.exists():
        existing_parent = existing_parent.parent
    resolved_parent = existing_parent.resolve(strict=True)
    try:
        resolved_parent.relative_to(root)
    except ValueError as exc:
        raise ValueError(f"{label} escapes the task artifact root") from exc
    return candidate, relative.as_posix()


def _write_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(f".{path.name}.tmp")
    temporary.write_text(
        json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    temporary.replace(path)


def _empty_stage(status: str = "not_executed") -> dict[str, object]:
    return {"status": status}


def _initial_status(route: str) -> dict[str, object]:
    return {
        "schema_version": SCHEMA_VERSION,
        "workflow": WORKFLOW,
        "task_id": None,
        "route": route,
        "status": "routing",
        "fallback_policy": (
            "forbidden_after_pilot_selection"
            if route == "report_ir_pilot"
            else "ordinary_direct_html_route_unchanged"
        ),
        "pilot_authorization": _empty_stage("not_provided"),
        "production_authorization": _empty_stage(),
        "report_ir_validation": _empty_stage(),
        "compiler": _empty_stage(),
        "html_qa": {
            "status": "not_executed",
            "execution_claim": "not_executed_by_orchestrator",
        },
        "project_handoff": {
            "status": "not_executed",
            "validation_execution_claim": "not_executed",
        },
        "diagnostics": [],
    }


def _short_text(value: object, label: str) -> str:
    if not isinstance(value, str) or not value.strip() or len(value) > 160:
        raise ValueError(f"{label} must be a non-empty string of at most 160 characters")
    return value.strip()


def _validate_pilot_authorization(raw: object) -> dict[str, str]:
    if not isinstance(raw, dict):
        raise ValueError("pilot authorization must be an object")
    if set(raw) != PILOT_AUTHORIZATION_KEYS:
        missing = ", ".join(sorted(PILOT_AUTHORIZATION_KEYS - set(raw))) or "none"
        extra = ", ".join(sorted(set(raw) - PILOT_AUTHORIZATION_KEYS)) or "none"
        raise ValueError(
            f"pilot authorization fields drifted; missing={missing}; extra={extra}"
        )
    expected = {
        "schema_version": SCHEMA_VERSION,
        "authorization_type": "report_ir_engineering_pilot",
        "status": "authorized",
        "scope": "project",
        "route": "report_ir_pilot",
    }
    for key, expected_value in expected.items():
        if raw[key] != expected_value:
            raise ValueError(f"pilot authorization {key} must equal {expected_value}")
    task_id = _short_text(raw["task_id"], "pilot authorization task_id")
    authorization_ref = _short_text(
        raw["authorization_ref"], "pilot authorization authorization_ref"
    )
    return {
        **{key: str(raw[key]) for key in expected},
        "task_id": task_id,
        "authorization_ref": authorization_ref,
    }


def _public_ir_validation(result: dict[str, Any]) -> dict[str, object]:
    return {
        "status": "valid" if result["compiler_ready"] else "invalid",
        "schema_valid": result["schema_valid"],
        "references_valid": result["references_valid"],
        "semantics_valid": result["semantics_valid"],
        "compiler_ready": result["compiler_ready"],
        "issues": result["issues"],
        "normalized_sha256": result.get("identity", {}).get("normalized_sha256"),
        "workflow_profile": result["workflow_profile"],
    }


def _validate_brief_binding(
    raw_ir: object,
    production_state: dict[str, Any],
) -> None:
    if not isinstance(raw_ir, dict) or not isinstance(raw_ir.get("traceability"), dict):
        raise ValueError("Report IR traceability must be present")
    traceability = raw_ir["traceability"]
    brief = production_state["design_brief"]
    if traceability.get("design_brief_confirmation") != "confirmed":
        raise ValueError("Report IR must record a confirmed design brief")
    if traceability.get("design_brief_ref") != brief["artifact_path"]:
        raise ValueError(
            "Report IR design_brief_ref must equal the current production-state brief path"
        )
    if traceability.get("design_brief_sha256") != brief["artifact_sha256"]:
        raise ValueError(
            "Report IR design_brief_sha256 must equal the current confirmed brief hash"
        )
    projection = raw_ir.get("projection")
    if not isinstance(projection, dict):
        raise ValueError("Report IR projection must be present")
    selected_motion = production_state["motion_density"]["density"]
    if projection.get("motion_density") != selected_motion:
        raise ValueError(
            "Report IR motion_density must equal the current production-state decision"
        )
    if production_state["visual_route"] == "built_in":
        build_binding = raw_ir.get("build_binding")
        theme = (
            build_binding.get("theme") if isinstance(build_binding, dict) else None
        )
        selected_theme = production_state["built_in_theme"]["theme_id"]
        if (
            not isinstance(theme, dict)
            or theme.get("kind") != "built_in"
            or theme.get("ref") != selected_theme
        ):
            raise ValueError(
                "Report IR built-in theme must equal the current production-state decision"
            )


def _handoff_binding_issues(
    handoff: dict[str, Any],
    *,
    html_ref: str,
    html_sha256: str,
    normalized_ir_ref: str,
    normalized_ir_sha256: str,
    manifest_ref: str,
    manifest_sha256: str,
    compiler_version: str,
    workflow_profile: dict[str, Any],
    design_brief_sha256: str,
) -> list[str]:
    current = [
        artifact
        for artifact in handoff.get("artifacts", [])
        if isinstance(artifact, dict) and artifact.get("role") == "current"
    ]
    if len(current) != 1:
        return ["handoff must contain exactly one current artifact"]
    artifact = current[0]
    issues: list[str] = []
    if handoff.get("schema_version") != "1.1":
        issues.append("pilot handoff must use Project Handoff schema_version 1.1")
    locator = artifact.get("locator")
    if locator != {"kind": "portable_path", "value": html_ref}:
        issues.append("current handoff artifact must point to the compiled pilot HTML")
    if artifact.get("sha256") != html_sha256:
        issues.append("current handoff artifact hash must match the compiled pilot HTML")
    versions = artifact.get("versions")
    if not isinstance(versions, dict) or versions.get("compiler_version") != compiler_version:
        issues.append("current handoff compiler_version must match the pilot build manifest")
    expected_ir_ref = {
        "ref": {"kind": "portable_path", "value": normalized_ir_ref},
        "sha256": normalized_ir_sha256,
    }
    if artifact.get("report_ir_ref") != expected_ir_ref:
        issues.append(
            "current handoff report_ir_ref must bind the compiled normalized Report IR"
        )
    expected_current_build = {
        "artifact_ref": artifact.get("artifact_id"),
        "build_manifest_ref": {
            "ref": {"kind": "portable_path", "value": manifest_ref},
            "sha256": manifest_sha256,
        },
        "workflow_profile": {
            "binding_state": workflow_profile["binding_state"],
            "primary_profile_id": workflow_profile["primary_profile_id"],
            "definition_version": workflow_profile["definition_version"],
            "binding_sha256": workflow_profile["binding_sha256"],
        },
    }
    if handoff.get("current_build") != expected_current_build:
        issues.append(
            "current_build must bind the newly generated Build Manifest and Workflow Profile"
        )
    confirmations = handoff.get("confirmations")
    handoff_brief = (
        confirmations.get("design_brief")
        if isinstance(confirmations, dict)
        else None
    )
    if (
        not isinstance(handoff_brief, dict)
        or handoff_brief.get("status") != "confirmed"
        or handoff_brief.get("artifact_sha256") != design_brief_sha256
    ):
        issues.append("handoff design brief must match the pilot production state")
    return issues


def _require_pilot_arguments(args: argparse.Namespace) -> None:
    missing = [
        name.replace("_", "-")
        for name in ("production_state", "report_ir", "output_dir")
        if getattr(args, name) is None
    ]
    if missing:
        raise WorkflowError(
            "routing",
            "pilot_arguments_missing",
            "authorized pilot requires: " + ", ".join(missing),
        )


def _run_pilot(
    args: argparse.Namespace,
    root: Path,
    status: dict[str, object],
) -> None:
    _require_pilot_arguments(args)
    assert args.pilot_authorization is not None
    try:
        authorization_path, authorization_ref = _input_path(
            root, args.pilot_authorization, "pilot authorization"
        )
        authorization = _validate_pilot_authorization(_load_json(authorization_path))
    except (OSError, UnicodeError, json.JSONDecodeError, ValueError) as exc:
        status["pilot_authorization"] = {"status": "invalid"}
        raise WorkflowError(
            "pilot_authorization", "pilot_authorization_invalid", str(exc)
        ) from exc
    status["pilot_authorization"] = {
        "status": "authorized",
        "scope": authorization["scope"],
        "task_id": authorization["task_id"],
        "authorization_ref": authorization["authorization_ref"],
        "artifact_ref": authorization_ref,
        "artifact_sha256": report_ir_core.sha256_file(authorization_path),
    }
    status["task_id"] = authorization["task_id"]

    try:
        production_path, production_ref = _input_path(
            root, args.production_state, "production state"
        )
        production_state = production_authorization.load_state(production_path, root)
        production_result = production_authorization.evaluate_state(production_state)
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        raise WorkflowError(
            "production_authorization", "production_state_invalid", str(exc)
        ) from exc
    if authorization["task_id"] != production_state["task_id"]:
        raise WorkflowError(
            "pilot_authorization",
            "pilot_task_mismatch",
            "pilot authorization task_id does not match production state",
        )
    status["production_authorization"] = {
        "status": production_result["status"],
        "artifact_ref": production_ref,
        "requested_action": "formal-html",
        "allowed": "formal-html" in production_result["allowed_actions"],
        "blocking_gates": production_result["blocking_gates"],
        "design_brief_ref": production_state["design_brief"]["artifact_path"],
        "design_brief_sha256": production_state["design_brief"]["artifact_sha256"],
        "design_decisions_sha256": production_state["design_brief"][
            "design_decisions_sha256"
        ],
        "built_in_theme": production_state["built_in_theme"],
        "motion_density": production_state["motion_density"],
    }
    if "formal-html" not in production_result["allowed_actions"]:
        raise WorkflowError(
            "production_authorization",
            "formal_html_not_authorized",
            "current production state does not authorize formal-html",
        )

    try:
        report_ir_path, report_ir_ref = _input_path(root, args.report_ir, "Report IR")
        raw_ir = _load_json(report_ir_path)
        _validate_brief_binding(raw_ir, production_state)
        ir_validation = report_ir_core.validate_ir(raw_ir, root)
    except (OSError, UnicodeError, json.JSONDecodeError, ValueError, RuntimeError) as exc:
        status["report_ir_validation"] = {
            "status": "binding_or_input_invalid",
            "validation_execution_claim": "not_completed",
        }
        raise WorkflowError("report_ir_validation", "report_ir_invalid", str(exc)) from exc
    status["report_ir_validation"] = _public_ir_validation(ir_validation)
    if not ir_validation["compiler_ready"]:
        raise WorkflowError(
            "report_ir_validation",
            "report_ir_not_compiler_ready",
            "Report IR failed one or more validation layers",
        )

    try:
        output_dir, output_ref = _output_path(root, args.output_dir, "compiler output")
        project_theme_dir = None
        if args.project_theme_dir is not None:
            theme_marker, _ = _input_path(
                root,
                args.project_theme_dir / "theme.json",
                "project theme manifest",
            )
            project_theme_dir = theme_marker.parent
        manifest = compile_report_ir.compile_ir(
            raw_ir,
            root,
            output_dir,
            report_ir_ref=report_ir_ref,
            project_theme_dir=project_theme_dir,
        )
    except (OSError, ValueError, RuntimeError, json.JSONDecodeError) as exc:
        status["compiler"] = {
            "status": "failed",
            "compiler_invocation": "local_compile_report_ir.compile_ir",
            "qa_execution_claim": "not_executed_by_orchestrator",
        }
        raise WorkflowError("compiler", "compiler_failed", str(exc)) from exc
    html_ref = f"{output_ref}/index.html"
    normalized_ir_ref = f"{output_ref}/report.ir.normalized.json"
    manifest_ref = f"{output_ref}/build-manifest.json"
    manifest_sha256 = report_ir_core.sha256_file(output_dir / "build-manifest.json")
    status["compiler"] = {
        "status": "compiled",
        "compiler_invocation": "local_compile_report_ir.compile_ir",
        "compiler_version": manifest["compiler_version"],
        "manifest_ref": manifest_ref,
        "manifest_sha256": manifest_sha256,
        "html_ref": html_ref,
        "html_sha256": manifest["outputs"]["html"]["sha256"],
        "normalized_ir_ref": normalized_ir_ref,
        "normalized_ir_sha256": manifest["outputs"]["normalized_ir"]["sha256"],
        "workflow_profile": manifest["workflow_profile"],
        "qa_execution_claim": manifest["qa_execution_claim"],
    }

    if args.handoff is None:
        status["status"] = "compiled_pending_qa_handoff"
        return

    try:
        handoff_path, handoff_ref = _input_path(root, args.handoff, "project handoff")
        handoff_bytes = handoff_path.read_bytes()
        raw_handoff = validate_project_handoff._strict_json_loads(  # noqa: SLF001
            handoff_bytes.decode("utf-8")
        )
        result = validate_project_handoff.evaluate_handoff(
            raw_handoff, root, handoff_bytes=handoff_bytes
        )
    except (OSError, UnicodeError, json.JSONDecodeError, ValueError, RuntimeError) as exc:
        status["project_handoff"] = {
            "status": "invalid",
            "validation_execution_claim": "attempted_by_project_handoff_validator",
            "qa_execution_claim": "not_executed_by_validator",
        }
        raise WorkflowError("project_handoff", "project_handoff_invalid", str(exc)) from exc
    status["project_handoff"] = {
        "status": result["status"],
        "artifact_ref": handoff_ref,
        "artifact_sha256": report_ir_core.sha256_file(handoff_path),
        "readiness": result["readiness"],
        "blocking_reasons": result["blocking_reasons"],
        "qa_execution_claim": result["qa_execution_claim"],
        "validation_execution_claim": "executed_by_project_handoff_validator",
    }
    if not result["readiness"]["bindings_valid"]:
        raise WorkflowError(
            "project_handoff",
            "project_handoff_bindings_invalid",
            "project handoff bindings are invalid",
        )
    assert isinstance(raw_handoff, dict)
    binding_issues = _handoff_binding_issues(
        raw_handoff,
        html_ref=html_ref,
        html_sha256=manifest["outputs"]["html"]["sha256"],
        normalized_ir_ref=normalized_ir_ref,
        normalized_ir_sha256=manifest["outputs"]["normalized_ir"]["sha256"],
        manifest_ref=manifest_ref,
        manifest_sha256=manifest_sha256,
        compiler_version=manifest["compiler_version"],
        workflow_profile=manifest["workflow_profile"],
        design_brief_sha256=production_state["design_brief"]["artifact_sha256"],
    )
    if binding_issues:
        status["project_handoff"]["pilot_binding_issues"] = binding_issues
        raise WorkflowError(
            "project_handoff",
            "pilot_handoff_binding_invalid",
            "; ".join(binding_issues),
        )
    status["project_handoff"]["pilot_build_binding_valid"] = True
    if result["readiness"]["delivery_ready"]:
        status["html_qa"] = {
            "status": "passed_records_bound_in_handoff",
            "execution_claim": "not_executed_by_orchestrator",
            "handoff_validator_claim": result["qa_execution_claim"],
        }
        status["status"] = "delivery_ready_recorded"
    else:
        status["html_qa"] = {
            "status": "not_delivery_ready_in_handoff",
            "execution_claim": "not_executed_by_orchestrator",
            "handoff_validator_claim": result["qa_execution_claim"],
        }
        status["status"] = "compiled_handoff_not_delivery_ready"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--artifact-root", type=Path, required=True)
    parser.add_argument("--status-output", type=Path, required=True)
    parser.add_argument("--pilot-authorization", type=Path)
    parser.add_argument("--production-state", type=Path)
    parser.add_argument("--report-ir", type=Path)
    parser.add_argument("--output-dir", type=Path)
    parser.add_argument("--project-theme-dir", type=Path)
    parser.add_argument("--handoff", type=Path)
    args = parser.parse_args()

    try:
        root = _artifact_root(args.artifact_root)
        status_output, _ = _output_path(root, args.status_output, "status output")
    except (OSError, ValueError) as exc:
        print(f"REPORT_IR_PILOT_INVALID {exc}")
        return 2

    pilot_selected = args.pilot_authorization is not None
    status = _initial_status("report_ir_pilot" if pilot_selected else "direct_html")
    try:
        if not pilot_selected:
            supplied = [
                name.replace("_", "-")
                for name in PILOT_ONLY_ARGUMENTS
                if getattr(args, name) is not None
            ]
            if supplied:
                raise WorkflowError(
                    "routing",
                    "pilot_authorization_required",
                    "Report IR arguments require explicit project Report IR authorization: "
                    + ", ".join(supplied),
                )
            status["status"] = "direct_html_unchanged"
        else:
            _run_pilot(args, root, status)
    except WorkflowError as exc:
        status["status"] = "blocked"
        status["diagnostics"].append(
            {"stage": exc.stage, "code": exc.code, "message": str(exc)}
        )
        _write_json(status_output, status)
        print(f"REPORT_IR_PILOT_BLOCKED stage={exc.stage} code={exc.code}")
        return 1

    _write_json(status_output, status)
    print(f"REPORT_IR_PILOT_RECORDED route={status['route']} status={status['status']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
