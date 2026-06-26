#!/usr/bin/env python3
"""
相关片段提取器（Relevant Segment Extraction）

从检索到的文档块中提取与问题最相关的片段，减少噪声、节省Token

使用方法：
    python segment_extractor.py --query "你的问题" --documents doc1.txt doc2.txt

核心功能：
    1. 多粒度切分：句子级、滑动窗口、语义边界
    2. 相关性评分：向量相似度 + LLM精评
    3. 指代消解：补全片段中缺失的主语
    4. 片段重组：按相关性排序，保持语义连贯
"""

import os
import re
import json
import logging
from dataclasses import dataclass
from typing import List, Dict, Any, Optional, Tuple
from enum import Enum

# 设置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class Granularity(Enum):
    """提取粒度"""
    SENTENCE = "sentence"           # 句子级
    SLIDING_WINDOW = "sliding_window"  # 滑动窗口
    SEMANTIC = "semantic"           # 语义边界


@dataclass
class Segment:
    """片段数据结构"""
    text: str                      # 片段文本
    source_doc: str                # 来源文档
    relevance_score: float         # 相关性得分
    start_pos: int                 # 原文起始位置
    end_pos: int                   # 原文结束位置
    resolved_text: Optional[str]   # 指代消解后的文本


class SegmentSplitter:
    """片段切分器"""
    
    def __init__(self, config: Dict = None):
        self.config = config or {}
        self.granularity = self.config.get('granularity', Granularity.SENTENCE)
        self.window_size = self.config.get('window_size', 100)  # 滑动窗口大小
        self.stride = self.config.get('stride', 50)  # 滑动窗口步长
    
    def split(self, text: str) -> List[Tuple[str, int, int]]:
        """
        切分文本为片段
        
        Args:
            text: 原始文本
        
        Returns:
            [(片段文本, 起始位置, 结束位置), ...]
        """
        if self.granularity == Granularity.SENTENCE:
            return self._split_sentences(text)
        elif self.granularity == Granularity.SLIDING_WINDOW:
            return self._split_sliding_window(text)
        elif self.granularity == Granularity.SEMANTIC:
            return self._split_semantic(text)
        else:
            return [(text, 0, len(text))]
    
    def _split_sentences(self, text: str) -> List[Tuple[str, int, int]]:
        """按句子切分"""
        segments = []
        # 匹配中英文句子结束符
        pattern = r'[^。！？.!?]*[。！？.!?]'
        
        for match in re.finditer(pattern, text):
            sentence = match.group().strip()
            if sentence:
                segments.append((sentence, match.start(), match.end()))
        
        # 处理最后没有结束符的文本
        remaining = text[segments[-1][2]:].strip() if segments else text.strip()
        if remaining:
            segments.append((remaining, len(text) - len(remaining), len(text)))
        
        return segments
    
    def _split_sliding_window(self, text: str) -> List[Tuple[str, int, int]]:
        """滑动窗口切分"""
        segments = []
        start = 0
        
        while start < len(text):
            end = min(start + self.window_size, len(text))
            # 尝试在完整词边界结束
            if end < len(text):
                # 向后找最近的标点或空格
                while end < len(text) and text[end] not in '。！？.!? \n':
                    end += 1
                end = min(end, start + self.window_size * 2)  # 限制最大长度
            
            segment = text[start:end].strip()
            if segment:
                segments.append((segment, start, end))
            
            start += self.stride
        
        return segments
    
    def _split_semantic(self, text: str) -> List[Tuple[str, int, int]]:
        """按语义边界切分（简化实现）"""
        # 先按段落切分
        paragraphs = text.split('\n\n')
        segments = []
        pos = 0
        
        for para in paragraphs:
            para = para.strip()
            if para:
                # 每个段落再按句子细分
                para_segments = self._split_sentences(para)
                for seg, s_start, s_end in para_segments:
                    segments.append((seg, pos + s_start, pos + s_end))
                pos += len(para) + 2  # +2 for \n\n
        
        return segments


