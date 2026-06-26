from __future__ import annotations

from dataclasses import dataclass

from sds_generator.config_loader import load_reconciliation_policy


@dataclass(frozen=True)
class ReconciliationPolicy:
    default_mode: str
    critical_conflict_release_block: bool
    single_low_authority_critical_numeric_to_no_data: bool
    prefer_conservative_transport_resolution: bool


def get_policy() -> ReconciliationPolicy:
    payload = load_reconciliation_policy()
    return ReconciliationPolicy(
        default_mode=str(payload.get("default_mode", "conservative_with_review")),
        critical_conflict_release_block=bool(payload.get("critical_conflict_release_block", True)),
        single_low_authority_critical_numeric_to_no_data=bool(
            payload.get("single_low_authority_critical_numeric_to_no_data", True)
        ),
        prefer_conservative_transport_resolution=bool(
            payload.get("prefer_conservative_transport_resolution", True)
        ),
    )
