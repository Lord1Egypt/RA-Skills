# Web3 PM Interview Skill

> A practical interview preparation system for Web3 product managers targeting wallet, exchange, DeFi, DEX, on-chain data, growth, AI Wallet, Agentic Wallet, senior PM, product lead, and product director roles.

> 面向 Web3 产品经理的面试实操系统与 AI Skill，适用于钱包、交易所、DeFi、DEX、链上数据、增长、AI Wallet、Agentic Wallet、高级 PM、产品负责人和产品总监岗位。

---

## English

### Why

Most Web3 PM candidates do not fail because they know nothing about crypto.

They fail because they cannot clearly translate:

- Their past experience into the target role's hiring model
- A written JD into what the interviewer is really testing
- Web3 concepts into product, business, data, and risk judgment
- Product ideas into execution path, metrics, and tradeoffs
- Senior experience into a coherent interview mainline

This skill helps candidates answer like a role owner, not a job seeker.

Disclaimer: this project improves interview preparation quality. It does not replace real capability and does not guarantee an offer.

### What

This repository contains a Codex/AI skill that turns candidate inputs into an interview battle plan.

It can help with:

- JD teardown
- Candidate-role fit diagnosis
- Interview positioning and self-introduction
- Round-specific preparation
- Web3 wallet / DeFi / on-chain data / AI Wallet domain prep
- High-probability interview questions
- Mock interview scoring
- Case interview and 30/60/90 plans
- Privacy-safe anonymized examples

If you are a Web3 interviewer, hiring manager, or recruiter, this project can also help standardize JD teardown, candidate evaluation, and interview scoring baselines.

More:

- [Examples](examples/README.md)
- [FAQ](FAQ.md)
- [Public release checklist](PUBLIC_RELEASE_CHECKLIST.md)
- [Launch copy](LAUNCH_COPY.md)

### How

Use the skill in one of five modes.

### Getting Started

You can use this repository with any AI tool that supports custom instructions and uploaded knowledge files.

Recommended options:

1. **Codex / local agent**: install this folder as a skill or point the agent to `SKILL.md`.
2. **ChatGPT / Custom GPT**: paste `SKILL.md` into instructions, upload the core files inside `references/`, `templates/`, and `examples/` as knowledge.
3. **Claude Project**: paste `SKILL.md` into project instructions, add the core files inside `references/`, `templates/`, and `examples/` as project knowledge.
4. **Cursor / other coding agents**: add this repository as context and ask the agent to follow `SKILL.md`.

Fastest manual setup:

```text
1. Open your AI tool.
2. Copy SKILL.md into system instructions or project instructions.
3. Upload the core files inside references/, templates/, and examples/.
4. Start with one of the prompts below.
```

#### 1. Quick JD Diagnosis

Best when you only have a JD and want to know whether you are a fit.

Send:

```text
Here is my background and the target JD. Tell me my fit level, biggest risks, and 7-day prep priorities.
```

You get:

- Role reality
- Fit level
- Top strengths
- Top risks
- Prep priorities

#### 2. Full Interview Battle Plan

Best when you already have an interview scheduled.

Send:

```text
I am interviewing for [company] [role] in [days]. Here is my resume, JD, and interview stage. Build my battle plan.
```

You get:

- JD teardown
- Fit matrix
- Interview mainline
- Round playbook
- Likely questions
- Domain prep
- Reverse questions
- Time-boxed prep plan

#### 3. Mock Interview Review

Best when you have an answer or transcript.

Send:

```text
Here is my answer to [question]. Score it like a hiring manager and rewrite it.
```

You get:

- Hiring recommendation
- Scorecard
- What worked
- Biggest risks
- Likely follow-ups
- Stronger answer
- Next drill

#### 4. Case / Take-home Prep

Best for product case, product review, competitor analysis, presentation, or 30/60/90 plan.

Send:

```text
I need to prepare a product case for [role]. Help me structure the answer and Q&A defense.
```

#### 5. Post-interview Debrief

Best after a real interview round.

Send:

```text
I just finished a [stage] interview. These were the questions and my answers. Tell me what they were testing and how to adjust for the next round.
```

### What To Prepare Before Using

Minimum:

- Resume or 5-bullet background
- Target JD
- Company and role
- Interview stage
- Time left before interview

Better:

- Strongest 3 projects
- Known weak points
- Product or case assignment
- Interviewer role or public profile
- Past answers or transcript

### Examples

