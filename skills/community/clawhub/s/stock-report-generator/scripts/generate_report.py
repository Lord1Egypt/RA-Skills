#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
股票复盘报告生成器 - 支持任意A股股票
支持午间复盘和全天复盘两种模式
"""

import os
import sys
from datetime import datetime, timedelta
from typing import Dict, List, Tuple

class StockReportGenerator:
    """股票复盘报告生成器"""
    
    def __init__(self, stock_name: str, stock_code: str):
        self.stock_name = stock_name
        self.stock_code = stock_code
        self.date = datetime.now().strftime("%Y-%m-%d")
        self.time = datetime.now().strftime("%H:%M")
        
    def calculate_scores(self, tech_data: dict, valuation_data: dict, 
                         fundamental_data: dict, capital_data: dict) -> Dict:
        """
        计算多维度评分
        基于A股标准化评分体系
        """
        # 技术面评分（30分）
        trend = tech_data.get("trend", "震荡")  # 上升/震荡/下降
        ma_alignment = tech_data.get("ma_alignment", "纠缠")  # 多头/纠缠/空头
        volume_price = tech_data.get("volume_price", "中性")  # 配合/中性/背离
        
        trend_score = 8 if trend == "上升" else (5 if trend == "震荡" else 2)
        ma_score = 8 if ma_alignment == "多头" else (5 if ma_alignment == "纠缠" else 2)
        vp_score = 8 if volume_price == "配合" else (5 if volume_price == "中性" else 2)
        tech_score = min(30, trend_score + ma_score + vp_score)
        
        # 估值评分（25分）
        pe_percentile = valuation_data.get("pe_percentile", 50)
        pb_percentile = valuation_data.get("pb_percentile", 50)
        dividend_yield = valuation_data.get("dividend_yield", 0)
        
        def get_percentile_score(p):
            if p < 30: return 8
            elif p < 50: return 6
            elif p < 70: return 4
            else: return 2
        
        pe_score = get_percentile_score(pe_percentile)
        pb_score = get_percentile_score(pb_percentile)
        div_score = 5 if dividend_yield > 3 else (4 if dividend_yield > 2 else (3 if dividend_yield > 1 else 1))
        valuation_score = min(25, pe_score + pb_score + div_score)
        
        # 基本面评分（25分）
        growth = fundamental_data.get("revenue_growth", 0)
        roe = fundamental_data.get("roe", 0)
        financial_health = fundamental_data.get("financial_health", "一般")
        
        growth_score = 8 if growth > 30 else (6 if growth > 20 else (4 if growth > 10 else (2 if growth > 0 else 1)))
        roe_score = 8 if roe > 20 else (6 if roe > 15 else (4 if roe > 10 else (2 if roe > 5 else 1)))
        health_score = {"优秀": 5, "良好": 4, "一般": 3, "承压": 1}.get(financial_health, 3)
        fundamental_score = min(25, growth_score + roe_score + health_score)
        
        # 资金面评分（20分）
        main_flow = capital_data.get("main_flow", "中性")  # 流入/中性/流出
        sentiment = capital_data.get("sentiment", "中性")  # 积极/中性/谨慎
        
        flow_score = 8 if main_flow == "流入" else (5 if main_flow == "中性" else 2)
        sentiment_score = 8 if sentiment == "积极" else (5 if sentiment == "中性" else 2)
        capital_score = min(20, flow_score + sentiment_score)
        
        # 综合评分
        total_score = tech_score + valuation_score + fundamental_score + capital_score
        
        # 评级
        if total_score >= 90:
            rating = "A"
            rating_desc = "优秀"
        elif total_score >= 75:
            rating = "B"
            rating_desc = "良好"
        elif total_score >= 60:
            rating = "C"
            rating_desc = "一般"
        else:
            rating = "D"
            rating_desc = "较差"
        
        return {
            "tech": tech_score,
            "valuation": valuation_score,
            "fundamental": fundamental_score,
            "capital": capital_score,
            "total": total_score,
            "rating": rating,
            "rating_desc": rating_desc
        }
    
    def generate_midday_report(self, data: dict) -> str:
        """
        生成午间复盘报告
        """
        report = f"""# {self.stock_name}_午间复盘_{self.date.replace('-', '')}

## {self.stock_name}（{self.stock_code}）午盘分析报告

