#!/usr/bin/env python3
"""
查询转换器（Query Transformer）
=================================
补全 config-template.json 中声明但未实现的 query_optimization 功能：
- HyDE（假设文档嵌入）：生成假设答案用于检索
- 查询扩展（Query Expansion）：生成多个语义变体
- 查询分解（Query Decomposition）：拆解复杂问题为子查询

降级行为：所有转换器在无 LLM 时自动回退为规则模式（零依赖可运行）。

使用方式：
    from query_transformer import HyDETransformer, QueryExpander, QueryDecomposer

    hyde = HyDETransformer(llm_client=your_llm)
    hypothetical_doc = hyde.transform("RAG 优化策略是什么？")
    # 用 hypothetical_doc 的向量进行检索（比原始 query 更精准）

    expander = QueryExpander(llm_client=your_llm)
    variants = expander.expand("RAG 优化策略是什么？", n=3)
    # ["RAG系统如何优化？", "有哪些RAG优化方法？", "如何提升RAG检索效果？"]

    decomposer = QueryDecomposer(llm_client=your_llm)
    sub_queries = decomposer.decompose("RAG和微调的区别是什么，各有什么优缺点？")
    # ["RAG和微调有什么区别？", "RAG有哪些优缺点？", "微调有哪些优缺点？"]
"""
import logging
import re
from typing import Dict, List, Optional

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


# ============================================================
# HyDE：假设文档嵌入（Hypothetical Document Embedding）
# ============================================================

class HyDETransformer:
    """
    用 LLM 生成一个假设性答案文档，再用该文档的向量进行检索。

    原理：用户查询（如 "RAG优化策略"）过于简短，直接编码后难以匹配
    完整的知识条目。先生成一个假设的完整回答，再编码，语义更丰富。

    适用场景：短查询（< 10 字）、模糊查询、概念性查询。
    不适用：精确匹配查询（如产品型号、版本号）。
    """

    # 规则模式的查询关键词映射（无 LLM 时的降级方案）
    _KEYWORD_MAP = {
        "rag": "RAG（Retrieval-Augmented Generation）是一种结合信息检索和生成模型的技术。"
               "常见优化策略包括：由小到大检索、混合检索、重排序、语义分块、"
               "Self-RAG、查询意图识别、多跳检索等。这些策略分别从分块、检索、"
               "排序和生成等维度提升检索准确性和答案质量。",
        "向量": "向量检索通过将文本转换为高维向量，计算语义相似度来检索相关文档。"
               "与基于关键词的 BM25 相比，向量检索能理解语义等价关系，"
               "但可能无法精确匹配专有名词。混合检索结合两者优势。",
        "优化": "优化策略涵盖检索前、检索中、检索后三个阶段。检索前优化包括"
               "语义分块、命题分块、上下文头增强；检索中优化包括混合检索、"
               "多跳检索、查询意图识别；检索后优化包括重排序、上下文压缩、"
               "引用溯源。",
        "分块": "文本分块是 RAG 的基础环节。常见策略有：定长分块（简单但可能"
               "切断语义）、语义分块（基于语义边界动态切分）、由小到大检索"
               "（小块检索、大块返回）、命题分块（最小事实单元）。",
    }

    def __init__(self, llm_client=None, config: Dict = None):
        self.llm = llm_client
        self.config = config or {}

    def transform(self, query: str) -> str:
        """
        生成假设文档。

        Args:
            query: 用户查询

        Returns:
            假设文档文本（用于向量化检索）
        """
        if not self.llm:
            return self._rule_hyde(query)

        prompt = self._build_prompt(query)
        result = self.llm.generate(prompt)

        if not result or result == "LLM 未配置":
            return self._rule_hyde(query)

        return result

    def _build_prompt(self, query: str) -> str:
        return f"""你是一个知识库检索系统。用户提出了一个问题，请你生成一个假设性的、完整的答案文档。

用户问题：{query}

请生成一个详细的回答文档，要求：
1. 包含对问题的完整回答
2. 包含相关背景知识和概念解释
3. 使用正式的书面语言
4. 回答应详细且全面，约 200-500 字
5. 只输出回答内容，不要解释

假设答案："""

    def _rule_hyde(self, query: str) -> str:
        """规则模式：基于关键词生成假设文档。"""
        query_lower = query.lower()
        for keyword, doc in self._KEYWORD_MAP.items():
            if keyword in query_lower:
                return doc
        return f"以下是关于「{query}」的参考信息。"


