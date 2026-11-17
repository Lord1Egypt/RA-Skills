#!/usr/bin/env python3
"""Apply a controlled Runtime editor patch back to TaoHtml Report IR v1."""

from __future__ import annotations

import argparse
import base64
import binascii
import copy
import json
import re
import sys
import tempfile
from html.parser import HTMLParser
from pathlib import Path
from typing import Any


SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from render_visual_system import local_image_data_uri  # noqa: E402
from report_ir_core import (  # noqa: E402
    canonical_bytes,
    load_json,
    schema_errors,
    sha256_bytes,
    strict_json_loads,
    validate_ir,
    workflow_profile_record,
    write_json,
)


PATCH_SCHEMA_PATH = (
    SCRIPT_DIR.parent / "references" / "report-ir-runtime-patch.schema.json"
)
PATCH_SCRIPT_ID = "taohtml-report-ir-runtime-patch"
DATA_URI = re.compile(
    r"^data:(image/(?:png|jpeg|webp)|image/svg\+xml);base64,([A-Za-z0-9+/=]+)$"
)
MAX_IMAGE_BYTES = 50 * 1024 * 1024
IMAGE_EXTENSIONS = {
    "image/png": ".png",
    "image/jpeg": ".jpg",
    "image/webp": ".webp",
    "image/svg+xml": ".svg",
}
TEXT_FIELDS = {
    "block": {"text", "caption"},
    "claim": {"statement"},
    "evidence": {"summary"},
    "page": {"task"},
    "narrative_unit": {"takeaway"},
    "appendix": {"title"},
}
ENTITY_COLLECTIONS = {
    "block": "blocks",
    "claim": "claims",
    "evidence": "evidence",
    "page": "pages",
    "narrative_unit": "narrative_units",
    "appendix": "appendices",
}


class PatchApplyError(RuntimeError):
    """Raised when a Runtime patch cannot be applied without guessing."""


class _EditedHtmlParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self._capturing_patch = False
        self._patch_chunks: list[str] = []
        self.patch_payloads: list[str] = []
        self.images: dict[str, list[dict[str, str]]] = {}

    def handle_starttag(
        self,
        tag: str,
        attrs: list[tuple[str, str | None]],
    ) -> None:
        attributes = {key: value or "" for key, value in attrs}
        if tag == "script" and attributes.get("id") == PATCH_SCRIPT_ID:
            if self._capturing_patch:
                raise PatchApplyError("nested Report IR patch scripts are invalid")
            self._capturing_patch = True
            self._patch_chunks = []
        if tag == "img" and attributes.get("data-ir-edit-key"):
            key = attributes["data-ir-edit-key"]
            self.images.setdefault(key, []).append(attributes)

    def handle_data(self, data: str) -> None:
        if self._capturing_patch:
            self._patch_chunks.append(data)

    def handle_endtag(self, tag: str) -> None:
        if tag == "script" and self._capturing_patch:
            self.patch_payloads.append("".join(self._patch_chunks))
            self._capturing_patch = False
            self._patch_chunks = []


def _load_patch_from_html(path: Path) -> tuple[dict[str, Any], _EditedHtmlParser]:
    parser = _EditedHtmlParser()
    parser.feed(path.read_text(encoding="utf-8"))
    parser.close()
    if parser._capturing_patch:
        raise PatchApplyError("Report IR patch script is not closed")
    if len(parser.patch_payloads) != 1:
        raise PatchApplyError(
            f"edited HTML must contain exactly one {PATCH_SCRIPT_ID!r} script; "
            f"observed={len(parser.patch_payloads)}"
        )
    try:
        patch = strict_json_loads(parser.patch_payloads[0])
    except (json.JSONDecodeError, ValueError) as exc:
        raise PatchApplyError(f"embedded Report IR patch is invalid JSON: {exc}") from exc
    if not isinstance(patch, dict):
        raise PatchApplyError("embedded Report IR patch must be a JSON object")
    return patch, parser


def _load_patch(
    patch_path: Path | None,
    edited_html: Path | None,
) -> tuple[dict[str, Any], _EditedHtmlParser | None]:
    if (patch_path is None) == (edited_html is None):
        raise PatchApplyError("provide exactly one of --patch or --edited-html")
    if edited_html is not None:
        return _load_patch_from_html(edited_html)
    assert patch_path is not None
    return load_json(patch_path), None


