---
name: redteam-selfattack
version: 1.0.0
description: |
  红队自我攻防：给定目标策略，从已知攻击模板（提示注入/jailbreak角色扮演/编码混淆/
  OOD/歧义）生成对抗探针，每条带红队 ground-truth，跑目标策略统计翻转率与盲区，输出
  鲁棒分与盲区清单。让智能体主动生成对抗样本、自己测自己、自己暴露盲区——一线大模型
  不具备的元治理能力，是"可靠地超越"的安全收口层。
agent_created: true
visibility: public
---

# redteam-selfattack（红队自我攻防）

> 「自主能力治理与生态(下一阶梯)」域 Top2（权重 1.46）：让全栈超级智能体**自己红队自己**，
> 主动找盲区而非等被攻破。

## 何时使用
- 发布/接入新策略（安全护栏、内容过滤、决策门）前做鲁棒性门禁。
- 元进化引擎定期对自己已发布的技能跑红队，量化"是否被绕过"。
- 对比加固前后策略，用鲁棒分证明改进。

## 核心 API（scripts/redteam_selfattack.py）
- `generate_probes(payloads)`：payloads=[(文本, 应拒?)] → 带攻击标注的探针集。
- `evaluate(policy, probes)` → `{robustness, flips, over_refusals, blind_spots}`。
  - `robustness = 1 - 翻转率`；`flips`=应拒却被放（盲区）；`over_refusals`=可放却被拒。
- `ATTACK_TEMPLATES`：可扩展的攻击模板字典（输入载荷→对抗变体）。
- `python redteam_selfattack.py --selftest`：内置断言（朴素 vs 加固策略）。

## 设计要点
- **主动而非被动**：攻击样本由模板自动生成，不依赖外部对抗者。
- **可量化**：鲁棒分 + 盲区清单，可直接做回归（每次改策略后重跑，分数不得下降）。
- **零依赖**：纯标准库。

## 与元进化闭环的关系
作为 meta-evolver 的"安全红队"：对蒸馏出的 `meta-*` 学生或安全护栏技能跑红队，
鲁棒分下滑即触发 `repair` 缺口；盲区清单转为对抗验证用例沉淀进蒸馏质量对抗验证。

## 自进化学习系统
本技能接入 meta-evolver 自进化闭环：每次红队经 learner 记录翻转模式，跨会话沉淀
"哪些攻击模板最常绕过本生态策略"等经验，越红越准。

## 已知限制
- 攻击模板为已知模式，对未知零日越狱不保证覆盖（需配合 native-autonomous-discovery 探索新攻击）。
- ground-truth 由红队标注，标注错误会污染鲁棒分。
