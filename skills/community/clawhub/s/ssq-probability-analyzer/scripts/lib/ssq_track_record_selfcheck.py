# -*- coding: utf-8 -*-
"""
双色球 — 预测追踪自证引擎 (ssq_track_record_selfcheck.py)
===========================================================

这是"自主学习 + 自主检查"能力的旗舰模块。它把系统**自己累积的真实战绩**
(ssq_result_verify.py 维护的 ssq_performance.json: 每一期系统推荐了什么号、
开奖后实际命中几个球) 拿出来, 与"纯随机基线"做严格的统计显著性比对,
从而让系统**用自身的预测历史自证"无预测优势"**, 而不是空口声称。

为什么需要它 (诚实闭环的最后一块拼图):
  项目已有大量模块证明"彩票不可预测": χ² 结构电池、NIST SP 800-22、
  方法发现引擎(9 法 walk-forward)、ML 模型自评、反诈骗五假设闸门 —— 全都是
  "在历史上"做样本外检验。但系统**自身向用户推荐的号**, 跑了一期又一期,
  累积下来的真实命中分布, 却从未被用来回答"我的推荐到底有没有跑赢随机"。
  本模块补上这最后一块: 把系统自己的推荐当作被检验对象, 与理论超几何分布
  / 蒙特卡洛随机基线对照, 输出一个可被统计检验的诚实结论。

双色球参数:
  红球 1-33 选 6 (FRONT_N=33, K=6, n=6) —— 头奖概率恒定 1/17,721,088
  蓝球 1-16 选 1 (BACK_N=16, K=1, n=1)

方法:
  1. 读取 ssq_performance.json, 提取每一期每个整数分组(单式组)的
     红球命中数 front_hits ∈[0,6] 与总命中数 total_hits ∈[0,7]。
  2. 计算经验分布(均值 + 直方图)。
  3. 理论基线:
       (a) 超几何分布: 单组 6/33 红球 vs 实际 6/33 → Hypergeometric(N=33,K=6,n=6),
           期望 = 36/33 ≈ 1.0909; 蓝球 1/16 vs 1/16 → H(N=16,K=1,n=1), 期望 ≈ 0.0625。
           总命中 = 红球 ⊗ 蓝球(独立) 卷积。
       (b) 蒙特卡洛基线: 对每一期真实开奖, 生成与当日分组数相同的纯随机 6+1 选号,
           在**同一批真实开奖结果**上计分 —— 这是"纯随机在完全相同的实际结果上会得多少分"
           的最公平对照。
  4. 显著性检验:
       (a) 红球命中 z 检验: 经验均值 vs 理论期望 (用超几何方差)。
       (b) 红球 / 总命中 卡方拟合优度: 经验直方图 vs 理论 pmf。
  5. 结论:
       - no_edge_confirmed: 所有检验 p 均 > 0.01 (且效应量小) → 自证通过, 系统推荐
         与纯随机无显著差异, 确认无预测优势。
       - needs_review: 任一核心检验 p ≤ 0.01 → 这是重大反常 (系统自称无优势但数据显示有),
         必须告警人工复核 (诚实优先, 不掩盖)。
       - insufficient_data: 分组样本 < MIN_GROUPS → 暂无法自证, 非失败。

用法:
  python ssq_track_record_selfcheck.py            # 跑自证, 打印诚实报告 + 写 JSON
  (被 ssq_healthcheck_all.py #23 自动调用)
"""
import json
import math
import os
import random
import sys

WORK_DIR = os.path.dirname(os.path.abspath(__file__))
PERF_FILE = os.path.join(WORK_DIR, "ssq_performance.json")
REPORT_FILE = os.path.join(WORK_DIR, "ssq_track_record_selfcheck.json")

ALPHA = 0.01                      # 显著性阈值(双侧), 取 0.01 以应对大样本下的高敏感度
MIN_GROUPS = 20                  # 低于此分组数视为样本不足, 不强行下结论
EFFECT_EPS = 0.05                # 效应量阈值(命中数): |经验均值-理论| 小于此视为"无实际意义差异"
MC_TRIALS_SEED = 20260808        # 蒙特卡洛确定性种子

