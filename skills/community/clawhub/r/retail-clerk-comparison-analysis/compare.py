"""
导购对比分析模块
基于 clerk-performance-analysis 的扩展，提供时间维度和横向对比功能
"""

import sys
import os
# 使用绝对路径导入 clerk-performance-analysis
perf_analysis_path = os.path.expanduser('~/.openclaw/skills/clerk-performance-analysis')
sys.path.insert(0, perf_analysis_path)
from analyze import analyze
from typing import Dict, List, Any
from datetime import datetime, timedelta


def compare_guide_over_time(
    store_id: str,
    guide_name: str,
    period_a_from: str,
    period_a_to: str,
    period_b_from: str,
    period_b_to: str,
    comparison_label: str = "对比"
) -> Dict:
    """
    导购自身时间维度对比（通用入口）
    
    使用场景：
    - 培训前后对比：period_a=培训前7天, period_b=培训后7天
    - 活动效果评估：period_a=活动前7天, period_b=活动期间
    - 月度环比：period_a=上月, period_b=本月
    - 波动归因：period_a=低谷期, period_b=高峰期
    
    Args:
        store_id: 门店ID
        guide_name: 导购姓名
        period_a_from: 时期A开始日期 (YYYY-MM-DD)
        period_a_to: 时期A结束日期 (YYYY-MM-DD)
        period_b_from: 时期B开始日期 (YYYY-MM-DD)
        period_b_to: 时期B结束日期 (YYYY-MM-DD)
        comparison_label: 对比标签，如"培训前后"、"活动前后"
    
    Returns:
        Dict: 对比分析结果
    """
    
    print(f"\n{'='*70}")
    print(f"导购时间维度对比分析 - {guide_name}")
    print(f"对比类型: {comparison_label}")
    print(f"{'='*70}\n")
    
    # 获取时期A的分析结果
    print(f"【获取时期A数据: {period_a_from} 至 {period_a_to}】")
    result_a = analyze(store_id, guide_name, period_a_from, period_a_to)
    
    # 获取时期B的分析结果
    print(f"\n【获取时期B数据: {period_b_from} 至 {period_b_to}】")
    result_b = analyze(store_id, guide_name, period_b_from, period_b_to)
    
    # 计算变化
    print(f"\n【计算对比变化】")
    changes = _calculate_changes(result_a, result_b)
    
    # 识别关键变化
    print(f"\n【识别关键变化】")
    key_findings = _identify_key_changes(result_a, result_b, changes)
    
    # 组装结果
    comparison = {
        'status': 'ok',
        'store_id': store_id,
        'guide_name': guide_name,
        'comparison_label': comparison_label,
        'period_a': {
            'from': period_a_from,
            'to': period_a_to,
            'metrics': result_a['core_metrics'],
            'findings': result_a['findings']
        },
        'period_b': {
            'from': period_b_from,
            'to': period_b_to,
            'metrics': result_b['core_metrics'],
            'findings': result_b['findings']
        },
        'changes': changes,
        'key_findings': key_findings,
        'recommendations': _generate_comparison_recommendations(key_findings, comparison_label)
    }
    
    # 打印对比结果
    _print_comparison_result(comparison)
    
    print(f"\n{'='*70}")
    print("对比分析完成")
    print(f"{'='*70}\n")
    
    return comparison


