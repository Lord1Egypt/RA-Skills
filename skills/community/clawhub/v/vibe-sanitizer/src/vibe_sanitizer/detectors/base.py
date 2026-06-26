from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path
from typing import Callable, Pattern

from vibe_sanitizer.models import MatchCandidate


PreviewBuilder = Callable[[re.Match[str]], str]
ReplacementBuilder = Callable[[re.Match[str], dict[str, str]], str | None]
MatchFilter = Callable[[re.Match[str]], bool]


@dataclass(frozen=True)
class DetectorContext:
    repo_root: Path
    home_dir: Path


@dataclass(frozen=True)
class RegexDetector:
    detector_id: str
    title: str
    category: str
    severity: str
    message: str
    pattern: Pattern[str]
    preview_builder: PreviewBuilder
    replacement_builder: ReplacementBuilder
    priority: int
    editable_in_place: bool
    review_required: bool
    span_group: str | int | None = None
    match_filter: MatchFilter | None = None

    def find_matches(self, text: str, placeholders: dict[str, str], severity: str) -> list[MatchCandidate]:
        matches: list[MatchCandidate] = []
        for match in self.pattern.finditer(text):
            if self.match_filter is not None and not self.match_filter(match):
                continue

            if self.span_group is None:
                start_offset, end_offset = match.span()
                matched_text = match.group()
            else:
                start_offset, end_offset = match.span(self.span_group)
                matched_text = match.group(self.span_group)

            if start_offset == end_offset:
                continue

            matches.append(
                MatchCandidate(
                    detector_id=self.detector_id,
                    title=self.title,
                    category=self.category,
                    severity=severity,
                    message=self.message,
                    start_offset=start_offset,
                    end_offset=end_offset,
                    preview=self.preview_builder(match),
                    replacement_text=self.replacement_builder(match, placeholders),
                    editable_in_place=self.editable_in_place,
                    review_required=self.review_required,
                    priority=self.priority,
                    matched_text=matched_text,
                )
            )
        return matches
