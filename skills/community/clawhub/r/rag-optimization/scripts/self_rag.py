#!/usr/bin/env python3
"""
Self-RAG / Corrective RAG 实现

自我纠错RAG：在检索和生成环节增加质量评估，自动纠正错误

使用方法：
    python self_rag.py --query "你的问题" --knowledge-base ./data/

核心功能：
    1. 检索质量评估：判断检索结果是否与问题相关
    2. 纠正动作决策：根据评估结果选择重试、转网络搜索或拒绝
    3. 生成后反思：检查答案是否基于检索内容，是否存在幻觉
"""

import os
import json
import logging
from dataclasses import dataclass
from typing import List, Dict, Any, Optional, Tuple
from enum import Enum

# 设置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class CorrectionAction(Enum):
    """纠正动作类型"""
    ACCEPT = "accept"              # 接受，继续生成
    RETRY = "retry"                # 重试检索
    WEB_SEARCH = "web_search"      # 转网络搜索
    REFUSE = "refuse"              # 拒绝回答


@dataclass
class RetrievalAssessment:
    """检索质量评估结果"""
    relevance_score: float        # 相关性得分 (0-1)
    coverage_score: float         # 覆盖度得分 (0-1)
    action: CorrectionAction      # 建议的纠正动作
    reason: str                   # 评估理由


@dataclass
class GenerationAssessment:
    """生成质量评估结果"""
    faithfulness_score: float     # 忠实度得分 (0-1)
    relevance_score: float        # 相关性得分 (0-1)
    has_hallucination: bool       # 是否存在幻觉
    action: str                   # 建议动作
    reason: str                   # 评估理由


