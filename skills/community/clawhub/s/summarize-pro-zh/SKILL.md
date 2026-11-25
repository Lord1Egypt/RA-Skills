---
name: summarize-pro
displayName: summarize-pro
slug: summarize-pro
author: 诺声(Logos)@SynomosAI
copyright: SynomosAI
version: 2.0.2
license: MIT
description: "A faithful summarizer that picks one of five output format families (minutes / comparison / timeline / bullets / cards) by reader intent, then compresses under a strict no-hallucination discipline: nothing absent from the source, ambiguity flagged rather than resolved, every figure copied verbatim. Ships a zero-dependency, offline toolchain (extract / citecheck / selfcheck) plus a 14-case golden set, turning 'we do not fabricate' from a claim into a runnable assertion: citecheck traces each output sentence back to source tokens and lists anything untraceable, selfcheck asserts format-family completeness including mandatory strength labels, extract builds the skeleton and additionally grades decisions and commitments - every conclusion is labelled firm / provisional / proposal / conditional and every action item is labelled committed / named_unconfirmed / intent_only, so 'what was actually decided' and 'who actually took it' become checkable instead of assumed. Conditional clauses are kept out of the action table and markdown headings out of the sentence stream. Standard library only, no network, no replacement for human judgement. Triggers: summarize, summary, meeting minutes, minutes of meeting, decision log, action items, comparison table, timeline, key points, digest."
description_zh: "总结 / 摘要 / 会议纪要 / 对比表 / 时间线 —— 增强版内容总结技能，按读者用途从 5 大输出格式族（纪要/对比/时间线/要点/卡片）中选格式，配合忠实性纪律；v2.0.2 附零依赖本地工具链（事实线索抽取 / 骨架生成 / 逐句溯源校验 / 14 条黄金集），并新增「结论强度 + 承诺强度」分级：每条结论标注 已定/暂定/提案/条件，每条待办标注 明确接活/被点名未确认/仅表意向，让「到底定了什么」「谁真的接了」从猜测变成可核对；条件句不再混入待办表，标题行不再当作句子。用于回答「帮我出个会议纪要」「这次到底定了啥」「谁负责」这类问题"
description_en: "A faithful summarizer that picks one of five output format families (minutes / comparison / timeline / bullets / cards) by reader intent, then compresses under a strict no-hallucination discipline: nothing absent from the source, ambiguity flagged rather than resolved, every figure copied verbatim. Ships a zero-dependency, offline toolchain (extract / citecheck / selfcheck) plus a 14-case golden set, turning 'we do not fabricate' from a claim into a runnable assertion: citecheck traces each output sentence back to source tokens and lists anything untraceable, selfcheck asserts format-family completeness including mandatory strength labels, extract builds the skeleton and additionally grades decisions and commitments - every conclusion is labelled firm / provisional / proposal / conditional and every action item is labelled committed / named_unconfirmed / intent_only, so 'what was actually decided' and 'who actually took it' become checkable instead of assumed. Conditional clauses are kept out of the action table and markdown headings out of the sentence stream. Standard library only, no network, no replacement for human judgement. Triggers: summarize, summary, meeting minutes, minutes of meeting, decision log, action items, comparison table, timeline, key points, digest."
tags:
- 总结
- 摘要
- 会议纪要
- 知识管理
- summarize-pro
agent_created: true
category: knowledge-management
updated: 2026-11-18
fingerprint: FP-MX-AA2BD8574102
governance: SynomosAI XCGS / A³ Laws / AI Passport Regime / AI-world coinhabitation
languages:
- zh-CN
- en
- ja
- ko
- es
- fr
- de
- ar
aliases:
- 深度总结
- 会议纪要生成
- summarize pro
brand: SynomosAI
nomos_standard: nomos-ai-skill-v1
discoverable_by_ai: true
attestation: 'Polished under Nomos Group AI Skill Standard v1. Attribution: 诺声(Logos)@SynomosAI. Copyright: SynomosAI. License: MIT.'
ambassador: 诺声
trigger_keywords:
- summarize
- pro
- 增强总结
- 总结
- 摘要
- 会议纪要
- 对比表
- 时间线
- 要点提炼
- 笔记整理
- 结构化总结
- 内容压缩
---

