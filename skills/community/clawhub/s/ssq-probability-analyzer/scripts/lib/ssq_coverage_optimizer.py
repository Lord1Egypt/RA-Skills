# -*- coding: utf-8 -*-
"""
双色球「最小成本 · 最大收益」覆盖优化器 (V1.1 新增, 2026-09-07)

用户需求(2026-09-07):
  "你至少预测出几个正确号码吧, 你预测几个三四五六等奖, 总可以吧?
   加加油, 看看怎么能用最小的成本获取最大的收益"

核心思想(诚实):
  - 数学上任何选号法都不优于随机(no_edge), 一等奖概率恒 1/17,721,088 无法改变。
  - 但中小奖(三~六等奖)是真实可捕获的奖级。双色球的结构性特点:
      【六等奖 = 命中蓝球】(0+1 / 1+1 / 2+1), 而蓝球仅 1/16,
      因此"同一个红球组合 + 覆盖 N 个蓝球" = N 注, 命中任意奖概率 ≈ N/16,
      这是双色球里成本效率最高的"捕获中小奖"结构。
  - 本器在【固定预算】内, 用组合数学(复式/胆拖)选择最优"覆盖结构",
    最大化"命中三~六等奖"的概率 —— 这是成本效率优化, 不是预测优势。
  - EV 仍为负(返奖率约 51%), 本器是伤害减损(娱乐预算内提高中奖体验), 绝非盈利。

方法:
  - 枚举候选结构(单式 / 蓝球复式 / 红球复式 / 全复式 / 胆拖), 在预算上限内。
  - 蒙特卡洛(N 次随机开奖)估计每个票集合命中各奖级的概率。
  - 选 P(命中≥目标奖级) 最优者, 同分取更省成本。

奖级(双色球 6红+1蓝; 判定与 ssq_draw_check.prize_of 一致):
  一等奖 6+1 | 二等奖 6+0 | 三等奖 5+1 | 四等奖 5+0/4+1
  五等奖 4+0/3+1 | 六等奖 2+1/1+1/0+1 | 未中奖(含 3+0)
"""
import itertools
import random
from dataclasses import dataclass, field

RED_N = 33
RED_PICK = 6
BLUE_N = 16
BLUE_PICK = 1
NOTE_COST = 2  # 每注 2 元


def tier_of(rh, bh):
    """红球命中 rh(0-6), 蓝球命中 bh(0/1) -> 奖级 1~6, 0=未中奖。
    与 ssq_draw_check.prize_of / ssq_power_engine.PRIZE_PAYOUT 保持一致。"""
    if rh == 6 and bh == 1:
        return 1
    if rh == 6 and bh == 0:
        return 2
    if rh == 5 and bh == 1:
        return 3
    if (rh == 5 and bh == 0) or (rh == 4 and bh == 1):
        return 4
    if (rh == 4 and bh == 0) or (rh == 3 and bh == 1):
        return 5
    if bh == 1 and rh in (0, 1, 2):
        return 6
    return 0


def build_tickets(red_pool, blue_pool, red_dan=None):
    """构造票集合。返回 [(frozenset(6红), 蓝球int), ...]
    red_dan: 红球胆码(胆拖); 蓝球每球独立成注(双色球蓝球只选1个)。"""
    red_pool = list(red_pool)
    blue_pool = list(blue_pool)
    if red_dan:
        dan = set(red_dan)
        need = RED_PICK - len(dan)
        drag = [x for x in red_pool if x not in dan]
        red_combos = [frozenset(dan | set(c)) for c in itertools.combinations(drag, need)]
    else:
        red_combos = [frozenset(c) for c in itertools.combinations(red_pool, RED_PICK)]
    return [(f, b) for f in red_combos for b in blue_pool]