def compare_guides(
    store_id: str,
    guide_names: List[str],
    from_date: str,
    to_date: str,
    comparison_focus: str = "all"
) -> Dict:
    """
    多人导购横向对比（高频使用场景）
    
    使用场景：
    - 晨会快速对比昨日表现
    - 周会排名和差距分析
    - 月度绩效对标
    - 标杆学习和经验分享
    
    Args:
        store_id: 门店ID
        guide_names: 导购姓名列表
        from_date: 分析开始日期 (YYYY-MM-DD)
        to_date: 分析结束日期 (YYYY-MM-DD)
        comparison_focus: 对比重点，可选 all/sales/new_customer/atv/attach
    
    Returns:
        Dict: 横向对比结果
    """
    
    print(f"\n{'='*70}")
    print(f"导购横向对比分析")
    print(f"门店: {store_id}")
    print(f"分析周期: {from_date} 至 {to_date}")
    print(f"{'='*70}\n")
    
    # 批量获取所有导购数据
    print(f"【批量获取 {len(guide_names)} 位导购数据】")
    guides_data = []
    for name in guide_names:
        result = analyze(store_id, name, from_date, to_date)
        guides_data.append({
            'name': name,
            'sales': result['core_metrics']['sales']['amount'],
            'sales_rank': result['core_metrics']['sales']['rank'],
            'sales_share': result['core_metrics']['sales']['share'],
            'orders': result['core_metrics']['orders']['count'],
            'atv': result['core_metrics']['atv']['value'],
            'new_customers': result['core_metrics']['new_customers']['count'],
            'attach': result['core_metrics']['attach']['qty_ratio'],
            'efficiency': result['core_metrics']['efficiency']['value'],
            'high_findings': len([f for f in result['findings'] if f['severity'] == 'high']),
            'medium_findings': len([f for f in result['findings'] if f['severity'] == 'medium'])
        })
    
    # 生成排名
    print(f"\n【生成多维排名】")
    rankings = {
        'by_sales': sorted(guides_data, key=lambda x: x['sales'], reverse=True),
        'by_new_customers': sorted(guides_data, key=lambda x: x['new_customers'], reverse=True),
        'by_atv': sorted(guides_data, key=lambda x: x['atv'], reverse=True),
        'by_attach': sorted(guides_data, key=lambda x: x['attach'], reverse=True),
        'by_orders': sorted(guides_data, key=lambda x: x['orders'], reverse=True)
    }
    
    # 找出标杆和待提升对象
    top_performer = rankings['by_sales'][0]
    bottom_performer = rankings['by_sales'][-1]
    
    # 生成差距分析
    print(f"\n【生成差距分析】")
    gap_analysis = _calculate_gaps(rankings['by_sales'])
    
    # 识别需要关注的导购
    needs_attention = [g for g in guides_data if g['high_findings'] > 0]
    
    # 组装结果
    comparison = {
        'status': 'ok',
        'store_id': store_id,
        'period': {'from': from_date, 'to': to_date},
        'total_guides': len(guide_names),
        'rankings': rankings,
        'top_performer': top_performer,
        'bottom_performer': bottom_performer,
        'gap_analysis': gap_analysis,
        'needs_attention': needs_attention,
        'quick_insights': _generate_quick_insights(rankings, guides_data)
    }
    
    # 打印对比结果
    _print_guides_comparison(comparison)
    
    print(f"\n{'='*70}")
    print("横向对比完成")
    print(f"{'='*70}\n")
    
    return comparison


def compare_with_benchmark(
    store_id: str,
    guide_name: str,
    benchmark_guide_name: str,
    from_date: str,
    to_date: str
) -> Dict:
    """
    与标杆导购对比（找差距）
    
    Args:
        store_id: 门店ID
        guide_name: 待提升导购姓名
        benchmark_guide_name: 标杆导购姓名
        from_date: 分析开始日期
        to_date: 分析结束日期
    
    Returns:
        Dict: 标杆对比结果
    """
    
    print(f"\n{'='*70}")
    print(f"标杆对比分析")
    print(f"待提升: {guide_name} vs 标杆: {benchmark_guide_name}")
    print(f"{'='*70}\n")
    
    # 获取两个导购的数据
    guide_result = analyze(store_id, guide_name, from_date, to_date)
    benchmark_result = analyze(store_id, benchmark_guide_name, from_date, to_date)
    
    # 计算差距
    gaps = _calculate_benchmark_gaps(guide_result, benchmark_result)
    
    # 识别学习点
    learning_points = _identify_learning_points(guide_result, benchmark_result)
    
    # 组装结果
    comparison = {
        'status': 'ok',
        'store_id': store_id,
        'period': {'from': from_date, 'to': to_date},
        'guide': {
            'name': guide_name,
            'metrics': guide_result['core_metrics'],
            'findings': guide_result['findings']
        },
        'benchmark': {
            'name': benchmark_guide_name,
            'metrics': benchmark_result['core_metrics'],
            'findings': benchmark_result['findings']
        },
        'gaps': gaps,
        'learning_points': learning_points,
        'action_plan': _generate_action_plan(gaps, learning_points)
    }
    
    # 打印对比结果
    _print_benchmark_comparison(comparison)
    
    print(f"\n{'='*70}")
    print("标杆对比完成")
    print(f"{'='*70}\n")
    
    return comparison


