#!/usr/bin/env python3
"""Read-only OpenClaw package update rehearsal."""

from __future__ import annotations

import argparse
import base64
import concurrent.futures
import hashlib
import hmac
import json
import os
import platform
from pathlib import Path, PurePosixPath
import re
import shutil
import stat
import subprocess
import sys
import tarfile
import tempfile
import time
from datetime import datetime, timedelta, timezone
from typing import Any


EFFECT = "read_only_openclaw_update_rehearsal"
INPUT_SCHEMA = "openclaw.safe_update.input.v1"
CUSTOMIZATIONS_SCHEMA = "openclaw.safe_update.customizations.v1"
COVERAGE_SCHEMA = "openclaw.safe_update.coverage.v1"
CORE_CLOSURE_SCHEMA = "openclaw.safe_update.core_closure.v1"
CORE_CANDIDATE_LOCK_SCHEMA = "openclaw.safe_update.core_candidate_lock.v1"
INSTALLATION_CANDIDATE_LOCK_SCHEMA = "openclaw.safe_update.installation_candidate_lock.v1"
INSTALLATION_ATTESTATION_SCHEMA = "openclaw.safe_update.installation_attestation.v1"
INSTALLATION_OBSERVATION_SCHEMA = "openclaw.safe_update.installation_observation.v1"
CORE_CLOSURE_ANALYZER_VERSION = "1.0.0"
CORE_CLOSURE_POLICY_VERSION = "1"
INSTALLATION_COMPOSITION_POLICY_VERSION = "1"
INSTALLATION_CONTRACT_SCHEMA = "openclaw.safe_update.installation_contract.v1"
STATUS_SCHEMA = "openclaw.safe_update.status.v2"
DECISION_SCHEMA = "openclaw.safe_update.decision.v1"
LEGACY_VERDICT_SCHEMA = "openclaw.safe_update.verdict.v1"
STATUS_FIELDS = frozenset(
    {
        "schema",
        "generated_at",
        "effect",
        "runtime_effect",
        "external_effect",
        "external_write_effect",
        "production_apply_allowed",
        "operator_approval",
        "phase",
        "post_activation_e2e",
        "verdict",
        "reason",
        "candidate_roots",
        "evidence_bundle",
        "next_step",
        "decision_content",
        "decision_digest",
        "run_envelope",
        "compatibility_view",
    }
)
DECISION_FIELDS = frozenset(
    {
        "schema",
        "phase",
        "verdict",
        "reason_code",
        "evidence_status",
        "gate_decision",
        "candidate_roots",
        "production_apply_allowed",
        "operator_approval",
        "post_activation_e2e",
        "next_step_code",
    }
)
EVIDENCE_STATUS_FIELDS = frozenset(
    {
        "runtime_truth",
        "core_candidate_lock",
        "installation_candidate_lock",
        "installation_attestation",
        "conservative_gates",
        "synthetic_update",
        "customization_compatibility",
        "installation_coverage",
        "post_upgrade_e2e_plan",
    }
)
EVIDENCE_BUNDLE_FIELDS = frozenset({"path", "sha256"})
PACKAGE_RE = re.compile(r"^(?:@[a-z0-9][a-z0-9._-]*/)?[a-z0-9][a-z0-9._-]*$")
VERSION_RE = re.compile(r"^\d+\.\d+\.\d+(?:-[0-9A-Za-z.-]+)?(?:\+[0-9A-Za-z.-]+)?$")
MAX_TEXT_MEMBER_BYTES = 4 * 1024 * 1024
MAX_ARCHIVE_MEMBER_BYTES = 512 * 1024 * 1024
DIFF_MEMBER_LIMIT = 250
NPM_REGISTRY = "https://registry.npmjs.org"
RUNTIME_COMMANDS = frozenset({"node", "npm"})
NPM_ENVIRONMENT_KEYS = (
    "ALL_PROXY",
    "COMSPEC",
    "HOME",
    "HTTP_PROXY",
    "HTTPS_PROXY",
    "LANG",
    "LC_ALL",
    "NODE_EXTRA_CA_CERTS",
    "NO_PROXY",
    "PATH",
    "PATHEXT",
    "SSL_CERT_DIR",
    "SSL_CERT_FILE",
    "SYSTEMROOT",
    "TEMP",
    "TMP",
    "TMPDIR",
    "USERPROFILE",
    "all_proxy",
    "http_proxy",
    "https_proxy",
    "no_proxy",
)
NPM_ENVIRONMENT_OVERRIDES = frozenset(
    {"NPM_CONFIG_CPU", "NPM_CONFIG_LIBC", "NPM_CONFIG_OS"}
)
SUPPORTED_INSTALL_SHAPES = {"npm_global_linux"}
SURFACE_CATEGORIES = {
    "attachment",
    "channel",
    "mcp",
    "memory",
    "other",
    "persona",
    "plugin",
    "provider",
    "service",
    "voice",
}
BUSINESS_CRITICALITIES = {"critical", "important", "best_effort"}
EVIDENCE_POLICIES = {"always", "impact_triggered", "sampled"}
COMPONENT_ROLES = {"core", "compatibility", "addon", "personalization", "configuration"}
DEPENDENCY_KINDS = {"runtime", "configuration", "state", "contract"}
PACKAGE_METADATA_FIELDS = (
    "engines",
    "dependencies",
    "optionalDependencies",
    "peerDependencies",
    "scripts",
    "bin",
)
LIFECYCLE_SCRIPTS = {"preinstall", "install", "postinstall", "prepack", "prepare"}
ATTESTATION_CONTENT_KINDS = {
    "plugin_package",
    "sidecar",
    "addon",
    "external_asset",
}
ATTESTATION_IDENTITY_KINDS = {
    "configuration_identity",
    "personalization_contract",
}
SAFE_OBSERVATION_NAME_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._/-]*$")
SERVICE_POINTER_RE = re.compile(
    r"(?:--config(?:=|\s+)|OPENCLAW_CONFIG=)(?P<path>[^\s\"']+)"
)
ENVIRONMENT_FILE_RE = re.compile(r"^EnvironmentFile=-?(?P<path>[^\s\"']+)$")
SERVICE_POINTER_DIRECTIVES = (
    b"ExecStart=",
    b"ExecStartPre=",
    b"ExecReload=",
    b"ExecStop=",
    b"Environment=",
    b"EnvironmentFile=",
)
MAX_SERVICE_UNIT_BYTES = 64 * 1024
CONSERVATIVE_INPUTS_SCHEMA = "openclaw.safe_update.conservative_inputs.v1"
CONSERVATIVE_GATES_SCHEMA = "openclaw.safe_update.conservative_gates.v1"
IMPACT_SHADOW_SCHEMA = "openclaw.safe_update.impact_shadow.v1"
SHADOW_ID_PREFIX = "shadow:"
ANALYSIS_CACHE_SCHEMA = "openclaw.safe_update.analysis_cache.v1"
ANALYSIS_CACHE_ENTRY_SCHEMA = "openclaw.safe_update.analysis_cache_entry.v1"
ARCHIVE_EXECUTION_SCHEMA = "openclaw.safe_update.archive_execution.v1"
ANALYZER_VERSION = "openclaw-safe-update.py:v1.3"
DETERMINISTIC_POLICY_VERSION = "conservative-gates:v1"
CACHE_NAMESPACES = {"archive", "contract", "policy", "shadow"}
MAX_ARCHIVE_WORKERS = 8
VOLATILE_ANALYSIS_FIELDS = {
    "generated_at",
    "effect",
    "runtime_effect",
    "external_effect",
    "external_write_effect",
    "production_apply_allowed",
    "operator_approval",
}
GATE_HANDLING = {"baseline", "conservative", "blocked"}
GATE_EVIDENCE_IDS = frozenset(
    {
        "lifecycle-download-evidence",
        "state-migration-rehearsal",
        "rollback-evidence",
        "plugin-sdk-contract",
        "launcher-service-contract",
        "permissions-contract",
        "protocol-contract",
        "channel-crypto-contract",
        "environment-matched-rehearsal",
    }
)
KOVA_EVIDENCE_SCHEMA = "openclaw.safe_update.kova_evidence.v1"
KOVA_EVIDENCE_POLICY_SCHEMA = "openclaw.safe_update.kova_evidence_policy.v1"
KOVA_RECEIPT_SCHEMA = "kova.matrix.run.receipt.v1"
KOVA_REPORT_SCHEMA = "kova.report.v1"
KOVA_ARTIFACT_INDEX_SCHEMA = "kova.artifact.index.v1"
KOVA_TARGET_IDENTITY_SCHEMA = "kova.target.identity.v1"
KOVA_RECORD_STATUSES = {
    "PASS",
    "FAIL",
    "INCOMPLETE",
    "BLOCKED",
    "SKIPPED",
    "DRY-RUN",
}
KOVA_EXACT_IDENTITY_KINDS = {"npm_integrity"}
KOVA_MAX_JSON_BYTES = 16 * 1024 * 1024
KOVA_MAX_CHECKSUM_BYTES = 8 * 1024
KOVA_MAX_BUNDLE_BYTES = 256 * 1024 * 1024
KOVA_MAX_BUNDLE_ENTRIES = 10_000
KOVA_MAX_BUNDLE_DECLARED_BYTES = 512 * 1024 * 1024
KOVA_SAFE_ID_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._:@/+-]{0,255}$")
CONSERVATIVE_CONDITION_IDS = frozenset(
    {
        "candidate-closure-resolved",
        "installation-attestation-fresh-complete",
        "authority-input-lossless",
        "lifecycle-download-evidence",
        "state-migration-rehearsal",
        "rollback-evidence",
        "plugin-sdk-contract",
        "launcher-service-contract",
        "permissions-contract",
        "protocol-contract",
        "channel-crypto-contract",
        "environment-matched-rehearsal",
        "native-optional-dependency-known",
    }
)


class RehearsalError(RuntimeError):
    pass


def now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def safety_fields() -> dict[str, Any]:
    return {
        "effect": EFFECT,
        "runtime_effect": "none",
        "external_effect": "npm_registry_read_only",
        "external_write_effect": "none",
        "production_apply_allowed": False,
        "operator_approval": False,
    }


def canonical_json_bytes(value: Any) -> bytes:
    return json.dumps(
        value,
        ensure_ascii=True,
        separators=(",", ":"),
        sort_keys=True,
    ).encode("utf-8")


def canonical_digest(value: Any) -> str:
    return "sha256:" + hashlib.sha256(canonical_json_bytes(value)).hexdigest()


def deterministic_analysis_value(value: dict[str, Any]) -> dict[str, Any]:
    return {
        key: item
        for key, item in value.items()
        if key not in VOLATILE_ANALYSIS_FIELDS
    }


def secure_cache_namespace(
    cache_dir: Path,
    namespace: str,
) -> tuple[Path, bytes] | None:
    try:
        cache_dir.mkdir(parents=True, mode=0o700, exist_ok=True)
        root_stat = cache_dir.lstat()
        if (
            not stat.S_ISDIR(root_stat.st_mode)
            or cache_dir.is_symlink()
            or root_stat.st_uid != os.getuid()
            or stat.S_IMODE(root_stat.st_mode) & 0o077
        ):
            return None

        key_path = cache_dir / ".integrity-key"
        if not key_path.exists():
            try:
                descriptor = os.open(
                    key_path,
                    os.O_WRONLY | os.O_CREAT | os.O_EXCL,
                    0o600,
                )
            except FileExistsError:
                pass
            else:
                with os.fdopen(descriptor, "w", encoding="ascii") as handle:
                    handle.write(os.urandom(32).hex())
                    handle.flush()
                    os.fsync(handle.fileno())
        key_stat = key_path.lstat()
        if (
            not stat.S_ISREG(key_stat.st_mode)
            or key_path.is_symlink()
            or key_stat.st_uid != os.getuid()
            or stat.S_IMODE(key_stat.st_mode) & 0o077
        ):
            return None
        key = bytes.fromhex(key_path.read_text(encoding="ascii"))
        if len(key) != 32:
            return None

        namespace_dir = cache_dir / namespace
        namespace_dir.mkdir(mode=0o700, exist_ok=True)
        namespace_stat = namespace_dir.lstat()
        if (
            not stat.S_ISDIR(namespace_stat.st_mode)
            or namespace_dir.is_symlink()
            or namespace_stat.st_uid != os.getuid()
            or stat.S_IMODE(namespace_stat.st_mode) & 0o077
        ):
            return None
        return namespace_dir, key
    except (OSError, ValueError):
        return None


def cache_entry_mac(key: bytes, entry: dict[str, Any]) -> str:
    return hmac.new(key, canonical_json_bytes(entry), hashlib.sha256).hexdigest()


def cached_analysis(
    *,
    cache_dir: Path | None,
    namespace: str,
    key_material: Any,
    provenance: list[dict[str, str]],
    build: Any,
    validate: Any | None = None,
) -> Any:
    if namespace not in CACHE_NAMESPACES:
        raise RehearsalError(f"unsupported cache namespace: {namespace}")
    key = canonical_digest(
        {
            "namespace": namespace,
            "analyzer_version": ANALYZER_VERSION,
            "policy_version": DETERMINISTIC_POLICY_VERSION,
            "input": key_material,
        }
    )
    if cache_dir is not None:
        secure_namespace = secure_cache_namespace(cache_dir, namespace)
        if secure_namespace is None:
            provenance.append(
                {"namespace": namespace, "key": key, "result": "ignored"}
            )
            return build()
        namespace_dir, integrity_key = secure_namespace
        entry_path = namespace_dir / f"{key.removeprefix('sha256:')}.json"
        if entry_path.is_file():
            try:
                entry_stat = entry_path.lstat()
                if (
                    not stat.S_ISREG(entry_stat.st_mode)
                    or entry_path.is_symlink()
                    or entry_stat.st_uid != os.getuid()
                    or stat.S_IMODE(entry_stat.st_mode) & 0o077
                ):
                    raise RehearsalError("cache entry permissions are unsafe")
                entry = read_json(entry_path)
                if (
                    not isinstance(entry, dict)
                    or set(entry)
                    != {
                        "schema",
                        "namespace",
                        "key",
                        "analyzer_version",
                        "policy_version",
                        "payload",
                        "payload_digest",
                        "mac",
                    }
                    or entry.get("schema") != ANALYSIS_CACHE_ENTRY_SCHEMA
                    or entry.get("namespace") != namespace
                    or entry.get("key") != key
                    or entry.get("analyzer_version") != ANALYZER_VERSION
                    or entry.get("policy_version") != DETERMINISTIC_POLICY_VERSION
                    or entry.get("payload_digest")
                    != canonical_digest(entry.get("payload"))
                    or not hmac.compare_digest(
                        str(entry.get("mac")),
                        cache_entry_mac(
                            integrity_key,
                            {
                                entry_key: entry_value
                                for entry_key, entry_value in entry.items()
                                if entry_key != "mac"
                            },
                        ),
                    )
                ):
                    raise RehearsalError("cache entry validation failed")
                if validate is not None and not validate(entry["payload"]):
                    raise RehearsalError("cache payload validation failed")
                provenance.append(
                    {"namespace": namespace, "key": key, "result": "hit"}
                )
                return entry["payload"]
            except RehearsalError:
                provenance.append(
                    {"namespace": namespace, "key": key, "result": "ignored"}
                )
        payload = build()
        if validate is not None and not validate(payload):
            raise RehearsalError("analysis payload validation failed")
        entry = {
            "schema": ANALYSIS_CACHE_ENTRY_SCHEMA,
            "namespace": namespace,
            "key": key,
            "analyzer_version": ANALYZER_VERSION,
            "policy_version": DETERMINISTIC_POLICY_VERSION,
            "payload": payload,
            "payload_digest": canonical_digest(payload),
        }
        entry["mac"] = cache_entry_mac(integrity_key, entry)
        write_json(entry_path, entry)
        entry_path.chmod(0o600)
        provenance.append(
            {"namespace": namespace, "key": key, "result": "miss"}
        )
        return payload
    provenance.append({"namespace": namespace, "key": key, "result": "disabled"})
    return build()


def build_rehearsal_input(
    *,
    candidate_roots: dict[str, str | None],
    installation_contract: dict[str, Any],
    installation_attestation: dict[str, Any],
    conservative_inputs: dict[str, Any],
    authoritative_analysis: dict[str, Any],
    options: dict[str, Any],
) -> dict[str, Any]:
    return {
        "schema": "openclaw.safe_update.rehearsal_input.v1",
        "candidate_roots": candidate_roots,
        "installation_contract_digest": (
            canonical_digest(installation_contract)
            if installation_contract
            else None
        ),
        "installation_attestation_digest": canonical_digest(
            installation_attestation
        ),
        "conservative_inputs": conservative_inputs,
        "authoritative_analysis_digest": canonical_digest(
            authoritative_analysis
        ),
        "policy_version": DETERMINISTIC_POLICY_VERSION,
        "analyzer_version": ANALYZER_VERSION,
        "options": options,
    }


def legacy_verdict_payload(status: dict[str, Any]) -> dict[str, Any]:
    return {
        "schema": LEGACY_VERDICT_SCHEMA,
        "generated_at": status["generated_at"],
        **safety_fields(),
        "verdict": status["verdict"],
        "reason": status["reason"],
        "evidence_bundle": status["evidence_bundle"],
        "next_step": status["next_step"],
    }


def build_status(
    *,
    generated_at: str,
    verdict: str,
    reason: str,
    reason_code: str,
    evidence_status: dict[str, str],
    gate_decision: dict[str, Any],
    candidate_roots: dict[str, str | None],
    evidence_bundle: dict[str, str],
    next_step: str,
    next_step_code: str,
) -> dict[str, Any]:
    decision_content = {
        "schema": DECISION_SCHEMA,
        "phase": "preflight",
        "verdict": verdict,
        "reason_code": reason_code,
        "evidence_status": evidence_status,
        "gate_decision": gate_decision,
        "candidate_roots": candidate_roots,
        "production_apply_allowed": False,
        "operator_approval": False,
        "post_activation_e2e": "not_run",
        "next_step_code": next_step_code,
    }
    status = {
        "schema": STATUS_SCHEMA,
        "generated_at": generated_at,
        **safety_fields(),
        "phase": "preflight",
        "post_activation_e2e": "not_run",
        "verdict": verdict,
        "reason": reason,
        "candidate_roots": candidate_roots,
        "evidence_bundle": evidence_bundle,
        "next_step": next_step,
        "decision_content": decision_content,
        "decision_digest": canonical_digest(decision_content),
        "run_envelope": {
            "generated_at": generated_at,
            "evidence_bundle": evidence_bundle,
        },
    }
    status["compatibility_view"] = {
        "schema": "openclaw.safe_update.compatibility_view.v1",
        "authoritative": False,
        "payload": legacy_verdict_payload(status),
    }
    return status


def parse_status(value: Any) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise RehearsalError("status must be a JSON object")
    if value.get("schema") != STATUS_SCHEMA:
        raise RehearsalError(f"status schema must be {STATUS_SCHEMA}")
    if set(value) != STATUS_FIELDS:
        raise RehearsalError("status contains unknown or missing fields")

    hard_invariants = {
        "effect": EFFECT,
        "runtime_effect": "none",
        "external_effect": "npm_registry_read_only",
        "external_write_effect": "none",
        "production_apply_allowed": False,
        "operator_approval": False,
        "phase": "preflight",
        "post_activation_e2e": "not_run",
    }
    for field, expected in hard_invariants.items():
        if value.get(field) != expected:
            raise RehearsalError(f"status invariant {field} must be {expected!r}")

    if not isinstance(value.get("generated_at"), str) or not value["generated_at"]:
        raise RehearsalError("status generated_at must be a non-empty string")
    if value.get("verdict") not in {"blocked", "ready_for_operator_plan"}:
        raise RehearsalError("status verdict is invalid")
    if not isinstance(value.get("reason"), str) or not value["reason"]:
        raise RehearsalError("status reason must be a non-empty string")
    if not isinstance(value.get("next_step"), str) or not value["next_step"]:
        raise RehearsalError("status next_step must be a non-empty string")
    candidate_roots = value.get("candidate_roots")
    if (
        not isinstance(candidate_roots, dict)
        or set(candidate_roots) != {"current", "target"}
        or any(
            root is not None
            and not re.fullmatch(r"sha256:[0-9a-f]{64}", str(root))
            for root in candidate_roots.values()
        )
    ):
        raise RehearsalError("status candidate_roots is invalid")
    bundle = value.get("evidence_bundle")
    if (
        not isinstance(bundle, dict)
        or set(bundle) != EVIDENCE_BUNDLE_FIELDS
        or not isinstance(bundle.get("path"), str)
        or not bundle["path"]
        or not re.fullmatch(r"[0-9a-f]{64}", str(bundle.get("sha256", "")))
    ):
        raise RehearsalError("status evidence_bundle is invalid")
    decision = value.get("decision_content")
    if not isinstance(decision, dict) or decision.get("schema") != DECISION_SCHEMA:
        raise RehearsalError(f"decision_content schema must be {DECISION_SCHEMA}")
    if set(decision) != DECISION_FIELDS:
        raise RehearsalError("decision_content contains unknown or missing fields")
    if value.get("decision_digest") != canonical_digest(decision):
        raise RehearsalError("decision_digest does not match decision_content")
    for field in (
        "phase",
        "verdict",
        "candidate_roots",
        "production_apply_allowed",
        "operator_approval",
        "post_activation_e2e",
    ):
        if decision.get(field) != value.get(field):
            raise RehearsalError(f"decision_content {field} does not match status")
    if not isinstance(decision.get("evidence_status"), dict):
        raise RehearsalError("decision_content evidence_status must be an object")
    if set(decision["evidence_status"]) != EVIDENCE_STATUS_FIELDS:
        raise RehearsalError(
            "decision_content evidence_status contains unknown or missing fields"
        )
    evidence_values = set(decision["evidence_status"].values())
    if not evidence_values or not evidence_values <= {"success", "failed"}:
        raise RehearsalError("decision_content evidence_status is invalid")
    gate_decision = decision.get("gate_decision")
    if (
        not isinstance(gate_decision, dict)
        or set(gate_decision)
        != {"status", "handling", "required_gates", "decision_digest"}
        or gate_decision.get("status") not in {"success", "failed"}
        or gate_decision.get("handling") not in GATE_HANDLING
        or not isinstance(gate_decision.get("required_gates"), list)
        or gate_decision["required_gates"] != sorted(gate_decision["required_gates"])
        or any(gate not in GATE_EVIDENCE_IDS for gate in gate_decision["required_gates"])
        or not re.fullmatch(
            r"sha256:[0-9a-f]{64}",
            str(gate_decision.get("decision_digest", "")),
        )
    ):
        raise RehearsalError("decision_content gate_decision is invalid")
    if decision["evidence_status"]["conservative_gates"] != gate_decision["status"]:
        raise RehearsalError(
            "decision_content gate_decision does not match conservative gate evidence"
        )
    expected_reason_code = (
        "required_evidence_failed"
        if value["verdict"] == "blocked"
        else "baseline_rehearsal_passed"
    )
    expected_next_step_code = (
        "repair_and_rerun"
        if value["verdict"] == "blocked"
        else "prepare_operator_plan"
    )
    if decision.get("reason_code") != expected_reason_code:
        raise RehearsalError("decision_content reason_code does not match verdict")
    if decision.get("next_step_code") != expected_next_step_code:
        raise RehearsalError("decision_content next_step_code does not match verdict")
    if value["verdict"] == "blocked" and "failed" not in evidence_values:
        raise RehearsalError("blocked status must contain failed evidence")
    if value["verdict"] == "ready_for_operator_plan" and evidence_values != {"success"}:
        raise RehearsalError("ready status requires all evidence to succeed")
    if value["verdict"] == "ready_for_operator_plan" and any(
        root is None for root in candidate_roots.values()
    ):
        raise RehearsalError("ready status requires both candidate roots")

    envelope = value.get("run_envelope")
    if not isinstance(envelope, dict):
        raise RehearsalError("run_envelope must be an object")
    if set(envelope) != {"generated_at", "evidence_bundle"}:
        raise RehearsalError("run_envelope contains unknown or missing fields")
    if envelope.get("generated_at") != value.get("generated_at"):
        raise RehearsalError("run_envelope generated_at does not match status")
    if envelope.get("evidence_bundle") != value.get("evidence_bundle"):
        raise RehearsalError("run_envelope evidence_bundle does not match status")

    compatibility = value.get("compatibility_view")
    if not isinstance(compatibility, dict):
        raise RehearsalError("compatibility_view must be an object")
    if set(compatibility) != {"schema", "authoritative", "payload"}:
        raise RehearsalError("compatibility_view contains unknown or missing fields")
    if compatibility.get("schema") != "openclaw.safe_update.compatibility_view.v1":
        raise RehearsalError("compatibility_view schema is invalid")
    if compatibility.get("authoritative") is not False:
        raise RehearsalError("compatibility_view must be non-authoritative")
    if compatibility.get("payload") != legacy_verdict_payload(value):
        raise RehearsalError("compatibility_view payload does not match status")
    return value


