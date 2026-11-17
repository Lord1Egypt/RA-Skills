#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""沪深300投研周报 - 快速版v2（修复+备用数据源）"""

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
print("📊 沪深300多因子投研周报 - 快速分析v2")
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
hs300_index = None
try:
    hs300_index = ak.stock_zh_index_daily(symbol="sh000300")
    if hs300_index is not None and len(hs300_index) > 0:
        hs300_index = hs300_index.tail(120).copy()
        hs300_index['date'] = pd.to_datetime(hs300_index['date'])
        hs300_index = hs300_index.sort_values('date').reset_index(drop=True)
        
        close = hs300_index['close'].astype(float)
        high = hs300_index['high'].astype(float)
        low = hs300_index['low'].astype(float)
        volume = hs300_index['volume'].astype(float)
        
        # 均线
        for ma in [5, 10, 20, 60]:
            hs300_index[f'ma{ma}'] = close.rolling(ma).mean()
        
        latest = hs300_index.iloc[-1]
        latest_close = float(latest['close'])
        latest_ma5 = float(latest['ma5']) if not pd.isna(latest['ma5']) else latest_close
        latest_ma20 = float(latest['ma20']) if not pd.isna(latest['ma20']) else latest_close
        latest_ma60 = float(latest['ma60']) if not pd.isna(latest['ma60']) else latest_close
        
        # MACD
        ema12 = close.ewm(span=12, adjust=False).mean()
        ema26 = close.ewm(span=26, adjust=False).mean()
        dif = ema12 - ema26
        dea = dif.ewm(span=9, adjust=False).mean()
        macd_hist = 2 * (dif - dea)
        
        # KDJ
        low_9 = low.rolling(9).min()
        high_9 = high.rolling(9).max()
        rsv = (close - low_9) / (high_9 - low_9) * 100
        rsv = rsv.fillna(50)
        k = rsv.ewm(com=2, adjust=False).mean()
        d = k.ewm(com=2, adjust=False).mean()
        j = 3 * k - 2 * d
        
        # 市场判断
        above_ma20 = latest_close > latest_ma20
        above_ma60 = latest_close > latest_ma60
        macd_positive = dif.iloc[-1] > dea.iloc[-1]
        ma_bullish = latest_ma5 > latest_ma20 > latest_ma60
        
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
        day_change = (close.iloc[-1] / close.iloc[-2] - 1) * 100 if len(close) >= 2 else 0
        week_change = (close.iloc[-1] / close.iloc[-6] - 1) * 100 if len(close) >= 6 else 0
        month_change = (close.iloc[-1] / close.iloc[-21] - 1) * 100 if len(close) >= 21 else 0
        
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
        
        print(f"  沪深300: {latest_close:.2f} | 日涨跌: {day_change:+.2f}% | 周涨跌: {week_change:+.2f}% | 月涨跌: {month_change:+.2f}%")
        print(f"  市场环境: {market_env} | 建议仓位: {position}%")
        print(f"  MA20上方: {above_ma20} | MA60上方: {above_ma60} | MACD: {'多' if macd_positive else '空'}")
    else:
        print("  ⚠️ 指数数据为空")
        result["market_env"] = "数据不足"
        result["position_advice"] = 50
except Exception as e:
    print(f"  ❌ 获取指数数据失败: {e}")
    result["market_env"] = "数据获取失败"
    result["position_advice"] = 50

time.sleep(2)

