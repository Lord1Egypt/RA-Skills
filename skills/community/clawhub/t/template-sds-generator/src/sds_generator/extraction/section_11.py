from __future__ import annotations

from sds_generator.extraction.base import ExtractionContext, extract_simple_fields


def extract_section_11(ctx: ExtractionContext):
    return extract_simple_fields(
        ctx,
        11,
        [
            {"field_name": "acute_toxicity_oral", "labels": ("Oral", "Acute toxicity Oral"), "stop_labels": ("Inhalation", "Dermal", "Skin corrosion/irritation")},
            {"field_name": "acute_toxicity_inhalation", "labels": ("Inhalation",), "stop_labels": ("Dermal", "Skin corrosion/irritation", "Serious eye damage/eye irritation")},
            {"field_name": "acute_toxicity_dermal", "labels": ("Dermal",), "stop_labels": ("Skin corrosion/irritation", "Serious eye damage/eye irritation")},
            {"field_name": "skin_corrosion_irritation", "labels": ("Skin corrosion/irritation",), "stop_labels": ("Serious eye damage/eye irritation", "Respiratory or skin sensitization")},
            {"field_name": "serious_eye_damage_irritation", "labels": ("Serious eye damage/eye irritation",), "stop_labels": ("Respiratory or skin sensitization", "Germ cell mutagenicity")},
            {"field_name": "respiratory_or_skin_sensitization", "labels": ("Respiratory or skin sensitization",), "stop_labels": ("Germ cell mutagenicity", "Carcinogenicity")},
            {"field_name": "germ_cell_mutagenicity", "labels": ("Germ cell mutagenicity",), "stop_labels": ("Carcinogenicity", "Reproductive toxicity")},
            {"field_name": "carcinogenicity", "labels": ("Carcinogenicity",), "stop_labels": ("Reproductive toxicity", "Specific target organ toxicity - single exposure")},
            {"field_name": "reproductive_toxicity", "labels": ("Reproductive toxicity",), "stop_labels": ("Specific target organ toxicity - single exposure", "Specific target organ toxicity - repeated exposure")},
            {"field_name": "stot_single_exposure", "labels": ("Specific target organ toxicity - single exposure",), "stop_labels": ("Specific target organ toxicity - repeated exposure", "Aspiration hazard")},
            {"field_name": "stot_repeated_exposure", "labels": ("Specific target organ toxicity - repeated exposure",), "stop_labels": ("Aspiration hazard", "Additional Information")},
            {"field_name": "aspiration_hazard", "labels": ("Aspiration hazard",), "stop_labels": ("Additional Information",)},
            {"field_name": "toxicological_additional_information", "labels": ("Additional Information",), "stop_labels": ()},
        ],
        extractor_name="section_11",
    )
