"""
semantic_chunker.py - 语义感知文本分段器
将解析后的文档段落按语义边界切分为适合 embedding 的 chunk
"""

from __future__ import annotations

import hashlib
import logging
import re
from dataclasses import dataclass, field
from typing import List

logger = logging.getLogger(__name__)


@dataclass
class Chunk:
    chunk_id: str
    doc_id: str
    content: str
    chapter: str = ""
    section: str = ""
    page_num: int = 0
    position: int = 0
    char_offset: int = 0
    char_length: int = 0
    prev_chunk_id: str = ""
    next_chunk_id: str = ""
    metadata: dict = field(default_factory=dict)


@dataclass
class ChunkResult:
    doc_id: str
    chunks: List[Chunk]
    total_chunks: int = 0
    total_chars: int = 0
    avg_chunk_chars: float = 0.0
    strategy_used: str = ""


class SemanticChunker:

    DEFAULT_MIN_CHUNK_CHARS = 200
    DEFAULT_MAX_CHUNK_CHARS = 1500
    DEFAULT_OVERLAP_CHARS = 50
    DEFAULT_TARGET_CHUNK_CHARS = 800

    def __init__(self, min_chars: int = None, max_chars: int = None,
                 overlap_chars: int = None, target_chars: int = None):
        self.min_chars = min_chars or self.DEFAULT_MIN_CHUNK_CHARS
        self.max_chars = max_chars or self.DEFAULT_MAX_CHUNK_CHARS
        self.overlap_chars = overlap_chars or self.DEFAULT_OVERLAP_CHARS
        self.target_chars = target_chars or self.DEFAULT_TARGET_CHUNK_CHARS

    def chunk_document(self, sections: list, doc_id: str,
                       strategy: str = "auto") -> ChunkResult:
        if not sections:
            return ChunkResult(doc_id=doc_id, chunks=[], strategy_used=strategy)

        strategy_map = {
            "structure": self._chunk_by_structure,
            "fixed": self._chunk_by_fixed,
            "sentence": self._chunk_by_sentence,
            "auto": self._chunk_auto,
        }
        chunk_fn = strategy_map.get(strategy, self._chunk_auto)
        result = chunk_fn(sections, doc_id)
        self._link_chunks(result.chunks)
        result.total_chunks = len(result.chunks)
        result.total_chars = sum(c.char_length for c in result.chunks)
        result.avg_chunk_chars = (
            result.total_chars / result.total_chunks if result.total_chunks else 0.0
        )
        return result

    def _chunk_by_structure(self, sections: list, doc_id: str) -> ChunkResult:
        groups = []
        current_group = {"title": "", "level": 0, "content_parts": [], "page_num": 0}

        for s in sections:
            level = getattr(s, "level", 0)
            title = getattr(s, "title", "")
            content = getattr(s, "content", "")
            page_num = getattr(s, "page_num", 0)

            if level > 0:
                if current_group["content_parts"]:
                    groups.append(current_group)
                current_group = {
                    "title": title,
                    "level": level,
                    "content_parts": [content] if content else [],
                    "page_num": page_num,
                }
            else:
                current_group["content_parts"].append(content)
                if current_group["page_num"] == 0:
                    current_group["page_num"] = page_num

        if current_group["content_parts"]:
            groups.append(current_group)

        groups = self._merge_short_groups(groups)

        chunks = []
        position = 0
        char_offset = 0
        for group in groups:
            full_content = "\n".join(group["content_parts"])
            if len(full_content) > self.max_chars:
                sub_parts = self._split_long_content(full_content, self.max_chars)
                for part in sub_parts:
                    chunk = Chunk(
                        chunk_id=self._generate_chunk_id(doc_id, position),
                        doc_id=doc_id,
                        content=part,
                        chapter=group["title"] if group["level"] <= 1 else "",
                        section=group["title"] if group["level"] > 1 else "",
                        page_num=group["page_num"],
                        position=position,
                        char_offset=char_offset,
                        char_length=len(part),
                    )
                    chunks.append(chunk)
                    position += 1
                    char_offset += len(part)
            else:
                chunk = Chunk(
                    chunk_id=self._generate_chunk_id(doc_id, position),
                    doc_id=doc_id,
                    content=full_content,
                    chapter=group["title"] if group["level"] <= 1 else "",
                    section=group["title"] if group["level"] > 1 else "",
                    page_num=group["page_num"],
                    position=position,
                    char_offset=char_offset,
                    char_length=len(full_content),
                )
                chunks.append(chunk)
                position += 1
                char_offset += len(full_content)

        return ChunkResult(doc_id=doc_id, chunks=chunks, strategy_used="structure")

    def _merge_short_groups(self, groups: list) -> list:
        if not groups:
            return groups
        merged = [groups[0]]
        for group in groups[1:]:
            prev_content = "\n".join(merged[-1]["content_parts"])
            if len(prev_content) < self.min_chars:
                merged[-1]["content_parts"].extend(group["content_parts"])
                if not merged[-1]["title"] and group["title"]:
                    merged[-1]["title"] = group["title"]
                    merged[-1]["level"] = group["level"]
            else:
                merged.append(group)
        return merged

    def _chunk_by_fixed(self, sections: list, doc_id: str) -> ChunkResult:
        all_content = "\n".join(getattr(s, "content", "") for s in sections)
        if not all_content.strip():
            return ChunkResult(doc_id=doc_id, chunks=[], strategy_used="fixed")

        sentences = self._split_sentences(all_content)
        chunks = []
        position = 0
        char_offset = 0
        current_sentences = []
        current_len = 0

        for sent in sentences:
            if current_len + len(sent) > self.target_chars and current_sentences:
                content = "".join(current_sentences)
                chunk = Chunk(
                    chunk_id=self._generate_chunk_id(doc_id, position),
                    doc_id=doc_id,
                    content=content,
                    position=position,
                    char_offset=char_offset,
                    char_length=len(content),
                )
                chunks.append(chunk)
                position += 1
                char_offset += len(content) - self.overlap_chars

                overlap_sentences = []
                overlap_len = 0
                for s in reversed(current_sentences):
                    if overlap_len + len(s) > self.overlap_chars:
                        break
                    overlap_sentences.insert(0, s)
                    overlap_len += len(s)
                current_sentences = overlap_sentences
                current_len = overlap_len

            current_sentences.append(sent)
            current_len += len(sent)

        if current_sentences:
            content = "".join(current_sentences)
            chunk = Chunk(
                chunk_id=self._generate_chunk_id(doc_id, position),
                doc_id=doc_id,
                content=content,
                position=position,
                char_offset=char_offset,
                char_length=len(content),
            )
            chunks.append(chunk)

        return ChunkResult(doc_id=doc_id, chunks=chunks, strategy_used="fixed")

    def _chunk_by_sentence(self, sections: list, doc_id: str) -> ChunkResult:
        all_content = "\n".join(getattr(s, "content", "") for s in sections)
        if not all_content.strip():
            return ChunkResult(doc_id=doc_id, chunks=[], strategy_used="sentence")

        sentences = self._split_sentences(all_content)
        if not sentences:
            return ChunkResult(doc_id=doc_id, chunks=[], strategy_used="sentence")

        avg_sent_len = sum(len(s) for s in sentences) / len(sentences)
        sentences_per_chunk = max(1, round(self.target_chars / avg_sent_len)) if avg_sent_len > 0 else 1

        chunks = []
        position = 0
        char_offset = 0
        i = 0

        while i < len(sentences):
            group = []
            group_len = 0
            j = i
            while j < len(sentences) and len(group) < sentences_per_chunk:
                group.append(sentences[j])
                group_len += len(sentences[j])
                j += 1

            if group_len < self.min_chars and j < len(sentences):
                while group_len < self.min_chars and j < len(sentences):
                    group.append(sentences[j])
                    group_len += len(sentences[j])
                    j += 1

            content = "".join(group)
            chunk = Chunk(
                chunk_id=self._generate_chunk_id(doc_id, position),
                doc_id=doc_id,
                content=content,
                position=position,
                char_offset=char_offset,
                char_length=len(content),
            )
            chunks.append(chunk)
            position += 1
            char_offset += len(content)
            i = j

        return ChunkResult(doc_id=doc_id, chunks=chunks, strategy_used="sentence")

    def _chunk_auto(self, sections: list, doc_id: str) -> ChunkResult:
        structure_levels = self._count_structure_levels(sections)

        if structure_levels >= 2:
            logger.debug("auto strategy: structure (levels=%d)", structure_levels)
            return self._chunk_by_structure(sections, doc_id)

        lengths = [len(getattr(s, "content", "")) for s in sections]
        if len(lengths) > 1:
            avg_len = sum(lengths) / len(lengths)
            variance = sum((l - avg_len) ** 2 for l in lengths) / len(lengths)
            std_dev = variance ** 0.5
            if std_dev < 100:
                logger.debug("auto strategy: fixed (std_dev=%.1f)", std_dev)
                return self._chunk_by_fixed(sections, doc_id)

        logger.debug("auto strategy: sentence")
        return self._chunk_by_sentence(sections, doc_id)

    def _merge_short_sections(self, sections: list) -> list:
        if not sections:
            return sections
        merged = [sections[0]]
        for s in sections[1:]:
            prev_content = getattr(merged[-1], "content", "")
            curr_content = getattr(s, "content", "")
            if len(prev_content) < self.min_chars:
                new_content = prev_content + "\n" + curr_content
                if hasattr(merged[-1], "content"):
                    merged[-1].content = new_content
                if not getattr(merged[-1], "title", "") and hasattr(s, "title"):
                    if hasattr(merged[-1], "title"):
                        merged[-1].title = s.title
            else:
                merged.append(s)
        return merged

    def _split_long_content(self, content: str, max_chars: int) -> list[str]:
        sentences = self._split_sentences(content)
        parts = []
        current_sentences = []
        current_len = 0

        for sent in sentences:
            if current_len + len(sent) > max_chars and current_sentences:
                parts.append("".join(current_sentences))
                current_sentences = []
                current_len = 0
            current_sentences.append(sent)
            current_len += len(sent)

        if current_sentences:
            if parts and len("".join(current_sentences)) < self.min_chars:
                last_part = parts.pop()
                parts.append(last_part + "".join(current_sentences))
            else:
                parts.append("".join(current_sentences))

        return parts if parts else [content]

    @staticmethod
    def _generate_chunk_id(doc_id: str, position: int) -> str:
        raw = f"{doc_id}_{position}"
        suffix = hashlib.md5(raw.encode()).hexdigest()[:8]
        return f"CHK_{doc_id[:16]}_{position:04d}_{suffix}"

    @staticmethod
    def _split_sentences(text: str) -> list[str]:
        sentences = re.split(r'(?<=[。！？\n;；.!?])\s*', text)
        return [s.strip() for s in sentences if s.strip()]

    @staticmethod
    def _count_structure_levels(sections: list) -> int:
        levels = set()
        for s in sections:
            if hasattr(s, "level") and s.level > 0:
                levels.add(s.level)
        return len(levels)

    @staticmethod
    def _link_chunks(chunks: list) -> None:
        for i, chunk in enumerate(chunks):
            if i > 0:
                chunk.prev_chunk_id = chunks[i - 1].chunk_id
            if i < len(chunks) - 1:
                chunk.next_chunk_id = chunks[i + 1].chunk_id
