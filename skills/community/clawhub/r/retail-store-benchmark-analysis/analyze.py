#!/usr/bin/env python3
"""
门店Benchmark分析 Skill (Store Benchmark Analysis)

与集团/区域其他门店对比，分析门店等级、排名变化、"件单价×连带率"矩阵象限。
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


class ComparisonScope(Enum):
    """对比范围"""
    GROUP = "group"          # 集团全部
    REGION = "region"        # 区域（西南区等）
    PROVINCE = "province"    # 省份
    CITY = "city"            # 城市


@dataclass
class StorePerformance:
    """门店业绩数据类"""
    store_id: str
    store_name: str
    sales: float
    orders: int
    atv: float
    attach_rate: float
    
    @property
    def piece_price(self) -> float:
        """件单价 = 客单价 / 连带率"""
        return self.atv / self.attach_rate if self.attach_rate > 0 else 0
    
    def to_dict(self) -> Dict:
        return {
            "store_id": self.store_id,
            "store_name": self.store_name,
            "sales": round(self.sales, 2),
            "orders": self.orders,
            "atv": round(self.atv, 2),
            "attach_rate": round(self.attach_rate, 2),
            "piece_price": round(self.piece_price, 2)
        }


@dataclass
class RankingResult:
    """排名结果"""
    current_rank: int
    total_stores: int
    percentile: float
    change_from_last: Optional[int] = None  # 环比排名变化
    
    @property
    def tier(self) -> str:
        """门店等级"""
        if self.percentile >= 90:
            return "A+"
        elif self.percentile >= 75:
            return "A"
        elif self.percentile >= 50:
            return "B"
        elif self.percentile >= 25:
            return "C"
        else:
            return "D"
    
    def to_dict(self) -> Dict:
        return {
            "current_rank": self.current_rank,
            "total_stores": self.total_stores,
            "percentile": round(self.percentile, 1),
            "tier": self.tier,
            "change": self.change_from_last
        }


def fetch_stores_performance(scope: ComparisonScope, scope_code: str,
                             from_date: str, to_date: str) -> List[StorePerformance]:
    """
    获取指定范围内所有门店的业绩数据
    
    Args:
        scope: 对比范围
        scope_code: 范围代码（如"昆明"、"西南区"）
        from_date: 开始日期
        to_date: 结束日期
    """
    # 构建WHERE条件
    if scope == ComparisonScope.CITY:
        where_clause = f"city_name = '{scope_code}'"
    elif scope == ComparisonScope.PROVINCE:
        where_clause = f"province_name = '{scope_code}'"
    elif scope == ComparisonScope.REGION:
        # 区域需要通过门店ID关联查询
        where_clause = f"region = '{scope_code}'"
    else:
        where_clause = "1=1"  # 集团全部
    
    sql = f"""
        SELECT 
            store_id,
            store_name,
            SUM(deal_amount) as total_sales,
            SUM(order_count) as total_orders,
            AVG(customer_unit_price) as avg_atv,
            AVG(deal_attach_rate) as avg_attach
        FROM v_gmv_daily_by_store
        WHERE {where_clause}
          AND biz_date BETWEEN '{from_date}' AND '{to_date}'
        GROUP BY store_id, store_name
        HAVING SUM(deal_amount) > 0
        ORDER BY total_sales DESC
    """
    
    result = query_database(sql)
    stores = []
    
    rows = result.get('results', [''])[0].strip().split('\n')
    for row in rows[1:]:  # 跳过header
        cols = row.split(',')
        if len(cols) >= 6:
            stores.append(StorePerformance(
                store_id=cols[0].strip(),
                store_name=cols[1].strip(),
                sales=float(cols[2]),
                orders=int(float(cols[3])),
                atv=float(cols[4]),
                attach_rate=float(cols[5])
            ))
    
    return stores


def calculate_ranking(stores: List[StorePerformance], target_store_id: str,
                     prev_rank: Optional[int] = None) -> Optional[RankingResult]:
    """
    计算门店排名
    
    Args:
        stores: 门店列表（已按销售额排序）
        target_store_id: 目标门店ID
        prev_rank: 上期排名（用于计算环比）
        
    Returns:
        RankingResult
    """
    total = len(stores)
    
    for i, store in enumerate(stores, 1):
        if store.store_id == target_store_id:
            percentile = (total - i) / total * 100
            change = None
            if prev_rank:
                change = prev_rank - i  # 排名上升为正
            
            return RankingResult(
                current_rank=i,
                total_stores=total,
                percentile=percentile,
                change_from_last=change
            )
    
    return None


def analyze_matrix_quadrant(stores: List[StorePerformance], target_store_id: str) -> Dict:
    """
    分析"件单价 × 连带率"矩阵象限
    
    象限划分：
    - Q1: 高件单价 + 高连带率（优质）
    - Q2: 低件单价 + 高连带率（走量型）
    - Q3: 低件单价 + 低连带率（落后）
    - Q4: 高件单价 + 低连带率（精品型）
    """
    # 计算中位数作为分界线
    piece_prices = [s.piece_price for s in stores if s.piece_price > 0]
    attach_rates = [s.attach_rate for s in stores if s.attach_rate > 0]
    
    median_piece = statistics.median(piece_prices) if piece_prices else 0
    median_attach = statistics.median(attach_rates) if attach_rates else 0
    
    # 统计各象限门店数
    quadrants = {"Q1": 0, "Q2": 0, "Q3": 0, "Q4": 0}
    target_quadrant = None
    
    for store in stores:
        pp = store.piece_price
        ar = store.attach_rate
        
        if pp >= median_piece and ar >= median_attach:
            q = "Q1"
        elif pp < median_piece and ar >= median_attach:
            q = "Q2"
        elif pp < median_piece and ar < median_attach:
            q = "Q3"
        else:
            q = "Q4"
        
        quadrants[q] += 1
        
        if store.store_id == target_store_id:
            target_quadrant = q
    
    quadrant_names = {
        "Q1": "高件单价+高连带（优质）",
        "Q2": "低件单价+高连带（走量）",
        "Q3": "低件单价+低连带（落后）",
        "Q4": "高件单价+低连带（精品）"
    }
    
    return {
        "median_piece_price": round(median_piece, 2),
        "median_attach_rate": round(median_attach, 2),
        "quadrants": quadrants,
        "target_quadrant": target_quadrant,
        "target_quadrant_name": quadrant_names.get(target_quadrant, ""),
        "quadrant_distribution": {
            k: f"{v}/{len(stores)} ({v/len(stores)*100:.1f}%)" 
            for k, v in quadrants.items()
        }
    }


def analyze(store_id: str, store_name: str = "",
            scope: str = "city", scope_code: str = "昆明",
            from_date: str = None, to_date: str = None,
            prev_from_date: str = None, prev_to_date: str = None) -> Dict:
    """
    Benchmark分析主函数
    
    Args:
        store_id: 目标门店ID
        store_name: 门店名称
        scope: 对比范围（group/region/province/city）
        scope_code: 范围代码
        from_date: 本期开始日期
        to_date: 本期结束日期
        prev_from_date: 上期开始日期（可选，用于环比）
        prev_to_date: 上期结束日期（可选）
    """
    if from_date is None:
        to_date = (date.today() - timedelta(days=1)).strftime("%Y-%m-%d")
        from_date = (date.today() - timedelta(days=30)).strftime("%Y-%m-%d")
    
    scope_enum = ComparisonScope(scope) if scope in [s.value for s in ComparisonScope] else ComparisonScope.CITY
    
    # 获取本期数据
    current_stores = fetch_stores_performance(scope_enum, scope_code, from_date, to_date)
    
    if not current_stores:
        return {"status": "error", "message": "未获取到门店数据"}
    
    # 计算排名
    ranking = calculate_ranking(current_stores, store_id)
    
    if not ranking:
        return {"status": "error", "message": f"未找到门店 {store_id} 的数据"}
    
    # 获取上期排名（如果提供）
    if prev_from_date and prev_to_date:
        prev_stores = fetch_stores_performance(scope_enum, scope_code, prev_from_date, prev_to_date)
        prev_ranking = calculate_ranking(prev_stores, store_id)
        if prev_ranking:
            ranking.change_from_last = prev_ranking.current_rank - ranking.current_rank
    
    # 矩阵象限分析
    matrix = analyze_matrix_quadrant(current_stores, store_id)
    
    # 获取目标门店详情
    target_store = None
    for s in current_stores:
        if s.store_id == store_id:
            target_store = s
            break
    
    return {
        "status": "ok",
        "store_id": store_id,
        "store_name": store_name or (target_store.store_name if target_store else ""),
        "scope": scope,
        "scope_code": scope_code,
        "period": {"from": from_date, "to": to_date},
        "target_store": target_store.to_dict() if target_store else None,
        "ranking": ranking.to_dict(),
        "matrix": matrix,
        "top_stores": [s.to_dict() for s in current_stores[:5]]  # TOP5
    }


def format_report(result: Dict) -> str:
    """格式化报告"""
    if result["status"] != "ok":
        return f"错误: {result.get('message', '未知错误')}"
    
    report = f"""
{'='*70}
{result['store_name']} - Benchmark分析报告
{'='*70}