def write_status(path: Path, value: dict[str, Any]) -> None:
    write_json(path, parse_status(value))


def read_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise RehearsalError(f"cannot read JSON {path}: {exc}") from exc


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = json.dumps(value, ensure_ascii=True, indent=2, sort_keys=True) + "\n"
    write_text(path, payload)


def write_text(path: Path, value: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, temporary = tempfile.mkstemp(prefix=f".{path.name}.", dir=path.parent)
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as handle:
            handle.write(value)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary, path)
    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)


def resolve_runtime_command(command: str) -> str:
    if command not in RUNTIME_COMMANDS:
        raise RehearsalError(f"unsupported runtime command: {command}")
    resolved = shutil.which(command)
    if resolved is None:
        raise RehearsalError(f"{command} is not available")
    return resolved


def detect_node_version() -> str:
    try:
        completed = subprocess.run(
            [resolve_runtime_command("node"), "--version"],
            check=True,
            capture_output=True,
            text=True,
            timeout=10,
        )
        candidate = completed.stdout.strip().removeprefix("v")
        if VERSION_RE.fullmatch(candidate):
            return candidate
    except (
        FileNotFoundError,
        RehearsalError,
        subprocess.CalledProcessError,
        subprocess.TimeoutExpired,
    ):
        pass
    return "unknown"


def inventory(args: argparse.Namespace) -> int:
    package_root = args.package_root.resolve()
    package_json_path = package_root / "package.json"
    package_json = read_json(package_json_path)
    if not isinstance(package_json, dict):
        raise RehearsalError("installed package.json must be an object")
    if package_json.get("name") != args.package_name:
        raise RehearsalError(f"installed package is not {args.package_name}")
    version = package_json.get("version")
    if not isinstance(version, str) or not VERSION_RE.fullmatch(version):
        raise RehearsalError("installed package version is not exact semver")

    node_version = detect_node_version()

    output = args.output_dir.resolve()
    output.mkdir(parents=True, exist_ok=True)
    common = {"generated_at": now_iso(), **safety_fields()}
    inventory_document = {
        "schema": "openclaw.safe_update.inventory.v1",
        **common,
        "status": "success",
        "package_name": args.package_name,
        "installed_version": version,
        "package_root_name": package_root.name,
        "host": {
            "platform": platform.system().lower(),
            "machine": platform.machine(),
            "node_version": node_version,
        },
        "declared_node_engine": (package_json.get("engines") or {}).get("node")
        if isinstance(package_json.get("engines"), dict)
        else None,
        "note": "No OpenClaw configuration, credentials, conversations, or service state were read.",
    }
    coverage_draft = {
        "schema": COVERAGE_SCHEMA,
        "install_shape": "npm_global_linux",
        "runtime": {
            "node_version": node_version,
            "os": platform.system().lower(),
            "arch": platform.machine().lower(),
            "libc": (platform.libc_ver()[0] or "unknown").lower(),
        },
        "surfaces": [],
        "draft": True,
        "instructions": (
            "Add every required channel, plugin, MCP, memory, provider, service, persona, "
            "attachment, and voice surface before simulation."
        ),
    }
    packages_draft = [
        {"name": args.package_name, "current": version, "target": "REPLACE_WITH_EXACT_VERSION"}
    ]
    write_json(output / "inventory.json", inventory_document)
    write_json(output / "coverage.draft.json", coverage_draft)
    write_json(output / "packages.draft.json", packages_draft)
    print(output / "inventory.json")
    return 0


def digest_file(path: Path, algorithm: str = "sha256") -> str:
    digest = hashlib.new(algorithm)
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def integrity_for(path: Path) -> str:
    digest = hashlib.sha512()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return "sha512-" + base64.b64encode(digest.digest()).decode("ascii")


def parse_packages(raw: str, current_version: str, target_version: str) -> list[dict[str, str]]:
    try:
        value = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise RehearsalError(f"packages JSON is invalid: {exc}") from exc
    if not isinstance(value, list) or not value:
        raise RehearsalError("packages JSON must be a non-empty list")

    packages: list[dict[str, str]] = []
    seen: set[str] = set()
    for entry in value:
        if isinstance(entry, str):
            package = {"name": entry, "current": current_version, "target": target_version}
        elif isinstance(entry, dict):
            package = {
                "name": entry.get("name"),
                "current": entry.get("current", current_version),
                "target": entry.get("target", target_version),
            }
        else:
            raise RehearsalError("each package must be a string or object")
        if not all(isinstance(package[key], str) and package[key] for key in package):
            raise RehearsalError("package name and versions must be non-empty strings")
        if not PACKAGE_RE.fullmatch(package["name"]):
            raise RehearsalError(f"invalid npm package name: {package['name']!r}")
        if not VERSION_RE.fullmatch(package["current"]) or not VERSION_RE.fullmatch(package["target"]):
            raise RehearsalError(f"package versions must be exact semver values: {package['name']}")
        if package["name"] in seen:
            raise RehearsalError(f"duplicate package: {package['name']}")
        seen.add(package["name"])
        packages.append(package)
    return packages


def run_npm_json(
    arguments: list[str],
    cache_dir: Path,
    working_dir: Path | None = None,
    environment_overrides: dict[str, str] | None = None,
) -> Any:
    overrides = environment_overrides or {}
    unsupported = sorted(set(overrides) - NPM_ENVIRONMENT_OVERRIDES)
    if unsupported:
        raise RehearsalError(
            "unsupported npm environment override: " + ", ".join(unsupported)
        )
    try:
        cache_dir.mkdir(parents=True, exist_ok=True)
    except OSError as exc:
        raise RehearsalError("cannot create isolated npm cache") from exc
    execution_dir = working_dir or cache_dir
    project_config = execution_dir / ".npmrc"
    try:
        if project_config.exists() and project_config.read_bytes():
            raise RehearsalError(
                "npm working directory contains a non-empty project .npmrc"
            )
        project_config.touch(exist_ok=True)
    except OSError as exc:
        raise RehearsalError("cannot isolate npm project configuration") from exc
    user_config = cache_dir / "user.npmrc"
    global_config = cache_dir / "global.npmrc"
    user_config.touch(exist_ok=True)
    global_config.touch(exist_ok=True)
    environment = {
        key: os.environ[key] for key in NPM_ENVIRONMENT_KEYS if key in os.environ
    }
    environment.setdefault("PATH", os.defpath)
    environment.update(
        {
            "NPM_CONFIG_IGNORE_SCRIPTS": "true",
            "NPM_CONFIG_AUDIT": "false",
            "NPM_CONFIG_FUND": "false",
            "NPM_CONFIG_UPDATE_NOTIFIER": "false",
            "NPM_CONFIG_CACHE": str(cache_dir),
            "NPM_CONFIG_LOGS_DIR": str(cache_dir / "_logs"),
            "NPM_CONFIG_REGISTRY": NPM_REGISTRY,
            "NPM_CONFIG_USERCONFIG": str(user_config),
            "NPM_CONFIG_GLOBALCONFIG": str(global_config),
            "NPM_CONFIG_MIN_RELEASE_AGE": "0",
            **overrides,
        }
    )
    try:
        completed = subprocess.run(
            [resolve_runtime_command("npm"), *arguments],
            cwd=execution_dir,
            check=True,
            capture_output=True,
            text=True,
            env=environment,
        )
    except FileNotFoundError as exc:
        raise RehearsalError("npm is not installed") from exc
    except subprocess.CalledProcessError as exc:
        lines = (exc.stderr or exc.stdout or "npm command failed").strip().splitlines()
        useful = [line for line in lines if "complete log" not in line.lower()]
        detail = " | ".join(useful[-3:] or lines[-1:])
        raise RehearsalError(f"npm command failed: {detail}") from exc
    try:
        return json.loads(completed.stdout)
    except json.JSONDecodeError as exc:
        raise RehearsalError("npm returned non-JSON output") from exc


def command_version(command: str) -> str:
    try:
        completed = subprocess.run(
            [resolve_runtime_command(command), "--version"],
            check=True,
            capture_output=True,
            text=True,
            timeout=10,
        )
    except (
        FileNotFoundError,
        subprocess.CalledProcessError,
        subprocess.TimeoutExpired,
    ) as exc:
        raise RehearsalError(f"{command} is not available") from exc
    value = completed.stdout.strip().removeprefix("v")
    if semver_tuple(value) is None:
        raise RehearsalError(f"{command} returned a non-exact version")
    return value


def package_name_from_lock_path(path: str) -> str:
    marker = "node_modules/"
    if marker not in path:
        raise RehearsalError(f"unsupported lockfile package path: {path!r}")
    suffix = path.rsplit(marker, 1)[1]
    parts = suffix.split("/")
    name = "/".join(parts[:2]) if suffix.startswith("@") else parts[0]
    if not PACKAGE_RE.fullmatch(name):
        raise RehearsalError(f"invalid package name in lockfile path: {path!r}")
    return name


def selector_matches(values: Any, actual: str) -> bool:
    if values is None:
        return True
    if not isinstance(values, list) or any(not isinstance(item, str) or not item for item in values):
        raise RehearsalError("package platform selector must be a list of strings")
    positives = {item for item in values if not item.startswith("!")}
    negatives = {item[1:] for item in values if item.startswith("!")}
    return actual not in negatives and (not positives or actual in positives)


def normalized_string_map(value: Any, field: str) -> dict[str, str]:
    if value is None:
        return {}
    if not isinstance(value, dict) or any(
        not isinstance(key, str) or not isinstance(item, str)
        for key, item in value.items()
    ):
        raise RehearsalError(f"lockfile {field} must be a string map")
    return dict(sorted(value.items()))


def build_core_closure(
    lockfile: Any,
    package: str,
    version: str,
    environment: dict[str, str],
) -> dict[str, Any]:
    if not isinstance(lockfile, dict) or lockfile.get("lockfileVersion") not in {2, 3}:
        raise RehearsalError("npm lockfileVersion must be 2 or 3")
    lock_packages = lockfile.get("packages")
    if not isinstance(lock_packages, dict) or not lock_packages:
        raise RehearsalError("npm lockfile packages are missing")
    if set(environment) != {"node_version", "npm_version", "os", "arch", "libc"}:
        raise RehearsalError("core closure environment is incomplete")
    if any(not isinstance(value, str) or not value for value in environment.values()):
        raise RehearsalError("core closure environment values must be non-empty strings")
    if semver_tuple(environment["node_version"]) is None or semver_tuple(environment["npm_version"]) is None:
        raise RehearsalError("core closure tool versions must be exact")

    packages: list[dict[str, Any]] = []
    for path, value in lock_packages.items():
        if path == "":
            continue
        if not isinstance(path, str) or not isinstance(value, dict):
            raise RehearsalError("npm lockfile package entry is invalid")
        if "link" in value:
            raise RehearsalError(f"mutable link dependency is unsupported: {path}")
        resolved = value.get("resolved")
        integrity = value.get("integrity")
        package_version = value.get("version")
        if (
            not isinstance(package_version, str)
            or not VERSION_RE.fullmatch(package_version)
            or not isinstance(resolved, str)
            or not resolved.startswith(f"{NPM_REGISTRY}/")
            or not isinstance(integrity, str)
            or not integrity.startswith(("sha512-", "sha1-"))
        ):
            raise RehearsalError(f"package closure lacks immutable registry identity: {path}")
        selectors = {
            "os": value.get("os"),
            "cpu": value.get("cpu"),
            "libc": value.get("libc"),
        }
        selected = (
            selector_matches(selectors["os"], environment["os"])
            and selector_matches(selectors["cpu"], environment["arch"])
            and selector_matches(selectors["libc"], environment["libc"])
        )
        package_name = value.get("name") or package_name_from_lock_path(path)
        if not isinstance(package_name, str) or not PACKAGE_RE.fullmatch(package_name):
            raise RehearsalError(f"invalid package name in lockfile entry: {path!r}")
        packages.append(
            {
                "path": path,
                "name": package_name,
                "version": package_version,
                "resolved": resolved,
                "integrity": integrity,
                "dependencies": normalized_string_map(value.get("dependencies"), "dependencies"),
                "optional_dependencies": normalized_string_map(
                    value.get("optionalDependencies"), "optionalDependencies"
                ),
                "peer_dependencies": normalized_string_map(
                    value.get("peerDependencies"), "peerDependencies"
                ),
                "flags": {
                    "dev": value.get("dev") is True,
                    "optional": value.get("optional") is True,
                    "peer": value.get("peer") is True,
                    "in_bundle": value.get("inBundle") is True,
                    "has_install_script": value.get("hasInstallScript") is True,
                },
                "selectors": {
                    key: sorted(item) if isinstance(item, list) else []
                    for key, item in selectors.items()
                },
                "selected_for_platform": selected,
            }
        )
    packages.sort(key=lambda item: (item["path"], item["name"], item["version"]))
    if not any(item["name"] == package and item["version"] == version for item in packages):
        raise RehearsalError(f"resolved closure does not contain {package}@{version}")
    content = {
        "schema": CORE_CLOSURE_SCHEMA,
        "root_package": {"name": package, "version": version},
        "environment": dict(sorted(environment.items())),
        "resolver": {
            "analyzer_version": CORE_CLOSURE_ANALYZER_VERSION,
            "policy_version": CORE_CLOSURE_POLICY_VERSION,
            "registry": NPM_REGISTRY,
            "lockfile_version": lockfile["lockfileVersion"],
            "package_lock_only": True,
            "ignore_scripts": True,
            "include_optional": True,
            "min_release_age_days": 0,
            "isolated_npm_config": True,
        },
        "packages": packages,
    }
    return {**content, "root": canonical_digest(content)}


def resolve_core_closure(
    package: str,
    version: str,
    cache_dir: Path,
    environment: dict[str, str],
) -> dict[str, Any]:
    with tempfile.TemporaryDirectory(prefix="openclaw-safe-update-lock-") as temporary:
        root = Path(temporary)
        write_json(
            root / "package.json",
            {
                "name": "openclaw-safe-update-candidate",
                "version": "0.0.0",
                "private": True,
                "dependencies": {package: version},
            },
        )
        run_npm_json(
            [
                "install",
                "--json",
                "--package-lock-only",
                "--ignore-scripts",
                "--include=optional",
            ],
            cache_dir,
            root,
            {
                "NPM_CONFIG_OS": environment["os"],
                "NPM_CONFIG_CPU": environment["arch"],
                "NPM_CONFIG_LIBC": environment["libc"],
            },
        )
        return build_core_closure(
            read_json(root / "package-lock.json"),
            package,
            version,
            environment,
        )


def registry_metadata(package: str, version: str, cache_dir: Path) -> dict[str, Any]:
    value = run_npm_json(["view", f"{package}@{version}", "--json"], cache_dir)
    if isinstance(value, list):
        matches = [
            item
            for item in value
            if isinstance(item, dict)
            and item.get("name") == package
            and item.get("version") == version
        ]
        if len(matches) != 1:
            raise RehearsalError(f"registry metadata mismatch for {package}@{version}")
        value = matches[0]
    if not isinstance(value, dict) or value.get("name") != package or value.get("version") != version:
        raise RehearsalError(f"registry metadata mismatch for {package}@{version}")
    dist = value.get("dist")
    if not isinstance(dist, dict) or not isinstance(dist.get("integrity"), str) or not isinstance(dist.get("shasum"), str):
        raise RehearsalError(f"registry metadata lacks integrity for {package}@{version}")
    return {
        "name": package,
        "version": version,
        "integrity": dist["integrity"],
        "shasum": dist["shasum"],
    }


def pack_archive(package: str, version: str, destination: Path, cache_dir: Path) -> str:
    destination.mkdir(parents=True, exist_ok=True)
    value = run_npm_json(
        ["pack", f"{package}@{version}", "--json", "--pack-destination", str(destination)],
        cache_dir,
    )
    if isinstance(value, dict):
        value = [
            item
            for item in value.values()
            if isinstance(item, dict)
            and item.get("name") == package
            and item.get("version") == version
        ]
    if not isinstance(value, list) or len(value) != 1 or not isinstance(value[0], dict):
        raise RehearsalError(f"unexpected npm pack result for {package}@{version}")
    filename = value[0].get("filename")
    if not isinstance(filename, str) or not (destination / filename).is_file():
        raise RehearsalError(f"npm pack did not create an archive for {package}@{version}")
    return filename


def fetch(args: argparse.Namespace) -> int:
    output = args.output_dir.resolve()
    if output.exists() and any(output.iterdir()):
        raise RehearsalError(f"output directory must be empty: {output}")
    output.mkdir(parents=True, exist_ok=True)
    packages = parse_packages(args.packages_json, args.current_version, args.target_version)
    core_packages = [item for item in packages if item["name"] == "openclaw"]
    if len(core_packages) != 1:
        raise RehearsalError("packages must contain exactly one openclaw core package")
    environment = {
        "node_version": command_version("node"),
        "npm_version": command_version("npm"),
        "os": args.platform_os,
        "arch": args.platform_arch,
        "libc": args.platform_libc,
    }
    records: list[dict[str, Any]] = []
    core_candidate: dict[str, Any] = {"package": "openclaw"}
    with tempfile.TemporaryDirectory(prefix="openclaw-safe-update-npm-") as cache:
        cache_dir = Path(cache)
        for package in packages:
            record: dict[str, Any] = {"name": package["name"]}
            for lane in ("current", "target"):
                version = package[lane]
                metadata = registry_metadata(package["name"], version, cache_dir)
                metadata["archive"] = pack_archive(
                    package["name"], version, output / lane, cache_dir
                )
                record[lane] = metadata
            records.append(record)
        core_package = core_packages[0]
        for lane in ("current", "target"):
            core_candidate[lane] = resolve_core_closure(
                "openclaw",
                core_package[lane],
                cache_dir,
                environment,
            )

    document = {
        "schema": INPUT_SCHEMA,
        "generated_at": now_iso(),
        **safety_fields(),
        "current_version": args.current_version,
        "target_version": args.target_version,
        "packages": records,
        "core_candidate": core_candidate,
    }
    write_json(output / "input-metadata.json", document)
    print(output / "input-metadata.json")
    return 0


def validate_core_closure(value: Any, package: str, version: str) -> dict[str, Any]:
    if not isinstance(value, dict) or value.get("schema") != CORE_CLOSURE_SCHEMA:
        raise RehearsalError(f"core closure schema must be {CORE_CLOSURE_SCHEMA}")
    content = {key: item for key, item in value.items() if key != "root"}
    if set(content) != {"schema", "root_package", "environment", "resolver", "packages"}:
        raise RehearsalError("core closure contains unknown or missing fields")
    if value.get("root") != canonical_digest(content):
        raise RehearsalError("core closure root does not match canonical content")
    if content.get("root_package") != {"name": package, "version": version}:
        raise RehearsalError(f"core closure root package mismatch for {package}@{version}")
    resolver = content.get("resolver")
    if not isinstance(resolver, dict) or resolver != {
        "analyzer_version": CORE_CLOSURE_ANALYZER_VERSION,
        "policy_version": CORE_CLOSURE_POLICY_VERSION,
        "registry": NPM_REGISTRY,
        "lockfile_version": resolver.get("lockfile_version") if isinstance(resolver, dict) else None,
        "package_lock_only": True,
        "ignore_scripts": True,
        "include_optional": True,
        "min_release_age_days": 0,
        "isolated_npm_config": True,
    }:
        raise RehearsalError("core closure resolver invariants are invalid")
    if resolver["lockfile_version"] not in {2, 3}:
        raise RehearsalError("core closure lockfile version is unsupported")
    environment = content.get("environment")
    if not isinstance(environment, dict) or set(environment) != {
        "node_version",
        "npm_version",
        "os",
        "arch",
        "libc",
    }:
        raise RehearsalError("core closure environment is invalid")
    if semver_tuple(str(environment.get("node_version", ""))) is None or semver_tuple(
        str(environment.get("npm_version", ""))
    ) is None:
        raise RehearsalError("core closure tool versions are invalid")
    packages = content.get("packages")
    if not isinstance(packages, list) or not packages:
        raise RehearsalError("core closure packages are missing")
    if packages != sorted(
        packages,
        key=lambda item: (item.get("path"), item.get("name"), item.get("version"))
        if isinstance(item, dict)
        else ("", "", ""),
    ):
        raise RehearsalError("core closure packages are not canonical")
    for item in packages:
        if (
            not isinstance(item, dict)
            or set(item)
            != {
                "path",
                "name",
                "version",
                "resolved",
                "integrity",
                "dependencies",
                "optional_dependencies",
                "peer_dependencies",
                "flags",
                "selectors",
                "selected_for_platform",
            }
            or not isinstance(item.get("name"), str)
            or not isinstance(item.get("path"), str)
            or not isinstance(item.get("version"), str)
            or not VERSION_RE.fullmatch(item["version"])
            or not isinstance(item.get("resolved"), str)
            or not item["resolved"].startswith(f"{NPM_REGISTRY}/")
            or not isinstance(item.get("integrity"), str)
            or not item["integrity"].startswith(("sha512-", "sha1-"))
            or not isinstance(item.get("selected_for_platform"), bool)
        ):
            raise RehearsalError("core closure package entry is invalid")
        for field in ("dependencies", "optional_dependencies", "peer_dependencies"):
            if normalized_string_map(item.get(field), field) != item.get(field):
                raise RehearsalError(f"core closure package {field} is not canonical")
        flags = item.get("flags")
        if (
            not isinstance(flags, dict)
            or set(flags)
            != {"dev", "optional", "peer", "in_bundle", "has_install_script"}
            or any(not isinstance(flag, bool) for flag in flags.values())
        ):
            raise RehearsalError("core closure package flags are invalid")
        selectors = item.get("selectors")
        if (
            not isinstance(selectors, dict)
            or set(selectors) != {"os", "cpu", "libc"}
            or any(
                not isinstance(values, list)
                or values != sorted(values)
                or any(not isinstance(selector, str) or not selector for selector in values)
                for values in selectors.values()
            )
        ):
            raise RehearsalError("core closure package selectors are invalid")
    return value


