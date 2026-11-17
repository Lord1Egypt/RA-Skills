---
name: task-decomposition
description: |
  任务分解器。把一句目标/需求自动拆成可执行的层级化工作分解结构（WBS）：阶段 → 任务 → 步骤，附依赖关系、工时估算（S/M/L）与建议执行顺序。纯规则、本地可跑，把"我要做 X"变成"第 1 步做 A、第 2 步做 B"。当用户需要"把这个目标拆成任务""帮我规划步骤""做个 WBS""decompose this goal""制定执行计划"时调用。
agent_created: true
visibility: "public"
---

# 任务分解器（Task Decomposition）

把模糊目标变成可落地的执行清单。核心：**分解不是罗列，而是给出顺序、依赖与工时**，让执行者知道先做什么、为什么。

## 适用场景
- 接到一个宏观目标，不知道从哪下手
- 项目启动前做 WBS（工作分解结构）
- 把"大任务"派给子 agent / 团队前先做切分
- 估算工作量、排期

## 分解框架（默认生命周期）
1. **调研/分析** — 搞清楚要什么、有什么约束
2. **设计/规划** — 定方案、定结构
3. **实现/执行** — 真正产出
4. **验证/测试** — 确认达标
5. **交付/发布** — 交付并复盘

## 标准工作流
```bash
python scripts/decompose.py --goal "上线一个用户反馈收集网页" --context "用 React+FastAPI" --out wbs.json
# 直接看 Markdown
python scripts/decompose.py --goal "写一份产品白皮书" --markdown wbs.md
```

输出 WBS 结构：
```json
{
  "goal": "...",
  "phases": [
    {"phase":"调研/分析","tasks":[{"task":"...","steps":[...],"effort":"M","depends_on":[]}]}
  ],
  "order": ["调研/分析","设计/规划","实现/执行","验证/测试","交付/发布"],
  "total_effort": "L"
}
```

## 质量门禁
- 每个任务是否都有可验证的完成标准？
- 依赖关系是否构成无环 DAG（避免互相依赖死锁）？

## 自进化学习系统
```bash
python scripts/learner.py record . --capability "任务分解" [--fail --error <类型> --note <说明>]
python scripts/learner.py insight .
python scripts/learner.py reflect .
```
- 某类目标总是缺某阶段 → 记录，reflect 建议把该阶段加入默认生命周期
- 用户常用技术栈 → `prefer` 记录，未来分解时自动带约束