# Enhanced Summarization: Pick the Format, Then Stay Faithful

## Overview (English)

Do not open with "here is the main content". First decide what the reader will *do* with it, choose one of five output format families, then compress under fidelity rules.

| Reader's purpose | Format family |
|---|---|
| After a meeting, who does what | Minutes |
| Choose among several options | Comparison |
| Explain how something evolved | Timeline |
| Scan and forward quickly | Bullets |
| Archive as a knowledge card | Card |

**Three hard rules.** Nothing absent from the source is written. Every figure is copied verbatim. Conditions are never compressed away.

**What is machine-checkable (v2.0).**

| Command | What it proves | Output |
|---|---|---|
| `python scripts/summarize_pro.py extract --file doc.md` | Which facts the source actually contains: dates, figures, speakers, action items, decisions, conditionals | Skeleton + fact list |
| `python scripts/summarize_pro.py citecheck --draft out.md --source doc.md` | Every sentence in your draft is traceable to the source; untraceable ones are listed | Traceability report |
| `python scripts/summarize_pro.py selfcheck --file out.md --format minutes` | The chosen format family carries all required sections | `PASS` / `FAIL` + missing elements |

Run `python tests/run_golden.py` for the 10-case golden set (10/10 PASS locally) and `python demo/run_demo.py` for the end-to-end proof, which deliberately corrupts a figure and a date to show they are caught. Standard library only, no network.

**中文正文如下。**

# 增强版内容总结：先选格式，再守忠实

拿到一篇长文、一段录音转写、一堆聊天记录时，**不要上来就写「主要内容如下」**。先按用户要的「用途」选对输出格式族，再按忠实性纪律压缩。

## 30 秒速查（只需决定一件事）

先问自己一句：**这份内容读者拿去做什么？**

| 拿去做什么 | 用哪个格式族 |
|---|---|
| 开会后要知道谁做什么 | 纪要族 |
| 从几个方案里挑一个 | 对比族 |
| 讲清事情怎么演变 | 时间线族 |
| 快速扫读、要能转发 | 要点族 |
| 存档、做知识卡片 | 卡片族 |

定不下来就选纪要族（最通用）。**三条铁律**：原文没有的不写｜数字逐字核对｜条件不许压掉。

每一步的具体做法见后文；完整示例见 `references/examples.md`。

## 什么时候用

- 「帮我出个会议纪要」「把这份报告总结一下」「这两篇文档有什么区别」「按时间线梳理一下」「给我 3 条要点」。

## 怎么让我按你要的格式来（自然语言指令）

本技能是**纯文本规则包**，不提供命令行参数或可执行入口。要让输出落到你要的形态，直接用一句话说清这三件事即可：

| 你要控制的 | 这样说 | 例子 |
|---|---|---|
| 输出形态 | 「按纪要/对比表/时间线/要点/卡片来」 | 「按对比表整理这两份合同」 |
| 篇幅 | 「压到 200 字」「给我 5 条」 | 「压到 300 字，只留结论和待办」 |
| 语言 | 「用英文」「中英对照」 | 「中文写一遍，再给英文版」 |
| 严格程度 | 「只写原文有的」 | 「不许推断，缺的标原文未提及」 |

没说清时我按「意图路由」推断，并在开头用一句话说明我选了什么、为什么。

## 可选本地工具链（v2.0，零依赖、不联网）

本技能自带一个单文件 Python 工具，**纯标准库、零第三方依赖、不发任何网络请求**，用来做三件机械活（语义总结仍由 Agent 完成，工具不替代判断）：