def compare_core_closures(current: dict[str, Any], target: dict[str, Any]) -> list[dict[str, Any]]:
    current_packages = {
        (item["path"], item["name"]): item for item in current["packages"]
    }
    target_packages = {
        (item["path"], item["name"]): item for item in target["packages"]
    }
    changes: list[dict[str, Any]] = []
    for key in sorted(set(current_packages) | set(target_packages)):
        before = current_packages.get(key)
        after = target_packages.get(key)
        if before == after:
            continue
        changes.append(
            {
                "path": key[0],
                "name": key[1],
                "change": "added" if before is None else "removed" if after is None else "changed",
                "current_version": before.get("version") if before else None,
                "target_version": after.get("version") if after else None,
                "current_selected": before.get("selected_for_platform") if before else None,
                "target_selected": after.get("selected_for_platform") if after else None,
                "current_flags": before.get("flags") if before else None,
                "target_flags": after.get("flags") if after else None,
                "current_selectors": before.get("selectors") if before else None,
                "target_selectors": after.get("selectors") if after else None,
            }
        )
    return changes


def build_core_candidate_lock(
    metadata: Any,
    runtime_environment: dict[str, Any],
    common: dict[str, Any],
) -> tuple[dict[str, Any], str]:
    errors: list[str] = []
    current: dict[str, Any] = {}
    target: dict[str, Any] = {}
    try:
        if not isinstance(metadata, dict):
            raise RehearsalError("input metadata is unavailable")
        candidate = metadata.get("core_candidate")
        if not isinstance(candidate, dict) or candidate.get("package") != "openclaw":
            raise RehearsalError("input metadata lacks the openclaw core candidate closure")
        current = validate_core_closure(
            candidate.get("current"),
            "openclaw",
            str(metadata.get("current_version", "")),
        )
        target = validate_core_closure(
            candidate.get("target"),
            "openclaw",
            str(metadata.get("target_version", "")),
        )
        if current["environment"] != target["environment"]:
            raise RehearsalError("current and target core closures use different environments")
        expected_platform = {
            key: runtime_environment.get(key) for key in ("os", "arch", "libc")
        }
        if {
            key: target["environment"].get(key) for key in ("os", "arch", "libc")
        } != expected_platform:
            raise RehearsalError(
                "core closure platform does not match the declared runtime platform"
            )
        package_entries = metadata.get("packages")
        openclaw_entry = next(
            (
                item
                for item in package_entries
                if isinstance(item, dict) and item.get("name") == "openclaw"
            ),
            None,
        ) if isinstance(package_entries, list) else None
        if not isinstance(openclaw_entry, dict):
            raise RehearsalError("input metadata lacks openclaw package evidence")
        for lane, closure in (("current", current), ("target", target)):
            package_metadata = openclaw_entry.get(lane)
            if not isinstance(package_metadata, dict):
                raise RehearsalError(f"openclaw {lane} package evidence is missing")
            root_entry = next(
                (
                    item
                    for item in closure["packages"]
                    if item["name"] == "openclaw"
                    and item["version"] == closure["root_package"]["version"]
                ),
                None,
            )
            if (
                not isinstance(root_entry, dict)
                or package_metadata.get("version") != closure["root_package"]["version"]
                or package_metadata.get("integrity") != root_entry.get("integrity")
            ):
                raise RehearsalError(
                    f"openclaw {lane} closure does not match package evidence"
                )
        current_by_key = {
            (item["path"], item["name"]): item for item in current["packages"]
        }
        for item in target["packages"]:
            previous = current_by_key.get((item["path"], item["name"]))
            if item["flags"]["has_install_script"] and (
                previous is None or not previous["flags"]["has_install_script"]
            ):
                raise RehearsalError(
                    f"target closure adds a transitive install script: {item['name']}"
                )
    except RehearsalError as exc:
        errors.append(str(exc))
    status = "failed" if errors else "success"
    report = {
        "schema": CORE_CANDIDATE_LOCK_SCHEMA,
        **common,
        "status": status,
        "package": "openclaw",
        "current_root": current.get("root"),
        "target_root": target.get("root"),
        "environment": target.get("environment"),
        "changed_packages": compare_core_closures(current, target) if not errors else [],
        "errors": errors,
    }
    return report, status


def validate_member(member: tarfile.TarInfo) -> None:
    pure = PurePosixPath(member.name)
    if pure.is_absolute() or ".." in pure.parts or not member.name:
        raise RehearsalError(f"unsafe archive member path: {member.name!r}")
    if member.issym() or member.islnk() or member.isdev() or member.isfifo():
        raise RehearsalError(f"unsupported archive member type: {member.name}")
    if member.size < 0 or member.size > MAX_ARCHIVE_MEMBER_BYTES:
        raise RehearsalError(f"archive member exceeds size limit: {member.name}")


def inspect_archive(path: Path) -> dict[str, Any]:
    file_hashes: dict[str, str] = {}
    package_json: dict[str, Any] | None = None
    with tarfile.open(path, "r:gz") as archive:
        members = archive.getmembers()
        for member in members:
            validate_member(member)
            if not member.isfile():
                continue
            extracted = archive.extractfile(member)
            if extracted is None:
                raise RehearsalError(f"cannot read archive member: {member.name}")
            digest = hashlib.sha256()
            payload = bytearray() if member.name == "package/package.json" else None
            for chunk in iter(lambda: extracted.read(1024 * 1024), b""):
                digest.update(chunk)
                if payload is not None:
                    if len(payload) + len(chunk) > MAX_TEXT_MEMBER_BYTES:
                        raise RehearsalError("package/package.json exceeds size limit")
                    payload.extend(chunk)
            file_hashes[member.name] = digest.hexdigest()
            if payload is not None:
                try:
                    package_json = json.loads(payload.decode("utf-8"))
                except (UnicodeDecodeError, json.JSONDecodeError, RecursionError) as exc:
                    raise RehearsalError("package/package.json is invalid") from exc
    if package_json is None:
        raise RehearsalError("archive lacks package/package.json")
    return {"package_json": package_json, "file_hashes": file_hashes}


def read_archive_text(path: Path, member_name: str) -> str:
    with tarfile.open(path, "r:gz") as archive:
        try:
            member = archive.getmember(member_name)
        except KeyError as exc:
            raise RehearsalError(f"archive member is missing: {member_name}") from exc
        validate_member(member)
        if not member.isfile() or member.size > MAX_TEXT_MEMBER_BYTES:
            raise RehearsalError(f"archive member is not a small regular file: {member_name}")
        extracted = archive.extractfile(member)
        if extracted is None:
            raise RehearsalError(f"cannot read archive member: {member_name}")
        try:
            return extracted.read(MAX_TEXT_MEMBER_BYTES + 1).decode("utf-8")
        except UnicodeDecodeError as exc:
            raise RehearsalError(f"archive member is not UTF-8 text: {member_name}") from exc


def verify_archive(path: Path, metadata: dict[str, Any]) -> dict[str, Any]:
    if not path.is_file():
        raise RehearsalError(f"archive is missing: {path}")
    if integrity_for(path) != metadata.get("integrity"):
        raise RehearsalError(f"integrity mismatch for {metadata.get('name')}@{metadata.get('version')}")
    if digest_file(path, "sha1") != metadata.get("shasum"):
        raise RehearsalError(f"shasum mismatch for {metadata.get('name')}@{metadata.get('version')}")
    inspected = inspect_archive(path)
    if integrity_for(path) != metadata.get("integrity") or digest_file(path, "sha1") != metadata.get("shasum"):
        raise RehearsalError(f"archive changed during inspection: {metadata.get('name')}")
    package_json = inspected["package_json"]
    if package_json.get("name") != metadata.get("name") or package_json.get("version") != metadata.get("version"):
        raise RehearsalError(f"package identity mismatch in {path.name}")
    return inspected


def verify_archive_cached(
    path: Path,
    metadata: dict[str, Any],
    cache_dir: Path | None,
    provenance: list[dict[str, str]],
) -> dict[str, Any]:
    if not path.is_file():
        raise RehearsalError(f"archive is missing: {path}")
    key_material = {
        "archive_sha256": digest_file(path),
        "archive_sha1": digest_file(path, "sha1"),
        "metadata": metadata,
    }
    inspected = cached_analysis(
        cache_dir=cache_dir,
        namespace="archive",
        key_material=key_material,
        provenance=provenance,
        build=lambda: verify_archive(path, metadata),
        validate=lambda payload: (
            isinstance(payload, dict)
            and isinstance(payload.get("package_json"), dict)
            and payload["package_json"].get("name") == metadata.get("name")
            and payload["package_json"].get("version") == metadata.get("version")
            and isinstance(payload.get("file_hashes"), dict)
        ),
    )
    package_json = inspected.get("package_json") if isinstance(inspected, dict) else None
    if (
        not isinstance(package_json, dict)
        or package_json.get("name") != metadata.get("name")
        or package_json.get("version") != metadata.get("version")
        or not isinstance(inspected.get("file_hashes"), dict)
    ):
        raise RehearsalError(f"cached archive analysis is invalid for {path.name}")
    return inspected


def analyze_archive_unit(
    task: dict[str, Any],
    cache_dir: Path | None,
    analyzer: Any = verify_archive_cached,
) -> dict[str, Any]:
    started = time.monotonic()
    provenance: list[dict[str, str]] = []
    try:
        inspection = analyzer(
            task["path"],
            task["metadata"],
            cache_dir,
            provenance,
        )
        return {
            "task_id": task["task_id"],
            "package": task["name"],
            "lane": task["lane"],
            "status": "success",
            "inspection": inspection,
            "error": None,
            "cache_provenance": provenance,
            "duration_ms": round((time.monotonic() - started) * 1000, 3),
        }
    except (KeyError, RehearsalError, OSError, tarfile.TarError) as exc:
        return {
            "task_id": task["task_id"],
            "package": task["name"],
            "lane": task["lane"],
            "status": "failed",
            "inspection": None,
            "error": str(exc),
            "cache_provenance": provenance,
            "duration_ms": round((time.monotonic() - started) * 1000, 3),
        }


def archive_timeout_result(
    task: dict[str, Any],
    timeout_seconds: float,
) -> dict[str, Any]:
    return {
        "task_id": task["task_id"],
        "package": task["name"],
        "lane": task["lane"],
        "status": "timed_out",
        "inspection": None,
        "error": (
            f"archive analysis timed out for {task['task_id']} "
            f"after {timeout_seconds:g}s"
        ),
        "cache_provenance": [],
        "duration_ms": round(timeout_seconds * 1000, 3),
    }


def run_archive_subprocess_unit(
    task: dict[str, Any],
    cache_dir: Path | None,
    timeout_seconds: float,
    command_override: list[str] | None = None,
) -> dict[str, Any]:
    command = command_override or [
        sys.executable,
        str(Path(__file__).resolve()),
        "_analyze-archive",
        "--task-id",
        task["task_id"],
        "--package",
        task["name"],
        "--lane",
        task["lane"],
        "--path",
        str(task["path"]),
        "--metadata-json",
        json.dumps(task["metadata"], ensure_ascii=True, sort_keys=True),
    ]
    if command_override is None and cache_dir is not None:
        command.extend(["--cache-dir", str(cache_dir)])
    try:
        completed = subprocess.run(
            command,
            check=False,
            capture_output=True,
            text=True,
            timeout=timeout_seconds,
        )
    except subprocess.TimeoutExpired:
        return archive_timeout_result(task, timeout_seconds)
    if completed.returncode != 0:
        detail = completed.stderr.strip() or f"exit {completed.returncode}"
        return {
            "task_id": task["task_id"],
            "package": task["name"],
            "lane": task["lane"],
            "status": "failed",
            "inspection": None,
            "error": f"archive analysis subprocess failed: {detail}",
            "cache_provenance": [],
            "duration_ms": 0,
        }
    try:
        result = json.loads(completed.stdout)
    except json.JSONDecodeError:
        result = None
    if (
        not isinstance(result, dict)
        or result.get("task_id") != task["task_id"]
        or result.get("package") != task["name"]
        or result.get("lane") != task["lane"]
        or result.get("status") not in {"success", "failed"}
        or not isinstance(result.get("cache_provenance"), list)
        or not isinstance(result.get("duration_ms"), (int, float))
    ):
        return {
            "task_id": task["task_id"],
            "package": task["name"],
            "lane": task["lane"],
            "status": "failed",
            "inspection": None,
            "error": "archive analysis subprocess returned invalid output",
            "cache_provenance": [],
            "duration_ms": 0,
        }
    return result


def execute_archive_analyses(
    tasks: list[dict[str, Any]],
    *,
    cache_dir: Path | None,
    workers: int,
    timeout_seconds: float,
    unit_runner: Any = run_archive_subprocess_unit,
) -> list[dict[str, Any]]:
    if workers < 1 or workers > MAX_ARCHIVE_WORKERS:
        raise RehearsalError(
            f"archive workers must be between 1 and {MAX_ARCHIVE_WORKERS}"
        )
    if timeout_seconds <= 0 or timeout_seconds > 900:
        raise RehearsalError(
            "archive timeout seconds must be greater than 0 and at most 900"
        )
    if not tasks:
        return []
    if cache_dir is not None and secure_cache_namespace(
        cache_dir,
        "archive",
    ) is None:
        cache_dir = None

    executor = concurrent.futures.ThreadPoolExecutor(
        max_workers=min(workers, len(tasks)),
        thread_name_prefix="safe-update-archive",
    )
    submissions = [
        (
            task,
            executor.submit(unit_runner, task, cache_dir, timeout_seconds),
        )
        for task in tasks
    ]
    results: list[dict[str, Any]] = []
    try:
        for task, future in submissions:
            try:
                result = future.result()
            except Exception as exc:
                result = {
                    "task_id": task["task_id"],
                    "package": task["name"],
                    "lane": task["lane"],
                    "status": "failed",
                    "inspection": None,
                    "error": (
                        f"archive analysis failed for {task['task_id']}: "
                        f"{type(exc).__name__}: {exc}"
                    ),
                    "cache_provenance": [],
                    "duration_ms": 0,
                }
            results.append(result)
    finally:
        executor.shutdown(wait=True, cancel_futures=True)
    return results


def archive_path(input_dir: Path, lane: str, metadata: dict[str, Any]) -> Path:
    filename = metadata.get("archive")
    if not isinstance(filename, str) or not filename or PurePosixPath(filename).name != filename:
        raise RehearsalError(f"unsafe archive filename for {metadata.get('name')}")
    return input_dir / lane / filename


def bounded(values: list[str]) -> dict[str, Any]:
    return {
        "count": len(values),
        "members": values[:DIFF_MEMBER_LIMIT],
        "truncated": len(values) > DIFF_MEMBER_LIMIT,
    }


def authority_archive_diff(
    current: dict[str, Any],
    target: dict[str, Any],
) -> dict[str, list[str]]:
    current_files = current["file_hashes"]
    target_files = target["file_hashes"]
    current_names = set(current_files)
    target_names = set(target_files)
    return {
        "added": sorted(target_names - current_names),
        "removed": sorted(current_names - target_names),
        "changed": sorted(
            name
            for name in current_names & target_names
            if current_files[name] != target_files[name]
        ),
    }


def compare_archives(current: dict[str, Any], target: dict[str, Any]) -> dict[str, Any]:
    authority_diff = authority_archive_diff(current, target)
    return {
        field: bounded(authority_diff[field])
        for field in ("added", "removed", "changed")
    }


def parse_conservative_inputs(value: Any) -> dict[str, Any]:
    if not isinstance(value, dict) or value.get("schema") != CONSERVATIVE_INPUTS_SCHEMA:
        raise RehearsalError(
            f"conservative inputs schema must be {CONSERVATIVE_INPUTS_SCHEMA}"
        )
    if set(value) != {"schema", "satisfied_gates", "operator_escalations"}:
        raise RehearsalError("conservative inputs contain unknown or missing fields")
    satisfied = value.get("satisfied_gates")
    escalations = value.get("operator_escalations")
    if not isinstance(satisfied, list) or not isinstance(escalations, list):
        raise RehearsalError("conservative input lists are invalid")
    normalized_gates: dict[str, str] = {}
    for item in satisfied:
        if (
            not isinstance(item, dict)
            or set(item) != {"id", "evidence_digest"}
            or item.get("id") not in GATE_EVIDENCE_IDS
            or not re.fullmatch(
                r"sha256:[0-9a-f]{64}",
                str(item.get("evidence_digest", "")),
            )
            or item["id"] in normalized_gates
        ):
            raise RehearsalError("satisfied gate entry is invalid")
        normalized_gates[item["id"]] = item["evidence_digest"]
    if (
        any(item not in CONSERVATIVE_CONDITION_IDS for item in escalations)
        or escalations != sorted(set(escalations))
    ):
        raise RehearsalError("operator escalations are invalid or not canonical")
    return {
        "satisfied_gates": normalized_gates,
        "operator_escalations": set(escalations),
    }


def empty_conservative_inputs() -> dict[str, Any]:
    return {"satisfied_gates": {}, "operator_escalations": set()}


def path_matches(path: str, *needles: str) -> bool:
    lowered = path.lower()
    return any(needle in lowered for needle in needles)


def conservative_machine_conditions(
    *,
    core_candidate_lock: dict[str, Any],
    installation_attestation_status: str,
    authority_packages: list[dict[str, Any]],
    authority_complete: bool,
) -> dict[str, bool]:
    changed_paths = sorted(
        {
            path
            for package in authority_packages
            for field in ("added", "removed", "changed")
            for path in package["archive_diff"][field]
        }
    )
    metadata_fields = {
        field
        for package in authority_packages
        for field in package.get("metadata_changed_fields", [])
    }
    closure_changes = core_candidate_lock.get("changed_packages", [])
    optional_or_native_unknown = any(
        (
            bool((change.get("current_flags") or {}).get("optional"))
            or bool((change.get("target_flags") or {}).get("optional"))
            or any(
                (change.get(side) or {}).get(selector)
                for side in ("current_selectors", "target_selectors")
                for selector in ("os", "cpu", "libc")
            )
        )
        and (
            change.get("current_selected") is None
            or change.get("target_selected") is None
        )
        for change in closure_changes
    )
    lifecycle_change = any(
        finding.get("id") == "lifecycle-script-changed"
        for package in authority_packages
        for finding in package.get("risk_findings", [])
    ) or any("install script" in error for error in core_candidate_lock.get("errors", []))
    state_change = any(
        path_matches(
            path,
            "/migration",
            "/migrations",
            "/schema",
            "/queue",
            "/crypto",
            "/cipher",
            "/keystore",
        )
        for path in changed_paths
    )
    plugin_sdk_change = any(
        path_matches(path, "/plugin", "/sdk", "/abi", "/loader", "module-resolver")
        for path in changed_paths
    )
    launcher_service_change = any(
        path_matches(path, "/launcher", "/service", "/systemd", "/gateway", "/bin/")
        for path in changed_paths
    )
    permissions_change = any(
        path_matches(path, "/permission", "/authz", "/acl", "/capability")
        for path in changed_paths
    )
    protocol_change = any(
        path_matches(path, "/protocol", "/transport", "/wire")
        for path in changed_paths
    )
    channel_crypto_change = any(
        path_matches(path, "/signal", "/matrix", "/telegram", "/whatsapp")
        and path_matches(path, "crypto", "encrypt", "e2e")
        for path in changed_paths
    )
    return {
        "candidate-closure-resolved": core_candidate_lock.get("status") != "success",
        "installation-attestation-fresh-complete": (
            installation_attestation_status != "success"
        ),
        "authority-input-lossless": not authority_complete,
        "lifecycle-download-evidence": lifecycle_change,
        "state-migration-rehearsal": state_change,
        "rollback-evidence": True,
        "plugin-sdk-contract": plugin_sdk_change,
        "launcher-service-contract": launcher_service_change,
        "permissions-contract": permissions_change,
        "protocol-contract": protocol_change,
        "channel-crypto-contract": channel_crypto_change,
        "environment-matched-rehearsal": "engines" in metadata_fields,
        "native-optional-dependency-known": optional_or_native_unknown,
    }


def evaluate_conservative_gates(
    *,
    core_candidate_lock: dict[str, Any],
    installation_attestation_status: str,
    authority_packages: list[dict[str, Any]],
    authority_complete: bool,
    inputs: dict[str, Any],
    common: dict[str, Any],
    input_errors: list[str] | None = None,
    machine_conditions: dict[str, bool] | None = None,
) -> tuple[dict[str, Any], str]:
    detected = machine_conditions or conservative_machine_conditions(
        core_candidate_lock=core_candidate_lock,
        installation_attestation_status=installation_attestation_status,
        authority_packages=authority_packages,
        authority_complete=authority_complete,
    )
    escalations = inputs["operator_escalations"]
    satisfied = inputs["satisfied_gates"]
    hard_block_ids = {
        "candidate-closure-resolved",
        "installation-attestation-fresh-complete",
        "authority-input-lossless",
        "native-optional-dependency-known",
    }
    decisions: list[dict[str, Any]] = []
    required_gates: set[str] = set()
    errors: list[str] = list(input_errors or [])
    conservative = bool(core_candidate_lock.get("changed_packages"))
    for gate_id in sorted(CONSERVATIVE_CONDITION_IDS):
        triggered = bool(detected[gate_id] or gate_id in escalations)
        required_gate = gate_id if triggered and gate_id in GATE_EVIDENCE_IDS else None
        if required_gate:
            required_gates.add(required_gate)
        if triggered and gate_id in hard_block_ids:
            outcome = "blocked"
            errors.append(f"{gate_id}: hard-blocking deterministic condition")
        elif required_gate and required_gate not in satisfied:
            outcome = "blocked"
            errors.append(f"{gate_id}: required evidence is missing")
        elif triggered:
            outcome = "conservative"
            conservative = True
        else:
            outcome = "pass"
        decisions.append(
            {
                "id": gate_id,
                "triggered": triggered,
                "source": (
                    "machine_and_operator"
                    if detected[gate_id] and gate_id in escalations
                    else "machine"
                    if detected[gate_id]
                    else "operator"
                    if gate_id in escalations
                    else "none"
                ),
                "outcome": outcome,
                "required_gate": required_gate,
                "evidence_digest": satisfied.get(required_gate) if required_gate else None,
            }
        )
    decision_content = {
        "schema": "openclaw.safe_update.conservative_gate_decision.v1",
        "handling": (
            "blocked" if errors else "conservative" if conservative else "baseline"
        ),
        "required_gates": sorted(required_gates),
        "decisions": decisions,
        "authority_digest": canonical_digest(authority_packages),
        "errors": errors,
    }
    status = "failed" if errors else "success"
    report = {
        "schema": CONSERVATIVE_GATES_SCHEMA,
        **common,
        "status": status,
        "handling": decision_content["handling"],
        "authority_digest": decision_content["authority_digest"],
        "decision_digest": canonical_digest(decision_content),
        "required_gates": decision_content["required_gates"],
        "satisfied_gates": [
            {"id": gate_id, "evidence_digest": satisfied[gate_id]}
            for gate_id in sorted(satisfied)
        ],
        "decisions": decisions,
        "errors": errors,
    }
    return report, status


