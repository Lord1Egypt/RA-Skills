from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass
import json
from typing import Any

from .client import SherpaDeskClient
from .db import finish_ingest_run, initialize_db, now_iso, start_ingest_run, upsert_ticket_details, upsert_tickets
from .documents import materialize_ticket_documents
from .settings import Settings
from .sync_state import set_json_state


@dataclass
class EnrichmentResult:
    status: str
    message: str
    stats: dict | None = None


def _build_client(settings: Settings) -> SherpaDeskClient:
    assert settings.api_key is not None
    return SherpaDeskClient(
        api_base_url=settings.api_base_url,
        api_key=settings.api_key,
        api_user=settings.api_user,
        org_key=settings.org_key,
        instance_key=settings.instance_key,
        timeout_seconds=settings.request_timeout_seconds,
        min_interval_seconds=settings.request_min_interval_seconds,
        request_tracking_db_path=settings.db_path,
    )


def _priority_rank(value: Any) -> int:
    normalized = str(value or "").strip().lower()
    ranks = {
        "critical": 0,
        "high": 1,
        "normal": 2,
        "medium": 2,
        "low": 3,
        "none": 4,
        "0": 5,
        "unknown": 6,
        "": 6,
    }
    return ranks.get(normalized, 6)


def _coverage_stats(rows: list[dict[str, Any]], key: str) -> dict[str, tuple[int, int]]:
    stats: dict[str, list[int]] = defaultdict(lambda: [0, 0])
    for row in rows:
        value = str(row.get(key) or "").strip() or "unknown"
        counts = stats[value]
        counts[0] += 1
        if row.get("has_detail"):
            counts[1] += 1
    return {value: (counts[0], counts[1]) for value, counts in stats.items()}


def _coverage_ratio(stats: dict[str, tuple[int, int]], value: Any) -> float:
    normalized = str(value or "").strip() or "unknown"
    total, covered = stats.get(normalized, (0, 0))
    if total <= 0:
        return 0.0
    return covered / total


def _retrieval_signal_stats(rows: list[dict[str, Any]], key: str) -> dict[str, tuple[int, int]]:
    signal_fields = (
        "has_detail",
        "has_issue_context",
        "has_action_context",
        "has_activity_context",
        "has_resolution_context",
        "has_attachment_context",
    )
    stats: dict[str, list[int]] = defaultdict(lambda: [0, 0])
    for row in rows:
        value = str(row.get(key) or "").strip() or "unknown"
        counts = stats[value]
        counts[0] += len(signal_fields)
        counts[1] += sum(1 for field in signal_fields if row.get(field))
    return {value: (counts[0], counts[1]) for value, counts in stats.items()}


def _retrieval_richness_ratio(stats: dict[str, tuple[int, int]], value: Any) -> float:
    normalized = str(value or "").strip() or "unknown"
    opportunities, hits = stats.get(normalized, (0, 0))
    if opportunities <= 0:
        return 0.0
    return hits / opportunities


def _hot_group_rows(rows: list[dict[str, Any]], bucket: int, has_detail: int) -> list[dict[str, Any]]:
    group = [row for row in rows if row["bucket"] == bucket and row["has_detail"] == has_detail]
    group.sort(key=lambda row: str(row.get("id") or ""), reverse=True)
    group.sort(key=lambda row: str(row.get("activity_at") or ""), reverse=True)
    group.sort(key=lambda row: _priority_rank(row.get("priority")))
    return group


def _cold_candidate_sort_key(
    row: dict[str, Any],
    category_stats: dict[str, tuple[int, int]],
    account_stats: dict[str, tuple[int, int]],
    technician_stats: dict[str, tuple[int, int]],
    category_signal_stats: dict[str, tuple[int, int]],
    account_signal_stats: dict[str, tuple[int, int]],
    technician_signal_stats: dict[str, tuple[int, int]],
) -> tuple:
    return (
        _retrieval_richness_ratio(category_signal_stats, row.get("category")),
        _coverage_ratio(category_stats, row.get("category")),
        _retrieval_richness_ratio(account_signal_stats, row.get("account_key")),
        _coverage_ratio(account_stats, row.get("account_key")),
        _retrieval_richness_ratio(technician_signal_stats, row.get("technician_key")),
        _coverage_ratio(technician_stats, row.get("technician_key")),
        _priority_rank(row.get("priority")),
        -len(str(row.get("category") or "")),
    )


