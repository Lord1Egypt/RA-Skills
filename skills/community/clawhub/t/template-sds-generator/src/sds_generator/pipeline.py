from __future__ import annotations

import json
import re
import shutil
from datetime import UTC, datetime
from itertools import chain
from pathlib import Path
from typing import Any

from sds_generator.content_policy import apply_content_policy_defaults
from sds_generator.config_loader import PROJECT_ROOT, load_defaults, load_template_contract
from sds_generator.extraction import extract_document_candidates
from sds_generator.logging_utils import get_logger
from sds_generator.models import (
    ChecklistBucket,
    FieldCandidate,
    FinalSDSDocument,
    GenerationMode,
    OutputArtifacts,
    ReviewNote,
    ReviewSeverity,
    ReviewStatus,
    RunInputBundle,
    SourceValueEvidence,
)
from sds_generator.outputs.checklist_md import write_review_checklist
from sds_generator.outputs.content_policy import write_content_policy_report
from sds_generator.outputs.ocr_audit import write_ocr_audit_report
from sds_generator.outputs.run_manifest import write_run_manifest
from sds_generator.outputs.source_map_csv import write_field_source_map_csv, write_field_source_map_markdown
from sds_generator.outputs.structured_json import write_structured_json
from sds_generator.parsing.file_router import parse_inputs
from sds_generator.provenance_overrides import apply_override_provenance
from sds_generator.reconcile import reconcile_documents
from sds_generator.reconcile.release_gate import apply_release_gate
from sds_generator.render import build_docx, export_docx_to_pdf, validate_template_against_contract
from sds_generator.validation.schema_validation import validate_structured_data


def _slugify(value: str, max_length: int) -> str:
    slug = re.sub(r"[^a-zA-Z0-9]+", "-", value).strip("-").lower()
    if not slug:
        slug = "sds"
    return slug[:max_length].rstrip("-") or "sds"


def resolve_run_root(inputs: list[str | Path], *, outdir: Path | None, product_name: str | None) -> Path:
    if outdir is not None:
        return outdir
    defaults = load_defaults()
    outputs_root = PROJECT_ROOT / defaults.get("outputs", {}).get("root", "outputs/runs")
    slug_max_length = int(defaults.get("generation", {}).get("slug_max_length", 48))
    seed = product_name or Path(inputs[0]).stem
    timestamp = datetime.now(UTC).strftime("%Y%m%dT%H%M%SZ")
    return outputs_root / f"{timestamp}_{_slugify(seed, slug_max_length)}"


def build_output_artifacts(run_root: Path) -> OutputArtifacts:
    normalized_dir = run_root / "normalized"
    extracted_dir = run_root / "extracted"
    reconciled_dir = run_root / "reconciled"
    final_dir = run_root / "final"
    audit_dir = run_root / "audit"
    logs_dir = run_root / "logs"
    for directory in (normalized_dir, extracted_dir, reconciled_dir, final_dir, audit_dir, logs_dir):
        directory.mkdir(parents=True, exist_ok=True)
    return OutputArtifacts(
        run_root=run_root,
        normalized_dir=normalized_dir,
        extracted_dir=extracted_dir,
        reconciled_dir=reconciled_dir,
        final_dir=final_dir,
        audit_dir=audit_dir,
        logs_dir=logs_dir,
        run_manifest_path=run_root / "run_manifest.json",
        docx_path=final_dir / "sds_document.docx",
        pdf_path=None,
        template_fill_report_path=normalized_dir / "template_fill_report.json",
        structured_json_path=audit_dir / "structured_data.json",
        content_policy_report_path=audit_dir / "content_policy_report.json",
        ocr_audit_path=audit_dir / "ocr_audit.json",
        field_source_map_csv_path=audit_dir / "field_source_map.csv",
        field_source_map_md_path=audit_dir / "field_source_map.md",
        review_checklist_path=audit_dir / "review_checklist.md",
        log_path=logs_dir / "run.log",
    )


def _write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")


def _dump_parsed_documents(documents, artifacts: OutputArtifacts) -> None:
    for index, document in enumerate(documents, start=1):
        path = artifacts.normalized_dir / f"source_{index:02d}_blocks.json"
        _write_json(path, document.model_dump(mode="json"))