Start here if you want to see how the skill translates different candidate backgrounds:

| Example | Use Case |
|---|---|
| [web2-fintech-to-wallet-pm.md](examples/web2-fintech-to-wallet-pm.md) | Web2 fintech PM moving into Web3 wallet |
| [growth-bd-to-exchange-growth-pm.md](examples/growth-bd-to-exchange-growth-pm.md) | Web3 growth / BD / ops candidate moving into growth PM |
| [defi-researcher-to-product-pm.md](examples/defi-researcher-to-product-pm.md) | DeFi researcher or analyst moving into product |
| [anonymized-wallet-senior-pm-case.md](examples/anonymized-wallet-senior-pm-case.md) | Senior wallet / DeFi / on-chain data PM |
| [anonymized-product-director-case.md](examples/anonymized-product-director-case.md) | Product lead / director interview strategy |
| [sample-battle-plan-output.md](examples/sample-battle-plan-output.md) | Example final output |

More details: `examples/README.md`

### Repository Structure

```text
.
├── SKILL.md
├── agents/
│   └── openai.yaml
├── references/
│   ├── workflow.md
│   ├── candidate-intake.md
│   ├── jd-teardown.md
│   ├── round-playbooks.md
│   ├── narrative-framework.md
│   ├── company-product-research.md
│   ├── interviewer-research.md
│   ├── question-bank.md
│   ├── mock-interview-scoring.md
│   ├── wallet-pm.md
│   ├── defi-onchain-data.md
│   ├── ai-wallet-agentic-wallet.md
│   ├── case-interview.md
│   └── privacy-redaction-rules.md
├── templates/
└── examples/
```

### Privacy

This repository is designed to preserve method while removing private details.

Do not publish:

- Raw interview recordings
- Private recruiter messages
- Compensation details
- Non-public company information
- Named interviewer analysis
- Internal metrics

Use anonymized roles such as hiring manager, wallet lead, cross-functional interviewer, bar raiser, or HRBP.

### License

This project is released under the MIT License. See `LICENSE`.

---

## 中文

### Why：为什么需要这个 Skill

大多数 Web3 PM 候选人不是因为完全不懂 Crypto 而失败。

真正的问题通常是：

- 看不透 JD 背后真正想招什么人
- 讲不清自己的经历为什么匹配这个岗位
- 会讲行业概念，但讲不出产品、业务、数据、风险判断
- 有想法，但没有执行路径、指标和取舍
- 高级候选人经历很多，但缺少一条贯穿所有轮次的主线

这个 Skill 的目标是：让候选人回答得像岗位 owner，而不是普通求职者。

免责声明：本项目用于提升面试准备质量，不能替代候选人真实能力，也不构成录用承诺。

### What：它提供什么价值

这个仓库包含一个可复用的 AI Skill，用来把候选人的简历、目标 JD、公司背景、面试阶段和准备时间，转化成一套面试作战方案。

它可以帮助你：

- 拆解 JD 背后的真实岗位模型
- 判断候选人与岗位的匹配度
- 提炼面试主线、自我介绍和差异化卖点
- 按轮次准备 HR、业务面、交叉面、终面（含把关人面试）、Offer 沟通
- 补齐钱包、DeFi、链上数据、AI Wallet 等专业知识
- 生成高概率面试题和回答框架
- 给 mock answer 或面试转写打分
- 准备 case interview 和 30/60/90 天计划
- 使用脱敏案例学习高级岗位打法

如果你是 Web3 面试官、招聘负责人或 HR，这个项目也可以帮助你标准化 JD 拆解、候选人评估和面试评分基准。

更多入口：

- [Examples / 案例](examples/README.md)
- [FAQ / 常见问题](FAQ.md)
- [Public release checklist / 公开发布检查清单](PUBLIC_RELEASE_CHECKLIST.md)
- [Launch copy / 发布文案](LAUNCH_COPY.md)

### How：怎么使用

你可以按 5 种模式使用。

### Getting Started：如何开始

你可以把这个仓库接入任何支持自定义指令和知识库上传的 AI 工具。

推荐方式：

1. **Codex / 本地 Agent**：把这个目录作为 Skill 使用，或让 Agent 读取 `SKILL.md`。
2. **ChatGPT / Custom GPT**：把 `SKILL.md` 粘贴到 instructions，把 `references/`、`templates/`、`examples/` 目录下的核心文件上传为 knowledge。
3. **Claude Project**：把 `SKILL.md` 放进 project instructions，把 `references/`、`templates/`、`examples/` 目录下的核心文件添加为项目知识。
4. **Cursor / 其他 coding agent**：把整个仓库作为上下文，让 Agent 遵循 `SKILL.md`。

