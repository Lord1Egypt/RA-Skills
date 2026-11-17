#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
量化选股脚本 - 六大维度评分
读取analysis_result.json，进行技术面/基本面/资金面/筹码面/量能/消息面综合评分
输出Top 3推荐
"""

import json
import time
import traceback
import numpy as np
import pandas as pd
from datetime import datetime

print("=" * 60)
print("量化选股脚本 - 六大维度评分")
print(f"运行时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print("=" * 60)

# ============================================================
# 1. 读取分析结果
# ============================================================
print("\n[1/6] 读取分析结果...")
try:
    with open('analysis_result.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    all_stocks = data.get('all_stocks', [])
    top10 = data.get('top10', [])
    market_env = data.get('market_env', {})
    print(f"  读取到 {len(all_stocks)} 只股票数据")
    print(f"  市场环境: {market_env.get('type', '未知')}")
except Exception as e:
    print(f"  读取失败: {e}")
    all_stocks = []
    top10 = []

# 取TOP 30进行深度分析（从top10 + 后续高分股票中选取）
candidates = all_stocks[:30] if len(all_stocks) >= 30 else all_stocks
print(f"  深度分析候选股票: {len(candidates)} 只")

# ============================================================
# 2. 资金面分析 - 获取主力资金流向
# ============================================================
print("\n[2/6] 获取资金面数据...")

import akshare as ak

fund_flow_data = {}
for i, stock in enumerate(candidates):
    code = stock['code']
    market = stock.get('market', 'sh')
    try:
        # 获取个股资金流向
        fund_df = ak.stock_individual_fund_flow(stock=code, market=market)
        if fund_df is not None and len(fund_df) > 0:
            fund_df = fund_df.tail(10)  # 最近10天
            
            # 解析列名
            col_map = {}
            for c in fund_df.columns:
                cl = str(c)
                if '日期' in cl or 'date' in cl.lower():
                    col_map[c] = 'date'
                elif '主力净流入' in cl and '净额' in cl:
                    col_map[c] = 'main_net'
                elif '超大单净流入' in cl and '净额' in cl:
                    col_map[c] = 'super_net'
                elif '大单净流入' in cl and '净额' in cl:
                    col_map[c] = 'big_net'
                elif '中单净流入' in cl and '净额' in cl:
                    col_map[c] = 'mid_net'
                elif '小单净流入' in cl and '净额' in cl:
                    col_map[c] = 'small_net'
            
            fund_df = fund_df.rename(columns=col_map)
            
            main_net_total = 0
            if 'main_net' in fund_df.columns:
                main_net_total = pd.to_numeric(fund_df['main_net'], errors='coerce').sum()
            
            # 近5日主力净流入
            main_net_5d = 0
            if 'main_net' in fund_df.columns:
                main_net_5d = pd.to_numeric(fund_df['main_net'], errors='coerce').tail(5).sum()
            
            fund_flow_data[code] = {
                'main_net_10d': main_net_total,
                'main_net_5d': main_net_5d,
                'has_data': True,
            }
        else:
            fund_flow_data[code] = {'has_data': False}
    except Exception as e:
        fund_flow_data[code] = {'has_data': False, 'error': str(e)}
    
    if (i + 1) % 10 == 0:
        print(f"  已获取 {i+1}/{len(candidates)} 只股票资金流向")
        time.sleep(0.5)

has_fund_data = sum(1 for v in fund_flow_data.values() if v.get('has_data'))
print(f"  资金面数据覆盖: {has_fund_data}/{len(candidates)} 只")

# ============================================================
# 3. 消息面分析 - 尝试pywencai
# ============================================================
print("\n[3/6] 消息面分析...")

hot_topics = {}
try:
    import pywencai
    result = pywencai.get(query="沪深300成分股近期利好消息", query_type="stock")
    if result is not None and isinstance(result, pd.DataFrame) and len(result) > 0:
        print(f"  获取到 {len(result)} 条热点数据")
        for _, row in result.head(30).iterrows():
            code_col = None
            for c in result.columns:
                if '代码' in str(c) or 'code' in str(c).lower():
                    code_col = c
                    break
            if code_col:
                code = str(row[code_col]).zfill(6)
                hot_topics[code] = True
    else:
        print("  pywencai返回数据为空，跳过消息面分析")
except Exception as e:
    print(f"  pywencai查询失败: {e}，跳过消息面分析")

# ============================================================
# 4. 六大维度综合评分
# ============================================================
print("\n[4/6] 六大维度综合评分...")

# 收集数据用于归一化
all_main_net = [v.get('main_net_5d', 0) for v in fund_flow_data.values() if v.get('has_data')]
if all_main_net:
    main_net_max = max(abs(x) for x in all_main_net if x != 0) if any(x != 0 for x in all_main_net) else 1
else:
    main_net_max = 1

quant_results = []

for stock in candidates:
    code = stock['code']
    name = stock['name']
    
    scores_6d = {}
    
    # --- 技术面 30% ---
    tech_score = 0
    # MACD状态
    if stock.get('macd_golden'):
        tech_score += 25
    if stock.get('macd_score', 50) > 70:
        tech_score += 20
    elif stock.get('macd_score', 50) > 50:
        tech_score += 10
    # KDJ状态
    if stock.get('kdj_golden'):
        tech_score += 20
    # 均线排列
    if stock.get('ma_bullish'):
        tech_score += 25
    # 趋势得分
    trend_s = stock.get('trend_score', 50)
    tech_score += trend_s * 0.1  # 最多10分
    
    scores_6d['technical'] = min(100, tech_score)
    
    # --- 基本面 25% ---
    fundamental_score = 50  # 默认中间值
    pe = stock.get('pe')
    pb = stock.get('pb')
    roe = stock.get('approx_roe')
    
    if pe and isinstance(pe, (int, float)) and pe > 0:
        if pe < 15:
            fundamental_score += 20
        elif pe < 25:
            fundamental_score += 10
        elif pe > 100:
            fundamental_score -= 20
        elif pe > 50:
            fundamental_score -= 10
    
    if roe and isinstance(roe, (int, float)):
        if roe > 20:
            fundamental_score += 25
        elif roe > 15:
            fundamental_score += 15
        elif roe > 10:
            fundamental_score += 5
        elif roe < 5:
            fundamental_score -= 15
    
    if pb and isinstance(pb, (int, float)) and pb > 0:
        if pb < 2:
            fundamental_score += 10
        elif pb < 4:
            fundamental_score += 5
        elif pb > 8:
            fundamental_score -= 10
    
    # 动量也加入基本面
    m20 = stock.get('momentum_20', 0)
    if m20 > 5:
        fundamental_score += 10
    elif m20 > 0:
        fundamental_score += 5
    
    scores_6d['fundamental'] = max(0, min(100, fundamental_score))
    
    # --- 资金面 15% ---
    fund_data = fund_flow_data.get(code, {})
    if fund_data.get('has_data'):
        main_net_5d = fund_data.get('main_net_5d', 0)
        # 归一化到0-100
        if main_net_max > 0:
            normalized = main_net_5d / main_net_max
            fund_score = 50 + normalized * 40  # 范围10-90
        else:
            fund_score = 50
    else:
        fund_score = 40  # 无数据略低
    
    scores_6d['fund_flow'] = max(0, min(100, fund_score))
    
    # --- 筹码面 10% ---
    # 用波动率估算筹码集中度：低波动=筹码集中
    volatility = stock.get('volatility', 50)
    if volatility < 20:
        chip_score = 85
    elif volatility < 30:
        chip_score = 70
    elif volatility < 40:
        chip_score = 55
    elif volatility < 50:
        chip_score = 40
    else:
        chip_score = 25
    
    scores_6d['chip'] = chip_score
    
    # --- 成交量震荡 10% ---
    vol_ratio = stock.get('vol_ratio', 1.0)
    turnover = stock.get('avg_turnover', 0)
    
    vol_score = 50
    if 1.0 < vol_ratio < 2.0:
        vol_score = 75  # 温和放量
    elif 0.8 <= vol_ratio <= 1.0:
        vol_score = 55  # 平稳
    elif 2.0 <= vol_ratio < 3.0:
        vol_score = 65  # 较大放量
    elif vol_ratio >= 3.0:
        vol_score = 35  # 过度放量
    else:
        vol_score = 35  # 缩量
    
    scores_6d['volume_volatility'] = vol_score
    
    # --- 消息面 10% ---
    if code in hot_topics:
        news_score = 80
    else:
        news_score = 50  # 无消息给中间分
    
    scores_6d['news'] = news_score
    
    # --- 综合得分 ---
    total_6d = (
        scores_6d['technical'] * 0.30 +
        scores_6d['fundamental'] * 0.25 +
        scores_6d['fund_flow'] * 0.15 +
        scores_6d['chip'] * 0.10 +
        scores_6d['volume_volatility'] * 0.10 +
        scores_6d['news'] * 0.10
    )
    
    quant_results.append({
        'code': code,
        'name': name,
        'scores_6d': scores_6d,
        'total_6d': round(total_6d, 2),
        'close': stock.get('close', 0),
        'pe': stock.get('pe'),
        'pb': stock.get('pb'),
        'approx_roe': stock.get('approx_roe'),
        'momentum_5': stock.get('momentum_5', 0),
        'momentum_20': stock.get('momentum_20', 0),
        'volatility': stock.get('volatility', 0),
        'fund_flow_5d': fund_data.get('main_net_5d', None) if fund_data.get('has_data') else None,
        'in_top10': any(t['code'] == code for t in top10),
        'prev_score': stock.get('total_score', 0),
    })

# 排序取Top 3
quant_results.sort(key=lambda x: x['total_6d'], reverse=True)
top3 = quant_results[:3]

print(f"\n  量化选股 Top 3:")
for i, s in enumerate(top3, 1):
    print(f"  {i}. {s['code']} {s['name']} - 综合得分: {s['total_6d']}")
    print(f"     技术面:{s['scores_6d']['technical']:.1f} 基本面:{s['scores_6d']['fundamental']:.1f} "
          f"资金面:{s['scores_6d']['fund_flow']:.1f} 筹码面:{s['scores_6d']['chip']:.1f} "
          f"量能:{s['scores_6d']['volume_volatility']:.1f} 消息面:{s['scores_6d']['news']:.1f}")

# ============================================================
# 5. 生成详细推荐理由
# ============================================================
print("\n[5/6] 生成推荐理由...")

for stock in top3:
    reasons = []
    
    # 技术面理由
    tech = stock['scores_6d']['technical']
    if tech > 70:
        reasons.append(f"技术面强势({tech:.0f}分)")
        if any(t.get('code') == stock['code'] and t.get('macd_golden') for t in top10):
            reasons.append("MACD金叉")
        if any(t.get('code') == stock['code'] and t.get('ma_bullish') for t in top10):
            reasons.append("均线多头排列")
    elif tech > 50:
        reasons.append(f"技术面中性偏强({tech:.0f}分)")
    else:
        reasons.append(f"技术面偏弱({tech:.0f}分)")
    
    # 基本面理由
    fund = stock['scores_6d']['fundamental']
    pe = stock.get('pe')
    roe = stock.get('approx_roe')
    if fund > 70:
        pe_str = f"PE={pe:.1f}" if pe else "PE未知"
        roe_str = f"ROE≈{roe:.1f}%" if roe else ""
        reasons.append(f"基本面优良({fund:.0f}分, {pe_str}{roe_str})")
    elif fund > 50:
        reasons.append(f"基本面中等({fund:.0f}分)")
    else:
        reasons.append(f"基本面一般({fund:.0f}分)")
    
    # 资金面理由
    ff = stock['scores_6d']['fund_flow']
    ff_val = stock.get('fund_flow_5d')
    if ff_val is not None:
        ff_str = f"近5日主力净流入{ff_val/10000:.2f}万" if abs(ff_val) > 10000 else f"近5日主力净流入{ff_val:.0f}元"
        if ff > 60:
            reasons.append(f"资金面看多({ff:.0f}分, {ff_str})")
        elif ff > 40:
            reasons.append(f"资金面中性({ff:.0f}分)")
        else:
            reasons.append(f"资金面偏空({ff:.0f}分)")
    else:
        reasons.append(f"资金面数据暂缺({ff:.0f}分)")
    
    # 筹码面理由
    chip = stock['scores_6d']['chip']
    vol = stock.get('volatility', 0)
    if chip > 70:
        reasons.append(f"筹码集中({chip:.0f}分, 波动率{vol:.1f}%)")
    elif chip > 50:
        reasons.append(f"筹码较分散({chip:.0f}分)")
    else:
        reasons.append(f"筹码分散({chip:.0f}分)")
    
    # 热点题材
    if stock['code'] in hot_topics:
        reasons.append("近期有热点题材")
    else:
        reasons.append("暂无突出热点题材")
    
    stock['reasons'] = reasons

# ============================================================
# 6. 保存结果
# ============================================================
print("\n[6/6] 保存结果...")

quant_output = {
    'generated_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
    'analysis_date': '2026-07-31',
    'candidates_count': len(candidates),
    'market_env': market_env,
    'top3': [],
    'all_quant_results': [{
        'code': r['code'],
        'name': r['name'],
        'total_6d': r['total_6d'],
        'scores_6d': r['scores_6d'],
    } for r in quant_results[:10]]
}

for stock in top3:
    quant_output['top3'].append({
        'code': stock['code'],
        'name': stock['name'],
        'total_6d': stock['total_6d'],
        'scores_6d': stock['scores_6d'],
        'close': stock['close'],
        'pe': stock.get('pe'),
        'pb': stock.get('pb'),
        'approx_roe': stock.get('approx_roe'),
        'reasons': stock.get('reasons', []),
        'momentum_5': stock.get('momentum_5', 0),
        'momentum_20': stock.get('momentum_20', 0),
    })

with open('quant_result.json', 'w', encoding='utf-8') as f:
    json.dump(quant_output, f, ensure_ascii=False, indent=2)

print(f"\n{'=' * 60}")
print(f"量化选股完成！结果已保存到 quant_result.json")
print(f"{'=' * 60}")
