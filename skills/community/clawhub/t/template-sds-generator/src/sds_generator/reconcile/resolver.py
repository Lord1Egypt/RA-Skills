from __future__ import annotations

from collections import defaultdict
from itertools import chain
from typing import Any

from sds_generator.config_loader import load_fixed_company
from sds_generator.extraction import extract_document_candidates
from sds_generator.models import (
    CandidateEquivalenceGroup,
    ChecklistBucket,
    FieldCandidate,
    FieldSourceMapRow,
    FinalSDSDocument,
    GenerationMode,
    ReviewSeverity,
    ReviewStatus,
    SourceSummary,
    ValueStatus,
)
from sds_generator.normalization import normalize_name, normalize_temperature, normalize_un_number
from sds_generator.provenance_overrides import apply_override_provenance
from sds_generator.reconcile.critical_fields import (
    is_critical_field,
    should_force_no_data_for_single_low_authority,
)
from sds_generator.reconcile.equivalence import build_equivalence_groups, canonicalize_value
from sds_generator.reconcile.policy import get_policy
from sds_generator.reconcile.release_gate import apply_release_gate
from sds_generator.reconcile.review_notes import build_review_note
from sds_generator.reconcile.scorer import rank_group, rank_group_authority_first, rank_group_for_field


def _source_summaries(documents) -> list[SourceSummary]:
    return [
        SourceSummary(
            file_name=document.file_name,
            source_profile=document.source_profile,
            source_authority=document.source_authority,
            revision_date=document.revision_date,
        )
        for document in documents
    ]


def _set_field(final_document: FinalSDSDocument, field_path: str, value: Any) -> None:
    section_name, field_name = field_path.split(".", 1)
    section = getattr(final_document, section_name)
    current_value = getattr(section, field_name)
    if isinstance(current_value, list):
        if value is None:
            coerced = []
        elif isinstance(value, tuple):
            coerced = list(value)
        elif isinstance(value, list):
            coerced = value
        else:
            coerced = [value]
        setattr(section, field_name, coerced)
        return
    if isinstance(value, tuple):
        setattr(section, field_name, value[0] if len(value) == 1 else list(value))
        return
    setattr(section, field_name, value)


def _select_group(field_path: str, groups: list[CandidateEquivalenceGroup]) -> CandidateEquivalenceGroup | None:
    if not groups:
        return None
    scorer = rank_group_for_field if groups else None
    return sorted(groups, key=lambda group: scorer(field_path, group), reverse=True)[0]


def _selection_metadata(
    *,
    field_path: str,
    selected_group: CandidateEquivalenceGroup | None,
    review_notes: list,
) -> tuple[str | None, str | None]:
    if selected_group is None:
        return (None, None)

    field_notes = [note for note in review_notes if note.field_path == field_path]
    if any(note.status == ReviewStatus.CONFLICT_RESOLVED_CONSERVATIVE for note in field_notes):
        note = next(note for note in field_notes if note.status == ReviewStatus.CONFLICT_RESOLVED_CONSERVATIVE)
        return ("conservative_conflict_resolution", note.why)

    if len(selected_group.candidates) > 1:
        return ("highest_authority_consensus", "Multiple supporting sources agreed on the selected normalized value.")

    if is_critical_field(field_path):
        return ("highest_authority_selected", "Selected the highest-authority supported value for a regulated critical field.")

    return (
        "highest_ranked_narrative_value",
        "Selected the highest-ranked narrative evidence using completeness, specificity, authority, and recency.",
    )


def _mode_conflict(mode_candidates: list[dict[str, Any]]) -> bool:
    has_hazardous = any(candidate.get("un_number") not in (None, "", "-") for candidate in mode_candidates)
    has_not_dangerous = any(candidate.get("status_note") == "Not dangerous goods" for candidate in mode_candidates)
    return has_hazardous and has_not_dangerous