def build_impact_shadow(
    *,
    authority_packages: list[dict[str, Any]],
    core_candidate_lock: dict[str, Any],
    installation_contract: dict[str, Any],
    baseline_check_ids: set[str],
    authority_complete: bool,
    common: dict[str, Any],
) -> dict[str, Any]:
    errors: list[str] = []
    changed_members = sorted(
        (
            package["name"],
            change_kind,
            member,
        )
        for package in authority_packages
        for change_kind in ("added", "removed", "changed")
        for member in package["archive_diff"][change_kind]
    )
    closure_changes = sorted(
        core_candidate_lock.get("changed_packages", []),
        key=lambda item: (str(item.get("name")), str(item.get("path"))),
    )
    closure_names = {
        str(item.get("name"))
        for item in closure_changes
        if isinstance(item.get("name"), str)
    }
    if not authority_complete:
        errors.append("authority input is incomplete")
    try:
        contract = canonical_installation_contract(installation_contract)
    except RehearsalError as exc:
        contract = {"components": [], "capabilities": [], "contracts": []}
        errors.append(str(exc))

    component_ids = {item["id"] for item in contract["components"]}
    if any(
        item.startswith(SHADOW_ID_PREFIX)
        for item in baseline_check_ids | component_ids
    ):
        errors.append("baseline or component ID collides with reserved shadow namespace")

    directly_affected: set[str] = set()
    mapped_members: set[tuple[str, str, str]] = set()
    for component in contract["components"]:
        for artifact in component["artifacts"]:
            if artifact["kind"] == "npm_archive_member":
                package, separator, member = artifact["ref"].partition(":")
                if not separator:
                    errors.append(
                        f"component {component['id']} has an unparseable "
                        "npm_archive_member ref"
                    )
                    continue
                for changed_member in changed_members:
                    if changed_member[0] == package and changed_member[2] == member:
                        directly_affected.add(component["id"])
                        mapped_members.add(changed_member)
            elif artifact["kind"] == "npm_package":
                package = artifact["ref"].split("@", 1)[0]
                if artifact["ref"].startswith("@"):
                    package = artifact["ref"].rsplit("@", 1)[0]
                if package in closure_names:
                    directly_affected.add(component["id"])

    affected = set(directly_affected)
    changed = True
    while changed:
        changed = False
        for component in contract["components"]:
            if component["id"] in affected:
                continue
            if any(
                dependency["component_id"] in affected
                for dependency in component["depends_on"]
            ):
                affected.add(component["id"])
                changed = True

    affected_components = sorted(affected)
    affected_capabilities = sorted(
        capability["id"]
        for capability in contract["capabilities"]
        if set(capability["component_ids"]) & affected
    )
    affected_contracts = sorted(
        {
            contract_id
            for component in contract["components"]
            if component["id"] in affected
            for contract_id in component["contract_ids"]
        }
    )
    would_add_checks = sorted(
        (
            {
                "id": f"{SHADOW_ID_PREFIX}check:{capability['id']}:{index}",
                "capability_id": capability["id"],
                "description": description,
            }
            for capability in contract["capabilities"]
            if capability["id"] in affected_capabilities
            for index, description in enumerate(
                capability["post_activation_checks"],
                start=1,
            )
        ),
        key=lambda item: item["id"],
    )
    generated_ids = [item["id"] for item in would_add_checks]
    if len(generated_ids) != len(set(generated_ids)):
        errors.append("generated shadow check IDs collide")
    if set(generated_ids) & (baseline_check_ids | component_ids):
        errors.append("generated shadow check ID collides with a declared ID")

    unmapped_members = sorted(
        (
            {
                "package": package,
                "change": change_kind,
                "member": member,
            }
            for package, change_kind, member in changed_members
            if (package, change_kind, member) not in mapped_members
        ),
        key=lambda item: (item["package"], item["change"], item["member"]),
    )
    mapped_closure_names = {
        str(item["ref"]).split("@", 1)[0]
        for component in contract["components"]
        for item in component["artifacts"]
        if item["kind"] == "npm_package" and not item["ref"].startswith("@")
    } | {
        str(item["ref"]).rsplit("@", 1)[0]
        for component in contract["components"]
        for item in component["artifacts"]
        if item["kind"] == "npm_package" and item["ref"].startswith("@")
    }
    unmapped_packages = sorted(closure_names - mapped_closure_names)
    would_flag_risks: list[dict[str, Any]] = []
    if unmapped_members:
        would_flag_risks.append(
            {
                "id": f"{SHADOW_ID_PREFIX}risk:unmapped-members",
                "kind": "unmapped_members",
                "count": len(unmapped_members),
            }
        )
    if unmapped_packages:
        would_flag_risks.append(
            {
                "id": f"{SHADOW_ID_PREFIX}risk:unmapped-packages",
                "kind": "unmapped_packages",
                "count": len(unmapped_packages),
            }
        )
    if closure_changes:
        would_flag_risks.append(
            {
                "id": f"{SHADOW_ID_PREFIX}risk:resolved-closure-drift",
                "kind": "resolved_closure_drift",
                "count": len(closure_changes),
            }
        )
    would_flag_risks.sort(key=lambda item: item["id"])
    shadow_content = {
        "schema": "openclaw.safe_update.impact_shadow_content.v1",
        "authoritative": False,
        "affected_components": affected_components,
        "affected_capabilities": affected_capabilities,
        "affected_contracts": affected_contracts,
        "would_add_checks": would_add_checks,
        "would_flag_risks": would_flag_risks,
        "would_block": bool(errors or unmapped_members or unmapped_packages),
        "would_omit_checks": [],
        "unmapped_members": unmapped_members,
        "unmapped_packages": unmapped_packages,
        "errors": errors,
    }
    return {
        "schema": IMPACT_SHADOW_SCHEMA,
        **common,
        "authoritative": False,
        "status": "failed" if errors else "success",
        "shadow_digest": canonical_digest(shadow_content),
        **{key: value for key, value in shadow_content.items() if key != "schema"},
    }


def semver_tuple(value: str) -> tuple[int, int, int] | None:
    candidate = value.removeprefix("v").split("-", 1)[0].split("+", 1)[0]
    parts = candidate.split(".")
    if not 1 <= len(parts) <= 3 or any(not part.isdigit() for part in parts):
        return None
    values = [int(part) for part in parts]
    return tuple((values + [0, 0])[:3])


def node_version_satisfies(version: str, expression: str) -> bool | None:
    actual = semver_tuple(version)
    if actual is None or not isinstance(expression, str) or not expression.strip():
        return None
    outcomes: list[bool | None] = []
    for alternative in expression.split("||"):
        clauses = alternative.strip().split()
        if not clauses:
            continue
        clause_outcomes: list[bool] = []
        for clause in clauses:
            match = re.fullmatch(r"(>=|<=|>|<|=|\^|~)?v?(\d+(?:\.\d+){0,2})(?:\.x)?", clause)
            if not match:
                outcomes.append(None)
                clause_outcomes = []
                break
            operator = match.group(1) or "="
            expected = semver_tuple(match.group(2))
            if expected is None:
                return None
            if operator == ">=":
                clause_outcomes.append(actual >= expected)
            elif operator == "<=":
                clause_outcomes.append(actual <= expected)
            elif operator == ">":
                clause_outcomes.append(actual > expected)
            elif operator == "<":
                clause_outcomes.append(actual < expected)
            elif operator == "^":
                clause_outcomes.append(actual >= expected and actual[0] == expected[0])
            elif operator == "~":
                clause_outcomes.append(actual >= expected and actual[:2] == expected[:2])
            else:
                specified_parts = len(match.group(2).split("."))
                clause_outcomes.append(actual[:specified_parts] == expected[:specified_parts])
        if clause_outcomes:
            outcomes.append(all(clause_outcomes))
    if True in outcomes:
        return True
    if outcomes and all(outcome is False for outcome in outcomes):
        return False
    return None


def compare_package_metadata(
    current: dict[str, Any], target: dict[str, Any], runtime_node_version: str | None
) -> dict[str, Any]:
    current_values = {field: current.get(field) for field in PACKAGE_METADATA_FIELDS}
    target_values = {field: target.get(field) for field in PACKAGE_METADATA_FIELDS}
    changed_fields = [
        field for field in PACKAGE_METADATA_FIELDS if current_values[field] != target_values[field]
    ]
    findings: list[dict[str, str]] = []

    current_scripts = (
        current_values.get("scripts") if isinstance(current_values.get("scripts"), dict) else {}
    )
    target_scripts = (
        target_values.get("scripts") if isinstance(target_values.get("scripts"), dict) else {}
    )
    changed_lifecycle = sorted(
        name
        for name in LIFECYCLE_SCRIPTS
        if current_scripts.get(name) != target_scripts.get(name)
    )
    if changed_lifecycle:
        findings.append(
            {
                "id": "lifecycle-script-changed",
                "severity": "blocked",
                "detail": "Lifecycle scripts changed: " + ", ".join(changed_lifecycle),
            }
        )

    target_engines = target_values.get("engines")
    target_node_engine = target_engines.get("node") if isinstance(target_engines, dict) else None
    if isinstance(target_node_engine, str):
        compatibility = node_version_satisfies(runtime_node_version or "", target_node_engine)
        if compatibility is False:
            findings.append(
                {
                    "id": "target-node-engine-incompatible",
                    "severity": "blocked",
                    "detail": f"Runtime Node {runtime_node_version} does not satisfy target engines.node {target_node_engine}",
                }
            )
        elif compatibility is None:
            findings.append(
                {
                    "id": "target-node-engine-unproven",
                    "severity": "blocked",
                    "detail": f"Cannot prove runtime Node {runtime_node_version or 'unknown'} satisfies target engines.node {target_node_engine}",
                }
            )

    return {
        "current": current_values,
        "target": target_values,
        "changed_fields": changed_fields,
        "risk_findings": findings,
    }


def load_coverage(
    path: Path | None, allow_none: bool
) -> tuple[dict[str, Any], list[str], str]:
    empty = {"install_shape": None, "runtime": {}, "surfaces": []}
    if path is None:
        if allow_none:
            return empty, [], "explicitly_not_required"
        return empty, ["coverage profile is required"], "missing"
    try:
        value = read_json(path)
    except RehearsalError as exc:
        return empty, [str(exc)], "invalid"
    if not isinstance(value, dict) or value.get("schema") != COVERAGE_SCHEMA:
        return empty, [f"coverage schema must be {COVERAGE_SCHEMA}"], "invalid"

    errors: list[str] = []
    install_shape = value.get("install_shape")
    if install_shape not in SUPPORTED_INSTALL_SHAPES:
        errors.append(f"unsupported install shape: {install_shape}")
    runtime = value.get("runtime")
    if not isinstance(runtime, dict):
        errors.append("coverage runtime must be an object")
        runtime = {}
    node_version = runtime.get("node_version")
    if not isinstance(node_version, str) or semver_tuple(node_version) is None:
        errors.append("coverage runtime.node_version must be an exact version")
    for field in ("os", "arch", "libc"):
        runtime_value = runtime.get(field)
        if (
            not isinstance(runtime_value, str)
            or not runtime_value
            or runtime_value == "unknown"
        ):
            errors.append(f"coverage runtime.{field} must be explicit")

    surfaces = value.get("surfaces")
    if not isinstance(surfaces, list):
        return empty, errors + ["coverage surfaces must be a list"], "invalid"
    if not surfaces and not allow_none:
        errors.append("coverage profile must declare at least one surface")
    normalized: list[dict[str, Any]] = []
    seen: set[str] = set()
    for index, surface in enumerate(surfaces):
        if not isinstance(surface, dict):
            errors.append(f"coverage surface {index} must be an object")
            continue
        surface_id = surface.get("id")
        category = surface.get("category")
        required = surface.get("required")
        customization_checks = surface.get("customization_checks", [])
        post_update_checks = surface.get("post_update_checks")
        if not isinstance(surface_id, str) or not surface_id or surface_id in seen:
            errors.append(f"coverage surface {index} has an invalid or duplicate id")
            continue
        seen.add(surface_id)
        if category not in SURFACE_CATEGORIES:
            errors.append(f"coverage surface {surface_id} has unsupported category")
            continue
        if not isinstance(required, bool):
            errors.append(f"coverage surface {surface_id} must declare required as boolean")
            continue
        if not isinstance(customization_checks, list) or any(
            not isinstance(item, str) or not item for item in customization_checks
        ):
            errors.append(f"coverage surface {surface_id} has invalid customization checks")
            continue
        if not isinstance(post_update_checks, list) or any(
            not isinstance(item, str) or not item.strip() for item in post_update_checks
        ):
            errors.append(f"coverage surface {surface_id} has invalid post-update checks")
            continue
        if required and not post_update_checks:
            errors.append(f"required coverage surface {surface_id} needs a post-update check")
        normalized.append(
            {
                "id": surface_id,
                "category": category,
                "required": required,
                "customization_checks": customization_checks,
                "post_update_checks": post_update_checks,
            }
        )
    return {
        "install_shape": install_shape,
        "runtime": {
            "node_version": node_version,
            "os": runtime.get("os"),
            "arch": runtime.get("arch"),
            "libc": runtime.get("libc"),
        },
        "surfaces": normalized,
    }, errors, "configured"


def load_customizations(path: Path | None, allow_none: bool) -> tuple[list[dict[str, Any]], list[str], str]:
    if path is None:
        if allow_none:
            return [], [], "explicitly_not_required"
        return [], ["customization manifest is required"], "missing"
    try:
        value = read_json(path)
    except RehearsalError as exc:
        return [], [str(exc)], "invalid"
    errors: list[str] = []
    if not isinstance(value, dict) or value.get("schema") != CUSTOMIZATIONS_SCHEMA:
        return [], [f"customization schema must be {CUSTOMIZATIONS_SCHEMA}"], "invalid"
    checks = value.get("checks")
    if not isinstance(checks, list):
        return [], ["customization checks must be a list"], "invalid"
    if not checks and not allow_none:
        errors.append("customization manifest has no checks")
    seen: set[str] = set()
    normalized: list[dict[str, Any]] = []
    for index, check in enumerate(checks):
        if not isinstance(check, dict):
            errors.append(f"customization check {index} must be an object")
            continue
        check_id = check.get("id")
        package = check.get("package")
        kind = check.get("kind")
        member = check.get("member")
        if not isinstance(check_id, str) or not check_id or check_id in seen:
            errors.append(f"customization check {index} has an invalid or duplicate id")
            continue
        seen.add(check_id)
        if not isinstance(package, str) or not PACKAGE_RE.fullmatch(package):
            errors.append(f"customization check {check_id} has an invalid package")
            continue
        if kind not in {"required_member", "member_contains"}:
            errors.append(f"customization check {check_id} has unsupported kind")
            continue
        if not isinstance(member, str) or not member or PurePosixPath(member).is_absolute() or ".." in PurePosixPath(member).parts:
            errors.append(f"customization check {check_id} has an unsafe member")
            continue
        normalized_check = {"id": check_id, "package": package, "kind": kind, "member": member}
        if kind == "member_contains":
            needle = check.get("needle")
            if not isinstance(needle, str) or not needle:
                errors.append(f"customization check {check_id} needs a non-empty needle")
                continue
            normalized_check["needle"] = needle
        normalized.append(normalized_check)
    return normalized, errors, "configured"


def parse_installation_contract(value: Any) -> dict[str, Any]:
    if not isinstance(value, dict) or value.get("schema") != INSTALLATION_CONTRACT_SCHEMA:
        raise RehearsalError(
            f"installation contract schema must be {INSTALLATION_CONTRACT_SCHEMA}"
        )
    if set(value) != {
        "schema",
        "install_shape",
        "runtime",
        "capabilities",
        "components",
        "contracts",
    }:
        raise RehearsalError("installation contract contains unknown or missing fields")
    if value.get("install_shape") not in SUPPORTED_INSTALL_SHAPES:
        raise RehearsalError("installation contract install shape is unsupported")
    if not isinstance(value.get("runtime"), dict):
        raise RehearsalError("installation contract runtime must be an object")

    capabilities = value.get("capabilities")
    components = value.get("components")
    contracts = value.get("contracts")
    if not isinstance(capabilities, list) or not capabilities:
        raise RehearsalError("installation contract capabilities must be a non-empty list")
    if not isinstance(components, list):
        raise RehearsalError("installation contract components must be a list")
    if not isinstance(contracts, list):
        raise RehearsalError("installation contract contracts must be a list")

    capability_ids: set[str] = set()
    component_ids: set[str] = set()
    contract_ids: set[str] = set()
    for contract in contracts:
        if (
            not isinstance(contract, dict)
            or set(contract) != {"id", "kind", "evidence_refs"}
            or not isinstance(contract.get("id"), str)
            or not contract["id"]
            or contract["id"] in contract_ids
            or not isinstance(contract.get("kind"), str)
            or not contract["kind"]
            or not isinstance(contract.get("evidence_refs"), list)
            or any(not isinstance(item, str) or not item for item in contract["evidence_refs"])
        ):
            raise RehearsalError("installation contract has an invalid or duplicate contract")
        contract_ids.add(contract["id"])

    for component in components:
        if not isinstance(component, dict) or set(component) != {
            "id",
            "roles",
            "application_phases",
            "artifacts",
            "contract_ids",
            "depends_on",
            "supports",
            "governance",
        }:
            raise RehearsalError("installation contract component shape is invalid")
        component_id = component.get("id")
        if (
            not isinstance(component_id, str)
            or not component_id
            or component_id in component_ids
        ):
            raise RehearsalError("installation contract has an invalid or duplicate component")
        component_ids.add(component_id)
        roles = component.get("roles")
        if (
            not isinstance(roles, list)
            or not roles
            or len(roles) != len(set(roles))
            or any(role not in COMPONENT_ROLES for role in roles)
        ):
            raise RehearsalError(f"component {component_id} has invalid roles")
        phases = component.get("application_phases")
        if not isinstance(phases, list) or any(
            not isinstance(item, str) or not item for item in phases
        ):
            raise RehearsalError(f"component {component_id} has invalid application phases")
        artifacts = component.get("artifacts")
        if not isinstance(artifacts, list) or any(
            not isinstance(item, dict)
            or set(item) != {"kind", "ref"}
            or not isinstance(item.get("kind"), str)
            or not isinstance(item.get("ref"), str)
            or not item["kind"]
            or not item["ref"]
            for item in artifacts
        ):
            raise RehearsalError(f"component {component_id} has invalid artifacts")
        if not isinstance(component.get("contract_ids"), list) or any(
            not isinstance(item, str) for item in component["contract_ids"]
        ):
            raise RehearsalError(f"component {component_id} has invalid contract references")
        dependencies = component.get("depends_on")
        if not isinstance(dependencies, list) or any(
            not isinstance(item, dict)
            or set(item) != {"component_id", "kind"}
            or item.get("kind") not in DEPENDENCY_KINDS
            or not isinstance(item.get("component_id"), str)
            for item in dependencies
        ):
            raise RehearsalError(f"component {component_id} has invalid dependencies")
        dependency_keys = [
            (item["component_id"], item["kind"]) for item in dependencies
        ]
        if len(dependency_keys) != len(set(dependency_keys)):
            raise RehearsalError(f"component {component_id} has duplicate dependencies")
        if not isinstance(component.get("supports"), list) or any(
            not isinstance(item, str) for item in component["supports"]
        ):
            raise RehearsalError(f"component {component_id} has invalid capability references")
        governance = component.get("governance")
        if not isinstance(governance, dict) or any(
            key not in {"owner", "removal", "upstream_reference", "kill_criteria"}
            for key in governance
        ):
            raise RehearsalError(f"component {component_id} has invalid governance")

    for capability in capabilities:
        if not isinstance(capability, dict) or set(capability) != {
            "id",
            "category",
            "business_criticality",
            "evidence_policy",
            "component_ids",
            "post_activation_checks",
        }:
            raise RehearsalError("installation contract capability shape is invalid")
        capability_id = capability.get("id")
        if (
            not isinstance(capability_id, str)
            or not capability_id
            or capability_id in capability_ids
        ):
            raise RehearsalError("installation contract has an invalid or duplicate capability")
        capability_ids.add(capability_id)
        if capability.get("category") not in SURFACE_CATEGORIES:
            raise RehearsalError(f"capability {capability_id} has an invalid category")
        if capability.get("business_criticality") not in BUSINESS_CRITICALITIES:
            raise RehearsalError(f"capability {capability_id} has invalid criticality")
        if capability.get("evidence_policy") not in EVIDENCE_POLICIES:
            raise RehearsalError(f"capability {capability_id} has invalid evidence policy")
        checks = capability.get("post_activation_checks")
        if not isinstance(checks, list) or not checks or any(
            not isinstance(item, str) or not item for item in checks
        ):
            raise RehearsalError(f"capability {capability_id} needs post-activation checks")
        if not isinstance(capability.get("component_ids"), list) or any(
            not isinstance(item, str) for item in capability["component_ids"]
        ):
            raise RehearsalError(f"capability {capability_id} has invalid component references")

    for component in components:
        component_id = component["id"]
        for contract_id in component["contract_ids"]:
            if contract_id not in contract_ids:
                raise RehearsalError(
                    f"component {component_id} references unknown contract {contract_id}"
                )
        for dependency in component["depends_on"]:
            if dependency["component_id"] not in component_ids:
                raise RehearsalError(
                    f"component {component_id} references unknown dependency "
                    f"{dependency['component_id']}"
                )
        for capability_id in component["supports"]:
            if capability_id not in capability_ids:
                raise RehearsalError(
                    f"component {component_id} references unknown capability {capability_id}"
                )
    for capability in capabilities:
        for component_id in capability["component_ids"]:
            if component_id not in component_ids:
                raise RehearsalError(
                    f"capability {capability['id']} references unknown component {component_id}"
                )
            component = next(item for item in components if item["id"] == component_id)
            if capability["id"] not in component["supports"]:
                raise RehearsalError(
                    f"capability {capability['id']} and component {component_id} disagree"
                )
    for component in components:
        for capability_id in component["supports"]:
            capability = next(
                item for item in capabilities if item["id"] == capability_id
            )
            if component["id"] not in capability["component_ids"]:
                raise RehearsalError(
                    f"component {component['id']} and capability {capability_id} disagree"
                )
    return value


