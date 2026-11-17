#!/usr/bin/env python3
"""Initialize a local Travel Buddy workspace and create consented profile shells.

Usage:
  python travel_workspace.py init [--workspace PATH]
  python travel_workspace.py create-profile PROFILE_ID --consent [--workspace PATH]
  python travel_workspace.py validate-profile PROFILE_JSON
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import unicodedata
from datetime import date
from pathlib import Path


DEFAULT_WORKSPACE = Path.home() / "Travel Buddy"
TEMPLATE = Path(__file__).resolve().parents[1] / "templates" / "personal-travel-profile.json"
SENSITIVE_KEYS = {
    "passport_number",
    "passportnumber",
    "passport_no",
    "passport_num",
    "passport_id",
    "passport_image",
    "document_number",
    "visa_image",
    "visa_number",
    "document_image",
    "payment_card",
    "card_number",
    "card_no",
    "credit_card",
    "payment_details",
    "cvv",
    "cvc",
    "security_code",
    "bank_account",
    "account_password",
    "password",
    "national_id",
    "id_number",
    "exact_home_address",
}
SENSITIVE_NON_ENGLISH_KEYS = {
    "护照号",
    "护照号码",
    "护照信息",
    "证件号",
    "证件号码",
    "证件照片",
    "护照照片",
    "签证号码",
    "银行卡",
    "银行卡号",
    "支付信息",
    "密码",
    "安全码",
    "详细地址",
    "精确住址",
    "家庭住址",
}
SENSITIVE_VALUE_PATTERNS = (
    re.compile(r"(?<!\d)(?:\d[ -]?){12,18}\d(?!\d)"),
    re.compile(r"(?:password|passwd|密码)\s*(?:[:：=]|为)\s*\S+", re.IGNORECASE),
    re.compile(r"(?:cvv|cvc|安全码)\s*(?:[:：=]|为)\s*\d{3,4}", re.IGNORECASE),
    re.compile(r"(?:passport|护照)\s*(?:number|no\.?|#|号(?:码)?)?\s*(?:[:：#=]|为)\s*[A-Za-z0-9-]{4,}", re.IGNORECASE),
)


def workspace_path(value: str | None) -> Path:
    return Path(value).expanduser() if value else DEFAULT_WORKSPACE


def profile_filename(profile_id: str) -> str:
    normalized = unicodedata.normalize("NFKC", profile_id)
    normalized = re.sub(r"[^\w-]+", "-", normalized, flags=re.UNICODE).strip("-_")
    if not normalized:
        raise ValueError("PROFILE_ID must contain at least one letter or number.")
    return normalized + ".json"


def find_sensitive_keys(value: object, path: str = "") -> list[str]:
    findings: list[str] = []
    if isinstance(value, dict):
        for key, child in value.items():
            key_path = f"{path}.{key}" if path else key
            normalized = re.sub(r"[^a-z0-9]+", "_", key.lower()).strip("_")
            if normalized in SENSITIVE_KEYS or str(key).strip().casefold() in SENSITIVE_NON_ENGLISH_KEYS:
                findings.append(key_path)
            findings.extend(find_sensitive_keys(child, key_path))
    elif isinstance(value, list):
        for index, child in enumerate(value):
            findings.extend(find_sensitive_keys(child, f"{path}[{index}]"))
    return findings


def find_sensitive_values(value: object, path: str = "") -> list[str]:
    """Flag likely credentials/document/payment values without retaining their content in an error."""
    findings: list[str] = []
    if isinstance(value, dict):
        for key, child in value.items():
            key_path = f"{path}.{key}" if path else str(key)
            findings.extend(find_sensitive_values(child, key_path))
    elif isinstance(value, list):
        for index, child in enumerate(value):
            findings.extend(find_sensitive_values(child, f"{path}[{index}]"))
    elif isinstance(value, str) and any(pattern.search(value) for pattern in SENSITIVE_VALUE_PATTERNS):
        findings.append(path or "value")
    return findings


def validate_profile(profile: object, lang: str = "en") -> list[str]:
    if not isinstance(profile, dict):
        return ["Profile must be a JSON object."]
    errors: list[str] = []
    if profile.get("profile_version") != "1.0":
        errors.append("profile_version must be 1.0.")
    if not profile.get("profile_id"):
        errors.append("profile_id is required.")
    consent = profile.get("storage_consent")
    if not isinstance(consent, dict) or consent.get("personal_profile") is not True or not consent.get("confirmed_at"):
        errors.append("storage_consent.personal_profile=true and confirmed_at are required before reuse.")
    for path in ("identity_and_language", "home_and_logistics", "travel_history", "recurring_preferences", "data_controls"):
        if not isinstance(profile.get(path), dict):
            errors.append(f"{path} must be an object.")
    digital_access = profile.get("digital_travel_access")
    if digital_access is not None:
        if not isinstance(digital_access, dict):
            errors.append("digital_travel_access must be an object when present.")
        else:
            for field in ("preferred_map_apps", "preferred_booking_platforms", "services_to_avoid"):
                if not isinstance(digital_access.get(field, []), list):
                    errors.append(f"digital_travel_access.{field} must be a list.")
            if digital_access.get("google_services_access", "unknown") not in {"available", "unavailable", "unknown"}:
                errors.append("digital_travel_access.google_services_access is invalid.")
            for field in ("booking_access_notes", "notes"):
                if digital_access.get(field) is not None and not isinstance(digital_access.get(field), str):
                    errors.append(f"digital_travel_access.{field} must be a string or null.")
    identity = profile.get("identity_and_language")
    if isinstance(identity, dict) and identity.get("residence_status") not in (
        None, "", "eu_eea_ch_citizen", "member_state_residence_permit",
        "eu_long_term_resident", "short_stay_visa_or_visa_free", "other_or_unspecified",
    ):
        errors.append("identity_and_language.residence_status is invalid.")
    history = profile.get("travel_history", {})
    if isinstance(history, dict):
        for key in ("visited_places", "wish_list", "excluded_places"):
            if not isinstance(history.get(key), list):
                errors.append(f"travel_history.{key} must be a list.")
    # The two refusals a traveller can cause from the form -- a passport number or a password typed
    # into a note -- are answered in the page's language; the rest name JSON paths the form cannot
    # produce, and stay in English for whoever is debugging the file.
    sensitive = find_sensitive_keys(profile)
    if sensitive:
        errors.append("档案包含不应保存的敏感字段：" + "、".join(sensitive) + "。" if lang == "zh"
                      else "Profile contains prohibited sensitive fields: " + ", ".join(sensitive) + ".")
    sensitive_values = find_sensitive_values(profile)
    if sensitive_values:
        errors.append("档案内容疑似包含证件/支付/密码等敏感值，位置：" + "、".join(sensitive_values) + "。" if lang == "zh"
                      else "Profile appears to contain prohibited sensitive values at: " + ", ".join(sensitive_values) + ".")
    return errors


def initialize(workspace: Path) -> None:
    for child in (workspace / "html", workspace / "plans", workspace / "profiles"):
        child.mkdir(parents=True, exist_ok=True)
    print(f"Workspace ready: {workspace}")


def create_profile(workspace: Path, profile_id: str, consent: bool) -> None:
    if not consent:
        raise ValueError("Refusing to create a reusable personal profile without --consent.")
    initialize(workspace)
    destination = workspace / "profiles" / profile_filename(profile_id)
    if destination.exists():
        raise FileExistsError(f"Profile already exists: {destination}")
    profile = json.loads(TEMPLATE.read_text(encoding="utf-8"))
    profile["profile_id"] = profile_id
    profile["storage_consent"] = {
        "personal_profile": True,
        "confirmed_at": date.today().isoformat(),
        "purpose": "Reuse travel preferences and constraints across future planning requests.",
    }
    destination.write_text(json.dumps(profile, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Created consented profile shell: {destination}")


def main() -> int:
    parser = argparse.ArgumentParser(description="Manage a local Travel Buddy workspace.")
    subparsers = parser.add_subparsers(dest="command", required=True)
    init_parser = subparsers.add_parser("init", help="Create html, plans, and profiles directories")
    init_parser.add_argument("--workspace", default=None)
    create_parser = subparsers.add_parser("create-profile", help="Create an empty consented profile shell")
    create_parser.add_argument("profile_id")
    create_parser.add_argument("--consent", action="store_true", help="Confirm the user opted in to local profile storage")
    create_parser.add_argument("--workspace", default=None)
    validate_parser = subparsers.add_parser("validate-profile", help="Validate a saved profile before use")
    validate_parser.add_argument("profile_json")
    args = parser.parse_args()
    try:
        if args.command == "init":
            initialize(workspace_path(args.workspace))
        elif args.command == "create-profile":
            create_profile(workspace_path(args.workspace), args.profile_id, args.consent)
        else:
            profile = json.loads(Path(args.profile_json).read_text(encoding="utf-8"))
            errors = validate_profile(profile)
            if errors:
                print("INVALID PROFILE")
                for error in errors:
                    print(f"- {error}")
                return 1
            print("VALID PROFILE")
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
