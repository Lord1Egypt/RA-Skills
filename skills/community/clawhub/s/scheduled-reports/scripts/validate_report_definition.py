#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import ipaddress
import json
import re
import sys
from datetime import datetime
from pathlib import Path
from urllib.parse import urlparse
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError


ALLOWED_STATUSES = {"draft", "enabled", "paused", "archived"}
REPORT_ID_RE = re.compile(r"^[a-z0-9][a-z0-9_-]*$")
ALLOWED_DELIVERY_CHANNELS = {"email", "conversation", "thread", "webhook", "folder"}
ALLOWED_TRIGGER_TYPES = {"hourly", "daily", "weekly", "monthly"}
ALLOWED_WEEK_DAYS = {"MON", "TUE", "WED", "THU", "FRI", "SAT", "SUN"}
AUTOMATION_SESSION_TARGETS = {"isolated", "main", "current"}
TIME_RE = re.compile(r"^(?:[01]\d|2[0-3]):[0-5]\d$")
SHA256_RE = re.compile(r"^[a-f0-9]{64}$")
EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
ENVIRONMENT_FINGERPRINT_RE = re.compile(r"^skills:[a-z0-9._-]+(?:,[a-z0-9._-]+)*$")
DAY_LABELS = {
    "MON": "Monday",
    "TUE": "Tuesday",
    "WED": "Wednesday",
    "THU": "Thursday",
    "FRI": "Friday",
    "SAT": "Saturday",
    "SUN": "Sunday",
}
DATA_SOURCE_SIGNAL_KEYS = {
    "apiRequestRef",
    "datasetRef",
    "fileRef",
    "jobRef",
    "pipelineRef",
    "query",
    "queryFile",
    "sourceRef",
    "storedProcedure",
}
LOCKED_SUBTREE_KEYS = (
    "schedule",
    "delivery",
    "output",
    "dataSources",
    "uiDefinition",
    "executionPrompt",
    "runtimeGuards",
)


def load_json(path: Path) -> object:
    try:
        return json.loads(path.read_text(encoding="utf-8-sig"))
    except FileNotFoundError as exc:
        raise SystemExit(f"Input file not found: {path}") from exc
    except json.JSONDecodeError as exc:
        raise SystemExit(f"Invalid JSON in {path}: {exc}") from exc


def is_non_empty_string(value: object) -> bool:
    return isinstance(value, str) and bool(value.strip())


def add_error(errors: list[str], message: str) -> None:
    errors.append(message)


def validate_required_string(
    obj: dict[str, object],
    key: str,
    errors: list[str],
    path: str,
) -> str | None:
    value = obj.get(key)
    if not is_non_empty_string(value):
        add_error(errors, f"{path}.{key} must be a non-empty string")
        return None
    return str(value).strip()


def validate_required_object(
    obj: dict[str, object],
    key: str,
    errors: list[str],
    path: str,
) -> dict[str, object] | None:
    value = obj.get(key)
    if not isinstance(value, dict):
        add_error(errors, f"{path}.{key} must be an object")
        return None
    return value


def validate_non_empty_object(
    obj: dict[str, object],
    key: str,
    errors: list[str],
    path: str,
) -> dict[str, object] | None:
    value = validate_required_object(obj, key, errors, path)
    if value is not None and not value:
        add_error(errors, f"{path}.{key} must be a non-empty object")
        return None
    return value


def collect_list_of_strings(value: object) -> list[str]:
    if not isinstance(value, list):
        return []
    result: list[str] = []
    for item in value:
        if isinstance(item, str) and item.strip():
            result.append(item.strip())
    return result


def is_int_like(value: object) -> bool:
    return isinstance(value, int) and not isinstance(value, bool)


def validate_time_string(value: object, path: str, errors: list[str]) -> str | None:
    if not is_non_empty_string(value):
        add_error(errors, f"{path} must be a non-empty string in HH:MM format")
        return None
    normalized = str(value).strip()
    if not TIME_RE.match(normalized):
        add_error(errors, f"{path} must use HH:MM 24-hour format")
        return None
    return normalized


