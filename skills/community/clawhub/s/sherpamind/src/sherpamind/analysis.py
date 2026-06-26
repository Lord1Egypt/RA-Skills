from __future__ import annotations

from pathlib import Path

from .db import connect, initialize_db
from .documents import DOCUMENT_MATERIALIZATION_VERSION


_DETAIL_PRESSURE_DIMENSIONS: tuple[tuple[str, str, int], ...] = (
    ("accounts", "COALESCE(NULLIF(a.name, ''), NULLIF(t.account_id, ''), 'unknown')", 10),
    (
        "categories",
        "COALESCE(NULLIF(t.category, ''), NULLIF(json_extract(t.raw_json, '$.creation_category_name'), ''), NULLIF(json_extract(t.raw_json, '$.class_name'), ''), NULLIF(json_extract(t.raw_json, '$.submission_category'), ''), 'unknown')",
        10,
    ),
    ("technicians", "COALESCE(NULLIF(te.display_name, ''), NULLIF(t.assigned_technician_id, ''), 'unassigned')", 3),
)


def list_ticket_counts_by_account(db_path: Path, limit: int = 20) -> list[dict]:
    with connect(db_path) as conn:
        rows = conn.execute(
            """
            SELECT COALESCE(a.name, t.account_id, 'unknown') AS account,
                   COUNT(*) AS ticket_count
            FROM tickets t
            LEFT JOIN accounts a ON a.id = t.account_id
            GROUP BY COALESCE(a.name, t.account_id, 'unknown')
            ORDER BY ticket_count DESC, account ASC
            LIMIT ?
            """,
            (limit,),
        ).fetchall()
    return [dict(row) for row in rows]


def list_ticket_counts_by_status(db_path: Path) -> list[dict]:
    with connect(db_path) as conn:
        rows = conn.execute(
            """
            SELECT COALESCE(status, 'unknown') AS status,
                   COUNT(*) AS ticket_count
            FROM tickets
            GROUP BY COALESCE(status, 'unknown')
            ORDER BY ticket_count DESC, status ASC
            """
        ).fetchall()
    return [dict(row) for row in rows]


def list_ticket_counts_by_priority(db_path: Path) -> list[dict]:
    with connect(db_path) as conn:
        rows = conn.execute(
            """
            SELECT COALESCE(priority, 'unknown') AS priority,
                   COUNT(*) AS ticket_count
            FROM tickets
            GROUP BY COALESCE(priority, 'unknown')
            ORDER BY ticket_count DESC, priority ASC
            """
        ).fetchall()
    return [dict(row) for row in rows]


def list_ticket_counts_by_technician(db_path: Path, limit: int = 20) -> list[dict]:
    with connect(db_path) as conn:
        rows = conn.execute(
            """
            SELECT COALESCE(te.display_name, t.assigned_technician_id, 'unassigned') AS technician,
                   COUNT(*) AS ticket_count
            FROM tickets t
            LEFT JOIN technicians te ON te.id = t.assigned_technician_id
            GROUP BY COALESCE(te.display_name, t.assigned_technician_id, 'unassigned')
            ORDER BY ticket_count DESC, technician ASC
            LIMIT ?
            """,
            (limit,),
        ).fetchall()
    return [dict(row) for row in rows]


def list_recent_tickets(db_path: Path, limit: int = 20) -> list[dict]:
    with connect(db_path) as conn:
        rows = conn.execute(
            """
            SELECT t.id,
                   t.subject,
                   t.status,
                   t.priority,
                   COALESCE(a.name, t.account_id) AS account,
                   COALESCE(u.display_name, t.user_id) AS user,
                   COALESCE(te.display_name, t.assigned_technician_id) AS technician,
                   t.created_at,
                   t.updated_at,
                   t.closed_at
            FROM tickets t
            LEFT JOIN accounts a ON a.id = t.account_id
            LEFT JOIN users u ON u.id = t.user_id
            LEFT JOIN technicians te ON te.id = t.assigned_technician_id
            ORDER BY COALESCE(t.updated_at, t.created_at) DESC, t.id DESC
            LIMIT ?
            """,
            (limit,),
        ).fetchall()
    return [dict(row) for row in rows]


def list_open_ticket_ages(db_path: Path, limit: int = 20) -> list[dict]:
    with connect(db_path) as conn:
        rows = conn.execute(
            """
            SELECT t.id,
                   t.subject,
                   COALESCE(a.name, t.account_id) AS account,
                   COALESCE(u.display_name, t.user_id) AS user,
                   COALESCE(te.display_name, t.assigned_technician_id) AS technician,
                   t.priority,
                   t.status,
                   t.created_at,
                   t.updated_at,
                   ROUND((julianday('now') - julianday(REPLACE(substr(t.created_at, 1, 19), 'T', ' '))), 2) AS age_days,
                   ROUND((julianday('now') - julianday(REPLACE(substr(COALESCE(t.updated_at, t.created_at), 1, 19), 'T', ' '))), 2) AS days_since_update
            FROM tickets t
            LEFT JOIN accounts a ON a.id = t.account_id
            LEFT JOIN users u ON u.id = t.user_id
            LEFT JOIN technicians te ON te.id = t.assigned_technician_id
            WHERE t.status = 'Open'
            ORDER BY age_days DESC, days_since_update DESC, t.id ASC
            LIMIT ?
            """,
            (limit,),
        ).fetchall()
    return [dict(row) for row in rows]