**报告日期**：{self.date}  
**报告时间**：{self.time}

---

## 一、实时行情

| 指标 | 数值 | 备注 |
|------|------|------|
| 当前价 | {data.get('current_price', '待获取')}元 | {data.get('price_comment', '较昨收涨跌')} |
| 涨跌幅 | {data.get('change_pct', '待获取')}% | {data.get('change_comment', '午盘表现评价')} |
| 今开/最高/最低 | {data.get('open', '--')} / {data.get('high', '--')} / {data.get('low', '--')} | 振幅{data.get('amplitude', '--')}% |
| 成交量 | {data.get('volume', '待获取')}万手 | {data.get('volume_comment', '半日量能评价')} |
| 成交额 | {data.get('turnover', '待获取')}亿元 | {data.get('turnover_comment', '较昨日对比')} |
| 换手率 | {data.get('turnover_rate', '待获取')}% | {data.get('turnover_rate_comment', '交投活跃度')} |
| 量比 | {data.get('volume_ratio', '待获取')} | {data.get('volume_ratio_comment', '量能充足/不足')} |
| 市盈率TTM | {data.get('pe_ttm', '待获取')} | {data.get('pe_comment', '估值位置')} |
| 总市值 | {data.get('market_cap', '待获取')}亿 | {data.get('market_cap_comment', '流通盘情况')} |

**午盘简评**：{data.get('midday_comment', '股价早盘走势描述，半日量能同比变化，市场情绪研判。')}

---

## 二、技术面分析

### 2.1 K线形态与均线系统
- **短期趋势**：{data.get('short_trend', '近5日股价走势描述')}
- **均线系统**：{data.get('ma_system', '股价与5日/10日均线关系')}
- **近期支撑**：{data.get('support', '支撑位价位及依据')}
- **短期压力**：{data.get('resistance', '压力位价位及依据')}

### 2.2 量能分析
- 近5日平均成交额约{data.get('avg_turnover_5d', 'xx')}亿元
- 今日午盘成交额{data.get('turnover', 'xx')}亿元，{data.get('volume_comparison', '对比评价')}
- 换手率{data.get('turnover_rate', 'x')}%处于近期{data.get('turnover_level', '低位/高位')}，{data.get('turnover_comment2', '筹码锁定/活跃度评价')}

### 2.3 技术指标预判
- **MACD**：{data.get('macd', '日线级别状态描述')}
- **KDJ**：{data.get('kdj', 'K/D线位置及信号')}
- **布林带**：{data.get('boll', '股价运行区间')}

---

## 三、基本面速览

### 3.1 估值水平
| 指标 | 当前值 | 评估 |
|------|--------|------|
| 市盈率TTM | {data.get('pe_ttm', 'xx')}倍 | {data.get('pe_eval', '历史分位评价')} |
| 市净率PB | {data.get('pb', 'x.xx')} | {data.get('pb_eval', '相对合理/偏高/偏低')} |
| 股息率TTM | {data.get('dividend', 'x')}% | {data.get('dividend_eval', '吸引力评价')} |

### 3.2 业绩与机构观点
- **ROE（TTM）**：{data.get('roe', 'xx.xx')}，{data.get('roe_eval', '评价')}
- **毛利率/净利率**：{data.get('gross_margin', 'xx.x')}% / {data.get('net_margin', 'xx.x')}%，{data.get('profitability', '盈利质量评价')}
- **近期机构评级**：{data.get('institution_view', '主要观点摘要')}

### 3.3 渠道价格动态
- {data.get('price_dynamics', '终端零售价变动情况')}
- {data.get('competitor_price', '竞品价格对比')}

---

## 四、市场环境

### 4.1 {data.get('sector_name', '所属板块')}板块整体表现
- **板块指数**：{data.get('sector_index', '板块指数涨跌')}
- **个股涨跌**：{data.get('sector_stocks', '板块内个股涨跌分布')}
- **龙头联动**：{data.get('sector_leaders', '主要龙头表现')}

**板块研判**：{data.get('sector_outlook', '板块整体评价')}

### 4.2 大盘与资金面
- **上证指数**：{data.get('sh_index', '点位及涨跌')}
- **主力资金**：{data.get('main_fund', '资金流向')}
- **市场情绪**：{data.get('market_sentiment', '情绪评价')}

---

## 五、午盘操作策略

