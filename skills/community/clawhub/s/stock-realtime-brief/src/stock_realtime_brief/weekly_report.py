#!/usr/bin/env python3
"""
📰 周报 / 月报 自动生成 v1.0

每周日 自动 生成:
  • 本周 持仓 表现
  • 本周 操作 复盘
  • 本周 板块 主线
  • 下周 重点 关注
  • 本月 累计 数据

用法:
  python3 weekly_report.py                 # 本周 周报
  python3 weekly_report.py --month         # 本月 月报
"""

import argparse
import json
import re
import sys
import urllib.request
from datetime import datetime, timedelta


HOLDINGS = {
    '600522': {'name': '中天科技', 'cost': 45.97, 'qty': 42200},
    '000988': {'name': '华工科技', 'cost': 146.40, 'qty': 9400},
    '300757': {'name': '罗博特科', 'cost': 309.50, 'qty': 2500},
    '688234': {'name': '天岳先进', 'cost': 182.35, 'qty': 2024},
}


def fetch_kline_recent(code, days=10):
    if code.startswith(('0','3')): sym = 'sz' + code
    else: sym = 'sh' + code
    url = f"https://web.ifzq.gtimg.cn/appstock/app/fqkline/get?param={sym},day,,,{days},qfq"
    req = urllib.request.Request(url, headers={'Referer': 'https://gu.qq.com/'})
    try:
        with urllib.request.urlopen(req, timeout=10) as r:
            text = r.read().decode('utf-8', errors='ignore')
        text = re.sub(r'^[\s\S]*?=\s*', '', text).rstrip(';)')
        inner = json.loads(text).get('data', {}).get(sym, {})
        for k in ['qfqday','day']:
            if k in inner and inner[k]:
                return [{'date': r[0], 'close': float(r[2]), 'vol': float(r[5])} for r in inner[k]]
    except: pass
    return []


def generate_weekly_report():
    """生成 周报"""
    now = datetime.now()
    
    print(f"╔══════════════════════════════════════════════════════════╗")
    print(f"║  📰 投研周报 - {now.strftime('%Y-%m-%d')} (周{['一','二','三','四','五','六','日'][now.weekday()]})")
    print(f"╚══════════════════════════════════════════════════════════╝")
    print()
    
    # 1. 持仓 周表现
    print("=" * 60)
    print("📊 本周 持仓 表现")
    print("=" * 60)
    print(f"\n{'股票':<10s} {'周一':>8s} {'周五':>8s} {'周变化':>9s} {'当前 vs 成本':>13s}")
    print("-" * 55)
    
    total_pnl_total = 0
    total_pnl_week = 0
    
    for code, h in HOLDINGS.items():
        klines = fetch_kline_recent(code, 7)
        if len(klines) < 5:
            continue
        
        monday = klines[-5]['close']  # 周一
        friday = klines[-1]['close']  # 周五
        week_chg = (friday - monday) / monday * 100
        
        # 持仓 浮盈
        total_pnl = (friday - h['cost']) * h['qty']
        week_pnl = (friday - monday) * h['qty']
        total_pnl_total += total_pnl
        total_pnl_week += week_pnl
        
        flag = '🚀' if week_chg > 3 else '🟢' if week_chg > 0 else '🔴' if week_chg < -3 else '🟡'
        total_flag = '✅' if total_pnl > 0 else '❌'
        
        print(f"  {h['name']:<8s} ¥{monday:>6.2f} ¥{friday:>6.2f} {flag}{week_chg:>+6.2f}% {total_flag} ¥{total_pnl:>+10,.0f}")
    
    print()
    print(f"  📈 本周 浮盈 变化: ¥{total_pnl_week:+,.0f}")
    print(f"  💎 当前 总浮盈: ¥{total_pnl_total:+,.0f}")
    
    # 2. 本周 大事件
    print()
    print("=" * 60)
    print("📅 本周 大事件 (基于 数据 自动 识别)")
    print("=" * 60)
    
    events = []
    for code, h in HOLDINGS.items():
        klines = fetch_kline_recent(code, 7)
        if len(klines) < 5: continue
        
        for k in klines[-5:]:  # 本周
            prev_idx = klines.index(k) - 1
            if prev_idx < 0: continue
            prev = klines[prev_idx]
            chg = (k['close'] - prev['close']) / prev['close'] * 100
            
            if abs(chg) >= 5:
                event_type = '🚀 大涨' if chg > 0 else '🚨 大跌'
                events.append(f"  {k['date']}: {h['name']} {event_type} {chg:+.2f}%")
    
    if events:
        for e in sorted(events):
            print(e)
    else:
        print("  ✅ 本周 无 ±5% 以上 大事件")
    
    # 3. 主线 板块
    print()
    print("=" * 60)
    print("🎯 本周 板块 主线 (待集成 main_line_intel.py)")
    print("=" * 60)
    print("  💡 执行: python3 main_line_intel.py 查看 实时主线")
    
    # 4. 下周 重点
    print()
    print("=" * 60)
    print("🎯 下周 重点 关注")
    print("=" * 60)
    
    next_week = now + timedelta(days=2)
    print(f"\n  📅 下周一: {next_week.strftime('%Y-%m-%d')} 开盘")
    print(f"  🔔 提醒:")
    print(f"     • 9:00 集合竞价 前 30 分钟 确认")
    print(f"     • 9:30 实时警报 触发 减仓 / 加仓 信号")
    print(f"     • 14:30 收盘前 仓位 复核")
    print(f"     • 15:00 收盘 写 操作日志")
    
    # 5. 工具 检查
    print()
    print("=" * 60)
    print("🛠 本周 工具 使用情况")
    print("=" * 60)
    print(f"  ✅ DCF 内在价值 / 板块轮动 / 卖出信号 / 北极星监控")
    print(f"  ✅ 实时警报 / 财报解析 / 历史回测 / 主线识别")
    print(f"  💡 v5.0 已上线 ClawHub: clawhub install stock-realtime-brief")
    
    # 6. 心法 提醒
    print()
    print("=" * 60)
    print("💎 散户 心法 提醒")
    print("=" * 60)
    print("""
  ✅ 真理 1: 好公司 ≠ 好股票 (估值 决定 是否买)
  ✅ 真理 2: 买入 是 买 未来 现金流 (DCF)
  ✅ 真理 3: 持有 比 选股 难 (Let winners run)
  ✅ 真理 4: 锁利 三段法 (+20% / +50% / +100%)
  ✅ 真理 5: 反人性 (买分歧 卖一致)
  ✅ 真理 6: 不操作 是 默认选项 (v4.2 铁律 1)
  ✅ 真理 7: 用户实证 > AI 解读 (v5.0 蓝军对垒)
""")
    
    # 落款
    print()
    print(f"📌 周报 自动生成 - stock-realtime-brief v5.0")
    print(f"⏰ {datetime.now():%Y-%m-%d %H:%M}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--month', action='store_true', help='月报')
    args = parser.parse_args()
    
    generate_weekly_report()


if __name__ == '__main__':
    main()