class RelevanceScorer:
    """相关性评分器"""
    
    def __init__(self, llm_client=None, embedding_model=None, config: Dict = None):
        self.llm = llm_client
        self.embedding_model = embedding_model
        self.config = config or {}
        self.score_mode = self.config.get('score_mode', 'hybrid')  # vector / llm / hybrid
        self.vector_threshold = self.config.get('vector_threshold', 0.3)
    
    def score(self, query: str, segment: str) -> float:
        """
        计算片段与查询的相关性得分
        
        Args:
            query: 用户查询
            segment: 片段文本
        
        Returns:
            相关性得分 (0-1)
        """
        if self.score_mode == 'vector':
            return self._vector_score(query, segment)
        elif self.score_mode == 'llm':
            return self._llm_score(query, segment)
        else:  # hybrid
            vector_score = self._vector_score(query, segment)
            # 向量得分高的才用LLM精评
            if vector_score >= self.vector_threshold:
                llm_score = self._llm_score(query, segment)
                return 0.3 * vector_score + 0.7 * llm_score
            return vector_score
    
    def _vector_score(self, query: str, segment: str) -> float:
        """使用向量相似度评分"""
        try:
            if self.embedding_model:
                from sentence_transformers import SentenceTransformer
                import numpy as np
                
                q_embedding = self.embedding_model.encode(query)
                s_embedding = self.embedding_model.encode(segment)
                
                similarity = np.dot(q_embedding, s_embedding) / (
                    np.linalg.norm(q_embedding) * np.linalg.norm(s_embedding)
                )
                return float(similarity)
            
            # 没有嵌入模型，使用简单的关键词匹配
            query_words = set(query.lower().split())
            segment_words = set(segment.lower().split())
            
            if not query_words:
                return 0.0
            
            overlap = len(query_words & segment_words) / len(query_words)
            return overlap
            
        except Exception as e:
            logger.error(f"向量评分失败: {e}")
            return 0.0
    
    def _llm_score(self, query: str, segment: str) -> float:
        """使用LLM评分"""
        if not self.llm:
            return 0.5
        
        try:
            prompt = f"""
请评估以下文本片段与用户问题的相关性（0-1分）：

用户问题：{query}

文本片段：{segment[:300]}

评分标准：
- 1.0: 片段直接回答了问题
- 0.7-0.9: 片段包含相关信息
- 0.4-0.6: 片段与问题有一定关联
- 0.0-0.3: 片段与问题无关

只返回一个0到1之间的数字。
"""
            
            response = self.llm.invoke(prompt) if hasattr(self.llm, 'invoke') else self.llm(prompt)
            score_text = response.strip() if isinstance(response, str) else str(response)
            score = float(''.join(c for c in score_text if c.isdigit() or c == '.'))
            return max(0.0, min(1.0, score))
            
        except Exception as e:
            logger.error(f"LLM评分失败: {e}")
            return 0.5


class ReferenceResolver:
    """指代消解器"""
    
    def __init__(self, llm_client=None, config: Dict = None):
        self.llm = llm_client
        self.config = config or {}
    
    def resolve(self, segment: str, context: str) -> str:
        """
        消除片段中的指代，补全主语
        
        Args:
            segment: 片段文本
            context: 上下文（用于识别被指代的实体）
        
        Returns:
            消解后的文本
        """
        if not self.llm:
            return segment
        
        # 检测是否包含指代词
        pronouns = ['它', '他', '她', '其', '这', '那', '该', '此']
        if not any(p in segment for p in pronouns):
            return segment
        
        try:
            prompt = f"""
请对以下文本片段进行指代消解，将代词替换为实际实体：

上下文：{context[:500]}

片段：{segment}

要求：
1. 识别片段中的代词（它、他、她、其、这、那、该、此等）
2. 根据上下文确定代词指代的实体
3. 将代词替换为实际实体名称
4. 如果无法确定，保留原样

输出：消解后的文本（只输出文本，不要解释）
"""
            
            response = self.llm.invoke(prompt) if hasattr(self.llm, 'invoke') else self.llm(prompt)
            return response.strip() if isinstance(response, str) else segment
            
        except Exception as e:
            logger.error(f"指代消解失败: {e}")
            return segment


