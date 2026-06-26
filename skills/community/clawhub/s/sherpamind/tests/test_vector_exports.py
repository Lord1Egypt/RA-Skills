import json
from pathlib import Path

from sherpamind.db import (
    initialize_db,
    replace_ticket_document_chunks,
    replace_ticket_documents,
    upsert_ticket_details,
    upsert_tickets,
)
from sherpamind.documents import DOCUMENT_MATERIALIZATION_VERSION
from sherpamind.vector_exports import export_embedding_manifest, export_embedding_ready_chunks, get_retrieval_readiness_summary


def seed(db: Path) -> None:
    initialize_db(db)
    upsert_tickets(
        db,
        [
            {
                "id": 101,
                "account_id": 1,
                "user_id": 2,
                "tech_id": 3,
                "subject": "hello",
                "status": "Open",
                "priority_name": "High",
                "creation_category_name": "Hardware",
                "created_time": "2026-03-19T01:00:00Z",
                "updated_time": "2026-03-19T03:00:00Z",
                "closed_time": None,
                "number": "T-101",
                "key": "abc-101",
                "technician_email": "tech@example.com",
                "user_phone": "520-555-0101",
                "account_location_name": "HQ Campus",
                "is_via_email_parser": True,
                "is_handle_by_callcentre": False,
            },
            {
                "id": 102,
                "account_id": 44,
                "user_id": 55,
                "tech_id": 66,
                "subject": "numeric fallback labels",
                "status": "Closed",
                "priority_name": "Low",
                "creation_category_name": "Software",
                "created_time": "2026-03-18T01:00:00Z",
                "updated_time": "2026-03-18T03:00:00Z",
                "closed_time": "2026-03-18T04:00:00Z",
                "number": "T-102",
                "key": "abc-102",
            },
        ],
        synced_at="2026-03-19T01:00:00Z",
    )
    upsert_ticket_details(
        db,
        [{
            "id": 101,
            "default_contract_name": "Gold",
            "location_name": "HQ",
            "department_key": "managed-services",
            "user_created_email": "dispatcher@example.com",
            "tech_type": "dispatcher",
            "days_old_in_minutes": 1440,
            "waiting_minutes": 30,
            "confirmed_by_name": "Tech Lead",
            "confirmed_date": "2026-03-19T05:00:00Z",
            "is_waiting_on_response": True,
            "is_resolved": False,
            "is_confirmed": True,
            "attachments": [{"id": 9, "name": "photo.png"}, {"id": 10, "name": "bundle.zip"}, {"id": 11, "name": "agent.log"}],
            "ticketlogs": [{"id": 1, "log_type": "Response", "note": "closed"}],
            "timelogs": [],
        }],
        synced_at="2026-03-19T01:00:00Z",
    )
    replace_ticket_documents(
        db,
        [
            {
                "doc_id": "ticket:101",
                "ticket_id": 101,
                "status": "Open",
                "account": "Acme",
                "user_name": "Alice",
                "technician": "Tech One",
                "updated_at": "2026-03-19T03:00:00Z",
                "text": "hello",
                "metadata": {
                    "priority": "High",
                    "category": "Hardware",
                    "class_name": "Service Request",
                    "submission_category": "Portal",
                    "resolution_category": "Completed",
                    "attachments_count": 3,
                    "attachment_extensions_csv": "log, png, zip",
                    "attachment_kinds_csv": "archive, image, log",
                    "attachment_kind_primary": "image",
                    "attachment_total_size_bytes": 3794,
                    "attachment_size_known_count": 0,
                    "attachment_image_count": 1,
                    "attachment_document_count": 0,
                    "attachment_spreadsheet_count": 0,
                    "attachment_archive_count": 1,
                    "attachment_log_count": 1,
                    "attachment_data_count": 0,
                    "attachment_audio_count": 0,
                    "attachment_video_count": 0,
                    "attachment_message_count": 0,
                    "attachment_other_count": 0,
                    "attachment_unknown_count": 0,
                    "has_attachments": True,
                    "ticketlogs_count": 5,
                    "public_log_count": 4,
                    "internal_log_count": 1,
                    "public_actor_count": 2,
                    "internal_actor_count": 1,
                    "total_actor_count": 3,
                    "waiting_log_count": 1,
                    "response_log_count": 2,
                    "resolution_log_count": 1,
                    "latest_log_date": "2026-03-19T10:00:00Z",
                    "latest_public_log_date": "2026-03-19T10:00:00Z",
                    "latest_internal_log_date": "2026-03-19T09:45:00Z",
                    "latest_public_actor_label": "Alice",
                    "latest_internal_actor_label": "Tech One",
                    "recent_public_actor_labels_csv": "Alice, Casey Dispatcher",
                    "recent_internal_actor_labels_csv": "Tech One",
                    "latest_waiting_log_date": "2026-03-20T10:00:00Z",
                    "latest_resolution_log_date": "2026-03-19T10:00:00Z",
                    "timelogs_count": 0,
                    "cleaned_subject": "hello",
                    "cleaned_initial_post": "Help me",
                    "cleaned_followup_note": "Waiting on customer reply",
                    "cleaned_explicit_followup_note": "Waiting on customer reply",
                    "cleaned_waiting_log_note": None,
                    "followup_note_source": "explicit_followup_note",
                    "cleaned_request_completion_note": "Complete during maintenance window",
                    "cleaned_next_step": "Call back tomorrow",
                    "cleaned_action_cue": "Call back tomorrow",
                    "action_cue_source": "next_step",
                    "cleaned_latest_response_note": "We are checking now",
                    "latest_response_date": "2026-03-19T09:15:00Z",
                    "cleaned_resolution_log_note": "Closed after maintenance",
                    "resolution_log_date": "2026-03-19T10:00:00Z",
                    "followup_date": "2026-03-20T10:00:00Z",
                    "request_completion_date": "2026-03-21T17:00:00Z",
                    "has_next_step": True,
                    "recent_log_types_csv": "Initial Post, Response",
                    "initial_response_present": True,
                    "user_email": "alice@example.com",
                    "user_email_domain": "example.com",
                    "user_created_email_domain": "example.com",
                    "technician_email_domain": "example.com",
                    "participant_email_domains_csv": "example.com",
                    "participant_email_domain_count": 1,
                    "public_participant_email_domains_csv": "example.com",
                    "public_participant_email_domain_count": 1,
                    "internal_participant_email_domains_csv": "example.com",
                    "internal_participant_email_domain_count": 1,
                    "support_group_name": "Managed Services",
                    "default_contract_name": "Gold",
                    "location_name": "HQ",
                    "account_location_name": "HQ Campus",
                    "department_key": "managed-services",
                    "department_label": "Managed Services",
                    "department_label_source": "support_group_name",
                    "ticket_number": "T-101",
                    "ticket_key": "abc-101",
                    "technician_email": "tech@example.com",
                    "user_phone": "520-555-0101",
                    "user_created_name": "Casey Dispatcher",
                    "user_created_email": "dispatcher@example.com",
                    "technician_type": "dispatcher",
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
                    "has_project_context": True,
                    "has_scheduled_parent": True,
                    "has_related_tickets": True,
                    "has_effort_tracking": True,
                    "has_public_logs": True,
                    "has_internal_logs": True,
                    "has_multi_public_participants": True,
                    "has_multi_internal_participants": False,
                    "has_named_public_participants": True,
                    "has_named_internal_participants": True,
                    "has_mixed_visibility_activity": True,
                    "has_waiting_logs": True,
                    "has_resolution_logs": True,
                    "days_old_in_minutes": 1440,
                    "waiting_minutes": 30,
                    "confirmed_by_name": "Tech Lead",
                    "confirmed_date": "2026-03-19T05:00:00Z",
                    "cleaned_confirmed_note": "User confirmed the printer was fixed.",
                    "is_via_email_parser": True,
                    "is_handle_by_callcentre": False,
                    "is_waiting_on_response": True,
                    "is_resolved": False,
                    "is_confirmed": True,
                    "account_label_source": "raw",
                    "user_label_source": "email",
                    "technician_label_source": "joined",
                    "resolution_summary": "Closed successfully",
                    "has_resolution_summary": True,
                    "materialization_version": DOCUMENT_MATERIALIZATION_VERSION,
                },
                "content_hash": "abc",
            },
            {
                "doc_id": "ticket:102",
                "ticket_id": 102,
                "status": "Closed",
                "account": "44",
                "user_name": "55",
                "technician": "66",
                "updated_at": "2026-03-18T03:00:00Z",
                "text": "numeric fallback labels",
                "metadata": {
                    "priority": "Low",
                    "category": "Software",
                    "department_label": "Dispatch",
                    "department_label_source": "class_name",
                    "ticket_number": "T-102",
                    "ticket_key": "abc-102",
                    "account_label_source": "id",
                    "user_label_source": "id",
                    "technician_label_source": "id",
                    "materialization_version": DOCUMENT_MATERIALIZATION_VERSION,
                },
                "content_hash": "ghi",
            },
        ],
        synced_at="2026-03-19T01:00:00Z",
    )
    replace_ticket_document_chunks(
        db,
        [
            {
                "chunk_id": "ticket:101:chunk:0",
                "doc_id": "ticket:101",
                "ticket_id": 101,
                "chunk_index": 0,
                "text": "chunk text",
                "content_hash": "def",
            },
            {
                "chunk_id": "ticket:102:chunk:0",
                "doc_id": "ticket:102",
                "ticket_id": 102,
                "chunk_index": 0,
                "text": "numeric fallback labels",
                "content_hash": "jkl",
            },
        ],
        synced_at="2026-03-19T01:00:00Z",
    )


