#!/usr/bin/env python3
"""Persistent local fallback store for pt-agent host implementations.

This script is intentionally small and dependency-free. It stores only config
records and secret references, never resolved secret values or torrent bytes.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


STORE_VERSION = "1.0"


class StoreError(Exception):
    def __init__(self, code: str, message: str, **extra: Any) -> None:
        self.payload = {"code": code, "message": message, **extra}
        super().__init__(message)


def _expanded_path(value: str) -> Path:
    return Path(os.path.expandvars(value)).expanduser()


def _installed_host_home(skill_root: Path | None = None) -> Path | None:
    """Infer the host home when the skill is installed as <host>/skills/pt-agent."""
    skill_root = skill_root or Path(__file__).resolve().parents[1]
    if skill_root.name != "pt-agent":
        return None
    for parent in skill_root.parents:
        if parent.name == "skills":
            return parent.parent
    return None


def default_store_info() -> tuple[Path, str]:
    """Resolve a host-neutral default store path.

    Priority:
    1. PT_AGENT_STORE points to the exact JSON file.
    2. PT_AGENT_HOME points to a pt-agent data directory.
    3. Host-specific homes when the host exposes one.
    4. Installed skill location, e.g. ~/.codex/skills/pt-agent.
    5. XDG state directory or ~/.local/state as the final fallback.
    """
    if value := os.environ.get("PT_AGENT_STORE"):
        return _expanded_path(value), "PT_AGENT_STORE"
    if value := os.environ.get("PT_AGENT_HOME"):
        return _expanded_path(value) / "store.json", "PT_AGENT_HOME"
    for env_name in ("CODEX_HOME", "HERMES_HOME", "OPENCLAW_HOME"):
        if value := os.environ.get(env_name):
            return _expanded_path(value) / "pt-agent" / "store.json", env_name
    if host_home := _installed_host_home():
        return host_home / "pt-agent" / "store.json", "installed_skill_home"
    if value := os.environ.get("XDG_STATE_HOME"):
        return _expanded_path(value) / "pt-agent" / "store.json", "XDG_STATE_HOME"
    return Path.home() / ".local" / "state" / "pt-agent" / "store.json", "xdg_state_fallback"


def resolve_store_path(override: str | None = None) -> tuple[Path, str]:
    if override:
        return _expanded_path(override), "--store"
    return default_store_info()


DEFAULT_STORE, DEFAULT_STORE_SOURCE = default_store_info()
PROFILE_OR_COOKIE_ONLY_ADAPTERS = {
    "nexusphp",
    "unit3d",
    "gazelle",
    "luminance",
    "rartracker",
    "tcg",
    "xbtit",
    "tbsource",
    "tbdev",
    "selector",
}
SAFE_REF_PREFIXES = ("secret://", "env://", "profile://", "proxy://")
REDACTED = "[redacted]"
SENSITIVE_QUERY_KEYS = {
    "apikey",
    "api_key",
    "auth",
    "cookie",
    "key",
    "passkey",
    "password",
    "rsskey",
    "token",
    "uid",
}


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def empty_store() -> dict[str, Any]:
    return {
        "version": STORE_VERSION,
        "trackers": {},
        "trackerDrafts": {},
        "trackerStats": {},
        "downloaders": {},
        "searchSolutions": {},
        "interactionState": {},
        "updatedAt": now_iso(),
    }


def load_store(path: Path) -> dict[str, Any]:
    if not path.exists():
        return empty_store()
    try:
        with path.open("r", encoding="utf-8") as fh:
            data = json.load(fh)
    except json.JSONDecodeError as exc:
        raise StoreError("store_invalid_json", "Store file is not valid JSON.", path=str(path), line=exc.lineno, column=exc.colno) from exc
    except OSError as exc:
        raise StoreError("store_unreadable", "Store file could not be read.", path=str(path)) from exc
    if not isinstance(data, dict):
        raise StoreError("store_invalid_shape", "Store root must be a JSON object.", path=str(path))
    base = empty_store()
    for key, value in data.items():
        base[key] = value
    return base


def atomic_write(path: Path, data: dict[str, Any]) -> None:
    import tempfile

    try:
        path.parent.mkdir(parents=True, exist_ok=True)
    except OSError as exc:
        raise StoreError("store_parent_unwritable", "Store directory could not be created.", path=str(path.parent)) from exc
    data["updatedAt"] = now_iso()
    try:
        fd, tmp_name = tempfile.mkstemp(prefix=".store.", suffix=".json", dir=str(path.parent))
    except OSError as exc:
        raise StoreError("store_tempfile_failed", "Temporary store file could not be created.", path=str(path.parent)) from exc
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as fh:
            json.dump(data, fh, ensure_ascii=False, indent=2, sort_keys=True)
            fh.write("\n")
        os.replace(tmp_name, path)
    except OSError as exc:
        raise StoreError("store_write_failed", "Store file could not be written.", path=str(path)) from exc
    finally:
        if os.path.exists(tmp_name):
            os.unlink(tmp_name)


def normalize_id(value: str) -> str:
    value = value.strip().lower()
    value = re.sub(r"[^a-z0-9]+", "-", value).strip("-")
    return value or "unnamed"


def looks_like_raw_secret(value: str) -> bool:
    if value.startswith(SAFE_REF_PREFIXES):
        return False
    if re.fullmatch(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d+)?(?:Z|[+-]\d{2}:\d{2})", value):
        return False
    lower = value.lower()
    if len(value) >= 32 and re.search(r"[A-Za-z]", value) and re.search(r"\d", value):
        return True
    if "cookie:" in lower or "set-cookie:" in lower:
        return True
    if re.search(r"(^|[?&;])(?:passkey|token|auth|apikey|api_key|rsskey|key|uid|password)=", lower):
        return True
    if re.search(r"(^|[;\s])[A-Za-z0-9_%.-]{2,}=([^;\s]{8,}|[^;]*%[0-9a-f]{2})", value, flags=re.I):
        return True
    return False


def secretish_key(key: str) -> bool:
    compact = re.sub(r"[^a-z0-9]", "", key.lower())
    if compact == "secretrefs":
        return False
    if compact in {
        "cookie",
        "credential",
        "password",
        "passwd",
        "passkey",
        "pwd",
        "secret",
        "setcookie",
        "token",
    }:
        return True
    return compact.endswith(("apikey", "apitoken", "passkey", "password", "secret", "token", "cookie"))


def reference_key(key: str) -> bool:
    compact = re.sub(r"[^a-z0-9]", "", key.lower())
    return compact in {
        "apikeyref",
        "cookieref",
        "credentialref",
        "feedurlref",
        "profileref",
        "proxyref",
        "secretref",
    }


def safe_reference(value: Any) -> bool:
    return isinstance(value, str) and value.startswith(SAFE_REF_PREFIXES)


def redact_url_if_sensitive(value: str) -> str:
    if "://" not in value or "?" not in value:
        return value
    try:
        parsed = re.split(r"[?&]", value.split("?", 1)[1])
    except IndexError:
        return value
    for pair in parsed:
        key = pair.split("=", 1)[0].lower()
        if key in SENSITIVE_QUERY_KEYS:
            return REDACTED
    return value


def redact_for_output(obj: Any, path: str = "") -> Any:
    if isinstance(obj, dict):
        redacted: dict[str, Any] = {}
        for key, value in obj.items():
            child_path = f"{path}.{key}" if path else key
            if (secretish_key(key) or reference_key(key)) and not safe_reference(value):
                redacted[key] = REDACTED
            else:
                redacted[key] = redact_for_output(value, child_path)
        return redacted
    if isinstance(obj, list):
        return [redact_for_output(value, f"{path}[{index}]") for index, value in enumerate(obj)]
    if isinstance(obj, str):
        value = redact_url_if_sensitive(obj)
        if value != obj or looks_like_raw_secret(value):
            return REDACTED
    return obj


def collect_raw_secret_paths(obj: Any, path: str = "") -> list[str]:
    findings: list[str] = []
    if isinstance(obj, dict):
        for key, value in obj.items():
            child_path = f"{path}.{key}" if path else key
            if (secretish_key(key) or reference_key(key)) and not safe_reference(value):
                findings.append(child_path)
                continue
            findings.extend(collect_raw_secret_paths(value, child_path))
    elif isinstance(obj, list):
        for index, value in enumerate(obj):
            findings.extend(collect_raw_secret_paths(value, f"{path}[{index}]"))
    elif isinstance(obj, str) and looks_like_raw_secret(obj):
        findings.append(path or "$")
    return findings


def drop_raw_secrets(obj: Any, path: str = "") -> tuple[Any, list[str]]:
    removed: list[str] = []
    if isinstance(obj, dict):
        cleaned: dict[str, Any] = {}
        for key, value in obj.items():
            child_path = f"{path}.{key}" if path else key
            if (secretish_key(key) or reference_key(key)) and not safe_reference(value):
                removed.append(child_path)
                continue
            cleaned_value, child_removed = drop_raw_secrets(value, child_path)
            cleaned[key] = cleaned_value
            removed.extend(child_removed)
        return cleaned, removed
    if isinstance(obj, list):
        cleaned_list = []
        for index, value in enumerate(obj):
            cleaned_value, child_removed = drop_raw_secrets(value, f"{path}[{index}]")
            cleaned_list.append(cleaned_value)
            removed.extend(child_removed)
        return cleaned_list, removed
    if isinstance(obj, str) and looks_like_raw_secret(obj):
        removed.append(path or "$")
        return None, removed
    return obj, removed


def reject_raw_secrets(obj: Any, path: str = "") -> None:
    if isinstance(obj, dict):
        for key, value in obj.items():
            child_path = f"{path}.{key}" if path else key
            if (secretish_key(key) or reference_key(key)) and not safe_reference(value):
                raise StoreError("unsafe_secret_value", f"Refusing to store raw secret-like value at {child_path}; use secret:// or env:// reference.", fieldPath=child_path)
            reject_raw_secrets(value, f"{path}.{key}" if path else key)
    elif isinstance(obj, list):
        for index, value in enumerate(obj):
            reject_raw_secrets(value, f"{path}[{index}]")
    elif isinstance(obj, str) and looks_like_raw_secret(obj):
        raise StoreError("unsafe_secret_value", f"Refusing to store raw secret-like value at {path}; use secret:// or env:// reference.", fieldPath=path)


def load_json_arg(value: str) -> dict[str, Any]:
    try:
        data = json.loads(value)
    except json.JSONDecodeError as exc:
        raise StoreError("invalid_json_arg", "Argument must be a valid JSON object.", line=exc.lineno, column=exc.colno) from exc
    if not isinstance(data, dict):
        raise StoreError("invalid_json_arg", "Argument must be a JSON object.")
    reject_raw_secrets(data)
    return data


def upsert_record(store: dict[str, Any], bucket: str, record: dict[str, Any]) -> dict[str, Any]:
    record_id = record.get("id") or record.get("sitePresetId") or record.get("displayName") or record.get("baseUrl")
    if not record_id:
        raise StoreError("validation_failed", "Record requires id, sitePresetId, displayName, or baseUrl.")
    record_id = normalize_id(str(record_id))
    existing = store.setdefault(bucket, {}).get(record_id, {})
    merged = {**existing, **record, "id": record_id, "updatedAt": now_iso()}
    if "createdAt" not in merged:
        merged["createdAt"] = existing.get("createdAt", now_iso())
    store[bucket][record_id] = merged
    return merged


def tracker_is_enabled_config(record: dict[str, Any]) -> bool:
    if record.get("enabled") is False:
        return False
    status = record.get("status")
    if status in {"active", "configured", "enabled"}:
        return True
    return status is None and record.get("enabled") is True


def upsert_tracker_stats(store: dict[str, Any], tracker_id: str, stats: dict[str, Any]) -> dict[str, Any]:
    tracker_id = normalize_id(tracker_id)
    if not tracker_id:
        raise StoreError("validation_failed", "Stats require tracker id.")
    existing = store.setdefault("trackerStats", {}).get(tracker_id, {})
    sanitized = sanitize_stats(stats)
    merged = {
        **existing,
        **sanitized,
        "trackerId": tracker_id,
        "updatedAt": now_iso(),
    }
    if sanitized.get("status") == "ok" and "message" not in sanitized:
        merged.pop("message", None)
    if sanitized.get("status") and sanitized.get("status") != "ok":
        for key in (
            "userId",
            "username",
            "levelName",
            "uploadedBytes",
            "downloadedBytes",
            "trueUploadedBytes",
            "trueDownloadedBytes",
            "ratio",
            "bonus",
            "bonusPerHour",
            "seeding",
            "seedingSizeBytes",
            "leeching",
            "invitations",
            "unreadMessages",
            "warnings",
            "hnrPreWarning",
            "hnrUnsatisfied",
        ):
            if key not in sanitized:
                merged.pop(key, None)
    if "createdAt" not in merged:
        merged["createdAt"] = existing.get("createdAt", now_iso())
    store["trackerStats"][tracker_id] = merged
    return merged


def sanitize_stats(stats: dict[str, Any]) -> dict[str, Any]:
    allowed = {
        "status",
        "message",
        "userId",
        "username",
        "levelName",
        "uploadedBytes",
        "downloadedBytes",
        "trueUploadedBytes",
        "trueDownloadedBytes",
        "ratio",
        "bonus",
        "bonusPerHour",
        "seeding",
        "seedingSizeBytes",
        "leeching",
        "invitations",
        "unreadMessages",
        "warnings",
        "hnrPreWarning",
        "hnrUnsatisfied",
        "lastCheckedAt",
    }
    sanitized = {key: value for key, value in stats.items() if key in allowed}
    reject_raw_secrets(sanitized)
    return sanitized


def find_tracker(store: dict[str, Any], query: str) -> dict[str, Any] | None:
    q = query.strip().lower()
    buckets = (store.get("trackers", {}), store.get("trackerDrafts", {}))
    for bucket in buckets:
        for record in bucket.values():
            candidates = [
                record.get("id"),
                record.get("displayName"),
                record.get("sitePresetId"),
                record.get("baseUrl"),
            ]
            candidates.extend(record.get("aka", []) if isinstance(record.get("aka"), list) else [])
            if any(str(candidate or "").strip().lower() == q for candidate in candidates):
                return record
            if record.get("baseUrl") and q in str(record.get("baseUrl")).lower():
                return record
    return None


def migrate_legacy(path: Path, legacy_path: Path) -> dict[str, Any]:
    store = load_store(path)
    if not legacy_path.exists():
        return store
    try:
        with legacy_path.open("r", encoding="utf-8") as fh:
            legacy = json.load(fh)
    except json.JSONDecodeError as exc:
        raise StoreError("legacy_invalid_json", "Legacy config is not valid JSON.", path=str(legacy_path), line=exc.lineno, column=exc.colno) from exc
    except OSError as exc:
        raise StoreError("legacy_unreadable", "Legacy config could not be read.", path=str(legacy_path)) from exc
    if not isinstance(legacy, dict):
        raise StoreError("legacy_invalid_shape", "Legacy config root must be a JSON object.", path=str(legacy_path))
    for tracker in legacy.get("trackers", []):
        tracker, removed = drop_raw_secrets(dict(tracker))
        auth_mode = tracker.get("authMode")
        status = "pending_validation"
        if removed:
            status = "pending_credential"
            tracker["credentialIssue"] = "Legacy import omitted raw secret fields; provide profileRef or secretRef."
        adapter_id = str(tracker.get("adapterId") or "").strip().lower()
        if auth_mode == "api_token" and adapter_id in PROFILE_OR_COOKIE_ONLY_ADAPTERS:
            status = "invalid_credential"
            tracker["credentialIssue"] = f"{adapter_id} does not accept api_token; use profileRef or secretRefs.cookie."
        tracker["status"] = status
        upsert_record(store, "trackerDrafts", tracker)
    for downloader in legacy.get("downloaders", []):
        downloader, removed = drop_raw_secrets(dict(downloader))
        if removed:
            downloader["status"] = "pending_credential"
            downloader["credentialIssue"] = "Legacy import omitted raw secret fields; provide credentialRef."
        upsert_record(store, "downloaders", downloader)
    store["legacyImportedFrom"] = str(legacy_path)
    atomic_write(path, store)
    return store


def store_location(path: Path, source: str) -> dict[str, Any]:
    return {
        "ok": True,
        "store": str(path),
        "storeSource": source,
        "exists": path.exists(),
        "parent": str(path.parent),
        "parentExists": path.parent.exists(),
    }


def store_doctor(path: Path, source: str, store: dict[str, Any]) -> dict[str, Any]:
    findings = sorted(set(collect_raw_secret_paths(store)))
    warnings: list[str] = []
    if findings:
        warnings.append("raw_secret_like_paths_detected")
    if path.exists() and not path.is_file():
        warnings.append("store_path_is_not_file")
    if path.parent.exists() and not os.access(path.parent, os.W_OK):
        warnings.append("store_parent_not_writable")
    return {
        **store_location(path, source),
        "ok": not findings and "store_path_is_not_file" not in warnings,
        "version": store.get("version"),
        "counts": {
            "trackers": len(store.get("trackers", {})),
            "trackerDrafts": len(store.get("trackerDrafts", {})),
            "trackerStats": len(store.get("trackerStats", {})),
            "downloaders": len(store.get("downloaders", {})),
            "searchSolutions": len(store.get("searchSolutions", {})),
        },
        "rawSecretLikePaths": findings,
        "warnings": warnings,
    }


def env_name(record_id: str, purpose: str, existing: set[str]) -> str:
    base = f"PT_AGENT_{normalize_id(record_id).replace('-', '_').upper()}_{purpose}"
    candidate = base
    suffix = 2
    while candidate in existing:
        candidate = f"{base}_{suffix}"
        suffix += 1
    existing.add(candidate)
    return candidate


def dotenv_quote(value: str) -> str:
    escaped = value.replace("\\", "\\\\").replace('"', '\\"').replace("\n", "\\n").replace("\r", "\\r")
    return f'"{escaped}"'


def append_env_values(path: Path, values: dict[str, str]) -> None:
    import tempfile

    if not values:
        return
    try:
        current = path.read_text(encoding="utf-8") if path.exists() else ""
    except OSError as exc:
        raise StoreError("env_file_unreadable", "Environment file could not be read.", path=str(path)) from exc
    if current and not current.endswith("\n"):
        current += "\n"
    block = "\n# Migrated by pt-agent; values are referenced from store.json.\n"
    block += "".join(f"{name}={dotenv_quote(value)}\n" for name, value in values.items())
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        fd, tmp_name = tempfile.mkstemp(prefix=f".{path.name}.", dir=str(path.parent))
        with os.fdopen(fd, "w", encoding="utf-8") as fh:
            fh.write(current)
            fh.write(block)
        os.chmod(tmp_name, 0o600)
        os.replace(tmp_name, path)
    except OSError as exc:
        raise StoreError("env_file_write_failed", "Environment file could not be updated.", path=str(path)) from exc
    finally:
        if "tmp_name" in locals() and os.path.exists(tmp_name):
            os.unlink(tmp_name)


def migrate_inline_secrets(store: dict[str, Any], env_file: Path) -> dict[str, Any]:
    try:
        env_text = env_file.read_text(encoding="utf-8") if env_file.exists() else ""
    except OSError as exc:
        raise StoreError("env_file_unreadable", "Environment file could not be read.", path=str(env_file)) from exc
    existing = set(re.findall(r"(?m)^\s*(?:export\s+)?([A-Za-z_][A-Za-z0-9_]*)\s*=", env_text))
    values: dict[str, str] = {}
    migrated: list[dict[str, str]] = []

    for tracker_id, tracker in store.get("trackers", {}).items():
        if not isinstance(tracker, dict):
            continue
        raw_cookie = tracker.get("cookie")
        if isinstance(raw_cookie, str) and raw_cookie and not safe_reference(raw_cookie):
            name = env_name(str(tracker_id), "COOKIE", existing)
            values[name] = raw_cookie
            secret_refs = tracker.get("secretRefs") if isinstance(tracker.get("secretRefs"), dict) else {}
            tracker["secretRefs"] = {**secret_refs, "cookie": f"env://{name}"}
            tracker.pop("cookie", None)
            migrated.append({"fieldPath": f"trackers.{tracker_id}.cookie", "ref": f"env://{name}"})

    for downloader_id, downloader in store.get("downloaders", {}).items():
        if not isinstance(downloader, dict):
            continue
        raw_credential = downloader.get("credentialRef")
        username = downloader.get("username")
        password = downloader.get("password")
        if isinstance(raw_credential, str) and raw_credential and not safe_reference(raw_credential):
            credential = raw_credential
            source_path = f"downloaders.{downloader_id}.credentialRef"
        elif isinstance(password, str) and password:
            credential = json.dumps({"username": str(username or ""), "password": password}, ensure_ascii=False)
            source_path = f"downloaders.{downloader_id}.password"
        else:
            continue
        name = env_name(str(downloader_id), "CREDENTIALS", existing)
        values[name] = credential
        downloader["credentialRef"] = f"env://{name}"
        downloader.pop("password", None)
        migrated.append({"fieldPath": source_path, "ref": f"env://{name}"})

    append_env_values(env_file, values)
    return {"migrated": migrated, "environmentVariables": sorted(values)}


def main() -> int:
    parser = argparse.ArgumentParser(description="pt-agent persistent fallback store")
    parser.add_argument(
        "--store",
        help=(
            "store path; defaults to PT_AGENT_STORE, PT_AGENT_HOME/store.json, "
            "host home, installed skill home, or XDG state"
        ),
    )
    sub = parser.add_subparsers(dest="cmd", required=True)

    sub.add_parser("init")
    sub.add_parser("location")
    sub.add_parser("summary")
    sub.add_parser("doctor")
    sub.add_parser("audit-secrets")

    p_upsert_tracker = sub.add_parser("upsert-tracker")
    p_upsert_tracker.add_argument("--json", required=True)
    p_upsert_tracker.add_argument("--draft", action="store_true")

    p_upsert_downloader = sub.add_parser("upsert-downloader")
    p_upsert_downloader.add_argument("--json", required=True)

    p_find = sub.add_parser("find-tracker")
    p_find.add_argument("query")

    p_state = sub.add_parser("set-state")
    p_state.add_argument("--json", required=True)

    p_stats = sub.add_parser("upsert-stats")
    p_stats.add_argument("--tracker", required=True)
    p_stats.add_argument("--json", required=True)

    p_migrate = sub.add_parser("migrate-legacy")
    p_migrate.add_argument("--legacy", default=str(Path.home() / ".hermes" / "pt-sites.json"))

    p_migrate_secrets = sub.add_parser("migrate-inline-secrets")
    p_migrate_secrets.add_argument("--env-file", required=True)

    args = parser.parse_args()
    path, path_source = resolve_store_path(args.store)
    try:
        if args.cmd == "location":
            print(json.dumps(store_location(path, path_source), ensure_ascii=False, indent=2))
            return 0
        store = load_store(path)
        if args.cmd == "init":
            atomic_write(path, store)
            print(json.dumps({"ok": True, "store": str(path), "storeSource": path_source}, ensure_ascii=False))
        elif args.cmd == "summary":
            print(json.dumps(redact_for_output({
                "store": str(path),
                "storeSource": path_source,
                "trackers": list(store.get("trackers", {}).values()),
                "trackerDrafts": list(store.get("trackerDrafts", {}).values()),
                "trackerStats": list(store.get("trackerStats", {}).values()),
                "downloaders": list(store.get("downloaders", {}).values()),
                "defaultSearchSolutionId": store.get("defaultSearchSolutionId"),
                "defaultDownloaderId": store.get("defaultDownloaderId"),
            }), ensure_ascii=False, indent=2))
        elif args.cmd == "doctor":
            print(json.dumps(redact_for_output(store_doctor(path, path_source, store)), ensure_ascii=False, indent=2))
        elif args.cmd == "audit-secrets":
            findings = sorted(set(collect_raw_secret_paths(store)))
            print(json.dumps({
                "ok": not findings,
                "store": str(path),
                "storeSource": path_source,
                "rawSecretLikePaths": findings,
            }, ensure_ascii=False, indent=2))
        elif args.cmd == "upsert-tracker":
            data = load_json_arg(args.json)
            bucket = "trackerDrafts" if args.draft or not tracker_is_enabled_config(data) else "trackers"
            record = upsert_record(store, bucket, data)
            atomic_write(path, store)
            print(json.dumps(redact_for_output({"ok": True, "bucket": bucket, "record": record}), ensure_ascii=False, indent=2))
        elif args.cmd == "upsert-downloader":
            data = load_json_arg(args.json)
            record = upsert_record(store, "downloaders", data)
            atomic_write(path, store)
            print(json.dumps(redact_for_output({"ok": True, "record": record}), ensure_ascii=False, indent=2))
        elif args.cmd == "find-tracker":
            record = find_tracker(store, args.query)
            print(json.dumps(redact_for_output({"found": record is not None, "record": record}), ensure_ascii=False, indent=2))
        elif args.cmd == "set-state":
            data = load_json_arg(args.json)
            store["interactionState"] = {**store.get("interactionState", {}), **data, "updatedAt": now_iso()}
            atomic_write(path, store)
            print(json.dumps(redact_for_output({"ok": True, "interactionState": store["interactionState"]}), ensure_ascii=False, indent=2))
        elif args.cmd == "upsert-stats":
            data = load_json_arg(args.json)
            record = upsert_tracker_stats(store, args.tracker, data)
            atomic_write(path, store)
            print(json.dumps(redact_for_output({"ok": True, "record": record}), ensure_ascii=False, indent=2))
        elif args.cmd == "migrate-legacy":
            migrated = migrate_legacy(path, Path(args.legacy).expanduser())
            print(json.dumps(redact_for_output({
                "ok": True,
                "store": str(path),
                "storeSource": path_source,
                "trackerDrafts": list(migrated.get("trackerDrafts", {}).values()),
                "downloaders": list(migrated.get("downloaders", {}).values()),
            }), ensure_ascii=False, indent=2))
        elif args.cmd == "migrate-inline-secrets":
            result = migrate_inline_secrets(store, Path(args.env_file).expanduser())
            reject_raw_secrets(store)
            atomic_write(path, store)
            print(json.dumps({
                "ok": True,
                "store": str(path),
                "storeSource": path_source,
                "envFile": str(Path(args.env_file).expanduser()),
                **result,
            }, ensure_ascii=False, indent=2))
    except StoreError as exc:
        print(json.dumps(redact_for_output({
            "ok": False,
            "store": str(path),
            "storeSource": path_source,
            "error": exc.payload,
        }), ensure_ascii=False, indent=2))
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
