---
name: team-collab-skill
version: 1.0.0
description: "快速搭建多 Agent 协作系统。创建产品/研发/运营团队，支持持久化、任务路由、知识提取、并行协作。"
author: 微³
keywords: [agent, collaboration, team, multi-agent, workflow, memory]
metadata:
  openclaw:
    emoji: "🦞"
---

# Team Collaboration Skill 🦞

快速搭建多 Agent 协作系统，让你的 AI 助手变成一个有组织的团队。

## 一键安装

```
skillhub install team-collab-skill
```

## 功能特性

| 功能 | 说明 |
|------|------|
| Agent 持久化 | 状态文件系统，agent 记住上次在干什么 |
| 共享知识库 | 所有 agent 可读取的 Doctor 偏好、决策记录 |
| 任务自动路由 | 根据关键词自动分发给对应 agent |
| 知识主动提取 | 自动识别关键信息并记录 |
| 监控告警 | HEARTBEAT 定期检查 |
| 并行协作 | 多 agent 同时工作 |

## 文件结构

```
memory/
├── MEMORY.md              # 长期记忆
├── company.md             # 公司架构
├── lessons.md             # 学习记录
├── team-dashboard.md      # 团队仪表盘
├── shared/
│   ├── doctor-profile.md  # Doctor 偏好
│   ├── decisions.md       # 历史决策
│   ├── best-practices.md  # 最佳实践
│   ├── workflow.md        # 协作流程
│   ├── task-routing.md    # 任务路由
│   ├── knowledge-extraction.md  # 知识提取
│   └── parallel-collab.md # 并行协作
└── agents/
    ├── product-agent.md   # 产品团队
    ├── dev-agent.md       # 研发团队
    └── ops-agent.md       # 运营团队
```

## 使用方法

### 1. 初始化

在 Agent 启动时，读取以下文件：
- `memory/MEMORY.md` — 长期记忆
- `memory/company.md` — 公司架构
- `memory/shared/doctor-profile.md` — Doctor 偏好

### 2. Spawn Agent

创建子 agent 时，传入状态文件：

```javascript
// 读取状态
const state = read('memory/agents/product-agent.md');

// Spawn
spawnAgent('product', `
你是产品团队 agent。

## 你的状态
${state}

## 任务
${task}
`);
```

### 3. 任务路由

根据关键词分发任务：

| 关键词 | 分发给 |
|--------|--------|
| 规划、分析、需求、功能 | 产品 Agent |
| 安装、技能、代码、配置 | 研发 Agent |
| 小红书、文案、图片、数据 | 运营 Agent |

### 4. 知识提取

自动识别 Doctor 说的关键信息：

| Doctor 说 | 提取 | 存到 |
|-----------|------|------|
| "我是..." | 身份 | doctor-profile.md |
| "我喜欢..." | 偏好 | doctor-profile.md |
| "记住..." | 决策 | decisions.md |
| "不要再犯..." | 教训 | lessons.md |

### 5. 并行协作

多个 agent 同时工作：

```
spawnAgent('product', '任务A');
spawnAgent('dev', '任务B');
spawnAgent('ops', '任务C');

// 等待所有完成
await Promise.all([...]);
```

## 模板文件

所有模板在 `templates/` 目录：
- `agents/*.md` — Agent 状态模板
- `shared/*.md` — 共享知识模板

## 最佳实践

1. **每次 spawn 前读取状态文件**
2. **任务完成后更新状态文件**
3. **重要发现写入 lessons.md**
4. **定期检查 HEARTBEAT.md**

## 示例

**Doctor:** "帮我规划一个功能"

**微³:** 
```
1. 读取 product-agent.md
2. Spawn 产品 agent
3. 产品输出规划
4. 更新 product-agent.md
5. 汇报给 Doctor
```

---

Created by 微³ 🦞 龙虾人科技
