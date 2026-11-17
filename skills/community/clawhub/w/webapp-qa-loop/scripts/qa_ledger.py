#!/usr/bin/env python3
"""Durable schema-v2 ledger for browser-centered web application QA.

This helper records caller-supplied facts only. It never executes project
commands, opens evidence, controls a browser, performs deployment, or grants
authorization.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
import time
import uuid
from collections import Counter
from contextlib import contextmanager
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable, Iterable


SCHEMA_VERSION = 2
LEDGER_NAME = "qa-ledger.json"
LOCK_NAME = ".qa-ledger.lock"

MODES = ("audit", "repair", "release")
DEPTHS = ("targeted", "smoke", "release-regression")
STATES = (
    "INTAKE", "DISCOVER", "BASELINE", "EXPLORE", "TRIAGE", "REPAIR",
    "LOCAL_VERIFY", "RELEASE_GATE", "DEPLOY", "REMOTE_VERIFY", "REPORT", "DELIVER",
)
SETTLEMENTS = ("active", "succeeded", "failed", "blocked")
SEVERITIES = ("P0", "P1", "P2", "P3")
ISSUE_STATUSES = ("open", "investigating", "fixed", "verified", "blocked", "wont-fix")
ISSUE_KINDS = (
    "functional", "interaction", "ui", "accessibility", "performance",
    "security", "data", "compatibility", "other",
)
APPROACHES = ("reuse", "configure", "extend", "extract", "new")
EVIDENCE_KINDS = ("before", "reproduction", "diagnosis", "repair", "after", "blocker", "release")
RISK_CLASSES = ("A", "B", "C")
REGRESSION_LEVELS = ("R0", "R1", "R2", "R3", "R4")
CHECK_KINDS = ("test", "lint", "typecheck", "build", "health", "deploy", "browser", "other")
CHECK_PHASES = ("baseline", "post-fix", "pre-deploy", "post-deploy")
COVERAGE_PHASES = ("baseline", "post-fix", "post-deploy")
RESULTS = ("pass", "fail", "blocked", "skipped")
ROLLBACK_READINESS = ("ready", "not-ready")
DEPLOY_RESULTS = (
    "pass", "failed-unchanged", "failed-partial", "unknown", "blocked",
)
CLEANUP_STATUSES = ("not-needed", "pending", "complete", "residual")
DECLARATION_DISPOSITIONS = ("in", "out", "baseline-debt")
DELIVERY_ACTIONS = (
    "commit", "push", "pr-create", "pr-update", "merge",
    "report-send", "report-upload", "other",
)
DELIVERY_RESULTS = ("planned", "succeeded", "failed", "blocked", "unknown")

ID_PATTERNS = {
    "target": ("TGT", re.compile(r"^TGT-(\d{3,12})$")),
    "scenario": ("SCN", re.compile(r"^SCN-(\d{3,12})$")),
    "check_plan": ("PLN", re.compile(r"^PLN-(\d{3,12})$")),
    "issue": ("QA", re.compile(r"^QA-(\d{3,12})$")),
    "check": ("CHK", re.compile(r"^CHK-(\d{3,12})$")),
    "coverage": ("COV", re.compile(r"^COV-(\d{3,12})$")),
    "attempt": ("ATT", re.compile(r"^ATT-(\d{3,12})$")),
    "delivery": ("DLV", re.compile(r"^DLV-(\d{3,12})$")),
}


class LedgerError(Exception):
    def __init__(self, message: str, exit_code: int = 3):
        super().__init__(message)
        self.exit_code = exit_code


def _text(value: str) -> str:
    value = value.strip()
    if not value:
        raise argparse.ArgumentTypeError("value must not be empty")
    return value


def _bool(value: str) -> bool:
    normalized = value.strip().lower()
    if normalized in {"true", "1", "yes", "y"}:
        return True
    if normalized in {"false", "0", "no", "n"}:
        return False
    raise argparse.ArgumentTypeError("expected true or false")


def _now(raw: str | None) -> str:
    if raw is None:
        dt = datetime.now(timezone.utc).replace(microsecond=0)
    else:
        try:
            dt = datetime.fromisoformat(raw.replace("Z", "+00:00"))
        except ValueError as exc:
            raise LedgerError(f"invalid RFC3339 timestamp: {raw}") from exc
        if dt.tzinfo is None:
            raise LedgerError("--at must include a timezone")
        dt = dt.astimezone(timezone.utc).replace(microsecond=0)
    return dt.isoformat().replace("+00:00", "Z")


def _dt(raw: str) -> datetime:
    try:
        return datetime.fromisoformat(raw.replace("Z", "+00:00"))
    except (TypeError, ValueError) as exc:
        raise LedgerError(f"invalid timestamp in ledger: {raw!r}", 5) from exc


def _run_dir(raw: str) -> Path:
    unexpanded = Path(raw)
    if not unexpanded.is_absolute():
        raise LedgerError("--run-dir must be absolute")
    candidate = unexpanded.expanduser()
    if not candidate.is_absolute():
        raise LedgerError("--run-dir must be absolute")
    if candidate.exists() and candidate.is_symlink():
        raise LedgerError("--run-dir must not be a symbolic link")
    resolved = candidate.resolve(strict=False)
    if resolved == Path(resolved.anchor):
        raise LedgerError("--run-dir must not be a filesystem root")
    return resolved


def _path(run_dir: Path) -> Path:
    return run_dir / LEDGER_NAME


@contextmanager
def _lock(run_dir: Path) -> Iterable[None]:
    if not run_dir.is_dir():
        raise LedgerError(f"run directory does not exist: {run_dir}", 4)
    lock_path = run_dir / LOCK_NAME
    deadline = time.monotonic() + 5.0
    while True:
        try:
            fd = os.open(lock_path, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
            with os.fdopen(fd, "w", encoding="utf-8") as handle:
                json.dump({"pid": os.getpid(), "created": time.time()}, handle)
            break
        except FileExistsError:
            try:
                stale = time.time() - lock_path.stat().st_mtime > 300
            except FileNotFoundError:
                continue
            if stale:
                try:
                    lock_path.unlink()
                except FileNotFoundError:
                    pass
                continue
            if time.monotonic() >= deadline:
                raise LedgerError("ledger is locked by another process", 75)
            time.sleep(0.05)
        except OSError as exc:
            raise LedgerError(f"cannot acquire ledger lock: {exc}", 5) from exc
    try:
        yield
    finally:
        try:
            lock_path.unlink()
        except FileNotFoundError:
            pass


def _read(run_dir: Path) -> dict[str, Any]:
    ledger_path = _path(run_dir)
    if not ledger_path.is_file():
        raise LedgerError(f"ledger does not exist: {ledger_path}", 4)
    try:
        with ledger_path.open("r", encoding="utf-8") as handle:
            data = json.load(handle)
    except (OSError, UnicodeError, json.JSONDecodeError, RecursionError) as exc:
        raise LedgerError(f"cannot read ledger: {exc}", 5) from exc
    if not isinstance(data, dict):
        raise LedgerError("ledger root must be an object", 5)
    return data


def _write(run_dir: Path, data: dict[str, Any]) -> None:
    target = _path(run_dir)
    temporary = run_dir / f".qa-ledger.{os.getpid()}.{uuid.uuid4().hex}.tmp"
    try:
        with temporary.open("x", encoding="utf-8", newline="\n") as handle:
            json.dump(data, handle, ensure_ascii=False, indent=2, sort_keys=True)
            handle.write("\n")
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary, target)
    except OSError as exc:
        raise LedgerError(f"cannot write ledger: {exc}", 5) from exc
    finally:
        try:
            temporary.unlink()
        except FileNotFoundError:
            pass


def _event(data: dict[str, Any], at: str, action: str, ref: str, detail: str) -> None:
    previous = data["run"]["updated_at"]
    if _dt(at) < _dt(previous):
        raise LedgerError(f"--at {at} precedes ledger updated_at {previous}")
    data["run"]["updated_at"] = at
    data["events"].append({"at": at, "action": action, "ref": ref, "detail": detail})


def _mutate(run_dir: Path, at: str, operation: Callable[[dict[str, Any]], str]) -> str:
    with _lock(run_dir):
        data = _read(run_dir)
        errors, _ = _safe_validate(data, strict=False)
        if errors:
            raise LedgerError("existing ledger is invalid: " + "; ".join(errors), 5)
        result = operation(data)
        errors, _ = _safe_validate(data, strict=False)
        if errors:
            raise LedgerError("mutation would create an invalid ledger: " + "; ".join(errors), 5)
        _write(run_dir, data)
        return result


def _next(data: dict[str, Any], kind: str) -> str:
    prefix, _ = ID_PATTERNS[kind]
    data["counters"][kind] += 1
    return f"{prefix}-{data['counters'][kind]:03d}"


def _entity(data: dict[str, Any], collection: str, entity_id: str, label: str) -> dict[str, Any]:
    for item in data.get(collection, []):
        if isinstance(item, dict) and item.get("id") == entity_id:
            return item
    raise LedgerError(f"unknown {label} id: {entity_id}", 4)


def _target(data: dict[str, Any], entity_id: str) -> dict[str, Any]:
    return _entity(data, "targets", entity_id, "target")


def _scenario(data: dict[str, Any], entity_id: str) -> dict[str, Any]:
    return _entity(data, "scenarios", entity_id, "scenario")


def _plan(data: dict[str, Any], entity_id: str) -> dict[str, Any]:
    return _entity(data, "check_plans", entity_id, "check plan")


def _issue(data: dict[str, Any], entity_id: str) -> dict[str, Any]:
    return _entity(data, "issues", entity_id, "issue")


def _attempt(data: dict[str, Any], entity_id: str) -> dict[str, Any]:
    return _entity(data, "deployment_attempts", entity_id, "attempt")


def _issue_refs(data: dict[str, Any], refs: list[str]) -> None:
    for ref in refs:
        _issue(data, ref)


def _dedupe(values: Iterable[str]) -> list[str]:
    return list(dict.fromkeys(values))


def _empty_gate() -> dict[str, Any]:
    return {
        "status": "pending", "target_id": "", "artifact": "", "attempt_id": "",
        "passed_at": "", "check_ids": [], "coverage_ids": [],
    }


def _latest(items: list[dict[str, Any]], key: Callable[[dict[str, Any]], tuple[Any, ...]]) -> dict[tuple[Any, ...], dict[str, Any]]:
    result: dict[tuple[Any, ...], dict[str, Any]] = {}
    for item in items:
        result[key(item)] = item
    return result


def _latest_plan(data: dict[str, Any], plan_id: str, target_id: str | None = None,
                 artifact: str | None = None, attempt_id: str | None = None) -> dict[str, Any] | None:
    matches = [item for item in data["checks"] if item["plan_id"] == plan_id]
    if target_id is not None:
        matches = [item for item in matches if item["target_id"] == target_id]
    if artifact is not None:
        matches = [item for item in matches if item["artifact"] == artifact]
    if attempt_id is not None:
        matches = [item for item in matches if item["attempt_id"] == attempt_id]
    return matches[-1] if matches else None


def _latest_scenario(data: dict[str, Any], scenario_id: str, phase: str | None = None,
                     target_id: str | None = None, artifact: str | None = None,
                     attempt_id: str | None = None) -> dict[str, Any] | None:
    matches = [item for item in data["coverage"] if item["scenario_id"] == scenario_id]
    if phase is not None:
        matches = [item for item in matches if item["phase"] == phase]
    if target_id is not None:
        matches = [item for item in matches if item["target_id"] == target_id]
    if artifact is not None:
        matches = [item for item in matches if item["artifact"] == artifact]
    if attempt_id is not None:
        matches = [item for item in matches if item["attempt_id"] == attempt_id]
    return matches[-1] if matches else None


def _evidence_kinds(issue: dict[str, Any]) -> set[str]:
    return {item["kind"] for item in issue["evidence"]}


def _linked_regression_pass(data: dict[str, Any], issue_id: str, level: str,
                            binding: tuple[str, str, str] | None = None,
                            required_phase: str | None = None,
                            not_before: str | None = None) -> bool:
    target_id, artifact, attempt_id = binding if binding else (None, None, None)
    candidates: list[dict[str, Any]] = []
    for plan in data["check_plans"]:
        if plan["regression_level"] != level or plan.get("disposition") != "in":
            continue
        if required_phase and plan["phase"] != required_phase:
            continue
        linked = issue_id in plan["issues"] or any(
            item["plan_id"] == plan["id"] and issue_id in item["issues"]
            for item in data["checks"]
        )
        if not linked:
            continue
        matches = [item for item in data["checks"] if item["plan_id"] == plan["id"]]
        if target_id is not None:
            matches = [item for item in matches if item["target_id"] == target_id]
        if artifact is not None:
            matches = [item for item in matches if item["artifact"] == artifact]
        if attempt_id is not None:
            matches = [item for item in matches if item["attempt_id"] == attempt_id]
        if not_before:
            matches = [item for item in matches if _dt(item["at"]) >= _dt(not_before)]
        if not matches:
            return False
        candidates.append(matches[-1])
    for scenario in data["scenarios"]:
        if scenario["regression_level"] != level or scenario.get("disposition") != "in":
            continue
        linked = issue_id in scenario["issues"] or any(
            item["scenario_id"] == scenario["id"] and issue_id in item["issues"]
            for item in data["coverage"]
        )
        if not linked:
            continue
        matches = [
            item for item in data["coverage"]
            if item["scenario_id"] == scenario["id"]
            and (required_phase is None or item["phase"] == required_phase)
        ]
        if target_id is not None:
            matches = [item for item in matches if item["target_id"] == target_id]
        if artifact is not None:
            matches = [item for item in matches if item["artifact"] == artifact]
        if attempt_id is not None:
            matches = [item for item in matches if item["attempt_id"] == attempt_id]
        if not_before:
            matches = [item for item in matches if _dt(item["at"]) >= _dt(not_before)]
        if not matches:
            return False
        candidates.append(matches[-1])
    if not candidates:
        return False
    return all(item["result"] == "pass" and bool(item["evidence"]) for item in candidates)


def _verified_issue_errors(data: dict[str, Any], issue: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    for field in ("root_cause", "resolution", "approach"):
        if not issue.get(field):
            errors.append(f"{issue['id']} verified requires {field}")
    fixed_at = issue.get("fixed_at", "")
    if not fixed_at:
        errors.append(f"{issue['id']} verified requires fixed_at")
    kinds = _evidence_kinds(issue)
    if "before" not in kinds:
        errors.append(f"{issue['id']} verified requires before evidence")
    for kind in ("repair", "after"):
        if not any(
            item["kind"] == kind and item.get("cycle") == issue.get("repair_cycle")
            for item in issue["evidence"]
        ):
            errors.append(f"{issue['id']} verified requires {kind} evidence from the current repair cycle")
    if fixed_at and not any(
        item["kind"] == "after" and item.get("cycle") == issue.get("repair_cycle")
        and _dt(item["at"]) >= _dt(fixed_at)
        for item in issue["evidence"]
    ):
        errors.append(f"{issue['id']} requires after evidence recorded after it was fixed")
    for level in ("R0", "R1"):
        if not _linked_regression_pass(
            data, issue["id"], level, required_phase="post-fix", not_before=fixed_at or None,
        ):
            errors.append(f"{issue['id']} verified requires a linked passing post-fix {level} result")
    return errors


def _transition_allowed(data: dict[str, Any], old: str, new: str) -> bool:
    if old == new:
        return False
    common = {
        "INTAKE": {"DISCOVER"},
        "DISCOVER": {"BASELINE"},
        "BASELINE": {"EXPLORE"},
        "EXPLORE": {"TRIAGE"},
        "REPORT": {"DELIVER"},
        "DELIVER": set(),
    }
    if old in common:
        return new in common[old]
    mode = data["run"]["mode"]
    repair_allowed = data["run"]["repair_authorized"]
    if mode == "audit":
        return old == "TRIAGE" and new == "REPORT"
    if mode == "repair":
        graph = {
            "TRIAGE": {"REPAIR", "LOCAL_VERIFY", "REPORT"},
            "REPAIR": {"LOCAL_VERIFY"},
            "LOCAL_VERIFY": {"TRIAGE", "REPAIR", "REPORT"},
        }
        return new in graph.get(old, set())
    graph = {
        "TRIAGE": ({"REPAIR", "LOCAL_VERIFY"} if repair_allowed else {"LOCAL_VERIFY"}),
        "REPAIR": {"LOCAL_VERIFY"},
        "LOCAL_VERIFY": ({"TRIAGE", "REPAIR", "RELEASE_GATE"} if repair_allowed else {"TRIAGE", "RELEASE_GATE"}),
        "RELEASE_GATE": {"DEPLOY"},
        "DEPLOY": {"REMOTE_VERIFY", "LOCAL_VERIFY", "REPORT"},
        "REMOTE_VERIFY": {"REPORT"},
    }
    return new in graph.get(old, set())


def _attempt_outcome_transition_allowed(old: str, new: str) -> bool:
    graph = {
        "not_deployed": {"succeeded", "failed-unchanged", "failed-partial", "unknown", "blocked"},
        "unknown": {
            "unknown", "succeeded", "failed-unchanged", "failed-partial", "blocked",
            "rolled-back", "rollback-failed",
        },
        "failed-partial": {
            "failed-partial", "succeeded", "failed-unchanged", "blocked",
            "rolled-back", "rollback-failed",
        },
        "succeeded": {"rolled-back", "rollback-failed"},
        "failed-unchanged": set(),
        "blocked": set(),
        "rolled-back": set(),
        "rollback-failed": set(),
    }
    return new in graph.get(old, set())


def _binding(data: dict[str, Any], target_id: str, artifact: str, attempt_id: str) -> list[str]:
    errors: list[str] = []
    release = data.get("release")
    if not release:
        return ["release is not configured"]
    if target_id != release["target_id"]:
        errors.append(f"target {target_id} does not match release target {release['target_id']}")
    if artifact != release["intended_artifact"]:
        errors.append("artifact does not match the intended release artifact")
    if attempt_id != release.get("active_attempt_id"):
        errors.append("attempt does not match the active release attempt")
    try:
        attempt = _attempt(data, attempt_id)
        if attempt["target_id"] != target_id or attempt["intended_artifact"] != artifact:
            errors.append("attempt target/artifact binding is inconsistent")
    except LedgerError as exc:
        errors.append(str(exc))
    return errors


def _release_gate_errors(data: dict[str, Any], attempt_id: str) -> list[str]:
    errors: list[str] = []
    release = data.get("release")
    if not release:
        return ["release is not configured"]
    target = _target(data, release["target_id"])
    artifact = release["intended_artifact"]
    errors.extend(_binding(data, target["id"], artifact, attempt_id))
    if not target["authorization_source"]:
        errors.append("release target lacks an authorization source")
    if target["production"] and target["authorization_scope"] != "current-task":
        errors.append("production target requires current-task authorization")
    rollback = release["rollback"]
    if rollback["readiness"] != "ready" or not rollback["plan"]:
        errors.append("rollback readiness and plan must be ready before deployment")
    if rollback["readiness"] == "ready" and not rollback.get("recovery_artifact"):
        errors.append("ready rollback requires an immutable recovery artifact")
    if not isinstance(rollback["execution_authorized"], bool):
        errors.append("rollback execution authorization must be explicitly recorded")
    if rollback["execution_authorized"] and not rollback.get("authorization_source"):
        errors.append("authorized rollback execution requires a current-task authorization source")
    required = [
        plan for plan in data["check_plans"]
        if plan["required"] and plan["phase"] != "post-deploy" and plan["disposition"] == "in"
    ]
    predeploy = [plan for plan in required if plan["phase"] == "pre-deploy"]
    if not predeploy:
        errors.append("release gate requires at least one required pre-deploy check plan")
    class_a = [
        scenario for scenario in data["scenarios"]
        if scenario["required"] and scenario["target_id"] == target["id"]
        and scenario["risk_class"] == "A" and scenario["disposition"] == "in"
    ]
    if not class_a:
        errors.append("release gate requires a declared class A scenario on the release target")
    health = [
        plan for plan in data["check_plans"]
        if plan["kind"] == "health" and plan["phase"] == "post-deploy" and plan["disposition"] == "in"
        and plan["target_id"] == target["id"]
    ]
    if not any(plan["required"] for plan in health):
        errors.append("release gate requires a required post-deploy health plan")
    for plan in required:
        if not plan["target_id"]:
            errors.append(f"required release plan {plan['id']} must declare a target")
            continue
        if plan["target_id"] != target["id"]:
            errors.append(f"required release plan {plan['id']} must use the release target")
            continue
        result = _latest_plan(data, plan["id"], plan["target_id"], artifact, attempt_id)
        if not result:
            errors.append(f"required plan {plan['id']} has no current result")
        elif result["result"] != "pass":
            errors.append(f"required plan {plan['id']} latest result is {result['result']}")
        elif not result["evidence"]:
            errors.append(f"required plan {plan['id']} latest result lacks evidence")
    gate_scenarios = [
        scenario for scenario in data["scenarios"]
        if scenario["target_id"] == target["id"] and scenario["disposition"] == "in"
        and scenario["required"] and scenario["risk_class"] in ("A", "B")
    ]
    for scenario in gate_scenarios:
        matches = [
            item for item in data["coverage"]
            if item["scenario_id"] == scenario["id"] and item["phase"] in ("baseline", "post-fix")
            and item["target_id"] == target["id"] and item["artifact"] == artifact
            and item["attempt_id"] == attempt_id
        ]
        result = matches[-1] if matches else None
        if not result:
            errors.append(f"gating scenario {scenario['id']} lacks bound pre-deploy coverage")
        elif result["result"] != "pass" or not result["evidence"]:
            errors.append(f"gating scenario {scenario['id']} lacks an evidenced pre-deploy pass")
    for issue in data["issues"]:
        if issue["scope_status"] != "in":
            continue
        if issue["status"] == "verified":
            errors.extend(_verified_issue_errors(data, issue))
            continue
        if data["run"]["repair_authorized"] or issue["severity"] in ("P0", "P1"):
            errors.append(f"{issue['id']} {issue['severity']} blocks deployment until verified")
    return errors


def _gate_check_ids(data: dict[str, Any], attempt_id: str) -> list[str]:
    release = data["release"]
    result_ids: list[str] = []
    for plan in data["check_plans"]:
        if not plan["required"] or plan["phase"] == "post-deploy" or plan["disposition"] != "in":
            continue
        result = _latest_plan(
            data, plan["id"], release["target_id"],
            release["intended_artifact"], attempt_id,
        )
        if result:
            result_ids.append(result["id"])
    return result_ids


def _gate_coverage_ids(data: dict[str, Any], attempt_id: str) -> list[str]:
    release = data["release"]
    result_ids: list[str] = []
    for scenario in data["scenarios"]:
        if not (
            scenario["required"] and scenario["risk_class"] in ("A", "B")
            and scenario["disposition"] == "in" and scenario["target_id"] == release["target_id"]
        ):
            continue
        matches = [
            item for item in data["coverage"]
            if item["scenario_id"] == scenario["id"] and item["phase"] in ("baseline", "post-fix")
            and item["target_id"] == release["target_id"]
            and item["artifact"] == release["intended_artifact"]
            and item["attempt_id"] == attempt_id
        ]
        if matches:
            result_ids.append(matches[-1]["id"])
    return result_ids


def _required_accounting_errors(data: dict[str, Any], mode: str) -> list[str]:
    errors: list[str] = []
    release = data.get("release")
    binding: tuple[str, str, str] | None = None
    if mode == "release" and release and release.get("active_attempt_id"):
        binding = (release["target_id"], release["intended_artifact"], release["active_attempt_id"])
    for scenario in data["scenarios"]:
        if scenario["disposition"] == "out":
            if not scenario["disposition_reason"] or not scenario["disposition_evidence"]:
                errors.append(f"excluded scenario {scenario['id']} lacks reason/evidence")
            continue
        if mode == "release" and binding and scenario["required"] and scenario["target_id"] == binding[0]:
            result = _latest_scenario(data, scenario["id"], "post-deploy", *binding)
        elif mode == "release" and binding:
            result = _latest_scenario(data, scenario["id"], None, *binding)
        else:
            result = _latest_scenario(data, scenario["id"])
        if not result:
            errors.append(f"declared scenario {scenario['id']} has no current result")
            continue
        if result["result"] in ("blocked", "skipped") and not result["details"]:
            errors.append(f"scenario {scenario['id']} {result['result']} requires a reason")
        if result["result"] in ("pass", "fail") and not result["evidence"]:
            errors.append(f"scenario {scenario['id']} {result['result']} requires evidence")
        if result["result"] == "fail":
            if not result["issues"]:
                errors.append(f"failing scenario {scenario['id']} must reference a confirmed issue")
            if not result["details"] or not result["evidence"]:
                errors.append(f"failing scenario {scenario['id']} requires details and reproduction evidence")
            for issue_id in result["issues"]:
                linked_issue = _issue(data, issue_id)
                kinds = _evidence_kinds(linked_issue)
                if not kinds.intersection({"before", "reproduction"}):
                    errors.append(f"{issue_id} lacks before/reproduction evidence")
                if mode in ("repair", "release") and linked_issue["scope_status"] == "in":
                    errors.append(f"failing scenario {scenario['id']} keeps {issue_id} unresolved")
        if (
            mode == "audit" and (scenario["required"] or scenario["risk_class"] in ("A", "B"))
            and result["result"] in ("blocked", "skipped")
        ):
            errors.append(
                f"required/high-risk scenario {scenario['id']} is {result['result']}"
            )
        if mode in ("repair", "release") and (scenario["required"] or scenario["risk_class"] in ("A", "B")):
            if result["result"] != "pass":
                errors.append(f"gating scenario {scenario['id']} latest result is {result['result']}")
    for plan in data["check_plans"]:
        if plan["disposition"] == "out":
            if not plan["disposition_reason"] or not plan["disposition_evidence"]:
                errors.append(f"excluded check plan {plan['id']} lacks reason/evidence")
            continue
        if mode == "release" and binding:
            if not plan["target_id"]:
                errors.append(f"release plan {plan['id']} must declare a target")
                continue
            result = _latest_plan(data, plan["id"], plan["target_id"], binding[1], binding[2])
        else:
            result = _latest_plan(data, plan["id"])
        if not result:
            errors.append(f"declared check {plan['id']} has no current result")
        elif plan["disposition"] == "baseline-debt":
            if result["result"] != "fail" or not result["evidence"] or not plan["disposition_reason"]:
                errors.append(f"baseline debt {plan['id']} requires an evidenced current failure and reason")
        elif plan["required"] and mode in ("repair", "release") and result["result"] != "pass":
            errors.append(f"required check {plan['id']} latest result is {result['result']}")
        elif mode == "audit" and plan["required"] and result["result"] in ("blocked", "skipped"):
            errors.append(f"required audit check {plan['id']} is {result['result']}")
        elif result["result"] in ("pass", "fail") and not result["evidence"]:
            errors.append(f"check {plan['id']} latest result lacks evidence")
        elif result["result"] in ("blocked", "skipped") and not result["details"]:
            errors.append(f"check {plan['id']} {result['result']} requires a reason")
        elif mode == "audit" and result["result"] == "fail" and (not result["details"] or not result["evidence"]):
            errors.append(f"failing audit check {plan['id']} requires details and evidence")
        elif mode == "audit" and result["result"] == "fail":
            if not result["issues"]:
                errors.append(f"failing audit check {plan['id']} must reference a confirmed issue")
            for issue_id in result["issues"]:
                if not _evidence_kinds(_issue(data, issue_id)).intersection({"before", "reproduction"}):
                    errors.append(f"{issue_id} lacks before/reproduction evidence")
    return errors


def _success_errors(data: dict[str, Any]) -> list[str]:
    mode = data["run"]["mode"]
    errors = _required_accounting_errors(data, mode)
    if not data["scenarios"]:
        errors.append("success requires at least one declared browser scenario")
    applicable_scenarios = [
        scenario for scenario in data["scenarios"] if scenario["disposition"] == "in"
    ]
    release = data.get("release")
    binding: tuple[str, str, str] | None = None
    if mode == "release" and release and release.get("active_attempt_id"):
        binding = (release["target_id"], release["intended_artifact"], release["active_attempt_id"])
    applicable_results: list[dict[str, Any]] = []
    for scenario in applicable_scenarios:
        if binding and scenario["required"] and scenario["target_id"] == binding[0]:
            result = _latest_scenario(data, scenario["id"], "post-deploy", *binding)
        elif binding:
            result = _latest_scenario(data, scenario["id"], None, *binding)
        else:
            result = _latest_scenario(data, scenario["id"])
        if result:
            applicable_results.append(result)
    if not applicable_scenarios:
        errors.append("success requires at least one applicable browser scenario")
    elif mode == "audit":
        if not any(item["result"] in ("pass", "fail") for item in applicable_results):
            errors.append("audit success requires at least one executed applicable browser scenario")
    elif not any(item["result"] == "pass" for item in applicable_results):
        errors.append("repair/release success requires an applicable passing browser scenario")
    cleanup = data["run"]["cleanup"]
    if cleanup["status"] == "pending":
        errors.append("cleanup is still pending")
    if cleanup["status"] == "residual" and not cleanup["details"]:
        errors.append("residual cleanup requires named leftovers")
    if data["deliveries"] and data["run"]["state"] != "DELIVER":
        errors.append("planned delivery requires DELIVER reconciliation")
    if data["run"]["state"] == "DELIVER":
        if not data["deliveries"]:
            errors.append("DELIVER success requires at least one delivery record")
        for delivery in data["deliveries"]:
            if delivery["status"] != "succeeded":
                errors.append(f"{delivery['id']} delivery outcome is {delivery['status']}")
            elif not delivery["external_id"] or not delivery["outcome_details"] or not delivery["evidence"]:
                errors.append(f"{delivery['id']} successful delivery lacks reconciled evidence")
    in_scope = [item for item in data["issues"] if item["scope_status"] == "in"]
    if mode in ("repair", "release"):
        for issue in data["issues"]:
            repaired = issue.get("fixed_at") or any(
                item["kind"] == "repair" for item in issue["evidence"]
            )
            if repaired and issue["status"] != "verified":
                errors.append(f"{issue['id']} has repair work but is not verified")
            if repaired and issue["status"] == "verified":
                errors.extend(_verified_issue_errors(data, issue))
            if issue["status"] == "verified" and issue.get("verified_coverage_counter", 0):
                recurrences = [
                    result for result in data["coverage"]
                    if result["result"] == "fail" and issue["id"] in result["issues"]
                    and int(result["id"].split("-")[1]) > issue["verified_coverage_counter"]
                ]
                if recurrences:
                    errors.append(
                        f"{issue['id']} failed after its current verification in "
                        f"{', '.join(item['id'] for item in recurrences)}; "
                        "a later pass cannot replace a new repair/verification cycle"
                    )
        for issue in in_scope:
            if data["run"]["repair_authorized"] and issue["status"] != "verified":
                errors.append(f"{issue['id']} is in scope and must be verified for repair success")
            elif issue["severity"] in ("P0", "P1") and issue["status"] != "verified":
                errors.append(f"{issue['id']} {issue['severity']} must be verified for success")
            repaired = issue.get("fixed_at") or any(
                item["kind"] == "repair" for item in issue["evidence"]
            )
            if issue["status"] == "verified" and not repaired:
                errors.extend(_verified_issue_errors(data, issue))
    if mode != "release":
        return _dedupe(errors)
    release = data.get("release")
    if not release or not release.get("active_attempt_id"):
        return _dedupe(errors + ["release and active attempt are required"])
    binding = (release["target_id"], release["intended_artifact"], release["active_attempt_id"])
    attempt = _attempt(data, binding[2])
    errors.extend(_binding(data, *binding))
    errors.extend(_release_gate_errors(data, binding[2]))
    gate = release["gate"]
    if gate["status"] != "passed" or (gate["target_id"], gate["artifact"], gate["attempt_id"]) != binding:
        errors.append("release gate is not passed for the active target/artifact/attempt")
    elif gate["check_ids"] != _gate_check_ids(data, binding[2]):
        errors.append("release gate snapshot is stale")
    elif gate["coverage_ids"] != _gate_coverage_ids(data, binding[2]):
        errors.append("release gate browser-coverage snapshot is stale")
    if attempt["outcome"] != "succeeded" or attempt["observed_artifact"] != binding[1]:
        errors.append("active deployment did not succeed with the intended artifact")
    if attempt["outcome"] == "succeeded" and not attempt["evidence"]:
        errors.append("successful deployment lacks provider or target-state evidence")
    target = _target(data, binding[0])
    health_plans = [
        plan for plan in data["check_plans"]
        if plan["kind"] == "health" and plan["phase"] == "post-deploy" and plan["disposition"] == "in"
        and plan["target_id"] == binding[0]
    ]
    if not any(plan["required"] for plan in health_plans):
        errors.append("release requires a required post-deploy health check plan")
    for plan in health_plans:
        history = [
            item for item in data["checks"]
            if item["plan_id"] == plan["id"] and item["target_id"] == binding[0]
            and item["artifact"] == binding[1] and item["attempt_id"] == binding[2]
        ]
        result = history[-1] if history else None
        if not result:
            errors.append(f"post-deploy health plan {plan['id']} has no bound result")
        elif result["result"] != "pass" or not result["evidence"]:
            errors.append(
                f"post-deploy health plan {plan['id']} requires an evidenced bound pass; "
                f"latest result is {result['result']}"
            )
        degraded = [item["id"] for item in history if item["result"] != "pass"]
        if degraded:
            errors.append(
                f"post-deploy health plan {plan['id']} recorded degradation in this attempt "
                f"({', '.join(degraded)}); a later pass cannot convert the attempt to success"
            )
    class_a = [
        scenario for scenario in data["scenarios"]
        if scenario["target_id"] == binding[0] and scenario["risk_class"] == "A"
        and scenario["disposition"] == "in"
    ]
    if not class_a:
        errors.append("release requires at least one class A scenario on the release target")
    elif not any(
        (result := _latest_scenario(data, scenario["id"], "post-deploy", *binding))
        and result["result"] == "pass"
        and bool(result["evidence"])
        for scenario in class_a
    ):
        errors.append("release requires a passing bound class A post-deploy scenario")
    for issue in in_scope:
        repaired = issue.get("fixed_at") or any(
            item["kind"] == "repair" for item in issue["evidence"]
        )
        if repaired and issue["status"] == "verified":
            for level in ("R0", "R1"):
                if not _linked_regression_pass(
                    data, issue["id"], level, binding, required_phase="post-deploy",
                    not_before=attempt["updated_at"],
                ):
                    errors.append(f"{issue['id']} lacks bound post-deploy {level} verification")
    if release["outcome"] != "succeeded":
        errors.append(f"release outcome is {release['outcome']}")
    return _dedupe(errors)


def _disposition_replay_errors(
    item: dict[str, Any], allowed: set[str], label: str,
) -> list[str]:
    errors: list[str] = []
    origin = item.get("disposition_origin")
    if not isinstance(origin, dict):
        return [f"{label} lacks an immutable disposition origin"]
    if origin.get("status") != "in" or origin.get("at") != item.get("created_at"):
        errors.append(f"{label} has an invalid disposition origin")
    try:
        previous_at = _dt(origin.get("at"))
    except LedgerError as exc:
        errors.append(f"{label} disposition origin {exc}")
        previous_at = None
    replay = origin.get("status")
    history = item.get("disposition_history")
    if not isinstance(history, list):
        return errors + [f"{label} has invalid disposition history"]
    for change in history:
        if not isinstance(change, dict):
            errors.append(f"{label} has malformed disposition history")
            continue
        if change.get("old") not in allowed or change.get("new") not in allowed:
            errors.append(f"{label} disposition history has an invalid status")
        if change.get("old") != replay:
            errors.append(f"{label} disposition history is discontinuous")
        if change.get("old") == change.get("new"):
            errors.append(f"{label} disposition history contains a no-op transition")
        if not isinstance(change.get("reason"), str) or not change.get("reason"):
            errors.append(f"{label} disposition history lacks a reason")
        if not isinstance(change.get("evidence"), str) or not change.get("evidence"):
            errors.append(f"{label} disposition history lacks evidence")
        try:
            change_at = _dt(change.get("at"))
            if previous_at is not None and change_at < previous_at:
                errors.append(f"{label} disposition history is not chronological")
            previous_at = change_at
        except LedgerError as exc:
            errors.append(f"{label} disposition history {exc}")
        replay = change.get("new")
    if item.get("disposition") != replay:
        errors.append(f"{label} disposition does not match replayed history")
    if history:
        latest = history[-1]
        if (
            item.get("disposition_reason") != latest.get("reason")
            or item.get("disposition_evidence") != latest.get("evidence")
            or item.get("disposition_at") != latest.get("at")
        ):
            errors.append(f"{label} disposition metadata does not match replayed history")
    elif any(item.get(field) for field in (
        "disposition_reason", "disposition_evidence", "disposition_at",
    )):
        errors.append(f"{label} initial disposition has unexplained metadata")
    return errors


def _validate(data: dict[str, Any], strict: bool) -> tuple[list[str], list[str]]:
    if data.get("schema_version") != SCHEMA_VERSION:
        if data.get("schema_version") == 1:
            return ["schema v1 is unsupported; create a new schema v2 run or migrate the ledger"], []
        return [f"schema_version must be {SCHEMA_VERSION}"], []
    errors: list[str] = []
    warnings: list[str] = []
    run = data.get("run")
    if not isinstance(run, dict):
        return ["run must be an object"], warnings
    for field in ("id", "name", "mode", "depth", "state", "settlement", "next_action", "created_at", "updated_at"):
        if not isinstance(run.get(field), str) or not run[field]:
            errors.append(f"run.{field} must be a nonempty string")
    if run.get("mode") not in MODES:
        errors.append("run.mode is invalid")
    if run.get("depth") not in DEPTHS:
        errors.append("run.depth is invalid")
    if run.get("state") not in STATES:
        errors.append("run.state is invalid")
    if run.get("settlement") not in SETTLEMENTS:
        errors.append("run.settlement is invalid")
    if not isinstance(run.get("repair_authorized"), bool):
        errors.append("run.repair_authorized must be boolean")
    if run.get("mode") == "audit" and run.get("repair_authorized"):
        errors.append("audit mode cannot authorize repair")
    if run.get("mode") == "repair" and not run.get("repair_authorized"):
        errors.append("repair mode requires repair_authorized=true")
    for field in ("scopes", "notes"):
        if not isinstance(run.get(field), list) or not all(isinstance(value, str) and value for value in run.get(field, [])):
            errors.append(f"run.{field} must be a list of nonempty strings")
    cleanup = run.get("cleanup")
    if not isinstance(cleanup, dict) or cleanup.get("status") not in CLEANUP_STATUSES or not isinstance(cleanup.get("details"), str):
        errors.append("run.cleanup must contain a valid status and string details")
    collections = (
        "targets", "scenarios", "check_plans", "issues", "checks", "coverage",
        "deployment_attempts", "deliveries", "transitions", "events",
    )
    for name in collections:
        if not isinstance(data.get(name), list):
            errors.append(f"{name} must be a list")
    counters = data.get("counters")
    if not isinstance(counters, dict):
        errors.append("counters must be an object")
        counters = {}
    for kind, (_, pattern) in ID_PATTERNS.items():
        if not isinstance(counters.get(kind), int) or counters.get(kind, -1) < 0:
            errors.append(f"counters.{kind} must be a nonnegative integer")
            continue
        collection = {
            "target": "targets", "scenario": "scenarios", "check_plan": "check_plans",
            "issue": "issues", "check": "checks", "coverage": "coverage",
            "attempt": "deployment_attempts", "delivery": "deliveries",
        }[kind]
        items = data.get(collection, []) if isinstance(data.get(collection), list) else []
        ids = [item.get("id") for item in items if isinstance(item, dict)]
        if len(ids) != len(set(ids)):
            errors.append(f"duplicate id in {collection}")
        numbers = [int(match.group(1)) for value in ids if isinstance(value, str) and (match := pattern.match(value))]
        if any(not isinstance(value, str) or not pattern.match(value) for value in ids):
            errors.append(f"invalid id in {collection}")
        if counters[kind] < max(numbers, default=0):
            errors.append(f"counters.{kind} is lower than the greatest id")
    if errors:
        return _dedupe(errors), warnings
    target_ids = {item["id"] for item in data["targets"]}
    scenario_ids = {item["id"] for item in data["scenarios"]}
    plan_ids = {item["id"] for item in data["check_plans"]}
    issue_ids = {item["id"] for item in data["issues"]}
    attempt_ids = {item["id"] for item in data["deployment_attempts"]}
    if run.get("current_target_id") and run["current_target_id"] not in target_ids:
        errors.append("run.current_target_id references an unknown target")
    for target in data["targets"]:
        if target["production"] and (target["authorization_scope"] != "current-task" or not target["authorization_source"]):
            errors.append(f"{target['id']} production target lacks current-task authorization")
    for scenario in data["scenarios"]:
        if scenario["target_id"] not in target_ids:
            errors.append(f"{scenario['id']} references unknown target")
        if scenario["risk_class"] not in RISK_CLASSES or scenario["regression_level"] not in REGRESSION_LEVELS:
            errors.append(f"{scenario['id']} has invalid risk/regression values")
        if any(ref not in issue_ids for ref in scenario["issues"]):
            errors.append(f"{scenario['id']} references unknown issue")
        if scenario.get("disposition") not in ("in", "out"):
            errors.append(f"{scenario['id']} has invalid disposition")
        errors.extend(_disposition_replay_errors(
            scenario, {"in", "out"}, scenario["id"],
        ))
        if scenario.get("disposition") == "out" and (
            not scenario.get("disposition_reason") or not scenario.get("disposition_evidence")
        ):
            errors.append(f"{scenario['id']} exclusion lacks reason/evidence")
    for plan in data["check_plans"]:
        if plan["kind"] not in CHECK_KINDS or plan["phase"] not in CHECK_PHASES or plan["regression_level"] not in REGRESSION_LEVELS:
            errors.append(f"{plan['id']} has invalid kind/phase/regression values")
        if plan["target_id"] and plan["target_id"] not in target_ids:
            errors.append(f"{plan['id']} references unknown target")
        if any(ref not in issue_ids for ref in plan["issues"]):
            errors.append(f"{plan['id']} references unknown issue")
        if plan.get("disposition") not in DECLARATION_DISPOSITIONS:
            errors.append(f"{plan['id']} has invalid disposition")
        errors.extend(_disposition_replay_errors(
            plan, set(DECLARATION_DISPOSITIONS), plan["id"],
        ))
        if plan.get("disposition") != "in" and (
            not plan.get("disposition_reason") or not plan.get("disposition_evidence")
        ):
            errors.append(f"{plan['id']} disposition lacks reason/evidence")
        if plan.get("disposition") == "baseline-debt" and plan.get("phase") != "baseline":
            errors.append(f"{plan['id']} baseline debt is not a baseline plan")
    for issue in data["issues"]:
        if issue["severity"] not in SEVERITIES or issue["status"] not in ISSUE_STATUSES or issue["kind"] not in ISSUE_KINDS:
            errors.append(f"{issue['id']} has invalid enum value")
        if issue["scope_status"] not in ("in", "out") or issue["approach"] not in ("",) + APPROACHES:
            errors.append(f"{issue['id']} has invalid scope/approach")
        if issue["scope_status"] == "out" and issue["status"] in ("investigating", "fixed", "verified"):
            errors.append(f"{issue['id']} out-of-scope issue cannot be {issue['status']}")
        if not isinstance(issue.get("fixed_at"), str) or not isinstance(issue.get("verified_at"), str):
            errors.append(f"{issue['id']} has invalid lifecycle timestamps")
        if (
            not isinstance(issue.get("verified_coverage_counter"), int)
            or issue.get("verified_coverage_counter", -1) < 0
            or issue.get("verified_coverage_counter", 0) > counters["coverage"]
        ):
            errors.append(f"{issue['id']} has an invalid verified coverage counter")
        if issue["status"] == "verified" and issue.get("verified_coverage_counter", 0) == 0:
            errors.append(f"{issue['id']} verified issue lacks a coverage-order boundary")
        if not isinstance(issue.get("repair_cycle"), int) or issue.get("repair_cycle", -1) < 0:
            errors.append(f"{issue['id']} has invalid repair cycle")
        origin = issue.get("classification_origin")
        origin_at: datetime | None = None
        if not isinstance(origin, dict):
            errors.append(f"{issue['id']} lacks an immutable classification origin")
            replay_severity = None
            replay_scope = None
        else:
            replay_severity = origin.get("severity")
            replay_scope = origin.get("scope")
            if replay_severity not in SEVERITIES or replay_scope not in ("in", "out"):
                errors.append(f"{issue['id']} has an invalid classification origin")
            if not isinstance(origin.get("reason"), str) or not isinstance(origin.get("evidence"), str):
                errors.append(f"{issue['id']} classification origin has invalid reason/evidence")
            elif replay_scope == "out" and (not origin["reason"] or not origin["evidence"]):
                errors.append(f"{issue['id']} initial out-of-scope classification lacks reason/evidence")
            try:
                origin_at = _dt(origin.get("at"))
                if origin.get("at") != issue.get("created_at"):
                    errors.append(f"{issue['id']} classification origin does not match creation time")
            except LedgerError as exc:
                errors.append(f"{issue['id']} classification origin {exc}")
        if not isinstance(issue.get("classification_history"), list):
            errors.append(f"{issue['id']} has invalid classification history")
        else:
            for change in issue["classification_history"]:
                if not isinstance(change, dict):
                    errors.append(f"{issue['id']} has malformed classification history")
                    continue
                if change.get("old_severity") not in SEVERITIES or change.get("new_severity") not in SEVERITIES:
                    errors.append(f"{issue['id']} classification has invalid severity")
                if change.get("old_scope") not in ("in", "out") or change.get("new_scope") not in ("in", "out"):
                    errors.append(f"{issue['id']} classification has invalid scope")
                if not isinstance(change.get("reason"), str) or not change.get("reason"):
                    errors.append(f"{issue['id']} classification lacks reason")
                if not isinstance(change.get("evidence"), str) or not change.get("evidence"):
                    errors.append(f"{issue['id']} classification lacks evidence")
                try:
                    change_at = _dt(change.get("at"))
                    if origin_at is not None and change_at < origin_at:
                        errors.append(f"{issue['id']} classification history is not chronological")
                    origin_at = change_at
                except LedgerError as exc:
                    errors.append(f"{issue['id']} classification {exc}")
                if replay_severity is not None and change.get("old_severity") != replay_severity:
                    errors.append(f"{issue['id']} classification severity history is discontinuous")
                if replay_scope is not None and change.get("old_scope") != replay_scope:
                    errors.append(f"{issue['id']} classification scope history is discontinuous")
                replay_severity = change.get("new_severity")
                replay_scope = change.get("new_scope")
        if replay_severity is not None and replay_severity != issue.get("severity"):
            errors.append(f"{issue['id']} severity does not match replayed classification history")
        if replay_scope is not None and replay_scope != issue.get("scope_status"):
            errors.append(f"{issue['id']} scope does not match replayed classification history")
        if not issue["evidence"]:
            errors.append(f"{issue['id']} requires evidence")
        if issue["scope_status"] == "out" and any(
            evidence.get("kind") == "repair" for evidence in issue["evidence"]
            if isinstance(evidence, dict)
        ):
            errors.append(f"{issue['id']} cannot be out of scope after repair work")
        for evidence in issue["evidence"]:
            if evidence.get("kind") not in EVIDENCE_KINDS or not evidence.get("reference"):
                errors.append(f"{issue['id']} has invalid evidence")
            if not isinstance(evidence.get("cycle"), int) or evidence.get("cycle", -1) < 0:
                errors.append(f"{issue['id']} evidence has invalid repair cycle")
            elif isinstance(issue.get("repair_cycle"), int) and evidence["cycle"] > issue["repair_cycle"]:
                errors.append(f"{issue['id']} evidence repair cycle is in the future")
    for check in data["checks"]:
        if check["plan_id"] not in plan_ids or check["target_id"] not in target_ids:
            errors.append(f"{check['id']} has an invalid plan/target reference")
        if any(ref not in issue_ids for ref in check["issues"]):
            errors.append(f"{check['id']} references unknown issue")
        if check["attempt_id"] and check["attempt_id"] not in attempt_ids:
            errors.append(f"{check['id']} references unknown attempt")
        if check.get("result") not in RESULTS:
            errors.append(f"{check['id']} has an invalid result")
    for result in data["coverage"]:
        if result["scenario_id"] not in scenario_ids or result["target_id"] not in target_ids:
            errors.append(f"{result['id']} has an invalid scenario/target reference")
        if any(ref not in issue_ids for ref in result["issues"]):
            errors.append(f"{result['id']} references unknown issue")
        if result["attempt_id"] and result["attempt_id"] not in attempt_ids:
            errors.append(f"{result['id']} references unknown attempt")
        if result.get("result") not in RESULTS or result.get("phase") not in COVERAGE_PHASES:
            errors.append(f"{result['id']} has an invalid phase/result")
        if result.get("result") == "fail":
            if not result.get("issues"):
                errors.append(f"{result['id']} failing browser result lacks a confirmed issue")
            if not result.get("details") or not result.get("evidence"):
                errors.append(f"{result['id']} failing browser result lacks details/reproduction evidence")
            for ref in result.get("issues", []):
                if ref in issue_ids and not _evidence_kinds(_issue(data, ref)).intersection(
                    {"before", "reproduction"}
                ):
                    errors.append(f"{result['id']} linked issue {ref} lacks before/reproduction evidence")
                if ref in issue_ids:
                    linked = _issue(data, ref)
                    if (
                        linked.get("status") == "verified"
                        and int(result["id"].split("-")[1])
                        > linked.get("verified_coverage_counter", 0)
                    ):
                        warnings.append(
                            f"{result['id']} records {ref} failing after its current verification; "
                            "the failure is preserved and blocks a repair/release success claim"
                        )
    attempt_outcomes = {
        "not_deployed", "succeeded", "failed-unchanged", "failed-partial",
        "unknown", "rolled-back", "rollback-failed", "blocked",
    }
    for attempt in data["deployment_attempts"]:
        if attempt.get("target_id") not in target_ids:
            errors.append(f"{attempt['id']} references an unknown target")
        if not isinstance(attempt.get("intended_artifact"), str) or not attempt.get("intended_artifact"):
            errors.append(f"{attempt['id']} has an invalid intended artifact")
        if not isinstance(attempt.get("observed_artifact"), str):
            errors.append(f"{attempt['id']} has an invalid observed artifact")
        if attempt.get("status") not in ("planned", "gated", "deployed", "finished"):
            errors.append(f"{attempt['id']} has an invalid status")
        if attempt.get("outcome") not in attempt_outcomes:
            errors.append(f"{attempt['id']} has an invalid outcome")
        if not isinstance(attempt.get("details"), str):
            errors.append(f"{attempt['id']} has invalid details")
        if not isinstance(attempt.get("evidence"), list) or not all(
            isinstance(value, str) and value for value in attempt.get("evidence", [])
        ):
            errors.append(f"{attempt['id']} has invalid evidence")
        history = attempt.get("outcome_history")
        if not isinstance(history, list):
            errors.append(f"{attempt['id']} has invalid outcome history")
            history = []
        accumulated_attempt_evidence: list[str] = []
        for observation in history:
            if not isinstance(observation, dict):
                errors.append(f"{attempt['id']} has malformed outcome history")
                continue
            if observation.get("outcome") not in attempt_outcomes - {"not_deployed"}:
                errors.append(f"{attempt['id']} history has invalid outcome")
            if not isinstance(observation.get("observed_artifact"), str):
                errors.append(f"{attempt['id']} history has invalid observed artifact")
            if not isinstance(observation.get("details"), str):
                errors.append(f"{attempt['id']} history has invalid details")
            if not isinstance(observation.get("evidence"), list) or not all(
                isinstance(value, str) and value for value in observation.get("evidence", [])
            ):
                errors.append(f"{attempt['id']} history has invalid evidence")
            else:
                accumulated_attempt_evidence = _dedupe(
                    accumulated_attempt_evidence + observation["evidence"]
                )
            if observation.get("outcome") == "succeeded":
                if observation.get("observed_artifact") != attempt.get("intended_artifact"):
                    errors.append(f"{attempt['id']} succeeded history has a mismatched artifact")
                if not observation.get("evidence"):
                    errors.append(f"{attempt['id']} succeeded history lacks evidence")
            if observation.get("outcome") == "failed-unchanged" and not observation.get("observed_artifact"):
                errors.append(f"{attempt['id']} failed-unchanged history lacks an observed artifact")
            if observation.get("outcome") in ("rolled-back", "rollback-failed"):
                if not isinstance(observation.get("trigger", ""), str):
                    errors.append(f"{attempt['id']} rollback history has invalid trigger")
                if not isinstance(observation.get("trigger_evidence", ""), str):
                    errors.append(f"{attempt['id']} rollback history has invalid trigger evidence")
                if observation.get("trigger") and not observation.get("trigger_evidence"):
                    errors.append(f"{attempt['id']} rollback trigger lacks evidence")
            try:
                _dt(observation.get("at"))
            except LedgerError as exc:
                errors.append(f"{attempt['id']} history {exc}")
        replayed_outcome = "not_deployed"
        for observation in history:
            if not isinstance(observation, dict) or observation.get("outcome") not in attempt_outcomes:
                continue
            observed_outcome = observation["outcome"]
            if not _attempt_outcome_transition_allowed(replayed_outcome, observed_outcome):
                errors.append(
                    f"{attempt['id']} has illegal outcome history transition "
                    f"{replayed_outcome} -> {observed_outcome}"
                )
                break
            replayed_outcome = observed_outcome
        if attempt.get("outcome") == "not_deployed" and history:
            errors.append(f"{attempt['id']} not_deployed attempt must not have outcome history")
        if attempt.get("outcome") != "not_deployed" and (
            not history or history[-1].get("outcome") != attempt.get("outcome")
        ):
            errors.append(f"{attempt['id']} current outcome does not match outcome history")
        if history:
            latest_attempt = history[-1]
            if (
                attempt.get("observed_artifact") != latest_attempt.get("observed_artifact")
                or attempt.get("details") != latest_attempt.get("details")
                or attempt.get("updated_at") != latest_attempt.get("at")
                or attempt.get("evidence") != accumulated_attempt_evidence
            ):
                errors.append(f"{attempt['id']} current fields do not match replayed outcome history")
        elif any((
            attempt.get("observed_artifact"), attempt.get("details"), attempt.get("evidence"),
        )):
            errors.append(f"{attempt['id']} not_deployed attempt has unexplained outcome data")
        try:
            if _dt(attempt.get("updated_at")) < _dt(attempt.get("created_at")):
                errors.append(f"{attempt['id']} updated_at precedes created_at")
        except LedgerError as exc:
            errors.append(f"{attempt['id']} {exc}")
        if attempt.get("outcome") == "succeeded":
            if attempt.get("status") != "deployed":
                errors.append(f"{attempt['id']} succeeded outcome requires deployed status")
            if attempt.get("observed_artifact") != attempt.get("intended_artifact"):
                errors.append(f"{attempt['id']} succeeded outcome has mismatched artifact")
            if not attempt.get("evidence"):
                errors.append(f"{attempt['id']} succeeded outcome lacks evidence")
        if attempt.get("outcome") == "failed-unchanged" and not attempt.get("observed_artifact"):
            errors.append(f"{attempt['id']} failed-unchanged outcome lacks an observed unchanged artifact")
        if attempt.get("outcome") in ("rolled-back", "rollback-failed"):
            if attempt.get("status") != "finished" or not attempt.get("details") or not attempt.get("evidence"):
                errors.append(f"{attempt['id']} rollback outcome requires finished status, details, and evidence")
        if attempt.get("outcome") == "rolled-back" and not attempt.get("observed_artifact"):
            errors.append(f"{attempt['id']} rolled-back outcome requires an observed recovery artifact")
    for delivery in data["deliveries"]:
        if delivery.get("action") not in DELIVERY_ACTIONS or delivery.get("status") not in DELIVERY_RESULTS:
            errors.append(f"{delivery['id']} has invalid action/status")
        for field in (
            "target", "authorization_scope", "authorization_source", "idempotency_key",
            "details", "external_id", "outcome_details", "created_at", "updated_at",
        ):
            if not isinstance(delivery.get(field), str):
                errors.append(f"{delivery['id']} has invalid {field}")
        if delivery.get("authorization_scope") != "current-task" or not delivery.get("authorization_source"):
            errors.append(f"{delivery['id']} lacks current-task delivery authorization")
        if not delivery.get("target") or not delivery.get("idempotency_key") or not delivery.get("details"):
            errors.append(f"{delivery['id']} lacks exact target/idempotency key/planned effect")
        if not isinstance(delivery.get("evidence"), list) or not all(
            isinstance(value, str) and value for value in delivery.get("evidence", [])
        ):
            errors.append(f"{delivery['id']} has invalid evidence")
        history = delivery.get("history")
        if not isinstance(history, list):
            errors.append(f"{delivery['id']} has invalid history")
            history = []
        replayed_delivery = "planned"
        try:
            previous_delivery_at = _dt(delivery.get("created_at"))
        except LedgerError as exc:
            errors.append(f"{delivery['id']} {exc}")
            previous_delivery_at = None
        delivery_graph = {
            "planned": {"unknown", "succeeded", "failed", "blocked"},
            "unknown": {"unknown", "succeeded", "failed", "blocked"},
            "succeeded": set(), "failed": set(), "blocked": set(),
        }
        for observation in history:
            if not isinstance(observation, dict) or observation.get("result") not in DELIVERY_RESULTS[1:]:
                errors.append(f"{delivery['id']} has malformed history")
                continue
            observed_result = observation["result"]
            if observed_result not in delivery_graph[replayed_delivery]:
                errors.append(
                    f"{delivery['id']} has illegal delivery history transition "
                    f"{replayed_delivery} -> {observed_result}"
                )
            replayed_delivery = observed_result
            if not isinstance(observation.get("external_id"), str) or not observation.get("details"):
                errors.append(f"{delivery['id']} history lacks external id shape/details")
            if not isinstance(observation.get("evidence"), list) or not all(
                isinstance(value, str) and value for value in observation.get("evidence", [])
            ):
                errors.append(f"{delivery['id']} history has invalid evidence")
            try:
                observation_at = _dt(observation.get("at"))
                if previous_delivery_at is not None and observation_at < previous_delivery_at:
                    errors.append(f"{delivery['id']} history is not chronological")
                previous_delivery_at = observation_at
            except LedgerError as exc:
                errors.append(f"{delivery['id']} history {exc}")
        if delivery.get("status") != replayed_delivery:
            errors.append(f"{delivery['id']} current status does not match replayed history")
        if history:
            latest_delivery = history[-1]
            if (
                delivery.get("external_id") != latest_delivery.get("external_id")
                or delivery.get("outcome_details") != latest_delivery.get("details")
                or delivery.get("evidence") != latest_delivery.get("evidence")
                or delivery.get("updated_at") != latest_delivery.get("at")
            ):
                errors.append(f"{delivery['id']} current outcome does not match replayed history")
        elif any((
            delivery.get("external_id"), delivery.get("outcome_details"), delivery.get("evidence"),
        )) or delivery.get("updated_at") != delivery.get("created_at"):
            errors.append(f"{delivery['id']} planned state has unexplained outcome data")
        if delivery.get("status") == "succeeded" and (
            not delivery.get("external_id") or not delivery.get("outcome_details") or not delivery.get("evidence")
        ):
            errors.append(f"{delivery['id']} succeeded delivery lacks external id/details/evidence")
        try:
            if _dt(delivery.get("updated_at")) < _dt(delivery.get("created_at")):
                errors.append(f"{delivery['id']} updated_at precedes created_at")
        except LedgerError as exc:
            errors.append(f"{delivery['id']} {exc}")
    release = data.get("release")
    if data["deployment_attempts"] and release is None:
        errors.append("deployment attempt history requires a release configuration")
    if release is not None:
        if not isinstance(release, dict) or release.get("target_id") not in target_ids:
            errors.append("release has an invalid target")
        else:
            if not isinstance(release.get("intended_artifact"), str) or not release.get("intended_artifact"):
                errors.append("release has an invalid intended artifact")
            if release.get("outcome") not in attempt_outcomes:
                errors.append("release has an invalid outcome")
            if not isinstance(release.get("configured_at"), str):
                errors.append("release has an invalid configured_at")
            else:
                try:
                    _dt(release["configured_at"])
                except LedgerError as exc:
                    errors.append(str(exc))
            rollback = release.get("rollback")
            if not isinstance(rollback, dict):
                errors.append("release rollback must be an object")
            else:
                if rollback.get("readiness") not in ROLLBACK_READINESS:
                    errors.append("release rollback has invalid readiness")
                if not isinstance(rollback.get("plan"), str) or not rollback.get("plan"):
                    errors.append("release rollback requires a plan")
                if not isinstance(rollback.get("execution_authorized"), bool):
                    errors.append("release rollback execution authorization must be boolean")
                if not isinstance(rollback.get("authorization_source"), str):
                    errors.append("release rollback has invalid authorization source")
                elif rollback.get("execution_authorized") and not rollback.get("authorization_source"):
                    errors.append("authorized rollback execution lacks current-task authorization source")
                if not isinstance(rollback.get("recovery_artifact"), str):
                    errors.append("release rollback has invalid recovery artifact")
                elif rollback.get("readiness") == "ready" and not rollback.get("recovery_artifact"):
                    errors.append("ready rollback lacks an immutable recovery artifact")
                if not isinstance(rollback.get("triggers"), list) or not all(
                    isinstance(value, str) and value for value in rollback.get("triggers", [])
                ):
                    errors.append("release rollback has invalid triggers")
                if release.get("outcome") in ("rolled-back", "rollback-failed") and not rollback.get("execution_authorized"):
                    errors.append("recorded rollback outcome lacks execution authorization")
            active_id = release.get("active_attempt_id")
            if not isinstance(active_id, str):
                errors.append("release has an invalid active attempt id")
            elif active_id:
                if active_id not in attempt_ids:
                    errors.append("release references an unknown active attempt")
                else:
                    active = _attempt(data, active_id)
                    if active.get("target_id") != release.get("target_id"):
                        errors.append("active attempt target does not match release target")
                    if active.get("intended_artifact") != release.get("intended_artifact"):
                        errors.append("active attempt artifact does not match release artifact")
                    if active.get("outcome") != release.get("outcome"):
                        errors.append("active attempt outcome does not match release outcome")
                    if (
                        active.get("outcome") == "rolled-back" and rollback.get("recovery_artifact")
                        and active.get("observed_artifact") != rollback.get("recovery_artifact")
                    ):
                        errors.append("active rollback artifact does not match configured recovery artifact")
                    if active.get("outcome") in ("rolled-back", "rollback-failed"):
                        observation = active.get("outcome_history", [])[-1] if active.get("outcome_history") else {}
                        configured_triggers = rollback.get("triggers", [])
                        if configured_triggers and observation.get("trigger") not in configured_triggers:
                            errors.append("recorded rollback does not match a configured trigger")
                        if configured_triggers and not observation.get("trigger_evidence"):
                            errors.append("recorded conditional rollback lacks trigger evidence")
            elif release.get("outcome") != "not_deployed":
                errors.append("release without an active attempt must be not_deployed")
            gate = release.get("gate")
            if not isinstance(gate, dict):
                errors.append("release gate must be an object")
            else:
                if gate.get("status") not in ("pending", "passed"):
                    errors.append("release gate has invalid status")
                for field in ("target_id", "artifact", "attempt_id", "passed_at"):
                    if not isinstance(gate.get(field), str):
                        errors.append(f"release gate has invalid {field}")
                if not isinstance(gate.get("check_ids"), list) or not all(
                    isinstance(value, str) and value for value in gate.get("check_ids", [])
                ):
                    errors.append("release gate has invalid check_ids")
                elif any(value not in {item["id"] for item in data["checks"]} for value in gate["check_ids"]):
                    errors.append("release gate references an unknown check result")
                if not isinstance(gate.get("coverage_ids"), list) or not all(
                    isinstance(value, str) and value for value in gate.get("coverage_ids", [])
                ):
                    errors.append("release gate has invalid coverage_ids")
                elif any(value not in {item["id"] for item in data["coverage"]} for value in gate["coverage_ids"]):
                    errors.append("release gate references an unknown coverage result")
                if gate.get("status") == "pending":
                    if (
                        any(gate.get(field) for field in ("target_id", "artifact", "attempt_id", "passed_at"))
                        or gate.get("check_ids") or gate.get("coverage_ids")
                    ):
                        errors.append("pending release gate must not retain a passed binding")
                elif gate.get("status") == "passed":
                    expected = (
                        release.get("target_id"), release.get("intended_artifact"),
                        release.get("active_attempt_id"),
                    )
                    actual = (gate.get("target_id"), gate.get("artifact"), gate.get("attempt_id"))
                    if actual != expected:
                        errors.append("passed release gate binding does not match active release")
                    if not gate.get("passed_at"):
                        errors.append("passed release gate requires passed_at")
                    else:
                        try:
                            _dt(gate["passed_at"])
                        except LedgerError as exc:
                            errors.append(str(exc))
            for attempt in data["deployment_attempts"]:
                if (
                    attempt.get("target_id") != release.get("target_id")
                    or attempt.get("intended_artifact") != release.get("intended_artifact")
                ):
                    errors.append(f"{attempt['id']} does not match the immutable release target/artifact")
            if len(data["deployment_attempts"]) > 2:
                errors.append("deployment attempt limit exceeded for the release target/artifact")
    if data["deliveries"] and run["state"] not in ("REPORT", "DELIVER"):
        errors.append("delivery records may exist only in REPORT or DELIVER state")
    if run["state"] == "DELIVER" and not data["deliveries"]:
        errors.append("DELIVER state requires an authorized delivery plan")
    if run["mode"] == "release" and run["state"] in ("DEPLOY", "REMOTE_VERIFY"):
        if not release or not release.get("active_attempt_id"):
            errors.append(f"{run['state']} requires an active release attempt")
    replay = "INTAKE"
    retry_transitions: list[dict[str, Any]] = []
    for transition in data["transitions"]:
        if transition.get("from") != replay or transition.get("to") not in STATES:
            errors.append("transition history is discontinuous")
            break
        if not _transition_allowed(data, replay, transition["to"]):
            if not (transition["to"] == "REPORT" and transition.get("settlement") in ("failed", "blocked")):
                errors.append(f"illegal transition {replay} -> {transition['to']}")
                break
        replay = transition["to"]
        if transition.get("from") == "DEPLOY" and transition.get("to") == "LOCAL_VERIFY":
            retry_transitions.append(transition)
    if len(retry_transitions) > 1:
        errors.append("deployment retry transition limit exceeded")
    for transition in retry_transitions:
        try:
            transition_at = _dt(transition.get("at"))
        except LedgerError as exc:
            errors.append(f"retry transition {exc}")
            continue
        reconciled = any(
            observation.get("outcome") == "failed-unchanged"
            and _dt(observation.get("at")) <= transition_at
            for attempt in data["deployment_attempts"]
            for observation in attempt.get("outcome_history", [])
            if isinstance(observation, dict)
        )
        if not reconciled:
            errors.append("deployment retry transition lacks prior failed-unchanged reconciliation")
    if replay != run["state"]:
        errors.append("run.state does not match replayed transition history")
    try:
        if _dt(run["updated_at"]) < _dt(run["created_at"]):
            errors.append("run.updated_at precedes run.created_at")
    except LedgerError as exc:
        errors.append(str(exc))
    if strict and not errors:
        if run["state"] not in ("REPORT", "DELIVER"):
            errors.append("strict completion requires REPORT or DELIVER state")
        if run["settlement"] != "succeeded":
            errors.append(f"strict success requires succeeded settlement, found {run['settlement']}")
        errors.extend(_success_errors(data))
    return _dedupe(errors), _dedupe(warnings)


def _safe_validate(data: dict[str, Any], strict: bool) -> tuple[list[str], list[str]]:
    try:
        return _validate(data, strict)
    except (KeyError, TypeError, IndexError, AttributeError, ValueError, OverflowError, LedgerError) as exc:
        return [f"malformed schema v2 ledger near {exc!s}"], []


def _cmd_init(args: argparse.Namespace, run_dir: Path, at: str) -> str:
    if run_dir.exists():
        if not run_dir.is_dir():
            raise LedgerError("--run-dir exists but is not a directory", 4)
        if any(run_dir.iterdir()):
            raise LedgerError("init requires a new or empty --run-dir", 4)
    else:
        try:
            run_dir.mkdir(parents=True)
        except OSError as exc:
            raise LedgerError(f"cannot create run directory: {exc}", 5) from exc
    repair_authorized = args.repair_authorized
    if repair_authorized is None:
        repair_authorized = args.mode == "repair"
    if args.mode == "audit" and repair_authorized:
        raise LedgerError("audit mode cannot authorize repair")
    if args.mode == "repair" and not repair_authorized:
        raise LedgerError("repair mode requires repair_authorized=true")
    run_id = f"RUN-{at.replace(':', '').replace('-', '')}-{uuid.uuid4().hex[:8]}"
    data = {
        "schema_version": SCHEMA_VERSION,
        "run": {
            "id": run_id, "name": args.name, "mode": args.mode, "depth": args.depth,
            "repair_authorized": repair_authorized, "state": "INTAKE", "settlement": "active",
            "settlement_reason": "", "project": args.project or "", "scopes": args.scope,
            "current_target_id": "", "current_url": "",
            "next_action": args.next_action or "Discover repository and target environment",
            "notes": [], "cleanup": {"status": "not-needed", "details": ""},
            "created_at": at, "updated_at": at,
        },
        "counters": {kind: 0 for kind in ID_PATTERNS},
        "targets": [], "scenarios": [], "check_plans": [], "issues": [],
        "checks": [], "coverage": [], "release": None, "deployment_attempts": [],
        "deliveries": [], "transitions": [],
        "events": [{"at": at, "action": "init", "ref": run_id, "detail": args.name}],
    }
    errors, _ = _safe_validate(data, strict=False)
    if errors:
        raise LedgerError("cannot initialize ledger: " + "; ".join(errors), 5)
    with _lock(run_dir):
        _write(run_dir, data)
    return str(_path(run_dir))


def _cmd_declare_target(args: argparse.Namespace, data: dict[str, Any], at: str) -> str:
    if args.production and (not args.authorization_source or not args.immutable_id):
        raise LedgerError("production target requires --immutable-id and --authorization-source from the current task")
    entity_id = _next(data, "target")
    data["targets"].append({
        "id": entity_id, "name": args.name, "environment": args.environment, "url": args.url,
        "production": args.production, "isolated": args.isolated,
        "immutable_id": args.immutable_id or f"{args.environment}:{args.url}",
        "authorization_scope": "current-task" if args.authorization_source else "discovered",
        "authorization_source": args.authorization_source or "", "created_at": at,
    })
    data["run"]["next_action"] = args.next_action or f"Declare scenarios for {entity_id}"
    _event(data, at, "declare-target", entity_id, args.name)
    return entity_id


def _cmd_declare_scenario(args: argparse.Namespace, data: dict[str, Any], at: str) -> str:
    if data["run"]["state"] in ("DEPLOY", "REMOTE_VERIFY", "REPORT", "DELIVER"):
        raise LedgerError("scenarios must be declared before DEPLOY")
    _target(data, args.target)
    _issue_refs(data, args.issue)
    entity_id = _next(data, "scenario")
    data["scenarios"].append({
        "id": entity_id, "flow": args.flow, "name": args.name, "risk_class": args.risk_class,
        "target_id": args.target, "route": args.route or "", "viewport": args.viewport or "",
        "regression_level": args.regression_level, "required": args.required,
        "issues": _dedupe(args.issue), "disposition": "in", "disposition_reason": "",
        "disposition_evidence": "", "disposition_at": "",
        "disposition_origin": {"status": "in", "at": at}, "disposition_history": [],
        "created_at": at,
    })
    if data.get("release") and args.target == data["release"]["target_id"] and args.required and args.risk_class in ("A", "B"):
        data["release"]["gate"] = _empty_gate()
    data["run"]["next_action"] = args.next_action or f"Execute {entity_id}"
    _event(data, at, "declare-scenario", entity_id, f"{args.flow}: {args.name}")
    return entity_id


def _cmd_declare_check(args: argparse.Namespace, data: dict[str, Any], at: str) -> str:
    if data["run"]["state"] in ("DEPLOY", "REMOTE_VERIFY", "REPORT", "DELIVER"):
        raise LedgerError("check plans must be declared before DEPLOY")
    if data["run"]["mode"] == "release" and not args.target:
        raise LedgerError("release check plans require --target")
    if args.target:
        _target(data, args.target)
    _issue_refs(data, args.issue)
    entity_id = _next(data, "check_plan")
    data["check_plans"].append({
        "id": entity_id, "name": args.name, "kind": args.kind, "phase": args.phase,
        "environment": args.environment, "target_id": args.target or "",
        "required": args.required, "regression_level": args.regression_level,
        "command": args.executed_command or "", "issues": _dedupe(args.issue),
        "disposition": "in", "disposition_reason": "", "disposition_evidence": "",
        "disposition_at": "", "disposition_origin": {"status": "in", "at": at},
        "disposition_history": [], "created_at": at,
    })
    if data.get("release") and args.required and args.phase != "post-deploy":
        data["release"]["gate"] = _empty_gate()
    data["run"]["next_action"] = args.next_action or f"Run {entity_id}"
    _event(data, at, "declare-check", entity_id, args.name)
    return entity_id


def _cmd_set_disposition(args: argparse.Namespace, data: dict[str, Any], at: str) -> str:
    if data["run"]["state"] in ("DEPLOY", "REMOTE_VERIFY", "REPORT", "DELIVER"):
        raise LedgerError("declaration disposition must be settled before DEPLOY")
    entity_id = args.entity_id
    if entity_id.startswith("SCN-"):
        item = _scenario(data, entity_id)
        if args.status == "baseline-debt":
            raise LedgerError("baseline-debt disposition applies only to check plans")
    elif entity_id.startswith("PLN-"):
        item = _plan(data, entity_id)
        if args.status == "baseline-debt":
            if item["phase"] != "baseline":
                raise LedgerError("baseline-debt requires a baseline check plan")
            release = data.get("release")
            if data["run"]["mode"] == "release" and release and release.get("active_attempt_id"):
                result = _latest_plan(
                    data, item["id"], release["target_id"],
                    release["intended_artifact"], release["active_attempt_id"],
                )
            else:
                result = _latest_plan(data, item["id"])
            if not result or result["result"] != "fail" or not result["evidence"]:
                raise LedgerError("baseline-debt requires a current evidenced failing baseline result")
    else:
        raise LedgerError("set-disposition requires an SCN-* or PLN-* id")
    old = item["disposition"]
    if old == args.status:
        raise LedgerError("declaration already has that disposition")
    item["disposition"] = args.status
    item["disposition_reason"] = args.reason
    item["disposition_evidence"] = args.evidence
    item["disposition_at"] = at
    item["disposition_history"].append({
        "old": old, "new": args.status, "reason": args.reason,
        "evidence": args.evidence, "at": at,
    })
    if data.get("release"):
        data["release"]["gate"] = _empty_gate()
    data["run"]["next_action"] = args.next_action or f"Reconcile coverage after {entity_id} disposition"
    _event(data, at, "set-disposition", entity_id, f"{old}->{args.status}: {args.reason}")
    return entity_id


def _evidence(kind: str, reference: str, note: str, at: str, cycle: int) -> dict[str, Any]:
    return {"kind": kind, "reference": reference, "note": note, "at": at, "cycle": cycle}


def _cmd_add_issue(args: argparse.Namespace, data: dict[str, Any], at: str) -> str:
    if args.scope_status == "out" and (not args.note or not args.classification_evidence):
        raise LedgerError("initial out-of-scope issue requires reason and classification evidence")
    entity_id = _next(data, "issue")
    evidence = [_evidence("before", ref, "", at, 0) for ref in args.before_evidence]
    evidence.extend(_evidence("reproduction", ref, "", at, 0) for ref in args.evidence)
    item = {
        "id": entity_id, "title": args.title, "area": args.area, "kind": args.kind,
        "severity": args.severity, "status": "open", "scope_status": args.scope_status,
        "steps": args.step, "expected": args.expected, "actual": args.actual,
        "evidence": evidence, "root_cause": "", "resolution": "", "approach": "",
        "reused": [], "verification_notes": [], "iteration": 0, "repair_cycle": 0,
        "fixed_at": "", "verified_at": "", "verified_coverage_counter": 0,
        "classification_origin": {
            "severity": args.severity, "scope": args.scope_status,
            "reason": args.note if args.scope_status == "out" else "",
            "evidence": args.classification_evidence if args.scope_status == "out" else "",
            "at": at,
        },
        "classification_history": [],
        "next_action": args.next_action or "Triage root cause",
        "notes": [args.note] if args.note else [], "created_at": at, "updated_at": at,
    }
    data["issues"].append(item)
    data["run"]["next_action"] = item["next_action"]
    _event(data, at, "add-issue", entity_id, args.title)
    return entity_id


def _cmd_add_evidence(args: argparse.Namespace, data: dict[str, Any], at: str) -> str:
    issue = _issue(data, args.issue_id)
    state = data["run"]["state"]
    if args.kind == "diagnosis" and state not in ("TRIAGE", "REPAIR", "LOCAL_VERIFY"):
        raise LedgerError("diagnosis evidence requires TRIAGE, REPAIR, or LOCAL_VERIFY state")
    if args.kind == "repair":
        if not data["run"]["repair_authorized"] or state != "REPAIR":
            raise LedgerError("repair evidence requires authorized REPAIR state")
        if issue["scope_status"] != "in":
            raise LedgerError("repair evidence requires an in-scope issue")
        if issue["status"] != "investigating":
            raise LedgerError("repair evidence requires an investigating issue")
    if args.kind == "after":
        if not data["run"]["repair_authorized"] or state not in ("LOCAL_VERIFY", "REMOTE_VERIFY"):
            raise LedgerError("after evidence requires LOCAL_VERIFY or REMOTE_VERIFY after authorized repair")
        if issue["status"] != "fixed":
            raise LedgerError("after evidence requires the issue to be fixed first")
    if args.kind == "release" and state not in ("DEPLOY", "REMOTE_VERIFY", "REPORT"):
        raise LedgerError("release evidence requires DEPLOY, REMOTE_VERIFY, or REPORT state")
    issue["evidence"].append(_evidence(
        args.kind, args.reference, args.note or "", at, issue["repair_cycle"],
    ))
    issue["updated_at"] = at
    if args.next_action:
        issue["next_action"] = args.next_action
        data["run"]["next_action"] = args.next_action
    _event(data, at, "add-evidence", issue["id"], args.kind)
    return issue["id"]


def _cmd_update(args: argparse.Namespace, data: dict[str, Any], at: str) -> str:
    if args.target_id.upper() == "RUN":
        issue_only = (
            args.status, args.severity, args.scope_status, args.root_cause, args.resolution,
            args.approach, args.reused, args.verification, args.advance_iteration,
            args.classification_evidence,
        )
        if any(issue_only):
            raise LedgerError("issue-specific update options cannot target RUN")
        changed: list[str] = []
        if args.current_target is not None:
            _target(data, args.current_target)
            data["run"]["current_target_id"] = args.current_target
            changed.append("current_target")
        if args.current_url is not None:
            data["run"]["current_url"] = args.current_url
            changed.append("current_url")
        if args.next_action is not None:
            data["run"]["next_action"] = args.next_action
            changed.append("next_action")
        if args.note:
            data["run"]["notes"].append(args.note)
            changed.append("note")
        if args.cleanup_status:
            data["run"]["cleanup"] = {"status": args.cleanup_status, "details": args.cleanup_details or ""}
            changed.append("cleanup")
        if not changed:
            raise LedgerError("update RUN requires at least one run-specific change")
        _event(data, at, "update-run", data["run"]["id"], ",".join(changed))
        return "RUN"
    if args.current_target or args.current_url or args.cleanup_status or args.cleanup_details:
        raise LedgerError("run-specific update options cannot target an issue")
    issue = _issue(data, args.target_id)
    old_status = issue["status"]
    state = data["run"]["state"]
    classification_change = (
        (args.severity is not None and args.severity != issue["severity"])
        or (args.scope_status is not None and args.scope_status != issue["scope_status"])
    )
    if classification_change:
        if state != "TRIAGE":
            raise LedgerError("severity or scope reclassification requires TRIAGE state")
        if not args.note or not args.classification_evidence:
            raise LedgerError("severity or scope reclassification requires reason and classification evidence")
        if args.scope_status == "out" and any(
            item["kind"] == "repair" for item in issue["evidence"]
        ):
            raise LedgerError("an issue cannot move out of scope after repair work; verify or explicitly revert it")
        issue["classification_history"].append({
            "old_severity": issue["severity"], "new_severity": args.severity or issue["severity"],
            "old_scope": issue["scope_status"], "new_scope": args.scope_status or issue["scope_status"],
            "reason": args.note, "evidence": args.classification_evidence, "at": at,
        })
    elif args.classification_evidence:
        raise LedgerError("classification evidence requires a severity or scope change")
    if args.root_cause is not None:
        if state not in ("TRIAGE", "REPAIR") or old_status != "investigating":
            raise LedgerError("root cause changes require an investigating issue in TRIAGE or REPAIR")
    if (args.resolution is not None or args.approach is not None or args.reused) and state != "REPAIR":
        raise LedgerError("resolution, approach, and reuse decisions require REPAIR state")
    if (args.resolution is not None or args.approach is not None or args.reused) and old_status != "investigating":
        raise LedgerError("resolution, approach, and reuse decisions require an investigating issue")
    if args.status is not None and args.status != old_status:
        allowed = {
            "open": {"investigating", "blocked", "wont-fix"},
            "investigating": {"fixed", "blocked", "wont-fix"},
            "fixed": {"investigating", "verified", "blocked", "wont-fix"},
            "verified": {"investigating"},
            "blocked": {"investigating", "wont-fix"},
            "wont-fix": {"investigating"},
        }
        if args.status not in allowed[old_status]:
            raise LedgerError(f"illegal issue status transition {old_status} -> {args.status}")
        if args.status == "investigating" and state not in ("TRIAGE", "REPAIR", "LOCAL_VERIFY"):
            raise LedgerError("investigating status requires TRIAGE, REPAIR, or LOCAL_VERIFY state")
        proposed_scope = args.scope_status or issue["scope_status"]
        if args.status == "investigating" and proposed_scope != "in":
            raise LedgerError("investigating status requires an in-scope issue")
        if args.status == "fixed" and state != "REPAIR":
            raise LedgerError("fixed status requires REPAIR state")
        if args.status == "verified" and state not in ("LOCAL_VERIFY", "REMOTE_VERIFY"):
            raise LedgerError("verified status requires LOCAL_VERIFY or REMOTE_VERIFY state")
        if args.status in ("blocked", "wont-fix") and not args.note:
            raise LedgerError(f"{args.status} status requires a reason in --note")
    proposed_status = args.status or issue["status"]
    proposed_scope = args.scope_status or issue["scope_status"]
    if proposed_scope == "out" and proposed_status in ("investigating", "fixed", "verified"):
        raise LedgerError(f"out-of-scope issue cannot be {proposed_status}")
    changed = []
    for field in ("status", "severity", "scope_status", "root_cause", "resolution", "approach", "next_action"):
        value = getattr(args, field)
        if value is not None:
            issue[field] = value
            changed.append(field)
    if args.reused:
        issue["reused"] = _dedupe(issue["reused"] + args.reused)
        changed.append("reused")
    if args.verification:
        issue["verification_notes"].extend(args.verification)
        changed.append("verification")
    if args.note:
        issue["notes"].append(args.note)
        changed.append("note")
    if args.advance_iteration:
        issue["iteration"] += 1
        changed.append("iteration")
    if not changed:
        raise LedgerError("issue update requires at least one change")
    if issue["status"] == "fixed":
        missing = [field for field in ("root_cause", "resolution", "approach") if not issue[field]]
        if missing:
            raise LedgerError("fixed issue is missing: " + ", ".join(missing))
        if not any(
            item["kind"] == "repair" and item.get("cycle") == issue["repair_cycle"]
            for item in issue["evidence"]
        ):
            raise LedgerError("fixed issue requires repair evidence from the current repair cycle")
        if old_status != "fixed":
            issue["fixed_at"] = at
            issue["verified_at"] = ""
    if issue["status"] == "verified":
        problems = _verified_issue_errors(data, issue)
        if problems:
            raise LedgerError("; ".join(problems))
        if old_status != "verified":
            issue["verified_at"] = at
            issue["verified_coverage_counter"] = data["counters"]["coverage"]
    if issue["status"] == "investigating" and old_status in ("fixed", "verified", "blocked", "wont-fix"):
        issue["fixed_at"] = ""
        issue["verified_at"] = ""
        issue["verified_coverage_counter"] = 0
    if issue["status"] == "investigating" and old_status != "investigating":
        issue["repair_cycle"] += 1
    issue["updated_at"] = at
    if args.next_action:
        data["run"]["next_action"] = args.next_action
    _event(data, at, "update-issue", issue["id"], ",".join(changed))
    return issue["id"]


def _result_binding(data: dict[str, Any], target_id: str, artifact: str, attempt_id: str,
                    required: bool) -> None:
    if required:
        problems = _binding(data, target_id, artifact, attempt_id)
        if problems:
            raise LedgerError("; ".join(problems))
    elif artifact or attempt_id:
        if not (artifact and attempt_id):
            raise LedgerError("artifact and attempt must be supplied together")
        problems = _binding(data, target_id, artifact, attempt_id)
        if problems:
            raise LedgerError("; ".join(problems))


def _cmd_add_check(args: argparse.Namespace, data: dict[str, Any], at: str) -> str:
    plan = _plan(data, args.plan)
    target = _target(data, args.target)
    allowed_states = {
        "baseline": {"BASELINE", "EXPLORE", "TRIAGE"},
        "post-fix": {"LOCAL_VERIFY"},
        "pre-deploy": {"LOCAL_VERIFY", "RELEASE_GATE"},
        "post-deploy": {"REMOTE_VERIFY"},
    }
    if data["run"]["mode"] == "release":
        allowed_states["baseline"].update({"LOCAL_VERIFY", "RELEASE_GATE"})
    if data["run"]["state"] not in allowed_states[plan["phase"]]:
        raise LedgerError(f"{plan['phase']} check cannot be recorded in {data['run']['state']} state")
    if plan["target_id"] and plan["target_id"] != target["id"]:
        raise LedgerError("check target does not match declared plan target")
    if plan["environment"] != target["environment"]:
        raise LedgerError("check target environment does not match declared plan environment")
    if args.result in ("pass", "fail") and not args.evidence:
        raise LedgerError("passing or failing check requires evidence")
    needs_binding = data["run"]["mode"] == "release"
    _result_binding(data, target["id"], args.artifact or "", args.attempt or "", needs_binding)
    refs = _dedupe(plan["issues"] + args.issue)
    _issue_refs(data, refs)
    if plan["phase"] == "post-fix":
        not_fixed = [ref for ref in refs if _issue(data, ref)["status"] not in ("fixed", "verified")]
        if not_fixed:
            raise LedgerError("post-fix check references issues not yet fixed: " + ", ".join(not_fixed))
    entity_id = _next(data, "check")
    data["checks"].append({
        "id": entity_id, "plan_id": plan["id"], "result": args.result,
        "target_id": target["id"], "artifact": args.artifact or "", "attempt_id": args.attempt or "",
        "details": args.details or "", "issues": refs, "evidence": args.evidence, "at": at,
    })
    if data.get("release") and plan["required"] and plan["phase"] != "post-deploy":
        data["release"]["gate"] = _empty_gate()
    if args.next_action:
        data["run"]["next_action"] = args.next_action
    _event(data, at, "add-check", entity_id, f"{plan['id']}:{args.result}")
    return entity_id


def _cmd_add_coverage(args: argparse.Namespace, data: dict[str, Any], at: str) -> str:
    scenario = _scenario(data, args.scenario)
    target = _target(data, args.target)
    allowed_states = {
        "baseline": {"BASELINE", "EXPLORE", "TRIAGE"},
        "post-fix": {"LOCAL_VERIFY"},
        "post-deploy": {"REMOTE_VERIFY"},
    }
    if data["run"]["mode"] == "release":
        allowed_states["baseline"].update({"LOCAL_VERIFY", "RELEASE_GATE"})
    if data["run"]["state"] not in allowed_states[args.phase]:
        raise LedgerError(f"{args.phase} coverage cannot be recorded in {data['run']['state']} state")
    if scenario["target_id"] != target["id"]:
        raise LedgerError("coverage target does not match declared scenario target")
    needs_binding = data["run"]["mode"] == "release"
    _result_binding(data, target["id"], args.artifact or "", args.attempt or "", needs_binding)
    refs = _dedupe(scenario["issues"] + args.issue)
    _issue_refs(data, refs)
    if args.result == "fail":
        if not refs:
            raise LedgerError("failing browser coverage requires a confirmed issue")
        if not args.details or not args.evidence:
            raise LedgerError("failing browser coverage requires details and reproduction evidence")
        missing_evidence = [
            ref for ref in refs
            if not _evidence_kinds(_issue(data, ref)).intersection({"before", "reproduction"})
        ]
        if missing_evidence:
            raise LedgerError(
                "failing browser coverage references issues without before/reproduction evidence: "
                + ", ".join(missing_evidence)
            )
    if args.phase == "post-fix":
        if args.result == "fail":
            not_in_cycle = [
                ref for ref in refs
                if _issue(data, ref)["status"] not in ("investigating", "fixed", "verified")
            ]
            if not_in_cycle:
                raise LedgerError(
                    "failing post-fix coverage references issues outside an active or completed repair cycle: "
                    + ", ".join(not_in_cycle)
                )
        else:
            not_fixed = [ref for ref in refs if _issue(data, ref)["status"] not in ("fixed", "verified")]
            if not_fixed:
                raise LedgerError("post-fix coverage references issues not yet fixed: " + ", ".join(not_fixed))
    entity_id = _next(data, "coverage")
    data["coverage"].append({
        "id": entity_id, "scenario_id": scenario["id"], "phase": args.phase, "result": args.result,
        "target_id": target["id"], "artifact": args.artifact or "", "attempt_id": args.attempt or "",
        "details": args.details or "", "issues": refs, "evidence": args.evidence, "at": at,
    })
    if (
        data.get("release") and args.phase != "post-deploy" and scenario["disposition"] == "in"
        and scenario["required"] and scenario["risk_class"] in ("A", "B")
    ):
        data["release"]["gate"] = _empty_gate()
    if args.next_action:
        data["run"]["next_action"] = args.next_action
    _event(data, at, "add-coverage", entity_id, f"{scenario['id']}:{args.result}")
    return entity_id


def _cmd_configure_release(args: argparse.Namespace, data: dict[str, Any], at: str) -> str:
    if data["run"]["mode"] != "release":
        raise LedgerError("configure-release requires release mode")
    if data["run"]["state"] in ("DEPLOY", "REMOTE_VERIFY", "REPORT", "DELIVER"):
        raise LedgerError("release configuration is immutable once deployment work begins")
    if args.rollback_readiness == "ready" and not args.rollback_recovery_artifact:
        raise LedgerError("ready rollback requires --rollback-recovery-artifact")
    if args.rollback_execution_authorized and not args.rollback_authorization_source:
        raise LedgerError("authorized rollback execution requires --rollback-authorization-source")
    target = _target(data, args.target)
    proposed = {
        "target_id": target["id"], "intended_artifact": args.intended_artifact,
        "rollback": {
            "readiness": args.rollback_readiness, "plan": args.rollback_plan,
            "execution_authorized": args.rollback_execution_authorized,
            "authorization_source": args.rollback_authorization_source or "",
            "recovery_artifact": args.rollback_recovery_artifact or "",
            "triggers": args.rollback_trigger,
        },
        "active_attempt_id": "", "outcome": "not_deployed",
        "gate": _empty_gate(),
        "configured_at": at,
    }
    existing = data.get("release")
    if existing:
        if data["deployment_attempts"] or existing.get("active_attempt_id"):
            raise LedgerError("release configuration cannot change after an attempt exists; start a new run")
        same = (
            existing.get("target_id") == proposed["target_id"]
            and existing.get("intended_artifact") == proposed["intended_artifact"]
            and existing.get("rollback") == proposed["rollback"]
        )
        if same:
            return target["id"]
        raise LedgerError("release target, artifact, and rollback policy are immutable; start a new run")
    data["release"] = proposed
    data["run"]["current_target_id"] = target["id"]
    data["run"]["next_action"] = args.next_action or "Declare required checks and deployment attempt"
    _event(data, at, "configure-release", target["id"], args.intended_artifact)
    return target["id"]


def _cmd_declare_attempt(args: argparse.Namespace, data: dict[str, Any], at: str) -> str:
    release = data.get("release")
    if not release:
        raise LedgerError("declare-attempt requires configured release")
    if data["run"]["state"] not in ("BASELINE", "EXPLORE", "TRIAGE", "LOCAL_VERIFY", "RELEASE_GATE"):
        raise LedgerError("declare-attempt requires BASELINE through RELEASE_GATE state")
    matching = [
        item for item in data["deployment_attempts"]
        if item["target_id"] == release["target_id"]
        and item["intended_artifact"] == release["intended_artifact"]
    ]
    active_id = release.get("active_attempt_id", "")
    if active_id:
        active = _attempt(data, active_id)
        if active["outcome"] == "not_deployed":
            return active_id
        if data["run"]["state"] != "LOCAL_VERIFY" or active["outcome"] != "failed-unchanged":
            raise LedgerError("a new attempt requires a reconciled failed-unchanged attempt in LOCAL_VERIFY")
        if not active["details"] or not active["evidence"]:
            raise LedgerError("retry requires reconciliation details and evidence")
    elif matching:
        raise LedgerError("attempt history exists without an active attempt; repair the ledger before retry")
    if len(matching) >= 2:
        raise LedgerError("deployment retry limit reached for this target/artifact")
    entity_id = _next(data, "attempt")
    data["deployment_attempts"].append({
        "id": entity_id, "target_id": release["target_id"],
        "intended_artifact": release["intended_artifact"], "observed_artifact": "",
        "status": "planned", "outcome": "not_deployed", "details": "", "evidence": [],
        "outcome_history": [],
        "created_at": at, "updated_at": at,
    })
    release["active_attempt_id"] = entity_id
    release["outcome"] = "not_deployed"
    release["gate"] = _empty_gate()
    data["run"]["next_action"] = args.next_action or f"Record pre-deploy checks for {entity_id}"
    _event(data, at, "declare-attempt", entity_id, release["intended_artifact"])
    return entity_id


def _cmd_release_gate(args: argparse.Namespace, data: dict[str, Any], at: str) -> str:
    if data["run"]["state"] != "RELEASE_GATE":
        raise LedgerError("release-gate requires RELEASE_GATE state")
    problems = _release_gate_errors(data, args.attempt)
    if problems:
        raise LedgerError("release gate failed: " + "; ".join(problems))
    release = data["release"]
    check_ids = _gate_check_ids(data, args.attempt)
    release["gate"] = {
        "status": "passed", "target_id": release["target_id"], "artifact": release["intended_artifact"],
        "attempt_id": args.attempt, "passed_at": at, "check_ids": check_ids,
        "coverage_ids": _gate_coverage_ids(data, args.attempt),
    }
    attempt = _attempt(data, args.attempt)
    attempt["status"] = "gated"
    attempt["updated_at"] = at
    data["run"]["next_action"] = args.next_action or "Advance to DEPLOY"
    _event(data, at, "release-gate", args.attempt, "passed")
    return args.attempt


def _cmd_record_deployment(args: argparse.Namespace, data: dict[str, Any], at: str) -> str:
    if data["run"]["state"] != "DEPLOY":
        raise LedgerError("record-deployment requires DEPLOY state")
    release = data.get("release")
    if not release or release["active_attempt_id"] != args.attempt:
        raise LedgerError("deployment attempt is not the active release attempt")
    gate = release["gate"]
    if gate["status"] != "passed" or gate["attempt_id"] != args.attempt:
        raise LedgerError("deployment attempt has not passed its release gate")
    attempt = _attempt(data, args.attempt)
    if not args.evidence:
        raise LedgerError("deployment outcome requires provider or target-state evidence")
    if args.result != "pass" and not args.details:
        raise LedgerError("non-passing deployment outcome requires details")
    observed = args.observed_artifact or ""
    if args.result == "pass":
        if not observed:
            raise LedgerError("successful deployment requires --observed-artifact")
        if observed != release["intended_artifact"]:
            raise LedgerError("observed artifact does not match intended artifact")
        outcome = "succeeded"
        status = "deployed"
    else:
        outcome = args.result
        status = "finished"
        if outcome == "failed-unchanged" and not observed:
            raise LedgerError("failed-unchanged deployment reconciliation requires --observed-artifact")
    if not _attempt_outcome_transition_allowed(attempt["outcome"], outcome):
        raise LedgerError(f"illegal deployment outcome transition {attempt['outcome']} -> {outcome}")
    attempt.update({
        "observed_artifact": observed, "status": status, "outcome": outcome,
        "details": args.details or "", "evidence": _dedupe(attempt["evidence"] + args.evidence),
        "updated_at": at,
    })
    attempt["outcome_history"].append({
        "outcome": outcome, "observed_artifact": observed, "details": args.details or "",
        "evidence": args.evidence, "at": at,
    })
    release["outcome"] = outcome
    data["run"]["next_action"] = args.next_action or (
        "Advance to REMOTE_VERIFY" if outcome == "succeeded" else "Reconcile target state before retry or report"
    )
    _event(data, at, "record-deployment", args.attempt, outcome)
    return args.attempt


def _cmd_record_rollback(args: argparse.Namespace, data: dict[str, Any], at: str) -> str:
    if data["run"]["state"] not in ("DEPLOY", "REMOTE_VERIFY"):
        raise LedgerError("record-rollback requires DEPLOY or REMOTE_VERIFY state")
    release = data.get("release")
    if not release or release.get("active_attempt_id") != args.attempt:
        raise LedgerError("rollback attempt is not the active release attempt")
    rollback = release["rollback"]
    if not rollback["execution_authorized"]:
        raise LedgerError("rollback execution was not authorized for this release")
    configured_triggers = rollback.get("triggers", [])
    if configured_triggers:
        if not args.trigger or args.trigger not in configured_triggers:
            raise LedgerError("conditional rollback requires an exact configured --trigger")
        if not args.trigger_evidence:
            raise LedgerError("conditional rollback requires --trigger-evidence")
    elif args.trigger_evidence and not args.trigger:
        raise LedgerError("--trigger-evidence requires --trigger")
    if args.trigger and not args.trigger_evidence:
        raise LedgerError("a recorded rollback trigger requires --trigger-evidence")
    if not args.evidence or not args.details:
        raise LedgerError("rollback outcome requires details and evidence")
    observed = args.observed_artifact or ""
    if args.result == "rolled-back":
        if not observed:
            raise LedgerError("successful rollback requires --observed-artifact")
        recovery = rollback.get("recovery_artifact", "")
        if not recovery:
            raise LedgerError("successful rollback requires a configured recovery artifact")
        if observed != recovery:
            raise LedgerError("observed rollback artifact does not match the recovery artifact")
        if args.health_result != "pass":
            raise LedgerError("successful rollback requires a passing restored-health result")
    attempt = _attempt(data, args.attempt)
    if not _attempt_outcome_transition_allowed(attempt["outcome"], args.result):
        raise LedgerError(f"illegal rollback outcome transition {attempt['outcome']} -> {args.result}")
    attempt.update({
        "observed_artifact": observed, "status": "finished", "outcome": args.result,
        "details": (
            f"rollback trigger={args.trigger or 'unconditional'}; "
            f"health={args.health_result}; {args.details}"
        ),
        "evidence": _dedupe(attempt["evidence"] + args.evidence), "updated_at": at,
    })
    attempt["outcome_history"].append({
        "outcome": args.result, "observed_artifact": observed,
        "details": (
            f"rollback trigger={args.trigger or 'unconditional'}; "
            f"health={args.health_result}; {args.details}"
        ),
        "evidence": args.evidence, "at": at,
        "trigger": args.trigger or "", "trigger_evidence": args.trigger_evidence or "",
    })
    release["outcome"] = args.result
    data["run"]["next_action"] = args.next_action or "Report rollback outcome and residual risk"
    _event(data, at, "record-rollback", args.attempt, f"{args.result}; health={args.health_result}")
    return args.attempt


def _cmd_plan_delivery(args: argparse.Namespace, data: dict[str, Any], at: str) -> str:
    if data["run"]["state"] != "REPORT":
        raise LedgerError("plan-delivery requires REPORT state")
    for item in data["deliveries"]:
        same_key = (
            item["action"] == args.action
            and item["target"] == args.target
            and item["idempotency_key"] == args.idempotency_key
        )
        if same_key:
            if (
                item["authorization_source"] == args.authorization_source
                and item["details"] == args.details
            ):
                return item["id"]
            raise LedgerError("delivery idempotency key already exists with different authority or effect")
    entity_id = _next(data, "delivery")
    data["deliveries"].append({
        "id": entity_id, "action": args.action, "target": args.target,
        "authorization_scope": "current-task",
        "authorization_source": args.authorization_source,
        "idempotency_key": args.idempotency_key, "details": args.details,
        "status": "planned", "external_id": "", "outcome_details": "",
        "evidence": [], "history": [], "created_at": at, "updated_at": at,
    })
    data["run"]["next_action"] = args.next_action or f"Advance to DELIVER and reconcile {entity_id}"
    _event(data, at, "plan-delivery", entity_id, f"{args.action}:{args.target}")
    return entity_id


def _cmd_record_delivery(args: argparse.Namespace, data: dict[str, Any], at: str) -> str:
    if data["run"]["state"] != "DELIVER":
        raise LedgerError("record-delivery requires DELIVER state")
    delivery = _entity(data, "deliveries", args.delivery, "delivery")
    if args.result == "succeeded" and not args.external_id:
        raise LedgerError("successful delivery requires --external-id")
    if not args.details or not args.evidence:
        raise LedgerError("delivery outcome requires details and evidence")
    if delivery["status"] in ("succeeded", "failed", "blocked"):
        same = (
            delivery["status"] == args.result
            and delivery["external_id"] == (args.external_id or "")
            and delivery["outcome_details"] == args.details
            and delivery["evidence"] == args.evidence
        )
        if same:
            return delivery["id"]
        raise LedgerError("terminal delivery outcome cannot be overwritten")
    delivery.update({
        "status": args.result, "external_id": args.external_id or "",
        "outcome_details": args.details, "evidence": args.evidence, "updated_at": at,
    })
    delivery["history"].append({
        "result": args.result, "external_id": args.external_id or "",
        "details": args.details, "evidence": args.evidence, "at": at,
    })
    data["run"]["next_action"] = args.next_action or (
        "Complete delivery handoff" if args.result == "succeeded"
        else f"Reconcile delivery state for {delivery['id']}"
    )
    _event(data, at, "record-delivery", delivery["id"], args.result)
    return delivery["id"]


def _cmd_advance(args: argparse.Namespace, data: dict[str, Any], at: str) -> str:
    old = data["run"]["state"]
    new = args.state
    settlement = args.settlement
    if new == "REPORT":
        settlement = settlement or "succeeded"
        if settlement in ("failed", "blocked"):
            if not args.reason:
                raise LedgerError(f"{settlement} settlement requires --reason")
        else:
            if not _transition_allowed(data, old, new):
                raise LedgerError(f"illegal successful transition {old} -> {new}")
            problems = _success_errors(data)
            if problems:
                raise LedgerError("success gate failed: " + "; ".join(problems))
    else:
        if settlement is not None:
            raise LedgerError("--settlement is valid only when advancing to REPORT")
        if not _transition_allowed(data, old, new):
            raise LedgerError(f"illegal transition {old} -> {new}")
    if new == "REPAIR" and not data["run"]["repair_authorized"]:
        raise LedgerError("REPAIR requires repair_authorized=true")
    if old == "REPORT" and new == "DELIVER":
        if not data["deliveries"]:
            raise LedgerError("DELIVER requires at least one explicitly authorized delivery plan")
        invalid = [
            item["id"] for item in data["deliveries"]
            if item["status"] != "planned" or item["authorization_scope"] != "current-task"
            or not item["authorization_source"] or not item["target"]
            or not item["idempotency_key"] or not item["details"]
        ]
        if invalid:
            raise LedgerError("DELIVER has invalid or already executed plans: " + ", ".join(invalid))
    if old == "DEPLOY" and new == "LOCAL_VERIFY":
        release = data.get("release")
        if not release or not release.get("active_attempt_id"):
            raise LedgerError("deployment retry requires an active attempt")
        attempt = _attempt(data, release["active_attempt_id"])
        if attempt["outcome"] != "failed-unchanged":
            raise LedgerError("retry requires a reconciled failed-unchanged deployment outcome")
        if not attempt["details"] or not attempt["evidence"]:
            raise LedgerError("retry requires reconciliation details and evidence")
        matching = [
            item for item in data["deployment_attempts"]
            if item["target_id"] == release["target_id"]
            and item["intended_artifact"] == release["intended_artifact"]
        ]
        if len(matching) >= 2:
            raise LedgerError("deployment retry limit reached for this target/artifact")
    if new == "DEPLOY":
        release = data.get("release")
        if not release or release["gate"]["status"] != "passed":
            raise LedgerError("DEPLOY requires a passing release gate")
        attempt_id = release.get("active_attempt_id", "")
        gate = release["gate"]
        binding = (release["target_id"], release["intended_artifact"], attempt_id)
        if (gate["target_id"], gate["artifact"], gate["attempt_id"]) != binding:
            raise LedgerError("DEPLOY requires a gate bound to the active target/artifact/attempt")
        problems = _release_gate_errors(data, attempt_id)
        if problems:
            raise LedgerError("DEPLOY gate recheck failed: " + "; ".join(problems))
        if gate["check_ids"] != _gate_check_ids(data, attempt_id):
            raise LedgerError("DEPLOY gate snapshot is stale; rerun release-gate")
        if gate["coverage_ids"] != _gate_coverage_ids(data, attempt_id):
            raise LedgerError("DEPLOY browser-coverage snapshot is stale; rerun release-gate")
    if new == "REMOTE_VERIFY":
        release = data.get("release")
        if not release or not release["active_attempt_id"]:
            raise LedgerError("REMOTE_VERIFY requires an active deployment attempt")
        attempt = _attempt(data, release["active_attempt_id"])
        if attempt["outcome"] != "succeeded" or attempt["observed_artifact"] != release["intended_artifact"]:
            raise LedgerError("REMOTE_VERIFY requires intended artifact successfully observed")
    data["run"]["state"] = new
    if new == "REPORT":
        data["run"]["settlement"] = settlement
        data["run"]["settlement_reason"] = args.reason or ""
    data["run"]["next_action"] = args.next_action or (
        "Deliver final report" if new == "REPORT" else f"Execute {new} phase"
    )
    data["transitions"].append({
        "from": old, "to": new, "settlement": settlement or "", "reason": args.reason or "", "at": at,
    })
    _event(data, at, "advance", data["run"]["id"], f"{old}->{new}")
    return new


def _summary(data: dict[str, Any]) -> dict[str, Any]:
    release = data.get("release")
    target = _target(data, release["target_id"]) if release else None
    attempt = _attempt(data, release["active_attempt_id"]) if release and release.get("active_attempt_id") else None
    latest_coverage = _latest(data["coverage"], lambda item: (item["scenario_id"], item["phase"], item["target_id"], item["artifact"], item["attempt_id"]))
    latest_checks = _latest(data["checks"], lambda item: (item["plan_id"], item["target_id"], item["artifact"], item["attempt_id"]))
    health_plan_ids = {
        item["id"] for item in data["check_plans"]
        if item["kind"] == "health" and item["phase"] == "post-deploy"
    }
    postdeploy_health_history = [
        item for item in data["checks"] if item["plan_id"] in health_plan_ids
    ]
    open_high = [
        {"id": item["id"], "severity": item["severity"], "status": item["status"], "title": item["title"]}
        for item in data["issues"]
        if item["scope_status"] == "in" and item["severity"] in ("P0", "P1") and item["status"] != "verified"
    ]
    post_verification_regressions = []
    for issue in data["issues"]:
        if issue["status"] != "verified" or not issue.get("verified_coverage_counter", 0):
            continue
        failures = [
            result for result in data["coverage"]
            if result["result"] == "fail" and issue["id"] in result["issues"]
            and int(result["id"].split("-")[1]) > issue["verified_coverage_counter"]
        ]
        if failures:
            post_verification_regressions.append({
                "issue_id": issue["id"], "verified_at": issue["verified_at"],
                "failure_ids": [item["id"] for item in failures],
                "latest_failure_at": failures[-1]["at"],
            })
    blocked = [
        {"type": "coverage", "id": item["id"], "result": item["result"], "details": item["details"]}
        for item in latest_coverage.values() if item["result"] in ("blocked", "skipped")
    ] + [
        {"type": "check", "id": item["id"], "result": item["result"], "details": item["details"]}
        for item in latest_checks.values() if item["result"] in ("blocked", "skipped")
    ]
    return {
        "run": data["run"], "active_target": target, "release": release, "active_attempt": attempt,
        "issue_counts": {
            "total": len(data["issues"]),
            "by_severity": dict(sorted(Counter(item["severity"] for item in data["issues"]).items())),
            "by_status": dict(sorted(Counter(item["status"] for item in data["issues"]).items())),
        },
        "open_high_severity": open_high, "blocked_or_skipped": blocked,
        "post_verification_regressions": post_verification_regressions,
        "declared_scenarios": data["scenarios"], "latest_coverage": list(latest_coverage.values()),
        "declared_checks": data["check_plans"], "latest_checks": list(latest_checks.values()),
        "postdeploy_health_history": postdeploy_health_history,
        "issues": data["issues"], "deployment_attempts": data["deployment_attempts"],
        "deliveries": data["deliveries"],
    }


def _markdown(summary: dict[str, Any]) -> str:
    run = summary["run"]
    lines = [
        f"# QA run: {run['name']}", "",
        f"- ID: {run['id']}",
        f"- Mode/depth: {run['mode']} / {run['depth']}; repair authorized: {str(run['repair_authorized']).lower()}",
        f"- State/settlement: {run['state']} / {run['settlement']}",
        f"- Current target/URL: {run['current_target_id'] or 'not recorded'} / {run['current_url'] or 'not recorded'}",
        f"- Next action: {run['next_action']}",
        f"- Cleanup: {run['cleanup']['status']} — {run['cleanup']['details'] or 'no details'}",
    ]
    if run["notes"]:
        lines.append(f"- Notes: {'; '.join(run['notes'])}")
    release = summary["release"]
    if release:
        attempt = summary["active_attempt"] or {}
        target = summary["active_target"] or {}
        lines.extend([
            "", "## Release context", "",
            f"- Target: {target.get('id')} / {target.get('immutable_id')} / {target.get('environment')}",
            f"- Intended/observed artifact: {release['intended_artifact']} / {attempt.get('observed_artifact') or 'not observed'}",
            f"- Attempt/outcome: {release.get('active_attempt_id') or 'none'} / {release['outcome']}",
            f"- Gate: {release['gate']['status']}",
            f"- Rollback: {release['rollback']['readiness']}; execution authorized: "
            f"{str(release['rollback']['execution_authorized']).lower()}; authority: "
            f"{release['rollback']['authorization_source'] or 'not granted'}",
        ])
        if summary["deployment_attempts"]:
            lines.extend(["", "## Deployment attempts", ""])
            for recorded in summary["deployment_attempts"]:
                lines.append(
                    f"- {recorded['id']} [{recorded['outcome']}; {recorded['status']}] "
                    f"intended={recorded['intended_artifact']}; "
                    f"observed={recorded['observed_artifact'] or 'not observed'}; "
                    f"created={recorded['created_at']}; updated={recorded['updated_at']}"
                )
                for observation in recorded["outcome_history"]:
                    lines.append(
                        f"  - {observation['at']} {observation['outcome']}: "
                        f"observed={observation['observed_artifact'] or 'not observed'}; "
                        f"{observation['details'] or 'no details'}; "
                        f"evidence={', '.join(observation['evidence']) or 'none'}"
                    )
    lines.extend(["", "## Issues", "", f"- Counts: {summary['issue_counts']}"])
    for item in summary["open_high_severity"]:
        lines.append(f"- OPEN HIGH: {item['id']} {item['severity']} [{item['status']}] {item['title']}")
    for item in summary["post_verification_regressions"]:
        lines.append(
            f"- REGRESSED: {item['issue_id']} was verified at {item['verified_at']} but failed in "
            f"{', '.join(item['failure_ids'])}; latest failure={item['latest_failure_at']}"
        )
    for issue in summary["issues"]:
        suffix = ""
        if issue["scope_status"] == "out":
            change = next(
                (
                    item for item in reversed(issue["classification_history"])
                    if item.get("new_scope") == "out" and item.get("old_scope") != "out"
                ),
                None,
            )
            source = change or issue.get("classification_origin", {})
            if source.get("reason") and source.get("evidence"):
                suffix = f" — out: {source['reason']}; evidence: {source['evidence']}"
        lines.append(
            f"- {issue['id']} {issue['severity']} [{issue['status']}; scope={issue['scope_status']}] "
            f"{issue['title']}{suffix}"
        )
        for change in issue["classification_history"]:
            lines.append(
                f"  - classification {change['at']}: severity "
                f"{change['old_severity']}->{change['new_severity']}; scope "
                f"{change['old_scope']}->{change['new_scope']}; reason={change['reason']}; "
                f"evidence={change['evidence']}"
            )
    if not summary["issues"]:
        lines.append("- No confirmed issues recorded.")
    lines.extend(["", "## Declared coverage and latest results", ""])
    results = {item["scenario_id"]: item for item in summary["latest_coverage"]}
    for scenario in summary["declared_scenarios"]:
        result = results.get(scenario["id"])
        latest = result["result"] if result else "unexecuted"
        disposition = scenario["disposition"]
        suffix = (
            f"; reason: {scenario['disposition_reason']}; evidence: {scenario['disposition_evidence']}"
            if disposition != "in" else ""
        )
        lines.append(
            f"- {scenario['id']} {scenario['risk_class']} {scenario['flow']}: {scenario['name']} "
            f"— disposition={disposition}{suffix}; latest={latest}"
        )
    lines.extend(["", "## Declared checks and latest results", ""])
    checks = {item["plan_id"]: item for item in summary["latest_checks"]}
    for plan in summary["declared_checks"]:
        result = checks.get(plan["id"])
        latest = result["result"] if result else "unexecuted"
        disposition = plan["disposition"]
        suffix = (
            f"; reason: {plan['disposition_reason']}; evidence: {plan['disposition_evidence']}"
            if disposition != "in" else ""
        )
        lines.append(
            f"- {plan['id']} {plan['phase']} {plan['name']} "
            f"— disposition={disposition}{suffix}; latest={latest}"
        )
    if summary["postdeploy_health_history"]:
        lines.extend(["", "## Post-deploy health history", ""])
        for result in summary["postdeploy_health_history"]:
            lines.append(
                f"- {result['id']} plan={result['plan_id']} result={result['result']}; "
                f"target={result['target_id']}; artifact={result['artifact'] or 'unbound'}; "
                f"attempt={result['attempt_id'] or 'unbound'}; at={result['at']}; "
                f"details={result['details'] or 'none'}; evidence={', '.join(result['evidence']) or 'none'}"
            )
    if summary["blocked_or_skipped"]:
        lines.extend(["", "## Blocked or skipped", ""])
        for item in summary["blocked_or_skipped"]:
            lines.append(f"- {item['type']} {item['id']} [{item['result']}] {item['details'] or 'no reason recorded'}")
    if summary["deliveries"]:
        lines.extend(["", "## Delivery actions", ""])
        for item in summary["deliveries"]:
            lines.append(
                f"- {item['id']} {item['action']} [{item['status']}] target={item['target']}; "
                f"authority={item['authorization_source']}; key={item['idempotency_key']}; "
                f"planned-effect={item['details']}; "
                f"external={item['external_id'] or 'not recorded'}; "
                f"outcome={item['outcome_details'] or 'not recorded'}; "
                f"evidence={', '.join(item['evidence']) or 'none'}"
            )
            for observation in item["history"]:
                lines.append(
                    f"  - {observation['at']} {observation['result']}: "
                    f"{observation['details']}; external={observation['external_id'] or 'not recorded'}; "
                    f"evidence={', '.join(observation['evidence']) or 'none'}"
                )
    return "\n".join(lines)


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Maintain a schema-v2 webapp QA ledger")
    parser.add_argument("--run-dir", required=True, help="absolute directory dedicated to one QA run")
    parser.add_argument("--at", help="optional RFC3339 timestamp for deterministic tests")
    commands = parser.add_subparsers(dest="subcommand", required=True)
    init = commands.add_parser("init", help="initialize a new schema-v2 ledger")
    init.add_argument("--name", required=True, type=_text)
    init.add_argument("--mode", required=True, choices=MODES)
    init.add_argument("--depth", required=True, choices=DEPTHS)
    init.add_argument("--repair-authorized", type=_bool)
    init.add_argument("--scope", action="append", required=True, type=_text)
    init.add_argument("--project", type=_text)
    init.add_argument("--next-action", type=_text)
    target = commands.add_parser("declare-target", help="declare one immutable environment target")
    target.add_argument("--name", required=True, type=_text)
    target.add_argument("--environment", required=True, type=_text)
    target.add_argument("--url", required=True, type=_text)
    target.add_argument("--immutable-id", type=_text)
    target.add_argument("--production", action="store_true")
    target.add_argument("--isolated", action="store_true")
    target.add_argument("--authorization-source", type=_text)
    target.add_argument("--next-action", type=_text)
    scenario = commands.add_parser("declare-scenario", help="declare planned browser coverage")
    scenario.add_argument("--flow", required=True, type=_text)
    scenario.add_argument("--name", required=True, type=_text)
    scenario.add_argument("--risk-class", required=True, choices=RISK_CLASSES)
    scenario.add_argument("--target", required=True, type=_text)
    scenario.add_argument("--route", type=_text)
    scenario.add_argument("--viewport", type=_text)
    scenario.add_argument("--regression-level", default="R1", choices=REGRESSION_LEVELS)
    group = scenario.add_mutually_exclusive_group()
    group.add_argument("--required", dest="required", action="store_true")
    group.add_argument("--optional", dest="required", action="store_false")
    scenario.set_defaults(required=True)
    scenario.add_argument("--issue", action="append", default=[], type=_text)
    scenario.add_argument("--next-action", type=_text)
    plan = commands.add_parser("declare-check", help="declare an automated or operational check")
    plan.add_argument("--name", required=True, type=_text)
    plan.add_argument("--kind", required=True, choices=CHECK_KINDS)
    plan.add_argument("--phase", required=True, choices=CHECK_PHASES)
    plan.add_argument("--environment", required=True, type=_text)
    plan.add_argument("--target", type=_text)
    group = plan.add_mutually_exclusive_group()
    group.add_argument("--required", dest="required", action="store_true")
    group.add_argument("--optional", dest="required", action="store_false")
    plan.set_defaults(required=False)
    plan.add_argument("--regression-level", default="R1", choices=REGRESSION_LEVELS)
    plan.add_argument("--command", dest="executed_command", type=_text)
    plan.add_argument("--issue", action="append", default=[], type=_text)
    plan.add_argument("--next-action", type=_text)
    disposition = commands.add_parser("set-disposition", help="record an evidenced scenario/check scope disposition")
    disposition.add_argument("entity_id", type=_text)
    disposition.add_argument("--status", required=True, choices=DECLARATION_DISPOSITIONS)
    disposition.add_argument("--reason", required=True, type=_text)
    disposition.add_argument("--evidence", required=True, type=_text)
    disposition.add_argument("--next-action", type=_text)
    issue = commands.add_parser("add", help="add one confirmed issue")
    issue.add_argument("--title", required=True, type=_text)
    issue.add_argument("--area", required=True, type=_text)
    issue.add_argument("--kind", required=True, choices=ISSUE_KINDS)
    issue.add_argument("--severity", required=True, choices=SEVERITIES)
    issue.add_argument("--scope-status", default="in", choices=("in", "out"))
    issue.add_argument("--classification-evidence", type=_text)
    issue.add_argument("--step", action="append", required=True, type=_text)
    issue.add_argument("--expected", required=True, type=_text)
    issue.add_argument("--actual", required=True, type=_text)
    issue.add_argument("--before-evidence", action="append", required=True, type=_text)
    issue.add_argument("--evidence", action="append", default=[], type=_text)
    issue.add_argument("--note", type=_text)
    issue.add_argument("--next-action", type=_text)
    evidence = commands.add_parser("add-evidence", help="add typed evidence to an issue")
    evidence.add_argument("issue_id", type=_text)
    evidence.add_argument("--kind", required=True, choices=EVIDENCE_KINDS)
    evidence.add_argument("--ref", "--reference", dest="reference", required=True, type=_text)
    evidence.add_argument("--note", type=_text)
    evidence.add_argument("--next-action", type=_text)
    update = commands.add_parser("update", help="update RUN metadata or one issue; state changes use advance")
    update.add_argument("target_id", type=_text)
    update.add_argument("--current-target", type=_text)
    update.add_argument("--current-url", type=_text)
    update.add_argument("--cleanup-status", choices=CLEANUP_STATUSES)
    update.add_argument("--cleanup-details", type=_text)
    update.add_argument("--status", choices=ISSUE_STATUSES)
    update.add_argument("--severity", choices=SEVERITIES)
    update.add_argument("--scope-status", choices=("in", "out"))
    update.add_argument("--classification-evidence", type=_text)
    update.add_argument("--root-cause", type=_text)
    update.add_argument("--resolution", type=_text)
    update.add_argument("--approach", choices=APPROACHES)
    update.add_argument("--reused", action="append", default=[], type=_text)
    update.add_argument("--verification", action="append", default=[], type=_text)
    update.add_argument("--advance-iteration", action="store_true")
    update.add_argument("--note", type=_text)
    update.add_argument("--next-action", type=_text)
    check = commands.add_parser("add-check", help="record a result for a declared check plan")
    check.add_argument("--plan", required=True, type=_text)
    check.add_argument("--result", required=True, choices=RESULTS)
    check.add_argument("--target", required=True, type=_text)
    check.add_argument("--artifact", type=_text)
    check.add_argument("--attempt", type=_text)
    check.add_argument("--details", type=_text)
    check.add_argument("--issue", action="append", default=[], type=_text)
    check.add_argument("--evidence", action="append", default=[], type=_text)
    check.add_argument("--next-action", type=_text)
    coverage = commands.add_parser("add-coverage", help="record a result for a declared browser scenario")
    coverage.add_argument("--scenario", required=True, type=_text)
    coverage.add_argument("--phase", required=True, choices=COVERAGE_PHASES)
    coverage.add_argument("--result", required=True, choices=RESULTS)
    coverage.add_argument("--target", required=True, type=_text)
    coverage.add_argument("--artifact", type=_text)
    coverage.add_argument("--attempt", type=_text)
    coverage.add_argument("--details", type=_text)
    coverage.add_argument("--issue", action="append", default=[], type=_text)
    coverage.add_argument("--evidence", action="append", default=[], type=_text)
    coverage.add_argument("--next-action", type=_text)
    configure = commands.add_parser("configure-release", help="bind release target, artifact, and rollback policy")
    configure.add_argument("--target", required=True, type=_text)
    configure.add_argument("--intended-artifact", required=True, type=_text)
    configure.add_argument("--rollback-readiness", required=True, choices=ROLLBACK_READINESS)
    configure.add_argument("--rollback-plan", required=True, type=_text)
    configure.add_argument("--rollback-execution-authorized", required=True, type=_bool)
    configure.add_argument("--rollback-authorization-source", type=_text)
    configure.add_argument("--rollback-recovery-artifact", type=_text)
    configure.add_argument("--rollback-trigger", action="append", default=[], type=_text)
    configure.add_argument("--next-action", type=_text)
    attempt = commands.add_parser("declare-attempt", help="create a target/artifact-bound deployment attempt")
    attempt.add_argument("--next-action", type=_text)
    gate = commands.add_parser("release-gate", help="validate and record the active pre-deploy gate")
    gate.add_argument("--attempt", required=True, type=_text)
    gate.add_argument("--next-action", type=_text)
    deployment = commands.add_parser("record-deployment", help="record the reconciled deployment outcome")
    deployment.add_argument("--attempt", required=True, type=_text)
    deployment.add_argument("--result", required=True, choices=DEPLOY_RESULTS)
    deployment.add_argument("--observed-artifact", type=_text)
    deployment.add_argument("--details", type=_text)
    deployment.add_argument("--evidence", action="append", default=[], type=_text)
    deployment.add_argument("--next-action", type=_text)
    rollback = commands.add_parser("record-rollback", help="record an authorized rollback outcome")
    rollback.add_argument("--attempt", required=True, type=_text)
    rollback.add_argument("--result", required=True, choices=("rolled-back", "rollback-failed"))
    rollback.add_argument("--observed-artifact", type=_text)
    rollback.add_argument("--health-result", required=True, choices=("pass", "fail", "unknown"))
    rollback.add_argument("--trigger", type=_text)
    rollback.add_argument("--trigger-evidence", type=_text)
    rollback.add_argument("--details", required=True, type=_text)
    rollback.add_argument("--evidence", action="append", required=True, type=_text)
    rollback.add_argument("--next-action", type=_text)
    delivery_plan = commands.add_parser(
        "plan-delivery", help="record one separately authorized Git or report delivery action",
    )
    delivery_plan.add_argument("--action", required=True, choices=DELIVERY_ACTIONS)
    delivery_plan.add_argument("--target", required=True, type=_text)
    delivery_plan.add_argument("--authorization-source", required=True, type=_text)
    delivery_plan.add_argument("--idempotency-key", required=True, type=_text)
    delivery_plan.add_argument("--details", required=True, type=_text)
    delivery_plan.add_argument("--next-action", type=_text)
    delivery_result = commands.add_parser(
        "record-delivery", help="record the reconciled result of an authorized delivery action",
    )
    delivery_result.add_argument("--delivery", required=True, type=_text)
    delivery_result.add_argument(
        "--result", required=True, choices=("succeeded", "failed", "blocked", "unknown"),
    )
    delivery_result.add_argument("--external-id", type=_text)
    delivery_result.add_argument("--details", required=True, type=_text)
    delivery_result.add_argument("--evidence", action="append", required=True, type=_text)
    delivery_result.add_argument("--next-action", type=_text)
    advance = commands.add_parser("advance", help="advance through the mode-aware state machine")
    advance.add_argument("state", choices=STATES)
    advance.add_argument("--settlement", choices=("succeeded", "failed", "blocked"))
    advance.add_argument("--reason", type=_text)
    advance.add_argument("--next-action", type=_text)
    summary = commands.add_parser("summary", help="print a read-only resume summary")
    summary.add_argument("--format", choices=("markdown", "json"), default="markdown")
    validate = commands.add_parser("validate", help="validate schema and optional success gates")
    validate.add_argument("--strict", action="store_true")
    validate.add_argument("--format", choices=("text", "json"), default="text")
    return parser


def main() -> int:
    parser = _parser()
    args = parser.parse_args()
    try:
        run_dir = _run_dir(args.run_dir)
        at = _now(args.at)
        if args.subcommand == "init":
            print(_cmd_init(args, run_dir, at))
            return 0
        if args.subcommand == "summary":
            data = _read(run_dir)
            errors, _ = _safe_validate(data, strict=False)
            if errors:
                raise LedgerError("invalid ledger: " + "; ".join(errors), 5)
            payload = _summary(data)
            print(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) if args.format == "json" else _markdown(payload))
            return 0
        if args.subcommand == "validate":
            data = _read(run_dir)
            errors, warnings = _safe_validate(data, strict=args.strict)
            payload = {"valid": not errors, "strict": args.strict, "errors": errors, "warnings": warnings}
            if args.format == "json":
                print(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True))
            else:
                print("VALID" if not errors else "INVALID")
                for warning in warnings:
                    print(f"WARNING: {warning}")
                for error in errors:
                    print(f"ERROR: {error}")
            return 0 if not errors else 3
        handlers: dict[str, Callable[[argparse.Namespace, dict[str, Any], str], str]] = {
            "declare-target": _cmd_declare_target,
            "declare-scenario": _cmd_declare_scenario,
            "declare-check": _cmd_declare_check,
            "set-disposition": _cmd_set_disposition,
            "add": _cmd_add_issue,
            "add-evidence": _cmd_add_evidence,
            "update": _cmd_update,
            "add-check": _cmd_add_check,
            "add-coverage": _cmd_add_coverage,
            "configure-release": _cmd_configure_release,
            "declare-attempt": _cmd_declare_attempt,
            "release-gate": _cmd_release_gate,
            "record-deployment": _cmd_record_deployment,
            "record-rollback": _cmd_record_rollback,
            "plan-delivery": _cmd_plan_delivery,
            "record-delivery": _cmd_record_delivery,
            "advance": _cmd_advance,
        }
        handler = handlers[args.subcommand]
        print(_mutate(run_dir, at, lambda data: handler(args, data, at)))
        return 0
    except LedgerError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return exc.exit_code


if __name__ == "__main__":
    raise SystemExit(main())
