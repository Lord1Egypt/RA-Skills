from __future__ import annotations

import json
from pathlib import Path

from .db import connect
from .documents import DOCUMENT_MATERIALIZATION_VERSION
from .vector_exports import _infer_chunk_sections

# Summary helpers in this module are intentionally factual/structural.
# They should organize and expose data for OpenClaw, not pre-interpret it too aggressively.


def _ratio(numerator: int, denominator: int) -> float:
    return round((numerator / denominator), 4) if denominator else 0.0


_ENTITY_METADATA_FIELDS: list[tuple[str, str]] = [
    ("cleaned_subject", "cleaned_subject"),
    ("issue_summary", "issue_summary"),
    ("cleaned_action_cue", "action_cue"),
    ("resolution_summary", "resolution_summary"),
    ("recent_log_types_csv", "recent_log_types"),
    ("attachment_kinds_csv", "attachment_metadata"),
    ("department_label", "department_label"),
]


def _entity_metadata_coverage(row: dict, total_tickets: int) -> dict[str, dict[str, float | int]]:
    coverage: dict[str, dict[str, float | int]] = {}
    for column_name, field_name in _ENTITY_METADATA_FIELDS:
        count = int(row.get(f"{field_name}_tickets") or 0)
        coverage[field_name] = {
            "tickets": count,
            "ratio": _ratio(count, total_tickets),
        }
    return coverage


