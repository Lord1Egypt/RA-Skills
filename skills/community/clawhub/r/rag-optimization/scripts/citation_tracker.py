#!/usr/bin/env python3
"""
引用溯源器（Citation Tracker）

为生成的答案添加来源引用，提升可信度和可解释性

使用方法：
    python citation_tracker.py --answer "答案文本" --sources doc1.txt doc2.txt

核心功能：
    1. 来源匹配：将答案片段与源文档匹配
    2. 引用标注：生成行内引用或脚注引用
    3. 可信度评估：评估答案的可信度
    4. 多格式输出：支持多种引用格式
"""

import os
import re
import json
import logging
from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional, Tuple
from enum import Enum

# 设置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class CitationFormat(Enum):
    """引用格式"""
    INLINE = "inline"          # 行内引用：文本[^1]
    FOOTNOTE = "footnote"      # 脚注引用：文本[^1] + 脚注区
    DETAILED = "detailed"      # 详细格式：文本 + 来源详情
    JSON = "json"              # JSON格式（程序化使用）


@dataclass
class Source:
    """来源文档"""
    id: str                           # 文档ID
    title: str                        # 文档标题
    content: str                      # 文档内容
    location: str = ""                # 具体位置（章节/页码）
    authority_level: int = 1          # 权威级别（1-5，5最高）
    publish_date: str = ""            # 发布日期
    url: str = ""                     # 来源链接


@dataclass
class Citation:
    """引用信息"""
    id: str                           # 引用ID
    source: Source                    # 来源文档
    matched_text: str                 # 匹配的原文
    match_type: str                   # 匹配类型：exact/fuzzy/entity
    confidence: float                 # 匹配置信度
    answer_segment: str               # 对应的答案片段
    start_pos: int = 0                # 答案中的起始位置
    end_pos: int = 0                  # 答案中的结束位置


@dataclass
class CitedSegment:
    """带引用的答案片段"""
    text: str                         # 片段文本
    citations: List[Citation]         # 引用列表
    is_inferred: bool = False         # 是否是推理得出
    confidence: float = 1.0           # 可信度


@dataclass
class CredibilityScore:
    """可信度评分"""
    source_coverage: float            # 有引用覆盖的内容占比
    citation_density: float           # 引用密度（引用数/片段数）
    source_authority: float           # 来源权威度
    overall_credibility: float        # 综合可信度
    details: Dict[str, Any] = field(default_factory=dict)