class RetrievalEvaluator:
    """检索质量评估器"""
    
    def __init__(self, llm_client=None, config: Dict = None):
        """
        初始化检索评估器
        
        Args:
            llm_client: LLM客户端（用于评估）
            config: 配置参数
        """
        self.llm = llm_client
        self.config = config or {}
        
        # 阈值配置
        self.high_threshold = self.config.get('high_relevance_threshold', 0.7)
        self.low_threshold = self.config.get('low_relevance_threshold', 0.3)
        
        # 评估模式：llm / vector / hybrid
        self.eval_mode = self.config.get('eval_mode', 'hybrid')
    
    def assess(self, query: str, documents: List[str]) -> RetrievalAssessment:
        """
        评估检索结果质量
        
        Args:
            query: 用户查询
            documents: 检索到的文档列表
        
        Returns:
            RetrievalAssessment: 评估结果
        """
        if not documents:
            return RetrievalAssessment(
                relevance_score=0.0,
                coverage_score=0.0,
                action=CorrectionAction.REFUSE,
                reason="未检索到任何文档"
            )
        
        # 根据评估模式选择方法
        if self.eval_mode == 'llm':
            relevance = self._llm_assess_relevance(query, documents)
        elif self.eval_mode == 'vector':
            relevance = self._vector_assess_relevance(query, documents)
        else:  # hybrid
            relevance = self._hybrid_assess_relevance(query, documents)
        
        # 计算覆盖度
        coverage = self._assess_coverage(query, documents)
        
        # 决定纠正动作
        action = self._decide_action(relevance)
        
        # 生成理由
        reason = self._generate_reason(relevance, coverage, action)
        
        return RetrievalAssessment(
            relevance_score=relevance,
            coverage_score=coverage,
            action=action,
            reason=reason
        )
    
    def _llm_assess_relevance(self, query: str, documents: List[str]) -> float:
        """使用LLM评估相关性"""
        if not self.llm:
            logger.warning("LLM客户端未配置，使用默认评估")
            return 0.5
        
        try:
            # 截取文档内容避免过长
            docs_preview = [d[:300] for d in documents[:5]]
            docs_text = "\n---\n".join(docs_preview)
            
            prompt = f"""
请评估以下检索结果与用户问题的相关性（0-1分）：

用户问题：{query}

检索到的文档：
{docs_text}

评分标准：
- 1.0: 文档完全匹配问题，能直接回答
- 0.7-0.9: 文档高度相关，包含主要信息
- 0.4-0.6: 文档部分相关，可能需要补充
- 0.1-0.3: 文档相关性低，信息不足
- 0.0: 文档完全不相关

只返回一个0到1之间的数字，不要其他内容。
"""
            
            from coze_workload_identity import requests
            # 假设 llm 是一个可调用的对象
            response = self.llm.invoke(prompt) if hasattr(self.llm, 'invoke') else self.llm(prompt)
            
            # 解析得分
            score_text = response.strip() if isinstance(response, str) else str(response)
            score = float(''.join(c for c in score_text if c.isdigit() or c == '.'))
            return max(0.0, min(1.0, score))
            
        except Exception as e:
            logger.error(f"LLM评估失败: {e}")
            return 0.5
    
    def _vector_assess_relevance(self, query: str, documents: List[str]) -> float:
        """使用向量相似度评估相关性"""
        try:
            from sentence_transformers import SentenceTransformer
            import numpy as np
            
            model = SentenceTransformer('all-MiniLM-L6-v2')
            
            # 计算查询和文档的向量
            query_embedding = model.encode(query)
            doc_embeddings = model.encode(documents[:10])
            
            # 计算余弦相似度
            similarities = np.dot(doc_embeddings, query_embedding) / (
                np.linalg.norm(doc_embeddings, axis=1) * np.linalg.norm(query_embedding)
            )
            
            # 返回最高相似度
            return float(np.max(similarities))
            
        except Exception as e:
            logger.error(f"向量评估失败: {e}")
            return 0.5
    
    def _hybrid_assess_relevance(self, query: str, documents: List[str]) -> float:
        """混合评估：先向量筛选，再LLM精评"""
        # 先用向量评估
        vector_score = self._vector_assess_relevance(query, documents)
        
        # 如果向量得分很高或很低，直接返回
        if vector_score >= 0.8 or vector_score <= 0.2:
            return vector_score
        
        # 中间分数用LLM精评
        llm_score = self._llm_assess_relevance(query, documents)
        
        # 加权融合
        return 0.4 * vector_score + 0.6 * llm_score
    
    def _assess_coverage(self, query: str, documents: List[str]) -> float:
        """评估文档对问题关键词的覆盖度"""
        # 简单的关键词覆盖计算
        query_words = set(query.lower().split())
        all_doc_words = set(' '.join(documents).lower().split())
        
        if not query_words:
            return 1.0
        
        coverage = len(query_words & all_doc_words) / len(query_words)
        return coverage
    
    def _decide_action(self, relevance: float) -> CorrectionAction:
        """根据相关性得分决定纠正动作"""
        if relevance >= self.high_threshold:
            return CorrectionAction.ACCEPT
        elif relevance >= self.low_threshold:
            return CorrectionAction.RETRY
        else:
            return CorrectionAction.WEB_SEARCH
    
    def _generate_reason(self, relevance: float, coverage: float, action: CorrectionAction) -> str:
        """生成评估理由"""
        reasons = []
        
        if relevance >= self.high_threshold:
            reasons.append(f"检索结果高度相关（得分:{relevance:.2f}）")
        elif relevance >= self.low_threshold:
            reasons.append(f"检索结果部分相关（得分:{relevance:.2f}），建议重试")
        else:
            reasons.append(f"检索结果相关性低（得分:{relevance:.2f}）")
        
        if coverage < 0.5:
            reasons.append(f"问题关键词覆盖不足（{coverage:.0%}）")
        
        return "；".join(reasons)


