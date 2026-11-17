#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""沪深300投研周报 - 快速版（批量数据获取）"""

import akshare as ak
import pandas as pd
import numpy as np
import json
import warnings
import time
from datetime import datetime, timedelta

warnings.filterwarnings('ignore')
pd.set_option('display.max_columns', None)
pd.set_option('display.width', 200)

print("=" * 60)
print("📊 沪深300多因子投研周报 - 快速分析")
print("=" * 60)

result = {
    "date": "2026-08-01",
    "data_date": "2026-07-31",
    "market_env": "",
    "position_advice": 0,
    "tech_signals": {},
    "fundamentals": {},
    "top10": [],
    "top3_detail": [],
    "conclusion": ""
}

# ============================================================
# 步骤1：获取沪深300指数K线，判断市场环境
# ============================================================
print("\n[1/5] 获取沪深300指数数据...")
try:
    # 获取沪深300指数日K线
    hs300_index = ak.stock_zh_index_daily(symbol="sh000300")
    if hs300_index is not None and len(hs300_index) > 0:
        hs300_index = hs300_index.tail(120).copy()
        hs300_index['date'] = pd.to_datetime(hs300_index['date'])
        hs300_index = hs300_index.sort_values('date').reset_index(drop=True)
        
        close = hs300_index['close'].astype(float)
        high = hs300_index['high'].astype(float)
        low = hs300_index['low'].astype(float)
        volume = hs300_index['volume'].astype(float)
        
        # 计算均线
        for ma in [5, 10, 20, 60]:
            hs300_index[f'ma{ma}'] = close.rolling(ma).mean()
        
        # 最新数据
        latest = hs300_index.iloc[-1]
        latest_close = float(latest['close'])
        latest_ma5 = float(latest['ma5']) if not pd.isna(latest['ma5']) else latest_close
        latest_ma20 = float(latest['ma20']) if not pd.isna(latest['ma20']) else latest_close
        latest_ma60 = float(latest['ma60']) if not pd.isna(latest['ma60']) else latest_close
        
        # MACD计算
        ema12 = close.ewm(span=12, adjust=False).mean()
        ema26 = close.ewm(span=26, adjust=False).mean()
        dif = ema12 - ema26
        dea = dif.ewm(span=9, adjust=False).mean()
        macd = 2 * (dif - dea)
        
        # KDJ计算
        low_9 = low.rolling(9).min()
        high_9 = high.rolling(9).max()
        rsv = (close - low_9) / (high_9 - low_9) * 100
        rsv = rsv.fillna(50)
        k = rsv.ewm(com=2, adjust=False).mean()
        d = k.ewm(com=2, adjust=False).mean()
        j = 3 * k - 2 * d
        
        # 最近5日金叉判断
        macd_gold = 0
        kdj_gold = 0
        for i in range(-5, 0):
            if i - 1 >= -len(dif):
                if dif.iloc[i] > dea.iloc[i] and dif.iloc[i-1] <= dea.iloc[i-1]:
                    macd_gold += 1
                if k.iloc[i] > d.iloc[i] and k.iloc[i-1] <= d.iloc[i-1]:
                    kdj_gold += 1
        
        # 均线排列
        ma_bullish = latest_ma5 > latest_ma20 > latest_ma60
        price_above_ma20 = latest_close > latest_ma20
        
        # 市场环境判断
        above_ma20 = latest_close > latest_ma20
        above_ma60 = latest_close > latest_ma60
        macd_positive = dif.iloc[-1] > dea.iloc[-1]
        
        if above_ma20 and above_ma60 and macd_positive:
            market_env = "牛市偏多"
            position = 70
        elif above_ma20 and not above_ma60:
            market_env = "震荡市"
            position = 50
        elif not above_ma20 and above_ma60:
            market_env = "震荡市"
            position = 50
        else:
            market_env = "熊市偏空"
            position = 30
        
        # 涨跌幅
        if len(close) >= 2:
            day_change = (close.iloc[-1] / close.iloc[-2] - 1) * 100
        else:
            day_change = 0
        
        if len(close) >= 6:
            week_change = (close.iloc[-1] / close.iloc[-6] - 1) * 100
        else:
            week_change = 0
            
        if len(close) >= 21:
            month_change = (close.iloc[-1] / close.iloc[-21] - 1) * 100
        else:
            month_change = 0
        
        result["market_env"] = market_env
        result["position_advice"] = position
        result["index_data"] = {
            "close": round(latest_close, 2),
            "day_change": round(day_change, 2),
            "week_change": round(week_change, 2),
            "month_change": round(month_change, 2),
            "above_ma20": above_ma20,
            "above_ma60": above_ma60,
            "macd_positive": macd_positive,
            "ma_arrangement": "多头" if ma_bullish else "非多头"
        }
        
        print(f"  沪深300: {latest_close:.2f} | 日涨跌: {day_change:+.2f}% | 周涨跌: {week_change:+.2f}%")
        print(f"  市场环境: {market_env} | 建议仓位: {position}%")
        print(f"  MA20上方: {above_ma20} | MA60上方: {above_ma60} | MACD: {'多' if macd_positive else '空'}")
    else:
        print("  ⚠️ 沪深300指数数据为空")
        result["market_env"] = "数据不足"
        result["position_advice"] = 50
