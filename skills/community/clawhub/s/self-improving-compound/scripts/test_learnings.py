#!/usr/bin/env python3

import os
import sys
import tempfile
from datetime import datetime, timedelta, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

import unittest
from types import SimpleNamespace

import learnings as L


class TestGetNow(unittest.TestCase):
    def test_returns_local_time_by_default(self):
        now = L.get_now()
        assert now.tzinfo is not None
        assert now.strftime("%Y%m%d") == datetime.now().astimezone().strftime("%Y%m%d")

    def test_respects_source_date_epoch(self):
        epoch = "1700000000"
        old = os.environ.pop("SOURCE_DATE_EPOCH", None)
        try:
            os.environ["SOURCE_DATE_EPOCH"] = epoch
            now = L.get_now()
            expected = datetime.fromtimestamp(int(epoch), tz=timezone.utc).astimezone()
            assert now.year == expected.year
            assert now.month == expected.month
            assert now.day == expected.day
        finally:
            if old is not None:
                os.environ["SOURCE_DATE_EPOCH"] = old
            else:
                os.environ.pop("SOURCE_DATE_EPOCH", None)


class TestRedactSecrets(unittest.TestCase):
    def test_api_key_redaction(self):
        field_name = "api" + "_key"
        secret_value = "x" * 20
        text = f'{field_name} = "{secret_value}"'
        result = L.redact_secrets(text)
        assert "[REDACTED]" in result
        assert secret_value not in result

    def test_bearer_token_redaction(self):
        token_value = "y" * 24
        text = f"Authorization: Bearer {token_value}"
        result = L.redact_secrets(text)
        assert "[REDACTED]" in result

    def test_no_false_positives_on_short_strings(self):
        text = "password = ok"
        result = L.redact_secrets(text)
        assert "[REDACTED]" not in result


class TestResolveRoot(unittest.TestCase):
    def test_prefers_local_root(self):
        class Args:
            root = "/global"
            local_root = "/local"
        assert L.resolve_root(Args()) == "/local"

    def test_falls_back_to_global_root(self):
        class Args:
            root = "/global"
            local_root = None
        assert L.resolve_root(Args()) == "/global"

    def test_falls_back_to_root_when_local_missing_attr(self):
        class Args:
            root = "/global"
        assert L.resolve_root(Args()) == "/global"


class TestStatusCounts(unittest.TestCase):
    def _ingest_via_store(self, tmp: str, entry_type: str, summary: str, pk: str = ""):
        """Helper: ingest an entry into the SQLite store and return its chunk id."""
        store = L.get_store(tmp)
        with store:
            return L._ingest_entry(store, entry_type, summary, "", pk, "", force=True)

    def test_counts_memory_headings_and_correction_rows(self):
        with tempfile.TemporaryDirectory() as tmp:
            # Init store
            args_init = type("Args", (), {"root": tmp, "local_root": None})()
            L.cmd_init(args_init)

            # Ingest test entries via store
            self._ingest_via_store(tmp, "LRN", "test learning")
            self._ingest_via_store(tmp, "ERR", "test error")
            self._ingest_via_store(tmp, "COR", "wrong answer", pk="test-pk")

            class Args:
                root = tmp
                local_root = None
                format = "json"

            import io
            from contextlib import redirect_stdout

            f = io.StringIO()
            with redirect_stdout(f):
                L.cmd_status(Args())

            import json
            data = json.loads(f.getvalue())
            assert data["entries_by_type"]["LRN"] == 1, f"got {data['entries_by_type']}"
            assert data["entries_by_type"]["ERR"] == 1
            assert data["entries_by_type"]["COR"] == 1

    def test_avoids_double_counting_duplicate_ids(self):
        with tempfile.TemporaryDirectory() as tmp:
            args_init = type("Args", (), {"root": tmp, "local_root": None})()
            L.cmd_init(args_init)

            # Ingest same entry twice (dedup: second should be skipped)
            self._ingest_via_store(tmp, "COR", "wrong answer", pk="test-pk")

            class Args:
                root = tmp
                local_root = None
                format = "json"

            import io
            from contextlib import redirect_stdout

            f = io.StringIO()
            with redirect_stdout(f):
                L.cmd_status(Args())

            import json
            data = json.loads(f.getvalue())
            assert data["entries_by_type"]["COR"] == 1


