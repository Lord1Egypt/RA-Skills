from __future__ import annotations

from sds_generator.extraction.base import ExtractionContext, extract_simple_fields


def extract_section_16(ctx: ExtractionContext):
    return extract_simple_fields(
        ctx,
        16,
        [
            {"field_name": "full_text_h_statements", "labels": ("Full text of H-Statements referred to under sections 2 and 3.",), "stop_labels": ("HMIS Rating", "Further information")},
            {"field_name": "references", "labels": ("References",), "stop_labels": ("Disclaimer", "Further information")},
            {"field_name": "disclaimer", "labels": ("Disclaimer", "Further information"), "stop_labels": ("Copyright",)},
            {"field_name": "additional_information", "labels": ("Additional Information",), "stop_labels": ()},
        ],
        extractor_name="section_16",
    )
