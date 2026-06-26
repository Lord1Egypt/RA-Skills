#!/usr/bin/env python3
"""
SKU对比分析 Skill
支持SKU的时间维度、横向、门店、导购等多维度对比分析
"""

import sys
import json
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from datetime import datetime, timedelta

# 添加 API 客户端路径
sys.path.insert(0, '/Users/yangguangwei/.openclaw/workspace-front-door')
from api_client import get_copilot_data

# 添加 SKU 分析 Skill 路径
sys.path.insert(0, '/Users/yangguangwei/.openclaw/skills/sku-store-analysis')
import analyze as sku_analyze


@dataclass
class Finding:
    """发现数据类"""
    title: str
    type: str
    metric: str
    evidence: str
    confidence: str
    implication: str


def fetch_sku_data(store_id: str, goods_base_id: str, from_date: str, to_date: str) -> Dict:
    """获取单SKU基础数据"""
    endpoint = f'/api/v1/store/dashboard/bi/goods/detail?storeId={store_id}&fromDate={from_date}&toDate={to_date}&goodsBaseId={goods_base_id}'
    return get_copilot_data(endpoint)


def fetch_sku_performance(store_id: str, goods_base_id: str, from_date: str, to_date: str) -> Dict:
    """获取单SKU导购表现数据"""
    endpoint = f'/api/v1/store/dashboard/bi/goods/performance?storeId={store_id}&fromDate={from_date}&toDate={to_date}&goodsBaseId={goods_base_id}'
    return get_copilot_data(endpoint)


def compare_sku_over_time(
    store_id: str,
    goods_base_id: str,
    period_a_from: str,
    period_a_to: str,
    period_b_from: str,
    period_b_to: str,
    store_name: str = "",
    comparison_label: str = "对比"
) -> Dict:
    """
    SKU时间维度对比（上市初期vs近期、促销前后等）
    
    Args:
        store_id: 门店ID
        goods_base_id: 商品基础ID
        period_a_from/to: 时期A起止日期
        period_b_from/to: 时期B起止日期
        store_name: 门店名称
        comparison_label: 对比标签（如"促销前后"、"上市初期vs近期"）
    """
    
    print(f"\n{'='*70}")
    print(f"SKU时间维度对比分析")
    print(f"商品ID: {goods_base_id}")
    print(f"对比类型: {comparison_label}")
    print(f"{'='*70}\n")
    
    # 获取时期A数据
    print(f"【获取时期A数据: {period_a_from} 至 {period_a_to}】")
    data_a = fetch_sku_data(store_id, goods_base_id, period_a_from, period_a_to)
    perf_a = fetch_sku_performance(store_id, goods_base_id, period_a_from, period_a_to)
    
    # 获取时期B数据
    print(f"\n【获取时期B数据: {period_b_from} 至 {period_b_to}】")
    data_b = fetch_sku_data(store_id, goods_base_id, period_b_from, period_b_to)
    perf_b = fetch_sku_performance(store_id, goods_base_id, period_b_from, period_b_to)
    
    if not data_a or 'goods' not in data_a or not data_b or 'goods' not in data_b:
        return {'status': 'error', 'message': '无法获取SKU数据'}
    
    # 计算变化
    print(f"\n【计算对比变化】")
    changes = calculate_sku_changes(data_a['goods'], data_b['goods'], perf_a, perf_b)
    
    # 生成洞察
    print(f"\n【生成对比洞察】")
    insights = generate_time_comparison_insights(
        data_a['goods'], data_b['goods'], 
        changes, comparison_label
    )
    
    result = {
        'status': 'ok',
        'store_id': store_id,
        'goods_base_id': goods_base_id,
        'comparison_label': comparison_label,
        'period_a': {
            'from': period_a_from,
            'to': period_a_to,
            'goods': data_a['goods']
        },
        'period_b': {
            'from': period_b_from,
            'to': period_b_to,
            'goods': data_b['goods']
        },
        'changes': changes,
        'insights': insights
    }
    
    print_time_comparison_result(result)
    
    print(f"\n{'='*70}")
    print("时间维度对比完成")
    print(f"{'='*70}\n")
    
    return result