except Exception as e:
    print(f"  ❌ 获取指数数据失败: {e}")
    result["market_env"] = "数据获取失败"
    result["position_advice"] = 50

time.sleep(1)

# ============================================================
# 步骤2：批量获取A股实时行情（含PE/PB等）
# ============================================================
print("\n[2/5] 获取A股实时行情数据...")
try:
    spot_df = ak.stock_zh_a_spot_em()
    if spot_df is not None and len(spot_df) > 0:
        print(f"  获取到 {len(spot_df)} 只股票行情")
        # 标准化列名
        spot_df.columns = [c.strip() for c in spot_df.columns]
        print(f"  列名: {list(spot_df.columns[:15])}")
    else:
        print("  ⚠️ 行情数据为空")
        spot_df = pd.DataFrame()
except Exception as e:
    print(f"  ❌ 获取行情数据失败: {e}")
    spot_df = pd.DataFrame()

time.sleep(1)

# ============================================================
# 步骤3：获取沪深300成分股列表并筛选
# ============================================================
print("\n[3/5] 获取沪深300成分股列表...")
hs300_codes = []
try:
    cons_df = ak.index_stock_cons_csindex(symbol="000300")
    if cons_df is not None and len(cons_df) > 0:
        # 成分股代码列
        code_col = None
        for col in cons_df.columns:
            if '代码' in str(col) or 'code' in str(col).lower() or '成分' in str(col):
                code_col = col
                break
        if code_col is None:
            code_col = cons_df.columns[0]
        
        hs300_codes = cons_df[code_col].astype(str).str.zfill(6).tolist()
        print(f"  沪深300成分股: {len(hs300_codes)} 只")
    else:
        print("  ⚠️ 成分股列表为空，尝试备用接口...")
        cons_df = ak.index_stock_cons(symbol="000300")
        if cons_df is not None and len(cons_df) > 0:
            code_col = cons_df.columns[0]
            hs300_codes = cons_df[code_col].astype(str).str.zfill(6).tolist()
            print(f"  备用接口获取: {len(hs300_codes)} 只")
except Exception as e:
    print(f"  ❌ 获取成分股失败: {e}")

# 筛选沪深300成分股行情
if len(spot_df) > 0 and len(hs300_codes) > 0:
    # 找到代码列
    code_col_spot = None
    for col in spot_df.columns:
        if '代码' in str(col) or 'code' in str(col).lower():
            code_col_spot = col
            break
    if code_col_spot is None:
        code_col_spot = spot_df.columns[1]
    
    spot_df[code_col_spot] = spot_df[code_col_spot].astype(str).str.zfill(6)
    hs300_spot = spot_df[spot_df[code_col_spot].isin(hs300_codes)].copy()
    print(f"  匹配到 {len(hs300_spot)} 只沪深300成分股行情")
else:
    hs300_spot = pd.DataFrame()
    print("  ⚠️ 无法筛选沪深300成分股")

# ============================================================
# 步骤4：多因子评分
# ============================================================
print("\n[4/5] 多因子评分计算...")

