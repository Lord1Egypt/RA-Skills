---
name: quantum-im
description: "量子密信即时通讯渠道插件。将 OpenClaw 接入量子密信平台，实现 AI 智能回复、多账号管理、安全配对等功能。支持文本、图片、文件、图文消息，群聊和私聊。"
homepage: https://github.com/openclaw/openclaw
metadata:
  {
    "openclaw":
      {
        "emoji": "📱",
        "requires": { "bins": ["node"] },
        "install":
          [
            {
              "id": "npm",
              "kind": "npm",
              "package": "quantum-im",
              "bins": ["node"],
              "label": "Install quantum-im dependencies",
            },
          ],
      },
  }
---

# 量子密信渠道插件 (Quantum IM)

将 OpenClaw 接入量子密信即时通讯平台。

## 功能特性

| 功能 | 说明 |
|------|------|
| 📝 **文本消息** | 支持普通文本、@提及、富文本 |
| 🖼️ **图片消息** | 自动上传发送，支持多种格式 |
| 📎 **文件消息** | 自动上传发送（≤30MB） |
| 📰 **图文消息** | 支持链接卡片展示 |
| 👥 **群聊支持** | 群消息接收与回复 |
| 🔐 **安全配对** | 私聊配对码验证机制 |
| 📊 **多账号** | 支持多个量子密信账号 |

---

## 何时使用

✅ **使用此插件：**

- 需要接入量子密信即时通讯平台
- 需要 AI 智能回复量子密信消息
- 需要管理多个量子密信账号
- 需要群聊或私聊安全控制

❌ **不使用此插件：**

- 使用其他 IM 平台（微信/Telegram/飞书等）
- 仅需单向消息推送（用量子推送脚本即可）

---

## 快速开始

### 1. 安装插件

```bash
# 从 ClawHub 安装
openclaw plugins install clawhub:quantum-im

# 安装依赖
cd ~/.openclaw/extensions/quantum-im
npm install
```

### 2. 配置 OpenClaw

编辑 `~/.openclaw/openclaw.json`：

```json
{
  "channels": {
    "quantum-im": {
      "enabled": true,
      "robotId": "你的机器人 ID",
      "key": "你的回调密钥",
      "host": "http://imtwo.zdxlz.com",
      "webhookPort": 3777,
      "webhookPath": "/quantum-im",
      "dmSecurity": "pairing",
      "allowFrom": [],
      "agent": "main"
    }
  },
  "plugins": {
    "entries": {
      "quantum-im": {
        "enabled": true
      }
    }
  }
}
```

### 3. 配置量子密信后台

在量子密信机器人管理后台，设置回调 URL：

```
http://<你的服务器 IP>:3777/quantum-im
```

### 4. 重启网关

```bash
openclaw gateway restart
openclaw channels status
```

---

## 配置选项

| 字段 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| `robotId` | string | ✅ | - | 量子密信机器人 ID |
| `key` | string | ✅ | - | 回调 URL 中的密钥 |
| `host` | string | ❌ | `http://imtwo.zdxlz.com` | 量子密信 API 主机 |
| `webhookPort` | number | ❌ | `3777` | webhook 监听端口 |
| `webhookPath` | string | ❌ | `/quantum-im` | webhook 路径 |
| `dmSecurity` | string | ❌ | `pairing` | 私聊安全策略 |
| `allowFrom` | string[] | ❌ | `[]` | 手机号白名单 |
| `agent` | string | ❌ | `main` | 处理消息的智能体 |

---

## 私聊安全策略

| 策略 | 说明 | 推荐场景 |
|------|------|---------|
| `pairing` | 新联系人需要配对码验证 | ✅ 推荐，平衡安全与便利 |
| `allowlist` | 只有白名单中的手机号可发消息 | 🔒 高安全，内部使用 |
| `open` | 任何人都可以发消息 | ⚠️ 慎用，可能被骚扰 |

**白名单配置示例：**
```json
{
  "dmSecurity": "allowlist",
  "allowFrom": ["13800138000", "13900139000"]
}
```

---

## 测试

### 测试 Webhook 接收

```bash
curl -X POST http://localhost:3777/quantum-im \
  -H "Content-Type: application/json" \
  -d '{
    "type": "text",
    "callBackUrl": "",
    "phone": "18800001111",
    "textMsg": { "content": "Hello OpenClaw!" }
  }'
```

**成功响应：** `{"success": true}`

### 检查状态

```bash
# 检查插件
openclaw plugins list

# 检查渠道
openclaw channels status

# 检查端口
ss -tlnp | grep 3777
```

---

## 常见问题

### Q: 收不到消息怎么办？

1. 确认插件已启用：`plugins.entries.quantum-im.enabled = true`
2. 检查端口监听：`ss -tlnp | grep 3777`
3. 检查网关日志：`openclaw logs --follow | grep quantum`
4. 验证回调 URL 配置正确

### Q: 配对码怎么获取？

首次联系时系统自动发送配对码提示。输入配对码完成验证后即可正常通信。

### Q: 如何配置多账号？

在 `accounts` 中添加多个账号配置，每个账号使用不同的 webhookPort。

---

## 故障排查

| 问题 | 可能原因 | 解决方法 |
|------|---------|---------|
| 端口未监听 | 插件未启用 | `enabled: true` |
| 收不到消息 | 回调 URL 错误 | 检查量子密信后台 |
| 发送失败 | API Key 错误 | 检查 robotId 和 key |
| 网关启动失败 | 配置错误 | `openclaw doctor --fix` |

---

## 相关资源

- [OpenClaw 官方文档](https://docs.openclaw.ai)
- [ClawHub 插件市场](https://clawhub.com)
- [GitHub 仓库](https://github.com/openclaw/openclaw)

---

## 许可证

MIT License © 2026 Michael Johnny
