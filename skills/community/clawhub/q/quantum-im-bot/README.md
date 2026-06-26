# 量子密信渠道插件 (Quantum IM) 🚀

将 OpenClaw 接入量子密信即时通讯平台，实现 AI 智能回复、多账号管理、安全配对等功能。

---

## 🆕 更新说明

### v1.0.1 (2026-03-27)

- 修复 `openclaw status` / `openclaw health` 场景下重复启动 webhook 导致的 `EADDRINUSE: 3777` 崩溃问题。
- 调整为仅在 Gateway 运行时启动量子密信 webhook 服务，避免诊断命令抢占端口。
- 增加端口冲突容错：检测到 `3777` 已被占用时，改为复用现有监听并继续运行。

---

## ✨ 功能特性

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

## 🚀 快速开始

### 1️⃣ 安装插件

```bash
# 从 ClawHub 安装（推荐）
openclaw plugins install clawhub:quantum-im

# 或从 npm 安装
openclaw plugins install quantum-im

# 或本地安装
openclaw plugins install /path/to/quantum-im-1.0.1.tgz
```

### 2️⃣ 安装依赖

```bash
cd ~/.openclaw/extensions/quantum-im
npm install
```

### 3️⃣ 配置 OpenClaw

编辑配置文件 `~/.openclaw/openclaw.json`：

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

> 💡 **提示：** 将 `robotId` 和 `key` 替换为你的实际配置，`agent` 指定处理消息的智能体。

### 4️⃣ 配置量子密信后台

登录量子密信机器人管理后台，设置回调 URL：

```
http://<你的服务器 IP>:3777/quantum-im
```

> 📌 **注意：** 确保 3777 端口可访问，如在公网服务器需配置防火墙。

### 5️⃣ 重启网关

```bash
openclaw gateway restart
```

### 6️⃣ 验证状态

```bash
# 检查插件状态
openclaw plugins list

# 检查渠道状态
openclaw channels status

# 检查端口监听
ss -tlnp | grep 3777
```

---

## ⚙️ 配置选项

| 字段 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| `robotId` | string | ✅ | - | 量子密信机器人 ID |
| `key` | string | ✅ | - | 回调 URL 中的密钥 |
| `host` | string | ❌ | `http://imtwo.zdxlz.com` | 量子密信 API 主机地址 |
| `webhookPort` | number | ❌ | `3777` | 本地 webhook 监听端口 |
| `webhookPath` | string | ❌ | `/quantum-im` | webhook 路径 |
| `dmSecurity` | string | ❌ | `pairing` | 私聊安全策略（见下表） |
| `allowFrom` | string[] | ❌ | `[]` | 允许直接发消息的手机号白名单 |
| `agent` | string | ❌ | `main` | 处理消息的智能体 ID |

---

## 🔐 私聊安全策略

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

## 🧪 测试

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

**成功响应：**
```json
{"success": true}
```

### 测试消息发送

```bash
curl -X POST "http://imtwo.zdxlz.com/im-external/v1/webhook/send?key=YOUR_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "type": "text",
    "callBackUrl": "",
    "phone": "18800001111",
    "textMsg": {"content": "测试消息"}
  }'
```

---

## ❓ 常见问题 (FAQ)

### Q1: 安装后收不到消息怎么办？

**检查步骤：**

1. **确认插件已启用**
   ```bash
   cat ~/.openclaw/openclaw.json | grep -A5 '"quantum-im"'
   # 确保 "enabled": true
   ```

2. **检查端口监听**
   ```bash
   ss -tlnp | grep 3777
   # 应显示 LISTEN 状态
   ```

3. **检查网关日志**
   ```bash
   openclaw logs --follow | grep quantum
   # 查看是否有错误信息
   ```

4. **验证回调 URL**
   - 确认量子密信后台配置的回调 URL 正确
   - 确认服务器防火墙允许 3777 端口入站

---

### Q2: 配对码怎么获取？

