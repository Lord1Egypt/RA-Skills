#!/usr/bin/env python3
"""
RAG系统评估脚本

使用方法：
    python evaluate.py --config config.json --test-data test_cases.json

输出：
    - 评估报告（JSON）
    - 可视化图表（可选）
"""

import argparse
import json
from dataclasses import dataclass
from typing import List, Dict, Any, Optional
import logging

# 设置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


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
    
    def __init__(self, rag_system, config: Dict = None):
        """
        初始化评估器
        
        Args:
            rag_system: RAG系统实例
            config: 评估配置
        """
        self.rag = rag_system
        self.config = config or {}
        
        # 默认配置
        self.metrics_config = {
            'recall_k': [5, 10, 20],
            'precision_k': [5, 10],
            'use_llm_judge': True,
            'llm_model': 'claude-3-5-sonnet-20241022'
        }
        self.metrics_config.update(self.config.get('metrics', {}))
    
    def evaluate(self, test_cases: List[TestCase]) -> Dict[str, Any]:
        """
        执行完整评估
        
        Args:
            test_cases: 测试用例列表
        
        Returns:
            评估报告
        """
        logger.info(f"开始评估，共 {len(test_cases)} 个测试用例")
        
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
        
        if self.metrics_config['use_llm_judge']:
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
        try:
            import anthropic
            client = anthropic.Anthropic()
            
            prompt = f"""
            请评估答案与问题的相关性（0-1分）：
            
            问题：{query}
            答案：{answer}
            
            只返回一个0到1之间的数字，不要其他内容。
            """
            
            response = client.messages.create(
                model=self.metrics_config['llm_model'],
                max_tokens=10,
                messages=[{"role": "user", "content": prompt}]
            )
            
            return float(response.content[0].text.strip())
        except Exception as e:
            logger.warning(f"LLM评估失败: {e}")
            return 0.5
    
    def _llm_judge_faithfulness(self, answer: str, sources: List) -> float:
        """LLM评估忠实度"""
        try:
            import anthropic
            client = anthropic.Anthropic()
            
            context = '\n\n'.join([str(s) for s in sources])
            
            prompt = f"""
            请评估答案是否基于提供的上下文生成，有无幻觉（0-1分）：
            
            上下文：{context}
            答案：{answer}
            
            只返回一个0到1之间的数字，不要其他内容。
            1分表示完全基于上下文，0分表示完全无关或有明显幻觉。
            """
            
            response = client.messages.create(
                model=self.metrics_config['llm_model'],
                max_tokens=10,
                messages=[{"role": "user", "content": prompt}]
            )
            
            return float(response.content[0].text.strip())
        except Exception as e:
            logger.warning(f"LLM评估失败: {e}")
            return 0.5
    
    def _llm_judge_completeness(self, answer: str, expected: str) -> float:
        """LLM评估完整性"""
        try:
            import anthropic
            client = anthropic.Anthropic()
            
            prompt = f"""
            请评估答案的完整性（0-1分）：
            
            期望答案要点：{expected}
            实际答案：{answer}
            
            只返回一个0到1之间的数字，不要其他内容。
            """
            
            response = client.messages.create(
                model=self.metrics_config['llm_model'],
                max_tokens=10,
                messages=[{"role": "user", "content": prompt}]
            )
            
            return float(response.content[0].text.strip())
        except Exception as e:
            logger.warning(f"LLM评估失败: {e}")
            return 0.5
    
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
                    'median': sorted(values)[len(values) // 2] if values else 0
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
                    'median': sorted(values)[len(values) // 2] if values else 0
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


def main():
    parser = argparse.ArgumentParser(description='RAG系统评估工具')
    parser.add_argument('--config', type=str, default='config.json', help='配置文件路径')
    parser.add_argument('--test-data', type=str, required=True, help='测试数据路径')
    parser.add_argument('--output', type=str, default='evaluation_report.json', help='输出报告路径')
    parser.add_argument('--verbose', action='store_true', help='详细输出')
    
    args = parser.parse_args()
    
    # 加载测试用例
    test_cases = load_test_cases(args.test_data)
    logger.info(f"已加载 {len(test_cases)} 个测试用例")
    
    # 这里需要替换为你的RAG系统实例
    # from your_rag import YourRAGSystem
    # rag = YourRAGSystem(config_path=args.config)
    
    # 示例：使用mock进行演示
    class MockRAG:
        def query(self, q):
            return {
                'answer': f"这是对'{q}'的回答",
                'sources': [{'id': f'doc_{i}'} for i in range(5)]
            }
    
    rag = MockRAG()
    
    # 执行评估
    evaluator = RAGEvaluator(rag)
    report = evaluator.evaluate(test_cases)
    
    # 保存报告
    save_report(report, args.output)
    
    # 打印摘要
    print_summary(report)


if __name__ == '__main__':
    main()
