# Session Branch — 会话分叉

[![版本](https://img.shields.io/badge/版本-1.1.0-blue)](https://github.com/EdwardWason/session-branch)
[![许可证](https://img.shields.io/badge/许可证-MIT--0-green)](LICENSE)
[![ClawHub](https://img.shields.io/badge/ClawHub-session--branch-orange)](https://clawhub.ai/skills/session-branch)

将当前编码会话分叉到新对话，完整保留上下文。自动生成结构化交接文档、启动提示词，引导新会话无缝接续。

## 为什么需要

长对话中 LLM 上下文压缩会降低质量。你想开新对话，但不想丢失所有知识、决策和代码上下文。Session Branch 通过生成一份完整的交接文档，让新 AI 会话可以"热启动"你的项目。

## 功能

- **结构化交接文档** — 12 节模板，覆盖项目身份、决策链、数据流、能力边界、代码变更、平台状态等
- **验证检查清单** — 12 大类 40+ 项，确保不遗漏
- **IDE 专属启动提示词** — 预置 TRAE SOLO / WorkBuddy / Cursor / Claude Code 模板
- **三步启动流程** — 加载 → 汇报 → 问询，新 AI 先理解再行动
- **个人信息自动过滤** — 自动剥离真实姓名、路径、token 和密钥
- **可接续方向枚举** — 列出下一步可做什么，含前置条件和复杂度评估
- **WorkBuddy 深度适配** — 身份文件体系（SOUL.md/IDENTITY.md/USER.md）、记忆体系、技能列表、定时任务、IMA/飞书通道、MCP 连接器

## 快速开始

### 安装

```bash
clawhub install session-branch
```

### 使用

在当前对话中说：

- "开个支线" / "分叉" / "branch" / "新任务但保留上下文"

Skill 将：
1. 分析当前会话和项目
2. 在项目中生成 `docs/session-handoff.md`
3. 给你一份新对话的启动提示词

### 在新对话中

粘贴启动提示词，新 AI 将：
1. 读取交接文档 + 规则文件
2. 汇报它了解到的项目状态
3. 建议可接续的支线方向
4. 问你想走哪条路

## 配置

| 设置 | 默认值 | 说明 |
|------|--------|------|
| `handoff_path` | `docs/session-handoff.md` | 交接文档保存路径 |
| `include_checklist` | `true` | 是否用检查清单验证 |
| `target_ide` | `auto` | 目标 IDE（auto/trae/workbuddy/cursor/claude-code） |

## 文档导航

| 文档 | 说明 |
|------|------|
| [SKILL.md](SKILL.md) | Skill 规范与执行流程 |
| [交接文档模板](references/handoff-template.md) | 12 节交接文档完整模板 |
| [验证检查清单](references/checklist.md) | 12 大类 40+ 项验证清单 |
| [启动提示词模板](references/startup-prompts.md) | 各 IDE 专属启动提示词 |
| [贡献指南](docs/CONTRIBUTING.md) | 如何参与贡献 |
| [发布指南](docs/PUBLISHING_GUIDE.md) | 如何发布新版本 |
| [CHANGELOG.md](CHANGELOG.md) | 版本变更记录 |

## 许可证

MIT-0

---

# Session Branch

[![version](https://img.shields.io/badge/version-1.1.0-blue)](https://github.com/EdwardWason/session-branch)
[![License](https://img.shields.io/badge/license-MIT--0-green)](LICENSE)
[![ClawHub](https://img.shields.io/badge/ClawHub-session--branch-orange)](https://clawhub.ai/skills/session-branch)

Branch your current coding session into a new conversation with full context handoff. Generate a structured handoff document, startup prompts, and guide the new session to pick up exactly where you left off.

## Why

When a coding conversation gets long, LLM context compression degrades quality. You want to start fresh but keep all the knowledge, decisions, and code context. Session Branch solves this by generating a comprehensive handoff document that a new AI session can read to "hot start" your project.

## Features

- **Structured Handoff Document** — 12-section template covering project identity, decision chain, data flow, capability boundary, code changes, platform status, and more
- **Validation Checklist** — 12 categories, 40+ items to ensure nothing is missed
- **IDE-Specific Startup Prompts** — Pre-built templates for TRAE SOLO, WorkBuddy, Cursor, and Claude Code
- **Three-Step Startup Flow** — Load → Report → Ask, so the new AI understands before acting
- **Personal Info Auto-Filter** — Strips real names, paths, tokens, and secrets from handoff docs
- **Branchable Directions** — Enumerates what can be built next with prerequisites and complexity
- **WorkBuddy Deep Adaptation** — Identity files (SOUL.md/IDENTITY.md/USER.md), memory system, skill list, scheduled tasks, IMA/Feishu channels, MCP connectors

## Quick Start

### Install

```bash
clawhub install session-branch
```

### Usage

In your current conversation, say:

- "开个支线" / "分叉" / "branch" / "new task but keep context"

The skill will:
1. Analyze your current session and project
2. Generate a `docs/session-handoff.md` in your project
3. Give you a startup prompt for the new conversation

### In the New Conversation

Paste the startup prompt. The new AI will:
1. Read the handoff document + rules
2. Report what it learned
3. Suggest branchable directions
4. Ask you which direction to pursue

## Configuration

| Setting | Default | Description |
|---------|---------|-------------|
| `handoff_path` | `docs/session-handoff.md` | Where to save the handoff document |
| `include_checklist` | `true` | Whether to validate against checklist |
| `target_ide` | `auto` | Target IDE for startup prompt (auto/trae/workbuddy/cursor/claude-code) |

## Documentation

| Document | Description |
|----------|-------------|
| [SKILL.md](SKILL.md) | Skill specification and execution flow |
| [Handoff Template](references/handoff-template.md) | Full template for handoff documents |
| [Validation Checklist](references/checklist.md) | 12 categories, 40+ items |
| [Startup Prompts](references/startup-prompts.md) | IDE-specific startup prompt templates |
| [Contributing](docs/CONTRIBUTING.md) | How to contribute |
| [Publishing Guide](docs/PUBLISHING_GUIDE.md) | How to publish new versions |
| [CHANGELOG.md](CHANGELOG.md) | Version history |

## License

MIT-0
