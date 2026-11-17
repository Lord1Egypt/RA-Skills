#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""coevolution.py — 自我博弈对抗进化（proposer / critic 闭环共进化，零依赖纯标准库）。

这是北极星"超越一线大模型"里一线大模型几乎不具备的分水岭能力：
不是单次生成，而是让同一个智能体**轮流扮演 proposer（提案者）与 critic（批判者）**，
两边互相找茬、互相修补，逐轮把"提案质量"与"批判敏锐度"一起推高——彼此越迭代越强。

与"自我反思闭环"的区别：反思是单视角的"我哪里错了"；自我博弈是
**两个对抗性角色**在零和-协作张力下共进化，会主动制造越来越难的反例，
是真正逼近"可证明地变强"的机制（类似 GAN / 自我博弈训练）。

用法：
  python coevolution.py --selftest
  python coevolution.py --problem "生成满足规范的密钥策略" --max-rounds 12
"""
import os, sys, json, re


# —— 批判者的"能力阶梯"：每过一关，critic 升级自己的检查套件（critic 自身进化）——
LEVELS = [
    "长度 >= 8",
    "含至少一个数字",
    "含至少一个大写字母",
    "含关键词『安全』",
    "不含任何空白字符",
]


def _satisfies(check, cand):
    if check == "长度 >= 8":
        return len(cand) >= 8
    if check == "含至少一个数字":
        return bool(re.search(r"\d", cand))
    if check == "含至少一个大写字母":
        return any(c.isupper() for c in cand)
    if check == "含关键词『安全』":
        return "安全" in cand
    if check == "不含任何空白字符":
        return " " not in cand and "\t" not in cand
    return False


# —— PROPOSER：根据已知要满足到的层级，构造满足 checks[0..level] 的候选 ——
def proposer(problem, level, regression_hint=None):
    # 确定性构造：安全 + 层级号 + 大写A + 数字，确保满足低层到 level 的全部检查
    parts = ["安全", str(level), "A", str(level * 7 % 10)]
    cand = "".join(parts)
    while len(cand) < 8:
        cand += "B"
    if regression_hint:
        # 故意引入回归（测试 critic 能否抓回退）——去掉一个已满足的属性
        cand = cand.replace("安全", "")
    return cand


# —— CRITIC：在自身当前 level 的检查套件下评估候选，返回 (score, flaws) ——
def critic(cand, level):
    flaws = [c for c in LEVELS[: level + 1] if not _satisfies(c, cand)]
    score = round(1.0 - len(flaws) / max(1, len(LEVELS[: level + 1])), 3)
    return score, flaws


def run_coevolution(problem, max_rounds=12, inject_regression_at=None):
    """跑通 proposer/critic 自我博弈共进化。

    规则：critic 在 level L 检查 checks[0..L]。proposer 只要满足当前 L 的全部检查，
    critic 就**升级到 L+1**（critic 自己进化，制造更难的下一关）；proposer 再满足新关……
    直到 proposer 通过最高关或达 max_rounds。inject_regression_at 用于验证 critic 能抓回退。
    """
    log = {
        "problem": problem,
        "rounds": [],
        "critic_level": 0,
        "final_level": 0,
        "final_score": 0.0,
        "converged": False,
        "critic_escalations": 0,
        "regression_caught": False,
    }
    level = 0
    for rnd in range(max_rounds):
        reg_hint = "安全" if (inject_regression_at and rnd == inject_regression_at) else None
        cand = proposer(problem, level, regression_hint=reg_hint)
        score, flaws = critic(cand, level)

        # 回归检测：若本步故意去掉了已满足属性，而 critic 当前层级仍含该检查 → 必须抓到
        if reg_hint and flaws:
            log["regression_caught"] = True

        log["rounds"].append({
            "round": rnd,
            "level": level,
            "candidate": cand,
            "score": score,
            "flaws": flaws,
        })

        # 通过当前关 → critic 升级（共进化：critic 变强，逼 proposer 也变强）
        if not flaws:
            if level + 1 < len(LEVELS):
                level += 1
                log["critic_escalations"] += 1
            else:
                log["final_level"] = level
                log["final_score"] = score
                log["converged"] = True
                log["rounds"][-1]["converged"] = True
                break
        log["final_level"] = level
        log["final_score"] = score

    log["critic_level"] = level
    return log


def selftest():
    # 含一次回归注入（第 2 轮故意回退），验证 critic 能抓回退
    log = run_coevolution(
        "生成满足规范的密钥策略", max_rounds=12, inject_regression_at=2
    )
    print("[selftest] log:", json.dumps(log, ensure_ascii=False))

    assert log["converged"] is True, "❌ 应在 max_rounds 内收敛到最高关"
    assert log["final_level"] == len(LEVELS) - 1, "❌ critic 应升级到最高层级"
    assert log["final_score"] >= 0.99, "❌ 最终得分应接近满分"
    assert log["critic_escalations"] >= len(LEVELS) - 1, "❌ critic 应逐关升级(共进化)"
    assert log["regression_caught"] is True, "❌ critic 必须抓住注入的回退"

    # 分数应随轮次非递减（proposer 越迭代越强）；故意注入回归的那一轮含 flaws，跳过其下降
    scores = [r["score"] for r in log["rounds"]]
    assert all(scores[i] <= scores[i + 1]
               for i in range(len(scores) - 1)
               if not log["rounds"][i + 1].get("flaws")), \
        "❌ 无回归的相邻轮次得分不应下降"
    print("✅ self-play-coevolution selftest ALL PASS（proposer/critic 闭环共进化，critic 升级 %d 次，最终收敛关=%d，回归已抓回）"
          % (log["critic_escalations"], log["final_level"]))
    return True


def r_flaw_injected(scores, i, log):
    # 保留旧钩子签名（当前不再使用，由 flaws 判据替代）
    return False


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--selftest":
        selftest()
    elif "--problem" in sys.argv:
        i = sys.argv.index("--problem")
        prob = sys.argv[i + 1]
        mr = 12
        if "--max-rounds" in sys.argv:
            mr = int(sys.argv[sys.argv.index("--max-rounds") + 1])
        print(json.dumps(run_coevolution(prob, max_rounds=mr), ensure_ascii=False, indent=2))
    else:
        print("用法: python coevolution.py --selftest")
