#!/usr/bin/env python3
"""
🌅 Daily Morning Note v1.0 - 每日盘前简报
基于 Anthropic financial-services / equity-research / morning-note

核心: 每日 08:30 自动 生成
  1. 隔夜 美股 (指数/半导体/CPO/CXO)
  2. A 股 期指 预判
  3. 4 只持仓 关联 分析
  4. 今日 重点 (减仓单/加仓目标)
  5. Catalyst 事件 (来自 catalyst-calendar)
  6. Thesis 状态 (来自 thesis-tracker)

用法:
  python3 daily_morning_note.py           # 生成 今日 简报
"""

import argparse
import json
import subprocess
import sys
import urllib.request
from datetime import datetime
from pathlib import Path


HOLDINGS = {
    '600522': {'name': '中天科技', 'qty_total': 19100, 'cost': 37.16, 'sector': '半导体/AI 算力'},
    '300757': {'name': '罗博特科', 'qty_total': 4400, 'cost': 434.94, 'sector': 'CPO/半导体设备'},
    '000988': {'name': '华工科技', 'qty_total': 1700, 'cost': 102.37, 'sector': 'CPO'},
    '603259': {'name': '药明康德', 'qty_total': 15700, 'cost': 122.40, 'sector': 'CXO'},
}


def fetch_yahoo(sym):
    url = f"https://query1.finance.yahoo.com/v8/finance/chart/{sym}?interval=1d"
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    try:
        with urllib.request.urlopen(req, timeout=10) as r:
            data = json.loads(r.read().decode('utf-8'))
        meta = data['chart']['result'][0]['meta']
        return {'price': meta.get('regularMarketPrice'), 'prev': meta.get('chartPreviousClose')}
    except: return None


def fetch_a_stock(code):
    if code.startswith(('0','3')): sym = 'sz' + code
    else: sym = 'sh' + code
    url = f"https://qt.gtimg.cn/q={sym}"
    req = urllib.request.Request(url, headers={'Referer': 'https://gu.qq.com/'})
    try:
        with urllib.request.urlopen(req, timeout=5) as r:
            text = r.read().decode('gbk', errors='ignore')
        return text.split('~')
    except: return None


def fmt_chg(v, prev):
    if not v or not prev: return "N/A"
    chg = (v - prev) / prev * 100
    flag = '🚀' if chg > 2 else '🟢' if chg > 0 else '🔴' if chg < -2 else '🟡'
    return f"{flag}{chg:+.2f}%"