def compare_skus(
    store_id: str,
    goods_base_ids: List[str],
    from_date: str,
    to_date: str,
    store_name: str = "",
    comparison_focus: str = "all"
) -> Dict:
    """
    多SKU横向对比（同品类、同价格带、TOP商品对比）
    
    Args:
        store_id: 门店ID
        goods_base_ids: 商品ID列表
        from_date/to_date: 分析日期范围
        store_name: 门店名称
        comparison_focus: 对比重点（all/sales/price/inventory/aiot）
    """
    
    print(f"\n{'='*70}")
    print(f"SKU横向对比分析")
    print(f"对比商品数: {len(goods_base_ids)}")
    print(f"分析周期: {from_date} 至 {to_date}")
    print(f"{'='*70}\n")
    
    # 批量获取SKU数据
    print("【批量获取SKU数据】")
    skus_data = []
    for goods_id in goods_base_ids:
        data = fetch_sku_data(store_id, goods_id, from_date, to_date)
        if data and 'goods' in data:
            skus_data.append({
                'goods_id': goods_id,
                'goods': data['goods']
            })
    
    if not skus_data:
        return {'status': 'error', 'message': '无法获取SKU数据'}
    
    # 生成排名
    print("\n【生成多维排名】")
    rankings = generate_sku_rankings(skus_data)
    
    # 生成洞察
    print("\n【生成对比洞察】")
    insights = generate_cross_sku_insights(skus_data, rankings)
    
    result = {
        'status': 'ok',
        'store_id': store_id,
        'period': {'from': from_date, 'to': to_date},
        'total_skus': len(skus_data),
        'rankings': rankings,
        'insights': insights
    }
    
    print_cross_sku_result(result)
    
    print(f"\n{'='*70}")
    print("横向对比完成")
    print(f"{'='*70}\n")
    
    return result


def compare_sku_clerks(
    store_id: str,
    goods_base_id: str,
    from_date: str,
    to_date: str,
    store_name: str = ""
) -> Dict:
    """
    SKU导购对比分析（高销售vs低销售、高转化vs低转化）
    
    Args:
        store_id: 门店ID
        goods_base_id: 商品基础ID
        from_date/to_date: 分析日期范围
        store_name: 门店名称
    """
    
    print(f"\n{'='*70}")
    print(f"SKU导购对比分析")
    print(f"商品ID: {goods_base_id}")
    print(f"分析周期: {from_date} 至 {to_date}")
    print(f"{'='*70}\n")
    
    # 获取导购表现数据
    print("【获取导购表现数据】")
    perf_data = fetch_sku_performance(store_id, goods_base_id, from_date, to_date)
    
    if not perf_data or 'clerks' not in perf_data:
        return {'status': 'error', 'message': '无法获取导购数据'}
    
    clerks_list = perf_data['clerks'].get('list', [])
    
    if not clerks_list:
        return {'status': 'error', 'message': '无导购销售数据'}
    
    # 分类导购
    print("【分析导购表现分层】")
    clerk_analysis = analyze_clerk_performance(clerks_list)
    
    # 生成洞察
    print("\n【生成导购对比洞察】")
    insights = generate_clerk_comparison_insights(clerk_analysis)
    
    result = {
        'status': 'ok',
        'store_id': store_id,
        'goods_base_id': goods_base_id,
        'period': {'from': from_date, 'to': to_date},
        'clerk_analysis': clerk_analysis,
        'insights': insights
    }
    
    print_clerk_comparison_result(result)
    
    print(f"\n{'='*70}")
    print("导购对比完成")
    print(f"{'='*70}\n")
    
    return result


