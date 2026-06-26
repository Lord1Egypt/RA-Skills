"""
chunk_retriever.py - 分段检索器
从数据库中检索 chunk，支持向量检索 + 上下文展开 + 精准回溯
"""

from __future__ import annotations

import logging
from dataclasses import dataclass, field
from typing import List, Optional

logger = logging.getLogger(__name__)


@dataclass
class ChunkHit:
    memory_id: str
    chunk_id: str
    doc_id: str
    content: str
    chapter: str = ""
    section: str = ""
    page_num: int = 0
    position: int = 0
    score: float = 0.0
    is_cold: bool = False


@dataclass
class ChunkSearchResult:
    query: str
    hits: List[ChunkHit]
    total_hits: int = 0
    context_expanded: bool = False
    strategy: str = ""


class ChunkRetriever:

    def __init__(self, store, embedding_store=None):
        self.store = store
        self.embedding_store = embedding_store

    def search(
        self,
        query: str,
        top_k: int = 5,
        expand_context: int = 1,
        doc_id: str = None,
        strategy: str = "auto",
    ) -> ChunkSearchResult:
        if strategy == "auto":
            if self.embedding_store:
                hits = self._search_hybrid(query, top_k, doc_id)
                strategy_used = "hybrid"
            else:
                hits = self._search_keyword(query, top_k, doc_id)
                strategy_used = "keyword"
        elif strategy == "vector":
            hits = self._search_vector(query, top_k, doc_id)
            strategy_used = "vector"
        elif strategy == "keyword":
            hits = self._search_keyword(query, top_k, doc_id)
            strategy_used = "keyword"
        elif strategy == "hybrid":
            hits = self._search_hybrid(query, top_k, doc_id)
            strategy_used = "hybrid"
        else:
            hits = self._search_keyword(query, top_k, doc_id)
            strategy_used = "keyword"

        context_expanded = False
        if expand_context > 0 and hits:
            expanded_hits = []
            seen_ids = set()
            for hit in hits:
                if hit.memory_id not in seen_ids:
                    expanded_hits.append(hit)
                    seen_ids.add(hit.memory_id)
                context = self.expand_context(hit, before=expand_context, after=expand_context)
                for ctx_hit in context:
                    if ctx_hit.memory_id not in seen_ids:
                        expanded_hits.append(ctx_hit)
                        seen_ids.add(ctx_hit.memory_id)
            expanded_hits.sort(key=lambda h: (h.doc_id, h.position))
            hits = expanded_hits
            context_expanded = True

        return ChunkSearchResult(
            query=query,
            hits=hits,
            total_hits=len(hits),
            context_expanded=context_expanded,
            strategy=strategy_used,
        )

    def _search_vector(
        self, query: str, top_k: int, doc_id: str = None
    ) -> list[ChunkHit]:
        if not self.embedding_store:
            return []
        try:
            results = self.embedding_store.search(query, top_k=top_k * 2)
            hits = []
            for item in results:
                memory_id = item.get("memory_id", "")
                score = item.get("score", 0.0)
                if not memory_id:
                    continue
                chunk_meta = self._get_chunk_by_memory_id(memory_id)
                if not chunk_meta:
                    continue
                if doc_id and chunk_meta.get("doc_id") != doc_id:
                    continue
                mem = self.store.get_memory(memory_id)
                if not mem:
                    continue
                hits.append(
                    ChunkHit(
                        memory_id=memory_id,
                        chunk_id=chunk_meta.get("chunk_id", ""),
                        doc_id=chunk_meta.get("doc_id", ""),
                        content=mem.get("content", ""),
                        chapter=chunk_meta.get("chapter", ""),
                        section=chunk_meta.get("section", ""),
                        page_num=chunk_meta.get("page_num", 0) or 0,
                        position=chunk_meta.get("position", 0) or 0,
                        score=score,
                        is_cold=mem.get("is_cold", False),
                    )
                )
            return hits[:top_k]
        except Exception as e:
            logger.debug("chunk_retriever: vector search: %s", e)
            return []

    def _search_keyword(
        self, query: str, top_k: int, doc_id: str = None
    ) -> list[ChunkHit]:
        try:
            mem_results = self.store.query(keyword=query, limit=top_k * 2)
            hits = []
            for mem in mem_results:
                memory_id = mem.get("memory_id", "")
                if not memory_id:
                    continue
                chunk_meta = self._get_chunk_by_memory_id(memory_id)
                if not chunk_meta:
                    continue
                if doc_id and chunk_meta.get("doc_id") != doc_id:
                    continue
                hits.append(
                    ChunkHit(
                        memory_id=memory_id,
                        chunk_id=chunk_meta.get("chunk_id", ""),
                        doc_id=chunk_meta.get("doc_id", ""),
                        content=mem.get("content", ""),
                        chapter=chunk_meta.get("chapter", ""),
                        section=chunk_meta.get("section", ""),
                        page_num=chunk_meta.get("page_num", 0) or 0,
                        position=chunk_meta.get("position", 0) or 0,
                        score=0.5,
                        is_cold=mem.get("is_cold", False),
                    )
                )
            return hits[:top_k]
        except Exception as e:
            logger.debug("chunk_retriever: keyword search: %s", e)
            return []

    def _search_hybrid(
        self, query: str, top_k: int, doc_id: str = None
    ) -> list[ChunkHit]:
        vec_hits = self._search_vector(query, top_k, doc_id)
        kw_hits = self._search_keyword(query, top_k, doc_id)
        return self._rrf_merge(vec_hits, kw_hits)[:top_k]

    def expand_context(
        self, hit: ChunkHit, before: int = 1, after: int = 1
    ) -> list[ChunkHit]:
        result = []
        current_meta = self._get_chunk_by_memory_id(hit.memory_id)
        if not current_meta:
            return result

        prev_id = current_meta.get("prev_chunk_id", "")
        for _ in range(before):
            if not prev_id:
                break
            prev_hit = self._get_chunk_hit_by_chunk_id(prev_id)
            if prev_hit:
                result.insert(0, prev_hit)
                prev_meta = self._get_chunk_by_memory_id(prev_hit.memory_id)
                prev_id = prev_meta.get("prev_chunk_id", "") if prev_meta else ""
            else:
                break

        next_id = current_meta.get("next_chunk_id", "")
        for _ in range(after):
            if not next_id:
                break
            next_hit = self._get_chunk_hit_by_chunk_id(next_id)
            if next_hit:
                result.append(next_hit)
                next_meta = self._get_chunk_by_memory_id(next_hit.memory_id)
                next_id = next_meta.get("next_chunk_id", "") if next_meta else ""
            else:
                break

        return result

    def get_document_chunks(self, doc_id: str) -> list[ChunkHit]:
        try:
            rows = self.store.conn.execute(
                """SELECT cm.chunk_id, cm.memory_id, cm.doc_id, cm.chapter, cm.section,
                          cm.page_num, cm.position
                   FROM chunk_meta cm
                   WHERE cm.doc_id = ?
                   ORDER BY cm.position ASC""",
                (doc_id,),
            ).fetchall()

            hits = []
            for row in rows:
                mem = self.store.get_memory(row["memory_id"])
                hits.append(
                    ChunkHit(
                        memory_id=row["memory_id"],
                        chunk_id=row["chunk_id"],
                        doc_id=row["doc_id"],
                        content=mem.get("content", "") if mem else "",
                        chapter=row["chapter"] or "",
                        section=row["section"] or "",
                        page_num=row["page_num"] or 0,
                        position=row["position"] or 0,
                        is_cold=mem.get("is_cold", False) if mem else False,
                    )
                )
            return hits
        except Exception as e:
            logger.debug("chunk_retriever: get_document_chunks: %s", e)
            return []

    def locate_source(self, memory_id: str) -> dict:
        chunk_meta = self._get_chunk_by_memory_id(memory_id)
        if not chunk_meta:
            return {"found": False, "memory_id": memory_id}

        doc_id = chunk_meta.get("doc_id", "")
        doc_meta = self._get_document_meta(doc_id)

        return {
            "found": True,
            "memory_id": memory_id,
            "chunk_id": chunk_meta.get("chunk_id", ""),
            "doc_id": doc_id,
            "chapter": chunk_meta.get("chapter", ""),
            "section": chunk_meta.get("section", ""),
            "page_num": chunk_meta.get("page_num", 0),
            "position": chunk_meta.get("position", 0),
            "char_offset": chunk_meta.get("char_offset", 0),
            "char_length": chunk_meta.get("char_length", 0),
            "document": doc_meta,
        }

    def _get_chunk_by_memory_id(self, memory_id: str) -> Optional[dict]:
        try:
            row = self.store.conn.execute(
                "SELECT * FROM chunk_meta WHERE memory_id = ?", (memory_id,)
            ).fetchone()
            return dict(row) if row else None
        except Exception:
            return None

    def _get_chunk_hit_by_chunk_id(self, chunk_id: str) -> Optional[ChunkHit]:
        try:
            row = self.store.conn.execute(
                "SELECT * FROM chunk_meta WHERE chunk_id = ?", (chunk_id,)
            ).fetchone()
            if not row:
                return None
            meta = dict(row)
            mem = self.store.get_memory(meta.get("memory_id", ""))
            return ChunkHit(
                memory_id=meta.get("memory_id", ""),
                chunk_id=meta.get("chunk_id", ""),
                doc_id=meta.get("doc_id", ""),
                content=mem.get("content", "") if mem else "",
                chapter=meta.get("chapter", ""),
                section=meta.get("section", ""),
                page_num=meta.get("page_num", 0) or 0,
                position=meta.get("position", 0) or 0,
                is_cold=mem.get("is_cold", False) if mem else False,
            )
        except Exception:
            return None

    def _get_document_meta(self, doc_id: str) -> Optional[dict]:
        try:
            row = self.store.conn.execute(
                "SELECT * FROM document_meta WHERE doc_id = ?", (doc_id,)
            ).fetchone()
            return dict(row) if row else None
        except Exception:
            return None

    @staticmethod
    def _rrf_merge(
        vec_hits: list[ChunkHit], kw_hits: list[ChunkHit], k: int = 60
    ) -> list[ChunkHit]:
        scores: dict[str, float] = {}
        hit_map: dict[str, ChunkHit] = {}

        for rank, hit in enumerate(vec_hits):
            scores[hit.memory_id] = scores.get(hit.memory_id, 0) + 1.0 / (k + rank + 1)
            hit_map[hit.memory_id] = hit

        for rank, hit in enumerate(kw_hits):
            scores[hit.memory_id] = scores.get(hit.memory_id, 0) + 1.0 / (k + rank + 1)
            if hit.memory_id not in hit_map:
                hit_map[hit.memory_id] = hit
            else:
                existing = hit_map[hit.memory_id]
                if hit.score > existing.score:
                    existing.score = hit.score

        sorted_ids = sorted(scores.items(), key=lambda x: -x[1])
        result = []
        for mid, score in sorted_ids:
            hit = hit_map[mid]
            hit.score = score
            result.append(hit)
        return result
