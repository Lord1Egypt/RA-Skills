from pathlib import Path

from sherpamind.db import initialize_db, upsert_accounts, upsert_ticket_details, upsert_tickets, upsert_technicians, upsert_users
from sherpamind.documents import materialize_ticket_documents
from sherpamind.public_artifacts import _invalid_source_rows, _source_materialization_gap_rows, generate_public_snapshot


def seed_fixture(db: Path) -> None:
    initialize_db(db)
    upsert_accounts(
        db,
        [
            {"id": 1, "name": "Acme"},
            {"id": 2, "name": "Beta Org"},
        ],
        synced_at="2026-03-19T01:00:00Z",
    )
    upsert_users(
        db,
        [
            {"id": 11, "account_id": 1, "FullName": "Alice User"},
            {"id": 12, "account_id": 2, "FullName": "Bob User"},
        ],
        synced_at="2026-03-19T01:00:00Z",
    )
    upsert_technicians(
        db,
        [
            {"id": 21, "FullName": "Tech One"},
            {"id": 22, "FullName": "Tech Two"},
        ],
        synced_at="2026-03-19T01:00:00Z",
    )
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
                "creation_category_name": "Email",
                "created_time": "2026-03-18T01:00:00Z",
                "updated_time": "2026-03-19T03:00:00Z",
            },
            {
                "id": 102,
                "account_id": 2,
                "user_id": 12,
                "tech_id": 22,
                "subject": "Issue B",
                "status": "Closed",
                "priority_name": "Low",
                "creation_category_name": "Printer",
                "created_time": "2026-03-17T01:00:00Z",
                "updated_time": "2026-03-19T04:00:00Z",
                "closed_time": "2026-03-19T04:00:00Z",
            },
        ],
        synced_at="2026-03-19T01:00:00Z",
    )
    upsert_ticket_details(
        db,
        [
            {
                "id": 101,
                "ticketlogs": [
                    {
                        "id": "log-101",
                        "log_type": "Comment",
                        "record_date": "2026-03-19T02:00:00Z",
                        "note": "Investigating mail flow.",
                        "plain_note": "Investigating mail flow.",
                        "user_firstname": "Tech",
                        "user_lastname": "One",
                    }
                ],
                "timelogs": [],
                "attachments": [
                    {"id": "a1", "name": "shot.png", "url": "https://example/shot.png", "size": 1234, "date": "2026-03-18T01:00:00Z"}
                ],
            }
        ],
        synced_at="2026-03-19T01:00:00Z",
    )
    materialize_ticket_documents(db)


