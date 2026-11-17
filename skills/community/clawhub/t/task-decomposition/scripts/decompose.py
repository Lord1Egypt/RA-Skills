#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
decompose.py — 任务分解器（WBS 生成）。

把目标拆成 阶段→任务→步骤，附依赖、工时估算、执行顺序。纯规则、本地可跑。

用法:
  python decompose.py --goal "上线一个用户反馈收集网页" --context "React+FastAPI" --out wbs.json
  python decompose.py --goal "写一份产品白皮书" --markdown wbs.md
"""
import os, sys, json, argparse

LIFECYCLE = ["调研/分析", "设计/规划", "实现/执行", "验证/测试", "交付/发布"]

# 阶段 -> 该阶段默认产出的任务模板（用目标短语填充）
PHASE_TASKS = {
    "调研/分析": ["明确目标与成功标准", "梳理约束与可用资源", "调研同类方案/竞品"],
    "设计/规划": ["确定整体方案与架构", "定义产出结构与接口", "制定排期与分工"],
    "实现/执行": ["搭建基础骨架", "实现核心功能", "补充边界与异常处理"],
    "验证/测试": ["编写/执行验证用例", "自查质量门禁", "修复发现的问题"],
    "交付/发布": ["整理交付物与文档", "发布/上线", "复盘与沉淀经验"],
}


def effort_for(phase, idx):
    # 粗略：实现阶段最重
    if phase == "实现/执行":
        return "L" if idx == 1 else "M"
    if phase in ("调研/分析", "设计/规划"):
        return "M"
    return "S"


def decompose(goal, context=""):
    g = goal.strip()
    phases = []
    for ph in LIFECYCLE:
        tasks = []
        for i, tname in enumerate(PHASE_TASKS[ph]):
            steps = [
                f"针对「{g}」，{tname}（结合上下文：{context or '无'}）",
                "产出可检查的中间结果",
                "记录决策与待办",
            ]
            tasks.append({
                "task": tname,
                "steps": steps,
                "effort": effort_for(ph, i),
                "depends_on": [PHASE_TASKS[ph][i - 1]] if i > 0 else ([LIFECYCLE[LIFECYCLE.index(ph) - 1]] if ph != LIFECYCLE[0] else []),
            })
        phases.append({"phase": ph, "tasks": tasks})
    total = "L" if any(t["effort"] == "L" for p in phases for t in p["tasks"]) else "M"
    return {
        "goal": g,
        "context": context,
        "phases": phases,
        "order": LIFECYCLE,
        "total_effort": total,
    }


def to_markdown(wbs):
    lines = [f"# 任务分解：{wbs['goal']}", ""]
    if wbs.get("context"):
        lines.append(f"> 上下文：{wbs['context']}")
        lines.append("")
    for ph in wbs["phases"]:
        lines.append(f"## {ph['phase']}")
        for t in ph["tasks"]:
            lines.append(f"- **{t['task']}** _(工时:{t['effort']})_")
            for s in t["steps"]:
                lines.append(f"  - {s}")
        lines.append("")
    lines.append(f"**建议顺序**：{' → '.join(wbs['order'])}")
    lines.append(f"**总工时估算**：{wbs['total_effort']}")
    return "\n".join(lines)


def main():
    ap = argparse.ArgumentParser(description="任务分解器")
    ap.add_argument("--goal", required=True)
    ap.add_argument("--context", default="")
    ap.add_argument("--out")
    ap.add_argument("--markdown")
    args = ap.parse_args()

    wbs = decompose(args.goal, args.context)
    if args.out:
        open(args.out, "w", encoding="utf-8").write(json.dumps(wbs, ensure_ascii=False, indent=2))
        print(f"✅ WBS 已生成 -> {args.out}（阶段 {len(wbs['phases'])}，总工时 {wbs['total_effort']}）")
    if args.markdown:
        open(args.markdown, "w", encoding="utf-8").write(to_markdown(wbs))
        print(f"✅ Markdown WBS -> {args.markdown}")
    if not args.out and not args.markdown:
        print(to_markdown(wbs))


if __name__ == "__main__":
    main()
