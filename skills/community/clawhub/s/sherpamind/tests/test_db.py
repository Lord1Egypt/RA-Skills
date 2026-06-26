from pathlib import Path

from sherpamind.db import (
    backfill_ticket_entity_stubs,
    backfill_ticket_technician_stubs,
    connect,
    finish_ingest_run,
    initialize_db,
    replace_ticket_document_chunks,
    replace_ticket_documents,
    start_ingest_run,
    upsert_accounts,
    upsert_ticket_details,
    upsert_tickets,
    upsert_technicians,
    upsert_users,
)


def test_initialize_db_creates_core_tables(tmp_path: Path) -> None:
    db = tmp_path / "sherpamind.sqlite3"
    initialize_db(db)
    with connect(db) as conn:
        rows = conn.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()
    names = {row['name'] for row in rows}
    assert 'tickets' in names
    assert 'accounts' in names
    assert 'users' in names
    assert 'ticket_comments' in names
    assert 'sync_state' in names
    assert 'ticket_details' in names
    assert 'ticket_logs' in names
    assert 'ticket_attachments' in names
    assert 'ticket_documents' in names
    assert 'ticket_document_chunks' in names
    assert 'api_request_events' in names


def test_upsert_seed_entities_roundtrip(tmp_path: Path) -> None:
    db = tmp_path / "sherpamind.sqlite3"
    initialize_db(db)
    upsert_accounts(db, [{"id": 1, "name": "Acme", "updated": "2026-03-19T00:00:00Z"}], synced_at="2026-03-19T01:00:00Z")
    upsert_users(db, [{"id": 2, "account_id": 1, "FullName": "User One", "email": "u@example.com"}], synced_at="2026-03-19T01:00:00Z")
    upsert_technicians(db, [{"id": 3, "FullName": "Tech One", "email": "t@example.com"}], synced_at="2026-03-19T01:00:00Z")
    upsert_tickets(
        db,
        [{
            "id": 4,
            "account_id": 1,
            "user_id": 2,
            "tech_id": 3,
            "subject": "Printer is haunted",
            "status": "Open",
            "priority_name": "High",
            "creation_category_name": "Hardware",
            "created_time": "2026-03-18T01:00:00Z",
            "updated_time": "2026-03-19T01:00:00Z",
        }],
        synced_at="2026-03-19T01:00:00Z",
    )
    upsert_ticket_details(
        db,
        [{
            "id": 4,
            "workpad": "secret work",
            "ticketlogs": [{"id": 99, "log_type": "Initial Post", "record_date": "2026-03-18T01:00:00Z", "plain_note": "printer broken"}],
            "timelogs": [],
            "attachments": [{"id": "a1", "name": "shot.png", "url": "https://example/shot.png", "size": 1234, "date": "2026-03-18T01:00:00Z"}],
        }],
        synced_at="2026-03-19T01:00:00Z",
    )
    replace_ticket_documents(
        db,
        [{"doc_id": "ticket:4", "ticket_id": 4, "status": "Open", "account": "Acme", "user_name": "User One", "technician": "Tech One", "updated_at": "2026-03-19T01:00:00Z", "text": "hello", "metadata": {}, "content_hash": "h1"}],
        synced_at="2026-03-19T01:00:00Z",
    )
    replace_ticket_document_chunks(
        db,
        [{"chunk_id": "ticket:4:chunk:0", "doc_id": "ticket:4", "ticket_id": 4, "chunk_index": 0, "text": "hello", "content_hash": "h1"}],
        synced_at="2026-03-19T01:00:00Z",
    )
    with connect(db) as conn:
        ticket = conn.execute("SELECT subject, priority, category FROM tickets WHERE id = '4'").fetchone()
        user = conn.execute("SELECT display_name FROM users WHERE id = '2'").fetchone()
        tech = conn.execute("SELECT display_name FROM technicians WHERE id = '3'").fetchone()
        detail = conn.execute("SELECT workpad, ticketlogs_count FROM ticket_details WHERE ticket_id = '4'").fetchone()
        attachment = conn.execute("SELECT name, size FROM ticket_attachments WHERE ticket_id = '4'").fetchone()
        doc = conn.execute("SELECT text FROM ticket_documents WHERE doc_id = 'ticket:4'").fetchone()
        chunk = conn.execute("SELECT text FROM ticket_document_chunks WHERE chunk_id = 'ticket:4:chunk:0'").fetchone()
    assert ticket["subject"] == "Printer is haunted"
    assert ticket["priority"] == "High"
    assert ticket["category"] == "Hardware"
    assert user["display_name"] == "User One"
    assert tech["display_name"] == "Tech One"
    assert detail["workpad"] == "secret work"
    assert detail["ticketlogs_count"] == 1
    assert attachment["name"] == "shot.png"
    assert attachment["size"] == 1234
    assert doc["text"] == "hello"
    assert chunk["text"] == "hello"