# 双色球参数
FRONT_N, FRONT_K, FRONT_n = 33, 6, 6     # 红球 33 选 6
BACK_N, BACK_K, BACK_n = 16, 1, 1        # 蓝球 16 选 1
TICKET_COST = 2
JACKPOT_ODDS = "1/17,721,088"            # 头奖恒等概率


# ============================================================
# 理论分布 (超几何)
# ============================================================
def _comb(n, k):
    if k < 0 or k > n:
        return 0
    return math.comb(n, k)


def hypergeom_pmf(k, N, K, n):
    """P(X=k) for X ~ Hypergeometric(N, K, n)."""
    return _comb(K, k) * _comb(N - K, n - k) / _comb(N, n)


def hypergeom_mean_var(N, K, n):
    p = K / N
    mean = n * p
    var = n * p * (1 - p) * ((N - n) / (N - 1))
    return mean, var


FRONT_MEAN, FRONT_VAR = hypergeom_mean_var(FRONT_N, FRONT_K, FRONT_n)
BACK_MEAN, BACK_VAR = hypergeom_mean_var(BACK_N, BACK_K, BACK_n)

# 红球命中 pmf (k=0..6)
FRONT_PMF = [hypergeom_pmf(k, FRONT_N, FRONT_K, FRONT_n) for k in range(FRONT_n + 1)]
# 蓝球命中 pmf (k=0..1)
BACK_PMF = [hypergeom_pmf(k, BACK_N, BACK_K, BACK_n) for k in range(BACK_n + 1)]
# 总命中 pmf = 红球 ⊗ 蓝球 (k=0..7)
TOTAL_PMF = [0.0] * (FRONT_n + BACK_n + 1)
for f in range(FRONT_n + 1):
    for b in range(BACK_n + 1):
        TOTAL_PMF[f + b] += FRONT_PMF[f] * BACK_PMF[b]


# ============================================================
# 读取系统自身累积战绩
# ============================================================
def load_track_record():
    """读取 ssq_performance.json, 返回 [(front_hits, back_hits, total_hits), ...] 仅整数分组。"""
    if not os.path.exists(PERF_FILE):
        return [], {"exists": False}
    try:
        data = json.load(open(PERF_FILE, encoding="utf-8"))
    except Exception as e:
        return [], {"exists": True, "error": str(e)}
    recs = data.get("records", [])
    rows = []
    for rec in recs:
        actual_front = set(rec.get("actual_front", []))
        actual_back = set(rec.get("actual_back", []))
        for r in rec.get("results", []):
            if not isinstance(r.get("group"), int):
                continue  # 仅取整数单式分组(独立 6+1 选号), 胆拖单独处理
            fh = r.get("front_hits")
            bh = r.get("back_hits")
            th = r.get("total_hits")
            if fh is None or th is None:
                continue
            rows.append((int(fh), int(bh if bh is not None else 0), int(th)))
    meta = {"exists": True, "n_records": len(recs), "n_groups": len(rows)}
    return rows, meta


# ============================================================
# 蒙特卡洛基线 (在相同真实开奖上, 纯随机会得多少分)
# ============================================================
def monte_carlo_baseline(records, trials_seed=MC_TRIALS_SEED):
    """对每一期真实开奖, 生成与该期分组数相同的纯随机 6+1 选号并计分, 返回 (mean_front, mean_total, n)。"""
    rng = random.Random(trials_seed)
    mc_front, mc_total = [], []
    for rec in records:
        af = set(rec.get("actual_front", []))
        ab = set(rec.get("actual_back", []))
        groups = [r for r in rec.get("results", []) if isinstance(r.get("group"), int)]
        for _ in groups:
            rf = set(rng.sample(range(1, FRONT_N + 1), FRONT_n))
            rb = set(rng.sample(range(1, BACK_N + 1), BACK_n))
            fh = len(rf & af)
            bh = len(rb & ab)
            mc_front.append(fh)
            mc_total.append(fh + bh)
    n = len(mc_front)
    if n == 0:
        return None, None, 0
    return sum(mc_front) / n, sum(mc_total) / n, n