def validate_timezone_name(value: object, path: str, errors: list[str]) -> str | None:
    if not is_non_empty_string(value):
        add_error(errors, f"{path} must be a non-empty IANA timezone name")
        return None
    normalized = str(value).strip()
    try:
        ZoneInfo(normalized)
    except ZoneInfoNotFoundError:
        add_error(errors, f"{path} must be a valid IANA timezone name")
        return None
    return normalized


def validate_iso_datetime(value: object, path: str, errors: list[str]) -> str | None:
    if not is_non_empty_string(value):
        add_error(errors, f"{path} must be a non-empty ISO-8601 datetime string")
        return None
    normalized = str(value).strip()
    try:
        datetime.fromisoformat(normalized.replace("Z", "+00:00"))
    except ValueError:
        add_error(errors, f"{path} must be a valid ISO-8601 datetime string")
        return None
    return normalized


def validate_required_int(
    obj: dict[str, object],
    key: str,
    errors: list[str],
    path: str,
) -> int | None:
    value = obj.get(key)
    if not is_int_like(value):
        add_error(errors, f"{path}.{key} must be an integer")
        return None
    return int(value)


def validate_sha256_string(value: object, path: str, errors: list[str]) -> str | None:
    if not is_non_empty_string(value):
        add_error(errors, f"{path} must be a non-empty SHA-256 hex string")
        return None
    normalized = str(value).strip().lower()
    if not SHA256_RE.match(normalized):
        add_error(errors, f"{path} must be a 64-character lowercase SHA-256 hex string")
        return None
    return normalized


def validate_non_empty_day_list(value: object, path: str, errors: list[str]) -> list[str]:
    if not isinstance(value, list) or not value:
        add_error(errors, f"{path} must be a non-empty list of weekday codes")
        return []

    normalized: list[str] = []
    seen: set[str] = set()
    for index, item in enumerate(value):
        if not is_non_empty_string(item):
            add_error(errors, f"{path}[{index}] must be a non-empty weekday code")
            continue
        day = str(item).strip().upper()
        if day not in ALLOWED_WEEK_DAYS:
            add_error(
                errors,
                f"{path}[{index}] must be one of: {', '.join(sorted(ALLOWED_WEEK_DAYS))}",
            )
            continue
        if day in seen:
            add_error(errors, f"{path}[{index}] duplicates weekday {day}")
            continue
        seen.add(day)
        normalized.append(day)
    return normalized


def render_schedule_summary(trigger: dict[str, object]) -> str | None:
    trigger_type = trigger.get("type")
    if not isinstance(trigger_type, str):
        return None

    normalized_type = trigger_type.strip().lower()
    if normalized_type == "hourly":
        interval_hours = trigger.get("intervalHours", 1)
        minute = trigger.get("minute", 0)
        if not is_int_like(interval_hours) or not is_int_like(minute):
            return None
        if interval_hours == 1:
            return f"Every hour at minute {int(minute):02d}"
        return f"Every {int(interval_hours)} hours at minute {int(minute):02d}"

    if normalized_type == "daily":
        time_value = trigger.get("time")
        if isinstance(time_value, str):
            return f"Every day at {time_value.strip()}"
        return None

    if normalized_type == "weekly":
        days = trigger.get("days")
        time_value = trigger.get("time")
        if isinstance(days, list) and isinstance(time_value, str):
            labels = [DAY_LABELS.get(str(day).strip().upper(), str(day)) for day in days]
            return f"Every {', '.join(labels)} at {time_value.strip()}"
        return None

    if normalized_type == "monthly":
        day_of_month = trigger.get("dayOfMonth")
        time_value = trigger.get("time")
        if isinstance(day_of_month, int) and isinstance(time_value, str):
            return f"Day {day_of_month} of every month at {time_value.strip()}"
        return None

    return None


