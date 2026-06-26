"""Smoke tests for the memory package (Phase 1 port)."""

from __future__ import annotations

import datetime
import json
import os
import sqlite3
import tempfile
import unittest

from memory.types import (
    Chunk, Metadata, SourceKind, SourceRef, chunk_id, approx_token_count,
)
from memory.store import MemoryStore, ListChunksQuery, SearchChunksQuery
from memory.chunker import ChunkerInput, ChunkerOptions, chunk_markdown
from memory.ingest import ingest_markdown


class TestTypes(unittest.TestCase):
    def test_source_kind_roundtrip(self):
        assert SourceKind.parse("chat") == SourceKind.CHAT
        assert SourceKind.CHAT.as_str() == "chat"

    def test_chunk_id_deterministic(self):
        a = chunk_id(SourceKind.CHAT, "chan-1", 0, "hello world")
        b = chunk_id(SourceKind.CHAT, "chan-1", 0, "hello world")
        assert a == b
        assert len(a) == 32  # first 32 hex chars

    def test_chunk_id_differs_on_seq(self):
        a = chunk_id(SourceKind.CHAT, "chan-1", 0, "hello")
        b = chunk_id(SourceKind.CHAT, "chan-1", 1, "hello")
        assert a != b

    def test_chunk_id_differs_on_content(self):
        a = chunk_id(SourceKind.CHAT, "chan-1", 0, "hello")
        b = chunk_id(SourceKind.CHAT, "chan-1", 0, "world")
        assert a != b

    def test_chunk_id_differs_on_kind(self):
        a = chunk_id(SourceKind.CHAT, "chan-1", 0, "hello")
        b = chunk_id(SourceKind.EMAIL, "chan-1", 0, "hello")
        assert a != b

    def test_approx_token_count(self):
        # 1 token ≈ 4 chars
        assert approx_token_count("a" * 40) == 10
        assert approx_token_count("") == 1  # minimum 1


