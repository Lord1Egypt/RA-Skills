# -*- coding: utf-8 -*-
"""
双色球 ML 模型样本外自评 (V1.0 新增)

目的: 科学严谨地回答"ML 模型到底有没有用", 而不是空口声称"增加了分析视角多样性"。
方法: 在历史上逐期做 walk-forward —
  用 [0, k) 期训练 → 预测第 k 期红球 (取模型 Top5) → 与真实开奖核对命中数
  累计统计 ML 三模型(加权频率/随机森林/遗传算法)的红球命中分布, 并与纯随机基线对比。

重要诚实声明: 彩票是独立随机事件。本自评仅用于揭示"模型是否提供可检测的优势",
若结果显示模型命中分布 ≈ 随机基线 (历史已证明 p>0.05 不显著), 则系统据此强化诚实结论,
而非编造"模型更准"。

用法:
  python ssq_ml_selfcheck.py            # 样本外回测(末200期)
  python ssq_ml_selfcheck.py --full    # 全量历史回测
"""
import sys
import io
import json
import random
from collections import Counter

# 注意: 不在模块顶层包装 sys.stdout (否则被其他脚本 import 时会篡改导入进程的 stdout 并导致其被关闭)
# 需要 UTF-8 输出时在 main() 内处理
from ssq_ml_models import generate_ml_prediction
from ssq_auto import load_valid_combos, passes_filters
from ssq_period import next_period as next_period_func


def _front_hit(pred_front, actual_front):
    """红球命中数"""
    return len(set(pred_front) & set(actual_front))


def walk_forward(draws, start=50, end=None, valid_combos=None):
    """逐期样本外回测 ML 模型红球命中。返回每模型的命中计数累加。"""
    if end is None:
        end = len(draws)
    models_hits = {  # 每个模型: 各期命中数列表
        'weighted_freq': [],
        'random_forest': [],
        'genetic_optimal': [],
    }
    random_hits = []  # 纯随机基线
    rng = random.Random(20240729)
    n_periods = 0
    prev_front = None
    for k in range(start, end):
        train = draws[:k]
        actual = draws[k]
        ml = generate_ml_prediction(train, valid_combos or [], target_period=actual['period'])
        prev_front = train[-1]['front'] if train else None
        for name, m in ml.items():
            pf = m.get('front', [])
            if pf:
                models_hits[name].append(_front_hit(pf, actual['front']))
        # 随机基线: 从1-33随机取5个(不限过滤, 公平比较)
        rand = sorted(rng.sample(range(1, 34), 6))
        random_hits.append(_front_hit(rand, actual['front']))
        n_periods += 1
    return models_hits, random_hits, n_periods


def summarize(hits_list):
    if not hits_list:
        return {'n': 0, 'mean': 0.0, 'ge3': 0.0, 'ge4': 0.0}
    n = len(hits_list)
    mean = sum(hits_list) / n
    ge3 = sum(1 for h in hits_list if h >= 3) / n
    ge4 = sum(1 for h in hits_list if h >= 4) / n
    return {'n': n, 'mean': mean, 'ge3': ge3, 'ge4': ge4}


def main():
    full = '--full' in sys.argv
    draws = json.load(open('ssq_history.json', encoding='utf-8'))
    valid_combos = load_valid_combos() or []
    start = 2700 if not full else 200
    end = len(draws)
    label = '全量' if full else f'末{end - start}期'
    print("=" * 70)
    print(f"ML 模型样本外自评 (walk-forward, {label})")
    print("=" * 70)
    print(f"  训练窗口: 逐期累积 [0,k) → 预测第 k 期")
    print(f"  期数: {end - start}")

    mh, rh, n = walk_forward(draws, start=start, end=end, valid_combos=valid_combos)

    print("\n  红球命中数分布 (越高越好; 随机期望≈5×5/35≈0.714):")
    print(f"  {'模型':<16}{'均值':>8}{'≥3球%':>10}{'≥4球%':>10}")
    summ = {}
    for name, h in mh.items():
        s = summarize(h)
        summ[name] = s
        print(f"  {name:<16}{s['mean']:>8.3f}{s['ge3']*100:>9.1f}%{s['ge4']*100:>9.1f}%")
    rs = summarize(rh)
    print(f"  {'随机基线':<16}{rs['mean']:>8.3f}{rs['ge3']*100:>9.1f}%{rs['ge4']*100:>9.1f}%")

    # 诚实结论
    best_mean = max(s['mean'] for s in summ.values())
    print("\n  " + "=" * 50)
    if best_mean <= rs['mean'] + 0.05:
        print(f"  ✅ 诚实结论: ML 模型红球命中均值({best_mean:.3f}) ≈ 随机基线({rs['mean']:.3f}),")
        print(f"     未检测到可复现优势。与既有回测(p>0.05)一致 — 系统无预测优势。")
    else:
        print(f"  ⚠ 检测到模型均值({best_mean:.3f})高于随机({rs['mean']:.3f}), 需进一步显著性检验。")
    print("  " + "=" * 50)
    print(f"\n  注: 此自评仅量化'模型是否有用', 不提升命中率。彩票本质随机, 请理性投注。")

    report = {
        'version': 'V1.0 ML Self-Check',
        'window': label,
        'n_periods': n,
        'models': summ,
        'random_baseline': rs,
        'conclusion': 'no_edge' if best_mean <= rs['mean'] + 0.05 else 'needs_review',
    }
    with open('ssq_ml_selfcheck.json', 'w', encoding='utf-8') as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    print(f"  ✓ 自评报告已存: ssq_ml_selfcheck.json")


if __name__ == '__main__':
    main()