def test_export_embedding_ready_chunks(tmp_path: Path) -> None:
    db = tmp_path / "sherpamind.sqlite3"
    seed(db)
    output = tmp_path / "embedding.jsonl"
    result = export_embedding_ready_chunks(db, output)
    assert result["status"] == "ok"
    rows = [json.loads(line) for line in output.read_text().splitlines()]
    row = next(item for item in rows if item["id"] == "ticket:101:chunk:0")
    assert len(rows) == 2
    assert row["metadata"]["account"] == "Acme"
    assert row["metadata"]["chunk_chars"] == len("chunk text")
    assert row["metadata"]["chunk_count_for_doc"] == 1
    assert row["metadata"]["doc_total_chunk_chars"] == len("chunk text")
    assert row["metadata"]["chunk_start_char"] == 0
    assert row["metadata"]["chunk_end_char"] == len("chunk text")
    assert row["metadata"]["chunk_char_span_ratio"] == 1.0
    assert row["metadata"]["previous_chunk_id"] is None
    assert row["metadata"]["next_chunk_id"] is None
    assert row["metadata"]["is_first_chunk"] is True
    assert row["metadata"]["is_last_chunk"] is True
    assert row["metadata"]["is_multi_chunk_doc"] is False
    assert row["metadata"]["chunk_primary_section"] == "general"
    assert row["metadata"]["chunk_section_labels"] == "general"
    assert row["metadata"]["chunk_section_count"] == 1
    assert row["metadata"]["chunk_has_issue_context"] is False
    assert row["metadata"]["chunk_has_activity_context"] is False
    assert row["metadata"]["chunk_section_line_counts"] == {"general": 1}
    assert row["metadata"]["priority"] == "High"
    assert row["metadata"]["class_name"] == "Service Request"
    assert row["metadata"]["submission_category"] == "Portal"
    assert row["metadata"]["resolution_category"] == "Completed"
    assert row["metadata"]["ticketlogs_count"] == 5
    assert row["metadata"]["public_log_count"] == 4
    assert row["metadata"]["internal_log_count"] == 1
    assert row["metadata"]["public_actor_count"] == 2
    assert row["metadata"]["internal_actor_count"] == 1
    assert row["metadata"]["total_actor_count"] == 3
    assert row["metadata"]["waiting_log_count"] == 1
    assert row["metadata"]["response_log_count"] == 2
    assert row["metadata"]["resolution_log_count"] == 1
    assert row["metadata"]["latest_log_date"] == "2026-03-19T10:00:00Z"
    assert row["metadata"]["latest_public_log_date"] == "2026-03-19T10:00:00Z"
    assert row["metadata"]["latest_internal_log_date"] == "2026-03-19T09:45:00Z"
    assert row["metadata"]["latest_public_actor_label"] == "Alice"
    assert row["metadata"]["latest_internal_actor_label"] == "Tech One"
    assert row["metadata"]["recent_public_actor_labels"] == "Alice, Casey Dispatcher"
    assert row["metadata"]["recent_internal_actor_labels"] == "Tech One"
    assert row["metadata"]["latest_waiting_log_date"] == "2026-03-20T10:00:00Z"
    assert row["metadata"]["latest_resolution_log_date"] == "2026-03-19T10:00:00Z"
    assert row["metadata"]["attachment_extensions"] == "log, png, zip"
    assert row["metadata"]["attachment_kinds"] == "archive, image, log"
    assert row["metadata"]["attachment_kind_primary"] == "image"
    assert row["metadata"]["attachment_total_size_bytes"] == 3794
    assert row["metadata"]["attachment_size_known_count"] == 0
    assert row["metadata"]["attachment_image_count"] == 1
    assert row["metadata"]["attachment_document_count"] == 0
    assert row["metadata"]["attachment_spreadsheet_count"] == 0
    assert row["metadata"]["attachment_archive_count"] == 1
    assert row["metadata"]["attachment_log_count"] == 1
    assert row["metadata"]["attachment_data_count"] == 0
    assert row["metadata"]["attachment_audio_count"] == 0
    assert row["metadata"]["attachment_video_count"] == 0
    assert row["metadata"]["attachment_message_count"] == 0
    assert row["metadata"]["attachment_other_count"] == 0
    assert row["metadata"]["attachment_unknown_count"] == 0
    assert row["metadata"]["has_attachments"] is True
    assert row["metadata"]["cleaned_followup_note"] == "Waiting on customer reply"
    assert row["metadata"]["cleaned_explicit_followup_note"] == "Waiting on customer reply"
    assert row["metadata"]["cleaned_waiting_log_note"] is None
    assert row["metadata"]["followup_note_source"] == "explicit_followup_note"
    assert row["metadata"]["cleaned_request_completion_note"] == "Complete during maintenance window"
    assert row["metadata"]["cleaned_next_step"] == "Call back tomorrow"
    assert row["metadata"]["cleaned_action_cue"] == "Call back tomorrow"
    assert row["metadata"]["action_cue_source"] == "next_step"
    assert row["metadata"]["cleaned_latest_response_note"] == "We are checking now"
    assert row["metadata"]["latest_response_date"] == "2026-03-19T09:15:00Z"
    assert row["metadata"]["cleaned_resolution_log_note"] == "Closed after maintenance"
    assert row["metadata"]["resolution_log_date"] == "2026-03-19T10:00:00Z"
    assert row["metadata"]["followup_date"] == "2026-03-20T10:00:00Z"
    assert row["metadata"]["request_completion_date"] == "2026-03-21T17:00:00Z"
    assert row["metadata"]["user_email_domain"] == "example.com"
    assert row["metadata"]["user_created_email_domain"] == "example.com"
    assert row["metadata"]["technician_email_domain"] == "example.com"
    assert row["metadata"]["participant_email_domains"] == "example.com"
    assert row["metadata"]["participant_email_domain_count"] == 1
    assert row["metadata"]["public_participant_email_domains"] == "example.com"
    assert row["metadata"]["public_participant_email_domain_count"] == 1
    assert row["metadata"]["internal_participant_email_domains"] == "example.com"
    assert row["metadata"]["internal_participant_email_domain_count"] == 1
    assert row["metadata"]["support_group_name"] == "Managed Services"
    assert row["metadata"]["default_contract_name"] == "Gold"
    assert row["metadata"]["location_name"] == "HQ"
    assert row["metadata"]["account_location_name"] == "HQ Campus"
    assert row["metadata"]["department_key"] == "managed-services"
    assert row["metadata"]["department_label"] == "Managed Services"
    assert row["metadata"]["department_label_source"] == "support_group_name"
    assert row["metadata"]["ticket_number"] == "T-101"
    assert row["metadata"]["ticket_key"] == "abc-101"
    assert row["metadata"]["technician_email"] == "tech@example.com"
    assert row["metadata"]["user_phone"] == "520-555-0101"
    assert row["metadata"]["user_created_name"] == "Casey Dispatcher"
    assert row["metadata"]["user_created_email"] == "dispatcher@example.com"
    assert row["metadata"]["technician_type"] == "dispatcher"
    assert row["metadata"]["project_id"] == 77
    assert row["metadata"]["project_name"] == "Printer Rollout"
    assert row["metadata"]["scheduled_ticket_id"] == 909
    assert row["metadata"]["related_tickets_count"] == 4
    assert row["metadata"]["estimated_time"] == 2.5
    assert row["metadata"]["remaining_hours"] == 1.25
    assert row["metadata"]["total_hours"] == 3.75
    assert row["metadata"]["total_time_in_minutes"] == 225
    assert row["metadata"]["labor_cost"] == 450
    assert row["metadata"]["percentage_complete"] == 60
    assert row["metadata"]["has_project_context"] is True
    assert row["metadata"]["has_scheduled_parent"] is True
    assert row["metadata"]["has_related_tickets"] is True
    assert row["metadata"]["has_effort_tracking"] is True
    assert row["metadata"]["has_public_logs"] is True
    assert row["metadata"]["has_internal_logs"] is True
    assert row["metadata"]["has_multi_public_participants"] is True
    assert row["metadata"]["has_multi_internal_participants"] is False
    assert row["metadata"]["has_named_public_participants"] is True
    assert row["metadata"]["has_named_internal_participants"] is True
    assert row["metadata"]["has_mixed_visibility_activity"] is True
    assert row["metadata"]["has_waiting_logs"] is True
    assert row["metadata"]["has_resolution_logs"] is True
    assert row["metadata"]["days_old_in_minutes"] == 1440
    assert row["metadata"]["waiting_minutes"] == 30
    assert row["metadata"]["confirmed_by_name"] == "Tech Lead"
    assert row["metadata"]["confirmed_date"] == "2026-03-19T05:00:00Z"
    assert row["metadata"]["cleaned_confirmed_note"] == "User confirmed the printer was fixed."
    assert row["metadata"]["is_via_email_parser"] is True
    assert row["metadata"]["is_handle_by_callcentre"] is False
    assert row["metadata"]["is_waiting_on_response"] is True
    assert row["metadata"]["is_resolved"] is False
    assert row["metadata"]["is_confirmed"] is True
    assert row["metadata"]["has_next_step"] is True
    assert row["metadata"]["recent_log_types"] == "Initial Post, Response"
    assert row["metadata"]["user_email"] == "alice@example.com"
    assert row["metadata"]["account_label_source"] == "raw"
    assert row["metadata"]["user_label_source"] == "email"
    assert row["metadata"]["technician_label_source"] == "joined"
    assert row["metadata"]["resolution_summary"] == "Closed successfully"
    assert row["metadata"]["has_resolution_summary"] is True