def _validate_patch_schema(patch: dict[str, Any]) -> None:
    schema = load_json(PATCH_SCHEMA_PATH)
    issues = schema_errors(patch, schema, schema)
    if issues:
        raise PatchApplyError("Runtime patch schema failed:\n- " + "\n- ".join(issues))
    if patch["operation_count"] != len(patch["operations"]):
        raise PatchApplyError(
            "Runtime patch operation_count does not match operations length"
        )
    keys = [operation["target"]["key"] for operation in patch["operations"]]
    if len(keys) != len(set(keys)):
        raise PatchApplyError("Runtime patch contains duplicate target keys")
    if keys != sorted(keys):
        raise PatchApplyError("Runtime patch operations must be sorted by target key")


def _index(ir: dict[str, Any], entity: str) -> dict[str, dict[str, Any]]:
    collection = ENTITY_COLLECTIONS[entity]
    return {item["id"]: item for item in ir[collection]}


def _target_key(target: dict[str, str]) -> str:
    return f"{target['entity']}:{target['id']}:{target['field']}"


def _resolve_text_field(
    ir: dict[str, Any],
    target: dict[str, str],
) -> tuple[dict[str, Any], str]:
    entity = target["entity"]
    identity = target["id"]
    field = target["field"]
    if entity == "block" and field.startswith("items."):
        parts = field.split(".")
        if len(parts) != 3 or parts[2] not in {"label", "value", "detail"}:
            raise PatchApplyError(f"unsupported block item field: {field}")
        block = _index(ir, "block").get(identity)
        if block is None:
            raise PatchApplyError(f"patch references unknown block: {identity}")
        item = next(
            (candidate for candidate in block.get("items", []) if candidate["id"] == parts[1]),
            None,
        )
        if item is None:
            raise PatchApplyError(
                f"patch references unknown block item: {identity}.{parts[1]}"
            )
        return item, parts[2]
    if field not in TEXT_FIELDS.get(entity, set()):
        raise PatchApplyError(f"unsupported text target: {entity}.{field}")
    record = _index(ir, entity).get(identity)
    if record is None:
        raise PatchApplyError(f"patch references unknown {entity}: {identity}")
    return record, field


def _fnv1a_js(value: str) -> str:
    """Match the Runtime's FNV-1a hash over JavaScript UTF-16 code units."""
    encoded = value.encode("utf-16-le", "surrogatepass")
    result = 2166136261
    for index in range(0, len(encoded), 2):
        code_unit = encoded[index] | (encoded[index + 1] << 8)
        result ^= code_unit
        result = (result * 16777619) & 0xFFFFFFFF
    return f"{result:08x}"


def _style_values(style: str) -> dict[str, str]:
    result: dict[str, str] = {}
    for declaration in style.split(";"):
        if ":" not in declaration:
            continue
        name, value = declaration.split(":", 1)
        result[name.strip().lower()] = value.strip()
    return result


def _image_state(attributes: dict[str, str]) -> dict[str, str]:
    styles = _style_values(attributes.get("style", ""))
    source = attributes.get("src", "")
    return {
        "src_fingerprint": _fnv1a_js(source),
        "object_position": styles.get("object-position", ""),
        "aspect_ratio": styles.get("aspect-ratio", ""),
    }


def _resolve_project_path(root: Path, relative: str, label: str) -> Path:
    root = root.resolve(strict=True)
    try:
        path = root.joinpath(*relative.split("/")).resolve(strict=True)
        path.relative_to(root)
    except (OSError, ValueError) as exc:
        raise PatchApplyError(f"{label} is unavailable or escapes artifact root") from exc
    if not path.is_file() or path.is_symlink():
        raise PatchApplyError(f"{label} must resolve to a regular non-symlink file")
    return path


def _expected_base_image_state(
    block: dict[str, Any],
    asset: dict[str, Any],
    artifact_root: Path,
) -> dict[str, str]:
    locator = asset["locator"]
    if locator["kind"] != "project_relative":
        raise PatchApplyError(
            f"runtime image patch requires project_relative asset: {asset['id']}"
        )
    source = _resolve_project_path(
        artifact_root,
        locator["value"],
        f"asset.{asset['id']}",
    )
    uri = local_image_data_uri(source)
    return {
        "src_fingerprint": _fnv1a_js(uri),
        "object_position": block.get("image_crop_position", ""),
        "aspect_ratio": block.get("image_aspect_ratio", ""),
    }