class GenerationEvaluator:
    """生成质量评估器"""
    
    def __init__(self, llm_client=None, config: Dict = None):
        self.llm = llm_client
        self.config = config or {}
        self.hallucination_threshold = self.config.get('hallucination_threshold', 0.5)
    
    def assess(self, query: str, answer: str, sources: List[str]) -> GenerationAssessment:
        """
        评估生成答案质量
        
        Args:
            query: 用户查询
            answer: 生成的答案
            sources: 检索到的源文档
        
        Returns:
            GenerationAssessment: 评估结果
        """
        # 评估忠实度（答案是否基于源文档）
        faithfulness = self._assess_faithfulness(answer, sources)
        
        # 评估相关性（答案是否回答了问题）
        relevance = self._assess_relevance(query, answer)
        
        # 检测幻觉
        has_hallucination = faithfulness < self.hallucination_threshold
        
        # 决定动作
        if has_hallucination:
            action = "regenerate"
        elif relevance < 0.5:
            action = "regenerate"
        else:
            action = "accept"
        
        # 生成理由
        reason = self._generate_reason(faithfulness, relevance, has_hallucination)
        
        return GenerationAssessment(
            faithfulness_score=faithfulness,
            relevance_score=relevance,
            has_hallucination=has_hallucination,
            action=action,
            reason=reason
        )
    
    def _assess_faithfulness(self, answer: str, sources: List[str]) -> float:
        """评估答案对源文档的忠实度"""
        if not self.llm:
            return 0.7  # 默认值
        
        try:
            sources_text = "\n---\n".join([s[:500] for s in sources[:3]])
            
            prompt = f"""
请评估以下答案是否基于提供的源文档生成（忠实度评估）：

源文档：
{sources_text}

答案：
{answer}

评分标准：
- 1.0: 答案完全基于源文档，没有添加外部信息
- 0.7-0.9: 答案主要基于源文档，有少量合理推理
- 0.4-0.6: 答案部分基于源文档，有一些未经验证的内容
- 0.0-0.3: 答案与源文档不符，存在幻觉

只返回一个0到1之间的数字。
"""
            
            response = self.llm.invoke(prompt) if hasattr(self.llm, 'invoke') else self.llm(prompt)
            score_text = response.strip() if isinstance(response, str) else str(response)
            score = float(''.join(c for c in score_text if c.isdigit() or c == '.'))
            return max(0.0, min(1.0, score))
            
        except Exception as e:
            logger.error(f"忠实度评估失败: {e}")
            return 0.7
    
    def _assess_relevance(self, query: str, answer: str) -> float:
        """评估答案与问题的相关性"""
        if not self.llm:
            return 0.7
        
        try:
            prompt = f"""
请评估以下答案是否回答了用户的问题：

问题：{query}
答案：{answer}

评分标准：
- 1.0: 完全回答了问题
- 0.5-0.9: 部分回答了问题
- 0.0-0.4: 没有回答问题或答非所问

只返回一个0到1之间的数字。
"""
            
            response = self.llm.invoke(prompt) if hasattr(self.llm, 'invoke') else self.llm(prompt)
            score_text = response.strip() if isinstance(response, str) else str(response)
            score = float(''.join(c for c in score_text if c.isdigit() or c == '.'))
            return max(0.0, min(1.0, score))
            
        except Exception as e:
            logger.error(f"相关性评估失败: {e}")
            return 0.7
    
    def _generate_reason(self, faithfulness: float, relevance: float, has_hallucination: bool) -> str:
        """生成评估理由"""
        reasons = []
        
        if has_hallucination:
            reasons.append(f"检测到可能的幻觉（忠实度:{faithfulness:.2f}）")
        
        if relevance < 0.5:
            reasons.append(f"答案与问题相关性不足（{relevance:.2f}）")
        
        if not reasons:
            reasons.append("答案质量良好")
        
        return "；".join(reasons)


