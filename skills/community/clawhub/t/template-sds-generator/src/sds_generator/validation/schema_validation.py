from __future__ import annotations

import json
from functools import lru_cache
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator

from sds_generator.config_loader import CONFIG_ROOT
from sds_generator.models import FinalSDSDocument


@lru_cache(maxsize=1)
def load_structured_schema(schema_path: Path | None = None) -> dict[str, Any]:
    target = schema_path or (CONFIG_ROOT / "structured_data.schema.json")
    with target.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def _validate_payload(payload: dict[str, Any], schema_path: Path | None = None) -> None:
    schema = load_structured_schema(schema_path)
    validator = Draft202012Validator(schema)
    errors = sorted(validator.iter_errors(payload), key=lambda error: list(error.path))
    if errors:
        first = errors[0]
        location = ".".join(str(part) for part in first.absolute_path) or "<root>"
        raise ValueError(f"Structured data schema validation failed at {location}: {first.message}")
    _validate_structured_sections(payload)


def _expected_section_fields() -> dict[str, set[str]]:
    document = FinalSDSDocument()
    return {
        section_key: set(section_model.__class__.model_fields)
        for section_key, section_model in document.ordered_sections()
    }


def _validate_structured_sections(payload: dict[str, Any]) -> None:
    sections = payload.get("sections")
    if not isinstance(sections, dict):
        raise ValueError("Structured data payload is missing a valid sections object.")

    expected = _expected_section_fields()
    missing_sections = [section for section in expected if section not in sections]
    if missing_sections:
        raise ValueError(f"Structured data schema validation failed at sections: missing sections {', '.join(missing_sections)}")

    for section_key, expected_fields in expected.items():
        section_payload = sections.get(section_key)
        if not isinstance(section_payload, dict):
            raise ValueError(f"Structured data schema validation failed at sections.{section_key}: section must be an object")
        missing_fields = sorted(expected_fields - set(section_payload))
        if missing_fields:
            raise ValueError(
                f"Structured data schema validation failed at sections.{section_key}: missing fields {', '.join(missing_fields)}"
            )


def validate_structured_json_file(path: Path, schema_path: Path | None = None) -> None:
    with path.open("r", encoding="utf-8") as handle:
        payload = json.load(handle)
    _validate_payload(payload, schema_path=schema_path)


def validate_structured_data(payload_or_path: dict[str, Any] | str | Path, schema_path: Path | None = None) -> None:
    if isinstance(payload_or_path, dict):
        _validate_payload(payload_or_path, schema_path=schema_path)
        return
    validate_structured_json_file(Path(payload_or_path), schema_path=schema_path)
