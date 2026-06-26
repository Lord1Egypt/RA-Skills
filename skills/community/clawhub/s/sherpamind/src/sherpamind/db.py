from __future__ import annotations

import json
import sqlite3
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

SCHEMA = """
PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS accounts (
    id TEXT PRIMARY KEY,
    name TEXT,
    raw_json TEXT NOT NULL,
    updated_at TEXT,
    synced_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS users (
    id TEXT PRIMARY KEY,
    account_id TEXT,
    display_name TEXT,
    email TEXT,
    raw_json TEXT NOT NULL,
    updated_at TEXT,
    synced_at TEXT NOT NULL,
    FOREIGN KEY(account_id) REFERENCES accounts(id)
);

CREATE TABLE IF NOT EXISTS technicians (
    id TEXT PRIMARY KEY,
    display_name TEXT,
    email TEXT,
    raw_json TEXT NOT NULL,
    updated_at TEXT,
    synced_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS tickets (
    id TEXT PRIMARY KEY,
    account_id TEXT,
    user_id TEXT,
    assigned_technician_id TEXT,
    subject TEXT,
    status TEXT,
    priority TEXT,
    category TEXT,
    created_at TEXT,
    updated_at TEXT,
    closed_at TEXT,
    raw_json TEXT NOT NULL,
    synced_at TEXT NOT NULL,
    FOREIGN KEY(account_id) REFERENCES accounts(id),
    FOREIGN KEY(user_id) REFERENCES users(id),
    FOREIGN KEY(assigned_technician_id) REFERENCES technicians(id)
);

CREATE TABLE IF NOT EXISTS ticket_details (
    ticket_id TEXT PRIMARY KEY,
    workpad TEXT,
    note TEXT,
    initial_response TEXT,
    sla_response_date TEXT,
    sla_complete_date TEXT,
    waiting_date TEXT,
    next_step_date TEXT,
    ticketlogs_count INTEGER NOT NULL DEFAULT 0,
    timelogs_count INTEGER NOT NULL DEFAULT 0,
    attachments_count INTEGER NOT NULL DEFAULT 0,
    raw_json TEXT NOT NULL,
    synced_at TEXT NOT NULL,
    FOREIGN KEY(ticket_id) REFERENCES tickets(id)
);

CREATE TABLE IF NOT EXISTS ticket_attachments (
    id TEXT PRIMARY KEY,
    ticket_id TEXT NOT NULL,
    name TEXT,
    url TEXT,
    size INTEGER,
    recorded_at TEXT,
    raw_json TEXT NOT NULL,
    synced_at TEXT NOT NULL,
    FOREIGN KEY(ticket_id) REFERENCES tickets(id)
);

CREATE TABLE IF NOT EXISTS ticket_logs (
    id TEXT PRIMARY KEY,
    ticket_id TEXT NOT NULL,
    log_type TEXT,
    record_date TEXT,
    note TEXT,
    plain_note TEXT,
    user_id TEXT,
    user_email TEXT,
    user_name TEXT,
    is_tech_only INTEGER,
    is_waiting INTEGER,
    raw_json TEXT NOT NULL,
    synced_at TEXT NOT NULL,
    FOREIGN KEY(ticket_id) REFERENCES tickets(id)
);

CREATE TABLE IF NOT EXISTS ticket_time_logs (
    id TEXT PRIMARY KEY,
    ticket_id TEXT NOT NULL,
    record_date TEXT,
    note TEXT,
    raw_json TEXT NOT NULL,
    synced_at TEXT NOT NULL,
    FOREIGN KEY(ticket_id) REFERENCES tickets(id)
);

CREATE TABLE IF NOT EXISTS ticket_comments (
    id TEXT PRIMARY KEY,
    ticket_id TEXT NOT NULL,
    author_type TEXT,
    author_id TEXT,
    created_at TEXT,
    body TEXT,
    raw_json TEXT NOT NULL,
    synced_at TEXT NOT NULL,
    FOREIGN KEY(ticket_id) REFERENCES tickets(id)
);

CREATE TABLE IF NOT EXISTS ticket_documents (
    doc_id TEXT PRIMARY KEY,
    ticket_id TEXT NOT NULL,
    status TEXT,
    account TEXT,
    user_name TEXT,
    technician TEXT,
    updated_at TEXT,
    text TEXT NOT NULL,
    raw_json TEXT NOT NULL,
    content_hash TEXT,
    synced_at TEXT NOT NULL,
    FOREIGN KEY(ticket_id) REFERENCES tickets(id)
);

CREATE TABLE IF NOT EXISTS ticket_document_chunks (
    chunk_id TEXT PRIMARY KEY,
    doc_id TEXT NOT NULL,
    ticket_id TEXT NOT NULL,
    chunk_index INTEGER NOT NULL,
    text TEXT NOT NULL,
    content_hash TEXT,
    synced_at TEXT NOT NULL,
    FOREIGN KEY(doc_id) REFERENCES ticket_documents(doc_id),
    FOREIGN KEY(ticket_id) REFERENCES tickets(id)
);

CREATE TABLE IF NOT EXISTS sync_state (
    key TEXT PRIMARY KEY,
    value TEXT NOT NULL,
    updated_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS ingest_runs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    mode TEXT NOT NULL,
    started_at TEXT NOT NULL,
    finished_at TEXT,
    status TEXT NOT NULL,
    notes TEXT
);

CREATE TABLE IF NOT EXISTS api_request_events (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    recorded_at TEXT NOT NULL,
    method TEXT NOT NULL,
    path TEXT NOT NULL,
    status_code INTEGER,
    outcome TEXT NOT NULL,
    attempt_kind TEXT,
    raw_json TEXT
);

CREATE TABLE IF NOT EXISTS vector_chunk_index (
    chunk_id TEXT PRIMARY KEY,
    doc_id TEXT NOT NULL,
    ticket_id TEXT NOT NULL,
    vector_json TEXT NOT NULL,
    dims INTEGER NOT NULL,
    content_hash TEXT,
    synced_at TEXT NOT NULL
);
"""


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def connect(db_path: Path) -> sqlite3.Connection:
    db_path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn


