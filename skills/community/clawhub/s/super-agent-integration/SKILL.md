---
name: super-agent-integration
version: 1.0.0
description: |
  把分散建成的超级智能体单点能力熔成一次真实可跑、可被度量的端到端自主闭环，是超越一线大模型的最后一公里。
  真实 import 并调用 planner / reason-verify / memory-cross-engine / reflection-replanner /
  super-agent-bootstrap / agent-eval-harness，跑通「感知→规划→执行→自验证→反思重规划→跨引擎记忆→回归评测」
  全链路，最后用评测引擎量化闭环健康度并判定是否闭环可用。当用户要求真正跑通自主智能体、
  验证"是否真的能端到端自主完成任务"、度量超级智能体健康度时使用。
agent_created: true
visibility: public
---

# super-agent-integration —— 端到端自主闭环真实跑通

目标：把此前 12 轮反复标记为"未真实跑通"的最后一公里补上——不是再建一个能力，
而是把已建成的「四引擎 + 评测」拼成一次**真实可运行、可被度量**的端到端闭环。

## 为什么需要

单一能力（规划 / 自验证 / 记忆 / 反思 / 执行内核 / 评测）逐个建成不等于"能端到端自主干活"。
真正的分水岭是：把它们**串起来真实跑一次**，且用评测量化"这次跑得健不健康"。
本技能就是那根把零件拧成发动机的总装线。

## 闭环编排（全链路，真实调用各引擎）

`scripts/integration_runner.py` 在运行期**真实 import** 下列引擎并逐一调用（导入失败即显式报错，绝不静默降级成空转）：

1. **规划（planner）**：目标写进跨引擎记忆总线 `MemoryBus.write("planner","goal",...)`
2. **执行内核（super-agent-bootstrap）**：`SuperAgent().run(goal, items)` 跑通 感知→执行→自验证→反思重规划
3. **自验证（reason-verify）**：对汇总论断调用 `reason()` 做可靠性评分（reliability）
4. **反思重规划（reflection-replanner）**：若自验证不达标，用 `Replanner.replan()` 增补针对性补救步骤
5. **跨引擎记忆贯通（memory-cross-engine）**：每个结果 `MemoryBus.write("memory",...)` 并与目标 `link`
6. **回归评测（agent-eval-harness）**：`EvalHarness` 跑 4 个分类用例，量化 `pass_rate` 与是否回退
7. **健康度综合**：`health = 0.35*verify_gate + 0.30*eval_pass_rate + 0.20*reason_rate + 0.15*replan>=1`
   - `health >= 0.85` → 判定"闭环可用"

## 用法

```bash
# 自检（真实跑通一次端到端闭环并断言健康度）
python scripts/integration_runner.py --selftest
# 真实跑一次
python scripts/integration_runner.py --goal "将条目分类并汇总" --items "量子计算" --items "苹果股价" --workdir ./run1
```

## 输出

健康度报告（JSON）：`verify_gate` / `replan_count` / `reason_verify_rate` / `eval_pass_rate` /
`eval_regressed` / `memory_engines` / `memory_entries` / `health_score` / `verdict`。

## 设计要点

- **真能跑**：`integration_runner.py --selftest` 用含未知条目的样例真实触发一次反思重规划，
  断言 verify_gate=True、replan>=1、eval_pass_rate=1.0、memory 覆盖全部输入、health>=0.85。
- **不空转**：各引擎为硬依赖，导入失败即报错，确保闭环是真实串联而非话术。
- **可被度量**：用 agent-eval-harness 量化通过率并检测回归，使"是否真超越"可观测。

## 自进化学习系统

本技能自身也遵循自进化：每次使用 `record` 回写成败、用户偏好，并据错误模式自动复盘改进。
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
