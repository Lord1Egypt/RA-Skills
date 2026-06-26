---
name: meeting-notes
description: Generate structured meeting minutes from transcripts or raw notes — extract key decisions, action items, and follow-ups. Use when the user needs to: (1) convert meeting recordings or transcripts into formatted notes, (2) extract decisions and owners from informal discussion, (3) track task assignments across multiple meetings, (4) produce meeting summaries for distribution, (5) archive meeting records for later reference. Supports 1:1s, team standups, client meetings, technical design reviews, and board/project steering meetings.
emoji: 📝
---

# Meeting Notes — 会议纪要助手

Transform meeting transcripts, audio summaries, or raw notes into structured, actionable meeting minutes.

## Supported Meeting Types

| Type | Best For | Template |
|:-----|:---------|:---------|
| **1:1 / 双人会** | 主管与下属的定期一对一 | Standard |
| **Standup / 站会** | 每日/每周团队同步 | Standup |
| **Team Meeting / 团队会** | 周会、项目同步、复盘 | Standard |
| **Client Meeting / 客户会** | 与外部的商务/需求讨论 | Client |
| **Design Review / 技术评审** | 架构设计、代码审查会议 | Technical |
| **Steering / 项目决策会** | 跨团队的重大决策 | Executive |
| **Retrospective / 回顾会** | 项目/迭代结束后的复盘 | Retro |

## Workflow

### Step 1: Determine input type

Ask what form the input is in:

- **Transcript** — Full conversation text (can be long; no need to read all if not needed)
- **Raw notes** — The user's bullet points or jotted notes
- **Audio recording** — Ask user to provide a transcript or summary first (no audio processing capability)
- **Already-concise summary** — The user just wants it formatted and structured

### Step 2: Select template

Use the template matching the meeting type. All templates follow the same core structure with type-specific sections.

🧾 **Meeting Type:** [1:1 | Standup | Team | Client | Technical | Executive | Retro]

```
# 📋 [会议主题]

**日期：** YYYY-MM-DD
**时间：** HH:MM - HH:MM (GMT+8)
**地点：** [会议室 / 线上链接]
**参会人：** [姓名1, 姓名2, ...]
**缺席人：** [姓名, N/A]
**记录人：** [姓名]

---

## 📌 会议目标
[2-3句话概括会议目的]

## 🗣 讨论要点

### 1. [议题1标题]
- 关键讨论：
  - [要点1]
  - [要点2]
- 争议点 / 不同意见：[如有]
- 结论：[最终决定或共识]

### 2. [议题2标题]
...

### [N]. [议题N标题]
...

## ⚡ 关键决策
| # | 决策内容 | 决策人 |
|:-:|:---------|:------:|
| 1 | [决策] | [姓名] |
| 2 | [决策] | [姓名] |

## ✅ 行动项 (Action Items)
| # | 事项 | 负责人 | 截止日期 | 状态 |
|:-:|:-----|:-------|:---------|:----:|
| 1 | [具体可执行的行动] | @[姓名] | YYYY-MM-DD | 🆕 新建 |
| 2 | [行动] | @[姓名] | YYYY-MM-DD | 🏃 进行中 |

## 📎 待查 / 备注
- [待核实信息或后续讨论点]
- [下次会议需要准备的资料]
- [引用文档/链接]
```

### Standup template variation

```
# ☀️ [Team Name] Standup — YYYY-MM-DD

## ✅ 昨日完成
- [姓名1]: [完成项]
- [姓名2]: [完成项]

## 🚧 今日计划
- [姓名1]: [计划项]
- [姓名2]: [计划项]

## ⚠️ 阻塞项 (Blockers)
| 阻塞内容 | 涉及人 | 需要谁协助 |
|:---------|:-------|:-----------|
| [问题] | @[姓名] | @[协助人] |

## 📊 整体进度
[项目/里程碑的总体进度描述]
```

### Client meeting variation

Add a "客户反馈" section:

```
## 💬 客户反馈
- **满意点：** [客户肯定的部分]
- **顾虑点：** [客户表达的担忧]
- **后续需求：** [客户提出的新需求或变更]

## 📝 纪要确认
[本次纪要需在 X 个工作日内发客户确认]
```

### Retrospective template variation

```
## 🔄 复盘要素

### 👍 做得好 (Good)
- [保持的事项]

### 👎 要改进 (Improve)
- [需要改变的事项]

### 💡 新尝试 (Try)
- [下个周期可以尝试的事项]

## 📊 健康度评分
[团队协作 | 沟通 | 代码质量 | 交付速度] 各维度评分 1-5

## 🎯 改进目标
| 改进项 | 具体目标 | 负责人 | 检查时间 |
|:-------|:---------|:-------|:---------|
| [目标] | [SMART定义] | @[姓名] | YYYY-MM-DD |
```

### Technical Design Review variation

```
## 🏗️ 架构方案

### 方案 A：[名称]
- 优点：[list]
- 缺点：[list]
- 预估工作量：[人天]

### 方案 B：[名称]
- 优点：[list]
- 缺点：[list]
- 预估工作量：[人天]

### 最终选择
[选定的方案及理由]

## ⚠️ 风险项
| 风险 | 影响 | 可能性 | 应对措施 |
|:-----|:-----|:-------|:---------|
| [描述] | [高/中/低] | [高/中/低] | [方案] |
```

### Step 3: Extract key information

When processing a transcript or raw notes, extract:

1. **Meeting metadata** — Topic, date (use current date if not specified), attendees, duration
2. **Agenda items / discussion topics** — Group related discussion into topics
3. **Decisions** — Any choices made ("we decided to...", "going with X", "approved")
4. **Action items** — Anything with an owner + deadline ("I'll send the report", "please review by Friday")
5. **Open questions / blockers** — Things left unresolved
6. **Next meeting** — Scheduled or not yet

### Step 4: Write the notes with the chosen template

Follow these rules:

- **Use the template exactly** — Don't skip sections; fill "N/A" or "暂无" if empty
- **Keep the meeting date accurate** — Use the meeting date, not today's date. Ask if uncertain
- **Be concise** — Use bullet points, not paragraphs. Each bullet = one idea
- **Action items must be concrete and assigned** — If the transcript says "we need to look into X" without an owner, ask: "Who owns this?"
- **Preserve context** — Include enough context for someone who didn't attend to understand
- **Don't fabricate** — If you're unsure about something, mark it with `[待确认]`
- **Chinese output is the default** — Use English only if the input is entirely English or the user requests it

### Step 5: Save and deliver

Save the meeting notes to a file:
```
meetings/YYYY-MM-DD_[topic-slug].md
```

If the user needs to share, confirm the path and offer to adjust formatting for the target platform (email, Slack, WeChat, Feishu).

## Special Notes

- **Assume no internet access** for audio transcription. Ask user to provide text input.
- **When the input is very long** (e.g., 1hr transcript), read the beginning and end, and sample the middle. Focus on decisions and action items.
- **For recurring meetings** (e.g., weekly standup), check prior notes in `meetings/` for continuity.
- **Action items from previous meetings** should be carried forward with updated status.
- **If multiple meeting notes are requested at once**, process them individually and save each to its own file.
