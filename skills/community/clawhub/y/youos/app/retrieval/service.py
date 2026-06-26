from __future__ import annotations

import json
import logging
import re
import sqlite3
from contextlib import closing
from dataclasses import asdict, dataclass, field
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Literal

import yaml

from app.core.embeddings import cosine_similarity, deserialize_embedding, get_embedding, get_embedding_model_id
from app.core.sender import classify_sender, extract_domain
from app.db.bootstrap import connect, resolve_sqlite_path

ResultType = Literal["document", "chunk", "reply_pair"]
ScopeType = Literal["all", "documents", "reply_pairs"]
ModeHint = Literal["work", "personal", "unknown"]

_TOKEN_PATTERN = re.compile(r"[a-z0-9]{2,}")

_WORK_SIGNALS = re.compile(
    r"\b(proposal|integration|api|contract|client|invoice|pricing|budget|deadline|"
    r"deliverable|stakeholder|timeline|vendor|compliance|saas|enterprise|onboard|"
    r"quote|demo|meeting|schedule|call|partner|partnership|agreement|nda|sla|"
    r"implementation|deployment|credentials|credentials|technical|support|ticket|"
    r"report|status|update|project|team|colleague|manager|hr|legal|document|sign|"
    r"audit|review|payment|billing|subscription|license|renewal|account|lab|hospital|"
    r"clinic|healthcare|software|platform|solution|service|product|feature|bug|issue|"
    r"request|requirement|specification|scope|milestone|delivery|handover|onboarding)\b",
    re.IGNORECASE,
)
_PERSONAL_SIGNALS = re.compile(
    r"\b(friend|family|personal|vacation|birthday|weekend|dinner|"
    r"wedding|holiday|kids|parents|trip|thanks for checking in|"
    r"catch up|catchup|hang out|hangout|drinks|lunch|coffee|"
    r"sister|brother|mum|mom|dad|uncle|aunt|cousin|girlfriend|boyfriend|"
    r"wife|husband|home|house|apartment|moving|baby|pregnant|"
    r"sick|travel|flight|hotel|ages|old group|Saturday|Sunday)\b",
    re.IGNORECASE,
)

logger = logging.getLogger(__name__)

# Config constants (C3)
SEMANTIC_TOP_N: int = 20
MIN_SCORE_FILTER: float = 0.2
SEMANTIC_SCALE_FACTOR: float = 10.0


@dataclass(slots=True)
class RetrievalRequest:
    query: str
    scope: ScopeType = "all"
    source_types: tuple[str, ...] = ()
    account_emails: tuple[str, ...] = ()
    top_k_documents: int | None = None
    top_k_chunks: int | None = None
    top_k_reply_pairs: int | None = None
    sender_type_hint: str | None = None
    sender_domain_hint: str | None = None
    language_hint: str | None = None
    intent_hint: str | None = None
    intent_hint_2: str | None = None
    thread_id: str | None = None


@dataclass(slots=True)
class RetrievalMatch:
    result_type: ResultType
    score: float
    lexical_score: float
    metadata_score: float
    source_type: str
    source_id: str
    account_email: str | None
    title: str | None
    author: str | None
    external_uri: str | None
    thread_id: str | None
    created_at: str | None
    updated_at: str | None
    document_id: int | None = None
    chunk_id: int | None = None
    chunk_index: int | None = None
    reply_pair_id: int | None = None
    snippet: str | None = None
    content: str | None = None
    inbound_text: str | None = None
    reply_text: str | None = None
    subject: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(slots=True)
class RetrievalResponse:
    query: str
    retrieval_method: str
    semantic_search_enabled: bool
    applied_filters: dict[str, Any]
    detected_mode: ModeHint
    documents: list[RetrievalMatch]
    chunks: list[RetrievalMatch]
    reply_pairs: list[RetrievalMatch]
    partial_semantic_coverage: bool = False
    max_score: float | None = None
    mean_score: float | None = None
    score_stddev: float | None = None
    # True only when the cross-encoder actually ran (vs. silent fallback).
    # Distinct from `reranker_enabled` config: a misconfigured instance with
    # the flag on but no sentence-transformers installed gets False here,
    # and the retrieval_method label above stays honest.
    reranker_applied: bool = False

    def to_dict(self) -> dict[str, Any]:
        return {
            "query": self.query,
            "retrieval_method": self.retrieval_method,
            "semantic_search_enabled": self.semantic_search_enabled,
            "applied_filters": self.applied_filters,
            "detected_mode": self.detected_mode,
            "documents": [match.to_dict() for match in self.documents],
            "chunks": [match.to_dict() for match in self.chunks],
            "reply_pairs": [match.to_dict() for match in self.reply_pairs],
            "partial_semantic_coverage": self.partial_semantic_coverage,
            "reranker_applied": self.reranker_applied,
        }


@dataclass(slots=True)
class RetrievalConfig:
    top_k_documents: int
    top_k_chunks: int
    top_k_reply_pairs: int
    recency_boost_days: int
    recency_boost_weight: float
    account_boost_weight: float
    source_weights: dict[str, float]
    semantic_weight: float = 0.4
    semantic_min_coverage: float = 0.01
    sender_type_boost: float = 0.15
    sender_domain_boost: float = 0.10
    sender_type_boost_map: dict[str, float] = field(default_factory=dict)
    reranker_enabled: bool = False
    # Cross-encoder reranker knobs (only consulted when reranker_enabled).
    # ``reranker_model_id=None`` → use app.core.reranker.DEFAULT_RERANKER_MODEL_ID.
    # ``reranker_blend_weight=None`` → 0.6 (CE 60% / FTS 40%, the historical default).
    # ``reranker_ce_score_scale=None`` → 10.0 (scale CE [0,1] up to FTS-comparable range).
    reranker_model_id: str | None = None
    reranker_blend_weight: float | None = None
    reranker_ce_score_scale: float | None = None
    subject_match_boost: float = 0.2
    topic_match_boost: float = 0.15
    # BM25 lexical-score saturation knobs. Defaults match the historical
    # hardcoded `min(raw_rank * 2.0, 10.0)` so behaviour is unchanged when the
    # config is silent; the autoresearch loop can A/B alternative values
    # against the existing golden-eval gate.
    lexical_scale: float = 2.0
    lexical_cap: float = 10.0
    # Per-token field-match bonus (the multiplier inside `_field_match_bonus`).
    # Was hardcoded to 0.25 at module level; surfacing it lets the autoresearch
    # loop A/B how much extra credit a literal title/subject term-match should
    # earn over a pure BM25 ranking.
    field_match_bonus_per_token: float = 0.25