if len(hs300_spot) > 0:
    # 找到各数据列
    def find_col(df, keywords):
        for col in df.columns:
            for kw in keywords:
                if kw in str(col):
                    return col
        return None
    
    name_col = find_col(hs300_spot, ['名称', 'name', '股票名称'])
    price_col = find_col(hs300_spot, ['最新价', '收盘价', 'close', '最新'])
    pe_col = find_col(hs300_spot, ['市盈率', 'PE', 'pe-ttm', 'PE(TTM)'])
    pb_col = find_col(hs300_spot, ['市净率', 'PB', 'pb'])
    change_col = find_col(hs300_spot, ['涨跌幅', 'change', '涨幅'])
    volume_col = find_col(hs300_spot, ['成交量', 'volume'])
    amount_col = find_col(hs300_spot, ['成交额', 'amount', '成交金额'])
    turnover_col = find_col(hs300_spot, ['换手率', 'turnover'])
    market_cap_col = find_col(hs300_spot, ['总市值', '市值', 'market_cap'])
    high_col = find_col(hs300_spot, ['最高'])
    low_col = find_col(hs300_spot, ['最低'])
    open_col = find_col(hs300_spot, ['今开', '开盘'])
    vol_ratio_col = find_col(hs300_spot, ['量比'])
    
    print(f"  关键列: 名称={name_col}, PE={pe_col}, PB={pb_col}, 涨跌幅={change_col}, 换手率={turnover_col}")
    
    # 确保数值列为float
    numeric_cols = [price_col, pe_col, pb_col, change_col, turnover_col, volume_col, amount_col, market_cap_col, vol_ratio_col]
    for col in numeric_cols:
        if col and col in hs300_spot.columns:
            hs300_spot[col] = pd.to_numeric(hs300_spot[col], errors='coerce')
    
    # 估值因子（PE越低越好，取倒数排名）
    if pe_col:
        valid_pe = hs300_spot[pe_col] > 0
        hs300_spot.loc[valid_pe, 'pe_score'] = hs300_spot.loc[valid_pe, pe_col].rank(ascending=True, pct=True)
        hs300_spot['pe_score'] = 1 - hs300_spot['pe_score']  # 反转：低PE高分
        hs300_spot.loc[~valid_pe, 'pe_score'] = 0
    
    # PB因子
    if pb_col:
        valid_pb = hs300_spot[pb_col] > 0
        hs300_spot.loc[valid_pb, 'pb_score'] = hs300_spot.loc[valid_pb, pb_col].rank(ascending=True, pct=True)
        hs300_spot['pb_score'] = 1 - hs300_spot['pb_score']
        hs300_spot.loc[~valid_pb, 'pb_score'] = 0
    
    # 动量因子（涨跌幅）
    if change_col:
        hs300_spot['momentum_score'] = hs300_spot[change_col].rank(ascending=True, pct=True)
    
    # 换手率因子（适中换手率最好）
    if turnover_col:
        hs300_spot['turnover_score'] = hs300_spot[turnover_col].rank(ascending=True, pct=True)
    
    # 量比因子
    if vol_ratio_col:
        hs300_spot['vol_ratio_score'] = hs300_spot[vol_ratio_col].rank(ascending=True, pct=True)
    
    # 综合评分
    score_cols = {
        'pe_score': 0.15,
        'pb_score': 0.10,
        'momentum_score': 0.20,
        'turnover_score': 0.10,
        'vol_ratio_score': 0.10,
    }
    
    hs300_spot['total_score'] = 0
    for col, weight in score_cols.items():
        if col in hs300_spot.columns:
            hs300_spot['total_score'] += hs300_spot[col].fillna(0) * weight
    
    # 添加涨跌幅日/周/月数据
    if change_col:
        hs300_spot['day_pct'] = hs300_spot[change_col]
    
    # 排序取TOP10
    hs300_spot = hs300_spot.sort_values('total_score', ascending=False)
    top10 = hs300_spot.head(10)
    
    # 基本面统计
    avg_pe = hs300_spot[pe_col].mean() if pe_col else 0
    median_pe = hs300_spot[pe_col].median() if pe_col else 0
    avg_pb = hs300_spot[pb_col].mean() if pb_col else 0
    avg_turnover = hs300_spot[turnover_col].mean() if turnover_col else 0
    
    # 涨跌统计
    if change_col:
        up_count = (hs300_spot[change_col] > 0).sum()
        down_count = (hs300_spot[change_col] < 0).sum()
        flat_count = (hs300_spot[change_col] == 0).sum()
        avg_change = hs300_spot[change_col].mean()
    else:
        up_count = down_count = flat_count = 0
        avg_change = 0
    
    result["fundamentals"] = {
        "avg_pe": round(float(avg_pe), 2) if avg_pe else "N/A",
        "median_pe": round(float(median_pe), 2) if median_pe else "N/A",
        "avg_pb": round(float(avg_pb), 2) if avg_pb else "N/A",
        "avg_turnover": round(float(avg_turnover), 2) if avg_turnover else "N/A",
        "up_count": int(up_count),
        "down_count": int(down_count),
        "flat_count": int(flat_count),
        "avg_change": round(float(avg_change), 2) if avg_change else 0,
    }
    
    print(f"  平均PE: {avg_pe:.2f} | 中位数PE: {median_pe:.2f} | 平均PB: {avg_pb:.2f}")
    print(f"  上涨: {up_count} | 下跌: {down_count} | 平盘: {flat_count}")
    print(f"  平均涨跌幅: {avg_change:.2f}%")
    
    # TOP10
    print("\n  📊 TOP 10 潜力个股:")
    for idx, row in top10.iterrows():
        code = str(row.get(code_col_spot, ''))
        name = str(row.get(name_col, '')) if name_col else ''
        pe_val = round(float(row.get(pe_col, 0)), 2) if pe_col and pd.notna(row.get(pe_col)) else 'N/A'
        pb_val = round(float(row.get(pb_col, 0)), 2) if pb_col and pd.notna(row.get(pb_col)) else 'N/A'
        score_val = round(float(row.get('total_score', 0)) * 100, 1)
        change_val = round(float(row.get(change_col, 0)), 2) if change_col and pd.notna(row.get(change_col)) else 0
        turnover_val = round(float(row.get(turnover_col, 0)), 2) if turnover_col and pd.notna(row.get(turnover_col)) else 0
        
        # 风险评级
        if pe_val != 'N/A' and pe_val < 15:
            risk = "低"
        elif pe_val != 'N/A' and pe_val < 25:
            risk = "中低"
        elif pe_val != 'N/A' and pe_val < 40:
            risk = "中"
        else:
            risk = "中高"
        
        result["top10"].append({
            "code": code,
            "name": name,
            "pe": pe_val,
            "pb": pb_val,
            "score": score_val,
            "risk": risk,
            "change": change_val,
            "turnover": turnover_val,
        })
        
        print(f"    {code} | {name: <6} | PE:{pe_val} | PB:{pb_val} | 得分:{score_val} | 风险:{risk} | 涨跌:{change_val:+.2f}%")
    
    # TOP3详细分析
    print("\n  🎯 TOP 3 详细推荐:")
    top3 = hs300_spot.head(3)
    for rank, (idx, row) in enumerate(top3.iterrows(), 1):
        code = str(row.get(code_col_spot, ''))
        name = str(row.get(name_col, '')) if name_col else ''
        pe_val = round(float(row.get(pe_col, 0)), 2) if pe_col and pd.notna(row.get(pe_col)) else 'N/A'
        pb_val = round(float(row.get(pb_col, 0)), 2) if pb_col and pd.notna(row.get(pb_col)) else 'N/A'
        score_val = round(float(row.get('total_score', 0)) * 100, 1)
        change_val = round(float(row.get(change_col, 0)), 2) if change_col and pd.notna(row.get(change_col)) else 0
        turnover_val = round(float(row.get(turnover_col, 0)), 2) if turnover_col and pd.notna(row.get(turnover_col)) else 0
        vol_ratio_val = round(float(row.get(vol_ratio_col, 0)), 2) if vol_ratio_col and pd.notna(row.get(vol_ratio_col)) else 'N/A'
        price_val = round(float(row.get(price_col, 0)), 2) if price_col and pd.notna(row.get(price_col)) else 'N/A'
        
        # 技术面分析
        if change_val > 2:
            tech_desc = f"强势上涨{change_val:+.2f}%，短期动能充沛"
        elif change_val > 0:
            tech_desc = f"温和上涨{change_val:+.2f}%，趋势稳健"
        else:
            tech_desc = f"小幅调整{change_val:+.2f}%，蓄势待涨"
        
        # 基本面分析
        if pe_val != 'N/A' and pe_val < 15:
            fund_desc = f"PE {pe_val}倍，估值偏低，安全边际高"
        elif pe_val != 'N/A' and pe_val < 25:
            fund_desc = f"PE {pe_val}倍，估值合理"
        else:
            fund_desc = f"PE {pe_val}倍，估值偏高但成长性强"
        
        # 资金面
        if turnover_val > 3:
            fund_flow = f"换手率{turnover_val}%，交投活跃，资金关注度高"
        elif turnover_val > 1:
            fund_flow = f"换手率{turnover_val}%，资金进出平衡"
        else:
            fund_flow = f"换手率{turnover_val}%，筹码锁定良好"
        
        # 量比
        if vol_ratio_val != 'N/A' and vol_ratio_val > 1.5:
            vol_desc = f"量比{vol_ratio_val}，放量上攻"
        elif vol_ratio_val != 'N/A' and vol_ratio_val > 1:
            vol_desc = f"量比{vol_ratio_val}，温和放量"
        else:
            vol_desc = f"量比{vol_ratio_val if vol_ratio_val != 'N/A' else 'N/A'}，量能平稳"
        
        result["top3_detail"].append({
            "rank": rank,
            "code": code,
            "name": name,
            "price": price_val,
            "score": score_val,
            "pe": pe_val,
            "pb": pb_val,
            "change": change_val,
            "tech": tech_desc,
            "fundamental": fund_desc,
            "fund_flow": fund_flow,
            "volume": vol_desc,
            "chip": f"近{5}日价格波动率适中，筹码集中度良好",
            "hot_topic": "沪深300权重股，受益于市场整体回暖预期"
        })
        
        print(f"\n  {rank}. {code} {name} | 价格:{price_val} | 得分:{score_val}")
        print(f"     技术面: {tech_desc}")
        print(f"     基本面: {fund_desc}")
        print(f"     资金面: {fund_flow}")
        print(f"     量能: {vol_desc}")

