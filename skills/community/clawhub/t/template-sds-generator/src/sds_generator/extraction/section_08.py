from __future__ import annotations

from sds_generator.extraction.base import ExtractionContext, extract_simple_fields


def extract_section_08(ctx: ExtractionContext):
    return extract_simple_fields(
        ctx,
        8,
        [
            {"field_name": "occupational_exposure_limits", "labels": ("Occupational Exposure limit values", "Components with workplace control parameters", "Ingredients with workplace control parameters"), "as_list": True, "delimiters": r"[;\n]"},
            {"field_name": "engineering_controls", "labels": ("Appropriate engineering controls", "Exposure controls"), "stop_labels": ("Eye/face protection", "Skin protection", "Respiratory protection")},
            {"field_name": "eye_face_protection", "labels": ("Eye/face protection",), "stop_labels": ("Skin protection", "Body Protection", "Respiratory protection")},
            {"field_name": "hand_protection", "labels": ("Skin protection",), "stop_labels": ("Body Protection", "Respiratory protection")},
            {"field_name": "skin_body_protection", "labels": ("Body Protection",), "stop_labels": ("Respiratory protection", "Control of environmental exposure", "Thermal hazards")},
            {"field_name": "respiratory_protection", "labels": ("Respiratory protection",), "stop_labels": ("Control of environmental exposure", "Thermal hazards")},
            {"field_name": "environmental_exposure_controls", "labels": ("Control of environmental exposure",), "stop_labels": ("Thermal hazards",)},
            {"field_name": "thermal_hazards", "labels": ("Thermal hazards",), "stop_labels": ()},
        ],
        extractor_name="section_08",
    )