def test_generate_public_snapshot(monkeypatch, tmp_path: Path) -> None:
    monkeypatch.setenv("SHERPAMIND_WORKSPACE_ROOT", str(tmp_path))
    db = tmp_path / ".SherpaMind" / "private" / "data" / "sherpamind.sqlite3"
    seed_fixture(db)
    result = generate_public_snapshot(db)
    assert result["status"] == "ok"
    assert result["account_docs_generated"] == 2
    assert result["technician_docs_generated"] == 2
    assert result["ticket_docs_generated"] == 1

    output = Path(result["output_path"])
    text = output.read_text()
    assert "SherpaMind Public Insight Snapshot" in text
    assert "Enrichment coverage" in text
    assert "Enrichment pressure — under-covered accounts" in text
    assert "Enrichment pressure — under-covered categories" in text
    assert "Enrichment pressure — under-covered technicians" in text
    assert "Sync freshness" in text
    assert "Attachment metadata summary" in text
    assert "Retrieval metadata readiness" in text
    assert "Account artifact coverage" in text
    assert "Technician artifact coverage" in text
    assert "Ticket artifact coverage" in text
    assert ".SherpaMind/private/data/sherpamind.sqlite3" in text

    retrieval_doc = tmp_path / ".SherpaMind" / "public" / "docs" / "retrieval-readiness.md"
    account_index = tmp_path / ".SherpaMind" / "public" / "docs" / "accounts" / "index.md"
    technician_index = tmp_path / ".SherpaMind" / "public" / "docs" / "technicians" / "index.md"
    ticket_index = tmp_path / ".SherpaMind" / "public" / "docs" / "tickets" / "index.md"
    acme_doc = tmp_path / ".SherpaMind" / "public" / "docs" / "accounts" / "Acme.md"
    beta_doc = tmp_path / ".SherpaMind" / "public" / "docs" / "accounts" / "Beta_Org.md"
    tech_one_doc = tmp_path / ".SherpaMind" / "public" / "docs" / "technicians" / "Tech_One.md"
    tech_two_doc = tmp_path / ".SherpaMind" / "public" / "docs" / "technicians" / "Tech_Two.md"
    ticket_101_doc = tmp_path / ".SherpaMind" / "public" / "docs" / "tickets" / "ticket_101.md"

    assert retrieval_doc.exists()
    assert account_index.exists()
    assert technician_index.exists()
    assert ticket_index.exists()
    assert acme_doc.exists()
    assert beta_doc.exists()
    assert tech_one_doc.exists()
    assert tech_two_doc.exists()
    assert ticket_101_doc.exists()

    retrieval_text = retrieval_doc.read_text()
    assert "SherpaMind Retrieval Readiness" in retrieval_text
    assert "Materialization lag summary" in retrieval_text
    assert "Materialization lag by ticket status" in retrieval_text
    assert "Materialization lag buckets" in retrieval_text
    assert "Top lagging documents" in retrieval_text
    assert "Missing vector chunk samples" in retrieval_text
    assert "Documents with missing vector chunks" in retrieval_text
    assert "Outdated vector chunk samples" in retrieval_text
    assert "Documents with outdated vector chunks" in retrieval_text
    assert "Dangling vector index samples" in retrieval_text
    assert "Lowest chunk-level metadata coverage" in retrieval_text
    assert "Follow-up cue source coverage" in retrieval_text
    assert "Action cue source coverage" in retrieval_text
    assert "Source-backed metadata promotion gaps" in retrieval_text
    assert "Source-backed metadata invalid-source hygiene" in retrieval_text
    assert "Entity label quality" in retrieval_text
    assert "Retrieval signal pressure — under-covered accounts" in retrieval_text
    assert "Retrieval signal pressure — under-covered categories" in retrieval_text
    assert "Retrieval signal pressure — under-covered technicians" in retrieval_text

    assert "Total account docs: `2`" in account_index.read_text()
    assert "Total technician docs: `2`" in technician_index.read_text()
    assert "Total ticket docs: `1`" in ticket_index.read_text()
    assert "Retrieval health" in acme_doc.read_text()
    assert "Retrieval lag buckets" in acme_doc.read_text()
    assert "Retrieval metadata coverage" in acme_doc.read_text()
    assert "Category breakdown" in tech_one_doc.read_text()
    assert "Retrieval health" in tech_one_doc.read_text()
    ticket_text = ticket_101_doc.read_text()
    assert "Artifact stats" in ticket_text
    assert "Retrieval health" in ticket_text
    assert "Chunk section inventory" in ticket_text
    assert "Recent logs" in ticket_text

    assert result["stale_account_docs_removed"] == 0
    assert result["stale_technician_docs_removed"] == 0
    assert result["stale_ticket_docs_removed"] == 0
    assert result["removed_files"] == []

    assert len(result["generated_files"]) >= 10
    for generated in result["generated_files"]:
        assert Path(generated).exists()


