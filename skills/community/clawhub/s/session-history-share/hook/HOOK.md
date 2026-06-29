---
name: session-history-share
description: "Inject previous session history into bootstrap"
metadata:
  { "openclaw": { "events": ["agent:bootstrap"] } }
---

# Session History Share

在每轮对话开始时，自动将旧 Session 的压缩摘要注入上下文。

## 逻辑
1. 从 event 获取 sessionKey 和 bootstrapFiles
2. 读取 `.session_history/<safeSessionKey>/` 下最新存档
3. 有内容则 push 到 bootstrapFiles（name 使用 `BOOTSTRAP.md`）

## 存档路径
- `.session_history/<safeSessionKey>/`
- safeSessionKey = sessionKey 中的冒号替换为下划线
