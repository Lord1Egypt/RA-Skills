"""Incremental hierarchical rule ingestion with optional BGE-M3 embeddings."""

from __future__ import annotations

import hashlib
import json
import uuid
from dataclasses import dataclass
from pathlib import Path

from sqlalchemy import delete, func, select, text

from ..db.database import Database
from ..db.models import (
    Campaign,
    CampaignRuleProfile,
    CampaignRulePublication,
    CompendiumEntry,
    EmbeddingModel,
    RuleChunk,
    RulePublication,
    RuleSection,
    RuleSet,
    RuleSource,
)
from .embedding import BgeM3Embedder, Embedder
from .parser import ParsedSection, parse_markdown

DEFAULT_RULE_SET_ID = "dnd5e-2024-srd-5.2.1"
DEFAULT_PUBLICATION_ID = "publication-srd-5.2.1"
DEFAULT_EMBEDDING_MODEL_ID = "embedding-bge-m3"
ZH_CN_RULE_SET_ID = "dnd5e-2014-srd-5.1"
ZH_CN_PUBLICATION_ID = "publication-srd-5.1-zh-cn"


@dataclass(frozen=True)
class IngestResult:
    rule_set_id: str
    publication_id: str
    sources_indexed: int
    sources_skipped: int
    sections: int
    chunks: int
    embeddings: int


def _stable_id(prefix: str, value: str) -> str:
    return f"{prefix}_{hashlib.sha256(value.encode('utf-8')).hexdigest()[:24]}"


def _checksum(content: str) -> str:
    return hashlib.sha256(content.encode("utf-8")).hexdigest()


def _embedding_text(
    rule_set: RuleSet, publication: RulePublication, breadcrumb: str, chunk_text: str
) -> str:
    return (
        f"{rule_set.game_system} | {rule_set.edition} | {rule_set.release}\n"
        f"{publication.name} | {breadcrumb}\n{chunk_text}"
    )


def _entry_type(section: ParsedSection) -> str | None:
    path = " / ".join(section.heading_path).casefold()
    if "spell descriptions" in path and section.depth >= 3:
        return "spell"
    if "condition" in path and section.depth >= 2:
        return "condition"
    if "magic item" in path and section.depth >= 3:
        return "item"
    if any(label in path for label in ("monsters", "stat blocks")) and section.depth >= 3:
        return "monster"
    return None