def _table_columns(conn: sqlite3.Connection, table_name: str) -> set[str]:
    rows = conn.execute(f"PRAGMA table_info({table_name})").fetchall()
    return {row['name'] for row in rows}


def initialize_db(db_path: Path) -> None:
    with connect(db_path) as conn:
        conn.executescript(SCHEMA)
        # Lightweight schema evolution for older local DBs created before new columns/tables existed.
        if 'ticket_documents' in {row['name'] for row in conn.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()}:
            ticket_doc_cols = _table_columns(conn, 'ticket_documents')
            if 'content_hash' not in ticket_doc_cols:
                conn.execute("ALTER TABLE ticket_documents ADD COLUMN content_hash TEXT")
        conn.commit()


def start_ingest_run(db_path: Path, mode: str, notes: str | None = None) -> int:
    with connect(db_path) as conn:
        cursor = conn.execute(
            "INSERT INTO ingest_runs(mode, started_at, status, notes) VALUES(?, ?, ?, ?)",
            (mode, now_iso(), "running", notes),
        )
        conn.commit()
        return int(cursor.lastrowid)


def finish_ingest_run(db_path: Path, run_id: int, status: str, notes: str | None = None) -> None:
    with connect(db_path) as conn:
        conn.execute(
            "UPDATE ingest_runs SET finished_at = ?, status = ?, notes = ? WHERE id = ?",
            (now_iso(), status, notes, run_id),
        )
        conn.commit()


def _json(value: Any) -> str:
    return json.dumps(value, sort_keys=True)


