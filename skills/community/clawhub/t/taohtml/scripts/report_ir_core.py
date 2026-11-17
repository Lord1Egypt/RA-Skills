#!/usr/bin/env python3
"""Strict, standard-library validation and normalization for TaoHtml Report IR v1."""

from __future__ import annotations

import copy
import hashlib
import json
import math
import re
from pathlib import Path, PurePosixPath
from typing import Any, Iterable
from urllib.parse import urlparse


SUPPORTED_REPORT_IR_VERSIONS = ("1.0", "1.1")
WORKFLOW_PROFILE_BINDING_CONTRACT_VERSION = "1.1"
WORKFLOW_PROFILE_DEFINITION_VERSION = "2.0"
WORKFLOW_PROFILE_IDS = {
    "formal-submission-writing",
    "research-analysis-argumentation",
    "periodic-operations-reporting",
    "proposal-planning-decision",
    "live-presentation-persuasion",
    "teaching-training-knowledge-transfer",
    "project-lifecycle-reporting",
    "brand-communication-editorial-publishing",
    "rule-response-application-defense",
}
SCRIPT_DIR = Path(__file__).resolve().parent
SKILL_DIR = SCRIPT_DIR.parent
SCHEMA_PATH = SKILL_DIR / "references" / "report-ir-v1.schema.json"
SHA256 = re.compile(r"^[0-9a-f]{64}$")
WINDOWS_ABSOLUTE = re.compile(r"^[A-Za-z]:[\\/]")
DANGEROUS_CONTENT = re.compile(
    r"<\s*(?:script|style|iframe|object|embed|link|meta)\b"
    r"|javascript\s*:|@import\b|\bon[a-z]+\s*=",
    re.IGNORECASE,
)
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
STANDARD_PAGE_ROLES = {
    "orient",
    "assert",
    "prove",
    "explain",
    "compare",
    "synthesize",
    "decide",
    "act",
}
STANDARD_PAGE_FORMS = {
    "poster",
    "evidence",
    "data",
    "process",
    "framework",
    "comparison",
    "case",
    "matrix",
    "source",
    "closing",
    "content",
    "section",
    "toc",
}
TEXT_BLOCK_KINDS = {
    "headline",
    "body_text",
    "quote",
    "methodology",
    "caveat",
    "call_to_action",
}
ITEM_BLOCK_KINDS = {"list", "process", "comparison", "timeline"}
REGISTRY_KEYS = (
    "claims",
    "evidence",
    "evidence_links",
    "sources",
    "datasets",
    "assets",
    "speaker_notes",
    "appendices",
    "extensions",
)


def _reject_duplicate_object_keys(
    pairs: list[tuple[str, object]],
) -> dict[str, object]:
    result: dict[str, object] = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"duplicate object key: {key}")
        result[key] = value
    return result


def _reject_non_finite_constant(value: str) -> object:
    raise ValueError(f"non-finite JSON number is not allowed: {value}")


def strict_json_loads(value: str) -> object:
    return json.loads(
        value,
        object_pairs_hook=_reject_duplicate_object_keys,
        parse_constant=_reject_non_finite_constant,
    )


def load_json(path: Path) -> dict[str, Any]:
    raw = strict_json_loads(path.read_text(encoding="utf-8"))
    if not isinstance(raw, dict):
        raise ValueError("Report IR root must be a JSON object")
    return raw


def canonical_bytes(value: object) -> bytes:
    return (
        json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
        .encode("utf-8")
    )


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def write_json(path: Path, value: object) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = json.dumps(value, ensure_ascii=False, indent=2) + "\n"
    path.write_bytes(payload.encode("utf-8"))
    return path


def normalize_ir(raw: dict[str, Any]) -> dict[str, Any]:
    """Add only neutral defaults; never create claims, evidence, pages, or content."""
    ir = copy.deepcopy(raw)
    for key in REGISTRY_KEYS:
        ir.setdefault(key, [])

    report = ir.get("report")
    if isinstance(report, dict):
        report.setdefault("language", "zh-CN")

    projection = ir.get("projection")
    if isinstance(projection, dict):
        projection.setdefault("interaction_level", "none")
        has_states = any(
            isinstance(page, dict) and bool(page.get("state_sequence"))
            for page in ir.get("pages", [])
        )
        projection.setdefault("state_complexity", "staged" if has_states else "static")

    for chapter in ir.get("chapters", []):
        if isinstance(chapter, dict):
            chapter.setdefault("evidence_rigor", ir.get("report", {}).get("evidence_rigor"))

    for unit in ir.get("narrative_units", []):
        if isinstance(unit, dict):
            unit.setdefault("prerequisite_unit_refs", [])

    for block in ir.get("blocks", []):
        if not isinstance(block, dict):
            continue
        block.setdefault("claim_refs", [])
        block.setdefault("evidence_refs", [])
        for item in block.get("items", []):
            if isinstance(item, dict):
                item.setdefault("claim_refs", [])
                item.setdefault("evidence_refs", [])

    for page in ir.get("pages", []):
        if isinstance(page, dict):
            page.setdefault("source_display", "hidden_manifest")

    runtime = ir.get("build_binding", {}).get("runtime")
    if isinstance(runtime, dict):
        runtime.setdefault("editor_enabled", True)

    return ir


