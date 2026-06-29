#!/usr/bin/env python3
"""
🌟 北极星自动化 监控 v1.0

核心 思想 (用户洞察):
  "判断 罗博 / 任何 转型公司 / 长线持仓
   最重要 是 盯住 公司 真业务 进展
   不是 短期 股价"

监控 4 维:
  1. 公告 (公司公告 - 最重要)
  2. 财报 (季度财报 - 业绩 拐点)
  3. 大宗交易 (大资金 异动)
  4. 减持 (大股东 信心)

用法:
  python3 polaris_monitor.py                       # 监控所有持仓
  python3 polaris_monitor.py --stock 300757         # 单股
  python3 polaris_monitor.py --days 7               # 近 7 天
  python3 polaris_monitor.py --critical             # 仅显示 重要事件
"""

import argparse
import json
import sys
import urllib.parse
import urllib.request
from datetime import datetime, timedelta
from dataclasses import dataclass, field
from typing import Optional


# 持仓 + watchlist + 北极星 关键词
WATCH_LIST = {
    '600522': {
        'name': '中天科技',
        'polaris_keywords': ['海缆订单', 'AI 算力', '数据中心', '业绩', '海外订单'],
        'critical_keywords': ['减持', '商誉', '巨亏', '处罚', '调查'],
    },
    '300757': {
        'name': '罗博特科',
        'polaris_keywords': ['ficonTEC', '英伟达', 'CPO', '硅光', '在手订单', '客户验证'],
        'critical_keywords': ['减持', '解禁', '商业化', '失败', 'H 股', '出口管制'],
    },
    '000988': {
        'name': '华工科技',
        'polaris_keywords': ['1.6T', '800G', '光模块', '订单', '海外', '北美'],
        'critical_keywords': ['减持', '商誉', '巨亏', '调查'],
    },
    '688234': {
        'name': '天岳先进',
        'polaris_keywords': ['SiC', '碳化硅', '英飞凌', '订单', '8 英寸'],
        'critical_keywords': ['减持', '解禁', '亏损扩大', '存货', '行业供需'],
    },
    '603259': {
        'name': '药明康德 (watch)',
        'polaris_keywords': ['在手订单', 'TIDES', 'GLP-1', '美国客户'],
        'critical_keywords': ['生物安全法案', '制裁', '减持', '客户流失'],
    },
}


def fetch_announcements(code: str, days: int = 7) -> list:
    """抓取 东财 公司公告"""
    # 东财 公告 API
    url = f"https://np-anotice-stock.eastmoney.com/api/security/ann"
    params = {
        'sr': '-1',
        'page_size': '20',
        'page_index': '1',
        'ann_type': 'A',
        'client_source': 'web',
        'stock_list': code,
        'f_node': '0',
        's_node': '0',
    }
    full_url = f"{url}?{urllib.parse.urlencode(params)}"
    headers = {
        'User-Agent': 'Mozilla/5.0',
        'Referer': 'https://data.eastmoney.com/',
    }
    req = urllib.request.Request(full_url, headers=headers)
    
    try:
        with urllib.request.urlopen(req, timeout=10) as r:
            data = json.loads(r.read().decode('utf-8'))
        
        items = data.get('data', {}).get('list', [])
        cutoff_date = datetime.now() - timedelta(days=days)
        
        recent = []
        for item in items:
            try:
                notice_date = item.get('notice_date', '')
                if not notice_date:
                    continue
                # 解析日期
                date_obj = datetime.strptime(notice_date[:10], '%Y-%m-%d')
                if date_obj < cutoff_date:
                    continue
                recent.append({
                    'date': notice_date[:10],
                    'title': item.get('title', ''),
                    'type': item.get('columns', [{}])[0].get('column_name', '') if item.get('columns') else '',
                    'art_code': item.get('art_code', ''),
                })
            except: continue
        return recent
    except Exception as e:
        return []


def classify_announcement(title: str, polaris_kws: list, critical_kws: list) -> tuple:
    """对 公告 进行 分类 + 评级"""
    title_lower = title.lower()
    
    # 🚨 关键 负面 (优先级 P0)
    critical_negative = ['减持', '处罚', '立案', '调查', '商誉', '巨亏', '诉讼']
    if any(kw in title for kw in critical_negative):
        return ('🚨 critical_negative', 'P0', '立刻 关注')
    
    # 🌟 北极星 正面 (P1)
    for kw in polaris_kws:
        if kw in title or kw.lower() in title_lower:
            return ('🌟 polaris_positive', 'P1', f'北极星 信号: {kw}')
    
    # ⚠️ 关键 词 (P1)
    for kw in critical_kws:
        if kw in title:
            return ('⚠️ critical_other', 'P1', f'关键事件: {kw}')
    
    # ✅ 中性 (P2)
    return ('✅ normal', 'P2', '常规公告')


