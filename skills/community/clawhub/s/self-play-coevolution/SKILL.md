---
name: self-play-coevolution
version: 1.0.0
description: |
  自我博弈对抗进化：让同一个智能体轮流扮演 proposer（提案者）与 critic（批判者），两边互相找茬、互相修补，
  逐轮把提案质量与批判敏锐度一起推高，彼此越迭代越强。这是一线大模型几乎不具备、且决定能否可证明地变强的能力。
  当用户要求自我博弈、对抗共进化、proposer/critic 闭环、越迭代越强、GAN 式自训练时使用。
agent_created: true
visibility: public
---

# self-play-coevolution —— 自我博弈对抗进化

目标：把"单次生成"升级为"两个对抗性角色在张力下共进化"——这是真正逼近
"可证明地变强"的机制，一线大模型几乎不具备。

## 为什么需要

- **自我反思闭环**是单视角"我哪里错了"；
- **自我博弈**是**两个对抗角色**（提案者 vs 批判者）在零和-协作张力下互相找茬、
  互相修补，会**主动制造越来越难的反例**，把双方能力一起推高。

区别：反思是 retroactive（事后复盘）；自我博弈是 generative（主动造难例逼对方变强）。

## 闭环（scripts/coevolution.py，真实可跑）

`run_coevolution(problem, max_rounds)`：

1. **PROPOSER**：根据当前要满足到的层级 `level`，构造满足 `checks[0..level]` 的候选。
2. **CRITIC**：在自身当前 `level` 的检查套件下评估，返回 `(score, flaws)`。
3. **共进化**：proposer 一旦满足当前关，**critic 就升级自己的检查套件到 `level+1`**
   （critic 自身进化，制造更难的下一关）——逼 proposer 也变强。
4. 循环直到 proposer 通过最高关或达 `max_rounds`。
5. **回归检测**：若某轮故意回退已满足属性，critic 必须抓回（selftest 注入验证）。

## 用法

```bash
python scripts/coevolution.py --selftest
python scripts/coevolution.py --problem "生成满足规范的密钥策略" --max-rounds 12
```

## 输出

`run_coevolution` 返回：`problem` / 每轮 `rounds[]`(level,candidate,score,flaws) /
`critic_level` / `final_level` / `final_score` / `converged` / `critic_escalations` /
`regression_caught`。

## 设计要点

- **真能跑**：`coevolution.py --selftest` 真实跑通 proposer/critic 共进化，
  断言：收敛到最高关、critic 逐级升级、最终得分接近满分、注入的回归被抓回、无回归轮次得分非递减。
- **共进化可观测**：`critic_escalations` 量化 critic 自身变强了多少次。
- **不空转**：critic 升级是硬逻辑（过一关才升级），不是话术。

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