def _entity_retrieval_health(conn, where_clause: str, params: tuple[object, ...]) -> dict:
    row = conn.execute(
        f"""
        WITH log_tickets AS (
            SELECT DISTINCT ticket_id FROM ticket_logs
        ),
        attachment_tickets AS (
            SELECT DISTINCT ticket_id FROM ticket_attachments
        ),
        chunk_counts AS (
            SELECT ticket_id, COUNT(*) AS chunk_count
            FROM ticket_document_chunks
            GROUP BY ticket_id
        ),
        ticket_core AS (
            SELECT t.id,
                   COALESCE(t.updated_at, t.created_at) AS updated_at,
                   doc.synced_at AS chunk_synced_at,
                   doc.raw_json AS document_raw_json,
                   CASE WHEN td.ticket_id IS NOT NULL THEN 1 ELSE 0 END AS detail_available,
                   CASE WHEN lt.ticket_id IS NOT NULL THEN 1 ELSE 0 END AS log_available,
                   CASE WHEN at.ticket_id IS NOT NULL THEN 1 ELSE 0 END AS attachment_available,
                   COALESCE(cc.chunk_count, 0) AS chunk_count
            FROM tickets t
            LEFT JOIN ticket_details td ON td.ticket_id = t.id
            LEFT JOIN ticket_documents doc ON doc.ticket_id = t.id
            LEFT JOIN log_tickets lt ON lt.ticket_id = t.id
            LEFT JOIN attachment_tickets at ON at.ticket_id = t.id
            LEFT JOIN chunk_counts cc ON cc.ticket_id = t.id
            WHERE {where_clause}
        )
        SELECT COUNT(*) AS total_tickets,
               SUM(detail_available) AS detail_tickets,
               SUM(log_available) AS log_tickets,
               SUM(attachment_available) AS attachment_tickets,
               SUM(CASE WHEN document_raw_json IS NOT NULL THEN 1 ELSE 0 END) AS document_tickets,
               SUM(CASE WHEN document_raw_json IS NULL THEN 1 ELSE 0 END) AS missing_document_tickets,
               SUM(CASE WHEN chunk_count > 1 THEN 1 ELSE 0 END) AS multi_chunk_tickets,
               SUM(CASE WHEN document_raw_json IS NOT NULL AND chunk_count = 0 THEN 1 ELSE 0 END) AS chunkless_document_tickets,
               SUM(CASE WHEN updated_at IS NULL THEN 1 ELSE 0 END) AS missing_updated_at_tickets,
               SUM(CASE WHEN chunk_synced_at IS NULL THEN 1 ELSE 0 END) AS missing_chunk_synced_at_tickets,
               SUM(CASE WHEN updated_at IS NOT NULL AND chunk_synced_at IS NOT NULL AND chunk_synced_at < updated_at THEN 1 ELSE 0 END) AS lagging_tickets,
               ROUND(AVG(CASE WHEN updated_at IS NOT NULL AND chunk_synced_at IS NOT NULL AND chunk_synced_at < updated_at
                              THEN (julianday(updated_at) - julianday(chunk_synced_at)) * 1440.0 END), 2) AS avg_lag_minutes,
               ROUND(MAX(CASE WHEN updated_at IS NOT NULL AND chunk_synced_at IS NOT NULL AND chunk_synced_at < updated_at
                              THEN (julianday(updated_at) - julianday(chunk_synced_at)) * 1440.0 END), 2) AS max_lag_minutes,
               MAX(chunk_synced_at) AS latest_chunk_synced_at,
               SUM(CASE WHEN json_extract(document_raw_json, '$.metadata.cleaned_subject') IS NOT NULL AND json_extract(document_raw_json, '$.metadata.cleaned_subject') != '' THEN 1 ELSE 0 END) AS cleaned_subject_tickets,
               SUM(CASE WHEN json_extract(document_raw_json, '$.metadata.issue_summary') IS NOT NULL AND json_extract(document_raw_json, '$.metadata.issue_summary') != '' THEN 1 ELSE 0 END) AS issue_summary_tickets,
               SUM(CASE WHEN COALESCE(json_extract(document_raw_json, '$.metadata.cleaned_action_cue'), json_extract(document_raw_json, '$.metadata.cleaned_followup_note')) IS NOT NULL
                         AND COALESCE(json_extract(document_raw_json, '$.metadata.cleaned_action_cue'), json_extract(document_raw_json, '$.metadata.cleaned_followup_note')) != '' THEN 1 ELSE 0 END) AS action_cue_tickets,
               SUM(CASE WHEN json_extract(document_raw_json, '$.metadata.resolution_summary') IS NOT NULL AND json_extract(document_raw_json, '$.metadata.resolution_summary') != '' THEN 1 ELSE 0 END) AS resolution_summary_tickets,
               SUM(CASE WHEN json_extract(document_raw_json, '$.metadata.recent_log_types_csv') IS NOT NULL AND json_extract(document_raw_json, '$.metadata.recent_log_types_csv') != '' THEN 1 ELSE 0 END) AS recent_log_types_tickets,
               SUM(CASE WHEN json_extract(document_raw_json, '$.metadata.attachment_kinds_csv') IS NOT NULL AND json_extract(document_raw_json, '$.metadata.attachment_kinds_csv') != '' THEN 1 ELSE 0 END) AS attachment_metadata_tickets,
               SUM(CASE WHEN json_extract(document_raw_json, '$.metadata.department_label') IS NOT NULL AND json_extract(document_raw_json, '$.metadata.department_label') != '' THEN 1 ELSE 0 END) AS department_label_tickets
        FROM ticket_core
        """,
        params,
    ).fetchone()
    stats = dict(row)
    total_tickets = int(stats.get("total_tickets") or 0)
    lagging_tickets = int(stats.get("lagging_tickets") or 0)
    lag_bucket_row = conn.execute(
        f"""
        WITH ticket_core AS (
            SELECT COALESCE(t.updated_at, t.created_at) AS updated_at,
                   doc.synced_at AS chunk_synced_at
            FROM tickets t
            LEFT JOIN ticket_documents doc ON doc.ticket_id = t.id
            WHERE {where_clause}
        )
        SELECT SUM(CASE WHEN updated_at IS NULL THEN 1 ELSE 0 END) AS missing_updated_at,
               SUM(CASE WHEN updated_at IS NOT NULL AND chunk_synced_at IS NULL THEN 1 ELSE 0 END) AS missing_chunk_synced_at,
               SUM(CASE WHEN updated_at IS NOT NULL AND chunk_synced_at IS NOT NULL AND chunk_synced_at >= updated_at THEN 1 ELSE 0 END) AS current_or_ahead,
               SUM(CASE WHEN updated_at IS NOT NULL AND chunk_synced_at IS NOT NULL AND chunk_synced_at < updated_at
                         AND (julianday(updated_at) - julianday(chunk_synced_at)) * 1440.0 <= 15 THEN 1 ELSE 0 END) AS lag_le_15m,
               SUM(CASE WHEN updated_at IS NOT NULL AND chunk_synced_at IS NOT NULL AND chunk_synced_at < updated_at
                         AND (julianday(updated_at) - julianday(chunk_synced_at)) * 1440.0 > 15
                         AND (julianday(updated_at) - julianday(chunk_synced_at)) * 1440.0 <= 60 THEN 1 ELSE 0 END) AS lag_le_1h,
               SUM(CASE WHEN updated_at IS NOT NULL AND chunk_synced_at IS NOT NULL AND chunk_synced_at < updated_at
                         AND (julianday(updated_at) - julianday(chunk_synced_at)) * 1440.0 > 60
                         AND (julianday(updated_at) - julianday(chunk_synced_at)) * 1440.0 <= 360 THEN 1 ELSE 0 END) AS lag_le_6h,
               SUM(CASE WHEN updated_at IS NOT NULL AND chunk_synced_at IS NOT NULL AND chunk_synced_at < updated_at
                         AND (julianday(updated_at) - julianday(chunk_synced_at)) * 1440.0 > 360
                         AND (julianday(updated_at) - julianday(chunk_synced_at)) * 1440.0 <= 1440 THEN 1 ELSE 0 END) AS lag_le_24h,
               SUM(CASE WHEN updated_at IS NOT NULL AND chunk_synced_at IS NOT NULL AND chunk_synced_at < updated_at
                         AND (julianday(updated_at) - julianday(chunk_synced_at)) * 1440.0 > 1440 THEN 1 ELSE 0 END) AS lag_gt_24h
        FROM ticket_core
        """,
        params,
    ).fetchone()
    lag_buckets = {key: int((lag_bucket_row[key] or 0)) for key in lag_bucket_row.keys()}
    metadata_coverage = _entity_metadata_coverage(stats, total_tickets)
    return {
        "detail_tickets": int(stats.get("detail_tickets") or 0),
        "detail_coverage_ratio": _ratio(int(stats.get("detail_tickets") or 0), total_tickets),
        "log_tickets": int(stats.get("log_tickets") or 0),
        "log_coverage_ratio": _ratio(int(stats.get("log_tickets") or 0), total_tickets),
        "attachment_tickets": int(stats.get("attachment_tickets") or 0),
        "attachment_coverage_ratio": _ratio(int(stats.get("attachment_tickets") or 0), total_tickets),
        "document_tickets": int(stats.get("document_tickets") or 0),
        "document_coverage_ratio": _ratio(int(stats.get("document_tickets") or 0), total_tickets),
        "missing_document_tickets": int(stats.get("missing_document_tickets") or 0),
        "missing_document_ratio": _ratio(int(stats.get("missing_document_tickets") or 0), total_tickets),
        "multi_chunk_tickets": int(stats.get("multi_chunk_tickets") or 0),
        "multi_chunk_ratio": _ratio(int(stats.get("multi_chunk_tickets") or 0), total_tickets),
        "chunkless_document_tickets": int(stats.get("chunkless_document_tickets") or 0),
        "chunkless_document_ratio": _ratio(int(stats.get("chunkless_document_tickets") or 0), total_tickets),
        "action_cue_tickets": int(stats.get("action_cue_tickets") or 0),
        "action_cue_ratio": _ratio(int(stats.get("action_cue_tickets") or 0), total_tickets),
        "resolution_summary_tickets": int(stats.get("resolution_summary_tickets") or 0),
        "resolution_summary_ratio": _ratio(int(stats.get("resolution_summary_tickets") or 0), total_tickets),
        "attachment_metadata_tickets": int(stats.get("attachment_metadata_tickets") or 0),
        "attachment_metadata_ratio": _ratio(int(stats.get("attachment_metadata_tickets") or 0), total_tickets),
        "lagging_tickets": lagging_tickets,
        "lagging_ratio": _ratio(lagging_tickets, total_tickets),
        "avg_lag_minutes": float(stats.get("avg_lag_minutes") or 0.0),
        "max_lag_minutes": float(stats.get("max_lag_minutes") or 0.0),
        "latest_chunk_synced_at": stats.get("latest_chunk_synced_at"),
        "missing_updated_at_tickets": int(stats.get("missing_updated_at_tickets") or 0),
        "missing_chunk_synced_at_tickets": int(stats.get("missing_chunk_synced_at_tickets") or 0),
        "lag_buckets": lag_buckets,
        "metadata_coverage": metadata_coverage,
    }


