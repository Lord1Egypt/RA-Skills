# Team Sessions

主控发号施令、成员各司其职的团队沟通流程规范。

用 `sessions_spawn` 与团队成员（子代理）高效沟通，零横向沟通，主控统一调度。

---

## ⚠️ 权限说明

本 skill 需要在 `openclaw.json` 中配置 subagent 权限，并重启 Gateway 使配置生效。

**关于 `allowAgents: ["*"]`**：这是 OpenClaw 标准配置，允许主控 spawn 子代理。`["*"]` 表示允许所有 agentId，不等于"所有 agent 都有权限"——子代理权限仍由主控控制。如果有特殊需求，可改为只列出需要的 agentId（如 `["analyst","writer"]`）。

---

## 特性

- **零横向沟通**：成员只与主代理通信，不互相打扰
- **Workspace 隔离**：每个成员独立 workspace，人格不串
- **标准流程**：判断类型 → 构造任务包 → 派发 → 等待结果
- **通用适配**：支持任意数量成员，不限定具体角色

## 快速开始

### 1. 安装

```bash
clawhub install team-sessions
```

### 2. 配置成员

```bash
# 创建成员 workspace
mkdir -p ~/.qclaw/workspace-main/{analyst,writer,reviewer}

# 写入成员 SOUL.md
echo "你是分析师，负责数据分析..." > ~/.qclaw/workspace-main/analyst/SOUL.md
echo "你是写手，负责内容创作..." > ~/.qclaw/workspace-main/writer/SOUL.md
```

### 3. 配置 openclaw.json

```json
{
  "agents": {
    "defaults": {
      "subagents": {
        "allowAgents": ["*"]
      }
    },
    "list": {
      "analyst": {
        "agentId": "analyst",
        "workspace": "~/.qclaw/workspace-main/analyst"
      },
      "writer": {
        "agentId": "writer",
        "workspace": "~/.qclaw/workspace-main/writer"
      }
    }
  }
}
```

### 4. 使用

对 Agent 说：

> 派分析师做竞品分析

Agent 自动执行：
```javascript
sessions_spawn({
  agentId: "analyst",
  cwd: "~/.qclaw/workspace-main/analyst",
  task: "...",
  mode: "run"
})
```

---

## 适用场景

- 内容创作团队（策划→写手→审核）
- 数据分析团队（采集→清洗→分析）
- 软件开发团队（设计→开发→测试）
- 任何需要分工协作的任务

---

## 版本

- v1.0.1（2026-04-24）— 补充权限说明，澄清 allowAgents 的实际影响