def test_source_materialization_gap_rows_use_document_gap_fields() -> None:
    rows = _source_materialization_gap_rows(
        {
            "support_group_name": {
                "status": "partial_materialization",
                "source_documents": 8,
                "materialized_documents": 5,
                "promotion_gap_documents": 3,
                "materialized_document_ratio": 0.625,
            },
            "default_contract_name": {
                "status": "missing_materialization",
                "source_documents": 4,
                "materialized_documents": 0,
                "promotion_gap_documents": 4,
                "materialized_document_ratio": 0.0,
            },
            "ticket_number": {
                "status": "materialized",
                "source_documents": 10,
                "materialized_documents": 10,
                "promotion_gap_documents": 0,
                "materialized_document_ratio": 1.0,
            },
        }
    )

    assert rows == [
        {
            "field": "default_contract_name",
            "status": "missing_materialization",
            "source_documents": 4,
            "materialized_documents": 0,
            "promotion_gap": 4,
            "materialized_ratio": "0.0%",
        },
        {
            "field": "support_group_name",
            "status": "partial_materialization",
            "source_documents": 8,
            "materialized_documents": 5,
            "promotion_gap": 3,
            "materialized_ratio": "62.5%",
        },
    ]


def test_invalid_source_rows_surface_source_hygiene_summary() -> None:
    rows = _invalid_source_rows(
        {
            "fields_with_invalid_source": [
                {
                    "field": "user_email_domain",
                    "raw_ticket_rows": 5,
                    "raw_detail_rows": 2,
                    "invalid_ticket_rows": 3,
                    "invalid_detail_rows": 1,
                    "source_documents": 4,
                },
                {
                    "field": "technician_email_domain",
                    "raw_ticket_rows": 2,
                    "raw_detail_rows": 0,
                    "invalid_ticket_rows": 1,
                    "invalid_detail_rows": 0,
                    "source_documents": 1,
                },
            ]
        }
    )

    assert rows == [
        {
            "field": "user_email_domain",
            "raw_ticket_rows": 5,
            "raw_detail_rows": 2,
            "invalid_ticket_rows": 3,
            "invalid_detail_rows": 1,
            "source_documents": 4,
        },
        {
            "field": "technician_email_domain",
            "raw_ticket_rows": 2,
            "raw_detail_rows": 0,
            "invalid_ticket_rows": 1,
            "invalid_detail_rows": 0,
            "source_documents": 1,
        },
    ]


def test_generate_public_snapshot_removes_stale_entity_docs(monkeypatch, tmp_path: Path) -> None:
    monkeypatch.setenv("SHERPAMIND_WORKSPACE_ROOT", str(tmp_path))
    db = tmp_path / ".SherpaMind" / "private" / "data" / "sherpamind.sqlite3"
    seed_fixture(db)

    account_dir = tmp_path / ".SherpaMind" / "public" / "docs" / "accounts"
    technician_dir = tmp_path / ".SherpaMind" / "public" / "docs" / "technicians"
    ticket_dir = tmp_path / ".SherpaMind" / "public" / "docs" / "tickets"
    account_dir.mkdir(parents=True, exist_ok=True)
    technician_dir.mkdir(parents=True, exist_ok=True)
    ticket_dir.mkdir(parents=True, exist_ok=True)

    stale_account = account_dir / "99999.md"
    stale_technician = technician_dir / "Legacy_Tech.md"
    stale_ticket = ticket_dir / "ticket_99999.md"
    account_index = account_dir / "index.md"
    technician_index = technician_dir / "index.md"
    ticket_index = ticket_dir / "index.md"

    stale_account.write_text("stale account doc\n")
    stale_technician.write_text("stale technician doc\n")
    stale_ticket.write_text("stale ticket doc\n")
    account_index.write_text("old account index\n")
    technician_index.write_text("old technician index\n")
    ticket_index.write_text("old ticket index\n")

    result = generate_public_snapshot(db)

    assert result["stale_account_docs_removed"] == 1
    assert result["stale_technician_docs_removed"] == 1
    assert result["stale_ticket_docs_removed"] == 1
    assert str(stale_account) in result["removed_files"]
    assert str(stale_technician) in result["removed_files"]
    assert str(stale_ticket) in result["removed_files"]
    assert not stale_account.exists()
    assert not stale_technician.exists()
    assert not stale_ticket.exists()
    assert account_index.exists()
    assert technician_index.exists()
    assert ticket_index.exists()
