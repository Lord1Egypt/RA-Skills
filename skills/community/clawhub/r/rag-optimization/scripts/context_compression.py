#!/usr/bin/env python3
"""
上下文压缩器（Context Compression）

压缩检索到的文档内容，减少Token消耗、降低噪声

使用方法：
    python context_compression.py --query "你的问题" --documents doc1.txt doc2.txt

核心功能：
    1. 提取式压缩：选择重要句子，去除冗余
    2. 摘要式压缩：LLM生成精简摘要
    3. 混合压缩：先提取再摘要
    4. 实体保护：确保关键数字/名称不被丢失
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


class CompressionMode(Enum):
    """压缩模式"""
    EXTRACTIVE = "extractive"      # 提取式：选择重要句子
    ABSTRACTIVE = "abstractive"    # 摘要式：LLM生成摘要
    HYBRID = "hybrid"              # 混合式：先提取再摘要


@dataclass
class CompressionResult:
    """压缩结果"""
    compressed_text: str              # 压缩后的文本
    original_length: int              # 原始长度
    compressed_length: int            # 压缩后长度
    compression_ratio: float          # 压缩比例
    preserved_entities: List[str]     # 保留的实体
    key_sentences: List[str]          # 关键句子
    mode: str                         # 压缩模式
    quality_score: float = 1.0        # 质量评分


@dataclass
class Entity:
    """实体数据结构"""
    text: str              # 实体文本
    type: str              # 实体类型
    start: int             # 起始位置
    end: int               # 结束位置
    must_preserve: bool = True  # 是否必须保留


class EntityProtector:
    """实体保护器 - 确保关键信息不被压缩丢失"""
    
    # 必须保护的实体类型
    PROTECTED_TYPES = {
        "NUMBER",       # 数字：1000mAh, 2小时, 2024年
        "DATE",         # 日期：2024年1月, 1月15日
        "PRODUCT",      # 产品名：iPhone 15, Model X
        "PERSON",       # 人名
        "ORG",          # 组织名：OpenAI, Google
        "MONEY",        # 金额：$100, 100元
        "PERCENT",      # 百分比：50%, 0.85
        "URL",          # 网址
    }
    
    def __init__(self, config: Dict = None):
        self.config = config or {}
        self.custom_entities = self.config.get('custom_entities', [])
    
    def extract_entities(self, text: str) -> List[Entity]:
        """
        从文本中提取需要保护的实体
        
        Args:
            text: 输入文本
        
        Returns:
            实体列表
        """
        entities = []
        
        # 1. 数字实体（包括单位）
        number_patterns = [
            r'\d+(?:\.\d+)?\s*(?:mAh|GB|MB|KB|TB|Hz|GHz|MHz|mm|cm|m|km|g|kg|ml|L|小时|分钟|秒|天|周|月|年|元|美元|%)',
            r'\d+(?:\.\d+)?%',  # 百分比
            r'\d{4}年(?:\d{1,2}月)?(?:\d{1,2}日)?',  # 日期
            r'\d{1,2}:\d{2}(?::\d{2})?',  # 时间
        ]
        
        for pattern in number_patterns:
            for match in re.finditer(pattern, text):
                entities.append(Entity(
                    text=match.group(),
                    type="NUMBER",
                    start=match.start(),
                    end=match.end(),
                    must_preserve=True
                ))
        
        # 2. 产品名/专有名词（大写开头的英文词组）
        product_pattern = r'\b[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*\b'
        for match in re.finditer(product_pattern, text):
            entity_text = match.group()
            # 排除常见句首词
            if entity_text not in ['The', 'This', 'That', 'These', 'Those', 'What', 'When', 'Where', 'Why', 'How']:
                entities.append(Entity(
                    text=entity_text,
                    type="PRODUCT",
                    start=match.start(),
                    end=match.end(),
                    must_preserve=True
                ))
        
        # 3. 中文专有名词（引号内）
        quoted_pattern = r'[""「『]([^""「』」\\s]+)[""』」]'
        for match in re.finditer(quoted_pattern, text):
            entities.append(Entity(
                text=match.group(1),
                type="PRODUCT",
                start=match.start(),
                end=match.end(),
                must_preserve=True
            ))
        
        # 4. URL
        url_pattern = r'https?://[^\s]+'
        for match in re.finditer(url_pattern, text):
            entities.append(Entity(
                text=match.group(),
                type="URL",
                start=match.start(),
                end=match.end(),
                must_preserve=True
            ))
        
        # 5. 自定义实体
        for custom in self.custom_entities:
            if custom in text:
                for match in re.finditer(re.escape(custom), text):
                    entities.append(Entity(
                        text=custom,
                        type="CUSTOM",
                        start=match.start(),
                        end=match.end(),
                        must_preserve=True
                    ))
        
        # 去重
        seen = set()
        unique_entities = []
        for e in entities:
            if e.text not in seen:
                seen.add(e.text)
                unique_entities.append(e)
        
        return unique_entities
    
    def check_preservation(self, original: str, compressed: str) -> Tuple[bool, List[str]]:
        """
        检查关键实体是否被保留
        
        Args:
            original: 原始文本
            compressed: 压缩后文本
        
        Returns:
            (是否全部保留, 缺失的实体列表)
        """
        original_entities = self.extract_entities(original)
        missing = []
        
        for entity in original_entities:
            if entity.must_preserve and entity.text not in compressed:
                missing.append(entity.text)
        
        return len(missing) == 0, missing


class SentenceExtractor:
    """句子提取器 - 用于提取式压缩"""
    
    def __init__(self, llm_client=None, embedding_model=None, config: Dict = None):
        self.llm = llm_client
        self.embedding_model = embedding_model
        self.config = config or {}
    
    def split_sentences(self, text: str) -> List[str]:
        """
        将文本切分为句子
        
        Args:
            text: 输入文本
        
        Returns:
            句子列表
        """
        # 匹配中英文句子结束符
        pattern = r'[^。！？.!?]+[。！？.!?]'
        sentences = []
        
        for match in re.finditer(pattern, text):
            sentence = match.group().strip()
            if sentence and len(sentence) > 5:  # 过滤过短的句子
                sentences.append(sentence)
        
        # 处理剩余文本
        remaining = text[match.end():].strip() if 'match' in dir() else text.strip()
        if remaining and len(remaining) > 5:
            sentences.append(remaining)
        
        return sentences
    
    def score_sentence(self, sentence: str, query: str, context: str = "") -> float:
        """
        计算句子的重要性得分
        
        Args:
            sentence: 待评分句子
            query: 用户查询
            context: 上下文
        
        Returns:
            重要性得分 (0-1)
        """
        score = 0.0
        
        # 1. 查询词覆盖度
        query_words = set(query.lower().split())
        sentence_words = set(sentence.lower().split())
        if query_words:
            coverage = len(query_words & sentence_words) / len(query_words)
            score += 0.3 * coverage
        
        # 2. 信息密度（数字、实体数量）
        numbers = len(re.findall(r'\d+(?:\.\d+)?', sentence))
        score += min(0.2, numbers * 0.05)
        
        # 3. 句子位置（首尾句更重要）
        # 由外部调用时处理
        
        # 4. LLM评分（如果可用）
        if self.llm:
            llm_score = self._llm_score(sentence, query)
            score = 0.5 * score + 0.5 * llm_score
        
        return min(1.0, score)
    
    def _llm_score(self, sentence: str, query: str) -> float:
        """使用LLM评分"""
        if not self.llm:
            return 0.5
        
        try:
            prompt = f"""
