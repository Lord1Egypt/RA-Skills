import json
from pathlib import Path

from sherpamind.db import initialize_db, upsert_accounts, upsert_ticket_details, upsert_tickets, upsert_technicians, upsert_users
from sherpamind.documents import (
    DOCUMENT_MATERIALIZATION_VERSION,
    _chunk_text,
    build_ticket_document_chunks,
    build_ticket_documents,
    ensure_current_ticket_materialization,
    export_ticket_chunks,
    export_ticket_documents,
    materialize_ticket_documents,
)


def seed_fixture(db: Path) -> None:
    initialize_db(db)
    upsert_accounts(db, [{"id": 1, "name": "Acme"}], synced_at="2026-03-19T01:00:00Z")
    upsert_users(db, [{"id": 11, "account_id": 1, "FullName": "Alice User", "email": "alice@example.com"}], synced_at="2026-03-19T01:00:00Z")
    upsert_technicians(db, [{"id": 21, "FullName": "Tech One", "email": "tech@example.com"}], synced_at="2026-03-19T01:00:00Z")
    upsert_tickets(
        db,
        [{
            "id": 101,
            "account_id": 1,
            "user_id": 11,
            "tech_id": 21,
            "subject": "Issue A",
            "status": "Open",
            "priority_name": "High",
            "class_name": "Hardware / Printer",
            "number": "T-101",
            "key": "abc-101",
            "created_time": "2026-03-18T01:00:00Z",
            "updated_time": "2026-03-19T03:00:00Z",
            "initial_post": "",
            "account_location_name": "HQ",
            "support_group_name": "Dispatch",
            "location_name": "Front Desk",
            "department_key": "service",
            "user_phone": "520-555-0101",
            "user_created_email": "dispatcher@example.com",
            "user_created_firstname": "Casey",
            "user_created_lastname": "Dispatcher",
            "technician_email": "queue@example.com",
            "tech_type": "dispatcher",
            "project_id": 77,
            "project_name": "Printer Rollout",
            "scheduled_ticket_id": 909,
            "related_tickets_count": 4,
            "estimated_time": 2.5,
            "remaining_hours": 1.25,
            "total_hours": 3.75,
            "total_time_in_minutes": 225,
            "labor_cost": 450,
            "percentage_complete": 60,
            "days_old_in_minutes": 1440,
            "waiting_minutes": 30,
            "is_via_email_parser": 1,
            "is_handle_by_callcentre": 0,
            "confirmed_by_name": "Dispatcher",
            "confirmed_date": "2026-03-19T04:30:00Z",
        }, {
            "id": 102,
            "account_id": 2,
            "user_id": 12,
            "tech_id": 999,
            "account_name": "Raw Account",
            "account_location_name": "Warehouse",
            "user_firstname": "Bob",
            "user_lastname": "Jones",
            "technician_firstname": "Queue",
            "technician_lastname": "Owner",
            "subject": "Issue B",
            "status": "Open",
            "priority_name": "Low",
            "created_time": "2026-03-18T02:00:00Z",
            "updated_time": "2026-03-19T04:00:00Z"
        }],
        synced_at="2026-03-19T01:00:00Z",
    )
    upsert_ticket_details(
        db,
        [{
            "id": 101,
            "plain_initial_post": "Can you help with issue A?\n\nThis ticket was created via the email parser.",
            "next_step": "Call back",
            "workpad": "Internal note",
            "initial_response": True,
            "followup_date": "2026-03-20T10:00:00Z",
            "followup_note": "Waiting on user approval",
            "request_completion_date": "2026-03-21T17:00:00Z",
            "request_completion_note": "Finish after-hours maintenance window",
            "support_group_name": "Managed Services",
            "default_contract_name": "Gold",
            "location_name": "HQ",
            "account_location_name": "HQ Campus",
            "department_key": "managed-services",
            "confirmed_by_name": "Tech Lead",
            "confirmed_date": "2026-03-19T05:00:00Z",
            "confirmed_note": "User confirmed the printer was fixed.",
            "is_via_email_parser": 1,
            "is_handle_by_callcentre": 0,
            "is_waiting_on_response": True,
            "is_resolved": False,
            "is_confirmed": True,
            "ticketlogs": [
                {"id": 503, "log_type": "Closed", "record_date": "2026-03-19T06:30:00Z", "plain_note": "Closed after printer service restored", "user_firstname": "Tech", "user_lastname": "One", "user_email": "tech@example.com", "is_tech_only": True},
                {"id": 502, "log_type": "Waiting on Response", "record_date": "2026-03-19T06:00:00Z", "plain_note": "Waiting on user approval", "user_firstname": "Alice", "user_lastname": "User", "user_email": "alice@example.com"},
                {"id": 501, "log_type": "Response", "record_date": "2026-03-19T05:30:00Z", "plain_note": "printer broken", "user_firstname": "Casey", "user_lastname": "Dispatcher", "user_email": "dispatcher@example.com"},
                {"id": 500, "log_type": "Initial Post", "record_date": "2026-03-18T01:00:00Z", "plain_note": "printer broken", "user_firstname": "Alice", "user_lastname": "User", "user_email": "alice@example.com"}
            ],
            "timelogs": [],
            "attachments": [
                {"id": "a1", "name": "shot.png", "url": "https://example/shot.png", "size": 1234, "date": "2026-03-18T01:00:00Z"},
                {"id": "a2", "name": "logs.zip", "url": "https://example/logs.zip", "size": 2048, "date": "2026-03-18T01:05:00Z"},
                {"id": "a3", "name": "agent.log", "url": "https://example/agent.log", "size": 512, "date": "2026-03-18T01:10:00Z"}
            ],
        }, {
            "id": 102,
            "followup_note": "Waiting for branch manager approval",
            "ticketlogs": [
                {"id": 601, "log_type": "Waiting on Response", "record_date": "2026-03-19T07:00:00Z", "plain_note": "Waiting for branch manager approval", "user_firstname": "Bob", "user_lastname": "Jones", "user_email": "bob@example.com"}
            ],
            "timelogs": [],
            "attachments": [],
        }],
        synced_at="2026-03-19T01:00:00Z",
    )