def _has_fts5_table(connection: sqlite3.Connection, table_name: str) -> bool:
    row = connection.execute("SELECT 1 FROM sqlite_master WHERE type='table' AND name=?", (table_name,)).fetchone()
    return row is not None


class RetrievalService:
    def __init__(self, *, db_path: Path, config: RetrievalConfig) -> None:
        self.db_path = db_path
        self.config = config

    @classmethod
    def from_database_url(cls, *, database_url: str, configs_dir: Path) -> RetrievalService:
        return cls(
            db_path=resolve_sqlite_path(database_url),
            config=_load_retrieval_config(configs_dir),
        )

    def retrieve(self, request: RetrievalRequest) -> RetrievalResponse:
        query = request.query.strip()
        if not query:
            raise ValueError("Retrieval query must not be empty.")

        # Expand query with synonyms for FTS (keep original for semantic)
        from app.core.query_expansion import expand_query

        fts_query_text = expand_query(query)

        tokens = _tokenize(fts_query_text)
        detected_mode = _detect_mode(query)
        filters = {
            "scope": request.scope,
            "source_types": list(request.source_types),
            "account_emails": list(request.account_emails),
        }

        with closing(connect(self.db_path)) as connection:
            connection.row_factory = sqlite3.Row
            use_fts = _has_fts5_table(connection, "chunks_fts")

            documents: list[RetrievalMatch] = []
            chunks: list[RetrievalMatch] = []
            reply_pairs: list[RetrievalMatch] = []

            if request.scope in ("all", "documents"):
                documents = self._retrieve_documents(connection, query=query, tokens=tokens, request=request)
                if use_fts:
                    chunks = self._retrieve_chunks_fts(connection, query=query, tokens=tokens, request=request)
                else:
                    chunks = self._retrieve_chunks_legacy(connection, query=query, tokens=tokens, request=request)

            if request.scope in ("all", "reply_pairs"):
                if use_fts:
                    reply_pairs = self._retrieve_reply_pairs_fts(connection, query=query, tokens=tokens, request=request)
                else:
                    reply_pairs = self._retrieve_reply_pairs_legacy(connection, query=query, tokens=tokens, request=request)

            # Hybrid semantic re-ranking
            semantic_enabled = False
            partial_coverage = False
            if reply_pairs:
                rp_semantic, rp_partial = self._apply_semantic_reranking(connection, query, reply_pairs, "reply_pairs")
                semantic_enabled = rp_semantic
                partial_coverage = rp_partial
            if chunks:
                ch_semantic, ch_partial = self._apply_semantic_reranking(connection, query, chunks, "chunks")
                semantic_enabled = semantic_enabled or ch_semantic
                partial_coverage = partial_coverage or ch_partial

            # Thread-based boosting
            if request.thread_id and reply_pairs:
                for match in reply_pairs:
                    if match.thread_id and match.thread_id == request.thread_id:
                        match.score = round(match.score * 2.0, 4)
                reply_pairs.sort(key=lambda m: (-m.score, m.result_type, m.source_id))

            # Topic-aware boosting
            if request.sender_domain_hint and reply_pairs and self.config.topic_match_boost > 0:
                sender_topics = _load_sender_topics(connection, request.sender_domain_hint)
                if sender_topics:
                    query_tokens = _tokenize(query)
                    for match in reply_pairs:
                        if match.metadata.get("inbound_author") or (match.author and request.sender_domain_hint in (match.author or "")):
                            if _check_topic_overlap(query_tokens, sender_topics):
                                match.score = round(match.score * (1.0 + self.config.topic_match_boost), 4)
                    reply_pairs.sort(key=lambda m: (-m.score, m.result_type, m.source_id))

            # Intent-based boosting
            if request.intent_hint and request.intent_hint != "general" and reply_pairs:
                from app.core.intent import classify_intent

                intent_targets = {request.intent_hint}
                if request.intent_hint_2 and request.intent_hint_2 != "general":
                    intent_targets.add(request.intent_hint_2)

                for match in reply_pairs:
                    if match.inbound_text:
                        # Check predicted_intent from metadata first, fall back to live classification
                        match_intent = match.metadata.get("predicted_intent") or classify_intent(match.inbound_text)
                        if match_intent in intent_targets:
                            boost = 1.2 if match_intent == request.intent_hint else 1.1
                            match.score = round(match.score * boost, 4)
                reply_pairs.sort(key=lambda m: (-m.score, m.result_type, m.source_id))

            # E14: language-filtered boosting — boost same-language pairs
            if request.language_hint and request.language_hint != "en" and reply_pairs:
                for match in reply_pairs:
                    match_lang = match.metadata.get("language")
                    if match_lang and match_lang == request.language_hint:
                        match.score = round(match.score * 1.3, 4)
                reply_pairs.sort(key=lambda m: (-m.score, m.result_type, m.source_id))

            # Optional cross-encoder reranking. Track whether the CE actually
            # fired (vs. silently fell back when the dep isn't installed or
            # the model fails to load) so the retrieval_method label below
            # reports honestly. Without this, a misconfigured instance with
            # `reranker_enabled: true` but no sentence-transformers installed
            # would claim `+reranker` in every trace and the user would never
            # know reranking wasn't happening.
            reranker_applied = False
            if self.config.reranker_enabled:
                from app.core.reranker import rerank

                rerank_kwargs = {
                    "model_id": self.config.reranker_model_id,
                    "blend_weight": self.config.reranker_blend_weight,
                    "ce_score_scale": self.config.reranker_ce_score_scale,
                }
                top_k_rp = request.top_k_reply_pairs or self.config.top_k_reply_pairs
                if len(reply_pairs) > top_k_rp:
                    reply_pairs, rp_applied = rerank(query, reply_pairs, top_k_rp, **rerank_kwargs)
                    reranker_applied = reranker_applied or rp_applied
                top_k_ch = request.top_k_chunks or self.config.top_k_chunks
                if len(chunks) > top_k_ch:
                    chunks, ch_applied = rerank(query, chunks, top_k_ch, **rerank_kwargs)
                    reranker_applied = reranker_applied or ch_applied

        method = "fts5_bm25" if use_fts else "lexical_v1"
        if semantic_enabled:
            method = f"{method}+semantic"
        if reranker_applied:
            method = f"{method}+reranker"

        # Compute score stats for reply_pairs
        max_score = None
        mean_score = None
        score_stddev = None
        if reply_pairs:
            scores = [rp.score for rp in reply_pairs]
            max_score = max(scores)
            mean_score = sum(scores) / len(scores)
            if len(scores) >= 2:
                variance = sum((s - mean_score) ** 2 for s in scores) / len(scores)
                score_stddev = variance**0.5
            else:
                score_stddev = 0.0

        return RetrievalResponse(
            query=query,
            retrieval_method=method,
            semantic_search_enabled=semantic_enabled,
            applied_filters=filters,
            detected_mode=detected_mode,
            documents=documents,
            chunks=chunks,
            reply_pairs=reply_pairs,
            partial_semantic_coverage=partial_coverage,
            max_score=max_score,
            mean_score=mean_score,
            score_stddev=score_stddev,
            reranker_applied=reranker_applied,
        )

    # -- Semantic reranking ────────────────────────────────────────────────

    def _apply_semantic_reranking(
        self,
        connection: sqlite3.Connection,
        query: str,
        matches: list[RetrievalMatch],
        table: str,
    ) -> tuple[bool, bool]:
        """Re-score matches using hybrid FTS + semantic similarity.

        Returns (semantic_enabled, partial_coverage) tuple.
        Only operates on top-20 FTS candidates for efficiency.
        """
        if not _has_embedding_column(connection, table):
            return False, False

        coverage = _embedding_coverage(connection, table)
        if coverage < self.config.semantic_min_coverage:
            return False, False

        partial_coverage = 0.01 <= coverage < 0.3

        # Get query embedding — if embedding generation fails, skip semantic
        try:
            query_emb = get_embedding(query)
        except Exception:
            logger.warning("Embedding generation failed for query, skipping semantic reranking", exc_info=True)
            return False, False

        id_field = "chunk_id" if table == "chunks" else "reply_pair_id"
        top_n = min(len(matches), SEMANTIC_TOP_N)
        fts_weight = 1.0 - self.config.semantic_weight
        sem_weight = self.config.semantic_weight

        # R2: Dynamic FTS score scale — use actual max FTS score to calibrate semantic scores
        fts_max = max((m.score for m in matches[:top_n]), default=SEMANTIC_SCALE_FACTOR)
        scale_factor = max(fts_max, 1.0)

        # Stale-embedding detection: if the configured embedding model differs
        # from the one a stored row was produced with, the cosine sim is
        # comparing vectors in different spaces — meaningless. Legacy rows
        # (embedding_model_id IS NULL) predate this column and are trusted as
        # matching the current model (no forced re-embed on upgrade).
        current_model_id = get_embedding_model_id()
        has_model_id_col = _has_column(connection, table, "embedding_model_id")
        select_cols = "embedding, embedding_model_id" if has_model_id_col else "embedding"

        for match in matches[:top_n]:
            row_id = getattr(match, id_field)
            if row_id is None:
                continue
            row = connection.execute(f"SELECT {select_cols} FROM {table} WHERE id = ?", (row_id,)).fetchone()  # noqa: S608
            if not row or not row["embedding"] or len(row["embedding"]) < 4:
                continue
            if has_model_id_col:
                stored_model_id = row["embedding_model_id"]
                if stored_model_id is not None and stored_model_id != current_model_id:
                    # Stale — different model, different embedding space.
                    continue
            emb = deserialize_embedding(row["embedding"])
            sim = cosine_similarity(query_emb, emb)
            # Normalize sim from [-1,1] to [0,1] range, then scale to match FTS score range
            sim_normalized = (sim + 1.0) / 2.0
            sim_score = sim_normalized * scale_factor
            match.score = round(fts_weight * match.score + sem_weight * sim_score, 4)

        # Re-sort after reranking
        matches.sort(key=lambda m: (-m.score, m.result_type, m.source_id))
        return True, partial_coverage

    # -- FTS5 paths ──────────────────────────────────────────────────────

    def _retrieve_chunks_fts(
        self,
        connection: sqlite3.Connection,
        *,
        query: str,
        tokens: list[str],
        request: RetrievalRequest,
    ) -> list[RetrievalMatch]:
        fts_query = _fts5_query(tokens)
        if not fts_query:
            return []
        rows = connection.execute(
            """
            SELECT
                c.id,
                c.chunk_index,
                c.content,
                c.metadata_json AS chunk_metadata_json,
                d.id AS document_id,
                d.source_type,
                d.source_id,
                d.title,
                d.author,
                d.external_uri,
                d.thread_id,
                d.created_at,
                d.updated_at,
                d.metadata_json AS document_metadata_json,
                cfts.rank AS fts_rank
            FROM chunks_fts AS cfts
            INNER JOIN chunks AS c ON c.id = cfts.rowid
            INNER JOIN documents AS d ON d.id = c.document_id
            WHERE chunks_fts MATCH ?
            ORDER BY cfts.rank
            LIMIT ?
            """,
            (fts_query, (request.top_k_chunks or self.config.top_k_chunks) * 3),
        ).fetchall()
        matches: list[RetrievalMatch] = []
        for row in rows:
            if not _matches_filters(
                source_type=row["source_type"],
                metadata_json=row["document_metadata_json"],
                source_types=request.source_types,
                account_emails=request.account_emails,
            ):
                continue
            match = self._score_chunk_row_fts(row, query=query, tokens=tokens, request=request)
            if match is not None:
                matches.append(match)
        return _top_matches(matches, request.top_k_chunks or self.config.top_k_chunks)

    def _retrieve_reply_pairs_fts(
        self,
        connection: sqlite3.Connection,
        *,
        query: str,
        tokens: list[str],
        request: RetrievalRequest,
    ) -> list[RetrievalMatch]:
        fts_query = _fts5_query(tokens)
        if not fts_query:
            return []
        rows = connection.execute(
            """
            SELECT
                rp.id,
                rp.source_type,
                rp.source_id,
                rp.thread_id,
                rp.inbound_text,
                rp.reply_text,
                rp.inbound_author,
                rp.reply_author,
                rp.paired_at,
                rp.metadata_json,
                d.id AS document_id,
                d.title,
                d.author,
                d.external_uri,
                d.created_at,
                d.updated_at,
                rpfts.rank AS fts_rank,
                COALESCE(rp.quality_score, 1.0) AS quality_score,
                rp.language
            FROM reply_pairs_fts AS rpfts
            INNER JOIN reply_pairs AS rp ON rp.id = rpfts.rowid
            LEFT JOIN documents AS d ON d.id = rp.document_id
            WHERE reply_pairs_fts MATCH ?
            ORDER BY rpfts.rank
            LIMIT ?
            """,
            (fts_query, (request.top_k_reply_pairs or self.config.top_k_reply_pairs) * 3),
        ).fetchall()
        matches: list[RetrievalMatch] = []
        for row in rows:
            if not _matches_filters(
                source_type=row["source_type"],
                metadata_json=row["metadata_json"],
                source_types=request.source_types,
                account_emails=request.account_emails,
            ):
                continue
            match = self._score_reply_pair_row_fts(row, query=query, tokens=tokens, request=request)
            if match is not None:
                matches.append(match)
        return _top_matches(matches, request.top_k_reply_pairs or self.config.top_k_reply_pairs)

    def _score_chunk_row_fts(
        self,
        row: sqlite3.Row,
        *,
        query: str,
        tokens: list[str],
        request: RetrievalRequest,
    ) -> RetrievalMatch | None:
        document_metadata = _loads_json(row["document_metadata_json"])
        chunk_metadata = _loads_json(row["chunk_metadata_json"])
        content = row["content"] or ""
        title = row["title"] or ""
        # FTS5 rank is negative (more negative = better match); normalize to positive
        raw_rank = abs(row["fts_rank"]) if row["fts_rank"] else 0.0
        lexical_score = (
            min(raw_rank * self.config.lexical_scale, self.config.lexical_cap)
            + _field_match_bonus(title, tokens, self.config.field_match_bonus_per_token)
        )
        metadata_score = self._metadata_score(
            source_type=row["source_type"],
            timestamp=row["updated_at"] or row["created_at"],
            account_email=_account_email_from_metadata(document_metadata),
            request_account_emails=request.account_emails,
        )
        metadata = dict(document_metadata)
        metadata["chunk"] = chunk_metadata
        return RetrievalMatch(
            result_type="chunk",
            score=round(lexical_score + metadata_score, 4),
            lexical_score=round(lexical_score, 4),
            metadata_score=round(metadata_score, 4),
            source_type=row["source_type"],
            source_id=row["source_id"],
            account_email=_account_email_from_metadata(document_metadata),
            title=row["title"],
            author=row["author"],
            external_uri=row["external_uri"],
            thread_id=row["thread_id"],
            created_at=row["created_at"],
            updated_at=row["updated_at"],
            document_id=row["document_id"],
            chunk_id=row["id"],
            chunk_index=row["chunk_index"],
            snippet=_make_snippet(content, tokens=tokens),
            content=content,
            metadata=metadata,
        )

    def _score_reply_pair_row_fts(
        self,
        row: sqlite3.Row,
        *,
        query: str,
        tokens: list[str],
        request: RetrievalRequest,
    ) -> RetrievalMatch | None:
        metadata = _loads_json(row["metadata_json"])
        # E14: include language in metadata for language-based boosting
        try:
            if row["language"]:
                metadata["language"] = row["language"]
        except (IndexError, KeyError):
            pass
        inbound_text = row["inbound_text"] or ""
        reply_text = row["reply_text"] or ""
        raw_rank = abs(row["fts_rank"]) if row["fts_rank"] else 0.0
        lexical_score = min(raw_rank * self.config.lexical_scale, self.config.lexical_cap)

        # Subject match boost
        pair_subject = metadata.get("subject", "")
        if pair_subject:
            lexical_score += _field_match_bonus(pair_subject, tokens, self.config.field_match_bonus_per_token) * 0.5

        metadata_score = self._metadata_score(
            source_type=row["source_type"],
            timestamp=row["paired_at"] or row["updated_at"] or row["created_at"],
            account_email=_account_email_from_metadata(metadata),
            request_account_emails=request.account_emails,
            inbound_author=row["inbound_author"],
            sender_type_hint=request.sender_type_hint,
            sender_domain_hint=request.sender_domain_hint,
        )
        # Apply quality_score multiplier from feedback
        quality_score = float(row["quality_score"]) if "quality_score" in row.keys() else 1.0
        # Surface quality into metadata so exemplar selection can rank by it.
        metadata["quality_score"] = quality_score
        combined = (lexical_score + metadata_score) * quality_score

        combined = self._apply_subject_boost(combined, pair_subject, tokens, self.config.subject_match_boost)

        return RetrievalMatch(
            result_type="reply_pair",
            score=round(combined, 4),
            lexical_score=round(lexical_score, 4),
            metadata_score=round(metadata_score, 4),
            source_type=row["source_type"],
            source_id=row["source_id"],
            account_email=_account_email_from_metadata(metadata),
            title=row["title"],
            author=row["reply_author"] or row["author"],
            external_uri=row["external_uri"],
            thread_id=row["thread_id"],
            created_at=row["created_at"],
            updated_at=row["updated_at"],
            document_id=row["document_id"],
            reply_pair_id=row["id"],
            snippet=_make_snippet(inbound_text, tokens=tokens),
            inbound_text=inbound_text,
            reply_text=reply_text,
            subject=pair_subject or None,
            metadata=metadata,
        )

    # -- Legacy paths (no FTS5) ──────────────────────────────────────────

    def _retrieve_documents(
        self,
        connection: sqlite3.Connection,
        *,
        query: str,
        tokens: list[str],
        request: RetrievalRequest,
    ) -> list[RetrievalMatch]:
        rows = connection.execute(
            """
            SELECT
                d.id,
                d.source_type,
                d.source_id,
                d.title,
                d.author,
                d.external_uri,
                d.thread_id,
                d.created_at,
                d.updated_at,
                d.content,
                d.metadata_json
            FROM documents AS d
            ORDER BY COALESCE(d.updated_at, d.created_at, d.created_ts) DESC
            LIMIT 500
            """
        ).fetchall()
        matches = [
            self._score_document_row(row, query=query, tokens=tokens, request=request)
            for row in rows
            if _matches_filters(
                source_type=row["source_type"],
                metadata_json=row["metadata_json"],
                source_types=request.source_types,
                account_emails=request.account_emails,
            )
        ]
        return _top_matches(matches, request.top_k_documents or self.config.top_k_documents)

    def _retrieve_chunks_legacy(
        self,
        connection: sqlite3.Connection,
        *,
        query: str,
        tokens: list[str],
        request: RetrievalRequest,
    ) -> list[RetrievalMatch]:
        rows = connection.execute(
            """
            SELECT
                c.id,
                c.chunk_index,
                c.content,
                c.metadata_json AS chunk_metadata_json,
                d.id AS document_id,
                d.source_type,
                d.source_id,
                d.title,
                d.author,
                d.external_uri,
                d.thread_id,
                d.created_at,
                d.updated_at,
                d.metadata_json AS document_metadata_json
            FROM chunks AS c
            INNER JOIN documents AS d
                ON d.id = c.document_id
            ORDER BY COALESCE(d.updated_at, d.created_at, d.created_ts) DESC, c.chunk_index ASC
            LIMIT 500
            """
        ).fetchall()
        matches = [
            self._score_chunk_row_legacy(row, query=query, tokens=tokens, request=request)
            for row in rows
            if _matches_filters(
                source_type=row["source_type"],
                metadata_json=row["document_metadata_json"],
                source_types=request.source_types,
                account_emails=request.account_emails,
            )
        ]
        return _top_matches(matches, request.top_k_chunks or self.config.top_k_chunks)

    def _retrieve_reply_pairs_legacy(
        self,
        connection: sqlite3.Connection,
        *,
        query: str,
        tokens: list[str],
        request: RetrievalRequest,
    ) -> list[RetrievalMatch]:
        rows = connection.execute(
            """
            SELECT
                rp.id,
                rp.source_type,
                rp.source_id,
                rp.thread_id,
                rp.inbound_text,
                rp.reply_text,
                rp.inbound_author,
                rp.reply_author,
                rp.paired_at,
                rp.metadata_json,
                COALESCE(rp.quality_score, 1.0) AS quality_score,
                d.id AS document_id,
                d.title,
                d.author,
                d.external_uri,
                d.created_at,
                d.updated_at
            FROM reply_pairs AS rp
            LEFT JOIN documents AS d
                ON d.id = rp.document_id
            ORDER BY COALESCE(rp.paired_at, d.updated_at, d.created_at, rp.created_ts) DESC
            LIMIT 500
            """
        ).fetchall()
        matches = [
            self._score_reply_pair_row_legacy(row, query=query, tokens=tokens, request=request)
            for row in rows
            if _matches_filters(
                source_type=row["source_type"],
                metadata_json=row["metadata_json"],
                source_types=request.source_types,
                account_emails=request.account_emails,
            )
        ]
        return _top_matches(matches, request.top_k_reply_pairs or self.config.top_k_reply_pairs)

    # -- Legacy scoring ──────────────────────────────────────────────────

    def _score_document_row(
        self,
        row: sqlite3.Row,
        *,
        query: str,
        tokens: list[str],
        request: RetrievalRequest,
    ) -> RetrievalMatch | None:
        metadata = _loads_json(row["metadata_json"])
        content = row["content"] or ""
        title = row["title"] or ""
        lexical_score = _score_text(query, tokens, f"{title}\n{content}")
        if lexical_score <= 0:
            return None
        metadata_score = self._metadata_score(
            source_type=row["source_type"],
            timestamp=row["updated_at"] or row["created_at"],
            account_email=_account_email_from_metadata(metadata),
            request_account_emails=request.account_emails,
        )
        return RetrievalMatch(
            result_type="document",
            score=round(lexical_score + metadata_score, 4),
            lexical_score=round(lexical_score, 4),
            metadata_score=round(metadata_score, 4),
            source_type=row["source_type"],
            source_id=row["source_id"],
            account_email=_account_email_from_metadata(metadata),
            title=row["title"],
            author=row["author"],
            external_uri=row["external_uri"],
            thread_id=row["thread_id"],
            created_at=row["created_at"],
            updated_at=row["updated_at"],
            document_id=row["id"],
            snippet=_make_snippet(content or title, tokens=tokens),
            content=content,
            metadata=metadata,
        )

    def _score_chunk_row_legacy(
        self,
        row: sqlite3.Row,
        *,
        query: str,
        tokens: list[str],
        request: RetrievalRequest,
    ) -> RetrievalMatch | None:
        document_metadata = _loads_json(row["document_metadata_json"])
        chunk_metadata = _loads_json(row["chunk_metadata_json"])
        content = row["content"] or ""
        title = row["title"] or ""
        lexical_score = (
            _score_text(query, tokens, f"{title}\n{content}")
            + _field_match_bonus(title, tokens, self.config.field_match_bonus_per_token)
        )
        if lexical_score <= 0:
            return None
        metadata_score = self._metadata_score(
            source_type=row["source_type"],
            timestamp=row["updated_at"] or row["created_at"],
            account_email=_account_email_from_metadata(document_metadata),
            request_account_emails=request.account_emails,
        )
        metadata = dict(document_metadata)
        metadata["chunk"] = chunk_metadata
        return RetrievalMatch(
            result_type="chunk",
            score=round(lexical_score + metadata_score, 4),
            lexical_score=round(lexical_score, 4),
            metadata_score=round(metadata_score, 4),
            source_type=row["source_type"],
            source_id=row["source_id"],
            account_email=_account_email_from_metadata(document_metadata),
            title=row["title"],
            author=row["author"],
            external_uri=row["external_uri"],
            thread_id=row["thread_id"],
            created_at=row["created_at"],
            updated_at=row["updated_at"],
            document_id=row["document_id"],
            chunk_id=row["id"],
            chunk_index=row["chunk_index"],
            snippet=_make_snippet(content, tokens=tokens),
            content=content,
            metadata=metadata,
        )

    def _score_reply_pair_row_legacy(
        self,
        row: sqlite3.Row,
        *,
        query: str,
        tokens: list[str],
        request: RetrievalRequest,
    ) -> RetrievalMatch | None:
        metadata = _loads_json(row["metadata_json"])
        inbound_text = row["inbound_text"] or ""
        reply_text = row["reply_text"] or ""
        pair_subject = metadata.get("subject", "")
        lexical_score = _score_text(query, tokens, inbound_text) + (_score_text(query, tokens, reply_text) * 0.35)
        if pair_subject:
            lexical_score += _field_match_bonus(pair_subject, tokens, self.config.field_match_bonus_per_token) * 0.5
        if lexical_score <= 0:
            return None
        metadata_score = self._metadata_score(
            source_type=row["source_type"],
            timestamp=row["paired_at"] or row["updated_at"] or row["created_at"],
            account_email=_account_email_from_metadata(metadata),
            request_account_emails=request.account_emails,
            inbound_author=row["inbound_author"],
            sender_type_hint=request.sender_type_hint,
            sender_domain_hint=request.sender_domain_hint,
        )
        quality_score = float(row["quality_score"]) if "quality_score" in row.keys() else 1.0
        # Surface quality into metadata so exemplar selection can rank by it.
        metadata["quality_score"] = quality_score
        combined = (lexical_score + metadata_score) * quality_score

        combined = self._apply_subject_boost(combined, pair_subject, tokens, self.config.subject_match_boost)

        return RetrievalMatch(
            result_type="reply_pair",
            score=round(combined, 4),
            lexical_score=round(lexical_score, 4),
            metadata_score=round(metadata_score, 4),
            source_type=row["source_type"],
            source_id=row["source_id"],
            account_email=_account_email_from_metadata(metadata),
            title=row["title"],
            author=row["reply_author"] or row["author"],
            external_uri=row["external_uri"],
            thread_id=row["thread_id"],
            created_at=row["created_at"],
            updated_at=row["updated_at"],
            document_id=row["document_id"],
            reply_pair_id=row["id"],
            snippet=_make_snippet(inbound_text, tokens=tokens),
            inbound_text=inbound_text,
            reply_text=reply_text,
            subject=pair_subject or None,
            metadata=metadata,
        )

    # -- Shared scoring helpers ──────────────────────────────────────────

    @staticmethod
    def _apply_subject_boost(combined: float, pair_subject: str, tokens: list[str], boost: float) -> float:
        """Apply subject token match multiplier if any long query token appears in the subject."""
        if not pair_subject or boost <= 0:
            return combined
        subject_lower = pair_subject.lower()
        for token in tokens:
            if len(token) > 4 and token in subject_lower:
                return combined * (1.0 + boost)
        return combined

    def _metadata_score(
        self,
        *,
        source_type: str,
        timestamp: str | None,
        account_email: str | None,
        request_account_emails: tuple[str, ...],
        inbound_author: str | None = None,
        sender_type_hint: str | None = None,
        sender_domain_hint: str | None = None,
    ) -> float:
        source_weight = self.config.source_weights.get(source_type, 1.0) - 1.0
        recency_bonus = _recency_bonus(
            timestamp,
            self.config.recency_boost_weight,
            self.config.recency_boost_days,
        )
        account_bonus = 0.0
        if request_account_emails and account_email and account_email in request_account_emails:
            account_bonus = self.config.account_boost_weight

        # Sender-aware boosts
        sender_bonus = 0.0
        sender_multiplier = 1.0
        if sender_type_hint and inbound_author:
            stored_sender_type = classify_sender(inbound_author)
            if stored_sender_type == sender_type_hint:
                sender_bonus += self.config.sender_type_boost
            if sender_domain_hint:
                stored_domain = extract_domain(inbound_author)
                if stored_domain and stored_domain == sender_domain_hint:
                    sender_bonus += self.config.sender_domain_boost
            # Apply per-type boost multiplier if available
            if self.config.sender_type_boost_map and sender_type_hint in self.config.sender_type_boost_map:
                sender_multiplier = self.config.sender_type_boost_map[sender_type_hint]

        base = source_weight + recency_bonus + account_bonus + sender_bonus
        return base * sender_multiplier