class CitationMatcher:
    """引用匹配器 - 将答案片段与源文档匹配"""
    
    def __init__(self, llm_client=None, config: Dict = None):
        self.llm = llm_client
        self.config = config or {}
        
        # 匹配阈值
        self.exact_threshold = self.config.get('exact_threshold', 0.95)
        self.fuzzy_threshold = self.config.get('fuzzy_threshold', 0.7)
        self.entity_threshold = self.config.get('entity_threshold', 0.5)
    
    def match(self, answer_segment: str, sources: List[Source]) -> List[Citation]:
        """
        匹配答案片段与源文档
        
        Args:
            answer_segment: 答案片段
            sources: 源文档列表
        
        Returns:
            匹配的引用列表
        """
        citations = []
        
        for source in sources:
            # 方法1: 精确匹配
            citation = self._exact_match(answer_segment, source)
            if citation:
                citations.append(citation)
                continue
            
            # 方法2: 模糊匹配
            citation = self._fuzzy_match(answer_segment, source)
            if citation:
                citations.append(citation)
                continue
            
            # 方法3: 实体匹配
            citation = self._entity_match(answer_segment, source)
            if citation:
                citations.append(citation)
        
        return citations
    
    def _exact_match(self, segment: str, source: Source) -> Optional[Citation]:
        """精确字符串匹配"""
        if segment in source.content:
            # 找到匹配位置
            start = source.content.find(segment)
            
            # 提取上下文
            context_start = max(0, start - 50)
            context_end = min(len(source.content), start + len(segment) + 50)
            context = source.content[context_start:context_end]
            
            return Citation(
                id=f"cite_{source.id}_exact",
                source=source,
                matched_text=segment,
                match_type="exact",
                confidence=1.0,
                answer_segment=segment
            )
        return None
    
    def _fuzzy_match(self, segment: str, source: Source) -> Optional[Citation]:
        """模糊匹配 - 基于相似度"""
        similarity = self._calculate_similarity(segment, source.content)
        
        if similarity >= self.fuzzy_threshold:
            # 找到最相似的片段
            matched_text = self._find_best_match(segment, source.content)
            
            return Citation(
                id=f"cite_{source.id}_fuzzy",
                source=source,
                matched_text=matched_text,
                match_type="fuzzy",
                confidence=similarity,
                answer_segment=segment
            )
        return None
    
    def _entity_match(self, segment: str, source: Source) -> Optional[Citation]:
        """基于实体的匹配"""
        # 提取实体
        entities = self._extract_entities(segment)
        
        if not entities:
            return None
        
        # 检查实体是否在源文档中
        matched_entities = []
        for entity in entities:
            if entity in source.content:
                matched_entities.append(entity)
        
        if len(matched_entities) >= len(entities) * self.entity_threshold:
            return Citation(
                id=f"cite_{source.id}_entity",
                source=source,
                matched_text=", ".join(matched_entities),
                match_type="entity",
                confidence=len(matched_entities) / len(entities),
                answer_segment=segment
            )
        return None
    
    def _calculate_similarity(self, text1: str, text2: str) -> float:
        """计算文本相似度"""
        # 简化的相似度计算
        words1 = set(text1.lower().split())
        words2 = set(text2.lower().split())
        
        if not words1:
            return 0.0
        
        intersection = len(words1 & words2)
        union = len(words1 | words2)
        
        # Jaccard相似度
        jaccard = intersection / union if union > 0 else 0
        
        # 覆盖度
        coverage = intersection / len(words1) if words1 else 0
        
        return 0.5 * jaccard + 0.5 * coverage
    
    def _find_best_match(self, segment: str, content: str) -> str:
        """在内容中找到最佳匹配片段"""
        # 按句子切分
        sentences = re.split(r'[。！？.!?]', content)
        
        best_match = ""
        best_score = 0
        
        for sentence in sentences:
            if len(sentence) < 10:
                continue
            
            score = self._calculate_similarity(segment, sentence)
            if score > best_score:
                best_score = score
                best_match = sentence
        
        return best_match
    
    def _extract_entities(self, text: str) -> List[str]:
        """提取实体"""
        entities = []
        
        # 数字和单位
        numbers = re.findall(r'\d+(?:\.\d+)?\s*(?:mAh|GB|MB|小时|分钟|元|%|年|月|日)', text)
        entities.extend(numbers)
        
        # 专有名词（大写开头）
        proper_nouns = re.findall(r'\b[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*\b', text)
        entities.extend(proper_nouns)
        
        # 引号内容
        quoted = re.findall(r'[""「『]([^""「』」]+)[""』」]', text)
        entities.extend(quoted)
        
        return list(set(entities))


