from __future__ import annotations

from sds_generator.extraction.base import ExtractionContext, extract_simple_fields


def extract_section_10(ctx: ExtractionContext):
    return extract_simple_fields(
        ctx,
        10,
        [
            {"field_name": "reactivity", "labels": ("Reactivity",), "stop_labels": ("Chemical stability", "Possibility of hazardous reactions")},
            {"field_name": "chemical_stability", "labels": ("Chemical stability",), "stop_labels": ("Possibility of hazardous reactions", "Conditions to avoid")},
            {"field_name": "possibility_of_hazardous_reactions", "labels": ("Possibility of hazardous reactions",), "stop_labels": ("Conditions to avoid", "Incompatible materials")},
            {"field_name": "conditions_to_avoid", "labels": ("Conditions to avoid",), "stop_labels": ("Incompatible materials", "Hazardous decomposition products")},
            {"field_name": "incompatible_materials", "labels": ("Incompatible materials",), "stop_labels": ("Hazardous decomposition products",)},
            {"field_name": "hazardous_decomposition_products", "labels": ("Hazardous decomposition products",), "stop_labels": ()},
        ],
        extractor_name="section_10",
    )
