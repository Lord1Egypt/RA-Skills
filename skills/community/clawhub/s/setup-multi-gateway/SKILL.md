# Multi-Gateway Setup Skill - 多网关配置技能

## 用途

当用户需要配置多个独立的 OpenClaw 网关实例时使用此技能。每个网关对应独立的 Agent、Workspace 和机器人。

## 🤖 多 Agent 协作架构

本技能配合 [`feishu-agent-send`](https://clawhub.com/skills/feishu-agent-send) 技能，实现完整的多 Agent 自主协作系统：

```
┌─────────────┐
│  Agent-A    │  统筹协调者
│  (19922)    │  - 接收用户指令
│             │  - 分解任务给其他 Agent
└─────┬───────┘
      │ sessions_send
      ▼
┌─────────────┐
│  Agent-B    │  执行助手
│  (19923)    │  - 接收 Agent-A 派发的任务
│             │  - 执行完成后调用 feishu-agent-send
└─────────────┘  - 自主汇报结果给用户
         │
         │ (飞书消息显示对应机器人名字)
         ▼
    ┌─────────
    │  用户   │
    └─────────
```

### 协作流程

1. **Agent-A 接收指令** → 用户发送任务给 Agent-A
2. **任务分解** → Agent-A 使用 `sessions_send` 派发给 Agent-B/C
3. **自主执行** → Agent-B/C 独立完成任务
4. **自主汇报** → Agent-B/C 调用 `feishu-agent-send` 用自己的身份发送结果
5. **用户感知** → 飞书显示对应机器人名字（如"小助手"/"运维助手"）

### 核心优势

- ✅ **身份隔离** - 每个 Agent 用自己的飞书应用发送消息，显示不同机器人名字
- ✅ **自主汇报** - 执行 Agent 完成后主动汇报，无需 Agent-A 转发
- ✅ **职责清晰** - 用户知道是哪个 Agent 完成的任务
- ✅ **解耦设计** - Agent-A 不阻塞，派发任务后可继续处理其他请求

## 🎯 适用场景

- ✅ 需要多个独立机器人（如：管理机器人 + 客服机器人 + 运维机器人）
- ✅ 隔离不同用途的 Agent（如：个人助理 + 工作助手）
- ✅ 为不同用户/团队创建独立的 AI 实例
- ✅ 测试不同配置而不影响生产环境

## 📋 前置检查

在开始之前，确认以下条件：

```bash
# 1. 检查 OpenClaw 版本
openclaw --version
# 需要 2026.3.3 或更高

# 2. 检查可用端口
netstat -tlnp | grep openclaw
# 确保目标端口未被占用

# 3. 检查磁盘空间
df -h ~/.openclaw
# 建议至少 1GB 可用空间

# 4. 检查内存
free -h
# 每个网关约占用 500-600MB 内存，确保有足够内存
```

---

## 🚀 快速开始

### 使用交互式向导（推荐）

```bash
openclaw mg
```

向导会自动：
1. ✅ 动态检测存在的配置文件
2. ✅ 让你选择配置来源
3. ✅ 自动复制并替换配置
4. ✅ 创建 systemd 服务
5. ✅ 可选跳过飞书配置（纯本地使用）

---

## 📖 完整文档

### 配置详解

#### 1. 网关配置结构

每个网关有独立的配置文件：

```json
{
  "agents": {
    "list": [{
      "id": "agent-a",
      "name": "Agent A",
      "workspace": "/home/admin/.openclaw/workspace-agent-a"
    }],
    "defaults": {
      "model": { "primary": "dashscope-coding/qwen3.5-plus" },
      "workspace": "/home/admin/.openclaw/workspace-agent-a"
    }
  },
  "gateway": {
    "port": 19925,
    "auth": {
      "mode": "token",
      "token": "agent-a-token-19925"
    }
  },
  "channels": {
    "feishu": {
      "enabled": true,
      "appId": "cli_xxx",
      "dmPolicy": "open"
    }
  },
  "tools": {
    "sessions": { "visibility": "all" },
    "agentToAgent": { "enabled": true }
  }
}
```

#### 2. 关键配置项

| 配置 | 说明 | 推荐值 |
|------|------|--------|
| `gateway.port` | 网关端口 | 19900-29999 |
| `channels.feishu.dmPolicy` | 私聊策略 | open/pairing |
| `channels.feishu.streaming` | 流式输出 | true |
| `tools.sessions.visibility` | 会话可见性 | all (统筹 Agent) |
| `tools.agentToAgent.enabled` | 跨 Agent 通信 | true (统筹 Agent) |

---

### 典型部署架构

| Agent | 端口 | Workspace | 用途 |
|-------|------|-----------|------|
| Agent-A | 19922 | workspace-agent-a | 统筹协调 |
| Agent-B | 19923 | workspace-agent-b | 执行助手 |
| Agent-C | 19930 | workspace-agent-c | 运维专家 |

> 💡 **提示**: 端口和名称可以根据需求自定义，mg 向导会自动检测可用端口。

---

### 跨 Agent 通信

#### 配置要求

在每个需要通信的 Agent 配置中添加：

```json
{
  "tools": {
    "sessions": { "visibility": "all" },
    "agentToAgent": { "enabled": true }
  }
}
```

#### 发送消息

```javascript
// Agent-A → Agent-B
sessions_send({
  sessionKey: "agent:agent-b:feishu:direct:ou_xxx",
  message: "请检查文档服务状态",
  timeoutSeconds: 0
})

// Agent-A → Agent-C
sessions_send({
  sessionKey: "agent:agent-c:feishu:direct:ou_xxx",
  message: "请检查系统负载",
  timeoutSeconds: 60
})
```

#### 会话 Key 格式

```
agent:{agentId}:{channel}:{chatType}:{peerId}
```

**示例**:
- `agent:agent-b:feishu:direct:ou_73eb93dd20542d4f03481dabb1e01677`
- `agent:agent-c:feishu:direct:ou_xxx`

---

### 运维命令

#### 服务管理

```bash
# 启动/停止/重启
systemctl --user start openclaw-gateway-agent-a.service
systemctl --user stop openclaw-gateway-agent-a.service
systemctl --user restart openclaw-gateway-agent-a.service

# 批量操作
systemctl --user start openclaw-gateway-{agent-a,agent-b,agent-c}.service
```

#### 日志查看

```bash
# 实时日志
journalctl --user -u openclaw-gateway-agent-a.service -f

# 最近 100 条
journalctl --user -u openclaw-gateway-agent-a.service -n 100
```

#### 故障排查

```bash
# 检查端口
netstat -tlnp | grep openclaw

# 检查 OOM
dmesg | grep -i oom

# 验证配置
node -e "JSON.parse(require('fs').readFileSync('~/.openclaw/openclaw-agent-a.json'))"
```

---

### 注意事项

1. **端口唯一** - 每个网关必须使用不同端口
2. **Workspace 隔离** - 每个 Agent 独立工作区
3. **内存规划** - 建议网关数量不超过系统内存的 70%（单网关约 500-600MB）
4. **渠道可选** - 可以不绑定任何渠道（纯本地使用），或根据需要绑定飞书/微信/钉钉等

---

## 📚 相关文档

- OpenClaw 官方文档：https://docs.openclaw.ai
- ClawHub 技能市场：https://clawhub.com

---

**技能版本**: 1.1.2  
**作者**: pikaqiuyaya  
**许可证**: MIT