def list_account_artifact_summaries(db_path: Path) -> list[dict]:
    with connect(db_path) as conn:
        rows = conn.execute(
            """
            WITH ticket_core AS (
                SELECT t.id,
                       COALESCE(a.id, t.account_id) AS account_ref,
                       COALESCE(a.name, t.account_id, 'unknown') AS account,
                       t.status,
                       COALESCE(t.updated_at, t.created_at) AS activity_at
                FROM tickets t
                LEFT JOIN accounts a ON a.id = t.account_id
            ),
            detail_tickets AS (
                SELECT DISTINCT ticket_id FROM ticket_details
            ),
            log_tickets AS (
                SELECT DISTINCT ticket_id FROM ticket_logs
            ),
            attachment_tickets AS (
                SELECT DISTINCT ticket_id FROM ticket_attachments
            ),
            document_tickets AS (
                SELECT DISTINCT ticket_id FROM ticket_documents
            ),
            chunk_counts AS (
                SELECT ticket_id, COUNT(*) AS chunk_count
                FROM ticket_document_chunks
                GROUP BY ticket_id
            )
            SELECT MIN(tc.account_ref) AS account_ref,
                   tc.account,
                   COUNT(*) AS total_tickets,
                   SUM(CASE WHEN tc.status = 'Open' THEN 1 ELSE 0 END) AS open_tickets,
                   SUM(CASE WHEN tc.status = 'Closed' THEN 1 ELSE 0 END) AS closed_tickets,
                   MAX(tc.activity_at) AS latest_activity_at,
                   SUM(CASE WHEN dt.ticket_id IS NOT NULL THEN 1 ELSE 0 END) AS detail_tickets,
                   SUM(CASE WHEN lt.ticket_id IS NOT NULL THEN 1 ELSE 0 END) AS log_tickets,
                   SUM(CASE WHEN at.ticket_id IS NOT NULL THEN 1 ELSE 0 END) AS attachment_tickets,
                   SUM(CASE WHEN doc.ticket_id IS NOT NULL THEN 1 ELSE 0 END) AS document_tickets,
                   COALESCE(SUM(cc.chunk_count), 0) AS chunk_count
            FROM ticket_core tc
            LEFT JOIN detail_tickets dt ON dt.ticket_id = tc.id
            LEFT JOIN log_tickets lt ON lt.ticket_id = tc.id
            LEFT JOIN attachment_tickets at ON at.ticket_id = tc.id
            LEFT JOIN document_tickets doc ON doc.ticket_id = tc.id
            LEFT JOIN chunk_counts cc ON cc.ticket_id = tc.id
            WHERE tc.account IS NOT NULL AND tc.account != '' AND tc.account != 'unknown'
            GROUP BY tc.account
            ORDER BY total_tickets DESC, latest_activity_at DESC, tc.account ASC
            """
        ).fetchall()
    summaries = []
    for row in rows:
        total_tickets = int(row["total_tickets"] or 0)
        detail_tickets = int(row["detail_tickets"] or 0)
        log_tickets = int(row["log_tickets"] or 0)
        attachment_tickets = int(row["attachment_tickets"] or 0)
        document_tickets = int(row["document_tickets"] or 0)
        summaries.append({
            "account_ref": row["account_ref"],
            "account": row["account"],
            "total_tickets": total_tickets,
            "open_tickets": int(row["open_tickets"] or 0),
            "closed_tickets": int(row["closed_tickets"] or 0),
            "latest_activity_at": row["latest_activity_at"],
            "detail_tickets": detail_tickets,
            "detail_coverage_ratio": _ratio(detail_tickets, total_tickets),
            "log_tickets": log_tickets,
            "log_coverage_ratio": _ratio(log_tickets, total_tickets),
            "attachment_tickets": attachment_tickets,
            "attachment_coverage_ratio": _ratio(attachment_tickets, total_tickets),
            "document_tickets": document_tickets,
            "document_coverage_ratio": _ratio(document_tickets, total_tickets),
            "chunk_count": int(row["chunk_count"] or 0),
        })
    return summaries


def list_technician_artifact_summaries(db_path: Path) -> list[dict]:
    with connect(db_path) as conn:
        rows = conn.execute(
            """
            WITH ticket_core AS (
                SELECT t.id,
                       COALESCE(te.id, t.assigned_technician_id) AS technician_ref,
                       COALESCE(te.display_name, t.assigned_technician_id, 'unassigned') AS technician,
                       t.status,
                       COALESCE(t.updated_at, t.created_at) AS activity_at
                FROM tickets t
                LEFT JOIN technicians te ON te.id = t.assigned_technician_id
            ),
            detail_tickets AS (
                SELECT DISTINCT ticket_id FROM ticket_details
            ),
            log_tickets AS (
                SELECT DISTINCT ticket_id FROM ticket_logs
            ),
            attachment_tickets AS (
                SELECT DISTINCT ticket_id FROM ticket_attachments
            ),
            document_tickets AS (
                SELECT DISTINCT ticket_id FROM ticket_documents
            ),
            chunk_counts AS (
                SELECT ticket_id, COUNT(*) AS chunk_count
                FROM ticket_document_chunks
                GROUP BY ticket_id
            )
            SELECT MIN(tc.technician_ref) AS technician_ref,
                   tc.technician,
                   COUNT(*) AS total_tickets,
                   SUM(CASE WHEN tc.status = 'Open' THEN 1 ELSE 0 END) AS open_tickets,
                   SUM(CASE WHEN tc.status = 'Closed' THEN 1 ELSE 0 END) AS closed_tickets,
                   MAX(tc.activity_at) AS latest_activity_at,
                   SUM(CASE WHEN dt.ticket_id IS NOT NULL THEN 1 ELSE 0 END) AS detail_tickets,
                   SUM(CASE WHEN lt.ticket_id IS NOT NULL THEN 1 ELSE 0 END) AS log_tickets,
                   SUM(CASE WHEN at.ticket_id IS NOT NULL THEN 1 ELSE 0 END) AS attachment_tickets,
                   SUM(CASE WHEN doc.ticket_id IS NOT NULL THEN 1 ELSE 0 END) AS document_tickets,
                   COALESCE(SUM(cc.chunk_count), 0) AS chunk_count
            FROM ticket_core tc
            LEFT JOIN detail_tickets dt ON dt.ticket_id = tc.id
            LEFT JOIN log_tickets lt ON lt.ticket_id = tc.id
            LEFT JOIN attachment_tickets at ON at.ticket_id = tc.id
            LEFT JOIN document_tickets doc ON doc.ticket_id = tc.id
            LEFT JOIN chunk_counts cc ON cc.ticket_id = tc.id
            WHERE tc.technician IS NOT NULL AND tc.technician != '' AND tc.technician != 'unassigned'
            GROUP BY tc.technician
            ORDER BY total_tickets DESC, latest_activity_at DESC, tc.technician ASC
            """
        ).fetchall()
    summaries = []
    for row in rows:
        total_tickets = int(row["total_tickets"] or 0)
        detail_tickets = int(row["detail_tickets"] or 0)
        log_tickets = int(row["log_tickets"] or 0)
        attachment_tickets = int(row["attachment_tickets"] or 0)
        document_tickets = int(row["document_tickets"] or 0)
        summaries.append({
            "technician_ref": row["technician_ref"],
            "technician": row["technician"],
            "total_tickets": total_tickets,
            "open_tickets": int(row["open_tickets"] or 0),
            "closed_tickets": int(row["closed_tickets"] or 0),
            "latest_activity_at": row["latest_activity_at"],
            "detail_tickets": detail_tickets,
            "detail_coverage_ratio": _ratio(detail_tickets, total_tickets),
            "log_tickets": log_tickets,
            "log_coverage_ratio": _ratio(log_tickets, total_tickets),
            "attachment_tickets": attachment_tickets,
            "attachment_coverage_ratio": _ratio(attachment_tickets, total_tickets),
            "document_tickets": document_tickets,
            "document_coverage_ratio": _ratio(document_tickets, total_tickets),
            "chunk_count": int(row["chunk_count"] or 0),
        })
    return summaries


