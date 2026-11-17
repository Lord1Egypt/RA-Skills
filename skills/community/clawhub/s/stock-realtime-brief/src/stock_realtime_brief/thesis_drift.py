#!/usr/bin/env python3
"""
🔍 Thesis Drift Detector v1.0 - 投资论点漂移检测
基于 ai-berkshire /thesis-drift + Anthropic thesis-tracker 融合

核心: 对比 两个 时间点 的 论文
区分: 事实变化 / 估值变化 / 措辞变化

用法:
  python3 thesis_drift.py                       # 对比 当前 vs 上次快照
  python3 thesis_drift.py --snapshot          # 保存 当前 快照
  python3 thesis_drift.py --code 300757       # 单股 详细
"""

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path

# 复用 thesis_tracker 数据
sys.path.insert(0, str(Path(__file__).parent))
from thesis_tracker import THESIS_DB, check_thesis

SNAPSHOT_DIR = Path.home() / '.openclaw' / 'workspace' / 'memory' / '_thesis_snapshots'


def save_snapshot():
    SNAPSHOT_DIR.mkdir(parents=True, exist_ok=True)
    now = datetime.now()
    snapshot = {
        'timestamp': now.isoformat(),
        'date': now.strftime('%Y-%m-%d'),
        'stocks': {},
    }
    for code in THESIS_DB:
        r = check_thesis(code)
        if r:
            snapshot['stocks'][code] = {
                'net_score': r['net_score'],
                'active': r['active_weight'],
                'watch': r['watch_weight'],
                'killed': r['killed_weight'],
                'theses': [{'id': t['id'], 'text': t['text'], 'status': t['status'], 'weight': t['weight'], 'evidence': t['evidence']} for t in r['theses']],
                'kill_switch': r['kill_switch'],
            }
    fname = SNAPSHOT_DIR / f"thesis-{now:%Y%m%d-%H%M}.json"
    fname.write_text(json.dumps(snapshot, ensure_ascii=False, indent=2))
    print(f"✅ 快照 已保存: {fname.name}")
    return fname


def load_latest_two():
    """加载 最近 两个 快照"""
    if not SNAPSHOT_DIR.exists(): return None, None
    files = sorted(SNAPSHOT_DIR.glob('thesis-*.json'), key=lambda p: p.name, reverse=True)
    if len(files) < 2: return None, None
    latest = json.loads(files[0].read_text())
    prev = json.loads(files[1].read_text())
    return latest, prev


def load_prev_and_current():
    """加载 上次快照 + 当前 状态"""
    if not SNAPSHOT_DIR.exists(): return None, None
    files = sorted(SNAPSHOT_DIR.glob('thesis-*.json'), key=lambda p: p.name, reverse=True)
    if not files: return None, None
    prev = json.loads(files[0].read_text())
    # 当前 状态
    current = {'timestamp': datetime.now().isoformat(), 'stocks': {}}
    for code in THESIS_DB:
        r = check_thesis(code)
        if r:
            current['stocks'][code] = {
                'net_score': r['net_score'],
                'active': r['active_weight'],
                'watch': r['watch_weight'],
                'killed': r['killed_weight'],
                'theses': [{'id': t['id'], 'text': t['text'], 'status': t['status'], 'weight': t['weight'], 'evidence': t['evidence']} for t in r['theses']],
            }
    return current, prev


def diff_thesis(current, previous, code):
    """对比 单股 论点 差异"""
    if code not in current['stocks'] or code not in previous['stocks']:
        return None
    
    cur = current['stocks'][code]
    prev = previous['stocks'][code]
    
    # 净分 变化
    score_diff = cur['net_score'] - prev['net_score']
    
    # 逐条 论点 对比
    changes = {'fact': [], 'valuation': [], 'wording': [], 'status_change': [], 'new_thesis': [], 'removed': []}
    
    prev_theses = {t['id']: t for t in prev['theses']}
    cur_theses = {t['id']: t for t in cur['theses']}
    
    for tid, c in cur_theses.items():
        p = prev_theses.get(tid)
        if not p:
            changes['new_thesis'].append(c)
            continue
        
        # 状态 变化 (active → watch/killed)
        if p['status'] != c['status']:
            changes['status_change'].append({
                'thesis': c,
                'prev_status': p['status'],
                'new_status': c['status'],
            })
        
        # 证据 变化 (事实 vs 措辞)
        if p['evidence'] != c['evidence']:
            # 简单 判断: 数字 变 = 事实 / 否则 = 措辞
            import re
            p_nums = set(re.findall(r'\d+\.?\d*', p['evidence']))
            c_nums = set(re.findall(r'\d+\.?\d*', c['evidence']))
            if p_nums != c_nums:
                changes['fact'].append({
                    'thesis': c,
                    'prev_evidence': p['evidence'],
                    'new_evidence': c['evidence'],
                })
            else:
                changes['wording'].append({
                    'thesis': c,
                    'prev_evidence': p['evidence'],
                    'new_evidence': c['evidence'],
                })
        
        # 权重 变化 (估值)
        if p['weight'] != c['weight']:
            changes['valuation'].append({
                'thesis': c,
                'prev_weight': p['weight'],
                'new_weight': c['weight'],
            })
    
    for tid, p in prev_theses.items():
        if tid not in cur_theses:
            changes['removed'].append(p)
    
    return {
        'code': code,
        'name': THESIS_DB[code]['name'],
        'score_diff': score_diff,
        'prev_score': prev['net_score'],
        'cur_score': cur['net_score'],
        'prev_date': previous.get('date', 'unknown'),
        'cur_date': current.get('date', 'today'),
        'changes': changes,
    }