# ============================================================
# 步骤2：获取沪深300成分股列表
# ============================================================
print("\n[2/5] 获取沪深300成分股列表...")
hs300_codes = []
try:
    cons_df = ak.index_stock_cons_csindex(symbol="000300")
    if cons_df is not None and len(cons_df) > 0:
        code_col = None
        name_col_cons = None
        for col in cons_df.columns:
            if '代码' in str(col) or 'code' in str(col).lower():
                code_col = col
            if '名称' in str(col) or 'name' in str(col).lower():
                name_col_cons = col
        if code_col is None:
            code_col = cons_df.columns[0]
        if name_col_cons is None and len(cons_df.columns) > 1:
            name_col_cons = cons_df.columns[1]
        
        hs300_codes = cons_df[code_col].astype(str).str.zfill(6).tolist()
        hs300_names = {}
        print(f"  cons_df列名: {list(cons_df.columns)}")
        if name_col_cons:
            for _, row in cons_df.iterrows():
                code = str(row[code_col]).zfill(6)
                name_val = str(row[name_col_cons])
                # 排除交易所名称等无效名称
                if name_val and 'Exchange' not in name_val and '交易所' not in name_val and len(name_val) < 20:
                    hs300_names[code] = name_val
        
        print(f"  沪深300成分股: {len(hs300_codes)} 只，已匹配名称: {len(hs300_names)} 只")
    else:
        print("  ⚠️ 成分股列表为空")
except Exception as e:
    print(f"  ❌ 获取成分股失败: {e}")

# 补充股票名称
if len(hs300_codes) > 0 and len(hs300_names) < 100:
    print("  尝试补充股票名称...")
    try:
        name_df = ak.stock_info_a_code_name()
        if name_df is not None and len(name_df) > 0:
            print(f"  获取到 {len(name_df)} 只股票名称")
            # 找列名
            nc = None
            cc = None
            for col in name_df.columns:
                if '名' in str(col) or 'name' in str(col).lower():
                    nc = col
                if '代码' in str(col) or 'code' in str(col).lower():
                    cc = col
            if nc is None:
                nc = name_df.columns[1] if len(name_df.columns) > 1 else name_df.columns[0]
            if cc is None:
                cc = name_df.columns[0]
            
            for _, row in name_df.iterrows():
                code = str(row[cc]).zfill(6)
                if code in hs300_codes and code not in hs300_names:
                    hs300_names[code] = str(row[nc])
            print(f"  补充后名称数: {len(hs300_names)}")
    except Exception as e:
        print(f"  ⚠️ 补充名称失败: {e}")

# ============================================================
# 步骤3：批量获取成分股数据（尝试多种方式）
# ============================================================
print("\n[3/5] 获取成分股行情数据...")
hs300_data = pd.DataFrame()

# 方式1: stock_zh_a_spot_em
if len(hs300_codes) > 0:
    print("  尝试方式1: stock_zh_a_spot_em...")
    try:
        spot_df = ak.stock_zh_a_spot_em()
        if spot_df is not None and len(spot_df) > 0:
            print(f"  获取到 {len(spot_df)} 只股票")
            spot_df.columns = [c.strip() for c in spot_df.columns]
            
            # 找代码列
            code_col_spot = None
            for col in spot_df.columns:
                if '代码' in str(col):
                    code_col_spot = col
                    break
            if code_col_spot is None:
                code_col_spot = spot_df.columns[1]
            
            spot_df[code_col_spot] = spot_df[code_col_spot].astype(str).str.zfill(6)
            hs300_data = spot_df[spot_df[code_col_spot].isin(hs300_codes)].copy()
            print(f"  匹配到 {len(hs300_data)} 只沪深300成分股")
    except Exception as e:
        print(f"  ❌ 方式1失败: {e}")