def test_upsert_tickets_backfills_entity_stub_rows(tmp_path: Path) -> None:
    db = tmp_path / "sherpamind.sqlite3"
    initialize_db(db)
    upsert_tickets(
        db,
        [{
            "id": 41,
            "account_id": 1,
            "account_name": "Acme Field Ops",
            "user_id": 2,
            "user_firstname": "Pat",
            "user_lastname": "Operator",
            "user_email": "pat@example.com",
            "tech_id": 333,
            "technician_firstname": "Queue",
            "technician_lastname": "Owner",
            "subject": "Printer is haunted",
            "status": "Open",
            "created_time": "2026-03-18T01:00:00Z",
            "updated_time": "2026-03-19T01:00:00Z",
        }],
        synced_at="2026-03-19T01:00:00Z",
    )
    with connect(db) as conn:
        account = conn.execute("SELECT name, raw_json FROM accounts WHERE id = '1'").fetchone()
        user = conn.execute("SELECT account_id, display_name, email, raw_json FROM users WHERE id = '2'").fetchone()
        tech = conn.execute("SELECT display_name, email, raw_json FROM technicians WHERE id = '333'").fetchone()
    assert account["name"] == "Acme Field Ops"
    assert 'ticket_stub' in account["raw_json"]
    assert user["account_id"] == '1'
    assert user["display_name"] == "Pat Operator"
    assert user["email"] == "pat@example.com"
    assert 'ticket_stub' in user["raw_json"]
    assert tech["display_name"] == "Queue Owner"
    assert tech["email"] is None
    assert 'ticket_stub' in tech["raw_json"]


def test_upsert_seed_entities_beat_stub_rows(tmp_path: Path) -> None:
    db = tmp_path / "sherpamind.sqlite3"
    initialize_db(db)
    upsert_tickets(
        db,
        [{
            "id": 41,
            "account_id": 1,
            "account_name": "Acme Field Ops",
            "user_id": 2,
            "user_firstname": "Pat",
            "user_lastname": "Operator",
            "tech_id": 333,
            "technician_firstname": "Queue",
            "technician_lastname": "Owner",
            "status": "Open",
            "created_time": "2026-03-18T01:00:00Z",
            "updated_time": "2026-03-19T01:00:00Z",
        }],
        synced_at="2026-03-19T01:00:00Z",
    )
    upsert_accounts(
        db,
        [{"id": 1, "name": "Acme", "updated": "2026-03-19T02:00:00Z"}],
        synced_at="2026-03-19T02:00:00Z",
    )
    upsert_users(
        db,
        [{"id": 2, "account_id": 1, "FullName": "Pat Operator", "email": "pat@example.com"}],
        synced_at="2026-03-19T02:00:00Z",
    )
    upsert_technicians(
        db,
        [{"id": 333, "FullName": "Queue Owner", "email": "queue@example.com", "type": "tech"}],
        synced_at="2026-03-19T02:00:00Z",
    )
    with connect(db) as conn:
        account = conn.execute("SELECT name, raw_json FROM accounts WHERE id = '1'").fetchone()
        user = conn.execute("SELECT display_name, email, raw_json FROM users WHERE id = '2'").fetchone()
        tech = conn.execute("SELECT display_name, email, raw_json FROM technicians WHERE id = '333'").fetchone()
    assert account["name"] == "Acme"
    assert 'ticket_stub' not in account["raw_json"]
    assert user["display_name"] == "Pat Operator"
    assert user["email"] == "pat@example.com"
    assert 'ticket_stub' not in user["raw_json"]
    assert tech["display_name"] == "Queue Owner"
    assert tech["email"] == "queue@example.com"
    assert 'ticket_stub' not in tech["raw_json"]


