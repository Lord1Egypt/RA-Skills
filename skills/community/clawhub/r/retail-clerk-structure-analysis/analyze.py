#!/usr/bin/env python3
"""
导购结构分析 Skill
分析导购表现结构和导购波动对门店业绩的贡献度
"""

import sys
sys.path.insert(0, '/Users/yangguangwei/.openclaw/workspace-front-door')
from api_client import get_copilot_data
from typing import Dict, List, Any
from dataclasses import dataclass
import math


@dataclass
class ClerkMetrics:
    """导购指标数据类"""
    name: str
    current_sales: float
    prev_sales: float
    current_orders: int
    prev_orders: int
    atv: float
    attach: float
    order_days: int
    
    @property
    def sales_change(self) -> float:
        """销售额变化量"""
        return self.current_sales - self.prev_sales
    
    @property
    def sales_change_pct(self) -> float:
        """销售额变化率"""
        if self.prev_sales > 0:
            return (self.current_sales - self.prev_sales) / self.prev_sales * 100
        return 100 if self.current_sales > 0 else 0
    
    @property
    def order_change(self) -> int:
        """订单数变化量"""
        return self.current_orders - self.prev_orders
    
    @property
    def is_growth(self) -> bool:
        """是否为增长型"""
        return self.sales_change > 0
    
    @property
    def is_decline(self) -> bool:
        """是否为下滑型（变化<-10%）"""
        return self.sales_change_pct < -10


def fetch_clerk_data(store_id: str, from_date: str, to_date: str) -> List[Dict]:
    """获取导购数据"""
    endpoint = f'/api/v1/store/dashboard/bi?storeId={store_id}&fromDate={from_date}&toDate={to_date}'
    return get_copilot_data(endpoint)


def parse_clerk_metrics(clerks_data: List[Dict]) -> List[ClerkMetrics]:
    """解析导购指标"""
    clerks = []
    for clerk in clerks_data:
        name = clerk.get('clerkName', '未知').strip()
        current_sales = clerk.get('saleAmount', 0) or clerk.get('salesAmount', 0)
        current_orders = clerk.get('effectiveOrderCount', 0)
        atv = clerk.get('customerUnitPrice', 0)
        attach = clerk.get('attachQtyRatio', 0)
        order_days = clerk.get('orderDaysCount', 0)
        
        # 上期数据
        prev_data = clerk.get('previous', {})
        prev_sales = prev_data.get('saleAmount', 0) or prev_data.get('salesAmount', 0)
        prev_orders = prev_data.get('effectiveOrderCount', 0)
        
        clerks.append(ClerkMetrics(
            name=name,
            current_sales=current_sales,
            prev_sales=prev_sales,
            current_orders=current_orders,
            prev_orders=prev_orders,
            atv=atv,
            attach=attach,
            order_days=order_days
        ))
    
    return clerks


def calculate_structure_metrics(clerks: List[ClerkMetrics]) -> Dict:
    """计算导购结构指标"""
    if not clerks:
        return {}
    
    total_sales = sum(c.current_sales for c in clerks)
    
    # 按销售额排序
    sorted_by_sales = sorted(clerks, key=lambda x: x.current_sales, reverse=True)
    
    # TOP3 占比
    top3_sales = sum(c.current_sales for c in sorted_by_sales[:3])
    top3_share = top3_sales / total_sales if total_sales else 0
    
    # 尾部3人占比
    bottom3_sales = sum(c.current_sales for c in sorted_by_sales[-3:])
    bottom3_share = bottom3_sales / total_sales if total_sales else 0
    
    # 帕累托分析（20%导购贡献多少业绩）
    clerk_count = len(clerks)
    top_20pct_count = max(1, int(clerk_count * 0.2))
    top_20pct_sales = sum(c.current_sales for c in sorted_by_sales[:top_20pct_count])
    pareto_ratio = top_20pct_sales / total_sales if total_sales else 0
    
    # 人效离散度（变异系数）
    sales_values = [c.current_sales for c in clerks if c.current_sales > 0]
    if len(sales_values) > 1:
        mean_sales = sum(sales_values) / len(sales_values)
        variance = sum((x - mean_sales) ** 2 for x in sales_values) / len(sales_values)
        std_dev = math.sqrt(variance)
        cv = std_dev / mean_sales if mean_sales else 0
    else:
        cv = 0
    
    return {
        "clerk_count": clerk_count,
        "total_sales": total_sales,
        "top3_share": round(top3_share, 3),
        "bottom3_share": round(bottom3_share, 3),
        "pareto_ratio": round(pareto_ratio, 3),
        "efficiency_cv": round(cv, 3),
        "mean_sales": round(sum(sales_values) / len(sales_values), 2) if sales_values else 0
    }


