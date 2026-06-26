---
name: wecom-channel-fix
description: 企业微信通道配置诊断与修复。当用户遇到企微通道无法连接、配置错误、插件 ID 不匹配、多账号模式不支持等问题时激活。支持配置检测、自动修复、单账号/多账号模式切换。
version: 1.0.0
license: MIT
author: OpenClaw Community
homepage: https://github.com/YOUR_USERNAME/openclaw-skill-wecom-channel-fix
metadata:
  {
    "openclaw":
      {
        "emoji": "🔧",
        "always": false,
        "requires":
          {
            "bins": [],
          },
      },
  }
---

# 企业微信通道配置诊断与修复技能

当用户遇到企业微信通道无法连接、消息无回复、配置错误等问题时，使用此技能进行诊断和修复。

## 触发场景

- "企微没反应"
- "企业微信通道配置错误"
- "wecom 连不上"
- "插件 ID 不匹配"
- "多账号模式不支持"
- "企微消息无回复"

## 诊断流程

### 步骤 1：检查通道状态

```bash
openclaw channels status 2>&1
```

**判断标准：**
- `enabled, configured, running` ✅ 正常
- `enabled, not configured, stopped` ❌ 配置缺失
- `error:*` ❌ 错误状态

### 步骤 2：检查配置文件

```bash
openclaw config get channels.wecom 2>&1
```

**检查项：**
1. `botId` 是否存在
2. `secret` 是否存在
3. 是否使用了不支持的 `accounts.*` 多账号结构

### 步骤 3：检查插件配置

```bash
grep -A 10 '"plugins"' ~/.openclaw/openclaw.json
```

**常见问题：**
- 插件 ID 不匹配（配置用 `wecom-openclaw-plugin`，实际导出 `wecom`）
- 插件未启用

### 步骤 4：查看日志

```bash
cat /tmp/openclaw/openclaw-$(date +%Y-%m-%d).log | grep -i wecom | tail -20
```

**关键错误：**
- `plugin id mismatch`
- `Invalid WebSocket frame`
- `Authentication failed`
- `not configured`

---

## 修复方案

### 问题 A：插件 ID 不匹配

**症状：**
```
[plugins] plugin id mismatch (config uses "wecom-openclaw-plugin", export uses "wecom")
plugins.entries.wecom: plugin not found: wecom
```

**修复：**

将 `openclaw.json` 中的插件配置从：
```json
{
  "plugins": {
    "allow": ["wecom-openclaw-plugin"],
    "entries": {
      "wecom-openclaw-plugin": {"enabled": true}
    }
  }
}
```

改为：
```json
{
  "plugins": {
    "allow": ["wecom"],
    "entries": {
      "wecom": {"enabled": true}
    }
  }
}
```

**原因：** 企微插件的 `openclaw.plugin.json` 中定义 `id: "wecom"`，但安装包名为 `@wecom/wecom-openclaw-plugin`，配置时应使用导出 ID 而非包名。

---

### 问题 B：多账号模式不支持

**症状：**
```
wecom default: 企业微信机器人 ID 或 Secret 未配置
config reload skipped (invalid config)
```

**当前配置（错误）：**
```json
{
  "channels": {
    "wecom": {
      "enabled": true,
      "defaultAccount": "main",
      "accounts": {
        "main": {"botId": "...", "secret": "..."},
        "ai-engineer": {"botId": "...", "secret": "..."}
      }
    }
  }
}
```

**修复（回退单账号模式）：**
```json
{
  "channels": {
    "wecom": {
      "enabled": true,
      "botId": "你的 botId",
      "secret": "你的 secret",
      "dmPolicy": "pairing"
    }
  },
  "bindings": [
    {
      "agentId": "main",
      "match": {"channel": "wecom", "accountId": "*"}
    }
  ]
}
```

**原因：** 企微插件（v1.0.8）不支持多账号模式，只接受扁平的 `botId`/`secret` 配置。

---

### 问题 C：通道未配置

**症状：**
```
企业微信 default: enabled, not configured, stopped
企业微信机器人 ID 或 Secret 未配置
```

**修复：**

1. 确认已安装企微插件：
```bash
openclaw plugins list | grep wecom
```