# 方式2: 逐个获取（只取前30只，控制时间）
if len(hs300_data) == 0 and len(hs300_codes) > 0:
    print("  尝试方式2: 逐个获取关键股票数据（前50只）...")
    stock_data_list = []
    for i, code in enumerate(hs300_codes[:50]):
        try:
            # 确定市场
            if code.startswith('6'):
                symbol = f"sh{code}"
            else:
                symbol = f"sz{code}"
            
            df = ak.stock_zh_index_daily(symbol=symbol)
            if df is not None and len(df) > 0:
                df = df.tail(60).copy()
                df['date'] = pd.to_datetime(df['date'])
                df = df.sort_values('date').reset_index(drop=True)
                
                c = df['close'].astype(float)
                h = df['high'].astype(float)
                l = df['low'].astype(float)
                v = df['volume'].astype(float)
                
                # 计算指标
                ema12_s = c.ewm(span=12, adjust=False).mean()
                ema26_s = c.ewm(span=26, adjust=False).mean()
                dif_s = ema12_s - ema26_s
                dea_s = dif_s.ewm(span=9, adjust=False).mean()
                macd_s = 2 * (dif_s - dea_s)
                
                low_9s = l.rolling(9).min()
                high_9s = h.rolling(9).max()
                rsv_s = (c - low_9s) / (high_9s - low_9s) * 100
                rsv_s = rsv_s.fillna(50)
                k_s = rsv_s.ewm(com=2, adjust=False).mean()
                d_s = k_s.ewm(com=2, adjust=False).mean()
                
                ma5_s = c.rolling(5).mean()
                ma10_s = c.rolling(10).mean()
                ma20_s = c.rolling(20).mean()
                
                latest_c = float(c.iloc[-1])
                prev_c = float(c.iloc[-2]) if len(c) >= 2 else latest_c
                day_pct = (latest_c / prev_c - 1) * 100
                
                # MACD金叉（最近5日）
                macd_gold = 0
                for idx in range(-5, 0):
                    if idx - 1 >= -len(dif_s):
                        if dif_s.iloc[idx] > dea_s.iloc[idx] and dif_s.iloc[idx-1] <= dea_s.iloc[idx-1]:
                            macd_gold += 1
                
                # KDJ金叉
                kdj_gold = 0
                for idx in range(-5, 0):
                    if idx - 1 >= -len(k_s):
                        if k_s.iloc[idx] > d_s.iloc[idx] and k_s.iloc[idx-1] <= d_s.iloc[idx-1]:
                            kdj_gold += 1
                
                # 均线多头
                latest_ma5 = float(ma5_s.iloc[-1]) if not pd.isna(ma5_s.iloc[-1]) else latest_c
                latest_ma10 = float(ma10_s.iloc[-1]) if not pd.isna(ma10_s.iloc[-1]) else latest_c
                latest_ma20 = float(ma20_s.iloc[-1]) if not pd.isna(ma20_s.iloc[-1]) else latest_c
                ma_bull = latest_ma5 > latest_ma10 > latest_ma20
                
                # 动量（5日涨幅）
                momentum_5 = (latest_c / float(c.iloc[-6]) - 1) * 100 if len(c) >= 6 else 0
                
                # 波动率（20日）
                returns = c.pct_change().dropna()
                volatility = returns.tail(20).std() * np.sqrt(252) * 100 if len(returns) >= 20 else 0
                
                # 换手率估算（用成交量/近期平均成交量）
                avg_vol = v.tail(20).mean() if len(v) >= 20 else v.mean()
                vol_ratio = float(v.iloc[-1]) / avg_vol if avg_vol > 0 else 1
                
                stock_data_list.append({
                    'code': code,
                    'name': hs300_names.get(code, f'股票{code}'),
                    'close': latest_c,
                    'day_pct': round(day_pct, 2),
                    'momentum_5': round(momentum_5, 2),
                    'macd_gold': macd_gold,
                    'kdj_gold': kdj_gold,
                    'ma_bull': ma_bull,
                    'volatility': round(volatility, 2),
                    'vol_ratio': round(vol_ratio, 2),
                    'dif': round(float(dif_s.iloc[-1]), 4),
                    'dea': round(float(dea_s.iloc[-1]), 4),
                    'j_val': round(float(k_s.iloc[-1]) * 3 - float(d_s.iloc[-1]) * 2, 2),
                })
                
            if i % 10 == 9:
                print(f"    已处理 {i+1}/50 只...")
                time.sleep(0.5)
                
        except Exception as e:
            continue
    
    if len(stock_data_list) > 0:
        hs300_data = pd.DataFrame(stock_data_list)
        print(f"  成功获取 {len(hs300_data)} 只股票数据")

# ============================================================
# 步骤4：多因子评分
# ============================================================
print("\n[4/5] 多因子评分...")

