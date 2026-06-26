#!/usr/bin/env python3
"""
查询意图识别器（Query Intent Recognition）

理解用户查询的真实意图，选择最优处理策略

使用方法：
    python query_intent.py --query "用户输入"

核心功能：
    1. 意图分类：事实型/开放型/比较型/流程型/故障排查型/复合型
    2. 复杂度评估：简单/中等/复杂
    3. 口语化标准化：将口语表达转为规范查询
    4. 策略路由：根据意图推荐处理策略
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


class QueryIntent(Enum):
    """查询意图类型"""
    FACTUAL = "factual"                     # 事实型：查询具体事实
    OPEN_ENDED = "open_ended"               # 开放型：开放式问题
    COMPARATIVE = "comparative"             # 比较型：比较类问题
    PROCEDURAL = "procedural"               # 流程型：步骤类问题
    TROUBLESHOOTING = "troubleshooting"     # 故障排查型：诊断问题
    DEFINITION = "definition"               # 定义型：概念解释
    COMPOUND = "compound"                   # 复合型：多个意图组合
    UNKNOWN = "unknown"                     # 未知类型


class QueryComplexity(Enum):
    """查询复杂度"""
    SIMPLE = "simple"       # 简单：单次检索可回答
    MEDIUM = "medium"       # 中等：可能需要多次检索
    COMPLEX = "complex"     # 复杂：需要多跳检索或推理


@dataclass
class IntentResult:
    """意图识别结果"""
    primary_intent: QueryIntent               # 主意图
    secondary_intents: List[QueryIntent]      # 次要意图
    confidence: float                         # 置信度
    complexity: QueryComplexity               # 复杂度
    normalized_query: str                     # 标准化查询
    entities: List[str]                       # 识别的实体
    sub_queries: List[str]                    # 分解的子问题（如有）
    suggested_strategy: Dict[str, Any]        # 建议的处理策略
    reasoning: str                            # 识别推理过程


class QueryNormalizer:
    """查询标准化器 - 处理口语化表达"""
    
    # 口语化表达映射表
    COLLOQUIAL_MAPPINGS = {
        # 疑问词
        "咋": "如何",
        "咋整": "如何解决",
        "咋办": "如何处理",
        "怎么个": "如何",
        "啥": "什么",
        "啥是": "什么是",
        "啥叫": "什么叫做",
        
        # 判断词
        "能不能": "是否可以",
        "行不行": "是否可行",
        "可以不": "是否可以",
        "会不会": "是否会",
        "有没有": "是否有",
        
        # 动作词
        "搞不懂": "不理解",
        "不明白": "不清楚",
        "弄不了": "无法处理",
        "整不会了": "不知道如何处理",
        
        # 语气词
        "呗": "",
        "嘛": "",
        "呢": "",
        "呀": "",
        "啊": "",
        "啦": "",
    }
    
    # 常见错别字修正
    TYPO_CORRECTIONS = {
        "以经": "已经",
        "在次": "再次",
        "做么": "怎么",
        "为什麽": "为什么",
        "那里": "哪里",
    }
    
    def __init__(self, llm_client=None, config: Dict = None):
        self.llm = llm_client
        self.config = config or {}
    
    def normalize(self, query: str) -> str:
        """
        标准化查询
        
        Args:
            query: 原始查询
        
        Returns:
            标准化后的查询
        """
        normalized = query.strip()
        
        # 1. 错别字修正
        for wrong, correct in self.TYPO_CORRECTIONS.items():
            normalized = normalized.replace(wrong, correct)
        
        # 2. 口语化替换
        for colloquial, formal in self.COLLOQUIAL_MAPPINGS.items():
            normalized = normalized.replace(colloquial, formal)
        
        # 3. 清理多余空格
        normalized = re.sub(r'\s+', ' ', normalized)
        
        # 4. 清理末尾标点
        normalized = normalized.rstrip('，。！？,.!?')
        
        # 5. 如果启用LLM，进行语法修正
        if self.llm and self._needs_grammar_fix(normalized):
            normalized = self._llm_fix_grammar(normalized)
        
        return normalized
    
    def _needs_grammar_fix(self, query: str) -> bool:
        """判断是否需要语法修正"""
        # 简单检查：如果查询太短或没有标点，可能需要修正
        if len(query) < 5:
            return False
        
        # 检查是否有明显的语法问题
        if not re.search(r'[？?？]$', query) and '?' in query:
            return True
        
        return False
    
    def _llm_fix_grammar(self, query: str) -> str:
        """使用LLM修正语法"""
        if not self.llm:
            return query
        
        try:
            prompt = f"""
