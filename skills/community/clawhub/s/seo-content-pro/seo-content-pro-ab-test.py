#!/usr/bin/env python3
"""
A/B 测试支持模块
用于测试不同标题的效果
"""

import json
import random
from typing import List, Dict

class ABTest:
    def __init__(self, variants: List[str]):
        self.variants = variants
        self.results = {variant: {"impressions": 0, "clicks": 0} for variant in variants}
    
    def get_variant(self) -> str:
        """随机获取一个变体用于展示"""
        return random.choice(self.variants)
    
    def record_impression(self, variant: str):
        """记录展示次数"""
        if variant in self.results:
            self.results[variant]["impressions"] += 1
    
    def record_click(self, variant: str):
        """记录点击次数"""
        if variant in self.results:
            self.results[variant]["clicks"] += 1
    
    def get_ctr(self, variant: str) -> float:
        """计算点击率 (CTR)"""
        if variant not in self.results:
            return 0.0
        impressions = self.results[variant]["impressions"]
        clicks = self.results[variant]["clicks"]
        return clicks / impressions if impressions > 0 else 0.0
    
    def get_best_performer(self) -> str:
        """获取表现最好的变体"""
        best_variant = self.variants[0]
        best_ctr = 0.0
        
        for variant in self.variants:
            ctr = self.get_ctr(variant)
            if ctr > best_ctr:
                best_ctr = ctr
                best_variant = variant
        
        return best_variant
    
    def get_report(self) -> Dict:
        """生成 A/B 测试报告"""
        report = {
            "variants": {},
            "best_performer": self.get_best_performer(),
            "total_impressions": sum(v["impressions"] for v in self.results.values()),
            "total_clicks": sum(v["clicks"] for v in self.results.values())
        }
        
        for variant, data in self.results.items():
            report["variants"][variant] = {
                "impressions": data["impressions"],
                "clicks": data["clicks"],
                "ctr": self.get_ctr(variant)
            }
        
        return report

if __name__ == "__main__":
    # 示例使用
    titles = [
        "如何在30分钟内写出爆款文章（完整指南）",
        "3个SEO内容写作技巧，第3个太实用了",
        "为什么你的SEO内容总是失败？原因在这里"
    ]
    
    ab_test = ABTest(titles)
    
    # 模拟测试数据
    for _ in range(100):
        variant = ab_test.get_variant()
        ab_test.record_impression(variant)
        if random.random() < 0.15:  # 15% 点击率
            ab_test.record_click(variant)
    
    report = ab_test.get_report()
    print(json.dumps(report, indent=2, ensure_ascii=False))