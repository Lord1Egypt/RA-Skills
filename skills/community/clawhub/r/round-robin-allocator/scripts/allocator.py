"""
round-robin-allocator  |  核心分配算法
========================================
通用均匀轮转分配：将 N 个"对象"在 T 个"轮次"中，
按比例分配 K 种"选项"，并尽量让每个对象每轮获得不同选项。

术语映射（可自定义，下面仅为示例）：
  对象  ← 项目 / 学生 / 用户 / 商品 ...
  轮次  ← 周期 / 周 / 月 / 阶段 ...
  选项  ← 方案 / 策略 / 组 / 颜色 ...

Public API
----------
allocate(N, T, K, ratios) -> list[dict]
    返回 N 个对象的分配结果。

每个结果 dict 结构：
  {
    "id":       int,          # 对象编号（1-based）
    "slots":    list[int],    # 每轮分到的选项编号（1-based），长度 T
    "used":     set[int],     # 已覆盖的选项集合
    "coverage": float,        # 覆盖率 = len(used) / K
  }
"""

from __future__ import annotations
import itertools
import random
from collections import defaultdict
from typing import Sequence


# ─────────────────────────────────────────────
# 公开接口
# ─────────────────────────────────────────────

def allocate(
    N: int,
    T: int,
    K: int,
    ratios: Sequence[float],
) -> list[dict]:
    """
    均匀轮转分配。

    Parameters
    ----------
    N : 对象数量（>0）
    T : 轮次数量（>0）
    K : 选项数量（>0，len(ratios) 必须 == K）
    ratios : 各选项的分配比例（可以是百分比或任意正数）

    Returns
    -------
    list of dict，每项包含 id / slots / used / coverage
    """
    if len(ratios) != K:
        raise ValueError(f"ratios 长度 {len(ratios)} 与 K={K} 不一致")
    if any(r < 0 for r in ratios):
        raise ValueError("比例不能为负数")
    total_ratio = sum(ratios)
    if total_ratio <= 0:
        raise ValueError("比例之和必须大于 0")

    norm = [r / total_ratio for r in ratios]

    objects = [{"id": i + 1, "slots": [], "used": set()} for i in range(N)]

    # ── 阶段1：为每轮生成选项池（确定性，按 Hamilton 大余数法） ──
    period_pools: list[list[int]] = []
    for _ in range(T):
        quotas = _hamilton_quota(N, norm, K)
        pool: list[int] = []
        for option_idx, count in enumerate(quotas):
            pool.extend([option_idx + 1] * count)
        period_pools.append(pool)

    # ── 阶段2：贪心分配（优先填补覆盖空白） ──
    for t in range(T):
        remaining: dict[int, int] = defaultdict(int)
        for opt in period_pools[t]:
            remaining[opt] += 1

        # 覆盖率低的对象优先处理
        order = sorted(range(N), key=lambda i: (len(objects[i]["used"]), i))

        for i in order:
            obj = objects[i]
            # 优先选"尚未覆盖"且剩余最多的选项
            novel = [(opt, cnt) for opt, cnt in remaining.items()
                     if cnt > 0 and opt not in obj["used"]]
            if novel:
                selected = max(novel, key=lambda x: (x[1], -x[0]))[0]
            else:
                # 退而求其次：选剩余最多的（重复也无妨）
                fallback = [(opt, cnt) for opt, cnt in remaining.items() if cnt > 0]
                if not fallback:
                    raise RuntimeError(f"轮次 {t+1} 选项池耗尽，请检查参数")
                selected = max(fallback, key=lambda x: (x[1], -x[0]))[0]

            obj["slots"].append(selected)
            obj["used"].add(selected)
            remaining[selected] -= 1

    # ── 阶段3：优化（尝试消除同轮次重复，提升覆盖率） ──
    _optimize(objects, period_pools, T, K)

    # ── 计算最终覆盖率 ──
    for obj in objects:
        obj["used"] = set(obj["slots"])          # 重新同步（优化后可能变化）
        obj["coverage"] = len(obj["used"]) / K

    return objects