def _decode_image_data_uri(source: str) -> tuple[bytes, str]:
    match = DATA_URI.fullmatch(source)
    if match is None:
        raise PatchApplyError(
            "edited image must use an embedded PNG, JPEG, WebP, or SVG data URI"
        )
    mime_type = match.group(1)
    try:
        payload = base64.b64decode(match.group(2), validate=True)
    except (binascii.Error, ValueError) as exc:
        raise PatchApplyError("edited image data URI has invalid base64") from exc
    if not payload:
        raise PatchApplyError("edited image data URI is empty")
    if len(payload) > MAX_IMAGE_BYTES:
        raise PatchApplyError(
            f"edited image exceeds the {MAX_IMAGE_BYTES // (1024 * 1024)} MB Runtime patch limit"
        )

    suffix = IMAGE_EXTENSIONS[mime_type]
    temporary_path: Path | None = None
    try:
        with tempfile.NamedTemporaryFile(suffix=suffix, delete=False) as handle:
            handle.write(payload)
            temporary_path = Path(handle.name)
        canonical_uri = local_image_data_uri(temporary_path)
    except (OSError, ValueError) as exc:
        raise PatchApplyError(f"edited image payload is invalid: {exc}") from exc
    finally:
        if temporary_path is not None:
            temporary_path.unlink(missing_ok=True)
    if not canonical_uri.startswith(f"data:{mime_type};base64,"):
        raise PatchApplyError("edited image MIME type disagrees with its file content")
    return payload, suffix


def _html_image(
    parser: _EditedHtmlParser | None,
    key: str,
) -> dict[str, str]:
    if parser is None:
        raise PatchApplyError(
            "replace_image operations require --edited-html so image bytes can be extracted"
        )
    candidates = parser.images.get(key, [])
    if not candidates:
        raise PatchApplyError(f"edited HTML has no image for Report IR target: {key}")
    states = {
        json.dumps(
            {
                "src": item.get("src", ""),
                "state": _image_state(item),
            },
            ensure_ascii=False,
            sort_keys=True,
        )
        for item in candidates
    }
    if len(states) != 1:
        raise PatchApplyError(
            f"edited HTML has divergent repeated images for Report IR target: {key}"
        )
    return candidates[0]


def _add_image_disclosure(
    ir: dict[str, Any],
    asset_id: str,
    image_sha256: str,
) -> None:
    unresolved_id = f"runtime-image-{image_sha256[:16]}"
    unresolved = ir["traceability"]["unresolved_items"]
    unresolved[:] = [item for item in unresolved if item["entity_ref"] != asset_id]
    unresolved.append(
        {
            "id": unresolved_id,
            "entity_ref": asset_id,
            "reason": "该图片由用户在 Runtime 编辑器中替换，文件完整性已验证，但内容含义尚未重新核验。",
            "customer_action": "请确认图片内容、品牌使用和事实表达无误。",
        }
    )
    ir["traceability"]["pending_verification_required"] = True


