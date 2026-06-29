"""Campaign-scoped exact, full-text, and BGE-M3 hybrid rule retrieval."""

from __future__ import annotations

import json
import re
from dataclasses import dataclass, replace
from typing import Any

import numpy as np
from sqlalchemy import func, or_, select, text

from ..db.database import Database
from ..db.models import (
    CampaignRuleProfile,
    CampaignRulePublication,
    CompendiumEntry,
    RuleChunk,
    RulePublication,
    RuleSection,
    RuleSet,
    RuleSource,
)
from .embedding import BgeM3Embedder, Embedder
from .ingest import DEFAULT_RULE_SET_ID


class RuleSearchError(RuntimeError):
    """Base error for rule retrieval."""


class RuleProfileNotFoundError(RuleSearchError):
    """A campaign has no configured rule profile."""


_DND_QUERY_TERMS: tuple[tuple[str, str], ...] = (
    ("擒抱", "Grappled grapple escape condition"),
    ("被抓", "Grappled grapple escape condition"),
    ("挣脱", "escape end condition"),
    ("法师", "Wizard"),
    ("术士", "Sorcerer"),
    ("邪术师", "Warlock"),
    ("牧师", "Cleric"),
    ("德鲁伊", "Druid"),
    ("圣武士", "Paladin"),
    ("游侠", "Ranger"),
    ("吟游诗人", "Bard"),
    ("施法", "Spellcasting spellcasting ability"),
    ("属性", "ability score"),
    ("豁免", "saving throw"),
    ("护甲等级", "Armor Class AC"),
    ("难度等级", "Difficulty Class DC"),
    ("专注", "Concentration"),
    ("反应", "Reaction"),
    ("附赠动作", "Bonus Action"),
)


def _enrich_query(query: str) -> str:
    """Append stable English SRD terms for common Chinese table language."""
    expansions = [english for chinese, english in _DND_QUERY_TERMS if chinese in query]
    return f"{query} {' '.join(dict.fromkeys(expansions))}".strip()


@dataclass(frozen=True)
class SearchScope:
    rule_set_id: str
    publication_ids: tuple[str, ...]


@dataclass(frozen=True)
class RuleSearchHit:
    rank: int
    score: float
    chunk_id: str
    rule_set: str
    publication: str
    breadcrumb: str
    heading: str
    text: str
    source_path: str
    start_line: int | None
    end_line: int | None
    char_start: int | None
    char_end: int | None
    citation: str
    channels: tuple[str, ...]


def _fts_query(query: str) -> str:
    terms = re.findall(r"[\w'-]+", query, flags=re.UNICODE)
    return " OR ".join(f'"{term.replace(chr(34), "")}"' for term in terms[:12])