def test_export_embedding_ready_chunks_infers_structured_chunk_sections(tmp_path: Path) -> None:
    db = tmp_path / "sherpamind.sqlite3"
    initialize_db(db)
    replace_ticket_documents(
        db,
        [{
            "doc_id": "ticket:301",
            "ticket_id": 301,
            "status": "Open",
            "account": "Acme",
            "user_name": "Alice",
            "technician": "Tech One",
            "updated_at": "2026-03-19T03:00:00Z",
            "text": "Issue summary: Printer offline\nNext step: Reboot print spooler\nRecent log summary: Spooler crashed overnight\nResolution log note: Restored after restart\nAttachments (metadata only): shot.png [1024 bytes]",
            "metadata": {"materialization_version": DOCUMENT_MATERIALIZATION_VERSION},
            "content_hash": "doc-301",
        }],
        synced_at="2026-03-19T01:00:00Z",
    )
    replace_ticket_document_chunks(
        db,
        [{
            "chunk_id": "ticket:301:chunk:0",
            "doc_id": "ticket:301",
            "ticket_id": 301,
            "chunk_index": 0,
            "text": "Issue summary: Printer offline\nNext step: Reboot print spooler\nRecent log summary: Spooler crashed overnight\nResolution log note: Restored after restart\nAttachments (metadata only): shot.png [1024 bytes]",
            "content_hash": "chunk-301",
        }],
        synced_at="2026-03-19T01:00:00Z",
    )

    output = tmp_path / "embedding-sections.jsonl"
    export_embedding_ready_chunks(db, output)
    row = json.loads(output.read_text().splitlines()[0])
    metadata = row["metadata"]

    assert metadata["chunk_primary_section"] == "issue"
    assert metadata["chunk_section_labels"] == "issue, action, activity, resolution, attachments"
    assert metadata["chunk_section_count"] == 5
    assert metadata["chunk_has_issue_context"] is True
    assert metadata["chunk_has_action_context"] is True
    assert metadata["chunk_has_activity_context"] is True
    assert metadata["chunk_has_resolution_context"] is True
    assert metadata["chunk_has_attachment_context"] is True
    assert metadata["chunk_has_identity_context"] is False
    assert metadata["chunk_section_line_counts"]["issue"] == 1
    assert metadata["chunk_section_line_counts"]["attachments"] == 1



