<div align="center" style="display: flex; align-items: center; justify-content: center; gap: 16px; flex-wrap: wrap;">

<img src="./images/icon.png" width="120" height="120">

<h1 style="margin: 0;">Smart Email</h1>

</div>

<!-- Language Switcher -->
> 🇨🇳 中文 | [English](./README_EN.md)

---

**AI 驱动的智能邮件管理助手** · 自动管理多邮箱 · 智能判断紧急邮件 · 多渠道推送

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.8+-green.svg)](https://www.python.org/)
[![OpenClaw](https://img.shields.io/badge/OpenClaw-Skill-orange.svg)](https://github.com/openclaw/openclaw)

---

## ✨ 功能特性

- **📬 多邮箱统一管理** — 同时接入 QQ、126、163、Outlook 多个邮箱
- **🤖 AI 自动分类** — 自动判断每封邮件是否紧急，无需手动筛选
- **📲 消息推送** — 紧急邮件和每日摘要自动推送到 Telegram / 飞书 / 钉钉等
- **💾 本地归档** — 邮件原文、Markdown、附件全部存档，随时可查
- **🖼️ 图片理解** — 可选开启，AI 能读懂邮件中的截图和照片

---

## 💬 Telegram 使用示例

接入 Telegram 后，Smart Email 会这样推送给你：

### 🚨 紧急邮件通知

<img src="./images/demo-urgent.png" width="400">

### 📧 每日邮件摘要

<img src="./images/demo-digest.png" width="400">

### 💬 与邮件对话

收到邮件后，你可以直接引用 `<!-- email_id: xxx -->` 与 Agent 对话，询问邮件详情、附件内容等：

<img src="./images/demo-conversation.png" width="600">

---

## 🛠️ 安装

### 自动安装（推荐）

将以下提示词发送给 OpenClaw（需包含 GitHub 仓库地址）：

```
请帮我安装 Smart Email（https://github.com/bu-bu-xxx/smart-email），
阅读 https://github.com/bu-bu-xxx/smart-email/blob/master/references/INSTALL.md 进行安装和初始化。
```

### 手动安装

```bash
# 1. 克隆仓库
cd ~/.openclaw/workspace/skills
git clone https://github.com/openclaw/smart-email.git
cd smart-email

# 2. 安装依赖
pip install -r requirements.txt

# 3. 配置环境变量
# Only copy template if ~/.openclaw/.env doesn't exist
[ -f ~/.openclaw/.env ] || cp .env.example ~/.openclaw/.env
# 编辑 ~/.openclaw/.env

# 4. 初始化
python3 -m smart_email init

# 5. 设置定时任务
python3 -m smart_email setup-cron --apply
```

---

## 🚀 快速使用

向 OpenClaw 发送以下提示词，即可开始引导配置：

```
我是新用户，想要开始使用 Smart Email，请帮我完成初始配置。
```

---

## ⚙️ 配置

```bash
# 邮箱（授权码，非登录密码）
SMART_EMAIL_QQ_EMAIL=xxx@qq.com
SMART_EMAIL_QQ_AUTH_CODE=xxx

# AI 分析方式
SMART_EMAIL_LLM_PROVIDER=openai  # openai | anthropic | subagent

# OpenAI 兼容 API
SMART_EMAIL_OPENAI_API_URL=https://api.example.com/v1
SMART_EMAIL_OPENAI_API_KEY=xxx
SMART_EMAIL_OPENAI_MODEL=gpt-4o-mini

# Anthropic API
SMART_EMAIL_ANTHROPIC_API_KEY=xxx
SMART_EMAIL_ANTHROPIC_MODEL=claude-sonnet-4-20250514

# 发送渠道
SMART_EMAIL_DELIVERY_CHANNEL=telegram  # telegram | dingtalk | feishu | wecom
SMART_EMAIL_DELIVERY_TARGET=@your_username
```

> 💡 **详细配置方法**可以随时询问 OpenClaw Agent，告诉它你在配置哪部分（如邮箱授权码、Telegram推送、AI模型等），它会逐步指导你完成。

完整配置示例见 [`.env.example`](.env.example)，配置指南参见 [USER_GUIDE](./references/USER_GUIDE.md)。

---

## 📁 目录结构

```
~/.openclaw/workspace/smart-email-data/
├── mail-archives/          # 邮件存档
│   └── 2025-03-10/
│       └── qq_20250310_143022/
│           ├── email.eml
│           ├── email.md
│           └── attachments/
├── outbox/
│   ├── pending/            # 待发送消息
│   └── sent/               # 已发送归档
├── logs/
└── data/
    └── mail_tracker.db
```

---

## 🏗️ 架构

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│    check    │     │   digest    │     │  dispatch   │
│  (每30分钟)  │     │  (每日定时)  │     │  (每5分钟)   │
└──────┬──────┘     └──────┬──────┘     └──────┬──────┘
       │                   │                   │
       ▼                   ▼                   ▼
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│  下载邮件    │     │  汇总邮件    │     │  读取 outbox │
│  AI分析紧急度 │     │  生成摘要    │     │  发送到渠道  │
│  生成urgent  │     │  生成digest  │     │  移动到sent  │
└──────┬──────┘     └──────┬──────┘     └─────────────┘
       │                   │
       └─────────┬─────────┘
                 ▼
         ┌───────────────┐
         │ outbox/pending │
         │   (消息队列)    │
         └───────────────┘
```

---

## 🔧 技术栈

- **语言**: Python 3.8+
- **依赖**: `openai`, `requests`, `python-dotenv`
- **协议**: IMAP (邮件收取)
- **平台**: [OpenClaw](https://github.com/openclaw/openclaw)

---

## 📄 License

[MIT](./LICENSE) · © 2026 [OpenClaw](https://github.com/openclaw/openclaw)
