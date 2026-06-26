#!/usr/bin/env python3
"""
历史基线分析 Skill v1.0
基于Agent API（数据库视图），提供多周期基线+四分位分析

数据源：
- v_gmv_daily_by_store（日粒度）
- v_gmv_weekly_by_store（周粒度）
- v_gmv_monthly_by_store（月粒度）
"""

import sys
import json
import statistics
from datetime import datetime, date, timedelta
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass
from enum import Enum

sys.path.insert(0, '/Users/yangguangwei/.openclaw/workspace-front-door')
from api_client import query_database


class BaselineType(Enum):
    """基线类型"""
    WEEKDAY = "weekday"      # 按星期几分组（周一、周二...）
    WEEK = "week"            # 自然周（周一至周日）
    MONTH = "month"          # 自然月（每月1日到最后1日）


class BaselinePeriod(Enum):
    """基线周期"""
    P13W = "13w"             # 13周（季度）
    P26W = "26w"             # 26周（半年）
    P52W = "52w"             # 52周（全年）
    P12M = "12m"             # 12个月


# 最小数据要求
MIN_SAMPLES = {
    BaselineType.WEEKDAY: 6,    # weekday至少6个样本
    BaselineType.WEEK: 6,       # 周基线至少6周
    BaselineType.MONTH: 6       # 月基线至少6个月
}


@dataclass
class BaselineMetrics:
    """基线指标数据类"""
    count: int               # 样本数
    mean: float              # 平均值
    median: float            # 中位数
    q25: float               # 25分位
    q50: float               # 50分位
    q75: float               # 75分位
    q90: float               # 90分位
    min_val: float           # 最小值
    max_val: float           # 最大值
    std: float               # 标准差
    iqr: float               # 四分位距 (Q75-Q25)
    
    def to_dict(self) -> Dict:
        """转换为字典"""
        return {
            "count": self.count,
            "mean": round(self.mean, 2),
            "median": round(self.median, 2),
            "q25": round(self.q25, 2),
            "q50": round(self.q50, 2),
            "q75": round(self.q75, 2),
            "q90": round(self.q90, 2),
            "min": round(self.min_val, 2),
            "max": round(self.max_val, 2),
            "std": round(self.std, 2),
            "iqr": round(self.iqr, 2)
        }
    
    def get_percentile_rank(self, value: float) -> Dict:
        """获取值所处的分位等级"""
        if value >= self.q90:
            return {"level": "优秀", "percentile": ">90%", "icon": "🟢"}
        elif value >= self.q75:
            return {"level": "良好", "percentile": "75-90%", "icon": "🟢"}
        elif value >= self.q50:
            return {"level": "中等", "percentile": "50-75%", "icon": "🟡"}
        elif value >= self.q25:
            return {"level": "偏低", "percentile": "25-50%", "icon": "🟠"}
        else:
            return {"level": "落后", "percentile": "<25%", "icon": "🔴"}
    
    def is_outlier(self, value: float, factor: float = 1.5) -> Tuple[bool, str]:
        """判断是否为异常值"""
        lower_bound = self.q25 - factor * self.iqr
        upper_bound = self.q75 + factor * self.iqr
        
        if value < lower_bound:
            return True, f"异常偏低（低于{lower_bound:.0f}）"
        elif value > upper_bound:
            return True, f"异常偏高（高于{upper_bound:.0f}）"
        else:
            return False, "正常范围"


def fetch_daily_data(store_id: str, from_date: str, to_date: str) -> List[Dict]:
    """
    获取日粒度历史数据
    
    数据源：v_gmv_daily_by_store
    """
    sql = f"""
        SELECT 
            biz_date,
            weekday_name,
            deal_amount,
            order_count,
            customer_unit_price,
            deal_attach_rate,
            deal_discount
        FROM v_gmv_daily_by_store
        WHERE store_id = '{store_id}'
          AND biz_date BETWEEN '{from_date}' AND '{to_date}'
        ORDER BY biz_date
    """
    
    result = query_database(sql)
    data = []
    
    # 解析结果
    rows = result.get('results', [''])[0].strip().split('\n')
    if len(rows) > 1:
        headers = [h.strip() for h in rows[0].split(',')]
        for row in rows[1:]:
            values = [v.strip() for v in row.split(',')]
            if len(values) == len(headers):
                record = dict(zip(headers, values))
                # 转换数值类型
                record['deal_amount'] = float(record.get('deal_amount', 0))
                record['order_count'] = int(record.get('order_count', 0))
                record['customer_unit_price'] = float(record.get('customer_unit_price', 0))
                record['deal_attach_rate'] = float(record.get('deal_attach_rate', 0))
                data.append(record)
    
    return data


