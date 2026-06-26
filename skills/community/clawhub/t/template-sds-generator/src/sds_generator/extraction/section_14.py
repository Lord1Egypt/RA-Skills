from __future__ import annotations

import re

from sds_generator.extraction.base import ExtractionContext, deduplicate_candidates, normalize_text


MODE_LABELS = {
    "dot": ("DOT (US)", "DOT"),
    "adr_rid": ("ADR/RID",),
    "imdg": ("IMDG",),
    "iata": ("IATA-DGR", "IATA"),
}
GROUP_HEADERS = (
    (("14.1 UN number", "UN Number"), "un_number"),
    (("14.2 UN proper shipping name", "UN Proper Shipping Name"), "proper_shipping_name"),
    (("14.3 Transport hazard class(es)", "Transport hazard class(es)"), "hazard_class"),
    (("14.4 Packaging group", "Packing group, if applicable", "Packing group"), "packing_group"),
    (("14.5 Environmental hazards", "Environmental hazards"), "environmental_hazard"),
)
INLINE_MODE_FIELDS = (
    ("un_number", re.compile(r"(?is)\bUN number:\s*([A-Za-z0-9-]+)")),
    ("hazard_class", re.compile(r"(?is)\bClass:\s*([0-9A-Za-z.]+)")),
    ("packing_group", re.compile(r"(?is)\bPacking group:\s*([A-Za-z0-9-]+)")),
    (
        "proper_shipping_name",
        re.compile(r"(?is)\bProper shipping name:\s*(.+?)(?=\s+(?:Marine pollutant:|Further information:|$))"),
    ),
    ("marine_pollutant", re.compile(r"(?is)\bMarine pollutant:\s*(yes|no)\b")),
)
SECTION_14_STOP_RE = re.compile(
    r"(?i)\b(?:Further information|Special precautions for user|14\.6|14\.7|SECTION\s+15|15\.1)\b"
)


def _find_group_header(text: str, labels: tuple[str, ...], start: int = 0) -> tuple[int, int] | None:
    sliced = text[start:]
    label_group = "|".join(re.escape(label) for label in labels)
    match = re.search(rf"(?im)(?:^|\n)\s*(?P<label>{label_group})(?=\s|$)", sliced)
    if not match:
        return None
    label_start = start + match.start("label")
    label_end = start + match.end("label")
    return (label_start, label_end)


def _has_grouped_headers(text: str) -> bool:
    return any(_find_group_header(text, aliases) for aliases, _field_name in GROUP_HEADERS)


def _clean_transport_value(value: str, *, field_name: str) -> str | None:
    cleaned = normalize_text(value)
    cleaned = re.sub(r"_+", "", cleaned).strip()
    cleaned = re.sub(r"\(For reference only, please check\.\)", "", cleaned, flags=re.IGNORECASE).strip()
    cleaned = re.sub(r"(?i)\b(?:Further information|Special precautions for user|14\.6|14\.7|SECTION\s+15|15\.1)\b.*$", "", cleaned).strip()
    if field_name == "environmental_hazard":
        cleaned = re.sub(r"(?i)^Marine pollutant:\s*", "", cleaned).strip()
    if cleaned in {"", "-"}:
        return None
    if field_name == "un_number" and cleaned.upper() != "NOT DANGEROUS GOODS" and not cleaned.upper().startswith("UN"):
        cleaned = f"UN{cleaned}"
    return normalize_text(cleaned) or None


def _find_mode_slices(body: str, *, environmental_hazard: bool = False) -> list[tuple[str, str]]:
    matches: list[tuple[int, int, str]] = []
    for mode_key, aliases in MODE_LABELS.items():
        for alias in sorted(aliases, key=len, reverse=True):
            trailer = r"(?:\s+Marine pollutant)?\s*:" if environmental_hazard else r"\s*:"
            pattern = re.compile(rf"(?is)(?P<label>{re.escape(alias)}){trailer}")
            for match in pattern.finditer(body):
                matches.append((match.start("label"), match.end(), mode_key))

    matches.sort(key=lambda item: (item[0], -(item[1] - item[0])))
    chosen: list[tuple[int, int, str]] = []
    occupied_until = -1
    for start, end, mode_key in matches:
        if start < occupied_until:
            continue
        chosen.append((start, end, mode_key))
        occupied_until = end

    slices: list[tuple[str, str]] = []
    for index, (_start, end, mode_key) in enumerate(chosen):
        next_start = chosen[index + 1][0] if index + 1 < len(chosen) else len(body)
        slices.append((mode_key, body[end:next_start]))
    return slices


