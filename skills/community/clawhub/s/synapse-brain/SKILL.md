---
name: synapse-brain
description: >
  Synapse Brain — OpenClaw 持久调度 Agent。
  基于 Managed Agents 架构，提供跨 Session 的任务管理、子代理调度、
  状态持久化和知识互操作能力。是 synapse-code 和 synapse-wiki 的调度核心。
  当用户提到任务调度、跨会话管理、多 Agent 协作、长期项目跟踪时使用此技能。
version: 2.0.1
date: 2026-04-11
user-invocable: true
metadata:
  openclaw:
    emoji: "🧬"
    requires:
      bins: ["python3"]
      python_min: "3.10"
    install: []
    homepage: "https://github.com/ankechenlab-node/synapse-brain"
tags: [multi-agent, orchestrator, session-management, task-routing, brain-agent]
---

# Synapse Brain Skill

**Synapse Brain = 持久调度 + 跨会话状态 + 子代理编排**

核心理念：AI Agent 应该是持久的"大脑"，而非每次从零开始的无状态会话。

| | 传统 Agent | Synapse Brain |
|--|------------|---------------|
| **会话** | 每次从零开始 | 状态持久化，醒来即恢复 |
| **调度** | 手动调用子代理 | 自动路由、分配、追踪 |
| **记忆** | 随会话消失 | state.json 持久化 |
| **协作** | 独立工作 | 调度 code/wiki 等 Skills |

---

## 🚦 快速决策：我该用什么？

```
你想做什么？
│
├─ 启动/恢复项目任务     → init（初始化 session）
│   └─ 例："继续做用户系统"、"开始新项目 X"
│
├─ 分配子任务给子代理    → dispatch（调度执行）
│   └─ 例："并行开发登录和注册"、"让 dev 实现导出"
│
├─ 查询任务状态           → status（状态查询）
│   └─ 例："现在进度如何？"、"昨天那个任务完成了没"
│
└─ 保存/恢复会话          → save/restore（状态管理）
    └─ 例："保存当前进度"、"恢复上次会话"
```

---

## 📋 命令速查卡片

| 命令 | 用途 | 示例 |
|------|------|------|
| `/synapse-brain init` | 初始化/恢复项目 session | `/synapse-brain init my-project "用户系统"` |
| `/synapse-brain dispatch` | 分发任务到子代理 | `/synapse-brain dispatch "并行开发 A 和 B"` |
| `/synapse-brain status` | 查询任务/子代理状态 | `/synapse-brain status my-project` |
| `/synapse-brain save` | 保存当前会话状态 | `/synapse-brain save` |
| `/synapse-brain restore` | 恢复上次会话 | `/synapse-brain restore` |

---

## Brain Agent 架构

```
用户请求
    ↓
┌─────────────────────────────┐
│  Synapse Brain (持久调度)     │
│                             │
│  1. Session Restore          │ ← state.json 恢复上下文
│  2. Intent Classification    │ ← 识别意图类型
│  3. Task Routing             │ ← 路由到合适 Skill/Agent
│  4. Subagent Dispatch        │ ← 调用 OpenClaw 子代理
│  5. Result Aggregation       │ ← 汇总结果
│  6. State Persist            │ ← 保存状态到 state.json
└─────────────┬───────────────┘
              ↓
    ┌─────────┼─────────┐
    ↓         ↓         ↓
synapse-  synapse-  专业子代理
  code      wiki    (dev/qa/arch)
```

---

## Session 持久化

Brain 通过 `state.json` 维护跨会话状态：

```json
{
  "session_id": "sess_20260410_001",
  "project": "my-project",
  "created_at": "2026-04-10T12:00:00Z",
  "updated_at": "2026-04-10T14:30:00Z",
  "tasks": [
    {
      "id": "task-001",
      "title": "用户登录功能",
      "status": "completed",
      "skill": "synapse-code",
      "mode": "lite",
      "agents_used": ["req-analyst", "developer", "qa-engineer"]
    },
    {
      "id": "task-002",
      "title": "用户注册功能",
      "status": "in_progress",
      "skill": "synapse-code",
      "mode": "lite",
      "stage": "DEV"
    }
  ],
  "subagents": {
    "active": 1,
    "completed": 3,
    "failed": 0
  },
  "knowledge": {
    "wiki_initialized": true,
    "wiki_root": "~/my-project/wiki",
    "last_ingest": "2026-04-10T13:00:00Z"
  }
}
```

---

## 子代理调度策略

Brain 根据任务特征自动选择调度策略：

| 策略 | 触发条件 | 行为 |
|------|---------|------|
| **sequential** | 任务有依赖关系 | 依次执行子代理 |
| **parallel** | 任务独立可并行 | 同时派发最多 8 个子代理 |
| **pipeline** | 标准开发流程 | REQ→ARCH→DEV→INT→QA→DEPLOY |
| **standalone** | 简单任务 | Brain 直接完成，不调子代理 |

---

## 与 synapse-code 互操作

```bash
# Brain 调度 code 执行开发任务
/synapse-brain dispatch "实现用户登录" --skill synapse-code --mode lite

# 等价于
/synapse-code run my-project "实现用户登录" --mode lite
```

Brain 会：
1. 自动记录任务到 session state
2. 调用 synapse-code 执行
3. 接收结果并更新任务状态
4. 触发 wiki 知识沉淀

---

## 与 synapse-wiki 互操作

```bash
# Brain 查询已有知识
/synapse-brain query "RAG 是什么？" --skill synapse-wiki

# Brain 保存新资料
/synapse-brain ingest ~/raw/article.md --skill synapse-wiki
```

Brain 会：
1. 检查 wiki 是否初始化
2. 调用 synapse-wiki 对应命令
3. 更新知识索引到 session state

---

## Scripts

| 脚本 | 用途 |
|------|------|
| `scripts/state_manager.py` | Session 状态持久化（CRUD） |
| `scripts/task_router.py` | 意图识别 + 任务路由 |
| `scripts/session_init.py` | 新 session 初始化 |
| `scripts/subagent_dispatch.py` | 子代理并行调度 |

---

## 安装

```bash
# 方式 1: 从源码安装（推荐）
git clone https://github.com/ankechenlab-node/synapse-brain.git
cd synapse-brain
./install.sh

# 方式 2: OpenClaw (从 ClawHub)
npx clawhub install synapse-brain

# 方式 3: 手动复制
cp -r synapse-brain ~/.openclaw/skills/
```

## 配置

Brain 需要与 synapse-code 和 synapse-wiki 配合使用：

```json
{
  "brain": {
    "state_dir": "~/.openclaw/brain-state",
    "auto_save": true,
    "auto_save_interval": 300,
    "skills": {
      "code": "synapse-code",
      "wiki": "synapse-wiki"
    }
  }
}
```

---

## 使用场景

- 🧠 **长期项目管理** — 跨多个 Session 追踪进度
- 🔄 **复杂任务编排** — 自动调度多个子代理协作
- 📊 **状态可视化** — 随时查询项目进展
- 🤝 **Skill 互操作** — code 和 wiki 的统一入口
- 💾 **会话持久化** — 每次醒来即恢复上下文
