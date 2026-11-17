#!/usr/bin/env python3
"""
RAG系统评估脚本

使用方法：
    python evaluate.py --config config.json --test-data test_cases.json

输出：
    - 评估报告（JSON）
    - 可览化图表（可选）
"""

import os
import sys
import argparse
import json
import statistics
import importlib
import inspect
from dataclasses import dataclass

# 统一 LLM 客户端抽象层
from llm_client import LLMClient, OpenAILikeClient, wrap_llm
from typing import List, Dict, Any, Optional
import logging

# ============================================================
# 自动加载 .env
# ============================================================
# H4 配套环节②：不再在此处另起一套 try/import dotenv，统一复用 llm_client 的入口。
# （`import llm_client` 时已自动加载一次；这里再显式调用只为记录状态，load_dotenv 幂等。）


# 设置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def _median(values: list) -> float:
    """
    中位数（H11 的单一职责点）。

    原实现 `sum(sorted(v)[n//2-1:n//2+1]) / min(2, len(v))` 恒取两个元素做平均：
    偶数长度碰巧正确（[1,2,3,4] → 2.5），奇数长度系统性偏低（[1,2,3,4,5] → 2.5，
    正确值 3.0）。3/5/9 条用例的评估报告都会受影响——而测试用例数量恰好奇数居多。

    抽出本函数的另一个理由：修复前该表达式在汇总处被复制了两遍（检索汇总、
    生成汇总），改一处漏一处是必然的。探针 `probe_round2.py::F6` 直接调用本函数，
    不再在探针里复刻一份公式（复刻会导致探针测的是自己，永远绿）。

    Args:
        values: 数值列表，可为空

    Returns:
        中位数；空列表返回 0（保持既有行为，避免下游除零）
    """
    return statistics.median(values) if values else 0

from llm_client import load_dotenv_if_available  # noqa: E402
DOTENV_LOADED = load_dotenv_if_available()       # noqa: E402
logger.debug(f".env 加载状态: {'已加载' if DOTENV_LOADED else '未加载（依赖真实环境变量）'}")


@dataclass
class TestCase:
    """测试用例"""
    query: str
    expected_answer: str
    expected_doc_ids: List[str]
    category: Optional[str] = None
    difficulty: Optional[str] = None  # easy, medium, hard


@dataclass
class EvaluationResult:
    """评估结果"""
    query: str
    retrieved_docs: List[str]
    generated_answer: str
    retrieval_metrics: Dict[str, float]
    generation_metrics: Dict[str, float]
    latency_ms: float


