---
name: super-agent
version: 1.0.0
description: |
  超级智能体闭环（整合与进阶·元能力之巅）。把已建成的超越性能力——
  长程自主规划(long-horizon-planner) · 自我反思闭环(self-reflection-loop) ·
  多步工具链编排(toolchain-orchestrator) · 可靠推理与自验证(reason-verify) ·
  持续学习记忆(continual-memory-engine) · 主动目标设定(proactive-goal-setter) ·
  代码生成自验证(code-self-verifier) · 检索增强生成(rag) · 工具调用(tool-use) ——
  熔成一条「感知→规划→执行→自验证→反思→记忆→再规划」的连续自进化 agent 闭环。
  当希望让 agent 以接近(乃至超越)一线大模型智能体的方式，自主把一个高远目标
  持续推进到底、且越跑越强时使用。
agent_created: true
visibility: public
---
# super-agent —— 超级智能体闭环

把分散的「超越性」元能力熔成**一条可持续运转、且自我增强的 agent 主循环**。
这是从「强模型」迈向「超级 agent」的关键整合跃迁：单点能力再强，不串成闭环也
只是工具；闭环一旦成型，agent 就能自主把遥远目标拆成可续做的路线、边做边验证、
做完即反思、反思即记忆、记忆即下一轮更聪明的规划。

## 闭环六阶段（loop.py 真实编排）

| 阶段 | 调用能力 | 作用 |
|------|----------|------|
| ① 感知 Sense | meta-evolver skill-self-improve | 刷新全局能力图、读取记忆与当前状态 |
| ② 规划 Plan | long-horizon-planner + proactive-goal-setter | 生成长程路线图、选定本轮最该推进的目标 |
| ③ 执行 Execute | toolchain-orchestrator + tool-use + rag | 编排工具链、调用工具、检索外部知识 |
| ④ 自验证 Verify | reason-verify + code-self-verifier + self-eval | 命题矛盾检测、事实锚定、代码自测、rubric 自评 |
| ⑤ 反思 Reflect | self-reflection-loop | 对照目标评估、定位偏差、产出改进意图 |
| ⑥ 记忆 Memorize | continual-memory-engine | 把经验/偏好/失败模式固化，跨会话越用越强 |

闭环可断点续跑（状态落盘），天然具备 long-horizon 属性。

## 使用

```bash
# 启动一次完整闭环推进（自动调用既有超越性技能脚本）
python super-agent/scripts/loop.py \
  --goal "把我的技能生态做成可售卖的 ClawHub 店铺并持续获客" \
  --max-steps 6 --out run_report.json --state state.json

# 仅生成路线图（委托 long-horizon-planner）
python super-agent/scripts/loop.py --goal "..." --plan-only
```

## 集成契约

- `loop.py` 通过**真实子进程调用**既有技能脚本：`long-horizon-planner/scripts/planner.py`
  （路线图）、`reason-verify/scripts/verify.py`（自验证）。找不到时优雅降级为内置逻辑，
  保证闭环在任何环境下都能跑通。
- 每个阶段产出结构化事件，最终聚合成 `run_report.json`：含各阶段状态、发现的偏差、
  下一步动作、置信度——可直接喂给下一轮，构成持续自进化轨迹。

## 自我进化

本技能自带 `learner.py` 自进化闭环（由 `skill-self-improve` 注入）。每次运行后，
把「哪类目标最难推进 / 哪个阶段最易失败 / 哪些能力组合最有效」记入 `learned_patterns.json`，
下一次自动调优编排策略。
