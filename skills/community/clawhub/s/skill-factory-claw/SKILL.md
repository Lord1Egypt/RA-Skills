---
name: harness
description: >
  Agent-first engineering knowledge base distilled from OpenAI's Harness Engineering post.
  Use this skill when the user asks about: agent-first development, agentic workflows, 
  how to structure codebases for AI agents, context management for agents, AGENTS.md best practices,
  agentic code review, autonomous coding agents, agent-driven architecture, Codex engineering,
  how to work with AI coding agents, agent engineering principles, progressive disclosure in docs,
  architecture constraints for agents, error tolerance strategy, technical debt garbage collection,
  agent-readable observability, self-review loops, merge strategy for high-throughput agent systems,
  智能体工程, 智能体优先开发, 智能体驱动编程, AGENTS.md 设计, 上下文管理, 智能体自主性,
  代码库对智能体可读, harness engineering, 渐进式披露, 架构约束早期化, 错误容忍策略,
  技术债务垃圾回收, 合并策略, 智能体自我审查, Ralph Wiggum 循环, 智能体可观测性.
version: "1.2"
source: "https://openai.com/zh-Hans-CN/index/harness-engineering/"
author: "OpenAI (Ryan Lopopolo), distilled by Claw"
created: "2026-04-17"
---

# Harness: Agent-First Engineering Knowledge Base

## 核心定位

本 Skill 是对 OpenAI 团队在 **Harness Engineering** 实践中积累的第一手智能体工程经验的系统化蒸馏。

**背景**：5个月内，3名工程师仅用提示（无人工编码）、借助 Codex 智能体，构建了约 **100 万行代码** 的产品。
- ~1,500 个 Pull Requests
- 平均每人每天 **3.5 个 PR** 的吞吐量
- 完成时间约为传统人工编写的 **1/10**

---

## 使用场景

当用户问到以下问题时，加载本 Skill 的 references/ 文档作为上下文来回答：

- 如何设计面向智能体的代码仓库结构？
- AGENTS.md 应该怎么写？
- 智能体工程中的上下文管理策略？
- 如何让应用对智能体"可读"（可观测）？
- 如何用架构约束替代微观管理？
- 如何处理智能体引入的技术债务？
- 人类工程师在智能体优先团队中的角色是什么？
- 智能体的自主水平如何随系统成熟度提升？

---

## Knowledge References

```
harness/
├── SKILL.md                            # 本文件（入口）
└── references/
    ├── harness-engineering.md          # OpenAI 原文完整蒸馏（主文档）
    ├── core-principles.md              # 10大核心原则速查表
    └── extended-sources.md             # 扩展信息源索引（Anthropic/GitHub/大V等）
```

加载知识时：
1. 优先读取 `references/core-principles.md` 快速定位
2. 需要深度背景时读取 `references/harness-engineering.md`
3. 需要扩展视角时读取 `references/extended-sources.md`

**多源整合**：本 skill 不仅包含 OpenAI Harness Engineering，还整合了 Anthropic Claude Code、GitHub Copilot Workspace、Aider 等业界最佳实践，持续追踪智能体工程前沿。

---

## Workflow

1. **识别用户问题的核心维度**：上下文管理 / 架构约束 / 可观测性 / 技术债务 / 人类角色 / 合并策略 / 文档体系
2. **读取对应 references 文档**
3. **结合用户具体场景**，从 Harness 经验中提炼可操作的建议
4. **输出时注明来源**：明确这是 OpenAI Harness Engineering 实践中验证过的方法

---

## 快速摘要（无需读文件即可回答的核心原则）

| 领域 | 黄金法则 |
|------|---------|
| 情境管理 | AGENTS.md ≤ 100行，作为目录指向深层文档；不要巨型配置文件 |
| 架构 | 严格分层（Types→Config→Repo→Service→Runtime→UI），通过 linter 自动强制 |
| 可读性 | UI + 日志 + 指标对智能体直接可读；接入 DevTools 协议 |
| 技术债务 | 黄金原则 + 循环清理 = 持续垃圾回收；小额偿还，不累积 |
| 合并策略 | 纠错成本低 > 等待成本高；减少阻塞门 |
| 文档 | 仓库是唯一记录系统；知识必须 push 进 repo 才对智能体可见 |
| 人类角色 | 设计环境 + 明确意图 + 构建反馈回路；不写代码，写约束 |
| 技术选型 | 偏好 API 稳定、可组合、在训练集中表现良好的技术栈 |
| 架构约束时机 | 严格分层约束是早期先决条件，不要等到百人团队再考虑 |
| 自我审查闭环 | 智能体在本地审核自身变更（Ralph Wiggum 循环），直到所有审阅人满意才合并 |
