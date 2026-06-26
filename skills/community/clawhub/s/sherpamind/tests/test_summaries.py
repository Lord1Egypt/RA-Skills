from pathlib import Path

from sherpamind.db import initialize_db, upsert_accounts, upsert_ticket_details, upsert_tickets, upsert_technicians, upsert_users
from sherpamind.documents import materialize_ticket_documents
from sherpamind.summaries import get_account_summary, get_technician_summary, get_ticket_summary, list_ticket_artifact_summaries


def seed_fixture(db: Path) -> None:
    initialize_db(db)
    upsert_accounts(db, [{"id": 1, "name": "Acme"}], synced_at="2026-03-19T01:00:00Z")
    upsert_users(db, [{"id": 11, "account_id": 1, "FullName": "Alice User"}], synced_at="2026-03-19T01:00:00Z")
    upsert_technicians(db, [{"id": 21, "FullName": "Tech One", "email": "tech@example.com"}], synced_at="2026-03-19T01:00:00Z")
    upsert_tickets(db, [
        {"id": 101, "account_id": 1, "user_id": 11, "tech_id": 21, "subject": "Issue A", "status": "Open", "updated_time": "2026-03-19T03:00:00Z", "created_time": "2026-03-18T01:00:00Z"},
        {"id": 102, "account_id": 1, "user_id": 11, "tech_id": 21, "subject": "Issue B", "status": "Closed", "updated_time": "2026-03-19T02:00:00Z", "created_time": "2026-03-18T01:00:00Z"},
    ], synced_at="2026-03-19T01:00:00Z")
    upsert_ticket_details(db, [{"id": 101, "ticketlogs": [{"id": 5001, "log_type": "Response", "plain_note": "done", "record_date": "2026-03-18T01:00:00Z"}], "timelogs": [], "attachments": []}], synced_at="2026-03-19T01:00:00Z")
    materialize_ticket_documents(db)


def test_account_summary(tmp_path: Path) -> None:
    db = tmp_path / "sherpamind.sqlite3"
    seed_fixture(db)
    summary = get_account_summary(db, "Acme")
    assert summary["status"] == "ok"
    assert summary["stats"]["total_tickets"] == 2
    assert summary["retrieval_health"]["document_tickets"] == 2
    assert summary["retrieval_health"]["detail_tickets"] == 1
    assert summary["retrieval_health"]["metadata_coverage"]["cleaned_subject"]["tickets"] == 2
    assert len(summary["open_tickets"]) == 1


def test_technician_summary(tmp_path: Path) -> None:
    db = tmp_path / "sherpamind.sqlite3"
    seed_fixture(db)
    summary = get_technician_summary(db, "Tech")
    assert summary["status"] == "ok"
    assert summary["stats"]["total_tickets"] == 2
    assert summary["retrieval_health"]["document_tickets"] == 2
    assert summary["retrieval_health"]["detail_tickets"] == 1
    assert summary["retrieval_health"]["lag_buckets"]["current_or_ahead"] == 2
    assert len(summary["open_tickets"]) == 1


def test_ticket_summary_and_artifact_listing(tmp_path: Path) -> None:
    db = tmp_path / "sherpamind.sqlite3"
    seed_fixture(db)

    artifacts = list_ticket_artifact_summaries(db)
    assert len(artifacts) == 1
    assert artifacts[0]["ticket_id"] == "101"
    assert artifacts[0]["detail_available"] is True
    assert artifacts[0]["log_count"] == 1
    assert artifacts[0]["document_available"] is True
    assert artifacts[0]["is_current_materialization_version"] is True
    assert artifacts[0]["chunk_count"] >= 1
    assert artifacts[0]["indexed_chunk_count"] == 0
    assert artifacts[0]["vector_ready"] is False

    summary = get_ticket_summary(db, "101")
    assert summary["status"] == "ok"
    assert summary["ticket"]["id"] == "101"
    assert summary["artifact_stats"]["detail_available"] is True
    assert summary["artifact_stats"]["log_count"] == 1
    assert summary["artifact_stats"]["attachment_count"] == 0
    assert summary["retrieval_health"]["is_current_materialization_version"] is True
    assert summary["retrieval_health"]["chunk_count"] >= 1
    assert summary["retrieval_health"]["indexed_chunk_count"] == 0
    assert summary["retrieval_health"]["vector_ready"] is False
    assert summary["chunk_inventory"]
    assert summary["chunk_inventory"][0]["chunk_primary_section"]
    assert len(summary["recent_logs"]) == 1