def validate_trigger(trigger: dict[str, object], errors: list[str]) -> None:
    trigger_type = validate_required_string(
        trigger, "type", errors, "definition.schedule.trigger"
    )
    if trigger_type is None:
        return

    normalized_type = trigger_type.lower()
    if normalized_type not in ALLOWED_TRIGGER_TYPES:
        add_error(
            errors,
            "definition.schedule.trigger.type must be one of: "
            + ", ".join(sorted(ALLOWED_TRIGGER_TYPES)),
        )
        return

    if normalized_type == "hourly":
        interval_hours = trigger.get("intervalHours", 1)
        if not is_int_like(interval_hours) or int(interval_hours) < 1:
            add_error(
                errors,
                "definition.schedule.trigger.intervalHours must be an integer >= 1 for hourly schedules",
            )
        minute = trigger.get("minute", 0)
        if not is_int_like(minute) or int(minute) < 0 or int(minute) > 59:
            add_error(
                errors,
                "definition.schedule.trigger.minute must be an integer between 0 and 59 for hourly schedules",
            )
        return

    if normalized_type == "daily":
        validate_time_string(
            trigger.get("time"),
            "definition.schedule.trigger.time",
            errors,
        )
        return

    if normalized_type == "weekly":
        validate_non_empty_day_list(
            trigger.get("days"),
            "definition.schedule.trigger.days",
            errors,
        )
        validate_time_string(
            trigger.get("time"),
            "definition.schedule.trigger.time",
            errors,
        )
        return

    if normalized_type == "monthly":
        day_of_month = trigger.get("dayOfMonth")
        if not is_int_like(day_of_month) or int(day_of_month) < 1 or int(day_of_month) > 31:
            add_error(
                errors,
                "definition.schedule.trigger.dayOfMonth must be an integer between 1 and 31 for monthly schedules",
            )
        validate_time_string(
            trigger.get("time"),
            "definition.schedule.trigger.time",
            errors,
        )
        return


def validate_email_address(
    value: object,
    path: str,
    errors: list[str],
    allowed_domains: set[str] | None = None,
) -> str | None:
    if not is_non_empty_string(value):
        add_error(errors, f"{path} must be a non-empty email address")
        return None
    normalized = str(value).strip()
    if not EMAIL_RE.match(normalized):
        add_error(errors, f"{path} must be a syntactically valid email address")
        return None
    domain = normalized.rsplit("@", 1)[1].lower()
    if allowed_domains is not None and domain not in allowed_domains:
        add_error(errors, f"{path} domain {domain} is not in delivery.policy.allowedDomains")
        return None
    return normalized


def validate_webhook_url(value: object, path: str, errors: list[str]) -> str | None:
    if not is_non_empty_string(value):
        add_error(errors, f"{path} must be a non-empty HTTPS URL")
        return None

    normalized = str(value).strip()
    parsed = urlparse(normalized)
    if parsed.scheme.lower() != "https":
        add_error(errors, f"{path} must use HTTPS")
        return None
    if not parsed.hostname:
        add_error(errors, f"{path} must include a hostname")
        return None

    host = parsed.hostname.lower()
    if host in {"localhost"} or host.endswith(".local"):
        add_error(errors, f"{path} must not target localhost or .local hosts")
        return None

    try:
        ip = ipaddress.ip_address(host)
    except ValueError:
        return normalized

    if any((ip.is_private, ip.is_loopback, ip.is_link_local, ip.is_reserved, ip.is_multicast)):
        add_error(errors, f"{path} must not target private, loopback, link-local, reserved, or multicast IPs")
        return None
    return normalized


def validate_folder_path(value: object, path: str, errors: list[str]) -> str | None:
    if not is_non_empty_string(value):
        add_error(errors, f"{path} must be a non-empty folder path")
        return None
    normalized = str(value).strip()
    parts = [part for part in re.split(r"[\\/]+", normalized) if part]
    if ".." in parts:
        add_error(errors, f"{path} must not contain parent-directory traversal")
        return None
    return normalized