def upsert_accounts(db_path: Path, accounts: list[dict[str, Any]], synced_at: str | None = None) -> int:
    synced_at = synced_at or now_iso()
    with connect(db_path) as conn:
        for account in accounts:
            conn.execute(
                """
                INSERT INTO accounts(id, name, raw_json, updated_at, synced_at)
                VALUES(?, ?, ?, ?, ?)
                ON CONFLICT(id) DO UPDATE SET
                    name = CASE
                        WHEN excluded.name IS NOT NULL AND trim(excluded.name) <> ''
                        THEN excluded.name
                        ELSE accounts.name
                    END,
                    raw_json = CASE
                        WHEN json_extract(excluded.raw_json, '$.source') = 'ticket_stub'
                             AND COALESCE(json_extract(accounts.raw_json, '$.source'), '') <> 'ticket_stub'
                        THEN accounts.raw_json
                        ELSE excluded.raw_json
                    END,
                    updated_at = COALESCE(excluded.updated_at, accounts.updated_at),
                    synced_at = excluded.synced_at
                """,
                (
                    str(account["id"]),
                    account.get("name"),
                    _json(account),
                    account.get("updated") or account.get("updated_time"),
                    synced_at,
                ),
            )
        conn.commit()
    return len(accounts)


def _display_name(record: dict[str, Any]) -> str | None:
    return record.get("FullName") or record.get("full_name2") or " ".join(
        part for part in [record.get("firstname"), record.get("lastname")] if part
    ) or None


def _ticket_account_stub(ticket: dict[str, Any]) -> dict[str, Any] | None:
    account_id = ticket.get("account_id")
    if account_id is None:
        return None
    name = ticket.get("account_name") or ticket.get("company") or ticket.get("account") or None
    return {
        "id": account_id,
        "name": name,
        "updated": ticket.get("updated_time"),
        "source": "ticket_stub",
    }


def _ticket_user_stub(ticket: dict[str, Any]) -> dict[str, Any] | None:
    user_id = ticket.get("user_id")
    if user_id is None:
        return None
    display_name = (
        ticket.get("user_name")
        or ticket.get("contact_name")
        or ticket.get("requester_name")
        or " ".join(
            part
            for part in [ticket.get("user_firstname"), ticket.get("user_lastname")]
            if part
        )
        or None
    )
    return {
        "id": user_id,
        "account_id": ticket.get("account_id"),
        "FullName": display_name,
        "email": ticket.get("user_email"),
        "updated_time": ticket.get("updated_time"),
        "source": "ticket_stub",
    }


def _ticket_technician_stub(ticket: dict[str, Any]) -> dict[str, Any] | None:
    technician_id = ticket.get("tech_id")
    if technician_id is None:
        return None
    display_name = (
        ticket.get("assigned_technician_name")
        or ticket.get("technician_name")
        or ticket.get("tech_name")
        or " ".join(
            part
            for part in [ticket.get("technician_firstname"), ticket.get("technician_lastname")]
            if part
        )
        or None
    )
    return {
        "id": technician_id,
        "FullName": display_name,
        "email": ticket.get("technician_email"),
        "updated_time": ticket.get("updated_time"),
        "source": "ticket_stub",
    }


def upsert_users(db_path: Path, users: list[dict[str, Any]], synced_at: str | None = None) -> int:
    synced_at = synced_at or now_iso()
    with connect(db_path) as conn:
        for user in users:
            conn.execute(
                """
                INSERT INTO users(id, account_id, display_name, email, raw_json, updated_at, synced_at)
                VALUES(?, ?, ?, ?, ?, ?, ?)
                ON CONFLICT(id) DO UPDATE SET
                    account_id = COALESCE(excluded.account_id, users.account_id),
                    display_name = CASE
                        WHEN excluded.display_name IS NOT NULL AND trim(excluded.display_name) <> ''
                        THEN excluded.display_name
                        ELSE users.display_name
                    END,
                    email = COALESCE(excluded.email, users.email),
                    raw_json = CASE
                        WHEN json_extract(excluded.raw_json, '$.source') = 'ticket_stub'
                             AND COALESCE(json_extract(users.raw_json, '$.source'), '') <> 'ticket_stub'
                        THEN users.raw_json
                        ELSE excluded.raw_json
                    END,
                    updated_at = COALESCE(excluded.updated_at, users.updated_at),
                    synced_at = excluded.synced_at
                """,
                (
                    str(user["id"]),
                    str(user["account_id"]) if user.get("account_id") is not None else None,
                    _display_name(user),
                    user.get("email"),
                    _json(user),
                    user.get("updated") or user.get("modified") or user.get("updated_time"),
                    synced_at,
                ),
            )
        conn.commit()
    return len(users)