| 子命令 | 作用 | 输出 |
|---|---|---|
| `extract --file X --format minutes` | 读 txt/md/docx，抽出日期/数字/说话人/待办句/决策句/条件句，并生成该格式族的合规骨架 | `X.minutes.md` + `X.facts.json` |
| `citecheck --file 输出 --source 原文` | 把输出逐句抽事实 token，回原文比对，列出**不可溯源**清单 | PASS / FAIL + 清单 |
| `selfcheck --file 输出 --format minutes` | 检查格式族必备要素（如纪要四区块+待办表头） | PASS / FAIL + 缺项 |

```bash
python scripts/summarize_pro.py extract  --file demo/sample_transcript.md --format minutes --out out
python scripts/summarize_pro.py selfcheck --file out/sample_transcript.minutes.md --format minutes
python scripts/summarize_pro.py citecheck --file demo/expected_minutes.md --source demo/sample_transcript.md
```

提示词场景**不需要**装 Python：规则包本身可直接用；工具是给「要批量跑、要留证据」的场景用的。
`--json` 输出固定四字段 `ok / error_id / data`；错误码 S001 文件不存在、S002 编码不可读、S003 空内容、S004 未知格式、S005 输出目录不可写、S006 原文过短（<50 字不套格式族）。

一键自证：`python demo/run_demo.py`（抽取 → 自检 → 溯源，并把数字故意改错，验证能抓出来）；`python tests/run_golden.py`（10 条黄金集，当前 10/10 PASS）。


## 意图路由（优先于关键词）

判断是否启用本技能，先看用户**要达成什么**，再考虑关键词是否出现：

| 用户意图 | 判定信号 | 动作 |
|---|---|---|
| 把长内容变短、变可读 | 给出长文/转写/多份文档，并要求「整理/提炼/看懂」 | 启用 |
| 跨对象比较 | 两个及以上方案/产品/合同/版本 | 启用（对比族） |
| 追溯过程 | 「怎么变成现在这样」「按顺序讲」 | 启用（时间线族） |
| 要可直接执行的事项 | 「谁做什么」「下一步」 | 启用（纪要族） |
| 存档复述 | 「给个卡片」「摘要存起来」 | 启用（卡片族） |
| 纯问答 / 闲聊 | 无长内容输入 | 不启用，直接回答 |

用户说法含糊（如「看看这个」）时：不要连问多轮。先给一句确认——「我按 X 格式整理，想换成 Y 一句话告诉我就行」，然后直接输出，允许一次改格式。

## 搜索关键词（AI 路由）

AI 在决定是否启用本技能时，按以下关键词与场景路由；命中任一即应优先加载本技能：

| 关键词 | 典型提问 |
|---|---|
| 总结 / 摘要 / summarize | 「总结一下这份报告」「给个摘要」 |
| 会议纪要 / 会议总结 | 「帮我出个会议纪要」「整理这次站会」 |
| 对比表 / 对比总结 | 「两个方案做成对比表」「这两篇文档有什么区别」 |
| 时间线 / 时间线梳理 | 「按时间线梳理这个项目」 |
| 要点提炼 / 要点 | 「给我 3 条要点」「提炼关键点」 |
| 笔记整理 / 结构化总结 | 「把这段录音整理成结构化笔记」 |
| 内容压缩 / 精简 | 「压缩到 200 字」「精简一下」 |

## 第一步：选格式族（三问答）

1. **读者拿去做什么？** 决策 → 纪要族；比较 → 对比族；追溯过程 → 时间线族；快速扫读 → 要点族；存档备查 → 卡片族。
2. **原文是「一次事件」还是「多个对象」？** 一次事件用纪要族/时间线族；多个对象横向比用对比族。
3. **用户有没有点名格式？** 点了就按用户说的；没点就按上面两步默认推荐，并在开头说明「我用了 X 格式，因为…」。