def _check_topic_overlap(query_tokens: list[str], topics: list[str]) -> bool:
    """Check if any query token (>4 chars) matches a sender's known topics."""
    topic_lower = {t.lower() for t in topics}
    for token in query_tokens:
        if len(token) > 2 and token in topic_lower:
            return True
    return False


def _load_sender_topics(connection: sqlite3.Connection, sender_domain: str) -> list[str]:
    """Load topics_json for a sender matching the given domain."""
    try:
        exists = connection.execute("SELECT 1 FROM sqlite_master WHERE type='table' AND name='sender_profiles'").fetchone()
        if not exists:
            return []
        row = connection.execute(
            "SELECT topics_json FROM sender_profiles WHERE domain = ? LIMIT 1",
            (sender_domain,),
        ).fetchone()
        if row and row["topics_json"]:
            topics = json.loads(row["topics_json"])
            return topics if isinstance(topics, list) else []
    except Exception:
        logger.warning("Failed to load sender topics for domain %s", sender_domain, exc_info=True)
    return []


def retrieve_context(
    request: RetrievalRequest,
    *,
    database_url: str,
    configs_dir: Path,
) -> RetrievalResponse:
    service = RetrievalService.from_database_url(database_url=database_url, configs_dir=configs_dir)
    return service.retrieve(request)


