#!/usr/bin/env python3
"""
多跳检索器（Multi-Hop Retriever）

通过迭代检索解决需要多步推理的复杂问题

使用方法：
    python multi_hop_retriever.py --query "复杂问题"

核心功能：
    1. 查询链构建：自动生成子查询链
    2. 迭代检索：逐步获取所需信息
    3. 终止判断：智能判断何时停止检索
    4. 答案聚合：合并多跳结果生成完整答案
"""

import os
import re
import json
import logging
from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional, Tuple, Callable
from enum import Enum

# 设置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class TerminationReason(Enum):
    """终止原因"""
    COMPLETE = "complete"               # 信息已完整
    MAX_HOPS = "max_hops"               # 达到最大跳数
    NO_NEW_INFO = "no_new_info"         # 无新信息
    SATISFIED = "satisfied"             # 已满足回答需求
    ERROR = "error"                     # 发生错误


@dataclass
class QueryHop:
    """单跳查询信息"""
    hop_index: int                      # 跳跃序号（从1开始）
    query: str                          # 当前查询
    retrieved_docs: List[str]           # 检索到的文档
    extracted_info: str                 # 提取的关键信息
    relevance_score: float              # 相关性得分
    next_query: Optional[str]           # 生成的下一跳查询
    entities_found: List[str]           # 发现的实体


@dataclass
class QueryChain:
    """查询链 - 记录多跳检索全过程"""
    original_query: str                 # 原始查询
    hops: List[QueryHop]                # 跳跃记录列表
    final_answer: str                   # 最终答案
    total_hops: int                     # 总跳数
    termination_reason: TerminationReason  # 终止原因
    confidence: float                   # 答案置信度
    metadata: Dict[str, Any] = field(default_factory=dict)


class SubQueryGenerator:
    """子查询生成器 - 根据当前结果生成下一步查询"""
    
    def __init__(self, llm_client=None, config: Dict = None):
        self.llm = llm_client
        self.config = config or {}
    
    def generate(self, original_query: str, current_info: str,
                 hop_history: List[QueryHop]) -> Tuple[Optional[str], str]:
        """
        生成下一跳查询
        
        Args:
            original_query: 原始问题
            current_info: 当前已获取的信息
            hop_history: 历史跳跃记录
        
        Returns:
            (下一跳查询, 推理过程)
        """
        if not self.llm:
            return None, "LLM未配置，无法生成子查询"
        
        # 构建历史摘要
        history_summary = self._build_history_summary(hop_history)
        
        prompt = f"""
原始问题：{original_query}

已获取的信息：
{current_info}

查询历史：
{history_summary}

请判断：
1. 当前信息是否足够回答原始问题？
2. 如果不足，还需要查询什么？

输出JSON格式：
{{
    "is_complete": true/false,
    "missing_info": "缺失的信息描述",
    "next_query": "下一跳查询（如果需要）",
    "reasoning": "判断推理过程"
}}

如果信息已足够，设置is_complete为true，next_query为空。
如果还需要更多信息，设置is_complete为false，并提供next_query。
"""
        
        try:
            response = self.llm.invoke(prompt) if hasattr(self.llm, 'invoke') else self.llm(prompt)
            response_text = response.strip() if isinstance(response, str) else str(response)
            
            # 解析JSON
            json_match = re.search(r'\{[\s\S]*\}', response_text)
            if json_match:
                data = json.loads(json_match.group())
                
                is_complete = data.get('is_complete', False)
                next_query = data.get('next_query', '') if not is_complete else None
                reasoning = data.get('reasoning', '')
                
                return next_query, reasoning
            
        except Exception as e:
            logger.error(f"生成子查询失败: {e}")
        
        return None, "解析失败"
    
    def _build_history_summary(self, hops: List[QueryHop]) -> str:
        """构建历史摘要"""
        if not hops:
            return "无"
        
        summaries = []
        for hop in hops:
            summaries.append(f"第{hop.hop_index}跳: 查询'{hop.query}' → 获取'{hop.extracted_info[:100]}...'")
        
        return "\n".join(summaries)


