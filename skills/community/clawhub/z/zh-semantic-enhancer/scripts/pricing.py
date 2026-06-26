#!/usr/bin/env python3
"""
分层定价系统 / Tiered Pricing System
"""

PRICING_TIERS = {
    "free": {
        "name": "免费版",
        "price": 0,
        "credits": 100,
        "features": ["基础分词", "简单实体识别", "常见成语识别"]
    },
    "basic": {
        "name": "基础版",
        "price": 0.001,
        "credits": 1000,
        "features": ["增强分词", "实体识别", "歧义消解", "成语俗语"]
    },
    "pro": {
        "name": "专业版",
        "price": 0.005,
        "credits": 5000,
        "features": ["专业版全部功能", "行业词典", "情感分析", "批量处理"]
    },
    "enterprise": {
        "name": "企业版",
        "price": 0.01,
        "credits": 20000,
        "features": ["全部功能", "自定义词典", "API接入", "优先支持", "SLA保障"]
    }
}

class PricingManager:
    """定价管理器"""
    
    def __init__(self, user_tier: str = "free"):
        self.tier = user_tier
        self.pricing = PRICING_TIERS.get(user_tier, PRICING_TIERS["free"])
    
    def get_credits(self) -> int:
        return self.pricing["credits"]
    
    def get_price_per_call(self) -> float:
        return self.pricing["price"]
    
    def get_features(self) -> List[str]:
        return self.pricing["features"]
    
    def upgrade_tier(self, new_tier: str) -> bool:
        if new_tier in PRICING_TIERS:
            self.tier = new_tier
            self.pricing = PRICING_TIERS[new_tier]
            return True
        return False