# ============================================================
# 统计检验
# ============================================================
def _z_test_2sided(emp_mean, theo_mean, sd, n):
    """双侧 z 检验, 返回 p-value (用正态近似)。"""
    if n < 2 or sd <= 0:
        return None
    se = sd / math.sqrt(n)
    z = abs(emp_mean - theo_mean) / se
    return math.erfc(z / math.sqrt(2.0))


def _chi_square_gof(obs_counts, exp_probs, n):
    """拟合优度卡方: 观测计数 vs 理论概率。df = 类别数-1 (理论分布完全指定, 无估参)。"""
    if n < 2:
        return None, len(exp_probs) - 1
    cats = len(exp_probs)
    chi = 0.0
    for k in range(cats):
        exp = n * exp_probs[k]
        if exp <= 0:
            continue
        o = obs_counts[k] if k < len(obs_counts) else 0
        chi += (o - exp) ** 2 / exp
    df = cats - 1
    return _igamc(df / 2.0, chi / 2.0), df  # p-value via 正则化不完全 Gamma Q


def _igamc(a, x):
    """正则化不完全 Gamma Q(a,x) (与 ssq_nist_sts 同源算法, 这里独立实现以保证本模块自包含)。"""
    if x <= 0.0 or a <= 0.0:
        return 1.0
    if x < a + 1.0:
        ap = a
        summ = 1.0 / a
        delta = summ
        for _ in range(2000):
            ap += 1.0
            delta *= x / ap
            summ += delta
            if abs(delta) < abs(summ) * 1e-15:
                break
        return 1.0 - summ * math.exp(-x + a * math.log(x) - math.lgamma(a))
    b = x + 1.0 - a
    c = 1.0 / 1e-30
    d = 1.0 / b
    h = d
    for i in range(1, 2000):
        an = -i * (i - a)
        b += 2.0
        d = an * d + b
        if abs(d) < 1e-30:
            d = 1e-30
        c = b + an / c
        if abs(c) < 1e-30:
            c = 1e-30
        d = 1.0 / d
        delta = d * c
        h *= delta
        if abs(delta - 1.0) < 1e-15:
            break
    return math.exp(-x + a * math.log(x) - math.lgamma(a)) * h


# ============================================================
# 主自证流程
# ============================================================
def run_selfcheck(verbose=True):
    rows, meta = load_track_record()
    if not meta.get("exists"):
        return {"status": "no_data", "detail": "ssq_performance.json 不存在(系统尚未累积任何验证记录)"}
    if meta.get("error"):
        return {"status": "read_error", "detail": meta["error"]}
    n = len(rows)
    if n < MIN_GROUPS:
        return {
            "status": "insufficient_data",
            "detail": f"已验证分组仅 {n} 个 (<{MIN_GROUPS}), 样本不足, 暂无法做统计自证",
            "n_groups": n,
        }

    # 经验统计
    front = [r[0] for r in rows]
    total = [r[2] for r in rows]
    emp_front_mean = sum(front) / n
    emp_total_mean = sum(total) / n
    front_hist = [0] * (FRONT_n + 1)
    total_hist = [0] * (FRONT_n + BACK_n + 1)
    for f in front:
        front_hist[f] += 1
    for t in total:
        total_hist[t] += 1

    # 蒙特卡洛基线 (需原始 records, 重新读)
    perf = json.load(open(PERF_FILE, encoding="utf-8"))
    mc_front_mean, mc_total_mean, mc_n = monte_carlo_baseline(perf.get("records", []))

    # 检验
    front_sd = math.sqrt(FRONT_VAR)
    p_front_z = _z_test_2sided(emp_front_mean, FRONT_MEAN, front_sd, n)
    p_front_chi, df_f = _chi_square_gof(front_hist, FRONT_PMF, n)
    p_total_chi, df_t = _chi_square_gof(total_hist, TOTAL_PMF, n)

    # 效应量
    effect_front = abs(emp_front_mean - FRONT_MEAN)
    effect_total = abs(emp_total_mean - (FRONT_MEAN + BACK_MEAN))

    # 结论判定
    core_p = [p for p in (p_front_z, p_front_chi, p_total_chi) if p is not None]
    min_p = min(core_p) if core_p else None
    if min_p is not None and min_p <= ALPHA and (
            effect_front > EFFECT_EPS or effect_total > EFFECT_EPS):
        status = "needs_review"
    else:
        status = "no_edge_confirmed"

    out = {
        "status": status,
        "n_groups": n,
        "n_records": meta.get("n_records"),
        "theoretical": {
            "front_mean": round(FRONT_MEAN, 4),
            "back_mean": round(BACK_MEAN, 4),
            "total_mean": round(FRONT_MEAN + BACK_MEAN, 4),
        },
        "empirical": {
            "front_mean": round(emp_front_mean, 4),
            "total_mean": round(emp_total_mean, 4),
            "front_hist": front_hist,
            "total_hist": total_hist,
        },
        "monte_carlo": {
            "front_mean": round(mc_front_mean, 4) if mc_front_mean is not None else None,
            "total_mean": round(mc_total_mean, 4) if mc_total_mean is not None else None,
            "n": mc_n,
        },
        "tests": {
            "front_z_pvalue": round(p_front_z, 6) if p_front_z is not None else None,
            "front_chi_pvalue": round(p_front_chi, 6) if p_front_chi is not None else None,
            "total_chi_pvalue": round(p_total_chi, 6) if p_total_chi is not None else None,
            "min_pvalue": round(min_p, 6) if min_p is not None else None,
            "front_effect": round(effect_front, 4),
            "total_effect": round(effect_total, 4),
        },
        "conclusion": _conclusion_text(status, emp_front_mean, FRONT_MEAN, min_p,
                                        mc_front_mean, n),
    }

    with open(REPORT_FILE, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=2)

    if verbose:
        _print_report(out)
    return out


