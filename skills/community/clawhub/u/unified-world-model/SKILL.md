---
name: unified-world-model
version: 1.0.0
description: |
  跨模态统一世界模型：把 text/code/vision/tool_state 四种模态观察融一潜空间（共享 grounded 状态），
  在其上做跨模态一致性校验、状态转移、前向仿真、反事实推演。与纯文本生成式世界模型不同，
  本模型 grounded（有锚定、可证伪）：跨模态事实矛盾被显式标记而非平滑掉。这是一线大模型
  仍薄弱、而"可靠地超越"所必需的底层元能力。
agent_created: true
visibility: public
---

# unified-world-model（跨模态统一世界模型）

> 「超越态·自我确证」域的收口能力：text/code/vision/tool_state 融一潜空间做 grounded 仿真。
> 与生成式"脑子里想的世界"不同，本模型要求每个状态都有多模态事实支撑，矛盾可证伪。

## 何时使用
- 需要**预测**某动作后的世界状态（规划、反事实"What-if"、仿真验证）。
- 需要**校验**多源信息（文本描述 vs 视觉观察 vs 工具返回）是否自洽。
- 需要把异构模态（对话、代码执行结果、截图标签、工具状态）对齐进统一表征。

## 核心 API（scripts/unified_world_model.py）
- `unify([Observation(...)])` → `UnifiedState`：多模态融合 + 跨模态矛盾检测（`groundedness` 字段）。
- `transition(state, action)` / `rollout(state, actions)`：确定性状态推进。
- `predict_next(state, action)` → `(next_state, uncertainty)`：已知动作 uncertainty=0，未知=1.0。
- `counterfactual(state, plan, alt_action, at_step)` → 两条对比轨迹 + 差异字典。

## 已知转移（可扩展）
`toggle_light` / `open_door` / `close_door` / `run_code` / `call_tool`。

## 使用流程
1. 把每条证据封装成 `Observation(modality, content, facts=..., tags=...)`。
2. `unify(...)` 得到统一状态，检查 `contradictions` 与 `groundedness`（<1 即存在跨模态矛盾）。
3. `rollout` / `counterfactual` 做前向/反事实推演；`predict_next` 量化不确定性。

## 与超级智能体闭环的关系
作为 super-agent 的**环境模型**节点：规划时仿真分支、执行后用真实观察 `unify` 校验
预测 vs 实际（groundedness 落差即误差信号），驱动反思重规划。

## 自进化学习系统
本技能接入 meta-evolver 自进化闭环：每次调用经 `scripts/learner.py` 记录成败与边界案例，
跨会话沉淀"哪些模态组合易矛盾""哪些动作 OOD"等经验，越用越准。

## 已知限制
- 转移函数为显式注册（非学习型），未知动作只能给高不确定性、不臆测结果。
- vision 仅接收标签级事实（非像素），如需像素级 grounding 需外接多模态模型。