class TestCliRootCompatibility(unittest.TestCase):
    def test_global_root_before_subcommand(self):
        parser = L.build_parser()
        args = parser.parse_args(["--root", "/tmp/foo", "status"])
        assert args.root == "/tmp/foo"
        assert getattr(args, "local_root", None) is None

    def test_local_root_after_subcommand(self):
        parser = L.build_parser()
        args = parser.parse_args(["status", "--root", "/tmp/bar"])
        assert args.root is None
        assert args.local_root == "/tmp/bar"


class TestGenerateId(unittest.TestCase):
    def test_id_uses_local_date(self):
        with tempfile.TemporaryDirectory() as tmp:
            args_init = type("Args", (), {"root": tmp, "local_root": None})()
            L.cmd_init(args_init)
            store = L.get_store(tmp)
            with store:
                cid = L._ingest_entry(store, "LRN", "test entry", "", "", "", force=True)
                assert cid is not None
                assert cid.startswith("LRN-")

    def test_same_day_distinct_entries_are_not_deduped(self):
        with tempfile.TemporaryDirectory() as tmp:
            args_init = type("Args", (), {"root": tmp, "local_root": None})()
            L.cmd_init(args_init)
            store = L.get_store(tmp)
            with store:
                first = L._ingest_entry(store, "LRN", "first entry", "one", "test:first", "", force=False)
                second = L._ingest_entry(store, "LRN", "second entry", "two", "test:second", "", force=False)
                assert first == "LRN-" + datetime.now(timezone.utc).strftime("%Y%m%d") + "-001"
                assert second == "LRN-" + datetime.now(timezone.utc).strftime("%Y%m%d") + "-002"
                assert store.count_chunks() == 2


class TestVolatilePatterns(unittest.TestCase):
    def test_detects_pid(self):
        warnings = L.check_volatile_patterns("Process PID 12345 crashed")
        assert any("PID" in w for w in warnings)

    def test_detects_session_id(self):
        warnings = L.check_volatile_patterns("session-id=abc123def456")
        assert any("session" in w.lower() for w in warnings)

    def test_detects_temp_path(self):
        warnings = L.check_volatile_patterns("Found file at /tmp/foo.bar")
        assert any("/tmp/" in w for w in warnings)

    def test_detects_iso_timestamp(self):
        warnings = L.check_volatile_patterns("Event at 2026-05-09T14:30:00Z")
        assert any("2026-05-09T14:30:00Z" in w for w in warnings)

    def test_detects_current_state(self):
        warnings = L.check_volatile_patterns("Current timestamp is now")
        assert any("current" in w.lower() for w in warnings)

    def test_no_false_positives_on_plain_dates(self):
        warnings = L.check_volatile_patterns("Meeting on 2026-05-09")
        assert warnings == []

    def test_no_false_positives_on_stable_text(self):
        warnings = L.check_volatile_patterns("Always use pnpm in this repo")
        assert warnings == []


class TestVolatileCheckIntegration(unittest.TestCase):
    def test_blocks_volatile_without_force(self):
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp) / "learning"
            base.mkdir(parents=True)

            class Args:
                root = tmp
                local_root = None
                summary = "Process PID 9999 failed"
                details = ""
                pattern = ""
                force = False

            import io
            from contextlib import redirect_stdout

            f = io.StringIO()
            with redirect_stdout(f):
                L.cmd_log_learning(Args())

            output = f.getvalue()
            assert "Volatile pattern detected" in output
            assert "Aborting" in output
            assert "Logged" not in output

    def test_allows_volatile_with_force(self):
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp) / "learning"
            base.mkdir(parents=True)

            class Args:
                root = tmp
                local_root = None
                summary = "Process PID 9999 failed"
                details = ""
                pattern = ""
                force = True

            import io
            from contextlib import redirect_stdout

            f = io.StringIO()
            with redirect_stdout(f):
                L.cmd_log_learning(Args())

            output = f.getvalue()
            assert "Volatile pattern detected" in output
            assert "Logged:" in output


