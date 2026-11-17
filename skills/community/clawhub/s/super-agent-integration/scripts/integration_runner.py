#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""integration_runner.py — 超级智能体「端到端自主闭环」真实跑通 harness（零依赖纯标准库）。

这是北极星"超越一线大模型"的最后一公里：把此前分散建成的单点能力
  long-horizon-planner(规划) / reason-verify(自验证) / continual-memory-engine(记忆)
  / memory-cross-engine(跨引擎记忆贯通) / reflection-replanner(反思重规划)
  / super-agent-bootstrap(执行内核) / agent-eval-harness(回归评测)
真实串成一次可运行、可被度量的端到端闭环，并产出健康度报告。

它不是薄壳：本脚本在运行期**真实 import 上述引擎并逐一调用**，跑通
「感知→规划→执行→自验证→反思重规划→跨引擎记忆→回归评测」全链路，
最后用 agent-eval-harness 量化健康度，判定闭环是否真的可用。

用法：
  python integration_runner.py --selftest
  python integration_runner.py --goal "将条目分类并汇总" --items "量子计算" --items "苹果股价" --workdir ./run1
"""
import os, sys, json, types, datetime

SKILLS = os.path.expanduser("~/.workbuddy/skills")


def _add(p):
    if p not in sys.path:
        sys.path.insert(0, p)


# —— 真实接入「四引擎 + 评测」生态（导入失败即显式报错，绝不静默降级成空转）——
_add(os.path.join(SKILLS, "super-agent-bootstrap/scripts"))
from super_agent import SuperAgent
_add(os.path.join(SKILLS, "memory-cross-engine/scripts"))
from memory_bus import MemoryBus
_add(os.path.join(SKILLS, "reflection-replanner/scripts"))
from replanner import Replanner
_add(os.path.join(SKILLS, "reason-verify/scripts"))
from verify import reason as reason_verify
_add(os.path.join(SKILLS, "agent-eval-harness/scripts"))
from eval_harness import EvalHarness, TestCase


def _verify_with_reason(question, answer, out_path):
    """用 reason-verify 引擎对一段论断做可靠性自验证。"""
    ns = types.SimpleNamespace(
        question=question, answer=answer, facts=None, out=out_path,
    )
    return reason_verify(ns)


def run_integration(goal, items, workdir):
    os.makedirs(workdir, exist_ok=True)
    mem_bus = MemoryBus(os.path.join(workdir, "memory_bus.jsonl"))
    agent = SuperAgent(os.path.join(workdir, "agent_memory.json"))

    # —— 1. 规划：把目标写进跨引擎记忆总线（planner 视角）——
    mem_bus.write("planner", "goal", goal)

    # —— 2-5. 执行内核跑通「感知→执行→自验证→反思重规划→记忆」——
    report = agent.run(goal, items)  # super-agent-bootstrap 内核
    verify_gate = bool(report.get("verify_gate"))
    replan_count = int(report.get("replan_count", 0))

    # —— 6. 自验证：用 reason-verify 对汇总论断做可靠性校验 ——
    summary = report.get("summary", {})
    answer_text = "分类汇总：" + "，".join(
        "%s=%d" % (k, v) for k, v in summary.items()
    )
    reason_out = os.path.join(workdir, "reason_summary.json")
    reason_rep = _verify_with_reason(
        "分类是否覆盖所有条目且每个分类合法", answer_text, reason_out
    )
    reason_rate = float(reason_rep.get("reliability", 0.0))

    # —— 7. 反思重规划：若自验证不达标，用 reflection-replanner 修订计划 ——
    extra_replans = 0
    if reason_rate < 0.8:
        plan = ["感知条目", "逐条分类", "校验分类合法性", "汇总数量"]
        trace = [{"step": s, "ok": True} for s in plan[:-1]] + [
            {"step": plan[-1], "ok": False}
        ]
        verify = {"passed": False, "issues": ["部分分类未被 reason-verify 判定可靠"]}
        rp = Replanner(plan, trace, verify)
        out = rp.replan()
        extra_replans += 1
        mem_bus.write("replanner", "revised_plan", json.dumps(out, ensure_ascii=False))
    total_replans = replan_count + extra_replans

    # —— 8. 跨引擎记忆贯通：把每个结果落盘并与目标关联 ——
    results = report.get("results", [])
    goal_id = "e0001"
    for r in results:
        eid = mem_bus.write(
            "memory", "result",
            "%s -> %s" % (r.get("item"), r.get("category")),
            links=[goal_id],
        )
    mem_bus.link(goal_id, eid) if results else None
    cross = mem_bus.cross_engine_view()

    # —— 9. 回归评测：用 agent-eval-harness 量化闭环健康度 ——
    def integrated_agent(prompt):
        # 把评测 prompt 当作一个待分类条目，复用同一内核
        rep = agent.run(goal, [prompt])
        hits = [r for r in rep.get("results", []) if r.get("item") == prompt]
        return hits[0]["category"] if hits else "其他"

    harness = EvalHarness(os.path.join(workdir, "regression.jsonl"))
    harness.add(TestCase("t_tech", "量子计算", expect_contains=["技术"]))
    harness.add(TestCase("t_fin", "苹果股价", expect_contains=["金融"]))
    harness.add(TestCase("t_life", "猫咪打盹", expect_contains=["生活"]))
    harness.add(TestCase("t_unk", "未知事物XYZ123", expect_contains=["其他"]))
    eval_summary = harness.run(integrated_agent)

    # —— 10. 健康度综合 ——
    health = round(
        0.35 * (1.0 if verify_gate else 0.0)
        + 0.30 * float(eval_summary.get("pass_rate", 0.0))
        + 0.20 * reason_rate
        + 0.15 * (1.0 if total_replans >= 1 else 0.0),
        3,
    )

    return {
        "goal": goal,
        "verify_gate": verify_gate,
        "replan_count": total_replans,
        "reason_verify_rate": round(reason_rate, 3),
        "eval_pass_rate": eval_summary.get("pass_rate"),
        "eval_regressed": eval_summary.get("regressed"),
        "memory_engines": cross.get("engines"),
        "memory_entries": cross.get("total"),
        "memory_links": cross.get("links"),
        "health_score": health,
        "verdict": "闭环可用" if health >= 0.85 else "闭环待改进",
    }


def selftest():
    wd = os.path.join(os.path.dirname(os.path.abspath(__file__)), "run_selftest")
    if os.path.isdir(wd):
        import shutil
        shutil.rmtree(wd)
    items = ["量子计算突破", "苹果股价创新高", "猫咪在阳光下打盹", "未知事物XYZ123"]
    rep = run_integration("将条目分类到技术/金融/生活并汇总", items, wd)

    print("[selftest] health report:", json.dumps(rep, ensure_ascii=False))

    assert rep["verify_gate"] is True, "❌ 验证门控应最终通过"
    assert rep["replan_count"] >= 1, "❌ 应触发至少一次反思重规划"
    assert rep["reason_verify_rate"] >= 0.8, "❌ reason-verify 可靠性应达标"
    assert rep["eval_pass_rate"] == 1.0, "❌ 回归评测通过率应为 1.0"
    assert rep["eval_regressed"] is False, "❌ 不应判定为能力回退"
    assert rep["memory_entries"] >= len(items), "❌ 跨引擎记忆条目应覆盖全部输入"
    assert rep["health_score"] >= 0.85, "❌ 闭环健康度应达标"
    assert rep["verdict"] == "闭环可用", "❌ 应判定闭环可用"

    if os.path.isdir(wd):
        import shutil
        shutil.rmtree(wd)
    print("✅ super-agent-integration selftest ALL PASS（四引擎 + 评测 真实串联跑通，health=%s）"
          % rep["health_score"])
    return True


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--selftest":
        selftest()
    elif "--goal" in sys.argv:
        i = sys.argv.index("--goal")
        goal = sys.argv[i + 1]
        items = []
        if "--items" in sys.argv:
            j = sys.argv.index("--items")
            k = j + 1
            while k < len(sys.argv) and not sys.argv[k].startswith("--"):
                items.append(sys.argv[k])
                k += 1
        wd = "./run_integration"
        if "--workdir" in sys.argv:
            wd = sys.argv[sys.argv.index("--workdir") + 1]
        print(json.dumps(run_integration(goal, items, wd), ensure_ascii=False, indent=2))
    else:
        print("用法: python integration_runner.py --selftest")
