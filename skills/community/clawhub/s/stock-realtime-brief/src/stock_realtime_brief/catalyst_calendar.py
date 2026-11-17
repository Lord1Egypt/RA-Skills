#!/usr/bin/env python3
"""
📅 Catalyst Calendar v1.0 - 催化剂 日历
基于 Anthropic financial-services / equity-research / catalyst-calendar

核心: 追踪 4 只 持仓 + Watchlist 关键 时间 节点
提前 提醒 T-7 / T-3 / T-1

用法:
  python3 catalyst_calendar.py              # 未来 60 天 所有 事件
  python3 catalyst_calendar.py --days 30    # 未来 30 天
"""

import argparse
from datetime import datetime, timedelta

CATALYSTS = [
    # 药明康德 (603259)
    {'date': '2026-07-15', 'code': '603259', 'name': '药明康德', 'type': 'earnings_preview',
     'event': 'Q2 业绩预告 (7 月中)', 'importance': 'HIGH'},
    {'date': '2026-08-30', 'code': '603259', 'name': '药明康德', 'type': 'earnings',
     'event': 'Q2 半年报 披露', 'importance': 'CRITICAL'},
    {'date': '2026-10-30', 'code': '603259', 'name': '药明康德', 'type': 'earnings',
     'event': 'Q3 财报', 'importance': 'HIGH'},
    {'date': '2026-12-28', 'code': '603259', 'name': '药明康德', 'type': 'debt_expiry',
     'event': '融资 ¥52 万 到期 (4,200 股 / 12/28)', 'importance': 'CRITICAL'},
    
    # 罗博特科 (300757)
    {'date': '2026-07-15', 'code': '300757', 'name': '罗博特科', 'type': 'earnings_preview',
     'event': 'Q2 业绩预告 (光电子拐点验证)', 'importance': 'CRITICAL'},
    {'date': '2026-08-30', 'code': '300757', 'name': '罗博特科', 'type': 'earnings',
     'event': 'Q2 半年报 (业绩拐点!)', 'importance': 'CRITICAL'},
    {'date': '2026-09-30', 'code': '300757', 'name': '罗博特科', 'type': 'other',
     'event': 'H 股 上市 进展 (预计 Q3-Q4)', 'importance': 'HIGH'},
    {'date': '2026-10-30', 'code': '300757', 'name': '罗博特科', 'type': 'earnings',
     'event': 'Q3 财报', 'importance': 'HIGH'},
    
    # 中天科技 (600522)
    {'date': '2026-07-15', 'code': '600522', 'name': '中天科技', 'type': 'earnings_preview',
     'event': 'Q2 业绩预告', 'importance': 'HIGH'},
    {'date': '2026-08-30', 'code': '600522', 'name': '中天科技', 'type': 'earnings',
     'event': 'Q2 半年报', 'importance': 'HIGH'},
    
    # 华工科技 (000988)
    {'date': '2026-07-15', 'code': '000988', 'name': '华工科技', 'type': 'earnings_preview',
     'event': 'Q2 业绩预告', 'importance': 'HIGH'},
    {'date': '2026-08-30', 'code': '000988', 'name': '华工科技', 'type': 'earnings',
     'event': 'Q2 半年报 (CPO 兑现)', 'importance': 'HIGH'},
    
    # 行业 事件
    {'date': '2026-07-30', 'code': None, 'name': '英伟达', 'type': 'industry',
     'event': '英伟达 Q2 财报 (北京 隔夜) - CPO/AI 定调', 'importance': 'CRITICAL'},
    {'date': '2026-08-20', 'code': None, 'name': 'Lumentum', 'type': 'industry',
     'event': 'Lumentum 财报 (罗博 上游 客户)', 'importance': 'HIGH'},
    {'date': '2026-07-10', 'code': None, 'name': '台积电', 'type': 'industry',
     'event': '台积电 Q2 财报', 'importance': 'HIGH'},
    
    # 政策 / 宏观
    {'date': '2026-07-10', 'code': None, 'name': '央行', 'type': 'macro',
     'event': '6 月 金融数据 + PPI/CPI', 'importance': 'MEDIUM'},
    {'date': '2026-07-30', 'code': None, 'name': '中央', 'type': 'macro',
     'event': '7 月 政治局会议 (下半年 定调)', 'importance': 'CRITICAL'},
]