# ─────────────────────────────────────────────
# 内部工具
# ─────────────────────────────────────────────

def _hamilton_quota(N: int, norm_ratios: list[float], K: int) -> list[int]:
    """Hamilton（最大余数）配额法：确保配额之和 == N。"""
    raw = [N * r for r in norm_ratios]
    quotas = [int(x) for x in raw]
    fractions = [(raw[i] - quotas[i], i) for i in range(K)]
    deficit = N - sum(quotas)
    # 按余数降序补齐
    for _, idx in sorted(fractions, reverse=True)[:deficit]:
        quotas[idx] += 1
    return quotas


def _optimize(objects: list[dict], pools: list[list[int]], T: int, K: int) -> None:
    """
    迭代优化：将重复使用次数最多的选项替换为未覆盖选项，
    前提是目标轮次的配额还有空余。
    """
    improved = True
    while improved:
        improved = False
        for obj in objects:
            slots = obj["slots"]
            freq: dict[int, int] = defaultdict(int)
            for s in slots:
                freq[s] += 1

            # 找重复最多的选项
            dup_options = [opt for opt, cnt in freq.items() if cnt > 1]
            if not dup_options:
                continue
            worst = max(dup_options, key=lambda x: freq[x])

            for t in range(T):
                if slots[t] != worst:
                    continue

                # 计算该轮各选项使用量
                used_in_t: dict[int, int] = defaultdict(int)
                for o in objects:
                    if t < len(o["slots"]):
                        used_in_t[o["slots"][t]] += 1
                pool_count: dict[int, int] = defaultdict(int)
                for opt in pools[t]:
                    pool_count[opt] += 1

                best = None
                best_gain = 0
                for cand in range(1, K + 1):
                    if cand == worst:
                        continue
                    if used_in_t.get(cand, 0) >= pool_count.get(cand, 0):
                        continue  # 该选项在此轮已无剩余配额
                    gain = 0 if cand in obj["used"] else 1
                    if gain > best_gain or (gain == best_gain and best and cand < best):
                        best = cand
                        best_gain = gain

                if best and best_gain > 0:
                    slots[t] = best
                    obj["used"] = set(slots)
                    improved = True
                    break


# ─────────────────────────────────────────────
# 统计辅助
# ─────────────────────────────────────────────

def compute_stats(results: list[dict], T: int, K: int) -> dict:
    """
    计算全局统计信息。

    Returns dict with keys:
      period_dist  : {t: {option: count}}
      avg_coverage : float
      full_coverage: int  (覆盖率==1 的对象数)
    """
    period_dist: dict[int, dict[int, int]] = {
        t: defaultdict(int) for t in range(T)
    }
    for obj in results:
        for t, opt in enumerate(obj["slots"]):
            period_dist[t][opt] += 1

    coverages = [obj["coverage"] for obj in results]
    return {
        "period_dist": period_dist,
        "avg_coverage": sum(coverages) / len(coverages) if coverages else 0.0,
        "full_coverage": sum(1 for c in coverages if c >= 1.0),
    }


# ─────────────────────────────────────────────
# 参数推断（N/K 二选一）
# ─────────────────────────────────────────────

def infer_K(N: int, T: int) -> int:
    """
    当 K 未指定时，从 N 和 T 推断。
    规则：K = T + 1（选项数比周期多1，制造有趣的覆盖竞争），
    但不超过 N 且不低于 3。
    """
    K = max(3, min(N, T + 1))
    return K


def infer_N(K: int, T: int) -> int:
    """
    当 N 未指定时，从 K 和 T 推断。
    规则：N = K * 3（每个选项每轮至少 3 个对象竞争），不低于 10。
    """
    N = max(K * 3, 10)
    return N


# ─────────────────────────────────────────────
# 后处理模式
# ─────────────────────────────────────────────

