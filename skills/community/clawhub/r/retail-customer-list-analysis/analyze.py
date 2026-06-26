#!/usr/bin/env python3
"""
客户清单分析 Skill v1.0
基于Shop API客户清单数据，快速查询不同类型客户的数量、试用情况汇总、导购匹配情况
"""

import sys
import json
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from collections import defaultdict

sys.path.insert(0, '/Users/yangguangwei/.openclaw/workspace-front-door')
from api_client import get_shop_data


# 客户类型映射
CUSTOMER_TYPE_MAP = {
    1: "普通客户",
    2: "潜在客户",
    3: "意向客户",
    4: "成交客户"
}


def fetch_customer_list(
    store_id: str,
    from_date: str,
    to_date: str,
    customer_type: Optional[List[int]] = None,
    badge_name: Optional[str] = None,
    page_no: int = 1,
    page_size: int = 100
) -> Dict:
    """
    获取客户清单数据
    
    Args:
        store_id: 门店ID
        from_date: 开始时间 (YYYY-MM-DD HH:mm:ss)
        to_date: 结束时间 (YYYY-MM-DD HH:mm:ss)
        customer_type: 客户类型列表 [1,2,3,4]，None表示全部
        badge_name: 导购姓名，None表示全部
        page_no: 页码
        page_size: 每页数量
    
    Returns:
        API返回数据
    """
    payload = {
        "storeId": store_id,
        "fromDate": from_date,
        "toDate": to_date,
        "pageNo": page_no,
        "pageSize": page_size
    }
    
    if customer_type is not None:
        payload["customerType"] = customer_type
    else:
        payload["customerType"] = []
    
    if badge_name is not None:
        payload["badgeName"] = badge_name
    
    return get_shop_data('/api/v1/customer/list', method='POST', data=payload)


def analyze_customer_types(customers: List[Dict]) -> Dict:
    """
    分析客户类型分布
    """
    type_counts = defaultdict(int)
    type_details = defaultdict(lambda: {
        "count": 0,
        "total_interested": 0,
        "total_trial": 0,
        "total_duration": 0,
        "total_trans_money": 0,
        "total_trans_count": 0
    })
    
    for customer in customers:
        customer_type = customer.get('customerType')
        type_name = CUSTOMER_TYPE_MAP.get(customer_type, f"未知类型({customer_type})")
        
        type_counts[type_name] += 1
        
        # 汇总各类型客户的试用情况
        type_details[type_name]["total_interested"] += customer.get('interestedItems', 0)
        type_details[type_name]["total_trial"] += customer.get('trialItems', 0)
        type_details[type_name]["total_duration"] += customer.get('duration', 0)
        type_details[type_name]["total_trans_money"] += customer.get('transMoney', 0)
        type_details[type_name]["total_trans_count"] += customer.get('transTotal', 0)
    
    total = len(customers)
    result = {}
    
    for type_name in ["普通客户", "潜在客户", "意向客户", "成交客户"]:
        count = type_counts.get(type_name, 0)
        details = type_details[type_name]
        
        result[type_name] = {
            "count": count,
            "percentage": round(count / total * 100, 1) if total > 0 else 0,
            "avg_interested": round(details["total_interested"] / count, 1) if count > 0 else 0,
            "avg_trial": round(details["total_trial"] / count, 1) if count > 0 else 0,
            "avg_duration_minutes": round(details["total_duration"] / count / 60, 1) if count > 0 else 0,
            "avg_trans_money": round(details["total_trans_money"] / count, 2) if count > 0 else 0
        }
    
    return result


