#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
submit_daily.py —— 每日精提:可过性预测 → 推荐最优 1-2 个 → 人工确认后提交(SKILL.md §④)

流程:
1. 分页拉 GET /users/self/alphas(status=ACTIVE)作为自相关基准(basis),
   各自的 PnL 日收益缓存到 wq_workspace/pnl_cache/ 避免重复拉
2. 对 pool.jsonl 里"尚未提交过"的候选,算对 ACTIVE 集合的 max |Pearson corr|
   ——这就是 SKILL.md §4.2 的"可过性预测器"(<0.70 SAFE / ≥0.75 必被挡)
3. 只推荐 corr < 0.70 的,按(universe 越小越优 → Fitness 降序)排序取前 2
   ——"每天只提最优 1-2 个,绝不掺弱"(§4.3,当天分是平均值)
4. 打印推荐表格后,逐个交互确认 y/N ——【提交永远人在环,无任何跳过确认的开关】
5. 确认后 POST /alphas/{id}/submit,轮询到 ACTIVE 或失败(打印 checks 里的失败项,
   如 SELF_CORRELATION),结果追加 wq_workspace/submit_log.jsonl

用法:
    python scripts/submit_daily.py

注意:按 3AM EDT 规划每日提交窗口(§1.3);断一天 = 永久少一天的分。
"""

import sys
import time

from wq_common import (
    BASE,
    CORR_SUBMIT_MAX,
    POLL_INTERVAL,
    POOL_PATH,
    SUBMIT_LOG_PATH,
    BrainSession,
    alpha_failed_checks,
    append_jsonl,
    ensure_workspace,
    get_alpha,
    get_daily_returns,
    load_jsonl,
    max_abs_corr,
    paginate,
    universe_size,
)

DAILY_PICK = 2            # 每天只提最优 1-2 个(SKILL.md §4.3 红线,勿调大)
SUBMIT_TIMEOUT = 900      # 单次提交校验最长等待(秒)


def fetch_active_basis(bs):
    """拉全部 status=ACTIVE 的 alpha 及其日收益(PnL 有本地缓存)。"""
    print("[1/4] 分页拉取已 ACTIVE 集合(自相关基准)…")
    actives = paginate(bs, f"{BASE}/users/self/alphas",
                       params={"status": "ACTIVE"})
    print(f"      当前 ACTIVE alpha:{len(actives)} 个")
    basis = []
    for a in actives:
        aid = a.get("id")
        if not aid:
            continue
        rets = get_daily_returns(bs, aid)   # 缓存在 wq_workspace/pnl_cache/
        if rets:
            basis.append(rets)
    if actives and len(basis) < len(actives):
        print(f"      [提示] 其中 {len(actives) - len(basis)} 个拉不到 PnL,基准不含它们")
    return basis


def already_submitted_ids():
    """从 submit_log.jsonl 读已提交(含提交失败)的 alpha id 集合。

    提交失败的也不再自动推荐——同一个 alpha 再提大概率同样的 check 再挂;
    确要重试,请手动编辑 wq_workspace/submit_log.jsonl 删掉对应行。
    """
    return {e.get("alpha_id") for e in load_jsonl(SUBMIT_LOG_PATH) if e.get("alpha_id")}


def score_candidates(bs, basis):
    """对池内未提交候选算可过性,返回 (推荐列表, 被排除列表)。"""
    pool = load_jsonl(POOL_PATH)
    done = already_submitted_ids()
    seen = set()
    fresh = []
    for c in pool:
        aid = c.get("alpha_id")
        if not aid or aid in done or aid in seen:
            continue
        seen.add(aid)
        fresh.append(c)
    print(f"[2/4] 候选池共 {len(pool)} 条,未提交 {len(fresh)} 条,逐个算可过性 …")

    eligible, excluded = [], []
    for c in fresh:
        rets = get_daily_returns(bs, c["alpha_id"])
        if not rets:
            c["_why"] = "拉不到 PnL,无法算相关"
            excluded.append(c)
            continue
        corr = max_abs_corr(rets, basis)
        c["max_corr_to_active"] = round(corr, 4)
        if corr < CORR_SUBMIT_MAX:
            eligible.append(c)
        else:
            c["_why"] = f"对 ACTIVE 集合相关 {corr:.2f} ≥ {CORR_SUBMIT_MAX}(会被自相关门槛挡)"
            excluded.append(c)

    # 排序:universe 越小越优,其次 Fitness 降序(SKILL.md §4.3 挑选优先级)
    eligible.sort(key=lambda c: (universe_size(c.get("universe")),
                                 -(c.get("fitness") or 0.0)))
    return eligible, excluded


def print_table(eligible, excluded):
    """打印推荐表格与排除原因(排除原因也要说清,§5.6 模板 B 的纪律)。"""
    print("\n[3/4] 今日推荐(corr<0.70,universe 小者优先,Fitness 降序,取前 2)")
    if not eligible:
        print("  没有可提交的候选。回去挖矿(mine.py)或做正交(换数据角色/分母,§3.4)。")
    else:
        hdr = f"  {'#':<3}{'alpha_id':<12}{'universe':<10}{'Sharpe':>7}{'Fitness':>8}{'corr':>6}  表达式"
        print(hdr)
        print("  " + "-" * (len(hdr) + 20))
        for i, c in enumerate(eligible):
            star = "★" if i < DAILY_PICK else " "
            expr = c.get("expression", "")
            if len(expr) > 52:
                expr = expr[:49] + "…"
            print(f"  {star}{i + 1:<2}{str(c.get('alpha_id')):<12}"
                  f"{str(c.get('universe')):<10}"
                  f"{_fmt(c.get('sharpe')):>7}{_fmt(c.get('fitness')):>8}"
                  f"{c.get('max_corr_to_active', 0):>6.2f}  {expr}")
        print(f"  (★ = 今日建议提交,最多 {DAILY_PICK} 个;当天分是平均值,绝不掺弱)")

    if excluded:
        print("\n  被排除的候选及原因:")
        for c in excluded:
            print(f"    - {c.get('alpha_id')}:{c.get('_why', '未知原因')}")


def submit_one(bs, cand):
    """POST /alphas/{id}/submit,轮询到 ACTIVE 或失败;返回 (result, fails)。"""
    aid = cand["alpha_id"]
    r = bs.post(f"{BASE}/alphas/{aid}/submit")
    if r.status_code not in (200, 201):
        print(f"    [提交被拒] HTTP {r.status_code}:{r.text[:200]}")
        return "POST_REJECTED", [f"HTTP {r.status_code}"]

    print(f"    已发起提交,轮询平台校验(每 {POLL_INTERVAL}s)…")
    started = time.time()
    while True:
        time.sleep(POLL_INTERVAL)
        alpha = get_alpha(bs, aid)
        status = alpha.get("status", "")
        fails = alpha_failed_checks(alpha)
        if status == "ACTIVE":
            print("    ✅ ACTIVE —— 通过全部校验,已进账!")
            return "ACTIVE", []
        if status in ("FAILED", "REJECTED") or (status == "UNSUBMITTED" and fails):
            # 平台判完:读 checks 里的 FAIL 项(如 SELF_CORRELATION / LOW_SHARPE)
            print(f"    ❌ 被挡(status={status}),失败项:{fails or ['未知']}")
            if "SELF_CORRELATION" in fails or "HIGH_CORRELATION" in fails:
                print("       → 自相关超标:换数据角色/换分母重构,别改中性化硬凑(§避坑⑤)")
            return "FAIL", fails
        if time.time() - started > SUBMIT_TIMEOUT:
            print(f"    [超时] 校验超过 {SUBMIT_TIMEOUT}s 未出结果,请稍后网页端核对")
            return "TIMEOUT", []
        # PENDING / CHECKING 等中间态:继续轮询


def main():
    ensure_workspace()
    if not POOL_PATH.exists():
        print(f"[错误] 找不到候选池 {POOL_PATH}。请先跑:python scripts/mine.py")
        sys.exit(1)

    bs = BrainSession()
    basis = fetch_active_basis(bs)
    eligible, excluded = score_candidates(bs, basis)
    print_table(eligible, excluded)

    picks = eligible[:DAILY_PICK]
    if not picks:
        return

    # ---- 人在环红线:每一个提交都必须人工逐个确认,没有任何跳过确认的开关 ----
    if not sys.stdin.isatty():
        print("\n[4/4] 检测到非交互环境:提交必须人工确认(SKILL.md 红线),"
              "本次不提交任何 alpha。请在终端里手动运行本脚本。")
        return

    print(f"\n[4/4] 逐个确认提交(共 {len(picks)} 个候选)")
    for c in picks:
        print(f"\n  候选 {c['alpha_id']}:{c.get('expression', '')}")
        print(f"    Sharpe={_fmt(c.get('sharpe'))}  Fitness={_fmt(c.get('fitness'))}  "
              f"universe={c.get('universe')}  对ACTIVE相关={c.get('max_corr_to_active')}")
        try:
            ans = input("    确认提交这个 alpha 进 Challenge?[y/N] ").strip().lower()
        except EOFError:
            ans = ""
        if ans != "y":
            print("    已跳过(未提交)。")
            append_jsonl(SUBMIT_LOG_PATH, {
                "alpha_id": None,   # 不记 alpha_id,保留下次再被推荐的资格
                "skipped_alpha_id": c["alpha_id"],
                "expression": c.get("expression"),
                "result": "SKIPPED_BY_USER",
                "at": time.strftime("%Y-%m-%d %H:%M:%S"),
            })
            continue

        result, fails = submit_one(bs, c)
        append_jsonl(SUBMIT_LOG_PATH, {
            "alpha_id": c["alpha_id"],
            "expression": c.get("expression"),
            "universe": c.get("universe"),
            "sharpe": c.get("sharpe"),
            "fitness": c.get("fitness"),
            "max_corr_to_active": c.get("max_corr_to_active"),
            "result": result,
            "fails": fails,
            "at": time.strftime("%Y-%m-%d %H:%M:%S"),
        })

    print("\n完成。明天 3AM EDT 刷新后跑 python scripts/check_score.py 核对分数是否上涨。")


def _fmt(v):
    return f"{v:.2f}" if isinstance(v, (int, float)) else "N/A"


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n[中断] 已手动停止;已完成的提交记录在", SUBMIT_LOG_PATH)
        sys.exit(130)