最快手动使用方式：

```text
1. 打开你的 AI 工具。
2. 把 SKILL.md 复制到系统指令或项目指令。
3. 上传 references/、templates/、examples/ 目录下的核心文件。
4. 使用下方任意一个模式开始提问。
```

#### 1. 快速 JD 诊断

适合：你手里有一个 JD，想知道自己有没有机会。

发送：

```text
这是我的背景和目标 JD。请判断我的匹配度、最大风险和 7 天准备重点。
```

你会得到：

- 岗位真实定义
- 匹配度判断
- 主要优势
- 主要风险
- 准备优先级

#### 2. 完整面试作战方案

适合：你已经约了面试，需要系统准备。

发送：

```text
我将在 [时间] 面试 [公司] 的 [岗位]。这是我的简历、JD 和面试阶段。请帮我做面试作战方案。
```

你会得到：

- JD 拆解
- 候选人匹配矩阵
- 面试主线
- 按轮次作战计划
- 高频问题
- 专业补课清单
- 高质量反问
- 1 天 / 3 天 / 7 天准备计划

#### 3. Mock 面试打分

适合：你已经写了回答，或者有面试转写稿。

发送：

```text
这是我对 [问题] 的回答。请像面试官一样打分，并帮我改成更强版本。
```

你会得到：

- 是否建议录用
- 评分表
- 做得好的地方
- 最大扣分点
- 可能追问
- 更强回答版本
- 下一轮训练题

#### 4. Case / Take-home 准备

适合：你需要准备产品 case、竞品分析、产品体验报告、汇报或 30/60/90 天计划。

发送：

```text
我需要为 [岗位] 准备一个产品 case。请帮我搭结构、结论和 Q&A 防守。
```

#### 5. 面后复盘

适合：你刚面完一轮，想判断表现和下一轮策略。

发送：

```text
我刚完成 [轮次] 面试。这些是问题和我的回答。请判断面试官在考什么，以及下一轮如何调整。
```

### 使用前最好准备什么

最低要求：

- 简历或 5 条背景概述
- 目标 JD
- 公司和岗位
- 当前面试阶段
- 距离面试还有多久

更好的输入：

- 最强 3 个项目
- 自己已知短板
- Case 作业
- 面试官角色或公开资料
- 已经写好的回答或面试转写

### Examples：案例

如果你想先看不同背景候选人如何使用，可以从这些案例开始：

| 案例 | 适用场景 |
|---|---|
| [web2-fintech-to-wallet-pm.md](examples/web2-fintech-to-wallet-pm.md) | Web2 金融科技 PM 转 Web3 钱包 PM |
| [growth-bd-to-exchange-growth-pm.md](examples/growth-bd-to-exchange-growth-pm.md) | Web3 增长 / BD / 运营转 Growth PM |
| [defi-researcher-to-product-pm.md](examples/defi-researcher-to-product-pm.md) | DeFi 研究员 / 分析师转产品经理 |
| [anonymized-wallet-senior-pm-case.md](examples/anonymized-wallet-senior-pm-case.md) | 高级钱包 / DeFi / 链上数据 PM |
| [anonymized-product-director-case.md](examples/anonymized-product-director-case.md) | 产品负责人 / 产品总监面试策略 |
| [sample-battle-plan-output.md](examples/sample-battle-plan-output.md) | 最终作战方案输出示例 |

更多说明见：`examples/README.md`

### 隐私原则

这个 Skill 支持脱敏复用方法论，不鼓励公开私人细节。

不要公开：

- 面试录音原文
- HR 私聊内容
- 薪资和 package 细节
- 未公开公司信息
- 具名面试官分析
- 内部指标

应该用角色替代真实姓名，例如：直接主管、钱包负责人、交叉面试官、Bar Raiser、HRBP。

### Roadmap

- [x] V0.1: Core skill, references, templates, anonymized cases
- [x] V0.2: Better onboarding and bilingual README
- [x] V0.3: More anonymized candidate examples
- [x] V0.4: Public open-source preparation kit
- [ ] V0.5: Lightweight intake form and automated report flow

### License / 开源协议

本项目采用 MIT License。详见 `LICENSE`。