def format_diff(d):
    if not d: return ""
    changes = d['changes']
    
    # 综合 变化
    total_changes = sum(len(v) for v in changes.values())
    if total_changes == 0:
        return f"\n  ✅ {d['name']}: 无 变化 (净分 {d['prev_score']:+d} → {d['cur_score']:+d})\n"
    
    # 变化 严重度
    if abs(d['score_diff']) >= 30 or changes['status_change']:
        alert = '🚨 重大 漂移!'
    elif abs(d['score_diff']) >= 15 or changes['fact']:
        alert = '⚠️ 中度 变化'
    elif changes['valuation']:
        alert = '🟡 估值 调整'
    else:
        alert = '🟢 措辞 变化'
    
    out = f"""
╔══════════════════════════════════════════════════════════╗
║  🔍 {d['name']} ({d['code']}) - Thesis Drift
╚══════════════════════════════════════════════════════════╝

📊 净分 变化:
  {d['prev_date']}: {d['prev_score']:+d}
  {d['cur_date']}: {d['cur_score']:+d}
  📈 变化: {d['score_diff']:+d}
  🎯 {alert}
"""
    
    if changes['status_change']:
        out += f"\n🚨 状态 变化 (最严重!):\n"
        for c in changes['status_change']:
            emoji = {'active': '✅', 'watch': '🟡', 'killed': '🔴'}
            out += f"  {c['thesis']['id']}: {emoji.get(c['prev_status'], '?')} → {emoji.get(c['new_status'], '?')}\n"
            out += f"     {c['thesis']['text']}\n"
    
    if changes['fact']:
        out += f"\n⚠️ 事实 变化 (数字/关键 事件 变):\n"
        for c in changes['fact']:
            out += f"  [{c['thesis']['id']}] {c['thesis']['text']}\n"
            out += f"     旧: {c['prev_evidence']}\n"
            out += f"     新: {c['new_evidence']}\n"
    
    if changes['valuation']:
        out += f"\n🟡 估值 调整 (权重 变):\n"
        for c in changes['valuation']:
            out += f"  [{c['thesis']['id']}] {c['thesis']['text']}\n"
            out += f"     权重: {c['prev_weight']:+d} → {c['new_weight']:+d}\n"
    
    if changes['new_thesis']:
        out += f"\n🌟 新增 论点:\n"
        for c in changes['new_thesis']:
            out += f"  + [{c['id']}] {c['text']}\n"
    
    if changes['removed']:
        out += f"\n🔴 移除 论点:\n"
        for c in changes['removed']:
            out += f"  - [{c['id']}] {c['text']}\n"
    
    if changes['wording']:
        out += f"\n📝 措辞 变化 (证据 用词 变 / 事实 未变):\n"
        for c in changes['wording'][:2]:
            out += f"  [{c['thesis']['id']}] {c['thesis']['text']}\n"
    
    return out


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--snapshot', action='store_true', help='保存 当前 快照')
    parser.add_argument('--code', help='单股 详细')
    parser.add_argument('--compare-last-two', action='store_true', help='对比 最近 2 个 快照')
    args = parser.parse_args()
    
    print(f"🔍 Thesis Drift Detector v1.0  /  {datetime.now():%Y-%m-%d %H:%M}")
    print("基于 ai-berkshire + Anthropic 融合\n")
    
    if args.snapshot:
        save_snapshot()
        return
    
    if args.compare_last_two:
        current, prev = load_latest_two()
    else:
        current, prev = load_prev_and_current()
    
    if not prev:
        print("⚠️ 未 找到 快照 / 请 先 运行:")
        print("   python3 thesis_drift.py --snapshot")
        return
    
    print(f"📊 对比: {prev.get('date','?')} → {current.get('date','today')}\n")
    
    codes = [args.code] if args.code else list(THESIS_DB.keys())
    
    has_alert = False
    for code in codes:
        d = diff_thesis(current, prev, code)
        if d:
            print(format_diff(d))
            if abs(d['score_diff']) >= 15 or d['changes']['status_change']:
                has_alert = True
    
    print("\n" + "=" * 60)
    if has_alert:
        print("🚨 综合: 有 论点 漂移! 立刻 复核")
    else:
        print("✅ 综合: 论点 稳定")


if __name__ == '__main__':
    main()
