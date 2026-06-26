#!/usr/bin/env python3
"""
销售业绩同比分析 Skill
支持门店和导购两个层级的业绩分析
"""

import sys
import json
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from datetime import datetime

# 添加 API 客户端路径
sys.path.insert(0, '/Users/yangguangwei/.openclaw/workspace-front-door')
from api_client import get_copilot_data


@dataclass
class Metric:
    """指标数据类"""
    code: str
    name: str
    current: float
    previous: float
    change_pct: float
    trend: str  # up, down, flat
    
    @property
    def diff(self) -> float:
        return self.current - self.previous


@dataclass
class Finding:
    """发现数据类"""
    title: str
    type: str  # fact, anomaly, hypothesis, recommendation
    metric: str
    evidence: str
    confidence: str  # high, medium, low
    implication: str


def fetch_store_data(store_id: str, from_date: str, to_date: str) -> Dict:
    """获取门店数据"""
    endpoint = f'/api/v1/store/dashboard/bi?storeId={store_id}&fromDate={from_date}&toDate={to_date}'
    return get_copilot_data(endpoint)


def parse_metrics(data: Dict) -> Dict[str, Metric]:
    """解析核心指标"""
    metrics = {}
    
    # 从 metrics 数组解析
    for m in data.get('metrics', []):
        code = m['metricsCode']
        
        # 处理带括号的数值（如 "89046.3(28.4%)"）
        current_val = m['metricsValue']
        if current_val and '(' in str(current_val):
            current_val = str(current_val).split('(')[0]
        
        prev_val = m.get('linkRelativeValue', 0)
        if prev_val and '(' in str(prev_val):
            prev_val = str(prev_val).split('(')[0]
        
        metrics[code] = Metric(
            code=code,
            name=m['metricsName'],
            current=float(current_val) if current_val else 0,
            previous=float(prev_val) if prev_val else 0,
            change_pct=float(m['linkRelativeRate']) if m.get('linkRelativeRate') else 0,
            trend=m.get('trend', 'flat')
        )
    
    # 添加有效销量
    if 'effectiveQtyCount' in data:
        current_qty = data['effectiveQtyCount']
        prev_qty = data.get('CompareEffectiveQtyCount', 0)
        change_pct = ((current_qty - prev_qty) / prev_qty * 100) if prev_qty else 0
        
        metrics['effective_qty_count'] = Metric(
            code='effective_qty_count',
            name='有效销量',
            current=float(current_qty),
            previous=float(prev_qty),
            change_pct=abs(change_pct),
            trend='down' if change_pct < 0 else 'up' if change_pct > 0 else 'flat'
        )
    
    # 添加平均折扣
    if 'avgDiscount' in data:
        current_discount = data['avgDiscount']
        prev_discount = data.get('compareAvgDiscount', 0)
        change_pct = ((current_discount - prev_discount) / prev_discount * 100) if prev_discount else 0
        
        metrics['avg_discount'] = Metric(
            code='avg_discount',
            name='平均折扣',
            current=float(current_discount),
            previous=float(prev_discount),
            change_pct=abs(change_pct),
            trend='down' if change_pct < 0 else 'up' if change_pct > 0 else 'flat'
        )
    
    return metrics


def calculate_attribution(metrics: Dict[str, Metric]) -> Dict:
    """计算业绩波动归因"""
    net_money = metrics.get('net_money')
    order_count = metrics.get('effective_order_count')
    atv = metrics.get('customer_unit_price')
    
    if not all([net_money, order_count, atv]):
        return {}
    
    # 计算各因素贡献
    order_diff = order_count.current - order_count.previous
    atv_diff = atv.current - atv.previous
    
    order_contribution = order_diff * atv.previous
    atv_contribution = atv_diff * order_count.current
    
    total_change = net_money.current - net_money.previous
    
    return {
        "order_contribution": round(order_contribution, 2),
        "atv_contribution": round(atv_contribution, 2),
        "primary_driver": "order" if abs(order_contribution) > abs(atv_contribution) else "atv",
        "order_contribution_pct": round(order_contribution / total_change * 100, 1) if total_change else 0,
        "atv_contribution_pct": round(atv_contribution / total_change * 100, 1) if total_change else 0
    }