def upsert_technicians(db_path: Path, technicians: list[dict[str, Any]], synced_at: str | None = None) -> int:
    synced_at = synced_at or now_iso()
    with connect(db_path) as conn:
        for technician in technicians:
            display_name = _display_name(technician)
            email = technician.get("email")
            updated_at = technician.get("updated") or technician.get("modified") or technician.get("updated_time")
            conn.execute(
                """
                INSERT INTO technicians(id, display_name, email, raw_json, updated_at, synced_at)
                VALUES(?, ?, ?, ?, ?, ?)
                ON CONFLICT(id) DO UPDATE SET
                    display_name = CASE
                        WHEN excluded.display_name IS NOT NULL AND trim(excluded.display_name) <> ''
                        THEN excluded.display_name
                        ELSE technicians.display_name
                    END,
                    email = COALESCE(excluded.email, technicians.email),
                    raw_json = CASE
                        WHEN json_extract(excluded.raw_json, '$.source') = 'ticket_stub'
                             AND COALESCE(json_extract(technicians.raw_json, '$.source'), '') <> 'ticket_stub'
                        THEN technicians.raw_json
                        ELSE excluded.raw_json
                    END,
                    updated_at = COALESCE(excluded.updated_at, technicians.updated_at),
                    synced_at = excluded.synced_at
                """,
                (
                    str(technician["id"]),
                    display_name,
                    email,
                    _json(technician),
                    updated_at,
                    synced_at,
                ),
            )
        conn.commit()
    return len(technicians)


def upsert_tickets(db_path: Path, tickets: list[dict[str, Any]], synced_at: str | None = None) -> int:
    synced_at = synced_at or now_iso()
    account_stubs = [stub for ticket in tickets if (stub := _ticket_account_stub(ticket)) is not None]
    if account_stubs:
        upsert_accounts(db_path, account_stubs, synced_at=synced_at)
    user_stubs = [stub for ticket in tickets if (stub := _ticket_user_stub(ticket)) is not None]
    if user_stubs:
        upsert_users(db_path, user_stubs, synced_at=synced_at)
    technician_stubs = [stub for ticket in tickets if (stub := _ticket_technician_stub(ticket)) is not None]
    if technician_stubs:
        upsert_technicians(db_path, technician_stubs, synced_at=synced_at)
    with connect(db_path) as conn:
        for ticket in tickets:
            conn.execute(
                """
                INSERT INTO tickets(
                    id, account_id, user_id, assigned_technician_id, subject, status, priority, category,
                    created_at, updated_at, closed_at, raw_json, synced_at
                )
                VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ON CONFLICT(id) DO UPDATE SET
                    account_id = excluded.account_id,
                    user_id = excluded.user_id,
                    assigned_technician_id = excluded.assigned_technician_id,
                    subject = excluded.subject,
                    status = excluded.status,
                    priority = excluded.priority,
                    category = excluded.category,
                    created_at = excluded.created_at,
                    updated_at = excluded.updated_at,
                    closed_at = excluded.closed_at,
                    raw_json = excluded.raw_json,
                    synced_at = excluded.synced_at
                """,
                (
                    str(ticket["id"]),
                    str(ticket["account_id"]) if ticket.get("account_id") is not None else None,
                    str(ticket["user_id"]) if ticket.get("user_id") is not None else None,
                    str(ticket["tech_id"]) if ticket.get("tech_id") is not None else None,
                    ticket.get("subject"),
                    ticket.get("status"),
                    ticket.get("priority_name") or ticket.get("priority"),
                    ticket.get("creation_category_name") or ticket.get("category"),
                    ticket.get("created_time"),
                    ticket.get("updated_time"),
                    ticket.get("closed_time"),
                    _json(ticket),
                    synced_at,
                ),
            )
        conn.commit()
    return len(tickets)