def validate_delivery_target(
    delivery: dict[str, object],
    target: dict[str, object],
    channel: str,
    errors: list[str],
) -> None:
    policy = delivery.get("policy")
    allowed_domains: set[str] | None = None
    if policy is not None:
        if not isinstance(policy, dict):
            add_error(errors, "definition.delivery.policy must be an object when present")
        else:
            if "allowedDomains" in policy:
                domains = collect_list_of_strings(policy.get("allowedDomains"))
                if not domains:
                    add_error(errors, "definition.delivery.policy.allowedDomains must be a non-empty array when present")
                else:
                    allowed_domains = {domain.lower() for domain in domains}

    if channel == "email":
        to_value = target.get("to")
        cc_value = target.get("cc")
        bcc_value = target.get("bcc")
        contact = target.get("contact")
        if to_value is not None:
            if not isinstance(to_value, list) or not to_value:
                add_error(errors, "definition.delivery.target.to must be a non-empty array when present")
            else:
                for index, item in enumerate(to_value):
                    validate_email_address(
                        item,
                        f"definition.delivery.target.to[{index}]",
                        errors,
                        allowed_domains,
                    )
        if cc_value is not None:
            if not isinstance(cc_value, list):
                add_error(errors, "definition.delivery.target.cc must be an array when present")
            else:
                for index, item in enumerate(cc_value):
                    validate_email_address(
                        item,
                        f"definition.delivery.target.cc[{index}]",
                        errors,
                        allowed_domains,
                    )
        if bcc_value is not None:
            add_error(errors, "definition.delivery.target.bcc is not allowed in this package")
        if contact is not None:
            validate_email_address(
                contact,
                "definition.delivery.target.contact",
                errors,
                allowed_domains,
            )
        if to_value is None and contact is None:
            add_error(
                errors,
                "definition.delivery.target must contain to[] or contact for email delivery",
            )

        definition = delivery.get("definition")
        if not isinstance(definition, dict):
            add_error(errors, "definition.delivery.definition must be an object for email delivery")
        else:
            validate_required_string(definition, "subject", errors, "definition.delivery.definition")
        return

    if channel in {"conversation", "thread"}:
        if not (
            is_non_empty_string(target.get("conversationId"))
            or is_non_empty_string(target.get("threadId"))
        ):
            add_error(
                errors,
                "definition.delivery.target must contain conversationId or threadId for conversation delivery",
            )
        definition = delivery.get("definition")
        if not isinstance(definition, dict):
            add_error(errors, "definition.delivery.definition must be an object for conversation delivery")
        else:
            validate_required_string(definition, "messageTemplate", errors, "definition.delivery.definition")
        return

    if channel == "webhook":
        endpoint_alias = target.get("endpointAlias")
        url_value = target.get("url")
        if endpoint_alias is None and url_value is None:
            add_error(
                errors,
                "definition.delivery.target must contain endpointAlias or url for webhook delivery",
            )
            return
        if endpoint_alias is not None and not is_non_empty_string(endpoint_alias):
            add_error(
                errors,
                "definition.delivery.target.endpointAlias must be a non-empty string when present",
            )
        if url_value is not None:
            validate_webhook_url(url_value, "definition.delivery.target.url", errors)
        return

    if channel == "folder":
        validate_folder_path(target.get("path"), "definition.delivery.target.path", errors)


def resolve_reference_path(reference: str, input_path: Path) -> Path:
    candidate = Path(reference)
    if candidate.is_absolute():
        return candidate

    cwd_candidate = Path.cwd() / candidate
    if cwd_candidate.exists():
        return cwd_candidate.resolve()
    return (input_path.parent / candidate).resolve()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def validate_data_source_definition(
    value: object,
    data_source: dict[str, object],
    input_path: Path,
    errors: list[str],
    path: str,
) -> None:
    if not isinstance(value, dict):
        add_error(errors, f"{path} must be an object")
        return
    if not value:
        add_error(errors, f"{path} must be a non-empty object")
        return

    actionable = False
    for key in DATA_SOURCE_SIGNAL_KEYS:
        candidate = value.get(key)
        if is_non_empty_string(candidate):
            actionable = True
            break

    if not actionable:
        add_error(
            errors,
            f"{path} must contain at least one deterministic data key with a non-empty value: "
            + ", ".join(sorted(DATA_SOURCE_SIGNAL_KEYS)),
        )
        return

    parameters = value.get("parameters")
    if parameters is not None and not isinstance(parameters, dict):
        add_error(errors, f"{path}.parameters must be an object when present")

    query_file = value.get("queryFile")
    if query_file is not None:
        if not is_non_empty_string(query_file):
            add_error(errors, f"{path}.queryFile must be a non-empty string when present")
            return
        query_file_hash = validate_sha256_string(
            data_source.get("queryFileSha256"),
            f"{path.rsplit('.', 1)[0]}.queryFileSha256",
            errors,
        )
        resolved_path = resolve_reference_path(str(query_file).strip(), input_path)
        if not resolved_path.exists() or not resolved_path.is_file():
            add_error(errors, f"{path}.queryFile must point to an existing file: {resolved_path}")
            return
        if query_file_hash is not None:
            actual_hash = sha256_file(resolved_path)
            if actual_hash != query_file_hash:
                add_error(
                    errors,
                    f"{path.rsplit('.', 1)[0]}.queryFileSha256 does not match the contents of {resolved_path}",
                )