def get_events(days_ahead=60):
    now = datetime.now()
    cutoff = now + timedelta(days=days_ahead)
    events = []
    for c in CATALYSTS:
        try:
            event_date = datetime.strptime(c['date'], '%Y-%m-%d')
            days_diff = (event_date - now).days
            if 0 <= days_diff <= days_ahead:
                events.append({**c, 'days_diff': days_diff})
        except: pass
    return sorted(events, key=lambda x: x['days_diff'])


def get_urgency(days_diff, importance):
    if days_diff <= 1: return '🚨🚨🚨 明日/今日'
    if days_diff <= 3: return '🚨🚨 T-3'
    if days_diff <= 7: return '🚨 T-7'
    if days_diff <= 14: return '⚠️ T-14'
    return '📅 未来'


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--days', type=int, default=60, help='未来 天数')
    args = parser.parse_args()
    
    print(f"📅 Catalyst Calendar v1.0  /  {datetime.now():%Y-%m-%d %H:%M}")
    print(f"基于 Anthropic financial-services / equity-research\n")
    
    events = get_events(args.days)
    if not events:
        print(f"✅ 未来 {args.days} 天 无 关键 事件")
        return
    
    # 按 重要度 分组
    critical = [e for e in events if e['importance'] == 'CRITICAL']
    high = [e for e in events if e['importance'] == 'HIGH']
    medium = [e for e in events if e['importance'] == 'MEDIUM']
    
    print(f"📊 未来 {args.days} 天 关键 事件 (共 {len(events)} 条):")
    print(f"  🚨 CRITICAL: {len(critical)} 条")
    print(f"  🟡 HIGH: {len(high)} 条")
    print(f"  🟢 MEDIUM: {len(medium)} 条")
    
    # 逐条 列
    if critical:
        print("\n" + "=" * 65)
        print("🚨 CRITICAL 事件")
        print("=" * 65)
        for e in critical:
            urgency = get_urgency(e['days_diff'], e['importance'])
            print(f"\n  {urgency}  {e['date']} ({e['days_diff']:+d} 天)")
            print(f"     [{e['code'] or 'MARKET'}] {e['name']}")
            print(f"     🎯 {e['event']}")
    
    if high:
        print("\n" + "=" * 65)
        print("🟡 HIGH 事件")
        print("=" * 65)
        for e in high:
            urgency = get_urgency(e['days_diff'], e['importance'])
            print(f"\n  {urgency}  {e['date']} ({e['days_diff']:+d} 天)")
            print(f"     [{e['code'] or 'MARKET'}] {e['name']}: {e['event']}")
    
    if medium:
        print("\n" + "=" * 65)
        print("🟢 MEDIUM 事件")
        print("=" * 65)
        for e in medium:
            print(f"  {e['date']} ({e['days_diff']:+d}天) [{e['code'] or 'MARKET'}] {e['event']}")
    
    # 提醒
    print()
    print("=" * 65)
    print("💡 建议 行动")
    print("=" * 65)
    if any(e['days_diff'] <= 7 for e in critical):
        print("\n  🚨 有 CRITICAL 事件 T-7 内 / 立刻 准备!")
    if any(e['type'] == 'earnings_preview' and e['days_diff'] <= 7 for e in events):
        print("  🎯 财报 预告 临近 / 集成 earnings-preview")
    if any(e['type'] == 'debt_expiry' and e['days_diff'] <= 30 for e in events):
        print("  💰 融资到期 <30天 / 立刻 规划 还款")


if __name__ == '__main__':
    main()