def _json_type_matches(value: object, expected: str) -> bool:
    if expected == "object":
        return isinstance(value, dict)
    if expected == "array":
        return isinstance(value, list)
    if expected == "string":
        return isinstance(value, str)
    if expected == "null":
        return value is None
    if expected == "boolean":
        return isinstance(value, bool)
    if expected == "integer":
        return isinstance(value, int) and not isinstance(value, bool)
    if expected == "number":
        return (
            isinstance(value, (int, float))
            and not isinstance(value, bool)
            and math.isfinite(value)
        )
    raise RuntimeError(f"unsupported schema type: {expected}")


def _resolve_ref(schema_root: dict[str, Any], ref: str) -> dict[str, Any]:
    if not ref.startswith("#/"):
        raise RuntimeError(f"unsupported external schema reference: {ref}")
    current: object = schema_root
    for token in ref[2:].split("/"):
        token = token.replace("~1", "/").replace("~0", "~")
        if not isinstance(current, dict) or token not in current:
            raise RuntimeError(f"unresolved schema reference: {ref}")
        current = current[token]
    if not isinstance(current, dict):
        raise RuntimeError(f"schema reference is not an object: {ref}")
    return current


def schema_errors(
    value: object,
    schema: dict[str, Any],
    schema_root: dict[str, Any],
    path: str = "$",
) -> list[str]:
    if "$ref" in schema:
        return schema_errors(value, _resolve_ref(schema_root, schema["$ref"]), schema_root, path)

    errors: list[str] = []
    for branch in schema.get("allOf", []):
        errors.extend(schema_errors(value, branch, schema_root, path))
    if "not" in schema and not schema_errors(value, schema["not"], schema_root, path):
        errors.append(f"{path} matches a forbidden schema branch")
    if "anyOf" in schema:
        branches = [schema_errors(value, item, schema_root, path) for item in schema["anyOf"]]
        if not any(not item for item in branches):
            errors.append(f"{path} does not match any allowed schema branch")
        return errors
    if "oneOf" in schema:
        branches = [schema_errors(value, item, schema_root, path) for item in schema["oneOf"]]
        matches = sum(not item for item in branches)
        if matches != 1:
            errors.append(f"{path} must match exactly one schema branch; matched={matches}")
        return errors

    if "const" in schema and value != schema["const"]:
        errors.append(f"{path} must equal {schema['const']!r}")
    if "enum" in schema and value not in schema["enum"]:
        errors.append(f"{path} must be one of {schema['enum']!r}")

    expected_type = schema.get("type")
    if expected_type is not None:
        expected = expected_type if isinstance(expected_type, list) else [expected_type]
        if not any(_json_type_matches(value, item) for item in expected):
            errors.append(f"{path} must have type {expected!r}")
            return errors

    if isinstance(value, dict):
        required = set(schema.get("required", []))
        missing = required - set(value)
        if missing:
            errors.append(f"{path} missing required fields: {', '.join(sorted(missing))}")
        properties = schema.get("properties", {})
        if schema.get("additionalProperties") is False:
            extra = set(value) - set(properties)
            if extra:
                errors.append(f"{path} has unknown fields: {', '.join(sorted(extra))}")
        for key, child in value.items():
            if key in properties:
                errors.extend(schema_errors(child, properties[key], schema_root, f"{path}.{key}"))
    elif isinstance(value, list):
        if len(value) < schema.get("minItems", 0):
            errors.append(f"{path} must contain at least {schema['minItems']} items")
        if "maxItems" in schema and len(value) > schema["maxItems"]:
            errors.append(f"{path} must contain at most {schema['maxItems']} items")
        if schema.get("uniqueItems"):
            normalized = [json.dumps(item, ensure_ascii=False, sort_keys=True) for item in value]
            if len(normalized) != len(set(normalized)):
                errors.append(f"{path} must contain unique items")
        if "items" in schema:
            for index, child in enumerate(value):
                errors.extend(schema_errors(child, schema["items"], schema_root, f"{path}[{index}]"))
    elif isinstance(value, str):
        if len(value) < schema.get("minLength", 0):
            errors.append(f"{path} is shorter than {schema['minLength']} characters")
        if "maxLength" in schema and len(value) > schema["maxLength"]:
            errors.append(f"{path} is longer than {schema['maxLength']} characters")
        if "pattern" in schema and re.search(schema["pattern"], value) is None:
            errors.append(f"{path} does not match the required pattern")
    elif isinstance(value, (int, float)) and not isinstance(value, bool):
        if not math.isfinite(value):
            errors.append(f"{path} must be a finite JSON number")
        elif "minimum" in schema and value < schema["minimum"]:
            errors.append(f"{path} must be at least {schema['minimum']}")
    return errors


