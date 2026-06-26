#!/usr/bin/env python3
"""
搜索质量评分器 - 评估搜索结果质量
"""
from typing import List, Dict, Tuple
from dataclasses import dataclass
import re


@dataclass
class QualityScore:
    """质量评分"""
    relevance: float      # 相关性 (0-1)
    coverage: float        # 覆盖率 (0-1)
    diversity: float      # 多样性 (0-1)
    freshness: float      # 新鲜度 (0-1)
    overall: float        # 综合评分 (0-1)
    issues: List[str]    # 问题列表


class SearchQualityScorer:
    """搜索质量评分器"""
    
    def __init__(self):
        self.min_score_threshold = 0.3  # 最低分数阈值
    
    def score_results(
        self,
        results: List[Dict],
        query: str,
        expected_types: List[str] = None
    ) -> Tuple[List[Dict], QualityScore]:
        """
        评估搜索结果质量
        
        Args:
            results: 搜索结果列表
            query: 查询文本
            expected_types: 期望的结果类型
        
        Returns:
            (过滤后的结果, 质量评分)
        """
        if not results:
            return [], QualityScore(0, 0, 0, 0, 0, ["No results"])
        
        issues = []
        
        # 1. 相关性评分
        query_terms = set(query.lower().split())
        relevance_scores = []
        for r in results:
            content = r.get("content", r.get("s", "")).lower()
            title = r.get("title", r.get("t", "")).lower()
            
            # 计算词项覆盖率
            content_terms = set(re.findall(r'\w+', content))
            title_terms = set(re.findall(r'\w+', title))
            
            term_coverage = len(query_terms & content_terms) / max(len(query_terms), 1)
            title_match = len(query_terms & title_terms) / max(len(query_terms), 1)
            
            relevance = term_coverage * 0.6 + title_match * 0.4
            relevance_scores.append(relevance)
            
            r["_relevance"] = relevance
        
        # 2. 覆盖率评分（结果数量是否足够）
        coverage = min(len(results) / 5, 1.0)  # 期望至少5个结果
        if len(results) < 3:
            issues.append("结果数量不足")
        
        # 3. 多样性评分（类型分布）
        types = [r.get("type", "unknown") for r in results]
        unique_types = len(set(types))
        type_diversity = min(unique_types / 3, 1.0)  # 期望至少3种类型
        
        # 4. 新鲜度评分
        freshness_scores = []
        for r in results:
            updated_at = r.get("updated_at", r.get("updatedAt", ""))
            if updated_at:
                # 简单评分：越新越好
                freshness_scores.append(0.8)
            else:
                freshness_scores.append(0.5)
        
        avg_relevance = sum(relevance_scores) / len(relevance_scores) if relevance_scores else 0
        avg_freshness = sum(freshness_scores) / len(freshness_scores) if freshness_scores else 0
        
        # 综合评分
        overall = (
            avg_relevance * 0.4 +
            coverage * 0.2 +
            type_diversity * 0.2 +
            avg_freshness * 0.2
        )
        
        quality = QualityScore(
            relevance=avg_relevance,
            coverage=coverage,
            diversity=type_diversity,
            freshness=avg_freshness,
            overall=overall,
            issues=issues
        )
        
        # 过滤低质量结果
        filtered = [r for r in results if r.get("_relevance", 0) >= self.min_score_threshold]
        
        return filtered, quality
    
    def suggest_improvement(self, quality: QualityScore) -> List[str]:
        """
        根据质量评分给出改进建议
        """
        suggestions = []
        
        if quality.relevance < 0.5:
            suggestions.append("相关性较低，尝试更精确的查询词")
        if quality.coverage < 0.5:
            suggestions.append("结果数量不足，扩大搜索范围")
        if quality.diversity < 0.5:
            suggestions.append("结果类型单一，使用混合搜索策略")
        if quality.freshness < 0.5:
            suggestions.append("结果可能过时，检查记忆更新时间")
        
        if not suggestions and quality.overall < 0.7:
            suggestions.append("整体质量一般，尝试调整搜索参数")
        
        return suggestions


def evaluate_search(
    results: List[Dict],
    query: str,
    expected_types: List[str] = None
) -> Tuple[List[Dict], QualityScore, List[str]]:
    """
    评估搜索质量的快捷函数
    """
    scorer = SearchQualityScorer()
    filtered, quality = scorer.score_results(results, query, expected_types)
    suggestions = scorer.suggest_improvement(quality)
    
    return filtered, quality, suggestions
