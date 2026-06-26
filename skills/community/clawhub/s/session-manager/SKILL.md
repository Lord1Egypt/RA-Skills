---
name: session-manager
description: |
  会话管理工具。自动追踪对话会话，提示用户切换话题创建新会话，
  并将会话记录保存到用户指定的位置（飞书多维表格或本地文件）。
  当用户说"切换话题"、"开新会话"、"新话题"时触发。
---

# Session Manager / 会话管理

自动管理对话会话的生命周期。Automatically manage dialogue session lifecycle.

## 触发场景 / Triggers

- 用户说「切换话题」「开新会话」「新话题」/ User says "switch topic", "new session", "new topic"
- 用户使用 `/new` 命令 / User uses `/new` command
- **主动检测**：在会话过程中，发现用户转换了话题但未切换，主动询问是否开启新会话 / **Active Detection**: When detecting topic shift during conversation without session switch, proactively ask if user wants to start a new session

## 主动询问规则 / Proactive Ask Rules

当检测到话题转换时（与当前会话主题明显无关），礼貌询问：/ When detecting topic shift (unrelated to current session topic), politely ask:

```
听起来你想聊一个新话题。需要我开启新会话吗？
上一段聊的是「{当前主题}」，我会把相关信息延续到新会话。

Sounds like you want to chat about a new topic. Should I start a new session?
The previous topic was "{current topic}", I'll carry relevant info to the new session.
```

## 会话创建流程 / Session Creation Flow

1. **询问用户**：确认是否开启新会话 / **Ask User**: Confirm whether to start a new session
2. **继承上下文**：询问是否需要把上一段交流的重要内容带入新会话 / **Inherit Context**: Ask if important info from previous conversation should be carried over
3. **创建记录**：在用户指定的存储位置创建会话记录 / **Create Record**: Create session record at user's specified storage location

## 存储位置 / Storage Options

支持两种方式，用户首次使用时询问偏好：/ Supports two options, ask user preference on first use:

### 1. 飞书多维表格（默认推荐）/ Feishu Bitable (Default Recommended)

需要字段 / Required fields:
- 会话ID（数字，整数）/ Session ID (number, integer)
- 会话主题（文本）/ Session Topic (text)
- 会话日期（日期）/ Session Date (date)
- 开始时刻（日期+时间）/ Start Time (date+time)
- 结束时刻（日期+时间）/ End Time (date+time)
- 前序会话ID（数字，可空）/ Previous Session ID (number, optional)

### 2. 本地 Markdown 文件 / Local Markdown Files

存储在 `memory/sessions/` 目录，文件名格式：`session-{id}.md` / Stored in `memory/sessions/`, filename format: `session-{id}.md`

```markdown
# 会话 {ID}: {主题}

- 开始时间: {ISO时间}
- 结束时间: {ISO时间}
- 前序会话: {ID}

## 内容摘要
...

# Session {ID}: {Topic}

- Start Time: {ISO time}
- End Time: {ISO time}
- Previous Session: {ID}

## Summary
...
```

## 会话结束 / Session End

用户结束会话或开启新会话时：/ When user ends session or starts new session:
1. 填写当前会话的「结束时刻」/ Fill in "End Time" for current session
2. 如果是接续之前会话，记录前序会话ID / If continuing from previous session, record Previous Session ID

## 状态管理 / State Management

在 `MEMORY.md` 中维护当前会话信息：/ Maintain current session info in `MEMORY.md`:

```
## 当前会话 / Current Session
- 会话ID: X / Session ID: X
- 会话主题: XXX / Session Topic: XXX
- 开始时间: YYYY-MM-DD HH:mm / Start Time: YYYY-MM-DD HH:mm
- 前序会话ID: X (如果有) / Previous Session ID: X (if any)
```

## 注意事项 / Notes

- 首次使用需询问用户存储偏好 / Ask user's storage preference on first use
- 飞书模式下，优先使用已配置的多维表格 / In Feishu mode, use pre-configured bitable if available
- 本地模式使用 Markdown 文件，可导出为其他格式 / Local mode uses Markdown files, can export to other formats