def _index(
    records: Iterable[dict[str, Any]],
    label: str,
    issues: list[str],
) -> dict[str, dict[str, Any]]:
    result: dict[str, dict[str, Any]] = {}
    for record in records:
        identity = record["id"]
        if identity in result:
            issues.append(f"duplicate {label} id: {identity}")
        result[identity] = record
    return result


def _check_refs(
    refs: Iterable[str],
    target: dict[str, Any],
    label: str,
    issues: list[str],
) -> None:
    for ref in refs:
        if ref not in target:
            issues.append(f"{label} references unknown id: {ref}")


def _looks_absolute(value: str) -> bool:
    return value.startswith("/") or value.startswith("file://") or bool(WINDOWS_ABSOLUTE.match(value))


def _safe_relative(value: str) -> bool:
    if _looks_absolute(value) or "\\" in value or "//" in value:
        return False
    parts = value.split("/")
    if any(part in {"", ".", ".."} for part in parts):
        return False
    pure = PurePosixPath(value)
    return not pure.is_absolute() and pure.as_posix() == value


def _validate_locator(locator: dict[str, Any], label: str, issues: list[str]) -> None:
    kind = locator["kind"]
    value = locator["value"]
    if kind == "project_relative" and not _safe_relative(value):
        issues.append(f"{label} must use a normalized project-relative path")
    elif kind == "url":
        parsed = urlparse(value)
        if parsed.scheme not in {"http", "https"} or not parsed.netloc:
            issues.append(f"{label} must use an http or https URL")
    elif kind == "stable_locator" and _looks_absolute(value):
        issues.append(f"{label} stable locator cannot be a local absolute path")


def _verify_bound_file(
    record: dict[str, Any],
    artifact_root: Path | None,
    label: str,
    issues: list[str],
    verified_files: list[str],
) -> None:
    locator = record["locator"]
    if locator["kind"] != "project_relative" or artifact_root is None:
        return
    expected = record.get("sha256")
    if record.get("integrity_status") == "verified" and expected is None:
        issues.append(f"{label} integrity_status=verified requires sha256")
        return
    if expected is None:
        return
    path = artifact_root.joinpath(*locator["value"].split("/"))
    try:
        resolved = path.resolve(strict=True)
        resolved.relative_to(artifact_root)
    except (OSError, ValueError):
        issues.append(f"{label} project-relative file is unavailable or escapes artifact root")
        return
    if not resolved.is_file() or resolved.is_symlink():
        issues.append(f"{label} must resolve to a regular non-symlink file")
        return
    actual = sha256_file(resolved)
    if actual != expected:
        issues.append(f"{label} hash drift: expected {expected}, observed {actual}")
        return
    verified_files.append(locator["value"])


def _reject_executable(value: object, path: str, issues: list[str]) -> None:
    if isinstance(value, dict):
        for key, child in value.items():
            if key.lower() in {"html", "css", "javascript", "script", "style"}:
                issues.append(f"{path}.{key} is an executable-content field")
            _reject_executable(child, f"{path}.{key}", issues)
    elif isinstance(value, list):
        for index, child in enumerate(value):
            _reject_executable(child, f"{path}[{index}]", issues)
    elif isinstance(value, str) and DANGEROUS_CONTENT.search(value):
        issues.append(f"{path} contains executable markup or a script-capable URL")


def _collect_stable_ids(
    value: object,
    path: str,
    seen: dict[str, str],
    issues: list[str],
) -> None:
    if isinstance(value, dict):
        identity = value.get("id")
        if isinstance(identity, str):
            if identity in seen:
                issues.append(
                    f"global stable id {identity!r} is reused at {seen[identity]} and {path}.id"
                )
            else:
                seen[identity] = f"{path}.id"
        for key, child in value.items():
            _collect_stable_ids(child, f"{path}.{key}", seen, issues)
    elif isinstance(value, list):
        for index, child in enumerate(value):
            _collect_stable_ids(child, f"{path}[{index}]", seen, issues)