def analyze_badge_match(customers: List[Dict]) -> Dict:
    """
    分析导购匹配情况
    """
    clerk_counts = defaultdict(lambda: {"count": 0, "types": defaultdict(int)})
    matched_count = 0
    unmatched_count = 0
    
    for customer in customers:
        badge_name = customer.get('badgeName')
        customer_type = customer.get('customerType')
        type_name = CUSTOMER_TYPE_MAP.get(customer_type, "未知")
        
        if badge_name and badge_name.strip():
            matched_count += 1
            clerk_counts[badge_name]["count"] += 1
            clerk_counts[badge_name]["types"][type_name] += 1
        else:
            unmatched_count += 1
            clerk_counts["未匹配"]["count"] += 1
            clerk_counts["未匹配"]["types"][type_name] += 1
    
    total = len(customers)
    
    # 转换为列表格式，按客户数排序
    clerk_list = []
    for clerk_name, data in sorted(clerk_counts.items(), key=lambda x: x[1]["count"], reverse=True):
        clerk_list.append({
            "badge_name": clerk_name,
            "count": data["count"],
            "types": dict(data["types"])
        })
    
    return {
        "matched": {
            "count": matched_count,
            "percentage": round(matched_count / total * 100, 1) if total > 0 else 0
        },
        "unmatched": {
            "count": unmatched_count,
            "percentage": round(unmatched_count / total * 100, 1) if total > 0 else 0,
            "note": "导购匹配失败，需检查工牌佩戴或系统配置"
        },
        "clerks": clerk_list
    }


def analyze_trial_summary(customers: List[Dict]) -> Dict:
    """
    分析试用情况汇总
    """
    if not customers:
        return {
            "avg_interested_items": 0,
            "avg_trial_items": 0,
            "trial_to_deal_conversion": 0,
            "avg_trans_money": 0
        }
    
    total_interested = sum(c.get('interestedItems', 0) for c in customers)
    total_trial = sum(c.get('trialItems', 0) for c in customers)
    total_trans_money = sum(c.get('transMoney', 0) for c in customers)
    
    # 有试用的客户数
    customers_with_trial = sum(1 for c in customers if c.get('trialItems', 0) > 0)
    
    # 试用后成交的客户数
    customers_trial_to_deal = sum(1 for c in customers if c.get('trialItems', 0) > 0 and c.get('transTotal', 0) > 0)
    
    return {
        "avg_interested_items": round(total_interested / len(customers), 1),
        "avg_trial_items": round(total_trial / len(customers), 1),
        "customers_with_trial": customers_with_trial,
        "trial_to_deal_conversion": round(customers_trial_to_deal / customers_with_trial * 100, 1) if customers_with_trial > 0 else 0,
        "avg_trans_money": round(total_trans_money / len(customers), 2)
    }


