---
name: superpowers-overview
description: Use when starting any development work or when unsure which superpowers development skill to use - provides entry point and navigation to the full superpowers skill suite for OpenClaw agents
---

# Superpowers 开发方法论 — OpenClaw 移植版

## 这是什么

Superpowers 是一套为 AI coding agent 设计的**结构化开发方法论**，核心是：
> Agent 不应一上来就写代码，而应该先理解需求 → 设计方案 → 制定计划 → TDD 实现 → 审查代码 → 收尾。

本技能套件将 Superpowers 移植到 OpenClaw Agent Runtime，针对 OpenClaw 的工具模型做了适配。

## 技能套件（9个）

### 🚀 入门

| 技能 | 何时用 | 做什么 |
|------|--------|--------|
| **`superpowers-overview`**（这个） | 不知道从哪里开始 | 查看套件全貌和入口 |
| **`superpowers-brainstorming`** | 要做新功能/改东西之前 | 探索需求，提出方案，获得批准 |
| **`superpowers-writing-plans`** | 有了设计，需要具体实现计划 | 写小粒度任务计划 |

### 🔨 执行

| 技能 | 何时用 | 做什么 |
|------|--------|--------|
| **`superpowers-isolated-workspace`** | 开始实现前 | 创建隔离 git 分支，建立干净起点 |
| **`superpowers-subagent-dev`** | 有实现计划，任务独立 | 派发 subagent 执行任务，两阶段审查 |
| **`superpowers-parallel-agents`** | 有多个独立问题要并行处理 | 并行派发多个 subagent 同时工作 |
| **`superpowers-tdd`** | 写任何实现代码之前 | 强制 RED-GREEN-REFACTOR 循环 |
| **`superpowers-executing-plans`** | 在本 session 顺序执行计划任务 | 按批次执行，有审查检查点 |

### ✅ 质量保障

| 技能 | 何时用 | 做什么 |
|------|--------|--------|
| **`superpowers-verification`** | 声称任何"完成了"/"通过了"之前 | 强制证据先行，必须运行验证命令 |
| **`superpowers-systematic-debugging`** | 遇到 bug/测试失败/意外行为 | 四阶段调试：根因→模式→假设→修复 |
| **`openclaw-requesting-code-review`** | 完成任务/重大功能/merge 之前 | 派发审查捕获问题 |
| **`openclaw-receiving-code-review`** | 收到代码审查反馈时 | 验证后实现，合理反驳 |
| **`superpowers-finishing-branch`** | 实现完成，测试通过，要收尾 | 展示 merge/PR/保留/丢弃选项 |

## 开发流程图

```
用户请求新功能
        │
        ▼
┌───────────────────────┐
│ superpowers-brainstorming │
│ 探索需求 + 设计方案     │
└───────────┬───────────┘
            │ 主人批准设计
            ▼
┌───────────────────────────┐
│ superpowers-isolated-workspace │
│ 创建隔离分支 + 干净基线   │
└───────────┬───────────────┘
            │
            ▼
┌───────────────────────┐
│ superpowers-writing-plans │
│ 写实现计划（任务清单）   │
└───────────┬───────────┘
            │
            ▼
    ┌───────┴───────┐
    │  选择执行模式   │
    └───────┬───────┘
            │
    ┌───────┴───────────────┐
    │                       │
    ▼                       ▼
┌────────────────┐  ┌─────────────────────┐
│ subagent-dev   │  │ executing-plans     │
│（推荐）         │  │（本 session 顺序）   │
│ 每个任务派发     │  │ 按批次执行          │
│ subagent+审查   │  │ 中间审查检查点      │
└───────┬────────┘  └──────────┬──────────┘
        │                     │
        └─────────┬───────────┘
                  │
                  ▼
        ┌─────────────────────┐
        │superpowers-finishing│
        │-branch             │
        │ merge/PR/保留/丢弃  │
        └─────────────────────┘
```

## 日常使用决策

**"我要做 X 功能"**
→ `superpowers-brainstorming` → `superpowers-writing-plans` → `superpowers-subagent-dev`

**"我要修 bug"**
→ `superpowers-systematic-debugging` → `superpowers-tdd` → `superpowers-verification`

**"有 3 个独立的测试失败"**
→ `superpowers-parallel-agents` → 分别并行调查 → 整合

**"代码写完了准备提交"**
→ `superpowers-verification` → `openclaw-requesting-code-review` → `superpowers-finishing-branch`

## 核心原则

1. **设计在实现之先** — 不要跳到代码
2. **证据在声称之前** — 不要说我修好了，要运行验证
3. **根因在修复之先** — 不要猜，要调试
4. **测试在代码之先** — TDD，不是测试后补
5. **审查在集成之先** — 问题要早发现

## OpenClaw 适配说明

相比 Superpowers 原版：

| 维度 | 原版 | OpenClaw 适配 |
|------|------|--------------|
| 隔离机制 | git worktree | git branch + 目录 |
| Skill 加载 | Skill 工具 | 读 SKILL.md 文件，语义触发 |
| Subagent | Task 级联 | `sessions_spawn` 独立 session |
| Todo 管理 | TodoWrite 工具 | 内联检查表 |
| 视觉辅助 | 浏览器工具 | `canvas` 工具 |
| 上下文传递 | 模板注入 | session 历史 + 文件系统 |

## 与 AGENTS.md 的关系

Superpowers 技能套件**补充**而非**替代** AGENTS.md：
- AGENTS.md = 我是谁、我的工作区、我的记忆系统
- Superpowers = 结构化开发流程和工程质量规范
- 两者协同：先了解我是谁，再用正确方法做事

---

## ClawHub 发布情况

所有 13 个技能均已发布至 ClawHub：

| 技能 | ClawHub Slug | 版本 | 备注 |
|------|-------------|------|------|
| superpowers-overview | `superpowers-overview` | 1.0.0 | 入口总览 |
| superpowers-tdd | `superpowers-tdd` | 1.0.0 | TDD 循环 |
| superpowers-verification | `superpowers-verification` | 1.0.0 | 证据先行 |
| superpowers-systematic-debugging | `superpowers-systematic-debugging` | 1.0.0 | 系统调试 |
| superpowers-brainstorming | `superpowers-brainstorming` | 1.0.0 | 设计流程 |
| superpowers-writing-plans | `superpowers-writing-plans` | 1.0.1 | 实现计划 |
| superpowers-subagent-dev | `superpowers-subagent-dev` | 1.0.1 | 子 agent 协调 |
| superpowers-finishing-branch | `superpowers-finishing-branch` | 1.0.1 | 分支收尾 |
| superpowers-isolated-workspace | `superpowers-isolated-workspace` | 1.0.1 | 隔离工作区 |
| superpowers-parallel-agents | `superpowers-parallel-agents` | 1.0.1 | 并行 agent |
| superpowers-receiving-code-review | `openclaw-receiving-code-review` | 1.0.0 | ⚠️ 原 slug 被占用，用 openclaw- 前缀 |
| superpowers-requesting-code-review | `openclaw-requesting-code-review` | 1.0.0 | ⚠️ 原 slug 被占用，用 openclaw- 前缀 |
| superpowers-executing-plans | `openclaw-executing-plans` | 1.0.0 | ⚠️ 原 slug 被占用，用 openclaw- 前缀 |