def adapt_v1_installation_contract(
    checks: list[dict[str, Any]],
    coverage_profile: dict[str, Any],
) -> dict[str, Any]:
    if not checks and not coverage_profile["surfaces"]:
        return parse_installation_contract(
            {
                "schema": INSTALLATION_CONTRACT_SCHEMA,
                "install_shape": coverage_profile["install_shape"],
                "runtime": coverage_profile["runtime"],
                "capabilities": [
                    {
                        "id": "openclaw.core",
                        "category": "other",
                        "business_criticality": "critical",
                        "evidence_policy": "always",
                        "component_ids": ["core.openclaw"],
                        "post_activation_checks": [
                            "verify OpenClaw starts after the approved update"
                        ],
                    }
                ],
                "components": [
                    {
                        "id": "core.openclaw",
                        "roles": ["core"],
                        "application_phases": ["core"],
                        "artifacts": [{"kind": "npm_package", "ref": "openclaw"}],
                        "contract_ids": ["openclaw-core-v1"],
                        "depends_on": [],
                        "supports": ["openclaw.core"],
                        "governance": {},
                    }
                ],
                "contracts": [
                    {
                        "id": "openclaw-core-v1",
                        "kind": "package_contract",
                        "evidence_refs": ["core candidate lock"],
                    }
                ],
            }
        )
    checks_by_id = {item["id"]: item for item in checks}
    component_supports: dict[str, list[str]] = {item["id"]: [] for item in checks}
    capabilities: list[dict[str, Any]] = []
    for surface in coverage_profile["surfaces"]:
        component_ids = [
            f"compatibility:{check_id}" for check_id in surface["customization_checks"]
        ]
        for check_id in surface["customization_checks"]:
            if check_id not in checks_by_id:
                raise RehearsalError(
                    f"coverage surface {surface['id']} references unknown check {check_id}"
                )
            component_supports[check_id].append(surface["id"])
        capabilities.append(
            {
                "id": surface["id"],
                "category": surface["category"],
                "business_criticality": "critical" if surface["required"] else "best_effort",
                "evidence_policy": "always" if surface["required"] else "impact_triggered",
                "component_ids": component_ids,
                "post_activation_checks": surface["post_update_checks"],
            }
        )
    contracts = [
        {
            "id": f"customization:{check['id']}",
            "kind": check["kind"],
            "evidence_refs": [check["id"]],
        }
        for check in checks
    ]
    components = [
        {
            "id": f"compatibility:{check['id']}",
            "roles": ["compatibility"],
            "application_phases": ["customization"],
            "artifacts": [
                {
                    "kind": "npm_archive_member",
                    "ref": f"{check['package']}:{check['member']}",
                }
            ],
            "contract_ids": [f"customization:{check['id']}"],
            "depends_on": [],
            "supports": component_supports[check["id"]],
            "governance": {},
        }
        for check in checks
    ]
    return parse_installation_contract(
        {
            "schema": INSTALLATION_CONTRACT_SCHEMA,
            "install_shape": coverage_profile["install_shape"],
            "runtime": coverage_profile["runtime"],
            "capabilities": capabilities,
            "components": components,
            "contracts": contracts,
        }
    )


def contract(args: argparse.Namespace) -> int:
    checks, customization_errors, _ = load_customizations(
        args.customizations.resolve(), False
    )
    coverage_profile, coverage_errors, _ = load_coverage(
        args.coverage.resolve(), False
    )
    errors = customization_errors + coverage_errors
    if errors:
        raise RehearsalError("; ".join(errors))
    document = adapt_v1_installation_contract(checks, coverage_profile)
    write_json(args.output.resolve(), document)
    print(args.output.resolve())
    return 0


EXTERNAL_ARTIFACT_RE = re.compile(
    r"^(?P<name>[A-Za-z0-9][A-Za-z0-9._/@+-]*)@"
    r"(?P<version>\d+\.\d+\.\d+(?:-[0-9A-Za-z.-]+)?(?:\+[0-9A-Za-z.-]+)?)"
    r"#sha256:(?P<digest>[0-9a-f]{64})$"
)


def canonical_installation_contract(value: Any) -> dict[str, Any]:
    contract = parse_installation_contract(value)
    capabilities = []
    for item in contract["capabilities"]:
        capabilities.append(
            {
                **item,
                "component_ids": sorted(item["component_ids"]),
                "post_activation_checks": sorted(item["post_activation_checks"]),
            }
        )
    components = []
    for item in contract["components"]:
        artifact_keys = [(artifact["kind"], artifact["ref"]) for artifact in item["artifacts"]]
        if not artifact_keys:
            raise RehearsalError(f"component {item['id']} has no artifacts")
        if len(artifact_keys) != len(set(artifact_keys)):
            raise RehearsalError(f"component {item['id']} has duplicate artifacts")
        components.append(
            {
                **item,
                "roles": sorted(item["roles"]),
                "application_phases": sorted(item["application_phases"]),
                "artifacts": sorted(
                    item["artifacts"], key=lambda artifact: (artifact["kind"], artifact["ref"])
                ),
                "contract_ids": sorted(item["contract_ids"]),
                "depends_on": sorted(
                    item["depends_on"],
                    key=lambda dependency: (
                        dependency["component_id"],
                        dependency["kind"],
                    ),
                ),
                "supports": sorted(item["supports"]),
            }
        )
    contracts = [
        {**item, "evidence_refs": sorted(item["evidence_refs"])}
        for item in contract["contracts"]
    ]
    return {
        **contract,
        "capabilities": sorted(capabilities, key=lambda item: item["id"]),
        "components": sorted(components, key=lambda item: item["id"]),
        "contracts": sorted(contracts, key=lambda item: item["id"]),
    }


def lock_component_artifact(
    artifact: dict[str, str],
    lane: str,
    metadata: dict[str, Any],
    closure: dict[str, Any],
) -> dict[str, Any]:
    kind = artifact["kind"]
    reference = artifact["ref"]
    if kind == "npm_package":
        candidates = [
            item
            for item in closure["packages"]
            if item["name"] == reference and item["selected_for_platform"]
        ]
        if len(candidates) != 1:
            raise RehearsalError(
                f"artifact {reference} does not resolve to one selected core package"
            )
        item = candidates[0]
        return {
            "kind": kind,
            "ref": reference,
            "identity": f"{item['name']}@{item['version']}",
            "integrity": item["integrity"],
        }
    if kind == "npm_archive_member":
        if ":" not in reference:
            raise RehearsalError(f"archive member artifact is malformed: {reference}")
        package_name, member = reference.split(":", 1)
        if (
            not PACKAGE_RE.fullmatch(package_name)
            or not member
            or PurePosixPath(member).is_absolute()
            or ".." in PurePosixPath(member).parts
        ):
            raise RehearsalError(f"archive member artifact is unsafe: {reference}")
        root_package = closure["root_package"]
        if package_name != root_package["name"]:
            raise RehearsalError(
                f"archive member package is outside the core closure root: {package_name}"
            )
        candidates = [
            item
            for item in closure["packages"]
            if item["name"] == package_name
            and item["version"] == root_package["version"]
            and item["selected_for_platform"]
        ]
        if len(candidates) != 1:
            raise RehearsalError(
                f"archive member package does not resolve to one core package: {package_name}"
            )
        package = candidates[0]
        return {
            "kind": kind,
            "ref": reference,
            "identity": f"{package_name}@{package['version']}:{member}",
            "integrity": package["integrity"],
        }
    if kind in {
        "plugin_package",
        "sidecar",
        "addon",
        "external_asset",
        "configuration_identity",
        "personalization_contract",
    }:
        match = EXTERNAL_ARTIFACT_RE.fullmatch(reference)
        if match is None:
            raise RehearsalError(
                f"external artifact must pin exact version and sha256: {reference}"
            )
        return {
            "kind": kind,
            "ref": reference,
            "identity": f"{match.group('name')}@{match.group('version')}",
            "integrity": f"sha256:{match.group('digest')}",
        }
    raise RehearsalError(f"unsupported installation artifact kind: {kind}")


def compose_installation_candidate(
    lane: str,
    metadata: dict[str, Any],
    installation_contract: dict[str, Any],
) -> dict[str, Any]:
    candidate = metadata.get("core_candidate")
    if not isinstance(candidate, dict):
        raise RehearsalError("core candidate closure is unavailable")
    closure = validate_core_closure(
        candidate.get(lane),
        "openclaw",
        str(metadata.get(f"{lane}_version", "")),
    )
    canonical_contract = canonical_installation_contract(installation_contract)
    contracts_by_id = {item["id"]: item for item in canonical_contract["contracts"]}
    components: list[dict[str, Any]] = []
    for component in canonical_contract["components"]:
        artifacts = [
            lock_component_artifact(item, lane, metadata, closure)
            for item in component["artifacts"]
        ]
        artifacts.sort(key=lambda item: (item["kind"], item["identity"], item["ref"]))
        contract_locks = [
            {
                "id": contract_id,
                "digest": canonical_digest(contracts_by_id[contract_id]),
            }
            for contract_id in sorted(component["contract_ids"])
        ]
        components.append(
            {
                "id": component["id"],
                "roles": sorted(component["roles"]),
                "application_phases": sorted(component["application_phases"]),
                "artifacts": artifacts,
                "contracts": contract_locks,
                "depends_on": sorted(
                    component["depends_on"],
                    key=lambda item: (item["component_id"], item["kind"]),
                ),
                "supports": sorted(component["supports"]),
                "governance_digest": canonical_digest(component["governance"]),
            }
        )
    components.sort(key=lambda item: item["id"])
    content = {
        "schema": "openclaw.safe_update.installation_candidate.v1",
        "lane": lane,
        "core_root": closure["root"],
        "installation_contract_digest": canonical_digest(canonical_contract),
        "composition_policy_version": INSTALLATION_COMPOSITION_POLICY_VERSION,
        "analyzer_version": CORE_CLOSURE_ANALYZER_VERSION,
        "environment": closure["environment"],
        "components": components,
    }
    return {**content, "root": canonical_digest(content)}


def build_installation_candidate_lock(
    metadata: Any,
    installation_contract: Any,
    common: dict[str, Any],
) -> tuple[dict[str, Any], str]:
    errors: list[str] = []
    current: dict[str, Any] = {}
    target: dict[str, Any] = {}
    try:
        if not isinstance(metadata, dict):
            raise RehearsalError("input metadata is unavailable")
        parsed_contract = canonical_installation_contract(installation_contract)
        current = compose_installation_candidate("current", metadata, parsed_contract)
        target = compose_installation_candidate("target", metadata, parsed_contract)
    except (KeyError, RehearsalError) as exc:
        errors.append(str(exc))
    status = "failed" if errors else "success"
    return {
        "schema": INSTALLATION_CANDIDATE_LOCK_SCHEMA,
        **common,
        "status": status,
        "current_root": current.get("root"),
        "target_root": target.get("root"),
        "current": current or None,
        "target": target or None,
        "errors": errors,
    }, status


def parse_utc_timestamp(value: Any, field: str) -> datetime:
    if not isinstance(value, str) or not value:
        raise RehearsalError(f"{field} must be a non-empty timestamp")
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError as exc:
        raise RehearsalError(f"{field} is not a valid timestamp") from exc
    if parsed.tzinfo is None:
        raise RehearsalError(f"{field} must include a timezone")
    return parsed.astimezone(timezone.utc)


def read_regular_file_digest(path: Path) -> tuple[str, str]:
    flags = os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0)
    try:
        descriptor = os.open(path, flags)
    except OSError as exc:
        raise RehearsalError(f"cannot open observed file: {path.name}") from exc
    try:
        metadata = os.fstat(descriptor)
        if not stat.S_ISREG(metadata.st_mode):
            raise RehearsalError(f"observed content is not a regular file: {path.name}")
        digest = hashlib.sha256()
        with os.fdopen(descriptor, "rb", closefd=False) as handle:
            for chunk in iter(lambda: handle.read(1024 * 1024), b""):
                digest.update(chunk)
        return "file", "sha256:" + digest.hexdigest()
    finally:
        os.close(descriptor)


def observed_path_type(path: Path) -> str:
    try:
        metadata = path.lstat()
    except OSError as exc:
        raise RehearsalError(f"cannot inspect observed path: {path.name}") from exc
    if stat.S_ISREG(metadata.st_mode):
        return "file"
    if stat.S_ISDIR(metadata.st_mode):
        return "directory"
    raise RehearsalError(f"observed path has unsupported type: {path.name}")


def parse_observation_spec(value: Any) -> dict[str, Any]:
    if (
        not isinstance(value, dict)
        or value.get("schema") != INSTALLATION_OBSERVATION_SCHEMA
        or set(value) != {"schema", "components", "services"}
        or not isinstance(value.get("components"), list)
        or not isinstance(value.get("services"), list)
    ):
        raise RehearsalError("installation observation spec is invalid")
    component_keys: set[tuple[str, str]] = set()
    for item in value["components"]:
        if (
            not isinstance(item, dict)
            or set(item)
            != {"component_id", "artifact_ref", "name", "path", "mode"}
            or not isinstance(item.get("component_id"), str)
            or not item["component_id"]
            or not isinstance(item.get("artifact_ref"), str)
            or not item["artifact_ref"]
            or not isinstance(item.get("name"), str)
            or not SAFE_OBSERVATION_NAME_RE.fullmatch(item["name"])
            or not isinstance(item.get("path"), str)
            or not item["path"]
            or item.get("mode") not in {"content_sha256", "identity_only"}
        ):
            raise RehearsalError("installation observation component is invalid")
        key = (item["component_id"], item["artifact_ref"])
        if key in component_keys:
            raise RehearsalError("installation observation has duplicate components")
        component_keys.add(key)
    service_names: set[str] = set()
    for item in value["services"]:
        if (
            not isinstance(item, dict)
            or set(item) != {"name", "path"}
            or not isinstance(item.get("name"), str)
            or not SAFE_OBSERVATION_NAME_RE.fullmatch(item["name"])
            or item["name"] in service_names
            or not isinstance(item.get("path"), str)
            or not item["path"]
        ):
            raise RehearsalError("installation observation service is invalid or duplicate")
        service_names.add(item["name"])
    return value


def read_service_config_pointers(path: Path) -> list[str]:
    flags = os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0)
    try:
        descriptor = os.open(path, flags)
    except OSError as exc:
        raise RehearsalError(f"cannot open observed service unit: {path.name}") from exc
    pointers: list[str] = []
    total = 0
    try:
        metadata = os.fstat(descriptor)
        if not stat.S_ISREG(metadata.st_mode):
            raise RehearsalError(f"observed service unit is not a regular file: {path.name}")
        with os.fdopen(descriptor, "rb", closefd=False) as handle:
            for raw_line in handle:
                total += len(raw_line)
                if total > MAX_SERVICE_UNIT_BYTES:
                    raise RehearsalError(
                        f"observed service unit exceeds size limit: {path.name}"
                    )
                stripped = raw_line.strip()
                if not stripped.startswith(SERVICE_POINTER_DIRECTIVES):
                    continue
                try:
                    line = stripped.decode("utf-8")
                except UnicodeDecodeError as exc:
                    raise RehearsalError(
                        f"observed service pointer line is not UTF-8: {path.name}"
                    ) from exc
                pointers.extend(
                    match.group("path") for match in SERVICE_POINTER_RE.finditer(line)
                )
                environment_file = ENVIRONMENT_FILE_RE.fullmatch(line)
                if environment_file is not None:
                    pointers.append(environment_file.group("path"))
    finally:
        os.close(descriptor)
    return pointers


def build_installation_attestation(
    candidate_lock: Any,
    observation_spec: Any,
    *,
    generated_at: str,
    ttl_seconds: int,
) -> dict[str, Any]:
    errors: list[str] = []
    residue: list[dict[str, str]] = []
    observed_components: list[dict[str, str]] = []
    observed_services: list[dict[str, Any]] = []
    missing: list[dict[str, str]] = []
    current_root: str | None = None
    try:
        if (
            not isinstance(candidate_lock, dict)
            or candidate_lock.get("schema") != INSTALLATION_CANDIDATE_LOCK_SCHEMA
            or candidate_lock.get("status") != "success"
            or not isinstance(candidate_lock.get("current"), dict)
            or not re.fullmatch(
                r"sha256:[0-9a-f]{64}",
                str(candidate_lock.get("current_root", "")),
            )
        ):
            raise RehearsalError("current installation candidate lock is unavailable")
        current_root = candidate_lock["current_root"]
        spec = parse_observation_spec(observation_spec)
        candidates: dict[tuple[str, str], dict[str, Any]] = {}
        required_external: set[tuple[str, str]] = set()
        for component in candidate_lock["current"].get("components", []):
            component_id = component.get("id")
            for artifact in component.get("artifacts", []):
                key = (component_id, artifact.get("ref"))
                candidates[key] = artifact
                if artifact.get("kind") in (
                    ATTESTATION_CONTENT_KINDS | ATTESTATION_IDENTITY_KINDS
                ):
                    required_external.add(key)

        observed_keys: set[tuple[str, str]] = set()
        configuration_paths: dict[str, str] = {}
        for item in spec["components"]:
            key = (item["component_id"], item["artifact_ref"])
            artifact = candidates.get(key)
            path = Path(item["path"]).expanduser()
            if artifact is None:
                residue.append(
                    {
                        "kind": "undeclared_component",
                        "name": item["name"],
                        "component_id": item["component_id"],
                    }
                )
                continue
            artifact_kind = artifact["kind"]
            if item["mode"] == "content_sha256":
                if artifact_kind not in ATTESTATION_CONTENT_KINDS:
                    raise RehearsalError(
                        f"content hashing is not allowed for {artifact_kind}"
                    )
                path_type, digest = read_regular_file_digest(path)
                status = "success" if digest == artifact["integrity"] else "failed"
                if status == "failed":
                    residue.append(
                        {
                            "kind": "artifact_integrity_mismatch",
                            "name": item["name"],
                            "component_id": item["component_id"],
                        }
                    )
            else:
                if artifact_kind not in ATTESTATION_IDENTITY_KINDS:
                    raise RehearsalError(
                        f"identity-only observation is not allowed for {artifact_kind}"
                    )
                path_type = observed_path_type(path)
                digest = canonical_digest(
                    {
                        "component_id": item["component_id"],
                        "artifact_ref": item["artifact_ref"],
                        "name": item["name"],
                        "type": path_type,
                    }
                )
                status = "success"
                if artifact_kind == "configuration_identity":
                    configuration_paths[os.path.abspath(path)] = item["component_id"]
            observed_keys.add(key)
            observed_components.append(
                {
                    "component_id": item["component_id"],
                    "artifact_ref": item["artifact_ref"],
                    "name": item["name"],
                    "type": path_type,
                    "mode": item["mode"],
                    "digest": digest,
                    "status": status,
                }
            )

        for component_id, artifact_ref in sorted(required_external - observed_keys):
            missing.append(
                {
                    "component_id": component_id,
                    "artifact_ref": artifact_ref,
                }
            )

        for service in spec["services"]:
            pointers = read_service_config_pointers(Path(service["path"]).expanduser())
            pointer_results: list[dict[str, Any]] = []
            for pointer in pointers:
                pointer_name = Path(pointer).name
                if not SAFE_OBSERVATION_NAME_RE.fullmatch(pointer_name):
                    raise RehearsalError(
                        f"service {service['name']} contains an unsafe config pointer"
                    )
                component_id = configuration_paths.get(os.path.abspath(pointer))
                declared = component_id is not None
                pointer_results.append(
                    {
                        "name": pointer_name,
                        "declared": declared,
                        "component_id": component_id,
                    }
                )
                if not declared:
                    residue.append(
                        {
                            "kind": "undeclared_generated_config",
                            "name": pointer_name,
                            "component_id": "",
                        }
                    )
            pointer_results.sort(key=lambda item: item["name"])
            observed_services.append(
                {
                    "name": service["name"],
                    "type": "service_unit",
                    "config_pointers": pointer_results,
                    "digest": canonical_digest(
                        {
                            "name": service["name"],
                            "config_pointers": pointer_results,
                        }
                    ),
                }
            )
    except (KeyError, OSError, RehearsalError) as exc:
        errors.append(str(exc))

    observed_components.sort(
        key=lambda item: (item["component_id"], item["artifact_ref"])
    )
    observed_services.sort(key=lambda item: item["name"])
    residue.sort(key=lambda item: (item["kind"], item["name"], item["component_id"]))
    observation_status = "failed" if errors else "success"
    completeness_status = (
        "unknown"
        if errors
        else "incomplete"
        if residue or missing
        else "complete"
    )
    freshness_status = "unknown" if current_root is None else "fresh"
    content = {
        "candidate_root": current_root,
        "observed_components": observed_components,
        "observed_services": observed_services,
        "missing": missing,
        "residue": residue,
    }
    status = (
        "success"
        if observation_status == "success"
        and freshness_status == "fresh"
        and completeness_status == "complete"
        else "failed"
    )
    generated = parse_utc_timestamp(generated_at, "generated_at")
    return {
        "schema": INSTALLATION_ATTESTATION_SCHEMA,
        "generated_at": generated_at,
        "expires_at": (
            generated + timedelta(seconds=ttl_seconds)
        ).replace(microsecond=0).isoformat(),
        "effect": "read_only_local_installation_attestation",
        "runtime_effect": "none",
        "external_effect": "none",
        "external_write_effect": "none",
        "production_apply_allowed": False,
        "operator_approval": False,
        "status": status,
        "axes": {
            "observation": observation_status,
            "freshness": freshness_status,
            "completeness": completeness_status,
        },
        "attestation_content": content,
        "attestation_digest": canonical_digest(content),
        "errors": errors,
    }


def failed_installation_attestation(
    generated_at: str,
    candidate_root: str | None,
) -> dict[str, Any]:
    content = {
        "candidate_root": candidate_root,
        "observed_components": [],
        "observed_services": [],
        "missing": [],
        "residue": [],
    }
    return {
        "schema": INSTALLATION_ATTESTATION_SCHEMA,
        "generated_at": generated_at,
        "expires_at": generated_at,
        "effect": "read_only_local_installation_attestation",
        "runtime_effect": "none",
        "external_effect": "none",
        "external_write_effect": "none",
        "production_apply_allowed": False,
        "operator_approval": False,
        "status": "failed",
        "axes": {
            "observation": "failed",
            "freshness": "unknown",
            "completeness": "unknown",
        },
        "attestation_content": content,
        "attestation_digest": canonical_digest(content),
        "errors": [
            "installation attestation is missing, stale, incomplete, or invalid"
        ],
    }