class TerminationChecker:
    """终止条件检查器"""
    
    def __init__(self, llm_client=None, config: Dict = None):
        self.llm = llm_client
        self.config = config or {}
        
        # 配置
        self.max_hops = self.config.get('max_hops', 3)
        self.min_new_info_ratio = self.config.get('min_new_info_ratio', 0.1)
    
    def should_stop(self, chain: QueryChain) -> Tuple[bool, TerminationReason, str]:
        """
        检查是否应该终止检索
        
        Args:
            chain: 当前查询链
        
        Returns:
            (是否终止, 终止原因, 原因说明)
        """
        # 条件1: 达到最大跳数
        if chain.total_hops >= self.max_hops:
            return True, TerminationReason.MAX_HOPS, f"已达到最大跳数限制({self.max_hops})"
        
        # 条件2: 检查新信息增量
        if len(chain.hops) >= 2:
            last_hop = chain.hops[-1]
            prev_hop = chain.hops[-2]
            
            # 简单的新信息检测
            new_info_ratio = self._calc_new_info_ratio(
                last_hop.extracted_info,
                prev_hop.extracted_info
            )
            
            if new_info_ratio < self.min_new_info_ratio:
                return True, TerminationReason.NO_NEW_INFO, "未检索到显著新信息"
        
        # 条件3: LLM判断信息完整性
        if self.llm and len(chain.hops) > 0:
            is_complete, reason = self._llm_check_completeness(chain)
            if is_complete:
                return True, TerminationReason.COMPLETE, reason
        
        return False, TerminationReason.COMPLETE, ""
    
    def _calc_new_info_ratio(self, current: str, previous: str) -> float:
        """计算新信息比例"""
        if not current:
            return 0.0
        
        current_words = set(current.lower().split())
        previous_words = set(previous.lower().split()) if previous else set()
        
        new_words = current_words - previous_words
        
        return len(new_words) / len(current_words) if current_words else 0
    
    def _llm_check_completeness(self, chain: QueryChain) -> Tuple[bool, str]:
        """使用LLM检查信息完整性"""
        all_info = "\n".join([hop.extracted_info for hop in chain.hops])
        
        prompt = f"""
原始问题：{chain.original_query}

已获取的信息：
{all_info}

请判断：这些信息是否足够回答原始问题？

输出JSON格式：
{{
    "is_complete": true/false,
    "reason": "判断理由"
}}
"""
        
        try:
            response = self.llm.invoke(prompt) if hasattr(self.llm, 'invoke') else self.llm(prompt)
            response_text = response.strip() if isinstance(response, str) else str(response)
            
            json_match = re.search(r'\{[\s\S]*\}', response_text)
            if json_match:
                data = json.loads(json_match.group())
                return data.get('is_complete', False), data.get('reason', '')
            
        except Exception as e:
            logger.error(f"LLM完整性检查失败: {e}")
        
        return False, ""


class InformationExtractor:
    """信息提取器 - 从检索结果中提取关键信息"""
    
    def __init__(self, llm_client=None, config: Dict = None):
        self.llm = llm_client
        self.config = config or {}
    
    def extract(self, query: str, documents: List[str]) -> Tuple[str, List[str]]:
        """
        从文档中提取与查询相关的关键信息
        
        Args:
            query: 查询
            documents: 文档列表
        
        Returns:
            (关键信息文本, 发现的实体列表)
        """
        if not documents:
            return "", []
        
        combined_text = "\n\n---\n\n".join(documents[:3])  # 最多处理3个文档
        
        if self.llm:
            return self._llm_extract(query, combined_text)
        else:
            return self._rule_extract(query, combined_text)
    
    def _llm_extract(self, query: str, text: str) -> Tuple[str, List[str]]:
        """使用LLM提取信息"""
        prompt = f"""
问题：{query}

文档内容：
{text[:2000]}

请从文档中提取与问题相关的关键信息。

输出JSON格式：
{{
    "key_info": "提取的关键信息",
    "entities": ["实体1", "实体2"]
}}
"""
        
        try:
            response = self.llm.invoke(prompt) if hasattr(self.llm, 'invoke') else self.llm(prompt)
            response_text = response.strip() if isinstance(response, str) else str(response)
            
            json_match = re.search(r'\{[\s\S]*\}', response_text)
            if json_match:
                data = json.loads(json_match.group())
                key_info = data.get('key_info', '')
                entities = data.get('entities', [])
                return key_info, entities
            
        except Exception as e:
            logger.error(f"LLM信息提取失败: {e}")
        
        return text[:500], []
    
    def _rule_extract(self, query: str, text: str) -> Tuple[str, List[str]]:
        """基于规则的信息提取"""
        # 提取包含查询词的句子
        query_words = set(query.lower().split())
        sentences = re.split(r'[。！？.!?]', text)
        
        relevant_sentences = []
        for sentence in sentences:
            sentence_words = set(sentence.lower().split())
            if query_words & sentence_words:
                relevant_sentences.append(sentence.strip())
        
        key_info = "。".join(relevant_sentences[:5])
        
        # 提取实体
        entities = re.findall(r'\b[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*\b', text)
        entities.extend(re.findall(r'\d+(?:\.\d+)?(?:年|月|日|小时|分钟|元|%|GB)', text))
        
        return key_info[:1000], list(set(entities))