### 5.1 持仓者建议
- **止盈位**：{data.get('take_profit', '目标价位')}（{data.get('take_profit_reason', '理由')}）
- **止损位**：{data.get('stop_loss', '防守价位')}（{data.get('stop_loss_reason', '理由')}）
- **操作建议**：{data.get('holder_action', '持有/减仓/清仓')}，{data.get('holder_reason', '理由')}

### 5.2 空仓者建议
- **介入时机**：{data.get('entry_condition', '触发条件')}
- **仓位建议**：{data.get('position_suggest', '配置比例')}
- **布局逻辑**：{data.get('entry_logic', '投资理由')}

### 5.3 短线/中线策略区分
| 策略 | 建议 | 理由 |
|------|------|------|
| 短线（1-5天） | {data.get('short_term', '观望/操作')} | {data.get('short_term_reason', '理由说明')} |
| 中线（1-3个月） | {data.get('mid_term', '持有/建仓')} | {data.get('mid_term_reason', '理由说明')} |

---

## 六、关键价位提醒

| 类型 | 价位 | 说明 |
|------|------|------|
| 强压力 | {data.get('strong_resistance', 'xx')}元 | {data.get('strong_resistance_note', '压力位说明')} |
| 压力 | {data.get('resistance', 'xx')}元 | {data.get('resistance_note', '压力位说明')} |
| 当前价 | {data.get('current_price', 'xx')}元 | 午盘运行区间 |
| 支撑 | {data.get('support', 'xx')}元 | {data.get('support_note', '支撑位说明')} |
| 强支撑 | {data.get('strong_support', 'xx')}元 | {data.get('strong_support_note', '支撑位说明')} |
| 止损位 | {data.get('stop_loss', 'xx')}元 | {data.get('stop_loss_note', '止损理由')} |

---

## 七、风险提示

1. **行业风险**：{data.get('sector_risk', '行业特定风险')}
2. **市场风险**：{data.get('market_risk', '大盘系统性风险')}
3. **业绩风险**：{data.get('earnings_risk', '业绩不及预期风险')}
4. **流动性风险**：{data.get('liquidity_risk', '成交量萎缩风险')}

---

**免责声明**：本报告基于公开信息整理，不构成投资建议。股市有风险，投资需谨慎。

**数据来源**：搜狐证券、东方财富、新浪财经等公开市场信息  
**分析师**：哆啦a梦  
**生成时间**：{self.date} {self.time}
"""
        return report
    
    def generate_full_report(self, data: dict, scores: dict) -> str:
        """
        生成全天复盘报告
        """
        report = f"""# {self.stock_name}_全天复盘_{self.date.replace('-', '')}

## {self.stock_name}({self.stock_code}) 全天复盘报告

**报告日期**：{self.date}  
**分析师**：哆啦a梦  
**免责声明**：本报告仅供参考，不构成投资建议。股市有风险，投资需谨慎。

---

## 一、多维度评分体系

### 1.1 综合评分概览

| 维度 | 权重 | 得分 | 评估 |
|------|------|------|------|
| 技术面 | 30% | {scores['tech']}分 | {data.get('tech_eval', '技术面评价')} |
| 估值水平 | 25% | {scores['valuation']}分 | {data.get('valuation_eval', '估值评价')} |
| 基本面 | 25% | {scores['fundamental']}分 | {data.get('fundamental_eval', '基本面评价')} |
| 资金面 | 20% | {scores['capital']}分 | {data.get('capital_eval', '资金面评价')} |
| **综合评分** | **100%** | **{scores['total']}分** | **评级：{scores['rating']}（{scores['rating_desc']}）** |

### 1.2 评分说明
- **技术面（{scores['tech']}分）**：{data.get('tech_detail', '详细说明')}
- **估值水平（{scores['valuation']}分）**：{data.get('valuation_detail', '详细说明')}
- **基本面（{scores['fundamental']}分）**：{data.get('fundamental_detail', '详细说明')}
- **资金面（{scores['capital']}分）**：{data.get('capital_detail', '详细说明')}

---

## 二、全天行情回顾

### 2.1 核心数据

