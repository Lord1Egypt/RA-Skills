from __future__ import annotations

from dataclasses import dataclass

from sds_generator.config_loader import load_field_registry
from sds_generator.models import FinalSDSDocument, ReviewSeverity


@dataclass(slots=True, frozen=True)
class ReleaseGateDecision:
    critical_conflicts_present: bool
    blocking_field_paths: list[str]

    @property
    def release_eligible(self) -> bool:
        return not self.critical_conflicts_present and not self.blocking_field_paths


def _is_missing_value(value: object) -> bool:
    return value in (None, "", [], {})


def _blocking_missing_field_paths(final_document: FinalSDSDocument) -> set[str]:
    blocking_fields: set[str] = set()
    for entry in load_field_registry().get("fields", []):
        if not (entry.get("evidence_required") and entry.get("release_blocking")):
            continue
        field_path = str(entry["field_path"])
        section_key, field_name = field_path.split(".", 1)
        value = getattr(getattr(final_document, section_key), field_name)
        if _is_missing_value(value):
            blocking_fields.add(field_path)
    return blocking_fields


def evaluate_release_gate(final_document: FinalSDSDocument) -> ReleaseGateDecision:
    critical_conflicts_present = any(
        note.severity == ReviewSeverity.CRITICAL for note in final_document.audit.review_notes
    )
    blocking_field_paths = {
        note.field_path
        for note in final_document.audit.review_notes
        if note.release_blocking
    }
    blocking_field_paths.update(_blocking_missing_field_paths(final_document))
    return ReleaseGateDecision(
        critical_conflicts_present=critical_conflicts_present,
        blocking_field_paths=sorted(blocking_field_paths),
    )


def apply_release_gate(final_document: FinalSDSDocument) -> ReleaseGateDecision:
    decision = evaluate_release_gate(final_document)
    final_document.document_meta.critical_conflicts_present = decision.critical_conflicts_present
    final_document.document_meta.release_eligible = decision.release_eligible
    return decision