def _dump_ocr_audit(documents, artifacts: OutputArtifacts) -> None:
    if artifacts.ocr_audit_path is not None:
        write_ocr_audit_report(documents, artifacts.ocr_audit_path)


def _build_ocr_review_notes(documents) -> list[ReviewNote]:
    notes: list[ReviewNote] = []
    for document in documents:
        if not document.ocr_low_confidence_pages:
            continue
        pages = sorted(set(document.ocr_low_confidence_pages))
        notes.append(
            ReviewNote(
                field_path=f"source_document.{document.file_name}.ocr_low_confidence",
                severity=ReviewSeverity.MODERATE,
                status=ReviewStatus.WARNING,
                why=f"OCR confidence fell below the configured threshold on pages {pages}.",
                source_values=[
                    SourceValueEvidence(file=document.file_name, page=page, value="low_confidence_ocr")
                    for page in pages
                ],
                checklist_bucket=ChecklistBucket.OCR_LOW_CONFIDENCE,
            )
        )
    return notes


def _dump_input_bundle(input_bundle: RunInputBundle, artifacts: OutputArtifacts) -> None:
    _write_json(artifacts.normalized_dir / "input_bundle.json", input_bundle.model_dump(mode="json"))


def _dump_template_validation_report(report, artifacts: OutputArtifacts) -> None:
    _write_json(artifacts.normalized_dir / "template_validation_report.json", report.model_dump(mode="json"))


def _dump_candidates(documents, candidates: list[FieldCandidate], artifacts: OutputArtifacts) -> None:
    for index, document in enumerate(documents, start=1):
        document_candidates = [
            candidate.model_dump(mode="json")
            for candidate in candidates
            if candidate.source_file == document.file_name
        ]
        path = artifacts.extracted_dir / f"source_{index:02d}_candidates.json"
        _write_json(path, document_candidates)


def _dump_reconciled(final_document: FinalSDSDocument, artifacts: OutputArtifacts) -> None:
    _write_json(artifacts.reconciled_dir / "final_model.json", final_document.model_dump(mode="json"))
    _write_json(
        artifacts.reconciled_dir / "review_notes.json",
        [note.model_dump(mode="json") for note in final_document.audit.review_notes],
    )


def _apply_overrides(final_document: FinalSDSDocument, *, product_name: str | None, cas: str | None) -> None:
    if product_name:
        final_document.section_1.product_name = product_name
        final_document.section_1.product_identifier = final_document.section_1.product_identifier or product_name
        final_document.document_meta.product_name_display = product_name
        final_document.document_meta.product_name_canonical = product_name
    if cas:
        final_document.section_1.cas_number = cas
        final_document.section_3.cas_number = cas
        final_document.document_meta.cas_number = cas
    

def _apply_section16_overrides(
    final_document: FinalSDSDocument,
    *,
    issue_date: str | None,
    revision_date: str | None,
    version: str | None,
) -> None:
    if issue_date:
        final_document.section_16.date_of_first_issue = issue_date
    if revision_date:
        final_document.section_16.revision_date = revision_date
    if version:
        final_document.section_16.version_number = version


def _append_override_notes(final_document: FinalSDSDocument, *, product_name: str | None, cas: str | None) -> None:
    if product_name:
        apply_override_provenance(
            field_rows=final_document.audit.field_source_map,
            review_notes=final_document.audit.review_notes,
            field_path="section_1.product_name",
            value=final_document.section_1.product_name,
            source_file="cli:--product-name",
            raw_excerpt=f"CLI override --product-name={product_name}",
            note_message="Product name was overridden by the CLI --product-name option.",
            note_status=ReviewStatus.WARNING,
            checklist_bucket=ChecklistBucket.SYSTEM_OVERRIDES,
        )
        if final_document.section_1.product_identifier == product_name:
            apply_override_provenance(
                field_rows=final_document.audit.field_source_map,
                review_notes=final_document.audit.review_notes,
                field_path="section_1.product_identifier",
                value=final_document.section_1.product_identifier,
                source_file="cli:--product-name",
                raw_excerpt=f"CLI override --product-name={product_name}",
                note_message="Product identifier was aligned to the CLI --product-name override.",
                note_status=ReviewStatus.WARNING,
                checklist_bucket=ChecklistBucket.SYSTEM_OVERRIDES,
            )
    if cas:
        for field_path in ("section_1.cas_number", "section_3.cas_number"):
            apply_override_provenance(
                field_rows=final_document.audit.field_source_map,
                review_notes=final_document.audit.review_notes,
                field_path=field_path,
                value=cas,
                source_file="cli:--cas",
                raw_excerpt=f"CLI override --cas={cas}",
                note_message=f"{field_path} was overridden by the CLI --cas option.",
                note_status=ReviewStatus.WARNING,
                checklist_bucket=ChecklistBucket.SYSTEM_OVERRIDES,
            )