def list_recent_account_activity(db_path: Path, days: int = 7, limit: int = 20) -> list[dict]:
    with connect(db_path) as conn:
        rows = conn.execute(
            """
            SELECT COALESCE(a.name, t.account_id, 'unknown') AS account,
                   COUNT(*) AS ticket_count,
                   SUM(CASE WHEN t.status = 'Open' THEN 1 ELSE 0 END) AS open_count,
                   SUM(CASE WHEN t.status = 'Closed' THEN 1 ELSE 0 END) AS closed_count,
                   MAX(COALESCE(t.updated_at, t.created_at)) AS latest_activity_at
            FROM tickets t
            LEFT JOIN accounts a ON a.id = t.account_id
            WHERE julianday(REPLACE(substr(COALESCE(t.updated_at, t.created_at), 1, 19), 'T', ' ')) >= julianday('now', ?)
            GROUP BY COALESCE(a.name, t.account_id, 'unknown')
            ORDER BY ticket_count DESC, latest_activity_at DESC, account ASC
            LIMIT ?
            """,
            (f'-{days} days', limit),
        ).fetchall()
    return [dict(row) for row in rows]


def list_technician_recent_load(db_path: Path, days: int = 7, limit: int = 20) -> list[dict]:
    with connect(db_path) as conn:
        rows = conn.execute(
            """
            SELECT COALESCE(te.display_name, t.assigned_technician_id, 'unassigned') AS technician,
                   COUNT(*) AS ticket_count,
                   SUM(CASE WHEN t.status = 'Open' THEN 1 ELSE 0 END) AS open_count,
                   SUM(CASE WHEN t.status = 'Closed' THEN 1 ELSE 0 END) AS closed_count,
                   MAX(COALESCE(t.updated_at, t.created_at)) AS latest_activity_at
            FROM tickets t
            LEFT JOIN technicians te ON te.id = t.assigned_technician_id
            WHERE julianday(REPLACE(substr(COALESCE(t.updated_at, t.created_at), 1, 19), 'T', ' ')) >= julianday('now', ?)
            GROUP BY COALESCE(te.display_name, t.assigned_technician_id, 'unassigned')
            ORDER BY ticket_count DESC, latest_activity_at DESC, technician ASC
            LIMIT ?
            """,
            (f'-{days} days', limit),
        ).fetchall()
    return [dict(row) for row in rows]


def list_ticket_log_types(db_path: Path, limit: int = 20) -> list[dict]:
    with connect(db_path) as conn:
        rows = conn.execute(
            """
            SELECT COALESCE(log_type, 'unknown') AS log_type,
                   COUNT(*) AS log_count
            FROM ticket_logs
            GROUP BY COALESCE(log_type, 'unknown')
            ORDER BY log_count DESC, log_type ASC
            LIMIT ?
            """,
            (limit,),
        ).fetchall()
    return [dict(row) for row in rows]


def list_ticket_attachment_summary(db_path: Path, limit: int = 20) -> list[dict]:
    with connect(db_path) as conn:
        rows = conn.execute(
            """
            SELECT t.id AS ticket_id,
                   t.subject,
                   COUNT(*) AS attachment_count,
                   SUM(COALESCE(ta.size, 0)) AS total_attachment_bytes,
                   MAX(ta.recorded_at) AS latest_attachment_at
            FROM ticket_attachments ta
            JOIN tickets t ON t.id = ta.ticket_id
            GROUP BY t.id, t.subject
            ORDER BY attachment_count DESC, total_attachment_bytes DESC, t.id DESC
            LIMIT ?
            """,
            (limit,),
        ).fetchall()
    return [dict(row) for row in rows]


