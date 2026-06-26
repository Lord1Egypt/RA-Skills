from __future__ import annotations

from sds_generator.extraction.base import ExtractionContext, extract_simple_fields


def extract_section_04(ctx: ExtractionContext):
    return extract_simple_fields(
        ctx,
        4,
        [
            {"field_name": "general_advice", "labels": ("General advice",), "stop_labels": ("If inhaled", "Inhalation", "In case of skin contact", "Following skin contact")},
            {"field_name": "inhalation", "labels": ("If inhaled", "After inhalation", "Inhalation"), "stop_labels": ("In case of skin contact", "Following skin contact", "In case of eye contact", "Following eye contact")},
            {"field_name": "skin_contact", "labels": ("In case of skin contact", "Following skin contact"), "stop_labels": ("In case of eye contact", "Following eye contact", "If swallowed", "Following ingestion")},
            {"field_name": "eye_contact", "labels": ("In case of eye contact", "Following eye contact"), "stop_labels": ("If swallowed", "Following ingestion", "Most important symptoms")},
            {"field_name": "ingestion", "labels": ("If swallowed", "Following ingestion"), "stop_labels": ("Most important symptoms", "Indication of any immediate medical attention")},
            {"field_name": "most_important_symptoms", "labels": ("Most important symptoms and effects, both acute and delayed",), "stop_labels": ("Indication of any immediate medical attention", "Notes to physician")},
            {"field_name": "immediate_medical_attention", "labels": ("Indication of any immediate medical attention and special treatment needed",), "stop_labels": ("Notes to physician",)},
            {"field_name": "notes_to_physician", "labels": ("Notes to physician",), "stop_labels": ()},
        ],
        extractor_name="section_04",
    )