class RAGEvaluator:
    """RAG系统评估器"""

    # NVIDIA API 配置（默认值，可用环境变量 DOUBAO_API_URL / DOUBAO_MODEL 覆盖）
    # 说明：项目实际使用 NVIDIA API（通过 .env 桥接），豆包变量名保持不变
    DOUBAO_API_URL = "https://integrate.api.nvidia.com/v1/chat/completions"
    DOUBAO_MODEL = "nvidia/nemotron-3-super-120b-a12b"  # 默认 NVIDIA 推理模型

    def __init__(self, rag_system, config: Dict = None):
        """
        初始化评估器

        Args:
            rag_system: RAG系统实例
            config: 评估配置
        """
        self.rag = rag_system
        self.config = config or {}

        # API 端点与模型支持环境变量覆盖（DOUBAO_API_URL / DOUBAO_MODEL）
        self.DOUBAO_API_URL = os.getenv("DOUBAO_API_URL", self.DOUBAO_API_URL)
        # 桥接：若 DOUBAO_API_URL 未通过环境变量覆盖，尝试从 NVIDIA_API_URL 获取
        if not os.getenv("DOUBAO_API_URL") and os.getenv("NVIDIA_API_URL"):
            self.DOUBAO_API_URL = os.getenv("NVIDIA_API_URL")
        self.DOUBAO_MODEL = os.getenv("DOUBAO_MODEL", self.DOUBAO_MODEL)

        # 获取 Doubao API 凭证（支持自动获取和手动配置）
        self.api_key, self.credential_source = self._get_doubao_api_key()

        # 使用平台 SDK 的 requests（仅供参考，实际调用通过 llm_client）
        self.requests_client = None
        if self.api_key:
            try:
                from coze_workload_identity import requests
                self.requests_client = requests
                logger.info(f"✓ 凭证获取成功（来源: {self.credential_source}），使用平台 SDK 进行 API 调用")
                logger.info(f"✓ 使用豆包（Doubao）大模型进行评估")
            except Exception as e:
                logger.warning(f"平台 SDK 初始化失败: {e}")
        else:
            logger.warning("✗ 未找到 Doubao API Key，LLM 评估功能将不可用")

        # 使用统一 LLM 客户端（OpenAI 兼容协议）
        if self.api_key:
            try:
                llm = OpenAILikeClient(
                    api_key=self.api_key,
                    api_url=self.DOUBAO_API_URL,
                    model=self.metrics_config['llm_model']
                )
                # H23: OpenAILikeClient 本身就是 LLMClient 子类，
                # 再包一层会造成 3×3=9 次重试放大；wrap_llm 对已是
                # LLMClient 的入参原样返回。
                self.llm_client = wrap_llm(llm)
                logger.info("✓ 使用统一 LLM 客户端进行评估")
            except Exception as e:
                logger.warning(f"LLM 客户端初始化失败: {e}")
                self.llm_client = None
        else:
            self.llm_client = None
            logger.warning("✗ 未找到 API Key，LLM 评估将不可用")

        # 默认配置
        self.metrics_config = {
            'recall_k': [5, 10, 20],
            'precision_k': [5, 10],
            'use_llm_judge': True,
            'llm_model': self.DOUBAO_MODEL
        }
        self.metrics_config.update(self.config.get('metrics', {}))

    def _get_doubao_api_key(self) -> tuple[Optional[str], str]:
        """
        获取 Doubao API Key

        优先级：
        1. Workload Identity 自动获取（如果环境支持）
        2. 环境变量读取（用户手动配置）
        3. 返回 None（降级使用简单指标）

        Returns:
            (API Key 或 None, 凭证来源描述)
        """
        skill_id = "7625263899650293803"

        # 方式 1：尝试使用 Workload Identity 自动获取
        try:
            from coze_workload_identity.client import Client
            client = Client()
            api_key = client.get_integration_credential("doubao")

            if api_key:
                source = "Workload Identity (自动获取)"
                logger.info(f"✓ 通过 Workload Identity 自动获取 Doubao 凭证")
                return api_key, source
        except ImportError:
            logger.debug("coze_workload_identity.client 不可用")
        except Exception as e:
            logger.debug(f"Workload Identity 获取失败: {type(e).__name__}")

        # 方式 2：从环境变量读取（用户手动配置）
        api_key = os.getenv(f"COZE_DOUBAO_API_KEY_{skill_id}")
        if api_key:
            source = f"环境变量 COZE_DOUBAO_API_KEY_{skill_id} (手动配置)"
            logger.info(f"✓ 从环境变量读取 Doubao API Key")
            return api_key, source

        # 方式 3：尝试通用环境变量（备用）
        api_key = os.getenv("DOUBAO_API_KEY")
        if api_key:
            source = "环境变量 DOUBAO_API_KEY (备用)"
            logger.info(f"✓ 从 DOUBAO_API_KEY 读取")
            return api_key, source

        # 方式 4：桥接 NVIDIA API 凭证（来自 .env 文件）
        api_key = os.getenv("NVIDIA_API_KEY")
        if api_key:
            source = "环境变量 NVIDIA_API_KEY (自动桥接，来自 .env)"
            logger.info(f"✓ 从 NVIDIA_API_KEY 读取（自动桥接到 DOUBAO 协议）")
            return api_key, source

        # 全部失败
        logger.warning("✗ 无法获取 Doubao API Key（所有方式均失败）")
        logger.warning("  可用方式：")
        logger.warning("    1. Workload Identity（需要环境变量支持）")
        logger.warning(f"    2. 环境变量 COZE_DOUBAO_API_KEY_{skill_id}")
        logger.warning("    3. 环境变量 DOUBAO_API_KEY（备用）")
        return None, "none"

    def evaluate(self, test_cases: List[TestCase]) -> Dict[str, Any]:
        """
        执行完整评估

        Args:
            test_cases: 测试用例列表

        Returns:
            评估报告
        """
        logger.info(f"开始评估，共 {len(test_cases)} 个测试用例")
        if self.api_key:
            logger.info(f"凭证来源: {self.credential_source}")
            logger.info(f"使用模型: {self.metrics_config['llm_model']}")
        else:
            logger.info("将使用简单指标（LLM 评估不可用）")

        results = []

        for i, case in enumerate(test_cases):
            logger.info(f"处理测试用例 {i+1}/{len(test_cases)}: {case.query[:50]}...")

            # 执行查询
            import time
            start_time = time.time()
            response = self.rag.query(case.query)
            latency = (time.time() - start_time) * 1000

            # 计算指标
            retrieval_metrics = self._calc_retrieval_metrics(
                response.get('sources', []),
                case.expected_doc_ids
            )

            generation_metrics = self._calc_generation_metrics(
                response.get('answer', ''),
                case.expected_answer,
                response.get('sources', []),
                case.query
            )

            results.append(EvaluationResult(
                query=case.query,
                retrieved_docs=response.get('sources', []),
                generated_answer=response.get('answer', ''),
                retrieval_metrics=retrieval_metrics,
                generation_metrics=generation_metrics,
                latency_ms=latency
            ))

        # 汇总报告
        report = self._generate_report(results, test_cases)

        return report

    def _calc_retrieval_metrics(self, retrieved: List, expected: List[str]) -> Dict[str, float]:
        """计算检索指标"""
        # 防御性处理：确保参数不为 None
        retrieved = retrieved or []
        expected = expected or []

        retrieved_ids = [doc.get('id', doc) if isinstance(doc, dict) else doc for doc in retrieved]

        metrics = {}

        # Recall@K
        for k in self.metrics_config['recall_k']:
            top_k = retrieved_ids[:k]
            if expected:
                recall = len(set(top_k) & set(expected)) / len(expected)
            else:
                recall = 0
            metrics[f'recall@{k}'] = recall

        # Precision@K
        for k in self.metrics_config['precision_k']:
            top_k = retrieved_ids[:k]
            if top_k:
                precision = len(set(top_k) & set(expected)) / len(top_k)
            else:
                precision = 0
            metrics[f'precision@{k}'] = precision

        # MRR (Mean Reciprocal Rank)
        mrr = 0
        for i, doc_id in enumerate(retrieved_ids):
            if expected and doc_id in expected:  # 修复：先检查 expected 不为空
                mrr = 1 / (i + 1)
                break
        metrics['mrr'] = mrr

        return metrics

    def _calc_generation_metrics(self, answer: str, expected: str,
                                  sources: List, query: str) -> Dict[str, float]:
        """计算生成指标"""
        metrics = {}

        if self.metrics_config['use_llm_judge'] and self.llm_client:
            # 使用LLM评估
            metrics['relevance'] = self._llm_judge_relevance(query, answer)
            metrics['faithfulness'] = self._llm_judge_faithfulness(answer, sources)
            metrics['completeness'] = self._llm_judge_completeness(answer, expected)
        else:
            # 使用简单指标
            metrics['answer_length'] = len(answer)
            metrics['overlap_score'] = self._calc_overlap(answer, expected)

        return metrics

    def _llm_judge_relevance(self, query: str, answer: str) -> float:
        """LLM评估相关性"""
        if not self.llm_client:
            return 0.5

        prompt = f"""请评估答案与问题的相关性（0-1分）：

问题：{query}
答案：{answer}

只返回一个0到1之间的数字，不要其他内容。"""
        return self.llm_client.score(prompt, default=0.5)

    def _llm_judge_faithfulness(self, answer: str, sources: List) -> float:
        """LLM评估忠实度"""
        if not self.llm_client:
            return 0.5

        context = '\n\n'.join([str(s) for s in sources])
        prompt = f"""请评估答案是否基于提供的上下文生成，有无幻觉（0-1分）：

上下文：{context}
答案：{answer}

只返回一个0到1之间的数字，不要其他内容。
1分表示完全基于上下文，0分表示完全无关或有明显幻觉。"""
        return self.llm_client.score(prompt, default=0.5)
    def _llm_judge_completeness(self, answer: str, expected: str) -> float:
        """LLM评估完整性"""
        if not self.llm_client:
            return 0.5

        prompt = f"""请评估答案的完整性（0-1分）：

期望答案要点：{expected}
实际答案：{answer}

只返回一个0到1之间的数字，不要其他内容。"""
        return self.llm_client.score(prompt, default=0.5)

    def _calc_overlap(self, answer: str, expected: str) -> float:
        """计算文本重叠度"""
        # 防御性处理
        answer = answer or ""
        expected = expected or ""

        answer_words = set(answer.lower().split())
        expected_words = set(expected.lower().split())

        if not expected_words:
            return 0

        overlap = len(answer_words & expected_words) / len(expected_words)
        return overlap

    def _generate_report(self, results: List[EvaluationResult],
                         test_cases: List[TestCase]) -> Dict[str, Any]:
        """生成评估报告"""
        # 防御性处理：检查结果是否为空
        if not results:
            return {
                'summary': {
                    'total_cases': 0,
                    'retrieval': {},
                    'generation': {},
                    'performance': {}
                },
                'category_analysis': {},
                'difficulty_analysis': {},
                'detailed_results': []
            }

        # 汇总检索指标
        retrieval_summary = {}
        if results[0].retrieval_metrics:
            for metric in results[0].retrieval_metrics.keys():
                values = [r.retrieval_metrics.get(metric, 0) for r in results]
                retrieval_summary[metric] = {
                    'mean': sum(values) / len(values) if values else 0,
                    'min': min(values) if values else 0,
                    'max': max(values) if values else 0,
                    # H11: 统一走 _median() 单一职责点（奇偶均正确）
                    'median': _median(values)
                }

        # 汇总生成指标
        generation_summary = {}
        if results[0].generation_metrics:
            for metric in results[0].generation_metrics.keys():
                values = [r.generation_metrics.get(metric, 0) for r in results]
                generation_summary[metric] = {
                    'mean': sum(values) / len(values) if values else 0,
                    'min': min(values) if values else 0,
                    'max': max(values) if values else 0,
                    # H11: 统一走 _median() 单一职责点（奇偶均正确）
                    'median': _median(values)
                }

        # 汇总性能指标
        latencies = [r.latency_ms for r in results]
        performance_summary = {
            'avg_latency_ms': sum(latencies) / len(latencies) if latencies else 0,
            'p50_latency_ms': sorted(latencies)[len(latencies) // 2] if latencies else 0,
            'p95_latency_ms': sorted(latencies)[int(len(latencies) * 0.95)] if len(latencies) > 1 else (latencies[0] if latencies else 0),
            'p99_latency_ms': sorted(latencies)[int(len(latencies) * 0.99)] if len(latencies) > 1 else (latencies[0] if latencies else 0)
        }

        # 按类别分析
        category_analysis = {}
        for case, result in zip(test_cases, results):
            if case.category:
                if case.category not in category_analysis:
                    category_analysis[case.category] = []
                category_analysis[case.category].append(result)

        category_summary = {}
        for category, cat_results in category_analysis.items():
            category_summary[category] = {
                'count': len(cat_results),
                'avg_recall@5': sum(r.retrieval_metrics.get('recall@5', 0) for r in cat_results) / len(cat_results),
                'avg_relevance': sum(r.generation_metrics.get('relevance', 0) for r in cat_results) / len(cat_results)
            }

        # 按难度分析
        difficulty_analysis = {}
        for case, result in zip(test_cases, results):
            if case.difficulty:
                if case.difficulty not in difficulty_analysis:
                    difficulty_analysis[case.difficulty] = []
                difficulty_analysis[case.difficulty].append(result)

        difficulty_summary = {}
        for difficulty, diff_results in difficulty_analysis.items():
            difficulty_summary[difficulty] = {
                'count': len(diff_results),
                'avg_recall@5': sum(r.retrieval_metrics.get('recall@5', 0) for r in diff_results) / len(diff_results),
                'avg_relevance': sum(r.generation_metrics.get('relevance', 0) for r in diff_results) / len(diff_results)
            }

        return {
            'summary': {
                'total_cases': len(test_cases),
                'retrieval': retrieval_summary,
                'generation': generation_summary,
                'performance': performance_summary
            },
            'category_analysis': category_summary,
            'difficulty_analysis': difficulty_summary,
            'detailed_results': [
                {
                    'query': r.query,
                    'retrieval': r.retrieval_metrics,
                    'generation': r.generation_metrics,
                    'latency_ms': r.latency_ms
                }
                for r in results
            ]
        }


def load_test_cases(file_path: str) -> List[TestCase]:
    """加载测试用例"""
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    return [
        TestCase(
            query=item['query'],
            expected_answer=item.get('expected_answer', ''),
            expected_doc_ids=item.get('expected_doc_ids', []),
            category=item.get('category'),
            difficulty=item.get('difficulty')
        )
        for item in data
    ]


def save_report(report: Dict, output_path: str):
    """保存评估报告"""
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    logger.info(f"报告已保存到: {output_path}")


def print_summary(report: Dict):
    """打印摘要"""
    print("\n" + "="*60)
    print("RAG系统评估报告")
    print("="*60)

    summary = report.get('summary', {})

    # 检索性能
    retrieval = summary.get('retrieval', {})
    if retrieval:
        print("\n📊 检索性能:")
        for metric, values in retrieval.items():
            if values and isinstance(values, dict):
                print(f"  {metric}: {values.get('mean', 0):.3f} (中位数: {values.get('median', 0):.3f})")

    # 生成质量
    generation = summary.get('generation', {})
    if generation:
        print("\n📝 生成质量:")
        for metric, values in generation.items():
            if values and isinstance(values, dict):
                print(f"  {metric}: {values.get('mean', 0):.3f}")

    # 性能指标
    performance = summary.get('performance', {})
    if performance:
        print("\n⚡ 性能指标:")
        print(f"  平均延迟: {performance.get('avg_latency_ms', 0):.1f}ms")
        print(f"  P95延迟: {performance.get('p95_latency_ms', 0):.1f}ms")

    if report.get('category_analysis'):
        print("\n📂 分类分析:")
        for category, stats in report['category_analysis'].items():
            if stats:
                print(f"  {category}: Recall@5={stats.get('avg_recall@5', 0):.3f}, 相关性={stats.get('avg_relevance', 0):.3f}")

    if report.get('difficulty_analysis'):
        print("\n🎯 难度分析:")
        for difficulty, stats in report['difficulty_analysis'].items():
            if stats:
                print(f"  {difficulty}: Recall@5={stats.get('avg_recall@5', 0):.3f}, 相关性={stats.get('avg_relevance', 0):.3f}")

    print("\n" + "="*60)


def print_comparison(old_report: Dict, new_report: Dict):
    """打印新旧评估报告的指标对比（Ablation 前后 diff）"""
    print("\n" + "=" * 60)
    print("指标对比（旧 → 新）")
    print("=" * 60)

    old_summary = old_report.get('summary', {})
    new_summary = new_report.get('summary', {})
    old_retrieval = old_summary.get('retrieval', {})
    new_retrieval = new_summary.get('retrieval', {})

    # 检索指标（越高越好）
    print("\n📊 检索指标:")
    for metric in sorted(set(old_retrieval) | set(new_retrieval)):
        old_val = old_retrieval.get(metric, {}).get('mean', 0) if isinstance(old_retrieval.get(metric), dict) else 0
        new_val = new_retrieval.get(metric, {}).get('mean', 0) if isinstance(new_retrieval.get(metric), dict) else 0
        diff = new_val - old_val
        arrow = "↑" if diff > 0.001 else ("↓" if diff < -0.001 else "→")
        print(f"  {metric}: {old_val:.3f} → {new_val:.3f} ({arrow} {diff:+.3f})")

    # 生成指标（越高越好）
    old_gen = old_summary.get('generation', {})
    new_gen = new_summary.get('generation', {})
    if old_gen or new_gen:
        print("\n📝 生成质量:")
        for metric in sorted(set(old_gen) | set(new_gen)):
            old_val = old_gen.get(metric, {}).get('mean', 0) if isinstance(old_gen.get(metric), dict) else 0
            new_val = new_gen.get(metric, {}).get('mean', 0) if isinstance(new_gen.get(metric), dict) else 0
            diff = new_val - old_val
            arrow = "↑" if diff > 0.001 else ("↓" if diff < -0.001 else "→")
            print(f"  {metric}: {old_val:.3f} → {new_val:.3f} ({arrow} {diff:+.3f})")

    # 性能指标（越低越好）
    old_perf = old_summary.get('performance', {})
    new_perf = new_summary.get('performance', {})
    if old_perf or new_perf:
        print("\n⚡ 性能指标（↓ 为改进）:")
        for metric in ['avg_latency_ms', 'p50_latency_ms', 'p95_latency_ms']:
            old_val = old_perf.get(metric, 0)
            new_val = new_perf.get(metric, 0)
            diff = new_val - old_val
            arrow = "↓" if diff < -0.1 else ("↑" if diff > 0.1 else "→")
            print(f"  {metric}: {old_val:.1f} → {new_val:.1f} ({arrow} {diff:+.1f}ms)")

    # 分类分析（Recall@5）
    old_cat = old_report.get('category_analysis', {})
    new_cat = new_report.get('category_analysis', {})
    if old_cat or new_cat:
        print("\n📂 分类 Recall@5:")
        for cat in sorted(set(old_cat) | set(new_cat)):
            old_val = old_cat.get(cat, {}).get('avg_recall@5', 0) if isinstance(old_cat.get(cat), dict) else 0
            new_val = new_cat.get(cat, {}).get('avg_recall@5', 0) if isinstance(new_cat.get(cat), dict) else 0
            diff = new_val - old_val
            arrow = "↑" if diff > 0.001 else ("↓" if diff < -0.001 else "→")
            print(f"  {cat}: {old_val:.3f} → {new_val:.3f} ({arrow} {diff:+.3f})")

    print("\n" + "=" * 60)


def load_rag_system(rag_class_spec: str = None,
                    config: Dict = None,
                    config_path: str = None):
    """
    H3：按 `--rag-class` 加载真实 RAG 系统；未指定时**显式**回退到 MockRAG。

    此前 main() 里 `args.config` 从未被使用，评估永远跑硬编码 MockRAG，
    用户以为拿到了真实系统的评估报告。这里把选择权交回给用户，
    并在回退时给出醒目警告（H3 配套环节①）。

    Args:
        rag_class_spec: "module:ClassName" 格式，如 `myrag.MyRAG:MyRAG`
        config: 已加载的配置字典（供接受 config= 的类使用）
        config_path: 配置文件路径（供接受 config_path= 的类使用）

    Returns:
        (rag_system, system_label)
    """
    if not rag_class_spec:
        class MockRAG:
            """仅用于流程演示：固定返回 doc_0..doc_4，结果不代表任何真实系统质量。"""

            def query(self, q):
                return {
                    'answer': f"这是对'{q}'的回答",
                    'sources': [{'id': f'doc_{i}'} for i in range(5)]
                }

        logger.warning("\n" + "=" * 62 + "\n"
                       "WARNING: 未指定 --rag-class，正在使用 MockRAG 评估。\n"
                       "  MockRAG 固定返回 doc_0..doc_4，本次报告的所有指标\n"
                       "  不代表任何真实系统的检索/生成质量，仅供流程演示。\n"
                       "  真实评估请传：--rag-class your_module:YourRAGClass\n"
                       + "=" * 62)
        return MockRAG(), "MockRAG"

    module_name, _, class_name = rag_class_spec.partition(":")
    if not module_name or not class_name:
        raise ValueError(
            f"--rag-class 格式应为 'module:ClassName'，实际收到: {rag_class_spec!r}")

    mod = importlib.import_module(module_name)
    cls = getattr(mod, class_name)

    # 按被测类的构造签名选择传参方式。
    # 不用 try/except TypeError 兜底——那会吞掉类内部的真实 TypeError。
    params = inspect.signature(cls.__init__).parameters
    kwargs = {}
    if "config_path" in params and config_path:
        kwargs["config_path"] = config_path
    elif "config" in params and config is not None:
        kwargs["config"] = config

    return cls(**kwargs), f"{module_name}.{class_name}"


def main():
    # Windows 控制台默认 GBK 编码无法打印 emoji，强制 UTF-8 输出
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
        sys.stderr.reconfigure(encoding='utf-8', errors='replace')

    parser = argparse.ArgumentParser(description='RAG系统评估工具')
    parser.add_argument('--config', type=str, default='config.json', help='配置文件路径')
    parser.add_argument('--rag-class', type=str, default=None,
                        help='待评估的真实 RAG 系统，格式 "module:ClassName"。'
                             '缺省时回退到 MockRAG（仅流程演示，指标不代表真实系统）')
    parser.add_argument('--test-data', type=str, required=True, help='测试数据路径')
    parser.add_argument('--output', type=str, default='evaluation_report.json', help='输出报告路径')
    parser.add_argument('--compare', type=str, default=None, help='旧报告路径，输出新旧指标对比（Ablation）')
    parser.add_argument('--verbose', action='store_true', help='详细输出')

    args = parser.parse_args()

    # H3：--config 不再是死参数，真正加载并传给评估器
    config = None
    if args.config:
        try:
            with open(args.config, 'r', encoding='utf-8') as f:
                config = json.load(f)
            logger.info(f"已加载配置文件: {args.config}")
        except FileNotFoundError:
            logger.warning(f"配置文件不存在（{args.config}），将使用默认评估配置")
        except json.JSONDecodeError as e:
            logger.error(f"配置文件 JSON 解析失败（{args.config}）: {e}")

    # 加载测试用例
    test_cases = load_test_cases(args.test_data)
    logger.info(f"已加载 {len(test_cases)} 个测试用例")

    rag, system_label = load_rag_system(args.rag_class, config, args.config)
    logger.info(f"待评估系统: {system_label}")

    # 执行评估
    evaluator = RAGEvaluator(rag, config=config)
    report = evaluator.evaluate(test_cases)

    # H3 配套环节②：报告里标明本次评估对象，Mock 结果不会被误读为真实指标
    report.setdefault('metadata', {})
    report['metadata'].update({
        'evaluated_system': system_label,
        'is_mock': system_label == 'MockRAG',
        'config_path': args.config if config is not None else None,
    })

    # 保存报告
    save_report(report, args.output)

    # 打印摘要
    print_summary(report)

    # 对比旧报告（Ablation）
    if args.compare:
        try:
            with open(args.compare, 'r', encoding='utf-8') as f:
                old_report = json.load(f)
            print_comparison(old_report, report)
        except Exception as e:
            logger.error(f"加载对比报告失败: {e}")
            print(f"⚠️ 无法加载旧报告 {args.compare}，跳过对比：{e}")


if __name__ == '__main__':
    main()
