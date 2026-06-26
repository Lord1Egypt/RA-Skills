# Redis Memory System v3.3.0

Fully automatic cross-session short-term memory system. Single script, config-driven, semantic tag index.

全自动跨会话短期记忆系统。单脚本 + 配置驱动 + 语义标签索引。

## 适配环境 / Requirements

| 项目 / Item | 规格 / Spec |
|-------------|-------------|
| 实例 / Instance | 任意（Redis 占用 < 50MB） |
| Redis | 单机模式 / Standalone |
| Agent | OpenClaw |

## 一键安装 / Quick Install

```bash
chmod +x scripts/setup.sh
bash scripts/setup.sh
```

## 用法 / Usage

```bash
# Sync dialogue to Redis (for cron)  · 同步对话到 Redis（给 cron 用）
bash scripts/memory.sh sync

# Read recent memory (last 3 days)  · 查最近 3 天记忆
bash scripts/memory.sh get <user>

# Read memory for N days  · 查最近 N 天记忆
bash scripts/memory.sh get <user> 7

# Read memory for a specific date  · 查指定日期记忆
bash scripts/memory.sh get <user> 2026-05-26

# Search by semantic tags  · 按语义标签搜索
bash scripts/memory.sh search <keyword>

# Manually write summary  · 手动写入摘要
bash scripts/memory.sh set <user> 2026-05-26 "Summary text"

# System overview  · 系统状态
bash scripts/memory.sh stats

# Redis connection check  · 检查 Redis 连通性
bash scripts/memory.sh ping
```

## 语义标签索引 / Semantic Tags (v3.3.0)

- LLM 自动为每日摘要提取 5 个概念级标签 / LLM auto-extracts 5 concept-level tags per day
- 倒排索引 `tagidx:<tag>` → 日期集合 / Inverted index for cross-date lookup
- Redis SINTER 支持 O(1) 多标签交集查询 / O(1) multi-tag intersection queries
- 零额外内存，不用 embedding 模型 / Zero extra memory, no embedding model needed