def _append_section16_override_notes(
    final_document: FinalSDSDocument,
    *,
    issue_date: str | None,
    revision_date: str | None,
    version: str | None,
) -> None:
    override_specs = (
        ("section_16.date_of_first_issue", issue_date, "cli:--issue-date", "Issue date was overridden by the CLI --issue-date option."),
        ("section_16.revision_date", revision_date, "cli:--revision-date", "Revision date was overridden by the CLI --revision-date option."),
        ("section_16.version_number", version, "cli:--version", "Version number was overridden by the CLI --version option."),
    )
    for field_path, value, source_file, note_message in override_specs:
        if not value:
            continue
        apply_override_provenance(
            field_rows=final_document.audit.field_source_map,
            review_notes=final_document.audit.review_notes,
            field_path=field_path,
            value=value,
            source_file=source_file,
            raw_excerpt=f"CLI override {source_file.split(':', 1)[1]}={value}",
            note_message=note_message,
            note_status=ReviewStatus.WARNING,
            checklist_bucket=ChecklistBucket.SYSTEM_OVERRIDES,
        )


def _copy_release_artifacts(artifacts: OutputArtifacts) -> None:
    release_dir = artifacts.run_root / "release"
    release_dir.mkdir(parents=True, exist_ok=True)
    for path in (
        artifacts.docx_path,
        artifacts.pdf_path,
        artifacts.run_manifest_path,
        artifacts.structured_json_path,
        artifacts.content_policy_report_path,
        artifacts.ocr_audit_path,
        artifacts.field_source_map_csv_path,
        artifacts.field_source_map_md_path,
        artifacts.review_checklist_path,
    ):
        if path is not None and path.exists():
            shutil.copy2(path, release_dir / path.name)


def _sync_final_bundle(artifacts: OutputArtifacts) -> None:
    for path in (
        artifacts.run_manifest_path,
        artifacts.structured_json_path,
        artifacts.content_policy_report_path,
        artifacts.field_source_map_csv_path,
        artifacts.field_source_map_md_path,
        artifacts.review_checklist_path,
    ):
        if path is not None and path.exists():
            shutil.copy2(path, artifacts.final_dir / path.name)


