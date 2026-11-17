#!/usr/bin/env python3
"""Single source of truth for executable project-theme layout grammar."""

from __future__ import annotations

from typing import Any


EXECUTABLE_LAYOUT_OPTIONS = {
    "page_axis": {"row", "column"},
    "alignment": {"start", "center", "end"},
    "cover_structure": {"split", "single-column"},
    "cover_split": {"7:5", "5:7", "1:1", "none"},
    "content_structure": {"card-grid", "stack", "single-focus"},
    "content_columns": {"1", "2", "3"},
    "image_placement": {"left", "right", "top", "bottom", "background"},
    "image_aspect_ratio": {"16:9", "4:3", "3:2", "1:1", "3:4"},
    "image_fit": {"cover", "contain"},
    "image_treatment": {"natural", "muted", "monochrome", "high-contrast"},
    "data_structure": {"source-chart-split", "chart-focus", "table-focus", "metrics-grid"},
    "data_columns": {"1", "2", "3"},
    "module_organization": {"hard-grid", "soft-stack", "open-field"},
    "density": {"low", "medium", "high"},
    "visual_focus": {"headline-and-image", "image-first", "balanced"},
}
EXECUTABLE_LAYOUT_OPTIONS_WITH_UNKNOWN = {
    field: {*values, "unknown"} for field, values in EXECUTABLE_LAYOUT_OPTIONS.items()
}

LAYOUT_FALLBACKS = {
    "page_axis": "column",
    "alignment": "start",
    "cover_structure": "single-column",
    "cover_split": "none",
    "content_structure": "stack",
    "content_columns": "1",
    "image_placement": "bottom",
    "image_aspect_ratio": "16:9",
    "image_fit": "contain",
    "image_treatment": "natural",
    "data_structure": "chart-focus",
    "data_columns": "1",
    "module_organization": "open-field",
    "density": "medium",
    "visual_focus": "balanced",
}

COVER_SPLIT_BY_STRUCTURE = {
    "split": {"7:5", "5:7", "1:1"},
    "single-column": {"none"},
}
COVER_PLACEMENT_BY_STRUCTURE = {
    "split": {"left", "right"},
    "single-column": {"top", "bottom", "background"},
}
CONTENT_COLUMNS_BY_STRUCTURE = {
    "card-grid": {"1", "2", "3"},
    "stack": {"1"},
    "single-focus": {"1"},
}
DATA_COLUMNS_BY_STRUCTURE = {
    "source-chart-split": {"2"},
    "chart-focus": {"1"},
    "table-focus": {"1"},
    "metrics-grid": {"1", "2", "3"},
}
SOURCE_CHART_IMAGE_PLACEMENTS = {"left", "right"}


def _allowed(values: set[str]) -> str:
    return ", ".join(sorted(values))


def validate_layout_values(values: dict[str, str]) -> None:
    """Reject any concrete executable layout without a defined visual program."""
    if set(values) != set(EXECUTABLE_LAYOUT_OPTIONS):
        raise ValueError("executable_layout must contain the complete layout grammar.")
    for field, options in EXECUTABLE_LAYOUT_OPTIONS.items():
        if values[field] not in options:
            raise ValueError(
                f"executable_layout.{field} must be one of: {_allowed(options)}."
            )

    cover = values["cover_structure"]
    split = values["cover_split"]
    if split not in COVER_SPLIT_BY_STRUCTURE[cover]:
        raise ValueError(
            f"executable_layout.cover_structure={cover} is incompatible with "
            f"cover_split={split}; allowed cover_split values: "
            f"{_allowed(COVER_SPLIT_BY_STRUCTURE[cover])}."
        )

    placement = values["image_placement"]
    if placement not in COVER_PLACEMENT_BY_STRUCTURE[cover]:
        raise ValueError(
            f"executable_layout.cover_structure={cover} is incompatible with "
            f"image_placement={placement}; allowed image_placement values: "
            f"{_allowed(COVER_PLACEMENT_BY_STRUCTURE[cover])}."
        )
    if placement == "background" and values["image_fit"] != "cover":
        raise ValueError(
            "executable_layout.image_placement=background requires image_fit=cover."
        )

    content = values["content_structure"]
    content_columns = values["content_columns"]
    if content_columns not in CONTENT_COLUMNS_BY_STRUCTURE[content]:
        raise ValueError(
            f"executable_layout.content_structure={content} is incompatible with "
            f"content_columns={content_columns}; allowed content_columns values: "
            f"{_allowed(CONTENT_COLUMNS_BY_STRUCTURE[content])}."
        )

    data = values["data_structure"]
    data_columns = values["data_columns"]
    if data_columns not in DATA_COLUMNS_BY_STRUCTURE[data]:
        raise ValueError(
            f"executable_layout.data_structure={data} is incompatible with "
            f"data_columns={data_columns}; allowed data_columns values: "
            f"{_allowed(DATA_COLUMNS_BY_STRUCTURE[data])}."
        )
    if data == "source-chart-split" and placement not in SOURCE_CHART_IMAGE_PLACEMENTS:
        raise ValueError(
            "executable_layout.data_structure=source-chart-split is incompatible with "
            f"image_placement={placement}; allowed image_placement values: "
            f"{_allowed(SOURCE_CHART_IMAGE_PLACEMENTS)}."
        )


