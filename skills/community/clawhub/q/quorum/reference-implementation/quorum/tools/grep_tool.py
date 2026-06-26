# SPDX-License-Identifier: MIT
# Copyright 2026 SharedIntellect — https://github.com/SharedIntellect/quorum

"""
Grep tool — file and pattern search with context lines.

Used by critics to gather evidence: find specific patterns, keys, or
sections in the artifact or supporting files.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class GrepMatch:
    """A single pattern match with surrounding context."""
    line_number: int
    line: str
    pattern: str
    context_before: list[str] = field(default_factory=list)
    context_after: list[str] = field(default_factory=list)
    file_path: str = ""

    def format(self, show_context: bool = True) -> str:
        """Human-readable match for evidence reporting."""
        parts = []
        if self.file_path:
            parts.append(f"File: {self.file_path}")

        if show_context and self.context_before:
            for i, line in enumerate(self.context_before):
                lineno = self.line_number - len(self.context_before) + i
                parts.append(f"  {lineno}: {line}")

        parts.append(f"→ {self.line_number}: {self.line}")

        if show_context and self.context_after:
            for i, line in enumerate(self.context_after):
                parts.append(f"  {self.line_number + i + 1}: {line}")

        return "\n".join(parts)


class GrepTool:
    """
    Pattern search tool.

    Searches file content or raw text for regex or literal patterns,
    returning matches with configurable context lines.
    """

    def __init__(self, context_lines: int = 2):
        self.context_lines = context_lines

    def search_text(
        self,
        text: str,
        pattern: str,
        *,
        ignore_case: bool = False,
        literal: bool = False,
        context_lines: int | None = None,
    ) -> list[GrepMatch]:
        """
        Search a text string for pattern.

        Args:
            text:          The text to search
            pattern:       Regex pattern (or literal string if literal=True)
            ignore_case:   Case-insensitive matching
            literal:       Treat pattern as a plain string, not regex
            context_lines: Override default context lines

        Returns:
            List of GrepMatch objects, one per matching line
        """
        ctx = context_lines if context_lines is not None else self.context_lines
        flags = re.IGNORECASE if ignore_case else 0
        search_pattern = re.escape(pattern) if literal else pattern

        lines = text.splitlines()
        matches: list[GrepMatch] = []

        for i, line in enumerate(lines):
            if re.search(search_pattern, line, flags=flags):
                before = lines[max(0, i - ctx) : i]
                after = lines[i + 1 : i + 1 + ctx]
                matches.append(
                    GrepMatch(
                        line_number=i + 1,
                        line=line,
                        pattern=pattern,
                        context_before=before,
                        context_after=after,
                    )
                )

        return matches

    def search_file(
        self,
        file_path: Path | str,
        pattern: str,
        *,
        ignore_case: bool = False,
        literal: bool = False,
        context_lines: int | None = None,
    ) -> list[GrepMatch]:
        """
        Search a file for pattern.

        Args:
            file_path: Path to file to search
            pattern:   Pattern to find
            ...        Same as search_text()

        Returns:
            List of GrepMatch objects
        """
        path = Path(file_path)
        try:
            text = path.read_text(encoding="utf-8", errors="replace")
        except FileNotFoundError:
            return []

        matches = self.search_text(
            text, pattern,
            ignore_case=ignore_case,
            literal=literal,
            context_lines=context_lines,
        )
        for m in matches:
            m.file_path = str(path)
        return matches

    def find_missing(self, text: str, required_patterns: list[str]) -> list[str]:
        """
        Check which required patterns are absent from text.

        Useful for completeness checking: "does this artifact mention X?"

        Returns:
            List of patterns that were NOT found
        """
        missing = []
        for pattern in required_patterns:
            if not self.search_text(text, pattern, ignore_case=True):
                missing.append(pattern)
        return missing

    def summarize_matches(self, matches: list[GrepMatch], max_chars: int = 800) -> str:
        """
        Produce a compact evidence string from a list of matches.
        Truncates if too many matches to keep evidence readable.
        """
        if not matches:
            return "(no matches found)"

        parts = []
        total_chars = 0
        for match in matches:
            formatted = match.format(show_context=True)
            if total_chars + len(formatted) > max_chars:
                remaining = len(matches) - len(parts)
                parts.append(f"... and {remaining} more matches")
                break
            parts.append(formatted)
            total_chars += len(formatted)

        return "\n---\n".join(parts)