def test_chunk_text_splits_large_single_paragraphs_for_vector_readiness() -> None:
    sentence = "This is a long sentence about printer troubleshooting and follow-up actions."
    text = " ".join([sentence] * 80)

    chunks = _chunk_text(text, target_chars=500)

    assert len(chunks) > 1
    assert max(len(chunk) for chunk in chunks) <= 500
    assert all(chunk.strip() for chunk in chunks)
    assert "printer troubleshooting" in chunks[0]
    assert "follow-up actions" in chunks[-1]



def test_chunk_text_rebalances_tiny_tail_chunks_for_vector_readiness() -> None:
    segments = [
        "Account: Acme",
        "Status: Closed",
        "Issue summary: " + ("Alpha beta gamma delta " * 60).strip(),
        "Recent log summary: " + ("Follow-up investigation note. " * 26).strip(),
        "Resolution log note: Rebooted the print server and confirmed queue health.",
        "Resolution/activity highlight: Service restored after queue cleanup.",
        "Resolution category: Completed",
    ]
    text = "\n".join(segments)

    chunks = _chunk_text(text, target_chars=360, min_chunk_chars=120)

    assert len(chunks) >= 3
    assert max(len(chunk) for chunk in chunks) <= 360
    assert len(chunks[-1]) >= 120
    assert "Resolution log note:" in chunks[-1]
    assert chunks[-1].endswith("Resolution category: Completed")