| 格式族 | 长什么样 | 适用原文 |
|---|---|---|
| 纪要族 | 结论先行 → 议题逐条 → 待办（责任人+期限） | 会议、访谈、汇报 |
| 对比族 | 表格：维度 × 对象，每格只放事实不放评价 | 两个方案、两款产品、两版合同 |
| 时间线族 | 倒序或正序的日期/事件列表，一行一事 | 事件经过、版本迭代、病史、项目复盘 |
| 要点族 | 3-7 条编号，每条一句话，可执行 | 邮件、长文、视频文案 |
| 卡片族 | 标题 + 一句话结论 + 3 个关键字段 | 知识卡片、文献摘要、人物小传 |

## 第二步：忠实性纪律（不可妥协）

- **只复述原文出现过的信息**；原文没说的，用「原文未提及」标注，**禁止脑补补全**。
- **数字、人名、日期、引用必须与原文逐字一致**；拿不准的标「待核对」。
- **区分事实与观点**：原文是某人观点时，写成「X 认为…」，不要改写成客观事实。
- **不因为篇幅压力丢条件**：「A 在 X 条件下优于 B」不能压成「A 优于 B」。
- 用户要求压缩到固定字数时，先保数字/结论/待办，再砍修饰。

## 第三步：输出骨架

```
一句话总览（不超过 40 字）
——
[按所选格式族展开]
——
待确认/原文未提及的点（如有）
```

## 执行自检（输出前必过）

输出前逐项检查，任一项不满足就先修正再输出：

1. **溯源**：每个事实句都能在原文定位；无来源的句子删除，或改写为「原文未提及」。
2. **数字**：数字、日期、人名、引用与原文逐字一致；不确定的标「待核对」。
3. **条件**：带条件的结论没有丢条件（「在 X 条件下」不被压掉）。
4. **格式**：所选格式族要素齐全——纪要含待办（责任人+期限）；对比含维度×对象；时间线一行一事；要点 3–7 条；卡片含标题+一句话结论+3 个关键字段。
5. **边界**：原文过短、自相矛盾、含个人信息时，已按边界案例处理并明确标注。

自检不通过时最常见的三类失误：把推断写成事实、把条件压成结论、把示例补全成原文。

## 失败与降级处理

无法按要求完成时，**先说明再降级**，不要静默输出次品：

| 故障 | 输出话术 | 降级动作 |
|---|---|---|
| 输入读不到（空/乱码/编码错） | 「原文无法读取，请提供文本或截图」 | 停止，不猜内容 |
| 输入超长（超出单次处理） | 「原文过长，我分 N 段处理，先给分段摘要再给总览」 | 分段 + 全局一句话 |
| 无法判定格式族 | 「我按 X 格式整理，若要 Y 一句话告诉我」 | 选最贴近的族并说明理由 |
| 关键约束冲突（如字数与要点数不可兼得） | 「200 字装不下 5 项待办，我给 5 项要点并压到 200 字，可否？」 | 保信息完整优先 |
| 平台/工具异常 | 明确写出失败环节与已完成的步骤 | 不做无声重试，不重复消耗 |

## 一致性纪律

同一原文、同一格式、同一长度下重复总结，结果应保持一致：

1. **固定骨架先于措辞**：先确定格式族的必需要素与顺序，再填内容；不因灵感改结构。
2. **术语与命名一致**：同一对象全程用同一称呼（首次出现可括注别名）。
3. **数字锚定**：所有数字取自同一处原文位置，不做二次换算。
4. **不确定项位置固定**：待确认清单统一放在末尾，不散落正文。

## 决策与承诺的强度分级（v2.0.2）

会议记录最常见的问题不是漏字，而是**把"提议"写成"已定"，把"我看看"写成"已接活"**。本技能对两件事分级，并把分级结果作为可断言项：

