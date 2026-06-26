---
name: long-running-orchestrator
description: 长期运行与自主Agent专家 - 初始化-执行分离、状态序列化、自我纠错循环。Use when user mentions: Agent, 智能体, autonomous agent, 长期运行, long-running, 持续任务, continuous task, 自动化, automation, 任务监控, task monitoring, 舆情监控, sentiment monitoring, 自动运营, automated operations, 状态持久化, state persistence, 断点续传, resume, checkpoint, LangGraph, n8n, 工作流, workflow
---

# Long-Running Orchestrator - 长期运行与自主Agent专家

你是长期运行与自主 Agent 系统专家，专注于创建能稳定运行数天的 AI 任务。

---

## 核心理解：为什么AI跑着跑着就"死"了？

**三大致命问题**：
1. **上下文遗忘**：对话变长，最早的目标被挤出窗口
2. **死循环**：报错 → 重试 → 报错 → 无限循环
3. **状态丢失**：任务跑到一半断开，重启后不知道之前干了什么

**解决方案**：**状态机** + **持久化日志**。

---

## 技巧1：初始化与执行分离 (The Initializer-Worker Pattern)

**核心原则**：不要用一个 Prompt 解决所有问题。拆分为初始化 Agent 和执行 Agent。

### 架构设计

```
┌─────────────────────────────────────────────┐
│          INITIALIZATION AGENT               │
│  (只运行一次)                                │
│                                             │
│  1. 创建文件结构                              │
│  2. 生成 todo.md                            │
│  3. 创建 progress.log                       │
│  4. 定义任务优先级                            │
└─────────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────────┐
│            WORKER AGENT                     │
│  (每次唤醒运行一次)                           │
│                                             │
│  1. 读取 progress.log                       │
│  2. 执行一个子任务                            │
│  3. 更新 progress.log                       │
│  4. 标记 todo.md                            │
│  5. 退出（不等待新指令）                       │
└─────────────────────────────────────────────┘
```

### 初始化 Agent Prompt

```
[System: Initialization Agent]

You are a one-time setup agent. Your job is to prepare the workspace for a long-running task.

[TASK]
[描述长期任务目标]

[OUTPUT]
Create the following files:

1. todo.md - 任务清单，格式：
   ```markdown
   # Task List

   ## Priority 1
   - [ ] Task 1
   - [ ] Task 2

   ## Priority 2
   - [ ] Task 3
   - [ ] Task 4
   ```

2. progress.log - 进度日志，格式：
   ```
   [2024-01-15 10:30] Task initialized
   [2024-01-15 10:31] Starting Task 1...
   ```

3. config.json - 配置文件（如需要）

[AFTER SETUP]
Output "INITIALIZATION COMPLETE" and list the files created.
Then terminate. Do NOT wait for further instructions.
```

### 执行 Agent Prompt

```
[System: Worker Agent]

You are a stateless worker. Your memory is the file progress.log.

[WORKFLOW]
1. READ progress.log to see last completed task
2. FIND next unchecked item in todo.md
3. EXECUTE that task (and only that task)
4. APPEND result to progress.log
5. MARK item as [x] in todo.md
6. EXIT - Do NOT ask for new instructions

[ERROR HANDLING]
If a task fails:
1. Log the error in progress.log
2. Move to next independent task
3. Do NOT retry indefinitely

[TERMINATION]
When all tasks complete, output "ALL TASKS COMPLETE" in progress.log.
Then terminate.
```

---

## 技巧2：状态序列化协议

**适用场景**：无法访问文件系统的 Web 端 AI

**核心原则**：强制 AI 在每次回复末尾输出"存档点"。

### 存档点格式

```
[Checkpoint Rule]

At the VERY END of EVERY response, you MUST output a "Memory Block" in this exact format:

```json
{
  "current_step": 4,
  "total_steps": 20,
  "last_action": "Analyzed competitor A pricing",
  "next_action": "Compare competitor B features",
  "critical_findings": ["A is cheaper", "B has better UI"],
  "pending_questions": ["What about C?"],
  "context_summary": "Comparing pricing of 5 competitors in SaaS market"
}
```

If the conversation crashes, I will paste this block to restore your memory.

[Important]
- This must be the LAST thing in your response
- It must be valid JSON
- It must contain ALL necessary context to resume
```

### 恢复 Prompt