class RuleIngestService:
    """Build the version -> publication -> section -> chunk retrieval hierarchy."""

    def __init__(self, database: Database, *, embedder: Embedder | None = None) -> None:
        self.database = database
        self.embedder = embedder

    def ingest_srd(
        self,
        references_dir: str | Path,
        *,
        embed: bool = True,
        force: bool = False,
    ) -> IngestResult:
        root = Path(references_dir).expanduser().resolve()
        files = sorted(root.glob("DND5eSRD_*.md"))
        if not files:
            raise FileNotFoundError(f"no SRD markdown files found in {root}")
        embedder = self.embedder or (BgeM3Embedder(show_progress=True) if embed else None)

        indexed = skipped = section_count = chunk_count = embedding_count = 0
        with self.database.transaction() as session:
            rule_set = session.get(RuleSet, DEFAULT_RULE_SET_ID)
            if rule_set is None:
                rule_set = RuleSet(
                    id=DEFAULT_RULE_SET_ID,
                    game_system="D&D 5e",
                    edition="2024",
                    release="SRD 5.2.1",
                    locale="en",
                    metadata_json={"license": "CC-BY-4.0"},
                )
                session.add(rule_set)
                session.flush()
            publication = session.get(RulePublication, DEFAULT_PUBLICATION_ID)
            if publication is None:
                publication = RulePublication(
                    id=DEFAULT_PUBLICATION_ID,
                    rule_set_id=DEFAULT_RULE_SET_ID,
                    name="System Reference Document 5.2.1",
                    slug="srd-5-2-1",
                    publication_type="core",
                    priority=100,
                    license="CC-BY-4.0",
                )
                session.add(publication)
                session.flush()
            model_row = None
            if embedder is not None:
                model_row = session.get(EmbeddingModel, DEFAULT_EMBEDDING_MODEL_ID)
                if model_row is None:
                    model_row = EmbeddingModel(
                        id=DEFAULT_EMBEDDING_MODEL_ID,
                        provider="sentence-transformers",
                        model_name=embedder.model_name,
                        dimensions=embedder.dimensions,
                    )
                    session.add(model_row)
                elif (
                    model_row.model_name != embedder.model_name
                    or model_row.dimensions != embedder.dimensions
                ):
                    raise ValueError("active embedding model metadata does not match the embedder")
            session.flush()

            for file_path in files:
                content = file_path.read_text(encoding="utf-8")
                checksum = _checksum(content)
                source_key = f"srd-5.2.1/{file_path.name}"
                source = session.scalar(
                    select(RuleSource).where(RuleSource.source_path == source_key)
                )
                if source is not None and source.checksum == checksum and not force:
                    chunks_total = int(
                        session.scalar(
                            select(func.count()).select_from(RuleChunk).where(
                                RuleChunk.source_id == source.id
                            )
                        )
                        or 0
                    )
                    embeddings_total = int(
                        session.scalar(
                            select(func.count()).select_from(RuleChunk).where(
                                RuleChunk.source_id == source.id,
                                RuleChunk.embedding_json.is_not(None),
                            )
                        )
                        or 0
                    )
                    if chunks_total and (embedder is None or embeddings_total == chunks_total):
                        skipped += 1
                        continue
                if source is None:
                    source = RuleSource(
                        id=_stable_id("source", source_key),
                        rule_set_id=rule_set.id,
                        publication_id=publication.id,
                        name=file_path.stem,
                        source_path=source_key,
                        source_type="markdown",
                        system_version="D&D 5e 2024 / SRD 5.2.1",
                        locale="en",
                        checksum=checksum,
                        metadata_json={"filename": file_path.name},
                    )
                    session.add(source)
                    session.flush()
                else:
                    old_section_ids = list(
                        session.scalars(
                            select(RuleSection.id).where(RuleSection.source_id == source.id)
                        )
                    )
                    if old_section_ids:
                        session.execute(
                            delete(CompendiumEntry).where(
                                CompendiumEntry.section_id.in_(old_section_ids)
                            )
                        )
                    session.execute(delete(RuleChunk).where(RuleChunk.source_id == source.id))
                    session.execute(delete(RuleSection).where(RuleSection.source_id == source.id))
                    source.rule_set_id = rule_set.id
                    source.publication_id = publication.id
                    source.checksum = checksum
                    source.metadata_json = {"filename": file_path.name}
                    session.flush()

                parsed_sections, parsed_chunks = parse_markdown(content)
                section_ids: dict[str, str] = {}
                for section in parsed_sections:
                    section_id = _stable_id("section", f"{source.id}:{section.path}")
                    section_ids[section.key] = section_id
                    session.add(
                        RuleSection(
                            id=section_id,
                            source_id=source.id,
                            publication_id=publication.id,
                            parent_id=(
                                section_ids.get(section.parent_key)
                                if section.parent_key is not None
                                else None
                            ),
                            section_type="chapter" if section.depth == 1 else "section",
                            title=section.title,
                            slug=section.slug,
                            path=section.path,
                            heading_path=list(section.heading_path),
                            depth=section.depth,
                            order_index=section.order_index,
                            start_line=section.start_line,
                            end_line=section.end_line,
                            char_start=section.char_start,
                            char_end=section.char_end,
                        )
                    )
                    # IDs are assigned explicitly, but SQLAlchemy cannot infer insert
                    # order without ORM relationships. Flush the hierarchy node before
                    # entries reference it.
                    session.flush()
                    entry_type = _entry_type(section)
                    if entry_type:
                        entry_id = _stable_id(
                            "entry", f"{rule_set.id}:{entry_type}:{section.title.casefold()}"
                        )
                        existing_entry = session.get(CompendiumEntry, entry_id)
                        values = {
                            "breadcrumb": list(section.heading_path),
                            "char_start": section.char_start,
                            "char_end": section.char_end,
                        }
                        if existing_entry is None:
                            session.add(
                                CompendiumEntry(
                                    id=entry_id,
                                    rule_set_id=rule_set.id,
                                    publication_id=publication.id,
                                    section_id=section_id,
                                    entry_type=entry_type,
                                    name=section.title,
                                    aliases=[],
                                    data_json=values,
                                    source=source_key,
                                    system_version="SRD 5.2.1",
                                )
                            )
                        else:
                            existing_entry.section_id = section_id
                            existing_entry.data_json = values
                            existing_entry.source = source_key
                session.flush()

                texts = [
                    _embedding_text(
                        rule_set,
                        publication,
                        " → ".join(chunk.heading_path),
                        chunk.text,
                    )
                    for chunk in parsed_chunks
                ]
                vectors = embedder.encode(texts) if embedder is not None else [None] * len(texts)
                rows: list[RuleChunk] = []
                for chunk, embedding_text, vector in zip(
                    parsed_chunks, texts, vectors, strict=True
                ):
                    chunk_id = _stable_id("chunk", f"{source.id}:{chunk.chunk_index}")
                    breadcrumb = " → ".join(chunk.heading_path)
                    row = RuleChunk(
                        id=chunk_id,
                        source_id=source.id,
                        section_id=section_ids[chunk.section_key],
                        embedding_model_id=model_row.id if model_row else None,
                        chunk_index=chunk.chunk_index,
                        heading=chunk.heading,
                        breadcrumb=breadcrumb,
                        start_line=chunk.start_line,
                        end_line=chunk.end_line,
                        char_start=chunk.char_start,
                        char_end=chunk.char_end,
                        token_count=max(1, len(chunk.text) // 4),
                        content_hash=_checksum(chunk.text),
                        chunk_text=chunk.text,
                        search_text=f"{breadcrumb}\n{chunk.text}",
                        embedding_json=vector,
                        metadata_json={"embedding_text_hash": _checksum(embedding_text)},
                    )
                    session.add(row)
                    rows.append(row)
                session.flush()
                if rows and session.bind is not None and session.bind.dialect.name == "postgresql":
                    session.execute(
                        text(
                            "UPDATE rule_chunks SET search_vector = "
                            "to_tsvector('simple', search_text) WHERE source_id = :source_id"
                        ),
                        {"source_id": source.id},
                    )
                    vector_payload = [
                        {"id": row.id, "vector": json.dumps(row.embedding_json)}
                        for row in rows
                        if row.embedding_json is not None
                    ]
                    if vector_payload:
                        session.execute(
                            text(
                                "UPDATE rule_chunks SET embedding_vector = CAST(:vector AS vector) "
                                "WHERE id = :id"
                            ),
                            vector_payload,
                        )
                indexed += 1
                section_count += len(parsed_sections)
                chunk_count += len(rows)
                embedding_count += sum(row.embedding_json is not None for row in rows)

        return IngestResult(
            rule_set_id=DEFAULT_RULE_SET_ID,
            publication_id=DEFAULT_PUBLICATION_ID,
            sources_indexed=indexed,
            sources_skipped=skipped,
            sections=section_count,
            chunks=chunk_count,
            embeddings=embedding_count,
        )

    def ingest_directory_srd(
        self,
        root_dir: str | Path,
        *,
        rule_set_id: str = ZH_CN_RULE_SET_ID,
        publication_id: str = ZH_CN_PUBLICATION_ID,
        embed: bool = True,
        force: bool = False,
    ) -> IngestResult:
        """Ingest a folder-based SRD (e.g. Chinese translation).

        Each subdirectory is a category; each ``.md`` file is a source.
        """
        root = Path(root_dir).expanduser().resolve()
        files = sorted(root.rglob("*.md"))
        # Filter out non-content files
        skip_names = {"index", "changelog", "legal", "notice", "terms", "readme"}
        files = [
            f for f in files
            if f.stem.casefold() not in skip_names and not f.stem.startswith("#")
        ]
        if not files:
            raise FileNotFoundError(f"no SRD markdown files found under {root}")
        embedder = self.embedder or (BgeM3Embedder(show_progress=True) if embed else None)

        indexed = skipped = section_count = chunk_count = embedding_count = 0
        with self.database.transaction() as session:
            rule_set = session.get(RuleSet, rule_set_id)
            if rule_set is None:
                rule_set = RuleSet(
                    id=rule_set_id,
                    game_system="D&D 5e",
                    edition="2014",
                    release="SRD 5.1",
                    locale="zh-CN",
                    metadata_json={"license": "CC-BY-4.0", "source": "SagiriWWW/DND.SRD.zh-CN"},
                )
                session.add(rule_set)
                session.flush()
            publication = session.get(RulePublication, publication_id)
            if publication is None:
                publication = RulePublication(
                    id=publication_id,
                    rule_set_id=rule_set_id,
                    name="D&D 5E SRD 中文版",
                    slug="srd-5-1-zh-cn",
                    publication_type="core",
                    priority=90,
                    license="CC-BY-4.0",
                )
                session.add(publication)
                session.flush()
            model_row = None
            if embedder is not None:
                model_row = session.get(EmbeddingModel, DEFAULT_EMBEDDING_MODEL_ID)
                if model_row is None:
                    model_row = EmbeddingModel(
                        id=DEFAULT_EMBEDDING_MODEL_ID,
                        provider="sentence-transformers",
                        model_name=embedder.model_name,
                        dimensions=embedder.dimensions,
                    )
                    session.add(model_row)

            for file_path in files:
                rel = file_path.relative_to(root)
                category_name = rel.parts[0] if len(rel.parts) > 1 else "_root"
                source_key = f"srd-5.1-zh-cn/{rel.as_posix()}"

                content = file_path.read_text(encoding="utf-8")
                checksum = _checksum(content)

                source = session.scalar(
                    select(RuleSource).where(RuleSource.source_path == source_key)
                )
                if source is not None and source.checksum == checksum and not force:
                    chunks_exist = session.scalar(
                        select(func.count()).select_from(RuleChunk).where(
                            RuleChunk.source_id == source.id
                        )
                    ) or 0
                    if chunks_exist:
                        skipped += 1
                        continue

                if source is None:
                    source = RuleSource(
                        id=_stable_id("source", source_key),
                        rule_set_id=rule_set.id,
                        publication_id=publication.id,
                        name=f"{category_name}/{file_path.stem}",
                        source_path=source_key,
                        source_type="markdown",
                        system_version="D&D 5e 2014 / SRD 5.1",
                        locale="zh-CN",
                        checksum=checksum,
                        metadata_json={
                            "filename": file_path.name,
                            "category": category_name,
                        },
                    )
                    session.add(source)
                    session.flush()
                else:
                    old_sid = list(session.scalars(
                        select(RuleSection.id).where(RuleSection.source_id == source.id)
                    ))
                    if old_sid:
                        session.execute(
                            delete(CompendiumEntry).where(
                                CompendiumEntry.section_id.in_(old_sid)
                            )
                        )
                    session.execute(delete(RuleChunk).where(RuleChunk.source_id == source.id))
                    session.execute(delete(RuleSection).where(RuleSection.source_id == source.id))
                    source.rule_set_id = rule_set.id
                    source.publication_id = publication.id
                    source.checksum = checksum
                    source.metadata_json = {
                        "filename": file_path.name,
                        "category": category_name,
                    }
                    session.flush()

                parsed_sections, parsed_chunks = parse_markdown(content)
                section_ids: dict[str, str] = {}
                for section in parsed_sections:
                    section_id = _stable_id("section", f"{source.id}:{section.path}")
                    section_ids[section.key] = section_id
                    session.add(
                        RuleSection(
                            id=section_id,
                            source_id=source.id,
                            publication_id=publication.id,
                            parent_id=(
                                section_ids.get(section.parent_key)
                                if section.parent_key is not None
                                else None
                            ),
                            section_type="chapter" if section.depth == 1 else "section",
                            title=section.title,
                            slug=section.slug,
                            path=section.path,
                            heading_path=list(section.heading_path),
                            depth=section.depth,
                            order_index=section.order_index,
                            start_line=section.start_line,
                            end_line=section.end_line,
                            char_start=section.char_start,
                            char_end=section.char_end,
                        )
                    )
                    session.flush()

                texts = [
                    _embedding_text(
                        rule_set, publication,
                        " → ".join(chunk.heading_path), chunk.text,
                    )
                    for chunk in parsed_chunks
                ]
                vectors = embedder.encode(texts) if embedder is not None else [None] * len(texts)
                for chunk, embedding_text, vector in zip(
                    parsed_chunks, texts, vectors, strict=True
                ):
                    chunk_id = _stable_id("chunk", f"{source.id}:{chunk.chunk_index}")
                    breadcrumb = " → ".join(chunk.heading_path)
                    session.add(
                        RuleChunk(
                            id=chunk_id,
                            source_id=source.id,
                            section_id=section_ids[chunk.section_key],
                            embedding_model_id=model_row.id if model_row else None,
                            chunk_index=chunk.chunk_index,
                            heading=chunk.heading,
                            breadcrumb=breadcrumb,
                            start_line=chunk.start_line,
                            end_line=chunk.end_line,
                            char_start=chunk.char_start,
                            char_end=chunk.char_end,
                            token_count=max(1, len(chunk.text) // 4),
                            content_hash=_checksum(chunk.text),
                            chunk_text=chunk.text,
                            search_text=f"{breadcrumb}\n{chunk.text}",
                            embedding_json=vector,
                            metadata_json={"_source": "zh-CN"},
                        )
                    )
                    session.flush()

                indexed += 1
                section_count += len(parsed_sections)
                chunk_count += len(parsed_chunks)
                embedding_count += sum(
                    1 for _ in parsed_chunks if embedder is not None
                )

        return IngestResult(
            rule_set_id=rule_set_id,
            publication_id=publication_id,
            sources_indexed=indexed,
            sources_skipped=skipped,
            sections=section_count,
            chunks=chunk_count,
            embeddings=embedding_count,
        )

    def bind_campaign(
        self,
        campaign_id: str,
        *,
        rule_set_id: str = DEFAULT_RULE_SET_ID,
        publication_ids: list[str] | None = None,
    ) -> str:
        publication_ids = publication_ids or [DEFAULT_PUBLICATION_ID]
        with self.database.transaction() as session:
            if session.get(Campaign, campaign_id) is None:
                raise ValueError(f"campaign not found: {campaign_id}")
            if session.get(RuleSet, rule_set_id) is None:
                raise ValueError(f"rule set not found: {rule_set_id}")
            profile = session.scalar(
                select(CampaignRuleProfile).where(
                    CampaignRuleProfile.campaign_id == campaign_id
                )
            )
            if profile is None:
                profile = CampaignRuleProfile(
                    id=f"rule_profile_{uuid.uuid4().hex}",
                    campaign_id=campaign_id,
                    rule_set_id=rule_set_id,
                    locale="en",
                )
                session.add(profile)
                session.flush()
            else:
                profile.rule_set_id = rule_set_id
                session.execute(
                    delete(CampaignRulePublication).where(
                        CampaignRulePublication.profile_id == profile.id
                    )
                )
            for priority, publication_id in enumerate(publication_ids, start=1):
                publication = session.get(RulePublication, publication_id)
                if publication is None or publication.rule_set_id != rule_set_id:
                    raise ValueError(f"publication not found in rule set: {publication_id}")
                session.add(
                    CampaignRulePublication(
                        id=f"rule_profile_publication_{uuid.uuid4().hex}",
                        profile_id=profile.id,
                        publication_id=publication_id,
                        priority=priority,
                    )
                )
            return profile.id