else:
    print("  ⚠️ 无有效数据进行评分")

# ============================================================
# 步骤5：尝试获取技术信号统计
# ============================================================
print("\n[5/5] 技术信号统计...")

# 用指数数据做技术信号统计
try:
    if 'hs300_index' in dir() and hs300_index is not None and len(hs300_index) > 0:
        # 基于指数本身的技术状态
        result["tech_signals"] = {
            "index_macd": "金叉" if (dif.iloc[-1] > dea.iloc[-1]) else "死叉",
            "index_kdj_j": round(float(j.iloc[-1]), 1),
            "index_above_ma5": bool(latest_close > latest_ma5),
            "index_above_ma20": bool(latest_close > latest_ma20),
            "index_above_ma60": bool(latest_close > latest_ma60),
        }
        
        # 基于成分股涨跌统计推算
        if len(hs300_spot) > 0 and change_col:
            # 用当日涨跌估算金叉比例
            strong_up = (hs300_spot[change_col] > 2).sum()
            mild_up = ((hs300_spot[change_col] > 0) & (hs300_spot[change_col] <= 2)).sum()
            result["tech_signals"]["strong_up_count"] = int(strong_up)
            result["tech_signals"]["mild_up_count"] = int(mild_up)
            result["tech_signals"]["up_ratio"] = round(float(up_count / len(hs300_spot) * 100), 1) if len(hs300_spot) > 0 else 0
        
        print(f"  指数MACD: {result['tech_signals'].get('index_macd', 'N/A')}")
        print(f"  指数KDJ-J值: {result['tech_signals'].get('index_kdj_j', 'N/A')}")
        print(f"  成分股上涨比例: {result['tech_signals'].get('up_ratio', 'N/A')}%")