def validate_data_sources(value: object, input_path: Path, errors: list[str]) -> list[str]:
    if not isinstance(value, list) or not value:
        add_error(errors, "definition.dataSources must be a non-empty array")
        return []

    ids: list[str] = []
    seen: set[str] = set()
    for index, item in enumerate(value):
        path = f"definition.dataSources[{index}]"
        if not isinstance(item, dict):
            add_error(errors, f"{path} must be an object")
            continue

        data_source_id = validate_required_string(item, "id", errors, path)
        if data_source_id and not REPORT_ID_RE.match(data_source_id):
            add_error(
                errors,
                f"{path}.id must contain only lowercase letters, digits, hyphens, or underscores",
            )
        if data_source_id:
            if data_source_id in seen:
                add_error(errors, f"{path}.id duplicates data source id {data_source_id}")
            seen.add(data_source_id)
            ids.append(data_source_id)

        validate_required_string(item, "backend", errors, path)
        validate_required_string(item, "purpose", errors, path)
        validate_data_source_definition(item.get("definition"), item, input_path, errors, f"{path}.definition")
    return ids


def validate_component(component: object, path: str, errors: list[str]) -> None:
    if not isinstance(component, dict):
        add_error(errors, f"{path} must be an object")
        return

    validate_required_string(component, "kind", errors, path)
    title = component.get("title")
    instructions = component.get("instructions")
    if not is_non_empty_string(title) and not is_non_empty_string(instructions):
        add_error(
            errors,
            f"{path} must contain title or instructions to explain the component intent",
        )


def validate_ui_definition(value: object, errors: list[str]) -> None:
    if not isinstance(value, dict):
        add_error(errors, "definition.uiDefinition must be an object")
        return
    if not value:
        add_error(errors, "definition.uiDefinition must be a non-empty object")
        return

    validate_required_string(value, "summary", errors, "definition.uiDefinition")

    has_must_include = bool(collect_list_of_strings(value.get("mustInclude")))
    has_constraints = bool(collect_list_of_strings(value.get("constraints")))
    components = value.get("components")
    has_components = isinstance(components, list) and bool(components)

    if not any((has_must_include, has_constraints, has_components)):
        add_error(
            errors,
            "definition.uiDefinition must contain at least one of mustInclude[], constraints[], or components[]",
        )

    if components is not None:
        if not isinstance(components, list) or not components:
            add_error(errors, "definition.uiDefinition.components must be a non-empty array")
        else:
            for index, component in enumerate(components):
                validate_component(
                    component,
                    f"definition.uiDefinition.components[{index}]",
                    errors,
                )

    dynamic_layout = value.get("dynamicLayout")
    if dynamic_layout is not None and not isinstance(dynamic_layout, bool):
        add_error(errors, "definition.uiDefinition.dynamicLayout must be a boolean when present")


def validate_runtime_guards(value: object, errors: list[str]) -> None:
    if not isinstance(value, dict):
        add_error(errors, "definition.runtimeGuards must be an object")
        return

    required_exact_values = {
        "treatDataAsUntrusted": True,
        "allowDataDrivenToolCalls": False,
        "allowDataDrivenRecipients": False,
        "enforceApprovedDeliveryTarget": True,
    }
    for key, expected_value in required_exact_values.items():
        actual_value = value.get(key)
        if actual_value is not expected_value:
            add_error(errors, f"definition.runtimeGuards.{key} must be {json.dumps(expected_value)}")