def parse_installation_attestation(
    value: Any,
    *,
    expected_candidate: dict[str, Any] | None,
    checked_at: str,
) -> dict[str, Any]:
    required_fields = {
        "schema",
        "generated_at",
        "expires_at",
        "effect",
        "runtime_effect",
        "external_effect",
        "external_write_effect",
        "production_apply_allowed",
        "operator_approval",
        "status",
        "axes",
        "attestation_content",
        "attestation_digest",
        "errors",
    }
    if (
        not isinstance(value, dict)
        or value.get("schema") != INSTALLATION_ATTESTATION_SCHEMA
        or set(value) != required_fields
    ):
        raise RehearsalError("installation attestation is invalid")
    invariants = {
        "effect": "read_only_local_installation_attestation",
        "runtime_effect": "none",
        "external_effect": "none",
        "external_write_effect": "none",
        "production_apply_allowed": False,
        "operator_approval": False,
    }
    if any(value.get(field) != expected for field, expected in invariants.items()):
        raise RehearsalError("installation attestation safety invariant failed")
    axes = value.get("axes")
    if (
        not isinstance(axes, dict)
        or set(axes) != {"observation", "freshness", "completeness"}
        or axes.get("observation") not in {"success", "failed"}
        or axes.get("freshness") not in {"fresh", "stale", "unknown"}
        or axes.get("completeness") not in {"complete", "incomplete", "unknown"}
    ):
        raise RehearsalError("installation attestation axes are invalid")
    content = value.get("attestation_content")
    if not isinstance(content, dict) or set(content) != {
        "candidate_root",
        "observed_components",
        "observed_services",
        "missing",
        "residue",
    }:
        raise RehearsalError("installation attestation content is invalid")
    if not isinstance(expected_candidate, dict):
        raise RehearsalError("installation candidate is unavailable for attestation")
    if value.get("attestation_digest") != canonical_digest(content):
        raise RehearsalError("installation attestation digest does not match content")
    expected_candidate_root = (
        expected_candidate.get("root") if isinstance(expected_candidate, dict) else None
    )
    if content.get("candidate_root") != expected_candidate_root:
        raise RehearsalError("installation attestation candidate root is stale")
    expected_external = {
        (component["id"], artifact["ref"])
        for component in (expected_candidate or {}).get("components", [])
        for artifact in component.get("artifacts", [])
        if artifact.get("kind") in (
            ATTESTATION_CONTENT_KINDS | ATTESTATION_IDENTITY_KINDS
        )
    }
    observed_components = content.get("observed_components")
    if not isinstance(observed_components, list) or any(
        not isinstance(item, dict)
        or item.get("status") != "success"
        or not isinstance(item.get("component_id"), str)
        or not isinstance(item.get("artifact_ref"), str)
        for item in observed_components
    ):
        raise RehearsalError("installation attestation component observations are invalid")
    observed_external = {
        (item["component_id"], item["artifact_ref"]) for item in observed_components
    }
    if observed_external != expected_external:
        raise RehearsalError("installation attestation does not cover external artifacts")
    if content.get("missing") != [] or content.get("residue") != []:
        raise RehearsalError("installation attestation contains unresolved residue")
    observed_services = content.get("observed_services")
    if not isinstance(observed_services, list) or any(
        not isinstance(service, dict)
        or any(
            not isinstance(pointer, dict) or pointer.get("declared") is not True
            for pointer in service.get("config_pointers", [])
        )
        for service in observed_services
    ):
        raise RehearsalError("installation attestation service observations are invalid")
    if parse_utc_timestamp(value["expires_at"], "expires_at") <= parse_utc_timestamp(
        checked_at, "checked_at"
    ):
        raise RehearsalError("installation attestation has expired")
    if (
        value.get("status") != "success"
        or axes != {
            "observation": "success",
            "freshness": "fresh",
            "completeness": "complete",
        }
        or value.get("errors") != []
    ):
        raise RehearsalError("installation attestation is not complete and fresh")
    return value


def attest(args: argparse.Namespace) -> int:
    if args.ttl_seconds <= 0:
        raise RehearsalError("attestation ttl must be positive")
    generated_at = now_iso()
    candidate_lock = read_json(args.candidate_lock.resolve())
    observation_spec = read_json(args.observation.resolve())
    document = build_installation_attestation(
        candidate_lock,
        observation_spec,
        generated_at=generated_at,
        ttl_seconds=args.ttl_seconds,
    )
    write_json(args.output.resolve(), document)
    print(args.output.resolve())
    return 0 if document["status"] == "success" else 2


def artifact_reference(path: Path, status: str) -> dict[str, Any]:
    return {"path": path.name, "sha256": digest_file(path), "status": status}


def analyze_archive_command(args: argparse.Namespace) -> int:
    try:
        metadata = json.loads(args.metadata_json)
    except json.JSONDecodeError as exc:
        raise RehearsalError(f"invalid archive metadata JSON: {exc}") from exc
    if not isinstance(metadata, dict):
        raise RehearsalError("archive metadata must be an object")
    result = analyze_archive_unit(
        {
            "task_id": args.task_id,
            "name": args.package,
            "lane": args.lane,
            "path": args.path.resolve(),
            "metadata": metadata,
        },
        args.cache_dir.resolve() if args.cache_dir else None,
    )
    print(json.dumps(result, ensure_ascii=True, separators=(",", ":"), sort_keys=True))
    return 0


def simulate(args: argparse.Namespace) -> int:
    input_dir = args.input_dir.resolve()
    output_dir = args.output_dir.resolve()
    output_dir.mkdir(parents=True, exist_ok=True)
    metadata_path = input_dir / "input-metadata.json"
    generated_at = now_iso()
    common = {"generated_at": generated_at, **safety_fields()}
    cache_dir = args.cache_dir.resolve() if args.cache_dir else None
    cache_provenance: list[dict[str, str]] = []
    runtime_errors: list[str] = []
    package_results: list[dict[str, Any]] = []
    authority_packages: list[dict[str, Any]] = []
    authority_complete = True
    target_archives: dict[str, tuple[Path, dict[str, Any], dict[str, Any]]] = {}
    coverage_profile, coverage_errors, coverage_mode = load_coverage(
        args.coverage.resolve() if args.coverage else None,
        args.allow_no_coverage,
    )
    if coverage_mode == "explicitly_not_required":
        runtime_arguments = {
            "node_version": args.runtime_node_version,
            "os": args.runtime_os,
            "arch": args.runtime_arch,
            "libc": args.runtime_libc,
        }
        if (
            not isinstance(args.runtime_node_version, str)
            or semver_tuple(args.runtime_node_version) is None
        ):
            coverage_errors.append(
                "--runtime-node-version is required when --allow-no-coverage is used"
            )
        for field in ("os", "arch", "libc"):
            value = runtime_arguments[field]
            if not isinstance(value, str) or not value or value == "unknown":
                coverage_errors.append(
                    f"--runtime-{field} is required when --allow-no-coverage is used"
                )
        coverage_profile["runtime"].update(runtime_arguments)
    runtime_node_version = coverage_profile.get("runtime", {}).get("node_version")

    try:
        metadata = read_json(metadata_path)
    except RehearsalError as exc:
        metadata = {}
        runtime_errors.append(str(exc))
    if not isinstance(metadata, dict) or metadata.get("schema") != INPUT_SCHEMA:
        runtime_errors.append(f"input schema must be {INPUT_SCHEMA}")
    core_candidate_lock, core_candidate_status = build_core_candidate_lock(
        metadata,
        coverage_profile.get("runtime", {}),
        common,
    )
    packages = metadata.get("packages") if isinstance(metadata, dict) else None
    if not isinstance(packages, list) or not packages:
        runtime_errors.append("input metadata must contain packages")
        packages = []

    seen_packages: set[str] = set()
    prepared_packages: list[dict[str, Any] | None] = []
    archive_tasks: list[dict[str, Any]] = []
    for package_index, entry in enumerate(packages):
        package_result: dict[str, Any] = {"status": "failed", "errors": []}
        try:
            if not isinstance(entry, dict) or not isinstance(entry.get("name"), str):
                raise RehearsalError("package metadata entry is invalid")
            name = entry["name"]
            package_result["name"] = name
            if name in seen_packages:
                raise RehearsalError(f"duplicate package metadata: {name}")
            seen_packages.add(name)
            current_metadata = entry.get("current")
            target_metadata = entry.get("target")
            if not isinstance(current_metadata, dict) or not isinstance(target_metadata, dict):
                raise RehearsalError(f"package metadata is incomplete for {name}")
            if current_metadata.get("name") != name or target_metadata.get("name") != name:
                raise RehearsalError(f"package metadata name mismatch for {name}")
            current_path = archive_path(input_dir, "current", current_metadata)
            target_path = archive_path(input_dir, "target", target_metadata)
            prepared_packages.append(
                {
                    "name": name,
                    "current_metadata": current_metadata,
                    "target_metadata": target_metadata,
                    "current_path": current_path,
                    "target_path": target_path,
                }
            )
            for lane, path, package_metadata in (
                ("current", current_path, current_metadata),
                ("target", target_path, target_metadata),
            ):
                archive_tasks.append(
                    {
                        "task_id": f"{package_index}:{name}:{lane}",
                        "package_index": package_index,
                        "name": name,
                        "lane": lane,
                        "path": path,
                        "metadata": package_metadata,
                    }
                )
        except (KeyError, RehearsalError, OSError) as exc:
            authority_complete = False
            package_result["errors"].append(str(exc))
            prepared_packages.append(None)
        package_results.append(package_result)

    archive_results: list[dict[str, Any]] = []
    try:
        archive_results = execute_archive_analyses(
            archive_tasks,
            cache_dir=cache_dir,
            workers=args.archive_workers,
            timeout_seconds=args.archive_timeout_seconds,
        )
    except RehearsalError as exc:
        runtime_errors.append(str(exc))
        authority_complete = False
    archive_result_by_id = {
        result["task_id"]: result
        for result in archive_results
    }
    for result in archive_results:
        cache_provenance.extend(result["cache_provenance"])

    for package_index, prepared in enumerate(prepared_packages):
        if prepared is None:
            continue
        package_result = package_results[package_index]
        name = prepared["name"]
        current_metadata = prepared["current_metadata"]
        target_metadata = prepared["target_metadata"]
        current_path = prepared["current_path"]
        target_path = prepared["target_path"]
        try:
            current_result = archive_result_by_id.get(
                f"{package_index}:{name}:current"
            )
            target_result = archive_result_by_id.get(
                f"{package_index}:{name}:target"
            )
            if current_result is None or target_result is None:
                raise RehearsalError(f"archive analysis result is missing for {name}")
            if current_result["status"] != "success":
                raise RehearsalError(current_result["error"])
            if target_result["status"] != "success":
                raise RehearsalError(target_result["error"])
            current_inspection = current_result["inspection"]
            target_inspection = target_result["inspection"]
            package_metadata = compare_package_metadata(
                current_inspection["package_json"],
                target_inspection["package_json"],
                runtime_node_version,
            )
            authority_packages.append(
                {
                    "name": name,
                    "archive_diff": authority_archive_diff(
                        current_inspection,
                        target_inspection,
                    ),
                    "metadata_changed_fields": package_metadata["changed_fields"],
                    "risk_findings": package_metadata["risk_findings"],
                }
            )
            blocking_findings = [
                finding
                for finding in package_metadata["risk_findings"]
                if finding.get("severity") == "blocked"
            ]
            package_result.update(
                {
                    "current_version": current_metadata["version"],
                    "target_version": target_metadata["version"],
                    "current_archive_sha256": digest_file(current_path),
                    "target_archive_sha256": digest_file(target_path),
                    "registry": {
                        "current": {
                            "integrity": current_metadata["integrity"],
                            "shasum": current_metadata["shasum"],
                        },
                        "target": {
                            "integrity": target_metadata["integrity"],
                            "shasum": target_metadata["shasum"],
                        },
                    },
                    "diff": compare_archives(current_inspection, target_inspection),
                    "package_metadata": package_metadata,
                    "status": "failed" if blocking_findings else "success",
                }
            )
            target_archives[name] = (target_path, target_inspection, target_metadata)
            package_result["errors"].extend(finding["detail"] for finding in blocking_findings)
        except (KeyError, RehearsalError, OSError, tarfile.TarError) as exc:
            authority_complete = False
            package_result["errors"].append(str(exc))

    runtime_status = (
        "success"
        if not runtime_errors and package_results and all(item["status"] == "success" for item in package_results)
        else "failed"
    )
    synthetic_status = "success" if package_results and all(item["status"] == "success" for item in package_results) else "failed"
    runtime_truth = {
        "schema": "openclaw.safe_update.runtime_truth.v1",
        **common,
        "status": runtime_status,
        "current_version": metadata.get("current_version"),
        "target_version": metadata.get("target_version"),
        "packages": [
            {
                "name": item.get("name"),
                "current_version": item.get("current_version"),
                "target_version": item.get("target_version"),
                "status": item["status"],
            }
            for item in package_results
        ],
        "errors": runtime_errors,
    }
    synthetic = {
        "schema": "openclaw.safe_update.synthetic_update.v1",
        **common,
        "status": synthetic_status,
        "packages": package_results,
    }

    checks, customization_errors, customization_mode = load_customizations(
        args.customizations.resolve() if args.customizations else None,
        args.allow_no_customizations,
    )
    check_results: list[dict[str, Any]] = []
    for check in checks:
        result = {key: check[key] for key in ("id", "package", "kind", "member")}
        result["status"] = "failed"
        result["reason"] = None
        archive_record = target_archives.get(check["package"])
        if archive_record is None:
            result["reason"] = "target package evidence is unavailable"
        elif check["member"] not in archive_record[1]["file_hashes"]:
            result["reason"] = "required member is missing"
        elif check["kind"] == "required_member":
            result["status"] = "success"
        else:
            try:
                text = read_archive_text(archive_record[0], check["member"])
                if check["needle"] in text:
                    result["status"] = "success"
                else:
                    result["reason"] = "required text anchor is missing"
            except (RehearsalError, OSError, tarfile.TarError) as exc:
                result["reason"] = str(exc)
        check_results.append(result)

    for name, (archive_path_value, _inspection, archive_metadata) in target_archives.items():
        if (
            integrity_for(archive_path_value) != archive_metadata.get("integrity")
            or digest_file(archive_path_value, "sha1") != archive_metadata.get("shasum")
        ):
            customization_errors.append(f"target archive changed during customization checks: {name}")

    customization_status = (
        "success"
        if not customization_errors and all(item["status"] == "success" for item in check_results)
        else "failed"
    )
    customizations = {
        "schema": "openclaw.safe_update.customization_compatibility.v1",
        **common,
        "status": customization_status,
        "mode": customization_mode,
        "checks": check_results,
        "errors": customization_errors,
    }

    customization_results_by_id = {item["id"]: item["status"] for item in check_results}
    known_customization_ids = set(customization_results_by_id)
    coverage_surface_results: list[dict[str, Any]] = []
    for surface in coverage_profile["surfaces"]:
        surface_errors: list[str] = []
        for check_id in surface["customization_checks"]:
            if check_id not in known_customization_ids:
                surface_errors.append(f"referenced customization check is missing: {check_id}")
            elif customization_results_by_id[check_id] != "success":
                surface_errors.append(f"referenced customization check failed: {check_id}")
        coverage_surface_results.append(
            {
                **surface,
                "status": "failed" if surface_errors else "success",
                "errors": surface_errors,
            }
        )
        coverage_errors.extend(f"surface {surface['id']}: {error}" for error in surface_errors)
    coverage_status = (
        "success"
        if not coverage_errors and all(item["status"] == "success" for item in coverage_surface_results)
        else "failed"
    )
    coverage_report = {
        "schema": "openclaw.safe_update.coverage_report.v1",
        **common,
        "status": coverage_status,
        "mode": coverage_mode,
        "install_shape": coverage_profile["install_shape"],
        "runtime": coverage_profile["runtime"],
        "surfaces": coverage_surface_results,
        "errors": coverage_errors,
    }
    installation_contract_errors: list[str] = []
    installation_contract: dict[str, Any] = {}
    try:
        if args.installation_contract:
            raw_installation_contract = read_json(
                args.installation_contract.resolve()
            )
        else:
            raw_installation_contract = adapt_v1_installation_contract(
                checks,
                coverage_profile,
            )
        installation_contract = cached_analysis(
            cache_dir=cache_dir,
            namespace="contract",
            key_material=raw_installation_contract,
            provenance=cache_provenance,
            build=lambda: canonical_installation_contract(
                raw_installation_contract
            ),
        )
    except RehearsalError as exc:
        installation_contract_errors.append(str(exc))
    if installation_contract_errors:
        installation_candidate_lock = {
            "schema": INSTALLATION_CANDIDATE_LOCK_SCHEMA,
            **common,
            "status": "failed",
            "current_root": None,
            "target_root": None,
            "current": None,
            "target": None,
            "errors": installation_contract_errors,
        }
        installation_candidate_status = "failed"
    else:
        (
            installation_candidate_lock,
            installation_candidate_status,
        ) = build_installation_candidate_lock(
            metadata,
            installation_contract,
            common,
        )
    installation_attestation_status = "failed"
    installation_attestation = failed_installation_attestation(
        generated_at,
        installation_candidate_lock.get("current_root"),
    )
    if args.installation_attestation:
        try:
            installation_attestation = parse_installation_attestation(
                read_json(args.installation_attestation.resolve()),
                expected_candidate=installation_candidate_lock.get("current"),
                checked_at=generated_at,
            )
            installation_attestation_status = "success"
        except RehearsalError:
            pass
    conservative_inputs = empty_conservative_inputs()
    conservative_input_errors: list[str] = []
    if args.conservative_inputs:
        try:
            conservative_inputs = parse_conservative_inputs(
                read_json(args.conservative_inputs.resolve())
            )
        except RehearsalError as exc:
            conservative_input_errors.append(str(exc))
            authority_complete = False
    machine_conditions = cached_analysis(
        cache_dir=cache_dir,
        namespace="policy",
        key_material={
            "core_candidate_lock": deterministic_analysis_value(
                core_candidate_lock
            ),
            "installation_attestation_status": installation_attestation_status,
            "authority_packages": authority_packages,
            "authority_complete": authority_complete,
        },
        provenance=cache_provenance,
        build=lambda: conservative_machine_conditions(
            core_candidate_lock=core_candidate_lock,
            installation_attestation_status=installation_attestation_status,
            authority_packages=authority_packages,
            authority_complete=authority_complete,
        ),
        validate=lambda payload: (
            isinstance(payload, dict)
            and set(payload) == CONSERVATIVE_CONDITION_IDS
            and all(isinstance(value, bool) for value in payload.values())
        ),
    )
    conservative_gates, conservative_gate_status = evaluate_conservative_gates(
        core_candidate_lock=core_candidate_lock,
        installation_attestation_status=installation_attestation_status,
        authority_packages=authority_packages,
        authority_complete=authority_complete,
        inputs=conservative_inputs,
        common=common,
        input_errors=conservative_input_errors,
        machine_conditions=machine_conditions,
    )
    impact_shadow = None
    if not args.disable_impact_shadow:
        shadow_payload = cached_analysis(
            cache_dir=cache_dir,
            namespace="shadow",
            key_material={
                "authority_packages": authority_packages,
                "core_candidate_lock": deterministic_analysis_value(
                    core_candidate_lock
                ),
                "installation_contract": installation_contract,
                "baseline_check_ids": sorted(item["id"] for item in checks),
                "authority_complete": authority_complete,
            },
            provenance=cache_provenance,
            build=lambda: {
                key: value
                for key, value in build_impact_shadow(
                    authority_packages=authority_packages,
                    core_candidate_lock=core_candidate_lock,
                    installation_contract=installation_contract,
                    baseline_check_ids={item["id"] for item in checks},
                    authority_complete=authority_complete,
                    common=common,
                ).items()
                if key not in {"schema", *VOLATILE_ANALYSIS_FIELDS}
            },
        )
        impact_shadow = {
            "schema": IMPACT_SHADOW_SCHEMA,
            **common,
            **shadow_payload,
        }
    normalized_conservative_inputs = {
        "satisfied_gates": [
            {"id": gate_id, "evidence_digest": digest}
            for gate_id, digest in sorted(
                conservative_inputs["satisfied_gates"].items()
            )
        ],
        "operator_escalations": sorted(
            conservative_inputs["operator_escalations"]
        ),
    }
    rehearsal_input = build_rehearsal_input(
        candidate_roots={
            "current": installation_candidate_lock.get("current_root"),
            "target": installation_candidate_lock.get("target_root"),
        },
        installation_contract=installation_contract,
        installation_attestation=installation_attestation,
        conservative_inputs=normalized_conservative_inputs,
        authoritative_analysis={
            "core_candidate_lock": deterministic_analysis_value(
                core_candidate_lock
            ),
            "authority_packages": authority_packages,
            "coverage_profile": coverage_profile,
            "customization_checks": checks,
        },
        options={
            "allow_no_customizations": bool(args.allow_no_customizations),
            "allow_no_coverage": bool(args.allow_no_coverage),
            "impact_shadow_enabled": not args.disable_impact_shadow,
            "coverage_mode": coverage_mode,
            "customization_mode": customization_mode,
        },
    )
    analysis_cache_report = {
        "schema": ANALYSIS_CACHE_SCHEMA,
        **common,
        "authoritative": False,
        "cache_enabled": cache_dir is not None,
        "rehearsal_input_digest": canonical_digest(rehearsal_input),
        "analyzer_version": ANALYZER_VERSION,
        "policy_version": DETERMINISTIC_POLICY_VERSION,
        "entries": cache_provenance,
        "counts": {
            result: sum(
                1 for item in cache_provenance if item["result"] == result
            )
            for result in ("hit", "miss", "ignored", "disabled")
        },
    }
    archive_execution_report = {
        "schema": ARCHIVE_EXECUTION_SCHEMA,
        **common,
        "authoritative": False,
        "workers_requested": args.archive_workers,
        "workers_used": min(args.archive_workers, len(archive_tasks))
        if archive_tasks
        else 0,
        "timeout_seconds": args.archive_timeout_seconds,
        "entries": [
            {
                "task_id": result["task_id"],
                "package": result["package"],
                "lane": result["lane"],
                "status": result["status"],
                "error": result["error"],
                "duration_ms": result["duration_ms"],
            }
            for result in archive_results
        ],
        "counts": {
            status: sum(
                1 for result in archive_results if result["status"] == status
            )
            for status in ("success", "failed", "timed_out")
        },
    }
    postcheck_plan = {
        "schema": "openclaw.safe_update.post_upgrade_e2e.v1",
        **common,
        "status": "success" if coverage_status == "success" else "failed",
        "execution_status": "not_run",
        "surfaces": [
            {
                "id": surface["id"],
                "category": surface["category"],
                "required": surface["required"],
                "checks": [
                    {"description": check, "status": "not_run"}
                    for check in surface["post_update_checks"]
                ],
            }
            for surface in coverage_surface_results
        ],
        "note": "This is a post-upgrade test plan, not evidence that the checks have run.",
    }

    runtime_path = output_dir / "runtime-truth.json"
    core_candidate_path = output_dir / "core-candidate-lock.json"
    installation_candidate_path = output_dir / "installation-candidate-lock.json"
    installation_attestation_path = output_dir / "installation-attestation.json"
    conservative_gates_path = output_dir / "conservative-gates.json"
    impact_shadow_path = output_dir / "impact-shadow.json"
    analysis_cache_path = output_dir / "analysis-cache.json"
    archive_execution_path = output_dir / "archive-execution.json"
    synthetic_path = output_dir / "synthetic-update.json"
    customization_path = output_dir / "customization-compatibility.json"
    coverage_path = output_dir / "coverage-report.json"
    postcheck_path = output_dir / "post-upgrade-e2e.json"
    write_json(runtime_path, runtime_truth)
    write_json(core_candidate_path, core_candidate_lock)
    write_json(installation_candidate_path, installation_candidate_lock)
    write_json(installation_attestation_path, installation_attestation)
    write_json(conservative_gates_path, conservative_gates)
    if impact_shadow is not None:
        write_json(impact_shadow_path, impact_shadow)
    write_json(analysis_cache_path, analysis_cache_report)
    write_json(archive_execution_path, archive_execution_report)
    write_json(synthetic_path, synthetic)
    write_json(customization_path, customizations)
    write_json(coverage_path, coverage_report)
    write_json(postcheck_path, postcheck_plan)

    blocked = any(
        status != "success"
        for status in (
            runtime_status,
            core_candidate_status,
            installation_candidate_status,
            installation_attestation_status,
            conservative_gate_status,
            synthetic_status,
            customization_status,
            coverage_status,
        )
    )
    verdict_value = "blocked" if blocked else "ready_for_operator_plan"
    evidence = {
        "schema": "openclaw.safe_update.evidence_bundle.v1",
        **common,
        "repair_class": "openclaw_upgrade",
        "verdict": verdict_value,
        "evidence": [
            artifact_reference(runtime_path, runtime_status),
            artifact_reference(core_candidate_path, core_candidate_status),
            artifact_reference(
                installation_candidate_path,
                installation_candidate_status,
            ),
            artifact_reference(
                installation_attestation_path,
                installation_attestation_status,
            ),
            artifact_reference(conservative_gates_path, conservative_gate_status),
            artifact_reference(synthetic_path, synthetic_status),
            artifact_reference(customization_path, customization_status),
            artifact_reference(coverage_path, coverage_status),
            artifact_reference(postcheck_path, postcheck_plan["status"]),
        ],
    }
    evidence_path = output_dir / "evidence-bundle.json"
    write_json(evidence_path, evidence)
    verdict = build_status(
        generated_at=generated_at,
        verdict=verdict_value,
        reason=(
            "required package, customization, runtime, or installation coverage evidence failed"
            if blocked
            else "package-level rehearsal passed; live mutation still requires an operator plan and approval"
        ),
        reason_code="required_evidence_failed" if blocked else "baseline_rehearsal_passed",
        evidence_status={
            "runtime_truth": runtime_status,
            "core_candidate_lock": core_candidate_status,
            "installation_candidate_lock": installation_candidate_status,
            "installation_attestation": installation_attestation_status,
            "conservative_gates": conservative_gate_status,
            "synthetic_update": synthetic_status,
            "customization_compatibility": customization_status,
            "installation_coverage": coverage_status,
            "post_upgrade_e2e_plan": postcheck_plan["status"],
        },
        gate_decision={
            "status": conservative_gate_status,
            "handling": conservative_gates["handling"],
            "required_gates": conservative_gates["required_gates"],
            "decision_digest": conservative_gates["decision_digest"],
        },
        candidate_roots={
            "current": installation_candidate_lock["current_root"],
            "target": installation_candidate_lock["target_root"],
        },
        evidence_bundle={"path": evidence_path.name, "sha256": digest_file(evidence_path)},
        next_step=(
            "repair evidence and rerun"
            if blocked
            else "prepare rollback-aware operator plan and stop before apply"
        ),
        next_step_code="repair_and_rerun" if blocked else "prepare_operator_plan",
    )
    verdict_path = output_dir / "verdict.json"
    write_status(verdict_path, verdict)
    operator_plan = (
        "# OpenClaw Upgrade Operator Plan\n\n"
        "## STOP BEFORE APPLY\n\n"
        "This rehearsal does not authorize or execute an upgrade. A human operator must review "
        "the evidence, choose a maintenance window, verify a lossless rollback, and separately approve "
        "the exact mutation.\n\n"
        f"- Verdict: `{verdict_value}`\n"
        f"- Current version: `{metadata.get('current_version', 'unknown')}`\n"
        f"- Target version: `{metadata.get('target_version', 'unknown')}`\n"
        f"- Install shape: `{coverage_profile.get('install_shape') or 'unknown'}`\n"
        f"- Current candidate root: `{installation_candidate_lock['current_root'] or 'unavailable'}`\n"
        f"- Target candidate root: `{installation_candidate_lock['target_root'] or 'unavailable'}`\n"
        f"- Installation attestation: `{installation_attestation_status}`\n"
        f"- Conservative gates: `{conservative_gate_status}` (`{conservative_gates['handling']}`)\n"
        f"- Evidence bundle: `{evidence_path.name}` (`{digest_file(evidence_path)}`)\n"
        f"- Post-upgrade E2E plan: `{postcheck_path.name}`\n\n"
        "## Required operator inputs\n\n"
        "- Exact maintenance window\n"
        "- Verified backup and lossless rollback command\n"
        "- Exact update command and affected paths\n"
        "- Separate approval for update, restart, or deploy\n\n"
        "## Exit criteria\n\n"
        "Every required post-upgrade check must be recorded as passed. Any failed or unproven surface "
        "means rollback or forward recovery, not acceptance.\n"
    )
    write_text(output_dir / "operator-plan.md", operator_plan)
    summary = (
        "# OpenClaw Safe Update Rehearsal\n\n"
        f"- Verdict: `{verdict_value}`\n"
        f"- Current version: `{metadata.get('current_version', 'unknown')}`\n"
        f"- Target version: `{metadata.get('target_version', 'unknown')}`\n"
        f"- Runtime evidence: `{runtime_status}`\n"
        f"- Core candidate lock: `{core_candidate_status}`\n"
        f"- Installation candidate lock: `{installation_candidate_status}`\n"
        f"- Installation attestation: `{installation_attestation_status}`\n"
        f"- Conservative gates: `{conservative_gate_status}` (`{conservative_gates['handling']}`)\n"
        f"- Package evidence: `{synthetic_status}`\n"
        f"- Customization evidence: `{customization_status}`\n"
        f"- Installation coverage: `{coverage_status}`\n"
        f"- Declared surfaces: `{len(coverage_surface_results)}`\n"
        "- Runtime effect: `none`\n"
        "- Production apply allowed: `false`\n"
        "- Operator approval: `false`\n\n"
        f"Next step: {verdict['next_step']}.\n"
    )
    write_text(output_dir / "summary.md", summary)
    print(verdict_path)
    return 2 if blocked else 0


