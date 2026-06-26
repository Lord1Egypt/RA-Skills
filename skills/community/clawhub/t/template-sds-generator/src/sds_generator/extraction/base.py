from __future__ import annotations

import json
import re
from dataclasses import dataclass
from itertools import chain
from typing import Any, Iterable, Sequence

from sds_generator.constants import NON_FABRICABLE_FIELDS
from sds_generator.models import FieldCandidate, ParsedSourceDocument, SourceReference
from sds_generator.parsing.layout_cleanup import normalize_text


SECTION_FIELD_PATH = "section_{section_number}.{field_name}"


def unique_list(values: Iterable[str]) -> list[str]:
    seen: set[str] = set()
    ordered: list[str] = []
    for value in values:
        cleaned = normalize_text(value)
        if not cleaned:
            continue
        key = cleaned.casefold()
        if key in seen:
            continue
        seen.add(key)
        ordered.append(cleaned)
    return ordered


def list_to_text(value: Any) -> str:
    if isinstance(value, str):
        return normalize_text(value)
    if isinstance(value, (list, tuple, set)):
        return "; ".join(normalize_text(str(item)) for item in value if normalize_text(str(item)))
    return normalize_text(json.dumps(value, ensure_ascii=True))


def split_tokens(value: str, delimiters: str = r"[;\n]") -> list[str]:
    return unique_list(re.split(delimiters, value))


def find_lines(text: str) -> list[str]:
    return [normalize_text(line) for line in text.splitlines() if normalize_text(line)]


def build_stop_labels(labels: Sequence[str], extra_stop_labels: Sequence[str] = ()) -> list[str]:
    return unique_list(chain(labels, extra_stop_labels))


def extract_labeled_value(text: str, labels: Sequence[str], stop_labels: Sequence[str] = ()) -> str | None:
    if not text:
        return None

    label_group = "|".join(sorted((re.escape(label) for label in labels), key=len, reverse=True))
    stops = build_stop_labels(stop_labels)
    stop_group = "|".join(sorted((re.escape(label) for label in stops), key=len, reverse=True))

    if stop_group:
        pattern = re.compile(
            rf"(?is)\b(?:{label_group})\b\s*[:#-]?\s*(?P<value>.*?)(?=(?:\b(?:{stop_group})\b\s*[:#-]?)|$)"
        )
    else:
        pattern = re.compile(rf"(?is)\b(?:{label_group})\b\s*[:#-]?\s*(?P<value>.+)")

    match = pattern.search(text)
    if not match:
        return None
    return normalize_text(match.group("value"))


def extract_reverse_labeled_value(text: str, labels: Sequence[str], stop_labels: Sequence[str] = ()) -> str | None:
    if not text:
        return None

    label_group = "|".join(sorted((re.escape(label) for label in labels), key=len, reverse=True))
    pattern = re.compile(rf"(?is):\s*(?P<value>.*?)(?=\s+\b(?:{label_group})\b)")

    match = pattern.search(text)
    if not match:
        return None
    return normalize_text(match.group("value"))


def search_pattern(pattern: re.Pattern[str], text: str) -> str | None:
    match = pattern.search(text)
    if not match:
        return None
    return normalize_text(match.group(1) if match.lastindex else match.group(0))


@dataclass(slots=True)
class ExtractionContext:
    document: ParsedSourceDocument

    def section_text(self, section_number: int) -> str:
        section = self.document.sections.get(section_number)
        return section.text if section else ""

    def section_pages(self, section_number: int) -> list[int]:
        section = self.document.sections.get(section_number)
        return section.pages if section else []

    def locate_page(self, section_number: int, excerpt: str | None = None) -> int | None:
        section = self.document.sections.get(section_number)
        if section is None:
            return None
        if not excerpt:
            return section.start_page

        needle = normalize_text(excerpt).casefold()
        for block in self.document.blocks:
            if block.block_id not in section.block_ids:
                continue
            if needle and needle in normalize_text(block.text).casefold():
                return block.page_number
        return section.start_page

    def source_reference(self, section_number: int, excerpt: str | None = None) -> SourceReference:
        page = self.locate_page(section_number, excerpt)
        return SourceReference(
            file_name=self.document.file_name,
            file_path=self.document.file_path,
            source_profile=self.document.source_profile,
            source_authority=self.document.source_authority,
            source_revision_date=self.document.revision_date,
            page=page,
            section=section_number,
            excerpt=normalize_text(excerpt or ""),
        )

    def make_candidate(
        self,
        section_number: int,
        field_name: str,
        raw_value: Any,
        *,
        normalized_value: Any = None,
        excerpt: str | None = None,
        extractor: str,
        confidence: float = 0.8,
        label: str | None = None,
        caveats: Sequence[str] | None = None,
    ) -> FieldCandidate:
        field_path = SECTION_FIELD_PATH.format(section_number=section_number, field_name=field_name)
        excerpt_text = normalize_text(excerpt or list_to_text(raw_value))
        return FieldCandidate(
            field_path=field_path,
            raw_value=raw_value,
            normalized_value=normalized_value if normalized_value is not None else raw_value,
            source_file=self.document.file_name,
            source_profile=self.document.source_profile,
            source_authority=self.document.source_authority,
            source_revision_date=self.document.revision_date,
            page=self.locate_page(section_number, excerpt_text),
            section=section_number,
            excerpt=excerpt_text,
            extractor=extractor,
            confidence=confidence,
            caveats=list(caveats or []),
            label=label,
            is_critical=field_path in NON_FABRICABLE_FIELDS,
            source_reference=self.source_reference(section_number, excerpt_text),
        )


def deduplicate_candidates(candidates: Sequence[FieldCandidate]) -> list[FieldCandidate]:
    seen: set[tuple[str, str, int | None]] = set()
    result: list[FieldCandidate] = []
    for candidate in candidates:
        normalized = list_to_text(candidate.normalized_value)
        key = (candidate.field_path, normalized.casefold(), candidate.page)
        if key in seen:
            continue
        seen.add(key)
        result.append(candidate)
    return result


def extract_simple_fields(
    ctx: ExtractionContext,
    section_number: int,
    specs: Sequence[dict[str, Any]],
    *,
    extractor_name: str,
) -> list[FieldCandidate]:
    text = ctx.section_text(section_number)
    if not text:
        return []

    labels_by_field = {spec["field_name"]: tuple(spec["labels"]) for spec in specs}
    all_labels = [label for labels in labels_by_field.values() for label in labels]
    candidates: list[FieldCandidate] = []
    for spec in specs:
        stop_labels = spec.get("stop_labels") or [label for label in all_labels if label not in spec["labels"]]
        value = extract_labeled_value(text, spec["labels"], stop_labels=stop_labels)
        if not value and spec.get("allow_reverse"):
            value = extract_reverse_labeled_value(text, spec["labels"], stop_labels=stop_labels)
        if not value:
            continue

        normalized = value
        if spec.get("as_list"):
            normalized = split_tokens(value, spec.get("delimiters", r"[;\n]"))
        candidates.append(
            ctx.make_candidate(
                section_number,
                spec["field_name"],
                value,
                normalized_value=normalized,
                excerpt=value,
                extractor=f"{extractor_name}.{spec['field_name']}",
                confidence=float(spec.get("confidence", 0.72)),
                label=spec["labels"][0],
            )
        )

    return deduplicate_candidates(candidates)