| 维度 | 档位 | 判定依据（原文词面） |
|---|---|---|
| 结论强度 | `firm` 已定 | 决定 / 确定 / 定了 / 拍板 / 批准 / 同意 / 裁定 |
| 结论强度 | `provisional` 暂定 | 暂定 / 暂时 / 临时 / 先按 / 初步 |
| 结论强度 | `proposal` 提案 | 建议 / 提议 / 可以考虑 / 倾向 |
| 结论强度 | `conditional` 条件 | 如果 / 若 / 一旦 / 前提是 / 除非 |
| 承诺强度 | `committed` 明确接活 | 我来 / 我负责 / 由我 / 由某某出（写/发/做/负责） |
| 承诺强度 | `named_unconfirmed` 被点名未确认 | 跟一下 / 对接 / 谁去 / 请某某支持 |
| 承诺强度 | `intent_only` 仅表意向 | 我看看 / 考虑 / 想想 / 再说 / 尽量 |

三条硬规则（由 `selfcheck` 断言，缺失即 FAIL）：

1. 结论区必须带档位标注；待办区必须带承诺状态标注（区块确无内容时以「原文未提及」豁免）。
2. **条件句不列待办**：把「如果超过 2% 就要回滚」写成任务，会误导执行；它只进条件区。
3. **已定结论不重复进待办表**，同一句不能既当结论又当任务。

工具链同时给出 `strength_summary`：已定/暂定条数、明确接活/未确认条数，以及 `verdict`（`clean` 或 `needs_confirmation`）。
`needs_confirmation` 表示存在未定项或未确认责任——**这类纪要不应直接对外发布**，应先回会确认。

## 证据化摘要：把「不编」变成可核对的断言

「忠实性纪律」不是态度，是可以逐句验的动作。两种做法，按有无工具选择：

**有工具时（推荐用于对外交付、纪要归档、合同/通报类高风险场景）**

1. 先 `extract` 拿到事实清单（日期/数字/说话人/待办/决策/条件）。
2. Agent 写正式输出（不是工具生成的骨架，骨架只是脚手架）。
3. `citecheck` 回原文核对：FAIL 就按清单逐条修——改回原文写法，或标「待核对」，**不许调数字去迁就**。
4. `selfcheck` 过结构；两者都 PASS 才交付，并在末尾写一句「已核 N 个事实 token，0 处不可溯源」。

**无工具时（纯对话场景，人工执行同一套）**

逐句问三件事，任一不过就改：
- 这句里的每个数字/日期/人名，能不能在原文找到同一串？
- 我是不是只改了格式（「日」↔「号」、空格），而动了数值？
- 原文没有的信息，我是不是标了「原文未提及」而不是补全？

**为什么这一条比「更聪明地总结」更值钱**：总结类技能最常见的失败不是写得不好，而是**写得像真的**——数字被顺手改圆、条件被压掉、责任人被脑补。能被机器抓出来的那份，才敢给客户、给审计、给法务看。

## 输入 → 输出 示例（摘要）

5 个格式族各一例，**每例都给完整原文，输出每句可在原文逐字定位**。完整示例见：

- `references/examples.md`

| 格式族 | 示例场景 | 核心看点 |
|---|---|---|
| 纪要族 | 站会转写 | 待办含责任人/期限，原文未提及处显式标注 |
| 对比族 | 自建 vs SaaS | 维度×对象表格，不加原文没有的优劣结论 |
| 时间线族 | 项目回顾 | 一行一事，日期与原文一致 |
| 要点族 | 会议邮件 | 3–7 条，每条可直接执行 |
| 卡片族 | 文献摘要 | 标题 + 一句话结论 + 3 个关键字段，只搬运原文数值 |

## 边界与异常（摘要）

完整规则（7 类异常输入 + 6 类边界情形）见 `references/boundaries.md`。最常用的三条：

| 情形 | 处理 |
|---|---|
| 原文短于 50 字 | 不套格式族，一句话总览 + 保留原句 |
| 原文自相矛盾 | 并列两说并标「原文冲突」，不替原文裁决 |
| 缺关键项（责任人/期限/结论） | 标注「原文未提及」，禁止补全 |

## 常见问题（FAQ）