# ==================== 辅助函数 ====================

def _calculate_changes(result_a: Dict, result_b: Dict) -> Dict:
    """计算两个时期的变化"""
    changes = {}
    
    # 定义指标访问路径
    metric_paths = {
        'sales': ('sales', 'amount'),
        'orders': ('orders', 'count'),
        'atv': ('atv', 'value'),
        'new_customers': ('new_customers', 'count'),
        'attach': ('attach', 'qty_ratio')
    }
    
    for metric, (key, subkey) in metric_paths.items():
        val_a = result_a['core_metrics'][key][subkey]
        val_b = result_b['core_metrics'][key][subkey]
        
        change = val_b - val_a
        change_pct = (change / val_a * 100) if val_a > 0 else 0
        
        changes[metric] = {
            'before': val_a,
            'after': val_b,
            'change': round(change, 2),
            'change_pct': round(change_pct, 1),
            'trend': 'up' if change > 0 else 'down' if change < 0 else 'stable'
        }
    
    return changes


def _identify_key_changes(result_a: Dict, result_b: Dict, changes: Dict) -> List[Dict]:
    """识别关键变化"""
    findings = []
    
    # 销售额变化 > 20%
    if abs(changes['sales']['change_pct']) > 20:
        findings.append({
            'type': 'significant_change',
            'metric': 'sales',
            'title': f'销售额{"提升" if changes["sales"]["change"] > 0 else "下降"}{abs(changes["sales"]["change_pct"]):.1f}%',
            'severity': 'high' if abs(changes['sales']['change_pct']) > 30 else 'medium',
            'details': f'从¥{changes["sales"]["before"]:,.0f}到¥{changes["sales"]["after"]:,.0f}'
        })
    
    # 新客数变化
    if changes['new_customers']['change'] > 0:
        findings.append({
            'type': 'improvement',
            'metric': 'new_customers',
            'title': f'新客获取能力提升',
            'severity': 'medium',
            'details': f'新增{changes["new_customers"]["change"]:.0f}人'
        })
    
    # 发现问题改善
    before_findings = {f['metric'] for f in result_a['findings']}
    after_findings = {f['metric'] for f in result_b['findings']}
    resolved = before_findings - after_findings
    
    if resolved:
        findings.append({
            'type': 'problem_resolved',
            'title': f'改善了{len(resolved)}个问题',
            'severity': 'low',
            'details': f'已解决: {", ".join(resolved)}'
        })
    
    return findings


def _generate_comparison_recommendations(findings: List[Dict], label: str) -> List[Dict]:
    """生成对比分析建议"""
    recommendations = []
    
    for finding in findings:
        if finding['type'] == 'significant_change' and finding['severity'] == 'high':
            if '提升' in finding['title']:
                recommendations.append({
                    'priority': 'medium',
                    'action': '固化成功经验',
                    'details': f'{label}取得显著提升，总结成功因素并固化',
                    'expected_impact': '保持提升效果'
                })
            else:
                recommendations.append({
                    'priority': 'high',
                    'action': '分析下滑原因',
                    'details': f'{label}出现下滑，需要深入分析原因',
                    'expected_impact': '止跌回升'
                })
    
    return recommendations


def _calculate_gaps(sorted_guides: List[Dict]) -> List[Dict]:
    """计算与标杆的差距"""
    if not sorted_guides:
        return []
    
    top = sorted_guides[0]
    gaps = []
    
    for guide in sorted_guides[1:]:
        gap_sales = top['sales'] - guide['sales']
        gap_pct = (gap_sales / top['sales'] * 100) if top['sales'] > 0 else 0
        
        gaps.append({
            'guide': guide['name'],
            'gap_to_top': gap_sales,
            'gap_pct': round(gap_pct, 1),
            'potential': f"若达到标杆，可提升¥{gap_sales:,.0f}"
        })
    
    return gaps


def _calculate_benchmark_gaps(guide_result: Dict, benchmark_result: Dict) -> Dict:
    """计算与标杆的具体差距"""
    gaps = {}
    
    metrics = ['sales', 'orders', 'atv', 'new_customers', 'attach']
    for metric in metrics:
        guide_val = guide_result['core_metrics'][metric]['amount'] if metric != 'attach' else guide_result['core_metrics'][metric]['qty_ratio']
        benchmark_val = benchmark_result['core_metrics'][metric]['amount'] if metric != 'attach' else benchmark_result['core_metrics'][metric]['qty_ratio']
        
        gap = benchmark_val - guide_val
        gap_pct = (gap / benchmark_val * 100) if benchmark_val > 0 else 0
        
        gaps[metric] = {
            'guide_value': guide_val,
            'benchmark_value': benchmark_val,
            'gap': round(gap, 2),
            'gap_pct': round(gap_pct, 1)
        }
    
    return gaps


