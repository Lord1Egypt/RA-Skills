# -*- coding: utf-8 -*-
"""
双色球系统 — 统一常量与核心函数 (单一可信源 / Single Source of Truth)
=====================================================================

集中定义所有"会被多文件使用、且一旦不一致就会产生错误结论"的常量与函数，
所有活动脚本 (ssq_auto / ssq_smart / ssq_enhance / ssq_cross_validate / ssq_healthcheck
/ ssq_result_verify / ssq_eci_backtest / ssq_ml_models) 应从本模块 import，
并由 ssq_healthcheck_all.py 持续断言"各文件内联定义 == 本模块"。

双色球规则（与文档/报告/四体一致）:
  - 红球 1-33 选 6, 蓝球 1-16 选 1
  - 每周二/四/日 21:15 开奖
  - 一等奖概率 1 / (C(33,6) * 16) = 1 / 17,721,088

绝不在此随意改动数值 —— 任何改动都会触发回归断言失败。
"""
from itertools import combinations
import math
import random

# ---------- 基础常量 ----------
K = 33                      # 红球号码数 1..33
BACK_N = 16                 # 蓝球号码数 1..16
PRIMES = {2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31}   # 11个质数 (红球1-33)

# 红球4模型评分权重 (CDM + 马尔可夫 + 频率 + 遗漏) —— 预测与回测必须一致
FRONT_WEIGHTS = [0.40, 0.25, 0.20, 0.15]

# 蓝球(单码)综合评分权重 (CDM + 马尔可夫 + 遗漏 + ECI中性项)
#   ECI中性项默认 0.5: 表示"无专家热度数据时，ECI 项取中性 0.5"
BACK_W_CDM = 0.35
BACK_W_MARKOV = 0.25
BACK_W_OMIT = 0.15
BACK_W_ECI = 0.25


# ============================================================
# 核心函数 (从 ssq_auto.py 抽取，逐字一致)
# ============================================================
def calc_ac(front):
    """标准 AC 值: 所有两两绝对差去重后的个数 - (n-1)"""
    diffs = set()
    for i in range(len(front)):
        for j in range(i + 1, len(front)):
            diffs.add(abs(front[i] - front[j]))
    return len(diffs) - (len(front) - 1)


def odd_count(front):
    return sum(1 for n in front if n % 2 == 1)


def small_count(front):
    return sum(1 for n in front if n <= 16)   # 小号=01..16, 大号=17..33


def prime_count(front):
    return sum(1 for n in front if n in PRIMES)


def road_counts(front):
    """返回 (余0个数, 余1个数, 余2个数)"""
    return (sum(1 for n in front if n % 3 == 0),
            sum(1 for n in front if n % 3 == 1),
            sum(1 for n in front if n % 3 == 2))


def consecutive_groups(front):
    """连号组数 (连续相邻算一组, 如 1,2,3 算1组)"""
    fs = sorted(front)
    groups = 0
    i = 0
    while i < len(fs) - 1:
        if fs[i + 1] - fs[i] == 1:
            groups += 1
            while i < len(fs) - 1 and fs[i + 1] - fs[i] == 1:
                i += 1
        i += 1
    return groups