class AnswerAggregator:
    """答案聚合器 - 合并多跳信息生成最终答案"""
    
    def __init__(self, llm_client=None, config: Dict = None):
        self.llm = llm_client
        self.config = config or {}
    
    def aggregate(self, chain: QueryChain) -> Tuple[str, float]:
        """
        聚合多跳结果生成最终答案
        
        Args:
            chain: 查询链
        
        Returns:
            (最终答案, 置信度)
        """
        if not chain.hops:
            return "抱歉，未找到相关信息。", 0.0
        
        # 收集所有信息
        all_info = []
        for hop in chain.hops:
            all_info.append(f"[第{hop.hop_index}跳] {hop.extracted_info}")
        
        combined_info = "\n\n".join(all_info)
        
        if self.llm:
            return self._llm_aggregate(chain.original_query, combined_info)
        else:
            return self._simple_aggregate(chain.original_query, combined_info)
    
    def _llm_aggregate(self, original_query: str, combined_info: str) -> Tuple[str, float]:
        """使用LLM聚合"""
        prompt = f"""
原始问题：{original_query}

通过多轮检索获取的信息：
{combined_info}

请基于以上信息，完整回答原始问题。

输出JSON格式：
{{
    "answer": "完整答案",
    "confidence": 0.0-1.0,
    "sources_used": ["使用的信息来源1", "使用的信息来源2"]
}}
"""
        
        try:
            response = self.llm.invoke(prompt) if hasattr(self.llm, 'invoke') else self.llm(prompt)
            response_text = response.strip() if isinstance(response, str) else str(response)
            
            json_match = re.search(r'\{[\s\S]*\}', response_text)
            if json_match:
                data = json.loads(json_match.group())
                answer = data.get('answer', '')
                confidence = float(data.get('confidence', 0.7))
                return answer, confidence
            
        except Exception as e:
            logger.error(f"LLM答案聚合失败: {e}")
        
        return combined_info[:500], 0.5
    
    def _simple_aggregate(self, original_query: str, combined_info: str) -> Tuple[str, float]:
        """简单聚合"""
        # 直接返回合并的信息
        return f"根据检索到的信息：\n\n{combined_info}", 0.5


