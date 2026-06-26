# SkillHub Daily · 每日 Skill 智能推荐

> 每日扫描 SkillHub (skillhub.cn) 全站 Top100 + 7 大分类，基于你的痛点精准推荐高价值 Skill。
> Daily scan of SkillHub, personalized recommendations based on your pain points.

[🇨🇳 中文](#中文) · [🇺🇸 English](#english)

---

## 中文

### ✨ 这是什么

**SkillHub Daily** 是一个 Agent Skill，让你的 AI 助手每天自动从 77000+ Skill 中挖出最值得安装的 3-5 个——不靠热度榜单，靠**匹配你的实际痛点**。

### 🎯 核心特点

- **痛点驱动**：先理解你需要什么，再推荐什么
- **信息差优先**：收藏率比下载量更真实——"试了就留下"比"试试就扔"更有价值
- **多通道存储**：IMA 知识库 / 飞书云文档 / Obsidian / 本地
- **双模式支持**：对话触发 / Cron 定时任务
- **跨平台**：WorkBuddy / qclaw / OpenClaw / Hermes / 纯脚本

### 📦 安装

#### 方式一：ClawHub 一键安装（推荐）

```bash
# 在 Agent 对话中
"帮我安装 skillhub-daily"
```

#### 方式二：手动安装

```bash
# qclaw
cp -r skillhub-daily/ ~/.qclaw/skills/

# WorkBuddy
cp -r skillhub-daily/ ~/.workbuddy/skills/

# OpenClaw
cp -r skillhub-daily/ ~/.openclaw/skills/

# Hermes
cp -r skillhub-daily/ ~/.hermes/skills/
```

### 🚀 快速开始

#### 1. 选择使用模式

Skill 安装后，Agent 会主动询问：

> 选 **A（常规模式）** 还是 **B（Cron 模式）**？

#### 2. 配置凭证（可选，仅 IMA 推送需要）

编辑 `references/config.json`：

```json
{
  "ima_client_id": "<your_client_id>",
  "ima_api_key": "<your_api_key>",
  "ima_kb_id": "<your_kb_id>"
}
```

#### 3. 触发使用

对话中输入：

- "每日推荐"
- "SkillHub 日报"
- "看看有什么好 Skill"
- "帮我推荐技能"

### ⏰ Cron 定时任务

**qclaw 飞书推送**（每日 07:00）：

```json
{
  "schedule": { "kind": "cron", "expr": "0 7 * * *", "tz": "Asia/Shanghai" },
  "sessionTarget": "isolated",
  "payload": {
    "kind": "agentTurn",
    "message": "请执行 skillhub-daily Skill，按 SKILL.md 步骤 1-7 完成每日推荐。\n\n# 痛点（请直接使用）\n- YouTube 字幕提取\n- 股票分析\n- n8n 工作流\n- Markdown 转换\n- 桌面自动化\n- 文档管理\n\n# 存储\n飞书云文档\n\n请完成后输出 200 字以内的对话摘要。"
  },
  "delivery": { "mode": "announce", "channel": "feishu" }
}
```

更多模板见 [references/prompt-templates.md](references/prompt-templates.md)

### 📚 文档

| 文档 | 说明 |
|------|------|
| [references/setup-wizard.md](references/setup-wizard.md) | 首次安装模式选择 |
| [references/platform-adapters.md](references/platform-adapters.md) | 跨平台适配 |
| [references/prompt-templates.md](references/prompt-templates.md) | Cron 提示词模板 |
| [references/briefing-template.md](references/briefing-template.md) | 简报格式 |
| [references/config.md](references/config.md) | 用户配置 |
| [references/source-contract.md](references/source-contract.md) | API 契约 |

### 📊 简报示例

```markdown
# SkillHub 每日简报 | 2026-06-03

基于您的记忆痛点（[痛点1]、[痛点2]、[痛点3]）个性化推荐

## 今日推荐（为您精选）

### 1. [技能名称] — [价值描述]

**匹配痛点**：[痛点]

[推荐理由]

**核心能力**：[能力1] → [能力2] → [能力3]

**安装**：`skillhub install [slug]`

## 被埋没的金子 Top 5
| 排名 | 技能名称 | 收藏率 | 埋没原因 | 爆发潜力 |
|------|---------|--------|----------|----------|
| #N | 名称 | X.XX% | 原因 | 高 |

## 全站潜力 Top 10
| 排名 | 技能名称 | 分类 | 收藏率 | 潜力分 | 推荐理由 |
|------|---------|------|--------|--------|----------|
| 1-10 | 名称 | 分类 | X.XX% | XX.XX | 20 字理由 |
```

### 🤝 贡献

欢迎 PR！参见 [CONTRIBUTING.md](docs/CONTRIBUTING.md)

### 📄 License

MIT © [SkillHub-Community](https://github.com/skillhub-community)

---

## English

### ✨ What is this

**SkillHub Daily** is an Agent Skill that makes your AI assistant automatically mine the 3-5 most valuable skills from 77,000+ every day—**not by popularity rankings, but by matching your real pain points**.

### 🎯 Core Features

- **Pain-point driven**: Understand what you need first, then recommend
- **Information edge first**: Star rate is more honest than download count—"tried and kept" beats "tried and dropped"
- **Multi-channel storage**: IMA knowledge base / Lark docs / Obsidian / local
- **Dual mode**: Interactive trigger / Cron scheduled task
- **Cross-platform**: WorkBuddy / qclaw / OpenClaw / Hermes / pure script

### 📦 Installation

#### Option 1: ClawHub one-click install (recommended)

```bash
# In your Agent conversation
"Help me install skillhub-daily"
```

#### Option 2: Manual install

```bash
# qclaw
cp -r skillhub-daily/ ~/.qclaw/skills/

# WorkBuddy
cp -r skillhub-daily/ ~/.workbuddy/skills/

# OpenClaw
cp -r skillhub-daily/ ~/.openclaw/skills/

# Hermes
cp -r skillhub-daily/ ~/.hermes/skills/
```

### 🚀 Quick Start

#### 1. Choose your mode

After Skill is installed, the Agent will ask:

> Choose **A (Interactive mode)** or **B (Cron mode)**?

#### 2. Configure credentials (optional, only for IMA push)

Edit `references/config.json`:

```json
{
  "ima_client_id": "<your_client_id>",
  "ima_api_key": "<your_api_key>",
  "ima_kb_id": "<your_kb_id>"
}
```

#### 3. Trigger usage

In conversation, say:

- "Daily recommendations"
- "SkillHub brief"
- "Show me good Skills"
- "Recommend skills for me"

### ⏰ Cron Scheduled Task

**qclaw Lark push** (daily 07:00):

```json
{
  "schedule": { "kind": "cron", "expr": "0 7 * * *", "tz": "Asia/Shanghai" },
  "sessionTarget": "isolated",
  "payload": {
    "kind": "agentTurn",
    "message": "Execute skillhub-daily Skill, follow SKILL.md steps 1-7.\n\n# Pain points (use directly)\n- YouTube subtitle extraction\n- Stock analysis\n- n8n workflow\n- Markdown conversion\n- Desktop automation\n- Document management\n\n# Storage\nLark cloud document\n\nOutput a 200-word summary when done."
  },
  "delivery": { "mode": "announce", "channel": "feishu" }
}
```

More templates: [references/prompt-templates.md](references/prompt-templates.md)

### 📚 Documentation

| Document | Description |
|----------|-------------|
| [references/setup-wizard.md](references/setup-wizard.md) | First-time mode selection |
| [references/platform-adapters.md](references/platform-adapters.md) | Cross-platform adapters |
| [references/prompt-templates.md](references/prompt-templates.md) | Cron prompt templates |
| [references/briefing-template.md](references/briefing-template.md) | Briefing format |
| [references/config.md](references/config.md) | User configuration |
| [references/source-contract.md](references/source-contract.md) | API contract |

### 📊 Briefing Example

```markdown
# SkillHub Daily Brief | 2026-06-03

Based on your memory pain points ([pain1], [pain2], [pain3])

## Today's Picks (Curated for You)

### 1. [Skill Name] — [Value description]

**Matches pain point**: [pain]

[Reasoning]

**Core capabilities**: [cap1] → [cap2] → [cap3]

**Install**: `skillhub install [slug]`

## Hidden Gems Top 5
| Rank | Skill | Star Rate | Why hidden | Potential |
|------|-------|-----------|------------|-----------|
| #N | Name | X.XX% | Reason | High |

## Site-wide Potential Top 10
| Rank | Skill | Category | Star Rate | Score | Why |
|------|-------|----------|-----------|-------|-----|
| 1-10 | Name | Cat | X.XX% | XX.XX | 20 chars |
```

### 🤝 Contributing

PRs welcome! See [CONTRIBUTING.md](docs/CONTRIBUTING.md)

### 📄 License

MIT © [SkillHub-Community](https://github.com/skillhub-community)

---

## Star History

[![Star History Chart](https://api.star-history.com/svg?repos=skillhub-community/skillhub-daily&type=Date)](https://star-history.com/#skillhub-community/skillhub-daily&Date)

## ClawHub Download History

[![ClawHub Downloads](https://img.shields.io/badge/ClawHub-skillhub--daily-blue)](https://clawhub.com/skills/skillhub-daily)

## 📊 Repository Stats

- **Version**: 6.2.0
- **License**: MIT
- **Platforms**: qclaw / WorkBuddy / OpenClaw / Hermes / pure script
- **Modes**: Interactive / Cron
- **Daily scan**: 240 skills (Top 100 + 7 categories × Top 20)
