# 多 Agent 支持说明

## 概述

Self-Evolution-CN 支持多个 agent 共享学习目录，所有 agent 的学习记录存储在共享目录中，并按 `Pattern-Key` 累计 `Recurrence-Count`。

## 共享目录结构

```
/root/.openclaw/shared-learning/     # 共享目录
├── ERRORS.md                       # 所有 agent 共享
├── LEARNINGS.md                    # 所有 agent 共享
└── FEATURE_REQUESTS.md             # 所有 agent 共享

/root/.openclaw/workspace-agent1/.learnings  # 软链接 → 共享目录
/root/.openclaw/workspace-agent2/.learnings  # 软链接 → 共享目录
/root/.openclaw/workspace-agent3/.learnings  # 独立目录（可选）
```

## 配置

详见 `SKILL.md` 快速开始部分。

## 统计逻辑

### 按 Pattern-Key 累计

所有 agent 的记录按 `Pattern-Key` 累计 `Recurrence-Count`，累计次数 >= 3 时自动提升到 SOUL.md。

### 提升判断

- 累计次数 >= 3 时自动提升到 SOUL.md
- Agent 字段仅用于追溯，不影响提升判断

## 脚本支持

### daily_review.sh

自动统计与提升脚本，每日 00:00 自动执行。

```bash
# 手动执行
./scripts/daily_review.sh
```

**功能：**
- 自动统计所有记录的重复次数
- 自动提升到 SOUL.md
- 共享目录：所有使用共享目录的智能体都提升
- 独立目录：对应智能体提升到自己的 SOUL.md

### trigger-daily-review.sh

Cron 触发脚本，每日 00:00 自动执行。

```bash
# 添加到 crontab
0 0 * * * /path/to/scripts/trigger-daily-review.sh
```

## 环境变量

| 变量 | 说明 | 默认值 |
|------|------|--------|
| `SHARED_LEARNING_DIR` | 共享学习目录路径 | `/root/.openclaw/shared-learning` |
| `SHARED_AGENTS` | 需要共享学习目录的 agent 列表 | `agent1` |
| `AGENT_ID` | 当前 agent ID | `main` |
| `AUTO_PROMOTE_ENABLED` | 是否启用自动提升 | `true` |

### 控制自动提升

```bash
# 禁用自动提升（仅统计）
export AUTO_PROMOTE_ENABLED=false

# 启用自动提升（默认）
export AUTO_PROMOTE_ENABLED=true
```

## 执行状态和日志

### 状态文件

**位置**：`$SHARED_LEARNING_DIR/heartbeat-state.json`

**查看状态：**
```bash
cat $SHARED_LEARNING_DIR/heartbeat-state.json
jq '.agents.agent1' $SHARED_LEARNING_DIR/heartbeat-state.json
```

### 日志文件

**位置**：`$SHARED_LEARNING_DIR/logs/heartbeat-daily.log`

**查看日志：**
```bash
tail -f $SHARED_LEARNING_DIR/logs/heartbeat-daily.log
grep 'Processing agent: agent1' $SHARED_LEARNING_DIR/logs/heartbeat-daily.log
```
