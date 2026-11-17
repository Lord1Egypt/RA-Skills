---
name: toolchain-orchestrator
description: |
  多步工具链编排引擎（超越性元能力）。以「规划器为中心」把多工具任务定义为依赖 DAG，确定性地按拓扑序执行，
  节点间通过 {{node_id}} 透传上游输出，支持校验/断点重跑/可视化。克服 ReAct 反应式的「局部优化陷阱」，
  让 agent 在复杂多工具工作流中全局协调、识别并行、追踪依赖。当用户/agent 需要「串起多个脚本/命令」「编排流水线」「重跑失败步骤」时调用。
agent_created: true
visibility: "public"
---

# 多步工具链编排引擎（toolchain-orchestrator）

让 agent 从「逐个手工跑命令」升级为「声明一条流水线、自动按依赖执行」。核心：把多工具任务建模为**依赖 DAG**，
用确定性的图执行模型（节点=工具，边=数据流）跑通整条链路，且可校验、可重放、可中断续跑。

## 能力依据（主流研究/框架）
- **Beyond ReAct (2025)**：以规划器为中心生成 DAG 执行计划（节点=工具，边=依赖），克服反应式「局部优化陷阱」，
  支持全局优化、并行识别、依赖追踪；在 StableToolBench 达 SOTA。
- **Strands GraphBuilder / Shannon**：图执行模型（节点=agent/tool，边=数据流），确定性、可观测、可重放。
- **ReAct / Plan-and-Execute**：Thought→Action→Observation 交织；或 规划-执行-重规划 闭环。
- 企业实践：显式工作流、链路追踪(observability)、失败恢复、中断重跑。

## 链定义（chain.json）
```json
{
  "name": "etl-demo",
  "nodes": {
    "extract":   {"run": "python extract.py data.csv", "depends_on": [], "capture": "stdout"},
    "transform": {"run": "python transform.py",        "depends_on": ["extract"], "capture": "stdout"},
    "load":      {"run": "echo done: {{transform}}",   "depends_on": ["transform"], "capture": "stdout"}
  }
}
```

## 标准工作流
```bash
# 1. 校验（依赖存在/成环/命令可达）
python scripts/orchestrator.py validate chain.json
# 2. 先看执行计划（拓扑序）
python scripts/orchestrator.py run chain.json --dry-run
# 3. 真正执行（上游 stdout 通过 {{node_id}} 透传；日志在 outputs/run_log.json）
python scripts/orchestrator.py run chain.json --out outputs
# 4. 某步失败后，修复该节点脚本，从它续跑
python scripts/orchestrator.py run chain.json --from transform --out outputs
# 5. 导出可视化
python scripts/orchestrator.py dot chain.json --out chain.dot
```
> 注：也支持 `.yaml` 链（优先用 PyYAML，缺失时回退极简子集解析）；命令默认走 shell，
> 仅执行**用户自己定义的链**，不用于运行不可信输入。

## 设计要点
- **规划-执行分离**：先声明 DAG，再执行，结构可视、可审计、易调试。
- **依赖透传**：`{{node_id}}` 把上游 stdout 注入下游命令，形成真实数据流。
- **断点续跑**：`--from <node>` 修复失败步骤后无需从零重来。
- **可观测**：每步返回码 + `run_log.json` 全链路记录，便于复盘。

## 质量门禁
- [ ] 链是否先过 `validate`（无环、依赖/命令存在）
- [ ] 节点间数据是否通过 `{{node_id}}` 正确透传（而非靠全局副作用）
- [ ] 失败节点是否有 `run_log.json` 记录，便于 `--from` 续跑
- [ ] 是否导出了 DOT 图供人工审阅依赖结构

## 自进化学习系统（越用越好用、越用越高效）

本技能内置通用学习模块 `scripts/learner.py`。每次使用后自动复盘、积累经验，逐步提升输出质量与执行效率，无需人工维护。

### 记忆文件
`learned_patterns.json`（位于本技能目录）记录：操作总数、各能力使用频次、错误模式、用户偏好、改进建议。

### 使用后请调用（Bash）
```bash
python scripts/learner.py record <本技能目录> --capability 工具链编排
python scripts/learner.py record <本技能目录> --capability 工具链编排 --fail --error 依赖成环 --note "chain.json 出现环"
python scripts/learner.py insight <本技能目录>
python scripts/learner.py reflect <本技能目录>
```

### 迭代规则
- **错误累计 ≥3 次** → 主动增加预检/兜底步骤，并将经验回写本 SKILL.md。
- **操作数 ≥10 次** → 分析高频能力优先打磨示例与质量，低频能力评估精简或合并。
- **重要用户偏好** → 写入 `learned_patterns.json`，下次调用直接采用，减少重复询问。

> 越用越懂你：第一次用是通用能力，第十次用已沉淀为你专属的最佳实践。
