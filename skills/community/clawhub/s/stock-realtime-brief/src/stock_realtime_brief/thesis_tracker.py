#!/usr/bin/env python3
"""
🎯 Thesis Tracker v1.0 - 投资论点 追踪
基于 Anthropic financial-services / equity-research / thesis-tracker

核心: 每只 持仓 3-5 条 关键论点 → 定期 复核 → 变化 立刻 警示
论点 失效 → 触发 减仓信号

用法:
  python3 thesis_tracker.py             # 全部 持仓 论点检查
  python3 thesis_tracker.py --code 603259  # 单股
"""

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path

THESIS_DB = {
    '603259': {
        'name': '药明康德',
        'sector': 'CXO 医药',
        'theses': [
            {'id': 'wxk-1', 'text': 'CXO 全球 Top 3 (护城河 强)', 'weight': 20, 'status': 'active',
             'evidence': 'Q1 +27% 净利 + 在手订单 ¥598 亿'},
            {'id': 'wxk-2', 'text': 'DCF 内在价值 ¥179 (+47%)', 'weight': 25, 'status': 'active',
             'evidence': 'PE 18.7 历史低位'},
            {'id': 'wxk-3', 'text': 'GLP-1 减重 需求 高增 (受益)', 'weight': 20, 'status': 'active',
             'evidence': '诺和 +3.40% / 礼来 +1.86% 美股'},
            {'id': 'wxk-4', 'text': '美国 客户 70% (地缘政治 风险)', 'weight': -15, 'status': 'watch',
             'evidence': '生物安全法案 阴影'},
            {'id': 'wxk-5', 'text': 'Q1/Q2 业绩 逐季 兑现', 'weight': 20, 'status': 'active',
             'evidence': '5/5 季正增 / Q2 待 8月 验证'},
        ],
        'kill_switch': ['生物安全法案 通过', 'Q2 业绩 大幅低于预期 (-20%)', '美国客户流失 ≥20%'],
    },
    '300757': {
        'name': '罗博特科',
        'sector': 'CPO / 半导体设备 (业务转型期)',
        'theses': [
            {'id': 'lbtk-1', 'text': 'ficonTEC 全球 CPO 设备 寡头', 'weight': 25, 'status': 'active',
             'evidence': '英伟达/台积电/博通/Lumentum/Intel/思科 都是客户'},
            {'id': 'lbtk-2', 'text': '新业务 (光电子) +870% 拐点已现', 'weight': 25, 'status': 'active',
             'evidence': '2025 光电子 ¥4.85亿 (2024 仅 ¥0.5亿 / +870%) / 光电子已追平光伏'},
            {'id': 'lbtk-3', 'text': '2026年1-4月新签订单 ¥10.21亿 = 印钞', 'weight': 25, 'status': 'active',
             'evidence': 'F公司硅光 ¥8.46亿 + 瑞士C OCS 2条 + 美国A ¥1.36亿'},
            {'id': 'lbtk-4', 'text': '在手订单 ¥11.05亿 (占2024年营收100%)', 'weight': 15, 'status': 'active',
             'evidence': '2025年报披露 / 2027-2028 集中兑现'},
            {'id': 'lbtk-5', 'text': '高盛 目标价 ¥688 (+30%)', 'weight': 15, 'status': 'active',
             'evidence': '4/16 高盛 首次覆盖 / 光器件设备全球领先'},
            {'id': 'lbtk-6', 'text': '老业务光伏出清 (-56%) 短期财报假象', 'weight': -5, 'status': 'watch',
             'evidence': '2025 光伏 ¥4.60亿 (-56%) / 但毛利率 29.79% 稳定 / 行业周期底部'},
        ],
        'kill_switch': [
            'Lumentum/英伟达 缩减扩产计划',
            'CPO 量产 延到 2030 后 (SemiAnalysis 加倍延后)',
            '光电子在手订单 12 个月内 无 大幅新增',
            'H股 上市 溢价 严重收敛 -50%',
        ],
    },
    '600522': {
        'name': '中天科技',
        'sector': 'AI 算力 / 海缆',
        'theses': [
            {'id': 'ztk-1', 'text': 'AI 算力 主升 (数据中心 建设)', 'weight': 25, 'status': 'active',
             'evidence': 'Q1 +46% 净利'},
            {'id': 'ztk-2', 'text': '海缆 海外订单 高增', 'weight': 20, 'status': 'active',
             'evidence': '海外 收入 占比 上升'},
            {'id': 'ztk-3', 'text': '业绩 +77% 浮盈 (你 已锁部分利)', 'weight': 20, 'status': 'active',
             'evidence': '你 已减 12,400 股'},
            {'id': 'ztk-4', 'text': '半导体 主线 承压 (短期风险)', 'weight': -15, 'status': 'watch',
             'evidence': '美光 -10% / 板块 -6.27%'},
            {'id': 'ztk-5', 'text': '长线 目标 ¥80+ (业绩+估值)', 'weight': 20, 'status': 'active',
             'evidence': '当前 PE 25 合理'},
        ],
        'kill_switch': ['海缆订单 大幅下滑', '大股东 减持 >5%', 'Q2 净利 增速 <10%'],
    },
    '000988': {
        'name': '华工科技',
        'sector': 'CPO / 光通信',
        'theses': [
            {'id': 'hgkj-1', 'text': 'CPO 龙头 + 1.6T 光模块', 'weight': 25, 'status': 'active',
             'evidence': 'Q1 +56% 净利'},
            {'id': 'hgkj-2', 'text': '业绩 +80% 浮盈 已 部分 兑现', 'weight': 20, 'status': 'active',
             'evidence': '你 已 减 1,700 股 @¥163 卖飞跌停'},
            {'id': 'hgkj-3', 'text': 'CPO 板块 SemiAnalysis 报告 冲击', 'weight': -20, 'status': 'watch',
             'evidence': 'AAOI -19% / Lumentum -15% 累计'},
            {'id': 'hgkj-4', 'text': '海外 客户 拓展 中', 'weight': 15, 'status': 'active',
             'evidence': '北美 客户 逐步 起量'},
            {'id': 'hgkj-5', 'text': '长线 目标 ¥250+ (若 CPO 兑现)', 'weight': 20, 'status': 'active',
             'evidence': '基于 v2.1 五维'},
        ],
        'kill_switch': ['CPO 量产 延至 2029 后', 'Q2 净利 增速 <20%', '美国 出口管制'],
    },
}


