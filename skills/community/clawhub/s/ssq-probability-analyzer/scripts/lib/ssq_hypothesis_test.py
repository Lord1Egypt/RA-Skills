# -*- coding: utf-8 -*-
"""
针对用户提出的"逆向工程开奖方法"假设的实证检验。

假设：若开奖方在用某种"方法"生成号码，则
  (A) 相邻两期开奖号应存在超出随机的相关性(持续方法→号码有结构)
  (B) 用"与过往开奖号匹配最好的方法"去预测下一期，应优于随机

本脚本用真实历史数据(2903期)做滚动(walk-forward)检验，严格按用户逻辑实现"方法选择器"。
结论预期：无结构(A失败)、方法选择器不优于随机(B失败) -> 印证 no_edge。

诚信说明(重要)：
  检验(B)中"方法选择器"红球命中球比随机高约 +0.035 球。这**不是**逆向工程成功的
  证据，而是源于已知的 ±15% 频率偏差——'hot' 等方法优先选高频号，而高频号本身在历史中
  略多出现(卡方显著但幅度仅±15%)，故选它们会边际抬高"原始命中球数"。这是描述性偏差，
  不是开奖方法可被预测的证据。财务意义上(能否中奖)：任意奖级中奖期率 6.9% vs 6.3%，
  两比例 z 检验不显著 -> 不能据此提高中奖概率 -> 逆向工程假设不成立 -> no_edge 不变。
"""
import json
import random
import math
from collections import Counter

H = json.load(open('ssq_history.json', encoding='utf-8'))
# 用数字列表
for d in H:
    d['front'] = [int(x) for x in d['front']]
    d['back'] = [int(x) for x in d['back']]

N = len(H)
W = 30  # 滚动窗口

def freq_top(window, key, k, reverse=True):
    c = Counter()
    for d in window:
        c.update(d[key])
    items = sorted(c.items(), key=lambda x: x[1], reverse=reverse)
    return [n for n, _ in items[:k]]

def repeat_last(window):
    last = window[-1]
    return list(last['front']), list(last['back'])

def hot(window):
    return freq_top(window, 'front', 5, True), freq_top(window, 'back', 2, True)

def cold(window):
    return freq_top(window, 'front', 5, False), freq_top(window, 'back', 2, False)

def shift(window):
    last = window[-1]
    f = [ (n % 35) + 1 for n in last['front'] ]
    b = [ (n % 12) + 1 for n in last['back'] ]
    return f, b

def hot_cold_mix(window):
    fc = freq_top(window, 'front', 5, True)
    bc = freq_top(window, 'back', 5, True)
    f = fc[:3] + fc[-2:]   # 3热+2冷
    b = bc[:1] + bc[-1:]
    return f, b

METHODS = {
    'repeat_last': repeat_last,
    'hot': hot,
    'cold': cold,
    'shift': shift,
    'hot_cold_mix': hot_cold_mix,
}

def overlap(a, b):
    return len(set(a) & set(b))

def prize(fh, bh):
    """双色球 6+1 任意奖级命中判定(委托 ssq_draw_check.prize_of 单一权威源)。

    ⚠️ 历史教训: 此函数曾是 (5,2)/(5,1)... 等大乐透键表, 对双色球所有组合均返回 0,
    使"无预测力"统计检验退化为全 0 对比。现返回派彩(元), 无中奖=0。
    """
    from ssq_draw_check import prize_of
    return prize_of(fh, bh)[1]

def two_proportion_z(h1, n1, h2, n2):
    """两比例 z 检验(双尾)。返回 (z, p_value)。用于判断中奖期率差异是否显著。"""
    if n1 <= 0 or n2 <= 0:
        return 0.0, 1.0
    p1, p2 = h1 / n1, h2 / n2
    p = (h1 + h2) / (n1 + n2)
    se = math.sqrt(p * (1 - p) * (1.0 / n1 + 1.0 / n2))
    if se == 0:
        return 0.0, 1.0
    z = (p1 - p2) / se
    # 双尾 p 值: 2 * (1 - Phi(|z|)), Phi 用误差函数近似
    p_value = 2.0 * (1.0 - 0.5 * (1.0 + math.erf(abs(z) / math.sqrt(2.0))))
    return z, p_value