def calculate_contributions(clerks: List[ClerkMetrics], total_change: float) -> List[Dict]:
    """计算各导购对门店业绩变化的贡献度"""
    if total_change == 0:
        return []
    
    contributions = []
    for clerk in clerks:
        contribution_pct = (clerk.sales_change / total_change * 100) if total_change else 0
        contributions.append({
            "name": clerk.name,
            "sales_change": round(clerk.sales_change, 2),
            "change_pct": round(clerk.sales_change_pct, 1),
            "contribution_pct": round(contribution_pct, 1),
            "type": "growth" if clerk.is_growth else "decline" if clerk.is_decline else "stable"
        })
    
    # 按贡献度排序（绝对值）
    contributions.sort(key=lambda x: abs(x["contribution_pct"]), reverse=True)
    return contributions


def identify_key_persons(clerks: List[ClerkMetrics], 
                         selection_mode: str = "cumulative",
                         cumulative_threshold: float = 0.8,
                         top_n: int = 3,
                         min_loss_threshold: float = None) -> Dict:
    """识别关键人 - 基于绝对下滑金额排序
    
    参数:
        selection_mode: 选择模式
            - "cumulative": 累计贡献度达到阈值（如80%）
            - "top_n": 固定取前N名
            - "threshold": 超过最小损失阈值
        cumulative_threshold: 累计贡献度阈值（默认80%）
        top_n: 固定取前N名时的数量
        min_loss_threshold: 最小损失阈值（如10000元）
    """
    if not clerks:
        return {"growth_clerks": [], "decline_clerks": [], "key_contributors": [], "key_drags": []}
    
    # 按销售额变化排序（升序：下滑最多在前）
    sorted_clerks = sorted(clerks, key=lambda x: x.sales_change)
    
    # 增长型/下滑型导购
    growth_clerks = [c for c in clerks if c.sales_change > 0]
    decline_clerks = [c for c in clerks if c.sales_change < 0]
    
    # 计算门店总下滑金额（用于累计贡献度）
    total_decline = sum([c.sales_change for c in decline_clerks])
    
    # 关键拖累者筛选逻辑
    key_drags = []
    
    if selection_mode == "cumulative" and total_decline < 0:
        # 累计贡献度模式：取贡献度达到阈值的前几名
        cumulative_loss = 0
        for c in sorted_clerks:
            if c.sales_change >= 0:  # 只考虑下滑的
                break
            cumulative_loss += c.sales_change
            key_drags.append(c)
            if abs(cumulative_loss / total_decline) >= cumulative_threshold:
                break
    
    elif selection_mode == "threshold" and min_loss_threshold:
        # 阈值模式：下滑超过阈值的
        key_drags = [c for c in sorted_clerks if c.sales_change < -min_loss_threshold]
    
    else:
        # 默认top_n模式
        key_drags = [c for c in sorted_clerks[:top_n] if c.sales_change < 0]
    
    # 关键贡献者：增长最多的（同样用累计贡献度逻辑）
    total_growth = sum([c.sales_change for c in growth_clerks])
    key_contributors = []
    if total_growth > 0:
        cumulative_growth = 0
        for c in sorted(growth_clerks, key=lambda x: x.sales_change, reverse=True):
            cumulative_growth += c.sales_change
            key_contributors.append(c)
            if cumulative_growth / total_growth >= cumulative_threshold:
                break
    
    # 计算累计贡献度
    drag_cumulative = []
    if total_decline < 0:
        cumsum = 0
        for c in key_drags:
            cumsum += c.sales_change
            drag_cumulative.append(abs(cumsum / total_decline))
    
    return {
        "selection_criteria": {
            "mode": selection_mode,
            "cumulative_threshold": cumulative_threshold if selection_mode == "cumulative" else None,
            "top_n": top_n if selection_mode == "top_n" else None,
            "min_loss_threshold": min_loss_threshold if selection_mode == "threshold" else None
        },
        "total_decline": round(total_decline, 2),
        "total_growth": round(total_growth, 2),
        "growth_clerks": [
            {"name": c.name, "sales_change": round(c.sales_change, 2), "change_pct": round(c.sales_change_pct, 1)}
            for c in growth_clerks
        ],
        "decline_clerks": [
            {"name": c.name, "sales_change": round(c.sales_change, 2), "change_pct": round(c.sales_change_pct, 1)}
            for c in decline_clerks
        ],
        "key_contributors": [
            {"name": c.name, "sales_change": round(c.sales_change, 2), "change_pct": round(c.sales_change_pct, 1)}
            for c in key_contributors
        ],
        "key_drags": [
            {"name": c.name, "sales_change": round(c.sales_change, 2), "change_pct": round(c.sales_change_pct, 1)}
            for c in key_drags
        ],
        "drill_down_targets": [
            {
                "rank": i + 1,
                "name": c.name,
                "sales_change": round(c.sales_change, 2),
                "change_pct": round(c.sales_change_pct, 1),
                "cumulative_share": round(drag_cumulative[i] * 100, 1) if i < len(drag_cumulative) else None,
                "current_sales": round(c.current_sales, 2),
                "prev_sales": round(c.prev_sales, 2),
                "current_orders": c.current_orders,
                "prev_orders": c.prev_orders,
                "atv": round(c.atv, 2),
                "attach": round(c.attach, 2)
            }
            for i, c in enumerate(key_drags)
        ]
    }