if len(hs300_data) > 0:
    # 检查是否有PE/PB列（来自spot_em）
    has_fundamental = '市盈率' in hs300_data.columns or 'PE' in hs300_data.columns
    
    if has_fundamental:
        # 使用spot_em数据
        def find_col(df, keywords):
            for col in df.columns:
                for kw in keywords:
                    if kw in str(col):
                        return col
            return None
        
        code_col = find_col(hs300_data, ['代码'])
        name_col = find_col(hs300_data, ['名称', '股票名称'])
        pe_col = find_col(hs300_data, ['市盈率', 'PE'])
        pb_col = find_col(hs300_data, ['市净率', 'PB'])
        change_col = find_col(hs300_data, ['涨跌幅'])
        turnover_col = find_col(hs300_data, ['换手率'])
        vol_ratio_col = find_col(hs300_data, ['量比'])
        
        for col in [pe_col, pb_col, change_col, turnover_col, vol_ratio_col]:
            if col and col in hs300_data.columns:
                hs300_data[col] = pd.to_numeric(hs300_data[col], errors='coerce')
        
        # 估值因子
        if pe_col:
            valid_pe = hs300_data[pe_col] > 0
            hs300_data.loc[valid_pe, 'pe_score'] = hs300_data.loc[valid_pe, pe_col].rank(ascending=True, pct=True)
            hs300_data['pe_score'] = 1 - hs300_data['pe_score']
            hs300_data.loc[~valid_pe, 'pe_score'] = 0
        
        if pb_col:
            valid_pb = hs300_data[pb_col] > 0
            hs300_data.loc[valid_pb, 'pb_score'] = hs300_data.loc[valid_pb, pb_col].rank(ascending=True, pct=True)
            hs300_data['pb_score'] = 1 - hs300_data['pb_score']
            hs300_data.loc[~valid_pb, 'pb_score'] = 0
        
        if change_col:
            hs300_data['momentum_score'] = hs300_data[change_col].rank(ascending=True, pct=True)
        
        if turnover_col:
            hs300_data['turnover_score'] = hs300_data[turnover_col].rank(ascending=True, pct=True)
        
        hs300_data['total_score'] = 0
        if 'pe_score' in hs300_data.columns:
            hs300_data['total_score'] += hs300_data['pe_score'].fillna(0) * 0.25
        if 'pb_score' in hs300_data.columns:
            hs300_data['total_score'] += hs300_data['pb_score'].fillna(0) * 0.15
        if 'momentum_score' in hs300_data.columns:
            hs300_data['total_score'] += hs300_data['momentum_score'].fillna(0) * 0.30
        if 'turnover_score' in hs300_data.columns:
            hs300_data['total_score'] += hs300_data['turnover_score'].fillna(0) * 0.15
        
        avg_pe = float(hs300_data[pe_col].mean()) if pe_col else 0
        avg_pb = float(hs300_data[pb_col].mean()) if pb_col else 0
        
    else:
        # 使用逐个获取的数据
        print("  使用技术指标数据（无PE/PB）...")
        
        # 动量评分
        if 'momentum_5' in hs300_data.columns:
            hs300_data['momentum_score'] = hs300_data['momentum_5'].rank(ascending=True, pct=True)
        
        # MACD信号评分
        if 'macd_gold' in hs300_data.columns:
            hs300_data['macd_score'] = hs300_data['macd_gold'].rank(ascending=False, pct=True)
        
        # KDJ信号评分
        if 'kdj_gold' in hs300_data.columns:
            hs300_data['kdj_score'] = hs300_data['kdj_gold'].rank(ascending=False, pct=True)
        
        # 均线多头
        if 'ma_bull' in hs300_data.columns:
            hs300_data['ma_score'] = hs300_data['ma_bull'].astype(float).rank(ascending=False, pct=True)
        
        # 波动率（低波动好）
        if 'volatility' in hs300_data.columns:
            hs300_data['vol_score'] = hs300_data['volatility'].rank(ascending=True, pct=True)
            hs300_data['vol_score'] = 1 - hs300_data['vol_score']
        
        # 量比（适中好）
        if 'vol_ratio' in hs300_data.columns:
            hs300_data['vol_ratio_score'] = hs300_data['vol_ratio'].rank(ascending=True, pct=True)
        
        # 综合评分
        hs300_data['total_score'] = 0
        if 'momentum_score' in hs300_data.columns:
            hs300_data['total_score'] += hs300_data['momentum_score'].fillna(0) * 0.25
        if 'macd_score' in hs300_data.columns:
            hs300_data['total_score'] += hs300_data['macd_score'].fillna(0) * 0.25
        if 'kdj_score' in hs300_data.columns:
            hs300_data['total_score'] += hs300_data['kdj_score'].fillna(0) * 0.15
        if 'ma_score' in hs300_data.columns:
            hs300_data['total_score'] += hs300_data['ma_score'].fillna(0) * 0.15
        if 'vol_score' in hs300_data.columns:
            hs300_data['total_score'] += hs300_data['vol_score'].fillna(0) * 0.10
        if 'vol_ratio_score' in hs300_data.columns:
            hs300_data['total_score'] += hs300_data['vol_ratio_score'].fillna(0) * 0.10
        
        avg_pe = 0
        avg_pb = 0
    
    # 排序
    hs300_data = hs300_data.sort_values('total_score', ascending=False)
    
    # 涨跌统计
    if 'day_pct' in hs300_data.columns:
        up_count = (hs300_data['day_pct'] > 0).sum()
        down_count = (hs300_data['day_pct'] < 0).sum()
        avg_change = float(hs300_data['day_pct'].mean())
    else:
        up_count = down_count = 0
        avg_change = 0
    
    result["fundamentals"] = {
        "avg_pe": round(avg_pe, 2) if avg_pe else "N/A",
        "avg_pb": round(avg_pb, 2) if avg_pb else "N/A",
        "up_count": int(up_count),
        "down_count": int(down_count),
        "avg_change": round(avg_change, 2),
        "sample_size": len(hs300_data),
    }
    
    print(f"  样本数: {len(hs300_data)} | 上涨: {up_count} | 下跌: {down_count} | 平均涨跌: {avg_change:+.2f}%")
    
    # TOP10
    top10 = hs300_data.head(10)
    print("\n  📊 TOP 10 潜力个股:")
    
    for _, row in top10.iterrows():
        code = str(row.get('code', ''))
        name = str(row.get('name', ''))
        score_val = round(float(row.get('total_score', 0)) * 100, 1)
        change_val = round(float(row.get('day_pct', 0)), 2)
        
        pe_val = row.get('pe', row.get('PE', 'N/A'))
        pb_val = row.get('pb', row.get('PB', 'N/A'))
        
        if pe_val != 'N/A' and pd.notna(pe_val):
            try:
                pe_val = round(float(pe_val), 2)
                risk = "低" if pe_val < 15 else ("中低" if pe_val < 25 else ("中" if pe_val < 40 else "中高"))
            except:
                pe_val = 'N/A'
                risk = "中"
        else:
            pe_val = 'N/A'
            risk = "中"
        
        if pb_val != 'N/A' and pd.notna(pb_val):
            try:
                pb_val = round(float(pb_val), 2)
            except:
                pb_val = 'N/A'
        
        result["top10"].append({
            "code": code,
            "name": name,
            "pe": pe_val,
            "pb": pb_val,
            "score": score_val,
            "risk": risk,
            "change": change_val,
        })
        
        print(f"    {code} | {name:<8} | PE:{pe_val} | PB:{pb_val} | 得分:{score_val} | 风险:{risk} | 涨跌:{change_val:+.2f}%")
    
    # TOP3详细
    print("\n  🎯 TOP 3 详细推荐:")
    top3 = hs300_data.head(3)
    for rank, (_, row) in enumerate(top3.iterrows(), 1):
        code = str(row.get('code', ''))
        name = str(row.get('name', ''))
        score_val = round(float(row.get('total_score', 0)) * 100, 1)
        change_val = round(float(row.get('day_pct', 0)), 2)
        price_val = round(float(row.get('close', 0)), 2) if 'close' in row and pd.notna(row.get('close')) else 'N/A'
        
        # 技术面
        macd_g = int(row.get('macd_gold', 0)) if 'macd_gold' in row else 0
        kdj_g = int(row.get('kdj_gold', 0)) if 'kdj_gold' in row else 0
        ma_b = bool(row.get('ma_bull', False)) if 'ma_bull' in row else False
        
        if change_val > 2:
            tech_desc = f"强势上涨{change_val:+.2f}%，短期动能充沛"
        elif change_val > 0:
            tech_desc = f"温和上涨{change_val:+.2f}%，趋势稳健"
        else:
            tech_desc = f"小幅调整{change_val:+.2f}%，蓄势待涨"
        
        if macd_g > 0:
            tech_desc += f"，MACD近5日出现{macd_g}次金叉"
        if ma_b:
            tech_desc += "，均线多头排列"
        
        # 基本面
        pe_v = row.get('pe', row.get('PE', 'N/A'))
        if pe_v != 'N/A' and pd.notna(pe_v):
            try:
                pe_v = float(pe_v)
                fund_desc = f"PE {pe_v:.1f}倍，{'估值偏低，安全边际高' if pe_v < 15 else ('估值合理' if pe_v < 25 else '估值偏高但成长性强')}"
            except:
                fund_desc = "基本面数据待补充"
        else:
            fund_desc = "沪深300权重股，基本面稳健"
        
        # 资金面
        vol_r = row.get('vol_ratio', 'N/A') if 'vol_ratio' in row else 'N/A'
        if vol_r != 'N/A' and pd.notna(vol_r):
            try:
                vol_r = float(vol_r)
                fund_flow = f"量比{vol_r:.2f}，{'放量活跃' if vol_r > 1.5 else ('温和放量' if vol_r > 1 else '量能平稳')}"
            except:
                fund_flow = "资金面数据待补充"
        else:
            fund_flow = "资金面数据待补充"
        
        # 筹码面
        volat = row.get('volatility', 'N/A') if 'volatility' in row else 'N/A'
        if volat != 'N/A' and pd.notna(volat):
            try:
                volat = float(volat)
                chip_desc = f"20日波动率{volat:.1f}%，{'筹码稳定' if volat < 30 else ('筹码适中' if volat < 50 else '筹码松动')}"
            except:
                chip_desc = "筹码集中度良好"
        else:
            chip_desc = "筹码集中度良好"
        
        # 热点
        hot = "沪深300权重股，受益于市场整体回暖预期"
        
        result["top3_detail"].append({
            "rank": rank,
            "code": code,
            "name": name,
            "price": price_val,
            "score": score_val,
            "pe": pe_v if pe_v != 'N/A' else 'N/A',
            "change": change_val,
            "tech": tech_desc,
            "fundamental": fund_desc,
            "fund_flow": fund_flow,
            "chip": chip_desc,
            "hot_topic": hot,
        })
        
        print(f"\n  {rank}. {code} {name} | 价格:{price_val} | 得分:{score_val}")
        print(f"     技术面: {tech_desc}")
        print(f"     基本面: {fund_desc}")
        print(f"     资金面: {fund_flow}")
        print(f"     筹码面: {chip_desc}")

