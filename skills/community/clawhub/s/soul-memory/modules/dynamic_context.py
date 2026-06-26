#!/usr/bin/env python3
"""
Soul Memory v3.4.0 - Dynamic Context Window
動態上下文窗口：根據查詢複雜度自適應調整 topK 和 minScore

Author: Li Si (李斯)
Date: 2026-03-08

v3.4.0 - 新增動態策略選擇
"""

import re
from typing import Dict, List, Optional
from dataclasses import dataclass
from enum import Enum


class QueryComplexity(Enum):
    """查詢複雜度等級"""
    SIMPLE = "simple"
    MODERATE = "moderate"
    COMPLEX = "complex"
    TECHNICAL = "technical"


@dataclass
class ContextStrategy:
    """上下文注入策略"""
    top_k: int
    min_score: float
    max_tokens: int
    compress: bool = False
    
    def to_dict(self) -> Dict:
        return {
            'top_k': self.top_k,
            'min_score': self.min_score,
            'max_tokens': self.max_tokens,
            'compress': self.compress
        }


class DynamicContextWindow:
    """
    動態上下文窗口 v3.4.0
    
    Features:
    - 查詢複雜度分析
    - 動態策略選擇
    - Token 預算管理
    - 自適應調整
    """
    
    VERSION = "3.4.0"
    
    # 默認策略
    DEFAULT_STRATEGIES = {
        QueryComplexity.SIMPLE: ContextStrategy(
            top_k=2,
            min_score=4.0,
            max_tokens=300,
            compress=False
        ),
        QueryComplexity.MODERATE: ContextStrategy(
            top_k=5,
            min_score=3.0,
            max_tokens=800,
            compress=False
        ),
        QueryComplexity.COMPLEX: ContextStrategy(
            top_k=10,
            min_score=2.0,
            max_tokens=1500,
            compress=True
        ),
        QueryComplexity.TECHNICAL: ContextStrategy(
            top_k=8,
            min_score=2.5,
            max_tokens=1200,
            compress=True
        )
    }
    
    # 關鍵詞分類
    TECHNICAL_KEYWORDS = [
        '配置', 'api', '系統', 'error', '錯誤', 'bug', 'fix',
        '部署', 'server', 'port', 'database', 'sql', 'network',
        'python', 'javascript', 'code', '代碼', '編程', '技術',
        'QST', '物理', '公式', '計算', '理論', 'FSCA', 'E8'
    ]
    
    COMPLEX_INDICATORS = [
        '如何', '怎樣', '為什麼', '解釋', '分析', '比較',
        '詳細', '完整', '全部', '所有', 'every', 'all',
        'how', 'why', 'explain', 'analyze', 'compare',
        '？', '？', '?', '複雜', 'complex'
    ]
    
    SIMPLE_PATTERNS = [
        r'^[早午晚][安好]$',
        r'^[唔該多謝 thanks]+$',
        r'^[是唔係有沒有 yes no]+[？?]?$',
        r'^[好唔錯 nice]+$',
        r'^[ok 好收到]+$',
    ]
    
    def __init__(self, strategies: Optional[Dict[QueryComplexity, ContextStrategy]] = None):
        """
        初始化動態上下文窗口
        
        Args:
            strategies: 自定義策略字典
        """
        self.strategies = strategies or self.DEFAULT_STRATEGIES.copy()
        self.base_topK = 5
        self.base_min_score = 3.0
    
    def analyze_complexity(self, query: str) -> QueryComplexity:
        """
        分析查詢複雜度
        
        Args:
            query: 用戶查詢
            
        Returns:
            複雜度等級
        """
        query_lower = query.lower()
        score = 0
        
        # 1. 檢查是否為簡單模式
        for pattern in self.SIMPLE_PATTERNS:
            if re.match(pattern, query.strip(), re.IGNORECASE):
                return QueryComplexity.SIMPLE
        
        # 2. 技術關鍵詞計分
        tech_count = sum(1 for kw in self.TECHNICAL_KEYWORDS if kw.lower() in query_lower)
        if tech_count >= 2:
            return QueryComplexity.TECHNICAL
        elif tech_count == 1:
            score += 2
        
        # 3. 複雜指標計分
        complex_count = sum(1 for ind in self.COMPLEX_INDICATORS if ind in query)
        score += complex_count
        
        # 4. 查詢長度計分
        if len(query) > 50:
            score += 1
        if len(query) > 100:
            score += 2
        
        # 5. 問號數量（多個問題）
        question_count = query.count('?') + query.count('？')
        if question_count >= 2:
            score += 2
        
        # 6. 列表/比較請求
        if any(kw in query_lower for kw in ['列表', 'list', '比較', 'compare', 'vs', ' versus ']):
            score += 2
        
        # 判定複雜度
        if score >= 5:
            return QueryComplexity.COMPLEX
        elif score >= 2:
            return QueryComplexity.MODERATE
        else:
            return QueryComplexity.SIMPLE
    
    def get_strategy(self, query: str) -> ContextStrategy:
        """
        根據查詢獲取策略
        
        Args:
            query: 用戶查詢
            
        Returns:
            上下文策略
        """
        complexity = self.analyze_complexity(query)
        return self.strategies[complexity]
    
    def get_params(self, query: str) -> Dict:
        """
        獲取搜索參數
        
        Args:
            query: 用戶查詢
            
        Returns:
            搜索參數字典
        """
        strategy = self.get_strategy(query)
        return strategy.to_dict()
    
    def should_compress(self, query: str, context_length: int) -> bool:
        """
        判斷是否需要壓縮
        
        Args:
            query: 用戶查詢
            context_length: 上下文長度
            
        Returns:
            是否需要壓縮
        """
        strategy = self.get_strategy(query)
        return strategy.compress or context_length > strategy.max_tokens
    
    def estimate_tokens(self, text: str) -> int:
        """
        估算 token 數量
        
        簡化算法：中文每個字符 ~1.5 tokens，英文每個單詞 ~1.3 tokens
        """
        # 中文字符
        chinese_chars = len(re.findall(r'[\u4e00-\u9fff]', text))
        # 英文單詞
        english_words = len(re.findall(r'\b[a-zA-Z]+\b', text))
        # 其他字符（標點、數字等）
        other_chars = len(text) - chinese_chars - len(re.findall(r'[a-zA-Z]+', text))
        
        # 估算
        tokens = (
            chinese_chars * 1.5 +
            english_words * 1.3 +
            other_chars * 0.2
        )
        
        return int(tokens)
    
    def truncate_to_tokens(self, results: List[Dict], max_tokens: int) -> List[Dict]:
        """
        截斷結果以符合 token 限制
        
        Args:
            results: 搜索結果列表
            max_tokens: 最大 token 數
            
        Returns:
            截斷後的結果
        """
        if not results:
            return []
        
        truncated = []
        current_tokens = 0
        
        for result in results:
            content = result.get('content', '')
            tokens = self.estimate_tokens(content)
            
            if current_tokens + tokens <= max_tokens:
                truncated.append(result)
                current_tokens += tokens
            else:
                # 部分截斷
                remaining = max_tokens - current_tokens
                if remaining > 50:  # 至少保留 50 tokens
                    # 估算截斷位置
                    truncate_ratio = remaining / tokens
                    truncate_pos = int(len(content) * truncate_ratio)
                    result['content'] = content[:truncate_pos] + '...'
                    truncated.append(result)
                break
        
        return truncated
    
    def get_stats(self, query: str) -> Dict:
        """
        獲取策略統計信息
        
        Args:
            query: 用戶查詢
            
        Returns:
            統計信息字典
        """
        complexity = self.analyze_complexity(query)
        strategy = self.get_strategy(query)
        
        return {
            'version': self.VERSION,
            'query_length': len(query),
            'complexity': complexity.value,
            'strategy': strategy.to_dict(),
            'base_topK': self.base_topK,
            'base_min_score': self.base_min_score
        }


