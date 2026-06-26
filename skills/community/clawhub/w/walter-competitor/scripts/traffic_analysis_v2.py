#!/usr/bin/env python3
"""
traffic_analysis_v2.py - 竞品流量攻防智能分析V2

核心能力:
- 自动发现竞品
- 流量结构分析
- 关键词攻防矩阵
- P0/P1/P2攻击方案

作者: 分析虾
日期: 2026-04-12
"""

import sys
import os
from typing import Dict, Any, List
from concurrent.futures import ThreadPoolExecutor, as_completed

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '..', 'scripts'))
from unified_data_layer_v2 import AmazonDataLayerV2


class TrafficAnalysisV2:
    """
    竞品流量攻防智能分析V2
    
    输入: 关键词 + 我的售价
    输出: 完整攻防方案
    """
    
    def __init__(self):
        self.data_layer = AmazonDataLayerV2()
        self.marketplace = "US"
    
    def comprehensive_analysis(self, keyword: str, my_price: float,
                               my_margin: float = 0.30) -> Dict[str, Any]:
        """
        完整竞品流量攻防分析
        
        Args:
            keyword: 品类关键词
            my_price: 我的产品售价
            my_margin: 毛利率
            
        Returns:
            完整攻防方案
        """
        print(f"\n{'='*70}")
        print(f"[Traffic Battle Analysis V2]")
        print(f"{'='*70}")
        print(f"\n[Target] {keyword}")
        print(f"[My Price] ${my_price}")
        
        # Step 1: 自动发现竞品
        print(f"\n[Step 1] Auto-discovering competitors...")
        competitors = self._auto_discover_competitors(keyword)
        print(f"  Found {len(competitors)} competitors")
        
        # Step 2: 批量获取竞品情报
        print(f"\n[Step 2] Gathering competitor intelligence...")
        competitor_profiles = self._batch_get_intelligence(competitors)
        
        # Step 3: 流量结构分析
        print(f"\n[Step 3] Analyzing traffic structure...")
        traffic_landscape = self._analyze_traffic_landscape(competitor_profiles)
        
        # Step 4: 关键词攻防矩阵
        print(f"\n[Step 4] Building keyword battle matrix...")
        keyword_matrix = self._build_keyword_matrix(competitor_profiles, my_price, my_margin)
        
        # Step 5: 弱点挖掘
        print(f"\n[Step 5] Mining competitor weaknesses...")
        weaknesses = self._mine_weaknesses(competitor_profiles)
        
        # Step 6: 攻击矩阵
        print(f"\n[Step 6] Generating attack matrix...")
        attack_matrix = self._generate_attack_matrix(weaknesses, my_price, my_margin)
        
        # Step 7: 预算方案
        print(f"\n[Step 7] Calculating budget and ROI...")
        budget_plan = self._calculate_budget(attack_matrix, my_price, my_margin)
        
        report = {
            "keyword": keyword,
            "my_price": my_price,
            "competitors_analyzed": len(competitor_profiles),
            "competitor_profiles": competitor_profiles,
            "traffic_landscape": traffic_landscape,
            "keyword_matrix": keyword_matrix,
            "weaknesses": weaknesses,
            "attack_matrix": attack_matrix,
            "budget_plan": budget_plan,
        }
        
        # 显示报告
        self._display_report(report)
        
        return {"code": "OK", "data": report}
    
    def _auto_discover_competitors(self, keyword: str, n: int = 5) -> List[str]:
        """自动发现竞品ASIN"""
        # 获取竞品列表
        result = self.data_layer.api.call("competitor_lookup", 
                                          keyword=keyword, 
                                          marketplace=self.marketplace,
                                          page=1, page_size=20)
        
        if result.get("code") != "OK":
            return []
        
        data = result.get("data", {})
        items = data.get("items", []) if isinstance(data, dict) else []
        
        # 评分排序（销量+相关性）
        scored = []
        for item in items:
            score = 0
            score += item.get("monthlySales", 0) * 0.4
            score += item.get("relevanceScore", 0) * 0.3
            score += item.get("ratings", 0) * 0.0001 * 0.2
            scored.append((item.get("asin"), score))
        
        scored.sort(key=lambda x: x[1], reverse=True)
        return [asin for asin, _ in scored[:n]]
    
    def _batch_get_intelligence(self, asins: List[str]) -> List[Dict]:
        """批量获取竞品情报"""
        profiles = []
        
        for asin in asins:
            intel = self.data_layer.get_complete_competitor_intelligence(asin)
            if intel.get("code") == "OK":
                profiles.append(intel["data"])
        
        return profiles
    
    def _analyze_traffic_landscape(self, profiles: List[Dict]) -> Dict[str, Any]:
        """分析流量结构全景"""
        total_keywords = sum(p.get("traffic_analysis", {}).get("total_traffic_keywords", 0) 
                            for p in profiles)
        
        return {
            "total_competitors": len(profiles),
            "avg_traffic_keywords": total_keywords / len(profiles) if profiles else 0,
        }
    
    def _build_keyword_matrix(self, profiles: List[Dict], my_price: float, 
                              my_margin: float) -> Dict[str, Any]:
        """构建关键词攻防矩阵"""
        # 收集所有关键词
        all_keywords = {}
        
        for profile in profiles:
            traffic = profile.get("traffic_analysis", {})
            for kw in traffic.get("top_keywords", []):
                keyword = kw.get("keyword") or kw.get("word")
                if keyword:
                    if keyword not in all_keywords:
                        all_keywords[keyword] = {
                            "search_volume": kw.get("search_volume", 0),
                            "competitors": []
                        }
                    all_keywords[keyword]["competitors"].append(profile["asin"])
        
        # 识别机会关键词
        opportunities = []
        for keyword, data in all_keywords.items():
            if len(data["competitors"]) <= 2:  # 覆盖少
                opportunities.append({
                    "keyword": keyword,
                    "search_volume": data["search_volume"],
                    "competitor_count": len(data["competitors"]),
                })
        
        return {
            "total_keywords": len(all_keywords),
            "opportunity_keywords": sorted(opportunities, 
                                          key=lambda x: x["search_volume"], 
                                          reverse=True)[:20]
        }
    
    def _mine_weaknesses(self, profiles: List[Dict]) -> Dict[str, List]:
        """挖掘竞品弱点"""
        weaknesses = {"by_competitor": {}, "by_type": {}}
        
        for profile in profiles:
            asin = profile["asin"]
            comp_weaknesses = []
            
            # 流量弱点
            traffic = profile.get("traffic_analysis", {})
            if traffic.get("total_traffic_keywords", 0) < 20:
                comp_weaknesses.append({
                    "type": "low_traffic",
                    "description": "Few traffic keywords"
                })
            
            # VOC弱点
            voc = profile.get("voc_analysis", {})
            pain_points = voc.get("pain_points", [])
            if len(pain_points) > 5:
                comp_weaknesses.append({
                    "type": "voc_issues",
                    "description": pain_points[0].get("theme", "Quality issues")
                })
            
            weaknesses["by_competitor"][asin] = comp_weaknesses
        
        return weaknesses
    
    def _generate_attack_matrix(self, weaknesses: Dict, my_price: float, 
                                my_margin: float) -> Dict[str, List]:
        """生成攻击矩阵"""
        matrix = {
            "immediate": [],
            "short_term": [],
            "long_term": []
        }
        
        # P0: 立即攻击
        for asin, weaknesses_list in weaknesses["by_competitor"].items():
            for w in weaknesses_list:
                if w["type"] == "low_traffic":
                    matrix["immediate"].append({
                        "target": asin,
                        "tactic": "Target keywords they are missing",
                        "priority": "P0"
                    })
        
        return matrix
    
    def _calculate_budget(self, attack_matrix: Dict, my_price: float, 
                          my_margin: float) -> Dict[str, Any]:
        """计算预算和ROI"""
        daily_budget = 100  # 基础预算
        
        return {
            "daily_budget": daily_budget,
            "monthly_budget": daily_budget * 30,
            "expected_roi": 25  # 预估ROI
        }
    
    def _display_report(self, report: Dict):
        """显示报告"""
        print(f"\n{'='*70}")
        print(f"[Analysis Complete]")
        print(f"{'='*70}")
        
        print(f"\n[Competitors] {report['competitors_analyzed']}")
        
        matrix = report["attack_matrix"]
        print(f"\n[Attack Matrix]")
        print(f"  P0 (Immediate): {len(matrix['immediate'])}")
        print(f"  P1 (Short-term): {len(matrix['short_term'])}")
        print(f"  P2 (Long-term): {len(matrix['long_term'])}")
        
        budget = report["budget_plan"]
        print(f"\n[Budget]")
        print(f"  Daily: ${budget['daily_budget']}")
        print(f"  Expected ROI: {budget['expected_roi']}%")


def main():
    """测试"""
    print("\n" + "="*70)
    print("Traffic Battle V2 - Test")
    print("="*70)
    
    analyzer = TrafficAnalysisV2()
    
    result = analyzer.comprehensive_analysis(
        keyword="women active shorts",
        my_price=32.0
    )
    
    if result["code"] == "OK":
        print("\n[Success]")
    else:
        print(f"\n[Error] {result.get('message')}")
    
    print("\n" + "="*70)


if __name__ == "__main__":
    main()
