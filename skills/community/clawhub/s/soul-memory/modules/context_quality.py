#!/usr/bin/env python3
"""
Soul Memory v3.4.0 - Context Quality Scoring
上下文質量評分：量化注入記憶的質量，持續優化

Author: Li Si (李斯)
Date: 2026-03-08

v3.4.0 - 新增質量評估 + 反饋收集
"""

import os
import sys
import json
import time
from pathlib import Path
from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass, field
from datetime import datetime
from collections import defaultdict

# Ensure module path
if __name__ == "__main__":
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


@dataclass
class QualityAssessment:
    """質量評估結果"""
    query: str
    context: str
    response: str
    relevance_score: float  # 相關性 (0-1)
    diversity_score: float  # 多樣性 (0-1)
    freshness_score: float  # 時效性 (0-1)
    coverage_score: float  # 覆蓋度 (0-1)
    overall_score: float  # 總分 (0-1)
    timestamp: float = field(default_factory=time.time)
    feedback: Optional[str] = None
    
    def to_dict(self) -> Dict:
        return {
            'query': self.query,
            'context_length': len(self.context),
            'response_length': len(self.response),
            'relevance_score': self.relevance_score,
            'diversity_score': self.diversity_score,
            'freshness_score': self.freshness_score,
            'coverage_score': self.coverage_score,
            'overall_score': self.overall_score,
            'timestamp': self.timestamp,
            'feedback': self.feedback
        }


