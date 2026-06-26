---
name: handoff
description: Compact the current conversation into a handoff document for another agent to pick up.
argument-hint: "What will the next session be used for?"
---

写一份 handoff document，总结当前对话，让 fresh agent 可以继续工作。保存到用户 OS 的 temporary directory，而不是当前 workspace。

在文档中包含一个 “suggested skills” section，建议 agent 应 invoke 的 skills。

不要重复已经捕获在其他 artifacts（PRDs、plans、ADRs、issues、commits、diffs）中的内容。改用 path 或 URL 引用它们。

Redact 任何 sensitive information，例如 API keys、passwords 或 personally identifiable information。

如果用户传入了 arguments，把它们视为下一次 session 重点的描述，并据此调整文档。