def _resolve_transport_modes(
    field_path: str,
    candidates: list[FieldCandidate],
    final_document: FinalSDSDocument,
    rows: list[FieldSourceMapRow],
):
    policy = get_policy()
    mode_to_entries: dict[str, list[tuple[FieldCandidate, dict[str, Any]]]] = defaultdict(list)
    for candidate in candidates:
        for mode in candidate.normalized_value:
            mode_to_entries[mode["mode"]].append((candidate, mode))

    selected_modes: list[dict[str, Any]] = []
    review_notes = []
    for mode_name in ("dot", "adr_rid", "imdg", "iata"):
        entries = mode_to_entries.get(mode_name, [])
        if not entries:
            continue
        mode_values = [entry for _candidate, entry in entries]
        conflict = _mode_conflict(mode_values)

        if mode_name == "adr_rid" and conflict:
            hazardous_entries = [entry for _candidate, entry in entries if entry.get("un_number") not in (None, "", "-")]
            if len(hazardous_entries) <= 1 and policy.prefer_conservative_transport_resolution:
                review_notes.append(
                    build_review_note(
                        field_path=field_path,
                        severity=ReviewSeverity.CRITICAL,
                        status=ReviewStatus.FORCED_NO_DATA,
                        chosen_value=None,
                        why="ADR/RID transport is supported only by a single low-authority source while Sigma-Aldrich contradicts it. Default conservative policy keeps ADR/RID unresolved.",
                        candidates=[candidate for candidate, _entry in entries],
                        release_blocking=True,
                        checklist_bucket=ChecklistBucket.CRITICAL_CONFLICTS,
                    )
                )
                continue

        def mode_rank(entry: tuple[FieldCandidate, dict[str, Any]]) -> tuple[int, int, int]:
            candidate, payload = entry
            completeness = sum(
                1
                for key in ("status_note", "un_number", "hazard_class", "packing_group", "proper_shipping_name", "marine_pollutant")
                if payload.get(key)
            )
            specificity = sum(len(str(payload.get(key, ""))) for key in ("proper_shipping_name", "un_number", "hazard_class", "packing_group"))
            return (completeness, specificity, candidate.source_authority)

        if conflict and mode_name in {"imdg", "iata"} and policy.prefer_conservative_transport_resolution:
            hazardous_entries = [entry for entry in entries if entry[1].get("un_number") not in (None, "", "-")]
            selected_candidate, selected_mode = (
                sorted(hazardous_entries, key=mode_rank, reverse=True)[0]
                if hazardous_entries
                else sorted(entries, key=mode_rank, reverse=True)[0]
            )
        else:
            selected_candidate, selected_mode = sorted(entries, key=mode_rank, reverse=True)[0]
        selected_modes.append(selected_mode)

        if conflict and mode_name in {"imdg", "iata"}:
            review_notes.append(
                build_review_note(
                    field_path=field_path,
                    severity=ReviewSeverity.CRITICAL,
                    status=ReviewStatus.CONFLICT_RESOLVED_CONSERVATIVE,
                    chosen_value=selected_mode,
                    why=f"{mode_name.upper()} transport is contradicted across sources. Conservative directly-supported hazardous transport data was selected and requires human review.",
                    candidates=[candidate for candidate, _entry in entries],
                    release_blocking=True,
                    checklist_bucket=ChecklistBucket.CRITICAL_CONFLICTS,
                )
            )

    if selected_modes:
        final_document.section_14.transport_modes = selected_modes
        un_numbers = {
            normalized
            for mode in selected_modes
            if mode.get("un_number")
            for normalized in [normalize_un_number(mode.get("un_number"))]
            if normalized
        }
        hazard_classes = {mode.get("hazard_class") for mode in selected_modes if mode.get("hazard_class") not in (None, "-")}
        packing_groups = {mode.get("packing_group") for mode in selected_modes if mode.get("packing_group") not in (None, "-")}
        if len(un_numbers) == 1:
            final_document.section_14.un_number = un_numbers.pop()
        if len(hazard_classes) == 1:
            final_document.section_14.transport_hazard_class = hazard_classes.pop()
        if len(packing_groups) == 1:
            final_document.section_14.packing_group = packing_groups.pop()

    selected_mode_keys = {mode["mode"] for mode in selected_modes}
    selection_reason = "conservative_conflict_resolution" if review_notes else "highest_authority_selected"
    selection_detail = (
        "Selected directly-supported hazardous transport data conservatively because sources disagreed by mode."
        if review_notes
        else "Selected the highest-authority mode-specific transport data."
    )
    for candidate in candidates:
        selected = any(mode["mode"] in selected_mode_keys for mode in candidate.normalized_value)
        rows.append(
            FieldSourceMapRow(
                field_path=field_path,
                selected=selected,
                selection_reason=selection_reason if selected else None,
                selection_detail=selection_detail if selected else None,
                display_value=str(candidate.normalized_value),
                status=ValueStatus.SELECTED if selected else ValueStatus.CANDIDATE_ONLY,
                source_file=candidate.source_file,
                source_profile=candidate.source_profile,
                source_authority=candidate.source_authority,
                source_revision_date=str(candidate.source_revision_date) if candidate.source_revision_date else None,
                page=candidate.page,
                section=candidate.section,
                raw_excerpt=candidate.excerpt,
                normalized_value=candidate.normalized_value,
                completeness_score=0,
                specificity_score=0,
                authority_score=candidate.source_authority,
                confidence=candidate.confidence,
                caveats=candidate.caveats,
                review_flag=any(note.field_path == field_path for note in review_notes),
            )
        )
    return review_notes