对比范围: {result['scope_code']} ({result['scope']})
分析周期: {result['period']['from']} 至 {result['period']['to']}

📊 门店排名
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
当前排名: 第 {result['ranking']['current_rank']} 名 / 共 {result['ranking']['total_stores']} 家
超过门店: {result['ranking']['percentile']:.1f}%
门店等级: {result['ranking']['tier']}
"""
    
    if result['ranking'].get('change'):
        change = result['ranking']['change']
        change_str = f"上升{change}名" if change > 0 else f"下降{abs(change)}名"
        report += f"环比变化: {change_str}\n"
    
    report += f"""

🎯 件单价 × 连带率矩阵
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
分界线:
  件单价中位数: ¥{result['matrix']['median_piece_price']}
  连带率中位数: {result['matrix']['median_attach_rate']}

本店位置: {result['matrix']['target_quadrant']} - {result['matrix']['target_quadrant_name']}

象限分布:
  Q1 (高件单+高连带): {result['matrix']['quadrant_distribution']['Q1']}
  Q2 (低件单+高连带): {result['matrix']['quadrant_distribution']['Q2']}
  Q3 (低件单+低连带): {result['matrix']['quadrant_distribution']['Q3']}
  Q4 (高件单+低连带): {result['matrix']['quadrant_distribution']['Q4']}

🏆 TOP5 门店
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""
    
    for i, store in enumerate(result['top_stores'], 1):
        report += f"{i}. {store['store_name'][:25]:<25} ¥{store['sales']:>10,.0f}\n"
    
    report += f"\n{'='*70}\n"
    return report


if __name__ == "__main__":
    # 测试
    result = analyze(
        store_id="416759_1714379448487",
        store_name="正义路60号",
        scope="city",
        scope_code="昆明",
        from_date="2026-03-01",
        to_date="2026-03-25"
    )
    
    print(format_report(result))
