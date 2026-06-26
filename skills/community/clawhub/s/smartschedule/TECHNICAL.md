# 自动化智能日程管理系统 — 技术文档

> 本文档详细说明系统的技术架构、OpenClaw 与 Python 模块的交互机制、
> 各组件的工作流程，以及关键算法的实现原理。

---

## 目录

1. [系统总体架构](#1-系统总体架构)
2. [OpenClaw 平台核心概念](#2-openclaw-平台核心概念)
3. [OpenClaw 如何调用 Python 函数](#3-openclaw-如何调用-python-函数)
4. [工作流程详解](#4-工作流程详解)
   - 4.1 [用户交互流程（添加日程）](#41-用户交互流程添加日程)
   - 4.2 [冲突检测与建议流程](#42-冲突检测与建议流程)
   - 4.3 [模糊指令处理流程](#43-模糊指令处理流程)
   - 4.4 [邮件汇总定时任务流程](#44-邮件汇总定时任务流程)
   - 4.5 [钉钉即时提醒流程](#45-钉钉即时提醒流程)
5. [数据持久化设计](#5-数据持久化设计)
6. [关键算法说明](#6-关键算法说明)
7. [文件结构与职责](#7-文件结构与职责)
8. [安全与异常处理](#8-安全与异常处理)

---

## 1. 系统总体架构

系统分为四层，自上而下依次为：

```
┌─────────────────────────────────────────────────┐
│              用户层（钉钉私聊 / Web）              │
│  "明天下午2点开组会" ──────────────────────────►   │
└──────────────────────┬──────────────────────────┘
                       │ 自然语言消息
                       ▼
┌─────────────────────────────────────────────────┐
│          OpenClaw Gateway（端口 12463）           │
│                                                   │
│  ┌───────────────┐  ┌──────────────────────┐     │
│  │ 钉钉连接器插件 │  │ OpenClaw Agent (LLM) │     │
│  │ (消息收发通道)  │  │ (意图理解 + 工具调用)  │     │
│  └───────────────┘  └──────────┬───────────┘     │
│                                │                   │
│  ┌──────────────┐   ┌─────────┴────────┐         │
│  │ Cron 定时引擎 │   │ Skill 技能系统    │         │
│  │ (周期性任务)   │   │ (SKILL.md 行为规范)│         │
│  └──────────────┘   └──────────────────┘         │
└──────────────────────┬──────────────────────────┘
                       │ exec 工具调用
                       ▼
┌─────────────────────────────────────────────────┐
│             Python 日程管理模块                    │
│                                                   │
│  schedule_manager.py   ←── CRUD / 冲突检测        │
│  email_summary.py      ←── 邮件汇总               │
│  check_upcoming.py     ←── 即将到期检查            │
└──────────────────────┬──────────────────────────┘
                       │ SQL 读写
                       ▼
┌─────────────────────────────────────────────────┐
│           SQLite 数据库 (schedules.db)            │
└─────────────────────────────────────────────────┘
```

---

## 2. OpenClaw 平台核心概念

理解以下概念是理解整个工作流程的前提：

### 2.1 Gateway

OpenClaw Gateway 是一个运行在服务器上的后台服务（端口 12463），负责：
- 接收来自各通道（钉钉、QQ、Web 等）的用户消息
- 将消息路由到 Agent 处理
- 管理 Cron 定时任务
- 维护会话状态

### 2.2 Agent

Agent 是 OpenClaw 的核心——一个由大语言模型（本系统使用通义千问 `qwen3.5-plus`）驱动的 AI 助手。Agent 的特点：

- **有工具调用能力**：Agent 不只是聊天，它可以调用 `exec`（执行命令）、`read`（读文件）、`edit`（改文件）、`message`（发消息）等工具
- **有 Skill（技能）指引**：通过 SKILL.md 文件告诉 Agent 面对特定任务应该如何操作
- **有持久化记忆**：通过工作区文件（MEMORY.md 等）在会话间保持连续性

### 2.3 Skill（技能）

Skill 是一个 Markdown 文件（`SKILL.md`），放在工作区的 `skills/` 目录下。它的作用是**教会 Agent 如何完成特定任务**。

Agent 在启动时会扫描所有 Skill，当用户的请求匹配某个 Skill 时，Agent 会读取该 SKILL.md 并按照其中的指引操作。

本系统的 Skill 文件是 `skills/schedule-manager/SKILL.md`，其中定义了：
- 可用的 Python 命令及参数格式
- 添加/修改/删除/查询日程的操作步骤
- 模糊指令的解析策略
- Cron 定时任务的注册模板

### 2.4 Cron（定时任务）

OpenClaw 内置了 Cron 引擎，可以注册周期性或一次性的定时任务。Cron 任务有两种执行模式：

| 模式 | payload.kind | 用途 |
|------|-------------|------|
| `systemEvent` | 向主会话注入提示 | 需要 Agent 在对话中响应 |
| `agentTurn` | 生成隔离子会话自主执行 | 后台任务，不干扰主对话 |

本系统的邮件汇总和钉钉提醒都使用 `agentTurn` + `sessionTarget: "isolated"` 模式，在后台自主执行，不占用用户的对话窗口。

### 2.5 Channel（通道）

通道是 Agent 与外部世界通信的桥梁。本系统涉及的通道：
- `dingtalk-connector`：钉钉机器人插件，负责接收/发送钉钉消息
- SMTP：通过 Python `smtplib` 直接发邮件（不经过 OpenClaw 通道）

---

## 3. OpenClaw 如何调用 Python 函数

这是整个系统最关键的机制。OpenClaw Agent（LLM）本身不能直接运行 Python，
它通过 **`exec` 工具** 间接执行。完整链路如下：

```
用户消息: "帮我添加明天下午2点的组会"
    │
    ▼
┌───────────────────────────────────────────────────┐
│ Step 1: LLM 意图理解                                │
│                                                     │
│ Agent 收到消息后，结合 SKILL.md 的指引，理解到：       │
│   - 操作类型：添加日程                                │
│   - 标题：组会                                       │
│   - 开始时间：明天 14:00                              │
│   - 结束时间：明天 15:00（未指定，默认+1小时）          │
└───────────────────────┬───────────────────────────┘
                        │
                        ▼
┌───────────────────────────────────────────────────┐
│ Step 2: Agent 决定调用 exec 工具                     │
│                                                     │
│ Agent 生成一个工具调用请求（tool_call）：              │
│                                                     │
│   工具名: exec                                       │
│   参数: {                                            │
│     "command": "python3",                            │
│     "args": [                                        │
│       "schedule/schedule_manager.py",                │
│       "add",                                         │
│       "{\"title\":\"组会\",                           │
│         \"start_time\":\"2026-04-07 14:00\",         │
│         \"end_time\":\"2026-04-07 15:00\"}"          │
│     ]                                                │
│   }                                                  │
│                                                     │
│ 注意：Agent 自动把"明天下午2点"转换成了精确的          │
│ "2026-04-07 14:00" 格式，这是 LLM 的推理能力。       │
└───────────────────────┬───────────────────────────┘
                        │
                        ▼
┌───────────────────────────────────────────────────┐
│ Step 3: Gateway 执行命令                             │
│                                                     │
│ OpenClaw Gateway 在服务器上实际执行 shell 命令：       │
│                                                     │
│   $ python3 schedule/schedule_manager.py add \       │
│     '{"title":"组会","start_time":"2026-04-07 14:00",│
│       "end_time":"2026-04-07 15:00"}'                │
│                                                     │
│ 工作目录：~/.openclaw/workspace/                     │
└───────────────────────┬───────────────────────────┘
                        │
                        ▼
┌───────────────────────────────────────────────────┐
│ Step 4: Python 脚本执行                              │
│                                                     │
│ schedule_manager.py 的 main() 函数被调用：            │
│   1. 解析命令行参数: cmd="add", args={...}           │
│   2. 调用 add_schedule() 函数                        │
│   3. add_schedule() 内部先调用 check_conflict()       │
│      检查时间冲突                                    │
│   4. 执行 SQL INSERT 写入 SQLite 数据库               │
│   5. 将结果（新日程 + 冲突列表）序列化为 JSON          │
│   6. print() 输出到 stdout                           │
│                                                     │
│ 输出示例:                                            │
│   {                                                  │
│     "schedule": {"id": 1, "title": "组会", ...},     │
│     "conflicts": []                                  │
│   }                                                  │
└───────────────────────┬───────────────────────────┘
                        │
                        ▼
┌───────────────────────────────────────────────────┐
│ Step 5: Agent 解读结果并回复用户                      │
│                                                     │
│ exec 工具把 Python 脚本的 stdout 返回给 Agent。       │
│ Agent 读取 JSON 结果：                                │
│   - conflicts 为空 → 没有冲突                        │
│   - schedule.id = 1 → 日程创建成功                   │
│                                                     │
│ Agent 生成自然语言回复：                              │
│   "📅 已添加日程：组会                                │
│    时间：2026-04-07 14:00 ~ 15:00                    │
│    添加成功，没有时间冲突！"                           │
│                                                     │
│ 回复通过钉钉连接器发回给用户。                        │
└───────────────────────────────────────────────────┘
```

### 关键点总结

| 环节 | 谁在做 | 做什么 |
|------|--------|--------|
| 自然语言理解 | LLM（qwen3.5-plus） | 把"明天下午2点"转换为"2026-04-07 14:00" |
| 决定调用什么工具 | LLM + SKILL.md | 根据 Skill 指引选择正确的命令和参数 |
| 执行 shell 命令 | OpenClaw Gateway | 在服务器上运行 `python3 schedule_manager.py ...` |
| 数据库操作 | Python 脚本 | 通过 sqlite3 模块执行 SQL |
| 解读结果 | LLM | 读取 JSON 输出，生成用户友好的回复 |
| 消息投递 | 钉钉连接器插件 | 把 Agent 的回复发送到钉钉 |

**Python 脚本的设计原则**：
- 所有输入通过命令行参数（JSON 字符串）传入
- 所有输出通过 `print()` 输出到 stdout（JSON 格式）
- 脚本本身不做任何消息收发，只负责数据操作
- Agent 是"大脑"，Python 脚本是"手"

---

## 4. 工作流程详解

### 4.1 用户交互流程（添加日程）

```
用户(钉钉)                  OpenClaw Agent                Python 脚本              SQLite
    │                           │                           │                      │
    │  "明天下午2点开组会"       │                           │                      │
    │ ────────────────────────► │                           │                      │
    │                           │                           │                      │
    │                           │ [理解意图]                 │                      │
    │                           │ 标题=组会                  │                      │
    │                           │ 时间=明天14:00~15:00       │                      │
    │                           │                           │                      │
    │                           │  exec: python3             │                      │
    │                           │  schedule_manager.py add   │                      │
    │                           │  '{"title":"组会",...}'     │                      │
    │                           │ ────────────────────────► │                      │
    │                           │                           │                      │
    │                           │                           │ check_conflict()     │
    │                           │                           │ ──────────────────► │
    │                           │                           │ ◄────── 无冲突 ──── │
    │                           │                           │                      │
    │                           │                           │ INSERT INTO          │
    │                           │                           │ schedules ...        │
    │                           │                           │ ──────────────────► │
    │                           │                           │ ◄──── id=1 ──────── │
    │                           │                           │                      │
    │                           │ ◄─── JSON 结果 ────────── │                      │
    │                           │ {"schedule":{...},         │                      │
    │                           │  "conflicts":[]}           │                      │
    │                           │                           │                      │
    │                           │ [生成回复]                 │                      │
    │  "📅 日程已添加: 组会      │                           │                      │
    │   时间: 明天14:00~15:00"  │                           │                      │
    │ ◄──────────────────────── │                           │                      │
```

### 4.2 冲突检测与建议流程

当新日程与已有日程时间重叠时，Agent 会进行多轮工具调用：

```
用户(钉钉)                  OpenClaw Agent                Python 脚本
    │                           │                           │
    │  "明天3点开论文研讨"       │                           │
    │ ────────────────────────► │                           │
    │                           │                           │
    │                           │ exec: add                 │
    │                           │ ────────────────────────► │
    │                           │                           │
    │                           │ ◄── JSON ─────────────── │
    │                           │ conflicts: [{组会,         │
    │                           │   14:00~15:30}]            │
    │                           │                           │
    │                           │ [发现冲突! 需要建议]        │
    │                           │                           │
    │                           │ exec: suggest              │
    │                           │ ────────────────────────► │
    │                           │                           │
    │                           │ ◄── JSON ─────────────── │
    │                           │ [{后移, 15:30~16:30},      │
    │                           │  {前移, 13:00~14:00}]      │
    │                           │                           │
    │  "⚠️ 与组会(14:00~15:30)  │                           │
    │   冲突！建议：             │                           │
    │   1. 后移至15:30~16:30    │                           │
    │   2. 前移至13:00~14:00    │                           │
    │   选哪个？"               │                           │
    │ ◄──────────────────────── │                           │
    │                           │                           │
    │  "选1"                    │                           │
    │ ────────────────────────► │                           │
    │                           │                           │
    │                           │ exec: update id=新日程     │
    │                           │ start=15:30 end=16:30     │
    │                           │ ────────────────────────► │
    │                           │                           │
    │  "✅ 已调整至15:30~16:30" │                           │
    │ ◄──────────────────────── │                           │
```

**冲突检测的 SQL 核心逻辑**（schedule_manager.py 第 158-168 行）：

```sql
SELECT * FROM schedules
WHERE start_time < '新日程结束时间'
  AND end_time > '新日程开始时间'
```

两个时间段 A 和 B 冲突的充要条件是：`A.start < B.end AND A.end > B.start`。
这比分别判断"A包含B"、"B包含A"、"部分重叠"要简洁得多。

### 4.3 模糊指令处理流程

模糊指令（如"把明天的组会往后挪一小时"）的处理完全依赖 LLM 的推理能力，
SKILL.md 提供了策略指引：

```
用户(钉钉)                  OpenClaw Agent                Python 脚本
    │                           │                           │
    │  "把明天的组会往后         │                           │
    │   挪一小时"               │                           │
    │ ────────────────────────► │                           │
    │                           │                           │
    │                           │ [意图分析]                 │
    │                           │ 1. 操作=修改时间            │
    │                           │ 2. 目标=明天的"组会"        │
    │                           │ 3. 方式=往后挪一小时        │
    │                           │                           │
    │                           │ [先搜索目标日程]            │
    │                           │ exec: search               │
    │                           │ '{"keyword":"组会"}'        │
    │                           │ ────────────────────────► │
    │                           │                           │
    │                           │ ◄── [{id:1, 组会,          │
    │                           │   14:00~15:30}] ────────── │
    │                           │                           │
    │                           │ [只有一条匹配，无歧义]      │
    │                           │ [计算新时间]                │
    │                           │ 14:00+1h=15:00             │
    │                           │ 15:30+1h=16:30             │
    │                           │                           │
    │                           │ exec: update id=1          │
    │                           │ start=15:00 end=16:30      │
    │                           │ ────────────────────────► │
    │                           │                           │
    │                           │ ◄── {schedule:{...},       │
    │                           │  conflicts:[]} ──────────  │
    │                           │                           │
    │  "✅ 组会已调整：           │                           │
    │   15:00~16:30（后移1小时）" │                           │
    │ ◄──────────────────────── │                           │
```

**歧义场景**：如果搜索到多条"组会"，Agent 不会猜测，而是列出候选项：

```
找到以下匹配日程：
  1. #3 周一组会 (14:00~15:30)
  2. #7 项目组会 (16:00~17:00)
你想修改哪一个？
```

### 4.4 邮件汇总定时任务流程

邮件汇总由 OpenClaw Cron 引擎驱动，每小时整点自动执行：

```
OpenClaw Cron引擎           隔离子Agent               Python 脚本            SMTP服务器
    │                           │                        │                     │
    │ [每小时整点触发]            │                        │                     │
    │                           │                        │                     │
    │ 创建隔离会话               │                        │                     │
    │ payload.kind=agentTurn    │                        │                     │
    │ ────────────────────────► │                        │                     │
    │                           │                        │                     │
    │                           │ [读取任务指令]           │                     │
    │                           │ "执行 email_summary.py" │                     │
    │                           │                        │                     │
    │                           │ exec: python3           │                     │
    │                           │ email_summary.py        │                     │
    │                           │ ─────────────────────► │                     │
    │                           │                        │                     │
    │                           │                        │ get_upcoming(24h)   │
    │                           │                        │ ──► SQLite ──►      │
    │                           │                        │                     │
    │                           │                        │ build_email()       │
    │                           │                        │ (HTML + 纯文本)      │
    │                           │                        │                     │
    │                           │                        │ send_email()        │
    │                           │                        │ ──────────────────► │
    │                           │                        │                     │
    │                           │                        │ SMTP_SSL连接         │
    │                           │                        │ login(邮箱, 授权码)   │
    │                           │                        │ send_message(邮件)   │
    │                           │                        │ ◄── 发送成功 ─────── │
    │                           │                        │                     │
    │                           │ ◄── {"status":"success"} │                   │
    │                           │                        │                     │
    │ ◄── 任务完成 ──────────── │                        │                     │
```

**email_summary.py 内部流程**：

1. `init_db()` — 确保数据库表存在
2. `load_config()` — 读取 `config.json` 获取 SMTP 配置
3. `get_upcoming(hours=24)` — 查询未来 24 小时的日程
4. `build_email()` — 生成邮件内容（同时包含纯文本和 HTML 版本）
5. `send_email()` — 通过 SMTP_SSL 连接 QQ 邮箱服务器发送

**邮件格式**：HTML 版本包含带样式的卡片式布局，每个日程一个蓝色边框卡片，
包含标题、时间、地点、备注。纯文本版本作为 fallback 提供相同信息。

### 4.5 钉钉即时提醒流程

钉钉提醒由 Cron 每 5 分钟触发，通过钉钉通道主动推送消息：

```
OpenClaw Cron引擎           隔离子Agent               Python 脚本
    │                           │                        │
    │ [每5分钟触发]              │                        │
    │                           │                        │
    │ 创建隔离会话               │                        │
    │ deliver=true              │                        │
    │ channel=dingtalk-connector│                        │
    │ to={staffId}              │                        │
    │ ────────────────────────► │                        │
    │                           │                        │
    │                           │ exec: python3           │
    │                           │ check_upcoming.py       │
    │                           │ ─────────────────────► │
    │                           │                        │
    │                           │                        │ get_due_soon(20min)
    │                           │                        │ ──► SQLite
    │                           │                        │ 查询: start_time 在
    │                           │                        │ 当前~20分钟后
    │                           │                        │ 且 remind_sent=0
    │                           │                        │
    │                           │                        │ [情况A: 无即将开始的日程]
    │                           │ ◄── {"status":          │
    │                           │  "no_upcoming"} ─────── │
    │                           │                        │
    │                           │ [无需操作，任务结束]      │
    │                           │                        │
    │   ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─    │
    │                           │                        │
    │                           │                        │ [情况B: 有即将开始的日程]
    │                           │                        │
    │                           │                        │ format_reminder()
    │                           │                        │ mark_reminded(id)
    │                           │                        │ ──► UPDATE remind_sent=1
    │                           │                        │
    │                           │ ◄── {"status":          │
    │                           │  "reminders_sent",      │
    │                           │  "message":"⏰ 日程提醒！│
    │                           │  组会 约15分钟后开始..."} │
    │                           │                        │
    │                           │ [将 message 内容         │
    │                           │  发送给用户]              │
    │                           │                        │
    │                           │ ──► 钉钉连接器 ──► 用户钉钉收到提醒
```

**防重复提醒机制**：

数据库表中的 `remind_sent` 字段（INTEGER, 默认 0）：
- `0` = 未发送提醒
- `1` = 已发送提醒

`get_due_soon()` 查询时附带条件 `AND remind_sent = 0`，确保每个日程只提醒一次。
`mark_reminded()` 在格式化提醒消息后立即将该字段置为 1。

---

## 5. 数据持久化设计

### 5.1 数据库选型

使用 **SQLite**，原因：
- 零配置，无需安装数据库服务
- 单文件存储，便于备份和迁移
- 并发读性能满足日程管理场景
- Python 标准库内置 `sqlite3` 模块

### 5.2 表结构

```sql
CREATE TABLE schedules (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,  -- 自增主键
    title       TEXT NOT NULL,                       -- 日程标题
    description TEXT DEFAULT '',                     -- 日程描述
    start_time  TEXT NOT NULL,                       -- 开始时间 (YYYY-MM-DD HH:MM)
    end_time    TEXT NOT NULL,                       -- 结束时间 (YYYY-MM-DD HH:MM)
    location    TEXT DEFAULT '',                     -- 地点
    remind_sent INTEGER DEFAULT 0,                   -- 是否已发送提醒 (0/1)
    created_at  TEXT NOT NULL,                       -- 创建时间
    updated_at  TEXT NOT NULL                        -- 最后更新时间
);
```

### 5.3 索引

```sql
CREATE INDEX idx_start ON schedules(start_time);  -- 加速时间范围查询
CREATE INDEX idx_end   ON schedules(end_time);     -- 加速冲突检测
```

### 5.4 并发安全

使用 WAL（Write-Ahead Logging）模式：`PRAGMA journal_mode=WAL`。
允许多个 Agent 会话同时读取数据库，写入操作自动排队。

---

## 6. 关键算法说明

### 6.1 时间冲突检测

两个时间段 `[A_start, A_end)` 和 `[B_start, B_end)` 存在重叠的充要条件：

```
A_start < B_end  AND  A_end > B_start
```

等价 SQL：

```sql
SELECT * FROM schedules
WHERE start_time < ?  -- ?=新日程的 end_time
  AND end_time > ?    -- ?=新日程的 start_time
```

覆盖了所有重叠情况（部分重叠、完全包含、被包含）。

### 6.2 替代时间建议算法

`suggest_alternative()` 向前后两个方向搜索最近的空闲时间段：

**向后搜索**：
1. 从新日程的结束时间开始，设为候选起点
2. 查询该时间点之后的已有日程（按 start_time 升序，最多 10 条）
3. 逐一检查：候选时间段是否与已有日程冲突
4. 如果冲突，候选起点跳到已有日程的结束时间之后
5. 如果不冲突，找到可用时间段

**向前搜索**：
1. 从新日程的开始时间减去持续时长，设为候选起点
2. 查询该时间点之前的已有日程（按 end_time 降序）
3. 类似逻辑向前查找
4. 额外检查：候选时间不能早于当前时间

---

## 7. 文件结构与职责

```
~/.openclaw/workspace/
│
├── schedule/                        # 日程管理模块目录
│   ├── schedule_manager.py          # 核心: CRUD + 冲突检测 + 建议算法
│   │   ├── get_conn()               #   获取 SQLite 连接
│   │   ├── init_db()                #   初始化数据库表和索引
│   │   ├── add_schedule()           #   添加日程 (自动检测冲突)
│   │   ├── get_schedule()           #   按 ID 查询
│   │   ├── list_schedules()         #   按时间范围列出
│   │   ├── update_schedule()        #   更新字段 (自动检测冲突)
│   │   ├── delete_schedule()        #   删除日程
│   │   ├── search_schedules()       #   关键词模糊搜索
│   │   ├── check_conflict()         #   时间冲突检测
│   │   ├── suggest_alternative()    #   替代时间建议
│   │   ├── get_upcoming()           #   查询未来 N 小时日程
│   │   ├── get_due_soon()           #   查询即将开始的日程
│   │   ├── mark_reminded()          #   标记已提醒
│   │   └── main()                   #   CLI 入口 (命令路由)
│   │
│   ├── email_summary.py             # 邮件汇总: 查询→格式化→SMTP发送
│   │   ├── load_config()            #   读取 config.json
│   │   ├── format_schedule_list()   #   纯文本格式化
│   │   ├── build_email()            #   构建 HTML + 纯文本邮件
│   │   ├── send_email()             #   SMTP_SSL 发送
│   │   └── main()                   #   入口
│   │
│   ├── check_upcoming.py            # 钉钉提醒: 检查→格式化→标记
│   │   ├── format_reminder()        #   格式化提醒文本
│   │   └── main()                   #   入口
│   │
│   ├── config.json                  # SMTP 邮箱配置
│   ├── schedules.db                 # SQLite 数据库 (运行时生成)
│   ├── SETUP.md                     # 用户使用手册
│   └── TECHNICAL.md                 # 本技术文档
│
└── skills/
    └── schedule-manager/
        └── SKILL.md                 # Agent 行为规范
                                     # (命令格式、操作步骤、
                                     #  模糊指令策略、cron模板)
```

### 各文件间的调用关系

```
SKILL.md ─────── 指导 ──────► OpenClaw Agent (LLM)
                                    │
                          exec 工具调用
                                    │
                    ┌───────────────┼───────────────┐
                    ▼               ▼               ▼
          schedule_manager.py  email_summary.py  check_upcoming.py
                    │               │               │
                    │          import from      import from
                    │          schedule_manager  schedule_manager
                    │               │               │
                    └───────┬───────┘───────────────┘
                            ▼
                      schedules.db (SQLite)
```

---

## 8. 安全与异常处理

### 8.1 SQL 注入防护

所有 SQL 查询使用参数化查询（`?` 占位符），不拼接字符串：

```python
# 安全写法（本系统采用）
conn.execute("SELECT * FROM schedules WHERE id = ?", (schedule_id,))

# 危险写法（绝对不用）
conn.execute(f"SELECT * FROM schedules WHERE id = {schedule_id}")
```

### 8.2 字段白名单

`update_schedule()` 函数只允许更新预定义的字段集合：

```python
allowed = {"title", "description", "start_time", "end_time", "location"}
fields = {k: v for k, v in kwargs.items() if k in allowed}
```

防止通过传入 `remind_sent`、`id` 等字段篡改系统状态。

### 8.3 邮件发送异常处理

`email_summary.py` 的 `main()` 函数用 try-except 包裹发送逻辑，
失败时输出错误 JSON 而不是崩溃，确保 Cron 任务不会因为临时网络问题而中断：

```python
try:
    send_email(msg, config)
    result = {"status": "success", ...}
except Exception as e:
    result = {"status": "error", "error": str(e), ...}
```

### 8.4 敏感信息保护

- `config.json` 包含 SMTP 授权码，已通过 `.gitignore` 中的规则避免被意外提交
  （虽然当前 `.gitignore` 未明确排除 config.json，建议生产环境中添加）
- OpenClaw 的 AGENTS.md 中有"不要泄露私人数据"的红线规则