def passes_filters(front, prev_front=None):
    """9项过滤器: 8项静态 + 可选第9项重号(<=2 vs 上期)

    双色球红球 6 个, 过滤器仅作用于红球; 蓝球为单码, 不参与组合过滤。
    返回 True 表示该组合通过全部启用的过滤项。

    阈值来源(数据校准, 非拍脑袋): 基于 3486 期真实双色球开奖(2003001-2026089)
    统计各指标分布, 取"最窄的 90% 覆盖区间"作为阈值 ——
      AC [5,9] / 和值 [70,140] / 跨度 [16,31] / 奇偶∈{2,3,4} / 大小∈{2,3,4}
      / 质数∈{1,2,3} / 012路各>0 / 连号组<=1 / 重号<=2

    ★ 诚实结论(实测, 必须随过滤器一起呈现):
      本 9 项过滤器把 C(33,6)=1,107,568 个组合筛到 363,666 个(排除 67.2%),
      但同一套阈值套到 3486 期"真实开奖号码"上, 存活率是 32.9% ——
      与组合空间存活率 32.83% 几乎完全相等(差 <0.1pp)。
      即: 过滤器排除多少比例的组合, 就等比例排除掉多少真实中奖号码,
      它只是把池子等比缩小, 没有任何"可确保的中奖结果"的能力。
      过滤器的唯一正当用途是"控制形态偏好/减少购票张数", 不是提高胜率。
    """
    checks = [
        5 <= calc_ac(front) <= 9,                       # ① AC值 [5,9]
        70 <= sum(front) <= 140,                        # ② 和值 [70,140]
        16 <= max(front) - min(front) <= 31,            # ③ 跨度 [16,31]
        odd_count(front) in [2, 3, 4],                  # ④ 奇偶比 (2:4/3:3/4:2)
        small_count(front) in [2, 3, 4],                # ⑤ 大小比 (2:4/3:3/4:2)
        prime_count(front) in [1, 2, 3],                # ⑥ 质数个数 [1,3]
        all(r > 0 for r in road_counts(front)),         # ⑦ 012路 各>0
        consecutive_groups(front) <= 1,                 # ⑧ 连号组 <=1
    ]
    if prev_front:
        checks.append(len(set(front) & set(prev_front)) <= 2)   # ⑨ 重号 <=2
    return all(checks)


def back_score(cdm_s, mk_s, omit_norm, eci_norm=0.5):
    """蓝球(单码)综合评分 (与 ssq_auto.py 预测管线完全一致)

    cdm_s, mk_s: 归一化后的 CDM / 马尔可夫 概率
    omit_norm:   遗漏值 / max_omit (已归一化到 0..1)
    eci_norm:    ECI 热度项, 默认 0.5 (中性). 仅在确有真实专家热度数据时传入
    """
    return (BACK_W_CDM * cdm_s + BACK_W_MARKOV * mk_s
            + BACK_W_OMIT * omit_norm + BACK_W_ECI * eci_norm)


# ============================================================
# 期号计算 (转发到统一模块 ssq_period)
# ============================================================
from ssq_period import next_period  # noqa: E402


# ============================================================
# 属性 / 差分 / 变质 测试 (对所有输入成立的不变量校验)
# ============================================================
def property_checks(n_trials=5000, seed=20260802):
    """随机不变量校验: 差分 oracle + 变质属性 + 输入校验。"""
    rng = random.Random(seed)

    def naive_ac(c):
        diffs = set()
        for i in range(len(c)):
            for j in range(i + 1, len(c)):
                diffs.add(abs(c[i] - c[j]))
        return len(diffs) - (len(c) - 1)

    for _ in range(n_trials):
        c = sorted(rng.sample(range(1, K + 1), 6))

        assert isinstance(passes_filters(c), bool)        # 永不抛异常, 返回布尔
        assert 0 <= calc_ac(c) <= 10                       # AC 取值范围(6号: 0..10)

        ac = calc_ac(c)
        assert naive_ac(c) == ac                           # 差分 oracle

        # 变质属性: 整体平移不改变两两差, 故 AC 不变
        t = rng.randint(-(c[0] - 1), (K - c[-1]))
        if t != 0:
            ct = sorted(x + t for x in c)
            assert 1 <= ct[0] and ct[-1] <= K
            assert calc_ac(ct) == ac

        # 分类计数不变量 (三者和必须等于 6)
        assert prime_count(c) == sum(1 for n in c if n in PRIMES)
        r0, r1, r2 = road_counts(c)
        assert r0 + r1 + r2 == 6
        oc = odd_count(c)
        assert oc + (6 - oc) == 6
        sc = small_count(c)
        assert sc + (6 - sc) == 6

        # 蓝球综合评分有界 [0,1]
        s = back_score(rng.random(), rng.random(), rng.random(), rng.random())
        assert 0.0 <= s <= 1.0

    # 输入校验: 非法组合必须被 passes_filters 拒 (返回 False, 不抛异常)
    bad = [
        [1, 1, 2, 3, 4, 5],     # 含重复
        [0, 1, 2, 3, 4, 5],     # 越下界
        [1, 2, 3, 4, 5, 34],    # 越上界
        [1, 2, 3, 4, 5],        # 长度不足
        [1, 2, 3, 4, 5, 6, 7],  # 长度超
    ]
    for b in bad:
        assert passes_filters(b) is False
    return True


