from __future__ import annotations

import re

from sds_generator.extraction.base import ExtractionContext, deduplicate_candidates, normalize_text, split_tokens
from sds_generator.extraction.shared_patterns import CAS_RE, EC_RE, FORMULA_RE, MOLECULAR_WEIGHT_RE


WINDOW_LABELS = (
    ("substance_or_mixture", ("Substance / Mixture", "Substance", "Mixture")),
    ("chemical_name", ("Chemical name",)),
    ("product_name", ("Product name",)),
    ("synonyms", ("Synonyms",)),
    ("cas_number", ("CAS-No.", "CAS")),
    ("formula", ("Formula", "MF")),
    ("molecular_weight", ("Molecular Weight", "Molecular weight", "MW")),
)
DISCLOSURE_SENTENCES = (
    "No ingredients are hazardous according to OSHA criteria.",
    "No components need to be disclosed according to the applicable regulations.",
)


def _collect_label_matches(text: str) -> list[tuple[int, int, str, str]]:
    matches: list[tuple[int, int, str, str]] = []
    for field_name, labels in WINDOW_LABELS:
        for label in sorted(labels, key=len, reverse=True):
            pattern = re.compile(rf"(?i)(?<![A-Za-z])(?P<label>{re.escape(label)})(?![A-Za-z])")
            for match in pattern.finditer(text):
                matches.append((match.start("label"), match.end("label"), field_name, label))

    matches.sort(key=lambda item: (item[0], -(item[1] - item[0])))
    chosen: list[tuple[int, int, str, str]] = []
    occupied_until = -1
    for start, end, field_name, label in matches:
        if start < occupied_until:
            continue
        chosen.append((start, end, field_name, label))
        occupied_until = end
    return chosen


def _clean_window_value(field_name: str, value: str) -> str | None:
    cleaned = normalize_text(value)
    cleaned = re.sub(r"_+", "", cleaned).strip()
    cleaned = re.sub(r"^(?:[:\-–.]\s*)+", "", cleaned)
    cleaned = re.sub(r"(?i)\b3\.1\s+Substances?\b.*$", "", cleaned).strip()
    cleaned = normalize_text(cleaned)
    if not cleaned:
        return None
    if field_name == "molecular_weight":
        cleaned = cleaned.rstrip(":").strip()
    return cleaned or None


def _extract_windows(text: str) -> dict[str, str]:
    windows: dict[str, str] = {}
    matches = _collect_label_matches(text)
    for index, (_start, end, field_name, _label) in enumerate(matches):
        next_start = matches[index + 1][0] if index + 1 < len(matches) else len(text)
        value = _clean_window_value(field_name, text[end:next_start])
        if value and field_name not in windows:
            windows[field_name] = value
    return windows


def _looks_like_cas(value: str | None) -> bool:
    return bool(value and CAS_RE.fullmatch(normalize_text(value)))


def _looks_like_formula(value: str | None) -> bool:
    return bool(value and FORMULA_RE.fullmatch(normalize_text(value)))


def _looks_like_molecular_weight(value: str | None) -> bool:
    return bool(value and re.fullmatch(r"[0-9]+(?:\.[0-9]+)?\s*(?:g/mol|g/mole)?", normalize_text(value), flags=re.IGNORECASE))


def _looks_like_synonym_list(value: str | None) -> bool:
    if not value:
        return False
    cleaned = normalize_text(value)
    if _looks_like_cas(cleaned) or _looks_like_formula(cleaned) or _looks_like_molecular_weight(cleaned):
        return False
    return "," in cleaned or ";" in cleaned


def _looks_like_substance_marker(value: str | None) -> bool:
    return bool(value and normalize_text(value).casefold() in {"substance", "mixture"})


def _extract_disclosure_statement(text: str) -> str | None:
    statements = [sentence for sentence in DISCLOSURE_SENTENCES if sentence in text]
    if not statements:
        return None
    return " ".join(statements)