# ============================================================
# 查询扩展（Query Expansion）
# ============================================================

class QueryExpander:
    """
    生成多个语义变体的查询，提高召回率。

    适用场景：查询词太少导致召回不足、需要多角度检索。
    """

    # 规则模式的同义词映射（无 LLM 时降级）
    _SYNONYMS = {
        "如何": ["怎么", "怎样", "方法"],
        "什么": ["哪些", "有哪些", "介绍"],
        "区别": ["差异", "不同", "对比"],
        "优化": ["改进", "提升", "增强", "改善"],
        "策略": ["方法", "方案", "技术"],
        "原理": ["机制", "工作方式", "如何工作"],
        "效果": ["性能", "表现", "能力"],
    }

    def __init__(self, llm_client=None, config: Dict = None):
        self.llm = llm_client
        self.config = config or {}

    def expand(self, query: str, n: int = 3) -> List[str]:
        """
        生成 n 个查询变体。

        Args:
            query: 原始查询
            n: 生成变体数量

        Returns:
            查询变体列表（包含原始查询）
        """
        if not self.llm:
            return self._rule_expand(query, n)

        prompt = f"""请将以下用户查询改写为 {n} 个不同的表达方式，每个变体应：
1. 保持原意不变
2. 使用不同的词汇或句式
3. 适合用于向量数据库检索

原始查询：{query}

输出格式：每行一个变体，共 {n} 行。"""

        result = self.llm.generate(prompt)
        if not result or result == "LLM 未配置":
            return self._rule_expand(query, n)

        variants = [line.strip() for line in result.strip().split('\n') if line.strip()]
        return [query] + variants[:n - 1]  # 确保包含原始查询

    def _rule_expand(self, query: str, n: int) -> List[str]:
        """规则模式：基于同义词替换生成变体。"""
        variants = [query]
        for word, synonyms in self._SYNONYMS.items():
            if word in query and len(variants) < n:
                for syn in synonyms[:n - len(variants)]:
                    new_q = query.replace(word, syn)
                    if new_q != query and new_q not in variants:
                        variants.append(new_q)
            if len(variants) >= n:
                break
        return variants[:n]


# ============================================================
# 查询分解（Query Decomposition）
# ============================================================