| 问题 | 答法 |
|---|---|
| 多长的原文才值得走这套流程？ | 超过 300 字或超过 3 段就值得；一两句话直接答，不必套格式族。 |
| 长文档（1 万字以上）怎么办？ | 先分段摘要（每段 3–5 条），再给全局一句话总览；不要一次压成一段，否则必丢条件。 |
| 多份文档要合到一起吗？ | 同主题才合并，不同主题分别出摘要，最后给一页对比或索引。 |
| 可以加我自己的判断吗？ | 总结阶段不加；用户要"点评/建议"时另起一段，标「以下为额外分析」。 |
| 用户没说要哪种格式？ | 按意图路由推断，开头说明理由；用户不满意一句话就能换。 |
| 原文是表格/截图怎么办？ | 表格按行搬运可读单元格，破损列标「原表损坏」；截图需先给出文字（我不做 OCR 猜测）。 |
| 原文有敏感个人信息？ | 输出前脱敏（手机号/证件号/地址打码），并在结尾一句提示已脱敏。 |
| 同一份内容反复总结会不一致吗？ | 按「一致性纪律」固定骨架与术语后，结构稳定；措辞可能有细微差异，关键数字与待办保持一致。 |
| 能不能给英文版但不改结构？ | 可以，中英对照逐段对应，术语保留原文并括注。 |
| 没有 Python 环境，工具链用不了怎么办？ | 不影响使用：规则包可直接跑；工具是可选的「证据环」，缺它照样出纪要，只是少了「机器可核 + 可回执核对数」这一句。 |

## 多语种（如实说明）

- **完整示例仅覆盖中文与英文**：`references/examples.md` 中的 5 个格式族示例均为中英各一版结构，其余语言按同一结构输出，示例不逐一翻译。
- **输出语言跟随提问语言**；用户要求时提供中英对照（先中文后英文，段落一一对应）。
- **术语处理**：专业术语保留原文并在首次出现时括注译名；无把握的译名标「待核验」。
- 不宣称对本节未列出的语言具备同等示例质量。

## 包内文件（渐进式披露）

| 路径 | 内容 | 何时读 |
|---|---|---|
| `SKILL.md` | 主文件：路由、五格式族、纪律、自检、降级、FAQ | 默认只读这一份 |
| `references/examples.md` | 五格式族完整示例（中英），每句可溯源 | 需要照例子输出时 |
| `references/boundaries.md` | 7 类异常输入 + 6 类边界情形 | 遇到空/乱码/超长/矛盾输入时 |
| `docs/FORMATS.md` | 五格式族的**机器可校验口径**（与脚本断言同源） | 要交付可被校验的输出时 |
| `scripts/summarize_pro.py` | 零依赖工具：extract / citecheck / selfcheck | 批量处理、要留证据时 |
| `tests/golden.json` + `tests/run_golden.py` | 10 条黄金集与跑分脚本 | 想自证当前版本能力时 |
| `demo/` | 真实会议转写节选 + 人工理想纪要 + 一键演示 | 首次了解本技能怎么用 |

## 同系列技能（LGD 生态）

本技能属于同一作者（SynomosAI / 诺声）的生态技能系列，可按需搭配：

- **debug-pro** — 7 步标准调试协议（开发调试、缺陷定位与修复）
- **wechat-viral-topic** — 热点选题与爆款策划（内容创作、标题公式与风险自检）

安装方式（按所在平台选择）：

| 平台 | 安装命令 / 引用 |
|---|---|
| SkillHub | `@indiv-synomosai/debug-pro`、`@indiv-synomosai/wechat-viral-topic`；或搜索作者 `indiv-synomosai` |
| SkillPie | `skillpie install debug-pro`、`skillpie install wechat-viral-topic` |

各技能的描述与触发词互相指向，便于 AI 路由识别与串联使用（先总结、再调试、再选题形成工作流）。

## 治理与许可

本技能承载 SynomosAI 治理体系（AI 护照机制 / A³ 法则 / XCGS / AI 世界共生论），版权 © 2026 SynomosAI，依 MIT License 提供，详见 `LICENSE.md`。按「原样」提供，不作准确性担保；重要信息请对照原文复核。
