from __future__ import annotations

import re

from sds_generator.extraction.base import ExtractionContext, deduplicate_candidates, normalize_text, split_tokens
from sds_generator.extraction.shared_patterns import CAS_RE, EC_RE, FORMULA_RE, MOLECULAR_WEIGHT_RE, PRODUCT_NUMBER_RE

LABEL_PATTERNS: list[tuple[str, tuple[str, ...]]] = [
    ("product_identifier", ("Product identifiers", "Product identifier")),
    ("product_name", ("Product name",)),
    ("product_number", ("Product Number", "CBnumber")),
    ("cas_number", ("CAS-No.", "CAS Number", "CAS No.", "CAS")),
    ("synonyms", ("Synonyms",)),
    ("relevant_identified_uses", ("Identified uses", "Relevant identified uses")),
    ("uses_advised_against", ("Uses advised against",)),
    ("supplier_company_name", ("Company Identification", "Company", "Manufacturer")),
    ("supplier_address", ("Address",)),
    ("supplier_telephone", ("Telephone", "Tel")),
    ("supplier_fax", ("Fax",)),
    ("supplier_website", ("Website",)),
    ("supplier_email", ("Email",)),
    (
        "emergency_telephone",
        (
            "Emergency telephone number",
            "Emergency Phone #",
            "Emergency phone number",
            "Emergency telephone",
            "Emergency phone",
        ),
    ),
]

COMPANY_SUFFIX_RE = re.compile(
    r"^(?P<company>.*?\b(?:LLC|Ltd\.?|Co\.Ltd\.?|Company|Inc\.?|Corp\.?|Corporation|GmbH|KGaA|SA|AG)\b)(?:\s+(?P<rest>.*))?$",
    flags=re.IGNORECASE,
)
PHONE_RE = re.compile(r"(?:\+?\d[\d\s()./-]{5,}\d)")
ADDRESS_HINT_RE = re.compile(r"\b(?:Road|Rd|Street|St|Avenue|Ave|District|City|Village|Building|Floor|KY|USA|Germany|Beijing)\b", flags=re.IGNORECASE)


def _looks_like_cas(value: str | None) -> bool:
    if not value:
        return False
    return CAS_RE.fullmatch(normalize_text(value)) is not None


def _looks_like_product_code(value: str | None) -> bool:
    if not value:
        return False
    cleaned = normalize_text(value)
    if _looks_like_cas(cleaned):
        return False
    if " " in cleaned:
        return False
    return re.fullmatch(r"[A-Za-z]{0,4}\d{3,12}[A-Za-z0-9-]*", cleaned) is not None


def _looks_like_phone(value: str | None) -> bool:
    if not value:
        return False
    cleaned = normalize_text(value)
    digits = re.sub(r"\D", "", cleaned)
    return len(digits) >= 7 and PHONE_RE.fullmatch(cleaned) is not None


def _looks_like_address(value: str | None) -> bool:
    if not value:
        return False
    cleaned = normalize_text(value)
    if _looks_like_phone(cleaned):
        return False
    if re.fullmatch(r"\d+", cleaned):
        return False
    return bool(re.search(r"\d", cleaned) or ADDRESS_HINT_RE.search(cleaned) or "," in cleaned)


def _clean_section_value(value: str) -> str:
    cleaned = normalize_text(value)
    cleaned = re.sub(r"_+", "", cleaned).strip()
    cleaned = re.sub(r"\b1\.[234]\b.*$", "", cleaned).strip()
    cleaned = re.sub(r"\bRelevant identified uses of the substance or mixture and uses advised against\b.*$", "", cleaned, flags=re.IGNORECASE).strip()
    cleaned = re.sub(r"\bDetails of the supplier of the safety data sheet\b.*$", "", cleaned, flags=re.IGNORECASE).strip()
    return cleaned.strip(" :;-")


def _clean_phone_value(value: str) -> str | None:
    cleaned = _clean_section_value(value)
    phone_matches = PHONE_RE.findall(cleaned)
    if phone_matches:
        return " ".join(normalize_text(item) for item in phone_matches)
    return cleaned if _looks_like_phone(cleaned) else None


