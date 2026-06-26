#!/bin/bash
# Veritas Memory — Initialize memory system for an agent
# Usage: ./init-memory.sh [agent-name]

set -e

AGENT="${1:-agent}"
WORKDIR="${PWD}"

echo "🧠 Veritas Memory — Initializing for $AGENT"
echo "   Workspace: $WORKDIR"
echo ""

# 1. Create directory structure
mkdir -p memory/{knowledge,decisions,lessons,checkpoints,archive}
echo "✓ Created memory/ directory structure"

# 2. Create STATE.md if not exists
if [ ! -f "STATE.md" ]; then
  cat > STATE.md << STATEEOF
# $AGENT 的状态

> 最后更新: $(date '+%Y-%m-%d %H:%M') CST
> ⚠️ 本文件是日志的缓存。如有疑问，回溯日志。

---

## 事件时间线

### $(date '+%Y-%m-%d')

| 时间 | 谁 | 做了什么 | 来源 |
|------|-----|---------|------|
| $(date '+%H:%M') | 系统 | Veritas Memory 初始化 | — |

---

## 当前综合状态（从时间线推导）

- 记忆体系: Veritas Memory 已初始化 [$(date '+%H:%M')]

---

## 禁止重做

| 事项 | 原因 | 来源 |
|------|------|------|
| — | — | — |

---

## 未完成的长期事项

- 无
STATEEOF
  echo "✓ Created STATE.md"
else
  echo "• STATE.md already exists"
fi

# 3. Create MEMORY.md if not exists
if [ ! -f "MEMORY.md" ]; then
  cat > MEMORY.md << MEMEOF
# $AGENT 的长期记忆

> 最后整理: $(date '+%Y-%m-%d') | Veritas Memory v1

## 身份
[Agent 身份描述]

## 关键信息
[服务器、通信方式、关键配置]

## 记忆体系
- STATE.md 替换 SESSION_HANDOFF.md — 事件时间线 + 当前状态 + 禁止重做
- 日志为 ground truth，STATE.md 为缓存
- 双向验证回路
- Memory Tender 子 agent 定期维护

## 用户决策记录
[按时间倒序的关键决策]

## 关键教训
详见: memory/lessons/README.md
MEMEOF
  echo "✓ Created MEMORY.md"
else
  echo "• MEMORY.md already exists"
fi

# 4. Create lessons README
if [ ! -f "memory/lessons/README.md" ]; then
  cat > memory/lessons/README.md << LESSONEOF
# 血泪教训

## [日期] — [教训标题]
[发生了什么、为什么、怎么避免]
LESSONEOF
  echo "✓ Created memory/lessons/README.md"
fi

# 5. Create today's daily note
TODAY="memory/$(date '+%Y-%m-%d').md"
if [ ! -f "$TODAY" ]; then
  cat > "$TODAY" << DAILYEOF
# $(date '+%Y-%m-%d')

## 当前状态
- Veritas Memory 已初始化

## 事件
- $(date '+%H:%M') | 系统 | 记忆体系初始化
DAILYEOF
  echo "✓ Created $TODAY"
else
  echo "• $TODAY already exists"
fi

echo ""
echo "🎉 Veritas Memory initialized for $AGENT"
echo ""
echo "Next: Update AGENTS.md startup protocol to read STATE.md"