def calculate_sku_changes(goods_a: Dict, goods_b: Dict, perf_a: Dict, perf_b: Dict) -> Dict:
    """计算SKU时期变化"""
    
    changes = {}
    
    # 销售指标变化
    sales_a = goods_a.get('dealAmount', 0)
    sales_b = goods_b.get('dealAmount', 0)
    changes['sales'] = {
        'before': sales_a,
        'after': sales_b,
        'change': sales_b - sales_a,
        'change_pct': round((sales_b - sales_a) / sales_a * 100, 1) if sales_a > 0 else 0
    }
    
    # 销量变化
    qty_a = goods_a.get('qty', 0)
    qty_b = goods_b.get('qty', 0)
    changes['qty'] = {
        'before': qty_a,
        'after': qty_b,
        'change': qty_b - qty_a,
        'change_pct': round((qty_b - qty_a) / qty_a * 100, 1) if qty_a > 0 else 0
    }
    
    # 成交均价变化
    avg_a = goods_a.get('dealAvgAmount', 0)
    avg_b = goods_b.get('dealAvgAmount', 0)
    changes['avg_price'] = {
        'before': avg_a,
        'after': avg_b,
        'change': avg_b - avg_a,
        'change_pct': round((avg_b - avg_a) / avg_a * 100, 1) if avg_a > 0 else 0
    }
    
    # 折扣率变化
    std_price = goods_a.get('standardPrice', 0)
    if std_price > 0:
        discount_a = (1 - avg_a / std_price) * 100
        discount_b = (1 - avg_b / std_price) * 100
        changes['discount'] = {
            'before': round(discount_a, 1),
            'after': round(discount_b, 1),
            'change': round(discount_b - discount_a, 1)
        }
    
    # 库存变化
    inv_a = goods_a.get('inventory', 0)
    inv_b = goods_b.get('inventory', 0)
    changes['inventory'] = {
        'before': inv_a,
        'after': inv_b,
        'change': inv_b - inv_a
    }
    
    # AIoT转化变化（如果有数据）
    if perf_a and perf_b and 'performances' in perf_a and 'performances' in perf_b:
        perf_data_a = perf_a['performances']
        perf_data_b = perf_b['performances']
        
        trans_rate_a = perf_data_a.get('deepTrialTransRate', 0)
        trans_rate_b = perf_data_b.get('deepTrialTransRate', 0)
        changes['deep_trial_trans_rate'] = {
            'before': trans_rate_a,
            'after': trans_rate_b,
            'change': round(trans_rate_b - trans_rate_a, 2)
        }
    
    return changes


def generate_time_comparison_insights(goods_a: Dict, goods_b: Dict, changes: Dict, label: str) -> List[Dict]:
    """生成时间对比洞察"""
    insights = []
    
    # 销售变化洞察
    sales_change = changes['sales']['change_pct']
    if abs(sales_change) > 20:
        direction = "提升" if sales_change > 0 else "下滑"
        insights.append({
            'type': 'significant_change',
            'title': f'销售额大幅{direction} {abs(sales_change):.1f}%',
            'evidence': f'从¥{changes["sales"]["before"]:,.2f}到¥{changes["sales"]["after"]:,.2f}',
            'implication': f'{label}取得显著{"成效" if sales_change > 0 else "变化"}，{"总结成功经验" if sales_change > 0 else "分析原因"}'
        })
    
    # 价格策略洞察
    if 'discount' in changes:
        discount_change = changes['discount']['change']
        if abs(discount_change) > 5:
            direction = "加大" if discount_change > 0 else "减少"
            insights.append({
                'type': 'price_strategy',
                'title': f'折扣力度{direction} {abs(discount_change):.1f}个百分点',
                'evidence': f'折扣率从{changes["discount"]["before"]:.1f}%到{changes["discount"]["after"]:.1f}%',
                'implication': '价格策略调整对销售的影响需评估'
            })
    
    # 库存变化洞察
    inv_change = changes['inventory']['change']
    if inv_change < -5:
        insights.append({
            'type': 'inventory',
            'title': f'库存减少 {abs(inv_change)}件',
            'evidence': f'从{changes["inventory"]["before"]}件到{changes["inventory"]["after"]}件',
            'implication': '动销加快，需关注补货'
        })
    
    # AIoT转化洞察
    if 'deep_trial_trans_rate' in changes:
        trans_change = changes['deep_trial_trans_rate']['change']
        if abs(trans_change) > 0.1:
            direction = "提升" if trans_change > 0 else "下降"
            insights.append({
                'type': 'conversion',
                'title': f'深度试用转化率{direction} {abs(trans_change):.0%}',
                'evidence': f'从{changes["deep_trial_trans_rate"]["before"]:.0%}到{changes["deep_trial_trans_rate"]["after"]:.0%}',
                'implication': f'{"导购销售技巧改善" if trans_change > 0 else "需优化转化流程"}'
            })
    
    return insights


