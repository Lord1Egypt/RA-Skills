#!/usr/bin/env python3
"""
Validate rolecard YAML files used by say-hi-to-me skill.
"""

from __future__ import annotations

import argparse
import re
from pathlib import Path
from typing import Dict, List

import yaml


REQUIRED_TOP_LEVEL = [
    "schema_version",
    "meta",
    "core_setting",
    "persona_background",
    "interests",
    "speech_style",
    "daily_routine",
    "emotion_expression",
    "behavior_rules",
    "dialogue_examples",
    "notes",
    "safety",
]

ALLOWED_STYLES = {"anime", "realistic"}
ALLOWED_GENDERS = {"female", "male", "nonbinary", "unspecified"}
ROMANTIC_LABELS = {"girlfriend", "boyfriend", "partner", "spouse"}


def read_yaml(path: Path) -> Dict:
    with path.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def validate_file(path: Path) -> List[str]:
    errors: List[str] = []
    data = read_yaml(path)

    if not isinstance(data, dict):
        return ["Top-level data must be a mapping/object."]

    for key in REQUIRED_TOP_LEVEL:
        if key not in data:
            errors.append(f"Missing top-level key: {key}")

    meta = data.get("meta", {})
    if not isinstance(meta, dict):
        errors.append("meta must be an object.")
    else:
        role_id = meta.get("id")
        if not role_id or not isinstance(role_id, str):
            errors.append("meta.id must be a non-empty string.")
        elif not re.match(r"^[a-z0-9-]+$", role_id):
            errors.append("meta.id must match ^[a-z0-9-]+$.")

    core = data.get("core_setting", {})
    if not isinstance(core, dict):
        errors.append("core_setting must be an object.")
    else:
        style = core.get("visual_style")
        if style not in ALLOWED_STYLES:
            errors.append(f"core_setting.visual_style must be one of {sorted(ALLOWED_STYLES)}.")

        gender = core.get("gender")
        if gender not in ALLOWED_GENDERS:
            errors.append(f"core_setting.gender must be one of {sorted(ALLOWED_GENDERS)}.")

        identity = core.get("identity", {})
        if not isinstance(identity, dict):
            errors.append("core_setting.identity must be an object.")
        else:
            label = identity.get("relationship_label")
            safety = data.get("safety", {})
            if label in ROMANTIC_LABELS:
                if not isinstance(safety, dict) or safety.get("requires_explicit_user_opt_in") is not True:
                    errors.append("Romantic relationship_label requires safety.requires_explicit_user_opt_in=true.")

    behavior = data.get("behavior_rules", {})
    if not isinstance(behavior, dict):
        errors.append("behavior_rules must be an object.")
    else:
        for section in ("companion", "technical_partner", "lifestyle_partner"):
            if section not in behavior:
                errors.append(f"behavior_rules.{section} is required.")
            elif not isinstance(behavior[section], list) or not behavior[section]:
                errors.append(f"behavior_rules.{section} must be a non-empty list.")

    return errors


def collect_files(path: Path) -> List[Path]:
    if path.is_file():
        return [path]
    return sorted(path.glob("*.yaml"))


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate rolecard YAML files")
    parser.add_argument("path", help="Rolecard YAML file or directory")
    args = parser.parse_args()

    path = Path(args.path).resolve()
    if not path.exists():
        print(f"[ERROR] Path does not exist: {path}")
        return 1

    files = collect_files(path)
    if not files:
        print(f"[ERROR] No YAML files found under: {path}")
        return 1

    total_errors = 0
    for file_path in files:
        errs = validate_file(file_path)
        if errs:
            total_errors += len(errs)
            print(f"[FAIL] {file_path}")
            for e in errs:
                print(f"  - {e}")
        else:
            print(f"[OK] {file_path}")

    return 1 if total_errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