def _prioritize_cold_candidates(
    rows: list[dict[str, Any]],
    remaining: int,
    coverage_rows: list[dict[str, Any]] | None = None,
) -> list[dict[str, Any]]:
    if remaining <= 0 or not rows:
        return []

    coverage_rows = coverage_rows or rows
    category_stats = _coverage_stats(coverage_rows, "category")
    account_stats = _coverage_stats(coverage_rows, "account_key")
    technician_stats = _coverage_stats(coverage_rows, "technician_key")
    category_signal_stats = _retrieval_signal_stats(coverage_rows, "category")
    account_signal_stats = _retrieval_signal_stats(coverage_rows, "account_key")
    technician_signal_stats = _retrieval_signal_stats(coverage_rows, "technician_key")
    ordered = list(rows)
    ordered.sort(key=lambda row: str(row.get("id") or ""), reverse=True)
    ordered.sort(key=lambda row: str(row.get("activity_at") or ""), reverse=True)
    ordered.sort(
        key=lambda row: _cold_candidate_sort_key(
            row,
            category_stats,
            account_stats,
            technician_stats,
            category_signal_stats,
            account_signal_stats,
            technician_signal_stats,
        )
    )

    selected: list[dict[str, Any]] = []
    seen_ids: set[str] = set()
    seen_categories: set[str] = set()
    seen_accounts: set[str] = set()
    seen_technicians: set[str] = set()

    for row in ordered:
        if len(selected) >= remaining:
            break
        category = str(row.get("category") or "").strip() or "unknown"
        account = str(row.get("account_key") or "").strip() or "unknown"
        technician = str(row.get("technician_key") or "").strip() or "unknown"
        if category in seen_categories and account in seen_accounts and technician in seen_technicians:
            continue
        selected.append(row)
        seen_ids.add(str(row["id"]))
        seen_categories.add(category)
        seen_accounts.add(account)
        seen_technicians.add(technician)

    for row in ordered:
        if len(selected) >= remaining:
            break
        row_id = str(row["id"])
        if row_id in seen_ids:
            continue
        selected.append(row)
        seen_ids.add(row_id)

    return selected


def _candidate_ticket_rows(db_path, limit: int) -> list[dict]:
    from .db import connect

    with connect(db_path) as conn:
        rows = conn.execute(
            """
            WITH prioritized AS (
                SELECT t.id,
                       CASE
                           WHEN t.status = 'Open' THEN 0
                           WHEN t.status = 'Closed'
                                AND t.closed_at IS NOT NULL
                                AND julianday(REPLACE(substr(t.closed_at, 1, 19), 'T', ' ')) >= julianday('now', '-7 days') THEN 1
                           ELSE 2
                       END AS bucket,
                       CASE WHEN td.ticket_id IS NULL THEN 0 ELSE 1 END AS has_detail,
                       COALESCE(t.updated_at, t.created_at) AS activity_at,
                       t.priority,
                       COALESCE(
                           NULLIF(t.category, ''),
                           NULLIF(json_extract(t.raw_json, '$.creation_category_name'), ''),
                           NULLIF(json_extract(t.raw_json, '$.class_name'), ''),
                           NULLIF(json_extract(t.raw_json, '$.submission_category'), ''),
                           'unknown'
                       ) AS category,
                       COALESCE(NULLIF(t.account_id, ''), 'unknown') AS account_key,
                       COALESCE(NULLIF(t.assigned_technician_id, ''), 'unknown') AS technician_key,
                       CASE
                           WHEN COALESCE(
                               json_extract(doc.raw_json, '$.metadata.cleaned_initial_post'),
                               json_extract(doc.raw_json, '$.metadata.cleaned_detail_note'),
                               json_extract(doc.raw_json, '$.metadata.cleaned_workpad')
                           ) IS NOT NULL THEN 1 ELSE 0
                       END AS has_issue_context,
                       CASE
                           WHEN COALESCE(
                               json_extract(doc.raw_json, '$.metadata.cleaned_next_step'),
                               json_extract(doc.raw_json, '$.metadata.cleaned_action_cue'),
                               json_extract(doc.raw_json, '$.metadata.cleaned_followup_note'),
                               json_extract(doc.raw_json, '$.metadata.cleaned_request_completion_note')
                           ) IS NOT NULL THEN 1 ELSE 0
                       END AS has_action_context,
                       CASE
                           WHEN COALESCE(CAST(json_extract(doc.raw_json, '$.metadata.ticketlogs_count') AS REAL), 0) > 0
                                OR COALESCE(
                                    json_extract(doc.raw_json, '$.metadata.recent_log_types_csv'),
                                    json_extract(doc.raw_json, '$.metadata.latest_response_date'),
                                    json_extract(doc.raw_json, '$.metadata.latest_public_log_date'),
                                    json_extract(doc.raw_json, '$.metadata.latest_internal_log_date'),
                                    json_extract(doc.raw_json, '$.metadata.participant_email_domains_csv'),
                                    json_extract(doc.raw_json, '$.metadata.recent_public_actor_labels_csv'),
                                    json_extract(doc.raw_json, '$.metadata.recent_internal_actor_labels_csv')
                                ) IS NOT NULL THEN 1 ELSE 0
                       END AS has_activity_context,
                       CASE
                           WHEN COALESCE(
                               json_extract(doc.raw_json, '$.metadata.resolution_summary'),
                               json_extract(doc.raw_json, '$.metadata.cleaned_resolution_log_note'),
                               json_extract(doc.raw_json, '$.metadata.resolution_category')
                           ) IS NOT NULL THEN 1 ELSE 0
                       END AS has_resolution_context,
                       CASE
                           WHEN COALESCE(CAST(json_extract(doc.raw_json, '$.metadata.attachments_count') AS REAL), 0) > 0
                                OR COALESCE(CAST(json_extract(doc.raw_json, '$.metadata.attachment_total_size_bytes') AS REAL), 0) > 0
                                OR COALESCE(
                                    json_extract(doc.raw_json, '$.metadata.attachment_extensions_csv'),
                                    json_extract(doc.raw_json, '$.metadata.attachment_kinds_csv')
                                ) IS NOT NULL THEN 1 ELSE 0
                       END AS has_attachment_context
                FROM tickets t
                LEFT JOIN ticket_details td ON td.ticket_id = t.id
                LEFT JOIN ticket_documents doc ON doc.ticket_id = t.id
            )
            SELECT id,
                   bucket,
                   has_detail,
                   activity_at,
                   priority,
                   category,
                   account_key,
                   technician_key,
                   has_issue_context,
                   has_action_context,
                   has_activity_context,
                   has_resolution_context,
                   has_attachment_context
            FROM prioritized
            """
        ).fetchall()
    all_rows = [dict(row) for row in rows]

    hot_rows = (
        _hot_group_rows(all_rows, bucket=0, has_detail=0)
        + _hot_group_rows(all_rows, bucket=0, has_detail=1)
        + _hot_group_rows(all_rows, bucket=1, has_detail=0)
        + _hot_group_rows(all_rows, bucket=1, has_detail=1)
    )

    selected: list[dict[str, Any]] = hot_rows[:limit]
    remaining = limit - len(selected)
    if remaining <= 0:
        return selected

    selected_ids = {str(row["id"]) for row in selected}
    cold_rows = [row for row in all_rows if row["bucket"] == 2 and str(row["id"]) not in selected_ids]

    cold_unenriched = [row for row in cold_rows if row["has_detail"] == 0]
    cold_enriched = [row for row in cold_rows if row["has_detail"] == 1]

    selected.extend(_prioritize_cold_candidates(cold_unenriched, remaining, coverage_rows=cold_rows))
    remaining = limit - len(selected)
    if remaining <= 0:
        return selected

    selected_ids = {str(row["id"]) for row in selected}
    cold_enriched = [row for row in cold_enriched if str(row["id"]) not in selected_ids]
    selected.extend(_prioritize_cold_candidates(cold_enriched, remaining, coverage_rows=cold_rows))
    return selected[:limit]


