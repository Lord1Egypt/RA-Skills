---
name: quick-note-capture
description: 快速记录一条笔记到本地文件，支持标签和时间戳，适合随手记录想法、待办和参考资料。
metadata:
  openclaw:
    emoji: "📝"
    tags:
      - notes
      - productivity
      - capture
---

# quick-note-capture

把一句话笔记追加到 `~/notes/inbox.md`，自动加上 ISO 时间戳和可选标签。

## 使用

调用方（插件或脚本）只需传入 `text`，可选 `tags`：

```bash
node scripts/capture.mjs --text "记得回 Sarah 的邮件" --tags work,followup
```

## 输出

- 文件路径：`~/notes/inbox.md`
- 追加格式：`- [2026-09-22T00:29:00Z] #work #followup 记得回 Sarah 的邮件`

## 前置条件

- Node.js ≥ 18
- 可写的 `~/notes/` 目录