def test_backfill_ticket_entity_stubs_repairs_existing_ticket_rows(tmp_path: Path) -> None:
    db = tmp_path / "sherpamind.sqlite3"
    initialize_db(db)
    upsert_tickets(
        db,
        [{
            "id": 41,
            "account_id": 1,
            "account_name": "Acme Field Ops",
            "user_id": 2,
            "user_firstname": "Pat",
            "user_lastname": "Operator",
            "tech_id": 333,
            "technician_firstname": "Queue",
            "technician_lastname": "Owner",
            "status": "Open",
            "created_time": "2026-03-18T01:00:00Z",
            "updated_time": "2026-03-19T01:00:00Z",
        }],
        synced_at="2026-03-19T01:00:00Z",
    )
    with connect(db) as conn:
        conn.execute("DELETE FROM accounts")
        conn.execute("DELETE FROM users")
        conn.execute("DELETE FROM technicians")
        conn.commit()
    result = backfill_ticket_entity_stubs(db, synced_at="2026-03-19T03:00:00Z")
    with connect(db) as conn:
        account = conn.execute("SELECT name FROM accounts WHERE id = '1'").fetchone()
        user = conn.execute("SELECT display_name FROM users WHERE id = '2'").fetchone()
        tech = conn.execute("SELECT display_name FROM technicians WHERE id = '333'").fetchone()
    assert result["account_rows_added"] == 1
    assert result["user_rows_added"] == 1
    assert result["technician_rows_added"] == 1
    assert account["name"] == "Acme Field Ops"
    assert user["display_name"] == "Pat Operator"
    assert tech["display_name"] == "Queue Owner"


def test_backfill_ticket_technician_stubs_reports_technician_slice(tmp_path: Path) -> None:
    db = tmp_path / "sherpamind.sqlite3"
    initialize_db(db)
    upsert_tickets(
        db,
        [{
            "id": 41,
            "tech_id": 333,
            "technician_firstname": "Queue",
            "technician_lastname": "Owner",
            "status": "Open",
            "created_time": "2026-03-18T01:00:00Z",
            "updated_time": "2026-03-19T01:00:00Z",
        }],
        synced_at="2026-03-19T01:00:00Z",
    )
    with connect(db) as conn:
        conn.execute("DELETE FROM technicians")
        conn.commit()
    result = backfill_ticket_technician_stubs(db, synced_at="2026-03-19T03:00:00Z")
    with connect(db) as conn:
        tech = conn.execute("SELECT display_name FROM technicians WHERE id = '333'").fetchone()
    assert result["technician_rows_added"] == 1
    assert tech["display_name"] == "Queue Owner"


def test_ingest_run_roundtrip(tmp_path: Path) -> None:
    db = tmp_path / "sherpamind.sqlite3"
    initialize_db(db)
    run_id = start_ingest_run(db, mode="seed", notes="test")
    finish_ingest_run(db, run_id, status="success", notes="done")
    with connect(db) as conn:
        row = conn.execute("SELECT mode, status, notes, finished_at FROM ingest_runs WHERE id = ?", (run_id,)).fetchone()
    assert row["mode"] == "seed"
    assert row["status"] == "success"
    assert row["notes"] == "done"
    assert row["finished_at"] is not None