# -- Mode detection ──────────────────────────────────────────────────────


def detect_mode(query: str) -> ModeHint:
    return _detect_mode(query)


def _detect_mode(query: str) -> ModeHint:
    work_hits = len(_WORK_SIGNALS.findall(query))
    personal_hits = len(_PERSONAL_SIGNALS.findall(query))
    if work_hits > personal_hits:
        return "work"
    if personal_hits > work_hits:
        return "personal"
    # Default to work when signals are ambiguous.
    # Only return unknown if the query is very short (< 4 words) and has no signals.
    words = query.split()
    if len(words) < 4 and work_hits == 0 and personal_hits == 0:
        return "unknown"
    return "work"


# -- Config loading ──────────────────────────────────────────────────────


def _load_retrieval_config(configs_dir: Path) -> RetrievalConfig:
    # Try new-style configs/retrieval/defaults.yaml first, fall back to configs/retrieval.yaml
    defaults_path = configs_dir / "retrieval" / "defaults.yaml"
    legacy_path = configs_dir / "retrieval.yaml"

    if defaults_path.exists():
        payload = yaml.safe_load(defaults_path.read_text(encoding="utf-8")) or {}
        # Also load source_weights from legacy config if present
        source_weights: dict[str, float] = {}
        if legacy_path.exists():
            legacy = yaml.safe_load(legacy_path.read_text(encoding="utf-8")) or {}
            ranking = legacy.get("ranking", {})
            source_weights = {str(k): float(v) for k, v in ranking.get("source_weights", {}).items()}
        return RetrievalConfig(
            top_k_documents=int(payload.get("top_k_documents", 3)),
            top_k_chunks=int(payload.get("top_k_chunks", 3)),
            top_k_reply_pairs=int(payload.get("top_k_reply_pairs", 5)),
            recency_boost_days=int(payload.get("recency_boost_days", 90)),
            recency_boost_weight=float(payload.get("recency_boost_weight", 0.2)),
            account_boost_weight=float(payload.get("account_boost_weight", 0.15)),
            source_weights=source_weights,
            semantic_weight=float(payload.get("semantic_weight", 0.4)),
            semantic_min_coverage=float(payload.get("semantic_min_coverage", 0.1)),
            sender_type_boost=float(payload.get("sender_type_boost", 0.15)),
            sender_domain_boost=float(payload.get("sender_domain_boost", 0.10)),
            sender_type_boost_map={str(k): float(v) for k, v in (payload.get("sender_type_boost_map") or {}).items()},
            reranker_enabled=bool(payload.get("reranker_enabled", False)),
            reranker_model_id=(payload.get("reranker_model_id") or None) or None,
            reranker_blend_weight=(
                float(payload["reranker_blend_weight"])
                if isinstance(payload.get("reranker_blend_weight"), (int, float))
                else None
            ),
            reranker_ce_score_scale=(
                float(payload["reranker_ce_score_scale"])
                if isinstance(payload.get("reranker_ce_score_scale"), (int, float))
                else None
            ),
            subject_match_boost=float(payload.get("subject_match_boost", 0.2)),
            topic_match_boost=float(payload.get("topic_match_boost", 0.15)),
            lexical_scale=float(payload.get("lexical_scale", 2.0)),
            lexical_cap=float(payload.get("lexical_cap", 10.0)),
            field_match_bonus_per_token=float(payload.get("field_match_bonus_per_token", 0.25)),
        )

    # Legacy path
    payload = yaml.safe_load(legacy_path.read_text(encoding="utf-8")) or {}
    defaults = payload.get("defaults", {})
    ranking = payload.get("ranking", {})
    return RetrievalConfig(
        top_k_documents=3,
        top_k_chunks=int(defaults.get("top_k_chunks", 8)),
        top_k_reply_pairs=int(defaults.get("top_k_reply_pairs", 4)),
        recency_boost_days=90,
        recency_boost_weight=float(ranking.get("recency_weight", 0.2)),
        account_boost_weight=0.15,
        source_weights={str(k): float(v) for k, v in ranking.get("source_weights", {}).items()},
    )


