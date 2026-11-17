#!/usr/bin/env python3
"""
统一文档单元协议（DocumentUnit）
===================================
定义统一的数据结构，让分块/命题/片段/引用等所有文档单元可互操作。

各脚本的数据类型统一继承自 DocumentUnit，实现：
- 命题分块 (Proposition) → DocumentUnit
- 片段提取 (Segment) → DocumentUnit
- 上下文头增强 (Chunk) → DocumentUnit
- 引用溯源 (Citation) → 可转换为 DocumentUnit

使用方式：
    from document_unit import DocumentUnit, UnitConverter

    # 直接使用
    unit = DocumentUnit(
        id="doc_1",
        content="RAG 是一种结合检索和生成的技术。",
        parent_paragraph="第一段：RAG 是一种...能降低幻觉。",
        metadata={"section": "第一章", "topic": "RAG"}
    )

    # 从已有类型转换
    unit = UnitConverter.from_dict({"id": "doc_1", "text": "...", "metadata": {}})
"""
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


# ============================================================
# 核心数据类
# ============================================================

@dataclass
class DocumentUnit:
    """
    统一文档单元：所有 RAG 处理流程中产生的文本块的基础数据结构。

    属性约定：
        - id: 全局唯一标识符
        - content: 用于向量化索引/检索的内容
        - parent_paragraph: 父块（用于返回给 LLM 的完整上下文）
        - metadata: 附加元数据（标题/章节/主题/实体等）
    """
    id: str
    content: str
    parent_paragraph: str = ""
    metadata: Dict[str, Any] = field(default_factory=dict)

    @property
    def length(self) -> int:
        """内容长度（字符数）。"""
        return len(self.content)

    @property
    def has_parent(self) -> bool:
        """是否有父块。"""
        return bool(self.parent_paragraph)

    def to_dict(self) -> Dict[str, Any]:
        """转换为字典（用于 JSON 序列化）。"""
        return {
            "id": self.id,
            "content": self.content,
            "parent_paragraph": self.parent_paragraph,
            "metadata": self.metadata,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "DocumentUnit":
        """从字典构造。"""
        return cls(
            id=data.get("id", data.get("doc_id", "")),
            content=data.get("content", data.get("text", data.get("raw_text", ""))),
            parent_paragraph=data.get("parent_paragraph", data.get("parent", "")),
            metadata=data.get("metadata", {}),
        )


# ============================================================
# 转换工具
# ============================================================

class UnitConverter:
    """
    各类数据结构与 DocumentUnit 之间的转换工具。

    支持：
        - from_proposition: 从 PropositionChunker 的 Proposition 转换
        - from_segment: 从 RelevantSegmentExtractor 的 Segment 转换
        - from_retrieval: 从 BM25Retriever 的 RetrievalResult 转换
        - from_dict: 从任意字典转换
        - to_list: 批量转换
    """

    @staticmethod
    def from_proposition(prop) -> DocumentUnit:
        """
        从 Proposition 对象转换。

        兼容 proposition_chunker.Proposition 的数据结构。
        """
        return DocumentUnit(
            id=prop.id,
            content=prop.content,
            parent_paragraph=prop.parent_paragraph,
            metadata={
                "is_atomic": getattr(prop, "is_atomic", True),
                "is_self_contained": getattr(prop, "is_self_contained", True),
                "entities": getattr(prop, "entities", []),
                "confidence": getattr(prop, "confidence", 1.0),
            },
        )

    @staticmethod
    def from_segment(seg) -> DocumentUnit:
        """
        从 Segment 对象转换。

        兼容 segment_extractor.Segment 的数据结构。
        """
        return DocumentUnit(
            id=getattr(seg, "source_doc", "unknown"),
            content=getattr(seg, "text", "") or getattr(seg, "resolved_text", ""),
            parent_paragraph=getattr(seg, "source_doc", ""),
            metadata={
                "relevance_score": getattr(seg, "relevance_score", 0.0),
                "start_pos": getattr(seg, "start_pos", 0),
                "end_pos": getattr(seg, "end_pos", 0),
            },
        )

    @staticmethod
    def from_retrieval(result) -> DocumentUnit:
        """
        从 RetrievalResult 对象转换。

        兼容 bm25_retriever.RetrievalResult 的数据结构。
        """
        return DocumentUnit(
            id=getattr(result, "id", "unknown"),
            content=getattr(result, "text", ""),
            parent_paragraph=getattr(result, "text", ""),
            metadata={
                "score": getattr(result, "score", 0.0),
                "metadata": getattr(result, "metadata", {}),
            },
        )

    @staticmethod
    def from_chunk(chunk) -> DocumentUnit:
        """
        从 Chunk 对象转换。

        兼容 chunker_factory.Chunk 的数据结构。
        """
        return DocumentUnit(
            id=getattr(chunk, "id", "unknown"),
            content=getattr(chunk, "content", ""),
            parent_paragraph=getattr(chunk, "parent_paragraph", ""),
            metadata=getattr(chunk, "metadata", {}),
        )

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> DocumentUnit:
        """从任意字典转换（兼容多种键名）。"""
        return DocumentUnit.from_dict(data)

    @staticmethod
    def from_source(source) -> DocumentUnit:
        """
        从 CitationTracker 的 Source 对象转换。

        兼容 citation_tracker.Source 的数据结构。
        """
        return DocumentUnit(
            id=getattr(source, "id", "unknown"),
            content=getattr(source, "content", ""),
            parent_paragraph=getattr(source, "content", ""),
            metadata={
                "title": getattr(source, "title", ""),
                "location": getattr(source, "location", ""),
                "authority_level": getattr(source, "authority_level", 1),
                "publish_date": getattr(source, "publish_date", ""),
                "url": getattr(source, "url", ""),
            },
        )

    @staticmethod
    def to_list(units, factory_fn) -> List[DocumentUnit]:
        """
        批量转换。

        Args:
            units: 原始对象列表
            factory_fn: 转换函数（如 UnitConverter.from_proposition）

        Returns:
            DocumentUnit 列表
        """
        return [factory_fn(u) for u in units if u]