def enrich_priority_ticket_details(settings: Settings, limit: int = 50, materialize_docs: bool = True) -> EnrichmentResult:
    initialize_db(settings.db_path)
    if not settings.api_key or not settings.org_key or not settings.instance_key:
        return EnrichmentResult(
            status='needs_config',
            message='Live API config is required before enrichment can run.',
        )

    run_id = start_ingest_run(settings.db_path, mode='enrich_priority_ticket_details', notes=f'limit={limit}')
    try:
        client = _build_client(settings)
        candidates = _candidate_ticket_rows(settings.db_path, limit=limit)
        ticket_ids = [str(row['id']) for row in candidates]
        details = []
        synced_at = now_iso()
        for ticket_id in ticket_ids:
            detail = client.get(f'tickets/{ticket_id}')
            if isinstance(detail, dict):
                details.append(detail)
        upsert_tickets(settings.db_path, details, synced_at=synced_at)
        upsert_ticket_details(settings.db_path, details, synced_at=synced_at)
        doc_stats = materialize_ticket_documents(settings.db_path, limit=None) if materialize_docs else None
        stats = {
            'candidate_ticket_count': len(ticket_ids),
            'enriched_ticket_count': len(details),
            'unenriched_candidates': sum(1 for row in candidates if row['has_detail'] == 0),
            'open_candidates': sum(1 for row in candidates if row['bucket'] == 0),
            'warm_candidates': sum(1 for row in candidates if row['bucket'] == 1),
            'cold_candidates': sum(1 for row in candidates if row['bucket'] == 2),
            'selected_category_count': len({str(row.get('category') or '').strip() or 'unknown' for row in candidates}),
            'selected_account_count': len({str(row.get('account_key') or '').strip() or 'unknown' for row in candidates}),
            'selected_technician_count': len({str(row.get('technician_key') or '').strip() or 'unknown' for row in candidates}),
            'synced_at': synced_at,
            'materialized_documents': doc_stats['document_count'] if doc_stats else None,
        }
        set_json_state(settings.db_path, 'enrichment.priority_tickets.last_state', stats)
        finish_ingest_run(settings.db_path, run_id, status='success', notes=json.dumps(stats, sort_keys=True))
        return EnrichmentResult(status='ok', message='Priority ticket detail enrichment completed.', stats=stats)
    except Exception as exc:
        finish_ingest_run(settings.db_path, run_id, status='failed', notes=f'{type(exc).__name__}: {exc}')
        raise