def generate_findings(structure: Dict, key_persons: Dict, total_change: float) -> List[Dict]:
    """生成诊断发现"""
    findings = []
    
    # 1. 头部集中度
    if structure.get("top3_share", 0) > 0.7:
        findings.append({
            "title": "导购业绩高度集中",
            "type": "anomaly",
            "metric": "top3_share",
            "evidence": f"TOP3导购贡献{structure['top3_share']*100:.1f}%业绩",
            "confidence": "high",
            "implication": "过度依赖少数导购，团队抗风险能力弱"
        })
    
    # 2. 人效差异
    if structure.get("efficiency_cv", 0) > 0.5:
        findings.append({
            "title": "导购人效差异过大",
            "type": "anomaly",
            "metric": "efficiency_cv",
            "evidence": f"人效变异系数{structure['efficiency_cv']:.2f}，团队能力不均衡",
            "confidence": "high",
            "implication": "需要针对性培训提升尾部导购"
        })
    
    # 3. 大面积下滑
    decline_count = len(key_persons.get("decline_clerks", []))
    total_count = structure.get("clerk_count", 0)
    if total_count > 0 and decline_count / total_count > 0.5:
        findings.append({
            "title": "导购大面积业绩下滑",
            "type": "anomaly",
            "metric": "decline_ratio",
            "evidence": f"{decline_count}/{total_count}的导购业绩下滑超10%",
            "confidence": "high",
            "implication": "门店层面存在系统性问题，非个别导购问题"
        })
    
    # 4. 关键拖累者群体（下滑金额最多的）
    drill_down = key_persons.get("drill_down_targets", [])
    if drill_down:
        total_loss = sum([d['sales_change'] for d in drill_down])
        if len(drill_down) == 1:
            d = drill_down[0]
            findings.append({
                "title": f"关键导购{d['name']}业绩下滑最严重",
                "type": "anomaly",
                "metric": "key_drag",
                "evidence": f"{d['name']}业绩下滑{abs(d['sales_change']):.0f}元（{d['change_pct']:.1f}%），建议优先下钻分析",
                "confidence": "high",
                "implication": "需立即访谈了解原因，可能是离职/调岗/状态问题"
            })
        else:
            names = "、".join([d['name'] for d in drill_down])
            findings.append({
                "title": f"{len(drill_down)}名导购业绩下滑最严重，需优先下钻",
                "type": "anomaly",
                "metric": "key_drags",
                "evidence": f"{names}合计下滑{abs(total_loss):.0f}元，占门店总下滑的{abs(total_loss/total_change*100):.1f}%",
                "confidence": "high",
                "implication": f"建议对这{len(drill_down)}名导购做深度下钻分析"
            })
    
    return findings


