from __future__ import annotations

import re

from sds_generator.extraction.base import ExtractionContext, deduplicate_candidates, extract_labeled_value, normalize_text, unique_list
from sds_generator.extraction.shared_patterns import P_CODE_RE


CLASSIFICATION_PATTERNS = (
    r"Acute aquatic toxicity \(Category 1\), H400",
    r"Chronic aquatic toxicity \(Category 1\), H410",
    r"Hazardous to the aquatic environment, short-term \(Acute\) - Category Acute 1",
    r"Hazardous to the aquatic environment, long-term \(Chronic\) - Category Chronic 1",
    r"Not a hazardous substance or mixture\.",
)
SECTION_21_LABELS = (
    "2.1 GHS Classification",
    "2.1 Classification of the substance or mixture",
    "Classification of the substance or mixture",
)
SECTION_22_LABELS = (
    "2.2 GHS Label elements, including precautionary statements",
    "2.2 GHS Label elements",
    "GHS Label elements, including precautionary statements",
    "Label elements",
)
SECTION_23_STOP_LABELS = (
    "2.3 Hazards not otherwise classified (HNOC) or not covered by GHS",
    "2.3 Other hazards",
    "2.3 Physical and chemical hazards",
    "2.4 Health hazards",
    "2.5 Environmental hazards",
    "2.6 Other hazards",
    "Other hazards",
    "SECTION 3",
)
PRECAUTIONARY_SUBLABELS = ("Prevention", "Response", "Storage", "Disposal")


def _window(text: str, start_labels: tuple[str, ...], stop_labels: tuple[str, ...]) -> str:
    lowered = text.casefold()
    starts = []
    for label in start_labels:
        index = lowered.find(label.casefold())
        if index >= 0:
            starts.append((index, len(label)))
    if not starts:
        return ""
    start_index, label_len = min(starts, key=lambda item: item[0])
    value_start = start_index + label_len
    while value_start < len(text) and text[value_start] in " :.-":
        value_start += 1

    stops = []
    for label in stop_labels:
        index = lowered.find(label.casefold(), value_start)
        if index >= 0:
            stops.append(index)
    value_end = min(stops) if stops else len(text)
    return normalize_text(text[value_start:value_end])


def _extract_classifications(text: str) -> list[str]:
    classifications = []
    for pattern in CLASSIFICATION_PATTERNS:
        match = re.search(pattern, text, flags=re.IGNORECASE)
        if match:
            classifications.append(match.group(0))
    return unique_list(classifications)


def _extract_signal_word(text: str) -> str | None:
    match = re.search(r"(?i)\bSignal word\s*(?:[:\s]+)(Warning|Danger)\b", text)
    if match:
        return match.group(1)
    reverse = re.search(r"(?i)\b(Warning|Danger)\s+Signal word\b", text)
    if reverse:
        return reverse.group(1)
    return None


def _extract_hazard_statements(text: str) -> list[str]:
    if not text:
        return []
    hazard_block = _window(
        text,
        ("Hazard statement(s)",),
        ("Precautionary statement(s)", "Prevention", "Response", "Storage", "Disposal", "Other hazards"),
    ) or text
    return _extract_code_statements(hazard_block, code_prefix="H", extra_stop_labels=("Precautionary statement(s)", "Other hazards"))


def _extract_code_statements(text: str, *, code_prefix: str, extra_stop_labels: tuple[str, ...] = ()) -> list[str]:
    pattern = re.compile(rf"(?i)\b({code_prefix}\d{{3}})\b")
    matches = list(pattern.finditer(text))
    if not matches:
        return []

    lowered = text.casefold()
    statements: list[str] = []
    for index, match in enumerate(matches):
        start = match.start()
        end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        for label in extra_stop_labels:
            stop_index = lowered.find(label.casefold(), start)
            if stop_index >= 0:
                end = min(end, stop_index)
        statement = normalize_text(text[start:end]).strip(" ;")
        if statement:
            statements.append(statement)
    return unique_list(statements)


def _extract_p_statements(text: str) -> list[str]:
    return _extract_code_statements(text, code_prefix="P", extra_stop_labels=("Other hazards",))


def _split_precautionary(statements: list[str]) -> tuple[list[str], list[str], list[str], list[str]]:
    prevention: list[str] = []
    response: list[str] = []
    storage: list[str] = []
    disposal: list[str] = []
    for statement in statements:
        code_match = P_CODE_RE.search(statement)
        if not code_match:
            continue
        code = code_match.group(0)
        if code in {"P273"}:
            prevention.append(statement)
        elif code in {"P391"}:
            response.append(statement)
        elif code in {"P501"}:
            disposal.append(statement)
        else:
            storage.append(statement)
    return (unique_list(prevention), unique_list(response), unique_list(storage), unique_list(disposal))


def _extract_precautionary_groups(text: str) -> tuple[list[str], list[str], list[str], list[str]]:
    block = _window(text, ("Precautionary statement(s)",), ("Other hazards",))
    if not block:
        return ([], [], [], [])

    explicit_groups: dict[str, list[str]] = {}
    found_explicit = any(
        re.search(rf"(?i)\b{label}\b\s*(?:P\d{{3}}\b|none\b)", block)
        for label in PRECAUTIONARY_SUBLABELS
    )
    if found_explicit:
        for label in PRECAUTIONARY_SUBLABELS:
            group_block = _window(block, (label,), tuple(item for item in PRECAUTIONARY_SUBLABELS if item != label))
            if group_block:
                explicit_groups[label.casefold()] = _extract_p_statements(group_block)
        return (
            unique_list(explicit_groups.get("prevention", [])),
            unique_list(explicit_groups.get("response", [])),
            unique_list(explicit_groups.get("storage", [])),
            unique_list(explicit_groups.get("disposal", [])),
        )

    return _split_precautionary(_extract_p_statements(block))