# -- Shared utility functions ────────────────────────────────────────────


def _has_embedding_column(connection: sqlite3.Connection, table: str) -> bool:
    """Check if the table has an embedding column."""
    cols = [row[1] for row in connection.execute(f"PRAGMA table_info({table})").fetchall()]
    return "embedding" in cols


def _has_column(connection: sqlite3.Connection, table: str, column: str) -> bool:
    cols = [row[1] for row in connection.execute(f"PRAGMA table_info({table})").fetchall()]
    return column in cols


def _embedding_coverage(connection: sqlite3.Connection, table: str) -> float:
    """Return the fraction of rows that have a non-NULL, non-empty embedding."""
    row = connection.execute(f"SELECT COUNT(*) FROM {table}").fetchone()
    total = row[0] if row else 0
    if total == 0:
        return 0.0
    row = connection.execute(f"SELECT COUNT(*) FROM {table} WHERE embedding IS NOT NULL AND LENGTH(embedding) > 0").fetchone()
    embedded = row[0] if row else 0
    return embedded / total


def _fts5_query(tokens: list[str]) -> str:
    """Build an FTS5 query string from tokens using OR logic."""
    if not tokens:
        return ""
    safe = [t for t in tokens if t.isalnum()]
    if not safe:
        return ""
    return " OR ".join(safe)


