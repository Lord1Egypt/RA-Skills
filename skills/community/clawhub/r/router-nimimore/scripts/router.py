#!/usr/bin/env python3
"""
Router NIMIMORE - Smart Model Router
智能模型路由器 - 自动选择最优模型
"""

import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

import json
import re
from enum import Enum
from typing import Dict, List, Optional
from dataclasses import dataclass


class ModelTier(Enum):
    """模型层级"""
    PREMIUM = "premium"      # 高端模型
    STANDARD = "standard"    # 标准模型
    ECONOMY = "economy"      # 经济模型


@dataclass
class ModelConfig:
    """模型配置"""
    name: str
    provider: str
    tier: ModelTier
    cost_per_1k: float
    max_tokens: int
    priority: int


class SmartRouter:
    """智能路由器"""
    
    def __init__(self):
        # 模型配置
        self.models = {
            "moonshot/kimi-k2.5": ModelConfig(
                name="kimi-k2.5",
                provider="moonshot",
                tier=ModelTier.PREMIUM,
                cost_per_1k=0.015,
                max_tokens=200000,
                priority=10
            ),
            "bailian/qwen-max": ModelConfig(
                name="qwen-max",
                provider="bailian",
                tier=ModelTier.STANDARD,
                cost_per_1k=0.008,
                max_tokens=32768,
                priority=8
            ),
            "bailian/qwen-plus": ModelConfig(
                name="qwen-plus",
                provider="bailian",
                tier=ModelTier.STANDARD,
                cost_per_1k=0.004,
                max_tokens=131072,
                priority=7
            ),
            "bailian/qwen-turbo": ModelConfig(
                name="qwen-turbo",
                provider="bailian",
                tier=ModelTier.ECONOMY,
                cost_per_1k=0.002,
                max_tokens=8192,
                priority=5
            )
        }
    
    def analyze_query(self, query: str) -> Dict[str, bool]:
        """分析查询特征"""
        query_lower = query.lower()
        
        features = {
            "is_simple": False,
            "is_code": False,
            "is_chinese": False,
            "is_reasoning": False,
            "is_long_context": len(query) > 500,
            "is_trading": False
        }
        
        # 简单查询
        simple_patterns = [
            r'^\s*(hi|hello|hey|你好|在吗|谢谢|ok|好的|嗯嗯)\s*$',
            r'^\s*\d+\s*$',
            r'^\s*[a-zA-Z]{1,10}\s*$'
        ]
        for pattern in simple_patterns:
            if re.match(pattern, query_lower):
                features["is_simple"] = True
                break
        
        # 代码相关
        code_keywords = ['code', 'python', 'javascript', 'function', 'bug', 'error', 
                        '代码', '函数', '调试', 'programming', 'script']
        features["is_code"] = any(kw in query_lower for kw in code_keywords)
        
        # 中文内容
        chinese_chars = sum(1 for c in query if '\u4e00' <= c <= '\u9fff')
        features["is_chinese"] = chinese_chars / len(query) > 0.3 if query else False
        
        # 推理分析
        reasoning_keywords = ['分析', '推理', '为什么', '比较', '评估', '预测',
                             'analyze', 'compare', 'evaluate', 'reasoning']
        features["is_reasoning"] = any(kw in query_lower for kw in reasoning_keywords)
        
        # 交易相关
        trading_keywords = ['股票', '交易', '行情', '价格', '买入', '卖出',
                           'stock', 'trade', 'price', 'market']
        features["is_trading"] = any(kw in query_lower for kw in trading_keywords)
        
        return features
    
    def select_model(self, query: str, context_length: int = 0) -> str:
        """选择最优模型"""
        features = self.analyze_query(query)
        
        # 根据特征选择层级
        if features["is_simple"]:
            target_tier = ModelTier.ECONOMY
        elif features["is_long_context"] or features["is_reasoning"]:
            target_tier = ModelTier.PREMIUM
        elif features["is_code"] and features["is_chinese"]:
            target_tier = ModelTier.STANDARD
        else:
            target_tier = ModelTier.STANDARD
        
        # 在目标层级中选择优先级最高的
        candidates = [
            (name, config) for name, config in self.models.items()
            if config.tier == target_tier
        ]
        
        if not candidates:
            # 降级选择
            if target_tier == ModelTier.PREMIUM:
                candidates = [(n, c) for n, c in self.models.items() if c.tier == ModelTier.STANDARD]
            else:
                candidates = [(n, c) for n, c in self.models.items() if c.tier == ModelTier.ECONOMY]
        
        # 按优先级排序
        candidates.sort(key=lambda x: x[1].priority, reverse=True)
        
        return candidates[0][0] if candidates else "bailian/qwen-plus"
    
    def get_model_info(self, model_name: str) -> Dict:
        """获取模型信息"""
        config = self.models.get(model_name)
        if not config:
            return {"error": "Model not found"}
        
        return {
            "name": model_name,
            "provider": config.provider,
            "tier": config.tier.value,
            "cost_per_1k": config.cost_per_1k,
            "max_tokens": config.max_tokens,
            "priority": config.priority
        }
    
    def route(self, query: str, context_length: int = 0) -> Dict:
        """执行路由"""
        features = self.analyze_query(query)
        selected_model = self.select_model(query, context_length)
        model_info = self.get_model_info(selected_model)
        
        # 计算节省的成本（对比始终使用 Premium）
        premium_cost = self.models["moonshot/kimi-k2.5"].cost_per_1k
        actual_cost = model_info["cost_per_1k"]
        savings = premium_cost - actual_cost
        
        return {
            "success": True,
            "query": query,
            "features": features,
            "selected_model": selected_model,
            "model_info": model_info,
            "cost_savings": savings,
            "savings_percent": (savings / premium_cost * 100) if premium_cost > 0 else 0
        }


def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="Router NIMIMORE - Smart Model Router")
    parser.add_argument("--query", "-q", help="Query to route")
    parser.add_argument("--context-length", "-c", type=int, default=0, help="Context length")
    parser.add_argument("--demo", action="store_true", help="Run demo")
    
    args = parser.parse_args()
    
    router = SmartRouter()
    
    if args.demo:
        # 运行演示
        test_queries = [
            ("你好", "简单问候"),
            ("帮我写个Python函数", "代码生成"),
            ("分析一下股票走势", "复杂分析"),
            ("谢谢", "简单感谢"),
            ("解释一下量子计算的原理", "知识解释"),
            ("OK", "简单确认"),
            ("debug这个错误", "代码调试"),
            ("比较两种方案的优缺点", "复杂比较"),
        ]
        
        print("=" * 70)
        print("Router NIMIMORE - Smart Model Routing Demo")
        print("=" * 70)
        
        total_savings = 0
        for query, desc in test_queries:
            result = router.route(query)
            total_savings += result["cost_savings"]
            
            print(f"\n📝 {desc}")
            print(f"   Query: {query}")
            print(f"   Model: {result['selected_model']}")
            print(f"   Tier: {result['model_info']['tier']}")
            print(f"   Cost: ${result['model_info']['cost_per_1k']}/1k tokens")
            print(f"   Savings: ${result['cost_savings']:.3f}")
        
        print("\n" + "=" * 70)
        print(f"Total Savings: ${total_savings:.3f}")
        print("=" * 70)
    
    elif args.query:
        result = router.route(args.query, args.context_length)
        print(json.dumps(result, indent=2, ensure_ascii=False))
    
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