def list_ticket_artifact_summaries(db_path: Path) -> list[dict]:
    with connect(db_path) as conn:
        rows = conn.execute(
            """
            WITH chunk_counts AS (
                SELECT ticket_id,
                       COUNT(*) AS chunk_count,
                       MIN(synced_at) AS earliest_chunk_synced_at,
                       MAX(synced_at) AS latest_chunk_synced_at,
                       SUM(CASE WHEN content_hash IS NOT NULL AND content_hash != '' THEN 1 ELSE 0 END) AS chunk_content_hash_count
                FROM ticket_document_chunks
                GROUP BY ticket_id
            ),
            vector_counts AS (
                SELECT ticket_id,
                       COUNT(*) AS indexed_chunk_count,
                       MIN(dims) AS min_dims,
                       MAX(dims) AS max_dims,
                       MIN(synced_at) AS earliest_vector_synced_at,
                       MAX(synced_at) AS latest_vector_synced_at
                FROM vector_chunk_index
                GROUP BY ticket_id
            )
            SELECT t.id,
                   json_extract(t.raw_json, '$.number') AS ticket_number,
                   json_extract(t.raw_json, '$.key') AS ticket_key,
                   t.subject,
                   t.status,
                   t.priority,
                   t.category,
                   COALESCE(a.name, t.account_id, 'unknown') AS account,
                   COALESCE(te.display_name, t.assigned_technician_id, 'unassigned') AS technician,
                   COALESCE(t.updated_at, t.created_at) AS updated_at,
                   CASE WHEN td.ticket_id IS NOT NULL THEN 1 ELSE 0 END AS detail_available,
                   CASE WHEN doc.ticket_id IS NOT NULL THEN 1 ELSE 0 END AS document_available,
                   doc.synced_at AS document_synced_at,
                   doc.content_hash AS document_content_hash,
                   COALESCE(json_extract(doc.raw_json, '$.metadata.materialization_version'), 0) AS materialization_version,
                   COALESCE(json_extract(doc.raw_json, '$.metadata.has_next_step'), 0) AS has_next_step,
                   COALESCE(json_extract(doc.raw_json, '$.metadata.has_attachments'), 0) AS has_attachments,
                   COALESCE(json_extract(doc.raw_json, '$.metadata.has_resolution_summary'), 0) AS has_resolution_summary,
                   COALESCE(json_extract(doc.raw_json, '$.metadata.cleaned_action_cue'), json_extract(doc.raw_json, '$.metadata.cleaned_followup_note')) AS action_cue,
                   COALESCE(log_counts.log_count, 0) AS log_count,
                   COALESCE(attachment_counts.attachment_count, 0) AS attachment_count,
                   COALESCE(chunk_counts.chunk_count, 0) AS chunk_count,
                   chunk_counts.earliest_chunk_synced_at,
                   chunk_counts.latest_chunk_synced_at,
                   COALESCE(chunk_counts.chunk_content_hash_count, 0) AS chunk_content_hash_count,
                   COALESCE(vector_counts.indexed_chunk_count, 0) AS indexed_chunk_count,
                   vector_counts.min_dims,
                   vector_counts.max_dims,
                   vector_counts.earliest_vector_synced_at,
                   vector_counts.latest_vector_synced_at,
                   CASE WHEN doc.synced_at IS NOT NULL AND COALESCE(t.updated_at, t.created_at) IS NOT NULL AND doc.synced_at < COALESCE(t.updated_at, t.created_at)
                        THEN ROUND((julianday(COALESCE(t.updated_at, t.created_at)) - julianday(doc.synced_at)) * 1440.0, 2)
                        ELSE 0 END AS lag_minutes
            FROM tickets t
            LEFT JOIN accounts a ON a.id = t.account_id
            LEFT JOIN technicians te ON te.id = t.assigned_technician_id
            LEFT JOIN ticket_details td ON td.ticket_id = t.id
            LEFT JOIN ticket_documents doc ON doc.ticket_id = t.id
            LEFT JOIN (
                SELECT ticket_id, COUNT(*) AS log_count
                FROM ticket_logs
                GROUP BY ticket_id
            ) log_counts ON log_counts.ticket_id = t.id
            LEFT JOIN (
                SELECT ticket_id, COUNT(*) AS attachment_count
                FROM ticket_attachments
                GROUP BY ticket_id
            ) attachment_counts ON attachment_counts.ticket_id = t.id
            LEFT JOIN chunk_counts ON chunk_counts.ticket_id = t.id
            LEFT JOIN vector_counts ON vector_counts.ticket_id = t.id
            WHERE t.status = 'Open'
               OR td.ticket_id IS NOT NULL
               OR COALESCE(log_counts.log_count, 0) > 0
               OR COALESCE(attachment_counts.attachment_count, 0) > 0
            ORDER BY CASE WHEN t.status = 'Open' THEN 0 ELSE 1 END,
                     COALESCE(t.updated_at, t.created_at) DESC,
                     t.id DESC
            """
        ).fetchall()
    return [
        {
            "ticket_id": row["id"],
            "ticket_number": row["ticket_number"],
            "ticket_key": row["ticket_key"],
            "subject": row["subject"],
            "status": row["status"],
            "priority": row["priority"],
            "category": row["category"],
            "account": row["account"],
            "technician": row["technician"],
            "updated_at": row["updated_at"],
            "detail_available": bool(row["detail_available"]),
            "document_available": bool(row["document_available"]),
            "document_synced_at": row["document_synced_at"],
            "materialization_version": int(row["materialization_version"] or 0),
            "is_current_materialization_version": int(row["materialization_version"] or 0) == DOCUMENT_MATERIALIZATION_VERSION,
            "has_next_step": bool(row["has_next_step"]),
            "has_attachments": bool(row["has_attachments"]),
            "has_resolution_summary": bool(row["has_resolution_summary"]),
            "action_cue": row["action_cue"],
            "log_count": int(row["log_count"] or 0),
            "attachment_count": int(row["attachment_count"] or 0),
            "chunk_count": int(row["chunk_count"] or 0),
            "indexed_chunk_count": int(row["indexed_chunk_count"] or 0),
            "missing_index_chunks": max(int(row["chunk_count"] or 0) - int(row["indexed_chunk_count"] or 0), 0),
            "vector_ready": bool(row["chunk_count"] or 0) and int(row["indexed_chunk_count"] or 0) == int(row["chunk_count"] or 0),
            "vector_dims": int(row["min_dims"] or 0) if row["min_dims"] is not None and row["min_dims"] == row["max_dims"] else None,
            "latest_vector_synced_at": row["latest_vector_synced_at"],
            "earliest_chunk_synced_at": row["earliest_chunk_synced_at"],
            "latest_chunk_synced_at": row["latest_chunk_synced_at"],
            "chunk_content_hash_count": int(row["chunk_content_hash_count"] or 0),
            "all_chunk_hashes_present": bool(row["chunk_count"] or 0) and int(row["chunk_content_hash_count"] or 0) == int(row["chunk_count"] or 0),
            "lag_minutes": float(row["lag_minutes"] or 0.0),
        }
        for row in rows
    ]