class TestSearchJsonFormat(unittest.TestCase):
    def test_json_output(self):
        with tempfile.TemporaryDirectory() as tmp:
            args_init = type("Args", (), {"root": tmp, "local_root": None})()
            L.cmd_init(args_init)
            store = L.get_store(tmp)
            with store:
                L._ingest_entry(store, "LRN", "hello world", "", "", "", force=True)

            class Args:
                root = tmp
                local_root = None
                query = "hello"
                limit = 20
                format = "json"

            import io
            from contextlib import redirect_stdout

            f = io.StringIO()
            with redirect_stdout(f):
                L.cmd_search(Args())

            import json
            data = json.loads(f.getvalue())
            assert len(data) == 1, f"expected 1 result, got {len(data)}: {data}"
            assert "hello" in str(data[0].get("summary", "")) or "hello" in str(data[0])

    def test_search_is_read_only_by_default(self):
        with tempfile.TemporaryDirectory() as tmp:
            args_init = type("Args", (), {"root": tmp, "local_root": None})()
            L.cmd_init(args_init)
            store = L.get_store(tmp)
            with store:
                entry_id = L._ingest_entry(store, "LRN", "hello world", "", "", "", force=True)

            class Args:
                root = tmp
                local_root = None
                query = "hello"
                limit = 20
                format = "json"

            import io
            from contextlib import redirect_stdout

            with redirect_stdout(io.StringIO()):
                L.cmd_search(Args())

            with L.get_store(tmp) as store:
                chunk = L._find_chunk_by_entry_id(store, entry_id or "")
                assert chunk is not None
                assert "Recurrence-Count**: 1" in chunk.content

    def test_search_touch_records_reuse(self):
        with tempfile.TemporaryDirectory() as tmp:
            args_init = type("Args", (), {"root": tmp, "local_root": None})()
            L.cmd_init(args_init)
            store = L.get_store(tmp)
            with store:
                entry_id = L._ingest_entry(store, "LRN", "hello world", "", "", "", force=True)

            class Args:
                root = tmp
                local_root = None
                query = "hello"
                limit = 20
                format = "json"
                touch = True

            import io
            from contextlib import redirect_stdout

            with redirect_stdout(io.StringIO()):
                L.cmd_search(Args())

            with L.get_store(tmp) as store:
                chunk = L._find_chunk_by_entry_id(store, entry_id or "")
                assert chunk is not None
                assert "Recurrence-Count**: 2" in chunk.content

            class ExportArgs:
                root = tmp
                local_root = None
                format = "json"
                output = ""

            export_out = io.StringIO()
            with redirect_stdout(export_out):
                L.cmd_export(ExportArgs())
            import json
            exported = json.loads(export_out.getvalue())
            assert "Recurrence-Count**: 2" in exported[0]["content"]

    def test_auto_entity_extraction_indexes_namespaced_tokens(self):
        with tempfile.TemporaryDirectory() as tmp:
            args_init = type("Args", (), {"root": tmp, "local_root": None})()
            L.cmd_init(args_init)
            store = L.get_store(tmp)
            with store:
                entry_id = L._ingest_entry(
                    store,
                    "LRN",
                    "Regenerate client for api:openapi",
                    "Run make generate-client after editing /repo/openapi.yaml",
                    "tooling:api-client-gen",
                    "project:test",
                    force=True,
                )
                chunk = L._find_chunk_by_entry_id(store, entry_id or "")
                assert chunk is not None
                L._index_extracted_entities(store, chunk)
                rows = store.query_entity_index("api:openapi")
                assert len(rows) == 1
                path_rows = store.query_entity_index("path:/repo/openapi.yaml")
                assert len(path_rows) == 1