def backfill_ticket_entity_stubs(db_path: Path, synced_at: str | None = None) -> dict[str, Any]:
    synced_at = synced_at or now_iso()
    with connect(db_path) as conn:
        ticket_rows = conn.execute("SELECT raw_json FROM tickets").fetchall()
        before_counts = {
            "accounts": int(conn.execute("SELECT COUNT(*) AS c FROM accounts").fetchone()["c"]),
            "users": int(conn.execute("SELECT COUNT(*) AS c FROM users").fetchone()["c"]),
            "technicians": int(conn.execute("SELECT COUNT(*) AS c FROM technicians").fetchone()["c"]),
        }

    def _collect_stubs(factory):
        stubs = []
        seen_ids: set[str] = set()
        for row in ticket_rows:
            ticket = json.loads(row["raw_json"])
            stub = factory(ticket)
            if not stub:
                continue
            stub_id = str(stub["id"])
            if stub_id in seen_ids:
                continue
            seen_ids.add(stub_id)
            stubs.append(stub)
        return stubs

    account_stubs = _collect_stubs(_ticket_account_stub)
    user_stubs = _collect_stubs(_ticket_user_stub)
    technician_stubs = _collect_stubs(_ticket_technician_stub)

    if account_stubs:
        upsert_accounts(db_path, account_stubs, synced_at=synced_at)
    if user_stubs:
        upsert_users(db_path, user_stubs, synced_at=synced_at)
    if technician_stubs:
        upsert_technicians(db_path, technician_stubs, synced_at=synced_at)

    with connect(db_path) as conn:
        after_counts = {
            "accounts": int(conn.execute("SELECT COUNT(*) AS c FROM accounts").fetchone()["c"]),
            "users": int(conn.execute("SELECT COUNT(*) AS c FROM users").fetchone()["c"]),
            "technicians": int(conn.execute("SELECT COUNT(*) AS c FROM technicians").fetchone()["c"]),
        }

    return {
        "status": "ok",
        "observed_ticket_account_ids": len(account_stubs),
        "observed_ticket_user_ids": len(user_stubs),
        "observed_ticket_technician_ids": len(technician_stubs),
        "account_count_before": before_counts["accounts"],
        "account_count_after": after_counts["accounts"],
        "account_rows_added": max(after_counts["accounts"] - before_counts["accounts"], 0),
        "user_count_before": before_counts["users"],
        "user_count_after": after_counts["users"],
        "user_rows_added": max(after_counts["users"] - before_counts["users"], 0),
        "technician_count_before": before_counts["technicians"],
        "technician_count_after": after_counts["technicians"],
        "technician_rows_added": max(after_counts["technicians"] - before_counts["technicians"], 0),
    }


def backfill_ticket_technician_stubs(db_path: Path, synced_at: str | None = None) -> dict[str, int | str]:
    result = backfill_ticket_entity_stubs(db_path, synced_at=synced_at)
    return {
        "status": result["status"],
        "observed_ticket_technician_ids": result["observed_ticket_technician_ids"],
        "technician_count_before": result["technician_count_before"],
        "technician_count_after": result["technician_count_after"],
        "technician_rows_added": result["technician_rows_added"],
    }


