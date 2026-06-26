#!/usr/bin/env python3
"""
命题分块器（Proposition Chunking）

将文档拆解为最小的事实单元（命题），每个命题独立可检索

使用方法：
    python proposition_chunker.py --input documents/ --output chunks/

核心功能：
    1. 命题识别：识别文档中的独立事实/观点
    2. 指代消解：补全命题中缺失的主语/宾语
    3. 父子映射：维护命题与原文段落的关联
    4. 去重聚合：处理相似或重复的命题
"""

import os
import re
import json
import logging
from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional, Set
from collections import defaultdict

# 设置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


@dataclass
class Proposition:
    """命题数据结构"""
    id: str                           # 命题ID
    content: str                      # 命题内容
    original_text: str                # 原始文本
    parent_paragraph: str             # 父段落
    metadata: Dict[str, Any] = field(default_factory=dict)  # 元数据
    
    # 命题属性
    is_atomic: bool = True            # 是否原子性（只表达一个事实）
    is_self_contained: bool = True    # 是否自包含（不需要额外上下文）
    entities: List[str] = field(default_factory=list)  # 涉及的实体
    confidence: float = 1.0           # 提取置信度


class PropositionExtractor:
    """命题提取器"""
    
    def __init__(self, llm_client=None, config: Dict = None):
        """
        初始化命题提取器
        
        Args:
            llm_client: LLM客户端
            config: 配置参数
        """
        self.llm = llm_client
        self.config = config or {}
        
        # 命题长度限制
        self.min_length = self.config.get('min_proposition_length', 15)
        self.max_length = self.config.get('max_proposition_length', 150)
        
        # 提取模式：strict / relaxed
        self.mode = self.config.get('mode', 'strict')
    
    def extract(self, text: str) -> List[Proposition]:
        """
        从文本中提取命题
        
        Args:
            text: 输入文本
        
        Returns:
            命题列表
        """
        if not self.llm:
            # 无LLM时使用规则方法
            return self._rule_based_extract(text)
        
        return self._llm_extract(text)
    
    def _llm_extract(self, text: str) -> List[Proposition]:
        """使用LLM提取命题"""
        propositions = []
        
        try:
            prompt = f"""
请将以下文本拆分为独立的事实陈述（命题）。

文本：
{text}

提取规则：
1. 每个命题只表达一个独立的事实或观点
2. 命题应该是原子性的，不可再分
3. 命题应该是自包含的，不需要额外上下文就能理解
4. 保持原文的准确性，不要添加或删减信息
5. 补全缺失的主语（将代词替换为实际实体）

输出格式：
每行一个命题，格式为：命题内容

示例：
原文："RAG是一种技术。它能降低幻觉。"
输出：
RAG是一种技术
RAG能降低幻觉
"""
            
            response = self.llm.invoke(prompt) if hasattr(self.llm, 'invoke') else self.llm(prompt)
            response_text = response.strip() if isinstance(response, str) else str(response)
            
            # 解析结果
            for i, line in enumerate(response_text.strip().split('\n')):
                line = line.strip()
                # 去除编号
                line = re.sub(r'^\d+[\.\)、]\s*', '', line)
                
                if not line or len(line) < self.min_length:
                    continue
                
                # 验证命题
                if self._validate_proposition(line):
                    propositions.append(Proposition(
                        id=f"prop_{len(propositions)}",
                        content=line,
                        original_text=text,
                        parent_paragraph=text,
                        is_atomic=self._check_atomicity(line),
                        is_self_contained=self._check_self_containment(line)
                    ))
            
            return propositions
            
        except Exception as e:
            logger.error(f"LLM提取失败: {e}")
            return self._rule_based_extract(text)
    
    def _rule_based_extract(self, text: str) -> List[Proposition]:
        """基于规则的命题提取（无LLM时的备选方案）"""
        propositions = []
        
        # 按句子切分
        sentences = self._split_sentences(text)
        
        for i, sentence in enumerate(sentences):
            # 检查是否是复合句
            sub_propositions = self._try_split_compound(sentence)
            
            if sub_propositions:
                for sub in sub_propositions:
                    if len(sub) >= self.min_length:
                        propositions.append(Proposition(
                            id=f"prop_{len(propositions)}",
                            content=sub,
                            original_text=sentence,
                            parent_paragraph=text,
                            is_atomic=True,
                            is_self_contained=self._check_self_containment(sub)
                        ))
            elif len(sentence) >= self.min_length:
                propositions.append(Proposition(
                    id=f"prop_{len(propositions)}",
                    content=sentence,
                    original_text=sentence,
                    parent_paragraph=text,
                    is_atomic=self._check_atomicity(sentence),
                    is_self_contained=self._check_self_containment(sentence)
                ))
        
        return propositions
    
    def _split_sentences(self, text: str) -> List[str]:
        """切分句子"""
        # 匹配中英文句子结束符
        pattern = r'[^。！？.!?]*[。！？.!?]'
        sentences = []
        
        for match in re.finditer(pattern, text):
            sentence = match.group().strip()
            if sentence:
                sentences.append(sentence)
        
        return sentences
    
    def _try_split_compound(self, sentence: str) -> List[str]:
        """尝试拆分复合句"""
        # 常见的复合句连接词
        connectors = ['，并且', '，而且', '，同时', '，另外', '，此外', 
                      ', and ', ', but ', ', while ']
        
        for conn in connectors:
            if conn in sentence:
                parts = sentence.split(conn)
                if len(parts) > 1:
                    # 确保每部分都是完整命题
                    return [p.strip() for p in parts if len(p.strip()) >= self.min_length]
        
        return []
    
    def _validate_proposition(self, text: str) -> bool:
        """验证是否是有效的命题"""
        # 长度检查
        if len(text) < self.min_length or len(text) > self.max_length:
            return False
        
        # 必须以句号等结束
        if not text.endswith(('。', '！', '？', '.', '!', '?')):
            return False
        
        return True
    
    def _check_atomicity(self, text: str) -> bool:
        """检查命题的原子性"""
        # 简单判断：不包含多个并列子句
        compound_indicators = ['，并且', '，而且', '，同时', '，另外']
        return not any(ind in text for ind in compound_indicators)
    
    def _check_self_containment(self, text: str) -> bool:
        """检查命题的自包含性"""
        # 检查是否包含代词
        pronouns = ['它', '他', '她', '其', '这', '那', '该', '此']
        return not any(p in text for p in pronouns)