def validate_environment_fingerprint(value: str, errors: list[str]) -> None:
    if not ENVIRONMENT_FINGERPRINT_RE.match(value):
        add_error(
            errors,
            "definition.verification.environmentFingerprint must use the canonical skills:<name>[,<name>...] format",
        )
        return

    items = value.removeprefix("skills:").split(",")
    if len(items) != len(set(items)):
        add_error(
            errors,
            "definition.verification.environmentFingerprint must not contain duplicate skill names",
        )
    if items != sorted(items):
        add_error(
            errors,
            "definition.verification.environmentFingerprint must list skill names in ascending lexicographic order",
        )


def validate_preview(value: object, input_path: Path, errors: list[str]) -> None:
    if not isinstance(value, dict):
        add_error(errors, "definition.preview must be an object when present")
        return
    artifact_ref = validate_required_string(value, "artifactRef", errors, "definition.preview")
    if artifact_ref is not None:
        resolved_path = resolve_reference_path(artifact_ref, input_path)
        if not resolved_path.exists() or not resolved_path.is_file():
            add_error(
                errors,
                f"definition.preview.artifactRef must point to an existing file: {resolved_path}",
            )


def validate_approval(value: object, expected_hash: str | None, errors: list[str]) -> None:
    if not isinstance(value, dict):
        add_error(errors, "definition.approval must be an object when present")
        return

    validate_iso_datetime(value.get("approvedAt"), "definition.approval.approvedAt", errors)
    approved_by = validate_required_object(value, "approvedBy", errors, "definition.approval")
    if approved_by is not None:
        if not (
            is_non_empty_string(approved_by.get("id"))
            or is_non_empty_string(approved_by.get("displayName"))
        ):
            add_error(errors, "definition.approval.approvedBy must contain id or displayName")

    approved_hash = validate_sha256_string(
        value.get("approvedSubtreeSha256"),
        "definition.approval.approvedSubtreeSha256",
        errors,
    )
    if approved_hash is not None and expected_hash is not None and approved_hash != expected_hash:
        add_error(
            errors,
            "definition.approval.approvedSubtreeSha256 must match definition.integrity.lockedSubtreeSha256",
        )


def canonical_json_bytes(value: object) -> bytes:
    return json.dumps(value, ensure_ascii=True, sort_keys=True, separators=(",", ":")).encode("utf-8")


def build_locked_subtree(payload: dict[str, object]) -> dict[str, object]:
    return {key: payload.get(key) for key in LOCKED_SUBTREE_KEYS}


def compute_locked_subtree_sha256(payload: dict[str, object]) -> str:
    return hashlib.sha256(canonical_json_bytes(build_locked_subtree(payload))).hexdigest()


def validate_integrity(payload: dict[str, object], errors: list[str]) -> None:
    integrity = validate_required_object(payload, "integrity", errors, "definition")
    if integrity is None:
        return

    expected_hash = validate_sha256_string(
        integrity.get("lockedSubtreeSha256"),
        "definition.integrity.lockedSubtreeSha256",
        errors,
    )
    if expected_hash is None:
        return

    actual_hash = compute_locked_subtree_sha256(payload)
    if actual_hash != expected_hash:
        add_error(errors, "definition.integrity.lockedSubtreeSha256 does not match the current locked subtree")


def validate_automation(value: object, errors: list[str]) -> None:
    if not isinstance(value, dict):
        add_error(errors, "definition.automation must be an object when present")
        return

    platform = validate_required_string(value, "platform", errors, "definition.automation")
    kind = validate_required_string(value, "kind", errors, "definition.automation")
    validate_required_string(value, "jobId", errors, "definition.automation")

    if platform and platform.lower() != "openclaw":
        add_error(errors, "definition.automation.platform must be openclaw when present")
    if kind and kind.lower() != "cron":
        add_error(errors, "definition.automation.kind must be cron when present")

    session_target = value.get("sessionTarget")
    if session_target is not None:
        if not is_non_empty_string(session_target):
            add_error(
                errors,
                "definition.automation.sessionTarget must be a non-empty string when present",
            )
        else:
            normalized = str(session_target).strip()
            if normalized not in AUTOMATION_SESSION_TARGETS and not normalized.startswith("session:"):
                add_error(
                    errors,
                    "definition.automation.sessionTarget must be isolated, main, current, or session:<id>",
                )


