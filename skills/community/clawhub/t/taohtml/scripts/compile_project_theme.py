#!/usr/bin/env python3
"""Compile a confirmed static-reference VI handoff into a project theme."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path
from typing import Any, Callable

SCRIPT_ROOT = Path(__file__).resolve().parent
if str(SCRIPT_ROOT) not in sys.path:
    sys.path.insert(0, str(SCRIPT_ROOT))

import render_reference_vi
from project_theme_layout import resolve_layout_items


THEME_SCHEMA_VERSION = "1.0"
LEGACY_SINGLE_HANDOFF_SCHEMA_VERSION = "1.0"
LEGACY_FAMILY_HANDOFF_SCHEMA_VERSION = "1.1"
CURRENT_SINGLE_HANDOFF_SCHEMA_VERSION = "2.0"
CURRENT_FAMILY_HANDOFF_SCHEMA_VERSION = "2.1"
HANDOFF_SCHEMA_VERSIONS = {
    LEGACY_SINGLE_HANDOFF_SCHEMA_VERSION,
    LEGACY_FAMILY_HANDOFF_SCHEMA_VERSION,
    CURRENT_SINGLE_HANDOFF_SCHEMA_VERSION,
    CURRENT_FAMILY_HANDOFF_SCHEMA_VERSION,
}
FAMILY_HANDOFF_SCHEMA_VERSIONS = {
    LEGACY_FAMILY_HANDOFF_SCHEMA_VERSION,
    CURRENT_FAMILY_HANDOFF_SCHEMA_VERSION,
}
CURRENT_HANDOFF_SCHEMA_VERSIONS = {
    CURRENT_SINGLE_HANDOFF_SCHEMA_VERSION,
    CURRENT_FAMILY_HANDOFF_SCHEMA_VERSION,
}
TOP_LEVEL_KEYS = {
    "schema_version",
    "project",
    "confirmation",
    "inputs",
    "target_mode",
    "customer_corrections",
}
OUTPUT_FILES = {"theme.json", "theme.css", "templates.html", "provenance.json"}
SLUG = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
SHA256 = re.compile(r"^[0-9a-f]{64}$")
HEX = re.compile(r"^#[0-9A-Fa-f]{6}$")
NUMBER_PX = re.compile(r"(?P<value>\d{1,3})(?:\s*[–—-]\s*\d{1,3})?\s*px", re.IGNORECASE)
PERCENT = re.compile(r"(?P<value>\d{1,2})\s*%")
REMOTE_ASSET = re.compile(
    r"(?:src|href)\s*=\s*['\"]\s*(?:https?:)?//|@import\b|url\(\s*['\"]?\s*(?:https?:)?//",
    re.IGNORECASE,
)


def _exact_object(raw: object, keys: set[str], label: str) -> dict[str, Any]:
    if not isinstance(raw, dict):
        raise ValueError(f"{label} must be an object.")
    actual = set(raw)
    if actual != keys:
        missing = ", ".join(sorted(keys - actual)) or "none"
        extra = ", ".join(sorted(actual - keys)) or "none"
        raise ValueError(f"{label} keys mismatch; missing: {missing}; extra: {extra}.")
    return raw


def _text(value: object, label: str, maximum: int = 120) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{label} must be a non-empty string.")
    normalized = value.strip()
    if len(normalized) > maximum:
        raise ValueError(f"{label} exceeds {maximum} characters.")
    return normalized


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _safe_input(root: Path, value: object, label: str) -> Path:
    relative = Path(_text(value, label, 240))
    if relative.is_absolute() or ".." in relative.parts:
        raise ValueError(f"{label} must be a safe path relative to the handoff file.")
    try:
        resolved = (root / relative).resolve(strict=True)
    except FileNotFoundError as exc:
        raise ValueError(f"{label} does not exist: {relative}") from exc
    try:
        resolved.relative_to(root)
    except ValueError as exc:
        raise ValueError(f"{label} escapes the handoff directory: {relative}") from exc
    if not resolved.is_file():
        raise ValueError(f"{label} is not a file: {relative}")
    return resolved


def load_handoff(
    path: Path,
) -> tuple[dict[str, Any], dict[str, Any], Path, Path | list[Path]]:
    try:
        handoff_path = path.expanduser().resolve(strict=True)
    except FileNotFoundError as exc:
        raise ValueError(f"Handoff request does not exist: {path}") from exc
    if not handoff_path.is_file():
        raise ValueError(f"Handoff request is not a file: {handoff_path}")
    try:
        raw = json.loads(handoff_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise ValueError(f"Handoff request is not valid JSON: {exc}") from exc
    request = _exact_object(raw, TOP_LEVEL_KEYS, "handoff")
    handoff_schema = request["schema_version"]
    if handoff_schema not in HANDOFF_SCHEMA_VERSIONS:
        raise ValueError(
            "handoff.schema_version must be one of: "
            + ", ".join(sorted(HANDOFF_SCHEMA_VERSIONS))
            + "."
        )
    is_family_handoff = handoff_schema in FAMILY_HANDOFF_SCHEMA_VERSIONS
    is_current_handoff = handoff_schema in CURRENT_HANDOFF_SCHEMA_VERSIONS

    project = _exact_object(request["project"], {"id", "display_name"}, "handoff.project")
    project_id = _text(project["id"], "handoff.project.id", 48)
    if not SLUG.fullmatch(project_id):
        raise ValueError("handoff.project.id must be a lowercase hyphenated slug.")
    display_name = _text(project["display_name"], "handoff.project.display_name", 80)

    confirmation_fields = {
        "status",
        "confirmation_ref" if is_current_handoff else "phrase",
        "vi_contract_sha256",
        "reference_images_sha256" if is_family_handoff else "reference_image_sha256",
    }
    confirmation = _exact_object(
        request["confirmation"], confirmation_fields, "handoff.confirmation"
    )
    if confirmation["status"] != "confirmed":
        raise ValueError('VI is not confirmed; status must be "confirmed".')
    if is_current_handoff:
        confirmation_ref = _text(
            confirmation["confirmation_ref"],
            "handoff.confirmation.confirmation_ref",
            160,
        )
        legacy_phrase = None
        confirmation_method = "conversation_ref"
    else:
        legacy_phrase = _text(
            confirmation["phrase"],
            "handoff.confirmation.phrase",
            20,
        )
        if legacy_phrase != "确认 VI":
            raise ValueError(
                'Legacy VI handoff is not confirmed; phrase must match its published schema.'
            )
        confirmation_ref = None
        confirmation_method = "legacy_phrase"
    if not isinstance(confirmation["vi_contract_sha256"], str) or not SHA256.fullmatch(
        confirmation["vi_contract_sha256"]
    ):
        raise ValueError("handoff.confirmation.vi_contract_sha256 must be a lowercase SHA-256 digest.")
    if not is_family_handoff:
        reference_hashes = [confirmation["reference_image_sha256"]]
        if not isinstance(reference_hashes[0], str) or not SHA256.fullmatch(reference_hashes[0]):
            raise ValueError(
                "handoff.confirmation.reference_image_sha256 must be a lowercase SHA-256 digest."
            )
        inputs = _exact_object(
            request["inputs"], {"vi_contract", "reference_image"}, "handoff.inputs"
        )
        reference_values = [inputs["reference_image"]]
    else:
        reference_hashes = confirmation["reference_images_sha256"]
        if (
            not isinstance(reference_hashes, list)
            or not 1 <= len(reference_hashes) <= 3
            or any(not isinstance(value, str) or not SHA256.fullmatch(value) for value in reference_hashes)
        ):
            raise ValueError(
                "handoff.confirmation.reference_images_sha256 must contain one to three lowercase SHA-256 digests."
            )
        inputs = _exact_object(
            request["inputs"], {"vi_contract", "reference_images"}, "handoff.inputs"
        )
        reference_values = inputs["reference_images"]
        if (
            not isinstance(reference_values, list)
            or len(reference_values) != len(reference_hashes)
        ):
            raise ValueError(
                "handoff.inputs.reference_images must align with reference_images_sha256."
            )
    root = handoff_path.parent.resolve()
    vi_path = _safe_input(root, inputs["vi_contract"], "handoff.inputs.vi_contract")
    reference_paths = [
        _safe_input(
            root,
            value,
            (
                "handoff.inputs.reference_image"
                if not is_family_handoff
                else f"handoff.inputs.reference_images[{index}]"
            ),
        )
        for index, value in enumerate(reference_values)
    ]
    if _sha256(vi_path) != confirmation["vi_contract_sha256"]:
        raise ValueError("Confirmed VI contract hash does not match the current file.")
    if [_sha256(reference_path) for reference_path in reference_paths] != reference_hashes:
        raise ValueError("Confirmed reference image hashes do not match the current files.")

    target_mode = request["target_mode"]
    if target_mode not in {"reading", "presentation"}:
        raise ValueError("handoff.target_mode must be reading or presentation.")
    corrections = request["customer_corrections"]
    if not isinstance(corrections, list) or len(corrections) > 20:
        raise ValueError("handoff.customer_corrections must be a list of at most 20 strings.")
    normalized_corrections = [
        _text(value, f"handoff.customer_corrections[{index}]", 180)
        for index, value in enumerate(corrections)
    ]

    contract = render_reference_vi.load_contract(vi_path)
    if render_reference_vi.is_family_contract(contract):
        if not is_family_handoff:
            raise ValueError(
                "VI schema 1.3/1.4 requires a family handoff schema with reference_images."
            )
    elif is_family_handoff:
        raise ValueError(
            "Legacy v1.1/v1.2 VI contracts require a single-reference handoff schema."
        )
    render_reference_vi.validate_source_bindings(contract, reference_paths)
    normalized = {
        "schema_version": handoff_schema,
        "project": {"id": project_id, "display_name": display_name},
        "confirmation": {
            "status": "confirmed",
            "confirmation_method": confirmation_method,
            "confirmation_ref": confirmation_ref,
            "legacy_phrase": legacy_phrase,
            "vi_contract_sha256": confirmation["vi_contract_sha256"],
            **(
                {"reference_images_sha256": reference_hashes}
                if is_family_handoff
                else {"reference_image_sha256": reference_hashes[0]}
            ),
        },
        "inputs": (
            {"vi_contract": vi_path.name, "reference_image": reference_paths[0].name}
            if not is_family_handoff
            else {
                "vi_contract": vi_path.name,
                "reference_images": [path.name for path in reference_paths],
            }
        ),
        "target_mode": target_mode,
        "customer_corrections": normalized_corrections,
    }
    return (
        normalized,
        contract,
        vi_path,
        reference_paths[0] if not is_family_handoff else reference_paths,
    )


def _luminance(color: str) -> float:
    channels = [int(color[index : index + 2], 16) / 255 for index in (1, 3, 5)]
    linear = [value / 12.92 if value <= 0.04045 else ((value + 0.055) / 1.055) ** 2.4 for value in channels]
    return 0.2126 * linear[0] + 0.7152 * linear[1] + 0.0722 * linear[2]


def _palette_token(
    items: list[dict[str, str]],
    token: str,
    keywords: tuple[str, ...],
    fallback: str,
    used: set[int],
    *,
    prefer_dark: bool = False,
    prefer_light: bool = False,
) -> tuple[str, dict[str, str]]:
    candidates = [
        (index, item)
        for index, item in enumerate(items)
        if item["status"] != "unknown" and HEX.fullmatch(item["value"])
    ]
    matches = [
        (index, item)
        for index, item in candidates
        if any(keyword in f"{item['name']} {item['role']}" for keyword in keywords)
    ]
    available = [(index, item) for index, item in (matches or candidates) if index not in used]
    if available:
        if prefer_dark:
            index, item = min(available, key=lambda entry: _luminance(entry[1]["value"]))
        elif prefer_light:
            index, item = max(available, key=lambda entry: _luminance(entry[1]["value"]))
        else:
            index, item = available[0]
        used.add(index)
        return item["value"].upper(), {
            "status": item["status"],
            "source": f"palette[{index}]",
            "basis": item["basis"],
        }
    return fallback, {
        "status": "fallback",
        "source": "compiler-neutral-default",
        "basis": f"VI did not provide a usable {token} color; neutral reversible fallback.",
    }


def _first_item(
    items: list[dict[str, str]], predicate: Callable[[dict[str, str]], bool]
) -> tuple[int, dict[str, str]] | None:
    return next(
        ((index, item) for index, item in enumerate(items) if item["status"] != "unknown" and predicate(item)),
        None,
    )


def _size_token(
    items: list[dict[str, str]],
    levels: tuple[str, ...],
    fallback: int,
    token: str,
) -> tuple[str, dict[str, str]]:
    result = _first_item(items, lambda item: item["level"].upper() in levels)
    if result:
        index, item = result
        match = NUMBER_PX.search(item["spec"])
        if match:
            value = int(match.group("value"))
            return f"{value}px", {
                "status": item["status"],
                "source": f"typography[{index}]",
                "basis": item["basis"],
            }
    return f"{fallback}px", {
        "status": "fallback",
        "source": "compiler-neutral-default",
        "basis": f"VI did not provide a parseable {token} size; neutral reversible fallback.",
    }


def _spacing_token(
    contract: dict[str, Any], labels: tuple[str, ...], fallback: str, token: str
) -> tuple[str, dict[str, str]]:
    result = _first_item(
        contract["layout"], lambda item: any(label in item["label"] for label in labels)
    )
    if result:
        index, item = result
        px = NUMBER_PX.search(item["value"])
        if px:
            return f"{int(px.group('value'))}px", {
                "status": item["status"],
                "source": f"layout[{index}]",
                "basis": item["basis"],
            }
        percent = PERCENT.search(item["value"])
        if percent:
            computed = round(1600 * int(percent.group("value")) / 100)
            return f"{computed}px", {
                "status": item["status"],
                "source": f"layout[{index}]",
                "basis": f"{item['basis']}；按 1600px 画布确定性换算。",
            }
    return fallback, {
        "status": "fallback",
        "source": "compiler-neutral-default",
        "basis": f"VI did not provide parseable {token}; neutral reversible fallback.",
    }


def _boundary_records(
    contract: dict[str, Any], usage_map: dict[str, list[str]]
) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    for section in render_reference_vi.SECTION_LIMITS:
        for index, item in enumerate(contract[section]):
            status = item["status"]
            path = f"{section}[{index}]"
            usage = sorted(set(usage_map.get(path, []))) if status != "unknown" else []
            records.append(
                {
                    "path": path,
                    "status": status,
                    "basis": item["basis"],
                    "eligible": status != "unknown",
                    "compiled": bool(usage),
                    "usage": usage,
                    "rule": (
                        "unknown is retained as an uncompiled boundary"
                        if status == "unknown"
                        else "eligible only; compiled is true only when usage targets are recorded"
                    ),
                }
            )
    for field, item in contract["executable_layout"].items():
        status = item["status"]
        path = f"executable_layout.{field}"
        usage = sorted(set(usage_map.get(path, []))) if status != "unknown" else []
        records.append(
            {
                "path": path,
                "value": item["value"],
                "status": status,
                "basis": item["basis"],
                "eligible": status != "unknown",
                "compiled": bool(usage),
                "usage": usage,
                "rule": (
                    "unknown is replaced only by a labeled neutral fallback"
                    if status == "unknown"
                    else "machine layout value compiled to the listed manifest, template, or CSS targets"
                ),
            }
        )
    return records


RHYTHM_BY_DENSITY = {
    "low": {
        "label_title": "24px",
        "title_lede": "20px",
        "heading_content": "44px",
        "card_title_body": "14px",
        "evidence_source": "20px",
    },
    "medium": {
        "label_title": "18px",
        "title_lede": "16px",
        "heading_content": "32px",
        "card_title_body": "12px",
        "evidence_source": "18px",
    },
    "high": {
        "label_title": "12px",
        "title_lede": "10px",
        "heading_content": "24px",
        "card_title_body": "8px",
        "evidence_source": "12px",
    },
}


def _compile_tokens(
    contract: dict[str, Any],
    plan: dict[str, str],
    structure_sources: dict[str, dict[str, str]],
) -> tuple[dict[str, str], dict[str, dict[str, str]]]:
    used: set[int] = set()
    colors: dict[str, str] = {}
    sources: dict[str, dict[str, str]] = {}
    color_specs = (
        ("canvas", ("画布", "底色", "纸张", "背景"), "#F4F2E9", False, True),
        ("ink", ("墨", "标题", "边框", "结构线", "正文"), "#17191A", True, False),
        ("signal", ("强调", "结论", "主要数据", "主色", "砖红"), "#B94B3F", False, False),
        ("accent", ("次级", "章节", "标签", "金", "黄"), "#C8A64B", False, False),
        ("panel", ("面板", "反白", "深", "图片"), "#233C37", True, False),
    )
    for token, keywords, fallback, dark, light in color_specs:
        colors[token], sources[f"colors.{token}"] = _palette_token(
            contract["palette"], token, keywords, fallback, used, prefer_dark=dark, prefer_light=light
        )
    colors["paper"] = colors["canvas"]
    sources["colors.paper"] = {
        **sources["colors.canvas"],
        "basis": f"{sources['colors.canvas']['basis']}；v1 复用为卡片纸色。",
    }

    display, display_source = _size_token(contract["typography"], ("H1",), 72, "display")
    heading, heading_source = _size_token(contract["typography"], ("H2", "H3"), 36, "heading")
    body, body_source = _size_token(contract["typography"], ("BODY", "P"), 20, "body")
    canvas_x, canvas_x_source = _spacing_token(
        contract, ("外边距", "安全区"), "64px", "horizontal canvas spacing"
    )
    gap, gap_source = _spacing_token(
        contract, ("模块间距", "组间距"), "22px", "module gap"
    )
    rhythm = RHYTHM_BY_DENSITY[plan["density"]]
    density_source = structure_sources["density"]
    if density_source["status"] == "fallback":
        rhythm_source = {
            "status": "fallback",
            "source": "compiler-neutral-default",
            "basis": "Unknown density uses the neutral medium semantic rhythm scale.",
        }
    else:
        density_item = contract["executable_layout"]["density"]
        rhythm_source = {
            "status": density_item["status"],
            "source": "executable_layout.density",
            "basis": f"{density_item['basis']}；确定性映射为 {plan['density']} 语义排版节奏。",
        }
    tokens = {
        **colors,
        "display_size": display,
        "heading_size": heading,
        "body_size": body,
        "caption_size": "13px",
        "canvas_x": canvas_x,
        "canvas_y": "46px",
        "gap": gap,
        **{f"rhythm_{name}": value for name, value in rhythm.items()},
    }
    sources.update(
        {
            "type.display_size": display_source,
            "type.heading_size": heading_source,
            "type.body_size": body_source,
            "type.caption_size": {
                "status": "fallback",
                "source": "compiler-neutral-default",
                "basis": "VI hierarchy does not require an exact caption size; neutral reversible fallback.",
            },
            "spacing.canvas_x": canvas_x_source,
            "spacing.canvas_y": {
                "status": "fallback",
                "source": "compiler-neutral-default",
                "basis": "Vertical safe area is a reversible runtime-fit fallback.",
            },
            "spacing.gap": gap_source,
            **{
                f"rhythm.{name}": dict(rhythm_source)
                for name in rhythm
            },
        }
    )
    return tokens, sources


def _layout_plan(
    contract: dict[str, Any],
) -> tuple[dict[str, str], dict[str, dict[str, str]], list[dict[str, Any]]]:
    plan, fallback_bases = resolve_layout_items(contract["executable_layout"])
    sources: dict[str, dict[str, str]] = {}
    fallbacks: list[dict[str, Any]] = []
    for field, item in contract["executable_layout"].items():
        path = f"executable_layout.{field}"
        if item["status"] == "unknown":
            sources[field] = {"status": "fallback", "source": "compiler-neutral-default"}
            fallbacks.append(
                {
                    "field": path,
                    "value": plan[field],
                    "status": "fallback",
                    "source": "compiler-neutral-default",
                    "basis": fallback_bases[field],
                    "usage": [],
                }
            )
        else:
            sources[field] = {"status": item["status"], "source": path}
    return plan, sources, fallbacks


def _layout_variants(plan: dict[str, str]) -> list[dict[str, str]]:
    split = plan["cover_split"].replace(":", "-")
    cover = (
        f"cover-split-{split}-image-{plan['image_placement']}-{plan['alignment']}"
        if plan["cover_structure"] == "split"
        else f"cover-single-column-image-{plan['image_placement']}-{plan['alignment']}"
    )
    data_variant = f"data-{plan['data_structure']}-{plan['data_columns']}-col"
    if plan["data_structure"] == "source-chart-split":
        data_variant += f"-image-{plan['image_placement']}"
    return [
        {"id": cover, "role": "cover"},
        {
            "id": f"content-{plan['content_structure']}-{plan['content_columns']}-col-{plan['module_organization']}",
            "role": "content",
        },
        {
            "id": f"process-{plan['page_axis']}-{plan['module_organization']}-{plan['density']}",
            "role": "content",
        },
        {
            "id": data_variant,
            "role": "evidence-data",
        },
        {
            "id": f"closing-{plan['content_structure']}-{plan['alignment']}-{plan['density']}",
            "role": "closing",
        },
    ]


def _evidence_choice(contract: dict[str, Any]) -> tuple[str, str | None, str]:
    for status in ("observed", "extension"):
        for index, item in enumerate(contract["evidence_language"]):
            if item["status"] == status and item["sample"] != "none":
                return item["sample"], f"evidence_language[{index}]", item["description"]
    return (
        "metric",
        None,
        "Neutral labeled metric fallback; no chart grammar is attributed to the reference.",
    )


def _evidence_markup(sample: str) -> str:
    if sample == "bar":
        return '<div class="pt-bars fragment" data-step="2"><div class="pt-bar"><strong>{{S4_M1_VALUE}}</strong><span>{{S4_M1_LABEL}}</span></div><div class="pt-bar"><strong>{{S4_M2_VALUE}}</strong><span>{{S4_M2_LABEL}}</span></div><div class="pt-bar"><strong>{{S4_M3_VALUE}}</strong><span>{{S4_M3_LABEL}}</span></div></div>'
    if sample == "line":
        return '<div class="pt-line-chart fragment" data-step="2"><svg viewBox="0 0 900 270" role="img" aria-label="{{S4_TITLE}}"><polyline points="45,220 250,145 455,178 655,72 850,105"/></svg><div class="pt-line-values"><strong>{{S4_M1_VALUE}}</strong><strong>{{S4_M2_VALUE}}</strong><strong>{{S4_M3_VALUE}}</strong></div></div>'
    if sample == "table":
        return '<table class="pt-table pt-table-focus fragment" data-step="2"><thead><tr><th>{{S4_TABLE_H1}}</th><th>{{S4_TABLE_H2}}</th><th>{{S4_TABLE_H3}}</th></tr></thead><tbody><tr><td>{{S4_R1_C1}}</td><td>{{S4_R1_C2}}</td><td>{{S4_R1_C3}}</td></tr><tr><td>{{S4_R2_C1}}</td><td>{{S4_R2_C2}}</td><td>{{S4_R2_C3}}</td></tr><tr><td>{{S4_R3_C1}}</td><td>{{S4_R3_C2}}</td><td>{{S4_R3_C3}}</td></tr></tbody></table>'
    if sample == "citation":
        return '<aside class="pt-citation-focus fragment" data-step="2"><strong>{{S4_SOURCE}}</strong><p>{{S4_LEDE}}</p></aside>'
    return '<div class="pt-metrics-focus fragment" data-step="2"><article><strong>{{S4_M1_VALUE}}</strong><span>{{S4_M1_LABEL}}</span></article><article><strong>{{S4_M2_VALUE}}</strong><span>{{S4_M2_LABEL}}</span></article><article><strong>{{S4_M3_VALUE}}</strong><span>{{S4_M3_LABEL}}</span></article></div>'


def _css(
    theme_id: str,
    tokens: dict[str, str],
    plan: dict[str, str],
    corporate_shell: dict[str, Any] | None = None,
) -> str:
    organization = plan["module_organization"]
    if organization == "hard-grid":
        border, radius, shadow = "3px solid var(--pt-ink)", "0", "none"
    elif organization == "soft-stack":
        border, radius, shadow = (
            "1px solid color-mix(in srgb, var(--pt-ink), transparent 72%)",
            "22px",
            "0 18px 48px rgba(38, 49, 58, .10)",
        )
    else:
        border, radius, shadow = "0 solid transparent", "0", "none"
    image_filter = {
        "natural": "none",
        "muted": "saturate(.68) contrast(1.03)",
        "monochrome": "grayscale(1) contrast(1.1)",
        "high-contrast": "contrast(1.25) saturate(1.05)",
    }[plan["image_treatment"]]
    text_align = {"start": "left", "center": "center", "end": "right"}[plan["alignment"]]
    align_items = {"start": "flex-start", "center": "center", "end": "flex-end"}[plan["alignment"]]
    copy_image_columns = {
        "7:5": ("7fr", "5fr"),
        "5:7": ("5fr", "7fr"),
        "1:1": ("1fr", "1fr"),
        "none": ("1fr", "1fr"),
    }[plan["cover_split"]]
    physical_columns = (
        reversed(copy_image_columns)
        if plan["image_placement"] == "left"
        else copy_image_columns
    )
    split_columns = " ".join(physical_columns)
    ratio_width, ratio_height = (
        int(part) for part in plan["image_aspect_ratio"].split(":")
    )
    aspect_ratio = f"{ratio_width} / {ratio_height}"
    title_width, focus_art_width, focus_art_height = {
        "headline-and-image": ("100%", 100, 480),
        "image-first": ("78%", 100, 540),
        "balanced": ("88%", 88, 460),
    }[plan["visual_focus"]]
    cover_art_width = focus_art_width
    cover_art_height = focus_art_height
    if plan["image_fit"] == "contain":
        cover_art_width = round(cover_art_width * 0.86)
        cover_art_height = round(cover_art_height * 0.82)
    cover_art_width_cap = round(cover_art_height * ratio_width / ratio_height)
    if plan["cover_structure"] == "split":
        cover_layout = (
            f"display:grid;grid-template-columns:{split_columns};gap:var(--pt-section-gap);"
            "align-items:center"
        )
    else:
        cover_layout = (
            f"display:flex;flex-direction:column;align-items:{align_items};justify-content:center;"
            f"gap:var(--pt-section-gap);text-align:{text_align}"
        )
        if plan["image_placement"] == "background":
            cover_layout += ";position:relative;overflow:hidden;isolation:isolate"
    content_columns = plan["content_columns"]
    data_columns = plan["data_columns"]
    evidence_columns = "2" if plan["data_structure"] == "source-chart-split" else "1"
    metric_columns = data_columns if plan["data_structure"] == "metrics-grid" else "3"
    process_layout = (
        "grid-template-columns:repeat(4,minmax(0,1fr))"
        if plan["page_axis"] == "row"
        else "grid-template-columns:minmax(0,860px);justify-content:center"
    )
    selector = f'.deck[data-theme="{theme_id}"]'
    corporate_css = ""
    if corporate_shell is not None:
        corporate_css = f"""
{selector} .slide.pt-corporate-page {{ position:absolute; isolation:isolate; overflow:hidden; padding:0; background:var(--pt-canvas); }}
{selector} .pt-corporate-fixed-shell {{ position:absolute; inset:0; z-index:3; overflow:hidden; pointer-events:none; animation:none !important; transition:none !important; transform:none !important; }}
{selector} .pt-corporate-fixed-region {{ position:absolute; z-index:1; display:block; object-fit:fill; pointer-events:none; animation:none !important; transition:none !important; transform:none !important; }}
{selector} .pt-corporate-editable {{ position:absolute; z-index:2; display:grid; align-content:center; overflow:hidden; padding:18px; }}
{selector} .pt-corporate-editable > .pt-cover-layout, {selector} .pt-corporate-editable > .pt-page-layout {{ min-height:0; height:100%; }}
{selector} .pt-corporate-editable .source-btn {{ top:12px; right:12px; }}
{selector} [data-shell-role="cover"] .pt-cover-layout {{ grid-template-columns:minmax(0,1fr) !important; gap:0; }}
{selector} [data-shell-role="cover"] .pt-cover-copy h1 {{ font-size:54px; line-height:.98; }}
{selector} [data-shell-role="cover"] .pt-cover-art {{ display:none !important; }}
{selector} [data-shell-role="section"] .pt-page-layout {{ height:100%; align-content:center; }}
"""
    return f"""{selector} {{
  --pt-canvas: {tokens['canvas']};
  --pt-ink: {tokens['ink']};
  --pt-signal: {tokens['signal']};
  --pt-accent: {tokens['accent']};
  --pt-panel: {tokens['panel']};
  --pt-paper: {tokens['paper']};
  --pt-display: {tokens['display_size']};
  --pt-heading: {tokens['heading_size']};
  --pt-body: {tokens['body_size']};
  --pt-caption: {tokens['caption_size']};
  --pt-canvas-x: {tokens['canvas_x']};
  --pt-canvas-y: {tokens['canvas_y']};
  --pt-gap: {tokens['gap']};
  --pt-rhythm-label-title: {tokens['rhythm_label_title']};
  --pt-rhythm-title-lede: {tokens['rhythm_title_lede']};
  --pt-rhythm-heading-content: {tokens['rhythm_heading_content']};
  --pt-rhythm-card-title-body: {tokens['rhythm_card_title_body']};
  --pt-rhythm-evidence-source: {tokens['rhythm_evidence_source']};
  --pt-section-gap: var(--pt-rhythm-heading-content);
  --pt-border: {border};
  --pt-radius: {radius};
  --pt-shadow: {shadow};
  --pt-text-align: {text_align};
  color: var(--pt-ink);
  background: var(--pt-canvas);
  font-family: Arial, "PingFang SC", "Microsoft YaHei", sans-serif;
}}