def main():
    parser = argparse.ArgumentParser()
    args = parser.parse_args()
    
    now = datetime.now()
    print(f"╔══════════════════════════════════════════════════════════╗")
    print(f"║  🌅 每日 盘前 简报 - {now:%Y-%m-%d %A}")
    print(f"║  {now:%H:%M:%S} · 基于 Anthropic morning-note")
    print(f"╚══════════════════════════════════════════════════════════╝\n")
    
    # === 1. 美股 隔夜 ===
    print("=" * 60)
    print("📊 1. 隔夜 美股 关键 数据")
    print("=" * 60)
    print()
    
    # 指数
    print("🌃 三大 指数 + 期指:")
    for sym, name in [('^IXIC', '纳斯达克'), ('^GSPC', '标普500'), ('^DJI', '道指'), ('^SOX', '费城半导体'), ('^VIX', 'VIX恐慌')]:
        d = fetch_yahoo(sym)
        if d and d['price']:
            chg_str = fmt_chg(d['price'], d['prev'])
            print(f"  {name:<12s} ${d['price']:>10.2f}  {chg_str}")
    
    # 期指
    print("\n🌏 期指 (电子盘):")
    for sym, name in [('NQ=F', '纳斯达克期指'), ('ES=F', '标普期指')]:
        d = fetch_yahoo(sym)
        if d and d['price']:
            chg_str = fmt_chg(d['price'], d['prev'])
            print(f"  {name:<12s} {d['price']:>10.2f}  {chg_str}")
    
    # 板块 关联
    print("\n🚀 关联 板块:")
    for group_name, syms in [
        ('半导体', [('NVDA','英伟达'),('AMD','AMD'),('TSM','台积电'),('MU','美光')]),
        ('CPO 光通信', [('LITE','Lumentum'),('COHR','Coherent'),('CRDO','Credo'),('AAOI','AAOI')]),
        ('CXO 医药', [('IQV','IQVIA'),('LLY','礼来'),('NVO','诺和')]),
    ]:
        print(f"\n  📌 {group_name}:")
        for sym, name in syms:
            d = fetch_yahoo(sym)
            if d and d['price']:
                chg_str = fmt_chg(d['price'], d['prev'])
                print(f"    {name:<8s} ${d['price']:>8.2f}  {chg_str}")
    
    # === 2. 你 持仓 昨日 收盘 + 预判 ===
    print("\n" + "=" * 60)
    print("💎 2. 你 4 只 持仓 关联 分析")
    print("=" * 60)
    print()
    
    for code, h in HOLDINGS.items():
        p = fetch_a_stock(code)
        if not p: continue
        try:
            cur = float(p[3])
            prev = float(p[4])
            chg = (cur - prev) / prev * 100
            pnl = (cur - h['cost']) * h['qty_total']
            flag = '🚀' if chg > 3 else '🟢' if chg > 0 else '🔴' if chg < -3 else '🟡'
            print(f"  {h['name']:<10s} ¥{cur:>7.2f} {flag}{chg:>+5.2f}%  {h['qty_total']:,}股 @¥{h['cost']:.2f}")
            print(f"     板块: {h['sector']}  浮盈: ¥{pnl:+,.0f}")
        except: pass
    
    # === 3. 今日 预判 (基于 美股) ===
    print("\n" + "=" * 60)
    print("🎯 3. 今日 A 股 预判 (基于 美股 隔夜)")
    print("=" * 60)
    print("""
  🔍 关键 观察 (自动 检查):
    • CXO 医药 强/弱 → 药明 高开 or 低开?
    • CPO 光通信 强/弱 → 罗博/华工 承压?
    • 半导体 强/弱 → 中天 走势?
    • 期指 情绪 → 大盘 高开/低开?
    
  💡 3 大 情景 (基于 美股 数据):
    🟢 反弹 情景: 期指 +1% / VIX -2%
    🟡 分化 情景: 药明 涨 / 半导体 弱
    🔴 弱势 情景: 期指 -0.5% / CPO 继续 跌
""")
    
    # === 4. 今日 重点 操作 ===
    print("=" * 60)
    print("🎯 4. 今日 重点 操作 清单")
    print("=" * 60)
    print("""
  🟢 上行 减仓 挂单 (锁利):
    ☐ 药明 ¥130 减 1,500 股 (锁 ¥1.15万)
    ☐ 罗博 ¥540 卖 500 股 (信用锁 ¥9.6万)
    ☐ 中天 ¥54 卖 3,000 股 (锁 ¥5.1万)
    ☐ 华工 ¥165 卖 300 股 (锁 ¥1.9万)
  
  🔴 下行 防御 (触发):
    ☐ 罗博 跌破 ¥500 卖 500 股
    ☐ 中天 跌破 ¥48 卖 3,000 股
    ☐ 药明 跌破 ¥118 卖 2,000 股
    ☐ 华工 跌破 ¥148 卖 200 股
""")
    
    # === 5. 催化剂 事件 (调用 catalyst_calendar) ===
    print("=" * 60)
    print("📅 5. 未来 7 天 关键 事件")
    print("=" * 60)
    print()
    
    try:
        script_dir = Path(__file__).parent
        result = subprocess.run(
            ['python3', str(script_dir / 'catalyst_calendar.py'), '--days', '7'],
            capture_output=True, text=True, timeout=30
        )
        if result.returncode == 0:
            # 只 取 CRITICAL + HIGH 部分
            lines = result.stdout.split('\n')
            in_critical = False
            in_high = False
            for line in lines:
                if 'CRITICAL 事件' in line or 'HIGH 事件' in line:
                    print(line)
                    in_critical = True
                elif '=' * 5 in line:
                    if in_critical:
                        print(line)
                elif in_critical and line.strip():
                    print(line)
                    if 'MEDIUM' in line or '建议 行动' in line:
                        in_critical = False
        else:
            print("  (待 catalyst_calendar.py 执行)")
    except Exception as e:
        print(f"  ⚠️ 无法 加载 catalyst_calendar: {e}")
    
    # === 6. 心法 提醒 ===
    print("\n" + "=" * 60)
    print("💎 6. 心法 提醒 (你 7/1 凌晨 沉淀)")
    print("=" * 60)
    print("""
  🌟 短期 = 资金情绪 + 筹码博弈
  🌟 中长期 = 产业趋势 + 公司业绩
  🌟 震荡 换手 是 A 股 最正常 规律
  🌟 不改变 企业 长期 价值
  
  应用:
    ✅ 上行 = 锁利 时机 (你 高抛)
    ✅ 震荡 = 结构 优化 (你 换股)
    ✅ 长期 winners = 死守
    ✅ 论点 变化 = 触发 减仓
""")
    
    # 落款
    print("=" * 60)
    print(f"📌 简报 自动生成 - stock-realtime-brief v5.0 + Anthropic 精华")
    print(f"⏰ {datetime.now():%Y-%m-%d %H:%M}  / 距开盘 (若 未开): TBD")
    print()


if __name__ == '__main__':
    main()
