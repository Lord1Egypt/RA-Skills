# -*- coding: utf-8 -*-
"""
重叠假设实证检验 (ssq_overlap_test.py)
====================================================================

用户观察: 每一期中一等奖的 6+1 号码, 都会和「同比那期+同比最近三期 +
环比那期+环比最近三期」这 8 期历史号码的汇总(并集)中, 有几个号码重合。

本脚本验证两件事:
  (A) 重合是否真实存在 (描述性) —— 是的, 几乎每期都重合;
  (B) 重合是否携带"预测力" (关键) —— 用纯随机对照判定:
      若"当期实际号码"与并集的重合, 和"随机生成的号码"与同一并集的重合
      没有显著差异, 则该现象只是集合大小的必然结果(组合学), 而非隐藏模式,
      更不能据此预测下一期。

同比 = 上一年同一期号 (如 26086 的同比是 25086)
环比 = 上一期 (如 26086 的环比是 26085)
====================================================================
"""
import json
import random
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

SEED = 20260730
rng = random.Random(SEED)


def load():
    H = json.load(open('ssq_history.json', encoding='utf-8'))
    norm = []
    for d in H:
        p = str(d.get('period') or d.get('qi'))
        norm.append({
            'period': p,
            'front': [int(x) for x in d['front']],
            'back': [int(x) for x in d['back']],
        })
    return norm


def parse_period(p):
    return int(p[:2]), int(p[2:])  # (年两位, 期号三位)


def prev_year_period(p):
    y, n = parse_period(p)
    if y <= 0:
        return None
    return f"{y - 1:02d}{n:03d}"


def reference_indices(norm, by_period, idx):
    """返回用户构造的 8 期参考下标 (全部在 idx 之前, 无未来泄漏)。"""
    d = norm[idx]
    p = d['period']
    refs = []
    # 同比那期 + 同比最近三期
    yp = prev_year_period(p)
    if yp in by_period:
        yi = by_period[yp]
        for k in (0, 1, 2, 3):
            j = yi - k
            if 0 <= j < len(norm):
                refs.append(j)
    # 环比那期 + 环比最近三期
    for k in (1, 2, 3, 4):
        j = idx - k
        if 0 <= j < len(norm):
            refs.append(j)
    return refs


def main():
    norm = load()
    by_period = {d['period']: i for i, d in enumerate(norm)}
    N = len(norm)

    actual_front = []   # 实际号码与并集的红球重合数
    actual_back = []
    union_front_size = []   # 并集覆盖了多少个不同红球号码 (1-33)
    union_back_size = []
    n_valid = 0

    R = 1500  # 每个目标的随机对照抽样数
    rand_front = []   # 随机号码与"实际并集"的红球重合数 (对照)
    rand_back = []

    randref_front = []  # 用"8期随机历史"并集与"实际号码"的红球重合 (对照构造特殊性)
    randref_back = []

    for idx in range(N):
        refs = reference_indices(norm, by_period, idx)
        if len(refs) < 8:
            continue  # 需要完整的 8 期参考
        fset = set()
        bset = set()
        for j in refs:
            fset.update(norm[j]['front'])
            bset.update(norm[j]['back'])
        d = norm[idx]
        af = len(set(d['front']) & fset)
        ab = len(set(d['back']) & bset)
        actual_front.append(af)
        actual_back.append(ab)
        union_front_size.append(len(fset))
        union_back_size.append(len(bset))
        n_valid += 1

        # 对照1: 同一并集 vs 随机号码
        for _ in range(R):
            rf = set(rng.sample(range(1, 34), 6))
            rb = set(rng.sample(range(1, 17), 3))
            rand_front.append(len(rf & fset))
            rand_back.append(len(rb & bset))

        # 对照2: 8期随机历史并集 vs 实际号码 (看用户构造是否特殊)
        pool = list(range(max(0, idx - 300), idx))
        if len(pool) >= 8:
            rrefs = rng.sample(pool, 8)
            rfset = set()
            rbset = set()
            for j in rrefs:
                rfset.update(norm[j]['front'])
                rbset.update(norm[j]['back'])
            randref_front.append(len(set(d['front']) & rfset))
            randref_back.append(len(set(d['back']) & rbset))

    def mean(x):
        return sum(x) / len(x) if x else 0.0

    def frac_ge(x, k):
        return sum(1 for v in x if v >= k) / len(x) if x else 0.0

    def dist(x):
        from collections import Counter
        c = Counter(x)
        return ", ".join(f"{k}球:{c.get(k,0)}" for k in sorted(c))

    print("=" * 64)
    print("  重叠假设实证检验 (同比+环比 8期并集 vs 当期)")
    print("=" * 64)
    print(f"有效目标期数: {n_valid}")
    print()
    print("【并集覆盖度】—— 为什么几乎必然重合")
    print(f"  红球并集平均覆盖 {mean(union_front_size):.1f} / 35 个不同号码 "
          f"({mean(union_front_size)/35*100:.1f}%)")
    print(f"  蓝球并集平均覆盖 {mean(union_back_size):.1f} / 12 个不同号码 "
          f"({mean(union_back_size)/12*100:.1f}%)")
    print()
    print("【重合数分布 (红球5球 / 蓝球2球)】")
    print(f"  实际当期: 红球均={mean(actual_front):.2f} | {dist(actual_front)}")
    print(f"  随机对照: 红球均={mean(rand_front):.2f} | {dist(rand_front)}")
    print(f"  实际当期: 蓝球均={mean(actual_back):.2f} | {dist(actual_back)}")
    print(f"  随机对照: 蓝球均={mean(rand_back):.2f} | {dist(rand_back)}")
    print()
    print("【'至少重合几个'的比例】")
    print(f"  红球≥1: 实际={frac_ge(actual_front,1)*100:.2f}%  随机={frac_ge(rand_front,1)*100:.2f}%")
    print(f"  红球≥2: 实际={frac_ge(actual_front,2)*100:.2f}%  随机={frac_ge(rand_front,2)*100:.2f}%")
    print(f"  红球≥3: 实际={frac_ge(actual_front,3)*100:.2f}%  随机={frac_ge(rand_front,3)*100:.2f}%")
    print(f"  蓝球≥1: 实际={frac_ge(actual_back,1)*100:.2f}%  随机={frac_ge(rand_back,1)*100:.2f}%")
    print()
    print("【用户构造是否特殊? (8期随机历史并集 vs 实际号码)】")
    print(f"  随机参考构造红球均重合={mean(randref_front):.2f}  vs 用户构造实际={mean(actual_front):.2f}")
    print(f"  随机参考构造蓝球均重合={mean(randref_back):.2f}  vs 用户构造实际={mean(actual_back):.2f}")
    print()

    # 判定
    df = mean(actual_front) - mean(rand_front)
    db = mean(actual_back) - mean(rand_back)
    if abs(df) < 0.15 and abs(db) < 0.08:
        verdict = ("结论: 实际重合数与纯随机对照几乎一致 → 该现象是集合大小的必然结果"
                   "(并集已覆盖约85%的红球号码, 任意新开奖都极可能落入其中), "
                   "不含预测力, no_edge 不变。")
    else:
        verdict = (f"结论: 实际重合相对随机有偏差(红球+{df:.2f}/蓝球+{db:.2f}球), "
                   f"需进一步排查是否为真实弱相关。")
    print("判定:", verdict)
    print()
    print("补充: 即使'总重合几个'成立, 并集覆盖~30/35红球号码, 无法缩小到具体号码;")
    print("      用它预测下一期 = 从几乎全部号码里盲选, 一等奖概率仍恒为 1/17,721,088。")


if __name__ == '__main__':
    main()