class RuleSearchService:
    """Retrieve only rules enabled by the current campaign profile."""

    def __init__(self, database: Database, *, embedder: Embedder | None = None) -> None:
        self.database = database
        self.embedder = embedder
        self._dense_cache: dict[SearchScope, tuple[list[str], np.ndarray]] = {}

    def search(
        self,
        query: str,
        *,
        campaign_id: str | None = None,
        rule_set_id: str | None = None,
        publication_ids: list[str] | None = None,
        top_k: int = 5,
        dense: bool = True,
    ) -> list[RuleSearchHit]:
        if not query.strip():
            raise ValueError("query must not be empty")
        if top_k < 1 or top_k > 50:
            raise ValueError("top_k must be between 1 and 50")
        with self.database.transaction() as session:
            scope = self._resolve_scope(
                session,
                campaign_id=campaign_id,
                rule_set_id=rule_set_id,
                publication_ids=publication_ids,
            )
            exact = self._exact_ids(session, query, scope)
            retrieval_query = _enrich_query(query)
            lexical = self._lexical_ids(
                session, retrieval_query, scope, limit=max(top_k * 10, 50)
            )
            dense_ranked: list[str] = []
            if dense:
                embedder = self.embedder or BgeM3Embedder()
                query_vector = embedder.encode([retrieval_query])[0]
                dense_ranked = self._dense_ids(
                    session, query_vector, scope, limit=max(top_k * 10, 50)
                )

            scores: dict[str, float] = {}
            channels: dict[str, set[str]] = {}
            for channel, ids, weight in (
                ("exact", exact, 2.0),
                ("lexical", lexical, 1.0),
                ("dense", dense_ranked, 1.0),
            ):
                for rank, chunk_id in enumerate(ids, start=1):
                    scores[chunk_id] = scores.get(chunk_id, 0.0) + weight / (60 + rank)
                    channels.setdefault(chunk_id, set()).add(channel)
            if not scores:
                return []
            ordered_ids = sorted(scores, key=scores.get, reverse=True)[:top_k]
            hits = self._materialize(session, ordered_ids, scores, channels)
            return [replace(hit, rank=index) for index, hit in enumerate(hits, start=1)]

    def expand(self, chunk_id: str, *, mode: str = "section") -> dict[str, Any]:
        if mode not in {"chunk", "paragraph", "section", "section-with-children"}:
            raise ValueError("unsupported expansion mode")
        with self.database.transaction() as session:
            chunk = session.get(RuleChunk, chunk_id)
            if chunk is None:
                raise RuleSearchError(f"rule chunk not found: {chunk_id}")
            section = session.get(RuleSection, chunk.section_id) if chunk.section_id else None
            if mode in {"chunk", "paragraph"} or section is None:
                chunks = [chunk]
            elif mode == "section":
                chunks = list(
                    session.scalars(
                        select(RuleChunk)
                        .where(RuleChunk.section_id == section.id)
                        .order_by(RuleChunk.chunk_index)
                    )
                )
            else:
                section_ids = list(
                    session.scalars(
                        select(RuleSection.id).where(
                            RuleSection.source_id == section.source_id,
                            or_(
                                RuleSection.path == section.path,
                                RuleSection.path.like(f"{section.path}/%"),
                            ),
                        )
                    )
                )
                chunks = list(
                    session.scalars(
                        select(RuleChunk)
                        .where(RuleChunk.section_id.in_(section_ids))
                        .order_by(RuleChunk.chunk_index)
                    )
                )
            source = session.get(RuleSource, chunk.source_id)
            publication = session.get(RulePublication, source.publication_id) if source else None
            rule_set = session.get(RuleSet, source.rule_set_id) if source else None
            start = min((item.char_start for item in chunks if item.char_start is not None), default=None)
            end = max((item.char_end for item in chunks if item.char_end is not None), default=None)
            breadcrumb = chunk.breadcrumb or chunk.heading or ""
            citation = self._citation(rule_set, publication, breadcrumb, start, end)
            return {
                "chunk_id": chunk_id,
                "mode": mode,
                "breadcrumb": breadcrumb,
                "text": "\n\n".join(item.chunk_text for item in chunks),
                "source_path": source.source_path if source else "",
                "char_start": start,
                "char_end": end,
                "citation": citation,
            }

    @staticmethod
    def _resolve_scope(
        session,
        *,
        campaign_id: str | None,
        rule_set_id: str | None,
        publication_ids: list[str] | None,
    ) -> SearchScope:
        if campaign_id:
            profile = session.scalar(
                select(CampaignRuleProfile).where(
                    CampaignRuleProfile.campaign_id == campaign_id
                )
            )
            if profile is None:
                raise RuleProfileNotFoundError(
                    f"campaign has no rule profile: {campaign_id}"
                )
            enabled = tuple(
                session.scalars(
                    select(CampaignRulePublication.publication_id)
                    .where(
                        CampaignRulePublication.profile_id == profile.id,
                        CampaignRulePublication.enabled.is_(True),
                    )
                    .order_by(CampaignRulePublication.priority.desc())
                )
            )
            return SearchScope(profile.rule_set_id, enabled)
        selected_rule_set = rule_set_id or DEFAULT_RULE_SET_ID
        if publication_ids is None:
            publication_ids = list(
                session.scalars(
                    select(RulePublication.id).where(
                        RulePublication.rule_set_id == selected_rule_set
                    )
                )
            )
        return SearchScope(selected_rule_set, tuple(publication_ids))

    @staticmethod
    def _scope_condition(scope: SearchScope):
        conditions = [RuleSource.rule_set_id == scope.rule_set_id]
        if scope.publication_ids:
            conditions.append(RuleSource.publication_id.in_(scope.publication_ids))
        else:
            conditions.append(RuleSource.publication_id.is_(None))
        return conditions

    def _exact_ids(self, session, query: str, scope: SearchScope) -> list[str]:
        folded = query.strip().casefold()
        section_ids = list(
            session.scalars(
                select(RuleSection.id)
                .join(RuleSource, RuleSource.id == RuleSection.source_id)
                .where(
                    *self._scope_condition(scope),
                    func.lower(RuleSection.title) == folded,
                )
                .order_by(RuleSection.depth.desc(), RuleSection.order_index)
                .limit(30)
            )
        )
        entries = list(
            session.scalars(
                select(CompendiumEntry).where(
                    CompendiumEntry.rule_set_id == scope.rule_set_id,
                    CompendiumEntry.publication_id.in_(scope.publication_ids),
                )
            )
        )
        for entry in entries:
            if entry.name.casefold() == folded or folded in {
                alias.casefold() for alias in entry.aliases or []
            }:
                if entry.section_id:
                    section_ids.insert(0, entry.section_id)
        if not section_ids:
            section_ids = list(
                session.scalars(
                    select(RuleSection.id)
                    .join(RuleSource, RuleSource.id == RuleSection.source_id)
                    .where(
                        *self._scope_condition(scope),
                        func.lower(RuleSection.title).contains(folded),
                    )
                    .order_by(RuleSection.depth.desc(), RuleSection.order_index)
                    .limit(20)
                )
            )
        if not section_ids:
            return []
        return list(
            session.scalars(
                select(RuleChunk.id)
                .where(RuleChunk.section_id.in_(section_ids))
                .order_by(RuleChunk.chunk_index)
                .limit(50)
            )
        )

    def _lexical_ids(
        self, session, query: str, scope: SearchScope, *, limit: int
    ) -> list[str]:
        dialect = session.bind.dialect.name
        ranked_ids: list[str] = []
        if dialect == "sqlite":
            match = _fts_query(query)
            if match:
                rows = session.execute(
                    text(
                        "SELECT chunk_id, bm25(rule_chunks_fts) AS rank "
                        "FROM rule_chunks_fts WHERE rule_chunks_fts MATCH :query "
                        "ORDER BY rank LIMIT :limit"
                    ),
                    {"query": match, "limit": max(limit * 5, 250)},
                )
                ranked_ids = [str(row[0]) for row in rows]
        elif dialect == "postgresql":
            params: dict[str, Any] = {
                "query": query,
                "rule_set_id": scope.rule_set_id,
                "limit": limit,
            }
            publication_sql = ""
            if scope.publication_ids:
                names = []
                for index, publication_id in enumerate(scope.publication_ids):
                    name = f"publication_{index}"
                    names.append(f":{name}")
                    params[name] = publication_id
                publication_sql = f"AND rs.publication_id IN ({','.join(names)})"
            rows = session.execute(
                text(
                    "SELECT rc.id, ts_rank_cd(rc.search_vector, "
                    "plainto_tsquery('simple', :query)) AS rank "
                    "FROM rule_chunks rc JOIN rule_sources rs ON rs.id = rc.source_id "
                    "WHERE rs.rule_set_id = :rule_set_id "
                    f"{publication_sql} "
                    "AND rc.search_vector @@ plainto_tsquery('simple', :query) "
                    "ORDER BY rank DESC LIMIT :limit"
                ),
                params,
            )
            ranked_ids = [str(row[0]) for row in rows]

        if ranked_ids:
            allowed = set(
                session.scalars(
                    select(RuleChunk.id)
                    .join(RuleSource, RuleSource.id == RuleChunk.source_id)
                    .where(
                        RuleChunk.id.in_(ranked_ids),
                        *self._scope_condition(scope),
                    )
                )
            )
            filtered = [chunk_id for chunk_id in ranked_ids if chunk_id in allowed]
            if filtered:
                return filtered[:limit]

        terms = re.findall(r"[\w'-]+", query.casefold(), flags=re.UNICODE)[:8]
        if not terms:
            return []
        conditions = [
            or_(
                *[
                    func.lower(RuleChunk.search_text).contains(term)
                    for term in terms
                ]
            )
        ]
        return list(
            session.scalars(
                select(RuleChunk.id)
                .join(RuleSource, RuleSource.id == RuleChunk.source_id)
                .where(*self._scope_condition(scope), *conditions)
                .order_by(RuleChunk.chunk_index)
                .limit(limit)
            )
        )

    def _dense_ids(
        self, session, query_vector: list[float], scope: SearchScope, *, limit: int
    ) -> list[str]:
        if session.bind.dialect.name == "postgresql":
            params: dict[str, Any] = {
                "vector": json.dumps(query_vector),
                "rule_set_id": scope.rule_set_id,
                "limit": limit,
            }
            publication_sql = ""
            if scope.publication_ids:
                names = []
                for index, publication_id in enumerate(scope.publication_ids):
                    name = f"publication_{index}"
                    names.append(f":{name}")
                    params[name] = publication_id
                publication_sql = f"AND rs.publication_id IN ({','.join(names)})"
            rows = session.execute(
                text(
                    "SELECT rc.id, 1 - (rc.embedding_vector <=> CAST(:vector AS vector)) AS score "
                    "FROM rule_chunks rc JOIN rule_sources rs ON rs.id = rc.source_id "
                    "WHERE rs.rule_set_id = :rule_set_id "
                    f"{publication_sql} AND rc.embedding_vector IS NOT NULL "
                    "ORDER BY rc.embedding_vector <=> CAST(:vector AS vector) LIMIT :limit"
                ),
                params,
            )
            return [str(row[0]) for row in rows]

        cached = self._dense_cache.get(scope)
        if cached is None:
            rows = list(
                session.execute(
                    select(RuleChunk.id, RuleChunk.embedding_json)
                    .join(RuleSource, RuleSource.id == RuleChunk.source_id)
                    .where(
                        *self._scope_condition(scope),
                        RuleChunk.embedding_json.is_not(None),
                    )
                )
            )
            chunk_ids = [str(row[0]) for row in rows]
            matrix = np.asarray([row[1] for row in rows], dtype=np.float32)
            cached = (chunk_ids, matrix)
            self._dense_cache[scope] = cached
        chunk_ids, matrix = cached
        if matrix.size == 0:
            return []
        vector = np.asarray(query_vector, dtype=np.float32)
        scores = matrix @ vector
        candidate_count = min(limit, len(chunk_ids))
        indexes = np.argpartition(scores, -candidate_count)[-candidate_count:]
        indexes = indexes[np.argsort(scores[indexes])[::-1]]
        return [chunk_ids[int(index)] for index in indexes]

    def _materialize(
        self,
        session,
        ordered_ids: list[str],
        scores: dict[str, float],
        channels: dict[str, set[str]],
    ) -> list[RuleSearchHit]:
        chunks = {
            chunk.id: chunk
            for chunk in session.scalars(
                select(RuleChunk).where(RuleChunk.id.in_(ordered_ids))
            )
        }
        source_ids = {chunk.source_id for chunk in chunks.values()}
        sources = {
            source.id: source
            for source in session.scalars(
                select(RuleSource).where(RuleSource.id.in_(source_ids))
            )
        }
        publication_ids = {
            source.publication_id for source in sources.values() if source.publication_id
        }
        publications = {
            item.id: item
            for item in session.scalars(
                select(RulePublication).where(RulePublication.id.in_(publication_ids))
            )
        }
        rule_set_ids = {source.rule_set_id for source in sources.values() if source.rule_set_id}
        rule_sets = {
            item.id: item
            for item in session.scalars(
                select(RuleSet).where(RuleSet.id.in_(rule_set_ids))
            )
        }
        hits: list[RuleSearchHit] = []
        for chunk_id in ordered_ids:
            chunk = chunks[chunk_id]
            source = sources[chunk.source_id]
            publication = publications.get(source.publication_id)
            rule_set = rule_sets.get(source.rule_set_id)
            breadcrumb = chunk.breadcrumb or chunk.heading or ""
            citation = self._citation(
                rule_set,
                publication,
                breadcrumb,
                chunk.char_start,
                chunk.char_end,
            )
            hits.append(
                RuleSearchHit(
                    rank=0,
                    score=scores[chunk_id],
                    chunk_id=chunk_id,
                    rule_set=(
                        f"{rule_set.game_system} {rule_set.edition} / {rule_set.release}"
                        if rule_set
                        else ""
                    ),
                    publication=publication.name if publication else "",
                    breadcrumb=breadcrumb,
                    heading=chunk.heading or "",
                    text=chunk.chunk_text,
                    source_path=source.source_path,
                    start_line=chunk.start_line,
                    end_line=chunk.end_line,
                    char_start=chunk.char_start,
                    char_end=chunk.char_end,
                    citation=citation,
                    channels=tuple(sorted(channels.get(chunk_id, set()))),
                )
            )
        return hits

    @staticmethod
    def _citation(
        rule_set: RuleSet | None,
        publication: RulePublication | None,
        breadcrumb: str,
        start: int | None,
        end: int | None,
    ) -> str:
        parts = []
        if rule_set:
            parts.append(f"{rule_set.game_system} {rule_set.edition} {rule_set.release}")
        if publication:
            parts.append(publication.name)
        if breadcrumb:
            parts.append(breadcrumb)
        location = " → ".join(parts)
        if start is not None and end is not None:
            return f"[{location}, chars {start}-{end}]"
        return f"[{location}]"
