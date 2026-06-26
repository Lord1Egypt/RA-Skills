---
name: feishu-file-send
description: |
  飞书文件发送标准流程 | Reliable Feishu file sending workflow.
  解决附件发送失败、用户收不到文件、mediaLocalRoots 路径限制等问题。
  Fixes missing attachments, mediaLocalRoots path issues, and combined text+file delivery failures.
---

# Feishu File Send / 飞书文件发送

Use this skill whenever you need to send a file to a Feishu user, or when a Feishu user reports they did not receive an attachment.

当需要向飞书用户发送文件，或用户反馈未收到附件时，使用此 Skill。

---

## Core Rule / 核心规则

**For Feishu, do NOT combine text and attachment in one outbound message when reliability matters.**

**飞书场景下，不要将文字说明和附件合并到同一条消息中发送。**

Always use this sequence / 始终按此顺序操作：

1. **Prepare the file** in an allowed local path / 将文件保存到允许的目录
2. **Send a short text message** first, if any explanation is needed / 先发一条简短文字说明
3. **Send the attachment** as a **separate** outbound message / 再单独发送附件

---

## When to Use / 使用场景

Use it when the user asks you to / 当用户要求你：

- send a file / 发送文件
- return an edited document / 返回编辑后的文档
- deliver a generated Word, Excel, PDF, PPT, TXT, image, or similar attachment / 发送生成的文档、表格、PDF、图片等附件
- test Feishu attachment sending / 测试飞书附件发送功能
- debug missing Feishu attachments / 排查飞书附件丢失问题
- diagnose file delivery failures in Feishu / 诊断飞书文件发送失败

This skill is especially important in Feishu DMs, but the same pattern is also safer in Feishu groups.

此 Skill 在飞书私聊中尤为重要，但在飞书群聊中也建议使用相同模式。

---

## Required Workflow / 标准流程

### 1. Check the file path / 检查文件路径

Before sending, ensure the file lives under an allowed `mediaLocalRoots` directory.

发送前，确保文件位于 `mediaLocalRoots` 配置的允许目录中。

Known-good path in most setups / 通常可用的路径：

- `~/.openclaw/workspace/` (the default workspace directory / 默认工作区目录)

If a generated file is under `/tmp/` or another temporary path, move or copy it into an allowed directory before sending, unless you already know that path is whitelisted in `mediaLocalRoots`.

如果文件在 `/tmp/` 或其他临时目录，请先复制到允许目录再发送，除非你确认该路径已在白名单中。

### 2. Send text separately / 先发送文字

If you need to say something like "here is the file" or explain what changed, send that as a plain text message first.

如果需要说明"这是文件"或解释修改内容，先发送纯文字消息。

Keep it short / 保持简短。

### 3. Send the attachment separately / 再发送附件

Send the file in its own message using the message tool with `media` set to the local file path.

使用 message 工具单独发送文件，`media` 参数设为本地文件路径。

**Do NOT attach explanatory text to the same outbound file message.**

**不要在同一条附件消息中包含说明文字。**

---

## What to Avoid / 禁止操作

Do **NOT** / **不要**：

- combine text and file in one Feishu outbound message when attachment visibility matters / 在需要确保附件可见性时，将文字和文件合并到一条消息
- assume `/tmp/` is safe to send from / 默认 `/tmp/` 目录可以发送文件
- use `MEDIA:` inline attachment rendering for Feishu when you need reliable file delivery, if you can directly use the `message` tool instead / 在需要可靠文件发送时，避免使用 `MEDIA:` 内联渲染，直接使用 message 工具

---

## Delivery Pattern / 发送模式

Preferred pattern / 推荐模式：

1. `message.send` with **text only** / 仅发送文字
2. `message.send` with **media only** / 仅发送附件
3. After tool success, do not duplicate the same content again in chat / 工具成功后，不要在聊天中重复相同内容

If you use `message` to deliver the user-visible reply, answer with `NO_REPLY`.

---

## Failure Diagnosis / 故障排查

If the recipient says they did not receive the file / 如果用户说没收到文件：

1. Confirm whether plain text messages are arriving / 确认纯文字消息能否正常收到
2. Confirm whether the file was sent as a standalone attachment message / 确认文件是否作为独立附件消息发送
3. Confirm the file path is inside `mediaLocalRoots` / 确认文件路径在 `mediaLocalRoots` 白名单内
4. Retry by copying the file into `~/.openclaw/workspace/` (or another allowed directory) and re-sending / 复制到 `~/.openclaw/workspace/` 或其他允许目录后重试
5. If needed, consult `references/feishu-file-sending-notes.md` / 如需更多细节，参考 `references/feishu-file-sending-notes.md`

---

## Known Validated File Types / 已验证的文件类型

Validated in Feishu DM on 2026-04-16 when sent separately / 2026-04-16 在飞书私聊中验证通过（分开发送）：

- **txt** — 纯文本
- **docx** — Word 文档
- **xlsx** — Excel 表格
- **pdf** — PDF 文档

You may still send other file types, but if reliability matters and they fail, debug using the same path and separation rules.

其他文件类型也可发送，如果失败请按相同规则排查。

---

## Config Tips / 配置建议

If dynamic files are commonly generated under `/tmp/`, consider adding `/tmp` to Feishu `mediaLocalRoots` in `~/.openclaw/openclaw.json` and restart gateway.

如果经常生成临时文件，可在配置中将 `/tmp` 加入飞书渠道的 `mediaLocalRoots` 白名单，然后重启 gateway。

---

## Reference / 参考

For the full tested behavior and troubleshooting notes, read / 完整实测记录和排查指南：

- `references/feishu-file-sending-notes.md`