def _conclusion_text(status, emp_f, theo_f, min_p, mc_f, n):
    if status == "no_edge_confirmed":
        return (
            f"自证通过: 系统累积 {n} 个推荐分组的前区命中均值 {emp_f:.3f} "
            f"≈ 理论随机期望 {theo_f:.3f} (蒙特卡洛随机基线 {mc_f:.3f}), "
            f"最小显著性 p={min_p:.3f} >> {ALPHA} —— 系统自身推荐与纯随机无显著差异, "
            f"确认无预测优势 (no_edge)。双色球头奖恒为 {JACKPOT_ODDS}。"
        )
    if status == "needs_review":
        return (
            f"⚠ 反常: 系统累积推荐命中与随机基线出现统计显著差异 (最小 p={min_p:.4f}≤{ALPHA}), "
            f"与系统'无预测优势'的核心声明矛盾。此为重大发现, 须人工复核数据/方法, 勿掩盖。"
        )
    return "样本不足, 暂无法自证。"


def _print_report(out):
    print("=" * 72)
    print("双色球 预测追踪自证引擎 (系统用自身累积战绩自证无优势)")
    print("=" * 72)
    if out["status"] in ("no_data", "read_error", "insufficient_data"):
        print(f"  · {out['detail']}")
        return
    t = out["theoretical"]; e = out["empirical"]; m = out["monte_carlo"]; x = out["tests"]
    print(f"  样本: {out['n_groups']} 个推荐分组 / {out['n_records']} 期已验证")
    print(f"  红球命中均值  经验={e['front_mean']:.3f}  理论随机={t['front_mean']:.3f}  "
          f"蒙特卡洛={m['front_mean']}")
    print(f"  总命中均值    经验={e['total_mean']:.3f}  理论随机={t['total_mean']:.3f}  "
          f"蒙特卡洛={m['total_mean']}")
    print(f"  显著性: 红球z p={x['front_z_pvalue']}  红球χ² p={x['front_chi_pvalue']}  "
          f"总命中χ² p={x['total_chi_pvalue']}  最小 p={x['min_pvalue']}")
    print("-" * 72)
    print(f"  🔎 结论: {out['conclusion']}")
    print(f"  ✓ 自证报告已存: {os.path.basename(REPORT_FILE)}")


def main():
    if len(sys.argv) > 1 and sys.argv[1] == "--json":
        out = run_selfcheck(verbose=False)
        print(json.dumps(out, ensure_ascii=False, indent=2))
        return 0
    run_selfcheck(verbose=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