def fetch_weekly_data(store_id: str, from_date: str, to_date: str) -> List[Dict]:
    """
    获取周粒度历史数据
    
    数据源：v_gmv_weekly_by_store
    """
    sql = f"""
        SELECT 
            year_week,
            week_start_date,
            week_end_date,
            deal_amount,
            order_count,
            customer_unit_price,
            deal_attach_rate
        FROM v_gmv_weekly_by_store
        WHERE store_id = '{store_id}'
          AND week_start_date >= '{from_date}'
          AND week_end_date <= '{to_date}'
        ORDER BY year_week
    """
    
    result = query_database(sql)
    # 类似解析逻辑...
    return []


def fetch_monthly_data(store_id: str, from_date: str, to_date: str) -> List[Dict]:
    """
    获取月粒度历史数据
    
    数据源：v_gmv_monthly_by_store
    """
    sql = f"""
        SELECT 
            year_month,
            deal_amount,
            order_count,
            customer_unit_price,
            deal_attach_rate
        FROM v_gmv_monthly_by_store
        WHERE store_id = '{store_id}'
          AND year_month BETWEEN '{from_date[:7]}' AND '{to_date[:7]}'
        ORDER BY year_month
    """
    
    result = query_database(sql)
    # 类似解析逻辑...
    return []