def search_ticket_documents(
    db_path: Path,
    query: str,
    limit: int = 20,
    account: str | None = None,
    status: str | None = None,
    technician: str | None = None,
    priority: str | None = None,
    category: str | None = None,
    class_name: str | None = None,
    submission_category: str | None = None,
    resolution_category: str | None = None,
    department: str | None = None,
) -> list[dict]:
    needle = f"%{query}%"
    clauses = [
        "(d.text LIKE ? COLLATE NOCASE OR d.account LIKE ? COLLATE NOCASE OR d.user_name LIKE ? COLLATE NOCASE OR d.technician LIKE ? COLLATE NOCASE)"
    ]
    params: list = [needle, needle, needle, needle]
    if account:
        clauses.append("d.account LIKE ? COLLATE NOCASE")
        params.append(f"%{account}%")
    if status:
        clauses.append("d.status = ?")
        params.append(status)
    if technician:
        clauses.append("d.technician LIKE ? COLLATE NOCASE")
        params.append(f"%{technician}%")
    if priority:
        clauses.append("json_extract(d.raw_json, '$.metadata.priority') = ?")
        params.append(priority)
    if category:
        clauses.append("json_extract(d.raw_json, '$.metadata.category') LIKE ? COLLATE NOCASE")
        params.append(f"%{category}%")
    if class_name:
        clauses.append("json_extract(d.raw_json, '$.metadata.class_name') LIKE ? COLLATE NOCASE")
        params.append(f"%{class_name}%")
    if submission_category:
        clauses.append("json_extract(d.raw_json, '$.metadata.submission_category') LIKE ? COLLATE NOCASE")
        params.append(f"%{submission_category}%")
    if resolution_category:
        clauses.append("json_extract(d.raw_json, '$.metadata.resolution_category') LIKE ? COLLATE NOCASE")
        params.append(f"%{resolution_category}%")
    if department:
        clauses.append("json_extract(d.raw_json, '$.metadata.department_label') LIKE ? COLLATE NOCASE")
        params.append(f"%{department}%")
    where = " AND ".join(clauses)
    with connect(db_path) as conn:
        rows = conn.execute(
            f"""
            SELECT d.doc_id, d.ticket_id, d.status, d.account, d.user_name, d.technician, d.updated_at, d.text,
                   json_extract(d.raw_json, '$.metadata.priority') AS priority,
                   json_extract(d.raw_json, '$.metadata.category') AS category,
                   json_extract(d.raw_json, '$.metadata.class_name') AS class_name,
                   json_extract(d.raw_json, '$.metadata.submission_category') AS submission_category,
                   json_extract(d.raw_json, '$.metadata.resolution_category') AS resolution_category,
                   json_extract(d.raw_json, '$.metadata.department_label') AS department_label
            FROM ticket_documents d
            WHERE {where}
            ORDER BY d.updated_at DESC, d.ticket_id DESC
            LIMIT ?
            """,
            (*params, limit),
        ).fetchall()
    return [dict(row) for row in rows]


def search_ticket_document_chunks(
    db_path: Path,
    query: str,
    limit: int = 20,
    account: str | None = None,
    status: str | None = None,
    technician: str | None = None,
    priority: str | None = None,
    category: str | None = None,
    class_name: str | None = None,
    submission_category: str | None = None,
    resolution_category: str | None = None,
    department: str | None = None,
) -> list[dict]:
    needle = f"%{query}%"
    clauses = ["c.text LIKE ? COLLATE NOCASE"]
    params: list = [needle]
    if account:
        clauses.append("d.account LIKE ? COLLATE NOCASE")
        params.append(f"%{account}%")
    if status:
        clauses.append("d.status = ?")
        params.append(status)
    if technician:
        clauses.append("d.technician LIKE ? COLLATE NOCASE")
        params.append(f"%{technician}%")
    if priority:
        clauses.append("json_extract(d.raw_json, '$.metadata.priority') = ?")
        params.append(priority)
    if category:
        clauses.append("json_extract(d.raw_json, '$.metadata.category') LIKE ? COLLATE NOCASE")
        params.append(f"%{category}%")
    if class_name:
        clauses.append("json_extract(d.raw_json, '$.metadata.class_name') LIKE ? COLLATE NOCASE")
        params.append(f"%{class_name}%")
    if submission_category:
        clauses.append("json_extract(d.raw_json, '$.metadata.submission_category') LIKE ? COLLATE NOCASE")
        params.append(f"%{submission_category}%")
    if resolution_category:
        clauses.append("json_extract(d.raw_json, '$.metadata.resolution_category') LIKE ? COLLATE NOCASE")
        params.append(f"%{resolution_category}%")
    if department:
        clauses.append("json_extract(d.raw_json, '$.metadata.department_label') LIKE ? COLLATE NOCASE")
        params.append(f"%{department}%")
    where = " AND ".join(clauses)
    with connect(db_path) as conn:
        rows = conn.execute(
            f"""
            SELECT c.chunk_id, c.doc_id, c.ticket_id, c.chunk_index, c.text,
                   d.status, d.account, d.technician, d.updated_at,
                   json_extract(d.raw_json, '$.metadata.priority') AS priority,
                   json_extract(d.raw_json, '$.metadata.category') AS category,
                   json_extract(d.raw_json, '$.metadata.class_name') AS class_name,
                   json_extract(d.raw_json, '$.metadata.submission_category') AS submission_category,
                   json_extract(d.raw_json, '$.metadata.resolution_category') AS resolution_category,
                   json_extract(d.raw_json, '$.metadata.department_label') AS department_label
            FROM ticket_document_chunks c
            JOIN ticket_documents d ON d.doc_id = c.doc_id
            WHERE {where}
            ORDER BY d.updated_at DESC, c.ticket_id DESC, c.chunk_index ASC
            LIMIT ?
            """,
            (*params, limit),
        ).fetchall()
    return [dict(row) for row in rows]


