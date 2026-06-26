---
name: subagent-creator
description: |
  子Agent创建工具 - 用于批量创建和管理OpenClaw子Agent
  包含完整的子Agent创建流程：目录结构、配置文件、飞书集成等
  用于快速创建具有独立workspace的子Agent
metadata:
  version: 1.0.0
  author: 小乔
  usage: 使用此skill可以快速创建新的子Agent
---

# 子Agent创建工具

## 简介

用于快速创建OpenClaw子Agent的完整解决方案。包含：
- 独立workspace目录
- 专属skills配置
- 飞书channel集成
- 消息前缀规则

## 创建流程

### 1. 创建目录结构

```
E:\openclaw\agents\{agent_name}\
├── SOUL.md           # Agent身份和性格
├── MEMORY.md        # Agent记忆配置
├── AGENTS.md        # 工作准则
├── USER.md          # 用户信息
├── TOOLS.md         # 工具配置
├── HEARTBEAT.md    # 心跳配置
├── identity.md     # 身份标识
├── skills/         # 专属skills目录
│   ├── [专属skill1]
│   ├── [专属skill2]
│   ├── proactive-agent
│   ├── self-improving
│   └── agent-memory
└── .openclaw/
    └── workspace-state.json
```

### 2. 配置飞书Channel

在 `C:\Users\Administrator\.openclaw\openclaw.json` 中添加：

```json
{
  "agents": {
    "list": [
      {
        "id": "agent_name",
        "workspace": "E:\\openclaw\\agents\\agent_name",
        "agentDir": "C:\\Users\\Administrator\\.openclaw\\agents\\agent_name\\agent"
      }
    ]
  },
  "channels": {
    "feishu": {
      "accounts": {
        "agent_name": {
          "appId": "cli_xxx",
          "appSecret": "xxx",
          "botName": "Agent名字",
          "requireMention": false
        }
      }
    }
  },
  "bindings": [
    {
      "agentId": "agent_name",
      "match": {
        "channel": "feishu",
        "accountId": "agent_name"
      }
    }
  ]
}
```

### 3. 配置Skills

将需要的skills复制到agent的skills目录：

```bash
# 复制专属skills
cp -r E:\openclaw\skills\[skill_name] E:\openclaw\agents\{agent_name}\skills\

# 复制通用skills
cp -r E:\openclaw\skills\proactive-agent E:\openclaw\agents\{agent_name}\skills\
cp -r E:\openclaw\skills\self-improving E:\openclaw\agents\{agent_name}\skills\
cp -r E:\openclaw\skills\agent-memory E:\openclaw\agents\{agent_name}\skills\
```

### 4. 必需的配置

#### SOUL.md 示例

```markdown
# SOUL.md - [Agent名字]是谁

## 身份

**名字**: [Agent名字]  
**角色**: [角色描述]  
**风格**: [风格描述]

## 核心能力

- [能力1]
- [能力2]

## 性格

- [性格特点1]
- [性格特点2]

## 沟通风格

- [沟通风格描述]

## 行为准则

### 消息同步
- 每次发送任何消息时（包括任务完成、协作消息、进度通报等），都要同步发送到飞书
- 使用 message 工具发送到对应群
- 格式：[Agent名字] 消息内容
- 不要筛选，所有消息都发往飞书

### 消息格式
- 每次发送飞书消息时，开头必须加上发送者标识
- 格式：[Agent名字] 消息内容
- 例如：[搜搜] 已完成搜索任务

### 工作环境
- Skills目录: E:\\openclaw\\agents\\{agent_name}\\skills
- 禁止使用全局skills目录
```

#### MEMORY.md 示例

```markdown
# MEMORY.md - [Agent名字]的记忆

## 飞书配置
- Agent ID: cli_xxx
- Session: xxx

## 技能配置

### 专属Skills
- [skill1]: [用途]
- [skill2]: [用途]

### 通用Skills
- proactive-agent: 主动Agent能力
- self-improving: 自我反思学习
- agent-memory: 持久化记忆
```

### 5. 创建飞书Bot

1. 在飞书开放平台创建应用
2. 获取 appId 和 appSecret
3. 添加Bot到群聊
4. 配置到openclaw.json

## 使用方法

### 创建新Agent

```bash
# 1. 创建目录结构
mkdir E:\openclaw\agents\{agent_name}

# 2. 复制配置文件
# (使用subagent-creator脚本)

# 3. 更新openclaw.json配置

# 4. 重启Gateway
openclaw gateway restart
```

### 调用子Agent

```python
from openclaw import sessions_spawn

# 触发子Agent执行任务
sessions_spawn(
    label="agent_name",
    mode="run",  # 或 "session"
    runtime="subagent",
    task="任务描述"
)
```

## 已创建的子Agent示例

| Agent | 角色 | 专属Skills |
|-------|------|----------|
| sousou | 信息搜索专家 | bocha-search, ddg-search, tavily-search, summarize |
| novelist | 小说创作 | humanizer |
| prosecutor_big | 资深评论家 | novel-writer-assistant |
| prosecutor_small | 严谨评论家 | novel-writer-assistant |
| assistant | 方案整合 | - |
| clever | 创意点子 | - |

## 注意事项

1. 每个Agent必须有独立的workspace目录
2. Skills必须复制到Agent自己的skills目录
3. 飞书Bot需要单独创建和应用配置
4. 重启Gateway使配置生效
5. 使用message工具发送飞书消息时需要指定channel和target