2. 配置 botId 和 secret：
```bash
openclaw config set channels.wecom.botId <YOUR_BOT_ID>
openclaw config set channels.wecom.secret <YOUR_SECRET>
openclaw config set channels.wecom.enabled true
```

3. 重启 gateway：
```bash
openclaw gateway restart
```

---

## 完整修复脚本

当用户确认需要修复时，可执行以下操作：

### 1. 备份当前配置
```bash
cp ~/.openclaw/openclaw.json ~/.openclaw/openclaw.json.backup.$(date +%Y%m%d%H%M%S)
```

### 2. 修复插件 ID
使用 `edit` 工具将 `wecom-openclaw-plugin` 替换为 `wecom`

### 3. 修复通道配置
如使用多账号模式，回退到单账号扁平结构

### 4. 验证修复
```bash
openclaw channels status 2>&1
openclaw gateway status 2>&1
```

### 5. 测试消息
让用户在企微发送测试消息，确认回复正常

---

## 配置模板

### 单账号模式（推荐，当前插件支持）

```json
{
  "channels": {
    "wecom": {
      "enabled": true,
      "botId": "aibXXXXXXXXXXXXXXXXXX",
      "secret": "XXXXXXXXXXXXXXXXXXXXXXXX",
      "dmPolicy": "pairing",
      "allowFrom": [],
      "groupPolicy": "open"
    }
  },
  "bindings": [
    {
      "agentId": "main",
      "match": {
        "channel": "wecom",
        "accountId": "*"
      }
    }
  ]
}
```

### 多账号模式（需要插件支持，当前不可用）

```json
{
  "channels": {
    "wecom": {
      "enabled": true,
      "defaultAccount": "main",
      "accounts": {
        "main": {
          "botId": "aibXXXXXXXXXXXXXXXXXX",
          "secret": "XXXXXXXXXXXXXXXXXXXXXXXX",
          "dmPolicy": "pairing"
        },
        "agent-2": {
          "botId": "aibYYYYYYYYYYYYYYYYYY",
          "secret": "YYYYYYYYYYYYYYYYYYYYYYYY",
          "dmPolicy": "pairing"
        }
      }
    }
  },
  "bindings": [
    {
      "agentId": "main",
      "match": {"channel": "wecom", "accountId": "main"}
    },
    {
      "agentId": "agent-2",
      "match": {"channel": "wecom", "accountId": "agent-2"}
    }
  ]
}
```

> ⚠️ 注意：企微插件 v1.0.8 **不支持**多账号模式，使用上述配置会导致通道无法启动。

---

## 验证清单

修复完成后，确认以下项：

- [ ] `openclaw channels status` 显示 `enabled, configured, running`
- [ ] 日志中无 `plugin id mismatch` 警告
- [ ] 日志中 `Authentication successful`
- [ ] 企微发送测试消息能收到回复
- [ ] WebSocket 心跳正常（日志中每 30s 一次 heartbeat）

---

## 常见问题 FAQ

**Q: 为什么插件 ID 不匹配？**
A: 企微插件的包名是 `@wecom/wecom-openclaw-plugin`，但插件导出的 ID 是 `wecom`。配置时应使用导出 ID。

**Q: 多账号模式什么时候支持？**
A: 需要联系企微插件开发者添加此功能。目前只能使用单账号模式。

**Q: 如何在单账号模式下使用多个 agent？**
A: 可以通过 main 代理转发消息，或使用 Web Dashboard 直接访问不同 agent。

**Q: 配对码在哪里查看？**
A: `openclaw pairing list wecom`

**Q: 如何批准配对？**
A: `openclaw pairing approve wecom <CODE>`

---

## 参考资料

- [企微插件 GitHub](https://github.com/openclaw/wecom-openclaw-plugin)
- [企业微信 AI Bot 文档](https://open.work.weixin.qq.com/help?doc_id=21657)
- [OpenClaw 通道配置文档](https://docs.openclaw.ai/channels)

---

## 注意事项

1. **修改配置前务必备份** `openclaw.json`
2. 修改配置后需要 **重启 gateway** 才能生效
3. 多账号模式需要等待插件更新支持
4. 如修复后仍有问题，查看完整日志：`/tmp/openclaw/openclaw-YYYY-MM-DD.log`