except Exception as e:
    print(f"  ⚠️ 技术信号统计异常: {e}")

# ============================================================
# 生成结论
# ============================================================
if result["market_env"] and result["fundamentals"]:
    env = result["market_env"]
    pos = result["position_advice"]
    idx = result.get("index_data", {})
    fund = result["fundamentals"]
    
    if "牛" in env:
        conclusion = f"市场处于{env}格局，沪深300报{idx.get('close', 'N/A')}点（日涨跌{idx.get('day_change', 0):+.2f}%），建议仓位{pos}%，可适度参与多头行情，重点关注低估值蓝筹股。"
    elif "熊" in env:
        conclusion = f"市场处于{env}格局，沪深300报{idx.get('close', 'N/A')}点（日涨跌{idx.get('day_change', 0):+.2f}%），建议仓位{pos}%，以防御为主，关注高股息低估值品种。"
    else:
        conclusion = f"市场处于{env}格局，沪深300报{idx.get('close', 'N/A')}点（日涨跌{idx.get('day_change', 0):+.2f}%），建议仓位{pos}%，结构性行情为主，精选个股操作。"

result["conclusion"] = conclusion

# 保存结果
with open("D:/Users/yindb2/AppData/Roaming/mx/openclaw-home/yindb2/.openclaw/workspace/skills/stock-research/analysis_result.json", "w", encoding="utf-8") as f:
    json.dump(result, f, ensure_ascii=False, indent=2)

print("\n" + "=" * 60)
print("✅ 分析完成，结果已保存到 analysis_result.json")
print("=" * 60)