def extract_section_03(ctx: ExtractionContext):
    text = ctx.section_text(3)
    if not text:
        return []

    windows = _extract_windows(text)
    candidates = []

    substance_or_mixture = None
    if _looks_like_substance_marker(windows.get("substance_or_mixture")):
        substance_or_mixture = normalize_text(windows["substance_or_mixture"]).title()
    elif re.search(r"(?i)\b3\.1\s+Substances\b", text) or re.search(r"(?im)^\s*Substance\s*$", text):
        substance_or_mixture = "Substance"
    elif re.search(r"(?im)^\s*Mixture\s*$", text):
        substance_or_mixture = "Mixture"
    if substance_or_mixture:
        candidates.append(
            ctx.make_candidate(
                3,
                "substance_or_mixture",
                substance_or_mixture,
                extractor="section_03.substance_or_mixture",
                confidence=0.92,
            )
        )

    chemical_name = None
    explicit_chemical_name = windows.get("chemical_name")
    product_name = windows.get("product_name")
    substance_window = windows.get("substance_or_mixture")
    if explicit_chemical_name and not any(
        (
            _looks_like_cas(explicit_chemical_name),
            _looks_like_formula(explicit_chemical_name),
            _looks_like_molecular_weight(explicit_chemical_name),
        )
    ):
        chemical_name = explicit_chemical_name
    elif substance_window and not _looks_like_substance_marker(substance_window) and not any(
        (_looks_like_cas(substance_window), _looks_like_formula(substance_window), _looks_like_molecular_weight(substance_window))
    ):
        chemical_name = substance_window
    elif product_name and not _looks_like_synonym_list(product_name) and not any(
        (_looks_like_cas(product_name), _looks_like_formula(product_name), _looks_like_molecular_weight(product_name))
    ):
        chemical_name = product_name
    if chemical_name:
        candidates.append(ctx.make_candidate(3, "chemical_name", chemical_name, extractor="section_03.chemical_name", confidence=0.9))

    synonyms_source = windows.get("synonyms")
    if (not synonyms_source or _looks_like_cas(synonyms_source) or _looks_like_formula(synonyms_source)) and _looks_like_synonym_list(product_name):
        synonyms_source = product_name
    if synonyms_source and not _looks_like_cas(synonyms_source):
        synonym_list = split_tokens(synonyms_source, delimiters=r"[,\n;]")
        if synonym_list:
            candidates.append(
                ctx.make_candidate(
                    3,
                    "common_name_and_synonyms",
                    synonym_list,
                    normalized_value=synonym_list,
                    excerpt=synonyms_source,
                    extractor="section_03.common_name_and_synonyms",
                    confidence=0.88,
                )
            )

    cas_number = None
    for value in (windows.get("cas_number"), windows.get("synonyms")):
        if _looks_like_cas(value):
            cas_number = normalize_text(value)
            break
    if not cas_number:
        cas_match = CAS_RE.search(text)
        cas_number = cas_match.group(0) if cas_match else None
    if cas_number:
        candidates.append(ctx.make_candidate(3, "cas_number", cas_number, extractor="section_03.cas_number", confidence=0.9))

    ec_match = EC_RE.search(text)
    if ec_match:
        candidates.append(ctx.make_candidate(3, "ec_number", ec_match.group(0), extractor="section_03.ec_number", confidence=0.86))

    formula = None
    for value in (windows.get("formula"), windows.get("cas_number")):
        if _looks_like_formula(value):
            formula = normalize_text(value)
            break
    if not formula:
        formula_match = FORMULA_RE.search(text)
        formula = formula_match.group(0) if formula_match else None
    if formula:
        candidates.append(ctx.make_candidate(3, "formula", formula, extractor="section_03.formula", confidence=0.88))

    molecular_weight = None
    for value in (windows.get("molecular_weight"), windows.get("formula")):
        if _looks_like_molecular_weight(value):
            molecular_weight = normalize_text(value)
            break
    if not molecular_weight:
        mw_match = MOLECULAR_WEIGHT_RE.search(text)
        molecular_weight = mw_match.group(1) if mw_match else None
    if molecular_weight:
        candidates.append(
            ctx.make_candidate(
                3,
                "molecular_weight",
                molecular_weight,
                extractor="section_03.molecular_weight",
                confidence=0.88,
            )
        )

    disclosure_statement = _extract_disclosure_statement(text)
    if disclosure_statement:
        candidates.append(
            ctx.make_candidate(
                3,
                "disclosure_statement",
                disclosure_statement,
                extractor="section_03.disclosure_statement",
                confidence=0.86,
            )
        )

    return deduplicate_candidates(candidates)