| 指标 | 数值 | 变化 |
|------|------|------|
| 收盘价 | {data.get('close', 'xx')}元 | {data.get('close_change', 'x%')} |
| 开盘价 | {data.get('open', 'xx')}元 | — |
| 最高价 | {data.get('high', 'xx')}元 | — |
| 最低价 | {data.get('low', 'xx')}元 | — |
| 成交额 | {data.get('turnover', 'x')}亿元 | {data.get('turnover_change', '—')} |
| 换手率 | {data.get('turnover_rate', 'x')}% | {data.get('turnover_change2', '缩量/放量')} |
| 市盈率 | {data.get('pe', 'xx')}倍 | — |
| 市净率 | {data.get('pb', 'x')}倍 | — |

### 2.2 日内走势特征
{data.get('intraday_feature', '全天走势描述')}

### 2.3 量能分析
- 今日成交：{data.get('volume', 'x')}万手
- 5日均量：约{data.get('avg_volume_5d', 'xx')}万手
- 量比：约{data.get('volume_ratio', 'x.xx')}，处于近期{data.get('volume_level', '地量/放量')}水平
- **解读**：{data.get('volume_comment', '量能解读')}

---

## 三、技术面深度分析

### 3.1 日K线形态
- **形态**：{data.get('candle_pattern', 'K线描述')}
- **位置**：{data.get('price_position', '股价所处区间位置')}
- **信号**：{data.get('tech_signal', '技术信号解读')}

### 3.2 均线系统

| 均线 | 位置 | 乖离率 | 状态 |
|------|------|--------|------|
| 5日线 | ~{data.get('ma5', 'xx')}元 | {data.get('ma5_bias', 'x')}% | {data.get('ma5_status', '状态')} |
| 10日线 | ~{data.get('ma10', 'xx')}元 | {data.get('ma10_bias', 'x')}% | {data.get('ma10_status', '状态')} |
| 20日线 | ~{data.get('ma20', 'xx')}元 | {data.get('ma20_bias', 'x')}% | {data.get('ma20_status', '状态')} |
| 60日线 | ~{data.get('ma60', 'xx')}元 | {data.get('ma60_bias', 'x')}% | {data.get('ma60_status', '状态')} |

**判断**：{data.get('ma_judgment', '均线系统整体评价')}

### 3.3 关键价位
- **支撑位**：{data.get('support', 'xx')}元（{data.get('support_reason', '理由')}）
- **压力位**：{data.get('resistance', 'xx')}元（{data.get('resistance_reason', '理由')}）
- **突破位**：{data.get('breakout', 'xx')}元（{data.get('breakout_reason', '关键突破价位')}）

### 3.4 趋势判断
- **短期趋势**：{data.get('short_trend', '趋势描述')}
- **中期趋势**：{data.get('mid_trend', '趋势描述')}
- **关键观察**：{data.get('key_observation', '需关注要点')}

---

## 四、基本面跟踪

### 4.1 估值水平

| 指标 | 当前值 | 评估 |
|------|--------|------|
| 市盈率(PE) | {data.get('pe', 'xx')}倍 | {data.get('pe_eval', '估值位置评价')} |
| 市净率(PB) | {data.get('pb', 'x.xx')} | {data.get('pb_eval', '评估')} |
| 行业PE中位数 | {data.get('pe_industry', 'xx')}倍 | {data.get('pe_comparison', '折价/溢价情况')} |
| 机构目标价 | {data.get('target_price', 'xx')}元 | {data.get('upside', '潜在空间')} |

**结论**：{data.get('valuation_conclusion', '估值整体评价')}

### 4.2 业绩回顾（最新财报）
- **主营收入**：{data.get('revenue', 'xxx')}亿元（同比{data.get('revenue_yoy', 'x%')}）
- **归母净利润**：{data.get('net_profit', 'xx')}亿元（同比{data.get('profit_yoy', 'x%')}）
- **单季表现**：{data.get('quarter_performance', '季度数据')}
- **分析**：{data.get('earnings_analysis', '业绩评价')}

### 4.3 机构持仓与评级
- **评级分布**：{data.get('rating_dist', '买入/增持/中性家数')}
- **目标均价**：{data.get('target_avg', 'xx')}元（较当前价有{data.get('upside_potential', 'xx')}%空间）
- **资金面**：{data.get('institution_flow', '机构动向描述')}

---

## 五、市场环境研判

### 5.1 {data.get('sector_name', '所属板块')}板块表现
- **行业特征**：{data.get('sector_feature', '板块整体特征')}
- **龙头对比**：{data.get('sector_comparison', '主要个股表现')}
- **板块动态**：{data.get('sector_dynamics', '近期重要动态')}