def _clean_company_value(value: str) -> tuple[str | None, str | None]:
    cleaned = _clean_section_value(value)
    cleaned = re.sub(r"\bPhone\s*:\s*.+$", "", cleaned, flags=re.IGNORECASE).strip()
    if not cleaned:
        return (None, None)
    match = COMPANY_SUFFIX_RE.match(cleaned)
    if not match:
        return (cleaned, None)
    company = normalize_text(match.group("company"))
    rest = normalize_text(match.group("rest") or "")
    address = rest if _looks_like_address(rest) else None
    return (company or None, address)


def _find_label_windows(text: str) -> list[tuple[str, str, int, int]]:
    matches: list[tuple[str, str, int, int]] = []
    for field_name, aliases in LABEL_PATTERNS:
        alias_group = "|".join(re.escape(alias) for alias in sorted(aliases, key=len, reverse=True))
        pattern = re.compile(rf"(?i)\b(?P<label>{alias_group})\b\s*[:#-]?\s*")
        for match in pattern.finditer(text):
            label = match.group("label")
            after = text[match.end():match.end() + 40]
            before = text[max(0, match.start() - 12):match.start()]
            if field_name == "supplier_telephone" and before.lower().endswith("emergency "):
                continue
            if field_name == "relevant_identified_uses" and label.lower() == "relevant identified uses" and after.lower().startswith("of the substance"):
                continue
            matches.append((field_name, label, match.start(), match.end()))
    matches.sort(key=lambda item: item[2])
    deduped: list[tuple[str, str, int, int]] = []
    last_start = None
    for item in matches:
        if item[2] == last_start:
            continue
        deduped.append(item)
        last_start = item[2]
    return deduped