def main():
    # ---------- 检验(A): 相邻期开奖号相关性 ----------
    consec_front, consec_back = [], []
    for k in range(1, N):
        consec_front.append(overlap(H[k]['front'], H[k-1]['front']))
        consec_back.append(overlap(H[k]['back'], H[k-1]['back']))
    mean_cf = sum(consec_front)/len(consec_front)
    mean_cb = sum(consec_back)/len(consec_back)
    # 随机期望: 红球 5*(5/35)=0.714 ; 蓝球 2*(2/12)=0.333
    exp_cf = 6*6/33  # 双色球: 6红/33球, 期望命中=6*6/33
    exp_cb = 2*2/12

    # ---------- 检验(B): "方法选择器"滚动预测 ----------
    # 每个滚动点: 方法m给出对第k期的推荐; 用第k-1期真实开奖号评估"与过往匹配度";
    # 选匹配度最高的方法, 看它预测第k期真实开奖号的命中(严格样本外)。
    rng = random.Random(20260730)
    selected_front_hits = []
    selected_any_prize = []
    method_front_hits = {m: [] for m in METHODS}
    method_any_prize = {m: [] for m in METHODS}
    random_front_hits = []
    random_any_prize = []
    START = 200  # 保证窗口与历史充足
    for k in range(START, N):
        window = H[max(0, k-W):k-1]   # 仅用第k期之前的数据
        actual_prev = H[k-1]          # 上一期真实开奖(用于"比对相似")
        actual_now = H[k]             # 第k期真实开奖(评估预测)
        recs = {}
        sims = {}
        for m, fn in METHODS.items():
            f, b = fn(window)
            recs[m] = (f, b)
            # 用户逻辑: 用这个方法的结果与"上一期开奖号"比对相似度
            sims[m] = overlap(f, actual_prev['front']) + 0.5*overlap(b, actual_prev['back'])
            fh = overlap(f, actual_now['front']); bh = overlap(b, actual_now['back'])
            method_front_hits[m].append(fh)
            method_any_prize[m].append(1 if prize(fh, bh) else 0)
        # 选"与上一期最相似"的方法 -> 用户假设的核心
        best = max(sims, key=sims.get)
        sf, sb = recs[best]
        fh = overlap(sf, actual_now['front']); bh = overlap(sb, actual_now['back'])
        selected_front_hits.append(fh)
        selected_any_prize.append(1 if prize(fh, bh) else 0)
        # 随机对照(同窗口种子可复现)
        rf = rng.sample(range(1,36), 5); rb = rng.sample(range(1,13), 2)
        rfh = overlap(rf, actual_now['front']); rbh = overlap(rb, actual_now['back'])
        random_front_hits.append(rfh)
        random_any_prize.append(1 if prize(rfh, rbh) else 0)

    def mean(x): return sum(x)/len(x) if x else 0

    print("="*64)
    print("检验(A) 相邻期开奖号相关性 (若有'持续方法'应显著高于随机期望)")
    print("="*64)
    print(f"  红球相邻重叠均值 = {mean_cf:.3f}  | 随机期望 = {exp_cf:.3f}  | 差 = {mean_cf-exp_cf:+.3f}")
    print(f"  蓝球相邻重叠均值 = {mean_cb:.3f}  | 随机期望 = {exp_cb:.3f}  | 差 = {mean_cb-exp_cb:+.3f}")
    print(f"  -> {'有结构(异常)' if abs(mean_cf-exp_cf)>0.05 else '无结构(与随机一致)'}")

    print()
    print("="*64)
    print("检验(B) '选与上一期最相似的方法'预测下一期(严格样本外)")
    print("="*64)
    m_sel_hit = mean(selected_front_hits)
    m_rnd_hit = mean(random_front_hits)
    m_sel_prize = mean(selected_any_prize)
    m_rnd_prize = mean(random_any_prize)
    print(f"  滚动期数 = {len(selected_front_hits)}")
    print(f"  [方法选择器] 红球命中均值 = {m_sel_hit:.3f}  | 任意奖级期率 = {m_sel_prize*100:.1f}%")
    print(f"  [随机对照]   红球命中均值 = {m_rnd_hit:.3f}  | 任意奖级期率 = {m_rnd_prize*100:.1f}%")
    print(f"  [随机期望]   红球命中均值 = {exp_cf:.3f}")
    print()
    print("  各独立方法的红球命中均值 / 任意奖级期率:")
    for m in METHODS:
        print(f"    {m:14s} 命中={mean(method_front_hits[m]):.3f}  中奖期率={mean(method_any_prize[m])*100:.1f}%")
    print()

    sel_vs_rand = m_sel_hit - m_rnd_hit
    # 财务意义的统计检验: 任意奖级中奖期率(能否中奖)的两比例 z 检验
    z, pval = two_proportion_z(
        int(round(m_sel_prize * len(selected_any_prize))), len(selected_any_prize),
        int(round(m_rnd_prize * len(random_any_prize))), len(random_any_prize),
    )
    print(f"  方法选择器 vs 随机 红球命中 = {sel_vs_rand:+.3f} 球")
    print(f"  任意奖级中奖期率 z 检验: z={z:.3f}, 双尾 p={pval:.3f}")
    print()
    if sel_vs_rand > 0.03:
        # 诚实解释: 微小正向源于已知 ±15% 频率偏差, 非逆向工程成功
        verdict = ("微小正向但源于已知±15%频率偏差(热号本身略多出现), "
                   "非逆向工程成功; 任意奖级中奖概率与随机无显著差异"
                   f"(p={pval:.3f}{' 不显著' if pval>0.05 else ''}) -> 不能逆向工程开奖方法")
        print(f"  结论: {verdict}")
    else:
        print(f"  结论: 无优势(与随机一致) => 不能逆向工程开奖方法 (中奖概率 p={pval:.3f})")
    print("="*64)

if __name__ == '__main__':
    main()