def post_process(
    results: list[dict],
    N: int,
    T: int,
    K: int,
    mode: str = "algorithm",
    repeat_ratio: list[float] | None = None,
    seed: int | None = None,
) -> list[dict]:
    """
    对 allocate() 的结果进行后处理，不改变分配方案本身，只改变排序/分布。

    四种模式：
      "algorithm" — 保持原样（ID 顺序）
      "random"    — 每个对象的 slots 随机打乱
      "fair"      — 将重复事件均匀分摊到各月
      "custom"    — 按用户指定的月间比例分配重复

    Parameters
    ----------
    results : allocate() 返回的结果
    N, T, K : 与 allocate() 相同
    mode : 后处理模式
    repeat_ratio : 仅 custom 模式使用，各月重复比例（例如 [4,2,7,1]）
    seed : 仅 random 模式使用，随机种子

    Returns
    -------
    list[dict] — 与 allocate() 格式相同，slots/used/coverage 已重算
    """
    if mode == "algorithm":
        return results  # 原样

    if mode == "random":
        return _post_random(results, K, seed)

    # 统计当前重复分布
    rep_per_month = _count_reps(results, T)

    if mode == "fair":
        total_reps = sum(rep_per_month)
        target = _distribute_evenly(total_reps, T)
    elif mode == "custom":
        if not repeat_ratio:
            raise ValueError("custom 模式需要提供 repeat_ratio 参数")
        total_reps = sum(rep_per_month)
        if total_reps == 0:
            return results  # 无重复可分配
        ratio = list(repeat_ratio)
        if len(ratio) == T:
            ratio[0] = 0  # t=0 不能有重复
        elif len(ratio) == T - 1:
            pass
        else:
            raise ValueError(f"repeat_ratio 长度应为 {T} 或 {T-1}")
        # 过滤全零比例
        if sum(ratio) <= 0:
            ratio = [1] * T
            ratio[0] = 0
        target = [0] * T
        sub_target = _distribute_by_ratio(total_reps, ratio)
        for i, v in enumerate(sub_target):
            target[i + (T - len(sub_target))] = v
    else:
        raise ValueError(f"未知模式: {mode}")

    _redistribute_reps(results, T, target, K)
    return results


# ─────────────────────────────────────────────
# 后处理内部函数
# ─────────────────────────────────────────────

def _count_reps(results: list[dict], T: int) -> list[int]:
    """计算各月的重复事件数"""
    reps = [0] * T
    for obj in results:
        seen = set()
        for t, s in enumerate(obj["slots"]):
            if s in seen:
                reps[t] += 1
            seen.add(s)
    return reps


def _distribute_evenly(total: int, T: int) -> list[int]:
    """将 total 个重复事件均匀分配到 T 个月（t=0 天然无重复）"""
    if T <= 1:
        return [total]
    # t=0 (第1月) 永远不能有重复（首次出现）
    possible = T - 1
    base = total // possible
    rem = total % possible
    target = [0] * T
    for i in range(1, T):
        target[i] = base
    # 前 rem 个可能月多分 1 个
    for i in range(1, 1 + rem):
        target[i] += 1
    return target


def _distribute_by_ratio(total: int, ratio: list[float]) -> list[int]:
    """按比例分配 total 个重复事件（t=0 天然无重复）"""
    # 如果提供了 T 个值，t=0 的比率被忽略（强制 0）
    # 如果提供了 T-1 个值，对应 t=1..T-1
    s = sum(ratio)
    raw = [total * r / s for r in ratio]
    target = [int(x) for x in raw]
    deficit = total - sum(target)
    remainders = [(raw[i] - target[i], i) for i in range(len(raw))]
    for _, idx in sorted(remainders, reverse=True)[:deficit]:
        target[idx] += 1
    return target


