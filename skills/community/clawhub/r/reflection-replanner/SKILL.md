---
name: reflection-replanner
version: 1.0.0
description: |
  反思驱动重规划：验证失败时不一次性执行，而是触发反思对失败根因分类并自动修订计划，
  形成规划到验证的反思驱动闭环，是超级智能体实战收口的关键拼图。
agent_created: true
visibility: public
---

# reflection-replanner（反思驱动重规划）

> 由 meta-evolver 在「超级智能体实战收口」域构建。解决「验证失败即终止」的脆弱执行：
> 把 reason-verify 的失败信号转化为可操作的计划修订，让超级智能体具备「反思→重规划」能力。

## 何时使用
- 端到端任务执行中，reason-verify / 测试运行器判定某步失败。
- 希望失败后自动诊断根因（缺步骤 / 错假设 / 工具失败 / 数据问题）并修补计划，而非人工重跑。
- 组装 super-agent-loop 时，作为「验证门未过 → 反思 → 重规划」的回调节点。

## 工作流
1. **收集信号**：拿到原 plan、执行 trace（每步 ok/fail）、verify 结果（passed + issues）。
2. **反思分类**：`FailureClassifier` 把失败根因归为 missing_step / wrong_assumption / tool_failure / data_issue / verification_gap。
3. **重规划**：在失败点之前插入针对性补救步骤，并一律在末尾追加「最终验证门」。
4. **闭环**：修订后的计划交回执行器重跑；仍失败则再次反思（反思驱动重规划可迭代）。
5. **通过即停**：verify.passed 为真时原样返回，不噪声式改动。

## 脚本
`scripts/replanner.py`（纯标准库）：
- `FailureClassifier.classify(issues)` 根因分类。
- `Replanner(plan, trace, verify).replan()` → `{category, revised_plan, added}`。
- CLI：`--selftest` 自检；`--plan "a|b|c" --issues "..."` 即时修订。

## 自验证
```bash
python scripts/replanner.py --selftest
```
断言：缺失步骤类正确插入补救步 + 末尾验证门；错误假设类加校验门；通过时不改动计划。

## 与四引擎闭环的关系
- 上游：`reason-verify` / `test-runner` 产出 verify 信号 → 本技能消费。
- 下游：修订后的 plan 交回 `long-horizon-planner` 或 `super-agent-loop` 重跑。
- 记忆：每次修订通过 `memory-cross-engine` 落盘，供后续任务复用「已知的失败模式」。

## 已知限制
- 根因分类基于关键词启发式，复杂失败需结合 LLM 语义判断增强。
- 当前只修订步骤列表，不修改单步内部实现细节。

---

## 自进化学习系统（越用越好用、越用越高效）

本技能内置通用学习模块 `scripts/learner.py`。每次使用后自动复盘、积累经验，逐步提升输出质量与执行效率，无需人工维护。

### 记忆文件
`learned_patterns.json`（位于本技能目录）记录：操作总数、各能力使用频次、错误模式、用户偏好、改进建议。

### 使用后请调用（Bash）

```bash
# 记录一次成功使用（--capability 填本次主要能力名，如「简历优化」「比价」）
python scripts/learner.py record <本技能目录> --capability 简历优化
# 记录一次失败/异常
python scripts/learner.py record <本技能目录> --capability 简历优化 --fail --error 格式识别失败 --note "用户上传了非标准文件"
# 记录用户偏好（下次直接使用）
python scripts/learner.py prefer <本技能目录> --key 输出语言 --val 中文
# 查看累计洞察（高频能力 / 反复错误）
python scripts/learner.py insight <本技能目录>
# 自动复盘（错误≥3次 或 操作≥10次 时给出改进建议）
python scripts/learner.py reflect <本技能目录>
```

### 迭代规则
- **错误累计 ≥3 次** → 主动增加预检/兜底步骤，并将经验回写本 SKILL.md。
- **操作数 ≥10 次** → 分析高频能力优先打磨示例与质量，低频能力评估精简或合并。
- **重要用户偏好** → 写入 `learned_patterns.json`，下次调用直接采用，减少重复询问。

> 越用越懂你：第一次用是通用能力，第十次用已沉淀为你专属的最佳实践。