def test_export_embedding_ready_chunks_includes_chunk_position_links(tmp_path: Path) -> None:
    db = tmp_path / "sherpamind.sqlite3"
    initialize_db(db)
    replace_ticket_documents(
        db,
        [{
            "doc_id": "ticket:201",
            "ticket_id": 201,
            "status": "Open",
            "account": "Acme",
            "user_name": "Alice",
            "technician": "Tech One",
            "updated_at": "2026-03-19T03:00:00Z",
            "text": "alpha beta gamma delta",
            "metadata": {"materialization_version": DOCUMENT_MATERIALIZATION_VERSION},
            "content_hash": "doc-201",
        }],
        synced_at="2026-03-19T01:00:00Z",
    )
    replace_ticket_document_chunks(
        db,
        [
            {
                "chunk_id": "ticket:201:chunk:0",
                "doc_id": "ticket:201",
                "ticket_id": 201,
                "chunk_index": 0,
                "text": "alpha beta",
                "content_hash": "chunk-0",
            },
            {
                "chunk_id": "ticket:201:chunk:1",
                "doc_id": "ticket:201",
                "ticket_id": 201,
                "chunk_index": 1,
                "text": "gamma delta",
                "content_hash": "chunk-1",
            },
        ],
        synced_at="2026-03-19T01:00:00Z",
    )

    output = tmp_path / "embedding-multi.jsonl"
    export_embedding_ready_chunks(db, output)
    rows = {row["id"]: row for row in (json.loads(line) for line in output.read_text().splitlines())}

    first = rows["ticket:201:chunk:0"]["metadata"]
    second = rows["ticket:201:chunk:1"]["metadata"]

    assert first["chunk_start_char"] == 0
    assert first["chunk_end_char"] == len("alpha beta")
    assert first["previous_chunk_id"] is None
    assert first["next_chunk_id"] == "ticket:201:chunk:1"
    assert first["chunk_char_span_ratio"] == round(len("alpha beta") / len("alpha betagamma delta"), 4)

    assert second["chunk_start_char"] == len("alpha beta")
    assert second["chunk_end_char"] == len("alpha beta") + len("gamma delta")
    assert second["previous_chunk_id"] == "ticket:201:chunk:0"
    assert second["next_chunk_id"] is None