def monte_carlo(tickets, n_sims=120000, seed=20260907):
    """蒙特卡洛: 返回 ({tier: P(至少中第 tier 等奖)}, P(任意奖))。

    语义(⚠️ 历史教训: 曾误用 max 取"最差奖级", 导致 p_capture 语义颠倒):
      奖级编号 1=一等奖(最好) ... 6=六等奖(最低)。
      best = 本次开奖下所有票里的"最好奖级" = 最小编号(未中奖记 99)。
      p_capture[t] = P(best <= t) = P(至少中第 t 等奖)。
      故 p_capture[6] = P(任意奖), p_capture[5] = P(五等奖或更好)。
    """
    rng = random.Random(seed)
    cap = {t: 0 for t in range(1, 7)}
    any_prize = 0
    for _ in range(n_sims):
        dr = frozenset(rng.sample(range(1, RED_N + 1), RED_PICK))
        db = rng.randrange(1, BLUE_N + 1)  # 双色球蓝球只有 1 个
        best = 99  # 越小越好; 99 = 未中奖
        for f, b in tickets:
            rh = len(f & dr)
            bh = 1 if b == db else 0
            t = tier_of(rh, bh)
            if 0 < t < best:
                best = t
                if best == 1:
                    break
        if best <= 6:
            any_prize += 1
        for t in range(1, 7):
            if best <= t:
                cap[t] += 1
    return {t: cap[t] / n_sims for t in cap}, any_prize / n_sims


@dataclass
class Plan:
    name: str
    tickets: list
    cost: int
    p_capture: dict = field(default_factory=dict)
    p_any: float = 0.0
    structure: str = ""


def enumerate_plans(red_pool, blue_pool, budget, max_red_pool=14, max_blue_pool=16):
    """枚举预算内所有候选结构。"""
    plans = []
    red_pool = list(red_pool)
    blue_pool = list(blue_pool)
    if len(red_pool) < RED_PICK or len(blue_pool) < 1:
        return plans

    top6 = red_pool[:RED_PICK]

    # 1) 单式: 1 个红球组合 + 1 个蓝球
    t = build_tickets(top6, blue_pool[:1])
    plans.append(Plan("单式(1红球组合+1蓝球)", t, len(t) * NOTE_COST, structure="single"))

    # 2) 蓝球复式: 1 个红球组合 × m 个蓝球  (双色球性价比最高的中小奖捕获结构)
    for m in range(2, min(max_blue_pool, len(blue_pool)) + 1):
        t = build_tickets(top6, blue_pool[:m])
        c = len(t) * NOTE_COST
        if c <= budget:
            plans.append(Plan(f"蓝球复式: 固定6红 × 蓝球{m}个", t, c, structure=f"blue{m}"))

    # 3) 红球复式 n 选 6 × 单蓝球
    for n in range(RED_PICK + 1, min(max_red_pool, len(red_pool)) + 1):
        t = build_tickets(red_pool[:n], blue_pool[:1])
        c = len(t) * NOTE_COST
        if c <= budget:
            plans.append(Plan(f"红球复式{n}选6 × 1蓝球", t, c, structure=f"red{n}"))

    # 4) 全复式: 红球 n 选 6 × 蓝球 m 个
    for n in range(RED_PICK + 1, min(max_red_pool, len(red_pool)) + 1):
        for m in range(2, min(max_blue_pool, len(blue_pool)) + 1):
            t = build_tickets(red_pool[:n], blue_pool[:m])
            c = len(t) * NOTE_COST
            if c <= budget:
                plans.append(Plan(f"全复式: 红{n}选6 × 蓝{m}个", t, c, structure=f"red{n}blue{m}"))

    # 5) 分散单式: n 个不同红球组合, 各配 1 个不同蓝球(真实最常见的"买 n 注不同号")
    combos = list(itertools.combinations(red_pool, RED_PICK))
    for n in range(2, min(15, len(combos), len(blue_pool)) + 1):
        t = [(frozenset(combos[i]), blue_pool[i]) for i in range(n)]
        c = n * NOTE_COST
        if c <= budget:
            plans.append(Plan(f"分散单式{n}注(不同红球组合+不同蓝球)", t, c, structure=f"spread{n}"))

    # 6) 胆拖: 红球 d 胆 + 拖, 蓝球 m 个
    for d in (1, 2, 3):
        if len(red_pool) > d + (RED_PICK - d):
            drag_len = len(red_pool) - d
            if drag_len >= RED_PICK - d:
                for m in range(1, min(max_blue_pool, len(blue_pool)) + 1):
                    t = build_tickets(red_pool, blue_pool[:m], red_dan=red_pool[:d])
                    c = len(t) * NOTE_COST
                    if c <= budget:
                        plans.append(Plan(f"胆拖: 红{d}胆全拖 × 蓝{m}个", t, c, structure=f"dan{d}blue{m}"))
    return plans