请评估以下句子对于回答用户问题的重要性（0-1分）：

用户问题：{query}

句子：{sentence}

评分标准：
- 1.0: 直接回答问题的关键信息
- 0.7-0.9: 包含重要相关信息
- 0.4-0.6: 有一定关联
- 0.0-0.3: 无关或冗余

只返回一个0到1之间的数字。
"""
            
            response = self.llm.invoke(prompt) if hasattr(self.llm, 'invoke') else self.llm(prompt)
            score_text = response.strip() if isinstance(response, str) else str(response)
            
            # 提取数字
            match = re.search(r'[\d.]+', score_text)
            if match:
                return float(match.group())
            return 0.5
            
        except Exception as e:
            logger.error(f"LLM评分失败: {e}")
            return 0.5
    
    def extract_key_sentences(self, text: str, query: str, 
                              target_count: int = None,
                              min_score: float = 0.3) -> List[Tuple[str, float]]:
        """
        提取关键句子
        
        Args:
            text: 输入文本
            query: 用户查询
            target_count: 目标句子数
            min_score: 最低分数阈值
        
        Returns:
            [(句子, 得分), ...]
        """
        sentences = self.split_sentences(text)
        
        # 计算每句得分
        scored = []
        for i, sentence in enumerate(sentences):
            score = self.score_sentence(sentence, query, text)
            
            # 首尾句加权
            if i == 0 or i == len(sentences) - 1:
                score = min(1.0, score * 1.2)
            
            scored.append((sentence, score))
        
        # 按得分排序
        scored.sort(key=lambda x: x[1], reverse=True)
        
        # 过滤低分句子
        filtered = [(s, sc) for s, sc in scored if sc >= min_score]
        
        # 返回指定数量
        if target_count:
            return filtered[:target_count]
        
        return filtered


class AbstractiveCompressor:
    """摘要式压缩器 - 使用LLM生成精简摘要"""
    
    def __init__(self, llm_client=None, config: Dict = None):
        self.llm = llm_client
        self.config = config or {}
        self.max_summary_length = self.config.get('max_summary_length', 500)
    
    def compress(self, text: str, query: str, 
                 target_length: int = None,
                 preserved_entities: List[str] = None) -> str:
        """
        使用LLM生成摘要
        
        Args:
            text: 输入文本
            query: 用户查询
            target_length: 目标长度
            preserved_entities: 必须保留的实体
        
        Returns:
            压缩后的文本
        """
        if not self.llm:
            logger.warning("LLM客户端未配置，返回原文")
            return text[:target_length] if target_length else text
        
        target_length = target_length or self.max_summary_length
        preserved_str = ""
        if preserved_entities:
            preserved_str = f"\n\n必须保留的关键信息：{', '.join(preserved_entities)}"
        
        prompt = f"""