class CorrectiveRAG:
    """纠正性RAG系统"""
    
    def __init__(self, retriever, generator, llm_client=None, config: Dict = None):
        """
        初始化CRAG系统
        
        Args:
            retriever: 检索器
            generator: 生成器
            llm_client: LLM客户端（用于评估）
            config: 配置参数
        """
        self.retriever = retriever
        self.generator = generator
        self.config = config or {}
        
        # 初始化评估器
        self.retrieval_evaluator = RetrievalEvaluator(llm_client, config)
        self.generation_evaluator = GenerationEvaluator(llm_client, config)
        
        # 重试配置
        self.max_retries = self.config.get('max_retries', 3)
        self.retry_strategies = ['hybrid', 'bm25', 'vector']  # 不同检索策略
    
    def query(self, question: str, top_k: int = 5) -> Dict[str, Any]:
        """
        执行带纠错的RAG查询
        
        Args:
            question: 用户问题
            top_k: 返回文档数量
        
        Returns:
            包含答案和评估信息的字典
        """
        results = {
            'question': question,
            'answer': None,
            'sources': [],
            'assessment': None,
            'corrections': []
        }
        
        # 阶段1：带纠错的检索
        for attempt in range(self.max_retries):
            logger.info(f"检索尝试 {attempt + 1}/{self.max_retries}")
            
            # 检索
            docs = self._retrieve_with_strategy(question, top_k, attempt)
            
            # 评估检索质量
            assessment = self.retrieval_evaluator.assess(question, docs)
            
            if assessment.action == CorrectionAction.ACCEPT:
                results['sources'] = docs
                results['assessment'] = assessment
                break
            elif assessment.action == CorrectionAction.RETRY:
                results['corrections'].append({
                    'type': 'retry',
                    'reason': assessment.reason,
                    'relevance': assessment.relevance_score
                })
                continue
            else:
                # WEB_SEARCH 或 REFUSE
                results['corrections'].append({
                    'type': assessment.action.value,
                    'reason': assessment.reason
                })
                if assessment.action == CorrectionAction.REFUSE:
                    results['answer'] = "抱歉，我无法找到相关信息来回答您的问题。"
                    return results
                # 这里可以集成网络搜索，暂时用重试代替
                continue
        
        # 阶段2：生成答案
        if results['sources']:
            answer = self.generator.generate(question, results['sources'])
            
            # 阶段3：生成后评估
            gen_assessment = self.generation_evaluator.assess(
                question, answer, results['sources']
            )
            
            if gen_assessment.action == 'regenerate':
                results['corrections'].append({
                    'type': 'regenerate',
                    'reason': gen_assessment.reason
                })
                # 重新生成（实际应用中可以调整prompt）
                answer = self.generator.generate(question, results['sources'])
            
            results['answer'] = answer
            results['generation_assessment'] = gen_assessment
        
        return results
    
    def _retrieve_with_strategy(self, query: str, top_k: int, attempt: int) -> List[str]:
        """根据尝试次数选择不同的检索策略"""
        strategy = self.retry_strategies[attempt % len(self.retry_strategies)]
        logger.info(f"使用检索策略: {strategy}")
        
        # 调用检索器（具体实现依赖检索器接口）
        if hasattr(self.retriever, 'retrieve'):
            return self.retriever.retrieve(query, top_k=top_k, strategy=strategy)
        else:
            # 简单模拟
            return [f"模拟文档{i+1} for: {query}" for i in range(top_k)]