def test_get_retrieval_readiness_summary(tmp_path: Path) -> None:
    db = tmp_path / "sherpamind.sqlite3"
    seed(db)
    summary = get_retrieval_readiness_summary(db)
    assert summary["chunk_count"] == 2
    assert summary["document_count"] == 2
    assert summary["chunk_quality"]["max_chunk_chars"] == len("numeric fallback labels")
    assert summary["document_chunk_topology"]["avg_chunks_per_document"] == 1.0
    assert summary["document_chunk_topology"]["single_chunk_document_count"] == 2
    assert summary["document_chunk_topology"]["multi_chunk_document_count"] == 0
    assert summary["freshness"]["document_count_with_timestamps"] == 2
    assert summary["freshness"]["documents_materialized_behind"] == 1
    assert summary["freshness"]["documents_materialized_current_or_ahead"] == 1
    assert summary["freshness"]["lagging_document_ratio"] == 0.5
    assert summary["freshness"]["max_lag_minutes"] == 120.0
    assert summary["freshness"]["avg_lag_minutes"] == 120.0
    assert summary["freshness"]["lag_buckets"]["lag_le_6h"]["documents"] == 1
    assert summary["freshness"]["status_breakdown"]["Open"]["lagging_documents"] == 1
    assert summary["freshness"]["status_breakdown"]["Closed"]["lagging_documents"] == 0
    assert summary["freshness"]["top_lagging_documents"][0]["ticket_id"] == 101
    assert summary["freshness"]["top_lagging_documents"][0]["lag_minutes"] == 120.0
    assert summary["materialization_freshness_lag"]["windows"]["latest_updated_at"] == summary["freshness"]["latest_updated_at"]
    assert summary["materialization_freshness_lag"]["lag_summary"]["documents_materialized_behind"] == 1
    assert summary["materialization_freshness_lag"]["status_breakdown"]["Open"]["lagging_documents"] == 1
    assert summary["materialization_freshness_lag"]["lag_buckets"]["lag_le_6h"]["documents"] == 1
    assert summary["materialization_freshness_lag"]["top_lagging_documents"][0]["ticket_id"] == 101
    assert summary["filter_facets"]["accounts"] == ["44", "Acme"]
    assert summary["filter_facets"]["priorities"] == ["High", "Low"]
    assert summary["filter_facets"]["class_names"] == ["Service Request"]
    assert summary["filter_facets"]["submission_categories"] == ["Portal"]
    assert summary["filter_facets"]["resolution_categories"] == ["Completed"]
    assert summary["filter_facets"]["departments"] == ["Dispatch", "Managed Services"]
    assert summary["filter_facets"]["attachment_extensions"] == ["log", "png", "zip"]
    assert summary["filter_facets"]["attachment_kinds"] == ["archive", "image", "log"]
    assert summary["filter_facets"]["user_email_domains"] == ["example.com"]
    assert summary["filter_facets"]["user_created_email_domains"] == ["example.com"]
    assert summary["filter_facets"]["technician_email_domains"] == ["example.com"]
    assert summary["filter_facets"]["participant_email_domains"] == ["example.com"]
    assert summary["filter_facets"]["chunk_primary_sections"] == ["general"]
    assert summary["filter_facets"]["chunk_section_labels"] == ["general"]
    assert summary["metadata_coverage"]["chunk_primary_section"]["chunks"] == 2
    assert summary["metadata_coverage"]["chunk_section_labels"]["chunks"] == 2
    assert summary["metadata_coverage"]["chunk_has_issue_context"]["chunks"] == 0
    assert summary["metadata_coverage"]["chunk_has_attachment_context"]["chunks"] == 0
    assert summary["metadata_coverage"]["cleaned_subject"]["chunks"] == 1
    assert summary["metadata_coverage"]["public_log_count"]["chunks"] == 1
    assert summary["metadata_coverage"]["internal_log_count"]["chunks"] == 1
    assert summary["metadata_coverage"]["public_actor_count"]["chunks"] == 1
    assert summary["metadata_coverage"]["internal_actor_count"]["chunks"] == 1
    assert summary["metadata_coverage"]["total_actor_count"]["chunks"] == 1
    assert summary["metadata_coverage"]["waiting_log_count"]["chunks"] == 1
    assert summary["metadata_coverage"]["response_log_count"]["chunks"] == 1
    assert summary["metadata_coverage"]["resolution_log_count"]["chunks"] == 1
    assert summary["metadata_coverage"]["latest_log_date"]["chunks"] == 1
    assert summary["metadata_coverage"]["latest_public_log_date"]["chunks"] == 1
    assert summary["metadata_coverage"]["latest_internal_log_date"]["chunks"] == 1
    assert summary["metadata_coverage"]["latest_public_actor_label"]["chunks"] == 1
    assert summary["metadata_coverage"]["latest_internal_actor_label"]["chunks"] == 1
    assert summary["metadata_coverage"]["recent_public_actor_labels"]["chunks"] == 1
    assert summary["metadata_coverage"]["recent_internal_actor_labels"]["chunks"] == 1
    assert summary["metadata_coverage"]["latest_waiting_log_date"]["chunks"] == 1
    assert summary["metadata_coverage"]["latest_resolution_log_date"]["chunks"] == 1
    assert summary["metadata_coverage"]["cleaned_followup_note"]["chunks"] == 1
    assert summary["metadata_coverage"]["cleaned_explicit_followup_note"]["chunks"] == 1
    assert summary["metadata_coverage"]["cleaned_waiting_log_note"]["chunks"] == 0
    assert summary["metadata_coverage"]["cleaned_action_cue"]["chunks"] == 1
    assert summary["metadata_coverage"]["cleaned_latest_response_note"]["chunks"] == 1
    assert summary["metadata_coverage"]["cleaned_resolution_log_note"]["chunks"] == 1
    assert summary["metadata_coverage"]["class_name"]["chunks"] == 1
    assert summary["metadata_coverage"]["submission_category"]["chunks"] == 1
    assert summary["metadata_coverage"]["resolution_category"]["chunks"] == 1
    assert summary["metadata_coverage"]["support_group_name"]["chunks"] == 1
    assert summary["metadata_coverage"]["user_email_domain"]["chunks"] == 1
    assert summary["metadata_coverage"]["user_created_email_domain"]["chunks"] == 1
    assert summary["metadata_coverage"]["technician_email_domain"]["chunks"] == 1
    assert summary["metadata_coverage"]["participant_email_domains"]["chunks"] == 1
    assert summary["metadata_coverage"]["public_participant_email_domains"]["chunks"] == 1
    assert summary["metadata_coverage"]["internal_participant_email_domains"]["chunks"] == 1
    assert summary["metadata_coverage"]["account_location_name"]["chunks"] == 1
    assert summary["metadata_coverage"]["department_key"]["chunks"] == 1
    assert summary["metadata_coverage"]["department_label"]["chunks"] == 2
    assert summary["metadata_coverage"]["ticket_number"]["chunks"] == 2
    assert summary["metadata_coverage"]["ticket_key"]["chunks"] == 2
    assert summary["metadata_coverage"]["attachment_extensions"]["chunks"] == 1
    assert summary["metadata_coverage"]["attachment_kinds"]["chunks"] == 1
    assert summary["metadata_coverage"]["attachment_kind_primary"]["chunks"] == 1
    assert summary["metadata_coverage"]["attachment_total_size_bytes"]["chunks"] == 1
    assert summary["metadata_coverage"]["attachment_size_known_count"]["chunks"] == 0
    assert summary["metadata_coverage"]["attachment_image_count"]["chunks"] == 1
    assert summary["metadata_coverage"]["attachment_document_count"]["chunks"] == 0
    assert summary["metadata_coverage"]["attachment_spreadsheet_count"]["chunks"] == 0
    assert summary["metadata_coverage"]["attachment_archive_count"]["chunks"] == 1
    assert summary["metadata_coverage"]["attachment_log_count"]["chunks"] == 1
    assert summary["metadata_coverage"]["attachment_data_count"]["chunks"] == 0
    assert summary["metadata_coverage"]["attachment_audio_count"]["chunks"] == 0
    assert summary["metadata_coverage"]["attachment_video_count"]["chunks"] == 0
    assert summary["metadata_coverage"]["attachment_message_count"]["chunks"] == 0
    assert summary["metadata_coverage"]["attachment_other_count"]["chunks"] == 0
    assert summary["metadata_coverage"]["attachment_unknown_count"]["chunks"] == 0
    assert summary["metadata_coverage"]["technician_email"]["chunks"] == 1
    assert summary["metadata_coverage"]["user_phone"]["chunks"] == 1
    assert summary["metadata_coverage"]["user_created_name"]["chunks"] == 1
    assert summary["metadata_coverage"]["user_created_email"]["chunks"] == 1
    assert summary["metadata_coverage"]["technician_type"]["chunks"] == 1
    assert summary["metadata_coverage"]["project_id"]["chunks"] == 1
    assert summary["metadata_coverage"]["project_name"]["chunks"] == 1
    assert summary["metadata_coverage"]["scheduled_ticket_id"]["chunks"] == 1
    assert summary["metadata_coverage"]["related_tickets_count"]["chunks"] == 1
    assert summary["metadata_coverage"]["estimated_time"]["chunks"] == 1
    assert summary["metadata_coverage"]["remaining_hours"]["chunks"] == 1
    assert summary["metadata_coverage"]["total_hours"]["chunks"] == 1
    assert summary["metadata_coverage"]["total_time_in_minutes"]["chunks"] == 1
    assert summary["metadata_coverage"]["labor_cost"]["chunks"] == 1
    assert summary["metadata_coverage"]["percentage_complete"]["chunks"] == 1
    assert summary["metadata_coverage"]["has_project_context"]["chunks"] == 1
    assert summary["metadata_coverage"]["has_scheduled_parent"]["chunks"] == 1
    assert summary["metadata_coverage"]["has_related_tickets"]["chunks"] == 1
    assert summary["metadata_coverage"]["has_effort_tracking"]["chunks"] == 1
    assert summary["metadata_coverage"]["has_public_logs"]["chunks"] == 1
    assert summary["metadata_coverage"]["has_internal_logs"]["chunks"] == 1
    assert summary["metadata_coverage"]["has_multi_public_participants"]["chunks"] == 1
    assert summary["metadata_coverage"]["has_multi_internal_participants"]["chunks"] == 0
    assert summary["metadata_coverage"]["has_named_public_participants"]["chunks"] == 1
    assert summary["metadata_coverage"]["has_named_internal_participants"]["chunks"] == 1
    assert summary["metadata_coverage"]["has_mixed_visibility_activity"]["chunks"] == 1
    assert summary["metadata_coverage"]["has_waiting_logs"]["chunks"] == 1
    assert summary["metadata_coverage"]["has_resolution_logs"]["chunks"] == 1
    assert summary["metadata_coverage"]["days_old_in_minutes"]["chunks"] == 1
    assert summary["metadata_coverage"]["waiting_minutes"]["chunks"] == 1
    assert summary["document_metadata_coverage"]["department_label"]["documents"] == 2
    assert summary["metadata_coverage"]["confirmed_date"]["chunks"] == 1
    assert summary["metadata_coverage"]["cleaned_confirmed_note"]["chunks"] == 1
    assert summary["metadata_coverage"]["is_via_email_parser"]["chunks"] == 1
    assert summary["metadata_coverage"]["is_handle_by_callcentre"]["chunks"] == 1
    assert summary["metadata_coverage"]["is_waiting_on_response"]["chunks"] == 1
    assert summary["source_metadata_coverage"]["support_group_name"]["status"] == "upstream_absent"
    assert summary["source_metadata_coverage"]["support_group_name"]["source_documents"] == 0
    assert summary["source_metadata_coverage"]["support_group_name"]["materialized_documents"] == 1
    assert summary["source_metadata_coverage"]["ticket_number"]["ticket_rows"] == 2
    assert summary["source_metadata_coverage"]["ticket_number"]["detail_rows"] == 0
    assert summary["source_metadata_coverage"]["project_name"]["detail_rows"] == 0
    assert summary["source_metadata_coverage"]["project_name"]["status"] == "upstream_absent"
    assert summary["source_metadata_coverage"]["scheduled_ticket_id"]["detail_rows"] == 0
    assert summary["source_metadata_coverage"]["scheduled_ticket_id"]["status"] == "upstream_absent"
    assert summary["source_metadata_coverage"]["user_email_domain"]["ticket_rows"] == 0
    assert summary["source_metadata_coverage"]["user_email_domain"]["status"] == "upstream_absent"
    assert summary["source_metadata_coverage"]["user_created_email_domain"]["detail_rows"] == 1
    assert summary["source_metadata_coverage"]["user_created_email_domain"]["status"] == "materialized"
    assert summary["source_metadata_coverage"]["technician_email_domain"]["ticket_rows"] == 1
    assert summary["source_metadata_coverage"]["technician_email_domain"]["status"] == "materialized"
    assert summary["source_metadata_coverage"]["default_contract_name"]["detail_rows"] == 1
    assert summary["source_metadata_coverage"]["default_contract_name"]["status"] == "materialized"
    assert summary["source_backed_metadata"]["fields"]["default_contract_name"]["status"] == "materialized"
    assert summary["source_backed_metadata"]["fields"]["support_group_name"]["status"] == "upstream_absent"
    assert summary["source_backed_metadata"]["status_counts"]["materialized"] >= 1
    assert summary["source_backed_metadata"]["status_counts"]["upstream_absent"] >= 1
    assert any(field["field"] == "support_group_name" for field in summary["source_backed_metadata"]["upstream_absent_fields"])
    assert summary["source_backed_metadata"]["fields_with_invalid_source"] == []
    assert summary["label_source_summary"]["account_label_source"]["id"]["chunks"] == 1
    assert summary["label_source_summary"]["account_label_source"]["raw"]["chunks"] == 1
    assert summary["label_source_summary"]["user_label_source"]["email"]["chunks"] == 1
    assert summary["label_source_summary"]["user_label_source"]["id"]["chunks"] == 1
    assert summary["label_source_summary"]["technician_label_source"]["joined"]["chunks"] == 1
    assert summary["label_source_summary"]["technician_label_source"]["id"]["chunks"] == 1
    assert summary["label_source_summary"]["department_label_source"]["class_name"]["chunks"] == 1
    assert summary["label_source_summary"]["department_label_source"]["support_group_name"]["chunks"] == 1
    assert summary["label_source_summary"]["followup_note_source"]["explicit_followup_note"]["chunks"] == 1
    assert summary["label_source_summary"]["followup_note_source"]["missing"]["chunks"] == 1
    assert summary["label_source_summary"]["action_cue_source"]["missing"]["chunks"] == 1
    assert summary["label_source_summary"]["action_cue_source"]["next_step"]["chunks"] == 1
    assert summary["entity_label_quality"]["account"]["readable_chunks"] == 1
    assert summary["entity_label_quality"]["account"]["identifier_like_chunks"] == 1
    assert summary["entity_label_quality"]["account"]["fallback_source_chunks"] == 1
    assert summary["entity_label_quality"]["account"]["identifier_like_distinct_value_sample"] == ["44"]
    assert summary["entity_label_quality"]["user"]["readable_source_chunks"] == 1
    assert summary["entity_label_quality"]["user"]["fallback_source_chunks"] == 1
    assert summary["entity_label_quality"]["technician"]["identifier_like_chunks"] == 1
    assert summary["entity_label_quality"]["department"]["readable_chunks"] == 2
    assert summary["retrieval_signal_pressure"]["accounts"]["summary"]["group_count"] == 0
    assert summary["retrieval_signal_pressure"]["categories"]["summary"]["group_count"] == 0
    assert summary["retrieval_signal_pressure"]["technicians"]["summary"]["group_count"] == 0
    assert summary["metadata_coverage"]["has_attachments"]["ratio"] == 0.5
    assert summary["materialization"]["current_version"] >= 1
    assert summary["materialization"]["current_version_docs"] == 2
    assert summary["materialization"]["stale_docs"] == 0
    assert summary["materialization"]["chunk_rows_at_current_version"] == 2
    assert summary["vector_index"]["total_chunk_rows"] == 2
    assert summary["content_hash_summary"]["present_count"] == 2


