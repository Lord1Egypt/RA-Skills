"""
chunk_indexer.py - 分段索引器
将 SemanticChunker 的输出写入数据库，包括：
- 为每个 chunk 生成独立的 memory_id
- 将 chunk 内容写入 memories 表
- 将 chunk 元数据写入 chunk_meta 表
- 将文档元数据写入 document_meta 表
- 为每个 chunk 生成向量 embedding
- 建立 chunk 间的 sequential 关联
"""

from __future__ import annotations

import hashlib
import logging
import time
import uuid
from dataclasses import dataclass, field
from typing import List, Optional

logger = logging.getLogger(__name__)


@dataclass
class IndexResult:
    doc_id: str
    total_chunks: int
    indexed_chunks: int
    failed_chunks: int
    total_vectors: int
    errors: List[str] = field(default_factory=list)


class ChunkIndexer:

    def __init__(self, store, encoder=None, embedding_store=None):
        self.store = store
        self.encoder = encoder
        self.embedding_store = embedding_store

    def index_document(
        self,
        chunk_result,
        title: str = "",
        source_path: str = "",
        source_type: str = "text",
        importance: str = "high",
        person_id: str = "P01",
        topics: list = None,
    ) -> IndexResult:
        if not chunk_result or not chunk_result.chunks:
            return IndexResult(
                doc_id="",
                total_chunks=0,
                indexed_chunks=0,
                failed_chunks=0,
                total_vectors=0,
                errors=["empty chunk_result"],
            )

        doc_id = self._generate_doc_id(title, source_path)
        total_chars = chunk_result.total_chars or sum(c.char_length for c in chunk_result.chunks)
        total_chunks = len(chunk_result.chunks)

        self._write_document_meta(
            doc_id, title, source_path, source_type, total_chunks, total_chars
        )

        indexed = 0
        failed = 0
        vectors = 0
        errors: list[str] = []
        chunks_with_ids: list[tuple] = []

        for chunk in chunk_result.chunks:
            try:
                memory_id = self._generate_chunk_memory_id(doc_id, chunk)
                content_hash = hashlib.sha256(chunk.content.encode("utf-8")).hexdigest()
                time_id = time.strftime("T%Y%m%d.%H%M%S")
                time_ts = int(time.time())

                topic_list = topics or ["doc.chunk"]

                self.store.insert_memory(
                    memory_id=memory_id,
                    time_id=time_id,
                    time_ts=time_ts,
                    person_id=person_id,
                    nature_id="D01",
                    content=chunk.content,
                    content_hash=content_hash,
                    topics=topic_list,
                    importance=importance,
                )

                self._write_chunk_meta(chunk.chunk_id, memory_id, doc_id, chunk)

                self._add_embedding(memory_id, chunk.content)
                if self.embedding_store:
                    vectors += 1

                chunks_with_ids.append((chunk, memory_id))
                indexed += 1

            except Exception as e:
                failed += 1
                err_msg = f"chunk {chunk.chunk_id}: {e}"
                errors.append(err_msg)
                logger.warning("chunk_indexer: %s", err_msg)

        if chunks_with_ids:
            self._write_sequential_links(chunks_with_ids)

        now = int(time.time())
        try:
            self.store.conn.execute(
                "UPDATE document_meta SET total_chunks = ?, updated_at = ? WHERE doc_id = ?",
                (indexed, now, doc_id),
            )
            self.store.conn.commit()
        except Exception as e:
            logger.debug("chunk_indexer: update doc_meta: %s", e)

        logger.info(
            "chunk_indexer: doc=%s indexed=%d failed=%d vectors=%d",
            doc_id, indexed, failed, vectors,
        )

        return IndexResult(
            doc_id=doc_id,
            total_chunks=total_chunks,
            indexed_chunks=indexed,
            failed_chunks=failed,
            total_vectors=vectors,
            errors=errors,
        )

    def _generate_doc_id(self, title: str, source_path: str) -> str:
        raw = f"{title}_{source_path}_{time.time()}"
        return "DOC_" + hashlib.md5(raw.encode()).hexdigest()[:12]

    def _generate_chunk_memory_id(self, doc_id: str, chunk, encoder=None) -> str:
        enc = encoder or self.encoder
        if enc:
            try:
                time_id = time.strftime("T%Y%m%d.%H%M%S")
                memory_id = enc.generate_memory_id(
                    time_id=time_id,
                    person_id="P01",
                    topic_codes=["doc.chunk"],
                    nature_id="D01",
                    tool_ids=[],
                )
                return memory_id
            except Exception:
                pass
        raw = f"{doc_id}_{chunk.position}_{chunk.char_offset}"
        suffix = uuid.uuid4().hex[:8]
        return f"T{time.strftime('%Y%m%d.%H%M%S')}_P01_doc.chunk_D01_{suffix}"

    def _write_document_meta(
        self,
        doc_id: str,
        title: str,
        source_path: str,
        source_type: str,
        total_chunks: int,
        total_chars: int,
    ):
        now = int(time.time())
        self.store.conn.execute(
            """INSERT OR REPLACE INTO document_meta
               (doc_id, title, source_path, source_type, total_chunks, total_chars, created_at, updated_at)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
            (doc_id, title, source_path, source_type, total_chunks, total_chars, now, now),
        )
        self.store.conn.commit()

    def _write_chunk_meta(self, chunk_id: str, memory_id: str, doc_id: str, chunk):
        self.store.conn.execute(
            """INSERT OR REPLACE INTO chunk_meta
               (chunk_id, memory_id, doc_id, chapter, section, page_num, position,
                prev_chunk_id, next_chunk_id, char_offset, char_length)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            (
                chunk_id,
                memory_id,
                doc_id,
                chunk.chapter,
                chunk.section,
                chunk.page_num,
                chunk.position,
                chunk.prev_chunk_id,
                chunk.next_chunk_id,
                chunk.char_offset,
                chunk.char_length,
            ),
        )
        self.store.conn.commit()

    def _write_sequential_links(self, chunks_with_ids: list):
        for i, (chunk, memory_id) in enumerate(chunks_with_ids):
            if i > 0:
                prev_mid = chunks_with_ids[i - 1][1]
                self.store.conn.execute(
                    """INSERT INTO memory_links (source_id, target_id, link_type, weight, reason)
                       VALUES (?, ?, 'sequential', 1.0, 'document_chunk_order')""",
                    (prev_mid, memory_id),
                )
        self.store.conn.commit()

    def _add_embedding(self, memory_id: str, content: str):
        if not self.embedding_store:
            return
        try:
            self.embedding_store.add(memory_id, content)
        except Exception as e:
            logger.debug("chunk_indexer: embedding failed for %s: %s", memory_id, e)
