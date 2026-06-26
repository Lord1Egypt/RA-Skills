# Skill Factory

> **"第一次工业革命结束的标志，是用机器来制造机器。**
> **Skill Factory，就是那台制造skill的机器。"**

这是一个用于 OpenClaw 的**元技能（meta-skill）**，将 skill 的创作过程——从一句模糊的想法，到打磨完毕、版本清晰、可直接发行的成品——变成一套可重复执行的标准化流程。

[![Version](https://img.shields.io/badge/version-2.4.0-blue.svg)](CHANGELOG.md)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![English README](https://img.shields.io/badge/README-English-blue.svg)](README.md)

---

## 它解决什么问题？

没有工作流直接上手制作 skill，常见结局：

- 需求没说清楚就开始干，做到一半发现方向不对
- 蒸馏完文章，发现漏了关键内容，还得回头重看
- 文件散落各处，想发布到 GitHub 才发现结构一团糟
- v1.0 做完了，不知道什么时候该升级、如何管理版本

Skill Factory 用**四阶段 SOP** 系统性地解决以上全部问题。

---

## 核心差异化

市面上的 skill 制作多是随兴而为。Skill Factory 的不同之处：

**基础层** — 开工前锁定范围：
- **Phase 0 三问锁定**：三个问题锁死需求，防止过度工程化

**质量层** — 确保知识完整：
- **强制原文二次核对**：蒸馏完必须回到原始来源比对，防止知识遗漏

**结构层** — 发行级从第一天开始：
- **每个 skill 独立 repo**：从第一天起就是发行级结构，随时可 push 到 GitHub
- **语义化版本管理**：清楚区分 MAJOR（范式重构）/ MINOR（增量添加）/ PATCH（修小问题）

**演进层** — 不只是 0→1，更是 1→N：
- **持续迭代机制**：有明确的升级路径和人机协作改进流程

关键在于：**这不是关于 Claw 能做什么，而是关于如何把无边界的能力，变成高质量、可重复的流水线。流程本身就是产品。**

---

## 快速上手

发给 Claw 一个想法即可：

```
新 skill：[名字]，[1-2句描述]，[来源链接（可选）]
```

或升级已有 skill：

```
skill升级：[名字]，[要加什么]，[新来源链接（可选）]
```

Claw 会立刻进入 Phase 0，回答 3 个问题后，流水线自动运转。

---

## 实际案例：制作 `harness` skill

以下是 Skill Factory 处理一次真实需求的完整过程：

**用户输入**（30秒）：
```
新 skill：harness，蒸馏 OpenAI 的智能体工程文章，
https://openai.com/index/harness-engineering/
```

**Phase 0** — 三问一轮解决：
- 目标用户：任何在做智能体工程的 Claw 实例
- 来源：OpenAI Harness Engineering 博客
- 发行形式：GitHub + 本地 workspace 同步

**Phase 1** — `web_fetch` 抓取原文，存入 `wip/harness/raw/`

**Phase 2** — 蒸馏为 `SKILL.md`（10 大原则）+ `references/`（两份文档）。强制二次核对步骤发现了 4 处遗漏，包括"Ralph Wiggum 自我审查循环"。

**Phase 3** — 独立 repo，MIT 协议，双语 README，git 打标签 `v1.2.0`，同步到 workspace。

**耗时**：约 10 分钟。没有这套工厂，同样的工作之前需要一整天迭代，且仍有知识盲区。

---

## 四阶段 SOP 概览

| 阶段 | 名称 | 产出 |
|------|------|------|
| 0 | 快速摄入 | `BRIEF.md`：锁定需求 |
| 1 | 资料收集 | `raw/`：原始资料 |
| 2 | 蒸馏 | `SKILL.md` + `references/` |
| 3 | 封装发行 | 带版本标签的独立 repo |

完整 SOP 见 [SKILL.md](SKILL.md)。

---

## 版本管理逻辑

借用软件工程的语义化版本，专为 skill 定制：

| 版本变动 | 何时触发 |
|----------|---------|
| `PATCH`（x.x.1）| 修错别字、调整触发词描述 |
| `MINOR`（x.1.0）| 新增来源、补充章节、扩展触发词 |
| `MAJOR`（2.0.0）| 核心结构重构、范式转变、激活方式改变 |

**MAJOR 不等于内容更多**——如果翻倍了 references 但结构不变，仍然是 MINOR。

---

## 目录结构

```
skill-factory/
├── SKILL.md         # 完整 SOP 文档（触发词 + 四阶段 + 版本管理 + 发行规范）
├── README.md        # 英文版说明
├── README_zh.md     # 本文件（中文说明）
├── CHANGELOG.md     # 版本历史
├── LICENSE          # MIT 开源协议
├── inbox/           # 想法投递区（随时丢，不会丢）
└── wip/             # 进行中的 skill 工作区
    └── <skill名>/
        ├── BRIEF.md
        ├── raw/
        └── draft/
```

---

## 安装方法

### 通过 ClawHub 安装（推荐）

```bash
claw skill install skillfactory
```

或使用完整标识符：

```bash
claw skill install github.com/zhelunSun/skill-factory
```

### 手动安装

1. 克隆仓库到技能目录：
```bash
git clone https://github.com/zhelunSun/skill-factory.git ~/.workbuddy/skills/skillfactory
```

2. 重启 Claw 会话 —— 技能将自动加载。

---

## 开源协议

MIT — 欢迎 fork、改造，用这个工厂造你自己的工厂。
