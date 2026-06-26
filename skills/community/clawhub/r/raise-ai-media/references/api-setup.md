# API 基础配置

## Base URL

所有 API 共用以下 Base URL：

```
https://ai.micrease.com
```

**所有 API 请求必须使用此 Base URL**，不要使用其他地址。

---

## API Key 配置

### 方式一：从 RaiseAI 获取 API Key（推荐）

1. 访问 [RaiseAI 控制台](https://ai.micrease.com) 登录账号
2. 进入「设置」→「API Key」页面
3. 点击「生成新密钥」，复制生成的 API Key（格式：`sk-xxx`）
4. 将 API Key 告诉 AI Agent：「我的 RaiseAI API Key 是 xxx」，Agent 会自动完成配置，API Key 存储在 Agent 的环境变量中

> 💡 **提示**：一个账号可以生成多个 API Key，如需区分权限可创建多个密钥。

### 方式二：OpenClaw 在配置文件中添加

在 `~/.openclaw/openclaw.json` 中添加以下配置：

```json
{
  "skills": {
    "entries": {
      "raise-ai-media": {
        "env": {
          "RAISE_AI_API_KEY": "你的APIKey"
        }
      }
    }
  }
}
```

> ⚠️ **API Key 泄露风险**：不要在公开场合（群聊、截图等）暴露你的 API Key，发现泄露请立即在控制台删除该密钥并重新生成。

---

## 认证 Header

所有请求必须在 HTTP Header 中传递：

```
Authorization: {RAISE_AI_API_KEY}
Content-Type: application/json; charset=utf-8
```

> ⚠️ 注意：`Authorization` 的值直接填入用户的 API Key，例如 `sk-079...9d6`（API Key 通常以 `sk-` 开头）。

---

## 配置清单

AI Agent 使用此技能时，需要以下配置：

| 配置项 | 说明 |
|---|---|
| RAISE_AI_API_KEY | 用户的 API Key，存储在 Agent 环境变量中。从 RaiseAI 控制台「设置」→「API Key」页面获取 |

所有配置均可通过告诉 Agent「我的 RaiseAI API Key 是 xxx」自动完成，API Key 会以环境变量形式持久化，无需手动填写。