def _parse_grouped_modes(text: str) -> list[dict[str, str]]:
    header_spans: list[tuple[int, int, str]] = []
    search_start = 0
    for aliases, field_name in GROUP_HEADERS:
        found = _find_group_header(text, aliases, start=search_start)
        if not found:
            continue
        start, end = found
        header_spans.append((start, end, field_name))
        search_start = end
    if not header_spans:
        return []

    modes: dict[str, dict[str, str]] = {}
    for index, (_start, end, field_name) in enumerate(header_spans):
        next_start = header_spans[index + 1][0] if index + 1 < len(header_spans) else len(text)
        body = text[end:next_start]
        stop_match = SECTION_14_STOP_RE.search(body)
        if stop_match:
            body = body[:stop_match.start()]
        for mode_key, raw_value in _find_mode_slices(body, environmental_hazard=field_name == "environmental_hazard"):
            value = _clean_transport_value(raw_value, field_name=field_name)
            mode = modes.setdefault(mode_key, {"mode": mode_key})
            if field_name == "proper_shipping_name" and value == "Not dangerous goods":
                mode["status_note"] = "Not dangerous goods"
            if value is None:
                continue
            mode[field_name] = value
    return [mode for mode in modes.values() if any(key != "mode" for key in mode)]


def _find_inline_mode_blocks(text: str) -> list[tuple[str, str]]:
    if _has_grouped_headers(text):
        return []

    matches: list[tuple[int, int, str]] = []
    for mode_key, aliases in MODE_LABELS.items():
        for alias in sorted(aliases, key=len, reverse=True):
            pattern = re.compile(rf"(?is)(?<![A-Za-z])(?P<label>{re.escape(alias)})(?![A-Za-z])")
            for match in pattern.finditer(text):
                matches.append((match.start("label"), match.end("label"), mode_key))

    matches.sort(key=lambda item: (item[0], -(item[1] - item[0])))
    chosen: list[tuple[int, int, str]] = []
    occupied_until = -1
    for start, end, mode_key in matches:
        if start < occupied_until:
            continue
        chosen.append((start, end, mode_key))
        occupied_until = end

    blocks: list[tuple[str, str]] = []
    for index, (_start, end, mode_key) in enumerate(chosen):
        next_start = chosen[index + 1][0] if index + 1 < len(chosen) else len(text)
        stop_match = SECTION_14_STOP_RE.search(text, end)
        if stop_match:
            next_start = min(next_start, stop_match.start())
        blocks.append((mode_key, text[end:next_start]))
    return blocks


def _parse_inline_modes(text: str) -> list[dict[str, str]]:
    modes: list[dict[str, str]] = []
    for mode_key, block in _find_inline_mode_blocks(text):
        mode: dict[str, str] = {"mode": mode_key}
        normalized_block = normalize_text(block)
        if normalized_block.startswith("Not dangerous goods"):
            mode["status_note"] = "Not dangerous goods"
        for field_name, pattern in INLINE_MODE_FIELDS:
            match = pattern.search(block)
            if not match:
                continue
            clean_field_name = "environmental_hazard" if field_name == "marine_pollutant" else field_name
            value = _clean_transport_value(match.group(1), field_name=clean_field_name)
            if value is None:
                continue
            mode[field_name] = value
        if any(key != "mode" for key in mode):
            modes.append(mode)
    return modes


def _merge_modes(primary: list[dict[str, str]], secondary: list[dict[str, str]]) -> list[dict[str, str]]:
    merged: dict[str, dict[str, str]] = {mode["mode"]: dict(mode) for mode in secondary}
    for mode in primary:
        merged[mode["mode"]] = dict(mode)
    return [merged[mode_key] for mode_key in ("dot", "adr_rid", "imdg", "iata") if mode_key in merged]


def _extract_general_statement(text: str, modes: list[dict[str, str]]) -> str | None:
    further_information = re.search(r"(?is)\bFurther information\s*:?\s*(.+)$", text)
    if further_information:
        value = _clean_transport_value(further_information.group(1), field_name="transport_general_statement")
        if value:
            return value
    if "Not classified as dangerous in the meaning of transport regulations." in text:
        return "Not classified as dangerous in the meaning of transport regulations."
    if modes and all(mode.get("status_note") == "Not dangerous goods" and not mode.get("un_number") for mode in modes):
        return "Not dangerous goods"
    return None


def extract_section_14(ctx: ExtractionContext):
    text = ctx.section_text(14)
    if not text:
        return []

    grouped_modes = _parse_grouped_modes(text)
    inline_modes = _parse_inline_modes(text)
    modes = _merge_modes(inline_modes, grouped_modes)

    candidates = []
    if modes:
        candidates.append(
            ctx.make_candidate(
                14,
                "transport_modes",
                modes,
                normalized_value=modes,
                excerpt="; ".join(f"{mode['mode']}: {mode.get('status_note') or mode.get('un_number', '')}" for mode in modes),
                extractor="section_14.transport_modes",
                confidence=0.92,
            )
        )

    general_statement = _extract_general_statement(text, modes)
    if general_statement:
        candidates.append(
            ctx.make_candidate(
                14,
                "transport_general_statement",
                general_statement,
                extractor="section_14.transport_general_statement",
                confidence=0.8,
            )
        )

    return deduplicate_candidates(candidates)