def test_source_metadata_coverage_treats_invalid_email_domains_as_upstream_quality_not_promotion_gap(tmp_path: Path) -> None:
    db = tmp_path / "sherpamind.sqlite3"
    initialize_db(db)
    upsert_tickets(
        db,
        [{
            "id": 201,
            "account_id": 1,
            "user_id": 2,
            "tech_id": 3,
            "subject": "invalid technician email",
            "status": "Open",
            "priority_name": "Normal",
            "created_time": "2026-03-19T01:00:00Z",
            "updated_time": "2026-03-19T03:00:00Z",
            "technician_email": "Dec 18 2017  9:01:07:433PMNew Tickets",
        }],
        synced_at="2026-03-19T01:00:00Z",
    )
    replace_ticket_documents(
        db,
        [{
            "doc_id": "ticket:201",
            "ticket_id": 201,
            "status": "Open",
            "account": "Acme",
            "user_name": "Alice",
            "technician": "Queue",
            "updated_at": "2026-03-19T03:00:00Z",
            "text": "invalid technician email",
            "metadata": {
                "priority": "Normal",
                "category": None,
                "ticket_number": None,
                "ticket_key": None,
                "technician_email": "Dec 18 2017  9:01:07:433PMNew Tickets",
                "technician_email_domain": None,
                "account_label_source": "raw",
                "user_label_source": "raw",
                "technician_label_source": "raw",
                "materialization_version": DOCUMENT_MATERIALIZATION_VERSION,
            },
            "content_hash": "bad-email-doc",
        }],
        synced_at="2026-03-19T01:00:00Z",
    )
    replace_ticket_document_chunks(
        db,
        [{
            "chunk_id": "ticket:201:chunk:0",
            "doc_id": "ticket:201",
            "ticket_id": 201,
            "chunk_index": 0,
            "text": "invalid technician email",
            "content_hash": "bad-email-chunk",
        }],
        synced_at="2026-03-19T01:00:00Z",
    )

    summary = get_retrieval_readiness_summary(db)
    field = summary["source_metadata_coverage"]["technician_email_domain"]

    assert field["raw_ticket_rows"] == 1
    assert field["ticket_rows"] == 0
    assert field["invalid_ticket_rows"] == 1
    assert field["source_documents"] == 0
    assert field["promotion_gap_documents"] == 0
    assert field["status"] == "upstream_absent"
    assert summary["source_backed_metadata"]["fields_with_promotion_gap"] == []
    assert summary["source_backed_metadata"]["fields_with_invalid_source"] == [
        {
            "field": "technician_email_domain",
            "raw_ticket_rows": 1,
            "raw_detail_rows": 0,
            "invalid_ticket_rows": 1,
            "invalid_detail_rows": 0,
            "source_documents": 0,
        }
    ]


