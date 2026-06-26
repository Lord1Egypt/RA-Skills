from __future__ import annotations

from sds_generator.extraction.base import ExtractionContext, extract_simple_fields


def extract_section_13(ctx: ExtractionContext):
    return extract_simple_fields(
        ctx,
        13,
        [
            {"field_name": "waste_treatment_methods_product", "labels": ("Product", "Waste treatment methods Product"), "stop_labels": ("Contaminated packaging", "Packaging")},
            {"field_name": "waste_treatment_methods_packaging", "labels": ("Contaminated packaging", "Packaging"), "stop_labels": ("Sewage disposal advice",)},
            {"field_name": "sewage_disposal_advice", "labels": ("Sewage disposal advice",), "stop_labels": ()},
        ],
        extractor_name="section_13",
    )