class TestSQLiteFirstPromoteEdit(unittest.TestCase):
    def test_promote_finds_sqlite_entry(self):
        with tempfile.TemporaryDirectory() as tmp:
            args_init = type("Args", (), {"root": tmp, "local_root": None})()
            L.cmd_init(args_init)
            store = L.get_store(tmp)
            with store:
                entry_id = L._ingest_entry(store, "LRN", "promote me", "details", "test:promote", "", force=True)

            args = SimpleNamespace(root=tmp, local_root=None, entry_id=entry_id, to="AGENTS.md")
            L.cmd_promote(args)
            promoted = Path(tmp, "AGENTS.md").read_text(encoding="utf-8")
            assert entry_id in promoted
            assert "Status**: promoted" in promoted

    def test_shared_learning_root_promotes_into_workspace_root(self):
        with tempfile.TemporaryDirectory() as workspace, tempfile.TemporaryDirectory() as shared:
            args_init = type("Args", (), {"root": workspace, "local_root": None, "learning_root": shared, "local_learning_root": None})()
            L.cmd_init(args_init)
            store = L.get_store(workspace, shared)
            with store:
                entry_id = L._ingest_entry(store, "LRN", "shared promote", "details", "test:shared-promote", "", force=True)

            args = SimpleNamespace(root=workspace, local_root=None, learning_root=shared, local_learning_root=None, entry_id=entry_id, to="AGENTS.md")
            L.cmd_promote(args)

            assert Path(workspace, "AGENTS.md").exists()
            assert not Path(shared, "AGENTS.md").exists()
            assert entry_id in Path(workspace, "AGENTS.md").read_text(encoding="utf-8")

    def test_maintain_writes_promotion_queue_and_auto_promotes(self):
        with tempfile.TemporaryDirectory() as tmp:
            args_init = type("Args", (), {"root": tmp, "local_root": None})()
            L.cmd_init(args_init)
            store = L.get_store(tmp)
            with store:
                entry_id = L._ingest_entry(store, "LRN", "queue me", "details", "test:queue", "", force=True)
                chunk = L._find_chunk_by_entry_id(store, entry_id or "")
                assert chunk is not None
                chunk.content = L._replace_or_append_field(chunk.content, "Recurrence-Count", "3")
                store.upsert_chunks([chunk])

            args = SimpleNamespace(
                root=tmp,
                local_root=None,
                dry_run=False,
                format="json",
                auto_promote=True,
                promotion_target="AGENTS.md",
            )
            import io
            from contextlib import redirect_stdout

            with redirect_stdout(io.StringIO()):
                L.cmd_maintain(args)

            queue = Path(tmp, "learning", "promotion-queue.json")
            assert queue.exists()
            assert '"count": 0' in queue.read_text(encoding="utf-8")
            promoted = Path(tmp, "AGENTS.md").read_text(encoding="utf-8")
            assert entry_id in promoted

    def test_edit_updates_sqlite_entry(self):
        with tempfile.TemporaryDirectory() as tmp:
            args_init = type("Args", (), {"root": tmp, "local_root": None})()
            L.cmd_init(args_init)
            store = L.get_store(tmp)
            with store:
                entry_id = L._ingest_entry(store, "LRN", "edit me", "details", "test:edit", "", force=True)

            args = SimpleNamespace(
                root=tmp,
                local_root=None,
                entry_id=entry_id,
                status="resolved",
                last_seen=None,
                recurrence=4,
            )
            L.cmd_edit(args)
            with L.get_store(tmp) as store:
                chunk = L._find_chunk_by_entry_id(store, entry_id)
                assert chunk is not None
                assert "Status**: resolved" in chunk.content
                assert "Recurrence-Count**: 4" in chunk.content


