# Smart Agent Workflow

**AI Agent 工作方法论 Skill — 专注 3高：高质量 + 高效率 + 高节省**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Version](https://img.shields.io/badge/version-1.1.0-blue.svg)]()
[![ClawHub](https://img.shields.io/badge/clawhub-smart--agent--workflow-blue)](https://clawhub.com)

---

## 🎯 这是什么

一个专注于"如何工作"的方法论 Skill，类似于 GTD 之于时间管理。

**不是又一个 agent 框架，而是让任何 AI agent 都能高效、可控、可靠地工作的方法论。**

### 核心价值

| 原则 | 解决的问题 | 实现方式 |
|------|-----------|---------|
| 🎯 高质量 | agent 容易失控、偏离目标 | WBS 拆分 + P0/P1 汇报规范 |
| ⚡ 高效率 | 任务执行混乱、缺少规范 | 任务类型判断 + 批次执行 |
| 💰 高节省 | Context 超限、Token 浪费 | Context 管理 + DO NOT 列表 + Credit Burn Loop 防护 |

---

## 📦 适用范围

**渠道无关，适用于任何 AI agent：**
- Claude Code（推荐）
- Cursor / Windsurf
- Codex
- OpenClaw
- 任何支持读取本地文件的 AI agent

---

## 🚀 快速开始（5分钟）

### 安装

```bash
# 通过 ClawHub 安装
clawhub install smart-agent-workflow

# 或者 git clone
git clone https://github.com/whhaijun/agent-workflow.git ~/smart-agent
```

### 让 Agent 读取规范

**Claude Code（`CLAUDE.md`）：**
```markdown
每次对话开始时读取 ~/smart-agent/AGENTS.md 并遵守所有规范
```

**Cursor（Settings → Rules for AI）：**
```
读取 ~/smart-agent/AGENTS.md 并遵守所有规范
```

### 开始使用

Agent 会自动按照规范工作，无需额外配置。

---

## 💡 核心规范

### 任务类型判断（30秒内）

```
收到任务
    ↓
新任务 or 连续任务？
    ↓
简单 or 复杂？（满足2条：文件≥3 / 步骤≥5 / 耗时>15分钟）
    ↓
简单任务 → P0 规范（3条）
复杂任务 → P0 + P1 规范（6条）
```

### P0 规范（所有任务必须，3条）

1. **复杂任务必须拆分** — 满足2条就拆，输出拆分方案
2. **卡住必须上报** — 失败≥2次 / 等待>30秒
3. **完成必须汇报** — 目标 + 结果 + 产出（3句话）

### P1 规范（复杂任务建议，3条）

4. **批次完成汇报** — 每批次完成后简短汇报
5. **危险操作确认** — git push / 对外发送 / 删除
6. **连续任务插断点** — 连续执行>15分钟插断点

---

## 🔧 推荐组合

**按需选择，不强制：**

```
最小配置（只用本 skill）
└── 获得：任务拆分 + 汇报规范 + Context 管理

标准配置（推荐）
├── smart-agent-workflow  # 工作方法论
└── self-improving        # 自我学习 + 纠错记忆

完整配置
├── smart-agent-workflow  # 工作方法论
├── self-improving        # 自我学习
└── proactivity           # 主动性 + 心跳检查
```

**安装推荐组合：**
```bash
clawhub install smart-agent-workflow
clawhub install self-improving
clawhub install proactivity
```

---

## 📚 文档结构

```
smart-agent-workflow/
├── SKILL.md                     # ClawHub 发布文件
├── AGENTS.md                    # 核心规范（必读）
├── IDENTITY.md                  # Agent 身份配置
├── memory/                      # 分层记忆（HOT/WARM/COLD）
├── logs/                        # 结构化日志
├── process-standards/           # 完整流程规范
│   ├── core/
│   │   ├── WBS_RULES_v3.0.md    # 任务拆分规范
│   │   ├── TASK_REPORTING_v3.0.md # 汇报规范
│   │   ├── SECURITY_CHECK.md    # 安全检查
│   │   └── CONTEXT_MANAGEMENT_v2.0.md # Context 管理
│   └── templates/               # 可直接使用的模板
└── scripts/                     # 工具脚本
```

---

## 🌟 和竞品的区别

| 能力 | smart-agent-workflow | self-improving | memory 类 | task-decomposer |
|------|:---:|:---:|:---:|:---:|
| 完整方法论 | ✅ | ❌ | ❌ | ❌ |
| 任务拆分 | ✅ | ❌ | ❌ | ✅ |
| 任务汇报 | ✅ | ❌ | ❌ | ❌ |
| 安全检查 | ✅ | ❌ | ❌ | ❌ |
| Context 管理 | ✅ | ❌ | ❌ | ❌ |
| 渠道无关 | ✅ | ✅ | 部分 | ✅ |
| 轻量（高节省） | ✅ | ✅ | ❌ | ✅ |

**核心差异：** 唯一提供完整工作方法论的 skill，其他都是单点解决方案。

---

## 📖 详细文档

- [核心规范](./AGENTS.md)
- [WBS 拆分规范](./process-standards/core/WBS_RULES_v3.0.md)
- [任务汇报规范](./process-standards/core/TASK_REPORTING_v3.0.md)
- [安全检查规范](./process-standards/core/SECURITY_CHECK.md)
- [Context 管理规范](./process-standards/core/CONTEXT_MANAGEMENT_v2.0.md)

---

## 📄 License

MIT License

---

**让任何 AI agent 都能高效、可控、可靠地工作。**
