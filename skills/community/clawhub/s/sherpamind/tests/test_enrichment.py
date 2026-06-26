from pathlib import Path

from sherpamind.enrichment import _candidate_ticket_rows, enrich_priority_ticket_details
from sherpamind.settings import Settings
from sherpamind.db import connect, initialize_db, replace_ticket_documents, upsert_ticket_details, upsert_tickets


class FakeClient:
    def get(self, path, params=None):
        ticket_id = path.split('/')[-1]
        return {
            'id': int(ticket_id),
            'subject': f'Ticket {ticket_id}',
            'status': 'Open',
            'created_time': '2026-03-18T01:00:00Z',
            'updated_time': '2026-03-19T01:00:00Z',
            'ticketlogs': [{'id': int(ticket_id) * 10, 'log_type': 'Initial Post', 'plain_note': 'hello', 'record_date': '2026-03-18T01:00:00Z'}],
            'timelogs': [],
            'attachments': [],
        }


def make_settings(tmp_path: Path) -> Settings:
    return Settings(
        api_base_url='https://api.sherpadesk.com',
        api_key='secret',
        api_user=None,
        org_key='org',
        instance_key='inst',
        db_path=tmp_path / 'sherpamind.sqlite3',
        watch_state_path=tmp_path / 'watch_state.json',
        notify_channel=None,
        request_min_interval_seconds=0,
        request_timeout_seconds=30,
        seed_page_size=100,
        seed_max_pages=None,
        hot_open_pages=5,
        warm_closed_pages=10,
        warm_closed_days=7,
        cold_closed_pages_per_run=2,
    )


def test_enrich_priority_ticket_details_populates_detail_tables(tmp_path: Path, monkeypatch) -> None:
    settings = make_settings(tmp_path)
    initialize_db(settings.db_path)
    upsert_tickets(settings.db_path, [
        {'id': 101, 'subject': 'Open A', 'status': 'Open', 'created_time': '2026-03-19T01:00:00Z', 'updated_time': '2026-03-19T02:00:00Z'},
        {'id': 102, 'subject': 'Closed B', 'status': 'Closed', 'created_time': '2026-03-18T01:00:00Z', 'updated_time': '2026-03-19T01:00:00Z', 'closed_time': '2999-03-18T01:00:00Z'},
    ])
    monkeypatch.setattr('sherpamind.enrichment._build_client', lambda settings: FakeClient())
    result = enrich_priority_ticket_details(settings, limit=2, materialize_docs=True)
    assert result.status == 'ok'
    with connect(settings.db_path) as conn:
        detail_count = conn.execute('SELECT COUNT(*) AS c FROM ticket_details').fetchone()['c']
        log_count = conn.execute('SELECT COUNT(*) AS c FROM ticket_logs').fetchone()['c']
        doc_count = conn.execute('SELECT COUNT(*) AS c FROM ticket_documents').fetchone()['c']
    assert detail_count == 2
    assert log_count == 2
    assert doc_count >= 2


def test_enrichment_prioritizes_unenriched_open_tickets(tmp_path: Path, monkeypatch) -> None:
    settings = make_settings(tmp_path)
    initialize_db(settings.db_path)
    upsert_tickets(settings.db_path, [
        {'id': 101, 'subject': 'Open A', 'status': 'Open', 'priority_name': 'High', 'created_time': '2026-03-19T01:00:00Z', 'updated_time': '2026-03-19T02:00:00Z'},
        {'id': 102, 'subject': 'Open B', 'status': 'Open', 'priority_name': 'Normal', 'created_time': '2026-03-19T01:00:00Z', 'updated_time': '2026-03-19T01:30:00Z'},
    ])
    upsert_ticket_details(settings.db_path, [{'id': 101, 'ticketlogs': [], 'timelogs': [], 'attachments': []}])
    seen = []

    class RecordingClient(FakeClient):
        def get(self, path, params=None):
            seen.append(path)
            return super().get(path, params=params)

    monkeypatch.setattr('sherpamind.enrichment._build_client', lambda settings: RecordingClient())
    enrich_priority_ticket_details(settings, limit=1, materialize_docs=False)
    assert seen == ['tickets/102']


def test_candidate_selection_spreads_cold_coverage_to_undercovered_categories(tmp_path: Path) -> None:
    db = tmp_path / 'sherpamind.sqlite3'
    initialize_db(db)
    upsert_tickets(db, [
        {
            'id': 201,
            'subject': 'Covered category detail seed',
            'status': 'Closed',
            'priority_name': 'Normal',
            'class_name': 'Hardware / Printer',
            'account_id': 1,
            'tech_id': 11,
            'created_time': '2025-01-01T01:00:00Z',
            'updated_time': '2025-01-01T02:00:00Z',
            'closed_time': '2025-01-01T03:00:00Z',
        },
        {
            'id': 202,
            'subject': 'Same covered category',
            'status': 'Closed',
            'priority_name': 'High',
            'class_name': 'Hardware / Printer',
            'account_id': 1,
            'tech_id': 11,
            'created_time': '2025-01-02T01:00:00Z',
            'updated_time': '2025-01-02T02:00:00Z',
            'closed_time': '2025-01-02T03:00:00Z',
        },
        {
            'id': 203,
            'subject': 'Undercovered software ticket',
            'status': 'Closed',
            'priority_name': 'Normal',
            'class_name': 'Software / Line of Business',
            'account_id': 2,
            'tech_id': 12,
            'created_time': '2025-01-03T01:00:00Z',
            'updated_time': '2025-01-03T02:00:00Z',
            'closed_time': '2025-01-03T03:00:00Z',
        },
    ])
    upsert_ticket_details(db, [{'id': 201, 'ticketlogs': [], 'timelogs': [], 'attachments': []}])

    candidates = _candidate_ticket_rows(db, limit=1)
    assert [row['id'] for row in candidates] == ['203']