def validate_verification(
    value: object,
    automation: dict[str, object] | None,
    expected_hash: str | None,
    errors: list[str],
) -> None:
    if not isinstance(value, dict):
        add_error(errors, "definition.verification must be an object when present")
        return

    validate_iso_datetime(
        value.get("activationCheckAt"),
        "definition.verification.activationCheckAt",
        errors,
    )
    mode = validate_required_string(
        value,
        "activationCheckMode",
        errors,
        "definition.verification",
    )
    fingerprint = validate_required_string(
        value,
        "environmentFingerprint",
        errors,
        "definition.verification",
    )
    if fingerprint is not None:
        validate_environment_fingerprint(fingerprint, errors)
    verified_hash = validate_sha256_string(
        value.get("verifiedSubtreeSha256"),
        "definition.verification.verifiedSubtreeSha256",
        errors,
    )
    if verified_hash is not None and expected_hash is not None and verified_hash != expected_hash:
        add_error(
            errors,
            "definition.verification.verifiedSubtreeSha256 must match definition.integrity.lockedSubtreeSha256",
        )
    if automation is not None and mode is not None:
        session_target = automation.get("sessionTarget")
        if is_non_empty_string(session_target) and str(session_target).strip() != mode:
            add_error(
                errors,
                "definition.verification.activationCheckMode must match definition.automation.sessionTarget",
            )


def validate_lifecycle_invariants(payload: dict[str, object], errors: list[str]) -> None:
    if payload.get("approval") is not None and payload.get("integrity") is None:
        add_error(errors, "definition.approval requires definition.integrity")
    if payload.get("verification") is not None and payload.get("integrity") is None:
        add_error(errors, "definition.verification requires definition.integrity")

    status = payload.get("status")
    if not isinstance(status, str):
        return

    if status not in {"enabled", "paused"}:
        return

    if payload.get("preview") is None:
        add_error(errors, f"definition.{status} reports must include preview metadata")
    if payload.get("approval") is None:
        add_error(errors, f"definition.{status} reports must include approval metadata")
    if payload.get("integrity") is None:
        add_error(errors, f"definition.{status} reports must include integrity metadata")
    if payload.get("automation") is None:
        add_error(errors, f"definition.{status} reports must include automation metadata")
    if payload.get("verification") is None:
        add_error(errors, f"definition.{status} reports must include verification metadata")