def extract_section_01(ctx: ExtractionContext):
    text = ctx.section_text(1)
    if not text:
        return []

    candidates = []
    windows = _find_label_windows(text)
    values_by_field: dict[str, list[str]] = {}
    company_identification_value: str | None = None
    inferred_company_address: str | None = None

    for index, (field_name, label, _start, value_start) in enumerate(windows):
        next_start = windows[index + 1][2] if index + 1 < len(windows) else len(text)
        value = _clean_section_value(text[value_start:next_start])
        if not value:
            continue
        values_by_field.setdefault(field_name, []).append(value)

        if field_name == "supplier_company_name" and label.lower() == "company identification":
            company_identification_value = value
            continue

        if field_name == "product_identifier":
            if not _looks_like_product_code(value) and not _looks_like_cas(value):
                candidates.append(ctx.make_candidate(1, "product_identifier", value, extractor="section_01.product_identifier", confidence=0.9))
        elif field_name == "product_name":
            if not _looks_like_product_code(value) and not _looks_like_cas(value):
                candidates.append(ctx.make_candidate(1, "product_name", value, extractor="section_01.product_name", confidence=0.94))
        elif field_name == "product_number":
            if _looks_like_product_code(value):
                candidates.append(ctx.make_candidate(1, "product_number", value, extractor="section_01.product_number", confidence=0.9))
        elif field_name == "cas_number":
            if _looks_like_cas(value):
                candidates.append(ctx.make_candidate(1, "cas_number", normalize_text(value), extractor="section_01.cas_number", confidence=0.95))
        elif field_name == "synonyms":
            if value.lower().startswith("relevant identified uses of the substance"):
                continue
            synonym_list = split_tokens(value, delimiters=r"[,\n;]")
            if synonym_list:
                candidates.append(ctx.make_candidate(1, "synonyms", synonym_list, normalized_value=synonym_list, excerpt=value, extractor="section_01.synonyms", confidence=0.88))
        elif field_name == "relevant_identified_uses":
            candidates.append(ctx.make_candidate(1, "relevant_identified_uses", value, extractor="section_01.relevant_identified_uses", confidence=0.84))
        elif field_name == "uses_advised_against":
            if len(value) <= 160:
                candidates.append(ctx.make_candidate(1, "uses_advised_against", value, extractor="section_01.uses_advised_against", confidence=0.78))
        elif field_name == "supplier_company_name":
            company_name, inferred_address = _clean_company_value(value)
            if company_name:
                candidates.append(ctx.make_candidate(1, "supplier_company_name", company_name, extractor="section_01.supplier_company_name", confidence=0.82))
            if inferred_address and not inferred_company_address:
                inferred_company_address = inferred_address
        elif field_name == "supplier_address":
            if _looks_like_address(value):
                candidates.append(ctx.make_candidate(1, "supplier_address", value, extractor="section_01.supplier_address", confidence=0.8))
        elif field_name == "supplier_telephone":
            phone = _clean_phone_value(value)
            if phone:
                candidates.append(ctx.make_candidate(1, "supplier_telephone", phone, extractor="section_01.supplier_telephone", confidence=0.82))
        elif field_name == "supplier_fax":
            fax = _clean_phone_value(value)
            if fax:
                candidates.append(ctx.make_candidate(1, "supplier_fax", fax, extractor="section_01.supplier_fax", confidence=0.82))
        elif field_name == "supplier_website":
            candidates.append(ctx.make_candidate(1, "supplier_website", value, extractor="section_01.supplier_website", confidence=0.8))
        elif field_name == "supplier_email":
            candidates.append(ctx.make_candidate(1, "supplier_email", value, extractor="section_01.supplier_email", confidence=0.8))
        elif field_name == "emergency_telephone":
            emergency = _clean_phone_value(value)
            if emergency:
                candidates.append(ctx.make_candidate(1, "emergency_telephone", emergency, extractor="section_01.emergency_telephone", confidence=0.84))

    product_identifier_values = values_by_field.get("product_identifier", [])
    product_name_values = values_by_field.get("product_name", [])
    product_number_values = values_by_field.get("product_number", [])
    cas_values = values_by_field.get("cas_number", [])

    if product_identifier_values:
        product_identifier = product_identifier_values[0]
        if not any(candidate.field_path == "section_1.product_name" for candidate in candidates):
            candidates.append(ctx.make_candidate(1, "product_name", product_identifier, extractor="section_01.product_name", confidence=0.86))

    for value in product_name_values:
        if _looks_like_product_code(value):
            candidates.append(ctx.make_candidate(1, "product_number", value, extractor="section_01.product_number", confidence=0.84))

    for value in product_number_values:
        if _looks_like_cas(value):
            candidates.append(ctx.make_candidate(1, "cas_number", normalize_text(value), extractor="section_01.cas_number", confidence=0.9))

    for value in cas_values:
        if not _looks_like_cas(value) and any(token in value for token in (",", ";")):
            synonym_list = split_tokens(value, delimiters=r"[,\n;]")
            if synonym_list:
                candidates.append(ctx.make_candidate(1, "synonyms", synonym_list, normalized_value=synonym_list, excerpt=value, extractor="section_01.synonyms", confidence=0.82))

    if company_identification_value and not any(candidate.field_path == "section_1.supplier_company_name" for candidate in candidates):
        candidates.append(
            ctx.make_candidate(
                1,
                "supplier_company_name",
                company_identification_value,
                extractor="section_01.supplier_company_name",
                confidence=0.76,
            )
        )

    if inferred_company_address and not any(candidate.field_path == "section_1.supplier_address" for candidate in candidates):
        candidates.append(ctx.make_candidate(1, "supplier_address", inferred_company_address, extractor="section_01.supplier_address", confidence=0.72))

    ec_match = EC_RE.search(text)
    if ec_match:
        candidates.append(ctx.make_candidate(1, "ec_number", ec_match.group(0), extractor="section_01.ec_number", confidence=0.9))

    formula_match = re.search(r"\b(?:Formula|MF)\s*:\s*([A-Za-z0-9]+)", text, flags=re.IGNORECASE)
    if not formula_match:
        formula_match = FORMULA_RE.search(text)
    if formula_match:
        formula = normalize_text(formula_match.group(1) if formula_match.lastindex else formula_match.group(0))
        candidates.append(ctx.make_candidate(1, "molecular_formula", formula, extractor="section_01.molecular_formula", confidence=0.86))

    mw_match = MOLECULAR_WEIGHT_RE.search(text)
    if mw_match:
        candidates.append(ctx.make_candidate(1, "molecular_weight", mw_match.group(1), extractor="section_01.molecular_weight", confidence=0.86))

    if not any(candidate.field_path == "section_1.product_number" for candidate in candidates):
        match = PRODUCT_NUMBER_RE.search(text)
        product_number = match.group(3) if match else None
        if product_number:
            candidates.append(ctx.make_candidate(1, "product_number", product_number, extractor="section_01.product_number", confidence=0.82))

    if not any(candidate.field_path == "section_1.cas_number" for candidate in candidates):
        cas_match = CAS_RE.search(text)
        if cas_match:
            candidates.append(ctx.make_candidate(1, "cas_number", cas_match.group(0), extractor="section_01.cas_number", confidence=0.9))

    return deduplicate_candidates(candidates)
