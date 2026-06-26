from __future__ import annotations

from pathlib import Path
from typing import Any

from sds_generator.constants import NO_DATA, SECTION_TITLES
from sds_generator.models import FinalSDSDocument, InventoryStatusEntry
from sds_generator.render.pictograms import render_pictogram_line
from sds_generator.render.styles import BODY_STYLE, LABEL_STYLE, SECTION_STYLE, apply_section_rule
from sds_generator.render.tables import add_key_value_table, add_matrix_table, render_section14_table, render_section3_table, render_section9_table

FIELD_LABEL_OVERRIDES = {
    "product_identifier": "Product identifier",
    "product_name": "Product name",
    "product_number": "Product number",
    "cas_number": "CAS No.",
    "ec_number": "EC No.",
    "molecular_formula": "Molecular formula",
    "molecular_weight": "Molecular weight",
    "relevant_identified_uses": "Relevant identified uses",
    "uses_advised_against": "Uses advised against",
    "supplier_company_name": "Supplier company name",
    "supplier_address": "Supplier address",
    "supplier_telephone": "Supplier telephone",
    "supplier_fax": "Supplier fax",
    "supplier_website": "Supplier website",
    "supplier_email": "Supplier email",
    "emergency_telephone": "Emergency telephone",
    "prepared_by": "Prepared by",
    "ghs_classifications": "GHS classifications",
    "signal_word": "Signal word",
    "hazard_statements": "Hazard statements",
    "precautionary_prevention": "Precautionary statements - prevention",
    "precautionary_response": "Precautionary statements - response",
    "precautionary_storage": "Precautionary statements - storage",
    "precautionary_disposal": "Precautionary statements - disposal",
    "hazards_not_otherwise_classified": "Hazards not otherwise classified",
    "summary_of_emergency": "Emergency overview",
    "physical_hazards": "Physical hazards",
    "health_hazards": "Health hazards",
    "environmental_hazards": "Environmental hazards",
    "other_hazards": "Other hazards",
    "substance_or_mixture": "Substance / Mixture",
    "common_name_and_synonyms": "Common name and synonyms",
    "occupational_exposure_limits": "Occupational exposure limits",
    "biological_limits": "Biological limits",
    "engineering_controls": "Engineering controls",
    "eye_face_protection": "Eye / face protection",
    "hand_protection": "Hand protection",
    "skin_body_protection": "Skin / body protection",
    "respiratory_protection": "Respiratory protection",
    "waste_treatment_methods_product": "Waste treatment methods - product",
    "waste_treatment_methods_packaging": "Waste treatment methods - packaging",
    "transport_general_statement": "Transport general statement",
    "un_number": "UN No.",
    "un_proper_shipping_name": "UN proper shipping name",
    "transport_hazard_class": "Transport hazard class",
    "packing_group": "Packing group",
    "transport_in_bulk": "Transport in bulk",
    "dot_status": "DOT status",
    "adr_rid_status": "ADR/RID status",
    "imdg_status": "IMDG status",
    "iata_status": "IATA status",
    "regulatory_specific": "Regulatory specific information",
    "inventory_statuses": "Inventory statuses",
    "sara_302": "SARA 302",
    "sara_313": "SARA 313",
    "sara_311_312": "SARA 311/312",
    "proposition_65": "Proposition 65",
    "china_registration": "China registration",
    "revision_date": "Revision date",
    "version_number": "Version number",
    "date_of_first_issue": "Date of first issue",
    "abbreviations_and_acronyms": "Abbreviations and acronyms",
    "full_text_h_statements": "Full text hazard statements",
}


def display_value(value: Any) -> str:
    if value in (None, "", [], {}):
        return NO_DATA
    if isinstance(value, bool):
        return "Yes" if value else "No"
    if isinstance(value, str):
        return value
    if isinstance(value, list):
        items = [display_value(item) for item in value if item not in (None, "", [], {})]
        return "\n".join(items) if items else NO_DATA
    return str(value)


def prettify_field_name(field_name: str) -> str:
    if field_name in FIELD_LABEL_OVERRIDES:
        return FIELD_LABEL_OVERRIDES[field_name]
    label = field_name.replace("_", " ")
    label = label.replace(" pH", " pH").replace(" ghs ", " GHS ")
    return label.capitalize()


def _add_heading(document, section_number: int) -> None:
    paragraph = document.add_paragraph(style=SECTION_STYLE)
    paragraph.add_run(SECTION_TITLES[section_number])
    apply_section_rule(paragraph)


def _add_label_value(document, label: str, value: Any) -> None:
    paragraph = document.add_paragraph(style=BODY_STYLE)
    paragraph.add_run(f"{label}: ").bold = True
    paragraph.add_run(display_value(value))


def _section_fields(section_model) -> list[tuple[str, Any]]:
    values: list[tuple[str, Any]] = []
    for field_name in section_model.model_fields:
        values.append((prettify_field_name(field_name), getattr(section_model, field_name)))
    return values


def _render_inventory_statuses(document, entries: list[InventoryStatusEntry]) -> None:
    rows = []
    for entry in entries:
        rows.append([entry.jurisdiction, entry.status, entry.details])
    if not rows:
        rows = [[NO_DATA, NO_DATA, NO_DATA]]
    add_matrix_table(
        document,
        ["Jurisdiction", "Status", "Details"],
        rows,
        column_widths_cm=[4.0, 4.0, 8.0],
    )


