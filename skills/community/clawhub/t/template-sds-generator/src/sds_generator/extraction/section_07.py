from __future__ import annotations

from sds_generator.extraction.base import ExtractionContext, deduplicate_candidates, extract_labeled_value, extract_simple_fields
from sds_generator.extraction.shared_patterns import TEMPERATURE_RE


def extract_section_07(ctx: ExtractionContext):
    text = ctx.section_text(7)
    if not text:
        return []

    candidates = extract_simple_fields(
        ctx,
        7,
        [
            {"field_name": "safe_handling_precautions", "labels": ("Precautions for safe handling",), "stop_labels": ("Conditions for safe storage, including any incompatibilities", "Recommended storage temperature", "Specific end use(s)")},
            {"field_name": "storage_conditions", "labels": ("Conditions for safe storage, including any incompatibilities", "Storage conditions"), "stop_labels": ("Recommended storage temperature", "Storage class", "Specific end use(s)")},
            {"field_name": "specific_end_uses", "labels": ("Specific end use(s)",), "stop_labels": ()},
        ],
        extractor_name="section_07",
    )

    storage_temperature = None
    direct_match = TEMPERATURE_RE.search(text)
    if direct_match:
        storage_temperature = direct_match.group(0)
    if not storage_temperature:
        storage_temperature = extract_labeled_value(text, ["Recommended storage temperature", "Storage temperature"], stop_labels=["Storage class", "Specific end use(s)", "7.3"])
    if storage_temperature:
        candidates.append(ctx.make_candidate(7, "storage_temperature", storage_temperature, extractor="section_07.storage_temperature", confidence=0.9))

    return deduplicate_candidates(candidates)
