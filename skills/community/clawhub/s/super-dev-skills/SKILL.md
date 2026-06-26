# 🧠 Super-Dev Suite · 全栈之神自进化套件

> **需求深访 + 共享语言 + TDD + 感官级UI/UX验证 + 供应链安全门禁 + 分层记忆系统 + 技能自我进化**  
> **每次任务自动沉淀经验、提炼 Skill、持续越用越强，交付绝对安全可靠、体验极致的工业艺术品。**
> 
> **内化 Google 工程文化，自带记忆与进化能力，从需求到交付的零缺陷全栈开发工厂。**

[![License](https://img.shields.io/badge/license-MIT-blue)](./LICENSE)
[![Claude Code](https://img.shields.io/badge/Claude%20Code-Compatible-green)]()
[![Skills](https://img.shields.io/badge/Skills-9%20modular%20roles-9cf)]()
[![Memory](https://img.shields.io/badge/Memory-.memory%2F%20self--evolution-orange)]()


## ✨ 为什么需要这个套件？

其他开发 Skill 要么是“一次性”的（每次从零开始，不记过往），要么只覆盖代码编写，忽略供应链安全和真实用户体验。**Super-Dev Suite** 是第一个同时具备以下能力的全栈开发套件：

- 🧠 **记忆与进化** – 通过 `.memory/` 三层记忆系统，项目事实、用户偏好、踩坑经验持续沉淀，越用越强。
- 🛡️ **供应链安全门禁** – 预安装恶意包扫描、深度静态分析、SBOM+CVE 审计，**恶意包零容忍**。
- 👁️ **人类感官级 UI/UX 审计** – 独立的体验师角色，模拟最挑剔用户，检测 AI 美学反模式。
- 🧪 **严格 TDD + 五轴审查** – 融合 agent-skills 的测试金字塔、DAMP、Beyonce Rule 和 Stop-the-Line。
- 📋 **结构化需求深访** – 假设先行、95% 置信度停止、Push Back 模糊需求。
- 🚀 **总控自动调度** – 一个入口，自动识别任务模式，按需激活 9 个专业子 Skill。

---

## 🆚 与 [agent-skills](https://github.com/addyosmani/agent-skills) 的关系

我们深度研究了 Addy Osmani 的 agent-skills，并将其精华**内化**到本套件中：

| agent-skills 优点 | 我们在哪里融合 |
| :--- | :--- |
| 假设声明、95% 置信度、Push Back | `super-dev-requirements` |
| 测试金字塔 80/15/5、DAMP、Beyonce Rule | `super-dev-tdd` |
| AI 美学反模式检测表 | `super-dev-ux` |
| Always/Ask/Never 安全边界 | `super-dev-security` |
| Chesterton's Fence | `super-dev-architect` |

同时我们补充了 agent-skills 所**没有**的核心能力：记忆进化、独立 UX 体验审计、供应链安全门禁、冷启动验证。  
如果你也安装了 agent-skills，总控会在对应阶段提示可用的 `/spec`、`/build` 等 slash 命令作为补充，两者完全兼容。

---

## 📁 套件结构

```

├── skills/
│   ├── super-dev-orchestrator.md      # 总控调度：模式识别、任务委派、记忆存取
│   ├── super-dev-requirements.md     # 需求分析师：结构化深访、用户故事、验收标准
│   ├── super-dev-architect.md        # 架构师：系统设计、技术选型、ADR
│   ├── super-dev-tdd.md              # TDD 工匠：垂直切片、红绿重构、五轴审查
│   ├── super-dev-ux.md               # 体验审计师：感官级 UI/UX 审计、AI 反模式检测
│   ├── super-dev-security.md         # 安全审计官：供应链门禁、依赖扫描、代码审计
│   ├── super-dev-memory.md           # 记忆官：三层记忆管理、加载、压缩
│   ├── super-dev-evolution.md        # 进化官：经验反思、技能提炼、Nudge Engine
│   └── super-dev-shared-language.md  # 语言官：统一领域语言，消除翻译损耗
└── memory/                           # 共用记忆库
    ├── MEMORY.md                     # 项目事实记忆（上限 2200 字符）
    ├── USER.md                       # 用户认知记忆（上限 1375 字符）
    ├── SKILLS.md                     # 自进化技能库
    └── EXPERIENCES/                  # 经验轨迹档案
```

## 📦 子 Skill 清单

| # | Skill | 文件 | 职责 |
|---|-------|------|------|
| 🎯 | Orchestrator | [super-dev-orchestrator.md](skills/super-dev-orchestrator/SKILL.md) | 总控调度、模式识别、任务委派、记忆存取 |
| 📋 | Requirements | [super-dev-requirements.md](skills/super-dev-requirements/SKILL.md) | 需求深访、用户故事提炼、验收标准、共享语言建立 |
| 🏗️ | Architect | [super-dev-architect.md](skills/super-dev-architect/SKILL.md) | 系统架构、技术选型、ADR 决策记录 |
| 🧪 | TDD | [super-dev-tdd.md](skills/super-dev-tdd/SKILL.md) | 测试驱动开发、Red→Green→Refactor 循环 |
| 🎨 | UX | [super-dev-ux.md](skills/super-dev-ux/SKILL.md) | 感官级 UI/UX 验证、无障碍、响应式 |
| 🔒 | Security | [super-dev-security.md](skills/super-dev-security/SKILL.md) | 供应链安全门禁、依赖扫描、代码审计 |
| 🧠 | Memory | [super-dev-memory.md](skills/super-dev-memory/SKILL.md) | 分层记忆系统、经验沉淀、知识检索 |
| 🔄 | Evolution | [super-dev-evolution.md](skills/super-dev-evolution/SKILL.md) | 技能自我进化、套件迭代优化 |
| 🗣️ | Shared Lang | [super-dev-shared-language.md](skills/super-dev-shared-language/SKILL.md) | 统一领域语言、消除翻译损耗 |

## 🚀 快速开始

### 1. 一键初始化
将以下脚本保存为 `init.sh` 并运行，自动创建所有文件：

```bash
#!/bin/bash
# 全栈之神套件初始化
set -e
mkdir -p .claude/skills .memory/EXPERIENCES

# 下载技能文件（实际使用时替换为你的文件地址）
# 或手动将本仓库中的 9 个 .md 文件复制到 .claude/skills/

# 初始化记忆
echo "# Project Memory (auto-maintained)" > .memory/MEMORY.md
echo "# User Profile (auto-maintained)" > .memory/USER.md
echo "# Skills Library (auto-maintained)" > .memory/SKILLS.md

echo "✅ 初始化完成！在 Claude Code 中激活 super-dev-orchestrator 即可开始。"
```

你也可以直接克隆本仓库，然后将 `skills/` 和 `memory/` 目录复制到项目的 `.claude/` 下。

### 2. 激活套件
在 Claude Code 中，输入：

```
激活 super-dev-orchestrator
```

总控会自动加载 `.memory/` 中的所有历史记忆，识别当前任务模式（BOOTSTRAP / FEATURE / FIX / REFACTOR），并委派给对应的子 Skill。

### 3. 典型工作流
- **新项目**：Orchestrator → Requirements → Shared Language → Security → Architect → TDD → UX → Evolution → Memory
- **新增功能**：Orchestrator（FEATURE 模式）→ Security（仅针对新依赖）→ TDD → UX（只审计变更部分）→ Evolution
- **修复 Bug**：Orchestrator（FIX 模式）→ TDD（Stop-the-Line）→ Evolution

---

## 🧩 各角色详解

| 角色 | 文件 | 一句话职责 |
| :--- | :--- | :--- |
| 🎯 总控 | `orchestrator` | 模式识别、任务委派、桥接外部 agent-skills |
| 📋 需求分析师 | `requirements` | 假设先行深访，输出精确验收标准 |
| 🗣️ 语言官 | `shared-language` | 建立统一术语表，消除“用户 vs Account”类损耗 |
| 🏗️ 架构师 | `architect` | 系统蓝图、数据库 DDL、ADR 决策记录 |
| 🧪 TDD 工匠 | `tdd` | 垂直切片、红绿重构、Stop-the-Line 调试 |
| 🎨 体验审计师 | `ux` | 模拟挑剔用户，检测 AI 美学反模式，输出感官 Bug |
| 🔒 安全审计官 | `security` | 四道供应链扫描，Always/Ask/Never 边界 |
| 🧠 记忆官 | `memory` | 三层记忆的读写压缩，语义检索 |
| 🔄 进化官 | `evolution` | 子任务反思、Skill 提炼、Nudge 提醒 |

---

## 🛡️ 安全承诺

- 所有依赖在 `npm install` **之前**进行恶意包数据库比对
- 使用 `ssafe` / `depspector` / `owasp-depscan` / `OpenSSF Scorecard` 四道防线
- 已知恶意包家族（Shai-Hulud、fezbox 等）**零容忍**
- 禁止 postinstall 自动执行，强制 lockfile 提交

---

## 📖 项目文档

套件自身在运行过程中会生成并维护以下文档：

- `CONTEXT.md` – 领域术语、用户画像、体验基线
- `specs/requirements.md` – 功能清单与验收标准
- `docs/adr/` – 架构决策记录
- `docs/security-gate-report.md` – 安全门禁报告
- `SECURITY.md` – 安全声明
- `README.md` – 项目门面（由交付官自动生成）

---

## 🤝 贡献

欢迎提交 Issue 或 PR 改进任何子 Skill。请确保修改后的 Skill 仍然与总控的委派接口兼容。

---

## 📄 许可证

MIT © 2026 小草
```