def _list_detail_gap_groups(conn, label_sql: str, *, min_tickets: int, limit: int = 10) -> list[dict]:
    rows = conn.execute(
        f"""
        WITH grouped AS (
            SELECT {label_sql} AS label,
                   CASE WHEN td.ticket_id IS NULL THEN 0 ELSE 1 END AS has_detail,
                   t.status,
                   CASE
                       WHEN t.status = 'Closed'
                            AND t.closed_at IS NOT NULL
                            AND julianday(REPLACE(substr(t.closed_at, 1, 19), 'T', ' ')) >= julianday('now', '-7 days') THEN 1
                       ELSE 0
                   END AS is_warm_closed,
                   COALESCE(t.updated_at, t.created_at) AS activity_at
            FROM tickets t
            LEFT JOIN ticket_details td ON td.ticket_id = t.id
            LEFT JOIN accounts a ON a.id = t.account_id
            LEFT JOIN technicians te ON te.id = t.assigned_technician_id
        )
        SELECT label,
               COUNT(*) AS total_tickets,
               SUM(has_detail) AS detail_tickets,
               SUM(CASE WHEN has_detail = 0 THEN 1 ELSE 0 END) AS detail_backlog,
               ROUND(CAST(SUM(has_detail) AS FLOAT) / COUNT(*), 4) AS detail_ratio,
               SUM(CASE WHEN status = 'Open' THEN 1 ELSE 0 END) AS open_tickets,
               SUM(CASE WHEN status = 'Open' AND has_detail = 1 THEN 1 ELSE 0 END) AS open_detail_tickets,
               SUM(CASE WHEN status = 'Open' AND has_detail = 0 THEN 1 ELSE 0 END) AS open_without_detail,
               SUM(is_warm_closed) AS warm_closed_tickets,
               SUM(CASE WHEN is_warm_closed = 1 AND has_detail = 1 THEN 1 ELSE 0 END) AS warm_closed_detail_tickets,
               SUM(CASE WHEN is_warm_closed = 1 AND has_detail = 0 THEN 1 ELSE 0 END) AS warm_closed_without_detail,
               MAX(activity_at) AS latest_activity_at
        FROM grouped
        GROUP BY label
        HAVING COUNT(*) >= ?
        ORDER BY detail_ratio ASC, detail_backlog DESC, total_tickets DESC, label ASC
        LIMIT ?
        """,
        (min_tickets, limit),
    ).fetchall()
    return [dict(row) for row in rows]


def _summarize_detail_gap_groups(rows: list[dict], *, min_tickets: int) -> dict:
    return {
        "min_tickets": min_tickets,
        "group_count": len(rows),
        "zero_detail_groups": sum(1 for row in rows if int(row.get("detail_tickets") or 0) == 0),
        "low_coverage_groups": sum(1 for row in rows if float(row.get("detail_ratio") or 0.0) < 0.25),
        "backlog_tickets": sum(int(row.get("detail_backlog") or 0) for row in rows),
        "open_backlog_tickets": sum(int(row.get("open_without_detail") or 0) for row in rows),
        "warm_closed_backlog_tickets": sum(int(row.get("warm_closed_without_detail") or 0) for row in rows),
    }


