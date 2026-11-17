#!/usr/bin/env python3
"""策略画布生成：按选定框架（SWOT/OODA/Scenario/FirstPrinciples）渲染结构化策略文档。"""
import argparse, os


FRAMEWORKS = {
    "swot": """# 策略画布 · SWOT

## 目标
{goal}

## 约束与上下文
{context}

## S 优势（内部）
{strength}

## W 劣势（内部）
{weakness}

## O 机会（外部）
{opportunity}

## T 威胁（外部）
{threat}

## 策略组合（SO/WO/ST/WT）
{combos}

## 度量
{metrics}
""",
    "ooda": """# 策略画布 · OODA

## 目标
{goal}

## 约束与上下文
{context}

## Observe 观察
{observe}

## Orient 定位（解读）
{orient}

## Decide 决策（选项与取舍）
{decide}

## Act 行动（首批动作）
{act}

## 反馈回路
{feedback}
""",
    "scenario": """# 策略画布 · 情景规划

## 目标
{goal}

## 约束与上下文
{context}

## 最好情景（及触发条件）
{best}

## 中性情景
{neutral}

## 最坏情景（及触发条件）
{worst}

## 鲁棒策略（跨情景通用）
{robust}

## 早期信号监控
{signals}
""",
    "first_principles": """# 策略画布 · 第一性原理

## 目标
{goal}

## 约束与上下文
{context}

## 不可再分的事实
{facts}

## 从事实重建的方案
{rebuild}

## 验证方式
{verify}
""",
}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--goal", required=True)
    ap.add_argument("--context", default="（待补充）")
    ap.add_argument("--framework", default="swot",
                    choices=list(FRAMEWORKS.keys()))
    ap.add_argument("--output", default=None)
    args = ap.parse_args()
    ph = "（待补充：由 agent 基于上下文补全）"
    doc = FRAMEWORKS[args.framework].format(
        goal=args.goal, context=args.context,
        strength=ph, weakness=ph, opportunity=ph, threat=ph,
        combos=ph, metrics=ph,
        observe=ph, orient=ph, decide=ph, act=ph, feedback=ph,
        best=ph, neutral=ph, worst=ph, robust=ph, signals=ph,
        facts=ph, rebuild=ph, verify=ph,
    )
    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(doc)
        print(f"✅ 策略画布已写入：{args.output}（框架={args.framework}）")
    else:
        print(doc)


if __name__ == "__main__":
    main()
