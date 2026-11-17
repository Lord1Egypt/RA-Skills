#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
三周期趋势雷达 v2.0 (three-period trend radar)
基于 月线/周线/日线 共振框架的 A 股趋势评分与筛选工具。

与《股市成长手册》均线体系完全对齐：
- 日线 MA5/10/20/60，MACD(12,26,9)
- 周线 MA5/10/20
- 月线 MA3/5/10

输入: 日线 OHLCV CSV。自动识别两种数据源格式:
  - iFinD: 列为 time(YYYYMMDD)/open/high/low/close/volume/thscode/thsname_cn
  - Yahoo: 列为 Date(ISO)/Open/High/Low/Close/Volume

用法:
  python3 radar.py 数据.csv [更多.csv ...]          # 批量评分排序（表格输出）
  python3 radar.py 数据.csv --json                   # 结构化 JSON 输出（供 agent 解析）
  python3 radar.py 数据.csv --detail                 # 单票详细三周期状态
  python3 radar.py 数据.csv --name 博杰股份          # 覆盖显示名

输出: 评分、checklist_pass、三周期状态、触发信号、近20日涨跌
"""

import argparse
import json
import sys

import numpy as np
import pandas as pd

# ---------------------------------------------------------------- 数据加载

def load_ohlcv(path):
    """读取 CSV 并规范为 Date/Open/High/Low/Close/Volume 升序 DataFrame 列表 [(name, df)]"""
    raw = pd.read_csv(path)
    cols = {c.lower(): c for c in raw.columns}

    # 日期列
    if 'time' in cols:
        date_col = cols['time']
        raw['Date'] = pd.to_datetime(raw[date_col].astype(str), format='%Y%m%d', errors='coerce')
    elif 'date' in cols:
        date_col = cols['date']
        raw['Date'] = pd.to_datetime(raw[date_col], errors='coerce', utc=True).dt.tz_localize(None)
    else:
        raise ValueError(f"{path}: 找不到日期列(time/Date)")

    rename = {}
    for std, aliases in {'Open': ['open', 'o'], 'High': ['high', 'h'], 'Low': ['low', 'l'],
                         'Close': ['close', 'c', 'adj close'], 'Volume': ['volume', 'vol', 'v']}.items():
        for a in aliases:
            if a in cols:
                rename[cols[a]] = std
                break
    raw = raw.rename(columns=rename)
    missing = [c for c in ['Open', 'High', 'Low', 'Close', 'Volume'] if c not in raw.columns]
    if missing:
        raise ValueError(f"{path}: 缺少列 {missing}")
    raw = raw.dropna(subset=['Date']).sort_values('Date')

    # 多标的文件按 thscode 拆分
    out = []
    if 'thscode' in raw.columns and raw['thscode'].nunique() > 1:
        for code, g in raw.groupby('thscode'):
            name = g['thsname_cn'].iloc[-1] if 'thsname_cn' in g.columns and pd.notna(g['thsname_cn'].iloc[-1]) else code
            out.append((str(name), g[['Date', 'Open', 'High', 'Low', 'Close', 'Volume']].reset_index(drop=True)))
    else:
        name = None
        if 'thsname_cn' in raw.columns and pd.notna(raw['thsname_cn'].iloc[-1]):
            name = str(raw['thsname_cn'].iloc[-1])
        out.append((name, raw[['Date', 'Open', 'High', 'Low', 'Close', 'Volume']].reset_index(drop=True)))
    return out


# ---------------------------------------------------------------- 指标计算

def calc_indicators(df, mas=(5, 10, 20, 60)):
    """MA + MACD(12,26,9) + 量能均线"""
    df = df.copy().sort_values('Date').reset_index(drop=True)
    for p in mas:
        df[f'MA{p}'] = df['Close'].rolling(p).mean()
    ema12 = df['Close'].ewm(span=12, adjust=False).mean()
    ema26 = df['Close'].ewm(span=26, adjust=False).mean()
    df['DIF'] = ema12 - ema26
    df['DEA'] = df['DIF'].ewm(span=9, adjust=False).mean()
    df['MACD'] = 2 * (df['DIF'] - df['DEA'])
    df['VOL_MA5'] = df['Volume'].rolling(5).mean()
    df['VOL_MA20'] = df['Volume'].rolling(20).mean()
    return df


def resample(df, rule):
    """日线 -> 周线(W-FRI) / 月线(ME)"""
    d = df.copy()
    d['Date'] = pd.to_datetime(d['Date'])
    d = d.set_index('Date')
    out = d.resample(rule).agg({'Open': 'first', 'High': 'max', 'Low': 'min',
                                'Close': 'last', 'Volume': 'sum'}).dropna().reset_index()
    return out


# ---------------------------------------------------------------- 趋势判定

def classify_period(row):
    """单周期趋势分类（含弱多/弱空试探）"""
    close, ma5, ma10 = row['Close'], row.get('MA5'), row.get('MA10')
    dif, dea = row.get('DIF'), row.get('DEA')
    if pd.isna(ma5) or pd.isna(ma10) or pd.isna(dif) or pd.isna(dea):
        return '数据不足'
    
    gold = dif > dea
    above = close > ma5
    ma_bull = ma5 > ma10
    
    if above and ma_bull and gold and dif > 0:
        return '强势多头'
    if above and ma_bull and gold:
        return '多头'
    if above and ma_bull:
        return '偏多'
    if above and not ma_bull:
        return '弱多试探'
    if (not above) and (not ma_bull) and (not gold) and dif < 0:
        return '强势空头'
    if (not above) and (not ma_bull) and (not gold):
        return '空头'
    if (not above) and (not ma_bull):
        return '偏空'
    if (not above) and ma_bull:
        return '弱空试探'
    return '横盘'


def check_divergence(df, lookback=30):
    """日线顶/底背离检测(收盘价 vs DIF)"""
    if len(df) < lookback + 5:
        return {'top_div': False, 'bot_div': False}
    recent = df.tail(lookback)
    res = {'top_div': False, 'bot_div': False}
    highs = recent[recent['Close'] == recent['Close'].rolling(5, center=True).max()]
    if len(highs) >= 2:
        h1, h2 = highs.iloc[-2], highs.iloc[-1]
        res['top_div'] = bool(h2['Close'] > h1['Close'] and h2['DIF'] < h1['DIF'])
    lows = recent[recent['Close'] == recent['Close'].rolling(5, center=True).min()]
    if len(lows) >= 2:
        l1, l2 = lows.iloc[-2], lows.iloc[-1]
        res['bot_div'] = bool(l2['Close'] < l1['Close'] and l2['DIF'] > l1['DIF'])
    return res


# ---------------------------------------------------------------- Checklist

def check_checklist(daily, weekly, monthly):
    """
    三周期共振买入 checklist（缺一不可）
    返回 (passed: bool, details: dict)
    """
    details = {
        'month_macd_gold': False,
        'month_dif_positive': False,
        'week_macd_gold': False,
        'week_ma_bull': False,
        'week_price_above_ma20': False,
        'day_macd_gold': False,
        'day_ma_bull': False,
        'day_no_top_div': False,
        'volume_ok': False,
    }
    
    dl = daily.iloc[-1]
    wl = weekly.iloc[-1] if len(weekly) else None
    ml = monthly.iloc[-1] if len(monthly) else None
    
    # 月线
    if ml is not None:
        details['month_macd_gold'] = bool(ml['DIF'] > ml['DEA'])
        details['month_dif_positive'] = bool(ml['DIF'] > 0)
    
    # 周线
    if wl is not None:
        details['week_macd_gold'] = bool(wl['DIF'] > wl['DEA'])
        details['week_ma_bull'] = bool(wl['MA5'] > wl['MA10'])
        details['week_price_above_ma20'] = bool(wl['Close'] > wl['MA20']) if not pd.isna(wl.get('MA20')) else False
    
    # 日线
    details['day_macd_gold'] = bool(dl['DIF'] > dl['DEA'])
    details['day_ma_bull'] = bool(dl['Close'] > dl['MA5'] > dl['MA10'])
    
    div = check_divergence(daily, 30)
    details['day_no_top_div'] = not div['top_div']
    
    # 成交量
    details['volume_ok'] = bool(dl['Volume'] > dl['VOL_MA20'] * 1.2)
    
    # checklist 通过条件：月线MACD金叉或DIF>0，周线MACD金叉+MA5>MA10+价>MA20，日线MACD金叉+价>MA5>MA10+无顶背离，成交量放大
    month_ok = details['month_macd_gold'] or details['month_dif_positive']
    week_ok = details['week_macd_gold'] and details['week_ma_bull'] and details['week_price_above_ma20']
    day_ok = details['day_macd_gold'] and details['day_ma_bull'] and details['day_no_top_div']
    vol_ok = details['volume_ok']
    
    passed = month_ok and week_ok and day_ok and vol_ok
    return passed, details


# ---------------------------------------------------------------- 雷达评分

def three_period_radar(df_daily, name):
    """核心引擎: 返回评分/checklist_pass/三周期状态/信号/各周期数据"""
    daily = calc_indicators(df_daily)
    weekly = calc_indicators(resample(df_daily, 'W-FRI'), mas=(5, 10, 20))
    monthly = calc_indicators(resample(df_daily, 'ME'), mas=(3, 5, 10))

    dl = daily.iloc[-1]
    wl = weekly.iloc[-1] if len(weekly) else None
    ml = monthly.iloc[-1] if len(monthly) else None

    score, signals = 0, []

    # 日线(权重低)
    if dl['Close'] > dl['MA5']: score += 2; signals.append('日线价上MA5')
    if dl['MA5'] > dl['MA10']: score += 2; signals.append('日线MA5上穿MA10')
    if dl['DIF'] > dl['DEA']: score += 3; signals.append('日线MACD金叉')
    if dl['DIF'] > 0: score += 3; signals.append('日线DIF零轴上')
    if dl['Close'] > dl['MA20']: score += 2; signals.append('日线价上MA20')
    if dl['Volume'] > dl['VOL_MA20'] * 1.2: score += 1; signals.append('日线放量')

    div = check_divergence(daily, 30)
    if div['top_div']: score -= 3; signals.append('⚠️日线顶背离')
    if div['bot_div']: score += 2; signals.append('✅日线底背离')

    # 周线(权重中)
    if wl is not None:
        if wl['Close'] > wl['MA5']: score += 3; signals.append('周线价上MA5')
        if wl['MA5'] > wl['MA10']: score += 3; signals.append('周线MA5上穿MA10')
        if wl['DIF'] > wl['DEA']: score += 4; signals.append('周线MACD金叉')
        if wl['DIF'] > 0: score += 4; signals.append('周线DIF零轴上')
        if wl['Close'] > wl['MA20']: score += 3; signals.append('周线价上MA20')

    # 月线(权重高)
    if ml is not None:
        if ml['Close'] > ml['MA5']: score += 4; signals.append('月线价上MA5')
        if ml['MA5'] > ml['MA10']: score += 4; signals.append('月线MA5上穿MA10')
        if ml['DIF'] > ml['DEA']: score += 5; signals.append('月线MACD金叉')
        if ml['DIF'] > 0: score += 5; signals.append('月线DIF零轴上')

    # 共振加分
    def is_bull(r):
        return r is not None and r['Close'] > r['MA5'] > r['MA10'] and r['DIF'] > r['DEA']
    d_bull, w_bull, m_bull = is_bull(dl), is_bull(wl), is_bull(ml)
    if d_bull and w_bull and m_bull: score += 15; signals.append('🌟三周期共振多')
    elif w_bull and m_bull: score += 10; signals.append('⭐周月共振')
    elif d_bull and w_bull: score += 8; signals.append('⭐日周共振')
    elif d_bull and m_bull: score += 8; signals.append('⭐日月共振')

    # 涨幅控制(防追高/避弱势)
    change_20 = None
    if len(daily) >= 20:
        change_20 = (daily['Close'].iloc[-1] / daily['Close'].iloc[-20] - 1) * 100
        if change_20 > 50: score -= 5; signals.append(f'⚠️近20日涨{change_20:.0f}%过高')
        elif change_20 > 30: score -= 2; signals.append(f'近20日涨{change_20:.0f}%注意追高')
        elif change_20 < -20: score -= 3; signals.append(f'近20日跌{change_20:.0f}%趋势弱')

    state_d = classify_period(dl)
    state_w = classify_period(wl) if wl is not None else '数据不足'
    state_m = classify_period(ml) if ml is not None else '数据不足'
    
    # checklist
    checklist_pass, checklist_details = check_checklist(daily, weekly, monthly)
    
    # 标签
    label = '回避'
    if checklist_pass and score >= 35:
        label = '推荐'
    elif checklist_pass or score >= 25:
        label = '观察'

    return {
        'name': name,
        'score': score,
        'checklist_pass': checklist_pass,
        'checklist_details': checklist_details,
        'label': label,
        'signals': signals,
        'close': dl['Close'],
        'change_20': change_20,
        'top_div': div['top_div'],
        'bot_div': div['bot_div'],
        'state': {'M': state_m, 'W': state_w, 'D': state_d},
        'daily': daily,
        'weekly': weekly,
        'monthly': monthly,
        'data_end': str(dl['Date'])[:10]
    }


# ---------------------------------------------------------------- 输出

def print_table(results):
    """表格输出（人类可读）"""
    results.sort(key=lambda x: x['score'], reverse=True)
    print(f"\n{'排名':<4}{'标的':<14}{'评分':>6}{'checklist':>10}  {'标签':<6}  {'三周期状态':<28}{'近20日':>8}  数据截止")
    print('-' * 95)
    for i, r in enumerate(results, 1):
        s = r['state']
        chg = f"{r['change_20']:+.1f}%" if r['change_20'] is not None else '—'
        chk = '✅通过' if r['checklist_pass'] else '❌未过'
        print(f"{i:<4}{r['name']:<14}{r['score']:>6}{chk:>10}  {r['label']:<6}  月{s['M']}/周{s['W']}/日{s['D']:<24}{chg:>8}  {r['data_end']}")


def print_detail(r):
    """详细输出"""
    print(f"\n{'=' * 72}\n【{r['name']}】 综合评分: {r['score']} | checklist: {'✅通过' if r['checklist_pass'] else '❌未过'} | 标签: {r['label']}")
    print(f"最新收盘: {r['close']:.2f} | 数据截止: {r['data_end']}")
    s = r['state']
    print(f"三周期状态: 月[{s['M']}] / 周[{s['W']}] / 日[{s['D']}]")
    if r['change_20'] is not None:
        print(f"近20日涨跌: {r['change_20']:.1f}%")
    print(f"触发信号: {' | '.join(r['signals'])}")
    
    cd = r['checklist_details']
    print(f"\nChecklist 明细:")
    for k, v in cd.items():
        mark = '✅' if v else '❌'
        print(f"  {mark} {k}")
    
    for label, df, key in (('月线', r['monthly'], ('MA5', 'MA10')),
                           ('周线', r['weekly'], ('MA5', 'MA10', 'MA20')),
                           ('日线', r['daily'], ('MA5', 'MA10', 'MA20', 'MA60'))):
        if len(df) == 0:
            print(f"  {label}: 数据不足")
            continue
        row = df.iloc[-1]
        parts = [f"价={row['Close']:.2f}"] + [f"{k}={row[k]:.2f}" for k in key if not pd.isna(row.get(k))]
        parts += [f"DIF={row['DIF']:.3f}", f"DEA={row['DEA']:.3f}"]
        print(f"  {label}({len(df)}根): " + ', '.join(parts))


def print_json(results):
    """JSON 输出（供 agent 解析）"""
    output = []
    for r in results:
        output.append({
            'name': r['name'],
            'score': r['score'],
            'checklist_pass': r['checklist_pass'],
            'label': r['label'],
            'state': r['state'],
            'close': float(r['close']),
            'change_20': float(r['change_20']) if r['change_20'] is not None else None,
            'top_div': r['top_div'],
            'bot_div': r['bot_div'],
            'signals': r['signals'],
            'data_end': r['data_end'],
            'checklist_details': {k: bool(v) for k, v in r['checklist_details'].items()}
        })
    print(json.dumps(output, ensure_ascii=False, indent=2))


# ---------------------------------------------------------------- 主函数

def main():
    ap = argparse.ArgumentParser(description='三周期趋势雷达 v2.0: 月/周/日线共振趋势评分')
    ap.add_argument('csv', nargs='+', help='日线 OHLCV CSV 文件(可为 ifind/yahoo 导出格式)')
    ap.add_argument('--detail', action='store_true', help='输出每标的详细三周期状态')
    ap.add_argument('--json', action='store_true', help='输出结构化 JSON（供 agent 解析）')
    ap.add_argument('--name', help='单文件模式下覆盖标的名称')
    args = ap.parse_args()

    results = []
    for path in args.csv:
        try:
            for auto_name, df in load_ohlcv(path):
                name = args.name or auto_name or path.rsplit('/', 1)[-1].replace('.csv', '')
                if len(df) < 60:
                    print(f'⚠️ {name}: 仅 {len(df)} 条日线, 月线指标可能不可靠(建议≥2年日线)', file=sys.stderr)
                results.append(three_period_radar(df, name))
        except Exception as e:
            print(f'✗ {path}: {e}', file=sys.stderr)

    if args.json:
        print_json(results)
    else:
        print_table(results)
        if args.detail:
            for r in results:
                print_detail(r)


if __name__ == '__main__':
    main()
