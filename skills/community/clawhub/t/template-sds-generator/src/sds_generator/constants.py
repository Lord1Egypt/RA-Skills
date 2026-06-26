from __future__ import annotations

NO_DATA = "No data available"

EXPECTED_SECTION_ORDER = [f"section_{index}" for index in range(1, 17)]

SECTION_TITLES = {
    1: "Section 1: Identification",
    2: "Section 2: Hazards identification",
    3: "Section 3: Composition/information on ingredients",
    4: "Section 4: First-aid measures",
    5: "Section 5: Fire-fighting measures",
    6: "Section 6: Accidental release measures",
    7: "Section 7: Handling and storage",
    8: "Section 8: Exposure controls/personal protection",
    9: "Section 9: Physical and chemical properties",
    10: "Section 10: Stability and reactivity",
    11: "Section 11: Toxicological information",
    12: "Section 12: Ecological information",
    13: "Section 13: Disposal considerations",
    14: "Section 14: Transport information",
    15: "Section 15: Regulatory information",
    16: "Section 16: Other information",
}

NON_FABRICABLE_FIELDS = {
    "section_1.ec_number",
    "section_2.ghs_classifications",
    "section_2.signal_word",
    "section_2.pictograms",
    "section_2.hazard_statements",
    "section_9.flash_point",
    "section_11.numerical_measures_of_toxicity",
    "section_14.un_number",
    "section_14.transport_hazard_class",
    "section_14.packing_group",
}