class RelevantSegmentExtractor:
    """相关片段提取器"""
    
    def __init__(self, llm_client=None, embedding_model=None, config: Dict = None):
        """
        初始化提取器
        
        Args:
            llm_client: LLM客户端
            embedding_model: 嵌入模型
            config: 配置参数
        """
        self.config = config or {}
        
        # 初始化组件
        self.splitter = SegmentSplitter(self.config)
        self.scorer = RelevanceScorer(llm_client, embedding_model, self.config)
        self.resolver = ReferenceResolver(llm_client, self.config)
        
        # 配置参数
        self.max_segments = self.config.get('max_segments', 10)
        self.min_relevance = self.config.get('min_relevance', 0.4)
        self.enable_resolution = self.config.get('enable_resolution', True)
    
    def extract(self, query: str, documents: List[str]) -> List[Segment]:
        """
        从文档中提取与查询相关的片段
        
        Args:
            query: 用户查询
            documents: 文档列表
        
        Returns:
            相关片段列表（按相关性排序）
        """
        all_segments = []
        
        for doc_idx, doc in enumerate(documents):
            # 1. 切分片段
            raw_segments = self.splitter.split(doc)
            
            for text, start, end in raw_segments:
                # 2. 计算相关性得分
                score = self.scorer.score(query, text)
                
                # 3. 筛选相关片段
                if score >= self.min_relevance:
                    # 4. 指代消解
                    resolved = None
                    if self.enable_resolution:
                        resolved = self.resolver.resolve(text, doc)
                    
                    all_segments.append(Segment(
                        text=text,
                        source_doc=f"doc_{doc_idx}",
                        relevance_score=score,
                        start_pos=start,
                        end_pos=end,
                        resolved_text=resolved
                    ))
        
        # 5. 排序并返回TopK
        all_segments.sort(key=lambda x: x.relevance_score, reverse=True)
        return all_segments[:self.max_segments]
    
    def extract_and_compose(self, query: str, documents: List[str]) -> str:
        """
        提取片段并重组为连贯文本
        
        Args:
            query: 用户查询
            documents: 文档列表
        
        Returns:
            重组后的相关内容文本
        """
        segments = self.extract(query, documents)
        
        if not segments:
            return ""
        
        # 使用消解后的文本
        texts = [s.resolved_text or s.text for s in segments]
        
        # 去重并保持顺序
        seen = set()
        unique_texts = []
        for t in texts:
            if t not in seen:
                seen.add(t)
                unique_texts.append(t)
        
        return '\n'.join(unique_texts)
    
    def get_context_for_llm(self, query: str, documents: List[str], 
                            max_length: int = 2000) -> str:
        """
        获取适合LLM输入的相关上下文
        
        Args:
            query: 用户查询
            documents: 文档列表
            max_length: 最大长度（字符数）
        
        Returns:
            裁剪后的上下文文本
        """
        segments = self.extract(query, documents)
        
        context_parts = []
        current_length = 0
        
        for seg in segments:
            text = seg.resolved_text or seg.text
            
            if current_length + len(text) > max_length:
                break
            
            context_parts.append(text)
            current_length += len(text)
        
        return '\n'.join(context_parts)


# 使用示例
if __name__ == '__main__':
    # 示例配置
    config = {
        'granularity': Granularity.SENTENCE,
        'score_mode': 'hybrid',
        'max_segments': 10,
        'min_relevance': 0.3,
        'enable_resolution': True
    }
    
    # 创建提取器
    extractor = RelevantSegmentExtractor(config=config)
    
    # 测试文档
    documents = [
        """
        RAG（检索增强生成）是一种结合信息检索和生成模型的技术。
        它通过检索相关文档来增强大语言模型的回答能力。
        RAG能够显著降低大模型的幻觉问题。
        相比微调，RAG更新知识的成本更低，大约只有微调的1/10。
        RAG系统的优化策略包括语义分块、重排序、混合检索等。
        """,
        """
        由小到大检索是RAG优化的核心策略之一。
        它的原理是用小块检索，返回大块上下文。
        这种方法可以将准确率从0.3提升到0.85以上。
        它能够同时保证检索精度和上下文完整性。
        """
    ]
    
    # 测试提取
    query = "RAG有什么优势？"
    segments = extractor.extract(query, documents)
    
    print(f"\n=== 查询: {query} ===\n")
    print("提取的相关片段：")
    for i, seg in enumerate(segments, 1):
        print(f"\n[{i}] 相关性: {seg.relevance_score:.2f}")
        print(f"原文: {seg.text}")
        if seg.resolved_text and seg.resolved_text != seg.text:
            print(f"消解后: {seg.resolved_text}")
    
    # 测试重组
    print("\n=== 重组后的上下文 ===")
    context = extractor.extract_and_compose(query, documents)
    print(context)
