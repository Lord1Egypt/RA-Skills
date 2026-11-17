#!/usr/bin/env python3
"""
🗳 多模型集成投票 v1.0

核心:
  关键决策 时 让 v5.0 多个 工具 + 模型 联合投票
  • 6 个 内置 模型 各自 评分
  • 综合 投票 给出 最终 建议
  • 与 v5.0 蓝军对垒 联动

6 个 投票 模型:
  1. 财报 评分 (financial_parser)
  2. 技术 信号 (sell_signal / 突破前高)
  3. 资金 流向 (主力资金)
  4. DCF 估值 (dcf_calculator)
  5. 板块 主线 (main_line_intel)
  6. 历史 回测 (backtest_engine)

用法:
  python3 multi_model_vote.py --code 600522     # 单股 6 模型 投票
"""

import argparse
import json
import re
import sys
import urllib.parse
import urllib.request
from datetime import datetime


HOLDINGS_INFO = {
    '600522': {'name': '中天科技', 'sector': '海缆/AI 算力'},
    '000988': {'name': '华工科技', 'sector': 'CPO'},
    '300757': {'name': '罗博特科', 'sector': 'CPO / 半导体设备'},
    '688234': {'name': '天岳先进', 'sector': 'SiC'},
    '603259': {'name': '药明康德', 'sector': 'CXO'},
}


def fetch_realtime(code):
    if code.startswith(('0','3')): sym = 'sz' + code
    else: sym = 'sh' + code
    url = f"https://qt.gtimg.cn/q={sym}"
    req = urllib.request.Request(url, headers={'Referer': 'https://gu.qq.com/'})
    try:
        with urllib.request.urlopen(req, timeout=5) as r:
            text = r.read().decode('gbk', errors='ignore')
        p = text.split('~')
        return {
            'current': float(p[3]),
            'prev': float(p[4]),
            'liangbi': float(p[49]) if len(p) > 49 and p[49] else 0,
            'pe': p[39] if len(p) > 39 else '',
        }
    except: return None


def fetch_financial(code):
    url = "https://datacenter-web.eastmoney.com/api/data/v1/get"
    params = {
        'reportName': 'RPT_LICO_FN_CPD',
        'columns': 'ALL',
        'filter': f'(SECURITY_CODE="{code}")',
        'pageSize': '4',
        'sortColumns': 'REPORTDATE',
        'sortTypes': '-1',
    }
    full_url = f"{url}?{urllib.parse.urlencode(params)}"
    req = urllib.request.Request(full_url, headers={'User-Agent': 'Mozilla/5.0', 'Referer': 'https://data.eastmoney.com/'})
    try:
        with urllib.request.urlopen(req, timeout=10) as r:
            data = json.loads(r.read().decode('utf-8'))
        if data.get('success'):
            return data.get('result', {}).get('data', [])
    except: pass
    return []


def fetch_kline(code, days=60):
    if code.startswith(('0','3')): sym = 'sz' + code
    else: sym = 'sh' + code
    url = f"https://web.ifzq.gtimg.cn/appstock/app/fqkline/get?param={sym},day,,,{days+5},qfq"
    req = urllib.request.Request(url, headers={'Referer': 'https://gu.qq.com/'})
    try:
        with urllib.request.urlopen(req, timeout=10) as r:
            text = r.read().decode('utf-8', errors='ignore')
        text = re.sub(r'^[\s\S]*?=\s*', '', text).rstrip(';)')
        inner = json.loads(text).get('data', {}).get(sym, {})
        for k in ['qfqday','day']:
            if k in inner and inner[k]:
                return [{'date': r[0], 'close': float(r[2]), 'high': float(r[3]), 'low': float(r[4]), 'vol': float(r[5])} for r in inner[k]]
    except: pass
    return []