def get_ticket_summary(db_path: Path, ticket_query: str, limit_logs: int = 10, limit_attachments: int = 10) -> dict:
    with connect(db_path) as conn:
        ticket = conn.execute(
            """
            SELECT t.id,
                   json_extract(t.raw_json, '$.number') AS ticket_number,
                   json_extract(t.raw_json, '$.key') AS ticket_key,
                   t.subject,
                   t.status,
                   t.priority,
                   t.category,
                   t.created_at,
                   t.updated_at,
                   t.closed_at,
                   t.account_id,
                   t.user_id,
                   t.assigned_technician_id,
                   COALESCE(a.name, t.account_id) AS account,
                   COALESCE(u.display_name, t.user_id) AS user_name,
                   COALESCE(u.email, json_extract(t.raw_json, '$.user_email')) AS user_email,
                   COALESCE(te.display_name, t.assigned_technician_id) AS technician,
                   COALESCE(te.email, json_extract(t.raw_json, '$.technician_email'), json_extract(t.raw_json, '$.tech_email')) AS technician_email,
                   doc.doc_id,
                   doc.synced_at AS document_synced_at,
                   doc.content_hash AS document_content_hash,
                   doc.raw_json AS document_raw_json,
                   CASE WHEN td.ticket_id IS NOT NULL THEN 1 ELSE 0 END AS detail_row_present,
                   COALESCE(log_counts.log_count, 0) AS log_count,
                   COALESCE(log_counts.public_log_count, 0) AS public_log_count,
                   COALESCE(log_counts.internal_log_count, 0) AS internal_log_count,
                   COALESCE(attachment_counts.attachment_count, 0) AS attachment_count,
                   COALESCE(chunk_counts.chunk_count, 0) AS chunk_count,
                   chunk_counts.earliest_chunk_synced_at,
                   chunk_counts.latest_chunk_synced_at,
                   COALESCE(chunk_counts.chunk_content_hash_count, 0) AS chunk_content_hash_count,
                   COALESCE(vector_counts.indexed_chunk_count, 0) AS indexed_chunk_count,
                   vector_counts.min_dims,
                   vector_counts.max_dims,
                   vector_counts.earliest_vector_synced_at,
                   vector_counts.latest_vector_synced_at,
                   CASE WHEN doc.synced_at IS NOT NULL AND COALESCE(t.updated_at, t.created_at) IS NOT NULL AND doc.synced_at < COALESCE(t.updated_at, t.created_at)
                        THEN ROUND((julianday(COALESCE(t.updated_at, t.created_at)) - julianday(doc.synced_at)) * 1440.0, 2)
                        ELSE 0 END AS lag_minutes
            FROM tickets t
            LEFT JOIN accounts a ON a.id = t.account_id
            LEFT JOIN users u ON u.id = t.user_id
            LEFT JOIN technicians te ON te.id = t.assigned_technician_id
            LEFT JOIN ticket_details td ON td.ticket_id = t.id
            LEFT JOIN ticket_documents doc ON doc.ticket_id = t.id
            LEFT JOIN (
                SELECT ticket_id,
                       COUNT(*) AS log_count,
                       SUM(CASE WHEN COALESCE(is_tech_only, 0) = 0 THEN 1 ELSE 0 END) AS public_log_count,
                       SUM(CASE WHEN COALESCE(is_tech_only, 0) = 1 THEN 1 ELSE 0 END) AS internal_log_count
                FROM ticket_logs
                GROUP BY ticket_id
            ) log_counts ON log_counts.ticket_id = t.id
            LEFT JOIN (
                SELECT ticket_id, COUNT(*) AS attachment_count
                FROM ticket_attachments
                GROUP BY ticket_id
            ) attachment_counts ON attachment_counts.ticket_id = t.id
            LEFT JOIN (
                SELECT ticket_id,
                       COUNT(*) AS chunk_count,
                       MIN(synced_at) AS earliest_chunk_synced_at,
                       MAX(synced_at) AS latest_chunk_synced_at,
                       SUM(CASE WHEN content_hash IS NOT NULL AND content_hash != '' THEN 1 ELSE 0 END) AS chunk_content_hash_count
                FROM ticket_document_chunks
                GROUP BY ticket_id
            ) chunk_counts ON chunk_counts.ticket_id = t.id
            LEFT JOIN (
                SELECT ticket_id,
                       COUNT(*) AS indexed_chunk_count,
                       MIN(dims) AS min_dims,
                       MAX(dims) AS max_dims,
                       MIN(synced_at) AS earliest_vector_synced_at,
                       MAX(synced_at) AS latest_vector_synced_at
                FROM vector_chunk_index
                GROUP BY ticket_id
            ) vector_counts ON vector_counts.ticket_id = t.id
            WHERE CAST(t.id AS TEXT) = ?
               OR json_extract(t.raw_json, '$.number') = ?
               OR json_extract(t.raw_json, '$.key') = ?
               OR t.subject = ? COLLATE NOCASE
            ORDER BY CASE
                       WHEN CAST(t.id AS TEXT) = ? THEN 0
                       WHEN json_extract(t.raw_json, '$.number') = ? THEN 1
                       WHEN json_extract(t.raw_json, '$.key') = ? THEN 2
                       WHEN t.subject = ? COLLATE NOCASE THEN 3
                       ELSE 4
                     END,
                     t.updated_at DESC,
                     t.id DESC
            LIMIT 1
            """,
            (ticket_query, ticket_query, ticket_query, ticket_query, ticket_query, ticket_query, ticket_query, ticket_query),
        ).fetchone()
        if not ticket:
            return {"status": "not_found", "ticket_query": ticket_query}

        recent_logs = conn.execute(
            """
            SELECT id,
                   COALESCE(log_type, 'unknown') AS log_type,
                   record_date,
                   COALESCE(user_name, user_email, user_id) AS actor,
                   COALESCE(is_tech_only, 0) AS is_tech_only,
                   COALESCE(plain_note, note) AS note
            FROM ticket_logs
            WHERE ticket_id = ?
            ORDER BY record_date DESC, id DESC
            LIMIT ?
            """,
            (ticket["id"], limit_logs),
        ).fetchall()
        attachments = conn.execute(
            """
            SELECT id, name, size, recorded_at, url
            FROM ticket_attachments
            WHERE ticket_id = ?
            ORDER BY recorded_at DESC, id DESC
            LIMIT ?
            """,
            (ticket["id"], limit_attachments),
        ).fetchall()
        chunk_rows = conn.execute(
            """
            SELECT c.chunk_id,
                   c.doc_id,
                   c.chunk_index,
                   c.text,
                   c.content_hash,
                   c.synced_at,
                   v.dims,
                   v.synced_at AS vector_synced_at,
                   CASE WHEN v.chunk_id IS NOT NULL THEN 1 ELSE 0 END AS vector_indexed
            FROM ticket_document_chunks c
            LEFT JOIN vector_chunk_index v ON v.chunk_id = c.chunk_id
            WHERE c.ticket_id = ?
            ORDER BY c.chunk_index ASC, c.chunk_id ASC
            """,
            (ticket["id"],),
        ).fetchall()

    document_metadata = {}
    if ticket["document_raw_json"]:
        try:
            document_metadata = (json.loads(ticket["document_raw_json"]) or {}).get("metadata", {})
        except Exception:
            document_metadata = {}

    chunk_inventory = []
    section_counts: dict[str, int] = {}
    label_counts: dict[str, int] = {}
    indexed_chunk_count = 0
    vector_dims: set[int] = set()
    for row in chunk_rows:
        section_info = _infer_chunk_sections(row["text"])
        for label in section_info["chunk_section_labels"]:
            label_counts[label] = label_counts.get(label, 0) + 1
        primary = str(section_info["chunk_primary_section"])
        section_counts[primary] = section_counts.get(primary, 0) + 1
        if row["vector_indexed"]:
            indexed_chunk_count += 1
        if row["dims"] is not None:
            vector_dims.add(int(row["dims"]))
        chunk_inventory.append({
            "chunk_id": row["chunk_id"],
            "doc_id": row["doc_id"],
            "chunk_index": int(row["chunk_index"] or 0),
            "chunk_chars": len(str(row["text"] or "")),
            "content_hash_present": bool(row["content_hash"]),
            "chunk_synced_at": row["synced_at"],
            "vector_indexed": bool(row["vector_indexed"]),
            "vector_synced_at": row["vector_synced_at"],
            "vector_dims": int(row["dims"]) if row["dims"] is not None else None,
            "chunk_primary_section": section_info["chunk_primary_section"],
            "chunk_section_labels": section_info["chunk_section_labels"],
            "chunk_has_identity_context": section_info["chunk_has_identity_context"],
            "chunk_has_workflow_context": section_info["chunk_has_workflow_context"],
            "chunk_has_project_context": section_info["chunk_has_project_context"],
            "chunk_has_action_context": section_info["chunk_has_action_context"],
            "chunk_has_issue_context": section_info["chunk_has_issue_context"],
            "chunk_has_activity_context": section_info["chunk_has_activity_context"],
            "chunk_has_resolution_context": section_info["chunk_has_resolution_context"],
            "chunk_has_attachment_context": section_info["chunk_has_attachment_context"],
        })

    chunk_count = int(ticket["chunk_count"] or 0)
    materialization_version = int(document_metadata.get("materialization_version") or 0)
    retrieval_health = {
        "document_synced_at": ticket["document_synced_at"],
        "document_content_hash_present": bool(ticket["document_content_hash"]),
        "materialization_version": materialization_version,
        "current_materialization_version": DOCUMENT_MATERIALIZATION_VERSION,
        "is_current_materialization_version": materialization_version == DOCUMENT_MATERIALIZATION_VERSION,
        "lag_minutes": float(ticket["lag_minutes"] or 0.0),
        "is_materialization_lagging": float(ticket["lag_minutes"] or 0.0) > 0.0,
        "chunk_count": chunk_count,
        "indexed_chunk_count": int(ticket["indexed_chunk_count"] or 0),
        "missing_index_chunks": max(chunk_count - int(ticket["indexed_chunk_count"] or 0), 0),
        "vector_ready": bool(chunk_count) and int(ticket["indexed_chunk_count"] or 0) == chunk_count,
        "vector_dims": sorted(vector_dims),
        "earliest_chunk_synced_at": ticket["earliest_chunk_synced_at"],
        "latest_chunk_synced_at": ticket["latest_chunk_synced_at"],
        "earliest_vector_synced_at": ticket["earliest_vector_synced_at"],
        "latest_vector_synced_at": ticket["latest_vector_synced_at"],
        "chunk_content_hash_count": int(ticket["chunk_content_hash_count"] or 0),
        "all_chunk_hashes_present": bool(chunk_count) and int(ticket["chunk_content_hash_count"] or 0) == chunk_count,
        "primary_section_counts": section_counts,
        "section_label_counts": label_counts,
    }

    return {
        "status": "ok",
        "ticket": {
            "id": ticket["id"],
            "ticket_number": ticket["ticket_number"],
            "ticket_key": ticket["ticket_key"],
            "subject": ticket["subject"],
            "status": ticket["status"],
            "priority": ticket["priority"],
            "category": ticket["category"],
            "account": ticket["account"],
            "account_id": ticket["account_id"],
            "user_name": ticket["user_name"],
            "user_id": ticket["user_id"],
            "user_email": ticket["user_email"],
            "technician": ticket["technician"],
            "technician_id": ticket["assigned_technician_id"],
            "technician_email": ticket["technician_email"],
            "created_at": ticket["created_at"],
            "updated_at": ticket["updated_at"],
            "closed_at": ticket["closed_at"],
        },
        "artifact_stats": {
            "detail_available": bool(ticket["detail_row_present"] or document_metadata.get("detail_available")),
            "document_available": bool(ticket["document_raw_json"]),
            "log_count": int(ticket["log_count"] or 0),
            "public_log_count": int(ticket["public_log_count"] or 0),
            "internal_log_count": int(ticket["internal_log_count"] or 0),
            "attachment_count": int(ticket["attachment_count"] or 0),
            "chunk_count": chunk_count,
            "has_next_step": bool(document_metadata.get("has_next_step")),
            "has_attachments": bool(document_metadata.get("has_attachments")),
            "has_resolution_summary": bool(document_metadata.get("has_resolution_summary")),
        },
        "retrieval_health": retrieval_health,
        "retrieval_metadata": {
            "cleaned_subject": document_metadata.get("cleaned_subject"),
            "cleaned_initial_post": document_metadata.get("cleaned_initial_post"),
            "cleaned_detail_note": document_metadata.get("cleaned_detail_note"),
            "cleaned_workpad": document_metadata.get("cleaned_workpad"),
            "cleaned_action_cue": document_metadata.get("cleaned_action_cue"),
            "action_cue_source": document_metadata.get("action_cue_source"),
            "cleaned_followup_note": document_metadata.get("cleaned_followup_note"),
            "followup_note_source": document_metadata.get("followup_note_source"),
            "cleaned_request_completion_note": document_metadata.get("cleaned_request_completion_note"),
            "resolution_summary": document_metadata.get("resolution_summary"),
            "latest_response_date": document_metadata.get("latest_response_date"),
            "latest_resolution_log_date": document_metadata.get("latest_resolution_log_date"),
            "recent_log_types_csv": document_metadata.get("recent_log_types_csv"),
            "department_label": document_metadata.get("department_label"),
            "department_label_source": document_metadata.get("department_label_source"),
            "support_group_name": document_metadata.get("support_group_name"),
            "default_contract_name": document_metadata.get("default_contract_name"),
            "account_location_name": document_metadata.get("account_location_name"),
            "location_name": document_metadata.get("location_name"),
            "project_name": document_metadata.get("project_name"),
            "scheduled_ticket_id": document_metadata.get("scheduled_ticket_id"),
            "attachment_kinds_csv": document_metadata.get("attachment_kinds_csv"),
            "attachment_extensions_csv": document_metadata.get("attachment_extensions_csv"),
            "attachment_total_size_bytes": document_metadata.get("attachment_total_size_bytes"),
            "materialization_version": document_metadata.get("materialization_version"),
        },
        "chunk_inventory": chunk_inventory,
        "recent_logs": [dict(row) for row in recent_logs],
        "attachments": [dict(row) for row in attachments],
    }


