"""PII detection engine — detect-only mode for auditing."""

from __future__ import annotations

from ..models import PIIMatch, PIIType
from .patterns import PATTERNS, mask_snippet


def detect_pii(text: str) -> list[PIIMatch]:
    """Scan text and return all PII matches without modifying the text."""
    matches: list[PIIMatch] = []
    counters: dict[str, int] = {}

    for line_number, line in enumerate(text.splitlines(), start=1):
        for pii_name, pattern, _desc in PATTERNS:
            for m in pattern.finditer(line):
                # Use captured group if exists, else full match
                matched_text = m.group(1) if m.lastindex else m.group(0)
                counters.setdefault(pii_name, 0)
                counters[pii_name] += 1
                placeholder = f"[{pii_name.upper()}_{counters[pii_name]}]"

                matches.append(
                    PIIMatch(
                        pii_type=PIIType(pii_name),
                        line_number=line_number,
                        start=m.start(),
                        end=m.end(),
                        original_snippet=mask_snippet(matched_text),
                        placeholder=placeholder,
                    )
                )
    return matches