def _identify_learning_points(guide_result: Dict, benchmark_result: Dict) -> List[Dict]:
    """识别可以向标杆学习的点"""
    learning_points = []
    
    # 新客获取差距大
    if benchmark_result['core_metrics']['new_customers']['count'] > guide_result['core_metrics']['new_customers']['count'] * 1.3:
        learning_points.append({
            'area': '新客获取',
            'gap': benchmark_result['core_metrics']['new_customers']['count'] - guide_result['core_metrics']['new_customers']['count'],
            'suggestion': f'学习{benchmark_result["guide_name"]}的新客开发方法'
        })
    
    # 连带率差距
    if benchmark_result['core_metrics']['attach']['qty_ratio'] > guide_result['core_metrics']['attach']['qty_ratio'] * 1.1:
        learning_points.append({
            'area': '连带销售',
            'gap': round(benchmark_result['core_metrics']['attach']['qty_ratio'] - guide_result['core_metrics']['attach']['qty_ratio'], 2),
            'suggestion': f'学习{benchmark_result["guide_name"]}的连带销售技巧'
        })
    
    return learning_points


def _generate_action_plan(gaps: Dict, learning_points: List[Dict]) -> List[Dict]:
    """生成改进行动计划"""
    actions = []
    
    for point in learning_points:
        actions.append({
            'priority': 'high',
            'focus_area': point['area'],
            'action': point['suggestion'],
            'target': f'缩小差距{point["gap"]}'
        })
    
    return actions


def _generate_quick_insights(rankings: Dict, guides_data: List[Dict]) -> List[Dict]:
    """生成快速洞察"""
    insights = []
    
    # 销售额集中度
    total_sales = sum(g['sales'] for g in guides_data)
    top3_sales = sum(g['sales'] for g in rankings['by_sales'][:3])
    concentration = top3_sales / total_sales if total_sales > 0 else 0
    
    if concentration > 0.7:
        insights.append({
            'type': 'risk',
            'title': '业绩过于集中',
            'details': f'TOP3贡献{concentration:.1%}业绩，尾部导购需要关注'
        })
    
    # 新客获取不均衡
    new_customer_counts = [g['new_customers'] for g in guides_data]
    if max(new_customer_counts) > min(new_customer_counts) * 3:
        insights.append({
            'type': 'opportunity',
            'title': '新客获取差异大',
            'details': '新客标杆经验值得推广'
        })
    
    return insights


# ==================== 打印函数 ====================

def _print_comparison_result(comparison: Dict):
    """打印时间对比结果"""
    print(f"\n{'='*70}")
    print(f"对比结果: {comparison['comparison_label']}")
    print(f"{'='*70}")
    
    changes = comparison['changes']
    print(f"\n核心指标变化:")
    print(f"{'指标':<12} {'时期A':>12} {'时期B':>12} {'变化':>10} {'变化率':>8}")
    print(f"{'-'*60}")
    
    for metric, label in [('sales', '销售额'), ('orders', '订单数'), ('atv', '客单价'), ('new_customers', '新客数')]:
        if metric in changes:
            c = changes[metric]
            change_str = f"{'+' if c['change'] > 0 else ''}{c['change']:,.0f}"
            change_pct_str = f"{'+' if c['change_pct'] > 0 else ''}{c['change_pct']:.1f}%"
            print(f"{label:<12} {c['before']:>12,.0f} {c['after']:>12,.0f} {change_str:>10} {change_pct_str:>8}")
    
    if comparison['key_findings']:
        print(f"\n关键发现:")
        for finding in comparison['key_findings']:
            emoji = "✅" if finding['type'] == 'improvement' else "⚠️" if finding['severity'] == 'high' else "ℹ️"
            print(f"  {emoji} {finding['title']}")
    
    if comparison['recommendations']:
        print(f"\n建议:")
        for rec in comparison['recommendations']:
            print(f"  • {rec['action']}: {rec['details']}")