def test_retrieval_signal_pressure_surfaces_low_coverage_groups(tmp_path: Path) -> None:
    db = tmp_path / "pressure.sqlite3"
    initialize_db(db)
    documents = []
    chunks = []
    for idx in range(10):
        ticket_id = 300 + idx
        documents.append({
            "doc_id": f"ticket:{ticket_id}",
            "ticket_id": ticket_id,
            "status": "Open" if idx < 7 else "Closed",
            "account": "Acme",
            "user_name": f"User {idx}",
            "technician": "Tech One" if idx < 3 else "Tech Two",
            "updated_at": f"2026-03-{10 + idx:02d}T03:00:00Z",
            "text": f"ticket {ticket_id}",
            "metadata": {
                "priority": "Normal",
                "category": "Hardware",
                "detail_available": idx < 2,
                "cleaned_initial_post": f"issue {ticket_id}" if idx == 0 else None,
                "cleaned_action_cue": f"action {ticket_id}" if idx == 0 else None,
                "recent_log_types_csv": "Response" if idx == 0 else None,
                "resolution_summary": "resolved" if idx == 9 else None,
                "attachments_count": 1 if idx == 0 else 0,
                "materialization_version": DOCUMENT_MATERIALIZATION_VERSION,
            },
            "content_hash": f"doc-{ticket_id}",
        })
        chunks.append({
            "chunk_id": f"ticket:{ticket_id}:chunk:0",
            "doc_id": f"ticket:{ticket_id}",
            "ticket_id": ticket_id,
            "chunk_index": 0,
            "text": f"ticket {ticket_id}",
            "content_hash": f"chunk-{ticket_id}",
            "synced_at": "2026-03-09T01:00:00Z" if idx == 0 else "2026-03-20T01:00:00Z",
        })
    replace_ticket_documents(db, documents, synced_at="2026-03-20T01:00:00Z")
    replace_ticket_document_chunks(db, chunks, synced_at="2026-03-20T01:00:00Z")

    summary = get_retrieval_readiness_summary(db)
    account_row = summary["retrieval_signal_pressure"]["accounts"]["rows"][0]
    category_row = summary["retrieval_signal_pressure"]["categories"]["rows"][0]
    technician_row = summary["retrieval_signal_pressure"]["technicians"]["rows"][0]

    assert summary["retrieval_signal_pressure"]["accounts"]["summary"]["group_count"] == 1
    assert summary["retrieval_signal_pressure"]["categories"]["summary"]["group_count"] == 1
    assert summary["retrieval_signal_pressure"]["technicians"]["summary"]["group_count"] == 2
    assert summary["retrieval_signal_pressure"]["accounts"]["summary"]["low_richness_groups"] == 1
    assert account_row["label"] == "Acme"
    assert account_row["total_documents"] == 10
    assert account_row["detail_documents"] == 2
    assert account_row["low_richness_backlog"] == 8
    assert account_row["lagging_documents"] == 0
    assert account_row["richness_ratio"] == 0.1167
    assert category_row["label"] == "Hardware"
    assert technician_row["label"] == "Tech Two"
    assert technician_row["low_richness_backlog"] == 8 - 1