{selector} .slide {{ padding: var(--pt-canvas-y) var(--pt-canvas-x) 56px; color: var(--pt-ink); background: var(--pt-canvas); }}
{selector} .slide::before {{ display: none; }}
{selector} :where(h1, h2, h3, p) {{ margin: 0; }}
{selector} .fragment {{ transform: translateY(14px); transition: opacity .42s cubic-bezier(.2,.8,.2,1), transform .42s cubic-bezier(.2,.8,.2,1); }}
{selector} .fragment.visible, {selector}[data-mode="reading"] .fragment {{ transform: none; }}
.pt-page-layout {{display:grid;gap:var(--pt-rhythm-heading-content)}}
.pt-heading-block {{display:grid;justify-items:{plan['alignment']};gap:var(--pt-rhythm-label-title);text-align:var(--pt-text-align)}}
.pt-heading-copy,.pt-cover-title-group {{display:grid;justify-items:{plan['alignment']};gap:var(--pt-rhythm-title-lede)}}
.pt-kicker {{ display: inline-flex; padding: 7px 11px; color: var(--pt-ink); background: var(--pt-accent); border: var(--pt-border); border-radius:var(--pt-radius); font-size: var(--pt-caption); font-weight: 900; letter-spacing: .08em; }}
.pt-title {{ max-width: {title_width}; font-size: var(--pt-heading); line-height: 1.02; font-weight: 950; text-align:var(--pt-text-align); }}
.pt-lede {{ max-width: 1040px; font-size: var(--pt-body); line-height: 1.42; text-align:var(--pt-text-align); }}
.pt-footer {{ position: absolute; left: var(--pt-canvas-x); right: var(--pt-canvas-x); bottom: 28px; padding-top: 10px; border-top: 2px solid var(--pt-ink); font-size: var(--pt-caption); font-weight: 800; }}
.pt-cover-layout {{ {cover_layout}; height: 100%; }}
.pt-cover h1 {{font-size:var(--pt-display);line-height:.98;font-weight:950;letter-spacing:-.035em}}
.pt-cover-copy {{display:grid;justify-items:{plan['alignment']};gap:var(--pt-rhythm-label-title);text-align:{text_align}}}
.pt-cover-art {{ position: relative; width:min({cover_art_width}%,{cover_art_width_cap}px); height:auto; aspect-ratio:{aspect_ratio}; justify-self:center; align-self:center; overflow:hidden; background:var(--pt-panel); border:var(--pt-border); border-radius:var(--pt-radius); box-shadow:var(--pt-shadow); }}
.pt-cover-image-background .pt-cover-art {{position:absolute;left:50%;top:50%;z-index:0;width:100%;height:auto;transform:translate(-50%,-50%)}}
.pt-cover-image-background .pt-cover-copy {{position:relative;z-index:1;padding:34px;max-width:900px;background:color-mix(in srgb,var(--pt-canvas),transparent 12%);border:var(--pt-border);border-radius:var(--pt-radius);box-shadow:var(--pt-shadow)}}
.pt-cover-art::before {{ content: ""; position: absolute; width: 78%; height: 38%; left: -8%; top: 18%; background: var(--pt-signal); filter:{image_filter}; clip-path: polygon(0 72%, 20% 38%, 42% 62%, 65% 5%, 100% 54%, 100% 100%, 0 100%); }}
.pt-cover-art::after {{ content: ""; position: absolute; width: 170px; height: 170px; right: 11%; top: 10%; border-radius: 50%; background: var(--pt-accent); filter:{image_filter}; }}
.pt-claim {{ position: absolute; left: 28px; right: 28px; bottom: 28px; display:grid; justify-items:start; gap:var(--pt-rhythm-card-title-body); padding: 20px 22px; color: var(--pt-canvas); background: var(--pt-ink); border-left: 10px solid var(--pt-signal); font-size: 21px; line-height: 1.32; font-weight: 800; }}
.pt-background-claim {{display:grid;justify-items:start;gap:var(--pt-rhythm-card-title-body);padding:20px 22px;color:var(--pt-canvas);background:var(--pt-ink);border-left:10px solid var(--pt-signal);font-size:21px;line-height:1.32;font-weight:800}}
.pt-card-grid {{ display: grid; grid-template-columns: repeat({content_columns}, minmax(0,1fr)); gap: var(--pt-gap); }}
.pt-card {{ display:grid;align-content:start;gap:var(--pt-rhythm-label-title);min-height:250px;padding:25px;background:var(--pt-paper);border:var(--pt-border);border-radius:var(--pt-radius);box-shadow:var(--pt-shadow)}}
.pt-card-copy,.pt-item-copy {{display:grid;gap:var(--pt-rhythm-card-title-body)}}
.pt-card h3 {{font-size:31px;line-height:1.05}}
.pt-card p {{ font-size: 18px; line-height: 1.45; }}
.pt-label {{ display: inline-flex; padding: 6px 9px; background: var(--pt-accent); border: 2px solid var(--pt-ink); font-size: 12px; font-weight: 900; }}
.pt-content-stack,.pt-content-focus {{display:grid;grid-template-columns:repeat({content_columns},minmax(0,1fr));justify-content:center;gap:var(--pt-gap)}}
.pt-line-item,.pt-focus-point {{display:grid;grid-template-columns:120px 1fr;gap:var(--pt-rhythm-label-title);align-items:center;padding:20px 24px;background:var(--pt-paper);border:var(--pt-border);border-radius:var(--pt-radius);box-shadow:var(--pt-shadow)}}
.pt-focus-lead {{padding:34px;text-align:{text_align};background:var(--pt-panel);color:var(--pt-canvas);border-radius:var(--pt-radius);box-shadow:var(--pt-shadow)}}
.pt-process {{ display:grid; {process_layout}; gap: var(--pt-gap); }}
.pt-step {{display:grid;align-content:start;gap:var(--pt-rhythm-label-title);min-height:220px;padding:26px;background:var(--pt-paper);border:var(--pt-border);border-radius:var(--pt-radius);box-shadow:var(--pt-shadow)}}
.pt-process-column {{gap:12px}}
.pt-process-column .pt-step {{display:grid;grid-template-columns:78px 1fr;min-height:0;align-items:center;padding:14px 22px}}
.pt-process-column .pt-step strong {{font-size:46px}}
.pt-step strong {{ display: block; color: var(--pt-signal); font-size: 62px; line-height: 1; font-weight: 950; }}
.pt-step h3 {{font-size:28px}}
.pt-step p {{ font-size: 17px; line-height: 1.42; }}
.pt-evidence-layout {{ display: grid; grid-template-columns: repeat({evidence_columns},minmax(0,1fr)); gap: var(--pt-gap); }}
.pt-source-frame {{ width:100%; aspect-ratio:{aspect_ratio}; margin:0; overflow:hidden; background:var(--pt-panel);border:var(--pt-border);border-radius:var(--pt-radius);box-shadow:var(--pt-shadow)}}
.pt-source-frame img {{ width: 100%; height: 100%; object-fit: {plan['image_fit']}; filter: {image_filter}; }}
.pt-data-panel,.pt-chart-focus,.pt-table-focus-wrap,.pt-metrics-grid {{display:grid;gap:var(--pt-rhythm-evidence-source);padding:24px;color:var(--pt-canvas);background:var(--pt-panel);border:var(--pt-border);border-radius:var(--pt-radius);box-shadow:var(--pt-shadow)}}
.pt-bars {{ display: grid; grid-template-columns: repeat(3, 1fr); align-items: end; gap: 20px; height: 210px; padding: 22px 18px 0; border-bottom: 2px solid var(--pt-canvas); }}
.pt-bar {{ display: grid; align-content: end; min-height: 40%; padding: 16px 10px; color: var(--pt-ink); background: var(--pt-signal); font-weight: 900; text-align: center; }}
.pt-bar:nth-child(2) {{ min-height: 68%; background: var(--pt-accent); }} .pt-bar:nth-child(3) {{ min-height: 88%; background: var(--pt-canvas); }}
.pt-bar strong {{ display: block; font-size: 38px; }} .pt-bar span {{ font-size: 12px; }}
.pt-table {{ width: 100%; border-collapse: collapse; font-size: 14px; }}
.pt-table th, .pt-table td {{ padding: 9px 10px; border-bottom: 1px solid color-mix(in srgb, var(--pt-canvas), transparent 60%); text-align: left; }}
.pt-line-chart svg {{width:100%;height:260px}} .pt-line-chart polyline {{fill:none;stroke:var(--pt-accent);stroke-width:16;stroke-linecap:round;stroke-linejoin:round}}
.pt-line-values {{display:flex;justify-content:space-around;font-size:30px}} .pt-metrics-focus {{display:grid;grid-template-columns:repeat({metric_columns},minmax(0,1fr));gap:var(--pt-gap)}}
.pt-metrics-focus article {{padding:30px;text-align:center;border:var(--pt-border);border-radius:var(--pt-radius)}} .pt-metrics-focus strong {{display:block;font-size:50px}}
.pt-citation-focus {{display:grid;place-items:center;gap:var(--pt-rhythm-title-lede);min-height:300px;padding:42px;text-align:center;border:var(--pt-border);border-radius:var(--pt-radius)}}
.pt-focus-source {{text-align:center;font-size:var(--pt-caption);opacity:.72}}
.pt-actions-grid {{ display: grid; grid-template-columns: repeat({content_columns}, minmax(0,1fr)); gap: var(--pt-gap); }}
.pt-action {{display:grid;align-content:start;gap:var(--pt-rhythm-label-title);min-height:230px;padding:24px;background:var(--pt-paper);border:var(--pt-border);border-radius:var(--pt-radius);box-shadow:var(--pt-shadow)}}
.pt-action-stack {{display:grid;grid-template-columns:minmax(0,860px);justify-content:center;gap:var(--pt-gap)}}
.pt-action-row {{display:grid;grid-template-columns:90px 1fr;gap:var(--pt-rhythm-label-title);align-items:center;padding:20px 28px;border-bottom:1px solid color-mix(in srgb,var(--pt-ink),transparent 75%)}}
.pt-action strong {{color:var(--pt-signal);font-size:54px;line-height:1}} .pt-action h3 {{font-size:27px}}
.pt-closing-stack {{display:grid;gap:var(--pt-rhythm-heading-content)}}
.pt-final {{padding:20px 24px;color:var(--pt-canvas);background:var(--pt-ink);border-left:12px solid var(--pt-signal);font-size:24px;font-weight:900}}
{selector} .source-btn {{ top: 48px; right: var(--pt-canvas-x); background: var(--pt-ink); color: var(--pt-canvas); border-radius: var(--pt-radius); }}
{corporate_css}
"""


def _heading(kicker: str, title: str, lede: str) -> str:
    return (
        '<div class="pt-heading-block" data-rhythm-check="--pt-rhythm-label-title">'
        f'<div class="pt-kicker" data-rhythm-from>{{{{{kicker}}}}}</div>'
        '<div class="pt-heading-copy" data-rhythm-to '
        'data-rhythm-check="--pt-rhythm-title-lede">'
        f'<h2 class="pt-title" data-rhythm-from>{{{{{title}}}}}</h2>'
        f'<p class="pt-lede" data-rhythm-to>{{{{{lede}}}}}</p></div></div>'
    )


def _page_layout(heading: str, body: str) -> str:
    return (
        '<div class="pt-page-layout" '
        'data-rhythm-check="--pt-rhythm-heading-content">'
        f'<div data-rhythm-from>{heading}</div>'
        f'<div data-rhythm-to>{body}</div></div>'
    )


def _bbox_style(bbox: list[float]) -> str:
    x, y, width, height = bbox
    return (
        f"left:{x * 100:.6f}%;top:{y * 100:.6f}%;"
        f"width:{width * 100:.6f}%;height:{height * 100:.6f}%"
    )


def _corporate_shell_contract(
    contract: dict[str, Any], extracted_regions: list[dict[str, object]]
) -> dict[str, Any] | None:
    if (
        contract.get("reference_mode") != "corporate_fidelity"
        or render_reference_vi.is_family_contract(contract)
    ):
        return None
    editable = contract["editable_regions"][0]
    fixed_html = "".join(
        f'<img class="pt-corporate-fixed-region" data-locked-region="{region["id"]}" '
        f'data-fixed-element-type="{region["type"]}" data-crop-sha256="{region["sha256"]}" '
        f'src="{region["data_uri"]}" alt="" style="{_bbox_style(region["bbox"])}">'
        for region in extracted_regions
    )
    return {
        "editable_region": editable,
        "fixed_regions": extracted_regions,
        "shell_html": (
            '<div class="pt-corporate-fixed-shell" aria-hidden="true" '
            'data-fixed-motion="none">'
            + fixed_html
            + "</div>"
        ),
    }


def _corporate_family_contract(
    contract: dict[str, Any], extracted_assets: list[dict[str, object]]
) -> dict[str, Any] | None:
    if not render_reference_vi.is_family_contract(contract):
        return None
    assets = {str(asset["id"]): asset for asset in extracted_assets}
    shells: dict[str, dict[str, Any]] = {}
    for variant in contract["shell_variants"]:
        fixed_regions: list[dict[str, object]] = []
        fixed_html: list[str] = []
        for placement in variant["locked_regions"]:
            asset = assets[str(placement["asset_id"])]
            fixed_region = {
                **placement,
                "source_page_id": asset["source_page_id"],
                "source_image_sha256": asset["source_image_sha256"],
                "source_bbox": asset["source_bbox"],
                "source_pixel_bbox": asset["source_pixel_bbox"],
                "source_crop_sha256": asset["source_crop_sha256"],
                "replaceable_regions": asset["replaceable_regions"],
                "crop_sha256": asset["sha256"],
                "crop_size": [asset["width"], asset["height"]],
            }
            fixed_regions.append(fixed_region)
            fixed_html.append(
                f'<img class="pt-corporate-fixed-region" '
                f'data-locked-region="{placement["id"]}" '
                f'data-fixed-element-type="{placement["type"]}" '
                f'data-asset-id="{placement["asset_id"]}" '
                f'data-source-page-id="{asset["source_page_id"]}" '
                f'data-crop-sha256="{asset["sha256"]}" '
                f'src="{asset["data_uri"]}" alt="" '
                f'style="{_bbox_style(placement["bbox"])}">'
            )
        shells[str(variant["role"])] = {
            "role": variant["role"],
            "status": variant["status"],
            "reference_page_id": variant["reference_page_id"],
            "fixed_regions": fixed_regions,
            "editable_region": variant["editable_region"],
            "basis": variant["basis"],
            "shell_html": (
                '<div class="pt-corporate-fixed-shell" aria-hidden="true" '
                'data-fixed-motion="none">'
                + "".join(fixed_html)
                + "</div>"
            ),
        }
    return {
        "reference_pages": contract["reference_pages"],
        "shared_assets": extracted_assets,
        "replaceable_regions": [
            region
            for asset in extracted_assets
            for region in asset["replaceable_regions"]
        ],
        "shared_brand_grammar": contract["shared_brand_grammar"],
        "shells": shells,
        "extension_pages": contract["extension_pages"],
        "limitations": contract["limitations"],
    }


def _wrap_page_content(
    role: str, body: str, corporate_shell: dict[str, Any] | None
) -> str:
    if corporate_shell is None:
        return body + '<div class="pt-footer">{{FOOTER}}</div>'
    editable = corporate_shell["editable_region"]
    if role not in editable["allowed_content"]:
        raise ValueError(
            f"Corporate editable region does not allow the generated {role} page role."
        )
    return (
        corporate_shell["shell_html"]
        + f'<div class="pt-corporate-editable" data-editable-region="{editable["id"]}" '
        f'data-content-role="{role}" style="{_bbox_style(editable["bbox"])}">'
        + body
        + "</div>"
    )


def _wrap_family_page(
    role: str, body: str, corporate_family: dict[str, Any]
) -> tuple[str, str]:
    shell = corporate_family["shells"][role]
    editable = shell["editable_region"]
    if editable["allowed_content"] != [role]:
        raise ValueError(f"Corporate {role} shell does not allow its generated page role.")
    source_page_id = shell["reference_page_id"] or ""
    section_attributes = (
        f'data-shell-role="{role}" '
        f'data-shell-status="{shell["status"]}" '
        f'data-source-page-id="{source_page_id}"'
    )
    content = (
        shell["shell_html"]
        + f'<div class="pt-corporate-editable" data-editable-region="{editable["id"]}" '
        f'data-content-role="{role}" style="{_bbox_style(editable["bbox"])}">'
        + body
        + "</div>"
    )
    return section_attributes, content


def _templates(
    plan: dict[str, str],
    variants: list[dict[str, str]],
    evidence_sample: str,
    corporate_shell: dict[str, Any] | None = None,
) -> str:
    page_class = " pt-corporate-page" if corporate_shell is not None else ""
    background_claim = ""
    if plan["image_placement"] == "background":
        background_claim = (
            '<aside class="pt-background-claim fragment" data-step="1" '
            'data-rhythm-check="--pt-rhythm-card-title-body">'
            '<span class="pt-label" data-rhythm-from>{{S1_LABEL}}</span>'
            '<p data-rhythm-to>{{S1_CLAIM}}</p></aside>'
        )
    cover_copy = (
        '<div class="pt-cover-copy" data-rhythm-check="--pt-rhythm-label-title">'
        '<div class="pt-kicker" data-rhythm-from>{{S1_KICKER}}</div>'
        '<div class="pt-cover-title-group" data-rhythm-to '
        'data-rhythm-check="--pt-rhythm-title-lede">'
        '<h1 data-rhythm-from>{{S1_TITLE_A}}<br>{{S1_TITLE_B}}</h1>'
        '<p class="pt-lede" data-rhythm-to>{{S1_LEDE}}</p></div>'
        f'{background_claim}</div>'
    )
    art_claim = ""
    if plan["image_placement"] != "background":
        art_claim = (
            '<aside class="pt-claim fragment" data-step="1" '
            'data-rhythm-check="--pt-rhythm-card-title-body">'
            '<span class="pt-label" data-rhythm-from>{{S1_LABEL}}</span>'
            '<p data-rhythm-to>{{S1_CLAIM}}</p></aside>'
        )
    cover_art = (
        f'<div class="pt-cover-art" role="img" aria-label="项目主题几何主视觉" '
        f'data-image-fit="{plan["image_fit"]}" '
        f'data-image-treatment="{plan["image_treatment"]}" '
        f'data-image-aspect-ratio="{plan["image_aspect_ratio"]}">'
        f'{art_claim}</div>'
    )
    cover_children = cover_art + cover_copy if plan["image_placement"] in {"left", "top"} else cover_copy + cover_art
    cover_body = f'<div class="pt-cover-layout pt-cover-{plan["cover_structure"]} pt-cover-image-{plan["image_placement"]}" data-cover-split="{plan["cover_split"]}">{cover_children}</div>'
    cover = f'<section class="slide active pt-cover{page_class}" data-title="核心命题" data-layout="{variants[0]["id"]}">{_wrap_page_content("cover", cover_body, corporate_shell)}</section>'

    content_items = [
        f'<article class="pt-card fragment" data-step="{index}" data-rhythm-check="--pt-rhythm-label-title"><span class="pt-label" data-rhythm-from>{{{{S2_{index}_LABEL}}}}</span><div class="pt-card-copy" data-rhythm-to data-rhythm-check="--pt-rhythm-card-title-body"><h3 data-rhythm-from>{{{{S2_{index}_TITLE}}}}</h3><p data-rhythm-to>{{{{S2_{index}_BODY}}}}</p></div></article>'
        for index in range(1, 4)
    ]
    if plan["content_structure"] == "card-grid":
        content_body = '<div class="pt-card-grid">' + "".join(content_items) + "</div>"
    elif plan["content_structure"] == "single-focus":
        focus_points = "".join(
            f'<article class="pt-focus-point fragment" data-step="{index}" data-rhythm-check="--pt-rhythm-label-title" data-rhythm-axis="inline"><span class="pt-label" data-rhythm-from>{{{{S2_{index}_LABEL}}}}</span><div class="pt-item-copy" data-rhythm-to data-rhythm-check="--pt-rhythm-card-title-body"><h3 data-rhythm-from>{{{{S2_{index}_TITLE}}}}</h3><p data-rhythm-to>{{{{S2_{index}_BODY}}}}</p></div></article>'
            for index in range(1, 4)
        )
        content_body = '<div class="pt-content-focus"><div class="pt-focus-lead fragment" data-step="1">{{S2_1_BODY}}</div>' + focus_points + "</div>"
    else:
        content_body = '<div class="pt-content-stack">' + "".join(
            f'<article class="pt-line-item fragment" data-step="{index}" data-rhythm-check="--pt-rhythm-label-title" data-rhythm-axis="inline"><span class="pt-label" data-rhythm-from>{{{{S2_{index}_LABEL}}}}</span><div class="pt-item-copy" data-rhythm-to data-rhythm-check="--pt-rhythm-card-title-body"><h3 data-rhythm-from>{{{{S2_{index}_TITLE}}}}</h3><p data-rhythm-to>{{{{S2_{index}_BODY}}}}</p></div></article>'
            for index in range(1, 4)
        ) + "</div>"
    content_layout = _page_layout(
        _heading("S2_KICKER", "S2_TITLE", "S2_LEDE"), content_body
    )
    content = f'<section class="slide{page_class}" data-title="内容诊断" data-layout="{variants[1]["id"]}">{_wrap_page_content("content", content_layout, corporate_shell)}</section>'

    step_tag = "li" if plan["page_axis"] == "column" else "article"
    step_axis = ' data-rhythm-axis="inline"' if plan["page_axis"] == "column" else ""
    process_body = "".join(
        f'<{step_tag} class="pt-step fragment" data-step="{index}" data-rhythm-check="--pt-rhythm-label-title"{step_axis}><strong data-rhythm-from>{{{{S3_{index}_NUM}}}}</strong><div class="pt-item-copy" data-rhythm-to data-rhythm-check="--pt-rhythm-card-title-body"><h3 data-rhythm-from>{{{{S3_{index}_TITLE}}}}</h3><p data-rhythm-to>{{{{S3_{index}_BODY}}}}</p></div></{step_tag}>'
        for index in range(1, 5)
    )
    process_wrapper = "ol" if step_tag == "li" else "div"
    process_content = f'<{process_wrapper} class="pt-process pt-process-{plan["page_axis"]}">{process_body}</{process_wrapper}>'
    process_layout = _page_layout(
        _heading("S3_KICKER", "S3_TITLE", "S3_LEDE"), process_content
    )
    process = f'<section class="slide{page_class}" data-title="内容机制" data-layout="{variants[2]["id"]}">{_wrap_page_content("process", process_layout, corporate_shell)}</section>'

    chart = _evidence_markup(evidence_sample)
    source_frame = '<figure class="pt-source-frame fragment" data-step="1"><img src="{{SOURCE_URI}}" alt="{{SOURCE_LABEL}}"></figure>'
    if plan["data_structure"] == "source-chart-split":
        data_panel = f'<div class="pt-data-panel" data-rhythm-check="--pt-rhythm-evidence-source"><div data-rhythm-from>{chart}</div><table class="pt-table fragment" data-step="3" data-rhythm-to><thead><tr><th>{{{{S4_TABLE_H1}}}}</th><th>{{{{S4_TABLE_H2}}}}</th><th>{{{{S4_TABLE_H3}}}}</th></tr></thead><tbody><tr><td>{{{{S4_R1_C1}}}}</td><td>{{{{S4_R1_C2}}}}</td><td>{{{{S4_R1_C3}}}}</td></tr><tr><td>{{{{S4_R2_C1}}}}</td><td>{{{{S4_R2_C2}}}}</td><td>{{{{S4_R2_C3}}}}</td></tr><tr><td>{{{{S4_R3_C1}}}}</td><td>{{{{S4_R3_C2}}}}</td><td>{{{{S4_R3_C3}}}}</td></tr></tbody></table></div>'
        data_children = (
            source_frame + data_panel
            if plan["image_placement"] == "left"
            else data_panel + source_frame
        )
        data_body = f'<div class="pt-evidence-layout" data-image-placement="{plan["image_placement"]}">{data_children}</div>'
    elif plan["data_structure"] == "table-focus":
        data_body = f'<div class="pt-evidence-layout" data-image-placement="{plan["image_placement"]}"><div class="pt-table-focus-wrap" data-rhythm-check="--pt-rhythm-evidence-source"><div data-rhythm-from>{_evidence_markup("table")}</div><p class="pt-focus-source" data-rhythm-to>{{{{S4_SOURCE}}}}</p></div></div>'
    elif plan["data_structure"] == "metrics-grid":
        data_body = f'<div class="pt-evidence-layout" data-image-placement="{plan["image_placement"]}"><div class="pt-metrics-grid" data-rhythm-check="--pt-rhythm-evidence-source"><div data-rhythm-from>{_evidence_markup("metric")}</div><p class="pt-focus-source" data-rhythm-to>{{{{S4_SOURCE}}}}</p></div></div>'
    else:
        data_body = f'<div class="pt-evidence-layout" data-image-placement="{plan["image_placement"]}"><div class="pt-chart-focus" data-rhythm-check="--pt-rhythm-evidence-source"><div data-rhythm-from>{chart}</div><p class="pt-focus-source" data-rhythm-to>{{{{S4_SOURCE}}}}</p></div></div>'
    data_layout = _page_layout(
        _heading("S4_KICKER", "S4_TITLE", "S4_LEDE"), data_body
    )
    data_body_with_source = f'<button class="source-btn" data-taohtml-edit-lock data-source="{{{{SOURCE_URI}}}}" data-source-kind="{{{{SOURCE_KIND}}}}" data-source-label="{{{{SOURCE_LABEL}}}}">{{{{S4_SOURCE}}}}</button>{data_layout}'
    data = f'<section class="slide{page_class}" data-title="证据与数据" data-layout="{variants[3]["id"]}">{_wrap_page_content("data", data_body_with_source, corporate_shell)}</section>'

    if plan["content_structure"] == "card-grid":
        closing_body = '<div class="pt-actions-grid">' + "".join(
            f'<article class="pt-action fragment" data-step="{index}" data-rhythm-check="--pt-rhythm-label-title"><strong data-rhythm-from>{{{{S5_{index}_NUM}}}}</strong><div class="pt-item-copy" data-rhythm-to data-rhythm-check="--pt-rhythm-card-title-body"><h3 data-rhythm-from>{{{{S5_{index}_TITLE}}}}</h3><p data-rhythm-to>{{{{S5_{index}_BODY}}}}</p></div></article>'
            for index in range(1, 4)
        ) + "</div>"
    else:
        closing_body = '<div class="pt-action-stack">' + "".join(
            f'<article class="pt-action-row fragment" data-step="{index}" data-rhythm-check="--pt-rhythm-label-title" data-rhythm-axis="inline"><strong data-rhythm-from>{{{{S5_{index}_NUM}}}}</strong><div class="pt-item-copy" data-rhythm-to data-rhythm-check="--pt-rhythm-card-title-body"><h3 data-rhythm-from>{{{{S5_{index}_TITLE}}}}</h3><p data-rhythm-to>{{{{S5_{index}_BODY}}}}</p></div></article>'
            for index in range(1, 4)
        ) + "</div>"
    closing_content = f'<div class="pt-closing-stack">{closing_body}<div class="pt-final fragment" data-step="4"><span class="pt-label">{{{{S5_LABEL}}}}</span> {{{{S5_CLAIM}}}}</div></div>'
    closing_layout = _page_layout(
        _heading("S5_KICKER", "S5_TITLE", "S5_LEDE"), closing_content
    )
    closing = f'<section class="slide{page_class}" data-title="行动收束" data-layout="{variants[4]["id"]}">{_wrap_page_content("closing", closing_layout, corporate_shell)}</section>'
    return "\n\n".join((cover, content, process, data, closing))


def _family_templates(
    plan: dict[str, str],
    variants: list[dict[str, str]],
    evidence_sample: str,
    corporate_family: dict[str, Any],
) -> str:
    """Reuse the shared theme grammar while routing five report roles to five shells."""
    base = _templates(plan, variants, evidence_sample, None)
    sections = re.findall(r"<section\b.*?</section>", base, flags=re.DOTALL)
    if len(sections) != 5:
        raise ValueError("Shared template compiler did not produce exactly five pages.")
    # Shared templates are cover, content, process, data, closing.  For a family,
    # the content and process grammars become toc and section; content uses the
    # action grammar, while data retains the evidence grammar.
    source_indices = {"cover": 0, "toc": 1, "section": 2, "content": 4, "data": 3}
    titles = {
        "cover": "封面",
        "toc": "目录",
        "section": "章节",
        "content": "普通内容",
        "data": "数据",
    }
    output: list[str] = []
    for page_index, role in enumerate(render_reference_vi.FAMILY_ROLES):
        source = sections[source_indices[role]]
        body_start = source.index(">") + 1
        body = source[body_start : -len("</section>")].replace(
            '<div class="pt-footer">{{FOOTER}}</div>', ""
        )
        if role == "cover":
            body, removed = re.subn(
                r'<div class="pt-cover-art"[^>]*>.*?</div>',
                "",
                body,
                count=1,
                flags=re.DOTALL,
            )
            if removed != 1:
                raise ValueError(
                    "Corporate family cover must remove the generated art layer; "
                    "the observed fixed composition is the only cover visual."
                )
        elif role == "section":
            body = _page_layout(
                _heading("S3_KICKER", "S3_TITLE", "S3_LEDE"), ""
            )
        attributes, wrapped = _wrap_family_page(role, body, corporate_family)
        active = " active" if page_index == 0 else ""
        output.append(
            f'<section class="slide{active} pt-corporate-page" '
            f'data-title="{titles[role]}" data-layout="corporate-{role}" '
            f'{attributes}>{wrapped}</section>'
        )
    return "\n\n".join(output)


def _json_text(value: object) -> str:
    return json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n"


GRAMMAR_USAGE = {
    "page_axis": ["templates.html:process DOM axis", "theme.css:.pt-process", "theme.json:identity.composition"],
    "alignment": ["templates.html:heading wrappers", "theme.css:--pt-text-align", "theme.json:identity.composition"],
    "cover_structure": ["templates.html:cover DOM wrapper", "theme.css:.pt-cover-layout", "theme.json:layout_variants[0]"],
    "cover_split": ["templates.html:.pt-cover-layout data-cover-split", "theme.json:layout_variants[0]"],
    "content_structure": ["templates.html:content and closing DOM branches", "theme.json:layout_variants[1,4]"],
    "content_columns": ["theme.css:content/closing grid-template-columns", "theme.json:layout_variants[1]"],
    "image_placement": ["templates.html:cover DOM order/background layer", "theme.css:.pt-cover-layout placement geometry", "theme.json:layout_variants[0]"],
    "image_aspect_ratio": ["templates.html:.pt-cover-art data-image-aspect-ratio", "theme.css:.pt-cover-art aspect-ratio", "theme.json:components.image"],
    "image_fit": ["templates.html:.pt-cover-art data-image-fit", "theme.css:.pt-cover-art width/background fill", "theme.json:components.image"],
    "image_treatment": ["templates.html:.pt-cover-art data-image-treatment", "theme.css:.pt-cover-art shape filter", "theme.json:identity.image_treatment"],
    "data_structure": ["templates.html:data DOM branch", "theme.css:data branch geometry", "theme.json:layout_variants[3]"],
    "data_columns": ["theme.css:structure-specific data grid-template-columns", "theme.json:layout_variants[3]"],
    "module_organization": ["theme.css:--pt-border/--pt-radius/--pt-shadow", "theme.json:identity.module_language"],
    "density": [
        "theme.css:semantic rhythm custom properties",
        "templates.html:data-rhythm-check contracts",
        "theme.json:layout_variants[2,4]",
    ],
    "visual_focus": ["theme.css:.pt-title/.pt-cover-art width and height", "theme.json:identity.composition"],
}


def _grammar_usage(field: str, plan: dict[str, str]) -> list[str]:
    usage = list(GRAMMAR_USAGE[field])
    if field == "cover_split":
        usage.append(
            "theme.css:.pt-cover-layout grid-template-columns"
            if plan["cover_structure"] == "split"
            else "compiler guardrail:single-column cover requires cover_split=none"
        )
    if plan["data_structure"] == "source-chart-split":
        conditional = {
            "image_placement": "templates.html:data source DOM order",
            "image_aspect_ratio": "theme.css:.pt-source-frame aspect-ratio",
            "image_fit": "theme.css:.pt-source-frame img object-fit",
            "image_treatment": "theme.css:.pt-source-frame img filter",
        }.get(field)
        if conditional:
            usage.append(conditional)
        if field == "image_placement":
            usage.append("theme.json:layout_variants[3]")
    return usage


def _token_targets(source_key: str) -> list[str]:
    token = source_key.split(".", 1)[1]
    if source_key.startswith("rhythm."):
        manifest_token = f"rhythm_{token}"
        css_token = f"--pt-rhythm-{token.replace('_', '-')}"
        return [
            f"theme.json:tokens.{manifest_token}",
            f"theme.css:{css_token}",
        ]
    css_token = {
        "display_size": "--pt-display",
        "heading_size": "--pt-heading",
        "body_size": "--pt-body",
        "caption_size": "--pt-caption",
        "canvas_x": "--pt-canvas-x",
        "canvas_y": "--pt-canvas-y",
        "gap": "--pt-gap",
    }.get(token, f"--pt-{token}")
    return [f"theme.json:tokens.{token}", f"theme.css:{css_token}"]


def compile_theme(request_path: Path, output_theme: Path) -> Path:
    request, contract, vi_path, reference_input = load_handoff(request_path)
    reference_paths = (
        [reference_input] if isinstance(reference_input, Path) else reference_input
    )
    theme_id = f"project-{request['project']['id']}"
    reference_mode = contract.get("reference_mode", "reconstruct")
    is_family = render_reference_vi.is_family_contract(contract)
    extracted_regions = (
        []
        if is_family
        else render_reference_vi.extract_locked_regions(contract, reference_paths[0])
    )
    extracted_assets = (
        render_reference_vi.extract_corporate_assets(contract, reference_paths)
        if is_family
        else []
    )
    corporate_shell = _corporate_shell_contract(contract, extracted_regions)
    corporate_family = _corporate_family_contract(contract, extracted_assets)
    plan, structure_sources, structure_fallbacks = _layout_plan(contract)
    tokens, token_sources = _compile_tokens(contract, plan, structure_sources)
    variants = (
        [{"id": f"corporate-{role}", "role": role} for role in render_reference_vi.FAMILY_ROLES]
        if corporate_family is not None
        else _layout_variants(plan)
    )
    evidence_sample, evidence_path, evidence_rule = _evidence_choice(contract)
    usage_map: dict[str, list[str]] = {}
    fallback_records: list[dict[str, Any]] = []

    for source_key, source in token_sources.items():
        targets = _token_targets(source_key)
        source["usage"] = targets
        if source["status"] == "fallback":
            fallback_records.append({"token": source_key, **source})
        else:
            usage_map.setdefault(source["source"], []).extend(targets)
    for field, source in structure_sources.items():
        targets = [
            f"theme.json:executable_layout.{field}",
            *_grammar_usage(field, plan),
            *usage_map.get(source["source"], []),
        ]
        targets = sorted(set(targets))
        source["usage"] = targets
        if source["status"] != "fallback":
            usage_map.setdefault(source["source"], []).extend(targets)
    for record in structure_fallbacks:
        field = record["field"].split(".", 1)[1]
        record["usage"] = [
            f"theme.json:executable_layout.{field}", *_grammar_usage(field, plan)
        ]
        fallback_records.append(record)
    if evidence_path is not None:
        usage_map.setdefault(evidence_path, []).extend(
            ["templates.html:data evidence markup", "theme.css:evidence visualization rules", "theme.json:identity.chart_evidence"]
        )
    else:
        fallback_records.append(
            {
                "field": "evidence_language",
                "value": evidence_sample,
                "status": "fallback",
                "source": "compiler-neutral-default",
                "basis": evidence_rule,
                "usage": ["templates.html:data evidence markup", "theme.css:evidence visualization rules"],
            }
        )
    preserve = [
        item["description"]
        for item in contract["guardrails"]
        if item["mode"] == "preserve" and item["status"] != "unknown"
    ]
    forbidden = [
        item["description"]
        for item in contract["guardrails"]
        if item["mode"] == "avoid" and item["status"] != "unknown"
    ]
    for index, item in enumerate(contract["guardrails"]):
        if item["status"] != "unknown":
            target = "theme.json:preserve guardrail" if item["mode"] == "preserve" else "theme.json:forbidden guardrail"
            usage_map.setdefault(f"guardrails[{index}]", []).append(target)
    boundaries = _boundary_records(contract, usage_map)
    counts = {
        status: sum(record["status"] == status for record in boundaries)
        for status in ("observed", "extension", "unknown")
    }
    counts["eligible"] = sum(record["eligible"] for record in boundaries)
    counts["compiled"] = sum(record["compiled"] for record in boundaries)
    composition = (
        f"{plan['cover_structure']} cover ({plan['cover_split']}) with image {plan['image_placement']}; "
        f"{plan['content_structure']} content in {plan['content_columns']} column(s); "
        f"{plan['page_axis']} process; {plan['data_structure']} data page in {plan['data_columns']} column(s); "
        f"{plan['module_organization']} modules, {plan['density']} density, {plan['visual_focus']} focus."
    )
    image_component = (
        f"Cover visual at {plan['image_placement']}, {plan['image_aspect_ratio']}, "
        f"{plan['image_fit']} fit, with the local evidence source sharing that placement; "
        "source_kind remains renderer-controlled."
        if plan["data_structure"] == "source-chart-split"
        else f"Cover visual at {plan['image_placement']}, {plan['image_aspect_ratio']}, "
        f"{plan['image_fit']} fit; this data structure does not place a local source image, "
        "and source_kind remains renderer-controlled."
    )
    manifest: dict[str, Any] = {
        "schema_version": THEME_SCHEMA_VERSION,
        "kind": "project",
        "id": theme_id,
        "display_name": request["project"]["display_name"],
        "description": "由已确认静态参考 VI 合同编译的当前项目专用主题",
        "project": {
            "id": request["project"]["id"],
            "target_mode": request["target_mode"],
            "global_built_in": False,
            "reference_mode": reference_mode,
        },
        "files": {
            "tokens": "theme.css",
            "templates": "templates.html",
            "provenance": "provenance.json",
        },
        "identity": {
            "composition": composition,
            "hierarchy": f"{plan['alignment']}-aligned {plan['visual_focus']} hierarchy at {plan['density']} information density.",
            "image_treatment": f"{plan['image_treatment']} cover visual and applicable local evidence imagery, {plan['image_fit']} fit, {plan['image_aspect_ratio']} ratio.",
            "module_language": f"{plan['module_organization']} organization with {plan['content_structure']} content modules.",
            "chart_evidence": evidence_rule,
            "motion": "TaoHtml Runtime reveal syntax; not observed or inferred from the static reference.",
        },
        "tokens": tokens,
        "token_sources": token_sources,
        "executable_layout": plan,
        "structure_sources": structure_sources,
        "canvas": {
            "aspect_ratio": "16:9",
            "grid": f"{plan['page_axis']} axis; {plan['content_columns']} content column(s); {plan['alignment']} alignment",
            "safe_area": f"{tokens['canvas_x']} horizontal; {tokens['canvas_y']} vertical",
        },
        "layout_variants": variants,
        "components": {
            "card": f"{plan['module_organization']} module used by the {plan['content_structure']} content structure.",
            "panel": f"{plan['data_structure']} evidence panel at {plan['density']} density.",
            "label": "Compact solid section tag with no provenance implication.",
            "border": f"Border, radius, and shadow are compiled from {plan['module_organization']}.",
            "image": image_component,
            "chart": evidence_rule,
        },
        "preserve": preserve,
        "forbidden": forbidden,
        "motion": {
            "observed_from_reference": False,
            "source": "TaoHtml shared Runtime and report-task reveal decisions",
            "enter": "generic opacity plus 14px upward reveal over 420ms",
            "stagger": "existing fragment and data-step syntax",
            "disabled": ["reference-inferred timing", "reference-inferred transitions", "cross-page morph"],
        },
        "compilation": {
            "confirmation_status": request["confirmation"]["status"],
            "confirmation_method": request["confirmation"]["confirmation_method"],
            "confirmation_ref": request["confirmation"]["confirmation_ref"],
            "legacy_phrase": request["confirmation"]["legacy_phrase"],
            "vi_schema_version": contract["schema_version"],
            "vi_contract_sha256": request["confirmation"]["vi_contract_sha256"],
            **(
                {
                    "reference_images_sha256": request["confirmation"][
                        "reference_images_sha256"
                    ]
                }
                if is_family
                else {
                    "reference_image_sha256": request["confirmation"][
                        "reference_image_sha256"
                    ]
                }
            ),
            "boundary_summary": counts,
            "customer_corrections": request["customer_corrections"],
        },
        "template_contract": {
            "placeholder_format": "{{UPPER_SNAKE_CASE}}",
            "minimum_slides": 5,
            "required_markers": ["data-layout", "fragment", "data-step"],
        },
    }
    if corporate_shell is not None:
        manifest["corporate_shell"] = {
            "source_image_sha256": request["confirmation"]["reference_image_sha256"],
            "source_image_size": [
                contract["source_image"]["width"],
                contract["source_image"]["height"],
            ],
            "editable_region": contract["editable_regions"][0],
            "fixed_elements": [
                {
                    "id": region["id"],
                    "type": region["type"],
                    "bbox": region["bbox"],
                    "pixel_bbox": region["pixel_bbox"],
                    "status": region["status"],
                    "basis": region["basis"],
                    "extraction": region["extraction"],
                    "crop_sha256": region["sha256"],
                    "crop_size": [region["width"], region["height"]],
                }
                for region in extracted_regions
            ],
            "extension_pages": contract["extension_pages"],
            "limitations": contract["limitations"],
            "fixed_motion": "none",
            "content_motion_scope": "editable_region_only",
            "full_screenshot_background": False,
            "logo_redraw": False,
        }
        manifest["motion"]["fixed_elements"] = "none"
        manifest["motion"]["scope"] = "editable_region_only"
    if corporate_family is not None:
        bindings = render_reference_vi.validate_source_bindings(contract, reference_paths)
        manifest["corporate_template_family"] = {
            "reference_pages": [
                {
                    **page,
                    "canvas_pixel_bbox": binding["canvas_pixel_bbox"],
                    "canvas_size": binding["canvas_size"],
                }
                for page, binding in zip(
                    contract["reference_pages"], bindings, strict=True
                )
            ],
            "shared_assets": [
                {
                    "id": asset["id"],
                    "type": asset["type"],
                    "source_page_id": asset["source_page_id"],
                    "source_image_sha256": asset["source_image_sha256"],
                    "source_bbox": asset["source_bbox"],
                    "source_pixel_bbox": asset["source_pixel_bbox"],
                    "source_crop_sha256": asset["source_crop_sha256"],
                    "replaceable_regions": asset["replaceable_regions"],
                    "status": asset["status"],
                    "basis": asset["basis"],
                    "extraction": asset["extraction"],
                    "crop_sha256": asset["sha256"],
                    "crop_size": [asset["width"], asset["height"]],
                }
                for asset in extracted_assets
            ],
            "replaceable_regions": corporate_family["replaceable_regions"],
            "shell_variants": [
                {
                    "role": shell["role"],
                    "status": shell["status"],
                    "reference_page_id": shell["reference_page_id"],
                    "fixed_regions": shell["fixed_regions"],
                    "editable_region": shell["editable_region"],
                    "basis": shell["basis"],
                }
                for shell in corporate_family["shells"].values()
            ],
            "shared_brand_grammar": corporate_family["shared_brand_grammar"],
            "extension_pages": corporate_family["extension_pages"],
            "limitations": corporate_family["limitations"],
        }
        manifest["motion"]["fixed_elements"] = "none"
        manifest["motion"]["scope"] = "editable_regions_only"
    provenance = {
        "schema_version": THEME_SCHEMA_VERSION,
        "theme_id": theme_id,
        "confirmed_inputs": {
            "vi_contract": vi_path.name,
            "vi_contract_sha256": _sha256(vi_path),
            **(
                {
                    "reference_images": [path.name for path in reference_paths],
                    "reference_images_sha256": [
                        _sha256(path) for path in reference_paths
                    ],
                }
                if is_family
                else {
                    "reference_image": reference_paths[0].name,
                    "reference_image_sha256": _sha256(reference_paths[0]),
                }
            ),
            "confirmation_status": request["confirmation"]["status"],
            "confirmation_method": request["confirmation"]["confirmation_method"],
            "confirmation_ref": request["confirmation"]["confirmation_ref"],
            "legacy_phrase": request["confirmation"]["legacy_phrase"],
            "target_mode": request["target_mode"],
            "customer_corrections": request["customer_corrections"],
            "reference_mode": reference_mode,
        },
        "boundary_policy": {
            "eligible": "observed or extension may compile, but eligibility alone never sets compiled true",
            "compiled": "true only when concrete usage targets are recorded",
            "observed": "eligible for direct deterministic compilation when used",
            "extension": "eligible only as a labeled report adaptation when used",
            "unknown": "retained with compiled false; a needed default is a separate fallback record",
            "fallback": "neutral reversible compiler default, never reference evidence",
        },
        "boundary_records": boundaries,
        "fallback_records": fallback_records,
        "motion_boundary": manifest["motion"],
    }
    if corporate_shell is not None:
        provenance["corporate_fidelity"] = manifest["corporate_shell"]
    if corporate_family is not None:
        provenance["corporate_fidelity"] = manifest["corporate_template_family"]
    corporate_css_contract = corporate_family or corporate_shell
    css = _css(theme_id, tokens, plan, corporate_css_contract).strip() + "\n"
    templates = (
        _family_templates(plan, variants, evidence_sample, corporate_family)
        if corporate_family is not None
        else _templates(plan, variants, evidence_sample, corporate_shell)
    ).strip() + "\n"
    for text, label in ((css, "theme.css"), (templates, "templates.html")):
        if REMOTE_ASSET.search(text):
            raise ValueError(f"Compiled {label} contains a remote asset reference.")

    supplied_output = output_theme.expanduser()
    if supplied_output.is_symlink():
        raise ValueError(f"Output theme directory must not be a symlink: {supplied_output}")
    output = supplied_output.resolve()
    if output.exists() and not output.is_dir():
        raise ValueError(f"Output theme path is not a directory: {output}")
    if output.exists():
        actual = {entry.name for entry in output.iterdir()}
        extra = actual - OUTPUT_FILES
        if extra:
            raise ValueError(f"Output theme directory contains unexpected files: {', '.join(sorted(extra))}")
        if any(entry.is_symlink() or not entry.is_file() for entry in output.iterdir()):
            raise ValueError(f"Output theme directory must contain regular files only: {output}")
    output.mkdir(parents=True, exist_ok=True)
    payloads = {
        "theme.json": _json_text(manifest),
        "theme.css": css,
        "templates.html": templates,
        "provenance.json": _json_text(provenance),
    }
    for filename, payload in payloads.items():
        target = output / filename
        target.write_text(payload, encoding="utf-8")
    return output


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Compile a machine-confirmed single-reference VI handoff into a deterministic project theme."
    )
    parser.add_argument("--request", type=Path, required=True, help="Confirmed VI handoff JSON.")
    parser.add_argument("--output-theme", type=Path, required=True, help="Project theme output directory.")
    args = parser.parse_args()
    try:
        output = compile_theme(args.request, args.output_theme)
    except (OSError, ValueError) as exc:
        print(f"PROJECT_THEME_COMPILE_FAILED: {exc}", file=sys.stderr)
        return 1
    print(f"PROJECT_THEME_COMPILE_OK {output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