def calculate_baseline(values: List[float]) -> Optional[BaselineMetrics]:
    """
    计算基线指标
    
    Args:
        values: 历史数据列表
        
    Returns:
        BaselineMetrics对象，数据不足返回None
    """
    if not values:
        return None
    
    n = len(values)
    sorted_values = sorted(values)
    
    # 计算四分位
    if n >= 4:
        quantiles = statistics.quantiles(sorted_values, n=4, method='inclusive')
        q25, q50, q75 = quantiles[0], quantiles[1], quantiles[2]
    else:
        q25 = sorted_values[n // 4]
        q50 = statistics.median(sorted_values)
        q75 = sorted_values[3 * n // 4]
    
    # 90分位
    q90 = sorted_values[int(n * 0.9)] if n >= 10 else sorted_values[-1]
    
    return BaselineMetrics(
        count=n,
        mean=statistics.mean(values),
        median=q50,
        q25=q25,
        q50=q50,
        q75=q75,
        q90=q90,
        min_val=min(values),
        max_val=max(values),
        std=statistics.stdev(values) if n > 1 else 0,
        iqr=q75 - q25
    )


def analyze_weekday_baseline(data: List[Dict], metrics: List[str] = None) -> Dict[str, Dict[str, BaselineMetrics]]:
    """
    按星期几分组计算多指标基线
    
    Args:
        data: 日粒度数据列表
        metrics: 分析指标列表，默认["deal_amount", "order_count", "customer_unit_price", "deal_attach_rate"]
        
    Returns:
        {星期几: {指标: BaselineMetrics}}
    """
    if metrics is None:
        metrics = ["deal_amount", "order_count", "customer_unit_price", "deal_attach_rate"]
    
    # 按星期几分组
    weekdays = ["周一", "周二", "周三", "周四", "周五", "周六", "周日"]
    weekday_groups = {wd: {m: [] for m in metrics} for wd in weekdays}
    
    for record in data:
        weekday = record.get('weekday_name', '')
        if weekday in weekday_groups:
            for metric in metrics:
                value = record.get(metric, 0)
                weekday_groups[weekday][metric].append(value)
    
    # 计算每个星期每个指标的基线
    baselines = {}
    for weekday in weekdays:
        baselines[weekday] = {}
        for metric in metrics:
            values = weekday_groups[weekday][metric]
            if len(values) >= MIN_SAMPLES[BaselineType.WEEKDAY]:
                baseline = calculate_baseline(values)
                if baseline:
                    baselines[weekday][metric] = baseline
    
    return baselines


def get_date_range(baseline_type: BaselineType, period: BaselinePeriod, 
                   end_date: str) -> Tuple[str, str]:
    """获取日期范围"""
    end_dt = datetime.strptime(end_date, "%Y-%m-%d")
    
    if period == BaselinePeriod.P13W:
        start_dt = end_dt - timedelta(weeks=13)
    elif period == BaselinePeriod.P26W:
        start_dt = end_dt - timedelta(weeks=26)
    elif period == BaselinePeriod.P52W:
        start_dt = end_dt - timedelta(weeks=52)
    elif period == BaselinePeriod.P12M:
        start_dt = end_dt - timedelta(days=365)
    else:
        start_dt = end_dt - timedelta(weeks=13)
    
    return start_dt.strftime("%Y-%m-%d"), end_date


def analyze(store_id: str, store_name: str = "",
            baseline_type: str = "week",
            period: str = "13w",
            end_date: str = None,
            metrics: List[str] = None) -> Dict:
    """
    基线分析主函数（支持多指标）
    
    Args:
        store_id: 门店ID
        store_name: 门店名称
        baseline_type: 基线类型（weekday/week/month）
        period: 基线周期（13w/26w/52w/12m）
        end_date: 结束日期，默认昨天
        metrics: 分析指标列表，默认["deal_amount", "order_count", "customer_unit_price", "deal_attach_rate"]
    """
    if end_date is None:
        end_date = (date.today() - timedelta(days=1)).strftime("%Y-%m-%d")
    
    if metrics is None:
        metrics = ["deal_amount", "order_count", "customer_unit_price", "deal_attach_rate"]
    
    baseline_type_enum = BaselineType(baseline_type)
    period_enum = BaselinePeriod(period)
    
    # 获取日期范围
    start_date, end_date = get_date_range(baseline_type_enum, period_enum, end_date)
    
    # 获取数据
    if baseline_type_enum == BaselineType.WEEKDAY:
        data = fetch_daily_data(store_id, start_date, end_date)
        if len(data) < MIN_SAMPLES[BaselineType.WEEKDAY]:
            return {
                "status": "error",
                "message": f"数据不足，需要至少{MIN_SAMPLES[BaselineType.WEEKDAY]}天数据，实际{len(data)}天"
            }
        
        # 按星期几分组计算多指标基线
        baselines = analyze_weekday_baseline(data, metrics)
        
        # 格式化输出
        formatted_baselines = {}
        for day, day_baselines in baselines.items():
            formatted_baselines[day] = {
                metric: baseline.to_dict() 
                for metric, baseline in day_baselines.items()
            }
        
        return {
            "status": "ok",
            "store_id": store_id,
            "store_name": store_name,
            "baseline_type": baseline_type,
            "period": period,
            "date_range": {"from": start_date, "to": end_date},
            "metrics": metrics,
            "baselines": formatted_baselines
        }
    
    # TODO: 实现week和month类型
    return {
        "status": "ok",
        "message": f"基线类型 {baseline_type} 分析框架已创建"
    }


def analyze_current_vs_baseline(store_id: str, current_date: str, 
                                 baseline_type: str = "weekday",
                                 period: str = "13w") -> Dict:
    """
    对比当前业绩与基线，分析波动归因
    
    Args:
        store_id: 门店ID
        current_date: 当前日期（分析哪一天）
        baseline_type: 基线类型
        period: 基线周期
        
    Returns:
        波动分析结果
    """
    # 获取当前日期数据
    current_data = fetch_daily_data(store_id, current_date, current_date)
    if not current_data:
        return {"status": "error", "message": f"未找到 {current_date} 的数据"}
    
    current = current_data[0]
    weekday = current.get('weekday_name', '')
    
    # 获取基线
    baseline_result = analyze(
        store_id=store_id,
        baseline_type=baseline_type,
        period=period,
        end_date=current_date,
        metrics=["deal_amount", "order_count", "customer_unit_price", "deal_attach_rate"]
    )
    
    if baseline_result.get("status") != "ok":
        return baseline_result
    
    baselines = baseline_result.get("baselines", {}).get(weekday, {})
    if not baselines:
        return {"status": "error", "message": f"未找到 {weekday} 的基线数据"}
    
    # 对比分析
    findings = []
    
    # 销售额分析
    sales_baseline = baselines.get("deal_amount")
    if sales_baseline:
        current_sales = current.get("deal_amount", 0)
        baseline_sales = sales_baseline["median"]
        sales_change_pct = (current_sales - baseline_sales) / baseline_sales * 100 if baseline_sales else 0
        
        baseline_obj = BaselineMetrics(
            count=sales_baseline["count"],
            mean=sales_baseline["mean"],
            median=sales_baseline["median"],
            q25=sales_baseline["q25"],
            q50=sales_baseline["q50"],
            q75=sales_baseline["q75"],
            q90=sales_baseline["q90"],
            min_val=sales_baseline["min"],
            max_val=sales_baseline["max"],
            std=sales_baseline["std"],
            iqr=sales_baseline["iqr"]
        )
        rank = baseline_obj.get_percentile_rank(current_sales)
        is_outlier, outlier_desc = baseline_obj.is_outlier(current_sales)
        
        findings.append({
            "metric": "销售额",
            "current": current_sales,
            "baseline": baseline_sales,
            "change_pct": round(sales_change_pct, 1),
            "rank": rank,
            "is_outlier": is_outlier,
            "outlier_desc": outlier_desc
        })
        
        # 如果销售额异常，归因到订单数和客单价
        if abs(sales_change_pct) > 10:
            order_baseline = baselines.get("order_count")
            atv_baseline = baselines.get("customer_unit_price")
            
            if order_baseline and atv_baseline:
                current_orders = current.get("order_count", 0)
                current_atv = current.get("customer_unit_price", 0)
                baseline_orders = order_baseline["median"]
                baseline_atv = atv_baseline["median"]
                
                order_change_pct = (current_orders - baseline_orders) / baseline_orders * 100 if baseline_orders else 0
                atv_change_pct = (current_atv - baseline_atv) / baseline_atv * 100 if baseline_atv else 0
                
                # 判断主要驱动因素
                if abs(order_change_pct) > abs(atv_change_pct):
                    primary_driver = "订单数"
                    driver_change = order_change_pct
                else:
                    primary_driver = "客单价"
                    driver_change = atv_change_pct
                
                findings.append({
                    "metric": "归因分析",
                    "primary_driver": primary_driver,
                    "driver_change_pct": round(driver_change, 1),
                    "order_change_pct": round(order_change_pct, 1),
                    "atv_change_pct": round(atv_change_pct, 1)
                })
    
    return {
        "status": "ok",
        "store_id": store_id,
        "current_date": current_date,
        "weekday": weekday,
        "findings": findings
    }


if __name__ == "__main__":
    # 测试基线分析
    print("="*60)
    print("【基线分析测试】")
    result = analyze(
        store_id="416759_1714379448487",
        store_name="正义路60号",
        baseline_type="weekday",
        period="13w",
        end_date="2026-03-25"
    )
    
    # 只打印周一的销售额基线
    if result.get("status") == "ok":
        monday_sales = result.get("baselines", {}).get("周一", {}).get("deal_amount", {})
        print(f"周一销售额基线: 平均¥{monday_sales.get('mean', 0):,.0f}, 中位数¥{monday_sales.get('median', 0):,.0f}")
    
    # 测试波动归因
    print("\n" + "="*60)
    print("【波动归因分析 - 2026-03-25】")
    result = analyze_current_vs_baseline(
        store_id="416759_1714379448487",
        current_date="2026-03-25",
        baseline_type="weekday",
        period="13w"
    )
    
    import json
    print(json.dumps(result, indent=2, ensure_ascii=False))