def _extract_pictograms(text: str, *, classifications: list[str], hazard_statements: list[str]) -> list[str]:
    if "Pictogram" not in text and "Pictogram(s)" not in text:
        return []
    if "GHS09" in text:
        return ["GHS09"]
    if any(token in text for token in ("Environment", "H400", "H410")):
        return ["GHS09"]
    if any("aquatic" in item.lower() for item in classifications + hazard_statements):
        return ["GHS09"]
    return []


def _clean_other_hazards(value: str | None) -> str | None:
    if not value:
        return None
    cleaned = normalize_text(value)
    cleaned = re.sub(r"_+", "", cleaned).strip()
    cleaned = cleaned.lstrip("–- ").strip()
    return cleaned or None


def extract_section_02(ctx: ExtractionContext):
    text = ctx.section_text(2)
    if not text:
        return []

    candidates = []
    classification_block = _window(text, SECTION_21_LABELS, SECTION_22_LABELS + SECTION_23_STOP_LABELS) or text
    label_elements_block = _window(text, SECTION_22_LABELS, SECTION_23_STOP_LABELS)

    classifications = _extract_classifications(classification_block)
    if classifications:
        candidates.append(
            ctx.make_candidate(
                2,
                "ghs_classifications",
                classifications,
                normalized_value=classifications,
                excerpt="; ".join(classifications),
                extractor="section_02.ghs_classifications",
                confidence=0.92,
            )
        )

    signal_word = _extract_signal_word(label_elements_block)
    if signal_word:
        candidates.append(ctx.make_candidate(2, "signal_word", signal_word, extractor="section_02.signal_word", confidence=0.94))

    hazard_statements = _extract_hazard_statements(label_elements_block)
    if hazard_statements:
        candidates.append(
            ctx.make_candidate(
                2,
                "hazard_statements",
                hazard_statements,
                normalized_value=hazard_statements,
                excerpt="; ".join(hazard_statements),
                extractor="section_02.hazard_statements",
                confidence=0.9,
            )
        )

    prevention, response, storage, disposal = _extract_precautionary_groups(label_elements_block)
    if prevention:
        candidates.append(
            ctx.make_candidate(
                2,
                "precautionary_prevention",
                prevention,
                normalized_value=prevention,
                excerpt="; ".join(prevention),
                extractor="section_02.precautionary_prevention",
                confidence=0.88,
            )
        )
    if response:
        candidates.append(
            ctx.make_candidate(
                2,
                "precautionary_response",
                response,
                normalized_value=response,
                excerpt="; ".join(response),
                extractor="section_02.precautionary_response",
                confidence=0.88,
            )
        )
    if storage:
        candidates.append(
            ctx.make_candidate(
                2,
                "precautionary_storage",
                storage,
                normalized_value=storage,
                excerpt="; ".join(storage),
                extractor="section_02.precautionary_storage",
                confidence=0.82,
            )
        )
    if disposal:
        candidates.append(
            ctx.make_candidate(
                2,
                "precautionary_disposal",
                disposal,
                normalized_value=disposal,
                excerpt="; ".join(disposal),
                extractor="section_02.precautionary_disposal",
                confidence=0.88,
            )
        )

    pictograms = _extract_pictograms(label_elements_block, classifications=classifications, hazard_statements=hazard_statements)
    if pictograms:
        candidates.append(
            ctx.make_candidate(
                2,
                "pictograms",
                pictograms,
                normalized_value=pictograms,
                excerpt="; ".join(pictograms),
                extractor="section_02.pictograms",
                confidence=0.8,
            )
        )

    other_hazards = _clean_other_hazards(
        extract_labeled_value(text, ["Other hazards", "Hazards not otherwise classified (HNOC) or not covered by GHS"], stop_labels=["SECTION 3", "3.1"])
    )
    if other_hazards:
        candidates.append(ctx.make_candidate(2, "other_hazards", other_hazards, extractor="section_02.other_hazards", confidence=0.82))

    summary = extract_labeled_value(text, ["Summary of emergency"], stop_labels=["2.1 GHS Classification", "2.1 Classification of the substance or mixture"])
    if summary:
        candidates.append(ctx.make_candidate(2, "summary_of_emergency", summary, extractor="section_02.summary_of_emergency", confidence=0.78))

    for field_name, label in (
        ("physical_hazards", "2.3 Physical and chemical hazards"),
        ("health_hazards", "2.4 Health hazards"),
        ("environmental_hazards", "2.5 Environmental hazards"),
    ):
        value = extract_labeled_value(text, [label], stop_labels=["2.4 Health hazards", "2.5 Environmental hazards", "2.6 Other hazards"])
        if value:
            candidates.append(ctx.make_candidate(2, field_name, value, extractor=f"section_02.{field_name}", confidence=0.76))

    return deduplicate_candidates(candidates)