### 5.2 大盘走势
- **上证指数**：{data.get('sh_index', '点位及涨跌')}
- **成交额**：{data.get('market_turnover', '两市成交情况')}
- **市场情绪**：{data.get('market_mood', '整体情绪评价')}

### 5.3 资金流向
- **北向资金**：{data.get('northbound', '流向及规模')}
- **主力资金**：{data.get('main_fund_flow', '流向及规模')}
- **{self.stock_name}**：{data.get('stock_fund_flow', '该股票资金流向')}

### 5.4 行业新闻
- **价格动态**：{data.get('price_news', '产品价格变化')}
- **行业趋势**：{data.get('industry_trend', '中长期趋势研判')}

---

## 六、次日及本周策略

### 6.1 短线操作策略（T+1）

| 情景 | 条件 | 操作建议 |
|------|------|----------|
| 情景A | {data.get('scenario_a_condition', '开盘条件')} | {data.get('scenario_a_action', '操作建议')} |
| 情景B | {data.get('scenario_b_condition', '盘中条件')} | {data.get('scenario_b_action', '操作建议')} |
| 情景C | {data.get('scenario_c_condition', '风险条件')} | {data.get('scenario_c_action', '操作建议')} |

### 6.2 本周趋势预判
- **基准情景**（概率{data.get('base_prob', 'xx')}%）：{data.get('base_scenario', '走势预判')}
- **乐观情景**（概率{data.get('bull_prob', 'xx')}%）：{data.get('bull_scenario', '走势预判')}
- **悲观情景**（概率{data.get('bear_prob', 'xx')}%）：{data.get('bear_scenario', '走势预判')}

### 6.3 持仓建议

| 仓位情况 | 建议 |
|----------|------|
| 空仓/轻仓 | {data.get('light_position', '操作建议')} |
| 已有仓位 | {data.get('hold_position', '操作建议')} |
| 重仓 | {data.get('heavy_position', '操作建议')} |

### 6.4 重点观察指标
- **量能变化**：{data.get('watch_volume', '观察要点')}
- **北向资金**：{data.get('watch_northbound', '观察要点')}
- **板块联动**：{data.get('watch_sector', '观察要点')}
- **大盘走向**：{data.get('watch_market', '观察要点')}

---

## 七、风险提示

### 7.1 下行风险因素
- **业绩风险**：{data.get('earnings_risk', '风险描述')}
- **行业风险**：{data.get('industry_risk', '风险描述')}
- **大盘风险**：{data.get('market_risk', '风险描述')}
- **资金风险**：{data.get('fund_risk', '风险描述')}
- **政策风险**：{data.get('policy_risk', '风险描述')}

### 7.2 关键观察节点
- {data.get('node1', '时间节点1')}
- {data.get('node2', '时间节点2')}
- {data.get('node3', '技术节点')}

---

## 八、总结

### 今日点评
{data.get('today_comment', '全天表现简要总结')}

### 核心观点
- **短期**：{data.get('short_view', '观点')}
- **中期**：{data.get('mid_view', '观点')}
- **长期**：{data.get('long_view', '观点')}

### 策略建议
{data.get('strategy_summary', '综合操作建议')}

---

