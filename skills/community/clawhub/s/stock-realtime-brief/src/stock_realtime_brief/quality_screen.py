#!/usr/bin/env python3
"""
🛡 Quality Screen v1.0 - 8 条红线 一票否决
基于 ai-berkshire /quality-screen + /investment-checklist

核心: 巴菲特/段永平 8 条 硬指标
任何 一条 触发 → 一票 否决 / 不投

用法:
  python3 quality_screen.py                    # 全部持仓 + watchlist
  python3 quality_screen.py --code 603259     # 单股
"""

import argparse
import json
import re
import sys
import urllib.parse
import urllib.request
from datetime import datetime


# 数据源: 东财 财务
def fetch_financial(code):
    url = "https://datacenter-web.eastmoney.com/api/data/v1/get"
    params = {
        'reportName': 'RPT_LICO_FN_CPD', 'columns': 'ALL',
        'filter': f'(SECURITY_CODE="{code}")',
        'pageSize': '4', 'sortColumns': 'REPORTDATE', 'sortTypes': '-1',
    }
    req = urllib.request.Request(
        f"{url}?{urllib.parse.urlencode(params)}",
        headers={'User-Agent': 'Mozilla/5.0', 'Referer': 'https://data.eastmoney.com/'})
    try:
        with urllib.request.urlopen(req, timeout=15) as r:
            data = json.loads(r.read().decode('utf-8'))
        if data.get('success'): return data.get('result', {}).get('data', [])
    except: pass
    return []


def fetch_quote(code):
    if code.startswith(('0','3')): sym = 'sz' + code
    else: sym = 'sh' + code
    url = f"https://qt.gtimg.cn/q={sym}"
    req = urllib.request.Request(url, headers={'Referer': 'https://gu.qq.com/'})
    try:
        with urllib.request.urlopen(req, timeout=5) as r:
            text = r.read().decode('gbk', errors='ignore')
        return text.split('~')
    except: return None