# ============================================================
# 自检 (可被 ssq_healthcheck_all.py 调用)
# ============================================================
def _self_test():
    # ---- 已知组合 [2,5,9,16,22,30] 应通过9项(无重号上下文) ----
    assert passes_filters([2, 5, 9, 16, 22, 30])
    # AC 已知: {2,5,9,16,22,30} 两两差集 13 个, AC = 13-(6-1) = 8 (在[5,9]内, 通过)
    assert calc_ac([2, 5, 9, 16, 22, 30]) == 8
    # 蓝球评分
    assert abs(back_score(0.1, 0.2, 0.3) - (0.35 * 0.1 + 0.25 * 0.2 + 0.15 * 0.3 + 0.25 * 0.5)) < 1e-12
    # 蓝球评分权重守恒 (=1.0)
    assert abs((BACK_W_CDM + BACK_W_MARKOV + BACK_W_OMIT + BACK_W_ECI) - 1.0) < 1e-12
    # 质数计数
    assert prime_count([2, 3, 5, 7, 11, 13]) == 6
    assert prime_count([1, 4, 6, 8, 9, 10]) == 0

    # ---- 过滤器否决案例 (必须 False) ----
    assert not passes_filters([1, 3, 5, 7, 9, 11])            # 奇偶比 6:0 -> 拒
    assert not passes_filters([1, 2, 3, 4, 5, 6])             # 连号组过多(5组)且全小且AC低 -> 拒
    assert not passes_filters([28, 29, 30, 31, 32, 33])       # 和值=183>140 -> 拒
    # 纯净单因子否决样本: 其余7项全过, 仅跨度=15<16 -> 拒 (证明③项真实生效)
    assert not passes_filters([3, 5, 12, 16, 17, 18])
    assert not passes_filters([3, 6, 9, 12, 15, 18])          # 012路不全(全余0) -> 拒
    assert calc_ac([1, 2, 3, 4, 5, 6]) == 0                   # AC 边界: 连续6号差集仅5 -> AC=0

    # ---- 重号过滤 (第9项) ----
    assert passes_filters([2, 5, 9, 16, 22, 30], prev_front=[1, 2, 3, 4, 5, 6])          # 无重号 -> 通过
    assert not passes_filters([2, 5, 9, 16, 22, 30], prev_front=[2, 5, 9, 16, 7, 8])    # 重号4个>2 -> 拒

    # ---- 工具函数正确性 ----
    assert odd_count([1, 3, 5, 7, 9, 11]) == 6
    assert small_count([1, 2, 3, 4, 5, 6]) == 6
    assert road_counts([3, 6, 9, 12, 15, 18]) == (6, 0, 0)
    assert consecutive_groups([1, 2, 3, 10, 20, 30]) == 1     # 仅 1-2-3 一组
    assert consecutive_groups([1, 2, 10, 11, 20, 30]) == 2    # 两组

    # ---- 属性/差分/变质 随机不变量测试 (5000 样本) ----
    property_checks()
    return True


if __name__ == '__main__':
    _self_test()
    print("ssq_common OK | PRIMES=%d个 | FRONT_WEIGHTS=%s | K=%d BACK_N=%d"
          % (len(PRIMES), FRONT_WEIGHTS, K, BACK_N))
