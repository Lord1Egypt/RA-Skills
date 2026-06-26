---
name: agent-harness
description: Agent Harness管理工具 - 创建、配置和使用ACP (Agent Coding Platform) harness进行代码开发。支持Claude Code、Codex、Gemini CLI等主流AI编码助手。
---

# Agent Harness 管理工具

> 💰 **本 Skill 已接入 SkillPay 付费系统**
> - 每次调用费用：**0.01 USDT**
> - 支付方式：BNB Chain USDT
> - 请先确保账户有足够余额

ACP (Agent Coding Platform) 工具管理 - 统一接口调用 Claude Code、Codex、Gemini CLI 等 AI 编码助手。

## 功能概述

本 Skill 提供以下能力：

1. **列出可用 Agents** - 查看当前可用的 ACP harness
2. **创建会话** - 启动 thread-bound persistent sessions
3. **发送任务** - 向指定 agent 发送编码任务
4. **管理会话** - 查看、监控、终止 agent 会话
5. **配置管理** - 设置默认 agent 和参数

## 使用场景

当用户需要以下功能时触发此 Skill：

- "帮我用 Claude Code 重构这段代码"
- "用 Codex 修复这个 bug"
- "启动一个 coding agent"
- "查看当前运行的 agents"
- "创建 ACP session"
- "管理 agent 会话"

## 核心命令

### 列出可用 Agents

```bash
# 查看系统配置的可用 agents
agents_list

# 或通过 ACP 方式列出
sessions_spawn --list-agents
```

### 创建 Agent 会话

```bash
# 使用 Claude Code 创建会话
sessions_spawn \
  --runtime acp \
  --agentId claude-code \
  --task "重构 payment.py 模块" \
  --mode session \
  --thread

# 使用 Codex 创建会话
sessions_spawn \
  --runtime acp \
  --agentId codex \
  --task "修复登录功能 bug" \
  --mode session \
  --thread

# 使用 Gemini CLI
sessions_spawn \
  --runtime acp \
  --agentId gemini-cli \
  --task "优化数据库查询" \
  --mode session \
  --thread
```

### 发送任务到现有会话

```bash
# 向指定 session 发送消息
sessions_send \
  --sessionKey <session-key> \
  --message "继续完成剩下的功能"
```

### 管理 Agent 会话

```bash
# 列出所有子 agents
subagents list

# 终止指定 agent
subagents kill --target <agent-id>

# 向 agent 发送指令
subagents steer --target <agent-id> --message "调整实现方案"
```

## 支持的 Agents

| Agent ID | 名称 | 提供商 | 适用场景 |
|----------|------|--------|----------|
| claude-code | Claude Code | Anthropic | 复杂重构、架构设计 |
| codex | Codex | OpenAI | 快速编码、bug修复 |
| gemini-cli | Gemini CLI | Google | 代码优化、文档生成 |

## 工作流示例

### 场景1：代码重构

```python
# Step 1: 启动 Claude Code session
sessions_spawn(
    task="重构 user_auth.py 模块，提取公共逻辑到基类",
    runtime="acp",
    agentId="claude-code",
    mode="session",
    thread=True
)

# Step 2: 等待结果 (系统会自动推送完成事件)
# 或使用 sessions_yield 结束当前 turn 接收结果
sessions_yield()
```

### 场景2：Bug 修复

```python
# 快速修复模式 - run (one-shot)
sessions_spawn(
    task="修复 login 函数中的空指针异常",
    runtime="acp",
    agentId="codex",
    mode="run",
    timeoutSeconds=300
)
```

### 场景3：多 Agent 协作

```python
# Agent 1: 设计 API
sessions_spawn(
    task="设计 REST API 接口规范",
    runtime="acp",
    agentId="claude-code",
    mode="session",
    thread=True,
    label="api-design"
)

# Agent 2: 实现后端
sessions_spawn(
    task="根据 API 规范实现后端代码",
    runtime="acp",
    agentId="codex",
    mode="session",
    thread=True,
    label="backend-impl"
)

# 监控进度
subagents list
```

## 最佳实践

### 选择合适的 Agent

- **Claude Code**: 适合复杂任务、需要深度推理的场景
- **Codex**: 适合快速编码、明确的编码任务
- **Gemini CLI**: 适合代码优化、性能改进

### 会话管理

1. **Thread-bound sessions**: 适合长期项目，保持上下文
2. **One-shot runs**: 适合简单任务，快速完成
3. **定期清理**: 及时终止不再需要的 sessions

### 任务描述技巧

- 提供清晰的上下文和约束条件
- 说明期望的输出格式
- 指定代码风格和规范
- 包含相关的文件路径

## 常见问题

### Q: 如何选择 agentId?

A: 如果不确定，优先尝试 `claude-code`。查看可用 agents：`agents_list`

### Q: session 和 run 模式有什么区别?

A: 
- `mode=session`: 持久会话，适合多轮对话，保持上下文
- `mode=run`: 一次性任务，完成后自动结束

### Q: 如何获取 session 结果?

A: 使用 `sessions_yield()` 结束当前 turn，子 agent 的结果会作为下一条消息推送。

### Q: 可以传递文件给 agent 吗?

A: 可以，使用 `attachments` 参数传递文件内容。

## 配置示例

```json
{
  "defaultAgent": "claude-code",
  "timeoutSeconds": 600,
  "preferredMode": "session",
  "threadBound": true
}
```

## 相关工具

- `agents_list`: 列出可用 agents
- `sessions_spawn`: 创建新会话
- `sessions_send`: 发送消息到会话
- `sessions_yield`: 结束当前 turn 接收结果
- `subagents`: 管理子 agents
- `sessions_list`: 列出所有会话
- `sessions_history`: 获取会话历史

## 注意事项

1. ACP harness 需要正确配置才能使用
2. 长时间运行的 sessions 需要适当管理
3. Thread-bound sessions 会保持上下文，注意 token 消耗
4. 敏感信息不要传递给外部 agents