首次联系时，系统会自动发送配对码提示到量子密信。

**流程：**
1. 用户发送消息到机器人
2. 机器人回复配对码提示
3. 用户在量子密信后台输入配对码
4. 完成验证，后续消息正常接收

**如需关闭配对验证：**
```json
{
  "dmSecurity": "open"
}
```

---

### Q3: 如何配置多个量子密信账号？

在 `accounts` 中添加多个账号配置：

```json
{
  "channels": {
    "quantum-im": {
      "enabled": true,
      "accounts": {
        "account1": {
          "robotId": "机器人 ID 1",
          "key": "密钥 1",
          "host": "http://imtwo.zdxlz.com",
          "webhookPort": 3777
        },
        "account2": {
          "robotId": "机器人 ID 2",
          "key": "密钥 2",
          "host": "http://imtwo.zdxlz.com",
          "webhookPort": 3778
        }
      }
    }
  }
}
```

---

### Q4: 网关重启后 3777 端口没启动？

**可能原因：**
- 插件未启用：`plugins.entries.quantum-im.enabled = false`
- 端口被占用：`ss -tlnp | grep 3777`
- 配置错误：检查 `openclaw.json` 语法

**解决方法：**
```bash
# 1. 检查配置
openclaw doctor

# 2. 修复配置
openclaw doctor --fix

# 3. 重启网关
openclaw gateway restart

# 4. 验证端口
sleep 3 && ss -tlnp | grep 3777
```

---

### Q5: 如何查看收到的消息？

**方法 1：查看网关日志**
```bash
openclaw logs --follow | grep "quantum-im"
```

**方法 2：查看 Control UI**
```
浏览器访问：http://localhost:18789
进入「Sessions」查看会话记录
```

---

### Q6: 发送图片/文件失败？

**检查项：**
- 文件大小 ≤ 30MB
- 文件路径可访问
- 量子密信 API 正常

**测试命令：**
```bash
# 检查 API 连通性
curl -I http://imtwo.zdxlz.com
```

---

## 🔧 故障排查

### 诊断命令

```bash
# 1. 检查插件状态
openclaw plugins list

# 2. 检查渠道配置
openclaw channels status

# 3. 检查端口监听
ss -tlnp | grep 3777

# 4. 查看网关日志
openclaw logs --follow

# 5. 测试 webhook
curl -X POST http://localhost:3777/quantum-im \
  -H "Content-Type: application/json" \
  -d '{"type":"text","phone":"18800001111","textMsg":{"content":"test"}}'
```

### 常见问题速查表

| 问题 | 可能原因 | 解决方法 |
|------|---------|---------|
| 端口未监听 | 插件未启用 | `enabled: true` |
| 收不到消息 | 回调 URL 错误 | 检查量子密信后台配置 |
| 发送失败 | API Key 错误 | 检查 `robotId` 和 `key` |
| 配对码不显示 | `dmSecurity` 配置 | 改为 `pairing` 或 `open` |
| 网关启动失败 | 配置语法错误 | `openclaw doctor --fix` |

---

## 📁 文件结构

```
extensions/quantum-im/
├── package.json           # 包配置
├── openclaw.plugin.json   # OpenClaw 插件配置
├── index.ts               # 主入口文件
├── README.md              # 本文档
├── package-lock.json      # 依赖锁定
└── src/
    ├── config.ts          # 配置管理
    └── api.ts             # 量子密信 API 客户端
```

---

## 📚 相关资源

- [OpenClaw 官方文档](https://docs.openclaw.ai)
- [ClawHub 插件市场](https://clawhub.com)
- [OpenClaw GitHub](https://github.com/openclaw/openclaw)
- [问题反馈](https://github.com/openclaw/openclaw/issues)

---

## 📄 许可证

MIT License © 2026 Michael Johnny

---

## 🙏 致谢

感谢 OpenClaw 社区和所有贡献者！

---

**有问题？** 欢迎提 Issue 或加入 OpenClaw 社区讨论！🦞