def test_export_embedding_manifest(tmp_path: Path) -> None:
    db = tmp_path / "sherpamind.sqlite3"
    seed(db)
    output = tmp_path / "manifest.json"
    result = export_embedding_manifest(db, output)
    assert result["status"] == "ok"
    manifest = json.loads(output.read_text())
    assert manifest["chunk_count"] == 2
    assert manifest["filter_facets"]["accounts"] == ["44", "Acme"]
    assert manifest["filter_facets"]["departments"] == ["Dispatch", "Managed Services"]
    assert manifest["filter_facets"]["attachment_extensions"] == ["log", "png", "zip"]
    assert manifest["filter_facets"]["attachment_kinds"] == ["archive", "image", "log"]
    assert manifest["filter_facets"]["user_email_domains"] == ["example.com"]
    assert manifest["filter_facets"]["user_created_email_domains"] == ["example.com"]
    assert manifest["filter_facets"]["technician_email_domains"] == ["example.com"]
    assert manifest["filter_facets"]["participant_email_domains"] == ["example.com"]
    assert manifest["filter_facets"]["chunk_primary_sections"] == ["general"]
    assert manifest["filter_facets"]["chunk_section_labels"] == ["general"]
    assert manifest["document_chunk_topology"]["avg_chunks_per_document"] == 1.0
    assert manifest["metadata_coverage"]["resolution_summary"]["chunks"] == 1
    assert manifest["document_metadata_coverage"]["resolution_summary"]["documents"] == 1
    assert manifest["metadata_coverage"]["public_log_count"]["chunks"] == 1
    assert manifest["metadata_coverage"]["public_actor_count"]["chunks"] == 1
    assert manifest["metadata_coverage"]["latest_public_actor_label"]["chunks"] == 1
    assert manifest["metadata_coverage"]["has_internal_logs"]["chunks"] == 1
    assert manifest["metadata_coverage"]["has_mixed_visibility_activity"]["chunks"] == 1
    assert manifest["metadata_coverage"]["account_location_name"]["chunks"] == 1
    assert manifest["metadata_coverage"]["project_name"]["chunks"] == 1
    assert manifest["metadata_coverage"]["has_effort_tracking"]["chunks"] == 1
    assert manifest["metadata_coverage"]["participant_email_domains"]["chunks"] == 1
    assert manifest["source_metadata_coverage"]["default_contract_name"]["detail_rows"] == 1
    assert manifest["source_metadata_coverage"]["support_group_name"]["status"] == "upstream_absent"
    assert manifest["source_backed_metadata"]["status_counts"]["upstream_absent"] >= 1
    assert manifest["materialization_freshness_lag"]["lag_summary"]["documents_materialized_behind"] == 1
    assert manifest["label_source_summary"]["account_label_source"]["raw"]["chunks"] == 1
    assert manifest["entity_label_quality"]["account"]["identifier_like_chunks"] == 1
