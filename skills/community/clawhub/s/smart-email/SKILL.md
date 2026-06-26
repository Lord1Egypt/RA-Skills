---
name: smart-email
description: Email assistant skill — check emails, AI summaries, daily digests. Supports Gmail, Outlook/M365, Google Workspace. Users interact through their chat platform (Telegram, Feishu, WhatsApp, etc.).
homepage: https://clawhub.ai/skills/smart-email
metadata: {"clawdbot":{"emoji":"📧","requires":{"bins":["node"]},"install":[{"id":"npm","kind":"npm","cwd":"__skill__","label":"Install dependencies"}]}}
---

# Smart Email — 邮件助手

让用户通过聊天（Telegram / 飞书 / WhatsApp）管理邮箱，查看邮件，获取 AI 摘要和每日日报。

## 用户可以说什么（意图识别）

当用户发送以下类型的消息时，使用此 skill：

| 用户说的话 | 执行的命令 |
|---|---|
| "查邮件" / "有新邮件吗" / "check email" | `check --summarize` |
| "查看 xxx@gmail.com 的邮件" | `check --summarize --account xxx@gmail.com` |
| "最近3天的邮件" | `check --summarize --since 4320` |
| "邮件日报" / "今天邮件总结" / "email digest" | `digest` |
| "读一下这封邮件" + uid | `read <uid>` |
| "添加邮箱" / "设置邮箱" / "setup email" | → 引导 setup 流程 |
| "删除邮箱 xxx" | `remove xxx@gmail.com` |
| "我有哪些邮箱" / "邮箱列表" | `accounts` |
| "设置 API Key" / "配置 AI" | → 引导 config 流程 |

## CLI

所有命令通过此路径执行，输出 JSON：

```bash
node <SKILL_DIR>/cli.js <command> [options]
```

`<SKILL_DIR>` 是此 skill 的安装目录。

## 命令参考

### check — 查看新邮件

```bash
node <SKILL_DIR>/cli.js check [--summarize] [--account EMAIL] [--since MINUTES] [--max N]
```

- `--summarize` — 包含 AI 摘要（推荐默认开启）
- `--since M` — 回看 M 分钟（默认 60）
- `--max N` — 最多返回 N 封（默认 10）
- `--account EMAIL` — 只查指定邮箱

输出示例：
```json
{
  "emails": [
    {
      "account": "user@gmail.com",
      "uid": "12345",
      "from": "Boss",
      "subject": "Q1 Report",
      "date": "2026-03-12T10:00:00Z",
      "bodyPreview": "Please review...",
      "summary": "🔴 老板要你审核 Q1 报告，需要尽快回复"
    }
  ],
  "total": 1
}
```

**格式化回复建议**：按邮件逐条展示，包含发件人、主题、AI摘要。标注重要程度。

### read — 读取邮件全文

```bash
node <SKILL_DIR>/cli.js read <uid> [--account EMAIL]
```

返回邮件全文 + AI 解读。

### digest — 邮件日报

```bash
node <SKILL_DIR>/cli.js digest [--since MINUTES] [--account EMAIL]
```

- `--since M` — 回看时间（默认 1440 = 24小时）

返回 AI 生成的邮件总结，按紧急/关注/可忽略分类。

### accounts — 查看已配置邮箱

```bash
node <SKILL_DIR>/cli.js accounts
```

### setup — 添加邮箱

```bash
# Gmail / Google Workspace
node <SKILL_DIR>/cli.js setup <email> --password <APP_PASSWORD>

# Outlook / M365 (OAuth2)
node <SKILL_DIR>/cli.js setup <email> --auth oauth

# Outlook / M365 (App Password)
node <SKILL_DIR>/cli.js setup <email> --auth password --password <APP_PASSWORD>
```

**引导用户的流程**：

1. 问用户邮箱地址
2. 自动检测类型（Gmail / Outlook / Workspace）
3. 如果是 Gmail/Workspace：
   - 告诉用户需要 App Password
   - 指导：Google 账户 → 安全性 → 两步验证 → 应用专用密码
   - 用户提供后执行 setup
4. 如果是 Outlook/M365：
   - 推荐 OAuth2（更安全，不需要密码）
   - 执行 `setup <email> --auth oauth`，会返回一个链接和验证码
   - 告诉用户在浏览器打开链接、输入验证码
   - 等待授权完成
5. 其他邮箱：问用户密码/App Password

### remove — 删除邮箱

```bash
node <SKILL_DIR>/cli.js remove <email>
```

### config — 配置

```bash
# 查看当前配置
node <SKILL_DIR>/cli.js config

# 设置 AI API Key（必需，用于邮件摘要）
node <SKILL_DIR>/cli.js config ai_api_key <KEY>

# 设置 API 地址和模型（可选）
node <SKILL_DIR>/cli.js config ai_api_base https://api.deepseek.com
node <SKILL_DIR>/cli.js config ai_model deepseek-chat

# Microsoft OAuth2 配置（Outlook 用户需要）
node <SKILL_DIR>/cli.js config ms_client_id <CLIENT_ID>
node <SKILL_DIR>/cli.js config ms_tenant_id <TENANT_ID>
```

## Web UI（可选）

提供浏览器界面，适合不喜欢命令行的用户：

```bash
node <SKILL_DIR>/server.js [--port 3900]
```

启动后会显示带 token 的 URL，打开即可在浏览器中配置和使用。

## 首次使用检查

当用户第一次使用邮件相关功能时，检查：

1. `accounts` 是否有已配置邮箱？没有 → 引导 setup
2. `config` 是否有 `ai_api_key`？没有 → 提示需要配置 AI Key（否则没有摘要功能）

## 数据存储

- 邮箱凭证：`<SKILL_DIR>/data/email.db`（SQLite，本地加密存储）
- 配置：`<SKILL_DIR>/data/config.json`
- 所有数据仅存在用户本地，不上传