class CitationFormatter:
    """引用格式化器 - 生成各种格式的引用"""
    
    def __init__(self, config: Dict = None):
        self.config = config or {}
        self.format = CitationFormat(self.config.get('format', 'footnote'))
    
    def format_citations(self, answer: str, 
                         citations: List[Citation],
                         format: str = None) -> str:
        """
        格式化带引用的答案
        
        Args:
            answer: 原始答案
            citations: 引用列表
            format: 输出格式
        
        Returns:
            格式化后的文本
        """
        citation_format = CitationFormat(format) if format else self.format
        
        if citation_format == CitationFormat.INLINE:
            return self._format_inline(answer, citations)
        elif citation_format == CitationFormat.FOOTNOTE:
            return self._format_footnote(answer, citations)
        elif citation_format == CitationFormat.DETAILED:
            return self._format_detailed(answer, citations)
        else:
            return self._format_json(answer, citations)
    
    def _format_inline(self, answer: str, citations: List[Citation]) -> str:
        """行内引用格式"""
        result = answer
        
        # 为每个引用添加标记
        for i, citation in enumerate(citations, 1):
            # 在匹配位置添加引用标记
            if citation.answer_segment in result:
                result = result.replace(
                    citation.answer_segment,
                    f"{citation.answer_segment}[^{i}]"
                )
        
        return result
    
    def _format_footnote(self, answer: str, citations: List[Citation]) -> str:
        """脚注格式"""
        # 添加行内引用
        result = self._format_inline(answer, citations)
        
        # 添加脚注区
        footnotes = ["\n\n---\n**引用来源：**\n"]
        
        seen_sources = set()
        for i, citation in enumerate(citations, 1):
            if citation.source.id not in seen_sources:
                seen_sources.add(citation.source.id)
                footnotes.append(
                    f"[^{i}]: {citation.source.title}"
                    f"{f' - {citation.source.location}' if citation.source.location else ''}"
                    f" (置信度: {citation.confidence:.0%})\n"
                )
        
        return result + "".join(footnotes)
    
    def _format_detailed(self, answer: str, citations: List[Citation]) -> str:
        """详细格式"""
        lines = ["## 答案\n"]
        
        # 分句处理
        sentences = re.split(r'([。！？.!?])', answer)
        
        cite_map = {}
        for citation in citations:
            if citation.answer_segment:
                cite_map[citation.answer_segment] = citation
        
        for i in range(0, len(sentences) - 1, 2):
            sentence = sentences[i] + (sentences[i+1] if i+1 < len(sentences) else "")
            
            # 查找匹配的引用
            matched_citation = None
            for seg, cite in cite_map.items():
                if seg in sentence:
                    matched_citation = cite
                    break
            
            if matched_citation:
                lines.append(f"- {sentence}")
                lines.append(f"  - **来源**: {matched_citation.source.title}")
                if matched_citation.source.location:
                    lines.append(f"  - **位置**: {matched_citation.source.location}")
                lines.append(f"  - **原文**: \"{matched_citation.matched_text[:100]}...\"")
                lines.append(f"  - **置信度**: {matched_citation.confidence:.0%}")
            else:
                lines.append(f"- {sentence}")
        
        return "\n".join(lines)
    
    def _format_json(self, answer: str, citations: List[Citation]) -> str:
        """JSON格式"""
        data = {
            "answer": answer,
            "citations": [
                {
                    "id": c.id,
                    "source_id": c.source.id,
                    "source_title": c.source.title,
                    "source_location": c.source.location,
                    "matched_text": c.matched_text,
                    "match_type": c.match_type,
                    "confidence": c.confidence,
                    "answer_segment": c.answer_segment
                }
                for c in citations
            ]
        }
        return json.dumps(data, ensure_ascii=False, indent=2)