class SelfRAG:
    """Self-RAG系统（更完整的自我反思RAG）"""
    
    def __init__(self, retriever, generator, llm_client=None, config: Dict = None):
        """
        初始化Self-RAG系统
        
        Args:
            retriever: 检索器
            generator: 生成器
            llm_client: LLM客户端
            config: 配置参数
        """
        self.retriever = retriever
        self.generator = generator
        self.llm = llm_client
        self.config = config or {}
        
        # 初始化组件
        self.crag = CorrectiveRAG(retriever, generator, llm_client, config)
        
        # Self-RAG特有配置
        self.enable_retrieval_decision = self.config.get('enable_retrieval_decision', True)
        self.enable_segment_labeling = self.config.get('enable_segment_labeling', True)
    
    def query(self, question: str) -> Dict[str, Any]:
        """
        执行Self-RAG查询
        
        Args:
            question: 用户问题
        
        Returns:
            包含答案、来源和反思标记的结果
        """
        results = {
            'question': question,
            'answer': None,
            'sources': [],
            'retrieval_needed': None,
            'segments': []  # 带标记的答案片段
        }
        
        # 阶段0：判断是否需要检索
        if self.enable_retrieval_decision:
            results['retrieval_needed'] = self._decide_retrieval_needed(question)
            if not results['retrieval_needed']:
                # 不需要检索，直接用模型知识回答
                results['answer'] = self.generator.generate(question, [])
                results['segments'] = self._label_segments(results['answer'], [])
                return results
        
        # 执行CRAG流程
        crag_result = self.crag.query(question)
        results.update(crag_result)
        
        # Self-RAG特有：对答案片段进行标记
        if self.enable_segment_labeling and results['answer']:
            results['segments'] = self._label_segments(
                results['answer'], 
                results['sources']
            )
        
        return results
    
    def _decide_retrieval_needed(self, question: str) -> bool:
        """判断问题是否需要检索外部知识"""
        if not self.llm:
            return True  # 默认需要检索
        
        try:
            prompt = f"""
请判断以下问题是否需要检索外部知识库来回答：

问题：{question}

判断标准：
- 涉及特定事实、数据、事件 → 需要检索
- 涉及公司/产品特定信息 → 需要检索
- 涉及最新信息 → 需要检索
- 通用知识、常识、推理题 → 不需要检索

只回答"是"或"否"。
"""
            
            response = self.llm.invoke(prompt) if hasattr(self.llm, 'invoke') else self.llm(prompt)
            return "是" in response
            
        except Exception as e:
            logger.error(f"检索决策失败: {e}")
            return True
    
    def _label_segments(self, answer: str, sources: List[str]) -> List[Dict]:
        """
        为答案片段添加来源标记
        
        Args:
            answer: 答案文本
            sources: 源文档列表
        
        Returns:
            带标记的片段列表
        """
        if not self.llm:
            # 简单分句
            sentences = answer.split('。')
            return [{'text': s + '。', 'source': 'unknown'} for s in sentences if s]
        
        try:
            sources_text = "\n".join([f"[{i+1}] {s[:200]}" for i, s in enumerate(sources)])
            
            prompt = f"""
请为答案的每个句子标注信息来源：

源文档：
{sources_text}

答案：
{answer}

输出格式：每行一个句子，格式为：
句子内容 | 来源标记

来源标记规则：
- [RET] 来自检索内容
- [KNW] 来自模型内部知识
- [MIX] 混合来源
"""
            
            response = self.llm.invoke(prompt) if hasattr(self.llm, 'invoke') else self.llm(prompt)
            
            segments = []
            for line in response.strip().split('\n'):
                if '|' in line:
                    parts = line.split('|')
                    segments.append({
                        'text': parts[0].strip(),
                        'source': parts[1].strip() if len(parts) > 1 else 'unknown'
                    })
            
            return segments
            
        except Exception as e:
            logger.error(f"片段标记失败: {e}")
            return [{'text': answer, 'source': 'unknown'}]


# 使用示例
if __name__ == '__main__':
    # 示例配置
    config = {
        'max_retries': 3,
        'high_relevance_threshold': 0.7,
        'low_relevance_threshold': 0.3,
        'eval_mode': 'hybrid',
        'hallucination_threshold': 0.5
    }
    
    # 创建模拟组件
    class MockRetriever:
        def retrieve(self, query, top_k=5, strategy='vector'):
            return [f"文档{i+1}: 关于{query}的相关内容..." for i in range(top_k)]
    
    class MockGenerator:
        def generate(self, query, sources):
            if sources:
                return f"根据检索到的信息，{query}的答案是..."
            return f"根据我的知识，{query}的答案是..."
    
    # 测试CRAG
    crag = CorrectiveRAG(
        retriever=MockRetriever(),
        generator=MockGenerator(),
        config=config
    )
    
    result = crag.query("RAG系统如何优化？")
    print("\n=== CRAG 结果 ===")
    print(f"问题: {result['question']}")
    print(f"答案: {result['answer']}")
    print(f"纠正次数: {len(result['corrections'])}")
    
    # 测试Self-RAG
    self_rag = SelfRAG(
        retriever=MockRetriever(),
        generator=MockGenerator(),
        config=config
    )
    
    result = self_rag.query("1+1等于几？")
    print("\n=== Self-RAG 结果 ===")
    print(f"需要检索: {result['retrieval_needed']}")
    print(f"答案: {result['answer']}")