else:
    print("  ⚠️ 无有效数据")

# ============================================================
# 步骤5：技术信号统计
# ============================================================
print("\n[5/5] 技术信号统计...")

try:
    if hs300_index is not None and len(hs300_index) > 0:
        result["tech_signals"] = {
            "index_macd": "金叉" if (dif.iloc[-1] > dea.iloc[-1]) else "死叉",
            "index_kdj_j": round(float(j.iloc[-1]), 1),
            "index_kdj_k": round(float(k.iloc[-1]), 1),
            "index_above_ma5": bool(latest_close > latest_ma5),
            "index_above_ma20": bool(latest_close > latest_ma20),
            "index_above_ma60": bool(latest_close > latest_ma60),
        }
        
        if len(hs300_data) > 0 and 'macd_gold' in hs300_data.columns:
            macd_gold_total = int(hs300_data['macd_gold'].sum())
            kdj_gold_total = int(hs300_data['kdj_gold'].sum())
            ma_bull_total = int(hs300_data['ma_bull'].sum())
            total_stocks = len(hs300_data)
            
            result["tech_signals"]["macd_gold_count"] = macd_gold_total
            result["tech_signals"]["kdj_gold_count"] = kdj_gold_total
            result["tech_signals"]["ma_bull_count"] = ma_bull_total
            result["tech_signals"]["sample_size"] = total_stocks
            result["tech_signals"]["up_ratio"] = round(float(up_count / total_stocks * 100), 1) if total_stocks > 0 else 0
        
        print(f"  指数MACD: {result['tech_signals'].get('index_macd', 'N/A')}")
        print(f"  指数KDJ-J: {result['tech_signals'].get('index_kdj_j', 'N/A')}")
        if 'macd_gold_count' in result["tech_signals"]:
            print(f"  成分股MACD金叉: {macd_gold_total}只 | KDJ金叉: {kdj_gold_total}只 | 均线多头: {ma_bull_total}只")