class MultiHopRetriever:
    """多跳检索器 - 主入口类"""
    
    def __init__(self, 
                 retriever: Callable = None,
                 llm_client=None,
                 config: Dict = None):
        """
        初始化多跳检索器
        
        Args:
            retriever: 检索函数，接收query返回文档列表
            llm_client: LLM客户端
            config: 配置参数
        """
        self.retriever = retriever
        self.llm = llm_client
        self.config = config or {}
        
        # 初始化组件
        self.sub_query_generator = SubQueryGenerator(llm_client, self.config)
        self.termination_checker = TerminationChecker(llm_client, self.config)
        self.info_extractor = InformationExtractor(llm_client, self.config)
        self.answer_aggregator = AnswerAggregator(llm_client, self.config)
        
        # 配置参数
        self.max_hops = self.config.get('max_hops', 3)
        self.top_k_per_hop = self.config.get('top_k_per_hop', 5)
    
    def retrieve(self, query: str) -> QueryChain:
        """
        执行多跳检索
        
        Args:
            query: 用户查询
        
        Returns:
            QueryChain: 完整的查询链
        """
        logger.info(f"开始多跳检索: {query}")
        
        # 初始化查询链
        chain = QueryChain(
            original_query=query,
            hops=[],
            final_answer="",
            total_hops=0,
            termination_reason=TerminationReason.COMPLETE,
            confidence=0.0
        )
        
        current_query = query
        all_retrieved_docs = set()  # 避免重复检索
        
        # 迭代检索
        for hop_index in range(1, self.max_hops + 1):
            logger.info(f"执行第 {hop_index} 跳检索: {current_query}")
            
            # 1. 检索
            docs = self._retrieve(current_query)
            
            # 去重
            new_docs = [d for d in docs if d not in all_retrieved_docs]
            all_retrieved_docs.update(docs)
            
            # 2. 提取信息
            extracted_info, entities = self.info_extractor.extract(current_query, new_docs)
            
            # 3. 计算相关性
            relevance = self._calc_relevance(query, extracted_info)
            
            # 4. 记录本跳
            hop = QueryHop(
                hop_index=hop_index,
                query=current_query,
                retrieved_docs=new_docs,
                extracted_info=extracted_info,
                relevance_score=relevance,
                next_query=None,
                entities_found=entities
            )
            chain.hops.append(hop)
            chain.total_hops = hop_index
            
            # 5. 检查终止条件
            should_stop, reason, explanation = self.termination_checker.should_stop(chain)
            
            if should_stop:
                logger.info(f"终止检索: {explanation}")
                chain.termination_reason = reason
                break
            
            # 6. 生成下一跳查询
            current_info = "\n".join([h.extracted_info for h in chain.hops])
            next_query, reasoning = self.sub_query_generator.generate(
                query, current_info, chain.hops
            )
            
            if not next_query:
                logger.info("无需继续检索")
                chain.termination_reason = TerminationReason.SATISFIED
                break
            
            hop.next_query = next_query
            current_query = next_query
        
        # 聚合答案
        chain.final_answer, chain.confidence = self.answer_aggregator.aggregate(chain)
        
        logger.info(f"多跳检索完成: {chain.total_hops}跳, 置信度: {chain.confidence:.0%}")
        
        return chain
    
    def _retrieve(self, query: str) -> List[str]:
        """执行检索"""
        if self.retriever:
            try:
                return self.retriever(query, top_k=self.top_k_per_hop)
            except Exception as e:
                logger.error(f"检索失败: {e}")
                return []
        
        # 模拟检索
        return [f"模拟文档{i+1}: 关于'{query}'的相关内容..." for i in range(self.top_k_per_hop)]
    
    def _calc_relevance(self, query: str, info: str) -> float:
        """计算相关性"""
        query_words = set(query.lower().split())
        info_words = set(info.lower().split())
        
        if not query_words:
            return 0.0
        
        overlap = len(query_words & info_words)
        return overlap / len(query_words)
    
    def get_hop_summary(self, chain: QueryChain) -> str:
        """
        获取检索过程摘要
        
        Args:
            chain: 查询链
        
        Returns:
            摘要文本
        """
        lines = [f"多跳检索摘要（共{chain.total_hops}跳）:\n"]
        
        for hop in chain.hops:
            lines.append(f"第{hop.hop_index}跳:")
            lines.append(f"  查询: {hop.query}")
            lines.append(f"  获取: {hop.extracted_info[:100]}...")
            if hop.next_query:
                lines.append(f"  下一步: {hop.next_query}")
            lines.append("")
        
        lines.append(f"最终答案: {chain.final_answer}")
        lines.append(f"置信度: {chain.confidence:.0%}")
        
        return "\n".join(lines)


# 使用示例
if __name__ == '__main__':
    # 模拟检索函数
    def mock_retriever(query: str, top_k: int = 5) -> List[str]:
        """模拟检索器"""
        mock_docs = {
            "供应商": [
                "产品A的主要供应商是X公司，成立于2010年。",
                "X公司是国内领先的零部件制造商。",
            ],
            "生产地": [
                "X公司的生产基地位于深圳市南山区。",
                "深圳工厂年产能达到100万件。",
            ],
            "RAG": [
                "RAG（检索增强生成）是一种结合检索和生成的技术。",
                "RAG能够降低大模型的幻觉问题。",
            ],
            "优化": [
                "RAG优化策略包括语义分块、重排序、混合检索等。",
                "由小到大检索可以将准确率从0.3提升到0.85。",
            ]
        }
        
        results = []
        for keyword, docs in mock_docs.items():
            if keyword in query:
                results.extend(docs[:top_k])
        
        if not results:
            results = [f"关于'{query}'的模拟检索结果"]
        
        return results[:top_k]
    
    # 创建多跳检索器
    config = {
        'max_hops': 3,
        'top_k_per_hop': 3
    }
    
    retriever = MultiHopRetriever(
        retriever=mock_retriever,
        config=config
    )
    
    # 测试查询
    test_queries = [
        "产品A的供应商在哪里生产？",
        "RAG技术有什么优势，以及如何优化？",
    ]
    
    print("\n=== 多跳检索测试 ===\n")
    
    for query in test_queries:
        print(f"查询: {query}")
        print("-" * 50)
        
        chain = retriever.retrieve(query)
        
        print(f"总跳数: {chain.total_hops}")
        print(f"终止原因: {chain.termination_reason.value}")
        print(f"置信度: {chain.confidence:.0%}")
        
        print("\n检索路径:")
        for hop in chain.hops:
            print(f"  第{hop.hop_index}跳: {hop.query}")
            print(f"    → 获取: {hop.extracted_info[:80]}...")
        
        print(f"\n最终答案:\n{chain.final_answer}")
        print("\n" + "=" * 50 + "\n")