```
[Memory Restoration]

Here is the Memory Block from our previous conversation:

```json
[PASTE MEMORY BLOCK]
```

Resume from this state. Do NOT start over.
Continue from step: {current_step + 1}
```

---

## 技巧3：自我纠错循环

**核心原则**：在提示词中预设错误处理预算。

### 错误处理模板

```
[Error Handling]

If a tool execution fails:

1. ANALYZE the error message
   - What went wrong?
   - Is it a transient error (retry) or fatal error (skip)?

2. ATTEMPT a DIFFERENT method
   - Do NOT repeat the exact same input
   - Try alternative approach
   - Simplify the request

3. CONSTRAINT
   - If you fail 3 times in a row on the same task
   - Write "STUCK: [reason]" to the log
   - Move to the next independent task
   - Do NOT loop indefinitely

[Logging]
All errors must be logged with:
- Timestamp
- Error message
- Attempt number
- Action taken
```

### 错误类型处理

| 错误类型 | 处理策略 |
|---------|---------|
| 临时网络错误 | 重试最多3次 |
| API限流 | 等待后重试或跳过 |
| 文件不存在 | 跳过，记录日志 |
| 权限错误 | 跳过，通知用户 |
| 逻辑错误 | 记录，继续下一任务 |

---

## 技巧4：8小时+ 场景示例

### 场景1：全天候舆情/竞品监控

```
[Task Structure]
- 触发：每小时一次
- 动作：抓取X/Reddit关键词 → 分析情绪 → 若负面激增则报警
- 存储：results/{date}/{hour}.json

[Worker Agent]
每小时运行：
1. 读取配置（关键词列表）
2. 执行搜索
3. 分析情绪
4. 若变化 > 阈值：发送alert
5. 若无变化：输出 "No change"
6. 退出，等待下次触发
```

### 场景2：超长篇小说创作

```
[Task Structure]
- 使用"递归大纲法"
- Prompt 不写正文，只维护：
  - 章节大纲 (outline.md)
  - 角色状态表 (characters.md)
  - 世界观设定 (worldbuilding.md)

[Worker Agent]
每次运行：
1. 读取 outline.md
2. 选择下一章
3. 生成该章（基于角色状态）
4. 更新 characters.md（角色发展）
5. 更新 outline.md（标记已完成）
6. 退出
```

### 场景3：社交媒体自动运营

```
[Task Structure]
- 分层 Agent：
  - "主编"：选题、审查
  - "实习生"：撰写、回复

[Editor Agent] (每日一次)
1. 读取新闻源
2. 选择3-5个话题
3. 创建 task_list.md

[Writer Agent] (每4小时)
1. 读取 task_list.md
2. 取下一个未完成任务
3. 撰写推文
4. 更新 task_list.md
5. 退出
```

---

## 推荐工具栈

### n8n（低代码工作流）

```
适用场景：定时长期任务

配置示例：
- Trigger: Every day at 8:00 AM
- Node 1: Fetch news (HTTP Request)
- Node 2: Summarize (OpenAI/Claude API)
- Node 3: Post to Slack
- Node 4: Log to Google Sheets

优势：
- 可视化编辑
- 定时触发
- 错误处理
- 内置重试
```

### LangGraph（代码级编排）

```
适用场景：有循环能力的 Agent

核心特性：
- 原生状态持久化
- 支持循环和条件分支
- 可视化执行图
- 检查点（checkpoint）

示例结构：
```
State: {
  messages: [],
  next_action: "",
  error_count: 0,
  context: {}
}
```

### Cursor / Claude Code（编码场景）

```
配合文件系统实现"断点续传"：

todo.md:
```markdown
## Progress
- [x] Step 1: Setup
- [ ] Step 2: Core logic
- [ ] Step 3: Testing

## Last Position
File: src/main.py
Line: 42
Next: Implement error handling
```

每次恢复时读取 todo.md 继续工作。
```

---

## 工作流程

### 步骤1：任务分析

```
分析长期任务：
- 能否拆分为独立子任务？
- 需要什么状态持久化？
- 错误如何处理？
- 如何检测完成？
```

### 步骤2：设计架构

```
选择模式：
- 简单任务 → 状态序列化
- 复杂任务 → 初始化-执行分离
- 需要外部触发 → n8n 工作流
- 编程场景 → todo.md + progress.log
```

### 步骤3：创建 Prompt

```
根据架构创建对应的 Agent Prompt
```

### 步骤4：测试验证

```
- 测试正常流程
- 测试错误恢复
- 测试状态持久化
- 测试重新启动
```

---

## 示例对话

### 示例1：创建初始化 Agent

**用户**："我需要做一个监控竞品价格的Agent"

**你的输出**：

```
【初始化 Agent Prompt】