请将以下用户查询转换为标准的、语法正确的问句形式。
保持原意不变，只做语法修正和表达规范化。

原始查询：{query}

输出：修正后的查询（只输出查询本身，不要解释）
"""
            
            response = self.llm.invoke(prompt) if hasattr(self.llm, 'invoke') else self.llm(prompt)
            fixed = response.strip() if isinstance(response, str) else str(response)
            return fixed
            
        except Exception as e:
            logger.error(f"LLM语法修正失败: {e}")
            return query


class ComplexityEvaluator:
    """复杂度评估器"""
    
    def __init__(self, config: Dict = None):
        self.config = config or {}
        
        # 复杂度权重
        self.weights = {
            'length': 0.2,           # 长度因子
            'connectors': 0.25,      # 连接词因子
            'sub_queries': 0.25,     # 子问题因子
            'entities': 0.15,        # 实体因子
            'inference': 0.15        # 推理需求因子
        }
    
    def evaluate(self, query: str, entities: List[str] = None) -> QueryComplexity:
        """
        评估查询复杂度
        
        Args:
            query: 查询文本
            entities: 已识别的实体列表
        
        Returns:
            QueryComplexity: 复杂度级别
        """
        score = 0.0
        
        # 1. 长度因子
        length = len(query)
        if length > 50:
            score += self.weights['length']
        elif length > 30:
            score += self.weights['length'] * 0.5
        
        # 2. 连接词因子
        connectors = ['和', '以及', '同时', '比较', '对比', '区别', '还有', '另外', '并且', '而且']
        connector_count = sum(1 for c in connectors if c in query)
        score += min(connector_count * 0.1, self.weights['connectors'])
        
        # 3. 子问题因子
        sub_queries = self._detect_sub_queries(query)
        score += min(len(sub_queries) * 0.1, self.weights['sub_queries'])
        
        # 4. 实体因子
        if entities:
            score += min(len(entities) * 0.05, self.weights['entities'])
        
        # 5. 推理需求因子
        if self._needs_inference(query):
            score += self.weights['inference']
        
        # 6. 多跳检测
        if self._needs_multi_hop(query):
            score += 0.1
        
        # 根据得分判断复杂度
        if score <= 0.3:
            return QueryComplexity.SIMPLE
        elif score <= 0.6:
            return QueryComplexity.MEDIUM
        else:
            return QueryComplexity.COMPLEX
    
    def _detect_sub_queries(self, query: str) -> List[str]:
        """检测子问题"""
        # 分隔符
        separators = ['，并且', '，同时', '，还有', '，另外', '?', '？', '和', '以及']
        
        sub_queries = []
        remaining = query
        
        for sep in separators:
            if sep in remaining:
                parts = remaining.split(sep)
                if len(parts) > 1:
                    sub_queries.extend([p.strip() for p in parts if p.strip()])
                    break
        
        return sub_queries if sub_queries else [query]
    
    def _needs_inference(self, query: str) -> bool:
        """判断是否需要推理"""
        inference_keywords = ['为什么', '原因', '如何分析', '怎么理解', '意味着', '说明什么']
        return any(kw in query for kw in inference_keywords)
    
    def _needs_multi_hop(self, query: str) -> bool:
        """判断是否需要多跳检索"""
        multi_hop_patterns = [
            r'.*的.*是.*',           # "A的B是C"型
            r'.*和.*的关系',         # 关系型
            r'.*属于.*',             # 归属型
            r'.*在哪里.*',           # 位置型
        ]
        
        for pattern in multi_hop_patterns:
            if re.search(pattern, query):
                return True
        
        return False


class IntentClassifier:
    """意图分类器"""
    
    # 意图特征关键词
    INTENT_KEYWORDS = {
        QueryIntent.FACTUAL: [
            '多少', '什么时候', '哪里', '谁', '哪个', '多大', '多长', '多重',
            '重量', '价格', '时间', '地点', '人数', '数量', '版本', '型号'
        ],
        QueryIntent.OPEN_ENDED: [
            '如何', '怎样', '怎么', '方法', '建议', '推荐', '看法', '观点',
            '最佳', '优化', '改进', '提升', '提高'
        ],
        QueryIntent.COMPARATIVE: [
            '区别', '差异', '比较', '对比', '不同', '哪个好', '哪个更',
            '优缺点', '优势', '劣势', '比', 'vs', 'VS'
        ],
        QueryIntent.PROCEDURAL: [
            '步骤', '流程', '怎么操作', '如何使用', '怎样安装', '教程',
            '指南', '说明书', '如何配置', '怎么设置'
        ],
        QueryIntent.TROUBLESHOOTING: [
            '为什么', '原因', '故障', '问题', '错误', '无法', '失败',
            '不工作', '不显示', '报错', '异常', '怎么办', '解决'
        ],
        QueryIntent.DEFINITION: [
            '是什么', '什么是', '定义', '概念', '含义', '意思',
            '解释', '介绍', '简述', '概述'
        ],
    }
    
    def __init__(self, llm_client=None, config: Dict = None):
        self.llm = llm_client
        self.config = config or {}
    
    def classify(self, query: str) -> Tuple[QueryIntent, float, List[QueryIntent]]:
        """
        分类查询意图
        
        Args:
            query: 查询文本
        
        Returns:
            (主意图, 置信度, 次要意图列表)
        """
        # 规则分类
        scores = {}
        
        for intent, keywords in self.INTENT_KEYWORDS.items():
            score = sum(1 for kw in keywords if kw in query) / len(keywords)
            if score > 0:
                scores[intent] = score
        
        # 如果没有匹配，使用LLM
        if not scores or max(scores.values()) < 0.1:
            if self.llm:
                return self._llm_classify(query)
            return QueryIntent.UNKNOWN, 0.5, []
        
        # 排序
        sorted_intents = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        
        primary_intent = sorted_intents[0][0]
        confidence = sorted_intents[0][1]
        secondary_intents = [intent for intent, score in sorted_intents[1:3] if score > 0.05]
        
        # 复合意图检测
        if len(sorted_intents) >= 2 and sorted_intents[1][1] > 0.1:
            primary_intent = QueryIntent.COMPOUND
            secondary_intents = [sorted_intents[0][0], sorted_intents[1][0]]
        
        # 归一化置信度
        confidence = min(1.0, confidence * 3)
        
        return primary_intent, confidence, secondary_intents
    
    def _llm_classify(self, query: str) -> Tuple[QueryIntent, float, List[QueryIntent]]:
        """使用LLM分类"""
        if not self.llm:
            return QueryIntent.UNKNOWN, 0.5, []
        
        try:
            prompt = f"""