def check_thesis(code):
    """检查 单股 论点 状态"""
    if code not in THESIS_DB: return None
    info = THESIS_DB[code]
    
    total_weight = 0
    active_weight = 0
    watch_weight = 0
    killed_weight = 0
    
    for t in info['theses']:
        total_weight += abs(t['weight'])
        if t['status'] == 'active': active_weight += t['weight']
        elif t['status'] == 'watch': watch_weight += abs(t['weight'])
        elif t['status'] == 'killed': killed_weight += abs(t['weight'])
    
    net_score = active_weight  # 正为看好 / 负为看空
    
    # 评级
    if net_score >= 70: rating = '🌟🌟🌟🌟🌟 极强 持有'
    elif net_score >= 50: rating = '🌟🌟🌟🌟 持有'
    elif net_score >= 30: rating = '🌟🌟🌟 观察'
    elif net_score >= 0: rating = '🟡 中性'
    else: rating = '🔴 减仓'
    
    return {
        'name': info['name'],
        'sector': info['sector'],
        'theses': info['theses'],
        'kill_switch': info['kill_switch'],
        'net_score': net_score,
        'total_weight': total_weight,
        'active_weight': active_weight,
        'watch_weight': watch_weight,
        'killed_weight': killed_weight,
        'rating': rating,
    }


def format_report(code, r):
    if not r: return f"❌ {code} 未配置"
    
    report = f"""
╔══════════════════════════════════════════════════════════╗
║  🎯 {r['name']} ({code}) - {r['sector']}
╚══════════════════════════════════════════════════════════╝

📊 论点 总览:
  ✅ Active (看好): {r['active_weight']:+d} 分
  🟡 Watch (观察): {r['watch_weight']} 分权重
  🔴 Killed (失效): {r['killed_weight']} 分权重
  
💎 净评分: {r['net_score']:+d} / 100
🎯 评级: {r['rating']}

📋 关键论点 (详细):
"""
    for t in r['theses']:
        emoji = {'active': '✅', 'watch': '🟡', 'killed': '🔴'}.get(t['status'], '❓')
        weight_str = f"+{t['weight']}" if t['weight'] > 0 else str(t['weight'])
        report += f"\n  {emoji} [{t['id']}] {t['text']} ({weight_str})\n"
        report += f"     证据: {t['evidence']}\n"
    
    report += f"\n🚨 Kill Switch (触发即 全清):\n"
    for k in r['kill_switch']:
        report += f"  🔴 {k}\n"
    
    return report


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--code', help='单股 代码')
    args = parser.parse_args()
    
    print(f"🎯 Thesis Tracker v1.0  /  {datetime.now():%Y-%m-%d %H:%M}")
    print("基于 Anthropic financial-services / equity-research\n")
    
    codes = [args.code] if args.code else list(THESIS_DB.keys())
    
    total_active = 0
    total_watch = 0
    
    for code in codes:
        r = check_thesis(code)
        print(format_report(code, r))
        if r:
            active_count = sum(1 for t in r['theses'] if t['status'] == 'active')
            watch_count = sum(1 for t in r['theses'] if t['status'] == 'watch')
            total_active += active_count
            total_watch += watch_count
    
    if not args.code:
        print("\n" + "=" * 60)
        print("📊 全持仓 论点 综合")
        print("=" * 60)
        print(f"\n  ✅ Active 论点: {total_active} 条")
        print(f"  🟡 Watch 论点: {total_watch} 条")
        print(f"  💡 建议: 每周 更新 一次 / 每月 复核 深度\n")


if __name__ == '__main__':
    main()
