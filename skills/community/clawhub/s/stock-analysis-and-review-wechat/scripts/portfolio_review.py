#!/usr/bin/env python3
"""
持仓复盘报告生成脚本
支持从JSON格式的持仓数据生成Markdown复盘报告
"""

import json
import sys
from datetime import datetime
from typing import Dict, List

def generate_review_report(
    portfolio: List[Dict], 
    market_summary: Dict,
    news_summary: str = "",
    output_file: str = None
) -> str:
    """
    生成持仓复盘报告
    
    Args:
        portfolio: 持仓列表，每项包含 {code, name, qty, cost, current, target_sell, target_buy}
        market_summary: 大盘数据 {sh_index, sz_index, cy_index, volume}
        news_summary: 消息面摘要
        output_file: 输出文件路径（可选）
    
    Returns:
        str: Markdown格式的复盘报告
    """
    
    today = datetime.now().strftime("%Y-%m-%d")
    
    report_lines = [
        f"# {today} 股票收盘复盘",
        "",
        "## 📊 大盘概览",
        "",
        f"- **上证指数**: {market_summary.get('sh_index', '-')} ({market_summary.get('sh_change', '-')}%)",
        f"- **深证成指**: {market_summary.get('sz_index', '-')} ({market_summary.get('sz_change', '-')}%)",
        f"- **创业板指**: {market_summary.get('cy_index', '-')} ({market_summary.get('cy_change', '-')}%)",
        f"- **成交额**: {market_summary.get('volume', '-')}亿元",
        "",
        "## 💼 持仓盘点",
        "",
        "| 标的 | 数量 | 成本价 | 最新价 | 盈亏 | 收益率 | 状态 |",
        "|------|------|--------|--------|------|--------|------|",
    ]
    
    total_pnl = 0
    total_value = 0
    
    for pos in portfolio:
        qty = pos.get('qty', 0)
        cost = pos.get('cost', 0)
        current = pos.get('current', 0)
        
        pnl = (current - cost) * qty
        pnl_pct = round((current - cost) / cost * 100, 2) if cost > 0 else 0
        value = current * qty
        
        total_pnl += pnl
        total_value += value
        
        # 状态标记
        if pnl_pct >= 15:
            status = "🎯 盈利丰厚"
        elif pnl_pct > 0:
            status = "📈 盈利持有"
        elif pnl_pct >= -3:
            status = "🔄 接近平盘"
        elif pnl_pct >= -5:
            status = "🟡 需要关注"
        else:
            status = "🔴 风险预警"
        
        report_lines.append(
            f"| {pos.get('name', '-')} | {qty} | ¥{cost} | ¥{current} | {'+' if pnl > 0 else ''}¥{round(pnl, 0)} | {'+' if pnl_pct > 0 else ''}{pnl_pct}% | {status} |"
        )
    
    total_return_pct = round(total_pnl / (total_value - total_pnl) * 100, 2) if total_value > total_pnl else 0
    
    report_lines.extend([
        "",
        f"**汇总**: 总市值约 ¥{round(total_value, 0)} | 总盈亏 {'+' if total_pnl > 0 else ''}¥{round(total_pnl, 0)} | 整体收益率 {'+' if total_return_pct > 0 else ''}{total_return_pct}%",
        "",
    ])
    
    # 预警分析
    report_lines.extend([
        "## 🚨 预警分析",
        "",
    ])
    
    alerts = []
    for pos in portfolio:
        qty = pos.get('qty', 0)
        cost = pos.get('cost', 0)
        current = pos.get('current', 0)
        target_sell = pos.get('target_sell')
        target_buy = pos.get('target_buy')
        
        pnl_pct = round((current - cost) / cost * 100, 2) if cost > 0 else 0
        
        # 止盈提醒
        if target_sell and current >= target_sell:
            alerts.append(f"- **🎯 {pos.get('name')} 触及止盈线**: 当前¥{current} >= 目标¥{target_sell}，建议减仓")
        
        # 补仓提醒
        if target_buy and current <= target_buy:
            alerts.append(f"- **🟡 {pos.get('name')} 触及加仓线**: 当前¥{current} <= 目标¥{target_buy}，建议加仓")
        
        # 亏损预警
        if pnl_pct < -10:
            alerts.append(f"- **🔴 {pos.get('name')} 亏损超10%**: 当前亏损{pnl_pct}%，建议评估是否止损")
    
    if alerts:
        report_lines.extend(alerts)
    else:
        report_lines.append("- 暂无预警，持仓正常")
    
    report_lines.append("")
    
    # 消息面
    if news_summary:
        report_lines.extend([
            "## 📰 消息面摘要",
            "",
            news_summary,
            "",
        ])
    
    # 策略建议
    report_lines.extend([
        "## 💡 明日策略建议",
        "",
        "### 持仓管理",
        "- 现有持仓以持有为主，关注预警标的",
        "- 严格按计划执行止盈止损",
        "",
        "### 建仓计划",
        "- 根据市场情况调整建仓节奏",
        "- 分批建仓，控制仓位",
        "",
        "---",
        "",
        f"*报告生成时间: {datetime.now().strftime("%Y-%m-%d %H:%M")}*",
    ])
    
    report = '\n'.join(report_lines)
    
    if output_file:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(report)
        print(f"报告已保存: {output_file}")
    
    return report


if __name__ == "__main__":
    # 示例用法
    example_portfolio = [
        {"code": "sh600919", "name": "江苏银行", "qty": 700, "cost": 8.99, "current": 10.78, "target_sell": 11.50},
        {"code": "sh601398", "name": "工商银行", "qty": 2300, "cost": 7.41, "current": 7.31, "target_buy": 6.80},
    ]
    
    example_market = {
        "sh_index": "4025.15",
        "sh_change": "+0.73",
        "sz_index": "12407.96",
        "sz_change": "+2.58",
        "cy_index": "2127.72",
        "cy_change": "+4.09",
        "volume": "15000",
    }
    
    example_news = """
1. **美联储政策**: 4月维持利率不变概率99.5%，降息或推迟至7月后
2. **地缘政治**: 俄乌停火协议进展，中东局势紧张
3. **贸易战**: 中美关税政策持续，特朗普计划5月访华
"""
    
    report = generate_review_report(example_portfolio, example_market, example_news)
    print(report)