def validate_definition(payload: object, input_path: Path) -> tuple[bool, dict[str, object]]:
    errors: list[str] = []

    if not isinstance(payload, dict):
        return False, {
            "valid": False,
            "input": str(input_path),
            "errors": ["Top-level JSON value must be an object"],
        }

    schema_version = validate_required_int(payload, "schemaVersion", errors, "definition")
    if schema_version is not None and schema_version != 1:
        add_error(errors, "definition.schemaVersion must be 1 in this package")

    report_id = validate_required_string(payload, "reportId", errors, "definition")
    if report_id and not REPORT_ID_RE.match(report_id):
        add_error(
            errors,
            "definition.reportId must contain only lowercase letters, digits, hyphens, or underscores",
        )

    name = validate_required_string(payload, "name", errors, "definition")
    purpose = validate_required_string(payload, "purpose", errors, "definition")

    owner = validate_required_object(payload, "owner", errors, "definition")
    if owner is not None:
        if not (
            is_non_empty_string(owner.get("id"))
            or is_non_empty_string(owner.get("displayName"))
        ):
            add_error(errors, "definition.owner must contain id or displayName")

    status = validate_required_string(payload, "status", errors, "definition")
    if status and status not in ALLOWED_STATUSES:
        add_error(
            errors,
            f"definition.status must be one of: {', '.join(sorted(ALLOWED_STATUSES))}",
        )

    schedule = validate_required_object(payload, "schedule", errors, "definition")
    schedule_summary = None
    if schedule is not None:
        validate_timezone_name(schedule.get("timezone"), "definition.schedule.timezone", errors)
        schedule_summary = validate_required_string(
            schedule,
            "summary",
            errors,
            "definition.schedule",
        )
        trigger = validate_non_empty_object(schedule, "trigger", errors, "definition.schedule")
        if trigger is not None:
            validate_trigger(trigger, errors)
            expected_summary = render_schedule_summary(trigger)
            if expected_summary is not None and schedule_summary is not None and schedule_summary != expected_summary:
                add_error(
                    errors,
                    "definition.schedule.summary must match the canonical summary derived from definition.schedule.trigger",
                )

    delivery = validate_required_object(payload, "delivery", errors, "definition")
    delivery_channel = None
    if delivery is not None:
        delivery_channel = validate_required_string(
            delivery, "channel", errors, "definition.delivery"
        )
        target = validate_required_object(delivery, "target", errors, "definition.delivery")
        if target is not None and delivery_channel:
            normalized_channel = delivery_channel.lower()
            if normalized_channel not in ALLOWED_DELIVERY_CHANNELS:
                add_error(
                    errors,
                    "definition.delivery.channel must be one of: "
                    + ", ".join(sorted(ALLOWED_DELIVERY_CHANNELS)),
                )
            else:
                validate_delivery_target(delivery, target, normalized_channel, errors)

    output = validate_required_object(payload, "output", errors, "definition")
    output_type = None
    if output is not None:
        output_type = validate_required_string(output, "type", errors, "definition.output")
        filename_template = output.get("filenameTemplate")
        if filename_template is not None and not is_non_empty_string(filename_template):
            add_error(
                errors,
                "definition.output.filenameTemplate must be a non-empty string when present",
            )

    data_source_ids = validate_data_sources(payload.get("dataSources"), input_path, errors)
    validate_ui_definition(payload.get("uiDefinition"), errors)
    validate_required_string(payload, "executionPrompt", errors, "definition")
    validate_runtime_guards(payload.get("runtimeGuards"), errors)

    integrity_hash: str | None = None
    integrity = payload.get("integrity")
    if isinstance(integrity, dict):
        candidate_hash = integrity.get("lockedSubtreeSha256")
        if is_non_empty_string(candidate_hash):
            normalized_hash = str(candidate_hash).strip().lower()
            if SHA256_RE.match(normalized_hash):
                integrity_hash = normalized_hash

    preview = payload.get("preview")
    if preview is not None:
        validate_preview(preview, input_path, errors)

    approval = payload.get("approval")
    if approval is not None:
        validate_approval(approval, integrity_hash, errors)

    automation = payload.get("automation")
    if automation is not None:
        validate_automation(automation, errors)

    verification = payload.get("verification")
    if verification is not None:
        validate_verification(
            verification,
            automation if isinstance(automation, dict) else None,
            integrity_hash,
            errors,
        )

    if payload.get("integrity") is not None:
        validate_integrity(payload, errors)

    validate_lifecycle_invariants(payload, errors)

    result = {
        "valid": not errors,
        "input": str(input_path),
        "schemaVersion": schema_version,
        "reportId": report_id,
        "name": name,
        "purpose": purpose,
        "status": status,
        "scheduleSummary": schedule_summary,
        "deliveryChannel": delivery_channel,
        "outputType": output_type,
        "dataSourceIds": data_source_ids,
        "errors": errors,
    }
    return not errors, result


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Validate a saved recurring-report definition."
    )
    parser.add_argument(
        "--input",
        required=True,
        help="Path to the JSON report definition to validate",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    input_path = Path(args.input).expanduser().resolve()
    payload = load_json(input_path)
    valid, result = validate_definition(payload, input_path)
    print(json.dumps(result, ensure_ascii=True, indent=2))
    return 0 if valid else 1


if __name__ == "__main__":
    sys.exit(main())