def get_enrichment_coverage(db_path: Path) -> dict:
    initialize_db(db_path)
    with connect(db_path) as conn:
        totals = conn.execute(
            """
            SELECT
                COUNT(*) AS total_tickets,
                SUM(CASE WHEN status = 'Open' THEN 1 ELSE 0 END) AS open_tickets,
                SUM(CASE WHEN status = 'Closed' THEN 1 ELSE 0 END) AS closed_tickets
            FROM tickets
            """
        ).fetchone()
        detail = conn.execute("SELECT COUNT(*) AS c FROM ticket_details").fetchone()["c"]
        logs = conn.execute("SELECT COUNT(DISTINCT ticket_id) AS c FROM ticket_logs").fetchone()["c"]
        attachments = conn.execute("SELECT COUNT(DISTINCT ticket_id) AS c FROM ticket_attachments").fetchone()["c"]
        open_detail = conn.execute(
            """
            SELECT COUNT(*) AS c
            FROM tickets t
            JOIN ticket_details td ON td.ticket_id = t.id
            WHERE t.status = 'Open'
            """
        ).fetchone()["c"]
        warm_detail = conn.execute(
            """
            SELECT COUNT(*) AS c
            FROM tickets t
            JOIN ticket_details td ON td.ticket_id = t.id
            WHERE t.status = 'Closed'
              AND t.closed_at IS NOT NULL
              AND julianday(REPLACE(substr(t.closed_at, 1, 19), 'T', ' ')) >= julianday('now', '-7 days')
            """
        ).fetchone()["c"]
        retrieval = conn.execute(
            """
            SELECT
                (SELECT COUNT(*) FROM ticket_documents) AS ticket_documents,
                (SELECT COUNT(*) FROM ticket_document_chunks) AS ticket_document_chunks,
                (SELECT COUNT(DISTINCT ticket_id) FROM ticket_document_chunks) AS chunk_ticket_coverage,
                (SELECT COALESCE(AVG(LENGTH(text)), 0) FROM ticket_document_chunks) AS avg_chunk_chars,
                (SELECT COALESCE(MAX(LENGTH(text)), 0) FROM ticket_document_chunks) AS max_chunk_chars,
                (SELECT COUNT(*) FROM ticket_document_chunks WHERE LENGTH(text) < 200) AS tiny_chunk_count,
                (SELECT COUNT(*) FROM ticket_document_chunks WHERE LENGTH(text) > 1800) AS over_target_chunk_count,
                (SELECT COUNT(*) FROM ticket_document_chunks WHERE chunk_index > 0) AS multi_chunk_rows,
                (SELECT COUNT(*) FROM ticket_documents WHERE COALESCE(json_extract(raw_json, '$.materialization_version'), json_extract(raw_json, '$.metadata.materialization_version'), 0) = {version}) AS current_materialization_docs,
                (SELECT COUNT(*) FROM ticket_documents WHERE COALESCE(json_extract(raw_json, '$.materialization_version'), json_extract(raw_json, '$.metadata.materialization_version')) IS NULL) AS unversioned_docs
            """.format(version=DOCUMENT_MATERIALIZATION_VERSION)
        ).fetchone()
        metadata = conn.execute(
            """
            SELECT
                COUNT(*) AS total_documents,
                SUM(CASE WHEN json_extract(raw_json, '$.metadata.priority') IS NOT NULL AND json_extract(raw_json, '$.metadata.priority') != '' THEN 1 ELSE 0 END) AS priority_docs,
                SUM(CASE WHEN json_extract(raw_json, '$.metadata.category') IS NOT NULL AND json_extract(raw_json, '$.metadata.category') != '' THEN 1 ELSE 0 END) AS category_docs,
                SUM(CASE WHEN json_extract(raw_json, '$.metadata.cleaned_subject') IS NOT NULL AND json_extract(raw_json, '$.metadata.cleaned_subject') != '' THEN 1 ELSE 0 END) AS cleaned_subject_docs,
                SUM(CASE WHEN json_extract(raw_json, '$.metadata.cleaned_initial_post') IS NOT NULL AND json_extract(raw_json, '$.metadata.cleaned_initial_post') != '' THEN 1 ELSE 0 END) AS issue_summary_docs,
                SUM(CASE WHEN json_extract(raw_json, '$.metadata.cleaned_detail_note') IS NOT NULL AND json_extract(raw_json, '$.metadata.cleaned_detail_note') != '' THEN 1 ELSE 0 END) AS detail_note_docs,
                SUM(CASE WHEN json_extract(raw_json, '$.metadata.cleaned_workpad') IS NOT NULL AND json_extract(raw_json, '$.metadata.cleaned_workpad') != '' THEN 1 ELSE 0 END) AS workpad_docs,
                SUM(CASE WHEN json_extract(raw_json, '$.metadata.cleaned_followup_note') IS NOT NULL AND json_extract(raw_json, '$.metadata.cleaned_followup_note') != '' THEN 1 ELSE 0 END) AS followup_note_docs,
                SUM(CASE WHEN json_extract(raw_json, '$.metadata.cleaned_next_step') IS NOT NULL AND json_extract(raw_json, '$.metadata.cleaned_next_step') != '' THEN 1 ELSE 0 END) AS next_step_docs,
                SUM(CASE WHEN json_extract(raw_json, '$.metadata.cleaned_action_cue') IS NOT NULL AND json_extract(raw_json, '$.metadata.cleaned_action_cue') != '' THEN 1 ELSE 0 END) AS action_cue_docs,
                SUM(CASE WHEN json_extract(raw_json, '$.metadata.cleaned_latest_response_note') IS NOT NULL AND json_extract(raw_json, '$.metadata.cleaned_latest_response_note') != '' THEN 1 ELSE 0 END) AS latest_response_note_docs,
                SUM(CASE WHEN json_extract(raw_json, '$.metadata.latest_response_date') IS NOT NULL AND json_extract(raw_json, '$.metadata.latest_response_date') != '' THEN 1 ELSE 0 END) AS latest_response_date_docs,
                SUM(CASE WHEN json_extract(raw_json, '$.metadata.cleaned_resolution_log_note') IS NOT NULL AND json_extract(raw_json, '$.metadata.cleaned_resolution_log_note') != '' THEN 1 ELSE 0 END) AS resolution_log_note_docs,
                SUM(CASE WHEN json_extract(raw_json, '$.metadata.resolution_log_date') IS NOT NULL AND json_extract(raw_json, '$.metadata.resolution_log_date') != '' THEN 1 ELSE 0 END) AS resolution_log_date_docs,
                SUM(CASE WHEN json_extract(raw_json, '$.metadata.next_step_date') IS NOT NULL AND json_extract(raw_json, '$.metadata.next_step_date') != '' THEN 1 ELSE 0 END) AS next_step_date_docs,
                SUM(CASE WHEN json_extract(raw_json, '$.metadata.recent_log_types_csv') IS NOT NULL AND json_extract(raw_json, '$.metadata.recent_log_types_csv') != '' THEN 1 ELSE 0 END) AS recent_log_types_docs,
                SUM(CASE WHEN json_extract(raw_json, '$.metadata.initial_response_present') = 1 THEN 1 ELSE 0 END) AS initial_response_docs,
                SUM(CASE WHEN json_extract(raw_json, '$.metadata.user_email') IS NOT NULL AND json_extract(raw_json, '$.metadata.user_email') != '' THEN 1 ELSE 0 END) AS user_email_docs,
                SUM(CASE WHEN json_extract(raw_json, '$.metadata.resolution_summary') IS NOT NULL AND json_extract(raw_json, '$.metadata.resolution_summary') != '' THEN 1 ELSE 0 END) AS resolution_summary_docs,
                SUM(CASE WHEN json_extract(raw_json, '$.metadata.detail_available') = 1 THEN 1 ELSE 0 END) AS detail_available_docs,
                SUM(CASE WHEN json_extract(raw_json, '$.metadata.attachments_count') IS NOT NULL THEN 1 ELSE 0 END) AS attachment_count_docs,
                SUM(CASE WHEN json_extract(raw_json, '$.metadata.has_attachments') = 1 THEN 1 ELSE 0 END) AS attachment_presence_docs
            FROM ticket_documents
            """
        ).fetchone()
        detail_gap_pressure = {
            dimension: {
                "summary": _summarize_detail_gap_groups(rows := _list_detail_gap_groups(conn, label_sql, min_tickets=min_tickets), min_tickets=min_tickets),
                "rows": rows,
            }
            for dimension, label_sql, min_tickets in _DETAIL_PRESSURE_DIMENSIONS
        }
    total_tickets = int(totals["total_tickets"] or 0)
    open_tickets = int(totals["open_tickets"] or 0)
    closed_tickets = int(totals["closed_tickets"] or 0)
    detail_count = int(detail or 0)
    log_count = int(logs or 0)
    attachment_count = int(attachments or 0)
    open_detail_count = int(open_detail or 0)
    warm_detail_count = int(warm_detail or 0)
    document_count = int(retrieval["ticket_documents"] or 0)
    chunk_count = int(retrieval["ticket_document_chunks"] or 0)
    chunk_ticket_coverage = int(retrieval["chunk_ticket_coverage"] or 0)
    total_documents = int(metadata["total_documents"] or 0)
    return {
        "total_tickets": total_tickets,
        "open_tickets": open_tickets,
        "closed_tickets": closed_tickets,
        "ticket_details_covered": detail_count,
        "ticket_logs_covered": log_count,
        "ticket_attachments_covered": attachment_count,
        "detail_coverage_ratio": round((detail_count / total_tickets), 4) if total_tickets else 0.0,
        "open_detail_coverage": open_detail_count,
        "open_detail_coverage_ratio": round((open_detail_count / open_tickets), 4) if open_tickets else 0.0,
        "warm_detail_coverage": warm_detail_count,
        "warm_detail_coverage_ratio": round((warm_detail_count / closed_tickets), 4) if closed_tickets else 0.0,
        "document_coverage_ratio": round((document_count / total_tickets), 4) if total_tickets else 0.0,
        "chunk_ticket_coverage_ratio": round((chunk_ticket_coverage / total_tickets), 4) if total_tickets else 0.0,
        "tickets": {
            "total": total_tickets,
            "open": open_tickets,
            "closed": closed_tickets,
        },
        "detail_gap_pressure": detail_gap_pressure,
        "enrichment": {
            "ticket_details_covered": detail_count,
            "ticket_logs_covered": log_count,
            "ticket_attachments_covered": attachment_count,
            "detail_coverage_ratio": round((detail_count / total_tickets), 4) if total_tickets else 0.0,
            "open_detail_coverage": open_detail_count,
            "open_detail_coverage_ratio": round((open_detail_count / open_tickets), 4) if open_tickets else 0.0,
            "warm_detail_coverage": warm_detail_count,
            "warm_detail_coverage_ratio": round((warm_detail_count / closed_tickets), 4) if closed_tickets else 0.0,
            "detail_backlog": max(total_tickets - detail_count, 0),
            "detail_gap_pressure": detail_gap_pressure,
        },
        "retrieval": {
            "ticket_documents": document_count,
            "ticket_document_chunks": chunk_count,
            "document_coverage_ratio": round((document_count / total_tickets), 4) if total_tickets else 0.0,
            "chunk_ticket_coverage": chunk_ticket_coverage,
            "chunk_ticket_coverage_ratio": round((chunk_ticket_coverage / total_tickets), 4) if total_tickets else 0.0,
            "multi_chunk_rows": int(retrieval["multi_chunk_rows"] or 0),
            "avg_chunk_chars": round(float(retrieval["avg_chunk_chars"] or 0), 1),
            "max_chunk_chars": int(retrieval["max_chunk_chars"] or 0),
            "tiny_chunk_count": int(retrieval["tiny_chunk_count"] or 0),
            "over_target_chunk_count": int(retrieval["over_target_chunk_count"] or 0),
            "materialization_version": DOCUMENT_MATERIALIZATION_VERSION,
            "current_materialization_docs": int(retrieval["current_materialization_docs"] or 0),
            "stale_materialization_docs": max(document_count - int(retrieval["current_materialization_docs"] or 0), 0),
            "stale_materialization_ratio": round((max(document_count - int(retrieval["current_materialization_docs"] or 0), 0) / document_count), 4) if document_count else 0.0,
            "unversioned_docs": int(retrieval["unversioned_docs"] or 0),
        },
        "metadata": {
            "total_documents": total_documents,
            "priority_docs": int(metadata["priority_docs"] or 0),
            "priority_coverage_ratio": round((int(metadata["priority_docs"] or 0) / total_documents), 4) if total_documents else 0.0,
            "category_docs": int(metadata["category_docs"] or 0),
            "category_coverage_ratio": round((int(metadata["category_docs"] or 0) / total_documents), 4) if total_documents else 0.0,
            "cleaned_subject_docs": int(metadata["cleaned_subject_docs"] or 0),
            "cleaned_subject_coverage_ratio": round((int(metadata["cleaned_subject_docs"] or 0) / total_documents), 4) if total_documents else 0.0,
            "issue_summary_docs": int(metadata["issue_summary_docs"] or 0),
            "issue_summary_coverage_ratio": round((int(metadata["issue_summary_docs"] or 0) / total_documents), 4) if total_documents else 0.0,
            "detail_note_docs": int(metadata["detail_note_docs"] or 0),
            "detail_note_coverage_ratio": round((int(metadata["detail_note_docs"] or 0) / total_documents), 4) if total_documents else 0.0,
            "workpad_docs": int(metadata["workpad_docs"] or 0),
            "workpad_coverage_ratio": round((int(metadata["workpad_docs"] or 0) / total_documents), 4) if total_documents else 0.0,
            "followup_note_docs": int(metadata["followup_note_docs"] or 0),
            "followup_note_coverage_ratio": round((int(metadata["followup_note_docs"] or 0) / total_documents), 4) if total_documents else 0.0,
            "next_step_docs": int(metadata["next_step_docs"] or 0),
            "next_step_coverage_ratio": round((int(metadata["next_step_docs"] or 0) / total_documents), 4) if total_documents else 0.0,
            "action_cue_docs": int(metadata["action_cue_docs"] or 0),
            "action_cue_coverage_ratio": round((int(metadata["action_cue_docs"] or 0) / total_documents), 4) if total_documents else 0.0,
            "latest_response_note_docs": int(metadata["latest_response_note_docs"] or 0),
            "latest_response_note_coverage_ratio": round((int(metadata["latest_response_note_docs"] or 0) / total_documents), 4) if total_documents else 0.0,
            "latest_response_date_docs": int(metadata["latest_response_date_docs"] or 0),
            "latest_response_date_coverage_ratio": round((int(metadata["latest_response_date_docs"] or 0) / total_documents), 4) if total_documents else 0.0,
            "resolution_log_note_docs": int(metadata["resolution_log_note_docs"] or 0),
            "resolution_log_note_coverage_ratio": round((int(metadata["resolution_log_note_docs"] or 0) / total_documents), 4) if total_documents else 0.0,
            "resolution_log_date_docs": int(metadata["resolution_log_date_docs"] or 0),
            "resolution_log_date_coverage_ratio": round((int(metadata["resolution_log_date_docs"] or 0) / total_documents), 4) if total_documents else 0.0,
            "next_step_date_docs": int(metadata["next_step_date_docs"] or 0),
            "next_step_date_coverage_ratio": round((int(metadata["next_step_date_docs"] or 0) / total_documents), 4) if total_documents else 0.0,
            "recent_log_types_docs": int(metadata["recent_log_types_docs"] or 0),
            "recent_log_types_coverage_ratio": round((int(metadata["recent_log_types_docs"] or 0) / total_documents), 4) if total_documents else 0.0,
            "initial_response_docs": int(metadata["initial_response_docs"] or 0),
            "initial_response_coverage_ratio": round((int(metadata["initial_response_docs"] or 0) / total_documents), 4) if total_documents else 0.0,
            "user_email_docs": int(metadata["user_email_docs"] or 0),
            "user_email_coverage_ratio": round((int(metadata["user_email_docs"] or 0) / total_documents), 4) if total_documents else 0.0,
            "resolution_summary_docs": int(metadata["resolution_summary_docs"] or 0),
            "resolution_summary_coverage_ratio": round((int(metadata["resolution_summary_docs"] or 0) / total_documents), 4) if total_documents else 0.0,
            "detail_available_docs": int(metadata["detail_available_docs"] or 0),
            "detail_available_coverage_ratio": round((int(metadata["detail_available_docs"] or 0) / total_documents), 4) if total_documents else 0.0,
            "attachment_count_docs": int(metadata["attachment_count_docs"] or 0),
            "attachment_count_coverage_ratio": round((int(metadata["attachment_count_docs"] or 0) / total_documents), 4) if total_documents else 0.0,
            "attachment_presence_docs": int(metadata["attachment_presence_docs"] or 0),
            "attachment_presence_coverage_ratio": round((int(metadata["attachment_presence_docs"] or 0) / total_documents), 4) if total_documents else 0.0,
        },
    }