def generate_sku_rankings(skus_data: List[Dict]) -> Dict:
    """生成SKU多维排名"""
    
    rankings = {
        'by_sales': sorted(skus_data, key=lambda x: x['goods'].get('dealAmount', 0), reverse=True),
        'by_qty': sorted(skus_data, key=lambda x: x['goods'].get('qty', 0), reverse=True),
        'by_price': sorted(skus_data, key=lambda x: x['goods'].get('dealAvgAmount', 0), reverse=True),
        'by_discount': sorted(skus_data, key=lambda x: x['goods'].get('dealAvgAmount', 0) / x['goods'].get('standardPrice', 1) if x['goods'].get('standardPrice', 0) > 0 else 0),
        'by_inventory': sorted(skus_data, key=lambda x: x['goods'].get('inventory', 0), reverse=True)
    }
    
    return rankings


def generate_cross_sku_insights(skus_data: List[Dict], rankings: Dict) -> List[Dict]:
    """生成横向对比洞察"""
    insights = []
    
    if len(skus_data) < 2:
        return insights
    
    # 销售集中度
    total_sales = sum(s['goods'].get('dealAmount', 0) for s in skus_data)
    top1_sales = rankings['by_sales'][0]['goods'].get('dealAmount', 0)
    top1_share = top1_sales / total_sales if total_sales > 0 else 0
    
    if top1_share > 0.5:
        insights.append({
            'type': 'concentration',
            'title': f'销售高度集中，TOP1占比{top1_share:.0%}',
            'evidence': f'{rankings["by_sales"][0]["goods"].get("goodsName", "")}销售额¥{top1_sales:,.2f}',
            'implication': '资源过于集中在单一SKU，需关注其他SKU培育'
        })
    
    # 价格差异
    prices = [s['goods'].get('dealAvgAmount', 0) for s in skus_data if s['goods'].get('dealAvgAmount', 0) > 0]
    if len(prices) >= 2:
        price_gap = max(prices) - min(prices)
        price_gap_pct = price_gap / min(prices) if min(prices) > 0 else 0
        if price_gap_pct > 0.5:
            insights.append({
                'type': 'price_variance',
                'title': f'价格差异大（{price_gap_pct:.0%}）',
                'evidence': f'最高价¥{max(prices):.0f} vs 最低价¥{min(prices):.0f}',
                'implication': '价格带覆盖广，需确保各价位段都有竞争力'
            })
    
    # 库存健康度
    low_inventory_skus = [s for s in skus_data if s['goods'].get('inventory', 0) <= 2 and s['goods'].get('inventory', 0) > 0]
    if low_inventory_skus:
        insights.append({
            'type': 'inventory_risk',
            'title': f'{len(low_inventory_skus)}个SKU库存偏低',
            'evidence': f'{", ".join([s["goods"].get("goodsName", "") for s in low_inventory_skus[:3]])}等',
            'implication': '存在断货风险，建议补货'
        })
    
    return insights


