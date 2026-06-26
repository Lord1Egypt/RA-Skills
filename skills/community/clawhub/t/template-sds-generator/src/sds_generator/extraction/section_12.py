from __future__ import annotations

from sds_generator.extraction.base import ExtractionContext, extract_simple_fields


def extract_section_12(ctx: ExtractionContext):
    return extract_simple_fields(
        ctx,
        12,
        [
            {"field_name": "ecotoxicity_fish", "labels": ("Toxicity to fish", "12.1 Toxicity"), "stop_labels": ("Toxicity to daphnia", "Persistence and degradability")},
            {"field_name": "ecotoxicity_daphnia", "labels": ("Toxicity to daphnia and other aquatic invertebrates",), "stop_labels": ("Toxicity to algae", "Persistence and degradability")},
            {"field_name": "ecotoxicity_algae", "labels": ("Toxicity to algae",), "stop_labels": ("Toxicity to microorganisms", "Persistence and degradability")},
            {"field_name": "ecotoxicity_microorganisms", "labels": ("Toxicity to microorganisms",), "stop_labels": ("Persistence and degradability", "Bioaccumulative potential")},
            {"field_name": "persistence_and_degradability", "labels": ("Persistence and degradability",), "stop_labels": ("Bioaccumulative potential", "Mobility in soil")},
            {"field_name": "bioaccumulative_potential", "labels": ("Bioaccumulative potential",), "stop_labels": ("Mobility in soil", "Results of PBT and vPvB assessment")},
            {"field_name": "mobility_in_soil", "labels": ("Mobility in soil",), "stop_labels": ("Results of PBT and vPvB assessment", "Other adverse effects")},
            {"field_name": "pbt_vpvb_assessment", "labels": ("Results of PBT and vPvB assessment", "PBT/vPvB assessment"), "stop_labels": ("Other adverse effects",)},
            {"field_name": "other_adverse_effects", "labels": ("Other adverse effects",), "stop_labels": ()},
        ],
        extractor_name="section_12",
    )
