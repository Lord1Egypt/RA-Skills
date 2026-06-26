from __future__ import annotations

from sds_generator.extraction.base import ExtractionContext, extract_simple_fields


def extract_section_15(ctx: ExtractionContext):
    return extract_simple_fields(
        ctx,
        15,
        [
            {"field_name": "sara_302", "labels": ("SARA 302 Components",), "stop_labels": ("SARA 313 Components", "SARA 311/312 Hazards")},
            {"field_name": "sara_313", "labels": ("SARA 313 Components",), "stop_labels": ("SARA 311/312 Hazards", "California Prop. 65 Components")},
            {"field_name": "sara_311_312", "labels": ("SARA 311/312 Hazards",), "stop_labels": ("California Prop. 65 Components", "Other regulations")},
            {"field_name": "proposition_65", "labels": ("California Prop. 65 Components",), "stop_labels": ("Other regulations",)},
            {"field_name": "other_regulations", "labels": ("Other regulations",), "stop_labels": ()},
        ],
        extractor_name="section_15",
    )
