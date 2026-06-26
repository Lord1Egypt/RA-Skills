---
name: smart-email
description: AI智能邮件管理助手，支持 QQ、126、163、Outlook 多邮箱 IMAP 收取，本地归档，AI 智能判断紧急邮件，自动发送到用户指定渠道（Telegram/钉钉/企业微信/飞书等）。
---

# Smart Email

AI智能邮件管理助手，支持多邮箱 IMAP 收取、本地归档、**自动发送到用户指定渠道**。

## 架构

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│  smart-email    │     │  smart-email    │     │  smart-email    │
│     check       │     │    digest       │     │   dispatch      │
│  (每30分钟)      │     │ (11:00, 17:00)  │     │  (每5分钟)       │
└────────┬────────┘     └────────┬────────┘     └────────┬────────┘
         │                       │                       │
         ▼                       ▼                       ▼
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│  下载邮件        │     │  汇总邮件        │     │  读取 outbox    │
│  AI分析紧急程度  │     │  生成摘要        │     │  发送到用户渠道  │
│  生成urgent消息  │     │  生成digest消息  │     │  移动到sent     │
└────────┬────────┘     └────────┬────────┘     └─────────────────┘
         │                       │
         └───────────┬───────────┘
                     ▼
         ┌─────────────────────┐
         │   outbox/pending/   │
         │   (消息队列)         │
         └─────────────────────┘
```

## 核心功能

| 功能 | 说明 |
|------|------|
| **多邮箱支持** | QQ、126、163、Outlook |
| **定时收取** | 每 30 分钟自动检查新邮件 |
| **AI 智能判断** | 支持 OpenAI / Anthropic / Subagent 三种分析方式 |
| **自动发送** | 紧急邮件和汇总自动发送到 Telegram/钉钉/企业微信/飞书等 |
| **每日汇总** | 每日 11:00 和 17:00 生成并发送邮件摘要 |
| **本地归档** | 保存原始 .eml、Markdown 和附件 |
| **多模态分析** | 可选开启，AI 分析时输入邮件正文图片 |

## 初次使用引导

当用户表示要开始使用 Smart Email 但尚未完成配置时，Agent 应主动引导用户完成以下步骤：

1. **阅读安装指南**：Agent 自行阅读 `references/USER_GUIDE.md` 获取完整的安装配置流程
2. **协助配置环境变量**：引导用户获取邮箱授权码、填写 .env 配置
3. **引导初始化测试**：指导用户运行 `init` 和 4 步测试流程
4. **协助部署 Cron**：帮助用户执行 `setup-cron --apply` 完成定时任务配置

Agent 应主动推进流程，不要只是告诉用户"请阅读 xxx"，而是自己读完后逐步引导用户操作。

## 核心配置

```bash
# 邮箱配置（使用授权码）
SMART_EMAIL_QQ_EMAIL=xxx@qq.com
SMART_EMAIL_QQ_AUTH_CODE=xxx

# AI 配置（必填）
SMART_EMAIL_LLM_PROVIDER=openai  # openai | anthropic | subagent

# OpenAI 配置
SMART_EMAIL_OPENAI_API_URL=https://api.example.com/v1
SMART_EMAIL_OPENAI_API_KEY=xxx
SMART_EMAIL_OPENAI_MODEL=gpt-4o-mini

# Anthropic 配置
SMART_EMAIL_ANTHROPIC_API_KEY=xxx
SMART_EMAIL_ANTHROPIC_MODEL=claude-sonnet-4-20250514

# 发送渠道配置（必填）
SMART_EMAIL_DELIVERY_CHANNEL=telegram  # telegram | dingtalk | wecom | feishu
SMART_EMAIL_DELIVERY_TARGET=@username
```

完整配置见 `references/USER_GUIDE.md`。

## CLI 命令

```bash
# 初始化
python3 -m smart_email init

# 检查并分析邮件
python3 -m smart_email check
python3 -m smart_email check --test        # 测试模式

# 生成汇总
python3 -m smart_email digest
python3 -m smart_email digest --test       # 测试模式

# 分发消息
python3 -m smart_email dispatch
python3 -m smart_email dispatch --test      # 测试模式

# 设置定时任务
python3 -m smart_email setup-cron --apply

# 查询邮件
python3 -m smart_email get-email <email_id>

# 清理
python3 -m smart_email clean
python3 -m smart_email clean-test
```

## 目录结构

```
~/.openclaw/workspace/smart-email-data/
├── mail-archives/          # 邮件存档（按日期组织）
├── outbox/
│   ├── pending/            # 待发送消息
│   └── sent/               # 已发送归档
├── logs/
└── data/
    └── mail_tracker.db      # 邮件追踪数据库
```

## Outbox 消息格式

```json
{
  "id": "uuid",
  "created_at": "2026-03-18T13:15:00+08:00",
  "source": "smart-email",
  "type": "urgent|digest|error",
  "priority": "high|normal|low",
  "content": {
    "title": "🚨 紧急邮件",
    "body": "详细内容（Markdown 格式）",
    "images": ["mail-archives/2025-03-18/qq_xxx/image_001.png"],
    "attachments": ["mail-archives/2025-03-18/qq_xxx/合同.pdf"]
  },
  "context": {
    "related_emails": ["qq_20250318_132700"],
    "mail_count": 1
  }
}
```

## Agent 使用指南

当用户引用 Digest 或紧急邮件内容询问具体邮件时：

### 步骤1：提取邮件ID

从消息底部注释提取：`<!-- email_id: xxx -->` 或 `<!-- email_ids: xxx, yyy -->`

### 步骤2：查询原文件

```bash
python3 -m smart_email get-email <邮件ID>
```

### 步骤3：读取邮件内容

| 文件类型 | 用途 |
|---------|------|
| `.md` | **推荐阅读**，格式清晰 |
| `.eml` | 原始邮件格式 |
| `attachments/` | 附件目录 |

### 完整示例

**用户**：`<!-- email_id: qq_20250321_143022 --> 这封邮件的附件是什么？`

**处理流程**：
1. 提取邮件ID：`qq_20250321_143022`
2. 运行查询命令
3. 检查 `attachments/` 目录
4. 回答用户

## 邮件ID说明

邮件ID格式：`{邮箱类型}_{YYYYMMDD}_{HHMMSS}`
示例：`qq_20250321_143022`

### 紧急邮件消息

```
🚨 紧急邮件

📧 [03-21 14:30] lihui@company.com
📌 主题：面试邀请

⚠️ 紧急原因：来自重要联系人

📝 摘要：贵公司邀请您参加面试...

<!-- email_id: qq_20250321_143022 -->
```

### Digest 汇总

```
📧 邮件摘要 (2025-03-21)

📌 重要 (3封)
📧 [03-21 14:30] lihui@company.com
   面试邀请
...

📎 共5封新邮件

<!-- email_ids: qq_20250321_143022, qq_20250321_150045, ... -->
```