def _detect_unit_cycles(
    units: dict[str, dict[str, Any]],
    issues: list[str],
) -> None:
    visiting: set[str] = set()
    visited: set[str] = set()

    def visit(identity: str, trail: list[str]) -> None:
        if identity in visiting:
            start = trail.index(identity) if identity in trail else 0
            issues.append(
                "narrative unit prerequisite cycle: "
                + " -> ".join(trail[start:] + [identity])
            )
            return
        if identity in visited or identity not in units:
            return
        visiting.add(identity)
        for dependency in units[identity]["prerequisite_unit_refs"]:
            visit(dependency, trail + [identity])
        visiting.remove(identity)
        visited.add(identity)

    for identity in units:
        visit(identity, [])


def _semantic_validation(
    ir: dict[str, Any],
    artifact_root: Path | None,
) -> tuple[list[str], list[str], list[str], list[str]]:
    reference_issues: list[str] = []
    semantic_issues: list[str] = []
    compiler_issues: list[str] = []
    verified_files: list[str] = []

    if ir["report_ir_version"] == "1.1":
        workflow_profile = ir["workflow_profile"]
        if not workflow_profile["selection_basis"].strip():
            semantic_issues.append(
                "workflow_profile.selection_basis must contain non-whitespace semantic evidence"
            )
        overlay_keys: set[tuple[str, str, str]] = set()
        for index, overlay in enumerate(workflow_profile["capability_overlays"]):
            label = f"workflow_profile.capability_overlays[{index}]"
            for field in ("bounded_capability", "reason", "affected_scope"):
                if not overlay[field].strip():
                    semantic_issues.append(
                        f"{label}.{field} must contain non-whitespace text"
                    )
            if overlay["source_profile_id"] == workflow_profile["primary_profile_id"]:
                semantic_issues.append(
                    f"{label}.source_profile_id cannot reference the primary Profile"
                )
            duplicate_key = (
                overlay["source_profile_id"],
                overlay["bounded_capability"].strip(),
                overlay["affected_scope"].strip(),
            )
            if duplicate_key in overlay_keys:
                semantic_issues.append(
                    f"{label} duplicates a source Profile, bounded capability, and affected scope"
                )
            overlay_keys.add(duplicate_key)

    chapters = _index(ir["chapters"], "chapter", reference_issues)
    units = _index(ir["narrative_units"], "narrative unit", reference_issues)
    blocks = _index(ir["blocks"], "block", reference_issues)
    claims = _index(ir["claims"], "claim", reference_issues)
    evidence = _index(ir["evidence"], "evidence", reference_issues)
    links = _index(ir["evidence_links"], "evidence link", reference_issues)
    sources = _index(ir["sources"], "source", reference_issues)
    datasets = _index(ir["datasets"], "dataset", reference_issues)
    assets = _index(ir["assets"], "asset", reference_issues)
    pages = _index(ir["pages"], "page", reference_issues)
    notes = _index(ir["speaker_notes"], "speaker note", reference_issues)
    appendices = _index(ir["appendices"], "appendix", reference_issues)

    stable_ids: dict[str, str] = {}
    _collect_stable_ids(ir, "$", stable_ids, reference_issues)

    page_order = ir["projection"]["page_order"]
    _check_refs(page_order, pages, "projection.page_order", reference_issues)
    if set(page_order) != set(pages):
        reference_issues.append("projection.page_order must reference every page exactly once")

    unit_membership: dict[str, int] = {identity: 0 for identity in units}
    for chapter in ir["chapters"]:
        _check_refs(chapter["narrative_unit_refs"], units, f"chapter.{chapter['id']}", reference_issues)
        for ref in chapter["narrative_unit_refs"]:
            if ref in unit_membership:
                unit_membership[ref] += 1
    for identity, count in unit_membership.items():
        if count == 0:
            reference_issues.append(f"narrative unit {identity} is not assigned to any chapter")
        elif count > 1:
            reference_issues.append(f"narrative unit {identity} is assigned to multiple chapters")

    for unit in ir["narrative_units"]:
        label = f"narrative_unit.{unit['id']}"
        _check_refs(unit["claim_refs"], claims, label, reference_issues)
        _check_refs(unit["block_refs"], blocks, label, reference_issues)
        _check_refs(unit["prerequisite_unit_refs"], units, label, reference_issues)
        if unit["id"] in unit["prerequisite_unit_refs"]:
            semantic_issues.append(f"{label} cannot depend on itself")
    _detect_unit_cycles(units, semantic_issues)

    for block in ir["blocks"]:
        label = f"block.{block['id']}"
        _check_refs(block["claim_refs"], claims, label, reference_issues)
        _check_refs(block["evidence_refs"], evidence, label, reference_issues)
        if "dataset_ref" in block and block["dataset_ref"] not in datasets:
            reference_issues.append(f"{label} references unknown dataset: {block['dataset_ref']}")
        if "asset_ref" in block and block["asset_ref"] not in assets:
            reference_issues.append(f"{label} references unknown asset: {block['asset_ref']}")
        for item in block.get("items", []):
            _check_refs(item["claim_refs"], claims, f"{label}.item.{item['id']}", reference_issues)
            _check_refs(item["evidence_refs"], evidence, f"{label}.item.{item['id']}", reference_issues)

        kind = block["kind"]
        if kind in TEXT_BLOCK_KINDS and "text" not in block:
            semantic_issues.append(f"{label} kind={kind} requires text")
        if kind in ITEM_BLOCK_KINDS and "items" not in block:
            semantic_issues.append(f"{label} kind={kind} requires items")
        if kind == "claim" and not block["claim_refs"]:
            semantic_issues.append(f"{label} kind=claim requires claim_refs")
        if kind == "metric" and "text" not in block and "items" not in block:
            semantic_issues.append(f"{label} kind=metric requires text or items")
        if kind == "data_visualization" and "dataset_ref" not in block:
            semantic_issues.append(f"{label} kind=data_visualization requires dataset_ref")
        if (
            kind == "data_visualization"
            and block.get("dataset_ref") in datasets
            and not datasets[block["dataset_ref"]].get("records")
        ):
            semantic_issues.append(f"{label} data visualization dataset requires records")
        if kind == "table" and "dataset_ref" not in block and "items" not in block:
            semantic_issues.append(f"{label} kind=table requires dataset_ref or items")
        if (
            kind == "table"
            and block.get("dataset_ref") in datasets
            and not datasets[block["dataset_ref"]].get("records")
        ):
            semantic_issues.append(f"{label} table dataset requires records")
        if kind == "image" and ("asset_ref" not in block or "alt" not in block):
            semantic_issues.append(f"{label} kind=image requires asset_ref and alt")
        if kind == "evidence_excerpt" and not block["evidence_refs"]:
            semantic_issues.append(f"{label} kind=evidence_excerpt requires evidence_refs")

    for item in ir["evidence_links"]:
        if item["claim_ref"] not in claims:
            reference_issues.append(f"evidence_link.{item['id']} references unknown claim: {item['claim_ref']}")
        if item["evidence_ref"] not in evidence:
            reference_issues.append(f"evidence_link.{item['id']} references unknown evidence: {item['evidence_ref']}")

    for item in ir["evidence"]:
        label = f"evidence.{item['id']}"
        _check_refs(item["source_refs"], sources, label, reference_issues)
        _check_refs(item["dataset_refs"], datasets, label, reference_issues)
        if not item["source_refs"] and not item["dataset_refs"]:
            semantic_issues.append(f"{label} must reference at least one source or dataset")

    for item in ir["datasets"]:
        _check_refs(item["source_refs"], sources, f"dataset.{item['id']}", reference_issues)
        if not item["source_refs"]:
            semantic_issues.append(f"dataset.{item['id']} must reference at least one source")

    for item in ir["sources"]:
        label = f"source.{item['id']}"
        _validate_locator(item["locator"], f"{label}.locator", semantic_issues)
        _verify_bound_file(item, artifact_root, label, semantic_issues, verified_files)
        if item["content_verification"] == "not_applicable" and item["claim_fit"] == "verified":
            semantic_issues.append(f"{label} cannot verify claim fit without content verification")
        if item["source_role"] in {"synthetic_fixture", "agent_generated_material"}:
            if item["content_verification"] == "verified" or item["claim_fit"] == "verified":
                semantic_issues.append(f"{label} generated or synthetic content cannot be fact-verified")

    for item in ir["assets"]:
        label = f"asset.{item['id']}"
        _validate_locator(item["locator"], f"{label}.locator", semantic_issues)
        if "source_ref" in item and item["source_ref"] not in sources:
            reference_issues.append(f"{label} references unknown source: {item['source_ref']}")
        if item["content_status"] == "verified" and item["locator"]["kind"] == "project_relative" and "sha256" not in item:
            semantic_issues.append(f"{label} verified project-relative asset requires sha256")
        _verify_bound_file(item, artifact_root, label, semantic_issues, verified_files)

    state_by_page: dict[str, dict[str, dict[str, Any]]] = {}
    for page in ir["pages"]:
        label = f"page.{page['id']}"
        if page["chapter_ref"] not in chapters:
            reference_issues.append(f"{label} references unknown chapter: {page['chapter_ref']}")
        _check_refs(page["narrative_unit_refs"], units, label, reference_issues)
        _check_refs(page["block_refs"], blocks, label, reference_issues)
        subtitle_ref = page.get("subtitle_ref")
        if subtitle_ref is not None:
            if subtitle_ref not in page["block_refs"]:
                reference_issues.append(
                    f"{label}.subtitle_ref must reference a block on the same page"
                )
            elif subtitle_ref in blocks and blocks[subtitle_ref]["kind"] != "body_text":
                semantic_issues.append(
                    f"{label}.subtitle_ref must reference an explicit body_text surface block"
                )
        intent = page["visual_intent"]
        if intent["primary_focus_ref"] not in page["block_refs"]:
            reference_issues.append(f"{label}.visual_intent primary focus must be a page block")
        if intent["reading_order"] != page["block_refs"]:
            if set(intent["reading_order"]) != set(page["block_refs"]):
                semantic_issues.append(f"{label}.visual_intent.reading_order must include every page block exactly once")
        for relationship in intent["relationships"]:
            for side in ("from_ref", "to_ref"):
                if relationship[side] not in page["block_refs"]:
                    reference_issues.append(f"{label}.visual_intent relationship {side} must be a page block")
        if page["role"] not in STANDARD_PAGE_ROLES and "fallback_role" not in intent:
            compiler_issues.append(f"{label} custom role requires visual_intent.fallback_role")
        if page["form"] not in STANDARD_PAGE_FORMS and "fallback_form" not in intent:
            compiler_issues.append(f"{label} custom form requires visual_intent.fallback_form")

        states = page.get("state_sequence", [])
        state_index = _index(states, f"state in {page['id']}", reference_issues)
        state_by_page[page["id"]] = state_index
        for state in states:
            _check_refs(state["visible_refs"], blocks, f"{label}.state.{state['id']}", reference_issues)
            _check_refs(state["emphasized_refs"], blocks, f"{label}.state.{state['id']}", reference_issues)
            invalid_visible = set(state["visible_refs"]) - set(page["block_refs"])
            invalid_emphasis = set(state["emphasized_refs"]) - set(state["visible_refs"])
            if invalid_visible:
                semantic_issues.append(f"{label}.state.{state['id']} exposes blocks outside the page")
            if invalid_emphasis:
                semantic_issues.append(f"{label}.state.{state['id']} emphasizes blocks that are not visible")
            if "focus_ref" in state and state["focus_ref"] not in state["visible_refs"]:
                semantic_issues.append(f"{label}.state.{state['id']} focus must be visible")
        if states:
            final_ref = page.get("reading_final_state_ref")
            if final_ref not in state_index:
                reference_issues.append(f"{label} requires a valid reading_final_state_ref")
            elif set(state_index[final_ref]["visible_refs"]) != set(page["block_refs"]):
                semantic_issues.append(f"{label} reading final state must expose every page block")
        elif "reading_final_state_ref" in page:
            semantic_issues.append(f"{label} cannot declare reading_final_state_ref without states")

    for note in ir["speaker_notes"]:
        label = f"speaker_note.{note['id']}"
        if note["page_ref"] not in pages:
            reference_issues.append(f"{label} references unknown page: {note['page_ref']}")
        elif "state_ref" in note and note["state_ref"] not in state_by_page[note["page_ref"]]:
            reference_issues.append(f"{label} references unknown state on page {note['page_ref']}")

    for appendix in ir["appendices"]:
        label = f"appendix.{appendix['id']}"
        _check_refs(appendix["block_refs"], blocks, label, reference_issues)
        _check_refs(appendix.get("source_refs", []), sources, label, reference_issues)

    runtime_mode = ir["build_binding"]["runtime"]["target_mode"]
    delivery_mode = ir["projection"]["delivery_mode"]
    if delivery_mode != "hybrid" and runtime_mode != delivery_mode:
        semantic_issues.append("build_binding.runtime.target_mode must match projection.delivery_mode")
    if delivery_mode == "reading" and ir["projection"]["state_complexity"] != "static":
        semantic_issues.append("reading projection must use state_complexity=static")
    if ir["projection"]["state_complexity"] == "static" and any(
        page.get("state_sequence") for page in ir["pages"]
    ):
        semantic_issues.append("state_complexity=static cannot contain page state sequences")
    if delivery_mode == "presentation" and ir["projection"]["motion_density"] != "minimal":
        if not any(page.get("state_sequence") for page in ir["pages"]):
            semantic_issues.append("non-minimal presentation motion requires at least one page state sequence")

    theme = ir["build_binding"]["theme"]
    if theme["kind"] == "built_in" and theme["ref"] not in BUILT_IN_THEME_IDS:
        compiler_issues.append(f"unknown built-in theme: {theme['ref']}")
    if theme["kind"] == "built_in" and "enterprise" in ir["build_binding"]:
        compiler_issues.append("enterprise binding requires a project_theme binding")

    for extension in ir["extensions"]:
        if extension["required"]:
            compiler_issues.append(f"required extension is unsupported: {extension['namespace']}")

    links_by_claim: dict[str, list[dict[str, Any]]] = {identity: [] for identity in claims}
    for item in ir["evidence_links"]:
        if item["claim_ref"] in links_by_claim:
            links_by_claim[item["claim_ref"]].append(item)

    formal_claims: set[str] = set()
    standard_claims: set[str] = set()
    for chapter in ir["chapters"]:
        target = formal_claims if chapter["evidence_rigor"] == "formal" else standard_claims
        if chapter["evidence_rigor"] not in {"formal", "standard"}:
            continue
        for unit_ref in chapter["narrative_unit_refs"]:
            if unit_ref in units:
                target.update(units[unit_ref]["claim_refs"])

    source_verified: dict[str, bool] = {
        identity: item["integrity_status"] in {"verified", "not_applicable"}
        and item["content_verification"] == "verified"
        and item["claim_fit"] == "verified"
        for identity, item in sources.items()
    }
    dataset_verified: dict[str, bool] = {
        identity: item["content_status"] == "verified"
        and bool(item["source_refs"])
        and any(source_verified.get(ref, False) for ref in item["source_refs"])
        for identity, item in datasets.items()
    }
    evidence_verified: dict[str, bool] = {
        identity: item["content_status"] == "verified"
        and (
            any(source_verified.get(ref, False) for ref in item["source_refs"])
            or any(dataset_verified.get(ref, False) for ref in item["dataset_refs"])
        )
        for identity, item in evidence.items()
    }
    for identity, item in datasets.items():
        if item["content_status"] == "verified" and not dataset_verified[identity]:
            semantic_issues.append(f"dataset.{identity} is marked verified without a verified source")
    for identity, item in evidence.items():
        if item["content_status"] == "verified" and not evidence_verified[identity]:
            semantic_issues.append(f"evidence.{identity} is marked verified without verified support")

    for identity, claim in claims.items():
        if claim["kind"] not in {"fact", "inference"}:
            continue
        claim_links = links_by_claim.get(identity, [])
        if identity in formal_claims | standard_claims and not claim_links:
            semantic_issues.append(f"claim.{identity} requires an evidence link at its effective rigor")
        if identity in formal_claims and claim["status"] == "verified":
            supporting = [
                item for item in claim_links
                if item["relation"] in {"supports", "qualifies"}
                and evidence_verified.get(item["evidence_ref"], False)
            ]
            if not supporting:
                semantic_issues.append(f"formal verified claim.{identity} lacks verified supporting evidence")

    pending_ids = {
        identity for identity, item in claims.items() if item["status"] != "verified"
    }
    pending_ids.update(
        identity for identity, item in evidence.items() if item["content_status"] != "verified"
    )
    pending_ids.update(
        identity for identity, item in datasets.items() if item["content_status"] != "verified"
    )
    pending_ids.update(
        identity for identity, item in assets.items() if item["content_status"] != "verified"
    )
    unresolved_refs = {
        item["entity_ref"] for item in ir["traceability"]["unresolved_items"]
    }
    _check_refs(unresolved_refs, stable_ids, "traceability.unresolved_items", reference_issues)
    undisclosed = pending_ids - unresolved_refs
    if undisclosed:
        semantic_issues.append(
            "pending, disputed, unsupported, or illustrative entities must be listed in traceability.unresolved_items: "
            + ", ".join(sorted(undisclosed))
        )
    if pending_ids and not ir["traceability"]["pending_verification_required"]:
        semantic_issues.append("traceability.pending_verification_required must be true while unresolved content exists")

    design_brief_ref = ir["traceability"]["design_brief_ref"]
    if _looks_absolute(design_brief_ref) or "\\" in design_brief_ref:
        semantic_issues.append("traceability.design_brief_ref must be portable and cannot use a local absolute path")
    if ir["traceability"]["design_brief_confirmation"] != "confirmed":
        compiler_issues.append(
            "traceability.design_brief_confirmation must be confirmed before compilation"
        )

    _reject_executable(ir, "$", semantic_issues)
    return reference_issues, semantic_issues, compiler_issues, sorted(set(verified_files))