def get_account_summary(db_path: Path, account_query: str, limit_open: int = 10, limit_recent: int = 10) -> dict:
    with connect(db_path) as conn:
        account = conn.execute(
            """
            SELECT id, name, raw_json
            FROM accounts
            WHERE id = ? OR name = ? COLLATE NOCASE OR name LIKE ? COLLATE NOCASE
            ORDER BY CASE WHEN id = ? THEN 0 WHEN name = ? COLLATE NOCASE THEN 1 ELSE 2 END, name ASC
            LIMIT 1
            """,
            (account_query, account_query, f"%{account_query}%", account_query, account_query),
        ).fetchone()
        if not account:
            fallback_account = conn.execute(
                """
                SELECT account_id AS id, account_id AS name
                FROM tickets
                WHERE account_id = ?
                LIMIT 1
                """,
                (account_query,),
            ).fetchone()
            if not fallback_account:
                return {"status": "not_found", "account_query": account_query}
            account = fallback_account
        open_tickets = conn.execute(
            """
            SELECT id, subject, status, priority, category, updated_at, closed_at
            FROM tickets
            WHERE account_id = ? AND status = 'Open'
            ORDER BY updated_at DESC, id DESC
            LIMIT ?
            """,
            (account["id"], limit_open),
        ).fetchall()
        recent_tickets = conn.execute(
            """
            SELECT id, subject, status, priority, category, updated_at
            FROM tickets
            WHERE account_id = ?
            ORDER BY updated_at DESC, id DESC
            LIMIT ?
            """,
            (account["id"], limit_recent),
        ).fetchall()
        stats = conn.execute(
            """
            WITH log_tickets AS (
                SELECT DISTINCT ticket_id FROM ticket_logs
            ),
            attachment_tickets AS (
                SELECT DISTINCT ticket_id FROM ticket_attachments
            ),
            chunk_counts AS (
                SELECT ticket_id, COUNT(*) AS chunk_count
                FROM ticket_document_chunks
                GROUP BY ticket_id
            )
            SELECT COUNT(*) AS total_tickets,
                   SUM(CASE WHEN t.status = 'Open' THEN 1 ELSE 0 END) AS open_tickets,
                   SUM(CASE WHEN t.status = 'Closed' THEN 1 ELSE 0 END) AS closed_tickets,
                   MAX(t.updated_at) AS latest_activity_at,
                   SUM(CASE WHEN td.ticket_id IS NOT NULL THEN 1 ELSE 0 END) AS detail_tickets,
                   SUM(CASE WHEN lt.ticket_id IS NOT NULL THEN 1 ELSE 0 END) AS log_tickets,
                   SUM(CASE WHEN at.ticket_id IS NOT NULL THEN 1 ELSE 0 END) AS attachment_tickets,
                   SUM(CASE WHEN doc.ticket_id IS NOT NULL THEN 1 ELSE 0 END) AS document_tickets,
                   COALESCE(SUM(cc.chunk_count), 0) AS chunk_count
            FROM tickets t
            LEFT JOIN ticket_details td ON td.ticket_id = t.id
            LEFT JOIN log_tickets lt ON lt.ticket_id = t.id
            LEFT JOIN attachment_tickets at ON at.ticket_id = t.id
            LEFT JOIN ticket_documents doc ON doc.ticket_id = t.id
            LEFT JOIN chunk_counts cc ON cc.ticket_id = t.id
            WHERE t.account_id = ?
            """,
            (account["id"],),
        ).fetchone()
        recent_log_types = conn.execute(
            """
            SELECT COALESCE(tl.log_type, 'unknown') AS log_type, COUNT(*) AS log_count
            FROM ticket_logs tl
            JOIN tickets t ON t.id = tl.ticket_id
            WHERE t.account_id = ?
            GROUP BY COALESCE(tl.log_type, 'unknown')
            ORDER BY log_count DESC, log_type ASC
            LIMIT 10
            """,
            (account["id"],),
        ).fetchall()
        status_breakdown = conn.execute(
            """
            SELECT COALESCE(status, 'unknown') AS status, COUNT(*) AS ticket_count
            FROM tickets
            WHERE account_id = ?
            GROUP BY COALESCE(status, 'unknown')
            ORDER BY ticket_count DESC, status ASC
            """,
            (account["id"],),
        ).fetchall()
        priority_breakdown = conn.execute(
            """
            SELECT COALESCE(priority, 'unknown') AS priority, COUNT(*) AS ticket_count
            FROM tickets
            WHERE account_id = ?
            GROUP BY COALESCE(priority, 'unknown')
            ORDER BY ticket_count DESC, priority ASC
            LIMIT 10
            """,
            (account["id"],),
        ).fetchall()
        category_breakdown = conn.execute(
            """
            SELECT COALESCE(category, 'unknown') AS category, COUNT(*) AS ticket_count
            FROM tickets
            WHERE account_id = ?
            GROUP BY COALESCE(category, 'unknown')
            ORDER BY ticket_count DESC, category ASC
            LIMIT 10
            """,
            (account["id"],),
        ).fetchall()
    stats_dict = dict(stats)
    total_tickets = int(stats_dict.get("total_tickets") or 0)
    detail_tickets = int(stats_dict.get("detail_tickets") or 0)
    log_tickets = int(stats_dict.get("log_tickets") or 0)
    attachment_tickets = int(stats_dict.get("attachment_tickets") or 0)
    document_tickets = int(stats_dict.get("document_tickets") or 0)
    stats_dict.update({
        "detail_coverage_ratio": _ratio(detail_tickets, total_tickets),
        "log_coverage_ratio": _ratio(log_tickets, total_tickets),
        "attachment_coverage_ratio": _ratio(attachment_tickets, total_tickets),
        "document_coverage_ratio": _ratio(document_tickets, total_tickets),
    })
    with connect(db_path) as conn:
        retrieval_health = _entity_retrieval_health(conn, "t.account_id = ?", (account["id"],))
    return {
        "status": "ok",
        "account": {"id": account["id"], "name": account["name"]},
        "stats": stats_dict,
        "retrieval_health": retrieval_health,
        "open_tickets": [dict(row) for row in open_tickets],
        "recent_tickets": [dict(row) for row in recent_tickets],
        "recent_log_types": [dict(row) for row in recent_log_types],
        "status_breakdown": [dict(row) for row in status_breakdown],
        "priority_breakdown": [dict(row) for row in priority_breakdown],
        "category_breakdown": [dict(row) for row in category_breakdown],
    }