class CredibilityScorer:
    """可信度评分器"""
    
    def __init__(self, config: Dict = None):
        self.config = config or {}
    
    def score(self, answer: str, citations: List[Citation]) -> CredibilityScore:
        """
        计算答案的可信度
        
        Args:
            answer: 答案文本
            citations: 引用列表
        
        Returns:
            CredibilityScore: 可信度评分
        """
        if not answer:
            return CredibilityScore(0, 0, 0, 0)
        
        # 1. 来源覆盖率
        source_coverage = self._calc_source_coverage(answer, citations)
        
        # 2. 引用密度
        citation_density = self._calc_citation_density(answer, citations)
        
        # 3. 来源权威度
        source_authority = self._calc_source_authority(citations)
        
        # 4. 综合可信度
        overall = self._calc_overall(source_coverage, citation_density, source_authority)
        
        return CredibilityScore(
            source_coverage=source_coverage,
            citation_density=citation_density,
            source_authority=source_authority,
            overall_credibility=overall,
            details={
                "total_citations": len(citations),
                "exact_matches": sum(1 for c in citations if c.match_type == "exact"),
                "fuzzy_matches": sum(1 for c in citations if c.match_type == "fuzzy"),
                "entity_matches": sum(1 for c in citations if c.match_type == "entity"),
            }
        )
    
    def _calc_source_coverage(self, answer: str, citations: List[Citation]) -> float:
        """计算有引用覆盖的内容占比"""
        if not citations:
            return 0.0
        
        # 统计有引用的字符数
        cited_chars = 0
        seen_segments = set()
        
        for citation in citations:
            if citation.answer_segment and citation.answer_segment not in seen_segments:
                cited_chars += len(citation.answer_segment)
                seen_segments.add(citation.answer_segment)
        
        return min(1.0, cited_chars / len(answer))
    
    def _calc_citation_density(self, answer: str, citations: List[Citation]) -> float:
        """计算引用密度"""
        if not answer:
            return 0.0
        
        # 每千字的引用数
        words = len(answer)
        citation_count = len(citations)
        
        density = (citation_count / words) * 1000 if words > 0 else 0
        
        # 归一化到0-1（假设每千字5个引用为最优）
        return min(1.0, density / 5)
    
    def _calc_source_authority(self, citations: List[Citation]) -> float:
        """计算来源权威度"""
        if not citations:
            return 0.0
        
        # 加权平均权威度
        total_weight = 0
        total_score = 0
        
        for citation in citations:
            weight = citation.confidence
            authority = citation.source.authority_level / 5.0
            total_weight += weight
            total_score += weight * authority
        
        return total_score / total_weight if total_weight > 0 else 0
    
    def _calc_overall(self, coverage: float, density: float, authority: float) -> float:
        """计算综合可信度"""
        # 权重
        w_coverage = 0.4
        w_density = 0.2
        w_authority = 0.4
        
        return coverage * w_coverage + density * w_density + authority * w_authority


class CitationTracker:
    """引用溯源器 - 主入口类"""
    
    def __init__(self, llm_client=None, config: Dict = None):
        """
        初始化引用溯源器
        
        Args:
            llm_client: LLM客户端
            config: 配置参数
        """
        self.config = config or {}
        self.llm = llm_client
        
        # 初始化组件
        self.matcher = CitationMatcher(llm_client, self.config)
        self.formatter = CitationFormatter(self.config)
        self.scorer = CredibilityScorer(self.config)
        
        # 配置
        self.default_format = self.config.get('default_format', 'footnote')
        self.min_confidence = self.config.get('min_confidence', 0.5)
    
    def track(self, answer: str, sources: List[Source],
              format: str = None,
              min_confidence: float = None) -> Dict[str, Any]:
        """
        追踪答案的引用来源
        
        Args:
            answer: 生成的答案
            sources: 源文档列表
            format: 输出格式
            min_confidence: 最低置信度阈值
        
        Returns:
            包含带引用答案和可信度评分的结果
        """
        min_conf = min_confidence or self.min_confidence
        
        # 1. 分句
        segments = self._split_answer(answer)
        
        # 2. 为每个片段匹配引用
        all_citations = []
        for segment in segments:
            if len(segment.strip()) < 5:  # 过滤太短的片段
                continue
            
            citations = self.matcher.match(segment, sources)
            
            # 过滤低置信度引用
            citations = [c for c in citations if c.confidence >= min_conf]
            
            all_citations.extend(citations)
        
        # 3. 去重
        all_citations = self._deduplicate_citations(all_citations)
        
        # 4. 格式化输出
        format_type = format or self.default_format
        formatted = self.formatter.format_citations(answer, all_citations, format_type)
        
        # 5. 计算可信度
        credibility = self.scorer.score(answer, all_citations)
        
        return {
            "original_answer": answer,
            "cited_answer": formatted,
            "citations": [
                {
                    "id": c.id,
                    "source_title": c.source.title,
                    "source_location": c.source.location,
                    "matched_text": c.matched_text[:100] + "..." if len(c.matched_text) > 100 else c.matched_text,
                    "match_type": c.match_type,
                    "confidence": c.confidence
                }
                for c in all_citations
            ],
            "credibility": {
                "overall": credibility.overall_credibility,
                "source_coverage": credibility.source_coverage,
                "citation_density": credibility.citation_density,
                "source_authority": credibility.source_authority,
                "details": credibility.details
            },
            "format": format_type
        }
    
    def _split_answer(self, answer: str) -> List[str]:
        """将答案分割为片段"""
        # 按句号分割
        segments = re.split(r'(?<=[。！？.!?])\s*', answer)
        return [s.strip() for s in segments if s.strip()]
    
    def _deduplicate_citations(self, citations: List[Citation]) -> List[Citation]:
        """去除重复引用"""
        seen = set()
        unique = []
        
        for citation in citations:
            key = (citation.source.id, citation.answer_segment)
            if key not in seen:
                seen.add(key)
                unique.append(citation)
        
        return unique
    
    def track_and_format(self, answer: str, sources: List[Source],
                         format: str = "footnote") -> str:
        """
        便捷方法：直接返回带引用的答案文本
        
        Args:
            answer: 原始答案
            sources: 源文档列表
            format: 输出格式
        
        Returns:
            带引用的答案
        """
        result = self.track(answer, sources, format=format)
        return result["cited_answer"]
    
    def get_credibility_report(self, answer: str, sources: List[Source]) -> str:
        """
        生成可信度报告
        
        Args:
            answer: 答案文本
            sources: 源文档列表
        
        Returns:
            可信度报告文本
        """
        result = self.track(answer, sources)
        cred = result["credibility"]
        
        report = f"""
## 可信度报告

### 综合评分: {cred['overall']:.0%}

#### 详细指标:
- **来源覆盖率**: {cred['source_coverage']:.0%}（答案中有引用支持的比例）
- **引用密度**: {cred['citation_density']:.0%}（引用密集程度）
- **来源权威度**: {cred['source_authority']:.0%}（来源的可靠性）

#### 引用统计:
- 总引用数: {cred['details']['total_citations']}
- 精确匹配: {cred['details']['exact_matches']}
- 模糊匹配: {cred['details']['fuzzy_matches']}
- 实体匹配: {cred['details']['entity_matches']}
"""
        return report


