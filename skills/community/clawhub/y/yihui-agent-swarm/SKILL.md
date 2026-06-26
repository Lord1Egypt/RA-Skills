---
name: agent-swarm
description: Multi-agent orchestration framework for OpenClaw. Define roles, route tasks, manage state, and coordinate agent teams using structured YAML configs and a proven communication protocol. Based on the YiHui team real production setup (小语/小美/大龙).
triggers:
  - 多 agent 协作
  - 编排
  - 任务路由
  - agent 团队
  - 角色定义
  - task routing
  - agent coordination
  - multi-agent orchestration
tags:
  - multi-agent
  - orchestration
  - workflow
  - coordination
  - openclaw
compatibility: openclaw
license: MIT
source: https://github.com/1yihui/YiHui
---

# Agent Swarm

Multi-agent orchestration framework for OpenClaw. Define roles, route tasks, manage state, and coordinate agent teams using a proven communication protocol.

## Core Philosophy

**YiHui 团队经验**：最好的编排不是"一个万能 Agent"，而是**专角色 + 清晰协议 + 状态可见**。

三个原则：
1. **角色隔离**：每个 Agent 知道自己是什么、不是什么
2. **协议通信**：Agent 之间通过结构化消息传递，不靠猜测
3. **状态外化**：任务状态写进 MemPalace，任何 Agent 能查、能接管

## Architecture

```
User Input
    ↓
[Router Agent]  ← 解析意图，判断类型
    ↓
[Specialist Agent(s)]  ← 执行子任务
    ↓
[Critic Agent]  ← 审查结果，决策是否通过
    ↓
[Master Agent]  ← 最终输出，兜底
```

## Role Types

### 1. Master（主控）

**职责**：调度、审查、路由、兜底

**特征**：
- 不直接执行，先判断
- 优先召回记忆（cortex + MemPalace）
- 路由决策 > 执行操作

**行为规则**：
- 每次任务开始前双重召回
- 写入 MemPalace 前先检查是否已有对应 Room
- 遇到未知请求，先问再动，不抢活

### 2. Specialist（专家管家）

**职责**：特定领域的深度执行

**特征**：
- 专注单一领域（运维/资讯/创意/代码）
- 有明确边界，不越界
- 执行结果直接上报，不自己汇总

**行为规则**：
- 边界内的活直接干，不请示
- 边界外的活立即上报 master
- 完成任务立即写记忆

### 3. Critic（审查）

**职责**：审查 specialist 的输出质量

**特征**：
- 挑剔，敢说不
- 关注：事实准确性、格式规范、安全风险
- 不提供替代方案，只判断是否通过

### 4. Router（路由）

**职责**：解析用户意图，分发给正确的 specialist

**特征**：
- 理解模糊请求
- 映射到已知角色/技能
- 处理跨领域请求的归属判断

## Communication Protocol

### Agent → Agent 消息格式

```yaml
message:
  from: agent_id          # 发件人
  to: agent_id            # 收件人
  type: task | report | question | escalate | approve
  priority: high | normal | low
  task:
    id: uuid             # 任务唯一ID
    description: string    # 任务描述
    context: []          # 关联上下文引用
    deadline: timestamp   # 可选截止时间
  status:
    state: pending | in_progress | blocked | done | escalate
    blockers: []         # 阻塞原因
    result: {}           # 结果（完成时填写）
  metadata:
    confidence: 0-1     # 置信度
    requires_approval: boolean
```

### 消息类型说明

| Type | 方向 | 说明 |
|------|------|------|
| `task` | Master → Specialist | 分配任务 |
| `report` | Specialist → Master | 任务完成报告 |
| `question` | Specialist ↔ Master | 边界模糊，需确认 |
| `escalate` | Specialist → Master | 超出能力，请求升级 |
| `approve` | Critic → Master | 审查结论 |

## State Machine

```
PENDING → IN_PROGRESS → [BLOCKED → IN_PROGRESS] → DONE
                ↓
            ESCALATED → IN_PROGRESS / DONE
```

**状态转移规则**：
- `pending → in_progress`：Router 确认后立即转移
- `in_progress → blocked`：遇到障碍（缺信息/缺权限）时转移，blocker 写入 message
- `blocked → in_progress`：Master 解除障碍后恢复
- `in_progress → escalated`：Specialist 判断超出边界时转移
- `any → done`：Critic 批准 or Master 兜底完成

## Memory Protocol

每个 Agent 必须遵守的记忆写入规则：

### 分工原则

| 系统 | 存储内容 | 写入时机 |
|------|---------|---------|
| **MemPalace** | 团队决策、系统改动、长期事实、跨 agent 知识 | 重要信息确认后立即写 |
| **Cortex (MemClaw)** | 会话偏好、临时对话记忆、用户画像 | 每次对话后增量写入 |

### 召回时机

**每次任务开始前必须执行双重召回**：
```
1. cortex_search — MemClaw 向量检索
2. mempalace__mempalace_search — MemPalace 结构化检索
```

**跨 Agent 协作时必须同时跑**：
- 防止重复写入
- 保证上下文连续性

### 跨 Agent 消息路由

使用飞书 channel 时，必须指定 `target` 参数：

| 目标 Agent | target 参数 |
|-----------|------------|
| Master（小语） | `user:ou_<master_open_id>` |
| Specialist（小美/大龙） | `user:ou_<specialist_open_id>` |
| 阿辉（用户） | 走 channel 默认路由 |

**禁止**：`accountId: default` — 会导致 400 错误

## Quick Start

### 1. 定义团队角色（YAML）

```yaml
# my-team.yaml
team:
  name: 我的团队
  agents:
    - id: master
      name: 小语
      role: master
      channel: feishu
      target: user:ou_xxx
    - id: specialist-ops
      name: 大龙
      role: specialist
      domain: [ops, security, diagnosis]
      channel: feishu
      target: user:ou_yyy
    - id: specialist-content
      name: 小美
      role: specialist
      domain: [news, creative, design]
      channel: feishu
      target: user:ou_zzz
```

### 2. 任务创建流程

```
用户输入 → Router 解析意图 → Master 分配 → Specialist 执行 → Critic 审查 → Master 汇总
```

### 3. 状态追踪

所有任务状态写入 MemPalace：

```python
# Task state stored in MemPalace
task_id: "uuid-xxx"
state: "in_progress"
owner: "specialist-ops"
created_at: timestamp
updated_at: timestamp
history: [state_transitions]
```

## Real Example: YiHui Team

真实生产配置（小语/小美/大龙）：

| Agent | 角色 | 飞书 ID | 职责边界 |
|-------|------|---------|---------|
| 🌸 小语 | Master | `ou_7d0630bcf6e7fb2c35c2033be5e23722` | 调度、审查、路由、兜底 |
| 🐉 大龙 | Specialist | `ou_6a94e9d0e8eb6112626bdacefd0f3438` | 运维、诊断、系统检查、安全审计 |
| 🌷 小美 | Specialist | `ou_96c1622be4c5efd17929c0d2ba5d3f99` | 新闻资讯、市场动态、图片、音乐、视频、文案 |

## File Structure

```
agent-swarm/
├── SKILL.md                    # This file
├── configs/
│   ├── team.yaml               # 团队配置模板
│   └── roles/
│       ├── master.yaml        # Master 角色定义
│       ├── specialist.yaml     # Specialist 角色定义
│       ├── critic.yaml         # Critic 角色定义
│       └── router.yaml         # Router 角色定义
└── examples/
    ├── workflow-basic.yaml      # 基础工作流示例
    └── workflow-research.yaml   # 研究任务工作流示例
```