def test_candidate_selection_prefers_retrieval_poor_cold_groups_when_detail_coverage_ties(tmp_path: Path) -> None:
    db = tmp_path / 'sherpamind.sqlite3'
    initialize_db(db)
    upsert_tickets(db, [
        {
            'id': 301,
            'subject': 'Hardware ticket one',
            'status': 'Closed',
            'priority_name': 'Normal',
            'class_name': 'Hardware / Printer',
            'account_id': 1,
            'tech_id': 11,
            'created_time': '2025-01-01T01:00:00Z',
            'updated_time': '2025-01-01T02:00:00Z',
            'closed_time': '2025-01-01T03:00:00Z',
        },
        {
            'id': 302,
            'subject': 'Hardware ticket two',
            'status': 'Closed',
            'priority_name': 'Normal',
            'class_name': 'Hardware / Printer',
            'account_id': 1,
            'tech_id': 11,
            'created_time': '2025-01-02T01:00:00Z',
            'updated_time': '2025-01-02T02:00:00Z',
            'closed_time': '2025-01-02T03:00:00Z',
        },
        {
            'id': 303,
            'subject': 'Software ticket one',
            'status': 'Closed',
            'priority_name': 'Normal',
            'class_name': 'Software / LOB',
            'account_id': 2,
            'tech_id': 12,
            'created_time': '2025-01-03T01:00:00Z',
            'updated_time': '2025-01-03T02:00:00Z',
            'closed_time': '2025-01-03T03:00:00Z',
        },
        {
            'id': 304,
            'subject': 'Software ticket two',
            'status': 'Closed',
            'priority_name': 'Normal',
            'class_name': 'Software / LOB',
            'account_id': 2,
            'tech_id': 12,
            'created_time': '2025-01-04T01:00:00Z',
            'updated_time': '2025-01-04T02:00:00Z',
            'closed_time': '2025-01-04T03:00:00Z',
        },
    ])
    replace_ticket_documents(
        db,
        [
            {
                'doc_id': 'ticket:301',
                'ticket_id': 301,
                'status': 'Closed',
                'account': 'Acme Hardware',
                'user_name': 'User One',
                'technician': 'Tech One',
                'updated_at': '2025-01-01T02:00:00Z',
                'text': 'hardware ticket 301',
                'metadata': {
                    'category': 'Hardware / Printer',
                    'cleaned_initial_post': 'printer offline',
                    'cleaned_action_cue': 'reboot spooler',
                    'recent_log_types_csv': 'Initial Post, Response',
                    'resolution_summary': 'resolved after restart',
                    'attachments_count': 1,
                },
                'content_hash': 'doc-301',
            },
            {
                'doc_id': 'ticket:302',
                'ticket_id': 302,
                'status': 'Closed',
                'account': 'Acme Hardware',
                'user_name': 'User Two',
                'technician': 'Tech One',
                'updated_at': '2025-01-02T02:00:00Z',
                'text': 'hardware ticket 302',
                'metadata': {
                    'category': 'Hardware / Printer',
                    'cleaned_initial_post': 'printer queue jammed',
                    'cleaned_action_cue': 'clear queue',
                    'recent_log_types_csv': 'Initial Post, Response',
                    'resolution_summary': 'resolved after queue clear',
                    'attachments_count': 2,
                },
                'content_hash': 'doc-302',
            },
            {
                'doc_id': 'ticket:303',
                'ticket_id': 303,
                'status': 'Closed',
                'account': 'Beta Software',
                'user_name': 'User Three',
                'technician': 'Tech Two',
                'updated_at': '2025-01-03T02:00:00Z',
                'text': 'software ticket 303',
                'metadata': {
                    'category': 'Software / LOB',
                },
                'content_hash': 'doc-303',
            },
            {
                'doc_id': 'ticket:304',
                'ticket_id': 304,
                'status': 'Closed',
                'account': 'Beta Software',
                'user_name': 'User Four',
                'technician': 'Tech Two',
                'updated_at': '2025-01-04T02:00:00Z',
                'text': 'software ticket 304',
                'metadata': {
                    'category': 'Software / LOB',
                },
                'content_hash': 'doc-304',
            },
        ],
        synced_at='2025-01-05T01:00:00Z',
    )

    candidates = _candidate_ticket_rows(db, limit=1)
    assert [row['id'] for row in candidates] == ['304']