def apply_patch(
    raw_ir: dict[str, Any],
    patch: dict[str, Any],
    artifact_root: Path,
    *,
    edited_html_parser: _EditedHtmlParser | None = None,
    meaning_impact: str,
) -> tuple[dict[str, Any], dict[str, Any], list[tuple[Path, bytes]]]:
    if meaning_impact not in {"preserving", "changing"}:
        raise PatchApplyError("meaning_impact must be preserving or changing")
    artifact_root = artifact_root.resolve(strict=True)
    validation = validate_ir(raw_ir, artifact_root)
    if not validation["compiler_ready"]:
        issues = [
            issue
            for layer in ("schema", "references", "semantics", "compiler")
            for issue in validation["issues"][layer]
        ]
        raise PatchApplyError("base Report IR is not compiler-ready:\n- " + "\n- ".join(issues))
    ir = copy.deepcopy(validation["normalized_ir"])
    base_hash = validation["identity"]["normalized_sha256"]
    if patch["base_ir_sha256"] != base_hash:
        raise PatchApplyError(
            "Runtime patch base_ir_sha256 does not match the normalized base Report IR"
        )
    if patch["report_id"] != ir["report"]["id"]:
        raise PatchApplyError("Runtime patch report_id does not match the base Report IR")
    if patch["projection_id"] != ir["projection"]["id"]:
        raise PatchApplyError("Runtime patch projection_id does not match the base Report IR")

    assets = {item["id"]: item for item in ir["assets"]}
    staged_assets: list[tuple[Path, bytes]] = []
    touched: list[dict[str, str]] = []
    for operation in patch["operations"]:
        target = operation["target"]
        if target["key"] != _target_key(target):
            raise PatchApplyError(
                f"Runtime patch target key is not canonical: {target['key']}"
            )
        if operation["op"] == "replace_text":
            record, field = _resolve_text_field(ir, target)
            if field not in record:
                raise PatchApplyError(
                    f"Runtime patch target field does not exist: {target['key']}"
                )
            if record[field] != operation["before"]:
                raise PatchApplyError(
                    f"stale Runtime patch before-value for target: {target['key']}"
                )
            record[field] = operation["value"]
        elif operation["op"] == "replace_image":
            if target["entity"] != "block" or target["field"] != "image":
                raise PatchApplyError("replace_image must target block.<id>.image")
            block = _index(ir, "block").get(target["id"])
            if block is None or block.get("kind") != "image":
                raise PatchApplyError(
                    f"replace_image references a non-image block: {target['id']}"
                )
            asset_id = operation["asset_id"]
            if block.get("asset_ref") != asset_id or asset_id not in assets:
                raise PatchApplyError(
                    f"replace_image asset binding is invalid for block: {target['id']}"
                )
            before = _expected_base_image_state(block, assets[asset_id], artifact_root)
            if before != operation["before"]:
                raise PatchApplyError(
                    f"stale Runtime image patch before-value for target: {target['key']}"
                )
            dom_ref = operation["value"]["dom_ref"]
            if dom_ref["value"] != target["key"]:
                raise PatchApplyError("replace_image dom_ref does not match target key")
            attributes = _html_image(edited_html_parser, target["key"])
            expected_attributes = {
                "data-ir-edit-kind": "image",
                "data-ir-edit-entity": "block",
                "data-ir-edit-id": target["id"],
                "data-ir-edit-field": "image",
                "data-ir-edit-asset-id": asset_id,
            }
            mismatched_attributes = {
                name: {"expected": expected, "observed": attributes.get(name)}
                for name, expected in expected_attributes.items()
                if attributes.get(name) != expected
            }
            if mismatched_attributes:
                raise PatchApplyError(
                    "edited HTML image annotations do not match the IR target: "
                    + json.dumps(mismatched_attributes, ensure_ascii=False, sort_keys=True)
                )
            actual_state = _image_state(attributes)
            declared_state = {
                key: operation["value"][key]
                for key in ("src_fingerprint", "object_position", "aspect_ratio")
            }
            if actual_state != declared_state:
                raise PatchApplyError(
                    f"edited HTML image state does not match patch: {target['key']}"
                )
            payload, suffix = _decode_image_data_uri(attributes.get("src", ""))
            image_sha256 = sha256_bytes(payload)
            relative = f"runtime-edits/{asset_id}-{image_sha256[:12]}{suffix}"
            assets[asset_id]["locator"] = {"kind": "project_relative", "value": relative}
            assets[asset_id]["sha256"] = image_sha256
            assets[asset_id]["content_status"] = "pending_verification"
            assets[asset_id].pop("source_ref", None)
            if actual_state["object_position"]:
                block["image_crop_position"] = actual_state["object_position"]
            else:
                block.pop("image_crop_position", None)
            if actual_state["aspect_ratio"]:
                block["image_aspect_ratio"] = actual_state["aspect_ratio"]
            else:
                block.pop("image_aspect_ratio", None)
            _add_image_disclosure(ir, asset_id, image_sha256)
            staged_assets.append((artifact_root / relative, payload))
        else:  # pragma: no cover - schema prevents this branch
            raise PatchApplyError(f"unsupported Runtime patch operation: {operation['op']}")
        touched.append(
            {
                "operation": operation["op"],
                "entity": target["entity"],
                "id": target["id"],
                "field": target["field"],
            }
        )

    previous_revision = ir["traceability"]["revision_id"]
    patch_sha256 = sha256_bytes(canonical_bytes(patch))
    ir["traceability"]["previous_revision_ref"] = previous_revision
    ir["traceability"]["revision_id"] = f"runtime-{patch_sha256[:16]}"
    if meaning_impact == "changing":
        ir["traceability"]["design_brief_confirmation"] = (
            "reconfirmation_required"
        )
    report = {
        "status": (
            "APPLIED" if meaning_impact == "preserving" else "RECONFIRMATION_REQUIRED"
        ),
        "base_ir_sha256": base_hash,
        "patch_sha256": patch_sha256,
        "workflow_profile": workflow_profile_record(ir),
        "meaning_impact": meaning_impact,
        "design_brief_reconfirmation_required": meaning_impact == "changing",
        "compiler_authorized": meaning_impact == "preserving",
        "operation_count": len(patch["operations"]),
        "touched_entities": touched,
        "written_assets": [
            path.relative_to(artifact_root).as_posix() for path, _payload in staged_assets
        ],
        "delivery_verification_required": bool(staged_assets),
    }
    return ir, report, staged_assets