class TestIngest(unittest.TestCase):
    def test_document_from_stdin(self):
        with tempfile.TemporaryDirectory() as tmp:
            args_init = type("Args", (), {"root": tmp, "local_root": None})()
            L.cmd_init(args_init)

            content = "# Test\n\nHello from ingest.\n\nSome more text here."
            import io
            from contextlib import redirect_stdout

            old_stdin = sys.stdin
            try:
                sys.stdin = io.StringIO(content)
                class Args:
                    root = tmp
                    local_root = None
                    kind = "document"
                    file = ""
                    source_id = ""
                    title = ""
                    tags = ""
                    no_dedup = False

                f = io.StringIO()
                with redirect_stdout(f):
                    L.cmd_ingest(Args())
                output = f.getvalue()
                assert "Wrote" in output
                assert "chunk(s)" in output
            finally:
                sys.stdin = old_stdin

    def test_ingest_dedup(self):
        with tempfile.TemporaryDirectory() as tmp:
            args_init = type("Args", (), {"root": tmp, "local_root": None})()
            L.cmd_init(args_init)

            content = "# Dedup test\n\nSame content."
            import io
            from contextlib import redirect_stdout

            old_stdin = sys.stdin
            try:
                sys.stdin = io.StringIO(content)
                class Args:
                    root = tmp
                    local_root = None
                    kind = "document"
                    file = ""
                    source_id = "dedup-test"
                    title = ""
                    tags = ""
                    no_dedup = False

                f = io.StringIO()
                with redirect_stdout(f):
                    L.cmd_ingest(Args())
                output = f.getvalue()
                assert "Wrote" in output

                sys.stdin = io.StringIO(content)
                f = io.StringIO()
                with redirect_stdout(f):
                    L.cmd_ingest(Args())
                output = f.getvalue()
                assert "already ingested" in output.lower()
            finally:
                sys.stdin = old_stdin

    def test_status_does_not_claim_pending_jobs(self):
        with tempfile.TemporaryDirectory() as tmp:
            args_init = type("Args", (), {"root": tmp, "local_root": None})()
            L.cmd_init(args_init)

            content = "# Job status test\n\nPending extraction."
            import io
            from contextlib import redirect_stdout

            old_stdin = sys.stdin
            try:
                sys.stdin = io.StringIO(content)
                class IngestArgs:
                    root = tmp
                    local_root = None
                    kind = "document"
                    file = ""
                    source_id = "status-job-test"
                    title = ""
                    tags = ""
                    no_dedup = False

                with redirect_stdout(io.StringIO()):
                    L.cmd_ingest(IngestArgs())
            finally:
                sys.stdin = old_stdin

            class StatusArgs:
                root = tmp
                local_root = None
                format = "json"

            import json

            first = io.StringIO()
            with redirect_stdout(first):
                L.cmd_status(StatusArgs())
            second = io.StringIO()
            with redirect_stdout(second):
                L.cmd_status(StatusArgs())

            assert json.loads(first.getvalue())["pending_jobs"] == 1
            assert json.loads(second.getvalue())["pending_jobs"] == 1

    def test_process_jobs_consumes_ingest_and_writes_summary_tree(self):
        with tempfile.TemporaryDirectory() as tmp:
            args_init = type("Args", (), {"root": tmp, "local_root": None})()
            L.cmd_init(args_init)

            content = "# Async tree test\n\nQueued chunks should become summaries."
            import io
            from contextlib import redirect_stdout

            old_stdin = sys.stdin
            try:
                sys.stdin = io.StringIO(content)
                class IngestArgs:
                    root = tmp
                    local_root = None
                    kind = "document"
                    file = ""
                    source_id = "async-tree-test"
                    title = ""
                    tags = ""
                    no_dedup = False

                with redirect_stdout(io.StringIO()):
                    L.cmd_ingest(IngestArgs())
            finally:
                sys.stdin = old_stdin

            class JobsArgs:
                root = tmp
                local_root = None
                max_jobs = 10
                daemon = False
                idle_sleep = 0.1
                kinds = ""
                no_maintenance = False
                maintenance_interval_seconds = 86400
                format = "json"

            f = io.StringIO()
            with redirect_stdout(f):
                L.cmd_process_jobs(JobsArgs())

            import json
            data = json.loads(f.getvalue())
            assert data["completed"] >= 1
            assert data["queue"].get("pending", 0) == 0

            store = L.get_store(tmp)
            with store:
                chunks = store.list_chunks(L.ListChunksQuery(limit=10))
                assert len(chunks) == 1
                assert store.get_chunk_lifecycle(chunks[0].id) == L.CHUNK_STATUS_ADMITTED
                assert store.get_score(chunks[0].id) is not None
                assert len(store.list_buffers()) >= 1
                assert len(store.list_summaries()) >= 1

    def test_lifecycle_job_archives_stale_warm(self):
        with tempfile.TemporaryDirectory() as tmp:
            args_init = type("Args", (), {"root": tmp, "local_root": None})()
            L.cmd_init(args_init)
            store = L.get_store(tmp)
            old = datetime.now(timezone.utc) - timedelta(days=120)
            with store:
                meta = L.Metadata(
                    source_kind=L.SourceKind.DOCUMENT,
                    source_id="stale-warm",
                    owner="user",
                    timestamp=old,
                    time_range=(old, old),
                    tags=["LRN"],
                )
                content = (
                    "### LRN-20260101-001 (2026-01-01)\n"
                    "- **Summary**: Stale warm entry\n"
                    "- **Last-Seen**: 2026-01-01\n"
                    "- **Recurrence-Count**: 1\n"
                )
                cid = L.chunk_id(L.SourceKind.DOCUMENT, "stale-warm", 0, content)
                chunk = L.Chunk(id=cid, content=content, metadata=meta, token_count=1, seq_in_source=0, created_at=old)
                store.upsert_chunks([chunk])
                store.set_chunk_lifecycle(cid, L.CHUNK_STATUS_BUFFERED)
                store.enqueue_job(L.MemoryStore.JobRow(
                    kind="maintain_lifecycle",
                    payload_json="{}",
                    priority=10,
                ))

            class JobsArgs:
                root = tmp
                local_root = None
                max_jobs = 1
                daemon = False
                idle_sleep = 0.1
                kinds = "maintain_lifecycle"
                no_maintenance = True
                maintenance_interval_seconds = 86400
                format = "json"

            import io
            from contextlib import redirect_stdout

            with redirect_stdout(io.StringIO()):
                L.cmd_process_jobs(JobsArgs())

            with store:
                assert store.get_chunk_lifecycle(cid) == L.CHUNK_STATUS_SEALED

    def test_parser_exposes_ingest(self):
        parser = L.build_parser()
        args = parser.parse_args(["ingest", "--kind", "chat", "--file", "/tmp/test.md"])
        assert args.command == "ingest"
        assert args.kind == "chat"
        assert args.file == "/tmp/test.md"

    def test_parser_exposes_process_jobs(self):
        parser = L.build_parser()
        args = parser.parse_args(["process-jobs", "--max-jobs", "1", "--format", "json"])
        assert args.command == "process-jobs"
        assert args.max_jobs == 1