def reconcile_documents(
    documents,
    candidates: list[FieldCandidate] | None = None,
    *,
    mode: GenerationMode = GenerationMode.DRAFT,
) -> FinalSDSDocument:
    if candidates is None:
        candidates = list(chain.from_iterable(extract_document_candidates(document) for document in documents))
    policy = get_policy()
    final_document = FinalSDSDocument()
    final_document.document_meta.generation_mode = mode
    final_document.document_meta.input_files = [document.file_name for document in documents]
    final_document.document_meta.source_summary = _source_summaries(documents)

    grouped_candidates: dict[str, list[FieldCandidate]] = defaultdict(list)
    for candidate in candidates:
        grouped_candidates[candidate.field_path].append(candidate)

    review_notes = []
    field_rows: list[FieldSourceMapRow] = []

    for field_path, field_candidates in grouped_candidates.items():
        if field_path == "section_14.transport_modes":
            review_notes.extend(_resolve_transport_modes(field_path, field_candidates, final_document, field_rows))
            continue
        if field_path in {"section_14.un_number", "section_14.transport_hazard_class", "section_14.packing_group"}:
            continue

        groups = build_equivalence_groups(field_candidates)
        selected_group = _select_group(field_path, groups)
        selected_value = selected_group.normalized_value if selected_group else None

        if should_force_no_data_for_single_low_authority(
            field_path,
            field_candidates,
            policy_enabled=policy.single_low_authority_critical_numeric_to_no_data,
        ):
            selected_value = None
            review_notes.append(
                build_review_note(
                    field_path=field_path,
                    severity=ReviewSeverity.MODERATE,
                    status=ReviewStatus.FORCED_NO_DATA,
                    chosen_value=None,
                    why="Only a single low-authority source provided a critical numeric value. Default policy forces No data available until higher-authority support exists.",
                    candidates=field_candidates,
                    checklist_bucket=ChecklistBucket.FORCED_NO_DATA,
                )
            )

        elif len(groups) > 1:
            group_values = [group.normalized_value for group in groups]
            if field_path == "section_2.ghs_classifications" and any(
                "Not a hazardous substance or mixture" in str(group_value) for group_value in group_values
            ):
                hazardous_groups = [
                    group
                    for group in groups
                    if "Not a hazardous substance or mixture" not in str(group.normalized_value)
                ]
                if hazardous_groups:
                    selected_group = sorted(hazardous_groups, key=lambda group: rank_group_for_field(field_path, group), reverse=True)[0]
                    selected_value = selected_group.normalized_value
                review_notes.append(
                    build_review_note(
                        field_path=field_path,
                        severity=ReviewSeverity.CRITICAL,
                        status=ReviewStatus.CONFLICT_RESOLVED_CONSERVATIVE,
                        chosen_value=selected_value,
                        why="Advanced ChemTech and ChemicalBook identify aquatic hazards while Sigma-Aldrich states the product is not hazardous. Conservative directly-supported classification selected; human review required before release.",
                        candidates=field_candidates,
                        release_blocking=True,
                        checklist_bucket=ChecklistBucket.CRITICAL_CONFLICTS,
                    )
                )
            elif field_path in {"section_1.synonyms", "section_3.common_name_and_synonyms"}:
                review_notes.append(
                    build_review_note(
                        field_path=field_path,
                        severity=ReviewSeverity.MODERATE,
                        status=ReviewStatus.WARNING,
                        chosen_value=selected_value,
                        why="Source synonym quality differs. The more specific protected-compound synonyms were selected over generic aliases such as N-Methyl glutamic acid.",
                        candidates=field_candidates,
                        checklist_bucket=ChecklistBucket.SOURCE_CAVEATS,
                    )
                )

        if selected_value is not None:
            _set_field(final_document, field_path, selected_value)

        selection_reason, selection_detail = _selection_metadata(
            field_path=field_path,
            selected_group=selected_group if selected_value is not None else None,
            review_notes=review_notes,
        )

        for group in groups:
            selected = selected_group is not None and group.semantic_key == selected_group.semantic_key and selected_value is not None
            for candidate in group.candidates:
                field_rows.append(
                    FieldSourceMapRow(
                        field_path=field_path,
                        selected=selected,
                        selection_reason=selection_reason if selected else None,
                        selection_detail=selection_detail if selected else None,
                        display_value=str(selected_value) if selected_value is not None else "No data available",
                        status=ValueStatus.SELECTED if selected else ValueStatus.CANDIDATE_ONLY,
                        source_file=candidate.source_file,
                        source_profile=candidate.source_profile,
                        source_authority=candidate.source_authority,
                        source_revision_date=str(candidate.source_revision_date) if candidate.source_revision_date else None,
                        page=candidate.page,
                        section=candidate.section,
                        raw_excerpt=candidate.excerpt,
                        normalized_value=canonicalize_value(candidate.field_path, candidate.normalized_value),
                        completeness_score=group.completeness_score,
                        specificity_score=group.specificity_score,
                        authority_score=group.authority_score,
                        confidence=candidate.confidence,
                        caveats=candidate.caveats,
                        review_flag=any(note.field_path == field_path for note in review_notes),
                    )
                )

    fixed_company = load_fixed_company()
    final_document.section_1.supplier_company_name = fixed_company["company_name"]
    final_document.section_1.supplier_address = fixed_company["address"]
    final_document.section_1.supplier_telephone = fixed_company["telephone"]
    final_document.section_1.supplier_fax = fixed_company["fax"]
    final_document.section_1.supplier_website = fixed_company["website"]
    final_document.section_1.supplier_email = fixed_company["email"]
    final_document.section_1.emergency_telephone = fixed_company["emergency_telephone"]
    final_document.section_1.prepared_by = fixed_company["prepared_by"]
    fixed_company_overrides = {
        "section_1.supplier_company_name": final_document.section_1.supplier_company_name,
        "section_1.supplier_address": final_document.section_1.supplier_address,
        "section_1.supplier_telephone": final_document.section_1.supplier_telephone,
        "section_1.supplier_fax": final_document.section_1.supplier_fax,
        "section_1.supplier_website": final_document.section_1.supplier_website,
        "section_1.supplier_email": final_document.section_1.supplier_email,
        "section_1.emergency_telephone": final_document.section_1.emergency_telephone,
        "section_1.prepared_by": final_document.section_1.prepared_by,
    }
    for field_path, value in fixed_company_overrides.items():
        apply_override_provenance(
            field_rows=field_rows,
            review_notes=review_notes,
            field_path=field_path,
            value=value,
            source_file="config/fixed_company.yml",
            raw_excerpt="Applied fixed supplier block from config/fixed_company.yml.",
            note_message="Value replaced with the fixed supplier block from config/fixed_company.yml.",
            note_status=ReviewStatus.OVERRIDDEN_FIXED_COMPANY,
        )

    if not final_document.section_1.product_name:
        final_document.section_1.product_name = normalize_name(final_document.section_1.product_identifier)
    final_document.document_meta.product_name_display = final_document.section_1.product_name
    final_document.document_meta.product_name_canonical = final_document.section_1.product_name
    final_document.document_meta.cas_number = final_document.section_1.cas_number

    final_document.audit.review_notes = review_notes
    final_document.audit.field_source_map = field_rows
    apply_release_gate(final_document)
    return final_document
