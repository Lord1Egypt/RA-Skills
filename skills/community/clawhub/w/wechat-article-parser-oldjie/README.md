<div align="center">

# 📰 微信公众号文章解析 skill (wechat-article-parser)

### *"让 AI 帮你快速读完一篇公众号文章，不漏重点。"*

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Node.js](https://img.shields.io/badge/Node.js-22%2B-green.svg)](https://nodejs.org)
[![Playwright](https://img.shields.io/badge/Playwright-latest-blue.svg)](https://playwright.dev)

[![Claude Code](https://img.shields.io/badge/Claude%20Code-Skill-blueviolet)](https://claude.ai/code)
[![OpenClaw](https://img.shields.io/badge/OpenClaw-Skill-teal)](https://github.com/openclaw/clawhub)
[![AgentSkills](https://img.shields.io/badge/AgentSkills-Standard-green)](https://agentskills.io)

<br>

解析微信公众号文章，提取核心要点和干货。支持多种文章类型的智能总结。

[📦 安装](#-安装) · [🚀 使用](#-使用) · [🔧 依赖](#-依赖)

</div>

---

## 📦 安装

把下面这行发给你的 Agent：

> 帮我安装 wechat-article-parser skill：https://github.com/oldjie/wechat-article-parser

你的 Agent 会自动克隆仓库并安装依赖。

<details>
<summary><b>👇 手动安装（不想用 AI 装？）</b></summary>

```bash
# 克隆仓库
git clone https://github.com/oldjie/wechat-article-parser.git ~/.claude/skills/wechat-article-parser

# 安装依赖
cd ~/.claude/skills/wechat-article-parser
npm install playwright cheerio

# 安装浏览器（仅需一次）
npx playwright install chromium
```

| 平台 | 安装路径 |
|------|---------|
| OpenClaw | `~/.openclaw/workspace/skills/wechat-article-parser` |
| Claude Code | `~/.claude/skills/wechat-article-parser` |
| Codex | `~/.codex/skills/wechat-article-parser` |

</details>

---

## 🚀 使用

在支持 Skill 的 Agent 中，直接发送微信公众号文章链接即可自动触发：

```
发送：https://mp.weixin.qq.com/s/xxxxx
```

或手动执行：

```bash
node scripts/fetch-wechat.js <公众号文章链接>
```

**示例：**
```bash
node scripts/fetch-wechat.js https://mp.weixin.qq.com/s/0d8x55t1t-SWQzG7jck7Pw
```

---

## 📤 输出说明

Skill 会根据文章类型智能调整输出方式：

| 文章类型 | 输出策略 |
|---------|---------|
| 干货/资讯类 | 简洁聚焦，提取核心要点 |
| 变化/事件类 | 理清背景→变化→原因→影响→争议 |
| 发布会/产品类 | 每个产品的背景、解决的问题、逻辑关系 |
| 科普/历史/故事类 | 保留关键人物、数据、年份、具体案例 |
| 推介/评测类 | 保留趣味，不过度精简 |

---

## 🔧 依赖

| 依赖 | 说明 |
|-----|------|
| Node.js 22+ | 运行环境 |
| playwright | 浏览器自动化抓取 |
| cheerio | HTML 解析 |

---

## 📂 项目结构

```
wechat-article-parser/
├── SKILL.md              # Skill 入口（frontmatter 配置）
├── README.md             # 本文件
├── LICENSE              # MIT 协议
└── scripts/
    └── fetch-wechat.js   # 公众号文章抓取脚本
```

---

## ⭐ 相关话题

- `ai-skill`
- `agent-skill`

---

<div align="center">

**MIT License** © [oldjie](https://github.com/oldjie)

</div>
