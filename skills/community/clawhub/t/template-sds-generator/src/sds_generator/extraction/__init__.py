from __future__ import annotations

from sds_generator.models import FieldCandidate, ParsedSourceDocument

from .base import ExtractionContext, deduplicate_candidates
from .section_01 import extract_section_01
from .section_02 import extract_section_02
from .section_03 import extract_section_03
from .section_04 import extract_section_04
from .section_05 import extract_section_05
from .section_06 import extract_section_06
from .section_07 import extract_section_07
from .section_08 import extract_section_08
from .section_09 import extract_section_09
from .section_10 import extract_section_10
from .section_11 import extract_section_11
from .section_12 import extract_section_12
from .section_13 import extract_section_13
from .section_14 import extract_section_14
from .section_15 import extract_section_15
from .section_16 import extract_section_16


SECTION_EXTRACTORS = {
    1: extract_section_01,
    2: extract_section_02,
    3: extract_section_03,
    4: extract_section_04,
    5: extract_section_05,
    6: extract_section_06,
    7: extract_section_07,
    8: extract_section_08,
    9: extract_section_09,
    10: extract_section_10,
    11: extract_section_11,
    12: extract_section_12,
    13: extract_section_13,
    14: extract_section_14,
    15: extract_section_15,
    16: extract_section_16,
}


def extract_document_candidates(document: ParsedSourceDocument) -> list[FieldCandidate]:
    ctx = ExtractionContext(document=document)
    candidates: list[FieldCandidate] = []
    for section_number, extractor in SECTION_EXTRACTORS.items():
        if section_number not in document.sections:
            continue
        candidates.extend(extractor(ctx))
    return deduplicate_candidates(candidates)
