---
name: lifecycle-hooks
description: Agent lifecycle hook 系统 — 基于 OpenClaw 内核能力设计，用 heartbeat + subagent 机制模拟关键事件触发。借鉴 rohitg00/agentmemory 的 13 hook 设计。
version: 0.2.0
owner: local-workspace-agent
tags: [memory, automation, hooks]
---

# Lifecycle Hooks（生命周期钩子）

基于 OpenClaw 内核能力重新设计。不是所有钩子都需要内核拦截——通过**heartbeat 轮询 + skill 行为模式**可以模拟大部分。

## 内核能力映射

| 钩子 | 内核支持方式 | 实现难度 |
|------|------------|---------|
| `subagent` 生命周期 | `sessions_spawn` + `sessions_yield` callback | ✅ 简单 |
| `session-end` | `cron` + `kind: agentTurn` + `delivery: session-end` | ✅ 简单 |
| `task-completed` | skill 层行为检测（artifact 写入/代码修改） | ✅ 简单 |
| `pre-tool-use` | **无法实现**（无工具调用拦截） | ❌ 不可能 |
| `post-tool-use` | **无法实现**（无工具结果回调） | ❌ 不可能 |
| `pre-compact` | OpenClaw 内置 | ✅ 已实现 |

---

## 实际可实现的钩子

### 1. subagent 生命周期（✅ 可实现）

**触发方式**：使用 `sessions_spawn` 派发子代理，通过 `sessions_yield` 等待结果时检测状态。

```python
# 子代理派发 → 记录 agent_id
spawn_runtime = sessions_spawn(
    label="audit-worker-1",
    runtime="subagent",
    mode="run",
    cleanup="delete",
    task="你是 security-auditor，审查以下代码..."
)
# sessions_yield 完成后自动触发 subagent-stop
result = sessions_yield(spawn_runtime)

# 自动动作：
# 1. 记录 subagent-stop 事件到 memory/
# 2. 检查 result 是否值得 skill-compounding
```

**自动记录到 memory/YYYY-MM-DD.md**：
```markdown
## [HH:MM] subagent-stop: audit-worker-1
- 耗时：{duration}s
- 结论：⚠️ 发现 3 个安全问题
- 下一步：提交 grill-me 确认优先级
```

### 2. session-end（✅ 可实现）

**触发方式**：用 `cron` 创建一次性任务，触发时机为"当前会话结束后"（用 `delivery: { sessionKey, delayMs }` 延迟触发）。

```python
# 当前会话结束时（用户发消息确认或检测到 inactive）
cron_add(
    name="session-end-memory",
    schedule={"kind": "once", "timestamp": now() + 30_000},  # 30秒后
    payload={
        "kind": "agentTurn",
        "prompt": "执行 session-end 增强逻辑",
        "sessionTarget": "main"
    },
    sessionTarget="isolated"
)
```

**session-end 增强逻辑**（在 isolated 会话执行）：
1. 读取当日 `memory/YYYY-MM-DD.md`
2. 检查是否有未完成的沉淀候选（代码修改/决策/成功解决问题的 skill 使用）
3. 如果有，调用 `skill-compounding` 检查
4. 更新 heartbeat-state.json

### 3. task-completed（✅ 可实现）

**触发方式**：在 agent 的**主循环行为中**检测关键模式，而非依赖工具层回调。

```python
# Skill 层实现：在每次回复后检查

def check_task_completed(agent_context):
    signals = [
        # Artifact 写入（写工具成功返回后）
        agent_context.last_tool == "write" and "artifacts/" in agent_context.last_tool_args.path,
        # 代码修改（exec 结果显示成功）
        agent_context.last_tool == "exec" and agent_context.last_tool_result.exit_code == 0
            and any(kw in agent_context.last_tool_args for kw in ["edit", "patch", "apply"]),
        # 重要发现（research 类 skill 完成后）
        agent_context.last_tool == "sessions_spawn"
            and agent_context.session_result.get("conclusion") == "success",
    ]
    
    if any(signals):
        trigger_skill_compounding_check(agent_context)
        write_daily_log("task_completed", agent_context.summary)
```

**注意**：这依赖 agent 的自我检测行为，不是内核级别的透明拦截。SOUL.md 中需要说明这一限制。

### 4. pre-tool-use / post-tool-use（❌ 无法实现）

**原因**：OpenClaw 内核没有工具调用拦截机制。

**替代方案**：通过**约定式行为**模拟：
- 高危操作（trash/delete/覆盖）→ agent 在执行前主动向用户确认
- 这不是"钩子自动触发"，而是 agent 遵循 SOUL.md 中的**安全确认规范**

```python
# Agent 行为规范（非钩子触发）

if tool_name in ["trash", "rm", "exec with destructive commands"]:
    # 不自动执行，而是询问用户
    # "确认删除 {path}？请回复 /approve"
```

---

## 钩子优先级（实际版）

| 钩子 | 可实现 | 说明 |
|------|--------|------|
| `subagent-start` | ✅ | sessions_spawn 时记录 |
| `subagent-stop` | ✅ | sessions_yield 返回后记录 |
| `task-completed` | ✅ | skill 层行为检测 |
| `session-end` | ✅ | cron 一次性任务 |
| `pre-compact` | ✅ | OpenClaw 内置 |
| `session-start` | ✅ | SOUL.md 已实现 |
| `pre-tool-use` | ❌ | 内核不支持 |
| `post-tool-use` | ❌ | 内核不支持 |

---

## 与 heartbeat 的配合

heartbeat 是所有运行时钩子的实际触发机制：

```
heartbeat（每30分钟）→ 检查待触发事件 → 执行对应钩子逻辑
```

**session-end 典型流程**：
1. 用户结束会话（或 heartbeat 检测到 inactive > 10分钟）
2. 创建 `session-end` cron 任务（delivery: session-end）
3. cron 触发 → isolated 会话执行 memory 写入 + skill-compounding 检查
4. 更新 heartbeat-state.json

---

## 与其他 Skill 的配合

- `skill-compounding`：subagent-stop 和 task-completed 都触发沉淀检查
- `brainstorming`：**约定式**替代 pre-tool-use（操作意图记录到 brainstorming 上下文）
- `conductor`：session-end 后检查是否进入下一阶段

---

## 落地现状（修订版）

| 钩子 | 状态 | 实现位置 |
|------|------|---------|
| `pre-compact` | ✅ | SOUL.md（内置） |
| `session-start` | ✅ | SOUL.md（内置） |
| `pre-tool-use` | ⚠️ 约定式 | SOUL.md 安全规范（非内核拦截） |
| `post-tool-use` | ⚠️ 约定式 | SOUL.md 安全规范（非内核拦截） |
| `task-completed` | ✅ | lifecycle-hooks skill（行为检测） |
| `subagent-start` | ✅ | lifecycle-hooks skill（sessions_spawn） |
| `subagent-stop` | ✅ | lifecycle-hooks skill（sessions_yield） |
| `session-end` | ✅ | lifecycle-hooks skill（cron） |

---

## 触发命令

"开启 hooks"、"检查生命周期钩子"、"记忆自动捕获怎么配置"