**报告生成时间**：{self.date} {self.time}  
**数据来源**：公开市场数据、东方财富、同花顺等
"""
        return report
    
    def generate_radar_chart(self, scores: dict, output_dir: str) -> str:
        """
        生成评分雷达图
        """
        try:
            import matplotlib.pyplot as plt
            import numpy as np
            
            # 设置中文字体
            plt.rcParams['font.sans-serif'] = ['WenQuanYi Zen Hei', 'SimHei', 'DejaVu Sans']
            plt.rcParams['axes.unicode_minus'] = False
            
            # 数据准备
            categories = ['技术面\n(30%)', '估值水平\n(25%)', '基本面\n(25%)', '资金面\n(20%)']
            values = [
                scores['tech'] / 30 * 100,
                scores['valuation'] / 25 * 100,
                scores['fundamental'] / 25 * 100,
                scores['capital'] / 20 * 100
            ]
            values += values[:1]  # 闭合
            
            # 角度
            angles = np.linspace(0, 2 * np.pi, len(categories), endpoint=False).tolist()
            angles += angles[:1]
            
            # 绘图
            fig, ax = plt.subplots(figsize=(10, 10), subplot_kw=dict(projection='polar'))
            ax.plot(angles, values, 'o-', linewidth=3, color='#2E86AB', markersize=8)
            ax.fill(angles, values, alpha=0.25, color='#2E86AB')
            
            # 添加参考线
            good_line = [80] * len(angles)
            pass_line = [60] * len(angles)
            ax.plot(angles, good_line, '--', linewidth=1.5, color='#4CAF50', alpha=0.7, label='良好线(80)')
            ax.plot(angles, pass_line, '--', linewidth=1.5, color='#FF9800', alpha=0.7, label='及格线(60)')
            
            ax.set_xticks(angles[:-1])
            ax.set_xticklabels(categories, fontsize=14, fontweight='bold')
            ax.set_ylim(0, 100)
            ax.set_yticks([20, 40, 60, 80, 100])
            ax.set_yticklabels(['20', '40', '60', '80', '100'], fontsize=10)
            
            # 标题
            title = f"{self.stock_name} 多维度评分雷达图\n综合评分: {scores['total']}分  评级: {scores['rating']}（{scores['rating_desc']}）"
            ax.set_title(title, fontsize=16, fontweight='bold', pad=30)
            ax.legend(loc='upper right', bbox_to_anchor=(1.3, 1.1), fontsize=11)
            ax.grid(True, linestyle='--', alpha=0.6)
            
            # 保存
            os.makedirs(output_dir, exist_ok=True)
            chart_path = os.path.join(output_dir, f"{self.stock_name}_雷达图_{self.date.replace('-', '')}.png")
            plt.savefig(chart_path, dpi=150, bbox_inches='tight', facecolor='white')
            plt.close()
            
            return chart_path
        except Exception as e:
            print(f"雷达图生成失败: {e}")
            return None
    
    def save_report(self, report: str, report_type: str, output_dir: str = None) -> str:
        """
        保存报告到文件
        """
        if output_dir is None:
            output_dir = os.path.expanduser(f"~/.openclaw/workspace/reports/stock/{self.stock_name}")
        
        os.makedirs(output_dir, exist_ok=True)
        
        date_str = self.date.replace("-", "")
        filename = f"{self.stock_name}_{report_type}_{date_str}.md"
        filepath = os.path.join(output_dir, filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(report)
        
        return filepath


def generate_sample_data(stock_name: str = "示例股票") -> dict:
    """
    生成示例数据（模板格式，实际使用时替换为真实股票数据）
    """
    return {
        # 实时行情 - 需替换为真实数据
        'current_price': '100.00',
        'price_comment': '较昨收涨跌x%',
        'change_pct': '0.00',
        'change_comment': '全天走势评价',
        'open': '99.50',
        'high': '101.20',
        'low': '99.00',
        'amplitude': '2.20',
        'volume': '10.5',
        'volume_comment': '成交量评价',
        'turnover': '10.5',
        'turnover_comment': '成交额对比',
        'turnover_rate': '0.5',
        'turnover_rate_comment': '换手率评价',
        'volume_ratio': '0.8',
        'volume_ratio_comment': '量比水平',
        'pe_ttm': '20.00',
        'pe_comment': '估值位置评价',
        'market_cap': '1000',
        'market_cap_comment': '流通盘情况',
        'midday_comment': '股价早盘走势描述，半日量能同比变化，市场情绪研判。',
        
        # 技术面 - 需替换为真实数据
        'short_trend': '近5日股价走势描述',
        'ma_system': '股价与5日/10日均线关系',
        'support': '支撑位价位及依据',
        'resistance': '压力位价位及依据',
        'avg_turnover_5d': '12',
        'turnover_level': '低位/高位',
        'turnover_comment2': '换手率评价',
        'macd': '日线级别状态描述',
        'kdj': 'K/D线位置及信号',
        'boll': '股价运行区间',
        
        # 基本面 - 需替换为真实数据
        'pb': '2.50',
        'pb_eval': '相对合理/偏高/偏低',
        'dividend': '3.00',
        'dividend_eval': '吸引力评价',
        'roe': '15.00',
        'roe_eval': '评价',
        'gross_margin': '30.0',
        'net_margin': '15.0',
        'profitability': '盈利质量评价',
        'institution_view': '机构观点摘要',
        'price_dynamics': '行业价格动态',
        'competitor_price': '竞品价格对比',
        
        # 市场环境 - 需替换为真实数据
        'sector_name': '所属板块',
        'sector_index': '板块指数涨跌',
        'sector_stocks': '板块内个股涨跌分布',
        'sector_leaders': '主要龙头表现',
        'sector_outlook': '板块整体评价',
        'sh_index': '上证指数点位及涨跌',
        'main_fund': '资金流向',
        'market_sentiment': '情绪评价',
        
        # 操作策略 - 需替换为真实数据
        'take_profit': '目标价位',
        'take_profit_reason': '理由',
        'stop_loss': '防守价位',
        'stop_loss_reason': '理由',
        'holder_action': '持有/减仓/清仓',
        'holder_reason': '理由',
        'entry_condition': '触发条件',
        'position_suggest': '配置比例',
        'entry_logic': '投资理由',
        'short_term': '观望/操作',
        'short_term_reason': '理由说明',
        'mid_term': '持有/建仓',
        'mid_term_reason': '理由说明',
        'strong_resistance': '105',
        'strong_resistance_note': '压力位说明',
        'resistance_note': '压力位说明',
        'support_note': '支撑位说明',
        'strong_support': '95',
        'strong_support_note': '支撑位说明',
        'stop_loss_note': '止损理由',
        
        # 风险提示 - 需替换为真实数据
        'sector_risk': '行业特定风险',
        'market_risk': '大盘系统性风险',
        'earnings_risk': '业绩不及预期风险',
        'liquidity_risk': '成交量萎缩风险',
        
        # 评分说明 - 需替换为真实数据
        'tech_eval': '技术面评价',
        'valuation_eval': '估值评价',
        'fundamental_eval': '基本面评价',
        'capital_eval': '资金面评价',
        'tech_detail': '详细说明',
        'valuation_detail': '详细说明',
        'fundamental_detail': '详细说明',
        'capital_detail': '详细说明',
        
        # 全天复盘专属 - 需替换为真实数据
        'close': '100.00',
        'close_change': '0.00%',
        'intraday_feature': '全天走势描述',
        'avg_volume_5d': '12',
        'volume_comment': '量能解读',
        'candle_pattern': 'K线描述',
        'price_position': '股价所处区间位置',
        'tech_signal': '技术信号解读',
        'ma5': '99.0',
        'ma5_bias': '1.0',
        'ma5_status': '状态',
        'ma10': '98.5',
        'ma10_bias': '1.5',
        'ma10_status': '状态',
        'ma20': '98.0',
        'ma20_bias': '2.0',
        'ma20_status': '状态',
        'ma60': '95.0',
        'ma60_bias': '5.0',
        'ma60_status': '状态',
        'ma_judgment': '均线系统整体评价',
        'resistance_reason': '压力位理由',
        'breakout': '110',
        'breakout_reason': '关键突破价位',
        'short_trend_full': '短期趋势描述',
        'mid_trend_full': '中期趋势描述',
        'key_observation': '需关注要点',
        'pe_eval_full': '估值位置评价',
        'pe_industry': '25.0',
        'pe_comparison': '折价/溢价情况',
        'target_price': '120.00',
        'upside': '20',
        'valuation_conclusion': '估值整体评价',
        'revenue': '100.0',
        'revenue_yoy': '10.0%',
        'net_profit': '20.0',
        'profit_yoy': '10.0%',
        'quarter_performance': '季度数据',
        'earnings_analysis': '业绩评价',
        'rating_dist': '买入/增持/中性家数',
        'target_avg': '120.00',
        'upside_potential': '20',
        'institution_flow': '机构动向描述',
        'sector_feature': '板块整体特征',
        'sector_comparison': '主要个股表现',
        'sector_dynamics': '近期重要动态',
        'market_turnover': '两市成交情况',
        'market_mood': '整体情绪评价',
        'northbound': '北向资金流向',
        'main_fund_flow': '主力资金流向',
        'stock_fund_flow': '该股票资金流向',
        'price_news': '产品价格变化',
        'industry_trend': '中长期趋势研判',
        'scenario_a_condition': '开盘条件',
        'scenario_a_action': '操作建议',
        'scenario_b_condition': '盘中条件',
        'scenario_b_action': '操作建议',
        'scenario_c_condition': '风险条件',
        'scenario_c_action': '操作建议',
        'base_prob': '60',
        'base_scenario': '走势预判',
        'bull_prob': '25',
        'bull_scenario': '走势预判',
        'bear_prob': '15',
        'bear_scenario': '走势预判',
        'light_position': '操作建议',
        'hold_position': '操作建议',
        'heavy_position': '操作建议',
        'watch_volume': '观察要点',
        'watch_northbound': '观察要点',
        'watch_sector': '观察要点',
        'watch_market': '观察要点',
        'earnings_risk_full': '风险描述',
        'industry_risk_full': '风险描述',
        'market_risk_full': '风险描述',
        'fund_risk_full': '风险描述',
        'policy_risk_full': '风险描述',
        'node1': '时间节点1',
        'node2': '时间节点2',
        'node3': '技术节点',
        'today_comment': '全天表现简要总结',
        'short_view': '观点',
        'mid_view': '观点',
        'long_view': '观点',
        'strategy_summary': '综合操作建议',
    }


if __name__ == "__main__":
    # 示例：生成指定股票的复盘报告
    # 使用方式：python generate_report.py <股票名称> <股票代码> <报告类型> [日期]
    # 示例：python generate_report.py 贵州茅台 600519.SH 全天复盘 2026-03-21
    
    import sys
    
    if len(sys.argv) >= 4:
        stock_name = sys.argv[1]
        stock_code = sys.argv[2]
        report_type = sys.argv[3]  # 午间复盘 / 全天复盘
        date = sys.argv[4] if len(sys.argv) > 4 else None
    else:
        # 默认示例
        stock_name = "示例股票"
        stock_code = "000001.SZ"
        report_type = "全天复盘"
        date = None
    
    generator = StockReportGenerator(stock_name, stock_code)
    if date:
        generator.date = date
    
    # 生成示例数据（实际使用时替换为真实数据）
    sample_data = generate_sample_data(stock_name)
    
    # 计算评分（示例参数，实际使用时根据真实数据调整）
    tech_data = {
        "trend": "震荡",
        "ma_alignment": "纠缠",
        "volume_price": "中性"
    }
    valuation_data = {
        "pe_percentile": 30,
        "pb_percentile": 35,
        "dividend_yield": 3.0
    }
    fundamental_data = {
        "revenue_growth": 10.0,
        "roe": 15.0,
        "financial_health": "良好"
    }
    capital_data = {
        "main_flow": "中性",
        "sentiment": "中性"
    }
    
    scores = generator.calculate_scores(tech_data, valuation_data, fundamental_data, capital_data)
    
    print("=" * 50)
    print(f"多维度评分结果 - {stock_name}")
    print("=" * 50)
    print(f"技术面: {scores['tech']}/30")
    print(f"估值水平: {scores['valuation']}/25")
    print(f"基本面: {scores['fundamental']}/25")
    print(f"资金面: {scores['capital']}/20")
    print(f"综合评分: {scores['total']}/100")
    print(f"评级: {scores['rating']}（{scores['rating_desc']}）")
    print("=" * 50)
    
    # 根据报告类型生成对应报告
    if report_type == "午间复盘":
        print(f"\n生成午间复盘报告...")
        report = generator.generate_midday_report(sample_data)
        filepath = generator.save_report(report, "午间复盘")
        print(f"✅ 午间复盘已保存: {filepath}")
    else:
        print(f"\n生成全天复盘报告...")
        report = generator.generate_full_report(sample_data, scores)
        filepath = generator.save_report(report, "全天复盘")
        print(f"✅ 全天复盘已保存: {filepath}")
        
        # 生成雷达图
        print("\n生成评分雷达图...")
        output_dir = os.path.expanduser(f"~/.openclaw/workspace/reports/stock/{stock_name}")
        chart_path = generator.generate_radar_chart(scores, output_dir)
        if chart_path:
            print(f"✅ 雷达图已保存: {chart_path}")
        else:
            print("⚠️ 雷达图生成失败（可能需要安装matplotlib）")
    
    print("\n" + "=" * 50)
    print("报告生成完毕！")
    print("=" * 50)
    print(f"\n使用说明：")
    print(f"  python generate_report.py <股票名称> <股票代码> <报告类型> [日期]")
    print(f"  示例：python generate_report.py 贵州茅台 600519.SH 全天复盘 2026-03-21")
