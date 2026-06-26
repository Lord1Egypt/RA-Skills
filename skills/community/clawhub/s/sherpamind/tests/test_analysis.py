from pathlib import Path

from sherpamind.analysis import (
    get_api_usage_summary,
    get_dataset_summary,
    get_enrichment_coverage,
    get_insight_snapshot,
    list_open_ticket_ages,
    list_recent_account_activity,
    list_recent_tickets,
    list_technician_recent_load,
    list_ticket_attachment_summary,
    list_ticket_counts_by_account,
    list_ticket_counts_by_priority,
    list_ticket_counts_by_status,
    list_ticket_counts_by_technician,
    list_ticket_log_types,
    search_ticket_document_chunks,
    search_ticket_documents,
)
from sherpamind.db import (
    initialize_db,
    record_api_request_event,
    replace_ticket_document_chunks,
    replace_ticket_documents,
    upsert_accounts,
    upsert_ticket_details,
    upsert_tickets,
    upsert_technicians,
    upsert_users,
)


def seed_fixture(db: Path) -> None:
    initialize_db(db)
    upsert_accounts(db, [{"id": 1, "name": "Acme"}, {"id": 2, "name": "Beta"}], synced_at="2026-03-19T01:00:00Z")
    upsert_users(db, [{"id": 11, "account_id": 1, "FullName": "Alice User"}], synced_at="2026-03-19T01:00:00Z")
    upsert_technicians(db, [{"id": 21, "FullName": "Tech One"}], synced_at="2026-03-19T01:00:00Z")
    upsert_tickets(
        db,
        [
            {
                "id": 101,
                "account_id": 1,
                "user_id": 11,
                "tech_id": 21,
                "subject": "Issue A",
                "status": "Open",
                "priority_name": "High",
                "created_time": "2026-03-18T01:00:00Z",
                "updated_time": "2026-03-19T03:00:00Z",
                "initial_post": "Can you help with issue A?",
            },
            {
                "id": 102,
                "account_id": 1,
                "subject": "Issue B",
                "status": "Closed",
                "priority_name": "Low",
                "created_time": "2026-03-18T01:00:00Z",
                "updated_time": "2026-03-19T02:00:00Z",
            },
            {
                "id": 103,
                "account_id": 2,
                "subject": "Issue C",
                "status": "Open",
                "priority_name": "High",
                "created_time": "2026-03-18T01:00:00Z",
                "updated_time": "2026-03-19T01:00:00Z",
            },
        ],
        synced_at="2026-03-19T01:00:00Z",
    )
    upsert_ticket_details(
        db,
        [{
            "id": 101,
            "ticketlogs": [{"id": 5001, "log_type": "Initial Post", "plain_note": "printer broken", "record_date": "2026-03-18T01:00:00Z"}],
            "timelogs": [],
            "attachments": [{"id": "a1", "name": "shot.png", "url": "https://example/shot.png", "size": 1234, "date": "2026-03-18T01:00:00Z"}],
        }],
        synced_at="2026-03-19T01:00:00Z",
    )
    replace_ticket_documents(
        db,
        [{
            "doc_id": "ticket:101",
            "ticket_id": 101,
            "status": "Open",
            "account": "Acme",
            "user_name": "Alice User",
            "technician": "Tech One",
            "updated_at": "2026-03-19T03:00:00Z",
            "text": "Printer issue A for Acme",
            "metadata": {
                "priority": "High",
                "category": "Hardware / Printer",
                "class_name": "Technical Incident",
                "submission_category": "Portal",
                "resolution_category": "In Progress",
                "department_label": "Managed Services",
            },
            "content_hash": "h1",
        }],
        synced_at="2026-03-19T01:00:00Z",
    )
    replace_ticket_document_chunks(
        db,
        [{"chunk_id": "ticket:101:chunk:0", "doc_id": "ticket:101", "ticket_id": 101, "chunk_index": 0, "text": "Printer issue A for Acme", "content_hash": "h1"}],
        synced_at="2026-03-19T01:00:00Z",
    )
    record_api_request_event(db, method="GET", path="tickets", status_code=200, outcome="http_response")