def archive_workers_argument(value: str) -> int:
    try:
        workers = int(value)
    except ValueError as exc:
        raise argparse.ArgumentTypeError("archive workers must be an integer") from exc
    if workers < 1 or workers > MAX_ARCHIVE_WORKERS:
        raise argparse.ArgumentTypeError(
            f"archive workers must be between 1 and {MAX_ARCHIVE_WORKERS}"
        )
    return workers


def archive_timeout_argument(value: str) -> float:
    try:
        timeout = float(value)
    except ValueError as exc:
        raise argparse.ArgumentTypeError(
            "archive timeout seconds must be a number"
        ) from exc
    if timeout <= 0 or timeout > 900:
        raise argparse.ArgumentTypeError(
            "archive timeout seconds must be greater than 0 and at most 900"
        )
    return timeout


class KovaEvidenceImportError(RuntimeError):
    def __init__(self, code: str):
        super().__init__(code)
        self.code = code


def kova_sha256_bytes(payload: bytes) -> str:
    return "sha256:" + hashlib.sha256(payload).hexdigest()


def kova_safe_identifier(value: Any) -> str | None:
    if isinstance(value, str) and KOVA_SAFE_ID_RE.fullmatch(value):
        return value
    return None


def read_bounded_regular_bytes(path: Path, limit: int, error_code: str) -> bytes:
    try:
        metadata = path.lstat()
        if path.is_symlink() or not stat.S_ISREG(metadata.st_mode):
            raise KovaEvidenceImportError(error_code)
        if metadata.st_size > limit:
            raise KovaEvidenceImportError(error_code)
        flags = os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0)
        descriptor = os.open(path, flags)
        try:
            opened = os.fstat(descriptor)
            if not stat.S_ISREG(opened.st_mode) or opened.st_size > limit:
                raise KovaEvidenceImportError(error_code)
            payload = bytearray()
            while True:
                chunk = os.read(descriptor, min(1024 * 1024, limit + 1 - len(payload)))
                if not chunk:
                    break
                payload.extend(chunk)
                if len(payload) > limit:
                    raise KovaEvidenceImportError(error_code)
            return bytes(payload)
        finally:
            os.close(descriptor)
    except KovaEvidenceImportError:
        raise
    except OSError as exc:
        raise KovaEvidenceImportError(error_code) from exc


def parse_bounded_json(path: Path, error_code: str) -> tuple[Any, bytes]:
    payload = read_bounded_regular_bytes(path, KOVA_MAX_JSON_BYTES, error_code)
    try:
        return json.loads(payload.decode("utf-8")), payload
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise KovaEvidenceImportError(error_code) from exc


def validate_kova_policy(value: Any) -> dict[str, Any]:
    if not isinstance(value, dict) or set(value) != {
        "schema",
        "policy_id",
        "supported_receipt_schemas",
        "supported_report_schemas",
        "required_mode",
        "target_binding",
        "reject_publication_omissions",
        "scenarios",
    }:
        raise KovaEvidenceImportError("policy-invalid")
    if value.get("schema") != KOVA_EVIDENCE_POLICY_SCHEMA:
        raise KovaEvidenceImportError("policy-invalid")
    policy_id = kova_safe_identifier(value.get("policy_id"))
    if policy_id is None:
        raise KovaEvidenceImportError("policy-invalid")

    def schema_list(field: str) -> list[str]:
        items = value.get(field)
        if (
            not isinstance(items, list)
            or not items
            or any(kova_safe_identifier(item) is None for item in items)
            or len(items) != len(set(items))
        ):
            raise KovaEvidenceImportError("policy-invalid")
        return sorted(items)

    receipts = schema_list("supported_receipt_schemas")
    reports = schema_list("supported_report_schemas")
    if receipts != [KOVA_RECEIPT_SCHEMA] or reports != [KOVA_REPORT_SCHEMA]:
        raise KovaEvidenceImportError("policy-invalid")
    if value.get("required_mode") != "execution":
        raise KovaEvidenceImportError("policy-invalid")
    if value.get("reject_publication_omissions") is not True:
        raise KovaEvidenceImportError("policy-invalid")

    binding = value.get("target_binding")
    if not isinstance(binding, dict) or set(binding) != {
        "component_id",
        "artifact_kind",
        "artifact_ref",
        "accepted_identity_kinds",
    }:
        raise KovaEvidenceImportError("policy-invalid")
    if (
        kova_safe_identifier(binding.get("component_id")) is None
        or binding.get("artifact_kind") != "npm_package"
        or kova_safe_identifier(binding.get("artifact_ref")) is None
    ):
        raise KovaEvidenceImportError("policy-invalid")
    identity_kinds = binding.get("accepted_identity_kinds")
    if (
        not isinstance(identity_kinds, list)
        or not identity_kinds
        or len(identity_kinds) != len(set(identity_kinds))
        or any(item not in KOVA_EXACT_IDENTITY_KINDS for item in identity_kinds)
    ):
        raise KovaEvidenceImportError("policy-invalid")

    scenarios = value.get("scenarios")
    if not isinstance(scenarios, list) or not scenarios:
        raise KovaEvidenceImportError("policy-invalid")
    normalized_scenarios: list[dict[str, Any]] = []
    scenario_ids: set[str] = set()
    for item in scenarios:
        if not isinstance(item, dict) or set(item) != {"id", "gate_ids", "required_evidence"}:
            raise KovaEvidenceImportError("policy-invalid")
        scenario_id = kova_safe_identifier(item.get("id"))
        gate_ids = item.get("gate_ids")
        required_evidence = item.get("required_evidence")
        if (
            scenario_id is None
            or scenario_id in scenario_ids
            or not isinstance(gate_ids, list)
            or not gate_ids
            or len(gate_ids) != len(set(gate_ids))
            or any(gate_id not in GATE_EVIDENCE_IDS for gate_id in gate_ids)
            or not isinstance(required_evidence, list)
            or not required_evidence
        ):
            raise KovaEvidenceImportError("policy-invalid")
        normalized_evidence: list[dict[str, str]] = []
        evidence_keys: set[tuple[str, str]] = set()
        for evidence in required_evidence:
            if not isinstance(evidence, dict) or set(evidence) != {"id", "category"}:
                raise KovaEvidenceImportError("policy-invalid")
            evidence_id = kova_safe_identifier(evidence.get("id"))
            category = evidence.get("category")
            key = (str(evidence_id), str(category))
            if (
                evidence_id is None
                or category not in {"command", "invariant", "collector"}
                or key in evidence_keys
            ):
                raise KovaEvidenceImportError("policy-invalid")
            evidence_keys.add(key)
            normalized_evidence.append({"id": evidence_id, "category": category})
        scenario_ids.add(scenario_id)
        normalized_scenarios.append(
            {
                "id": scenario_id,
                "gate_ids": sorted(gate_ids),
                "required_evidence": sorted(
                    normalized_evidence, key=lambda evidence: (evidence["id"], evidence["category"])
                ),
            }
        )
    normalized_scenarios.sort(key=lambda item: item["id"])
    return {
        **value,
        "supported_receipt_schemas": receipts,
        "supported_report_schemas": reports,
        "target_binding": {
            **binding,
            "accepted_identity_kinds": sorted(identity_kinds),
        },
        "scenarios": normalized_scenarios,
    }


def validate_kova_candidate_lock(
    value: Any,
    binding: dict[str, Any],
) -> tuple[str, dict[str, Any]]:
    if (
        not isinstance(value, dict)
        or value.get("schema") != INSTALLATION_CANDIDATE_LOCK_SCHEMA
        or value.get("status") != "success"
        or not isinstance(value.get("target"), dict)
    ):
        raise KovaEvidenceImportError("candidate-lock-invalid")
    target = value["target"]
    target_root = value.get("target_root")
    if (
        not isinstance(target_root, str)
        or not re.fullmatch(r"sha256:[0-9a-f]{64}", target_root)
        or target.get("root") != target_root
    ):
        raise KovaEvidenceImportError("candidate-lock-invalid")
    target_content = {key: item for key, item in target.items() if key != "root"}
    if canonical_digest(target_content) != target_root:
        raise KovaEvidenceImportError("candidate-lock-invalid")
    components = target.get("components")
    if not isinstance(components, list):
        raise KovaEvidenceImportError("candidate-lock-invalid")
    matching_components = [
        item
        for item in components
        if isinstance(item, dict) and item.get("id") == binding["component_id"]
    ]
    if len(matching_components) != 1:
        raise KovaEvidenceImportError("candidate-binding-missing")
    artifacts = matching_components[0].get("artifacts")
    if not isinstance(artifacts, list):
        raise KovaEvidenceImportError("candidate-binding-missing")
    matching_artifacts = [
        item
        for item in artifacts
        if isinstance(item, dict)
        and item.get("kind") == binding["artifact_kind"]
        and item.get("ref") == binding["artifact_ref"]
    ]
    if len(matching_artifacts) != 1:
        raise KovaEvidenceImportError("candidate-binding-missing")
    artifact = matching_artifacts[0]
    if (
        kova_safe_identifier(artifact.get("identity")) is None
        or not isinstance(artifact.get("integrity"), str)
        or len(artifact["integrity"]) > 1024
    ):
        raise KovaEvidenceImportError("candidate-binding-missing")
    if not valid_kova_npm_integrity(artifact["integrity"]):
        raise KovaEvidenceImportError("candidate-binding-missing")
    package_identity = artifact["identity"]
    if "@" not in package_identity:
        raise KovaEvidenceImportError("candidate-binding-missing")
    package_name, package_version = package_identity.rsplit("@", 1)
    if package_name != binding["artifact_ref"] or not VERSION_RE.fullmatch(package_version):
        raise KovaEvidenceImportError("candidate-binding-mismatch")
    return target_root, artifact


def valid_kova_npm_integrity(value: Any) -> bool:
    if not isinstance(value, str) or not value.startswith("sha512-"):
        return False
    encoded = value.removeprefix("sha512-")
    try:
        decoded = base64.b64decode(encoded, validate=True)
    except (ValueError, TypeError):
        return False
    return len(decoded) == hashlib.sha512().digest_size


def resolve_kova_artifact_path(receipt_path: Path, value: Any) -> Path:
    if not isinstance(value, str) or not value or "\x00" in value:
        raise KovaEvidenceImportError("receipt-artifact-reference-invalid")
    candidate = Path(value)
    if not candidate.is_absolute():
        candidate = receipt_path.parent / candidate
    return Path(os.path.abspath(candidate))


def validate_kova_checksum(bundle_path: Path, checksum_path: Path) -> str:
    read_bounded_regular_bytes(
        bundle_path,
        KOVA_MAX_BUNDLE_BYTES,
        "bundle-unreadable",
    )
    checksum_payload = read_bounded_regular_bytes(
        checksum_path,
        KOVA_MAX_CHECKSUM_BYTES,
        "checksum-invalid",
    )
    try:
        checksum_text = checksum_payload.decode("ascii")
    except UnicodeDecodeError as exc:
        raise KovaEvidenceImportError("checksum-invalid") from exc
    match = re.fullmatch(r"([0-9a-f]{64})  ([^/\\\r\n]+)\r?\n?", checksum_text)
    if match is None or match.group(2) != bundle_path.name:
        raise KovaEvidenceImportError("checksum-invalid")
    observed = digest_file(bundle_path)
    if not hmac.compare_digest(observed, match.group(1)):
        raise KovaEvidenceImportError("bundle-checksum-mismatch")
    return "sha256:" + observed


def safe_kova_archive_name(value: Any) -> str | None:
    if not isinstance(value, str) or not value or len(value.encode("utf-8")) > 4096:
        return None
    if value.startswith("/") or "\\" in value or any(ord(char) < 32 for char in value):
        return None
    parts = value.split("/")
    if len(parts) > 64 or any(not part or part in {".", ".."} for part in parts):
        return None
    if PurePosixPath(value).as_posix() != value:
        return None
    return value


def read_kova_tar_member(
    archive: tarfile.TarFile,
    member: tarfile.TarInfo,
    limit: int,
) -> bytes:
    if not member.isfile() or member.size < 0 or member.size > limit:
        raise KovaEvidenceImportError("bundle-member-invalid")
    handle = archive.extractfile(member)
    if handle is None:
        raise KovaEvidenceImportError("bundle-member-invalid")
    payload = handle.read(limit + 1)
    if len(payload) != member.size or len(payload) > limit:
        raise KovaEvidenceImportError("bundle-member-invalid")
    return payload


def validate_kova_bundle(
    bundle_path: Path,
    report_path: Path,
    report_payload: bytes,
    reject_publication_omissions: bool,
) -> tuple[str, bytes]:
    try:
        with tarfile.open(bundle_path, mode="r:gz") as archive:
            file_members: dict[str, tarfile.TarInfo] = {}
            total_declared = 0
            physical_count = 0
            for member in archive.getmembers():
                physical_count += 1
                if physical_count > KOVA_MAX_BUNDLE_ENTRIES:
                    raise KovaEvidenceImportError("bundle-member-limit")
                if safe_kova_archive_name(member.name) is None:
                    raise KovaEvidenceImportError("bundle-member-invalid")
                if member.isdir():
                    continue
                if not member.isfile() or member.name in file_members:
                    raise KovaEvidenceImportError("bundle-member-invalid")
                total_declared += member.size
                if total_declared > KOVA_MAX_BUNDLE_DECLARED_BYTES:
                    raise KovaEvidenceImportError("bundle-member-limit")
                file_members[member.name] = member

            index_names = [
                name for name in file_members if name.endswith("/artifact-index.json")
            ]
            if len(index_names) != 1:
                raise KovaEvidenceImportError("artifact-index-missing")
            index_name = index_names[0]
            index_payload = read_kova_tar_member(
                archive,
                file_members[index_name],
                KOVA_MAX_JSON_BYTES,
            )
            try:
                index = json.loads(index_payload.decode("utf-8"))
            except (UnicodeDecodeError, json.JSONDecodeError) as exc:
                raise KovaEvidenceImportError("artifact-index-invalid") from exc
            if not isinstance(index, dict) or index.get("schemaVersion") != KOVA_ARTIFACT_INDEX_SCHEMA:
                raise KovaEvidenceImportError("artifact-index-invalid")
            bundle_root = safe_kova_archive_name(index.get("bundleRoot"))
            entries = index.get("entries")
            omissions = index.get("publicationOmissions")
            if (
                bundle_root is None
                or "/" in bundle_root
                or index_name != f"{bundle_root}/artifact-index.json"
                or not isinstance(entries, list)
                or len(entries) > KOVA_MAX_BUNDLE_ENTRIES
                or not isinstance(omissions, dict)
            ):
                raise KovaEvidenceImportError("artifact-index-invalid")
            omission_entries = omissions.get("entries")
            if (
                not isinstance(omissions.get("fileCount"), int)
                or not isinstance(omissions.get("totalBytes"), int)
                or not isinstance(omission_entries, list)
                or omissions["fileCount"] != len(omission_entries)
            ):
                raise KovaEvidenceImportError("artifact-index-invalid")
            if reject_publication_omissions and (
                omissions["fileCount"] != 0
                or omissions["totalBytes"] != 0
                or omission_entries
            ):
                raise KovaEvidenceImportError("publication-omission")

            indexed_names: set[str] = set()
            indexed_paths: set[str] = set()
            indexed_total = 0
            report_matches = 0
            for entry in entries:
                if not isinstance(entry, dict) or set(entry) != {
                    "path",
                    "archivePath",
                    "bytes",
                    "sha256",
                }:
                    raise KovaEvidenceImportError("artifact-index-invalid")
                path = safe_kova_archive_name(entry.get("path"))
                archive_path = safe_kova_archive_name(entry.get("archivePath"))
                size = entry.get("bytes")
                digest = entry.get("sha256")
                if (
                    path is None
                    or archive_path is None
                    or path in indexed_paths
                    or not isinstance(size, int)
                    or size < 0
                    or not isinstance(digest, str)
                    or re.fullmatch(r"[0-9a-f]{64}", digest) is None
                ):
                    raise KovaEvidenceImportError("artifact-index-invalid")
                indexed_paths.add(path)
                member_name = f"{bundle_root}/{archive_path}"
                if member_name in indexed_names or member_name not in file_members:
                    raise KovaEvidenceImportError("artifact-index-invalid")
                indexed_names.add(member_name)
                payload = read_kova_tar_member(
                    archive,
                    file_members[member_name],
                    KOVA_MAX_BUNDLE_DECLARED_BYTES,
                )
                if len(payload) != size or hashlib.sha256(payload).hexdigest() != digest:
                    raise KovaEvidenceImportError("bundle-member-digest-mismatch")
                indexed_total += size
                if path in {report_path.name, "report.json"}:
                    report_matches += 1
                    if payload != report_payload:
                        raise KovaEvidenceImportError("bundled-report-mismatch")
            if (
                index.get("fileCount") != len(entries)
                or index.get("totalBytes") != indexed_total
                or report_matches != 1
                or set(file_members) != indexed_names | {index_name}
            ):
                raise KovaEvidenceImportError("artifact-index-incomplete")
            return kova_sha256_bytes(index_payload), index_payload
    except KovaEvidenceImportError:
        raise
    except (OSError, tarfile.TarError, EOFError) as exc:
        raise KovaEvidenceImportError("bundle-invalid") from exc


def normalize_kova_summary(value: Any) -> dict[str, Any]:
    if not isinstance(value, dict) or set(value) != {"total", "statuses"}:
        raise KovaEvidenceImportError("summary-invalid")
    total = value.get("total")
    statuses = value.get("statuses")
    if (
        not isinstance(total, int)
        or total < 0
        or not isinstance(statuses, dict)
        or any(
            status not in KOVA_RECORD_STATUSES
            or not isinstance(count, int)
            or count < 0
            for status, count in statuses.items()
        )
        or sum(statuses.values()) != total
    ):
        raise KovaEvidenceImportError("summary-invalid")
    return {"total": total, "statuses": dict(sorted(statuses.items()))}