class QueryDecomposer:
    """
    将复杂查询拆解为多个子查询，分别检索后汇总。

    适用场景：复合问题（"A和B的区别是什么，各有什么优缺点"）、
    需要多步推理的问题。
    """

    # 常见复合连接词
    _CONNECTORS = [
        "的区别", "差异", "对比",
        "以及", "还有", "同时",
        "和", "与", "及",
        "什么", "怎么", "如何",
    ]

    # 常见复合模式
    _COMPOUND_PATTERNS = [
        (r'(什么|如何|怎么).*(什么|如何|怎么)', 'two_questions'),
        (r'(区别|差异|不同).*?(什么|如何|怎么)', 'compare_and_detail'),
        (r'(有哪些|什么).*?(如何|怎么|为什么)', 'list_and_method'),
        (r'(优点|优势).*?(缺点|劣势)', 'pros_and_cons'),
    ]

    def __init__(self, llm_client=None, config: Dict = None):
        self.llm = llm_client
        self.config = config or {}

    def decompose(self, query: str) -> List[str]:
        """
        将复杂查询拆解为子查询。

        Args:
            query: 原始查询

        Returns:
            子查询列表
        """
        # 先用规则模式检测
        rule_result = self._rule_decompose(query)
        if rule_result:
            return rule_result

        if not self.llm:
            return [query]

        prompt = f"""请将以下复杂查询拆解为 2-4 个独立的子查询。
每个子查询应能单独用一次检索回答。

原始查询：{query}

拆解原则：
1. 每个子查询表达一个独立的子问题
2. 子查询组合起来覆盖原始查询的全部意图
3. 保持子查询的独立性和完整性

输出格式：每行一个子查询。"""

        result = self.llm.generate(prompt)
        if not result or result == "LLM 未配置":
            return [query]

        sub_queries = [line.strip() for line in result.strip().split('\n')
                      if line.strip() and len(line.strip()) > 3]
        return sub_queries if sub_queries else [query]

    def _rule_decompose(self, query: str) -> Optional[List[str]]:
        """规则模式：基于模式匹配拆解查询。"""
        for pattern, match_type in self._COMPOUND_PATTERNS:
            if re.search(pattern, query):
                if match_type == 'two_questions':
                    parts = re.split(r'(？|\?|。|！)', query)
                    sub_queries = [p.strip() for p in parts if p.strip() and len(p.strip()) > 3]
                    return sub_queries if len(sub_queries) > 1 else None
                elif match_type == 'compare_and_detail':
                    return [
                        query.split('的')[0] + '和什么有关？' if '什么' in query else query,
                        query
                    ]
                elif match_type == 'pros_and_cons':
                    # "A的优点是什么，缺点是什么"
                    parts = re.split(r'(优点|优势|缺点|劣势)', query)
                    if len(parts) >= 3:
                        return [parts[0].strip() + '的' + parts[1].strip(),
                                parts[0].strip() + '的' + parts[2].strip()] if len(parts) >= 4 else None
        return None


# ============================================================
# 统一查询转换器（组合以上三种策略）
# ============================================================

class QueryTransformer:
    """
    统一查询转换器：根据查询特征自动选择最合适的转换策略。

    决策逻辑：
    - 短查询（< 5 字）→ HyDE
    - 模糊查询 → 查询扩展
    - 复杂查询 → 查询分解
    - 普通查询 → 原样输出
    """

    def __init__(self, llm_client=None, config: Dict = None):
        self.config = config or {}
        self.llm = llm_client
        self.hyde = HyDETransformer(llm_client=llm_client, config=config)
        self.expander = QueryExpander(llm_client=llm_client, config=config)
        self.decomposer = QueryDecomposer(llm_client=llm_client, config=config)

    def transform(self, query: str) -> Dict[str, str]:
        """
        智能转换查询，返回原始查询 + 转换后的查询。

        Args:
            query: 原始查询

        Returns:
            包含原始查询、转换后查询和策略类型的字典
        """
        strategy = self._select_strategy(query)

        if strategy == 'hyde':
            hypothetical = self.hyde.transform(query)
            return {
                'original': query,
                'transformed': hypothetical,
                'strategy': 'hyde'
            }
        elif strategy == 'expand':
            variants = self.expander.expand(query)
            return {
                'original': query,
                'transformed': variants,
                'strategy': 'expand'
            }
        elif strategy == 'decompose':
            sub_queries = self.decomposer.decompose(query)
            return {
                'original': query,
                'transformed': sub_queries,
                'strategy': 'decompose'
            }
        else:
            return {
                'original': query,
                'transformed': query,
                'strategy': 'none'
            }

    def _select_strategy(self, query: str) -> str:
        """根据查询特征选择策略。"""
        # 短查询 → HyDE
        if len(query) <= 5:
            return 'hyde'

        # 模糊查询（含 "如何"、"什么" 等）→ 查询扩展
        vague_keywords = ['如何', '什么', '怎么', '怎样', '有哪些']
        if any(kw in query for kw in vague_keywords) and len(query) <= 15:
            return 'expand'

        # 复合查询 → 查询分解
        connectors = ['的区别', '以及', '还有', '同时', '优点', '缺点']
        if any(conn in query for conn in connectors):
            return 'decompose'

        return 'none'
