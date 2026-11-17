#!/usr/bin/env python3
"""Compile validated TaoHtml Report IR v1 into deterministic offline HTML."""

from __future__ import annotations

import argparse
import copy
import html
import json
import math
import re
import sys
import unicodedata
from pathlib import Path
from typing import Any, Iterable


SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from render_visual_system import (  # noqa: E402
    CONTROLLED_STEP_CONTRACT,
    END_MARKER,
    SHELL_PATH,
    START_MARKER,
    inline_editor_assets,
    local_image_data_uri,
)
from report_ir_core import (  # noqa: E402
    canonical_bytes,
    load_json,
    sha256_bytes,
    sha256_file,
    validate_ir,
    workflow_profile_record,
    write_json,
)
from theme_runtime import load_built_in_theme, load_project_theme  # noqa: E402


COMPILER_VERSION = "0.2.0-dev"
RUNTIME_BUNDLE_VERSION = "fragment-v1+editor-v1+ir-patch-v1"
SKILL_ROOT = SCRIPT_DIR.parent
REPORT_IR_ASSET_ROOT = SKILL_ROOT / "assets" / "report-ir"
REPORT_IR_STYLE_PATH = REPORT_IR_ASSET_ROOT / "report-ir.css"
THEME_PROFILES_PATH = REPORT_IR_ASSET_ROOT / "theme-profiles.json"
RUNTIME_PATCH_SCHEMA_PATH = (
    SKILL_ROOT / "references" / "report-ir-runtime-patch.schema.json"
)
STANDARD_LAYOUT_BY_FORM = {
    "poster": "hero",
    "closing": "hero",
    "section": "hero",
    "data": "evidence",
    "evidence": "evidence",
    "source": "evidence",
    "process": "sequence",
    "timeline": "sequence",
    "comparison": "comparison",
    "matrix": "comparison",
    "toc": "grid",
    "framework": "grid",
    "case": "grid",
    "content": "grid",
}
SUPPORTED_LAYOUTS = {"hero", "grid", "sequence", "evidence", "comparison"}
RASTER_OR_VECTOR_IMAGE = {".png", ".jpg", ".jpeg", ".webp", ".svg"}
PROJECT_SHELL_ROLES = ("cover", "toc", "section", "content", "data")
ADAPTIVE_ITEM_KINDS = {"list", "process", "comparison", "timeline"}
MIN_LAYOUT_VIEWPORT_WIDTH = 1366
BUILT_IN_SAFE_CONTENT_WIDTH = 1240
PROJECT_THEME_FALLBACK_CONTENT_WIDTH = 640
CORPORATE_EDITABLE_HORIZONTAL_PADDING = 36
CONTENT_COLUMN_GAP = 18
BLOCK_HORIZONTAL_PADDING = 48
MIN_READABLE_ITEM_COLUMN = 240
MAX_SAFE_TITLE_UNITS = 150
MAX_SAFE_ITEM_UNITS = 240
MAX_SAFE_PAGE_UNITS = 1600


class CompileError(RuntimeError):
    """Raised when a compiler boundary cannot be satisfied safely."""


def _semantic_graph_sha256(ir: dict[str, Any]) -> str:
    """Hash theme-independent report meaning and delivery intent once."""
    semantic_keys = (
        "report",
        "projection",
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
        "traceability",
        "extensions",
    )
    return sha256_bytes(canonical_bytes({key: ir[key] for key in semantic_keys}))


def _escape(value: object, *, quote: bool = True) -> str:
    return html.escape(str(value), quote=quote)


def _edit_attributes(
    kind: str,
    entity: str,
    identity: str,
    field: str,
) -> str:
    key = f"{entity}:{identity}:{field}"
    return (
        f'data-ir-edit-kind="{_escape(kind)}" '
        f'data-ir-edit-entity="{_escape(entity)}" '
        f'data-ir-edit-id="{_escape(identity)}" '
        f'data-ir-edit-field="{_escape(field)}" '
        f'data-ir-edit-key="{_escape(key)}"'
    )