def _matches_filters(
    *,
    source_type: str,
    metadata_json: str,
    source_types: tuple[str, ...],
    account_emails: tuple[str, ...],
) -> bool:
    if source_types and source_type not in source_types:
        return False
    if not account_emails:
        return True
    metadata = _loads_json(metadata_json)
    account_email = _account_email_from_metadata(metadata)
    return account_email in account_emails


def _loads_json(raw_json: str | None) -> dict[str, Any]:
    if not raw_json:
        return {}
    try:
        payload = json.loads(raw_json)
    except json.JSONDecodeError:
        return {}
    return payload if isinstance(payload, dict) else {}


def _account_email_from_metadata(metadata: dict[str, Any]) -> str | None:
    account_email = metadata.get("account_email")
    return account_email if isinstance(account_email, str) and account_email else None


def _tokenize(text: str) -> list[str]:
    return list(dict.fromkeys(_TOKEN_PATTERN.findall(text.lower())))


def _score_text(query: str, tokens: list[str], text: str) -> float:
    if not text:
        return 0.0
    lowered = text.lower()
    normalized_query = query.lower()
    score = 0.0
    if normalized_query in lowered:
        score += 4.0
    if not tokens:
        return score
    matched_tokens = 0
    token_occurrences = 0
    for token in tokens:
        occurrences = lowered.count(token)
        if occurrences:
            matched_tokens += 1
            token_occurrences += min(occurrences, 3)
    if matched_tokens == 0:
        return score
    score += (matched_tokens / len(tokens)) * 5.0
    score += token_occurrences * 0.35
    return score