class ReferenceResolver:
    """指代消解器"""
    
    def __init__(self, llm_client=None, config: Dict = None):
        self.llm = llm_client
        self.config = config or {}
    
    def resolve(self, proposition: Proposition, context: str) -> Proposition:
        """
        消除命题中的指代
        
        Args:
            proposition: 命题对象
            context: 上下文文本
        
        Returns:
            消解后的命题对象
        """
        # 检查是否需要消解
        pronouns = ['它', '他', '她', '其', '这', '那', '该', '此']
        if not any(p in proposition.content for p in pronouns):
            return proposition
        
        if not self.llm:
            return proposition
        
        try:
            prompt = f"""
请对以下命题进行指代消解：

上下文：{context[:500]}

命题：{proposition.content}

要求：
1. 识别命题中的代词
2. 根据上下文确定代词指代的实体
3. 将代词替换为实际实体名称
4. 保持句子通顺

只输出消解后的命题，不要解释。
"""
            
            response = self.llm.invoke(prompt) if hasattr(self.llm, 'invoke') else self.llm(prompt)
            resolved = response.strip() if isinstance(response, str) else proposition.content
            
            # 创建新的命题对象
            return Proposition(
                id=proposition.id,
                content=resolved,
                original_text=proposition.original_text,
                parent_paragraph=proposition.parent_paragraph,
                metadata={**proposition.metadata, 'resolved_from': proposition.content},
                is_atomic=proposition.is_atomic,
                is_self_contained=True  # 消解后应该是自包含的
            )
            
        except Exception as e:
            logger.error(f"指代消解失败: {e}")
            return proposition


class PropositionDeduplicator:
    """命题去重器"""
    
    def __init__(self, config: Dict = None):
        self.config = config or {}
        self.similarity_threshold = self.config.get('similarity_threshold', 0.9)
    
    def deduplicate(self, propositions: List[Proposition]) -> List[Proposition]:
        """
        去除重复或高度相似的命题
        
        Args:
            propositions: 命题列表
        
        Returns:
            去重后的命题列表
        """
        if len(propositions) <= 1:
            return propositions
        
        unique = []
        seen_texts = set()
        
        for prop in propositions:
            # 精确匹配
            normalized = self._normalize(prop.content)
            
            if normalized in seen_texts:
                continue
            
            # 相似度检查（简化版）
            is_duplicate = False
            for seen in seen_texts:
                if self._simple_similarity(normalized, seen) >= self.similarity_threshold:
                    is_duplicate = True
                    break
            
            if not is_duplicate:
                unique.append(prop)
                seen_texts.add(normalized)
        
        return unique
    
    def _normalize(self, text: str) -> str:
        """文本标准化"""
        # 去除标点和空白
        return re.sub(r'[^\w]', '', text.lower())
    
    def _simple_similarity(self, text1: str, text2: str) -> float:
        """简单的文本相似度计算"""
        if not text1 or not text2:
            return 0.0
        
        # Jaccard相似度
        set1 = set(text1)
        set2 = set(text2)
        
        intersection = len(set1 & set2)
        union = len(set1 | set2)
        
        return intersection / union if union > 0 else 0.0