def upsert_ticket_details(db_path: Path, ticket_details: list[dict[str, Any]], synced_at: str | None = None) -> int:
    synced_at = synced_at or now_iso()
    with connect(db_path) as conn:
        for detail in ticket_details:
            ticket_id = str(detail["id"])
            attachments = detail.get("attachments") if isinstance(detail.get("attachments"), list) else []
            ticketlogs = detail.get("ticketlogs") if isinstance(detail.get("ticketlogs"), list) else []
            timelogs = detail.get("timelogs") if isinstance(detail.get("timelogs"), list) else []
            conn.execute(
                """
                INSERT INTO ticket_details(
                    ticket_id, workpad, note, initial_response, sla_response_date, sla_complete_date,
                    waiting_date, next_step_date, ticketlogs_count, timelogs_count, attachments_count,
                    raw_json, synced_at
                ) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ON CONFLICT(ticket_id) DO UPDATE SET
                    workpad = excluded.workpad,
                    note = excluded.note,
                    initial_response = excluded.initial_response,
                    sla_response_date = excluded.sla_response_date,
                    sla_complete_date = excluded.sla_complete_date,
                    waiting_date = excluded.waiting_date,
                    next_step_date = excluded.next_step_date,
                    ticketlogs_count = excluded.ticketlogs_count,
                    timelogs_count = excluded.timelogs_count,
                    attachments_count = excluded.attachments_count,
                    raw_json = excluded.raw_json,
                    synced_at = excluded.synced_at
                """,
                (
                    ticket_id,
                    detail.get("workpad"),
                    detail.get("note"),
                    str(detail.get("initial_response")) if detail.get("initial_response") is not None else None,
                    detail.get("sla_response_date"),
                    detail.get("sla_complete_date"),
                    detail.get("waiting_date"),
                    detail.get("next_step_date"),
                    len(ticketlogs),
                    len(timelogs),
                    len(attachments),
                    _json(detail),
                    synced_at,
                ),
            )

            conn.execute("DELETE FROM ticket_attachments WHERE ticket_id = ?", (ticket_id,))
            for attachment in attachments:
                conn.execute(
                    """
                    INSERT INTO ticket_attachments(id, ticket_id, name, url, size, recorded_at, raw_json, synced_at)
                    VALUES(?, ?, ?, ?, ?, ?, ?, ?)
                    ON CONFLICT(id) DO UPDATE SET
                        ticket_id = excluded.ticket_id,
                        name = excluded.name,
                        url = excluded.url,
                        size = excluded.size,
                        recorded_at = excluded.recorded_at,
                        raw_json = excluded.raw_json,
                        synced_at = excluded.synced_at
                    """,
                    (
                        str(attachment["id"]),
                        ticket_id,
                        attachment.get("name"),
                        attachment.get("url"),
                        attachment.get("size"),
                        attachment.get("date"),
                        _json(attachment),
                        synced_at,
                    ),
                )

            for log in ticketlogs:
                log_id = str(log["id"])
                user_name = " ".join(part for part in [log.get("user_firstname"), log.get("user_lastname")] if part) or None
                conn.execute(
                    """
                    INSERT INTO ticket_logs(
                        id, ticket_id, log_type, record_date, note, plain_note, user_id, user_email, user_name,
                        is_tech_only, is_waiting, raw_json, synced_at
                    ) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    ON CONFLICT(id) DO UPDATE SET
                        ticket_id = excluded.ticket_id,
                        log_type = excluded.log_type,
                        record_date = excluded.record_date,
                        note = excluded.note,
                        plain_note = excluded.plain_note,
                        user_id = excluded.user_id,
                        user_email = excluded.user_email,
                        user_name = excluded.user_name,
                        is_tech_only = excluded.is_tech_only,
                        is_waiting = excluded.is_waiting,
                        raw_json = excluded.raw_json,
                        synced_at = excluded.synced_at
                    """,
                    (
                        log_id,
                        ticket_id,
                        log.get("log_type"),
                        log.get("record_date"),
                        log.get("note"),
                        log.get("plain_note"),
                        str(log.get("user_id")) if log.get("user_id") is not None else None,
                        log.get("user_email"),
                        user_name,
                        1 if log.get("is_tech_only") else 0,
                        1 if log.get("is_waiting") else 0,
                        _json(log),
                        synced_at,
                    ),
                )

            for timelog in timelogs:
                if timelog.get("id") is None:
                    continue
                conn.execute(
                    """
                    INSERT INTO ticket_time_logs(id, ticket_id, record_date, note, raw_json, synced_at)
                    VALUES(?, ?, ?, ?, ?, ?)
                    ON CONFLICT(id) DO UPDATE SET
                        ticket_id = excluded.ticket_id,
                        record_date = excluded.record_date,
                        note = excluded.note,
                        raw_json = excluded.raw_json,
                        synced_at = excluded.synced_at
                    """,
                    (
                        str(timelog["id"]),
                        ticket_id,
                        timelog.get("record_date"),
                        timelog.get("note"),
                        _json(timelog),
                        synced_at,
                    ),
                )
        conn.commit()
    return len(ticket_details)