def analyze(store_id: str, from_date: str, to_date: str, store_name: str = "",
            selection_mode: str = "cumulative",
            cumulative_threshold: float = 0.8,
            top_n: int = 3,
            min_loss_threshold: float = None,
            verbose: bool = False) -> Dict:
    """
    导购结构分析主函数

    参数:
        store_id: 门店ID
        from_date: 分析开始日期 (YYYY-MM-DD)
        to_date: 分析结束日期 (YYYY-MM-DD)
        store_name: 门店名称（可选）
        selection_mode: 选择模式 - "cumulative"/"top_n"/"threshold"
        cumulative_threshold: 累计贡献度阈值 (0-1)，默认0.8
        top_n: 固定取前N名，默认3
        min_loss_threshold: 最小损失阈值（元），threshold模式使用
        verbose: 是否输出详细日志（默认False）
    """
    def log(*args, **kwargs):
        if verbose:
            print(*args, **kwargs)
    
    log("=" * 80)
    log(f"导购结构分析报告 - {store_name or store_id}")
    log(f"分析周期: {from_date} 至 {to_date}")
    log("=" * 80)
    log()
    
    # 获取数据
    log("【第一步：获取导购数据】")
    data = fetch_clerk_data(store_id, from_date, to_date)
    clerks_data = data.get('clerks', [])
    log(f"导购人数: {len(clerks_data)}")
    log()
    
    # 解析指标
    log("【第二步：解析导购指标】")
    clerks = parse_clerk_metrics(clerks_data)
    for c in clerks:
        trend = "↑" if c.is_growth else "↓" if c.is_decline else "→"
        log(f"  {c.name:<10} 本期{c.current_sales:>8.0f}元  上期{c.prev_sales:>8.0f}元  {c.sales_change_pct:>+6.1f}% {trend}")
    log()
    
    # 计算门店总变化
    total_current = sum(c.current_sales for c in clerks)
    total_prev = sum(c.prev_sales for c in clerks)
    total_change = total_current - total_prev
    
    log(f"门店合计: 本期{total_current:.0f}元  上期{total_prev:.0f}元  变化{total_change:+.0f}元 ({total_change/total_prev*100 if total_prev else 0:+.1f}%)")
    log()
    
    # 计算结构指标
    log("【第三步：导购表现结构分析】")
    structure = calculate_structure_metrics(clerks)
    log(f"  导购人数: {structure['clerk_count']}")
    log(f"  人均业绩: {structure['mean_sales']:.0f}元")
    log(f"  TOP3占比: {structure['top3_share']*100:.1f}%")
    log(f"  尾部3人占比: {structure['bottom3_share']*100:.1f}%")
    log(f"  帕累托比率: {structure['pareto_ratio']*100:.1f}% (20%导购贡献)")
    log(f"  人效变异系数: {structure['efficiency_cv']:.2f}")
    log()
    
    # 计算贡献度
    log("【第四步：导购波动归因分析】")
    contributions = calculate_contributions(clerks, total_change)
    log(f"{'导购':<10} {'业绩变化':>12} {'变化率':>10} {'贡献度':>10} {'类型':>8}")
    log("-" * 60)
    for c in contributions:
        type_label = {"growth": "增长", "decline": "下滑", "stable": "稳定"}[c["type"]]
        log(f"{c['name']:<10} {c['sales_change']:>+12.0f} {c['change_pct']:>+9.1f}% {c['contribution_pct']:>+9.1f}% {type_label:>8}")
    log()
    
    # 识别关键人
    log("【第五步：关键人识别 - 基于累计贡献度】")
    key_persons = identify_key_persons(
        clerks,
        selection_mode=selection_mode,
        cumulative_threshold=cumulative_threshold,
        top_n=top_n,
        min_loss_threshold=min_loss_threshold
    )
    
    criteria = key_persons.get("selection_criteria", {})
    mode = criteria.get("mode", "cumulative")
    if mode == "cumulative":
        log(f"  选择标准: 累计贡献度≥{criteria.get('cumulative_threshold', 0.8)*100:.0f}%")
    elif mode == "top_n":
        log(f"  选择标准: 取前{criteria.get('top_n', 3)}名")
    elif mode == "threshold":
        log(f"  选择标准: 损失≥{criteria.get('min_loss_threshold', 0):.0f}元")
    log(f"  门店总下滑: {key_persons.get('total_decline', 0):.0f}元")
    log()

    # 下钻目标
    drill_down = key_persons.get("drill_down_targets", [])
    if drill_down:
        if mode == "cumulative":
            log(f"  下钻目标（累计贡献前{criteria.get('cumulative_threshold', 0.8)*100:.0f}%）:")
        elif mode == "top_n":
            log(f"  下钻目标（前{criteria.get('top_n', 3)}名）:")
        elif mode == "threshold":
            log(f"  下钻目标（损失≥{criteria.get('min_loss_threshold', 0):.0f}元）:")
        log(f"  {'排名':<6} {'导购':<10} {'业绩变化':>12} {'变化率':>10} {'累计占比':>10}")
        log("  " + "-" * 60)
        for d in drill_down:
            cum_share = d.get('cumulative_share', 0)
            cum_str = f"{cum_share:>9.1f}%" if cum_share else "-"
            log(f"  {d['rank']:<6} {d['name']:<10} {d['sales_change']:>+12.0f} {d['change_pct']:>+9.1f}% {cum_str}")
    log()
    
    log(f"  增长型导购: {len(key_persons['growth_clerks'])}人")
    log(f"  下滑型导购: {len(key_persons['decline_clerks'])}人")
    log()
    
    # 生成诊断
    log("【第六步：综合诊断】")
    findings = generate_findings(structure, key_persons, total_change)
    if findings:
        for i, f in enumerate(findings, 1):
            log(f"  {i}. [{f['type'].upper()}] {f['title']}")
            log(f"     证据: {f['evidence']}")
            log(f"     影响: {f['implication']}")
            log()
    else:
        log("  ✓ 未发现明显异常")
    
    log("=" * 80)
    
    return {
        "status": "ok",
        "store_id": store_id,
        "store_name": store_name,
        "analysis_period": {"from": from_date, "to": to_date},
        "structure": structure,
        "contributions": contributions,
        "key_persons": key_persons,
        "findings": findings,
        "total_change": round(total_change, 2)
    }


if __name__ == "__main__":
    result = analyze(
        store_id="416759_1714379448487",
        from_date="2026-03-01",
        to_date="2026-03-25",
        store_name="正义路60号店",
        verbose=True
    )