请分析以下用户查询的意图类型：

查询：{query}

意图类型：
- factual: 事实型，查询具体事实（数量、时间、地点等）
- open_ended: 开放型，开放式问题（如何、建议等）
- comparative: 比较型，比较类问题（区别、对比等）
- procedural: 流程型，步骤类问题（如何操作、流程等）
- troubleshooting: 故障排查型，诊断问题（为什么、故障等）
- definition: 定义型，概念解释（是什么、定义等）
- compound: 复合型，包含多个意图

输出JSON格式：
{{
    "primary_intent": "意图类型",
    "confidence": 0.0-1.0,
    "secondary_intents": ["意图1", "意图2"],
    "reasoning": "判断理由"
}}
"""
            
            response = self.llm.invoke(prompt) if hasattr(self.llm, 'invoke') else self.llm(prompt)
            response_text = response.strip() if isinstance(response, str) else str(response)
            
            # 解析JSON
            json_match = re.search(r'\{[\s\S]*\}', response_text)
            if json_match:
                data = json.loads(json_match.group())
                
                primary = QueryIntent(data.get('primary_intent', 'unknown'))
                confidence = float(data.get('confidence', 0.5))
                secondary = [QueryIntent(s) for s in data.get('secondary_intents', [])]
                
                return primary, confidence, secondary
            
        except Exception as e:
            logger.error(f"LLM意图分类失败: {e}")
        
        return QueryIntent.UNKNOWN, 0.5, []


class EntityExtractor:
    """实体提取器"""
    
    def __init__(self, config: Dict = None):
        self.config = config or {}
    
    def extract(self, query: str) -> List[str]:
        """
        从查询中提取实体
        
        Args:
            query: 查询文本
        
        Returns:
            实体列表
        """
        entities = []
        
        # 1. 数字和单位
        numbers = re.findall(r'\d+(?:\.\d+)?(?:年|月|日|时|分|秒|元|万|亿|km|m|kg|g|GB|MB|%)?', query)
        entities.extend(numbers)
        
        # 2. 英文专有名词
        english = re.findall(r'\b[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*\b', query)
        entities.extend(english)
        
        # 3. 引号内容
        quoted = re.findall(r'[""「『]([^""「』」]+)[""』」]', query)
        entities.extend(quoted)
        
        # 4. 产品型号
        models = re.findall(r'[A-Z]+\d+[A-Z]*|\d+[A-Z]+\d*', query)
        entities.extend(models)
        
        # 去重
        return list(set(entities))


class StrategyRouter:
    """策略路由器 - 根据意图推荐处理策略"""
    
    # 各意图对应的默认策略
    INTENT_STRATEGIES = {
        QueryIntent.FACTUAL: {
            'retrieval_mode': 'bm25_weighted',
            'rerank': True,
            'top_k': 5,
            'multi_hop': False,
            'compression': True,
            'description': '精确匹配优先'
        },
        QueryIntent.OPEN_ENDED: {
            'retrieval_mode': 'vector_weighted',
            'rerank': True,
            'top_k': 10,
            'multi_hop': False,
            'compression': True,
            'description': '召回优先，内容丰富'
        },
        QueryIntent.COMPARATIVE: {
            'retrieval_mode': 'hybrid',
            'rerank': True,
            'top_k': 8,
            'multi_hop': True,
            'query_decomposition': True,
            'compression': True,
            'description': '双向检索+对比分析'
        },
        QueryIntent.PROCEDURAL: {
            'retrieval_mode': 'hybrid',
            'rerank': True,
            'top_k': 5,
            'multi_hop': False,
            'compression': False,
            'description': '保持步骤完整性'
        },
        QueryIntent.TROUBLESHOOTING: {
            'retrieval_mode': 'hybrid',
            'rerank': True,
            'top_k': 10,
            'multi_hop': True,
            'query_decomposition': True,
            'compression': True,
            'description': '广泛召回+多步分析'
        },
        QueryIntent.DEFINITION: {
            'retrieval_mode': 'vector_weighted',
            'rerank': True,
            'top_k': 3,
            'multi_hop': False,
            'compression': False,
            'description': '概念解释优先'
        },
        QueryIntent.COMPOUND: {
            'retrieval_mode': 'hybrid',
            'rerank': True,
            'top_k': 10,
            'multi_hop': True,
            'query_decomposition': True,
            'compression': True,
            'description': '分解子问题分别处理'
        },
    }
    
    def __init__(self, config: Dict = None):
        self.config = config or {}
    
    def route(self, intent_result: IntentResult) -> Dict[str, Any]:
        """
        根据意图结果推荐处理策略
        
        Args:
            intent_result: 意图识别结果
        
        Returns:
            处理策略配置
        """
        strategy = self.INTENT_STRATEGIES.get(
            intent_result.primary_intent,
            self.INTENT_STRATEGIES[QueryIntent.OPEN_ENDED]
        ).copy()
        
        # 根据复杂度调整
        if intent_result.complexity == QueryComplexity.SIMPLE:
            strategy['top_k'] = max(3, strategy.get('top_k', 5) - 2)
            strategy['multi_hop'] = False
        
        elif intent_result.complexity == QueryComplexity.COMPLEX:
            strategy['top_k'] = strategy.get('top_k', 5) + 5
            strategy['max_hops'] = 3
        
        # 添加元数据
        strategy['intent'] = intent_result.primary_intent.value
        strategy['complexity'] = intent_result.complexity.value
        strategy['confidence'] = intent_result.confidence
        
        return strategy


class QueryIntentRecognizer:
    """查询意图识别器 - 主入口类"""
    
    def __init__(self, llm_client=None, config: Dict = None):
        """
        初始化意图识别器
        
        Args:
            llm_client: LLM客户端
            config: 配置参数
        """
        self.config = config or {}
        self.llm = llm_client
        
        # 初始化组件
        self.normalizer = QueryNormalizer(llm_client, self.config)
        self.complexity_evaluator = ComplexityEvaluator(self.config)
        self.intent_classifier = IntentClassifier(llm_client, self.config)
        self.entity_extractor = EntityExtractor(self.config)
        self.strategy_router = StrategyRouter(self.config)
    
    def recognize(self, query: str) -> IntentResult:
        """
        识别查询意图
        
        Args:
            query: 用户查询
        
        Returns:
            IntentResult: 完整的意图识别结果
        """
        # 1. 标准化查询
        normalized = self.normalizer.normalize(query)
        
        # 2. 提取实体
        entities = self.entity_extractor.extract(query)
        
        # 3. 分类意图
        primary_intent, confidence, secondary_intents = self.intent_classifier.classify(normalized)
        
        # 4. 评估复杂度
        complexity = self.complexity_evaluator.evaluate(normalized, entities)
        
        # 5. 检测子问题
        sub_queries = self._detect_sub_queries(normalized, primary_intent)
        
        # 6. 生成推理过程
        reasoning = self._generate_reasoning(
            query, normalized, primary_intent, complexity, entities
        )
        
        # 7. 构建结果
        result = IntentResult(
            primary_intent=primary_intent,
            secondary_intents=secondary_intents,
            confidence=confidence,
            complexity=complexity,
            normalized_query=normalized,
            entities=entities,
            sub_queries=sub_queries,
            suggested_strategy={},
            reasoning=reasoning
        )
        
        # 8. 推荐策略
        result.suggested_strategy = self.strategy_router.route(result)
        
        return result
    
    def _detect_sub_queries(self, query: str, intent: QueryIntent) -> List[str]:
        """检测并分解子问题"""
        if intent != QueryIntent.COMPOUND:
            return []
        
        sub_queries = []
        
        # 按分隔符分解
        separators = ['，并且', '，同时', '，还有', '，另外', '和', '以及']
        
        for sep in separators:
            if sep in query:
                parts = query.split(sep)
                sub_queries = [p.strip() for p in parts if len(p.strip()) > 3]
                break
        
        # 如果有多个子问题，返回它们
        if len(sub_queries) > 1:
            return sub_queries
        
        return []
    
    def _generate_reasoning(self, original: str, normalized: str,
                            intent: QueryIntent, complexity: QueryComplexity,
                            entities: List[str]) -> str:
        """生成识别推理过程"""
        reasons = []
        
        # 查询标准化
        if original != normalized:
            reasons.append(f"查询已标准化：'{original}' → '{normalized}'")
        
        # 意图判断
        intent_desc = {
            QueryIntent.FACTUAL: "查询具体事实信息",
            QueryIntent.OPEN_ENDED: "开放式问题，需要综合回答",
            QueryIntent.COMPARATIVE: "比较类问题，需要对比分析",
            QueryIntent.PROCEDURAL: "流程类问题，需要步骤说明",
            QueryIntent.TROUBLESHOOTING: "故障排查问题",
            QueryIntent.DEFINITION: "概念定义问题",
            QueryIntent.COMPOUND: "复合问题，包含多个子意图",
        }
        reasons.append(f"判断为{intent_desc.get(intent, '未知意图')}")
        
        # 复杂度
        complexity_desc = {
            QueryComplexity.SIMPLE: "简单问题，单次检索可回答",
            QueryComplexity.MEDIUM: "中等复杂度，可能需要多次检索",
            QueryComplexity.COMPLEX: "复杂问题，需要多跳检索或深度推理",
        }
        reasons.append(complexity_desc[complexity])
        
        # 实体
        if entities:
            reasons.append(f"识别到关键实体：{', '.join(entities[:5])}")
        
        return "；".join(reasons)
    
    def get_strategy(self, query: str) -> Dict[str, Any]:
        """
        便捷方法：直接获取处理策略
        
        Args:
            query: 用户查询
        
        Returns:
            处理策略配置
        """
        result = self.recognize(query)
        return result.suggested_strategy
    
    def is_multi_hop_needed(self, query: str) -> bool:
        """
        判断是否需要多跳检索
        
        Args:
            query: 用户查询
        
        Returns:
            是否需要多跳
        """
        result = self.recognize(query)
        return result.suggested_strategy.get('multi_hop', False)


# 使用示例
if __name__ == '__main__':
    # 创建意图识别器
    recognizer = QueryIntentRecognizer()
    
    # 测试查询
    test_queries = [
        "产品A的价格是多少？",
        "如何优化RAG系统的检索效果？",
        "RAG和微调有什么区别？",
        "手机咋充不进电呢？",
        "什么是知识图谱？",
        "RAG的优势是什么，以及如何实现？",
        "产品A的供应商在哪里生产？",
    ]
    
    print("\n=== 查询意图识别结果 ===\n")
    
    for query in test_queries:
        result = recognizer.recognize(query)
        
        print(f"查询: {query}")
        print(f"  标准化: {result.normalized_query}")
        print(f"  主意图: {result.primary_intent.value}")
        print(f"  复杂度: {result.complexity.value}")
        print(f"  置信度: {result.confidence:.0%}")
        print(f"  实体: {result.entities}")
        if result.sub_queries:
            print(f"  子问题: {result.sub_queries}")
        print(f"  推荐策略: {result.suggested_strategy.get('description', '')}")
        print(f"  推理: {result.reasoning}")
        print()
