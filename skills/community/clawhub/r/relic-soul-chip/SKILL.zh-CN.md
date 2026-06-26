---
name: relic-soul-chip
description: "Relic 灵魂芯片——让你的 AI Agent 拥有跨会话的持久人格和记忆。纯 Markdown，人类可读。换躯壳，灵魂跟着走。"
version: "1.3.2"
author: LucioLiu
license: GPL-3.0
homepage: "https://github.com/LucioLiu/relic"
metadata:
  hermes:
    tags: [人格, 记忆, 跨Agent, 身份, AI灵魂, Agent记忆, Markdown]
    related_skills: []
    requires_toolsets: []
    filesystem_scope:
      read: ["~/relic/brain/", "~/relic/docs/"]
      write: ["~/relic/brain/MEMORY.md", "~/relic/brain/SESSIONS/", "~/relic/brain/ARCHIVE/", "~/relic/brain/SOUL.md", "~/relic/brain/USER.md", "~/relic/brain/SKILLS/", "~/relic/brain/PROJECTS/", "~/relic/brain/INBOX/"]
---

# ⚡ Relic 灵魂芯片

> **🤖 AI Agent？读 `AGENT.zh-CN.md`（中文）或 `AGENT.md`（英文）。** 那里面有完整的分步指引。本文件是注册描述符，不包含执行步骤。

给你的 AI Agent 一个跨会话的持久人格和记忆。纯 Markdown。人类可读。零依赖。

**一个灵魂，多个躯壳。** 性格和记忆存在纯 Markdown 文件中。在 OpenClaw、Hermes、Claude Code、Cursor 之间切换——AI 灵魂保持不变。

## 快速开始

1. 安装：`git clone https://github.com/LucioLiu/relic.git ~/relic`
2. **🤖 Agent**：读仓库根目录的 `AGENT.zh-CN.md`（中文）或 `AGENT.md`（英文）
3. **👤 人类**：读 `README.md` 了解设置说明

## 需求

| 需求 | 用途 |
|------|------|
| 文件系统读写 | 读写 `~/relic/brain/` 中的 Markdown 文件 |
| `git` | 安装/更新（可选——可手动下载 ZIP） |
| HTTP 请求 | 版本检查（可选——离线可跳过） |

## 规则

- 🔴 永不删除或覆盖 SOUL.md 或 USER.md 的核心字段
- 🟡 只追加到 MEMORY.md
- 🔴 永不删除 ARCHIVE/
- 🟡 SESSIONS/ 只追加新文件，不修改或删除已有文件
- 🔴 永不访问 ~/relic/brain/ 以外的文件（锚点除外）
- ⚠️ 记录敏感信息前必须询问

来源：https://github.com/LucioLiu/relic