def test_build_materialize_and_export_ticket_documents(tmp_path: Path) -> None:
    db = tmp_path / "sherpamind.sqlite3"
    seed_fixture(db)
    docs = build_ticket_documents(db)
    docs_by_id = {doc["ticket_id"]: doc for doc in docs}

    primary = docs_by_id["101"]
    assert primary["doc_id"] == "ticket:101"
    assert "Issue A" in primary["text"]
    assert "Issue summary:" in primary["text"]
    assert "This ticket was created via the email parser." not in primary["text"]
    assert "Internal note" in primary["text"]
    assert "printer broken" in primary["text"]
    assert "Support group: Managed Services" in primary["text"]
    assert "Contract: Gold" in primary["text"]
    assert "Ticket number: T-101" in primary["text"]
    assert "Ticket key: abc-101" in primary["text"]
    assert "Public log count: 3" in primary["text"]
    assert "Internal log count: 1" in primary["text"]
    assert "Distinct public participant count: 2" in primary["text"]
    assert "Distinct internal participant count: 1" in primary["text"]
    assert "Distinct participant count: 3" in primary["text"]
    assert "Waiting log count: 1" in primary["text"]
    assert "Response log count: 2" in primary["text"]
    assert "Resolution log count: 1" in primary["text"]
    assert "Latest log date: 2026-03-19T06:30:00Z" in primary["text"]
    assert "Latest public log date: 2026-03-19T06:00:00Z" in primary["text"]
    assert "Latest internal log date: 2026-03-19T06:30:00Z" in primary["text"]
    assert "Latest public participant: Alice User" in primary["text"]
    assert "Latest internal participant: Tech One" in primary["text"]
    assert "Recent public participants: Alice User, Casey Dispatcher" in primary["text"]
    assert "Recent internal participants: Tech One" in primary["text"]
    assert "Mixed visibility activity: True" in primary["text"]
    assert "Latest waiting log date: 2026-03-19T06:00:00Z" in primary["text"]
    assert "Latest resolution log date: 2026-03-19T06:30:00Z" in primary["text"]
    assert "User email: alice@example.com" in primary["text"]
    assert "User email domain: example.com" in primary["text"]
    assert "Technician email: queue@example.com" in primary["text"]
    assert "Technician email domain: example.com" in primary["text"]
    assert "Created by: Casey Dispatcher" in primary["text"]
    assert "Created by email: dispatcher@example.com" in primary["text"]
    assert "Created by email domain: example.com" in primary["text"]
    assert "Participant email domains: example.com" in primary["text"]
    assert "Public participant email domains: example.com" in primary["text"]
    assert "Internal participant email domains: example.com" in primary["text"]
    assert "User phone: 520-555-0101" in primary["text"]
    assert "Location: HQ" in primary["text"]
    assert "Account location: HQ Campus" in primary["text"]
    assert "Department: Managed Services" in primary["text"]
    assert "Department key: managed-services" in primary["text"]
    assert "Via email parser: True" in primary["text"]
    assert "Handled by call centre: False" in primary["text"]
    assert "Confirmed date: 2026-03-19T05:00:00Z" in primary["text"]
    assert "Confirmed note: User confirmed the printer was fixed." in primary["text"]
    assert "Waiting minutes: 30" in primary["text"]
    assert "Ticket age minutes: 1440" in primary["text"]
    assert "Technician type: dispatcher" in primary["text"]
    assert "Project: Printer Rollout" in primary["text"]
    assert "Project ID: 77" in primary["text"]
    assert "Scheduled ticket ID: 909" in primary["text"]
    assert "Related ticket count: 4" in primary["text"]
    assert "Estimated time: 2.5" in primary["text"]
    assert "Remaining hours: 1.25" in primary["text"]
    assert "Total hours: 3.75" in primary["text"]
    assert "Total time minutes: 225" in primary["text"]
    assert "Labor cost: 450" in primary["text"]
    assert "Percent complete: 60" in primary["text"]
    assert "Follow-up note: Waiting on user approval" in primary["text"]
    assert "Latest response date: 2026-03-19T05:30:00Z" in primary["text"]
    assert "Latest response note: printer broken" in primary["text"]
    assert "Resolution log date: 2026-03-19T06:30:00Z" in primary["text"]
    assert "Resolution log note: Closed after printer service restored" in primary["text"]
    assert "Requested completion note: Finish after-hours maintenance window" in primary["text"]
    assert "Attachments (metadata only)" in primary["text"]
    assert "Attachment kinds: archive, image, log" in primary["text"]
    assert "Attachment extensions: log, png, zip" in primary["text"]
    assert "Attachment total size bytes: 3794" in primary["text"]
    assert primary["metadata"]["attachments"][0]["name"] == "shot.png"
    assert primary["metadata"]["attachment_names"] == ["shot.png", "logs.zip", "agent.log"]
    assert primary["metadata"]["attachment_extensions"] == ["log", "png", "zip"]
    assert primary["metadata"]["attachment_extensions_csv"] == "log, png, zip"
    assert primary["metadata"]["attachment_kinds"] == ["archive", "image", "log"]
    assert primary["metadata"]["attachment_kinds_csv"] == "archive, image, log"
    assert primary["metadata"]["attachment_kind_primary"] == "image"
    assert primary["metadata"]["attachment_total_size_bytes"] == 3794
    assert primary["metadata"]["attachment_archive_count"] == 1
    assert primary["metadata"]["attachment_image_count"] == 1
    assert primary["metadata"]["attachment_log_count"] == 1
    assert primary["metadata"]["has_attachments"] is True
    assert primary["metadata"]["category"] == "Hardware / Printer"
    assert primary["metadata"]["public_log_count"] == 3
    assert primary["metadata"]["internal_log_count"] == 1
    assert primary["metadata"]["public_actor_count"] == 2
    assert primary["metadata"]["internal_actor_count"] == 1
    assert primary["metadata"]["total_actor_count"] == 3
    assert primary["metadata"]["waiting_log_count"] == 1
    assert primary["metadata"]["response_log_count"] == 2
    assert primary["metadata"]["resolution_log_count"] == 1
    assert primary["metadata"]["latest_log_date"] == "2026-03-19T06:30:00Z"
    assert primary["metadata"]["latest_public_log_date"] == "2026-03-19T06:00:00Z"
    assert primary["metadata"]["latest_internal_log_date"] == "2026-03-19T06:30:00Z"
    assert primary["metadata"]["latest_public_actor_label"] == "Alice User"
    assert primary["metadata"]["latest_internal_actor_label"] == "Tech One"
    assert primary["metadata"]["recent_public_actor_labels"] == ["Alice User", "Casey Dispatcher"]
    assert primary["metadata"]["recent_public_actor_labels_csv"] == "Alice User, Casey Dispatcher"
    assert primary["metadata"]["recent_internal_actor_labels"] == ["Tech One"]
    assert primary["metadata"]["recent_internal_actor_labels_csv"] == "Tech One"
    assert primary["metadata"]["latest_waiting_log_date"] == "2026-03-19T06:00:00Z"
    assert primary["metadata"]["latest_resolution_log_date"] == "2026-03-19T06:30:00Z"
    assert primary["metadata"]["cleaned_subject"] == "Issue A"
    assert primary["metadata"]["cleaned_initial_post"] == "Can you help with issue A?"
    assert primary["metadata"]["cleaned_workpad"] == "Internal note"
    assert primary["metadata"]["cleaned_followup_note"] == "Waiting on user approval"
    assert primary["metadata"]["cleaned_explicit_followup_note"] == "Waiting on user approval"
    assert primary["metadata"]["cleaned_waiting_log_note"] == "Waiting on user approval"
    assert primary["metadata"]["followup_note_source"] == "explicit_followup_note"
    assert primary["metadata"]["cleaned_request_completion_note"] == "Finish after-hours maintenance window"
    assert primary["metadata"]["cleaned_next_step"] == "Call back"
    assert primary["metadata"]["cleaned_action_cue"] == "Call back"
    assert primary["metadata"]["action_cue_source"] == "next_step"
    assert primary["metadata"]["cleaned_latest_response_note"] == "printer broken"
    assert primary["metadata"]["latest_response_date"] == "2026-03-19T05:30:00Z"
    assert primary["metadata"]["cleaned_resolution_log_note"] == "Closed after printer service restored"
    assert primary["metadata"]["resolution_log_date"] == "2026-03-19T06:30:00Z"
    assert primary["metadata"]["followup_date"] == "2026-03-20T10:00:00Z"
    assert primary["metadata"]["request_completion_date"] == "2026-03-21T17:00:00Z"
    assert primary["metadata"]["support_group_name"] == "Managed Services"
    assert primary["metadata"]["default_contract_name"] == "Gold"
    assert primary["metadata"]["location_name"] == "HQ"
    assert primary["metadata"]["account_location_name"] == "HQ Campus"
    assert primary["metadata"]["department_key"] == "managed-services"
    assert primary["metadata"]["department_label"] == "Managed Services"
    assert primary["metadata"]["department_label_source"] == "support_group_name"
    assert primary["metadata"]["ticket_number"] == "T-101"
    assert primary["metadata"]["ticket_key"] == "abc-101"
    assert primary["metadata"]["technician_email"] == "queue@example.com"
    assert primary["metadata"]["user_phone"] == "520-555-0101"
    assert primary["metadata"]["user_created_name"] == "Casey Dispatcher"
    assert primary["metadata"]["user_created_email"] == "dispatcher@example.com"
    assert primary["metadata"]["technician_type"] == "dispatcher"
    assert primary["metadata"]["project_id"] == 77
    assert primary["metadata"]["project_name"] == "Printer Rollout"
    assert primary["metadata"]["scheduled_ticket_id"] == 909
    assert primary["metadata"]["related_tickets_count"] == 4
    assert primary["metadata"]["estimated_time"] == 2.5
    assert primary["metadata"]["remaining_hours"] == 1.25
    assert primary["metadata"]["total_hours"] == 3.75
    assert primary["metadata"]["total_time_in_minutes"] == 225
    assert primary["metadata"]["labor_cost"] == 450
    assert primary["metadata"]["percentage_complete"] == 60
    assert primary["metadata"]["has_project_context"] is True
    assert primary["metadata"]["has_scheduled_parent"] is True
    assert primary["metadata"]["has_related_tickets"] is True
    assert primary["metadata"]["has_effort_tracking"] is True
    assert primary["metadata"]["has_public_logs"] is True
    assert primary["metadata"]["has_internal_logs"] is True
    assert primary["metadata"]["has_multi_public_participants"] is True
    assert primary["metadata"]["has_multi_internal_participants"] is False
    assert primary["metadata"]["has_named_public_participants"] is True
    assert primary["metadata"]["has_named_internal_participants"] is True
    assert primary["metadata"]["has_mixed_visibility_activity"] is True
    assert primary["metadata"]["has_waiting_logs"] is True
    assert primary["metadata"]["has_resolution_logs"] is True
    assert primary["metadata"]["days_old_in_minutes"] == 1440
    assert primary["metadata"]["waiting_minutes"] == 30
    assert primary["metadata"]["confirmed_by_name"] == "Tech Lead"
    assert primary["metadata"]["confirmed_date"] == "2026-03-19T05:00:00Z"
    assert primary["metadata"]["cleaned_confirmed_note"] == "User confirmed the printer was fixed."
    assert primary["metadata"]["is_via_email_parser"] is True
    assert primary["metadata"]["is_handle_by_callcentre"] is False
    assert primary["metadata"]["is_waiting_on_response"] is True
    assert primary["metadata"]["is_resolved"] is False
    assert primary["metadata"]["is_confirmed"] is True
    assert primary["metadata"]["has_next_step"] is True
    assert primary["metadata"]["recent_log_types"] == ["Closed", "Waiting on Response", "Response", "Initial Post"]
    assert primary["metadata"]["recent_log_types_csv"] == "Closed, Waiting on Response, Response, Initial Post"
    assert primary["metadata"]["initial_response_present"] is True
    assert primary["metadata"]["user_email"] == "alice@example.com"
    assert primary["metadata"]["user_email_domain"] == "example.com"
    assert primary["metadata"]["user_created_email_domain"] == "example.com"
    assert primary["metadata"]["technician_email_domain"] == "example.com"
    assert primary["metadata"]["participant_email_domains"] == ["example.com"]
    assert primary["metadata"]["participant_email_domains_csv"] == "example.com"
    assert primary["metadata"]["participant_email_domain_count"] == 1
    assert primary["metadata"]["public_participant_email_domains"] == ["example.com"]
    assert primary["metadata"]["public_participant_email_domains_csv"] == "example.com"
    assert primary["metadata"]["public_participant_email_domain_count"] == 1
    assert primary["metadata"]["internal_participant_email_domains"] == ["example.com"]
    assert primary["metadata"]["internal_participant_email_domains_csv"] == "example.com"
    assert primary["metadata"]["internal_participant_email_domain_count"] == 1
    assert primary["metadata"]["detail_available"] is True
    assert primary["metadata"]["account_label_source"] == "joined"
    assert primary["metadata"]["user_label_source"] == "joined"
    assert primary["metadata"]["technician_label_source"] == "joined"
    assert primary["materialization_version"] == DOCUMENT_MATERIALIZATION_VERSION
    assert primary["metadata"]["materialization_version"] == DOCUMENT_MATERIALIZATION_VERSION

    fallback = docs_by_id["102"]
    assert fallback["account"] == "Raw Account"
    assert fallback["user_name"] == "Bob Jones"
    assert fallback["technician"] == "Queue Owner"
    assert "Account: Raw Account" in fallback["text"]
    assert "User: Bob Jones" in fallback["text"]
    assert "Technician: Queue Owner" in fallback["text"]
    assert "Account location: Warehouse" in fallback["text"]
    assert fallback["metadata"]["account_location_name"] == "Warehouse"
    assert fallback["metadata"]["cleaned_followup_note"] == "Waiting for branch manager approval"
    assert fallback["metadata"]["cleaned_explicit_followup_note"] == "Waiting for branch manager approval"
    assert fallback["metadata"]["cleaned_waiting_log_note"] == "Waiting for branch manager approval"
    assert fallback["metadata"]["followup_note_source"] == "explicit_followup_note"
    assert fallback["metadata"]["public_actor_count"] == 1
    assert fallback["metadata"]["internal_actor_count"] == 0
    assert fallback["metadata"]["total_actor_count"] == 1
    assert fallback["metadata"]["latest_public_actor_label"] == "Bob Jones"
    assert fallback["metadata"]["recent_public_actor_labels"] == ["Bob Jones"]
    assert fallback["metadata"]["participant_email_domains"] == []
    assert fallback["metadata"]["participant_email_domains_csv"] is None
    assert fallback["metadata"]["public_participant_email_domains"] == []
    assert fallback["metadata"]["internal_participant_email_domains"] == []
    assert fallback["metadata"]["has_named_public_participants"] is True
    assert fallback["metadata"]["cleaned_action_cue"] == "Waiting for branch manager approval"
    assert fallback["metadata"]["action_cue_source"] == "followup_note"
    assert fallback["metadata"]["has_next_step"] is True
    assert fallback["metadata"]["account_label_source"] == "joined"
    assert fallback["metadata"]["user_label_source"] == "joined"
    assert fallback["metadata"]["technician_label_source"] == "joined"

    chunks = build_ticket_document_chunks(docs)
    chunks_by_ticket = {chunk["ticket_id"]: chunk for chunk in chunks}
    assert chunks_by_ticket["101"]["chunk_id"].startswith("ticket:101:chunk:")
    assert chunks_by_ticket["101"]["account"] == "Acme"

    materialized = materialize_ticket_documents(db)
    assert materialized["status"] == "ok"
    assert materialized["chunk_count"] >= 1
    assert materialized["materialization_version"] == DOCUMENT_MATERIALIZATION_VERSION

    output = tmp_path / "ticket-docs.jsonl"
    result = export_ticket_documents(db, output)
    assert result["status"] == "ok"
    assert result["document_count"] == 2

    chunk_output = tmp_path / "ticket-chunks.jsonl"
    chunk_result = export_ticket_chunks(db, chunk_output)
    assert chunk_result["status"] == "ok"
    assert chunk_result["chunk_count"] >= 1

    rematerialization_check = ensure_current_ticket_materialization(db)
    assert rematerialization_check["status"] == "ok"
    assert rematerialization_check["refreshed"] is False
    assert rematerialization_check["materialization"]["current_version"] == DOCUMENT_MATERIALIZATION_VERSION

    lines = output.read_text().splitlines()
    assert len(lines) == 2
    exported_ids = {json.loads(line)["doc_id"] for line in lines}
    assert exported_ids == {"ticket:101", "ticket:102"}