def _redistribute_reps(
    results: list[dict],
    T: int,
    target: list[int],
    K: int,
) -> None:
    """
    通过枚举每个对象的 slots 全排列（T≤6 时 T!≤720 可接受），
    使用 running filled 计数精确匹配目标重复分布。
    """
    if T > 6:
        return _redistribute_reps_fallback(results, T, target, K)

    current = _count_reps(results, T)
    excess_periods = {t for t in range(T) if current[t] > target[t]}
    if not excess_periods:
        return

    # 已填充计数（随处理进度更新）
    filled = list(current)

    for obj in results:
        slots = obj["slots"]
        # 检查是否有重复在超额月
        obj_reps = _count_reps_for_each_t(slots)
        contributes = any(obj_reps[t] and t in excess_periods for t in range(T))
        if not contributes:
            continue

        best_perm = None
        best_score = -999999

        for perm in set(itertools.permutations(slots)):
            rep_t = _count_reps_for_each_t(perm)
            score = 0
            for t in range(T):
                if not rep_t[t]:
                    continue
                # 这个排列在 t 月产生重复
                remaining = target[t] - filled[t]
                if remaining > 0:
                    # 还缺重复，贡献它 → 奖励
                    score += 10 + remaining  # 越缺奖励越高
                elif remaining <= -10:
                    # 严重超额 → 重罚
                    score -= 200
                elif remaining < 0:
                    # 轻微超额 → 轻罚
                    score -= 50
                # remaining ≈ 0 时无惩罚（允许微小偏差）
            if score > best_score:
                best_score = score
                best_perm = list(perm)

        if best_perm is not None and best_score > -999999:
            # 更新 filled 计数
            old_reps = _count_reps_for_each_t(slots)
            new_reps = _count_reps_for_each_t(best_perm)
            for t in range(T):
                if old_reps[t]:
                    filled[t] -= 1
                if new_reps[t]:
                    filled[t] += 1
            obj["slots"] = best_perm

    # 重算覆盖率
    for obj in results:
        obj["used"] = set(obj["slots"])
        obj["coverage"] = len(obj["used"]) / K


def _count_reps_for_each_t(slots: list[int]) -> list[int]:
    """计算一个对象在每个时间步是否有重复（0/1 布尔值）"""
    T = len(slots)
    reps = [0] * T
    seen = set()
    for t, s in enumerate(slots):
        if s in seen:
            reps[t] = 1
        seen.add(s)
    return reps


def _redistribute_reps_fallback(
    results: list[dict],
    T: int,
    target: list[int],
    K: int,
) -> None:
    """T>6 时的近似回退：多次随机排列取最优，使用 running filled"""
    current = _count_reps(results, T)
    excess_periods = {t for t in range(T) if current[t] > target[t]}
    if not excess_periods:
        return
    filled = list(current)

    for obj in results:
        slots = obj["slots"]
        obj_reps = _count_reps_for_each_t(slots)
        contributes = any(obj_reps[t] and t in excess_periods for t in range(T))
        if not contributes:
            continue

        best_perm = None
        best_score = -999999

        for _ in range(500):
            perm = slots[:]
            random.shuffle(perm)
            rep_t = _count_reps_for_each_t(perm)
            score = 0
            for t in range(T):
                if not rep_t[t]:
                    continue
                remaining = target[t] - filled[t]
                if remaining > 0:
                    score += 10 + remaining
                elif remaining <= -10:
                    score -= 200
                elif remaining < 0:
                    score -= 50
            if score > best_score:
                best_score = score
                best_perm = perm

        if best_perm is not None and best_score > -999999:
            old_reps = _count_reps_for_each_t(slots)
            new_reps = _count_reps_for_each_t(best_perm)
            for t in range(T):
                if old_reps[t]:
                    filled[t] -= 1
                if new_reps[t]:
                    filled[t] += 1
            obj["slots"] = best_perm


def _post_random(
    results: list[dict],
    K: int,
    seed: int | None = None,
) -> list[dict]:
    """随机打乱每个对象的 slots（对象间配额不变，覆盖率不变）"""
    rng = random.Random(seed) if seed is not None else random
    for obj in results:
        rng.shuffle(obj["slots"])
        obj["used"] = set(obj["slots"])
        obj["coverage"] = len(obj["used"]) / K
    return results