def workflow_profile_record(ir: dict[str, Any]) -> dict[str, Any]:
    """Return the deterministic build record without interpreting Profile semantics."""
    version = ir.get("report_ir_version")
    binding = ir.get("workflow_profile")
    if version == "1.0" and binding is None:
        return {
            "binding_contract_version": WORKFLOW_PROFILE_BINDING_CONTRACT_VERSION,
            "binding_state": "legacy_unbound",
            "primary_profile_id": None,
            "definition_version": None,
            "selection_basis": None,
            "capability_overlays": [],
            "binding_sha256": None,
        }
    valid_binding_shape = (
        version in SUPPORTED_REPORT_IR_VERSIONS
        and version == "1.1"
        and isinstance(binding, dict)
        and binding.get("primary_profile_id") in WORKFLOW_PROFILE_IDS
        and binding.get("definition_version") == WORKFLOW_PROFILE_DEFINITION_VERSION
        and isinstance(binding.get("selection_basis"), str)
        and isinstance(binding.get("capability_overlays"), list)
    )
    if valid_binding_shape:
        assert isinstance(binding, dict)
        return {
            "binding_contract_version": WORKFLOW_PROFILE_BINDING_CONTRACT_VERSION,
            "binding_state": "bound",
            "primary_profile_id": binding["primary_profile_id"],
            "definition_version": binding["definition_version"],
            "selection_basis": binding["selection_basis"],
            "capability_overlays": copy.deepcopy(binding["capability_overlays"]),
            "binding_sha256": sha256_bytes(canonical_bytes(binding)),
        }
    return {
        "binding_contract_version": WORKFLOW_PROFILE_BINDING_CONTRACT_VERSION,
        "binding_state": "invalid",
        "primary_profile_id": None,
        "definition_version": None,
        "selection_basis": None,
        "capability_overlays": [],
        "binding_sha256": None,
    }


