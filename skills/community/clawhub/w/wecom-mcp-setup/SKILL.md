---
name: wecom-setup
description: 企业微信 MCP 配置指南。当用户需要"添加企业微信"、"配置企微"、"启用企微消息"、"设置企业微信集成"时触发。提供完整的 MCP Server 配置、权限白名单设置和 Gateway 重启指引。
---

# 企业微信 MCP 配置指南

本技能指导如何在 OpenClaw 中配置企业微信 MCP 集成，启用后可使用消息收发、待办管理、会议调度等功能。

## 前置条件

- OpenClaw 已安装并正常运行
- 企业微信管理员权限（用于获取 Corp ID、Agent ID 和 Secret）
- 可用的 wecom-mcp-server

---

## 配置步骤

### 步骤 1：添加 MCP Server

编辑 `~/.openclaw/workspace/config/mcporter.json`，在 `mcpServers` 中添加：

```json
{
  "mcpServers": {
    "wecom_mcp": {
      "command": "npx",
      "args": ["-y", "wecom-mcp-server"],
      "env": {
        "WECOM_CORP_ID": "<你的企业ID>",
        "WECOM_AGENT_ID": "<你的应用ID>",
        "WECOM_SECRET": "<你的应用密钥>"
      }
    }
  }
}
```

> **获取凭证**：登录企业微信管理后台 → 应用管理 → 选择应用 → 查看 Corp ID、Agent ID 和 Secret

### 步骤 2：配置工具权限白名单

检查当前权限配置：

```bash
openclaw config get tools.profile
```

- 如果返回 `full` → 跳过此步骤，所有工具已无限制
- 如果返回其他值 → 执行以下命令：

```bash
openclaw config set tools.alsoAllow '["wecom_mcp"]'
```

> 如果 `alsoAllow` 中已有其他工具，需要合并写入，例如：
> ```bash
> openclaw config set tools.alsoAllow '["other_tool", "wecom_mcp"]'
> ```

### 步骤 3：重启 Gateway

配置变更后必须重启 Gateway：

```bash
openclaw gateway restart
```

### 步骤 4：验证配置

重启后，可以测试 MCP 是否正常工作：

```bash
mcporter list
```

如果看到 `wecom_mcp` 在列表中，说明配置成功。

---

## 可用的企业微信 Skills

配置完成后，以下 skills 将自动可用：

| Skill | 功能 |
|-------|------|
| `wecom-msg` | 消息收发、聊天记录查看 |
| `wecom-get-todo-list` | 待办列表查询 |
| `wecom-edit-todo` | 待办创建/更新/删除 |
| `wecom-schedule` | 日程管理 |
| `wecom-meeting-create` | 会议创建 |
| `wecom-meeting-query` | 会议查询 |
| `wecom-contact-lookup` | 通讯录查询 |

---

## 故障排查

### MCP Server 无法启动

1. 检查 Node.js 版本（需要 18+）
2. 确认凭证是否正确
3. 查看 Gateway 日志：`openclaw gateway logs`

### 工具调用无权限

确认 `tools.alsoAllow` 包含 `wecom_mcp`：

```bash
openclaw config get tools.alsoAllow
```

### 找不到 openclaw 命令

- 确认 OpenClaw 已安装
- 检查 PATH 环境变量

---

## 安全提示

- **不要**将包含真实凭证的配置文件分享给他人
- 企业微信凭证应存储在本地配置文件中，不要提交到版本控制
- 定期轮换应用密钥以保证安全
