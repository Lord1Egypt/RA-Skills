---
name: feishu-multi-bot
description: "OpenClaw 多飞书机器人 + 多 Agent 配置指南：一个 Gateway 实例运行多个飞书机器人，每个机器人绑定不同 Agent，实现独立工作空间、独立会话、独立人格。"
---

# SKILL.md - OpenClaw 多飞书机器人 + 多 Agent 配置指南

## 概述

在一个 OpenClaw Gateway 实例上运行多个飞书机器人，每个机器人绑定不同的 Agent（独立工作空间、独立会话、独立人格），实现一个 Gateway 服务多个飞书场景。

## 架构

```
飞书机器人A (cli_aaa) ──绑定──→ Agent: main  (🦞 私人助手, workspace-main)
飞书机器人B (cli_bbb) ──绑定──→ Agent: team  (🤖 小组助手, workspace-team)
飞书机器人C (cli_ccc) ──绑定──→ Agent: xxx   (...)
```

每个 Agent 拥有：
- 独立的工作空间（SOUL.md / AGENTS.md / USER.md）
- 独立的会话存储
- 独立的 auth profiles
- 可选的独立模型/人格

## 前置条件

- 已安装 OpenClaw Gateway
- 已在[飞书开放平台](https://open.feishu.cn/app)为每个机器人创建企业应用
- 每个应用已配置好：权限、事件订阅（长连接 `im.message.receive_v1`）、机器人能力、已发布

## 操作步骤

### 1. 创建 Agent 工作空间

为每个新 Agent 创建独立工作空间目录：

```bash
mkdir -p ~/.openclaw/workspace-<agentId>/memory ~/.openclaw/workspace-<agentId>/avatars
```

创建必要的文件：

**AGENTS.md** - Agent 行为准则
**SOUL.md** - 人格/性格定义
**TOOLS.md** - 本地工具笔记
**IDENTITY.md** - 身份信息（名字、emoji）
**USER.md** - 用户信息
**MEMORY.md** - 长期记忆（初始为空）
**HEARTBEAT.md** - 心跳配置（初始为空）

### 2. 修改配置文件

编辑 `~/.openclaw/openclaw.json`，完成三件事：

#### 2.1 飞书配置迁移到 accounts 多账号格式

```json5
{
  channels: {
    feishu: {
      enabled: true,
      defaultAccount: "default",       // 默认账号
      groupPolicy: "open",
      accounts: {
        // 保留原有的机器人
        default: {
          appId: "cli_original_app_id",
          appSecret: "original_secret",
          botName: "主机器人名称"
        },
        // 新增的机器人
        team: {
          appId: "cli_new_app_id",
          appSecret: "new_secret",
          botName: "小组机器人名称"
        },
        // 可以继续加更多...
        // support: {
        //   appId: "cli_xxx",
        //   appSecret: "xxx",
        //   botName: "客服机器人"
        // }
      }
    }
  }
}
```

> ⚠️ 如果原来用的是顶层 `appId`/`appSecret` 格式，迁移到 `accounts` 后旧字段会保留但不生效，`accounts` 格式优先。

#### 2.2 添加 Agent 列表

```json5
{
  agents: {
    defaults: {
      model: { primary: "xiaomi/xiaomi/mimo-claw-0306" },
      workspace: "/root/.openclaw/workspace",
      // ... 其他默认配置
    },
    list: [
      // main agent 不需要显式列出，它是默认的
      {
        id: "team",
        workspace: "/root/.openclaw/workspace-team",
        agentDir: "/root/.openclaw/agents/team/agent",
        identity: {
          name: "小组助手",
          emoji": "🤖"
        }
      },
      // 可以继续加更多 agent...
    ]
  }
}
```

> `main` agent 由系统自动创建，使用 `agents.defaults.workspace` 作为工作空间，不需要在 `list` 中声明（除非你想覆盖它的 identity）。

#### 2.3 添加路由绑定（bindings）

```json5
{
  bindings: [
    // 默认账号的飞书消息路由到 main agent（省略也行，main 是 fallback）
    // { agentId: "main", match: { channel: "feishu", accountId: "default" } },

    // team 账号的飞书消息路由到 team agent
    {
      agentId: "team",
      match: {
        channel: "feishu",
        accountId: "team"
      }
    },

    // 进阶：按用户/群组路由（更精确的匹配优先级更高）
    // {
    //   agentId: "team",
    //   match: {
    //     channel: "feishu",
    //     peer: { kind: "group", id: "oc_xxx" }  // 特定群组
    //   }
    // },
    // {
    //   agentId: "support",
    //   match: {
    //     channel: "feishu",
    //     peer: { kind: "direct", id: "ou_xxx" }  // 特定用户
    //   }
    // }
  ]
}
```

### 3. 重启 Gateway

```bash
openclaw gateway restart
```

或使用 `config.patch` 自动重启。

### 4. 验证

```bash
# 查看 agent 列表和绑定关系
openclaw agents list --bindings

# 查看飞书账号状态
openclaw channels status

# 查看日志
openclaw logs --follow
```

### 5. 审批配对

首次和新机器人对话时需要审批配对：

```bash
openclaw pairing list feishu
openclaw pairing approve feishu <CODE>
```

或直接配置 `dmPolicy: "open"` + `allowFrom: ["*"]` 跳过配对。

## 路由优先级

绑定匹配从高到低：

1. `peer` 匹配（精确的用户/群组 ID）
2. `parentPeer` 匹配（线程继承）
3. `guildId + roles`（Discord 角色路由）
4. `guildId` / `teamId`
5. `accountId` 匹配（飞书账号级别）
6. channel 级别匹配（`accountId: "*"`）
7. fallback 到 default agent（main）

同级别多条匹配时，配置中靠前的优先。

## 常见场景

### 场景 1：一个飞书机器人，不同用户路由到不同 Agent

```json5
bindings: [
  { agentId: "main", match: { channel: "feishu", peer: { kind: "direct", id: "ou_manager" } } },
  { agentId: "team", match: { channel: "feishu", peer: { kind: "direct", id: "ou_member" } } },
]
```

### 场景 2：群组绑定专属 Agent

```json5
bindings: [
  { agentId: "team", match: { channel: "feishu", peer: { kind: "group", id: "oc_project_x" } } },
  { agentId: "main", match: { channel: "feishu" } },  // 其余走 main
]
```

### 场景 3：多个 Agent 用不同模型

```json5
agents: {
  list: [
    {
      id: "fast",
      workspace: "~/.openclaw/workspace-fast",
      model: { primary: "xiaomi/xiaomi/mimo-claw-0306" }
    },
    {
      id: "deep",
      workspace: "~/.openclaw/workspace-deep",
      model: { primary: "deepseek/deepseek-reasoner" }
    }
  ]
}
```

## 注意事项

- 每个 Agent 的 `agentDir` 必须唯一，不能共享，否则会 auth/会话冲突
- 飞书应用需要在开放平台完成：机器人能力、权限、事件订阅（长连接）、发布审批
- `appId` 和 `appSecret` 放在配置文件中，确保文件权限安全（`chmod 600`）
- 删除 Agent 时用 `openclaw agents delete <agentId>`，会清理对应的工作空间和会话
