---
name: super-dev-suite
description: 全栈之神·自进化零缺陷交付套件总入口。激活后自动启动总控调度系统。
alwaysOn: true
triggers:
  - pattern: "super-dev|全栈之神|超级开发|零缺陷"
    description: "用户显式激活套件时触发"
---

## 套件概述

本套件将原 `super-dev-evolution` 单体 Skill 拆分为**轻量、专注、按需激活**的子 Skill 套件，解决"每次激活加载大量无关指令、上下文浪费严重"的核心痛点。

## 架构设计

```
                    ┌─────────────────────────┐
                    │  super-dev-orchestrator  │
                    │  总控：模式识别·委派·记忆  │
                    └───────┬───────┬─────────┘
                            │       │
          ┌─────────────────┼───────┼─────────────────┐
          │                 │       │                 │
          ▼                 ▼       ▼                 ▼
┌─────────────┐  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐
│ requirements│  │   architect  │  │     tdd      │  │      ux      │
│  需求深访    │  │   架构设计    │  │  TDD驱动开发  │  │  UI/UX验证   │
└─────────────┘  └──────────────┘  └──────────────┘  └──────────────┘
          │                 │       │                 │
          └─────────────────┼───────┼─────────────────┘
                            │       │
                    ┌───────┴───────┴─────────┐
                    ▼                         ▼
            ┌──────────────┐          ┌──────────────┐
            │   security   │          │    memory    │
            │   安全门禁     │          │   分层记忆    │
            └──────────────┘          └──────────────┘
                            │
                    ┌───────┴───────┐
                    ▼               ▼
            ┌──────────────┐  ┌──────────────┐
            │  evolution   │  │ shared-lang  │
            │   自进化      │  │   共享语言    │
            └──────────────┘  └──────────────┘
```

## 子 Skill 清单

| Skill | 文件路径 | 职责 | 激活条件 |
|-------|----------|------|----------|
| 🎯 Orchestrator | `skills/super-dev-orchestrator/SKILL.md` | 总控调度、模式识别、任务委派、记忆存取 | 任务开始/结束 |
| 📋 Requirements | `skills/super-dev-requirements/SKILL.md` | 需求深访、用户故事提炼、验收标准 | 新功能/需求变更 |
| 🏗️ Architect | `skills/super-dev-architect/SKILL.md` | 系统架构、技术选型、模块设计 | 架构决策 |
| 🧪 TDD | `skills/super-dev-tdd/SKILL.md` | 测试驱动开发、红绿重构循环 | 编码实现 |
| 🎨 UX | `skills/super-dev-ux/SKILL.md` | 感官级UI/UX验证、无障碍、响应式 | 前端/UI变更 |
| 🔒 Security | `skills/super-dev-security/SKILL.md` | 供应链安全、代码审计、依赖扫描 | 依赖变更/部署前 |
| 🧠 Memory | `skills/super-dev-memory/SKILL.md` | 分层记忆系统、经验沉淀、知识管理 | 任务完成后 |
| 🔄 Evolution | `skills/super-dev-evolution/SKILL.md` | 技能自我进化、套件迭代优化 | 周期性/里程碑 |
| 🗣️ Shared Lang | `skills/super-dev-shared-language/SKILL.md` | 共享语言建立、DDD统一语言 | 需求/建模阶段 |

## 使用方式

### 首次激活
```
激活 super-dev 套件，我准备开始 [任务类型]
```

### 按需激活子 Skill
```
激活 super-dev-tdd，重构 UserService 模块
激活 super-dev-security，审计新引入的依赖
```

### 任务结束
```
激活 super-dev-orchestrator，沉淀本次经验
```

## 核心原则

1. **单一职责**：每个子 Skill 只做一件事，做到极致
2. **按需加载**：不预先加载无关指令，节省上下文
3. **总控调度**：Orchestrator 负责模式识别和任务委派
4. **记忆闭环**：每次任务自动沉淀经验，越用越强
5. **安全默认**：Security 作为默认门禁，不跳过
