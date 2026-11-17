"""
双色球专家战绩自算 / 随机基线对照 (V1.0.8 新增)

诚实机制: 不采信平台自报命中率(幸存者偏差 + 指标注水 + 事后篡改)。
每期开奖后, 用系统自己抓到的专家推荐 vs 实际开奖号独立打分; 同时生成
"机选基线" 用相同口径打分。任何专家的排名只有相对基线才有意义——
若专家红球均命中 ≤ 随机基线, 即证明无超额优势(与理论一致)。

用法:
  python ssq_expert_tracker.py            # 对未评分期号打分 + 打印近20期汇总
  (被 ssq_smart.py Phase 0.x 以非致命子进程调用)
"""
import json
import os
import random
from datetime import datetime
from collections import defaultdict

ACC_FILE = 'ssq_expert_accuracy.json'
HIST_FILE = 'ssq_expert_history.json'
DATA_FILE = 'ssq_history.json'


def _load(path, default):
    try:
        with open(path, encoding='utf-8') as f:
            return json.load(f)
    except Exception:
        return default


def score_pick(front, back, af, ab):
    """单组专家推荐 vs 实际开奖的命中数(描述性)。"""
    fh = len(set(front) & set(af))
    bh = len(set(back) & set(ab))
    return {'front_hits': fh, 'back_hits': bh}


def random_baseline(af, ab, n=500, seed=None):
    """机选基线: 生成 n 组随机 6+1 用相同口径打分, 返回均值。"""
    rnd = random.Random(seed)
    tot_f = tot_b = 0
    for _ in range(n):
        f = rnd.sample(range(1, 34), 6)
        b = rnd.sample(range(1, 17), 3)
        s = score_pick(f, b, af, ab)
        tot_f += s['front_hits']
        tot_b += s['back_hits']
    return {'front_hits': round(tot_f / n, 3), 'back_hits': round(tot_b / n, 3)}


def run_tracker(periods_back=9999):
    """对 ssq_expert_history.json 中、尚未评分的期号, 用 ssq_history.json 实际开奖号打分。
    幂等: 已评分期号跳过。返回本次新增评分的期数。非致命。"""
    hist = _load(HIST_FILE, [])
    data = _load(DATA_FILE, [])
    if not hist or not data:
        return 0
    actual = {int(e['period']): e for e in data}
    acc = _load(ACC_FILE, {'_meta': {
        'note': '专家战绩自算 vs 随机基线; 不采信平台自报命中率',
        'scored_rule': '每期开奖后用系统自身抓到的专家推荐 vs 实际开奖独立打分',
    }, 'records': []})
    scored = {r['period'] for r in acc.get('records', [])}
    new = 0
    for rec in hist:
        p = int(rec.get('period'))
        if p in scored:
            continue
        a = actual.get(p)
        if not a:
            continue  # 该期尚未开奖或无数据
        af = [int(x) for x in a['front']]
        ab = [int(x) for x in a['back']]
        experts = {}
        for e in rec.get('experts', []):
            name = e.get('expert') or e.get('name')
            f = [int(x) for x in e.get('front', [])]
            b = [int(x) for x in e.get('back', [])]
            if len(f) != 5 or len(b) != 2:
                continue
            experts[name] = score_pick(f, b, af, ab)
        base = random_baseline(af, ab)
        acc['records'].append({
            'period': p,
            'actual_front': af,
            'actual_back': ab,
            'experts': experts,
            'baseline': base,
            'expert_count': len(experts),
        })
        scored.add(p)
        new += 1
    if new:
        acc['_meta']['last_updated'] = datetime.now().strftime('%Y-%m-%d %H:%M')
        with open(ACC_FILE, 'w', encoding='utf-8') as f:
            json.dump(acc, f, ensure_ascii=False, indent=2)
    return new


def summary(periods=20):
    """近 periods 期每专家红球均命中, 与随机基线对比, 降序。"""
    acc = _load(ACC_FILE, {'records': []})
    recs = acc.get('records', [])[-periods:]
    if not recs:
        return None
    agg = defaultdict(lambda: {'fh': 0, 'bh': 0, 'n': 0})
    bf = bh = bn = 0
    for r in recs:
        for name, s in r.get('experts', {}).items():
            agg[name]['fh'] += s['front_hits']
            agg[name]['bh'] += s['back_hits']
            agg[name]['n'] += 1
        bf += r['baseline']['front_hits']
        bh += r['baseline']['back_hits']
        bn += 1
    base_fh = bf / bn if bn else 0
    rows = []
    for name, v in agg.items():
        if v['n']:
            rows.append((name, round(v['fh'] / v['n'], 3),
                         round(v['bh'] / v['n'], 3), v['n']))
    rows.sort(key=lambda x: -x[1])
    return {
        'periods': len(recs),
        'baseline_front_hits': round(base_fh, 3),
        'experts': rows,
        'note': '专家红球均命中 vs 随机基线; 若专家≤基线则说明无超额优势(符合理论)。',
    }


if __name__ == '__main__':
    n = run_tracker()
    print(f"本次新增评分期数: {n}")
    s = summary()
    if not s:
        print("暂无足够评分数据(需先有 ssq_expert_history.json 且对应期已开奖)。")
    else:
        print(f"近 {s['periods']} 期 | 随机基线红球均命中 {s['baseline_front_hits']}")
        for name, fh, bh, cnt in s['experts'][:15]:
            print(f"  {name:10s} 红球均命中 {fh}  蓝球均命中 {bh}  (n={cnt})")