def get_technician_summary(db_path: Path, technician_query: str, limit_open: int = 10, limit_recent: int = 10) -> dict:
    with connect(db_path) as conn:
        technician = conn.execute(
            """
            SELECT id, display_name, email
            FROM technicians
            WHERE id = ? OR display_name = ? COLLATE NOCASE OR display_name LIKE ? COLLATE NOCASE
            ORDER BY CASE WHEN id = ? THEN 0 WHEN display_name = ? COLLATE NOCASE THEN 1 ELSE 2 END, display_name ASC
            LIMIT 1
            """,
            (technician_query, technician_query, f"%{technician_query}%", technician_query, technician_query),
        ).fetchone()
        if not technician:
            fallback_technician = conn.execute(
                """
                SELECT assigned_technician_id AS id, assigned_technician_id AS display_name, NULL AS email
                FROM tickets
                WHERE assigned_technician_id = ?
                LIMIT 1
                """,
                (technician_query,),
            ).fetchone()
            if not fallback_technician:
                return {"status": "not_found", "technician_query": technician_query}
            technician = fallback_technician
        open_tickets = conn.execute(
            """
            SELECT id, subject, status, priority, category, updated_at
            FROM tickets
            WHERE assigned_technician_id = ? AND status = 'Open'
            ORDER BY updated_at DESC, id DESC
            LIMIT ?
            """,
            (technician["id"], limit_open),
        ).fetchall()
        recent_tickets = conn.execute(
            """
            SELECT id, subject, status, priority, category, updated_at
            FROM tickets
            WHERE assigned_technician_id = ?
            ORDER BY updated_at DESC, id DESC
            LIMIT ?
            """,
            (technician["id"], limit_recent),
        ).fetchall()
        stats = conn.execute(
            """
            WITH log_tickets AS (
                SELECT DISTINCT ticket_id FROM ticket_logs
            ),
            attachment_tickets AS (
                SELECT DISTINCT ticket_id FROM ticket_attachments
            ),
            chunk_counts AS (
                SELECT ticket_id, COUNT(*) AS chunk_count
                FROM ticket_document_chunks
                GROUP BY ticket_id
            )
            SELECT COUNT(*) AS total_tickets,
                   SUM(CASE WHEN t.status = 'Open' THEN 1 ELSE 0 END) AS open_tickets,
                   SUM(CASE WHEN t.status = 'Closed' THEN 1 ELSE 0 END) AS closed_tickets,
                   MAX(t.updated_at) AS latest_activity_at,
                   SUM(CASE WHEN td.ticket_id IS NOT NULL THEN 1 ELSE 0 END) AS detail_tickets,
                   SUM(CASE WHEN lt.ticket_id IS NOT NULL THEN 1 ELSE 0 END) AS log_tickets,
                   SUM(CASE WHEN at.ticket_id IS NOT NULL THEN 1 ELSE 0 END) AS attachment_tickets,
                   SUM(CASE WHEN doc.ticket_id IS NOT NULL THEN 1 ELSE 0 END) AS document_tickets,
                   COALESCE(SUM(cc.chunk_count), 0) AS chunk_count
            FROM tickets t
            LEFT JOIN ticket_details td ON td.ticket_id = t.id
            LEFT JOIN log_tickets lt ON lt.ticket_id = t.id
            LEFT JOIN attachment_tickets at ON at.ticket_id = t.id
            LEFT JOIN ticket_documents doc ON doc.ticket_id = t.id
            LEFT JOIN chunk_counts cc ON cc.ticket_id = t.id
            WHERE t.assigned_technician_id = ?
            """,
            (technician["id"],),
        ).fetchone()
        recent_log_types = conn.execute(
            """
            SELECT COALESCE(tl.log_type, 'unknown') AS log_type, COUNT(*) AS log_count
            FROM ticket_logs tl
            JOIN tickets t ON t.id = tl.ticket_id
            WHERE t.assigned_technician_id = ?
            GROUP BY COALESCE(tl.log_type, 'unknown')
            ORDER BY log_count DESC, log_type ASC
            LIMIT 10
            """,
            (technician["id"],),
        ).fetchall()
        status_breakdown = conn.execute(
            """
            SELECT COALESCE(status, 'unknown') AS status, COUNT(*) AS ticket_count
            FROM tickets
            WHERE assigned_technician_id = ?
            GROUP BY COALESCE(status, 'unknown')
            ORDER BY ticket_count DESC, status ASC
            """,
            (technician["id"],),
        ).fetchall()
        priority_breakdown = conn.execute(
            """
            SELECT COALESCE(priority, 'unknown') AS priority, COUNT(*) AS ticket_count
            FROM tickets
            WHERE assigned_technician_id = ?
            GROUP BY COALESCE(priority, 'unknown')
            ORDER BY ticket_count DESC, priority ASC
            LIMIT 10
            """,
            (technician["id"],),
        ).fetchall()
        category_breakdown = conn.execute(
            """
            SELECT COALESCE(category, 'unknown') AS category, COUNT(*) AS ticket_count
            FROM tickets
            WHERE assigned_technician_id = ?
            GROUP BY COALESCE(category, 'unknown')
            ORDER BY ticket_count DESC, category ASC
            LIMIT 10
            """,
            (technician["id"],),
        ).fetchall()
    stats_dict = dict(stats)
    total_tickets = int(stats_dict.get("total_tickets") or 0)
    detail_tickets = int(stats_dict.get("detail_tickets") or 0)
    log_tickets = int(stats_dict.get("log_tickets") or 0)
    attachment_tickets = int(stats_dict.get("attachment_tickets") or 0)
    document_tickets = int(stats_dict.get("document_tickets") or 0)
    stats_dict.update({
        "detail_coverage_ratio": _ratio(detail_tickets, total_tickets),
        "log_coverage_ratio": _ratio(log_tickets, total_tickets),
        "attachment_coverage_ratio": _ratio(attachment_tickets, total_tickets),
        "document_coverage_ratio": _ratio(document_tickets, total_tickets),
    })
    with connect(db_path) as conn:
        retrieval_health = _entity_retrieval_health(conn, "t.assigned_technician_id = ?", (technician["id"],))
    return {
        "status": "ok",
        "technician": {"id": technician["id"], "display_name": technician["display_name"], "email": technician["email"]},
        "stats": stats_dict,
        "retrieval_health": retrieval_health,
        "open_tickets": [dict(row) for row in open_tickets],
        "recent_tickets": [dict(row) for row in recent_tickets],
        "recent_log_types": [dict(row) for row in recent_log_types],
        "status_breakdown": [dict(row) for row in status_breakdown],
        "priority_breakdown": [dict(row) for row in priority_breakdown],
        "category_breakdown": [dict(row) for row in category_breakdown],
    }
