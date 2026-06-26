---
name: secretary-memory
description: "秘书式记忆系统 - 会话自动摘要与跨会话召回"
metadata:
  { "openclaw": { "emoji": "📝", "events": ["session:compact:before", "session:compact:after", "message:sent"], "requires": { "bins": ["node", "python3"] } } }
---

# Secretary Memory Hook

在会话压缩前后以及每次消息发送后自动运行秘书记忆系统的脚本。

## 触发时机

| 事件 | 触发 |
|------|------|
| `session:compact:before` | 确保根目录 md 文件已迁移到分区 + 生成摘要 |
| `session:compact:after` | 运行 `context_loader.py` 加载上下文 |
| `message:sent` | 增量记录回复内容到日志（轻量级，不跑LLM）|

## 自动修复索引遗漏

每次 `session:compact:before` 触发时，会自动检查 `memory/` 根目录下的 md 文件：
- 发现游离的 md 文件 → 自动迁移到 `projects/` 分区
- 迁移后自动重建 FTS5 索引

这修复了 v3.0 的索引遗漏问题（根目录文件不会被索引）

## 增量记录说明

`message:sent` 触发时，会将回复内容追加到当天的增量日志文件：
- 路径：`memory/daily/.增量日志_{session_key}.mdl`
- 格式：`时间戳 | 内容（截取前200字）`
- 不会触发 LLM，只有 compact 时才生成正式摘要

## 依赖脚本

- `/root/.openclaw/workspace/skills/secretary-memory/scripts/session_summary.py` — 功能3：会话自动摘要
- `/root/.openclaw/workspace/skills/secretary-memory/scripts/profile_miner.py` — 功能4：偏好提取（暂禁用）
- `/root/.openclaw/workspace/skills/secretary-memory/scripts/context_loader.py` — 功能8：跨会话召回
- `/root/.openclaw/workspace/skills/secretary-memory/scripts/fts5_index.py` — FTS5 索引管理