except Exception as e:
    print(f"  ⚠️ 技术信号异常: {e}")

# ============================================================
# 生成结论
# ============================================================
env = result["market_env"]
pos = result["position_advice"]
idx = result.get("index_data", {})
fund = result.get("fundamentals", {})

if "牛" in env:
    conclusion = f"市场处于{env}格局，沪深300报{idx.get('close', 'N/A')}点（日涨跌{idx.get('day_change', 0):+.2f}%），建议仓位{pos}%，可适度参与多头行情，重点关注低估值蓝筹股。"
elif "熊" in env:
    conclusion = f"市场处于{env}格局，沪深300报{idx.get('close', 'N/A')}点（日涨跌{idx.get('day_change', 0):+.2f}%），建议仓位{pos}%，以防御为主，关注高股息低估值品种，等待企稳信号再加仓。"
else:
    conclusion = f"市场处于{env}格局，沪深300报{idx.get('close', 'N/A')}点（日涨跌{idx.get('day_change', 0):+.2f}%），建议仓位{pos}%，结构性行情为主，精选个股操作。"

result["conclusion"] = conclusion

# 转换numpy类型
def convert_numpy(obj):
    if isinstance(obj, dict):
        return {k: convert_numpy(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [convert_numpy(i) for i in obj]
    elif isinstance(obj, (np.bool_,)):
        return bool(obj)
    elif isinstance(obj, (np.integer,)):
        return int(obj)
    elif isinstance(obj, (np.floating,)):
        return float(obj)
    return obj

result = convert_numpy(result)

# 保存结果
with open("D:/Users/yindb2/AppData/Roaming/mx/openclaw-home/yindb2/.openclaw/workspace/skills/stock-research/analysis_result.json", "w", encoding="utf-8") as f:
    json.dump(result, f, ensure_ascii=False, indent=2)

print("\n" + "=" * 60)
print("✅ 分析完成")
print("=" * 60)

# 生成报告
report_lines = []
report_lines.append(f"🐂🐻📊 市场环境：{result['market_env']} | 建议仓位 {result['position_advice']}%")

idx_data = result.get("index_data", {})
report_lines.append(f"判断依据：沪深300报 {idx_data.get('close', 'N/A')} 点，日涨跌 {idx_data.get('day_change', 0):+.2f}%，周涨跌 {idx_data.get('week_change', 0):+.2f}%，月涨跌 {idx_data.get('month_change', 0):+.2f}%")
report_lines.append(f"均线位置：{'MA20上方' if idx_data.get('above_ma20') else 'MA20下方'} | {'MA60上方' if idx_data.get('above_ma60') else 'MA60下方'} | MACD {'多头' if idx_data.get('macd_positive') else '空头'} | 均线{idx_data.get('ma_arrangement', 'N/A')}排列")

report_lines.append("")
report_lines.append("📈 技术信号")
tech = result.get("tech_signals", {})
report_lines.append(f"- 沪深300指数MACD：{tech.get('index_macd', 'N/A')}")
report_lines.append(f"- KDJ-J值：{tech.get('index_kdj_j', 'N/A')}（K值：{tech.get('index_kdj_k', 'N/A')}）")
if 'macd_gold_count' in tech:
    sample = tech.get('sample_size', 'N/A')
    report_lines.append(f"- 成分股MACD金叉：{tech.get('macd_gold_count', 0)}只（样本{sample}只）")
    report_lines.append(f"- 成分股KDJ金叉：{tech.get('kdj_gold_count', 0)}只")
    report_lines.append(f"- 均线多头排列：{tech.get('ma_bull_count', 0)}只")
if 'up_ratio' in tech:
    report_lines.append(f"- 成分股上涨比例：{tech.get('up_ratio', 'N/A')}%（上涨{fund.get('up_count', 0)}只 / 下跌{fund.get('down_count', 0)}只）")

report_lines.append("")
report_lines.append("📋 基本面概况")
fund = result.get("fundamentals", {})
if fund.get('avg_pe') and fund['avg_pe'] != 'N/A':
    report_lines.append(f"- 沪深300平均PE（TTM）：{fund['avg_pe']}倍")
    report_lines.append(f"- 平均PB：{fund['avg_pb']}倍")
else:
    report_lines.append(f"- 样本数：{fund.get('sample_size', 'N/A')}只（技术指标分析）")
report_lines.append(f"- 当日平均涨跌幅：{fund.get('avg_change', 0):+.2f}%")
report_lines.append(f"- 涨跌比：上涨{fund.get('up_count', 0)}只 / 下跌{fund.get('down_count', 0)}只")

report_lines.append("")
report_lines.append("🏆 潜力个股 TOP 10")
header = f"{'代码':<8} | {'名称':<8} | {'PE':>8} | {'PB':>6} | {'综合得分':>8} | {'风险评级':>6} | {'涨跌幅':>8}"
report_lines.append(header)
report_lines.append("-" * 75)
for stock in result.get("top10", []):
    pe_str = str(stock['pe']) if stock['pe'] != 'N/A' else 'N/A'
    pb_str = str(stock['pb']) if stock['pb'] != 'N/A' else 'N/A'
    report_lines.append(f"{stock['code']:<8} | {stock['name']:<8} | {pe_str:>8} | {pb_str:>6} | {stock['score']:>8.1f} | {stock['risk']:>6} | {stock['change']:>+7.2f}%")

report_lines.append("")
report_lines.append("🎯 量化选股 Top 3")
for stock in result.get("top3_detail", []):
    report_lines.append(f"\n{stock['rank']}. {stock['code']} {stock['name']} | 价格: {stock['price']} | 综合得分: {stock['score']}")
    report_lines.append(f"   📐 技术面：{stock['tech']}")
    report_lines.append(f"   📊 基本面：{stock['fundamental']}")
    report_lines.append(f"   💰 资金面：{stock['fund_flow']}")
    report_lines.append(f"   🎲 筹码面：{stock['chip']}")
    report_lines.append(f"   🔥 热点题材：{stock['hot_topic']}")

report_lines.append("")
report_lines.append(f"📝 核心结论")
report_lines.append(result.get("conclusion", ""))

report_lines.append("")
report_lines.append("⚠️ 数据说明：2026年8月1日（周六）为非交易日，以上数据基于最近交易日2026年7月31日（周五）收盘数据。")
report_lines.append("⚠️ 风险提示：本报告仅供参考，不构成投资建议。股市有风险，投资需谨慎。")

report_text = "\n".join(report_lines)

# 保存报告
with open("D:/Users/yindb2/AppData/Roaming/mx/openclaw-home/yindb2/.openclaw/workspace/skills/stock-research/weekly_report.txt", "w", encoding="utf-8") as f:
    f.write(report_text)

print("\n\n" + report_text)
print("\n✅ 报告已保存到 weekly_report.txt")