# 使用示例
if __name__ == '__main__':
    # 创建引用溯源器
    tracker = CitationTracker()
    
    # 测试数据
    answer = """
    RAG是一种结合信息检索和生成模型的技术。它能够显著降低大模型的幻觉问题。
    根据研究，RAG可以将准确率从0.3提升到0.85以上。
    相比微调，RAG更新知识的成本更低，大约只有微调的1/10。
    """
    
    sources = [
        Source(
            id="doc_1",
            title="RAG技术白皮书",
            content="""
            RAG（检索增强生成）是一种结合信息检索和生成模型的技术。
            它通过检索相关文档来增强大语言模型的回答能力。
            RAG能够显著降低大模型的幻觉问题。
            """,
            location="第2章",
            authority_level=5
        ),
        Source(
            id="doc_2",
            title="RAG优化指南",
            content="""
            由小到大检索是RAG优化的核心策略之一。
            这种方法可以将准确率从0.3提升到0.85以上。
            相比微调，RAG更新知识的成本更低，大约只有微调的1/10。
            """,
            location="第3章",
            authority_level=4
        )
    ]
    
    # 追踪引用
    result = tracker.track(answer, sources, format="footnote")
    
    print("\n=== 引用溯源结果 ===\n")
    print("带引用的答案:")
    print(result["cited_answer"])
    
    print("\n可信度评分:")
    cred = result["credibility"]
    print(f"  综合可信度: {cred['overall']:.0%}")
    print(f"  来源覆盖率: {cred['source_coverage']:.0%}")
    print(f"  来源权威度: {cred['source_authority']:.0%}")
    
    print("\n引用详情:")
    for cite in result["citations"]:
        print(f"  [{cite['id']}] {cite['source_title']} - {cite['source_location']}")
        print(f"      匹配类型: {cite['match_type']}, 置信度: {cite['confidence']:.0%}")