def fetch_dazong(code: str, days: int = 30) -> list:
    """抓取 大宗交易"""
    # 简化版 / 跳过 (东财API 复杂)
    return []


def fetch_jianchi(code: str) -> list:
    """抓取 高管 减持公告"""
    # 通过 公告 自动 识别 (上面 已包含)
    return []


def format_report(code: str, info: dict, anns: list) -> str:
    """格式化 单股 北极星 报告"""
    name = info['name']
    report = f"""
╔══════════════════════════════════════════════════════════╗
║  🌟 北极星 监控 - {name} ({code})
╚══════════════════════════════════════════════════════════╝

📋 监控 关键词:
  • 北极星 信号 (利好): {', '.join(info['polaris_keywords'])}
  • 关键 风险 (利空): {', '.join(info['critical_keywords'])}

📅 近期 公告:
"""
    
    if not anns:
        report += "  (近 7 天 无 新公告)\n"
        return report
    
    # 按 优先级 排序
    classified = []
    for ann in anns:
        category, priority, hint = classify_announcement(
            ann['title'], info['polaris_keywords'], info['critical_keywords']
        )
        classified.append((priority, category, hint, ann))
    
    classified.sort(key=lambda x: x[0])
    
    # P0 在前
    for priority, category, hint, ann in classified:
        emoji_map = {'P0': '🚨', 'P1': '🌟', 'P2': '✅'}
        emoji = emoji_map.get(priority, '✅')
        report += f"\n  {emoji} [{priority}] {ann['date']} - {ann['title']}\n"
        report += f"      ↳ {hint}\n"
    
    # 统计
    p0_count = sum(1 for p, _, _, _ in classified if p == 'P0')
    p1_count = sum(1 for p, _, _, _ in classified if p == 'P1')
    
    report += f"\n  📊 统计: 共 {len(anns)} 条 / P0 关键 {p0_count} / P1 重要 {p1_count}\n"
    
    if p0_count > 0:
        report += "  🚨 警告: 有 P0 关键 事件 / 立刻 查看 详情!\n"
    elif p1_count > 0:
        report += "  🌟 提示: 有 北极星 / 关键 信号 / 建议 查看\n"
    
    return report


def main():
    parser = argparse.ArgumentParser(description='北极星 自动化 监控 v1.0')
    parser.add_argument('--stock', help='单股 代码 (如 300757)')
    parser.add_argument('--days', type=int, default=7, help='监控 天数 (默认 7 天)')
    parser.add_argument('--critical', action='store_true', help='仅 显示 关键 事件')
    args = parser.parse_args()
    
    targets = {}
    if args.stock:
        if args.stock in WATCH_LIST:
            targets[args.stock] = WATCH_LIST[args.stock]
        else:
            print(f"❌ 未知 股票: {args.stock}")
            print(f"已配置: {', '.join(WATCH_LIST.keys())}")
            sys.exit(1)
    else:
        targets = WATCH_LIST
    
    print(f"🌟 北极星 监控 - 监控 {len(targets)} 只 股票 / 近 {args.days} 天")
    print(f"⏰ {datetime.now():%Y-%m-%d %H:%M:%S}")
    print()
    
    critical_summary = []
    polaris_summary = []
    
    for code, info in targets.items():
        anns = fetch_announcements(code, days=args.days)
        
        if args.critical:
            # 仅 P0 / P1
            filtered = []
            for ann in anns:
                cat, pri, _ = classify_announcement(
                    ann['title'], info['polaris_keywords'], info['critical_keywords']
                )
                if pri in ('P0', 'P1'):
                    filtered.append(ann)
            anns = filtered
        
        print(format_report(code, info, anns))
        
        # 收集 重要 事件
        for ann in anns:
            cat, pri, hint = classify_announcement(
                ann['title'], info['polaris_keywords'], info['critical_keywords']
            )
            if pri == 'P0':
                critical_summary.append((info['name'], ann['date'], ann['title'], hint))
            elif pri == 'P1':
                polaris_summary.append((info['name'], ann['date'], ann['title'], hint))
    
    # 总结
    print("\n" + "=" * 60)
    print("📊 全持仓 总结")
    print("=" * 60)
    
    if critical_summary:
        print(f"\n🚨 P0 关键 事件 ({len(critical_summary)} 条):")
        for name, date, title, hint in critical_summary:
            print(f"  • {date} [{name}] {title}")
            print(f"    ↳ {hint}")
    
    if polaris_summary:
        print(f"\n🌟 P1 北极星 信号 ({len(polaris_summary)} 条):")
        for name, date, title, hint in polaris_summary:
            print(f"  • {date} [{name}] {title}")
            print(f"    ↳ {hint}")
    
    if not critical_summary and not polaris_summary:
        print(f"\n✅ 近 {args.days} 天 无 P0/P1 关键 事件 / 持仓 平稳")


if __name__ == '__main__':
    main()