def _field_match_bonus(text: str, tokens: list[str], multiplier: float = 0.25) -> float:
    """Bonus added on top of BM25 when query tokens literally appear in a
    structured field (title / subject). ``multiplier`` is the per-token
    contribution — historically hardcoded to 0.25; now configurable via
    ``RetrievalConfig.field_match_bonus_per_token`` so the autoresearch loop
    can tune the title/subject vs BM25 balance."""
    if not text:
        return 0.0
    lowered = text.lower()
    matched = sum(1 for token in tokens if token in lowered)
    return matched * multiplier


def _recency_bonus(timestamp: str | None, recency_weight: float, boost_days: int = 90) -> float:
    import math

    if not timestamp:
        return 0.0
    parsed = _parse_timestamp(timestamp)
    if parsed is None:
        return 0.0
    age_days = max((datetime.now(UTC) - parsed).days, 0)
    return round(recency_weight * math.exp(-age_days / boost_days), 4)


def _parse_timestamp(value: str) -> datetime | None:
    normalized = value.strip()
    if not normalized:
        return None
    if normalized.endswith("Z"):
        normalized = normalized[:-1] + "+00:00"
    try:
        parsed = datetime.fromisoformat(normalized)
    except ValueError:
        return None
    if parsed.tzinfo is None:
        return parsed.replace(tzinfo=UTC)
    return parsed.astimezone(UTC)


def _make_snippet(text: str, *, tokens: list[str], window: int = 220) -> str:
    clean_text = " ".join(text.split())
    if len(clean_text) <= window:
        return clean_text
    lowered = clean_text.lower()
    token_positions = [lowered.find(token) for token in tokens if lowered.find(token) >= 0]
    start = 0
    if token_positions:
        pivot = min(token_positions)
        start = max(pivot - (window // 4), 0)
    end = min(start + window, len(clean_text))
    snippet = clean_text[start:end]
    prefix = "..." if start > 0 else ""
    suffix = "..." if end < len(clean_text) else ""
    return f"{prefix}{snippet}{suffix}"


def _top_matches(matches: list[RetrievalMatch | None], limit: int) -> list[RetrievalMatch]:
    filtered = [match for match in matches if match is not None]
    filtered.sort(key=lambda match: (-match.score, match.result_type, match.source_id))
    return filtered[:limit]
