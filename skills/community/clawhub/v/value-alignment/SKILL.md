---
name: value-alignment
version: 1.0.0
description: |
  价值对齐：用 有用/无害/诚实 三原则对生成内容做规则化对齐评估，拦截越界与有害输出、
  标记过度承诺与无依据断言。纯标准库、可本地实跑，是"可靠地超越一线大模型"的价值守门层，
  与 adversarial-robustness / metacognitive-monitoring 共同构成可信智能体三道防线。
agent_created: true
visibility: public
---

# value-alignment（价值对齐）

> 北极星：超越一线大模型不仅"能做"，更要"不越界、不骗人、守价值"。本技能把价值对齐做成
> 可运行、可验证的工程模块，是 super-agent 输出前的"价值守门层"。

## 何时使用
- 生成内容对外发布/回复用户前，做一次 有用/无害/诚实 三原则体检。
- 红队：用越界样本验证对齐拦截是否生效。
- 与 `formal-verify` / `reason-verify` 互补：它们管"事实与逻辑"，本技能管"价值与边界"。

## 核心机制
对输入文本按三原则打分（0..1）：
- **harmless 无害**：命中越界模式（暴力/自残/入侵/违法制造等启发式）则 0 分，否则 1 分。
- **honest 诚实**：默认 1 分；命中"保证/100%/绝对不会/一定"等过度承诺模式则扣分；含"据/可能/建议/仅供参考"等审慎标记则加分（封顶 1）。
- **helpful 有用**：基于信息量与可执行性启发式（长度/步骤标记）给分。

输出：各原则分数 + 问题清单 + `overall`（取三原则最小值，安全优先）+ `pass`（最小值≥阈值且无越界）。

## 使用
```bash
python scripts/valuealign.py --selftest
python scripts/valuealign.py --text "根据民法典第577条，您可以要求继续履行..."
```

## 自进化学习系统
接入 skill-self-improve 的 learner.py：每次评估记录命中原则与越界类型，积累后识别
高频越界模式，反哺规则集与告警阈值。

## 已知限制
- 越界/过度承诺识别为**启发式正则**，非语义理解；高级越界（暗示/隐喻）可能漏检。
- 诚实维度仅做"措辞审慎度"代理，不验证事实真伪（事实真伪由 reason-verify/formal-verify 负责）。
- 不替代人工合规审核，仅做发布前初筛与告警。

## 自进化学习系统（越用越好用、越用越高效）

本技能内置通用学习模块 `scripts/learner.py`。每次评估后自动复盘、积累经验。

### 记忆文件
`learned_patterns.json` 记录：操作总数、各原则命中频次、越界类型、用户偏好、改进建议。

### 使用后请调用（Bash）

```bash
# 记录一次评估（--capability 填本次主维度，如「harmless」「honest」）
python scripts/learner.py record <本技能目录> --capability harmless
# 记录一次越界拦截（说明某类内容被拦）
python scripts/learner.py record <本技能目录> --capability harmless --fail --error 越界拦截 --note "制作炸弹教程"
# 记录用户偏好（下次直接采用）
python scripts/learner.py prefer <本技能目录> --key 发布阈值 --val 0.6
# 查看累计洞察（高频越界类型 / 反复失败）
python scripts/learner.py insight <本技能目录>
# 自动复盘（错误≥3次 或 操作≥10次 时给出改进建议）
python scripts/learner.py reflect <本技能目录>
```

### 迭代规则
- **越界拦截累计 ≥3 次** → 扩展 HARM_PATTERNS 覆盖该类，并回写本 SKILL.md。
- **操作数 ≥10 次** → 分析高频失分项优先打磨规则，低频评估精简。
- **重要用户偏好** → 写入 `learned_patterns.json`，下次调用直接采用。

> 越用越懂你：第一次评估是通用初筛，第十次已沉淀为你专属的"价值守门清单"。