def validate_kova_target_identity(
    receipt: dict[str, Any],
    report: dict[str, Any],
    artifact: dict[str, Any],
    accepted_kinds: list[str],
) -> tuple[dict[str, Any], list[str], list[str]]:
    receipt_identity = receipt.get("targetIdentity")
    report_identity = report.get("targetIdentity")
    if receipt_identity is None and report_identity is None:
        return {
            "status": "missing",
            "identity_kind": None,
            "identity_digest": None,
        }, ["target-identity"], ["target-identity-missing"]
    if receipt_identity is None or report_identity is None:
        return {
            "status": "missing",
            "identity_kind": None,
            "identity_digest": None,
        }, ["target-identity"], ["target-identity-incomplete"]
    if receipt_identity != report_identity:
        raise KovaEvidenceImportError("target-identity-disagreement")
    records = report.get("records")
    if not isinstance(records, list) or not records:
        raise KovaEvidenceImportError("records-invalid")
    for record in records:
        if not isinstance(record, dict):
            raise KovaEvidenceImportError("records-invalid")
        if record.get("status") not in {"DRY-RUN", "SKIPPED"}:
            if record.get("targetIdentity") is None:
                return {
                    "status": "missing",
                    "identity_kind": None,
                    "identity_digest": None,
                }, ["record-target-identity"], ["record-target-identity-missing"]
            if record["targetIdentity"] != report_identity:
                raise KovaEvidenceImportError("record-target-identity-disagreement")
    identity = receipt_identity
    if not isinstance(identity, dict) or set(identity) != {
        "schemaVersion",
        "requestedSelector",
        "resolvedVersion",
        "npmIntegrity",
        "gitSha",
        "buildDigest",
    }:
        raise KovaEvidenceImportError("target-identity-invalid")
    if identity.get("schemaVersion") != KOVA_TARGET_IDENTITY_SCHEMA:
        raise KovaEvidenceImportError("target-identity-invalid")
    requested = identity.get("requestedSelector")
    resolved = identity.get("resolvedVersion")
    if kova_safe_identifier(requested) is None or not isinstance(resolved, str) or not VERSION_RE.fullmatch(resolved):
        raise KovaEvidenceImportError("target-identity-invalid")
    artifact_identity = artifact["identity"]
    if "@" not in artifact_identity:
        raise KovaEvidenceImportError("candidate-binding-missing")
    candidate_version = artifact_identity.rsplit("@", 1)[1]
    if resolved != candidate_version or requested != f"npm:{candidate_version}":
        return {
            "status": "mismatch",
            "identity_kind": None,
            "identity_digest": canonical_digest(identity),
        }, [], ["target-identity-mismatch"]
    if report.get("target") != requested:
        return {
            "status": "mismatch",
            "identity_kind": None,
            "identity_digest": canonical_digest(identity),
        }, [], ["target-identity-mismatch"]

    exact_values = {
        "npm_integrity": identity.get("npmIntegrity"),
        "git_sha": identity.get("gitSha"),
        "build_digest": identity.get("buildDigest"),
    }
    populated = [kind for kind, item in exact_values.items() if item is not None]
    identity_digest = canonical_digest(identity)
    if not populated:
        return {
            "status": "version_only",
            "identity_kind": None,
            "identity_digest": identity_digest,
        }, ["target-identity-exact"], ["target-identity-version-only"]
    if len(populated) != 1:
        raise KovaEvidenceImportError("target-identity-invalid")
    identity_kind = populated[0]
    exact_value = exact_values[identity_kind]
    if not isinstance(exact_value, str) or not exact_value or len(exact_value) > 1024:
        raise KovaEvidenceImportError("target-identity-invalid")
    if identity_kind not in accepted_kinds:
        return {
            "status": "version_only",
            "identity_kind": identity_kind,
            "identity_digest": identity_digest,
        }, ["target-identity-kind"], ["target-identity-kind-not-accepted"]
    matches = False
    if identity_kind == "npm_integrity":
        matches = hmac.compare_digest(exact_value, artifact["integrity"])
    if not matches:
        return {
            "status": "mismatch",
            "identity_kind": identity_kind,
            "identity_digest": identity_digest,
        }, [], ["target-identity-mismatch"]
    return {
        "status": "exact",
        "identity_kind": identity_kind,
        "identity_digest": identity_digest,
    }, [], []


def validate_kova_environment(
    report: dict[str, Any],
    candidate_lock: dict[str, Any],
) -> tuple[list[str], list[str]]:
    target = candidate_lock.get("target")
    expected = target.get("environment") if isinstance(target, dict) else None
    if not isinstance(expected, dict) or set(expected) != {
        "node_version",
        "npm_version",
        "os",
        "arch",
        "libc",
    }:
        raise KovaEvidenceImportError("candidate-lock-invalid")
    # Kova platformInfo() describes the harness process, not the OCM runtime.
    # kova.report.v1 has no target toolchain contract; never infer one from it.
    return ["target-environment"], ["target-environment-incomplete"]


def aggregate_kova_scenarios(
    report: dict[str, Any],
    policy: dict[str, Any],
) -> tuple[list[dict[str, Any]], list[str], list[str]]:
    records = report.get("records")
    if not isinstance(records, list):
        raise KovaEvidenceImportError("records-invalid")
    normalized_records: list[dict[str, Any]] = []
    status_counts: dict[str, int] = {}
    for record in records:
        if not isinstance(record, dict):
            raise KovaEvidenceImportError("records-invalid")
        scenario = kova_safe_identifier(record.get("scenario"))
        status_value = record.get("status")
        if scenario is None or status_value not in KOVA_RECORD_STATUSES:
            raise KovaEvidenceImportError("record-status-invalid")
        status_counts[status_value] = status_counts.get(status_value, 0) + 1
        ledger = record.get("evidenceLedger")
        ledger_status = "missing"
        ledger_digest = None
        passed_evidence: set[tuple[str, str]] = set()
        if isinstance(ledger, dict):
            ledger_digest = canonical_digest(ledger)
            entries = ledger.get("entries")
            valid_entries = (
                isinstance(entries, list)
                and bool(entries)
                and all(
                    isinstance(item, dict)
                    and kova_safe_identifier(item.get("id")) is not None
                    and kova_safe_identifier(item.get("category")) is not None
                    and isinstance(item.get("required"), bool)
                    and item.get("status") in {"passed", "failed", "missing", "skipped"}
                    for item in entries
                )
            )
            required_entries = (
                [item for item in entries if item.get("required") is True]
                if valid_entries
                else []
            )
            expected_summary: dict[str, Any] | None = None
            if valid_entries:
                by_status: dict[str, int] = {}
                by_category: dict[str, int] = {}
                for item in entries:
                    by_status[item["status"]] = by_status.get(item["status"], 0) + 1
                    by_category[item["category"]] = by_category.get(item["category"], 0) + 1
                expected_summary = {
                    "total": len(entries),
                    "required": len(required_entries),
                    "requiredMissing": sum(item["status"] == "missing" for item in required_entries),
                    "requiredFailed": sum(item["status"] == "failed" for item in required_entries),
                    "byStatus": dict(sorted(by_status.items())),
                    "byCategory": dict(sorted(by_category.items())),
                }
            if (
                ledger.get("schemaVersion") == "kova.evidenceLedger.v1"
                and ledger.get("completeness") == "complete"
                and valid_entries
                and bool(required_entries)
                and all(item.get("status") == "passed" for item in required_entries)
                and ledger.get("summary") == expected_summary
            ):
                ledger_status = "complete"
                passed_evidence = {
                    (item["id"], item["category"])
                    for item in required_entries
                    if item["status"] == "passed"
                }
            else:
                ledger_status = "incomplete"
        normalized_records.append(
            {
                "scenario": scenario,
                "status": status_value,
                "ledger_status": ledger_status,
                "ledger_digest": ledger_digest,
                "passed_evidence": passed_evidence,
            }
        )
    summary = normalize_kova_summary(report.get("summary"))
    if summary != {"total": len(records), "statuses": dict(sorted(status_counts.items()))}:
        raise KovaEvidenceImportError("summary-mismatch")

    missing: list[str] = []
    errors: list[str] = []
    results: list[dict[str, Any]] = []
    for requirement in policy["scenarios"]:
        scenario_id = requirement["id"]
        matching = [item for item in normalized_records if item["scenario"] == scenario_id]
        if not matching:
            results.append(
                {
                    "id": scenario_id,
                    "status": "MISSING",
                    "evidence_ledger_status": None,
                    "evidence_ledger_digest": None,
                }
            )
            missing.append(f"scenario:{scenario_id}")
            errors.append("required-scenario-missing")
            continue
        statuses = {item["status"] for item in matching}
        ledgers = {item["ledger_status"] for item in matching}
        aggregate_status = next(iter(statuses)) if len(statuses) == 1 else "MIXED"
        aggregate_ledger = next(iter(ledgers)) if len(ledgers) == 1 else "incomplete"
        ledger_digest = canonical_digest(
            sorted(
                (
                    {
                        "status": item["status"],
                        "ledger_status": item["ledger_status"],
                        "ledger_digest": item["ledger_digest"],
                    }
                    for item in matching
                ),
                key=lambda item: canonical_json_bytes(item),
            )
        )
        results.append(
            {
                "id": scenario_id,
                "status": aggregate_status,
                "evidence_ledger_status": aggregate_ledger,
                "evidence_ledger_digest": ledger_digest,
            }
        )
        if statuses != {"PASS"}:
            missing.append(f"scenario:{scenario_id}")
            errors.append("required-scenario-not-pass")
        if ledgers != {"complete"}:
            missing.append(f"ledger:{scenario_id}")
            errors.append("evidence-ledger-incomplete")
        required_evidence = {
            (item["id"], item["category"])
            for item in requirement["required_evidence"]
        }
        if any(not required_evidence.issubset(item["passed_evidence"]) for item in matching):
            missing.append(f"ledger-proof:{scenario_id}")
            errors.append("required-ledger-proof-missing")
    if any(status != "PASS" for status in status_counts):
        errors.append("report-contains-non-pass")
        missing.append("report-all-records-pass")
    return results, sorted(set(missing)), sorted(set(errors))


def kova_source_defaults(receipt_sha256: str | None = None) -> dict[str, Any]:
    return {
        "receipt_schema": "unknown",
        "receipt_sha256": receipt_sha256,
        "report_schema": None,
        "report_sha256": None,
        "bundle_sha256": None,
        "artifact_index_sha256": None,
        "run_id": None,
        "mode": None,
    }


def build_kova_evidence_document(
    *,
    status_value: str,
    policy_id: str,
    candidate_binding: dict[str, Any],
    source: dict[str, Any],
    scenarios: list[dict[str, Any]],
    eligible_gates: list[dict[str, str]],
    missing_requirements: list[str],
    error_codes: list[str],
) -> dict[str, Any]:
    content = {
        "policy_id": policy_id,
        "candidate_binding": candidate_binding,
        "source": source,
        "scenarios": scenarios,
        "eligible_gates": eligible_gates,
        "missing_requirements": sorted(set(missing_requirements)),
        "error_codes": sorted(set(error_codes)),
        "canonical_status_effect": "evidence_for_named_gate_only",
        "post_activation_e2e": "not_run",
    }
    generated_at = now_iso()
    return {
        "schema": KOVA_EVIDENCE_SCHEMA,
        "generated_at": generated_at,
        "effect": "read_only_kova_evidence_import",
        "runtime_effect": "none",
        "external_effect": "none",
        "external_write_effect": "none",
        "production_apply_allowed": False,
        "operator_approval": False,
        "status": status_value,
        "evidence_content": content,
        "evidence_digest": canonical_digest(content),
        "run_envelope": {"generated_at": generated_at},
    }


def kova_evidence(args: argparse.Namespace) -> int:
    receipt_path = Path(os.path.abspath(args.receipt))
    candidate_path = Path(os.path.abspath(args.candidate_lock))
    policy_path = Path(os.path.abspath(args.policy))
    output_path = Path(os.path.abspath(args.output))
    policy_id = "invalid-policy"
    source = kova_source_defaults()
    candidate_binding = {
        "status": "missing",
        "scope": "core_npm_artifact_only",
        "target_candidate_root": None,
        "identity_kind": None,
        "identity_digest": None,
    }
    scenarios: list[dict[str, Any]] = []
    missing: list[str] = []
    errors: list[str] = []
    eligible_gates: list[dict[str, str]] = []
    status_value = "rejected"
    try:
        policy_raw, _ = parse_bounded_json(policy_path, "policy-invalid")
        policy = validate_kova_policy(policy_raw)
        policy_id = policy["policy_id"]
        candidate_raw, _ = parse_bounded_json(candidate_path, "candidate-lock-invalid")
        target_root, artifact = validate_kova_candidate_lock(
            candidate_raw,
            policy["target_binding"],
        )
        candidate_binding["target_candidate_root"] = target_root

        receipt_raw, receipt_payload = parse_bounded_json(receipt_path, "receipt-invalid")
        source["receipt_sha256"] = kova_sha256_bytes(receipt_payload)
        if not isinstance(receipt_raw, dict):
            raise KovaEvidenceImportError("receipt-invalid")
        receipt_schema = receipt_raw.get("schemaVersion")
        if receipt_schema not in policy["supported_receipt_schemas"]:
            raise KovaEvidenceImportError("receipt-schema-unsupported")
        source["receipt_schema"] = receipt_schema
        mode = receipt_raw.get("mode")
        run_id = kova_safe_identifier(receipt_raw.get("runId"))
        if mode != policy["required_mode"] or run_id is None:
            raise KovaEvidenceImportError("receipt-contract-invalid")
        source["mode"] = mode
        source["run_id"] = run_id

        report_path = resolve_kova_artifact_path(receipt_path, receipt_raw.get("jsonPath"))
        bundle_path = resolve_kova_artifact_path(receipt_path, receipt_raw.get("bundlePath"))
        checksum_path = resolve_kova_artifact_path(receipt_path, receipt_raw.get("checksumPath"))
        if output_path in {
            receipt_path,
            candidate_path,
            policy_path,
            report_path,
            bundle_path,
            checksum_path,
        }:
            raise KovaEvidenceImportError("output-collides-with-input")
        report_raw, report_payload = parse_bounded_json(report_path, "report-invalid")
        source["report_sha256"] = kova_sha256_bytes(report_payload)
        if not isinstance(report_raw, dict):
            raise KovaEvidenceImportError("report-invalid")
        report_schema = report_raw.get("schemaVersion")
        if report_schema not in policy["supported_report_schemas"]:
            raise KovaEvidenceImportError("report-schema-unsupported")
        source["report_schema"] = report_schema
        if report_raw.get("mode") != mode or report_raw.get("runId") != run_id:
            raise KovaEvidenceImportError("receipt-report-mismatch")
        report_summary = normalize_kova_summary(report_raw.get("summary"))
        receipt_summary = normalize_kova_summary(receipt_raw.get("summary"))
        if report_summary != receipt_summary:
            raise KovaEvidenceImportError("receipt-report-mismatch")
        receipt_gate = receipt_raw.get("gate")
        report_gate = report_raw.get("gate")
        if receipt_gate is not None or report_gate is not None:
            if (
                not isinstance(receipt_gate, dict)
                or not isinstance(report_gate, dict)
                or receipt_gate.get("verdict") != "SHIP"
                or report_gate.get("verdict") != "SHIP"
            ):
                raise KovaEvidenceImportError("kova-gate-not-ship")

        source["bundle_sha256"] = validate_kova_checksum(bundle_path, checksum_path)
        source["artifact_index_sha256"], _ = validate_kova_bundle(
            bundle_path,
            report_path,
            report_payload,
            policy["reject_publication_omissions"],
        )
        identity, identity_missing, identity_errors = validate_kova_target_identity(
            receipt_raw,
            report_raw,
            artifact,
            policy["target_binding"]["accepted_identity_kinds"],
        )
        candidate_binding.update(identity)
        missing.extend(identity_missing)
        errors.extend(identity_errors)
        if any(
            "environment-matched-rehearsal" in requirement["gate_ids"]
            for requirement in policy["scenarios"]
        ):
            environment_missing, environment_errors = validate_kova_environment(
                report_raw, candidate_raw,
            )
            missing.extend(environment_missing)
            errors.extend(environment_errors)
        scenarios, scenario_missing, scenario_errors = aggregate_kova_scenarios(
            report_raw,
            policy,
        )
        missing.extend(scenario_missing)
        errors.extend(scenario_errors)
        if (
            candidate_binding["status"] == "mismatch"
            or "target-environment-mismatch" in errors
        ):
            status_value = "rejected"
        elif missing or errors:
            status_value = "incomplete"
        else:
            status_value = "accepted"
            gate_to_scenarios: dict[str, list[dict[str, Any]]] = {}
            scenario_by_id = {item["id"]: item for item in scenarios}
            for requirement in policy["scenarios"]:
                for gate_id in requirement["gate_ids"]:
                    gate_to_scenarios.setdefault(gate_id, []).append(
                        scenario_by_id[requirement["id"]]
                    )
            for gate_id in sorted(gate_to_scenarios):
                gate_content = {
                    "schema": "openclaw.safe_update.kova_gate_evidence.v1",
                    "policy_id": policy_id,
                    "gate_id": gate_id,
                    "target_candidate_root": target_root,
                    "target_identity_digest": candidate_binding["identity_digest"],
                    "receipt_sha256": source["receipt_sha256"],
                    "report_sha256": source["report_sha256"],
                    "bundle_sha256": source["bundle_sha256"],
                    "artifact_index_sha256": source["artifact_index_sha256"],
                    "scenarios": sorted(
                        gate_to_scenarios[gate_id], key=lambda item: item["id"]
                    ),
                }
                eligible_gates.append(
                    {"id": gate_id, "evidence_digest": canonical_digest(gate_content)}
                )
    except KovaEvidenceImportError as exc:
        status_value = "rejected"
        errors.append(exc.code)
    except (OSError, ValueError, TypeError, tarfile.TarError):
        status_value = "rejected"
        errors.append("import-failed")

    document = build_kova_evidence_document(
        status_value=status_value,
        policy_id=policy_id,
        candidate_binding=candidate_binding,
        source=source,
        scenarios=scenarios,
        eligible_gates=eligible_gates if status_value == "accepted" else [],
        missing_requirements=missing,
        error_codes=errors,
    )
    write_json(output_path, document)
    print(output_path)
    return 0 if status_value == "accepted" else 2


def parser() -> argparse.ArgumentParser:
    root = argparse.ArgumentParser(description=__doc__)
    subcommands = root.add_subparsers(dest="command", required=True)

    inventory_parser = subcommands.add_parser(
        "inventory", help="create a public-safe local installation inventory and coverage draft"
    )
    inventory_parser.add_argument("--package-root", type=Path, required=True)
    inventory_parser.add_argument("--package-name", default="openclaw")
    inventory_parser.add_argument("--output-dir", type=Path, required=True)
    inventory_parser.set_defaults(handler=inventory)

    attest_parser = subcommands.add_parser(
        "attest",
        help="create a public-safe local installation attestation",
    )
    attest_parser.add_argument("--candidate-lock", type=Path, required=True)
    attest_parser.add_argument("--observation", type=Path, required=True)
    attest_parser.add_argument("--ttl-seconds", type=int, default=900)
    attest_parser.add_argument("--output", type=Path, required=True)
    attest_parser.set_defaults(handler=attest)

    fetch_parser = subcommands.add_parser("fetch", help="fetch immutable npm package evidence")
    fetch_parser.add_argument("--current-version", required=True)
    fetch_parser.add_argument("--target-version", required=True)
    fetch_parser.add_argument("--packages-json", default='["openclaw"]')
    fetch_parser.add_argument("--platform-os", default=platform.system().lower())
    fetch_parser.add_argument("--platform-arch", default=platform.machine().lower())
    fetch_parser.add_argument(
        "--platform-libc",
        default=(platform.libc_ver()[0] or "unknown").lower(),
    )
    fetch_parser.add_argument("--output-dir", type=Path, required=True)
    fetch_parser.set_defaults(handler=fetch)

    simulate_parser = subcommands.add_parser("simulate", help="run a read-only package rehearsal")
    simulate_parser.add_argument("--input-dir", type=Path, required=True)
    simulate_parser.add_argument("--customizations", type=Path)
    simulate_parser.add_argument("--allow-no-customizations", action="store_true")
    simulate_parser.add_argument("--coverage", type=Path)
    simulate_parser.add_argument("--installation-contract", type=Path)
    simulate_parser.add_argument("--installation-attestation", type=Path)
    simulate_parser.add_argument("--conservative-inputs", type=Path)
    simulate_parser.add_argument("--disable-impact-shadow", action="store_true")
    simulate_parser.add_argument("--cache-dir", type=Path)
    simulate_parser.add_argument(
        "--archive-workers",
        type=archive_workers_argument,
        default=1,
    )
    simulate_parser.add_argument(
        "--archive-timeout-seconds",
        type=archive_timeout_argument,
        default=120.0,
    )
    simulate_parser.add_argument("--allow-no-coverage", action="store_true")
    simulate_parser.add_argument("--runtime-node-version")
    simulate_parser.add_argument("--runtime-os")
    simulate_parser.add_argument("--runtime-arch")
    simulate_parser.add_argument("--runtime-libc")
    simulate_parser.add_argument("--output-dir", type=Path, required=True)
    simulate_parser.set_defaults(handler=simulate)

    archive_parser = subcommands.add_parser(
        "_analyze-archive",
        help=argparse.SUPPRESS,
    )
    archive_parser.add_argument("--task-id", required=True)
    archive_parser.add_argument("--package", required=True)
    archive_parser.add_argument(
        "--lane",
        choices=("current", "target"),
        required=True,
    )
    archive_parser.add_argument("--path", type=Path, required=True)
    archive_parser.add_argument("--metadata-json", required=True)
    archive_parser.add_argument("--cache-dir", type=Path)
    archive_parser.set_defaults(handler=analyze_archive_command)

    contract_parser = subcommands.add_parser(
        "contract", help="translate v1.1 manifests into an installation contract"
    )
    contract_parser.add_argument("--customizations", type=Path, required=True)
    contract_parser.add_argument("--coverage", type=Path, required=True)
    contract_parser.add_argument("--output", type=Path, required=True)
    contract_parser.set_defaults(handler=contract)

    kova_parser = subcommands.add_parser(
        "kova-evidence",
        help="validate and import an existing Kova evidence bundle",
    )
    kova_parser.add_argument("--receipt", type=Path, required=True)
    kova_parser.add_argument("--candidate-lock", type=Path, required=True)
    kova_parser.add_argument("--policy", type=Path, required=True)
    kova_parser.add_argument("--output", type=Path, required=True)
    kova_parser.set_defaults(handler=kova_evidence)
    return root


def main() -> int:
    args = parser().parse_args()
    try:
        return args.handler(args)
    except (RehearsalError, OSError, tarfile.TarError, RecursionError) as exc:
        print(f"blocked: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
