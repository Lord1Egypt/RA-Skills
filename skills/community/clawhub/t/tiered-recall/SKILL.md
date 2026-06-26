---
name: tiered-recall
version: 1.2.2
description: 分层回忆系统，解决上下文长度限制，保持项目延续性。默认自动加载最近7天记忆，支持手动全量回忆、自定义天数、项目回忆和主题回忆。当前版本采用 slim index，只保留文件名、行号和标题，不存摘要，避免 token 膨胀。
license: MIT
author: davidme6
homepage: https://github.com/davidme6/tiered-recall
repository: https://github.com/davidme6/tiered-recall
keywords: [memory, recall, context, session, continuity]
changelog: "v1.2.2: 自动7天 + 手动全量/自定义天数 + slim index。v1.2.0: 修复索引 token 膨胀。v1.1.0: 增加10字摘要。v1.0.0: 初始版本。"
---

# Tiered Recall

Tiered Recall 是一套给 AI 助手使用的分层回忆系统，用来解决跨会话后的上下文恢复问题。

## 核心目标

- 保留长期核心记忆
- 自动恢复最近 7 天上下文
- 识别活跃项目
- 用低成本索引支持更深层的回忆

## 自动加载

默认新 session 会依次加载：
1. `MEMORY.md`
2. 最近 7 天日志
3. 活跃项目
4. 记忆索引

## 手动回忆

支持的典型触发：
- `回忆全部`
- `回忆最近14天`
- `回忆 [项目名]`
- `回忆 [日期]`
- `回忆 [关键词]`

## 脚本

```bash
# 重建索引
python skills/tiered-recall/scripts/build-index.py

# 默认加载（最近7天）
python skills/tiered-recall/scripts/load.py

# 全量加载
python skills/tiered-recall/scripts/load.py --full

# 自定义天数
python skills/tiered-recall/scripts/load.py --days 14
```

## 索引策略

当前版本使用 slim index。

索引条目只保留：
- 文件名 `f`
- 行号 `l`
- 标题 `t`

不再写入摘要字段，避免索引膨胀。

## 与 Jarvis Core 协作

本技能是 `jarvis-core` 的依赖项。

当 `jarvis-core` 需要在新会话里恢复用户状态、项目连续性和关系上下文时，可以自动调用本技能作为记忆加载层。

## 当前版本

### v1.2.2
- 自动 7 天加载
- 手动全量 / 自定义天数
- slim index
- 适合作为 `jarvis-core` 的稳定依赖版本