def test_analysis_reports(tmp_path: Path) -> None:
    db = tmp_path / "sherpamind.sqlite3"
    seed_fixture(db)
    by_account = list_ticket_counts_by_account(db)
    by_status = list_ticket_counts_by_status(db)
    by_priority = list_ticket_counts_by_priority(db)
    by_technician = list_ticket_counts_by_technician(db)
    by_log_type = list_ticket_log_types(db)
    by_attachment = list_ticket_attachment_summary(db)
    recent = list_recent_tickets(db, limit=2)
    open_ages = list_open_ticket_ages(db, limit=2)
    recent_accounts = list_recent_account_activity(db, days=30, limit=5)
    recent_techs = list_technician_recent_load(db, days=30, limit=5)
    usage = get_api_usage_summary(db)
    coverage = get_enrichment_coverage(db)
    summary = get_dataset_summary(db)
    snapshot = get_insight_snapshot(db)
    search = search_ticket_documents(
        db,
        'printer',
        limit=5,
        account='Acme',
        status='Open',
        technician='Tech',
        priority='High',
        category='Printer',
        class_name='Incident',
        submission_category='Port',
        resolution_category='Progress',
        department='Managed',
    )
    search_chunks = search_ticket_document_chunks(
        db,
        'printer',
        limit=5,
        account='Acme',
        status='Open',
        technician='Tech',
        priority='High',
        category='Printer',
        class_name='Incident',
        submission_category='Port',
        resolution_category='Progress',
        department='Managed',
    )

    assert by_account[0]["account"] == "Acme"
    assert by_account[0]["ticket_count"] == 2
    assert {row["status"]: row["ticket_count"] for row in by_status}["Open"] == 2
    assert {row["priority"]: row["ticket_count"] for row in by_priority}["High"] == 2
    assert by_technician[0]["ticket_count"] >= 1
    assert by_log_type[0]["log_type"] == "Initial Post"
    assert by_attachment[0]["attachment_count"] == 1
    assert recent[0]["subject"] == "Issue A"
    assert open_ages[0]["status"] == "Open"
    assert recent_accounts[0]["ticket_count"] >= 1
    assert recent_techs[0]["ticket_count"] >= 1
    assert usage["requests_last_hour"] == 1
    assert coverage["ticket_details_covered"] == 1
    assert coverage["open_detail_coverage"] == 1
    assert coverage["detail_gap_pressure"]["accounts"]["summary"]["min_tickets"] == 10
    assert coverage["detail_gap_pressure"]["categories"]["summary"]["min_tickets"] == 10
    assert coverage["detail_gap_pressure"]["technicians"]["summary"]["min_tickets"] == 3
    assert coverage["detail_gap_pressure"]["accounts"]["rows"] == []
    assert coverage["enrichment"]["detail_gap_pressure"]["technicians"]["rows"] == []
    assert coverage["retrieval"]["ticket_documents"] == 1
    assert coverage["retrieval"]["ticket_document_chunks"] == 1
    assert coverage["metadata"]["priority_docs"] == 1
    assert coverage["metadata"]["cleaned_subject_docs"] == 0
    assert coverage["metadata"]["next_step_docs"] == 0
    assert coverage["metadata"]["action_cue_docs"] == 0
    assert coverage["metadata"]["attachment_presence_docs"] == 0
    assert summary["counts"]["tickets"] == 3
    assert summary["counts"]["ticket_logs"] == 1
    assert summary["counts"]["ticket_attachments"] == 1
    assert summary["counts"]["ticket_document_chunks"] == 1
    assert summary["counts"]["api_request_events"] == 1
    assert snapshot["dataset_summary"]["counts"]["tickets"] == 3
    assert search[0]["doc_id"] == "ticket:101"
    assert search[0]["priority"] == "High"
    assert search[0]["submission_category"] == "Portal"
    assert search[0]["department_label"] == "Managed Services"
    assert search_chunks[0]["chunk_id"] == "ticket:101:chunk:0"
    assert search_chunks[0]["class_name"] == "Technical Incident"
    assert search_chunks[0]["resolution_category"] == "In Progress"


def test_enrichment_coverage_surfaces_detail_gap_pressure(tmp_path: Path) -> None:
    db = tmp_path / "sherpamind.sqlite3"
    initialize_db(db)
    upsert_accounts(db, [{"id": 1, "name": "Acme"}, {"id": 2, "name": "Beta"}], synced_at="2026-03-19T01:00:00Z")
    upsert_technicians(
        db,
        [{"id": 21, "FullName": "Tech One"}, {"id": 22, "FullName": "Tech Two"}],
        synced_at="2026-03-19T01:00:00Z",
    )
    tickets = []
    for offset in range(10):
        tickets.append(
            {
                "id": 200 + offset,
                "account_id": 1,
                "tech_id": 21,
                "subject": f"Acme issue {offset}",
                "status": "Open" if offset < 2 else "Closed",
                "closed_time": "2099-03-18T01:00:00Z" if offset >= 2 else None,
                "priority_name": "High",
                "creation_category_name": "Networking",
                "created_time": "2026-03-18T01:00:00Z",
                "updated_time": f"2026-03-19T0{(offset % 9) + 1}:00:00Z",
            }
        )
    for offset in range(4):
        tickets.append(
            {
                "id": 400 + offset,
                "account_id": 2,
                "tech_id": 22,
                "subject": f"Beta issue {offset}",
                "status": "Closed",
                "closed_time": "2026-02-01T01:00:00Z",
                "priority_name": "Low",
                "creation_category_name": "Printer",
                "created_time": "2026-01-01T01:00:00Z",
                "updated_time": f"2026-02-01T0{offset + 1}:00:00Z",
            }
        )
    upsert_tickets(db, tickets, synced_at="2026-03-19T01:00:00Z")
    upsert_ticket_details(
        db,
        [
            {"id": 200, "ticketlogs": [], "timelogs": [], "attachments": []},
            {"id": 400, "ticketlogs": [], "timelogs": [], "attachments": []},
            {"id": 401, "ticketlogs": [], "timelogs": [], "attachments": []},
        ],
        synced_at="2026-03-19T01:00:00Z",
    )

    coverage = get_enrichment_coverage(db)

    account_rows = coverage["detail_gap_pressure"]["accounts"]["rows"]
    assert account_rows[0]["label"] == "Acme"
    assert account_rows[0]["total_tickets"] == 10
    assert account_rows[0]["detail_tickets"] == 1
    assert account_rows[0]["detail_backlog"] == 9
    assert account_rows[0]["open_without_detail"] == 1
    assert account_rows[0]["warm_closed_without_detail"] == 8
    assert account_rows[0]["detail_ratio"] == 0.1

    category_rows = coverage["detail_gap_pressure"]["categories"]["rows"]
    assert category_rows[0]["label"] == "Networking"
    assert category_rows[0]["detail_backlog"] == 9

    technician_rows = coverage["detail_gap_pressure"]["technicians"]["rows"]
    assert technician_rows[0]["label"] == "Tech One"
    assert technician_rows[0]["detail_ratio"] == 0.1
    assert coverage["detail_gap_pressure"]["technicians"]["summary"]["low_coverage_groups"] >= 1