def vote_financial(code):
    """模型 1: 财报评分"""
    data = fetch_financial(code)
    if not data: return None, "数据无"
    
    latest = data[0]
    rev_yoy = float(latest.get('YSTZ', 0) or 0)
    net_yoy = float(latest.get('SJLTZ', 0) or 0)
    roe = float(latest.get('WEIGHTAVG_ROE', 0) or 0)
    
    score = 0
    if rev_yoy > 30: score += 30
    elif rev_yoy > 10: score += 20
    elif rev_yoy > 0: score += 10
    if net_yoy > 30: score += 30
    elif net_yoy > 0: score += 20
    if roe > 15: score += 30
    elif roe > 10: score += 20
    elif roe > 5: score += 10
    
    if score >= 70: vote = '强买'
    elif score >= 50: vote = '买'
    elif score >= 30: vote = '中性'
    else: vote = '不买'
    
    return score, f"营收+{rev_yoy:.0f}% 净利+{net_yoy:.0f}% ROE{roe:.1f}% → {vote}"


def vote_technical(code):
    """模型 2: 技术信号"""
    klines = fetch_kline(code, 60)
    if not klines or len(klines) < 30: return None, "K线无"
    
    current = klines[-1]['close']
    closes = [k['close'] for k in klines]
    ma20 = sum(closes[-20:]) / 20
    
    score = 0
    if current > ma20: score += 30
    
    # 突破 60 日前高
    prev_60 = klines[:-1] if len(klines) > 60 else klines[:-1]
    if prev_60:
        prev_high = max(k['high'] for k in prev_60[-60:])
        if current >= prev_high * 0.99:
            score += 40
        elif current >= prev_high * 0.95:
            score += 20
    
    # 5 日上涨 趋势
    if klines[-1]['close'] > klines[-5]['close']:
        score += 15
    
    # 量比
    avg_vol = sum(k['vol'] for k in klines[-20:]) / 20
    if klines[-1]['vol'] > avg_vol * 1.5:
        score += 15
    
    if score >= 70: vote = '强买'
    elif score >= 50: vote = '买'
    elif score >= 30: vote = '中性'
    else: vote = '不买'
    
    return score, f"MA20 {ma20:.1f} / 现价 {current:.1f} → {vote}"


def vote_capital_flow(code):
    """模型 3: 资金流向 (简化)"""
    # 简化 用 量比 代替
    rt = fetch_realtime(code)
    if not rt: return None, "无"
    
    lb = rt['liangbi']
    chg = (rt['current'] - rt['prev']) / rt['prev'] * 100
    
    score = 0
    if lb >= 2: score += 30
    elif lb >= 1.5: score += 20
    elif lb >= 1: score += 10
    
    if chg > 3: score += 40
    elif chg > 0: score += 20
    elif chg > -3: score += 10
    
    if score >= 60: vote = '强买'
    elif score >= 40: vote = '买'
    elif score >= 20: vote = '中性'
    else: vote = '不买'
    
    return score, f"量比 {lb:.2f} 今涨 {chg:+.2f}% → {vote}"


def vote_dcf(code):
    """模型 4: DCF 估值 (简化版)"""
    # 简化: 用 PE 估算
    rt = fetch_realtime(code)
    if not rt or not rt['pe']: return None, "PE 无"
    try:
        pe = float(rt['pe'])
    except: return None, "PE 解析失败"
    
    score = 0
    if 0 < pe < 30: score += 60
    elif pe < 60: score += 40
    elif pe < 100: score += 20
    elif pe < 200: score += 10
    else: score += 0
    
    if score >= 40: vote = '买'
    elif score >= 20: vote = '中性'
    else: vote = '不买'
    
    return score, f"PE {pe:.1f} → {vote}"


def vote_sector_main_line(code, sector_hint):
    """模型 5: 板块主线"""
    # 用 板块 名 关键词 简化
    sector_keywords = {
        '半导体': 'BK0480',
        'CPO': 'CPO',
        '光通信': '光通信',
        'AI': 'AI',
        'SiC': 'SiC',
        'CXO': 'CXO',
        '海缆': '海缆',
    }
    
    # 简化: 用 持仓 板块 直接 配对
    score = 50  # 默认 中性
    sector_name = sector_hint.split('/')[0].strip() if '/' in sector_hint else sector_hint
    
    # 实际 应该 调 main_line_intel
    note = f"板块 {sector_name} (待 联动 main_line_intel)"
    return score, note