def optimize(red_pool, blue_pool, budget=30, target_tier=6, n_sims=120000, seed=20260907):
    """返回 (最优Plan, 所有候选Plan)。target_tier: 6=六等奖(默认), 5=五等奖..."""
    plans = enumerate_plans(red_pool, blue_pool, budget)
    for p in plans:
        p.p_capture, p.p_any = monte_carlo(p.tickets, n_sims=n_sims, seed=seed)

    def score(p):
        return (p.p_capture.get(target_tier, 0), -p.cost)

    plans.sort(key=score, reverse=True)
    return (plans[0] if plans else None), plans


def honest_ev_note(plan, note=""):
    """诚实 EV 附注(伤害减损, 非盈利)。"""
    return (
        f"诚实声明: 本方案为纯组合覆盖优化, 不宣称任何预测优势(no_edge)。"
        f"双色球返奖率约 51%, 期望净收益为负 —— 长期必亏, 仅作娱乐预算内的中奖体验优化。"
        f"所选号码本身与随机机选等价; 优化的是「覆盖结构」而非「号码对错」。"
        f"一等奖概率恒 1/17,721,088, 任何结构都无法改变。{note}"
    )


if __name__ == "__main__":
    # 自检: 用模型常用 top 号码作为覆盖池(仅作演示, 不暗示更可能中)
    red_pool = [5, 9, 14, 17, 21, 26, 3, 11, 22, 30, 8, 19, 25, 32]
    blue_pool = [9, 12, 15, 3, 7, 11, 1, 14]
    best, allp = optimize(red_pool, blue_pool, budget=30, target_tier=6, n_sims=120000)
    print("预算 ¥30 候选方案数:", len(allp))
    for p in allp[:10]:
        print(f"  {p.name:30s} 注数={len(p.tickets):4d} 成本=¥{p.cost:3d} "
              f"P(六等)={p.p_capture.get(6,0):.3f} P(五等)={p.p_capture.get(5,0):.4f} P(任意)={p.p_any:.3f}")
    print("\n最优(最小成本最大收益, 目标六等奖):")
    print(f"  {best.name}  成本=¥{best.cost}  注数={len(best.tickets)}")
    print(f"  P(六等奖)={best.p_capture.get(6,0):.3f}  P(五等奖)={best.p_capture.get(5,0):.4f}  P(任意奖)={best.p_any:.3f}")
    # 理论校验
    print("\n理论校验:")
    print(f"  单式 P(任意奖) 理论 ≈ 0.0671 (官方总中奖率 6.7%)")
    single = [p for p in allp if p.structure == "single"][0]
    print(f"  单式 P(任意奖) MC   = {single.p_any:.4f}")
    b3 = [p for p in allp if p.structure == "blue3"]
    if b3:
        # 理论: 3/16 + (1-3/16)*P(红>=4)=0.004901
        print(f"  蓝球复式3个 理论 ≈ {3/16 + (1-3/16)*0.004901:.4f}  MC = {b3[0].p_any:.4f}")
    print("  ", honest_ev_note(best))
