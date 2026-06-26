from __future__ import annotations

from sds_generator.extraction.base import ExtractionContext, extract_simple_fields


def extract_section_05(ctx: ExtractionContext):
    return extract_simple_fields(
        ctx,
        5,
        [
            {"field_name": "suitable_extinguishing_media", "labels": ("Suitable extinguishing media", "Extinguishing media"), "stop_labels": ("Unsuitable extinguishing media", "Specific hazards", "Advice for firefighters")},
            {"field_name": "unsuitable_extinguishing_media", "labels": ("Unsuitable extinguishing media",), "stop_labels": ("Specific hazards", "Hazardous combustion products", "Advice for firefighters")},
            {"field_name": "specific_hazards_arising", "labels": ("Specific hazards arising from the substance or mixture", "Specific Hazards Arising from the Chemical"), "stop_labels": ("Hazardous combustion products", "Advice for firefighters", "Further information")},
            {"field_name": "hazardous_combustion_products", "labels": ("Hazardous combustion products",), "stop_labels": ("Advice for firefighters", "Further information")},
            {"field_name": "firefighting_advice", "labels": ("Advice for firefighters",), "stop_labels": ("Further information",)},
            {"field_name": "further_information", "labels": ("Further information",), "stop_labels": ()},
        ],
        extractor_name="section_05",
    )