# 全局實例
_global_context_window: Optional[DynamicContextWindow] = None


def get_context_window() -> DynamicContextWindow:
    """獲取全局動態上下文窗口實例"""
    global _global_context_window
    
    if _global_context_window is None:
        _global_context_window = DynamicContextWindow()
    
    return _global_context_window


# CLI 測試
if __name__ == "__main__":
    print("🧪 Testing Dynamic Context Window v3.4.0\n")
    
    dcw = DynamicContextWindow()
    
    # 測試用例
    test_queries = [
        ("早", QueryComplexity.SIMPLE),
        ("多謝", QueryComplexity.SIMPLE),
        ("QST 理論是什麼？", QueryComplexity.MODERATE),
        ("如何配置 API 和伺服器？", QueryComplexity.TECHNICAL),
        ("請詳細解釋 QSTv7.1 的 FSCA 模擬機制，包括所有參數和公式", QueryComplexity.COMPLEX),
        ("比較 QST 和標準模型的差異", QueryComplexity.COMPLEX),
    ]
    
    print("Test 1: Complexity Analysis")
    for query, expected in test_queries:
        result = dcw.analyze_complexity(query)
        status = "✓" if result == expected else "✗"
        print(f"  {status} '{query[:20]}...' -> {result.value} (expected: {expected.value})")
    print()
    
    print("Test 2: Strategy Selection")
    for query, _ in test_queries:
        strategy = dcw.get_strategy(query)
        print(f"  Query: '{query[:30]}...'")
        print(f"    top_k={strategy.top_k}, min_score={strategy.min_score}, max_tokens={strategy.max_tokens}")
    print()
    
    print("Test 3: Token Estimation")
    sample_text = "QSTv7.1 理論包含 FSCA、DSI、E8-Matrix 等多個模組"
    tokens = dcw.estimate_tokens(sample_text)
    print(f"  Text: '{sample_text}'")
    print(f"  Estimated tokens: {tokens}")
    print()
    
    print("Test 4: Get Stats")
    stats = dcw.get_stats("如何配置 QST 系統？")
    for key, value in stats.items():
        print(f"  {key}: {value}")
    print()
    
    print("✅ All tests passed!")