def _write_applied_result(
    ir: dict[str, Any],
    report: dict[str, Any],
    staged_assets: list[tuple[Path, bytes]],
    artifact_root: Path,
    output_ir: Path,
    output_report: Path,
) -> dict[str, Any]:
    created_paths: list[Path] = []
    try:
        for path, payload in staged_assets:
            path.parent.mkdir(parents=True, exist_ok=True)
            if path.exists() and path.read_bytes() != payload:
                raise PatchApplyError(f"runtime edit asset path collision: {path}")
            if not path.exists():
                path.write_bytes(payload)
                created_paths.append(path)
        validation = validate_ir(ir, artifact_root)
        reconfirmation_required = report["design_brief_reconfirmation_required"]
        required_layers_valid = all(
            validation[key]
            for key in ("schema_valid", "references_valid", "semantics_valid")
        )
        expected_confirmation_issue = (
            "traceability.design_brief_confirmation must be confirmed before compilation"
        )
        valid_draft_gate = (
            reconfirmation_required
            and required_layers_valid
            and not validation["compiler_ready"]
            and validation["issues"]["compiler"] == [expected_confirmation_issue]
        )
        if not validation["compiler_ready"] and not valid_draft_gate:
            issues = [
                issue
                for layer in ("schema", "references", "semantics", "compiler")
                for issue in validation["issues"][layer]
            ]
            raise PatchApplyError(
                "patched Report IR is not compiler-ready:\n- " + "\n- ".join(issues)
            )
        normalized = validation["normalized_ir"]
        report["patched_ir_sha256"] = validation["identity"]["normalized_sha256"]
        report["report_ir_validation"] = {
            key: validation[key]
            for key in (
                "schema_valid",
                "references_valid",
                "semantics_valid",
                "compiler_ready",
                "qa_execution_claim",
            )
        }
        report["report_ir_validation"]["issues"] = validation["issues"]
        write_json(output_ir, normalized)
        write_json(output_report, report)
        return report
    except Exception:
        for path in created_paths:
            path.unlink(missing_ok=True)
        raise


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Apply an exported TaoHtml Runtime editor patch to Report IR v1."
    )
    parser.add_argument("base_ir", type=Path)
    source = parser.add_mutually_exclusive_group(required=True)
    source.add_argument("--edited-html", type=Path)
    source.add_argument("--patch", type=Path)
    parser.add_argument("--artifact-root", type=Path, required=True)
    parser.add_argument("--output-ir", type=Path, required=True)
    parser.add_argument("--output-report", type=Path, required=True)
    parser.add_argument(
        "--meaning-impact",
        choices=("preserving", "changing"),
        required=True,
        help="Agent/user classification: whether the edit preserves or changes report meaning.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        base_path = args.base_ir.resolve(strict=True)
        output_ir_path = args.output_ir.resolve()
        output_report_path = args.output_report.resolve()
        if output_ir_path == base_path:
            raise PatchApplyError("--output-ir must not overwrite the base Report IR")
        if output_report_path in {base_path, output_ir_path}:
            raise PatchApplyError(
                "--output-report must be distinct from the base and output Report IR"
            )
        raw_ir = load_json(args.base_ir)
        patch, html_parser = _load_patch(args.patch, args.edited_html)
        _validate_patch_schema(patch)
        ir, report, staged_assets = apply_patch(
            raw_ir,
            patch,
            args.artifact_root,
            edited_html_parser=html_parser,
            meaning_impact=args.meaning_impact,
        )
        final = _write_applied_result(
            ir,
            report,
            staged_assets,
            args.artifact_root.resolve(strict=True),
            args.output_ir,
            args.output_report,
        )
    except (OSError, ValueError, PatchApplyError) as exc:
        print(f"REPORT_IR_PATCH_ERROR: {exc}", file=sys.stderr)
        return 1
    print(json.dumps(final, ensure_ascii=False, indent=2))
    return 0 if not final["design_brief_reconfirmation_required"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