def vote_backtest(code):
    """模型 6: 历史回测 (简化)"""
    # 看 近 6 个月 表现
    klines = fetch_kline(code, 120)
    if not klines or len(klines) < 60: return None, "无"
    
    start = klines[0]['close']
    end = klines[-1]['close']
    total_ret = (end - start) / start * 100
    
    # 最大 回撤
    peak = klines[0]['high']
    max_dd = 0
    for k in klines:
        if k['high'] > peak: peak = k['high']
        dd = (k['low'] - peak) / peak * 100
        if dd < max_dd: max_dd = dd
    
    score = 0
    if total_ret > 30: score += 40
    elif total_ret > 10: score += 25
    elif total_ret > 0: score += 10
    
    if max_dd > -10: score += 30
    elif max_dd > -20: score += 20
    elif max_dd > -30: score += 10
    
    if score >= 50: vote = '买'
    elif score >= 30: vote = '中性'
    else: vote = '不买'
    
    return score, f"近 6 月 {total_ret:+.1f}% / 最大回撤 {max_dd:.1f}% → {vote}"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--code', required=True, help='股票代码')
    args = parser.parse_args()
    
    code = args.code
    info = HOLDINGS_INFO.get(code, {'name': code, 'sector': '未知'})
    
    print(f"🗳 多模型集成投票 v1.0")
    print(f"📌 {info['name']} ({code}) - {info['sector']}")
    print(f"⏰ {datetime.now():%Y-%m-%d %H:%M}")
    print()
    
    models = [
        ('财报评分', vote_financial),
        ('技术信号', vote_technical),
        ('资金流向', vote_capital_flow),
        ('DCF 估值', vote_dcf),
        ('板块主线', lambda c: vote_sector_main_line(c, info['sector'])),
        ('历史回测', vote_backtest),
    ]
    
    print("=" * 65)
    print(f"{'模型':<14s} {'分数':>5s}  评估")
    print("=" * 65)
    
    total_score = 0
    valid_count = 0
    votes = []
    
    for name, fn in models:
        try:
            score, note = fn(code)
            if score is None:
                print(f"  {name:<12s} {'N/A':>5s}  {note}")
                continue
            
            total_score += score
            valid_count += 1
            
            # 投票
            if score >= 60: vote = '🟢 买'; votes.append('买')
            elif score >= 40: vote = '🟡 中性'; votes.append('中')
            else: vote = '🔴 不买'; votes.append('不买')
            
            print(f"  {name:<12s} {score:>4d}  {vote} | {note}")
        except Exception as e:
            print(f"  {name:<12s} {'ERR':>5s}  {e}")
    
    # 综合 投票 结果
    print()
    print("=" * 65)
    print("🏆 综合 投票 结果")
    print("=" * 65)
    
    if valid_count > 0:
        avg_score = total_score / valid_count
        buy_count = votes.count('买')
        neutral_count = votes.count('中')
        nobuy_count = votes.count('不买')
        
        print(f"\n  📊 6 模型 投票:")
        print(f"     🟢 买: {buy_count} 票")
        print(f"     🟡 中性: {neutral_count} 票")
        print(f"     🔴 不买: {nobuy_count} 票")
        print(f"\n  📈 平均得分: {avg_score:.1f}/100")
        
        if avg_score >= 65 and buy_count >= 3:
            final = '🚀 强烈买入'
        elif avg_score >= 50:
            final = '🟢 买入'
        elif avg_score >= 35:
            final = '🟡 中性 / 持有'
        elif avg_score >= 20:
            final = '🔴 减仓'
        else:
            final = '🚨 强烈减仓 / 退出'
        
        print(f"\n  💎 最终 决策: {final}")
        
        # 共识 vs 分歧
        if buy_count >= 4:
            print(f"  ✅ 高度 共识 ({buy_count}/{valid_count} 买入)")
        elif buy_count >= 3 and nobuy_count >= 2:
            print(f"  ⚠️ 模型 分歧 / 谨慎 决策")
        elif nobuy_count >= 4:
            print(f"  ❌ 高度 共识 不看好")


if __name__ == '__main__':
    main()
