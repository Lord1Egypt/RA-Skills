#!/usr/bin/env python3
"""
目标追踪分析 Skill v3.0
支持日/周/月多周期追踪，适配不同考核场景
"""

import sys
import json
from pathlib import Path
from datetime import datetime, date, timedelta
from typing import Dict, List, Optional, Any, Tuple
from enum import Enum

sys.path.insert(0, '/Users/yangguangwei/.openclaw/workspace-front-door')
from api_client import get_copilot_data


class TrackingPeriod(Enum):
    """追踪周期类型"""
    DAILY = "daily"      # 日追踪 - 用于每日晨会、实时预警
    WEEKLY = "weekly"    # 周追踪 - 用于周会复盘、周目标
    MONTHLY = "monthly"  # 月追踪 - 用于月度考核、最终达成


# 配置文件路径
DAILY_TARGETS_FILE = Path("~/.openclaw/workspace-store-ops-analyst/targets/daily_targets.json").expanduser()


def load_daily_targets() -> Dict:
    """加载每日目标配置"""
    if DAILY_TARGETS_FILE.exists():
        with open(DAILY_TARGETS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {"stores": {}}


def get_store_info(store_code: str) -> Optional[Dict]:
    """获取门店基本信息"""
    targets = load_daily_targets()
    store_data = targets.get("stores", {}).get(store_code)
    if store_data:
        return {
            "store_code": store_code,
            "store_name": store_data.get("store_name", ""),
            "city": store_data.get("city", "")
        }
    return None


def get_daily_target(store_code: str, date_str: str) -> Optional[float]:
    """获取某日目标"""
    targets = load_daily_targets()
    store_data = targets.get("stores", {}).get(store_code)
    
    if not store_data:
        return None
    
    try:
        dt = datetime.strptime(date_str, "%Y-%m-%d")
        month_key = f"{dt.year}-{dt.month:02d}"
        daily_targets = store_data.get("daily_targets", {}).get(month_key, [])
        
        if dt.day <= len(daily_targets):
            return daily_targets[dt.day - 1]
    except:
        pass
    
    return None


def get_period_target(store_code: str, period_type: TrackingPeriod, 
                      start_date: str, end_date: str) -> Dict:
    """
    获取指定周期的目标
    
    Returns:
        {
            "period_type": "daily/weekly/monthly",
            "start_date": "2026-03-01",
            "end_date": "2026-03-26",
            "days_count": 26,
            "target_amount": 296088.0,
            "daily_breakdown": [...]
        }
    """
    targets = load_daily_targets()
    store_data = targets.get("stores", {}).get(store_code)
    
    if not store_data:
        return {"status": "error", "message": "未找到门店目标配置"}
    
    try:
        start_dt = datetime.strptime(start_date, "%Y-%m-%d")
        end_dt = datetime.strptime(end_date, "%Y-%m-%d")
    except:
        return {"status": "error", "message": "日期格式错误"}
    
    # 收集周期内的每日目标
    daily_breakdown = []
    current_dt = start_dt
    
    while current_dt <= end_dt:
        date_str = current_dt.strftime("%Y-%m-%d")
        month_key = f"{current_dt.year}-{current_dt.month:02d}"
        daily_targets = store_data.get("daily_targets", {}).get(month_key, [])
        
        target = daily_targets[current_dt.day - 1] if current_dt.day <= len(daily_targets) else 0
        
        daily_breakdown.append({
            "date": date_str,
            "weekday": current_dt.weekday(),  # 0=周一, 6=周日
            "target": target
        })
        
        current_dt += timedelta(days=1)
    
    total_target = sum(d["target"] for d in daily_breakdown)
    
    return {
        "status": "ok",
        "store_code": store_code,
        "store_name": store_data.get("store_name", ""),
        "period_type": period_type.value if period_type else "custom",
        "start_date": start_date,
        "end_date": end_date,
        "days_count": len(daily_breakdown),
        "target_amount": total_target,
        "daily_breakdown": daily_breakdown,
        "avg_daily": total_target / len(daily_breakdown) if daily_breakdown else 0
    }


def fetch_actual_data(level: str, code: str = None, parent: str = None, 
                       from_date: str = None, to_date: str = None) -> Dict:
    """
    获取实际业绩数据（支持多层级）
    
    Args:
        level: 层级 (store/region/province/city/group)
        code: 目标代码（门店ID/区域名/省份名/城市名）
        parent: 父级代码（如城市的省份）
        from_date: 开始日期
        to_date: 结束日期
    """
    base_endpoint = '/api/v1/store/overview/bi'
    params = []
    
    if level == "store" and code:
        params.append(f"storeId={code}")
    elif level == "city" and code:
        params.append(f"city={code}")
        if parent:
            params.append(f"province={parent}")
    elif level == "province" and code:
        params.append(f"province={code}")
    elif level == "region" and code:
        params.append(f"region={code}")
    # level == "group" 时不加任何筛选参数
    
    if from_date:
        params.append(f"fromDate={from_date}")
    if to_date:
        params.append(f"toDate={to_date}")
    
    endpoint = base_endpoint
    if params:
        endpoint += "?" + "&".join(params)
    
    return get_copilot_data(endpoint)


def parse_actual_metrics(data: Dict, level: str = "store") -> Dict:
    """
    解析实际业绩指标（支持多层级）
    
    Args:
        data: API返回数据
        level: 层级 (store/region/province/city/group)
    """
    metrics = {}
    
    # 门店级别：使用 metrics 数组
    if level == "store":
        for m in data.get('metrics', []):
            code = m['metricsCode']
            current_val = m['metricsValue']
            if current_val and '(' in str(current_val):
                current_val = str(current_val).split('(')[0]
            metrics[code] = float(current_val) if current_val else 0
        
        if 'effectiveQtyCount' in data:
            metrics['effective_qty_count'] = data['effectiveQtyCount']
        if 'avgDiscount' in data:
            metrics['avg_discount'] = data['avgDiscount']
    
    # 区域/省份/城市/集团级别：使用 overview 对象
    else:
        current = data.get('storesOverviewCurrentPeriod', {})
        previous = data.get('storesOverviewPreviousPeriod', {})
        
        # 本期数据
        metrics['net_money'] = current.get('totalSalesAmount', 0)
        metrics['customer_unit_price'] = current.get('customerUnitPrice', 0)
        metrics['attach_qty_ratio'] = current.get('attachQtyRatio', 0)
        metrics['active_store_count'] = current.get('activeStoreCount', 0)
        
        # 上期数据（用于环比）
        metrics['prev_net_money'] = previous.get('totalSalesAmount', 0)
        metrics['prev_customer_unit_price'] = previous.get('customerUnitPrice', 0)
    
    return metrics


def analyze_period(level: str, code: str, parent: str = None,
                   period_type: TrackingPeriod = None,
                   start_date: str = None, end_date: str = None, 
                   verbose: bool = False) -> Dict:
    """
    分析指定周期的目标达成情况（支持多层级）
    
    Args:
        level: 层级 (store/region/province/city/group)
        code: 目标代码（门店ID/区域名/省份名/城市名）
        parent: 父级代码（可选）
        period_type: 周期类型（日/周/月）
        start_date: 开始日期
        end_date: 结束日期
        verbose: 是否输出日志
    """
    def log(*args, **kwargs):
        if verbose:
            print(*args, **kwargs)
    
    # 获取目标
    target_info = get_period_target(code, period_type, start_date, end_date)
    if target_info.get("status") != "ok":
        return target_info
    
    name = target_info.get("store_name", code)
    
    log(f"{'='*60}")
    log(f"{name} - {period_type.value if period_type else 'custom'}目标追踪")
    log(f"周期: {start_date} 至 {end_date}")
    log(f"{'='*60}")
    
    # 获取实际数据
    log("【获取实际业绩】")
    data = fetch_actual_data(level, code, parent, start_date, end_date)
    
    # 解析实际销售额（支持多层级）
    metrics = parse_actual_metrics(data, level)
    actual_sales = metrics.get('net_money', 0)
    
    log(f"目标: ¥{target_info['target_amount']:,.0f}")
    log(f"实际: ¥{actual_sales:,.2f}")
    
    # 计算达成率
    target_amount = target_info["target_amount"]
    achievement_rate = actual_sales / target_amount if target_amount else 0
    gap = target_amount - actual_sales
    
    # 日均数据
    days_count = target_info["days_count"]
    avg_daily_target = target_info["avg_daily"]
    avg_daily_actual = actual_sales / days_count if days_count else 0
    
    log(f"达成率: {achievement_rate*100:.1f}%")
    log()
    
    # 风险评估（保留黄绿黄灯效果）
    if achievement_rate >= 1.0:
        risk_level = "🟢 正常"
        risk_desc = "已达成目标"
        alert_level = "normal"
    elif achievement_rate >= 0.95:
        risk_level = "🟡 关注"
        risk_desc = "接近目标"
        alert_level = "watch"
    elif achievement_rate >= 0.85:
        risk_level = "🟠 警告"
        risk_desc = "进度偏慢"
        alert_level = "warning"
    elif achievement_rate >= 0.70:
        risk_level = "🔴 告警"
        risk_desc = "明显落后"
        alert_level = "alert"
    else:
        risk_level = "🔴 紧急"
        risk_desc = "严重落后"
        alert_level = "critical"
    
    # 生成建议
    recommendations = []
    if achievement_rate < 0.95:
        gap_pct = (1 - achievement_rate) * 100
        recommendations.append({
            "type": "immediate",
            "action": f"缺口{gap_pct:.1f}%，需日均提升¥{gap/(days_count if period_type == TrackingPeriod.DAILY else 7):,.0f}",
            "priority": "high" if achievement_rate < 0.85 else "medium"
        })
    
    return {
        "status": "ok",
        "store_id": store_id,
        "store_code": store_code,
        "store_name": store_name,
        "period": {
            "type": period_type.value,
            "start_date": start_date,
            "end_date": end_date,
            "days": days_count
        },
        "target": {
            "amount": target_amount,
            "avg_daily": avg_daily_target
        },
        "actual": {
            "sales": actual_sales,
            "avg_daily": avg_daily_actual
        },
        "achievement": {
            "rate": round(achievement_rate, 4),
            "gap": round(gap, 2),
            "status": "achieved" if achievement_rate >= 1.0 else "behind"
        },
        "risk": {
            "level": risk_level,
            "description": risk_desc,
            "alert_level": alert_level  # 用于主动告警
        },
        "recommendations": recommendations
    }


def analyze(store_id: str, store_code: str = None, period: str = "monthly",
            month: str = "2026-03", current_date: str = None, 
            verbose: bool = False) -> Dict:
    """
    统一入口 - 目标追踪分析
    
    Args:
        store_id: 门店ID
        store_code: 门店代码（如"530102063"）
        period: 周期类型 (daily/weekly/monthly)
        month: 月份 (YYYY-MM)
        current_date: 当前日期，默认今天
        verbose: 是否输出日志
    """
    # 门店代码映射
    if not store_code:
        store_code_map = {
            "416759_1714379448487": "530102063",  # 正义路60号
        }
        store_code = store_code_map.get(store_id)
    
    if not store_code:
        return {"status": "error", "message": "需要提供门店代码"}
    
    # 确定日期范围
    if current_date is None:
        current_date = date.today().strftime("%Y-%m-%d")
    
    # 解析周期
    period_type = TrackingPeriod(period) if period in [p.value for p in TrackingPeriod] else TrackingPeriod.MONTHLY
    
    if period_type == TrackingPeriod.DAILY:
        # 日追踪：昨天或今天的达成
        start_date = current_date
        end_date = current_date
        
    elif period_type == TrackingPeriod.WEEKLY:
        # 周追踪：本周一至今天
        dt = datetime.strptime(current_date, "%Y-%m-%d")
        monday = dt - timedelta(days=dt.weekday())
        start_date = monday.strftime("%Y-%m-%d")
        end_date = current_date
        
    else:  # MONTHLY
        # 月追踪：月初至今天
        start_date = f"{month}-01"
        end_date = current_date
    
    return analyze_period(store_id, store_code, period_type, start_date, end_date, verbose)


def format_report(result: Dict) -> str:
    """格式化报告"""
    if result["status"] != "ok":
        return f"错误: {result.get('message', '未知错误')}"
    
    period_type = result["period"]["type"]
    period_label = {"daily": "日", "weekly": "周", "monthly": "月"}.get(period_type, period_type)
    
    report = f"""
{'='*60}
{result['store_name']} - {period_label}度目标追踪
{'='*60}

周期: {result['period']['start_date']} 至 {result['period']['end_date']}
天数: {result['period']['days']}天

📊 目标达成
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
目标: ¥{result['target']['amount']:,.0f}
实际: ¥{result['actual']['sales']:,.2f}
达成率: {result['achievement']['rate']*100:.1f}%

日均目标: ¥{result['target']['avg_daily']:,.0f}
日均实际: ¥{result['actual']['avg_daily']:,.0f}

🚨 风险评估
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
等级: {result['risk']['level']}
评估: {result['risk']['description']}
告警级别: {result['risk']['alert_level']}

{'='*60}
"""
    return report


# 主动告警检查函数（供定时任务调用）
def check_alerts(store_id: str, store_code: str, period: str = "daily", 
                 t_minus: int = 1) -> Optional[Dict]:
    """
    检查是否需要告警（支持T-N数据延迟）
    
    Args:
        store_id: 门店ID
        store_code: 门店代码
        period: 周期类型
        t_minus: 数据延迟天数，默认T-1（昨天数据）
    
    Returns:
        如果需要告警，返回告警信息；否则返回None
    """
    # 计算检查日期（T-N）
    check_date = (date.today() - timedelta(days=t_minus)).strftime("%Y-%m-%d")
    
    result = analyze(store_id, store_code, period, current_date=check_date)
    
    if result.get("status") != "ok":
        return None
    
    alert_level = result.get("risk", {}).get("alert_level", "normal")
    
    # 只有 warning/alert/critical 才触发告警
    if alert_level in ["warning", "alert", "critical"]:
        return {
            "store_id": store_id,
            "store_name": result["store_name"],
            "period": period,
            "alert_level": alert_level,
            "achievement_rate": result["achievement"]["rate"],
            "check_date": check_date,  # T-N日期
            "message": f"【{check_date}数据】{result['store_name']} {period}目标达成率{result['achievement']['rate']*100:.1f}%，{result['risk']['description']}"
        }
    
    return None


def check_alerts_batch(period: str = "daily", t_minus: int = 1) -> List[Dict]:
    """
    批量检查所有门店告警
    
    Returns:
        所有需要告警的门店列表
    """
    alerts = []
    
    # 门店ID映射表（实际应从配置读取）
    store_mappings = {
        "416759_1714379448487": "530102063",  # 正义路60号
        # 其他门店...
    }
    
    for store_id, store_code in store_mappings.items():
        alert = check_alerts(store_id, store_code, period, t_minus)
        if alert:
            alerts.append(alert)
    
    # 按告警级别排序
    priority_order = {"critical": 0, "alert": 1, "warning": 2}
    alerts.sort(key=lambda x: priority_order.get(x["alert_level"], 3))
    
    return alerts


if __name__ == "__main__":
    # 测试三种周期
    print("\n" + "="*70)
    print("【日追踪】")
    result = analyze(
        store_id="416759_1714379448487",
        store_code="530102063",
        period="daily",
        current_date="2026-03-26",
        verbose=True
    )
    print(format_report(result))
    
    print("\n" + "="*70)
    print("【周追踪】")
    result = analyze(
        store_id="416759_1714379448487",
        store_code="530102063",
        period="weekly",
        current_date="2026-03-26",
        verbose=True
    )
    print(format_report(result))
    
    print("\n" + "="*70)
    print("【月追踪】")
    result = analyze(
        store_id="416759_1714379448487",
        store_code="530102063",
        period="monthly",
        current_date="2026-03-26",
        verbose=True
    )
    print(format_report(result))
    
    # 测试告警检查（T-1）
    print("\n" + "="*70)
    print("【告警检查 - T-1】")
    alert = check_alerts("416759_1714379448487", "530102063", "daily", t_minus=1)
    if alert:
        print(f"⚠️ 告警: {alert['message']}")
    else:
        print("✅ 无告警")
    
    # 测试批量告警检查
    print("\n" + "="*70)
    print("【批量告警检查】")
    alerts = check_alerts_batch("daily", t_minus=1)
    if alerts:
        print(f"发现 {len(alerts)} 条告警:")
        for a in alerts:
            print(f"  [{a['alert_level']}] {a['store_name']}: {a['achievement_rate']*100:.1f}%")
    else:
        print("✅ 所有门店正常")