def get_api_usage_summary(db_path: Path, hourly_limit: int = 600) -> dict:
    initialize_db(db_path)
    with connect(db_path) as conn:
        last_hour = conn.execute(
            """
            SELECT COUNT(*) AS request_count,
                   SUM(CASE WHEN status_code IS NOT NULL AND status_code >= 400 THEN 1 ELSE 0 END) AS error_count,
                   MIN(recorded_at) AS earliest_at,
                   MAX(recorded_at) AS latest_at
            FROM api_request_events
            WHERE julianday(recorded_at) >= julianday('now', '-1 hour')
            """
        ).fetchone()
        top_paths = conn.execute(
            """
            SELECT path, COUNT(*) AS request_count
            FROM api_request_events
            WHERE julianday(recorded_at) >= julianday('now', '-1 hour')
            GROUP BY path
            ORDER BY request_count DESC, path ASC
            LIMIT 10
            """
        ).fetchall()
    request_count = int(last_hour["request_count"] or 0)
    return {
        "requests_last_hour": request_count,
        "errors_last_hour": int(last_hour["error_count"] or 0),
        "remaining_hourly_budget": max(0, hourly_limit - request_count),
        "budget_utilization_ratio": round(request_count / hourly_limit, 4),
        "earliest_request_at": last_hour["earliest_at"],
        "latest_request_at": last_hour["latest_at"],
        "top_paths_last_hour": [dict(row) for row in top_paths],
    }