def generate_sds_package(
    inputs: list[str | Path] | None = None,
    *,
    input_bundle: RunInputBundle | None = None,
    outdir: Path | None = None,
    mode: GenerationMode = GenerationMode.DRAFT,
    enable_ocr: bool = False,
    allow_estimated_physchem: bool = False,
    product_name: str | None = None,
    cas: str | None = None,
    issue_date: str | None = None,
    revision_date: str | None = None,
    version: str | None = None,
) -> tuple[FinalSDSDocument, OutputArtifacts]:
    if input_bundle is not None:
        source_inputs = [str(path) for path in input_bundle.evidence_paths]
    elif inputs is not None:
        source_inputs = [str(path) for path in inputs]
    else:
        raise ValueError("Either inputs or input_bundle must be supplied.")

    run_root = resolve_run_root(source_inputs, outdir=outdir, product_name=product_name)
    artifacts = build_output_artifacts(run_root)
    logger = get_logger(name=f"sds_generator.{run_root.name}", log_file=artifacts.log_path)
    logger.info("Starting SDS generation in %s mode", mode.value)
    if allow_estimated_physchem:
        logger.info("Estimated physical/chemical data override enabled for this run.")
    if input_bundle is not None:
        logger.info("Using template asset %s", input_bundle.template_docx.name)
        logger.info("Using prompt rules asset %s", input_bundle.prompt_file.name)
        _dump_input_bundle(input_bundle, artifacts)
        template_contract = load_template_contract()
        template_report = validate_template_against_contract(input_bundle.template_docx, template_contract)
        _dump_template_validation_report(template_report, artifacts)
        logger.info(
            "Validated template %s against contract v%s",
            input_bundle.template_docx.name,
            template_report.contract_version,
        )

    documents = parse_inputs(source_inputs, enable_ocr=enable_ocr, logger=logger)
    _dump_parsed_documents(documents, artifacts)
    _dump_ocr_audit(documents, artifacts)

    candidates = list(chain.from_iterable(extract_document_candidates(document) for document in documents))
    _dump_candidates(documents, candidates, artifacts)

    final_document = reconcile_documents(documents, candidates, mode=mode)
    if input_bundle is not None:
        final_document.document_meta.template_file = input_bundle.template_docx.name
        final_document.document_meta.prompt_file = input_bundle.prompt_file.name
    final_document.audit.review_notes.extend(_build_ocr_review_notes(documents))
    apply_content_policy_defaults(final_document)
    _apply_overrides(final_document, product_name=product_name, cas=cas)
    _apply_section16_overrides(
        final_document,
        issue_date=issue_date,
        revision_date=revision_date,
        version=version,
    )
    _append_override_notes(final_document, product_name=product_name, cas=cas)
    _append_section16_override_notes(
        final_document,
        issue_date=issue_date,
        revision_date=revision_date,
        version=version,
    )
    apply_release_gate(final_document)
    _dump_reconciled(final_document, artifacts)

    _docx_path, docx_notes = build_docx(
        final_document,
        artifacts.docx_path,
        template_path=input_bundle.template_docx if input_bundle is not None else None,
        preserve_template_layout=input_bundle is not None,
        template_fill_report_path=artifacts.template_fill_report_path if input_bundle is not None else None,
    )
    final_document.audit.review_notes.extend(docx_notes)

    pdf_path, pdf_notes = export_docx_to_pdf(artifacts.docx_path, artifacts.final_dir)
    artifacts.pdf_path = pdf_path
    final_document.audit.review_notes.extend(pdf_notes)
    apply_release_gate(final_document)

    structured_output = write_structured_json(final_document, artifacts.structured_json_path)
    validate_structured_data(artifacts.structured_json_path)
    if artifacts.content_policy_report_path is not None:
        write_content_policy_report(final_document, artifacts.content_policy_report_path, structured_output=structured_output)
    write_field_source_map_csv(final_document, artifacts.field_source_map_csv_path, structured_output=structured_output)
    if artifacts.field_source_map_md_path is not None:
        write_field_source_map_markdown(final_document, artifacts.field_source_map_md_path, structured_output=structured_output)
    write_review_checklist(
        final_document.audit.review_notes,
        artifacts.review_checklist_path,
        release_eligible=final_document.document_meta.release_eligible,
        final_document=final_document,
    )
    write_run_manifest(
        documents=documents,
        final_document=final_document,
        artifacts=artifacts,
        settings={
            "enable_ocr": enable_ocr,
            "allow_estimated_physchem": allow_estimated_physchem,
            "mode": mode.value,
            "product_name_override": product_name,
            "cas_override": cas,
            "issue_date_override": issue_date,
            "revision_date_override": revision_date,
            "version_override": version,
        },
    )
    _sync_final_bundle(artifacts)

    if mode == GenerationMode.RELEASE and final_document.document_meta.release_eligible:
        _copy_release_artifacts(artifacts)

    logger.info("Generated DOCX at %s", artifacts.docx_path)
    if artifacts.pdf_path is not None:
        logger.info("Generated PDF at %s", artifacts.pdf_path)
    logger.info("Generated structured audit outputs under %s", artifacts.audit_dir)
    return final_document, artifacts
