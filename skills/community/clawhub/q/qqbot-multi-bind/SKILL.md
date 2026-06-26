---
name: qqbot-multi-bind
description: 快速配置 OpenClaw 多 QQBot 账号绑定到不同 Agent。用于首次安装 QQBot、新增 QQBot 账号、创建 agent 绑定关系、重启 gateway 使配置生效。当用户需要安装 QQBot 插件、添加新的 QQBot 机器人或配置多账号路由时使用此技能。
---

# QQBot 多账号绑定配置

## 配置格式说明

`channels.qqbot.accounts` 使用**对象格式**，每个 accountId 作为 key：

```json
"accounts": {
  "<account-id>": {
    "enabled": true,
    "appId": "<app-id>",
    "clientSecret": "<secret>"
  }
}
```

- 顶层 `appId`/`clientSecret` 是默认账户（accountId = "default"）
- `accounts` 下的每个 key 就是该账户的 accountId
- 每个账户可独立配置 `enabled`、`name`、`allowFrom`、`systemPrompt` 等

---

## 首次安装 QQBot（从零开始）

### Step 1 — 在 QQ 开放平台创建机器人

1. 访问 [QQ 开放平台](https://bot.q.qq.com/)，用手机 QQ 扫码登录
2. 点击「创建机器人」
3. 记录 **AppID** 和 **AppSecret**（AppSecret 只显示一次，务必保存好）

⚠️ 注意：创建后机器人会出现在 QQ 消息列表，但会回复"机器人去火星了"，需完成配置才能正常使用。

### Step 2 — 安装插件

**方式 A：npm 安装（推荐）**
```bash
openclaw plugins install @tencent-connect/openclaw-qqbot
```

**方式 B：源码一键安装**
```bash
git clone https://github.com/tencent-connect/openclaw-qqbot.git && cd openclaw-qqbot
bash ./scripts/upgrade-via-source.sh --appid YOUR_APPID --secret YOUR_SECRET
```

**方式 C：手动安装**
```bash
git clone https://github.com/tencent-connect/openclaw-qqbot.git && cd openclaw-qqbot
npm install --omit=dev
openclaw plugins install .
```

### Step 3 — 配置 OpenClaw

**CLI 方式（推荐）**
```bash
openclaw channels add --channel qqbot --token "AppID:AppSecret"
```

**手动编辑配置文件**

编辑 `~/.openclaw/openclaw.json`：
```json
{
  "channels": {
    "qqbot": {
      "enabled": true,
      "appId": "Your AppID",
      "clientSecret": "Your AppSecret"
    }
  }
}
```

### Step 4 — 启动测试
```bash
openclaw gateway
```

---

## 多账号配置（新增第二个机器人）

### 前置条件

- 已有 OpenClaw 安装并运行
- 已有 qqbot 插件安装
- 已有至少一个 agent（如 `main`）
- 新的 QQBot AppID 和 ClientSecret

### 方式一：CLI 命令添加（推荐）

```bash
openclaw channels add --channel qqbot --account <account-id> --token "AppID:AppSecret"
```

示例：
```bash
openclaw channels add --channel qqbot --account bot2 --token "222222222:secret-of-bot-2"
```

然后添加 agent 绑定：
```bash
openclaw agents add <agent-name>  # 如需要新 agent
```

编辑 `~/.openclaw/openclaw.json`，在 `bindings` 中添加：
```json
{
  "agentId": "<agent-id>",
  "match": {
    "channel": "qqbot",
    "accountId": "<account-id>"
  }
}
```

### 方式二：手动编辑配置

#### 1. 创建新 Agent（如需要）
```bash
openclaw agents add <agent-name>
```

#### 2. 编辑 `~/.openclaw/openclaw.json`

**添加账号到 accounts**：
```json
"channels": {
  "qqbot": {
    "enabled": true,
    "allowFrom": ["*"],
    "accounts": {
      "main": {
        "enabled": true,
        "appId": "1903000001",
        "clientSecret": "your-secret-here"
      },
      "<new-account-id>": {
        "enabled": true,
        "appId": "<new-app-id>",
        "clientSecret": "<new-secret>"
      }
    }
  }
}
```

**添加路由到 bindings**：
```json
"bindings": [
  {
    "agentId": "main",
    "match": { "channel": "qqbot", "accountId": "main" }
  },
  {
    "agentId": "<agent-id>",
    "match": { "channel": "qqbot", "accountId": "<new-account-id>" }
  }
]
```

#### 3. 重启并验证
```bash
openclaw gateway restart
openclaw agents list --bindings
```

---

## 完整示例配置

```json
{
  "agents": {
    "list": [
      { "id": "main", "model": "bailian/kimi-k2.5" },
      { "id": "coding", "model": "bailian/kimi-k2.5" },
      { "id": "notify", "model": "bailian/kimi-k2.5" }
    ]
  },
  "channels": {
    "qqbot": {
      "enabled": true,
      "allowFrom": ["*"],
      "accounts": {
        "main": { "enabled": true, "appId": "1903000001", "clientSecret": "secret-1" },
        "coding": { "enabled": true, "appId": "1903000002", "clientSecret": "secret-2" },
        "notify": { "enabled": true, "appId": "1903000003", "clientSecret": "secret-3" }
      }
    }
  },
  "bindings": [
    { "agentId": "main", "match": { "channel": "qqbot", "accountId": "main" } },
    { "agentId": "coding", "match": { "channel": "qqbot", "accountId": "coding" } },
    { "agentId": "notify", "match": { "channel": "qqbot", "accountId": "notify" } }
  ]
}
```

---

## 常见问题

**Q: 一个 agent 可以绑定多个 QQBot 吗？**
A: 可以！添加多个 bindings 指向同一个 agentId。

**Q: 一个 QQBot 可以发给多个 agent 吗？**
A: 不可以，一个消息只能路由到一个 agent。

**Q: 如何删除某个 QQBot？**
A: 从 `accounts` 和 `bindings` 中删除对应条目，重启 gateway。

**Q: 如何与另一个 agent 对话？**
A: `openclaw agent --agent <agent-name> --message "你的消息"`

**Q: 如何启用跨 agent 会话访问？**
A: 在 `openclaw.json` 中添加：
```json
{
  "tools": {
    "sessions": {
      "visibility": "all"
    }
  }
}
```
然后重启 gateway。