def get_dataset_summary(db_path: Path) -> dict:
    initialize_db(db_path)
    with connect(db_path) as conn:
        counts = {}
        for table in [
            "accounts",
            "users",
            "technicians",
            "tickets",
            "ticket_details",
            "ticket_attachments",
            "ticket_logs",
            "ticket_time_logs",
            "ticket_documents",
            "ticket_document_chunks",
            "ticket_comments",
            "ingest_runs",
            "api_request_events",
        ]:
            counts[table] = conn.execute(f"SELECT COUNT(*) AS c FROM {table}").fetchone()["c"]
        latest_run = conn.execute(
            "SELECT id, mode, started_at, finished_at, status, notes FROM ingest_runs ORDER BY id DESC LIMIT 1"
        ).fetchone()
    return {
        "counts": counts,
        "latest_ingest_run": dict(latest_run) if latest_run else None,
        "api_usage": get_api_usage_summary(db_path),
    }


def get_insight_snapshot(db_path: Path) -> dict:
    return {
        "dataset_summary": get_dataset_summary(db_path),
        "status_counts": list_ticket_counts_by_status(db_path),
        "priority_counts": list_ticket_counts_by_priority(db_path),
        "top_accounts": list_ticket_counts_by_account(db_path, limit=10),
        "top_technicians": list_ticket_counts_by_technician(db_path, limit=10),
        "oldest_open_tickets": list_open_ticket_ages(db_path, limit=10),
        "recent_account_activity_7d": list_recent_account_activity(db_path, days=7, limit=10),
        "recent_technician_load_7d": list_technician_recent_load(db_path, days=7, limit=10),
        "ticket_log_types": list_ticket_log_types(db_path, limit=10),
        "attachment_summary": list_ticket_attachment_summary(db_path, limit=10),
        "recent_tickets": list_recent_tickets(db_path, limit=10),
    }