def validate_ir(
    raw: dict[str, Any],
    artifact_root: Path | None = None,
) -> dict[str, Any]:
    normalized = normalize_ir(raw)
    schema = load_json(SCHEMA_PATH)
    syntax_issues = schema_errors(normalized, schema, schema)
    if syntax_issues:
        reference_issues: list[str] = []
        semantic_issues: list[str] = []
        compiler_issues: list[str] = []
        verified_files: list[str] = []
    else:
        reference_issues, semantic_issues, compiler_issues, verified_files = _semantic_validation(
            normalized,
            artifact_root.resolve(strict=True) if artifact_root is not None else None,
        )

    schema_valid = not syntax_issues
    references_valid = schema_valid and not reference_issues
    semantics_valid = references_valid and not semantic_issues
    compiler_ready = semantics_valid and not compiler_issues
    status = "PASS" if compiler_ready else "FAIL"
    workflow_profile = workflow_profile_record(normalized)
    return {
        "report_ir_version": normalized.get("report_ir_version"),
        "status": status,
        "schema_valid": schema_valid,
        "references_valid": references_valid,
        "semantics_valid": semantics_valid,
        "compiler_ready": compiler_ready,
        "issues": {
            "schema": syntax_issues,
            "references": reference_issues,
            "semantics": semantic_issues,
            "compiler": compiler_issues,
        },
        "identity": {
            "report_id": normalized.get("report", {}).get("id"),
            "projection_id": normalized.get("projection", {}).get("id"),
            "revision_id": normalized.get("traceability", {}).get("revision_id"),
            "normalized_sha256": sha256_bytes(canonical_bytes(normalized)),
            "workflow_profile_binding_sha256": workflow_profile["binding_sha256"],
        },
        "workflow_profile": workflow_profile,
        "counts": {
            key: len(normalized.get(key, []))
            for key in (
                "chapters",
                "narrative_units",
                "blocks",
                "claims",
                "evidence",
                "evidence_links",
                "sources",
                "datasets",
                "assets",
                "pages",
                "speaker_notes",
                "appendices",
                "extensions",
            )
        },
        "verified_files": verified_files,
        "qa_execution_claim": "not_executed_by_validator",
        "normalized_ir": normalized,
    }
