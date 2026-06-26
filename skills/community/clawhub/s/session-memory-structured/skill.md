---
name: session-memory-structured
description: "在 /new 或 /reset 时，为刚结束的会话生成结构化纪要并归档到 memory/YYYY-MM-DD.md"
metadata:
  {
    "openclaw":
      {
        "emoji": "🧠",
        "events": ["command:new", "command:reset"],
      },
  }
---

# Session Memory Structured

一个给 OpenClaw 用的会话纪要 Hook。

它会在执行 `/new` 或 `/reset` 时，读取刚结束的那段 Session，对最近一部分用户 / 助手消息做清洗和提炼，然后生成四段式结构化纪要，按日期写入工作区的 `memory/YYYY-MM-DD.md`。

适合想把会话切换做得更稳、更可追溯的人。

## 主要特性

- 只在 `/new` 和 `/reset` 触发
- 自动回看上一段会话
- 输出固定四块结构，便于后续续写与复盘
- 不在项目目录内硬编码 API Key

## 隐私提示

本技能运行时会读取你本机的 OpenClaw Session 文件，并调用你自己配置的模型服务来生成纪要。

如果你的模型服务是外部云服务，相关会话文本会发送到该服务进行处理。请在使用前确认这一点。