请将以下文本压缩为{target_length}字以内的精简摘要，用于回答用户问题。

用户问题：{query}
{preserved_str}

原始文本：
{text[:2000]}

压缩要求：
1. 保留与问题直接相关的核心信息
2. 保留所有数字、日期、专有名词
3. 去除冗余和无关内容
4. 保持语义连贯
5. 输出压缩后的文本，不要解释

压缩后文本：
"""
        
        try:
            response = self.llm.invoke(prompt) if hasattr(self.llm, 'invoke') else self.llm(prompt)
            compressed = response.strip() if isinstance(response, str) else str(response)
            return compressed
            
        except Exception as e:
            logger.error(f"LLM摘要失败: {e}")
            return text[:target_length] if target_length else text


class ContextCompressor:
    """上下文压缩器 - 主入口类"""
    
    def __init__(self, llm_client=None, embedding_model=None, config: Dict = None):
        """
        初始化压缩器
        
        Args:
            llm_client: LLM客户端
            embedding_model: 嵌入模型
            config: 配置参数
        """
        self.config = config or {}
        self.llm = llm_client
        self.embedding_model = embedding_model
        
        # 初始化组件
        self.entity_protector = EntityProtector(self.config)
        self.sentence_extractor = SentenceExtractor(llm_client, embedding_model, self.config)
        self.abstractive_compressor = AbstractiveCompressor(llm_client, self.config)
        
        # 配置参数
        self.mode = CompressionMode(self.config.get('mode', 'hybrid'))
        self.target_ratio = self.config.get('compression_ratio', 0.5)
        self.max_output_length = self.config.get('max_output_length', 2000)
        self.min_output_length = self.config.get('min_output_length', 200)
    
    def compress(self, documents: List[str], query: str,
                 mode: str = None,
                 target_length: int = None,
                 preserve_entities: bool = True) -> CompressionResult:
        """
        压缩文档内容
        
        Args:
            documents: 文档列表
            query: 用户查询
            mode: 压缩模式（覆盖默认配置）
            target_length: 目标长度
            preserve_entities: 是否保护实体
        
        Returns:
            CompressionResult: 压缩结果
        """
        # 合并文档
        combined_text = "\n\n---\n\n".join(documents)
        original_length = len(combined_text)
        
        # 确定目标长度
        if not target_length:
            target_length = max(
                self.min_output_length,
                min(int(original_length * self.target_ratio), self.max_output_length)
            )
        
        # 确定压缩模式
        compression_mode = CompressionMode(mode) if mode else self.mode
        
        # 提取需要保护的实体
        preserved_entities = []
        if preserve_entities:
            all_entities = []
            for doc in documents:
                all_entities.extend(self.entity_protector.extract_entities(doc))
            preserved_entities = list(set(e.text for e in all_entities if e.must_preserve))
        
        # 根据模式执行压缩
        if compression_mode == CompressionMode.EXTRACTIVE:
            compressed, key_sentences = self._extractive_compress(
                combined_text, query, target_length
            )
        elif compression_mode == CompressionMode.ABSTRACTIVE:
            compressed = self._abstractive_compress(
                combined_text, query, target_length, preserved_entities
            )
            key_sentences = []
        else:  # HYBRID
            compressed, key_sentences = self._hybrid_compress(
                combined_text, query, target_length, preserved_entities
            )
        
        # 验证实体保留
        all_preserved, missing = self.entity_protector.check_preservation(
            combined_text, compressed
        )
        
        # 如果有实体丢失，尝试补充
        if missing:
            compressed = self._add_missing_entities(compressed, missing, query)
        
        # 计算质量分数
        quality_score = self._calculate_quality(
            original=combined_text,
            compressed=compressed,
            query=query,
            entities_preserved=all_preserved
        )
        
        return CompressionResult(
            compressed_text=compressed,
            original_length=original_length,
            compressed_length=len(compressed),
            compression_ratio=len(compressed) / original_length if original_length > 0 else 0,
            preserved_entities=preserved_entities,
            key_sentences=key_sentences,
            mode=compression_mode.value,
            quality_score=quality_score
        )
    
    def _extractive_compress(self, text: str, query: str, 
                              target_length: int) -> Tuple[str, List[str]]:
        """提取式压缩"""
        # 估计需要的句子数
        avg_sentence_length = 50
        target_count = target_length // avg_sentence_length + 1
        
        # 提取关键句子
        key_sentences = self.sentence_extractor.extract_key_sentences(
            text, query, target_count=target_count
        )
        
        # 组装压缩文本
        compressed_parts = []
        current_length = 0
        
        for sentence, score in key_sentences:
            if current_length + len(sentence) <= target_length:
                compressed_parts.append(sentence)
                current_length += len(sentence)
        
        compressed = "".join(compressed_parts)
        return compressed, [s for s, _ in key_sentences[:10]]
    
    def _abstractive_compress(self, text: str, query: str,
                               target_length: int,
                               preserved_entities: List[str]) -> str:
        """摘要式压缩"""
        return self.abstractive_compressor.compress(
            text, query, target_length, preserved_entities
        )
    
    def _hybrid_compress(self, text: str, query: str,
                          target_length: int,
                          preserved_entities: List[str]) -> Tuple[str, List[str]]:
        """混合压缩：先提取关键句子，再用LLM精炼"""
        # 第一步：提取式压缩（获取双倍长度）
        extract_target = min(target_length * 2, len(text) * 0.7)
        extracted, key_sentences = self._extractive_compress(
            text, query, int(extract_target)
        )
        
        # 第二步：LLM摘要精炼
        if self.llm:
            compressed = self.abstractive_compressor.compress(
                extracted, query, target_length, preserved_entities
            )
        else:
            compressed = extracted[:target_length]
        
        return compressed, key_sentences
    
    def _add_missing_entities(self, compressed: str, missing: List[str], 
                               query: str) -> str:
        """补充丢失的实体"""
        if not missing:
            return compressed
        
        # 在末尾添加缺失的关键实体
        additions = f"\n\n关键数据：{', '.join(missing)}"
        return compressed + additions
    
    def _calculate_quality(self, original: str, compressed: str,
                           query: str, entities_preserved: bool) -> float:
        """计算压缩质量分数"""
        score = 0.0
        
        # 1. 压缩比例合理性（0.3-0.7最佳）
        ratio = len(compressed) / len(original) if original else 0
        if 0.3 <= ratio <= 0.7:
            score += 0.3
        elif 0.2 <= ratio <= 0.8:
            score += 0.2
        else:
            score += 0.1
        
        # 2. 实体保留
        if entities_preserved:
            score += 0.3
        else:
            score += 0.1
        
        # 3. 查询相关性（简单检查）
        query_words = set(query.lower().split())
        compressed_words = set(compressed.lower().split())
        relevance = len(query_words & compressed_words) / len(query_words) if query_words else 0
        score += 0.4 * relevance
        
        return min(1.0, score)
    
    def compress_for_llm(self, documents: List[str], query: str,
                         max_tokens: int = 4000,
                         mode: str = "hybrid") -> str:
        """
        便捷方法：直接返回适合LLM输入的压缩文本
        
        Args:
            documents: 文档列表
            query: 用户查询
            max_tokens: 最大Token数（约等于字符数/2）
            mode: 压缩模式
        
        Returns:
            压缩后的文本
        """
        result = self.compress(
            documents=documents,
            query=query,
            mode=mode,
            target_length=max_tokens * 2,  # Token转字符
            preserve_entities=True
        )
        return result.compressed_text


# 使用示例
if __name__ == '__main__':
    # 示例配置
    config = {
        'mode': 'hybrid',
        'compression_ratio': 0.5,
        'max_output_length': 1000,
    }
    
    # 创建压缩器
    compressor = ContextCompressor(config=config)
    
    # 测试文档
    documents = [
        """
        RAG（检索增强生成）是一种结合信息检索和生成模型的技术。
        它通过检索相关文档来增强大语言模型的回答能力。
        RAG能够显著降低大模型的幻觉问题，根据研究报告降低率可达50%以上。
        相比微调，RAG更新知识的成本更低，大约只有微调的1/10。
        RAG系统的优化策略包括语义分块、重排序、混合检索等多种方法。
        由小到大检索是RAG优化的核心策略之一，准确率可从0.3提升到0.85。
        """,
        """
        产品规格参数：
        - 电池容量：5000mAh
        - 充电功率：65W快充
        - 充电时间：约45分钟充满
        - 上市时间：2024年3月
        - 建议售价：2999元
        """
    ]
    
    # 测试压缩
    query = "这个产品的充电参数是什么？RAG技术有什么优势？"
    result = compressor.compress(documents, query)
    
    print("\n=== 上下文压缩结果 ===\n")
    print(f"原始长度: {result.original_length} 字符")
    print(f"压缩后长度: {result.compressed_length} 字符")
    print(f"压缩比例: {result.compression_ratio:.1%}")
    print(f"压缩模式: {result.mode}")
    print(f"质量分数: {result.quality_score:.2f}")
    print(f"\n保留的实体: {result.preserved_entities}")
    print(f"\n压缩后文本:\n{result.compressed_text}")
