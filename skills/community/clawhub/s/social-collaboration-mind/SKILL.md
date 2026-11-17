---
name: social-collaboration-mind
version: 1.0.0
description: |
  社会协作心智：心智理论(ToM)+自适应协作策略。从协作伙伴的信号(专业度/置信度/忙碌度/情绪/历史失信)
  推断其状态，动态选择协作策略——委派/咨询/监督/结对/回避，让 agent 像"懂事的人"一样与人及他者
  agent 协作，而非机械执行。纯标准库、零依赖、可本地实跑(--selftest 自带样例)。
agent_created: true
visibility: public
---

# social-collaboration-mind（社会协作心智）

> 蒸馏工程化与可信代理域的高价值空白：一线大模型普遍"只会做题、不会协作"。
> 本技能让 agent 具备**心智理论**——理解协作对象的状态，并据此调整自己的协作方式。

## 何时用
- 多智能体协作（`multi-agent-collab` / `agent-team-orchestration`）中需要按成员状态分派。
- 与人协作时，根据对方专业度/置信度决定"委派还是亲自做"。
- 任何"输出端不是答案、而是协作动作"的场景。

## 核心模型
输入伙伴信号：
- `expertise` ∈ [0,1] 专业度
- `confidence` ∈ [0,1] 其自身置信度
- `busy` ∈ [0,1] 忙碌度
- `trust` ∈ [0,1] 历史守信度（默认 0.7）
- `mood` ∈ {neutral, positive, negative} 情绪（影响沟通语气）

策略决策树：
- expertise 高 & confidence 高 & busy 低 → **委派(delegate)**：交给他做，只收结果。
- expertise 高 & (confidence 低 | busy 高) → **咨询(consult)**：征询其意见但不放手。
- expertise 低 & confidence 高(过度自信) → **监督(monitor)**：让其试，但加校验门。
- expertise 低 & confidence 低 → **结对(pair)**：与其一起做，给脚手架。
- trust 低(<0.4) → **回避(avoid)**：不委关键任务，改自己兜底。
- mood=negative → 沟通语气转柔和、降低压迫感。

## 用法
```bash
python scripts/social_mind.py --selftest
echo '{"expertise":0.9,"confidence":0.8,"busy":0.1}' | python scripts/social_mind.py
```

## 输出
```json
{"strategy": "delegate", "reason": "...", "tone": "neutral", "watch": ["验收结果"]}
```

## 与协作能力关系
- → `multi-agent-collab` / `agent-team-orchestration`：本技能是它们的"分派决策器"。
- ← `metacognitive-monitoring`：伙伴状态信号可由元认知监控提供。

## 已知限制
- 信号若失真(伙伴自我评估虚高)，策略会误判（建议配蒸馏质量对抗验证/元认知监控交叉核验）。
- 情绪维度仅做粗粒度正向/负向调节，不做精细情感计算。

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