def _print_guides_comparison(comparison: Dict):
    """打印横向对比结果"""
    rankings = comparison['rankings']
    
    print(f"\n{'='*70}")
    print(f"销售额排名")
    print(f"{'='*70}")
    print(f"{'排名':<4} {'导购':<10} {'销售额':>10} {'占比':>6} {'订单':>4} {'客单价':>8} {'新客':>4}")
    print(f"{'-'*70}")
    for i, g in enumerate(rankings['by_sales'], 1):
        print(f"#{i:<3} {g['name']:<10} ¥{g['sales']:>8,.0f} {g['sales_share']:>5.1f}% {g['orders']:>4}单 ¥{g['atv']:>6,.0f} {g['new_customers']:>4}人")
    
    print(f"\n{'='*70}")
    print(f"单项标杆")
    print(f"{'='*70}")
    print(f"🏆 销售额最高: {comparison['top_performer']['name']} (¥{comparison['top_performer']['sales']:,.0f})")
    print(f"🏆 新客数最多: {rankings['by_new_customers'][0]['name']} ({rankings['by_new_customers'][0]['new_customers']}人)")
    print(f"🏆 客单价最高: {rankings['by_atv'][0]['name']} (¥{rankings['by_atv'][0]['atv']:,.0f})")
    print(f"🏆 连带率最高: {rankings['by_attach'][0]['name']} ({rankings['by_attach'][0]['attach']:.2f})")
    
    if comparison['needs_attention']:
        print(f"\n{'='*70}")
        print(f"需要关注")
        print(f"{'='*70}")
        for g in comparison['needs_attention']:
            print(f"⚠️ {g['name']}: 有{g['high_findings']}个高风险问题")
    
    if comparison['quick_insights']:
        print(f"\n{'='*70}")
        print(f"快速洞察")
        print(f"{'='*70}")
        for insight in comparison['quick_insights']:
            emoji = "🚨" if insight['type'] == 'risk' else "💡"
            print(f"{emoji} {insight['title']}: {insight['details']}")


def _print_benchmark_comparison(comparison: Dict):
    """打印标杆对比结果"""
    guide = comparison['guide']
    benchmark = comparison['benchmark']
    gaps = comparison['gaps']
    
    print(f"\n{'='*70}")
    print(f"与标杆差距分析")
    print(f"{'='*70}")
    print(f"{'指标':<12} {guide['name']:>10} {benchmark['name']:>10} {'差距':>10} {'差距率':>8}")
    print(f"{'-'*60}")
    
    for metric, label in [('sales', '销售额'), ('orders', '订单数'), ('atv', '客单价'), ('new_customers', '新客数')]:
        if metric in gaps:
            g = gaps[metric]
            gap_str = f"{'+' if g['gap'] > 0 else ''}{g['gap']:,.0f}"
            gap_pct_str = f"{g['gap_pct']:.1f}%"
            print(f"{label:<12} {g['guide_value']:>10,.0f} {g['benchmark_value']:>10,.0f} {gap_str:>10} {gap_pct_str:>8}")
    
    if comparison['learning_points']:
        print(f"\n{'='*70}")
        print(f"学习要点")
        print(f"{'='*70}")
        for point in comparison['learning_points']:
            print(f"📚 {point['area']}: {point['suggestion']}")
    
    if comparison['action_plan']:
        print(f"\n{'='*70}")
        print(f"行动计划")
        print(f"{'='*70}")
        for action in comparison['action_plan']:
            print(f"✅ {action['focus_area']}: {action['action']}")


if __name__ == "__main__":
    # 测试时间对比
    print("\n" + "="*70)
    print("测试: 培训前后对比")
    print("="*70)
    
    result = compare_guide_over_time(
        store_id="416759_1714379448487",
        guide_name="李翠",
        period_a_from="2026-03-01",
        period_a_to="2026-03-07",
        period_b_from="2026-03-16",
        period_b_to="2026-03-22",
        comparison_label="新品销售培训前后"
    )
    
    print("\n" + "="*70)
    print("测试: 多人横向对比")
    print("="*70)
    
    result = compare_guides(
        store_id="416759_1714379448487",
        guide_names=["李翠", "杨丽", "赵泽瑞"],
        from_date="2026-03-25",
        to_date="2026-03-25"
    )
