#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
walter-competitor-monitor.py - 亚马逊竞品监控

核心问题: "我的竞品在做什么？"

作者: 分析虾 🦐
日期: 2026-04-13
"""

import sys
import os
import re
from typing import Dict, Any, List, Optional
from datetime import datetime

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..', 'scripts')))
from unified_data_layer_v2 import AmazonDataLayerV2


class CompetitorMonitor:
    """亚马逊竞品监控"""
    
    def __init__(self):
        self.data_layer = AmazonDataLayerV2()
        self.marketplace = "US"
    
    # =========================================================================
    # 主入口
    # =========================================================================
    
    def analyze(self, user_input: str) -> Dict[str, Any]:
        """
        竞品监控完整流程
        
        Args:
            user_input: 用户输入，如 "监控 CRZ YOGA" 或 "分析 ASIN B071WV2SRC"
            
        Returns:
            竞品监控报告
        """
        print(f"\n{'='*70}")
        print(f"[Competitor Monitor]")
        print(f"{'='*70}")
        
        # 1. 解析竞品标识
        print(f"\n[Step 1/5] Parsing Competitors...")
        targets = self._parse_targets(user_input)
        print(f"[Found] {len(targets)} target(s)")
        
        for t in targets:
            print(f"  - {t['type'].upper()}: {t['id']}")
        
        # 2. 获取基础情报
        print(f"\n[Step 2/5] Fetching Intelligence...")
        intelligence = []
        for target in targets:
            intel = self._get_intel(target)
            if intel:
                intelligence.append(intel)
                self._display_intel_summary(intel)
        
        if not intelligence:
            return {
                'scene': 'competitor_monitor',
                'error': 'No competitor data found',
                'targets': targets
            }
        
        # 3. 流量词分析
        print(f"\n[Step 3/5] Traffic Keyword Analysis...")
        keywords = self._analyze_keywords(intelligence)
        self._display_keywords(keywords)
        
        # 4. VOC分析
        print(f"\n[Step 4/5] VOC Analysis...")
        voc = self._analyze_voc(intelligence)
        self._display_voc(voc)
        
        # 5. 行动建议
        print(f"\n[Step 5/5] Action Recommendations...")
        actions = self._generate_actions(keywords, voc)
        self._display_actions(actions)
        
        # 汇总
        return {
            'scene': 'competitor_monitor',
            'timestamp': datetime.now().isoformat(),
            'targets': targets,
            'intelligence': intelligence,
            'keywords': keywords,
            'voc': voc,
            'actions': actions
        }
    
    # =========================================================================
    # 核心方法
    # =========================================================================
    
    def _parse_targets(self, text: str) -> List[Dict[str, str]]:
        """解析竞品标识"""
        targets = []
        
        # 提取ASIN (10位字母数字)
        asins = re.findall(r'\b([A-Z0-9]{10})\b', text.upper())
        for asin in set(asins):  # 去重
            targets.append({'type': 'asin', 'id': asin})
        
        # 提取品牌名（移除监控/分析等词）
        brand = text
        for kw in ['监控', '关注', '分析', '竞品', '竞争对手', '看看', '查一下', 
                   'ASIN', '这几个', '还有', '和', ',', '，']:
            brand = brand.replace(kw, '')
        brand = brand.strip()
        
        # 如果有品牌名且没有找到ASIN，用品牌名作为查询
        if brand and not asins:
            targets.append({'type': 'brand', 'id': brand})
        # 如果有品牌名且找到了ASIN，也添加品牌名用于显示
        elif brand and asins:
            targets.append({'type': 'brand', 'id': brand})
        
        # 默认：如果什么都没找到，用原始文本
        if not targets:
            targets.append({'type': 'unknown', 'id': text.strip()})
        
        return targets
    
    def _get_intel(self, target: Dict) -> Optional[Dict[str, Any]]:
        """获取竞品情报"""
        asin = None
        
        if target['type'] == 'asin':
            asin = target['id']
        elif target['type'] == 'brand':
            # 用brand name查询ASIN
            asin = self._find_asin_by_brand(target['id'])
        
        if not asin:
            return None
        
        # 获取完整情报
        result = self.data_layer.get_complete_competitor_intelligence(asin)
        
        if result.get('code') != 'OK':
            # 返回基本信息
            return {
                'asin': asin,
                'name': target['id'],
                'type': target['type'],
                'error': result.get('message', 'API failed')
            }
        
        data = result.get('data', {})
        
        # 提取关键信息
        detail = data.get('detail', {})
        reviews = data.get('reviews', {})
        traffic = data.get('traffic_keywords', [])
        
        # 计算月销量 (简化估算: BSR → 销量)
        bsr = detail.get('bsr', 0)
        est_sales = self._estimate_sales(bsr)
        
        # 计算月收入
        price = detail.get('price', 0)
        monthly_revenue = est_sales * price if price else 0
        
        return {
            'asin': asin,
            'name': detail.get('title', target['id'])[:60],
            'type': target['type'],
            'price': price,
            'rating': detail.get('rating', 0),
            'reviews': detail.get('reviews', 0),
            'bsr': bsr,
            'est_sales': est_sales,
            'monthly_revenue': monthly_revenue,
            'traffic_keywords': traffic[:10] if traffic else [],
            'review_data': reviews
        }
    
    def _find_asin_by_brand(self, brand: str) -> Optional[str]:
        """通过品牌名查找ASIN"""
        result = self.data_layer.api.call(
            'competitor_lookup',
            keyword=brand,
            marketplace=self.marketplace,
            page=1,
            page_size=3
        )
        
        if result.get('code') == 'OK':
            products = result.get('data', [])
            if products:
                return products[0].get('asin')
        
        return None
    
    def _estimate_sales(self, bsr: int) -> int:
        """根据BSR估算月销量 (简化模型)"""
        if bsr <= 0:
            return 0
        elif bsr <= 100:
            return 5000
        elif bsr <= 500:
            return 2000
        elif bsr <= 1000:
            return 1000
        elif bsr <= 5000:
            return 500
        elif bsr <= 10000:
            return 200
        elif bsr <= 50000:
            return 50
        else:
            return 10
    
    def _analyze_keywords(self, intelligence: List[Dict]) -> Dict[str, Any]:
        """流量词分析"""
        all_keywords = []
        
        for intel in intelligence:
            keywords = intel.get('traffic_keywords', [])
            for kw in keywords:
                all_keywords.append({
                    'keyword': kw.get('keyword', ''),
                    'traffic_share': kw.get('traffic_share', 0),
                    'rank': kw.get('rank', 0),
                    'type': kw.get('type', 'organic')
                })
        
        # 按流量排序
        all_keywords.sort(key=lambda x: x.get('traffic_share', 0), reverse=True)
        
        # 去重（保留排名最高的）
        seen = {}
        unique_keywords = []
        for kw in all_keywords:
            k = kw['keyword'].lower()
            if k not in seen:
                seen[k] = True
                unique_keywords.append(kw)
        
        # 分类统计
        organic = [kw for kw in unique_keywords if kw.get('type') == 'organic']
        sponsored = [kw for kw in unique_keywords if kw.get('type') == 'sponsored']
        
        return {
            'total': len(unique_keywords),
            'organic': len(organic),
            'sponsored': len(sponsored),
            'top_keywords': unique_keywords[:15]
        }
    
    def _analyze_voc(self, intelligence: List[Dict]) -> Dict[str, Any]:
        """VOC分析"""
        pain_points = {}
        praise_points = {}
        total_reviews = 0
        
        for intel in intelligence:
            reviews = intel.get('review_data', {})
            if isinstance(reviews, dict):
                positive = reviews.get('positive', [])
                negative = reviews.get('negative', [])
                
                total_reviews += len(positive) + len(negative)
                
                for review in positive:
                    for tag in review.get('tags', []):
                        praise_points[tag] = praise_points.get(tag, 0) + 1
                
                for review in negative:
                    for tag in review.get('tags', []):
                        pain_points[tag] = pain_points.get(tag, 0) + 1
        
        # 排序
        top_pains = sorted(pain_points.items(), key=lambda x: x[1], reverse=True)[:5]
        top_praises = sorted(praise_points.items(), key=lambda x: x[1], reverse=True)[:5]
        
        return {
            'total_reviews': total_reviews,
            'pain_points': [{'tag': t, 'count': c} for t, c in top_pains],
            'praise_points': [{'tag': t, 'count': c} for t, c in top_praises]
        }
    
    def _generate_actions(self, keywords: Dict, voc: Dict) -> List[Dict[str, str]]:
        """生成行动建议"""
        actions = []
        
        # 基于VOC痛点
        if voc.get('pain_points'):
            top_pain = voc['pain_points'][0]
            actions.append({
                'type': 'differentiation',
                'title': f'攻击痛点: {top_pain["tag"]}',
                'desc': f'{top_pain["count"]}条差评提到此问题',
                'priority': 'HIGH'
            })
        
        # 基于流量词
        if keywords.get('top_keywords'):
            top_kw = keywords['top_keywords'][0]
            actions.append({
                'type': 'keyword',
                'title': f'核心关键词: "{top_kw["keyword"]}"',
                'desc': f'占比 {top_kw["traffic_share"]*100:.1f}% 流量',
                'priority': 'HIGH'
            })
        
        # 差异化建议
        if len(keywords.get('top_keywords', [])) >= 3:
            actions.append({
                'type': 'strategy',
                'title': '长尾关键词策略',
                'desc': '避免与头部直接竞争，占领细分市场',
                'priority': 'MEDIUM'
            })
        
        return actions
    
    # =========================================================================
    # 显示方法
    # =========================================================================
    
    def _display_intel_summary(self, intel: Dict):
        """显示情报摘要"""
        if intel.get('error'):
            print(f"  ⚠️ {intel['name']}: {intel['error']}")
            return
        
        print(f"\n  📊 {intel.get('name', 'Unknown')}")
        print(f"     ASIN: {intel.get('asin', 'N/A')}")
        print(f"     Price: ${intel.get('price', 0):.2f} | Rating: {intel.get('rating', 0):.1f}")
        print(f"     Reviews: {intel.get('reviews', 0):,} | BSR: #{intel.get('bsr', 0):,}")
        print(f"     Est. Sales: {intel.get('est_sales', 0):,}/mo | Revenue: ${intel.get('monthly_revenue', 0):,.0f}/mo")
    
    def _display_keywords(self, keywords: Dict):
        """显示流量词"""
        print(f"\n[Traffic Keywords] {keywords.get('total', 0)} found")
        print(f"  Organic: {keywords.get('organic', 0)} | Sponsored: {keywords.get('sponsored', 0)}")
        
        for i, kw in enumerate(keywords.get('top_keywords', [])[:8], 1):
            share = kw.get('traffic_share', 0) * 100
            print(f"  {i}. {kw.get('keyword', 'Unknown')} ({share:.1f}%)")
    
    def _display_voc(self, voc: Dict):
        """显示VOC分析"""
        print(f"\n[Consumer Insights] Based on {voc.get('total_reviews', 0)} reviews")
        
        print(f"\n  🔴 Pain Points:")
        for item in voc.get('pain_points', [])[:3]:
            print(f"      - {item['tag']} ({item['count']})")
        
        print(f"\n  🟢 Praise Points:")
        for item in voc.get('praise_points', [])[:3]:
            print(f"      - {item['tag']} ({item['count']})")
    
    def _display_actions(self, actions: List[Dict]):
        """显示行动建议"""
        print(f"\n[Action Recommendations]")
        for action in actions:
            priority = action.get('priority', 'MEDIUM')
            symbol = '🔴' if priority == 'HIGH' else '🟡'
            print(f"  {symbol} [{priority}] {action.get('title', '')}")
            print(f"      {action.get('desc', '')}")


# =========================================================================
# 主入口
# =========================================================================

if __name__ == '__main__':
    import json
    
    monitor = CompetitorMonitor()
    
    # 测试场景1: 品牌监控
    print("\n" + "="*70)
    print("TEST 1: Brand Monitor")
    print("="*70)
    
    result1 = monitor.analyze("监控 CRZ YOGA")
    print(f"\n[Result] Targets: {len(result1.get('targets', []))}")
    
    # 测试场景2: ASIN监控
    print("\n" + "="*70)
    print("TEST 2: ASIN Monitor")
    print("="*70)
    
    result2 = monitor.analyze("分析 ASIN B071WV2SRC")
    print(f"\n[Result] Targets: {len(result2.get('targets', []))}")
    
    # 测试场景3: 批量监控
    print("\n" + "="*70)
    print("TEST 3: Multi-ASIN Monitor")
    print("="*70)
    
    result3 = monitor.analyze("分析 B071WV2SRC, B08KHQY9DV")
    print(f"\n[Result] Targets: {len(result3.get('targets', []))}")