class PropositionChunker:
    """命题分块器"""
    
    def __init__(self, llm_client=None, config: Dict = None):
        """
        初始化命题分块器
        
        Args:
            llm_client: LLM客户端
            config: 配置参数
        """
        self.config = config or {}
        
        # 初始化组件
        self.extractor = PropositionExtractor(llm_client, self.config)
        self.resolver = ReferenceResolver(llm_client, self.config)
        self.deduplicator = PropositionDeduplicator(self.config)
        
        # 父子映射
        self.proposition_to_parent: Dict[str, str] = {}
        self.parent_to_propositions: Dict[str, List[str]] = defaultdict(list)
    
    def chunk(self, document: str) -> List[Proposition]:
        """
        将文档切分为命题
        
        Args:
            document: 输入文档
        
        Returns:
            命题列表
        """
        # 1. 按段落切分
        paragraphs = self._split_paragraphs(document)
        
        all_propositions = []
        
        for para in paragraphs:
            if not para.strip():
                continue
            
            # 2. 提取命题
            propositions = self.extractor.extract(para)
            
            # 3. 指代消解
            if self.config.get('enable_resolution', True):
                resolved = []
                for prop in propositions:
                    resolved_prop = self.resolver.resolve(prop, para)
                    resolved.append(resolved_prop)
                propositions = resolved
            
            # 4. 建立父子映射
            for prop in propositions:
                self.proposition_to_parent[prop.id] = para
                self.parent_to_propositions[para].append(prop.id)
            
            all_propositions.extend(propositions)
        
        # 5. 去重
        if self.config.get('enable_deduplication', True):
            all_propositions = self.deduplicator.deduplicate(all_propositions)
        
        return all_propositions
    
    def chunk_batch(self, documents: List[str]) -> Dict[str, List[Proposition]]:
        """
        批量处理多个文档
        
        Args:
            documents: 文档列表
        
        Returns:
            文档ID到命题列表的映射
        """
        results = {}
        
        for i, doc in enumerate(documents):
            doc_id = f"doc_{i}"
            results[doc_id] = self.chunk(doc)
        
        return results
    
    def get_parent_context(self, proposition_id: str) -> Optional[str]:
        """获取命题的父段落"""
        return self.proposition_to_parent.get(proposition_id)
    
    def get_child_propositions(self, paragraph: str) -> List[str]:
        """获取段落的所有子命题"""
        return self.parent_to_propositions.get(paragraph, [])
    
    def _split_paragraphs(self, text: str) -> List[str]:
        """切分段落"""
        # 按空行切分
        paragraphs = re.split(r'\n\s*\n', text)
        return [p.strip() for p in paragraphs if p.strip()]
    
    def to_indexable_format(self, propositions: List[Proposition]) -> List[Dict]:
        """
        转换为可索引的格式（用于向量数据库）
        
        Args:
            propositions: 命题列表
        
        Returns:
            可索引的数据列表
        """
        indexable = []
        
        for prop in propositions:
            indexable.append({
                'id': prop.id,
                'text': prop.content,
                'metadata': {
                    'original_text': prop.original_text,
                    'parent_paragraph': prop.parent_paragraph,
                    'is_atomic': prop.is_atomic,
                    'is_self_contained': prop.is_self_contained,
                    'entities': prop.entities,
                    'confidence': prop.confidence
                }
            })
        
        return indexable


# 使用示例
if __name__ == '__main__':
    # 示例配置
    config = {
        'min_proposition_length': 15,
        'max_proposition_length': 150,
        'mode': 'strict',
        'enable_resolution': True,
        'enable_deduplication': True
    }
    
    # 创建分块器
    chunker = PropositionChunker(config=config)
    
    # 测试文档
    document = """
    RAG（检索增强生成）是一种结合信息检索和生成模型的技术。
    它能够显著降低大模型的幻觉问题。
    相比微调，RAG更新知识的成本更低。
    
    由小到大检索是RAG优化的核心策略。
    它的原理是用小块检索，返回大块上下文。
    这种方法可以将准确率从0.3提升到0.85以上。
    """
    
    # 执行分块
    propositions = chunker.chunk(document)
    
    print("\n=== 命题分块结果 ===\n")
    print(f"原文共 {len(document)} 字符")
    print(f"提取 {len(propositions)} 个命题\n")
    
    for i, prop in enumerate(propositions, 1):
        print(f"[{i}] {prop.content}")
        print(f"    原子性: {'✓' if prop.is_atomic else '✗'}")
        print(f"    自包含: {'✓' if prop.is_self_contained else '✗'}")
        print()
    
    # 转换为索引格式
    indexable = chunker.to_indexable_format(propositions)
    print(f"\n=== 可索引数据示例 ===")
    print(json.dumps(indexable[0], ensure_ascii=False, indent=2))