def replace_ticket_documents(db_path: Path, docs: list[dict[str, Any]], synced_at: str | None = None) -> int:
    synced_at = synced_at or now_iso()
    with connect(db_path) as conn:
        if docs:
            ticket_ids = sorted({str(doc["ticket_id"]) for doc in docs})
            placeholders = ",".join("?" for _ in ticket_ids)
            conn.execute(f"DELETE FROM ticket_documents WHERE ticket_id IN ({placeholders})", ticket_ids)
        for doc in docs:
            conn.execute(
                """
                INSERT INTO ticket_documents(doc_id, ticket_id, status, account, user_name, technician, updated_at, text, raw_json, content_hash, synced_at)
                VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    doc["doc_id"],
                    str(doc["ticket_id"]),
                    doc.get("status"),
                    doc.get("account"),
                    doc.get("user_name"),
                    doc.get("technician"),
                    doc.get("updated_at"),
                    doc["text"],
                    _json(doc),
                    doc.get("content_hash"),
                    synced_at,
                ),
            )
        conn.commit()
    return len(docs)


def replace_ticket_document_chunks(db_path: Path, chunks: list[dict[str, Any]], synced_at: str | None = None) -> int:
    synced_at = synced_at or now_iso()
    with connect(db_path) as conn:
        if chunks:
            ticket_ids = sorted({str(chunk["ticket_id"]) for chunk in chunks})
            placeholders = ",".join("?" for _ in ticket_ids)
            conn.execute(f"DELETE FROM ticket_document_chunks WHERE ticket_id IN ({placeholders})", ticket_ids)
        for chunk in chunks:
            conn.execute(
                """
                INSERT INTO ticket_document_chunks(chunk_id, doc_id, ticket_id, chunk_index, text, content_hash, synced_at)
                VALUES(?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    chunk["chunk_id"],
                    chunk["doc_id"],
                    str(chunk["ticket_id"]),
                    int(chunk["chunk_index"]),
                    chunk["text"],
                    chunk.get("content_hash"),
                    synced_at,
                ),
            )
        conn.commit()
    return len(chunks)


def record_api_request_event(
    db_path: Path,
    *,
    method: str,
    path: str,
    status_code: int | None,
    outcome: str,
    attempt_kind: str | None = None,
    extra: dict[str, Any] | None = None,
) -> None:
    initialize_db(db_path)
    with connect(db_path) as conn:
        conn.execute(
            """
            INSERT INTO api_request_events(recorded_at, method, path, status_code, outcome, attempt_kind, raw_json)
            VALUES(?, ?, ?, ?, ?, ?, ?)
            """,
            (
                now_iso(),
                method,
                path,
                status_code,
                outcome,
                attempt_kind,
                _json(extra or {}),
            ),
        )
        conn.commit()


def prune_api_request_events(db_path: Path, retention_days: int) -> int:
    initialize_db(db_path)
    with connect(db_path) as conn:
        cursor = conn.execute(
            "DELETE FROM api_request_events WHERE julianday(recorded_at) < julianday('now', ?)",
            (f'-{retention_days} days',),
        )
        conn.commit()
        return int(cursor.rowcount)