def _render_generic_section(document, section_model) -> None:
    for label, value in _section_fields(section_model):
        _add_label_value(document, label, value)


def _render_section_1(document, section_model) -> None:
    priority_fields = [
        ("Product identifier", section_model.product_identifier),
        ("Product name", section_model.product_name),
        ("Synonyms", section_model.synonyms),
        ("Product number", section_model.product_number),
        ("CAS No.", section_model.cas_number),
        ("Molecular formula", section_model.molecular_formula),
        ("Molecular weight", section_model.molecular_weight),
        ("Relevant identified uses", section_model.relevant_identified_uses),
        ("Uses advised against", section_model.uses_advised_against),
        ("Supplier company name", section_model.supplier_company_name),
        ("Supplier address", section_model.supplier_address),
        ("Supplier telephone", section_model.supplier_telephone),
        ("Supplier fax", section_model.supplier_fax),
        ("Supplier website", section_model.supplier_website),
        ("Supplier email", section_model.supplier_email),
        ("Emergency telephone", section_model.emergency_telephone),
        ("Prepared by", section_model.prepared_by),
    ]
    for label, value in priority_fields:
        _add_label_value(document, label, value)


def _render_section_2(document, section_model, *, assets_root: Path | None, warning_sink: list[tuple[str, str]]) -> None:
    _add_label_value(document, "GHS classifications", section_model.ghs_classifications)
    pictogram_label = document.add_paragraph(style=LABEL_STYLE)
    pictogram_label.add_run("Pictograms")
    pictogram_paragraph = document.add_paragraph(style=BODY_STYLE)
    for message in render_pictogram_line(pictogram_paragraph, section_model.pictograms, assets_root=assets_root):
        warning_sink.append(("section_2.pictograms", message))
    _add_label_value(document, "Signal word", section_model.signal_word)
    _add_label_value(document, "Hazard statements", section_model.hazard_statements)
    _add_label_value(document, "Precautionary statements - prevention", section_model.precautionary_prevention)
    _add_label_value(document, "Precautionary statements - response", section_model.precautionary_response)
    _add_label_value(document, "Precautionary statements - storage", section_model.precautionary_storage)
    _add_label_value(document, "Precautionary statements - disposal", section_model.precautionary_disposal)
    _add_label_value(document, "Hazards not otherwise classified", section_model.hazards_not_otherwise_classified)
    _add_label_value(document, "Emergency overview", section_model.summary_of_emergency)
    _add_label_value(document, "Physical hazards", section_model.physical_hazards)
    _add_label_value(document, "Health hazards", section_model.health_hazards)
    _add_label_value(document, "Environmental hazards", section_model.environmental_hazards)
    _add_label_value(document, "Other hazards", section_model.other_hazards)


def _render_section_15(document, section_model) -> None:
    scalar_rows = [
        ("Regulatory specific information", section_model.regulatory_specific),
        ("SARA 302", section_model.sara_302),
        ("SARA 313", section_model.sara_313),
        ("SARA 311/312", section_model.sara_311_312),
        ("Proposition 65", section_model.proposition_65),
        ("China registration", section_model.china_registration),
        ("Other regulations", section_model.other_regulations),
    ]
    add_key_value_table(document, scalar_rows)
    inventory_label = document.add_paragraph(style=LABEL_STYLE)
    inventory_label.add_run("Inventory statuses")
    _render_inventory_statuses(document, section_model.inventory_statuses)


def _render_section_16(document, section_model) -> None:
    scalar_rows = [
        ("Revision date", section_model.revision_date),
        ("Version number", section_model.version_number),
        ("Date of first issue", section_model.date_of_first_issue),
        ("Disclaimer", section_model.disclaimer),
        ("Additional information", section_model.additional_information),
    ]
    add_key_value_table(document, scalar_rows)
    _add_label_value(document, "Abbreviations and acronyms", section_model.abbreviations_and_acronyms)
    _add_label_value(document, "Full text hazard statements", section_model.full_text_h_statements)
    _add_label_value(document, "References", section_model.references)


def render_sections(
    document,
    final_document: FinalSDSDocument,
    *,
    assets_root: Path | None = None,
) -> list[tuple[str, str]]:
    warning_sink: list[tuple[str, str]] = []
    for section_key, section_model in final_document.ordered_sections():
        section_number = int(section_key.split("_", 1)[1])
        _add_heading(document, section_number)
        if section_key == "section_1":
            _render_section_1(document, section_model)
        elif section_key == "section_2":
            _render_section_2(document, section_model, assets_root=assets_root, warning_sink=warning_sink)
        elif section_key == "section_3":
            render_section3_table(document, section_model)
        elif section_key == "section_9":
            render_section9_table(document, section_model)
        elif section_key == "section_14":
            render_section14_table(document, section_model)
        elif section_key == "section_15":
            _render_section_15(document, section_model)
        elif section_key == "section_16":
            _render_section_16(document, section_model)
        else:
            _render_generic_section(document, section_model)
    return warning_sink
