# Task Detection + Proactive Thinking 🎯

[English](#english) | [中文](#中文)

---

<a name="english"></a>
## English

Automatically detect task anomalies, intelligently analyze causes, and proactively propose solutions for OpenClaw agents.

### Features

- 🔍 **Auto Scan**: Detect stalled, blocked, overdue, and duplicate tasks
- 🧠 **Proactive Thinking**: Analyze causes and generate 3 solution options
- 🤖 **Auto-fix**: Attempt automatic resolution without human intervention
- 📱 **Smart Alerts**: Push critical notifications via Feishu
- 🌐 **Multi-language**: Support for English and Chinese

### Installation

```bash
npx skills add clawwizard/task-detection-thinking
```

### Usage

```bash
# Manual trigger
node skills/task-detection-thinking/scripts/detect.js

# Or ask your OpenClaw agent:
# "Check task status" / "检测任务状态"
```

### How It Works

1. **Scan** HEARTBEAT.md + WORKING.md for task anomalies
2. **Analyze** context and historical memory
3. **Generate** 3 solution options
4. **Auto-fix** what can be fixed automatically
5. **Alert** on critical issues via Feishu

### Configuration

See [SKILL.md](./SKILL.md) for detailed configuration options.

### Task Management Templates

This skill works with standardized task management files:

#### HEARTBEAT.md - Global Task Board

```markdown
## Global Task Board
| TaskID | Task Name | Status | Progress | Deadline | Last Update | Block Reason |
|--------|-----------|--------|----------|----------|-------------|--------------|
| T001 | Initialize three-layer memory | Done | 100% | 2026-03-10 | 2026-03-10 | None |
| T002 | Integrate vector retrieval | Active | 60% | 2026-03-15 | 2026-03-12 | Waiting for API key |
| T003 | Test proactive thinking | Waiting | 0% | 2026-03-20 | 2026-03-11 | Depends on T002 |
```

**Status Definitions:**
- **Queue** - Waiting to start
- **Active** - In progress
- **Waiting** - Blocked/Waiting
- **Done** - Completed
- **Aborted** - Cancelled

#### WORKING.md - Project-Level Task Rules

All subtasks must include:
- Status (Queue/Active/Waiting/Done)
- Progress percentage
- Owner/Assignee
- Dependencies

**Auto-detection Rules:**
- Active tasks stalled >24h auto-marked as "Abnormal"
- Blocked tasks must fill "Block Reason" and "Support Needed"
- Daily 23:00 auto-summary to HEARTBEAT.md

---

<a name="中文"></a>
## 中文

自动检测任务异常，智能分析原因，主动提出解决方案的 OpenClaw 智能体技能。

### 功能特点

- 🔍 **自动扫描**：检测停滞、阻塞、超期和重复任务
- 🧠 **主动思考**：分析原因并生成3个解决方案
- 🤖 **自动修复**：无需人工干预自动解决问题
- 📱 **智能告警**：通过飞书推送关键通知
- 🌐 **多语言**：支持英文和中文

### 安装

```bash
npx skills add clawwizard/task-detection-thinking
```

### 使用方法

```bash
# 手动触发
node skills/task-detection-thinking/scripts/detect.js

# 或向你的 OpenClaw 助手说：
# "检查任务状态" / "Check task status"
```

### 工作原理

1. **扫描** HEARTBEAT.md + WORKING.md 寻找任务异常
2. **分析** 上下文和历史记忆
3. **生成** 3个解决方案选项
4. **自动修复** 可以自动解决的问题
5. **告警** 关键问题通过飞书通知

### 配置

详细配置选项请查看 [SKILL.md](./SKILL.md)（英文）或 [locales/zh/SKILL.md](./locales/zh/SKILL.md)（中文）。

### 任务管理模板

本技能配合标准化的任务管理文件使用：

#### HEARTBEAT.md - 全局任务看板

```markdown
## 全局任务看板
| 任务ID | 任务名称 | 状态 | 进度 | 截止时间 | 最后更新 | 阻塞原因 |
|--------|----------|------|------|----------|----------|----------|
| T001 | 初始化三层记忆 | Done | 100% | 2026-03-10 | 2026-03-10 | 无 |
| T002 | 集成向量检索 | Active | 60% | 2026-03-15 | 2026-03-12 | 等待API密钥 |
| T003 | 测试主动思考 | Waiting | 0% | 2026-03-20 | 2026-03-11 | 依赖T002完成 |
```

**状态定义：**
- **Queue** - 等待开始
- **Active** - 进行中
- **Waiting** - 阻塞/等待
- **Done** - 已完成
- **Aborted** - 已取消

#### WORKING.md - 项目级任务规则

所有子任务必须标注：
- 状态（Queue/Active/Waiting/Done）
- 进度百分比
- 负责人
- 依赖项

**自动检测规则：**
- 停滞超24小时的Active任务自动标记为"异常"
- 阻塞任务必须填写"阻塞原因"和"所需支持"
- 每日23:00自动汇总所有任务状态到HEARTBEAT.md

---

## License

MIT © OpenDolph