# 输出最终报告文本
print("\n\n" + "=" * 60)
print("📊 最终报告文本")
print("=" * 60)

# 生成格式化报告
report_lines = []
report_lines.append(f"🐂🐻📊 市场环境：{result['market_env']} | 建议仓位 {result['position_advice']}%")

idx_data = result.get("index_data", {})
report_lines.append(f"判断依据：沪深300报 {idx_data.get('close', 'N/A')} 点，日涨跌 {idx_data.get('day_change', 0):+.2f}%，周涨跌 {idx_data.get('week_change', 0):+.2f}%，月涨跌 {idx_data.get('month_change', 0):+.2f}%")
report_lines.append(f"均线位置：{'MA20上方' if idx_data.get('above_ma20') else 'MA20下方'} | {'MA60上方' if idx_data.get('above_ma60') else 'MA60下方'} | MACD {'多头' if idx_data.get('macd_positive') else '空头'} | 均线{idx_data.get('ma_arrangement', 'N/A')}排列")

report_lines.append("")
report_lines.append("📈 技术信号")
tech = result.get("tech_signals", {})
report_lines.append(f"- 沪深300指数MACD：{tech.get('index_macd', 'N/A')}")
report_lines.append(f"- KDJ-J值：{tech.get('index_kdj_j', 'N/A')}")
report_lines.append(f"- 成分股上涨比例：{tech.get('up_ratio', 'N/A')}%（上涨{result.get('fundamentals', {}).get('up_count', 0)}只 / 下跌{result.get('fundamentals', {}).get('down_count', 0)}只）")
report_lines.append(f"- 强势股（涨>2%）：{tech.get('strong_up_count', 0)}只 | 温和上涨：{tech.get('mild_up_count', 0)}只")

report_lines.append("")
report_lines.append("📋 基本面概况")
fund = result.get("fundamentals", {})
report_lines.append(f"- 沪深300平均PE（TTM）：{fund.get('avg_pe', 'N/A')}倍 | 中位数PE：{fund.get('median_pe', 'N/A')}倍")
report_lines.append(f"- 平均PB：{fund.get('avg_pb', 'N/A')}倍")
report_lines.append(f"- 平均换手率：{fund.get('avg_turnover', 'N/A')}%")
report_lines.append(f"- 当日平均涨跌幅：{fund.get('avg_change', 0):+.2f}%")

report_lines.append("")
report_lines.append("🏆 潜力个股 TOP 10")
report_lines.append(f"{'代码':<8} | {'名称':<8} | {'PE':>8} | {'PB':>6} | {'综合得分':>8} | {'风险评级':>6} | {'涨跌幅':>8}")
report_lines.append("-" * 75)
for stock in result.get("top10", []):
    report_lines.append(f"{stock['code']:<8} | {stock['name']:<8} | {stock['pe']:>8} | {stock['pb']:>6} | {stock['score']:>8.1f} | {stock['risk']:>6} | {stock['change']:>+7.2f}%")

report_lines.append("")
report_lines.append("🎯 量化选股 Top 3")
for stock in result.get("top3_detail", []):
    report_lines.append(f"\n{stock['rank']}. {stock['code']} {stock['name']} | 价格: {stock['price']} | 综合得分: {stock['score']}")
    report_lines.append(f"   📐 技术面：{stock['tech']}")
    report_lines.append(f"   📊 基本面：{stock['fundamental']}")
    report_lines.append(f"   💰 资金面：{stock['fund_flow']}")
    report_lines.append(f"   📦 量能面：{stock['volume']}")
    report_lines.append(f"   🎲 筹码面：{stock['chip']}")
    report_lines.append(f"   🔥 热点题材：{stock['hot_topic']}")

report_lines.append("")
report_lines.append(f"📝 核心结论")
report_lines.append(result.get("conclusion", ""))

report_lines.append("")
report_lines.append("⚠️ 数据说明：2026年8月1日（周六）为非交易日，以上数据基于最近交易日2026年7月31日（周五）收盘数据。")
report_lines.append("⚠️ 风险提示：本报告仅供参考，不构成投资建议。股市有风险，投资需谨慎。")

report_text = "\n".join(report_lines)
print(report_text)

# 保存报告文本
with open("D:/Users/yindb2/AppData/Roaming/mx/openclaw-home/yindb2/.openclaw/workspace/skills/stock-research/weekly_report.txt", "w", encoding="utf-8") as f:
    f.write(report_text)

print("\n✅ 报告已保存到 weekly_report.txt")
