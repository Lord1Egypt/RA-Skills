from __future__ import annotations

from sds_generator.extraction.base import ExtractionContext, extract_simple_fields


def extract_section_06(ctx: ExtractionContext):
    return extract_simple_fields(
        ctx,
        6,
        [
            {"field_name": "personal_precautions", "labels": ("Personal precautions, protective equipment and emergency procedures", "Personal Precautions, protective equipment, and emergency procedure"), "stop_labels": ("Environmental precautions", "Methods and materials for containment and cleaning up", "Reference to other sections")},
            {"field_name": "environmental_precautions", "labels": ("Environmental precautions",), "stop_labels": ("Methods and materials for containment and cleaning up", "Reference to other sections")},
            {"field_name": "cleanup_methods", "labels": ("Methods and materials for containment and cleaning up",), "stop_labels": ("Reference to other sections",)},
            {"field_name": "reference_to_other_sections", "labels": ("Reference to other sections",), "stop_labels": ()},
        ],
        extractor_name="section_06",
    )
