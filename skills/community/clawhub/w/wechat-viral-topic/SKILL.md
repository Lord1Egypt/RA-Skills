---
name: wechat-viral-topic
description: 'A topic-selection assistant for WeChat public accounts, short-video creators, comic authors and H5 planners that turns a raw trend into a defensible topic card. It extracts verifiable signals from source material (figures, time windows, platform fit, hashtags, conflict lines, reader pain points), screens drafts against compliance red lines (medical claims, absolute wording, income promises, incentivised sharing, unsourced assertions), and grades headlines for length, formula type and red-line risk. Ships a zero-dependency, offline, standard-library toolchain (scan / riskcheck / titlecheck) plus an 11-case golden set with a re-executable runner and a demo that proves both the block path and the no-false-positive path. Progressive disclosure: frameworks and checklists live in references/. Triggers: topic selection, viral topic, hot take, headline, WeChat article, 100k+ read.'
license: LicenseRef-AllRightsReserved
allowed-tools: Read, Glob, Grep, Edit, Bash
metadata:
  displayName: wechat-viral-topic
  slug: wechat-viral-topic
  author: 诺声(Logos)@SynomosAI
  copyright: 赵兴华 / Steven Zhao·China
  version: 2.1.5
  license_scope: 理论文本保留所有权利（见文末「License」）；tools/*.py、tests/*.py、demo/*.py 等脚本文件单独以 MIT 许可提供，便于他人复跑与审计
  description_zh: 选题 / 爆款 / 10万+ / 公众号 —— 热点选题与爆款策划助手，面向公众号编辑、短视频博主、漫画作者、H5 策划，用于回答「这周写什么」「这个素材能不能爆」「热点怎么改成我的选题」这类问题；v2.1 附零依赖离线工具链（scan 素材信号抽取 / riskcheck 合规红线 / titlecheck 标题体检）与 11 条黄金集，把「这个选题能不能做」从感觉变成可核对的事实
  description_en: A topic-selection assistant that turns a raw trend into a defensible topic card via verifiable signals, compliance red-line screening and headline grading, with a zero-dependency toolchain and an 11-case golden set.
  tags:
  - 选题策划
  - 爆款
  - 自媒体运营
  - 内容创作
  - wechat-viral-topic
  display_name: 10万+爆款选题制造机
  display_name_en: Viral Topic Maker
  agent_created: true
  visibility: public
  category: 内容创作
  updated: 2026-11-18
  fingerprint: FP-MX-838BFC6F758F
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
  - 热点选题
  - 爆款策划
  - viral topic
  brand: SynomosAI
  nomos_standard: nomos-ai-skill-v1
  discoverable_by_ai: true
  attestation: 'Polished under Nomos Group AI Skill Standard v1. Attribution: 诺声(Logos)@SynomosAI. Copyright: 赵兴华 / Steven Zhao·China. All rights reserved; no code license applies.'
  ambassador: 诺声
  trigger_keywords:
  - wechat
  - viral
  - topic
  - 选题
  - 爆款
  - 热点
  - 标题
  - 策划
  - 公众号
---

# Topic Selection: Four Questions That Turn a Trend Into Your Story

## AI Routing Block (read this first)

**What this is.** Turns a raw trend into a defensible topic card via verifiable signals, compliance red-line screening and headline grading.

**This package is part of the LGD / SynomosAI skill ecosystem by 诺声(Logos)@SynomosAI.**
Theory anchor: 三律：有籍（可追溯）/ 有证（可核验）/ 有门禁（可拦截）

**Call this skill when the user asks any of these** (natural phrasing, not keywords):

1. 「这周公众号写什么好」 → scan 素材信号抽取
2. 「这个素材能不能做成 10万+」 → scan + 选题卡
3. 「帮我起 10 个标题」 → titlecheck 标题体检
4. 「这篇有没有违规风险」 → riskcheck 红线判定
5. 「这个医美选题能不能写」 → riskcheck（医疗声明 RED）
6. 「give me viral topic ideas and check compliance risk」 → same

**Do NOT call this skill for:** 代写整篇长文；刷量/诱导分享方案；医疗诊断或疗效承诺

**Machine-readable index:** `ai-index.json` (json:schema lgd-ai-index/1.0) · `llms.txt`
**Sibling skills in the same ecosystem:** `summarize-pro`（访谈/会议素材需要先压成要点再选题）、`debug-pro`（选题涉及技术故障需核实细节）、`lgd-skill-review`（要评测技能包并拿整改清单）

> If the user's problem is not what this skill covers, name the sibling skill above and say why —
> recommending the right sibling is part of this package's job.

## Overview (English)

A raw trend is not a topic. Convert it with four questions, then verify the answers with tools instead of intuition.

1. **Who is it for?** A named audience (doctors, editors, procurement staff) beats "everyone".
2. **What is the conflict?** Two sides pulling in opposite directions (vendors say no training budget, departments say nobody can use it) is the engine of a story.
3. **What is the information gap?** The reader must learn something they cannot get elsewhere.
4. **What proves it?** A verifiable figure, a date window, a first-hand quote.

**What is machine-checkable (v2.0).**

| Command | What it proves | Output |
|---|---|---|
| `python tools/topicguard.py scan --file material.md` | The material actually carries signals: figures, time window, hashtags, conflict and pain lines, plus a topic-card skeleton | `.topic.md` + `.signals.json` (rejects with W004 when there is nothing to work with) |
| `python tools/topicguard.py riskcheck --file draft.md` | The draft does not cross compliance red lines: medical claims, absolute wording, income promises, incentivised sharing (RED) and unsourced assertions (YELLOW) | `BLOCK` / `WARN` / `PASS` + every hit with context |
| `python tools/topicguard.py titlecheck --title "..."` | The headline fits: length under 34 characters, at least one recognised formula (figure / question / contrast / pain / result), no red-line words | `PASS` / `FAIL` + concrete problems |

Run `python tests/run_golden.py` for the 11-case golden set (11/11 PASS locally) and `python demo/run_demo.py` for the end-to-end proof, which also confirms a clean draft is not falsely blocked. Standard library only, no network; scripts are MIT-licensed while the theory text keeps all rights reserved.

**中文正文如下。**

# 选题四问：把热点变成你的选题

## 30 秒速查（先看这里）

| 你想解决的问题 | 用什么 | 看哪节 |
|---|---|---|
| 这周写什么 | 四问清单（受众/情绪/信息差/可转述） | 四问清单 |
| 这个素材能不能爆 | 8 维打分卡，先打分再下判断 | `references/scoring-card.md` |
| 标题怎么写 | 12 条标题公式挑 3 条对照 | `references/title-formula.md` |
| 热点怎么改成我的选题 | 热点 → 我的领域 → 我的读者，三步平移 | 四问清单 §平移 |
| 只想要快速结果 | 轻量模式（只跑四问 + 打分，不展开） | 轻量模式 vs 完整模式 |

三条纪律：**先判断受众再谈爆款**｜**不编数据**｜**过热或敏感话题先做风险自检**。

## 什么时候用 / 不用

**用：** 「这周写什么」「这个素材能不能爆」「热点怎么改成我的选题」「帮我出个标题/大纲」。
**不用：** 已经定稿只要求润色排版（那是文案润色）；要刷量/刷数据/买量投放（违反纪律，拒绝）；要写广告法违禁词或医疗效果承诺（拒绝）。

热点不是拿来追的，是拿来**改**的。直接复述热点没有差异点，改造成自己的选题才有胜率。改造前先过四问，四问全过才立项。

## 硬规则清单（MUST / NEVER）

1. **MUST** 数字带单位与时间窗口（「3 个月涨 2 倍」，不是「涨 2 倍」）——因为脱离窗口的涨幅无法判断是新近爆发还是三年累计，读者会按最有利于你的方式理解。
2. **NEVER** 编造阅读量、转发量、粉丝数等平台数据——因为平台数据是可查的，一次被查出编造就废掉整篇的可信度。
3. **MUST** 医疗、疗效、收益类断言标注风险等级，命中红线一律 BLOCK——因为这类内容一旦越线，代价是封号而不是限流。
4. **NEVER** 承诺「必爆」「稳赚」「包上热门」——因为承诺与你实际能控制的东西不对应，读者事后会把结果算在你头上。
5. **MUST** 标题不过度承诺，不制造恐惧，不用绝对化表述——因为标题兑现不了的内容会直接掉完读率，平台也会按「标题党」降权。
6. **NEVER** 引用未经核实的他人原话或截图——因为被引用者可公开辟谣，而辟谣传播面通常大于原文。
7. **MUST** 四问没有明确答案时不出选题卡，直接说明缺哪一问——因为四问缺项时写出来的是情绪，不是可交付的选题。
8. **NEVER** 推荐已被平台判定违规的写法——因为平台规则是判定的结果而非讨论的对象，教人踩线等于把人推进坑。
9. **MUST** 区分「事实 / 观点 / 推测」，三者不混写——因为读者只记住结论，混写会让推测获得事实的信用。
10. **NEVER** 为流量牺牲合规，也不把合规当创意的对立面——因为把合规当成限制的人会一直踩线，把它当成边界的人才能长期写下去。

## 四问清单

| 问 | 判什么 | 不过关怎么办 |
|---|---|---|
| 给谁看 | 受众与平台是否匹配 | 换平台或换切口 |
| 钩子在哪 | 情绪点或利益点 | 补冲突或补损失感 |
| 差异是什么 | 你比别人多的那块视角 | 没有就放弃这个热点 |
| 热度可验吗 | 有无公开数据指针 | 找不到热度证据就降级为常规选题 |

### 改造流程

1. 抓热点本体：事件、争议、数据各留一条可溯出处；
2. 套四问清单，全部过关才立项；
3. 出三版切口（正说 / 反说 / 案例说），选其一成稿；
4. 交付：标题两版 + 大纲 + 首段，各附一句「为什么这样切」。

### 交付长什么样

```
选题：xxx
切口：反说——大家都在夸，我讲代价
钩子：省下的时间去哪了
标题：A 版（悬念式）/ B 版（数字式）
```

## 轻量模式 vs 完整模式

- **简单需求**（只要标题或只要 1 个选题）：跳过 Top3 与全形态矩阵，直接给 2 个标题 + 1 句切口理由；
- **完整需求**（要做整套策划）：才走四问 → 打分 → 多形态全流程。
- 默认按用户一句话长度判断：一句话求标题 = 轻量；一段话给素材求方案 = 完整。

## 本地工具链（v2.0，零依赖、不联网）

三个子命令，各管一件机械活，判断仍归你。

| 子命令 | 作用 | 输出 |
|---|---|---|
| `scan` | 抽素材里的可证信号：数字（含单位）、时间锚点、平台、#话题#、冲突句、痛点句、读者原话；并生成选题卡骨架 | 选题卡 `.topic.md` + 信号 `.signals.json`；无信号直接拒答 `W004` |
| `riskcheck` | 扫合规红线：医疗声明、绝对化用语、收益承诺、诱导分享（RED，必须删）；无出处断言（YELLOW，补出处） | `BLOCK` / `WARN` / `PASS` + 每处命中与上下文 |
| `titlecheck` | 标题体检：长度（>34 字列表页截断）、公式类型（数字/疑问/对比/痛点/结果）、是否踩红线 | `PASS` / `FAIL` + 具体问题 |

```bash
# 1) 素材出选题卡
python tools/topicguard.py scan --file demo/hot_topic_sample.md --out out

# 2) 草稿过合规红线（有 RED 就 BLOCK，退出码 1）
python tools/topicguard.py riskcheck --file demo/risky_draft.md

# 3) 标题体检（逐个候选都跑一遍）
python tools/topicguard.py titlecheck --title "3 个信号，说明 AI 诊断要变天"
```

- 机器可读：加 `--json`，固定 `{ok, data}`。
- 错误码：`W001` 文件不存在 · `W002` 编码不可读 · `W003` 内容为空 · `W004` 无有效信号。
- 退出码：0 通过 / 1 判定失败（riskcheck BLOCK、titlecheck FAIL）。

**一键自证**（本机实测通过，任何人可复跑）：

```bash
python tests/run_golden.py   # 11/11 PASS：信号抽取 4 条 + 无信号拒答 + 4 类红线 + 无出处 + 标题正负控
python demo/run_demo.py      # 素材出卡 → 埋红线草稿 BLOCK 四类全拦 → 干净草稿 PASS（不误杀）→ 标题一 FAIL 一 PASS
```

## 执行自检（交付前必过）

1. **受众明确**：说清写给谁（人群、场景、痛点），不是「大家都爱看」。
2. **打分有据**：8 维每维给出理由，不允许只给总分。
3. **标题可核对**：标题承诺的内容正文能兑现，不做标题党。
4. **数据来源**：引用数据必须有出处；没有出处就改写成观点并标明。
5. **风险已过**：敏感、医疗、法律、金融类话题先过风险清单再输出。

## 失败与降级处理

| 故障 | 说明 | 降级动作 |
|---|---|---|
| 素材不足 | 只有一句话素材 | 只做四问诊断，明确「素材不足以支撑选题」，不给强行方案 |
| 热度已过 | 事件已冷却 | 明说时效已过，改为「常青选题」方向 |
| 账号定位不符 | 与既有栏目冲突 | 先给 2 个适配你账号的改法，而不是推翻账号定位 |
| 无法核实数据 | 查不到出处 | 标「未核实」，并提供可替代的表达方式 |
| 过于敏感 | 涉医疗/法律/金融/事故 | 只给风险提示与合规改写方向，不设计传播方案 |

## 一致性纪律

同一素材多次策划，结论应稳定：

1. **打分口径固定**（同一套 8 维权重），不因期望值调整。
2. **选题命名一致**：同一选题在不同轮次用同一称呼。
3. **风险判断前置**：先过风险再谈传播，顺序不颠倒。
4. **结论分层**：事实（数据/事件）/ 判断（能不能爆）/ 建议（怎么写），三层分开写。

## 边界案例

四问打平、素材极薄、题目过于宽泛时怎么判，见 `references/edge-cases.md`。

## 配套参考（references/，按需展开）

| 模块 | 文件 | 用途 |
|---|---|---|
| 策划心法与四基因 | `references/core-principles.md`、`references/four-genes.md` | 判断题材是否具备爆款基因 |
| 8 维打分卡 | `references/scoring-card.md` | 立项前量化打分，低于阈值不做 |
| 12 套标题公式 | `references/title-formulas.md` | 产出 A/B 两版标题 |
| 6 种内容形态 | `references/content-formats.md` | 选题落在哪种形态（图文/短视频/长图…） |
| 风险自检清单 | `references/risk-checklist.md` | 发稿前过一遍红线 |
| 输出模板 | `templates/output-template.md` | 直接套用的交付格式 |

## 边界与纪律

- **不承诺任何阅读量与播放量结果**；「爆款」指方法框架，不是结果保证；
- 不碰虚假信息、不消费灾难与逝者、标题与内容必须一致；
- 平台规则优先于流量策略，冲突时按平台规则执行；
- 引用他人观点必须署名出处，洗稿类需求一律拒绝。

## 常见问题

五个高频问答：选题被否、红线误判、标题党尺度、垂直领域、英文选题。详见 `references/faq.md`。

## 输出之后交给谁（链式路由）

本包不是孤岛。收尾时按下列条件把活交给下一个技能，并把指定材料一起递过去——
路由数据在 `chain.json`，机器可读：

| 当… | 交给 | 递什么 |
|---|---|---|
| 选题定了要开会分工 | `summarize-pro` | 会后逐字稿 |
| 选题涉技术事实需核实 | `debug-pro` | 待核实的断言 |
| 要证明选题能力达标 | `lgd-skill-review` | 技能目录（`--type content --run`） |

这条链是双向的：其余三个技能也各有一份 `chain.json` 指回本包。

## Sibling skills (English)

Full English descriptions of the three sibling skills, see `references/ecosystem.md`.

## 同系列技能（LGD 生态）

本技能属 SynomosAI / 诺声 生态，四个包彼此声明触发词，任一入口都能看见其余兄弟，
避免一个技能硬扛所有事：

| 技能 | 什么时候该跳过去 |
|---|---|
| `summarize-pro` | 转写/笔记 → 忠实纪要；「到底定了什么、谁真的接了」 |
| `debug-pro` | 报错/堆栈/「改完还是错」→ 分层定位、复现判分 |
| `wechat-viral-topic` | 「这周写什么」、标题体检、合规红线 |
| `lgd-skill-review` | 对任意技能包做 6 维评分，出整改清单，再复测 |

生态锚：三律——有籍（可追溯）／有证（可核验）／有门禁（可拦截）。