def analyze_clerk_performance(clerks_list: List[Dict]) -> Dict:
    """分析导购表现分层"""
    
    # 过滤有销售的导购
    active_clerks = [c for c in clerks_list if c.get('salesAmount', 0) > 0]
    
    if not active_clerks:
        return {'active_clerks': [], 'zero_sales_clerks': clerks_list}
    
    # 按销售额排序
    sorted_by_sales = sorted(active_clerks, key=lambda x: x.get('salesAmount', 0), reverse=True)
    
    # 分层
    total_sales = sum(c.get('salesAmount', 0) for c in active_clerks)
    
    # 高销售导购（TOP 30%）
    high_sales_count = max(1, len(active_clerks) // 3)
    high_sales = sorted_by_sales[:high_sales_count]
    
    # 低销售导购（后 30%）
    low_sales = sorted_by_sales[-high_sales_count:]
    
    # 高转化导购（deepTrialTransRate > 50%）
    high_conversion = [c for c in active_clerks if c.get('deepTrialTransRate', 0) >= 0.5]
    
    # 低转化导购（deepTrialTransRate < 20% 但有试用）
    low_conversion = [c for c in active_clerks if c.get('deepTrialTransRate', 0) < 0.2 and c.get('deepTrialGroup', 0) > 0]
    
    # 零销售导购
    zero_sales = [c for c in clerks_list if c.get('salesAmount', 0) == 0]
    
    return {
        'total_clerks': len(clerks_list),
        'active_clerks': len(active_clerks),
        'high_sales': high_sales,
        'low_sales': low_sales,
        'high_conversion': high_conversion,
        'low_conversion': low_conversion,
        'zero_sales': zero_sales,
        'top_performer': sorted_by_sales[0] if sorted_by_sales else None,
        'bottom_performer': sorted_by_sales[-1] if sorted_by_sales else None
    }


def generate_clerk_comparison_insights(clerk_analysis: Dict) -> List[Dict]:
    """生成导购对比洞察"""
    insights = []
    
    # 销售集中度
    if clerk_analysis['active_clerks'] > 0:
        top1 = clerk_analysis['top_performer']
        if top1:
            top1_share = top1.get('salesPercentageFloat', 0)
            if top1_share > 0.4:
                insights.append({
                    'type': 'concentration',
                    'title': f'销售高度集中，TOP1导购占比{top1_share:.0%}',
                    'evidence': f'{top1.get("clerkName", "").strip()}销售额¥{top1.get("salesAmount", 0):,.2f}',
                    'implication': '过于依赖单一导购，需培养团队销售能力'
                })
    
    # 零销售问题
    if clerk_analysis['zero_sales']:
        insights.append({
            'type': 'zero_sales',
            'title': f'{len(clerk_analysis["zero_sales"])}位导购零销售',
            'evidence': f'{", ".join([c.get("clerkName", "").strip() for c in clerk_analysis["zero_sales"][:3]])}等未售出',
            'implication': '需培训或激励措施'
        })
    
    # 高转化标杆
    if clerk_analysis['high_conversion']:
        top_converter = max(clerk_analysis['high_conversion'], key=lambda x: x.get('deepTrialTransRate', 0))
        insights.append({
            'type': 'best_practice',
            'title': f'高转化标杆: {top_converter.get("clerkName", "").strip()}',
            'evidence': f'深度试用转化率{top_converter.get("deepTrialTransRate", 0):.0%}',
            'implication': '总结其销售技巧，推广给团队'
        })
    
    # 低转化问题
    if clerk_analysis['low_conversion']:
        insights.append({
            'type': 'improvement',
            'title': f'{len(clerk_analysis["low_conversion"])}位导购转化偏低',
            'evidence': f'深度试用转化率低于20%',
            'implication': '需优化跟进流程或销售话术'
        })
    
    return insights


# ==================== 打印函数 ====================

def print_time_comparison_result(result: Dict):
    """打印时间对比结果"""
    changes = result['changes']
    
    print(f"\n{'='*70}")
    print(f"对比变化汇总")
    print(f"{'='*70}")
    print(f"{'指标':<15} {'时期A':>12} {'时期B':>12} {'变化':>10} {'变化率':>8}")
    print(f"{'-'*60}")
    
    for metric, label in [('sales', '销售额'), ('qty', '销量'), ('avg_price', '成交均价')]:
        if metric in changes:
            c = changes[metric]
            change_str = f"{'+' if c['change'] > 0 else ''}{c['change']:,.0f}"
            change_pct_str = f"{'+' if c['change_pct'] > 0 else ''}{c['change_pct']:.1f}%"
            print(f"{label:<15} {c['before']:>12,.0f} {c['after']:>12,.0f} {change_str:>10} {change_pct_str:>8}")
    
    if result['insights']:
        print(f"\n{'='*70}")
        print(f"关键洞察")
        print(f"{'='*70}")
        for i, insight in enumerate(result['insights'], 1):
            print(f"\n{i}. {insight['title']}")
            print(f"   证据: {insight['evidence']}")
            print(f"   建议: {insight['implication']}")


def print_cross_sku_result(result: Dict):
    """打印横向对比结果"""
    rankings = result['rankings']
    
    print(f"\n{'='*70}")
    print(f"销售额排名")
    print(f"{'='*70}")
    print(f"{'排名':<4} {'商品':<15} {'销售额':>10} {'销量':>6} {'均价':>8}")
    print(f"{'-'*50}")
    for i, s in enumerate(rankings['by_sales'], 1):
        g = s['goods']
        print(f"#{i:<3} {g.get('goodsName', ''):<15} ¥{g.get('dealAmount', 0):>8,.0f} {g.get('qty', 0):>5}件 ¥{g.get('dealAvgAmount', 0):>7,.0f}")
    
    if result['insights']:
        print(f"\n{'='*70}")
        print(f"对比洞察")
        print(f"{'='*70}")
        for i, insight in enumerate(result['insights'], 1):
            emoji = {"concentration": "⚠️", "price_variance": "📊", "inventory_risk": "🔔"}.get(insight['type'], "•")
            print(f"\n{i}. {emoji} {insight['title']}")
            print(f"   证据: {insight['evidence']}")
            print(f"   建议: {insight['implication']}")


def print_clerk_comparison_result(result: Dict):
    """打印导购对比结果"""
    analysis = result['clerk_analysis']
    
    print(f"\n{'='*70}")
    print(f"导购表现分层")
    print(f"{'='*70}")
    print(f"总导购数: {analysis['total_clerks']} | 有销售: {analysis['active_clerks']} | 零销售: {len(analysis['zero_sales'])}")
    
    if analysis['top_performer']:
        top = analysis['top_performer']
        print(f"\n🏆 销售冠军: {top.get('clerkName', '').strip()}")
        print(f"   销售额: ¥{top.get('salesAmount', 0):,.2f} ({top.get('salesPercentage', '0')})")
        print(f"   连带率: {top.get('attachQtyRatio', 0):.2f}")
    
    if analysis['high_conversion']:
        print(f"\n📈 高转化导购 ({len(analysis['high_conversion'])}位):")
        for c in analysis['high_conversion'][:3]:
            print(f"   • {c.get('clerkName', '').strip()}: 转化率{c.get('deepTrialTransRate', 0):.0%}")
    
    if analysis['low_conversion']:
        print(f"\n📉 待提升导购 ({len(analysis['low_conversion'])}位):")
        for c in analysis['low_conversion'][:3]:
            print(f"   • {c.get('clerkName', '').strip()}: 转化率{c.get('deepTrialTransRate', 0):.0%}")
    
    if result['insights']:
        print(f"\n{'='*70}")
        print(f"导购洞察")
        print(f"{'='*70}")
        for i, insight in enumerate(result['insights'], 1):
            emoji = {"concentration": "⚠️", "zero_sales": "🔔", "best_practice": "🏆", "improvement": "📈"}.get(insight['type'], "•")
            print(f"\n{i}. {emoji} {insight['title']}")
            print(f"   证据: {insight['evidence']}")
            print(f"   建议: {insight['implication']}")


if __name__ == "__main__":
    # 测试1: 时间维度对比
    print("\n" + "="*70)
    print("测试1: 时间维度对比")
    print("="*70)
    
    result = compare_sku_over_time(
        store_id="416759_1714379448487",
        goods_base_id="34311",
        period_a_from="2026-03-01",
        period_a_to="2026-03-15",
        period_b_from="2026-03-16",
        period_b_to="2026-03-26",
        comparison_label="3月上半月vs下半月"
    )
    
    # 测试2: 导购对比
    print("\n" + "="*70)
    print("测试2: 导购对比分析")
    print("="*70)
    
    result = compare_sku_clerks(
        store_id="416759_1714379448487",
        goods_base_id="34311",
        from_date="2026-03-01",
        to_date="2026-03-26"
    )
