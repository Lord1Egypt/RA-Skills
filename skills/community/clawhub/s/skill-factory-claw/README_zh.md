# Harness

**智能体优先工程知识库，以 OpenAI Harness Engineering 为核心，整合业界多方最佳实践。**

[![版本](https://img.shields.io/badge/版本-1.2-blue.svg)](./SKILL.md)
[![协议](https://img.shields.io/badge/协议-MIT-green.svg)](./LICENSE)
[![English](https://img.shields.io/badge/Docs-English-blue.svg)](./README.md)

---

## 这个 Skill 解决什么问题

Harness 是一个让 AI 智能体能够更高效工作的工程知识库。它回答的核心问题包括：

- 代码库该如何组织，才能让智能体顺畅工作？
- `AGENTS.md` 应该写什么，写多长？
- 如何管理上下文，而不让智能体被信息淹没？
- 哪些架构约束应该从第一天就强制执行？
- 高吞吐量智能体工作流中，技术债务怎么处理？

这些知识来自真实验证：OpenAI Harness Engineering 团队用 3 名工程师、5 个月、零人工编码，构建了约 100 万行代码的产品。

---

## 核心卖点

### 1. 多源整合，不止一家之言

以 OpenAI Harness Engineering 为核心框架，并与以下来源交叉验证和扩展：
- **Anthropic** — Claude Code 和 Computer Use 生产环境实践
- **GitHub** — Copilot Workspace 工作流模式
- **开源社区** — Aider、Cline、Continue.dev 一线经验
- **技术领袖** — Eugene Yan、Chip Huyen 等深度洞见

→ 完整信息源见 [`references/extended-sources.md`](./references/extended-sources.md)

### 2. 结构化，便于快速检索

三个 reference 文件，各有明确职责——原则速查表、完整蒸馏文档、扩展来源索引，按需加载。

### 3. 原则而非清单

10 大核心原则构成完整的智能体优先开发方法论，而非零散技巧的堆砌。

### 4. 持续维护

版本化管理，随领域演进更新新来源。

---

## 10 大核心原则

| 原则 | 核心观点 |
|------|---------|
| **人类掌舵，智能体执行** | 设计环境 + 明确意图 + 构建反馈回路 |
| **情境稀缺** | `AGENTS.md` ≤ 100行，渐进式披露 |
| **不变量约束 > 微观管理** | 通过 linter 强制架构分层，而非靠指令控制 |
| **应用对智能体可读** | UI + 日志 + 指标对智能体直接可见 |
| **持续垃圾回收** | 小额持续偿还技术债务，不积累 |
| **纠错 > 等待** | 减少阻塞合并门，快速迭代 |
| **仓库即唯一真相** | 不在 repo = 对智能体不存在 |
| **Ralph Wiggum 闭环** | 智能体自我审查变更，直到所有审阅人满意 |
| **架构是 Day-1 先决条件** | 严格分层是基础，而非奢侈品 |
| **偏好智能体可读的技术** | 可组合、API 稳定、训练集中充分表示 |

---

## 快速上手

安装到 `~/.workbuddy/skills/harness/` 后，当你询问以下问题时，skill 会自动加载：

- 如何为智能体设计代码库结构
- 如何编写 `AGENTS.md`
- 上下文管理策略
- 架构约束与分层设计
- 智能体可观测性建设
- 高吞吐量工作流中的技术债务处理

---

## 文件结构

```
harness/
├── SKILL.md                    # Skill 入口（触发词 + 快速摘要）
├── README.md                   # 英文版介绍
├── README_zh.md                # 中文版介绍（本文件）
├── CHANGELOG.md                # 版本历史
├── LICENSE                     # MIT
└── references/
    ├── harness-engineering.md  # OpenAI Harness Engineering 完整蒸馏
    ├── core-principles.md      # 10 大核心原则速查表
    └── extended-sources.md     # 扩展信息源索引（Anthropic/GitHub/社区等）
```

---

## 安装方式

```powershell
Copy-Item -Recurse -Force "harness\" "$env:USERPROFILE\.workbuddy\skills\harness\"
```

---

## 核心来源

| 来源 | 作者/组织 | 价值 |
|------|----------|------|
| [Harness Engineering](https://openai.com/zh-Hans-CN/index/harness-engineering/) | Ryan Lopopolo, OpenAI | 核心框架，100万行代码实战验证 |
| [Claude Code](https://docs.anthropic.com/en/docs/agents-and-tools/claude-code/overview) | Anthropic | 官方 agentic coding 实践 |
| [Aider](https://github.com/Aider-AI/aider) | Paul Gauthier | 最成熟的 AI 结对编程工具 |
| [Eugene Yan](https://eugeneyan.com/) | Eugene Yan | ML Engineering 深度洞见 |
| [Chip Huyen](https://huyenchip.com/) | Chip Huyen | ML Systems 系统设计视角 |

---

## 协议

MIT — 自由使用，欢迎贡献。

> *"Humans steer, agents row."* — Harness Engineering