def analyze(
    store_id: str,
    from_date: str,
    to_date: str,
    customer_type: Optional[List[int]] = None,
    badge_name: Optional[str] = None,
    store_name: str = ""
) -> Dict:
    """
    主分析函数 - 客户清单分析
    
    Args:
        store_id: 门店ID
        from_date: 开始时间 (YYYY-MM-DD HH:mm:ss)
        to_date: 结束时间 (YYYY-MM-DD HH:mm:ss)
        customer_type: 客户类型列表 [1,2,3,4]，None表示全部
        badge_name: 导购姓名，None表示全部
        store_name: 门店名称（可选）
    
    Returns:
        分析结果字典
    """
    print(f"=" * 70)
    print(f"客户清单分析报告 - {store_name or store_id}")
    print(f"查询周期: {from_date} 至 {to_date}")
    if customer_type:
        type_names = [CUSTOMER_TYPE_MAP.get(t, str(t)) for t in customer_type]
        print(f"客户类型: {', '.join(type_names)}")
    if badge_name:
        print(f"导购筛选: {badge_name}")
    print(f"=" * 70)
    print()
    
    # 获取数据（支持分页，先获取第一页）
    print("【正在获取客户清单数据...】")
    data = fetch_customer_list(store_id, from_date, to_date, customer_type, badge_name, page_no=1, page_size=100)
    
    customers = data.get('list', [])
    page_info = data.get('page', {})
    
    total_count = page_info.get('total', len(customers))
    
    print(f"  总客户数: {total_count}")
    print(f"  当前页: {page_info.get('current', 1)}/{page_info.get('pages', 1)}")
    print()
    
    if not customers:
        return {
            "status": "ok",
            "store_id": store_id,
            "query_period": {"from": from_date, "to": to_date},
            "summary": {
                "total_customers": 0,
                "message": "未找到符合条件的客户数据"
            },
            "customer_list": [],
            "page": page_info
        }
    
    # 分析客户类型分布
    print("【客户类型分布】")
    type_distribution = analyze_customer_types(customers)
    for type_name, info in type_distribution.items():
        if info['count'] > 0:
            print(f"  {type_name}: {info['count']}人 ({info['percentage']}%)")
            print(f"    平均感兴趣商品: {info['avg_interested']}件")
            print(f"    平均试用商品: {info['avg_trial']}件")
            if info['avg_trans_money'] > 0:
                print(f"    平均成交金额: ¥{info['avg_trans_money']}")
    print()
    
    # 分析导购匹配情况
    print("【导购匹配情况】")
    badge_analysis = analyze_badge_match(customers)
    print(f"  已匹配导购: {badge_analysis['matched']['count']}人 ({badge_analysis['matched']['percentage']}%)")
    print(f"  匹配失败: {badge_analysis['unmatched']['count']}人 ({badge_analysis['unmatched']['percentage']}%)")
    if badge_analysis['unmatched']['count'] > 0:
        print(f"    ⚠️ {badge_analysis['unmatched']['note']}")
    print()
    print("  各导购客户数:")
    for clerk in badge_analysis['clerks'][:5]:  # 只显示前5
        types_str = ', '.join([f"{k}:{v}" for k, v in clerk['types'].items()])
        print(f"    {clerk['badge_name']}: {clerk['count']}人 ({types_str})")
    print()
    
    # 试用情况汇总
    print("【试用情况汇总】")
    trial_summary = analyze_trial_summary(customers)
    print(f"  平均感兴趣商品: {trial_summary['avg_interested_items']}件")
    print(f"  平均试用商品: {trial_summary['avg_trial_items']}件")
    print(f"  有试用客户数: {trial_summary['customers_with_trial']}人")
    print(f"  试用后成交转化率: {trial_summary['trial_to_deal_conversion']}%")
    print(f"  平均成交金额: ¥{trial_summary['avg_trans_money']}")
    print()
    
    result = {
        "status": "ok",
        "store_id": store_id,
        "store_name": store_name,
        "query_period": {"from": from_date, "to": to_date},
        "filters": {
            "customer_type": customer_type,
            "badge_name": badge_name
        },
        "summary": {
            "total_customers": total_count,
            "by_type": type_distribution,
            "by_badge": badge_analysis,
            "trial_summary": trial_summary
        },
        "customer_list": customers,
        "page": page_info
    }
    
    return result


def format_report(result: Dict) -> str:
    """格式化报告输出"""
    lines = []
    lines.append("=" * 70)
    lines.append(f"客户清单分析报告")
    lines.append(f"门店: {result.get('store_name', result['store_id'])}")
    lines.append(f"周期: {result['query_period']['from']} 至 {result['query_period']['to']}")
    lines.append("=" * 70)
    lines.append("")
    
    summary = result.get('summary', {})
    
    # 客户类型分布
    lines.append("【客户类型分布】")
    for type_name, info in summary.get('by_type', {}).items():
        if info['count'] > 0:
            lines.append(f"  {type_name}: {info['count']}人 ({info['percentage']}%)")
    lines.append("")
    
    # 导购匹配
    badge = summary.get('by_badge', {})
    lines.append("【导购匹配】")
    lines.append(f"  已匹配: {badge.get('matched', {}).get('count', 0)}人")
    lines.append(f"  未匹配: {badge.get('unmatched', {}).get('count', 0)}人")
    lines.append("")
    
    # 试用汇总
    trial = summary.get('trial_summary', {})
    lines.append("【试用情况】")
    lines.append(f"  平均试用商品: {trial.get('avg_trial_items', 0)}件")
    lines.append(f"  试用后成交转化率: {trial.get('trial_to_deal_conversion', 0)}%")
    lines.append("")
    
    return "\n".join(lines)


if __name__ == "__main__":
    # 测试
    print("客户清单分析 Skill 测试")
    print("=" * 70)
    
    result = analyze(
        store_id="416759_1714379448487",
        from_date="2026-03-25 00:00:00",
        to_date="2026-03-25 23:59:59",
        store_name="正义路60号店"
    )
    
    print("\n" + "=" * 70)
    print("测试完成")
    print(f"状态: {result['status']}")
    print(f"总客户数: {result['summary']['total_customers']}")
