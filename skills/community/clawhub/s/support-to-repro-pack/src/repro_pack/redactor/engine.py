"""PII redaction engine — detect and replace PII in text."""

from __future__ import annotations

from ..models import PIIMatch, PIIType, RedactionReport
from .patterns import PATTERNS, mask_snippet


class RedactionEngine:
    """Stateful redaction engine that tracks replacements across calls."""

    def __init__(self) -> None:
        self._counters: dict[str, int] = {}
        self._matches: list[PIIMatch] = []
        self._lines_processed: int = 0

    def redact(self, text: str) -> str:
        """Redact all PII from text, returning sanitized version."""
        lines = text.splitlines(keepends=True)
        result_lines: list[str] = []

        for line_idx, line in enumerate(lines):
            line_number = self._lines_processed + line_idx + 1
            # Collect all matches for this line, sort by position descending
            # so we can replace from right to left without offset issues
            line_matches: list[tuple[int, int, str, str, str]] = []

            for pii_name, pattern, _desc in PATTERNS:
                for m in pattern.finditer(line):
                    matched_text = m.group(1) if m.lastindex else m.group(0)
                    self._counters.setdefault(pii_name, 0)
                    self._counters[pii_name] += 1
                    placeholder = f"[{pii_name.upper()}_{self._counters[pii_name]}]"

                    line_matches.append(
                        (m.start(), m.end(), pii_name, matched_text, placeholder)
                    )

            # Remove overlapping matches: keep the longest match at each position
            line_matches.sort(key=lambda x: (x[0], -(x[1] - x[0])))
            filtered: list[tuple[int, int, str, str, str]] = []
            last_end = -1
            for item in line_matches:
                if item[0] >= last_end:
                    filtered.append(item)
                    last_end = item[1]
            # Sort by start position descending for safe replacement
            line_matches = sorted(filtered, key=lambda x: x[0], reverse=True)

            modified_line = line
            for start, end, pii_name, matched_text, placeholder in line_matches:
                self._matches.append(
                    PIIMatch(
                        pii_type=PIIType(pii_name),
                        line_number=line_number,
                        start=start,
                        end=end,
                        original_snippet=mask_snippet(matched_text),
                        placeholder=placeholder,
                    )
                )
                modified_line = modified_line[:start] + placeholder + modified_line[end:]

            result_lines.append(modified_line)

        self._lines_processed += len(lines)
        return "".join(result_lines)

    def get_report(self) -> RedactionReport:
        """Generate a redaction audit report."""
        return RedactionReport(
            total_found=len(self._matches),
            replacements=list(self._matches),
            regex_matched=len(self._matches),
            lines_processed=self._lines_processed,
        )

    def reset(self) -> None:
        """Reset engine state."""
        self._counters.clear()
        self._matches.clear()
        self._lines_processed = 0