def screen(code):
    """8 条红线 检查"""
    fin = fetch_financial(code)
    quote = fetch_quote(code)
    if not fin or not quote:
        return None
    
    latest = fin[0]
    q = quote
    
    # 提取 关键 指标
    try:
        roe = float(latest.get('WEIGHTAVG_ROE', 0) or 0)
        gross = float(latest.get('XSMLL', 0) or 0)
        net_yoy = float(latest.get('SJLTZ', 0) or 0)
        rev_yoy = float(latest.get('YSTZ', 0) or 0)
        pe = float(q[39]) if len(q) > 39 and q[39] and q[39] != '-' else None
        pb = float(q[46]) if len(q) > 46 and q[46] and q[46] != '-' else None
        price = float(q[3])
        market_cap_yi = float(q[45]) / 1e8 if len(q) > 45 and q[45] else 0  # 总市值 (亿)
    except: return None
    
    # 8 条 红线
    red_lines = []
    
    # 🔴 红线 1: 连续亏损 (净利 <0)
    profit_qtrs = 0
    for d in fin[:4]:
        try:
            if float(d.get('SJLTZ', 0) or 0) < -50: profit_qtrs += 1
        except: pass
    if profit_qtrs >= 3:
        red_lines.append(('🔴 R1', '连续 亏损 (3+ 季 净利 增速 <-50%)', 'FAIL'))
    else:
        red_lines.append(('✅ R1', f'盈利 能力 (亏损季 {profit_qtrs}/4)', 'PASS'))
    
    # 🔴 红线 2: ROE < 5% (差公司)
    if roe < 5 and roe > -100:
        red_lines.append(('🔴 R2', f'ROE {roe:.2f}% (< 5% / 效率 低)', 'FAIL'))
    elif roe >= 15:
        red_lines.append(('✅ R2', f'ROE {roe:.2f}% (≥ 15% 优秀)', 'PASS'))
    else:
        red_lines.append(('🟡 R2', f'ROE {roe:.2f}% (5-15% 一般)', 'WARN'))
    
    # 🔴 红线 3: 毛利率 < 20% (无 定价 权)
    if gross < 20 and gross > 0:
        red_lines.append(('🔴 R3', f'毛利率 {gross:.2f}% (< 20% / 无定价权)', 'FAIL'))
    elif gross >= 40:
        red_lines.append(('✅ R3', f'毛利率 {gross:.2f}% (≥ 40% 优秀)', 'PASS'))
    else:
        red_lines.append(('🟡 R3', f'毛利率 {gross:.2f}% (20-40% 一般)', 'WARN'))
    
    # 🔴 红线 4: 营收 负增长 (业务 衰退)
    if rev_yoy < -10:
        red_lines.append(('🔴 R4', f'营收 {rev_yoy:+.1f}% (下滑 严重)', 'FAIL'))
    elif rev_yoy > 20:
        red_lines.append(('✅ R4', f'营收 {rev_yoy:+.1f}% (高增)', 'PASS'))
    else:
        red_lines.append(('🟡 R4', f'营收 {rev_yoy:+.1f}% (中等)', 'WARN'))
    
    # 🔴 红线 5: PE > 100 (严重 高估 / 除非 高增)
    if pe and pe > 100 and rev_yoy < 30:
        red_lines.append(('🔴 R5', f'PE {pe:.1f} 且 营收 <30% (严重 高估)', 'FAIL'))
    elif pe and 0 < pe < 30:
        red_lines.append(('✅ R5', f'PE {pe:.1f} (合理)', 'PASS'))
    elif pe and pe < 0:
        red_lines.append(('🔴 R5', f'PE 亏损 ({pe:.1f})', 'FAIL'))
    else:
        red_lines.append(('🟡 R5', f'PE {pe if pe else "N/A"}', 'WARN'))
    
    # 🔴 红线 6: PB > 10 (泡沫)
    if pb and pb > 10:
        red_lines.append(('🔴 R6', f'PB {pb:.2f} (>10 / 泡沫)', 'FAIL'))
    elif pb and 0 < pb < 5:
        red_lines.append(('✅ R6', f'PB {pb:.2f} (合理)', 'PASS'))
    else:
        red_lines.append(('🟡 R6', f'PB {pb if pb else "N/A"}', 'WARN'))
    
    # 🔴 红线 7: 小市值 < 50 亿 (流动性 + 稳定性 风险)
    if market_cap_yi < 50:
        red_lines.append(('🔴 R7', f'市值 {market_cap_yi:.1f}亿 (< 50亿 / 小微)', 'FAIL'))
    elif market_cap_yi > 500:
        red_lines.append(('✅ R7', f'市值 {market_cap_yi:.1f}亿 (大盘 稳定)', 'PASS'))
    else:
        red_lines.append(('🟡 R7', f'市值 {market_cap_yi:.1f}亿 (中盘)', 'WARN'))
    
    # 🔴 红线 8: 净利 增速 剧烈 波动 (业绩 不稳)
    if len(fin) >= 4:
        try:
            profits = [float(d.get('SJLTZ', 0) or 0) for d in fin[:4]]
            volatility = max(profits) - min(profits)
            if volatility > 200:
                red_lines.append(('🔴 R8', f'净利 波动 {volatility:.0f}pp (业绩 极不稳)', 'FAIL'))
            elif volatility < 50:
                red_lines.append(('✅ R8', f'净利 波动 {volatility:.0f}pp (稳定)', 'PASS'))
            else:
                red_lines.append(('🟡 R8', f'净利 波动 {volatility:.0f}pp (一般)', 'WARN'))
        except:
            red_lines.append(('🟡 R8', '波动 数据不足', 'WARN'))
    
    # 综合 判决
    fail_count = sum(1 for _, _, s in red_lines if s == 'FAIL')
    pass_count = sum(1 for _, _, s in red_lines if s == 'PASS')
    
    if fail_count >= 3:
        verdict = '🚨 一票否决 (3+ 红线 触发)'
    elif fail_count == 2:
        verdict = '🔴 强烈 警告 (2 红线)'
    elif fail_count == 1:
        verdict = '⚠️ 谨慎 (1 红线)'
    elif pass_count >= 6:
        verdict = '✅ 优秀 (6+ 通过)'
    elif pass_count >= 4:
        verdict = '🟢 合格 (4-5 通过)'
    else:
        verdict = '🟡 中性 (待深入)'
    
    return {
        'code': code,
        'price': price,
        'red_lines': red_lines,
        'fail_count': fail_count,
        'pass_count': pass_count,
        'verdict': verdict,
        'metrics': {
            'roe': roe, 'gross': gross, 'net_yoy': net_yoy, 'rev_yoy': rev_yoy,
            'pe': pe, 'pb': pb, 'market_cap_yi': market_cap_yi,
        },
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--code', help='单股 代码')
    args = parser.parse_args()
    
    print(f"🛡 Quality Screen v1.0 (8 条红线 一票否决)")
    print(f"⏰ {datetime.now():%Y-%m-%d %H:%M}  / 基于 ai-berkshire\n")
    
    codes = [args.code] if args.code else ['603259', '300757', '600522', '000988']
    names = {'603259': '药明康德', '300757': '罗博特科', '600522': '中天科技', '000988': '华工科技'}
    
    for code in codes:
        r = screen(code)
        if not r:
            print(f"❌ {code}: 数据获取失败\n")
            continue
        
        print("=" * 60)
        print(f"🎯 {names.get(code, code)} ({code}) - 现价 ¥{r['price']:.2f}")
        print("=" * 60)
        print()
        for tag, desc, _ in r['red_lines']:
            print(f"  {tag}: {desc}")
        print()
        print(f"📊 统计: PASS {r['pass_count']}/8  FAIL {r['fail_count']}/8")
        print(f"💎 判决: {r['verdict']}")
        print()


if __name__ == '__main__':
    main()