def resolve_layout_items(
    items: dict[str, dict[str, Any]],
) -> tuple[dict[str, str], dict[str, str]]:
    """Resolve unknowns to recorded compatibility-aware fallbacks and validate."""
    values = {
        field: (
            LAYOUT_FALLBACKS[field]
            if items[field]["status"] == "unknown"
            else items[field]["value"]
        )
        for field in EXECUTABLE_LAYOUT_OPTIONS
    }
    fallback_bases = {
        field: "Unknown VI layout value uses the neutral reversible compiler default."
        for field in EXECUTABLE_LAYOUT_OPTIONS
        if items[field]["status"] == "unknown"
    }

    if items["cover_structure"]["status"] == "unknown":
        split_hint = (
            items["cover_split"]["value"]
            if items["cover_split"]["status"] != "unknown"
            else None
        )
        placement_hint = (
            items["image_placement"]["value"]
            if items["image_placement"]["status"] != "unknown"
            else None
        )
        data_hint = (
            items["data_structure"]["value"]
            if items["data_structure"]["status"] != "unknown"
            else None
        )
        values["cover_structure"] = (
            "split"
            if split_hint in {"7:5", "5:7", "1:1"}
            or placement_hint in {"left", "right"}
            or data_hint == "source-chart-split"
            else "single-column"
        )
        fallback_bases["cover_structure"] = (
            "Unknown cover structure uses the neutral form compatible with the declared "
            "cover split, image placement, and data structure."
        )

    if items["content_structure"]["status"] == "unknown":
        column_hint = (
            items["content_columns"]["value"]
            if items["content_columns"]["status"] != "unknown"
            else "1"
        )
        values["content_structure"] = (
            "card-grid" if column_hint in {"2", "3"} else "stack"
        )
        fallback_bases["content_structure"] = (
            "Unknown content structure uses the neutral form compatible with the declared columns."
        )

    if items["data_structure"]["status"] == "unknown":
        column_hint = (
            items["data_columns"]["value"]
            if items["data_columns"]["status"] != "unknown"
            else "1"
        )
        values["data_structure"] = (
            "metrics-grid" if column_hint in {"2", "3"} else "chart-focus"
        )
        fallback_bases["data_structure"] = (
            "Unknown data structure uses the neutral form compatible with the declared columns."
        )

    cover = values["cover_structure"]
    if items["cover_split"]["status"] == "unknown":
        values["cover_split"] = "1:1" if cover == "split" else "none"
        fallback_bases["cover_split"] = (
            f"Unknown cover split uses the neutral value compatible with {cover}."
        )
    if items["image_placement"]["status"] == "unknown":
        values["image_placement"] = "right" if cover == "split" else "bottom"
        fallback_bases["image_placement"] = (
            f"Unknown image placement uses the neutral value compatible with {cover}."
        )

    content = values["content_structure"]
    if items["content_columns"]["status"] == "unknown":
        values["content_columns"] = "1"
        fallback_bases["content_columns"] = (
            f"Unknown content columns use the neutral value compatible with {content}."
        )

    data = values["data_structure"]
    if items["data_columns"]["status"] == "unknown":
        values["data_columns"] = {
            "source-chart-split": "2",
            "chart-focus": "1",
            "table-focus": "1",
            "metrics-grid": "3",
        }[data]
        fallback_bases["data_columns"] = (
            f"Unknown data columns use the neutral value compatible with {data}."
        )
    if (
        items["image_fit"]["status"] == "unknown"
        and values["image_placement"] == "background"
    ):
        values["image_fit"] = "cover"
        fallback_bases["image_fit"] = (
            "Unknown image fit uses cover because background placement must fill its layer."
        )

    validate_layout_values(values)
    return values, fallback_bases