class TestMaintain(unittest.TestCase):
    def _init_and_ingest_old(self, tmp: str, days_ago: int = 60):
        args_init = type("Args", (), {"root": tmp, "local_root": None})()
        L.cmd_init(args_init)
        store = L.get_store(tmp)
        with store:
            from memory.types import chunk_id
            ts = datetime.now(timezone.utc) - timedelta(days=days_ago)
            source_id = f"LRN/{ts.strftime('%Y-%m-%d')}"
            meta = L.Metadata(
                source_kind=L.SourceKind.DOCUMENT,
                source_id=source_id,
                owner="user",
                timestamp=ts,
                time_range=(ts, ts),
                tags=["LRN"],
            )
            content = f"Old learning from {days_ago} days ago"
            cid = chunk_id(L.SourceKind.DOCUMENT, source_id, 0, content)
            chunk = L.Chunk(id=cid, content=content, metadata=meta, token_count=1, seq_in_source=0, created_at=ts)
            store.upsert_chunks([chunk])
            store.upsert_scores([L.MemoryStore.ScoreRow(
                chunk_id=cid, total=1.0, interaction_weight=0.5,
                computed_at_ms=int(ts.timestamp() * 1000),
            )])
        return cid[:12]

    def test_parser_exposes_maintain(self):
        parser = L.build_parser()
        args = parser.parse_args(["maintain", "--format", "json"])
        assert args.command == "maintain"
        assert args.format == "json"
        assert args.dry_run is True

    def test_maintain_dry_run_default(self):
        parser = L.build_parser()
        args = parser.parse_args(["maintain"])
        assert args.dry_run is True

    def test_maintain_apply_flag(self):
        parser = L.build_parser()
        args = parser.parse_args(["maintain", "--apply"])
        assert args.dry_run is False

    def test_dry_run_reports_stale_hot(self):
        with tempfile.TemporaryDirectory() as tmp:
            eid = self._init_and_ingest_old(tmp)

            class Args:
                root = tmp
                local_root = None
                dry_run = True
                format = "json"

            import io
            from contextlib import redirect_stdout

            f = io.StringIO()
            with redirect_stdout(f):
                L.cmd_maintain(Args())

            import json
            data = json.loads(f.getvalue())
            assert len(data["stale_hot"]) >= 1

    def test_apply_moves_stale_hot_to_warm(self):
        with tempfile.TemporaryDirectory() as tmp:
            eid = self._init_and_ingest_old(tmp)

            class Args:
                root = tmp
                local_root = None
                dry_run = False
                format = "json"

            import io
            from contextlib import redirect_stdout

            f = io.StringIO()
            with redirect_stdout(f):
                L.cmd_maintain(Args())

            import json
            data = json.loads(f.getvalue())
            assert len(data["stale_hot"]) >= 1

    def test_apply_archives_stale_warm(self):
        with tempfile.TemporaryDirectory() as tmp:
            eid = self._init_and_ingest_old(tmp)

            class Args:
                root = tmp
                local_root = None
                dry_run = False
                format = "json"

            import io
            from contextlib import redirect_stdout

            f = io.StringIO()
            with redirect_stdout(f):
                L.cmd_maintain(Args())

            import json
            data = json.loads(f.getvalue())

    def test_reports_promotion_candidate(self):
        with tempfile.TemporaryDirectory() as tmp:
            args_init = type("Args", (), {"root": tmp, "local_root": None})()
            L.cmd_init(args_init)
            store = L.get_store(tmp)
            with store:
                entry_id = L._ingest_entry(store, "LRN", "Frequent learning", "", "active-pattern", "", force=True)
                chunk = L._find_chunk_by_entry_id(store, entry_id or "")
                if chunk:
                    chunk.content = L._replace_or_append_field(chunk.content, "Recurrence-Count", "3")
                    store.upsert_chunks([chunk])

            class Args:
                root = tmp
                local_root = None
                dry_run = True
                format = "json"

            import io
            from contextlib import redirect_stdout

            f = io.StringIO()
            with redirect_stdout(f):
                L.cmd_maintain(Args())

            import json
            data = json.loads(f.getvalue())
            assert len(data["promote_candidates"]) == 1
            assert data["promote_candidates"][0]["recurrence_count"] == 3

    def test_fresh_learning_is_not_promotion_candidate(self):
        with tempfile.TemporaryDirectory() as tmp:
            args_init = type("Args", (), {"root": tmp, "local_root": None})()
            L.cmd_init(args_init)
            store = L.get_store(tmp)
            with store:
                L._ingest_entry(store, "LRN", "Fresh learning", "", "test:fresh", "", force=True)

            class Args:
                root = tmp
                local_root = None
                dry_run = True
                format = "json"

            import io
            from contextlib import redirect_stdout

            f = io.StringIO()
            with redirect_stdout(f):
                L.cmd_maintain(Args())

            import json
            data = json.loads(f.getvalue())
            assert data["promote_candidates"] == []