def _index(records: Iterable[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    return {record["id"]: record for record in records}


def _load_theme_profiles() -> dict[str, dict[str, Any]]:
    raw = load_json(THEME_PROFILES_PATH)
    if raw.get("schema_version") != "1.0" or not isinstance(raw.get("themes"), dict):
        raise CompileError("Report IR theme profiles must declare schema_version 1.0")
    profiles = raw["themes"]
    for theme_id, profile in profiles.items():
        if not isinstance(profile, dict):
            raise CompileError(f"Theme profile {theme_id} must be an object")
        variants = profile.get("layout_variants")
        if not isinstance(variants, dict) or set(variants) != SUPPORTED_LAYOUTS:
            raise CompileError(
                f"Theme profile {theme_id} must map every generic layout family"
            )
        transitions = profile.get("supported_transition_intents")
        if not isinstance(transitions, list) or not all(
            isinstance(item, str) for item in transitions
        ):
            raise CompileError(
                f"Theme profile {theme_id} has an invalid transition capability list"
            )
    return profiles


def _project_theme_profile(theme: Any) -> dict[str, Any]:
    """Create a deterministic generic-layout bridge for a validated project theme."""
    variants = theme.manifest.get("layout_variants", [])
    variant_ids = [
        item.get("id")
        for item in variants
        if isinstance(item, dict) and isinstance(item.get("id"), str)
    ]
    if not variant_ids:
        raise CompileError(f"Project theme has no layout variants: {theme.theme_id}")
    role_variants = {
        item.get("role"): item.get("id")
        for item in variants
        if isinstance(item, dict)
        and item.get("role") in PROJECT_SHELL_ROLES
        and isinstance(item.get("id"), str)
    }
    fallback = role_variants.get("content", variant_ids[0])
    content_width_by_role = _project_theme_content_widths(theme.manifest)
    return {
        "display_name": theme.display_name,
        "profile_version": "project-theme-1.0",
        "layout_variants": {
            "hero": role_variants.get("cover", fallback),
            "grid": role_variants.get("content", fallback),
            "sequence": role_variants.get("content", fallback),
            "evidence": role_variants.get("data", fallback),
            "comparison": role_variants.get("content", fallback),
        },
        "supported_transition_intents": ["initial", "reveal", "final"],
        "content_width_by_role": content_width_by_role,
    }


def _normalized_editable_width(editable: object) -> float | None:
    if not isinstance(editable, dict):
        return None
    bbox = editable.get("bbox")
    if (
        not isinstance(bbox, list)
        or len(bbox) != 4
        or isinstance(bbox[2], bool)
        or not isinstance(bbox[2], (int, float))
        or not 0 < float(bbox[2]) <= 1
    ):
        return None
    return max(
        MIN_READABLE_ITEM_COLUMN,
        MIN_LAYOUT_VIEWPORT_WIDTH * float(bbox[2])
        - CORPORATE_EDITABLE_HORIZONTAL_PADDING,
    )


def _project_theme_content_widths(manifest: dict[str, Any]) -> dict[str, float]:
    family = manifest.get("corporate_template_family")
    if isinstance(family, dict):
        widths = {
            str(shell["role"]): width
            for shell in family.get("shell_variants", [])
            if isinstance(shell, dict)
            and isinstance(shell.get("role"), str)
            and (width := _normalized_editable_width(shell.get("editable_region")))
            is not None
        }
        if set(widths) == set(PROJECT_SHELL_ROLES):
            return {**widths, "default": min(widths.values())}

    corporate = manifest.get("corporate_shell")
    if isinstance(corporate, dict):
        width = _normalized_editable_width(corporate.get("editable_region"))
        if width is not None:
            return {role: width for role in (*PROJECT_SHELL_ROLES, "default")}

    tokens = manifest.get("tokens", {})
    canvas_x = tokens.get("canvas_x") if isinstance(tokens, dict) else None
    match = re.fullmatch(r"\s*(\d+(?:\.\d+)?)px\s*", str(canvas_x))
    if match is not None:
        width = MIN_LAYOUT_VIEWPORT_WIDTH - 2 * float(match.group(1))
        return {"default": max(PROJECT_THEME_FALLBACK_CONTENT_WIDTH, width)}
    return {"default": PROJECT_THEME_FALLBACK_CONTENT_WIDTH}


def _class_tokens(opening_tag: str) -> list[str]:
    match = re.search(r'\bclass="([^"]*)"', opening_tag)
    if match is None:
        raise CompileError("Project theme page section is missing a class attribute")
    return match.group(1).split()


def _replace_class_tokens(opening_tag: str, tokens: list[str]) -> str:
    return re.sub(
        r'\bclass="[^"]*"',
        f'class="{_escape(" ".join(tokens))}"',
        opening_tag,
        count=1,
    )


def _replace_or_add_attribute(opening_tag: str, name: str, value: str) -> str:
    replacement = f'{name}="{_escape(value)}"'
    pattern = rf'\b{re.escape(name)}="[^"]*"'
    if re.search(pattern, opening_tag):
        return re.sub(pattern, replacement, opening_tag, count=1)
    return opening_tag[:-1] + f" {replacement}>"


def _find_div_content_bounds(document: str, required_class: str) -> tuple[int, int, int, int]:
    opening_start = opening_end = -1
    for match in re.finditer(r"<div\b[^>]*>", document, flags=re.IGNORECASE | re.DOTALL):
        try:
            classes = _class_tokens(match.group(0))
        except CompileError:
            continue
        if required_class in classes:
            if opening_start >= 0:
                raise CompileError(f"Project shell contains multiple .{required_class} regions")
            opening_start, opening_end = match.start(), match.end()
    if opening_start < 0:
        raise CompileError(f"Project shell is missing .{required_class}")
    depth = 1
    for match in re.finditer(
        r"</?div\b[^>]*>", document[opening_end:], flags=re.IGNORECASE | re.DOTALL
    ):
        token = match.group(0)
        if token.startswith("</"):
            depth -= 1
        elif not token.rstrip().endswith("/>"):
            depth += 1
        if depth == 0:
            closing_start = opening_end + match.start()
            closing_end = opening_end + match.end()
            return opening_start, opening_end, closing_start, closing_end
    raise CompileError(f"Project shell .{required_class} region is not closed")


def _project_sections_by_role(templates: str) -> dict[str, str]:
    sections: dict[str, str] = {}
    for match in re.finditer(
        r"<section\b[^>]*>.*?</section>", templates, flags=re.IGNORECASE | re.DOTALL
    ):
        section = match.group(0)
        opening = section[: section.index(">") + 1]
        role_match = re.search(r'\bdata-shell-role="([^"]+)"', opening)
        if role_match is None:
            continue
        role = role_match.group(1)
        if role in sections:
            raise CompileError(f"Project theme repeats corporate shell role: {role}")
        sections[role] = section
    if set(sections) != set(PROJECT_SHELL_ROLES):
        raise CompileError("Corporate project theme must expose all five shell roles")
    return sections


def _generic_page_parts(section: str) -> tuple[str, str, list[str], dict[str, str]]:
    opening = section[: section.index(">") + 1]
    shell_start, _, _, shell_end = _find_div_content_bounds(section, "ri-page-shell")
    title_match = re.search(r'\bdata-title="([^"]*)"', opening)
    if title_match is None:
        raise CompileError("Generated Report IR page is missing data-title")
    attributes = {
        name: match.group(1)
        for name in ("data-ir-page-id", "data-ir-derived-page-id", "data-ir-appendix-ref", "data-ir-role", "data-ir-form")
        if (match := re.search(rf'\b{name}="([^"]*)"', opening)) is not None
    }
    classes = [
        token
        for token in _class_tokens(opening)
        if token.startswith(
            ("ri-layout-", "ri-block-count-", "ri-density-", "ri-arrangement-")
        )
    ]
    return html.unescape(title_match.group(1)), section[shell_start:shell_end], classes, attributes


def _route_project_shell_role(page: dict[str, Any] | None, output_index: int) -> str:
    if page is None:
        return "content"
    form = page["form"]
    if output_index == 0 or form == "poster":
        return "cover"
    if form == "toc":
        return "toc"
    if form == "section":
        return "section"
    if form in {"data", "evidence", "source"}:
        return "data"
    return "content"


class CorporateShellRenderer:
    """Clone validated shell variants without changing protected shell descendants."""

    def __init__(self, theme: Any) -> None:
        self.theme = theme
        self.sections = _project_sections_by_role(theme.templates)
        self.variant_by_role = {
            item["role"]: item["id"]
            for item in theme.manifest["layout_variants"]
            if item.get("role") in PROJECT_SHELL_ROLES
        }

    def wrap(
        self,
        generic_section: str,
        *,
        page: dict[str, Any] | None,
        output_index: int,
    ) -> tuple[str, str, str]:
        role = _route_project_shell_role(page, output_index)
        template = self.sections[role]
        title, page_shell, report_classes, report_attributes = _generic_page_parts(
            generic_section
        )
        _, editable_open_end, editable_close_start, _ = _find_div_content_bounds(
            template, "pt-corporate-editable"
        )
        rendered = template[:editable_open_end] + page_shell + template[editable_close_start:]
        opening_end = rendered.index(">") + 1
        opening = rendered[:opening_end]
        classes = [token for token in _class_tokens(opening) if token != "active"]
        classes.extend(token for token in report_classes if token not in classes)
        classes.append("ri-corporate-page")
        if output_index == 0:
            classes.append("active")
        opening = _replace_class_tokens(opening, classes)
        opening = _replace_or_add_attribute(opening, "data-title", title)
        opening = _replace_or_add_attribute(opening, "data-ir-shell-role", role)
        for name, value in report_attributes.items():
            opening = _replace_or_add_attribute(opening, name, value)
        rendered = opening + rendered[opening_end:]
        rendered, removed = re.subn(
            r'<span class="ri-page-number" data-taohtml-edit-lock>[^<]*</span>',
            "",
            rendered,
            count=1,
        )
        if removed != 1:
            raise CompileError(
                "Corporate Report IR shell requires exactly one derived page-number field"
            )
        return rendered, role, self.variant_by_role[role]


def _resolve_project_path(root: Path, value: str, label: str) -> Path:
    candidate = root.joinpath(*value.split("/"))
    try:
        resolved = candidate.resolve(strict=True)
        resolved.relative_to(root)
    except (OSError, ValueError) as exc:
        raise CompileError(f"{label} is unavailable or escapes the artifact root") from exc
    if not resolved.is_file() or resolved.is_symlink():
        raise CompileError(f"{label} must resolve to a regular non-symlink file")
    return resolved


def _format_number(value: float) -> str:
    if math.isfinite(value) and value.is_integer():
        return f"{int(value):,}"
    return f"{value:,.2f}".rstrip("0").rstrip(".")


def _text_units(value: object) -> float:
    """Approximate rendered em width without assuming a particular language."""
    units = 0.0
    for character in str(value):
        if character.isspace():
            units += 0.35
        elif unicodedata.east_asian_width(character) in {"W", "F"}:
            units += 1.0
        elif character.isalnum():
            units += 0.58
        else:
            units += 0.7
    return units


def _item_units(item: dict[str, Any]) -> tuple[float, float]:
    segments = [
        _text_units(item[field])
        for field in ("label", "value", "detail")
        if field in item
    ]
    return sum(segments), max(segments, default=0.0)


def _block_units(block: dict[str, Any]) -> float:
    total = sum(_text_units(block.get(field, "")) for field in ("text", "caption"))
    for item in block.get("items", []):
        total += _item_units(item)[0]
    return total


def _motion_plan(
    page: dict[str, Any],
    supported_transition_intents: set[str],
) -> tuple[dict[str, dict[str, str]], list[str]]:
    """Map semantic states to the existing monotonic Runtime step contract."""
    states = page.get("state_sequence", [])
    if not states:
        return {}, []
    first_visible: dict[str, int] = {}
    prior_visible: set[str] = set()
    warnings: list[str] = []
    for state_index, state in enumerate(states):
        visible = set(state["visible_refs"])
        hidden_again = prior_visible - visible
        if hidden_again:
            raise CompileError(
                f"page.{page['id']} uses non-monotonic visibility not supported by "
                f"{CONTROLLED_STEP_CONTRACT}: {', '.join(sorted(hidden_again))}"
            )
        for block_ref in visible:
            first_visible.setdefault(block_ref, state_index)
        prior_visible = visible
        if state["transition_intent"] not in supported_transition_intents:
            warnings.append(
                f"page.{page['id']}.state.{state['id']} transition_intent="
                f"{state['transition_intent']} is compiled as a monotonic reveal"
            )
    plan: dict[str, dict[str, str]] = {}
    for block_ref in page["block_refs"]:
        first_index = first_visible.get(block_ref)
        if first_index is None:
            raise CompileError(
                f"page.{page['id']} final state does not expose block {block_ref}"
            )
        state = states[first_index]
        metadata = {
            "state_id": state["id"],
            "transition_intent": state["transition_intent"],
        }
        if first_index > 0:
            metadata["step"] = str(first_index)
        plan[block_ref] = metadata
    return plan, warnings


def _motion_attributes(
    block_id: str,
    plan: dict[str, dict[str, str]],
    emphasized_refs: set[str],
) -> tuple[str, str]:
    metadata = plan.get(block_id, {})
    classes: list[str] = []
    attributes = [f'data-ir-block-id="{_escape(block_id)}"']
    if "step" in metadata:
        classes.append("fragment")
        attributes.append(f'data-step="{metadata["step"]}"')
    if block_id in emphasized_refs:
        classes.append("ri-emphasis")
    if "state_id" in metadata:
        attributes.append(f'data-ir-first-state="{_escape(metadata["state_id"])}"')
        attributes.append(
            f'data-ir-transition-intent="{_escape(metadata["transition_intent"])}"'
        )
    return " ".join(classes), " ".join(attributes)


class ReportRenderer:
    def __init__(
        self,
        ir: dict[str, Any],
        artifact_root: Path,
        theme_profile: dict[str, Any],
    ) -> None:
        self.ir = ir
        self.artifact_root = artifact_root
        self.theme_profile = theme_profile
        self.chapters = _index(ir["chapters"])
        self.units = _index(ir["narrative_units"])
        self.blocks = _index(ir["blocks"])
        self.claims = _index(ir["claims"])
        self.evidence = _index(ir["evidence"])
        self.sources = _index(ir["sources"])
        self.datasets = _index(ir["datasets"])
        self.assets = _index(ir["assets"])
        self.pages = _index(ir["pages"])
        self.links_by_claim: dict[str, list[dict[str, Any]]] = {
            claim_id: [] for claim_id in self.claims
        }
        for link in ir["evidence_links"]:
            self.links_by_claim.setdefault(link["claim_ref"], []).append(link)
        self.notes_by_page: dict[str, list[dict[str, Any]]] = {}
        for note in ir["speaker_notes"]:
            self.notes_by_page.setdefault(note["page_ref"], []).append(note)
        self.warnings: list[str] = []
        self.source_map_pages: dict[str, Any] = {}

    def _resolved_form(self, page: dict[str, Any]) -> str:
        form = page["form"]
        if form not in STANDARD_LAYOUT_BY_FORM:
            form = page["visual_intent"].get("fallback_form", "content")
        return form

    def _layout(self, page: dict[str, Any]) -> tuple[str, str]:
        form = self._resolved_form(page)
        layout = STANDARD_LAYOUT_BY_FORM.get(form, "grid")
        return layout, self.theme_profile["layout_variants"][layout]

    def _base_block_columns(self, layout: str, block_count: int) -> int:
        if block_count <= 1 or layout == "hero":
            return 1
        if layout == "sequence":
            return block_count
        if layout == "evidence":
            return 2
        if layout == "grid" and block_count in {3, 5, 6}:
            return 3
        return 2

    def _content_width(self, page: dict[str, Any], output_index: int) -> float:
        widths = self.theme_profile.get("content_width_by_role", {})
        if not isinstance(widths, dict):
            return PROJECT_THEME_FALLBACK_CONTENT_WIDTH
        role = _route_project_shell_role(page, output_index)
        raw = widths.get(role, widths.get("default"))
        if isinstance(raw, bool) or not isinstance(raw, (int, float)) or raw <= 0:
            return PROJECT_THEME_FALLBACK_CONTENT_WIDTH
        return float(raw)

    def _item_column_count(
        self,
        block: dict[str, Any],
        *,
        parent_width: float,
    ) -> int:
        items = block.get("items", [])
        if not items:
            return 1
        footprints = [_item_units(item) for item in items]
        maximum_total = max((total for total, _ in footprints), default=0.0)
        maximum_segment = max((segment for _, segment in footprints), default=0.0)
        if maximum_total > MAX_SAFE_ITEM_UNITS:
            raise CompileError(
                f"block.{block['id']} exceeds the safe item layout budget "
                f"({maximum_total:.1f} > {MAX_SAFE_ITEM_UNITS} text units)"
            )
        if maximum_total > 60 or maximum_segment > 42:
            minimum_width = 520
        elif maximum_total > 32 or maximum_segment > 20:
            minimum_width = 390
        elif maximum_total > 20 or maximum_segment > 14:
            minimum_width = 310
        else:
            minimum_width = MIN_READABLE_ITEM_COLUMN
        available = max(MIN_READABLE_ITEM_COLUMN, parent_width - BLOCK_HORIZONTAL_PADDING)
        possible = max(
            1,
            math.floor(
                (available + CONTENT_COLUMN_GAP)
                / (minimum_width + CONTENT_COLUMN_GAP)
            ),
        )
        return min(len(items), 4, possible)

    def _layout_plan(
        self,
        page: dict[str, Any],
        *,
        title_text: str,
        subtitle_text: str,
        body_refs: list[str],
        layout: str,
        output_index: int,
    ) -> dict[str, Any]:
        blocks = [self.blocks[ref] for ref in body_refs]
        title_units = _text_units(title_text)
        page_units = title_units + _text_units(subtitle_text) + sum(
            _block_units(block) for block in blocks
        )
        if title_units > MAX_SAFE_TITLE_UNITS:
            raise CompileError(
                f"page.{page['id']} title exceeds the safe fixed-canvas layout budget "
                f"({title_units:.1f} > {MAX_SAFE_TITLE_UNITS} text units)"
            )
        if page_units > MAX_SAFE_PAGE_UNITS:
            raise CompileError(
                f"page.{page['id']} exceeds the safe fixed-canvas layout budget "
                f"({page_units:.1f} > {MAX_SAFE_PAGE_UNITS} text units)"
            )

        adaptive_blocks = [
            block
            for block in blocks
            if block["kind"] in ADAPTIVE_ITEM_KINDS
            and 3 <= len(block.get("items", [])) <= 4
        ]
        dense_adaptive_ids = {
            block["id"]
            for block in adaptive_blocks
            if max((_item_units(item)[0] for item in block["items"]), default=0) > 32
        }
        content_width = self._content_width(page, output_index)
        base_columns = self._base_block_columns(layout, len(blocks))
        default_parent_width = (
            content_width
            if base_columns == 1
            else (content_width - (base_columns - 1) * CONTENT_COLUMN_GAP)
            / base_columns
        )
        default_item_columns = {
            block["id"]: self._item_column_count(
                block,
                parent_width=default_parent_width,
            )
            for block in adaptive_blocks
        }
        full_width_item_columns = {
            block["id"]: self._item_column_count(
                block,
                parent_width=content_width,
            )
            for block in adaptive_blocks
        }
        wide_item_ids = {
            block["id"]
            for block in adaptive_blocks
            if len(blocks) > 1
            and (
                block["id"] in dense_adaptive_ids
                or full_width_item_columns[block["id"]]
                > default_item_columns[block["id"]]
            )
        }
        item_columns: dict[str, int] = {}
        for block in adaptive_blocks:
            item_columns[block["id"]] = (
                full_width_item_columns[block["id"]]
                if block["id"] in wide_item_ids
                else default_item_columns[block["id"]]
            )

        if title_units > 72 or page_units > 760:
            density = "compact"
        elif title_units > 46 or page_units > 430:
            density = "dense"
        else:
            density = "standard"
        arrangement = "wide-items" if wide_item_ids else "standard"
        return {
            "density": density,
            "arrangement": arrangement,
            "item_columns": item_columns,
            "wide_item_ids": wide_item_ids,
            "title_units": round(title_units, 2),
            "page_units": round(page_units, 2),
            "content_width": round(content_width, 2),
            "minimum_readable_item_column": MIN_READABLE_ITEM_COLUMN,
        }

    def _source_ids_for_claim(self, claim_ref: str) -> set[str]:
        result: set[str] = set()
        for link in self.links_by_claim.get(claim_ref, []):
            evidence = self.evidence.get(link["evidence_ref"])
            if evidence is None:
                continue
            result.update(evidence["source_refs"])
            for dataset_ref in evidence["dataset_refs"]:
                dataset = self.datasets.get(dataset_ref)
                if dataset is not None:
                    result.update(dataset["source_refs"])
        return result

    def _source_ids_for_block(self, block: dict[str, Any]) -> set[str]:
        result: set[str] = set()
        for claim_ref in block["claim_refs"]:
            result.update(self._source_ids_for_claim(claim_ref))
        for evidence_ref in block["evidence_refs"]:
            evidence = self.evidence.get(evidence_ref)
            if evidence is None:
                continue
            result.update(evidence["source_refs"])
            for dataset_ref in evidence["dataset_refs"]:
                dataset = self.datasets.get(dataset_ref)
                if dataset is not None:
                    result.update(dataset["source_refs"])
        dataset_ref = block.get("dataset_ref")
        if dataset_ref in self.datasets:
            result.update(self.datasets[dataset_ref]["source_refs"])
        asset_ref = block.get("asset_ref")
        if asset_ref in self.assets and "source_ref" in self.assets[asset_ref]:
            result.add(self.assets[asset_ref]["source_ref"])
        for item in block.get("items", []):
            for claim_ref in item["claim_refs"]:
                result.update(self._source_ids_for_claim(claim_ref))
            for evidence_ref in item["evidence_refs"]:
                evidence = self.evidence.get(evidence_ref)
                if evidence is not None:
                    result.update(evidence["source_refs"])
        return result

    def _page_source_ids(self, page: dict[str, Any]) -> list[str]:
        result: set[str] = set()
        for block_ref in page["block_refs"]:
            result.update(self._source_ids_for_block(self.blocks[block_ref]))
        for unit_ref in page["narrative_unit_refs"]:
            for claim_ref in self.units[unit_ref]["claim_refs"]:
                result.update(self._source_ids_for_claim(claim_ref))
        return sorted(result)

    def _source_line(self, source_ids: list[str]) -> str:
        values: list[str] = []
        for source_id in source_ids:
            source = self.sources[source_id]
            locator = source["locator"]
            label = source.get("title", source_id)
            publisher = f" · {source['publisher']}" if "publisher" in source else ""
            published = f" · {source['published_date']}" if "published_date" in source else ""
            page_locator = f" · {source['page_locator']}" if "page_locator" in source else ""
            values.append(
                f"{label}{publisher}{published}{page_locator} · {locator['value']}"
            )
        return "；".join(values)

    def _render_items(self, block: dict[str, Any], columns: int | None = None) -> str:
        items: list[str] = []
        for index, item in enumerate(block["items"], start=1):
            value = (
                f'<span class="ri-item-value" '
                f'{_edit_attributes("text", "block", block["id"], f"items.{item["id"]}.value")}'
                f' data-taohtml-edit="text">{_escape(item["value"])}</span>'
                if "value" in item
                else ""
            )
            detail = (
                f'<p class="ri-item-detail" '
                f'{_edit_attributes("text", "block", block["id"], f"items.{item["id"]}.detail")} '
                f'data-taohtml-edit="text">'
                f'{_escape(item["detail"])}</p>'
                if "detail" in item
                else ""
            )
            items.append(
                f'<li class="ri-item" data-ir-item-id="{_escape(item["id"])}">'
                f'<span class="ri-item-index" data-taohtml-edit-lock>{index:02d}</span>'
                f'<span class="ri-item-label" '
                f'{_edit_attributes("text", "block", block["id"], f"items.{item["id"]}.label")} '
                f'data-taohtml-edit="text">'
                f'{_escape(item["label"])}</span>{value}{detail}</li>'
            )
        column_class = f" ri-item-columns-{columns}" if columns is not None else ""
        return f'<ol class="ri-items{column_class}">{"".join(items)}</ol>'

    def _render_metrics(self, block: dict[str, Any]) -> str:
        if "items" not in block:
            return (
                f'<p class="ri-claim-statement" '
                f'{_edit_attributes("text", "block", block["id"], "text")} '
                f'data-taohtml-edit="text">{_escape(block["text"])}</p>'
            )
        metrics = []
        for item in block["items"]:
            metrics.append(
                f'<div class="ri-metric" data-ir-item-id="{_escape(item["id"])}">'
                f'<strong class="ri-metric-value" '
                f'{_edit_attributes("text", "block", block["id"], f"items.{item["id"]}.value")} '
                f'data-taohtml-edit="text">'
                f'{_escape(item.get("value", "—"))}</strong>'
                f'<span class="ri-metric-label" '
                f'{_edit_attributes("text", "block", block["id"], f"items.{item["id"]}.label")} '
                f'data-taohtml-edit="text">'
                f'{_escape(item["label"])}</span></div>'
            )
        return f'<div class="ri-metrics">{"".join(metrics)}</div>'

    def _render_chart(self, block: dict[str, Any]) -> str:
        dataset = self.datasets[block["dataset_ref"]]
        records = dataset.get("records", [])
        maximum = max((abs(float(record["value"])) for record in records), default=1.0)
        if maximum == 0:
            maximum = 1.0
        rows: list[str] = []
        for record in records:
            value = float(record["value"])
            width = max(0.0, min(100.0, abs(value) / maximum * 100.0))
            negative = " negative" if value < 0 else ""
            rows.append(
                f'<div class="ri-bar-row" data-ir-record-id="{_escape(record["id"])}">'
                f'<span class="ri-bar-label" data-taohtml-edit="text">{_escape(record["label"])}</span>'
                f'<span class="ri-bar-track"><span class="ri-bar{negative}" '
                f'style="--ri-bar:{width:.4f}%"></span></span>'
                f'<strong class="ri-bar-value" data-taohtml-edit="text">'
                f'{_escape(_format_number(value))} {_escape(dataset["unit"])}</strong></div>'
            )
        meta = " · ".join(
            value
            for value in (
                dataset.get("time_range", ""),
                dataset.get("geography", ""),
                dataset["method"],
            )
            if value
        )
        chart = (
            '<div class="ri-chart" data-taohtml-edit-lock>'
            f'<h3 class="ri-chart-title">{_escape(dataset["title"])}</h3>'
            f'{"".join(rows)}'
            f'<p class="ri-chart-meta">{_escape(meta)}</p>'
            '</div>'
        )
        caption = block.get("caption", "")
        if not caption:
            return chart
        return (
            chart
            + f'<p class="ri-chart-caption" '
            f'{_edit_attributes("text", "block", block["id"], "caption")} '
            f'data-taohtml-edit="text">{_escape(caption)}</p>'
        )

    def _render_table(self, block: dict[str, Any]) -> str:
        rows: list[str] = []
        if "dataset_ref" in block:
            dataset = self.datasets[block["dataset_ref"]]
            for record in dataset.get("records", []):
                rows.append(
                    f'<tr data-ir-record-id="{_escape(record["id"])}">'
                    f'<td data-taohtml-edit="text">{_escape(record["label"])}</td>'
                    f'<td data-taohtml-edit="text">{_escape(_format_number(float(record["value"])))} '
                    f'{_escape(dataset["unit"])}</td></tr>'
                )
            caption = dataset["title"]
        else:
            for item in block["items"]:
                rows.append(
                    f'<tr data-ir-item-id="{_escape(item["id"])}">'
                    f'<td data-taohtml-edit="text">{_escape(item["label"])}</td>'
                    f'<td data-taohtml-edit="text">{_escape(item.get("value", item.get("detail", "")))}</td></tr>'
                )
            caption = block.get("caption", "数据表")
        return (
            f'<table class="ri-table" data-taohtml-edit-lock><caption class="ri-chart-title">'
            f'{_escape(caption)}</caption>'
            '<thead><tr><th>项目</th><th>值</th></tr></thead>'
            f'<tbody>{"".join(rows)}</tbody></table>'
        )

    def _render_image(self, block: dict[str, Any]) -> str:
        asset = self.assets[block["asset_ref"]]
        locator = asset["locator"]
        if locator["kind"] != "project_relative":
            raise CompileError(
                f"asset.{asset['id']} must be project_relative for an offline image build"
            )
        path = _resolve_project_path(
            self.artifact_root,
            locator["value"],
            f"asset.{asset['id']}",
        )
        if path.suffix.lower() not in RASTER_OR_VECTOR_IMAGE:
            raise CompileError(f"asset.{asset['id']} is not a supported offline image")
        uri = local_image_data_uri(path)
        caption = block.get("caption", "")
        inline_styles = []
        if "image_crop_position" in block:
            inline_styles.append(f'object-position:{block["image_crop_position"]}')
        if "image_aspect_ratio" in block:
            inline_styles.append(f'aspect-ratio:{block["image_aspect_ratio"]}')
        style = f' style="{_escape(";".join(inline_styles))}"' if inline_styles else ""
        return (
            '<figure class="ri-image-frame">'
            f'<img src="{_escape(uri)}" alt="{_escape(block["alt"])}" '
            f'data-ir-asset-id="{_escape(asset["id"])}" '
            f'data-ir-edit-asset-id="{_escape(asset["id"])}" '
            f'{_edit_attributes("image", "block", block["id"], "image")}'
            f'{style}>'
            + (
                f'<figcaption {_edit_attributes("text", "block", block["id"], "caption")} '
                f'data-taohtml-edit="text">{_escape(caption)}</figcaption>'
                if caption
                else ""
            )
            + '</figure>'
        )

    def _render_claims(self, block: dict[str, Any]) -> str:
        values: list[str] = []
        for claim_ref in block["claim_refs"]:
            claim = self.claims[claim_ref]
            values.append(
                f'<div class="ri-claim" data-ir-claim-id="{_escape(claim_ref)}">'
                f'<span class="ri-claim-kind" data-taohtml-edit-lock>'
                f'{_escape(claim["kind"])} · {_escape(claim["status"])}</span>'
                f'<p class="ri-claim-statement" '
                f'{_edit_attributes("text", "claim", claim_ref, "statement")} '
                f'data-taohtml-edit="text">'
                f'{_escape(claim["statement"])}</p></div>'
            )
        return "".join(values)

    def _render_evidence(self, block: dict[str, Any]) -> str:
        values: list[str] = []
        for evidence_ref in block["evidence_refs"]:
            evidence = self.evidence[evidence_ref]
            values.append(
                f'<div class="ri-evidence" data-ir-evidence-id="{_escape(evidence_ref)}">'
                f'<span class="ri-block-label" data-taohtml-edit-lock>'
                f'{_escape(evidence["content_status"])}</span>'
                f'<p class="ri-evidence-copy" '
                f'{_edit_attributes("text", "evidence", evidence_ref, "summary")} '
                f'data-taohtml-edit="text">'
                f'{_escape(evidence["summary"])}</p></div>'
            )
        return "".join(values)

    def render_block(
        self,
        block: dict[str, Any],
        plan: dict[str, dict[str, str]],
        emphasized_refs: set[str],
        *,
        item_columns: int | None = None,
        wide_items: bool = False,
    ) -> str:
        extra_classes, motion_attrs = _motion_attributes(
            block["id"], plan, emphasized_refs
        )
        kind = block["kind"]
        layout_classes = []
        if item_columns is not None:
            layout_classes.append("ri-adaptive-items")
        if wide_items:
            layout_classes.append("ri-wide-items")
        classes = (
            f"ri-block ri-block-{kind} {' '.join(layout_classes)} {extra_classes}"
        ).strip()
        if kind == "body_text":
            body = (
                f'<p class="ri-copy" {_edit_attributes("text", "block", block["id"], "text")} '
                f'data-taohtml-edit="text">{_escape(block["text"])}</p>'
            )
        elif kind == "headline":
            body = (
                f'<h2 class="ri-block-title" {_edit_attributes("text", "block", block["id"], "text")} '
                f'data-taohtml-edit="text">{_escape(block["text"])}</h2>'
            )
        elif kind == "quote":
            body = (
                f'<blockquote class="ri-quote" {_edit_attributes("text", "block", block["id"], "text")} '
                f'data-taohtml-edit="text">{_escape(block["text"])}</blockquote>'
            )
        elif kind == "methodology":
            body = (
                f'<p class="ri-method" {_edit_attributes("text", "block", block["id"], "text")} '
                f'data-taohtml-edit="text">{_escape(block["text"])}</p>'
            )
        elif kind == "caveat":
            body = (
                f'<p class="ri-caveat" {_edit_attributes("text", "block", block["id"], "text")} '
                f'data-taohtml-edit="text">{_escape(block["text"])}</p>'
            )
        elif kind == "call_to_action":
            body = (
                f'<p class="ri-cta" {_edit_attributes("text", "block", block["id"], "text")} '
                f'data-taohtml-edit="text">{_escape(block["text"])}</p>'
            )
        elif kind in {"list", "process", "comparison", "timeline"}:
            body = self._render_items(block, item_columns)
        elif kind == "metric":
            body = self._render_metrics(block)
        elif kind == "data_visualization":
            body = self._render_chart(block)
        elif kind == "table":
            body = self._render_table(block)
        elif kind == "image":
            body = self._render_image(block)
        elif kind == "claim":
            body = self._render_claims(block)
        elif kind == "evidence_excerpt":
            body = self._render_evidence(block)
        else:  # Schema validation should make this unreachable.
            raise CompileError(f"Unsupported semantic block kind: {kind}")
        return (
            f'<article class="{classes}" data-ir-kind="{_escape(kind)}" {motion_attrs}>'
            f'{body}</article>'
        )

    def render_page(self, page: dict[str, Any], output_index: int) -> str:
        chapter = self.chapters[page["chapter_ref"]]
        plan, warnings = _motion_plan(
            page,
            set(self.theme_profile["supported_transition_intents"]),
        )
        self.warnings.extend(warnings)
        emphasized_refs = {
            ref
            for state in page.get("state_sequence", [])
            for ref in state["emphasized_refs"]
        }
        reading_order = page["visual_intent"]["reading_order"]
        title_ref = next(
            (ref for ref in reading_order if self.blocks[ref]["kind"] == "headline"),
            None,
        )
        if title_ref is None:
            unit = self.units[page["narrative_unit_refs"][0]]
            title_text = unit["takeaway"]
            title_motion_classes = ""
            title_motion_attrs = 'data-ir-derived-title="true"'
            title_edit_attrs = _edit_attributes(
                "text", "narrative_unit", unit["id"], "takeaway"
            )
            self.warnings.append(
                f"page.{page['id']} has no headline block; title is derived from its first narrative unit"
            )
        else:
            title_text = self.blocks[title_ref]["text"]
            title_motion_classes, title_motion_attrs = _motion_attributes(
                title_ref, plan, emphasized_refs
            )
            title_edit_attrs = _edit_attributes("text", "block", title_ref, "text")
        subtitle_ref = page.get("subtitle_ref")
        subtitle_text = (
            str(self.blocks[subtitle_ref]["text"])
            if isinstance(subtitle_ref, str)
            else ""
        )
        subtitle_html = ""
        if isinstance(subtitle_ref, str):
            subtitle_motion_classes, subtitle_motion_attrs = _motion_attributes(
                subtitle_ref, plan, emphasized_refs
            )
            subtitle_class = f"ri-subtitle {subtitle_motion_classes}".strip()
            subtitle_html = (
                f'<p class="{subtitle_class}" data-ir-kind="body_text" '
                f'data-ir-block-id="{_escape(subtitle_ref)}" {subtitle_motion_attrs} '
                f'{_edit_attributes("text", "block", subtitle_ref, "text")} '
                f'data-taohtml-edit="text">{_escape(subtitle_text)}</p>'
            )
        body_refs = [
            ref for ref in reading_order if ref not in {title_ref, subtitle_ref}
        ]
        layout, theme_variant = self._layout(page)
        layout_plan = self._layout_plan(
            page,
            title_text=title_text,
            subtitle_text=subtitle_text,
            body_refs=body_refs,
            layout=layout,
            output_index=output_index,
        )
        rendered_blocks = "".join(
            self.render_block(
                self.blocks[ref],
                plan,
                emphasized_refs,
                item_columns=layout_plan["item_columns"].get(ref),
                wide_items=ref in layout_plan["wide_item_ids"],
            )
            for ref in body_refs
        )
        source_ids = self._page_source_ids(page)
        source_display = page["source_display"]
        if source_display in {"inline", "footer"} and source_ids:
            source_text = self._source_line(source_ids)
        elif source_display == "appendix" and source_ids:
            source_text = "完整来源见附录：" + "、".join(source_ids)
        else:
            source_text = ""
        classes = (
            f"slide ri-page ri-layout-{layout} ri-block-count-{len(body_refs)}"
            f" ri-density-{layout_plan['density']}"
            f" ri-arrangement-{layout_plan['arrangement']}"
            + (" active" if output_index == 0 else "")
        )
        header_title_class = f"ri-title {title_motion_classes}".strip()
        source_html = (
            f'<span class="ri-sources" data-taohtml-edit-lock>'
            f'<span class="ri-source-label">来源</span> '
            f'<span>{_escape(source_text)}</span></span>'
            if source_text
            else '<span class="ri-sources"></span>'
        )
        state_ids = [state["id"] for state in page.get("state_sequence", [])]
        self.source_map_pages[page["id"]] = {
            "output_index": output_index,
            "selector": f'[data-ir-page-id="{page["id"]}"]',
            "chapter_ref": page["chapter_ref"],
            "narrative_unit_refs": page["narrative_unit_refs"],
            "block_selectors": {
                block_ref: f'[data-ir-block-id="{block_ref}"]'
                for block_ref in page["block_refs"]
            },
            "state_ids": state_ids,
            "subtitle_ref": subtitle_ref,
            "requested_composition_family": page["visual_intent"]["composition_family"],
            "resolved_layout_family": layout,
            "resolved_theme_variant": theme_variant,
            "layout_plan": {
                key: value
                for key, value in layout_plan.items()
                if key != "wide_item_ids"
            },
        }
        return (
            f'<section class="{classes}" data-title="{_escape(title_text)}" '
            f'data-layout="{_escape(theme_variant)}" data-ir-page-id="{_escape(page["id"])}" '
            f'data-ir-role="{_escape(page["role"])}" data-ir-form="{_escape(page["form"])}">'
            '<div class="ri-page-shell">'
            '<header class="ri-header">'
            f'<p class="ri-kicker" data-taohtml-edit-lock>{_escape(chapter["title"])} · '
            f'{_escape(page["role"])} / {_escape(page["form"])}</p>'
            f'<h1 class="{header_title_class}" {title_motion_attrs} {title_edit_attrs} '
            f'data-taohtml-edit="text">{_escape(title_text)}</h1>'
            f'{subtitle_html}'
            '</header>'
            f'<div class="ri-content">{rendered_blocks}</div>'
            f'<footer class="ri-footer">{source_html}'
            f'<span class="ri-page-number" data-taohtml-edit-lock>'
            f'{output_index + 1:02d}</span></footer>'
            '</div></section>'
        )

    def render_appendix(self, appendix: dict[str, Any], output_index: int) -> str:
        derived_id = f"appendix-page-{appendix['id']}"
        blocks = "".join(
            self.render_block(self.blocks[ref], {}, set())
            for ref in appendix["block_refs"]
        )
        sources = self._source_line(appendix.get("source_refs", []))
        self.source_map_pages[derived_id] = {
            "output_index": output_index,
            "selector": f'[data-ir-derived-page-id="{derived_id}"]',
            "appendix_ref": appendix["id"],
            "block_selectors": {
                block_ref: f'[data-ir-block-id="{block_ref}"]'
                for block_ref in appendix["block_refs"]
            },
            "state_ids": [],
            "resolved_layout_family": "grid",
            "resolved_theme_variant": self.theme_profile["layout_variants"]["grid"],
        }
        return (
            '<section class="slide ri-page ri-layout-grid" '
            f'data-title="{_escape(appendix["title"])}" data-layout="appendix" '
            f'data-ir-derived-page-id="{_escape(derived_id)}" data-ir-appendix-ref="{_escape(appendix["id"])}">'
            '<div class="ri-page-shell"><header class="ri-header">'
            '<p class="ri-kicker" data-taohtml-edit-lock>APPENDIX</p>'
            f'<h1 class="ri-title" {_edit_attributes("text", "appendix", appendix["id"], "title")} '
            f'data-taohtml-edit="text">{_escape(appendix["title"])}</h1>'
            '</header>'
            f'<div class="ri-content">{blocks}</div>'
            '<footer class="ri-footer">'
            f'<span class="ri-sources" data-taohtml-edit-lock>{_escape(sources)}</span>'
            f'<span class="ri-page-number" data-taohtml-edit-lock>{output_index + 1:02d}</span>'
            '</footer></div></section>'
        )

    def render_all(self) -> str:
        sections: list[str] = []
        state_complexity = self.ir["projection"]["state_complexity"]
        if state_complexity in {"reflow", "scene"}:
            self.warnings.append(
                f"projection.state_complexity={state_complexity} is reduced to staged "
                f"visibility by Runtime {CONTROLLED_STEP_CONTRACT}"
            )
        for page_id in self.ir["projection"]["page_order"]:
            sections.append(self.render_page(self.pages[page_id], len(sections)))
        for appendix in self.ir["appendices"]:
            sections.append(self.render_appendix(appendix, len(sections)))
        return "\n".join(sections)

    def render_all_corporate(self, shell_renderer: CorporateShellRenderer) -> str:
        sections: list[str] = []
        state_complexity = self.ir["projection"]["state_complexity"]
        if state_complexity in {"reflow", "scene"}:
            self.warnings.append(
                f"projection.state_complexity={state_complexity} is reduced to staged "
                f"visibility by Runtime {CONTROLLED_STEP_CONTRACT}"
            )
        for page_id in self.ir["projection"]["page_order"]:
            page = self.pages[page_id]
            generic = self.render_page(page, len(sections))
            rendered, role, variant = shell_renderer.wrap(
                generic, page=page, output_index=len(sections)
            )
            self.source_map_pages[page_id]["resolved_theme_variant"] = variant
            self.source_map_pages[page_id]["corporate_shell_role"] = role
            sections.append(rendered)
        for appendix in self.ir["appendices"]:
            derived_id = f"appendix-page-{appendix['id']}"
            generic = self.render_appendix(appendix, len(sections))
            rendered, role, variant = shell_renderer.wrap(
                generic, page=None, output_index=len(sections)
            )
            self.source_map_pages[derived_id]["resolved_theme_variant"] = variant
            self.source_map_pages[derived_id]["corporate_shell_role"] = role
            sections.append(rendered)
        return "\n".join(sections)

    def speaker_notes_payload(self) -> dict[str, Any]:
        return {
            "schema_version": "1.0",
            "notes_by_page": {
                page_id: copy.deepcopy(notes)
                for page_id, notes in sorted(self.notes_by_page.items())
            },
        }


def _render_shell(
    ir: dict[str, Any],
    sections: str,
    theme_css: str,
    theme_id: str,
    theme_name: str,
    notes_payload: dict[str, Any],
    report_ir_sha256: str,
    theme_kind: str,
) -> str:
    shell = inline_editor_assets(SHELL_PATH.read_text(encoding="utf-8"))
    if shell.count(START_MARKER) != 1 or shell.count(END_MARKER) != 1:
        raise CompileError("Runtime shell is missing unique slide markers")
    prefix, remainder = shell.split(START_MARKER, 1)
    _, suffix = remainder.split(END_MARKER, 1)
    rendered = f"{prefix}{START_MARKER}\n{sections}\n{END_MARKER}{suffix}"
    report_css = REPORT_IR_STYLE_PATH.read_text(encoding="utf-8")
    styles = (
        f'  <style id="taohtml-visual-system" data-theme-id="{_escape(theme_id)}" '
        f'data-theme-kind="{_escape(theme_kind)}">\n'
        f'{theme_css}\n  </style>\n'
        f'  <style id="taohtml-report-ir-style">\n{report_css}\n  </style>\n'
    )
    rendered = rendered.replace("</head>", f"{styles}</head>", 1)
    language = ir["report"].get("language", "zh-CN")
    rendered = rendered.replace('<html lang="en">', f'<html lang="{_escape(language)}">', 1)
    rendered = re.sub(
        r"<title>.*?</title>",
        f'<title>{_escape(ir["report"]["title"], quote=False)}</title>',
        rendered,
        count=1,
        flags=re.DOTALL,
    )
    mode = ir["build_binding"]["runtime"]["target_mode"]
    editor_enabled = ir["build_binding"]["runtime"]["editor_enabled"]
    old_deck = (
        f'<main class="deck" id="deck" data-taohtml-step-contract="{CONTROLLED_STEP_CONTRACT}">'
    )
    new_deck = (
        f'<main class="deck" id="deck" data-theme="{_escape(theme_id)}" '
        f'data-theme-name="{_escape(theme_name)}" data-theme-kind="{_escape(theme_kind)}" '
        f'data-mode="{_escape(mode)}" '
        f'data-report-ir-version="{_escape(ir["report_ir_version"])}" '
        f'data-report-ir-sha256="{report_ir_sha256}" '
        f'data-report-id="{_escape(ir["report"]["id"])}" '
        f'data-projection-id="{_escape(ir["projection"]["id"])}" '
        f'data-taohtml-step-contract="{CONTROLLED_STEP_CONTRACT}">'
    )
    if old_deck not in rendered:
        raise CompileError("Runtime shell deck hook is unavailable")
    rendered = rendered.replace(old_deck, new_deck, 1)
    if not editor_enabled:
        rendered = rendered.replace(
            '        <button id="editToggle">编辑模式</button>\n', "", 1
        )
    notes_json = json.dumps(
        notes_payload, ensure_ascii=False, sort_keys=True, separators=(",", ":")
    ).replace("</", "<\\/")
    metadata = (
        '<script type="application/json" id="taohtml-speaker-notes" '
        f'data-report-ir-sha256="{report_ir_sha256}">{notes_json}</script>\n  '
    )
    rendered = rendered.replace("  <script>\n    const slides", f"  {metadata}<script>\n    const slides", 1)
    return rendered.replace("\r\n", "\n").replace("\r", "\n")


def compile_ir(
    raw: dict[str, Any],
    artifact_root: Path,
    output_dir: Path,
    *,
    report_ir_ref: str = "report.ir.json",
    project_theme_dir: Path | None = None,
) -> dict[str, Any]:
    artifact_root = artifact_root.resolve(strict=True)
    validation = validate_ir(raw, artifact_root)
    if not validation["compiler_ready"]:
        messages = [
            f"{layer}: {issue}"
            for layer, issues in validation["issues"].items()
            for issue in issues
        ]
        raise CompileError("Report IR is not compiler-ready: " + " | ".join(messages))
    ir = validation["normalized_ir"]
    theme_binding = ir["build_binding"]["theme"]
    if theme_binding["kind"] == "built_in":
        if project_theme_dir is not None:
            raise CompileError("--project-theme-dir cannot be used with a built_in theme")
        theme = load_built_in_theme(theme_binding["ref"])
        profiles = _load_theme_profiles()
        if theme.theme_id not in profiles:
            raise CompileError(
                f"Built-in theme lacks a Report IR compiler profile: {theme.theme_id}"
            )
        profile = copy.deepcopy(profiles[theme.theme_id])
        profile["content_width_by_role"] = {
            "default": BUILT_IN_SAFE_CONTENT_WIDTH
        }
        if profile["display_name"] != theme.display_name:
            raise CompileError(f"Theme profile display name drift: {theme.theme_id}")
        reference_mode = None
    else:
        if project_theme_dir is None:
            raise CompileError("project_theme binding requires --project-theme-dir")
        theme = load_project_theme(project_theme_dir)
        if theme.theme_id != theme_binding["ref"]:
            raise CompileError(
                f"Project theme binding mismatch: IR requests {theme_binding['ref']}, "
                f"bundle provides {theme.theme_id}"
            )
        profile = _project_theme_profile(theme)
        project = theme.manifest.get("project", {})
        reference_mode = project.get("reference_mode", "reconstruct")
        has_enterprise = "enterprise" in ir["build_binding"]
        if reference_mode == "corporate_fidelity" and not has_enterprise:
            raise CompileError(
                "corporate_fidelity project theme requires build_binding.enterprise"
            )
        if reference_mode != "corporate_fidelity" and has_enterprise:
            raise CompileError(
                "build_binding.enterprise can only be used with a corporate_fidelity project theme"
            )
    declared_theme_version = theme_binding.get("version")
    actual_theme_contract_version = theme.manifest.get("schema_version")
    if (
        declared_theme_version is not None
        and declared_theme_version != actual_theme_contract_version
    ):
        raise CompileError(
            f"Theme binding version drift for {theme.theme_id}: declared "
            f"{declared_theme_version}, available {actual_theme_contract_version}"
        )
    normalized_hash = validation["identity"]["normalized_sha256"]
    renderer = ReportRenderer(ir, artifact_root, profile)
    if reference_mode == "corporate_fidelity":
        sections = renderer.render_all_corporate(
            CorporateShellRenderer(theme)
        )
    else:
        sections = renderer.render_all()
    shell_theme_kind = "built-in" if theme_binding["kind"] == "built_in" else "project"
    html_text = _render_shell(
        ir,
        sections,
        theme.css,
        theme.theme_id,
        theme.display_name,
        renderer.speaker_notes_payload(),
        normalized_hash,
        shell_theme_kind,
    )
    html_bytes = html_text.encode("utf-8")
    source_map = {
        "schema_version": "1.0",
        "report_ir_sha256": normalized_hash,
        "compiler_version": COMPILER_VERSION,
        "pages": renderer.source_map_pages,
    }
    source_map_bytes = canonical_bytes(source_map) + b"\n"
    normalized_bytes = canonical_bytes(ir) + b"\n"
    manifest = {
        "schema_version": "1.0",
        "compiler_version": COMPILER_VERSION,
        "report_ir": {
            "ref": report_ir_ref,
            "version": ir["report_ir_version"],
            "revision_id": ir["traceability"]["revision_id"],
            "normalized_sha256": normalized_hash,
            "semantic_graph_sha256": _semantic_graph_sha256(ir),
        },
        "workflow_profile": workflow_profile_record(ir),
        "theme": {
            "kind": theme_binding["kind"],
            "id": theme.theme_id,
            "reference_mode": reference_mode,
            "binding_version": theme_binding.get("version"),
            "manifest_sha256": sha256_file(theme.root / "theme.json"),
            "css_sha256": sha256_bytes(theme.css.encode("utf-8")),
            "compiler_profile_version": profile["profile_version"],
            "compiler_profile_sha256": (
                sha256_file(THEME_PROFILES_PATH)
                if theme_binding["kind"] == "built_in"
                else sha256_bytes(canonical_bytes(profile))
            ),
        },
        "runtime": {
            "bundle_version": RUNTIME_BUNDLE_VERSION,
            "report_ir_patch_contract": "embedded-html-v1",
            "report_ir_patch_schema_sha256": sha256_file(RUNTIME_PATCH_SCHEMA_PATH),
            "target_mode": ir["build_binding"]["runtime"]["target_mode"],
            "step_contract": ir["build_binding"]["runtime"]["step_contract"],
            "editor_enabled": ir["build_binding"]["runtime"]["editor_enabled"],
            "shell_sha256": sha256_file(SHELL_PATH),
            "report_ir_style_sha256": sha256_file(REPORT_IR_STYLE_PATH),
        },
        "outputs": {
            "html": {"ref": "index.html", "sha256": sha256_bytes(html_bytes)},
            "source_map": {
                "ref": "source-map.json",
                "sha256": sha256_bytes(source_map_bytes),
            },
            "normalized_ir": {
                "ref": "report.ir.normalized.json",
                "sha256": sha256_bytes(normalized_bytes),
            },
        },
        "counts": {
            "chapters": len(ir["chapters"]),
            "pages": len(ir["pages"]),
            "appendix_pages": len(ir["appendices"]),
            "output_pages": len(renderer.source_map_pages),
            "blocks": len(ir["blocks"]),
            "claims": len(ir["claims"]),
            "evidence": len(ir["evidence"]),
        },
        "degradations": sorted(set(renderer.warnings)),
        "open_boundaries": [
            "composition_graph_and_non_monotonic_state_runtime_not_implemented",
        ],
        "validation": {
            "schema_valid": validation["schema_valid"],
            "references_valid": validation["references_valid"],
            "semantics_valid": validation["semantics_valid"],
            "compiler_ready": validation["compiler_ready"],
            "verified_files": validation["verified_files"],
        },
        "qa_execution_claim": "not_executed_by_compiler",
    }
    if theme_binding["kind"] == "project_theme":
        manifest["theme"].update(
            {
                "templates_sha256": sha256_file(theme.root / "templates.html"),
                "provenance_sha256": sha256_file(theme.root / "provenance.json"),
            }
        )
    if reference_mode == "corporate_fidelity":
        manifest["enterprise_shell"] = {
            **copy.deepcopy(ir["build_binding"]["enterprise"]),
            "fidelity_validation": "validated_project_theme_bundle",
            "protected_shell_policy": "fixed_descendants_preserved",
        }

    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / "index.html").write_bytes(html_bytes)
    (output_dir / "source-map.json").write_bytes(source_map_bytes)
    (output_dir / "report.ir.normalized.json").write_bytes(normalized_bytes)
    write_json(output_dir / "build-manifest.json", manifest)
    return manifest


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("report_ir", type=Path)
    parser.add_argument("--artifact-root", type=Path)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--project-theme-dir", type=Path)
    args = parser.parse_args()
    artifact_root = args.artifact_root or args.report_ir.parent
    try:
        raw = load_json(args.report_ir)
        manifest = compile_ir(
            raw,
            artifact_root,
            args.output_dir,
            report_ir_ref=args.report_ir.name,
            project_theme_dir=args.project_theme_dir,
        )
    except (CompileError, OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"REPORT_IR_COMPILE_FAILED {exc}")
        return 1
    print(
        "REPORT_IR_COMPILED "
        f"pages={manifest['counts']['output_pages']} "
        f"theme={manifest['theme']['id']} "
        f"degradations={len(manifest['degradations'])} "
        f"output={args.output_dir / 'index.html'}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