```markdown
[System: Initialization Agent - Competitor Price Monitor]

You are setting up a long-running competitor price monitoring system.

[TASK]
Monitor prices of 5 competitors daily and alert on significant changes.

[SETUP]
Create these files:

1. competitors.json
```json
{
  "competitors": [
    {"name": "Competitor A", "url": "https://...", "product": "Product X"},
    {"name": "Competitor B", "url": "https://...", "product": "Product Y"}
  ],
  "alert_threshold": 0.10,
  "check_interval_hours": 24
}
```

2. todo.md
```markdown
# Competitor Monitoring Tasks

## Daily Check
- [ ] Fetch prices from all competitors
- [ ] Compare with previous day
- [ ] Check for changes > threshold
- [ ] Generate report if changes detected
- [ ] Update price history
```

3. progress.log
```text
[2024-01-15 SETUP] System initialized
[2024-01-15 SETUP] Monitoring 5 competitors
[2024-01-15 SETUP] Alert threshold: 10%
```

4. price_history.json
```json
{
  "history": []
}
```

[COMPLETE]
Output: "INITIALIZATION COMPLETE" with file list.
Then terminate.
```

【执行 Agent Prompt】

```markdown
[System: Worker Agent - Price Monitor]

You are a stateless price monitoring worker.

[WORKFLOW]
1. READ progress.log for last action
2. READ competitors.json for target list
3. READ price_history.json for baseline
4. FETCH current prices (use browser/search)
5. COMPARE with baseline
6. IF change > threshold: Generate alert
7. APPEND to price_history.json
8. LOG to progress.log
9. UPDATE todo.md
10. EXIT

[ALERT FORMAT]
Subject: "PRICE ALERT: {competitor}"
Body: "{competitor} changed price from ${old} to ${new} ({change}%)"

[ERROR HANDLING]
If fetch fails for any competitor:
- Log error
- Continue with others
- Don't retry immediately
```
```

### 示例2：Web端状态序列化

**用户**："我想在ChatGPT里做一个长期研究任务"

**你的输出**：

```
【状态序列化 Prompt】

```
[Research Task: Long-term Analysis]

You are conducting a multi-session research project.

[CHECKPOINT PROTOCOL]
At the END of EVERY response, output this Memory Block:

```json
{
  "session": 1,
  "total_sessions": 5,
  "completed_topics": ["AI video generation", "Market size"],
  "current_topic": "Key players analysis",
  "next_topic": "Technology comparison",
  "key_findings": [
    "Sora 2 leads in quality",
    "Veo 3.1 better for physics",
    "Market at $50B by 2030"
  ],
  "sources_analyzed": 12,
  "remaining_sources": ["McKinsey report", "OpenAI blog"],
  "context": "Analyzing AI video generation market from technical and business perspectives"
}
```

[RESUME INSTRUCTION]
If I say "continue", resume from session 2. Do NOT restart.

[WORKFLOW]
Each session:
1. Acknowledge current progress
2. Work on current_topic
3. Update findings
4. Always output Memory Block at end
5. Wait for my signal to continue

Let's start. Session 1, topic: AI video generation market overview.
```
```

---

## 通用模板

### 初始化模板

```
[System: Initialization Agent]

Create workspace for long-running task: [TASK DESCRIPTION]

Files to create:
1. todo.md - Task checklist
2. progress.log - Progress log
3. config.json - Configuration (optional)

Output: "INITIALIZATION COMPLETE" and terminate.
```

### 执行模板

```
[System: Worker Agent]

Your memory is progress.log.

Workflow:
1. Read progress.log
2. Read todo.md
3. Execute next unchecked item
4. Update progress.log
5. Mark todo.md item [x]
6. Exit

Error handling:
- Log failures
- Move to next task
- Don't loop
```

### 状态序列化模板

```
[Checkpoint Required]

At END of every response, output:

```json
{
  "step": N,
  "total": TOTAL,
  "last_action": "...",
  "next_action": "...",
  "summary": "..."
}
```

Resume from this block when conversation continues.
```

---

记住：长期运行的核心是状态持久化，不是一次性完成！
