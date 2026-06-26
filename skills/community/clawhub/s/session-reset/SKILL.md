---
name: session-reset
description: 安全地重置 OpenClaw agent sessions，支持备份、预览、恢复和批量操作。用于：1) 清理过期的 agent 会话上下文，2) 重置特定 agents 的 session，3) 批量重置六部/秘书 sessions，4) 查看和恢复历史备份。当用户需要"reset session"、"清理 session"、"重置 agents"或"清理上下文"时使用此 skill。
---

# Session Reset

安全地管理 OpenClaw agent sessions，支持一键重置、自动备份和恢复功能。

## Overview

此 skill 提供安全的 session 重置功能，适用于以下场景：
- 批量清理 agents 的过期会话上下文
- 重置特定 agents 以应用新的 SOUL.md 配置
- 定期维护，释放磁盘空间
- 从备份恢复误删的 sessions

## 快速开始

### 首次使用（初始化）

```bash
# 运行初始化，交互式选择默认 agents
openclaw session-reset --init
```

初始化流程：
1. 自动发现所有 agents
2. 选择导入方式：[1]全部导入 / [2]多选 / [3]取消
3. 保存配置到 `~/.openclaw/session-reset-config.json`

### 日常使用

```bash
# 预览将要重置的内容
openclaw session-reset --scope default --dry-run

# 确认无误后执行重置
openclaw session-reset --scope default

# 重置配置的默认 agents
openclaw session-reset --scope agents
```

## 工作流程

```
首次使用:
  reset-session --init
    → 发现 agents
    → 选择导入方式
    → 保存配置

日常使用:
  1. 选择 scope → 确定重置范围 (default/all/agents/cron/subagent/agent1,agent2)
  2. 预览/确认 → 使用 --dry-run 预览，或直接执行
  3. 自动备份 → 创建带时间戳的备份到 ~/.openclaw/session-backups/
  4. 执行重置 → 删除 session JSONL 文件
  5. 自动重建 → 下次消息触发时 OpenClaw 自动创建新 session
```

## 命令参考

### 初始化命令

```bash
# 首次使用 - 初始化配置
openclaw session-reset --init
```

### 基本命令

```bash
# 重置所有 Discord 频道 sessions（默认，不含 Cron/Subagent）
openclaw session-reset --scope default

# 预览模式（不执行实际重置）
openclaw session-reset --scope default --dry-run

# 重置配置的默认 agents（需先初始化）
openclaw session-reset --scope agents

# 重置指定 agents
openclaw session-reset --scope main,hubu,libu

# 重置所有 sessions（含 Cron + Subagent）
openclaw session-reset --scope all

# 仅重置 Cron 任务
openclaw session-reset --scope cron

# 仅重置 Subagent
openclaw session-reset --scope subagent
```

### 备份管理

```bash
# 查看所有备份
openclaw session-reset --list-backups

# 从指定备份恢复
openclaw session-reset --restore 20250305_143022

# 清理旧备份（默认：30天前，最多保留10个）
openclaw session-reset --cleanup

# 自定义清理策略
openclaw session-reset --cleanup --cleanup-days 7 --cleanup-max 5
```

### 高级选项

```bash
# 强制执行，跳过确认提示
openclaw session-reset --scope default --force
```

## Scope 参数详解

| Scope 值 | 说明 | 适用场景 | 是否需要初始化 |
|----------|------|----------|----------------|
| `default` | 所有 Discord 频道 sessions | 日常清理，最常用的选项 | 否 |
| `all` | 全部 sessions | 彻底重置，包含所有类型 | 否 |
| `agents` | 配置的默认 agents | 批量重置常用 agents | ✅ 需要 `--init` |
| `cron` | 仅 Cron 任务 sessions | 重置定时任务状态 | 否 |
| `subagent` | 仅 Subagent sessions | 清理子代理会话 | 否 |
| `agent1,agent2` | 指定 agents（逗号分隔） | 精确控制重置范围 | 否 |

**注意**: `--scope agents` 需要事先运行 `--init` 配置默认 agents。

## 安全机制

1. **强制备份**
   - 任何重置操作前自动创建备份
   - 备份位置：`~/.openclaw/session-backups/YYYYMMDD_HHMMSS/`
   - 包含完整的 session JSONL 文件和清单

2. **二次确认**
   - 显示统计信息（agents数量、文件数、预估大小）
   - 需输入 `yes` 确认后执行

3. **预览模式**
   - `--dry-run` 仅显示将要重置的内容
   - 不产生任何实际影响

4. **可恢复性**
   - 支持 `--restore <timestamp>` 恢复到任意备份
   - 备份永久保留，直到手动清理

## 备份策略

- **默认保留**: 30 天内 + 最多 10 个备份
- **清理命令**: `openclaw session-reset --cleanup`
- **自定义**: `--cleanup-days N --cleanup-max M`

## 注意事项

- 重置后 agents 会丢失当前会话上下文
- 下次收到消息时会自动创建新的 session
- 建议在低峰期执行批量重置
- 重要操作前使用 `--dry-run` 预览
- 无法重置当前正在运行的 session（需从外部终端执行）

## 使用示例

### 示例 1：首次使用（初始化）
```bash
# 运行初始化，选择默认 agents
openclaw session-reset --init

# 输出示例：
# ✓ 发现 7 个 agents:
#   1. main         (5 sessions)
#   2. hubu         (3 sessions)
#   ...
#
# 选择导入方式:
#   1. 导入全部 agents
#   2. 多选 agents
#   3. 取消初始化
```

### 示例 2：日常维护
```bash
# 预览将要清理的内容
openclaw session-reset --scope default --dry-run

# 确认无误后执行
openclaw session-reset --scope default
```

### 示例 3：批量重置配置的 agents
```bash
# 重置初始化时配置的默认 agents
openclaw session-reset --scope agents --dry-run
openclaw session-reset --scope agents
```

### 示例 4：恢复备份
```bash
# 查看可用备份
openclaw session-reset --list-backups

# 恢复到指定时间点
openclaw session-reset --restore 20250305_143022
```

## Resources

### scripts/

- `reset-session.py` - 核心脚本，实现 session 重置、备份、恢复功能