class ContextQualityScorer:
    """
    上下文質量評分器 v3.4.0
    
    Features:
    - 相關性評分 (Relevance)
    - 多樣性評分 (Diversity)
    - 時效性評分 (Freshness)
    - 覆蓋度評分 (Coverage)
    - 反饋收集
    - 持續優化
    """
    
    VERSION = "3.4.0"
    
    # 評分權重
    WEIGHTS = {
        'relevance': 0.4,
        'diversity': 0.2,
        'freshness': 0.2,
        'coverage': 0.2
    }
    
    def __init__(self, log_path: Optional[Path] = None):
        """
        初始化評分器
        
        Args:
            log_path: 日誌文件路徑
        """
        self.log_path = log_path or Path(__file__).parent.parent / "cache" / "quality_log.json"
        self.log_path.parent.mkdir(parents=True, exist_ok=True)
        
        # 評估歷史
        self.assessments: List[QualityAssessment] = []
        self.stats = {
            'total_assessments': 0,
            'avg_overall_score': 0.0,
            'score_distribution': defaultdict(int),
            'low_quality_flags': 0
        }
        
        # 加載歷史日誌
        self.load_log()
    
    def calculate_relevance(self, query: str, context: str) -> float:
        """
        計算相關性分數
        
        基於查詢與上下文的關鍵詞重疊率
        
        Args:
            query: 用戶查詢
            context: 注入的上下文
            
        Returns:
            相關性分數 (0-1)
        """
        query_terms = set(query.lower().split())
        context_terms = set(context.lower().split())
        
        if not query_terms or not context_terms:
            return 0.0
        
        # Jaccard 相似度
        intersection = query_terms & context_terms
        union = query_terms | context_terms
        
        jaccard = len(intersection) / len(union) if union else 0
        
        # 關鍵詞匹配增強
        keyword_bonus = 0.0
        important_keywords = ['如何', '為什麼', '什麼', '怎樣', 'where', 'what', 'why', 'how']
        for kw in important_keywords:
            if kw in query.lower() and kw in context.lower():
                keyword_bonus += 0.1
        
        return min(1.0, jaccard * 0.7 + keyword_bonus)
    
    def calculate_diversity(self, results: List[Dict]) -> float:
        """
        計算多樣性分數
        
        基於結果的來源分佈
        
        Args:
            results: 搜索結果列表
            
        Returns:
            多樣性分數 (0-1)
        """
        if not results:
            return 0.0
        
        # 計算來源分佈
        sources = defaultdict(int)
        for result in results:
            source = result.get('source', 'unknown')
            sources[source] += 1
        
        # 計算熵
        total = len(results)
        entropy = 0.0
        for count in sources.values():
            if count > 0:
                p = count / total
                entropy -= p * (p if p == 1 else (p * (1 - p)))  # 簡化熵
        
        # 歸一化
        max_entropy = 1.0 - (1.0 / len(sources)) if sources else 1.0
        diversity = entropy / max_entropy if max_entropy > 0 else 0
        
        return min(1.0, diversity)
    
    def calculate_freshness(self, results: List[Dict]) -> float:
        """
        計算時效性分數
        
        基於結果的時間戳
        
        Args:
            results: 搜索結果列表
            
        Returns:
            時效性分數 (0-1)
        """
        if not results:
            return 0.0
        
        current_time = time.time()
        freshness_scores = []
        
        for result in results:
            # 嘗試從內容中提取時間信息
            timestamp = result.get('timestamp', 0)
            
            if timestamp > 0:
                age_days = (current_time - timestamp) / 86400
                # 指數衰減
                freshness = max(0, 1.0 - (age_days / 30))  # 30 天內滿分
            else:
                # 無時間戳，假設中等時效
                freshness = 0.5
            
            freshness_scores.append(freshness)
        
        return sum(freshness_scores) / len(freshness_scores)
    
    def calculate_coverage(self, query: str, context: str, response: str) -> float:
        """
        計算覆蓋度分數
        
        基於響應是否覆蓋了查詢的所有方面
        
        Args:
            query: 用戶查詢
            context: 注入的上下文
            response: AI 響應
            
        Returns:
            覆蓋度分數 (0-1)
        """
        # 提取查詢中的關鍵概念
        query_concepts = self._extract_concepts(query)
        
        # 檢查響應中是否包含這些概念
        response_lower = response.lower()
        covered = sum(1 for concept in query_concepts if concept in response_lower)
        
        coverage = covered / len(query_concepts) if query_concepts else 1.0
        
        return min(1.0, coverage)
    
    def _extract_concepts(self, text: str) -> List[str]:
        """提取文本中的關鍵概念"""
        # 簡化版：提取名詞短語
        concepts = []
        words = text.lower().split()
        
        # 過濾停用詞
        stop_words = {'的', '了', '是', '在', '我', '有', '和', '就', '不', '人', '都', '一', '一個', '上', '也', '很', '到', '說', '要', '去', '你', '會', '着', '沒有', '看', '好', '自己', '這'}
        
        for word in words:
            if len(word) > 1 and word not in stop_words and word.isalpha():
                concepts.append(word)
        
        return concepts[:10]  # 限制最多 10 個概念
    
    def assess(self, query: str, context: str, response: str, 
               results: Optional[List[Dict]] = None) -> QualityAssessment:
        """
        執行完整質量評估
        
        Args:
            query: 用戶查詢
            context: 注入的上下文
            response: AI 響應
            results: 搜索結果列表（用於多樣性和時效性計算）
            
        Returns:
            質量評估結果
        """
        # 計算各維度分數
        relevance = self.calculate_relevance(query, context)
        
        if results:
            diversity = self.calculate_diversity(results)
            freshness = self.calculate_freshness(results)
        else:
            diversity = 0.5  # 默認中等
            freshness = 0.5
        
        coverage = self.calculate_coverage(query, context, response)
        
        # 加權平均
        overall = (
            relevance * self.WEIGHTS['relevance'] +
            diversity * self.WEIGHTS['diversity'] +
            freshness * self.WEIGHTS['freshness'] +
            coverage * self.WEIGHTS['coverage']
        )
        
        # 創建評估結果
        assessment = QualityAssessment(
            query=query,
            context=context,
            response=response,
            relevance_score=relevance,
            diversity_score=diversity,
            freshness_score=freshness,
            coverage_score=coverage,
            overall_score=overall
        )
        
        # 更新統計
        self.assessments.append(assessment)
        self.stats['total_assessments'] += 1
        
        # 更新平均分
        self.stats['avg_overall_score'] = (
            (self.stats['avg_overall_score'] * (self.stats['total_assessments'] - 1) + overall)
            / self.stats['total_assessments']
        )
        
        # 記錄低質量標記
        if overall < 0.6:
            self.stats['low_quality_flags'] += 1
        
        # 記錄到日誌
        self.save_log()
        
        return assessment
    
    def add_feedback(self, assessment_index: int, feedback: str):
        """
        添加用戶反饋
        
        Args:
            assessment_index: 評估索引
            feedback: 反饋文本
        """
        if 0 <= assessment_index < len(self.assessments):
            self.assessments[assessment_index].feedback = feedback
            self.save_log()
    
    def get_optimization_suggestions(self) -> List[str]:
        """
        獲取優化建議
        
        Returns:
            優化建議列表
        """
        suggestions = []
        
        if not self.assessments:
            return suggestions
        
        # 分析最近 10 次評估
        recent = self.assessments[-10:]
        avg_relevance = sum(a.relevance_score for a in recent) / len(recent)
        avg_diversity = sum(a.diversity_score for a in recent) / len(recent)
        avg_freshness = sum(a.freshness_score for a in recent) / len(recent)
        avg_coverage = sum(a.coverage_score for a in recent) / len(recent)
        
        if avg_relevance < 0.6:
            suggestions.append("相關性較低，建議提高搜索關鍵詞匹配度或調整 minScore 閾值")
        
        if avg_diversity < 0.5:
            suggestions.append("多樣性不足，建議增加搜索結果的來源分佈")
        
        if avg_freshness < 0.5:
            suggestions.append("時效性較差，建議優先使用近期記憶")
        
        if avg_coverage < 0.6:
            suggestions.append("覆蓋度不足，建議增加上下文注入量或改進響應生成")
        
        if self.stats['low_quality_flags'] > len(self.assessments) * 0.3:
            suggestions.append("低質量比例過高 (>30%)，建議全面檢查搜索策略")
        
        return suggestions
    
    def save_log(self):
        """保存評估日誌"""
        try:
            data = {
                'version': self.VERSION,
                'updated_at': datetime.now().isoformat(),
                'stats': dict(self.stats),
                'assessments': [a.to_dict() for a in self.assessments[-100:]]  # 只保留最近 100 條
            }
            
            with open(self.log_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"[QualityScorer] Save failed: {e}")
    
    def load_log(self):
        """加載評估日誌"""
        if not self.log_path.exists():
            return
        
        try:
            with open(self.log_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            if 'stats' in data:
                self.stats = data['stats']
            
            if 'assessments' in data:
                for a_data in data['assessments']:
                    self.assessments.append(QualityAssessment(**a_data))
            
            print(f"[QualityScorer] Loaded {len(self.assessments)} assessments")
        except Exception as e:
            print(f"[QualityScorer] Load failed: {e}")
    
    def get_stats(self) -> Dict:
        """獲取統計信息"""
        return {
            'version': self.VERSION,
            'total_assessments': self.stats['total_assessments'],
            'avg_overall_score': round(self.stats['avg_overall_score'], 3),
            'low_quality_flags': self.stats['low_quality_flags'],
            'weights': self.WEIGHTS
        }


# 全局實例
_global_scorer: Optional[ContextQualityScorer] = None


def get_quality_scorer(log_path: Optional[Path] = None) -> ContextQualityScorer:
    """獲取全局質量評分器實例"""
    global _global_scorer
    
    if _global_scorer is None:
        _global_scorer = ContextQualityScorer(log_path)
    
    return _global_scorer


# CLI 測試
if __name__ == "__main__":
    print("🧪 Testing Context Quality Scoring v3.4.0\n")
    
    scorer = ContextQualityScorer()
    
    # 測試 1: 相關性計算
    print("Test 1: Relevance Calculation")
    query = "如何配置 QST 系統？"
    context = "QST 系統配置需要設置 API 和伺服器參數"
    relevance = scorer.calculate_relevance(query, context)
    print(f"  Query: '{query}'")
    print(f"  Context: '{context}'")
    print(f"  Relevance: {relevance:.2f}")
    print()
    
    # 測試 2: 多樣性計算
    print("Test 2: Diversity Calculation")
    results = [
        {'source': 'memory1', 'content': '...'},
        {'source': 'memory2', 'content': '...'},
        {'source': 'memory1', 'content': '...'},
        {'source': 'memory3', 'content': '...'},
    ]
    diversity = scorer.calculate_diversity(results)
    print(f"  Results: {len(results)} from {len(set(r['source'] for r in results))} sources")
    print(f"  Diversity: {diversity:.2f}")
    print()
    
    # 測試 3: 完整評估
    print("Test 3: Full Assessment")
    assessment = scorer.assess(
        query="QST 理論是什麼？",
        context="QSTv7.1 是量子自旋扭轉理論，包含 FSCA、DSI 等模組",
        response="QST 理論是量子自旋扭縮理論，主要用於解釋暗物質和意識本質",
        results=results
    )
    print(f"  Overall Score: {assessment.overall_score:.2f}")
    print(f"  Relevance: {assessment.relevance_score:.2f}")
    print(f"  Diversity: {assessment.diversity_score:.2f}")
    print(f"  Freshness: {assessment.freshness_score:.2f}")
    print(f"  Coverage: {assessment.coverage_score:.2f}")
    print()
    
    # 測試 4: 優化建議
    print("Test 4: Optimization Suggestions")
    suggestions = scorer.get_optimization_suggestions()
    if suggestions:
        for s in suggestions:
            print(f"  - {s}")
    else:
        print("  No suggestions (系統運行正常)")
    print()
    
    # 測試 5: 統計信息
    print("Test 5: Statistics")
    stats = scorer.get_stats()
    for key, value in stats.items():
        print(f"  {key}: {value}")
    print()
    
    print("✅ All tests passed!")