class TestStoreSchema(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.NamedTemporaryFile(suffix=".db", delete=False)
        self.tmp.close()
        self.store = MemoryStore(self.tmp.name)
        self.store.open()

    def tearDown(self):
        self.store.close()
        os.unlink(self.tmp.name)

    def test_all_tables_exist(self):
        expected = {
            "mem_tree_chunks",
            "mem_tree_score",
            "mem_tree_entity_index",
            "mem_tree_trees",
            "mem_tree_summaries",
            "mem_tree_buffers",
            "mem_tree_entity_hotness",
            "mem_tree_jobs",
            "mem_tree_ingested_sources",
        }
        conn = sqlite3.connect(self.tmp.name)
        cursor = conn.execute(
            "SELECT name FROM sqlite_master WHERE type='table'"
        )
        tables = {row[0] for row in cursor.fetchall()}
        conn.close()
        for t in expected:
            assert t in tables, f"Table {t} not found in {tables}"

    def test_upsert_and_get_chunk(self):
        ts = datetime.datetime(2026, 5, 17, tzinfo=datetime.timezone.utc)
        meta = Metadata.point_in_time(SourceKind.CHAT, "chan-1", "user1", ts)
        c = Chunk(
            id=chunk_id(SourceKind.CHAT, "chan-1", 0, "hello"),
            content="hello",
            metadata=meta,
            token_count=approx_token_count("hello"),
            seq_in_source=0,
            created_at=ts,
        )
        n = self.store.upsert_chunks([c])
        assert n == 1
        got = self.store.get_chunk(c.id)
        assert got is not None
        assert got.id == c.id
        assert got.content == "hello"
        assert got.metadata.source_kind == SourceKind.CHAT

    def test_upsert_idempotent(self):
        ts = datetime.datetime(2026, 5, 17, tzinfo=datetime.timezone.utc)
        meta = Metadata.point_in_time(SourceKind.CHAT, "chan-1", "user1", ts)
        c = Chunk(
            id=chunk_id(SourceKind.CHAT, "chan-1", 0, "hello"),
            content="hello",
            metadata=meta,
            token_count=1,
            seq_in_source=0,
            created_at=ts,
        )
        self.store.upsert_chunks([c])
        self.store.upsert_chunks([c])  # second upsert same id
        assert self.store.count_chunks() == 1

    def test_list_chunks(self):
        ts = datetime.datetime(2026, 5, 17, tzinfo=datetime.timezone.utc)
        meta = Metadata.point_in_time(SourceKind.CHAT, "chan-1", "user1", ts)
        chunk = Chunk(
            id=chunk_id(SourceKind.CHAT, "chan-1", 0, "hello"),
            content="hello",
            metadata=meta,
            token_count=1,
            seq_in_source=0,
            created_at=ts,
        )
        self.store.upsert_chunks([chunk])
        results = self.store.list_chunks(ListChunksQuery(limit=10))
        assert len(results) == 1

    def test_search_chunks_uses_fts_or_fallback(self):
        ts = datetime.datetime(2026, 5, 17, tzinfo=datetime.timezone.utc)
        meta = Metadata.point_in_time(SourceKind.DOCUMENT, "doc-search", "user1", ts)
        chunk = Chunk(
            id=chunk_id(SourceKind.DOCUMENT, "doc-search", 0, "Phoenix migration runbook"),
            content="Phoenix migration runbook",
            metadata=meta,
            token_count=3,
            seq_in_source=0,
            created_at=ts,
        )
        self.store.upsert_chunks([chunk])
        results = self.store.search_chunks(SearchChunksQuery(query="Phoenix", limit=5))
        assert len(results) == 1
        assert results[0][0].id == chunk.id

    def test_source_dedup(self):
        assert not self.store.is_source_ingested(SourceKind.CHAT, "chan-1")
        assert self.store.claim_source_ingest(SourceKind.CHAT, "chan-1", 5)
        assert self.store.is_source_ingested(SourceKind.CHAT, "chan-1")
        assert not self.store.claim_source_ingest(SourceKind.CHAT, "chan-1")

    def test_score_roundtrip(self):
        ts = datetime.datetime(2026, 5, 17, tzinfo=datetime.timezone.utc)
        meta = Metadata.point_in_time(SourceKind.CHAT, "chan-1", "user1", ts)
        cid = chunk_id(SourceKind.CHAT, "chan-1", 0, "score test")
        chunk = Chunk(id=cid, content="score test", metadata=meta, token_count=1, seq_in_source=0, created_at=ts)
        self.store.upsert_chunks([chunk])

        now_ms = int(ts.timestamp() * 1000)
        score = MemoryStore.ScoreRow(chunk_id=cid, total=0.85, computed_at_ms=now_ms)
        self.store.upsert_scores([score])
        got = self.store.get_score(cid)
        assert got is not None
        assert got.total == 0.85

    def test_job_enqueue_and_claim(self):
        job_id = self.store.enqueue_job(MemoryStore.JobRow(
            kind="test_job", payload_json='{"a":1}',
        ))
        assert job_id > 0
        assert self.store.count_jobs(status="pending") == 1
        claimed = self.store.claim_next_job()
        assert claimed is not None
        assert claimed["kind"] == "test_job"
        assert self.store.count_jobs(status="pending") == 0
        assert self.store.count_jobs(status="running") == 1

        self.store.complete_job(claimed["id"])
        assert self.store.count_jobs(status="running") == 0
        assert self.store.count_jobs(status="completed") == 1

    def test_job_claim_is_atomic_across_store_instances(self):
        job_id = self.store.enqueue_job(MemoryStore.JobRow(
            kind="test_job", payload_json='{"a":1}',
        ))
        assert job_id > 0

        other = MemoryStore(self.tmp.name)
        try:
            first = other.claim_next_job()
            second = self.store.claim_next_job()
        finally:
            other.close()

        assert first is not None
        assert first["id"] == job_id
        assert second is None
        assert self.store.count_jobs(status="running") == 1

    def test_job_dedupe_key_suppresses_active_duplicates(self):
        first = self.store.enqueue_job(MemoryStore.JobRow(
            kind="extract_chunk", payload_json='{"a":1}', dedupe_key="extract:abc",
        ))
        second = self.store.enqueue_job(MemoryStore.JobRow(
            kind="extract_chunk", payload_json='{"a":1}', dedupe_key="extract:abc",
        ))
        assert first > 0
        assert second == 0
        assert self.store.count_jobs(status="pending") == 1

    def test_job_failure_retries_then_fails(self):
        job_id = self.store.enqueue_job(MemoryStore.JobRow(
            kind="test_job", payload_json="{}", max_retries=0,
        ))
        claimed = self.store.claim_next_job()
        assert claimed is not None
        self.store.fail_job(claimed["id"], "boom", retry_delay_ms=0)
        got = self.store.get_job(job_id)
        assert got is not None
        assert got["status"] == "failed"
        assert "boom" in got["error"]

    def test_chunk_lifecycle(self):
        ts = datetime.datetime(2026, 5, 17, tzinfo=datetime.timezone.utc)
        meta = Metadata.point_in_time(SourceKind.CHAT, "chan-1", "user1", ts)
        cid = chunk_id(SourceKind.CHAT, "chan-1", 0, "lifecycle")
        chunk = Chunk(id=cid, content="lifecycle", metadata=meta, token_count=1, seq_in_source=0, created_at=ts)
        self.store.upsert_chunks([chunk])

        self.store.set_chunk_lifecycle(cid, "buffered")
        assert self.store.get_chunk_lifecycle(cid) == "buffered"

    def test_entity_index_upsert_dedupes_node(self):
        row = MemoryStore.EntityIndexRow(
            entity_id="pattern-key:test",
            node_id="chunk-1",
            node_kind="chunk",
            entity_kind="pattern_key",
            surface="test",
            score=1.0,
            timestamp_ms=1,
        )
        self.store.upsert_entity_index([row, row])
        rows = self.store.query_entity_index("pattern-key:test")
        assert len(rows) == 1


class TestChunker(unittest.TestCase):
    def test_single_short_document(self):
        ts = datetime.datetime(2026, 5, 17, tzinfo=datetime.timezone.utc)
        meta = Metadata.point_in_time(SourceKind.DOCUMENT, "doc-1", "user1", ts)
        inp = ChunkerInput(
            source_kind=SourceKind.DOCUMENT,
            source_id="doc-1",
            markdown="Short doc",
            metadata=meta,
        )
        chunks = chunk_markdown(inp)
        assert len(chunks) == 1
        assert chunks[0].content == "Short doc"
        assert chunks[0].seq_in_source == 0
        assert len(chunks[0].id) == 32

    def test_chat_splits_at_boundaries(self):
        """Each message exceeds half of max_chars → they land in separate chunks."""
        ts = datetime.datetime(2026, 5, 17, tzinfo=datetime.timezone.utc)
        meta = Metadata.point_in_time(SourceKind.CHAT, "chan-1", "user1", ts)
        # 260 chars each > max_chars/2 (200) → greedy pack flushes between them
        inp = ChunkerInput(
            source_kind=SourceKind.CHAT,
            source_id="chan-1",
            markdown="## User 1\n" + ("x" * 250) + "\n## User 2\n" + ("y" * 250),
            metadata=meta,
        )
        chunks = chunk_markdown(inp, ChunkerOptions(max_tokens=100))
        assert len(chunks) == 2, f"expected 2, got {len(chunks)}"
        assert "User 1" in chunks[0].content
        assert "User 2" in chunks[1].content

    def test_chat_packs_small_messages(self):
        """Small messages within max_tokens are greedily packed into one chunk."""
        ts = datetime.datetime(2026, 5, 17, tzinfo=datetime.timezone.utc)
        meta = Metadata.point_in_time(SourceKind.CHAT, "chan-1", "user1", ts)
        inp = ChunkerInput(
            source_kind=SourceKind.CHAT,
            source_id="chan-1",
            markdown="## A\nhello\n## B\nworld",
            metadata=meta,
        )
        chunks = chunk_markdown(inp, ChunkerOptions(max_tokens=100))
        assert len(chunks) == 1
        assert "hello" in chunks[0].content
        assert "world" in chunks[0].content

    def test_empty_input(self):
        ts = datetime.datetime(2026, 5, 17, tzinfo=datetime.timezone.utc)
        meta = Metadata.point_in_time(SourceKind.DOCUMENT, "doc-1", "user1", ts)
        inp = ChunkerInput(
            source_kind=SourceKind.DOCUMENT,
            source_id="doc-1",
            markdown="",
            metadata=meta,
        )
        chunks = chunk_markdown(inp)
        assert len(chunks) == 1
        assert chunks[0].content == ""


class TestIngest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.NamedTemporaryFile(suffix=".db", delete=False)
        self.tmp.close()
        self.store = MemoryStore(self.tmp.name)
        self.store.open()

    def tearDown(self):
        self.store.close()
        os.unlink(self.tmp.name)

    def test_ingest_basic(self):
        ts = datetime.datetime(2026, 5, 17, tzinfo=datetime.timezone.utc)
        meta = Metadata.point_in_time(SourceKind.DOCUMENT, "doc-1", "user1", ts)
        result = ingest_markdown(
            self.store,
            SourceKind.DOCUMENT,
            "doc-1",
            "# Test\n\nHello world memory.",
            meta,
        )
        assert result.chunks_written >= 1
        assert len(result.chunk_ids) >= 1
        assert not result.already_ingested

    def test_ingest_dedup(self):
        ts = datetime.datetime(2026, 5, 17, tzinfo=datetime.timezone.utc)
        meta = Metadata.point_in_time(SourceKind.DOCUMENT, "doc-dup", "user1", ts)
        r1 = ingest_markdown(self.store, SourceKind.DOCUMENT, "doc-dup", "content", meta)
        r2 = ingest_markdown(self.store, SourceKind.DOCUMENT, "doc-dup", "content", meta)
        assert r1.chunks_written >= 1
        assert r2.already_ingested

    def test_ingest_roundtrip_via_list(self):
        ts = datetime.datetime(2026, 5, 17, tzinfo=datetime.timezone.utc)
        meta = Metadata.point_in_time(SourceKind.CHAT, "chan-ingest", "user1", ts)
        # 2 small doc sources → 2 chunks (one per source), then list back
        r1 = ingest_markdown(self.store, SourceKind.DOCUMENT, "doc-a", "hello world", meta)
        r2 = ingest_markdown(self.store, SourceKind.DOCUMENT, "doc-b", "memory test", meta)
        assert r1.chunks_written == 1
        assert r2.chunks_written == 1
        chunks = self.store.list_chunks(ListChunksQuery(limit=10))
        assert len(chunks) == 2


if __name__ == "__main__":
    unittest.main()