def identify_anomalies(metrics: Dict[str, Metric]) -> List[Finding]:
    """识别异常"""
    findings = []
    
    # 销售大幅下滑
    net_money = metrics.get('net_money')
    if net_money and net_money.change_pct > 30 and net_money.trend == 'down':
        findings.append(Finding(
            title="销售额大幅下滑",
            type="anomaly",
            metric="net_money",
            evidence=f"本期销售额{net_money.current:.0f}元，环比下降{net_money.change_pct:.1f}%",
            confidence="high",
            implication="门店经营压力显著，需紧急诊断原因"
        ))
    elif net_money and net_money.change_pct > 10 and net_money.trend == 'down':
        findings.append(Finding(
            title="销售额下滑",
            type="anomaly",
            metric="net_money",
            evidence=f"本期销售额{net_money.current:.0f}元，环比下降{net_money.change_pct:.1f}%",
            confidence="high",
            implication="门店销售表现转弱，需关注改进"
        ))
    
    # 新客获取困难
    new_customer = metrics.get('new_customer_count')
    if new_customer and new_customer.change_pct > 40 and new_customer.trend == 'down':
        findings.append(Finding(
            title="新客获取大幅下降",
            type="anomaly",
            metric="new_customer_count",
            evidence=f"本期新增会员{new_customer.current:.0f}人，环比下降{new_customer.change_pct:.1f}%",
            confidence="high",
            implication="获客渠道效果减弱，需激活引流策略"
        ))
    
    # 连带率偏低
    attach = metrics.get('attach_qty_ratio')
    if attach and attach.current < 1.3:
        findings.append(Finding(
            title="连带率偏低",
            type="anomaly",
            metric="attach_qty_ratio",
            evidence=f"本期连带率{attach.current:.1f}，低于健康阈值1.3",
            confidence="medium",
            implication="连带销售能力不足，需优化商品组合和推销技巧"
        ))
    
    return findings


def generate_recommendations(findings: List[Finding], attribution: Dict) -> List[Dict]:
    """生成建议"""
    recommendations = []
    
    # 基于归因生成建议
    if attribution.get('primary_driver') == 'order':
        recommendations.append({
            "priority": "high",
            "action": "诊断订单下滑原因",
            "details": "分析客流、转化率变化，定位是引流问题还是转化问题",
            "expected_impact": "识别订单下滑根因"
        })
    elif attribution.get('primary_driver') == 'atv':
        recommendations.append({
            "priority": "high",
            "action": "提升客单价策略",
            "details": "优化商品组合、提升连带率、引导高价值商品",
            "expected_impact": "客单价提升10-15%"
        })
    
    # 基于异常生成建议
    for finding in findings:
        if finding.metric == 'new_customer_count':
            recommendations.append({
                "priority": "high",
                "action": "激活新客获取渠道",
                "details": "检查线上推广和线下地推效果，优化引流方案",
                "expected_impact": "新客数恢复至上期水平"
            })
        elif finding.metric == 'attach_qty_ratio':
            recommendations.append({
                "priority": "medium",
                "action": "提升连带销售能力",
                "details": "设计商品组合套餐，培训员工连带销售话术",
                "expected_impact": "连带率提升至1.5+"
            })
    
    return recommendations


def analyze(params: Dict) -> Dict:
    """
    主分析函数
    
    参数:
        subject_type: 'store' 或 'clerk'
        subject_id: 门店ID或导购ID
        subject_name: 名称
        time_window: { from: 'YYYY-MM-DD', to: 'YYYY-MM-DD' }
    """
    subject_type = params.get('subject_type', 'store')
    subject_id = params.get('subject_id')
    subject_name = params.get('subject_name', '')
    time_window = params.get('time_window', {})
    
    if not subject_id:
        return {"status": "error", "message": "缺少 subject_id"}
    
    from_date = time_window.get('from')
    to_date = time_window.get('to')
    
    if not from_date or not to_date:
        return {"status": "error", "message": "缺少时间范围"}
    
    try:
        # 获取数据
        data = fetch_store_data(subject_id, from_date, to_date)
        
        # 解析指标
        metrics = parse_metrics(data)
        
        # 计算归因
        attribution = calculate_attribution(metrics)
        
        # 识别异常
        findings = identify_anomalies(metrics)
        
        # 生成建议
        recommendations = generate_recommendations(findings, attribution)
        
        # 构建输出
        return {
            "status": "ok",
            "subject_type": subject_type,
            "subject_id": subject_id,
            "subject_name": subject_name,
            "analysis_period": {
                "current": {
                    "from": data.get('statFromDate', from_date),
                    "to": data.get('statToDate', to_date)
                },
                "previous": {
                    "from": data.get('compareFromDate', ''),
                    "to": data.get('compareToDate', '')
                }
            },
            "core_metrics": {
                code: {
                    "current": m.current,
                    "previous": m.previous,
                    "change_pct": m.change_pct,
                    "trend": m.trend
                } for code, m in metrics.items()
            },
            "attribution": attribution,
            "findings": [
                {
                    "title": f.title,
                    "type": f.type,
                    "metric": f.metric,
                    "evidence": f.evidence,
                    "confidence": f.confidence,
                    "implication": f.implication
                } for f in findings
            ],
            "recommendations": recommendations
        }
        
    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }


if __name__ == "__main__":
    # 测试
    result = analyze({
        "subject_type": "store",
        "subject_id": "416759_1714379448487",
        "subject_name": "正义路60号店",
        "time_window": {
            "from": "2026-03-01",
            "to": "2026-03-25"
        }
    })
    print(json.dumps(result, indent=2, ensure_ascii=False))
