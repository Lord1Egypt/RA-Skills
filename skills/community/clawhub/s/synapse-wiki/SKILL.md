---
name: synapse-wiki
description: >
  Synapse Wiki — 智能知识库管理系统。
  自动摄取原始资料，增量构建持久化知识网络，支持智能查询和健康检查。
  知识随时间复利积累，越用越聪明。
  当用户提到 wiki、知识库、摄取资料、查询知识、整理文档时使用此技能。
version: 2.0.1
updated: 2026-04-15
date: 2026-04-10
user-invocable: true
metadata:
  openclaw:
    emoji: "🧠"
    requires:
      bins: ["python3"]
    install: []
    homepage: "https://github.com/ankechenlab-node/synapse-wiki"
tags: [knowledge-base, wiki, documentation, learning, obsidian, brain-compatible]
---

# Synapse Wiki Skill

**Synapse Wiki = 持久化知识网络 + 增量积累 + 自动健康维护**

核心理念：知识应该随时间复利增长，而非每次从零开始。

| | 传统笔记 | Synapse Wiki |
|--|---------|--------------|
| **机制** | 手动整理 + 检索 | 自动编译原始资料成知识网络 |
| **知识形式** | 孤立文档 | 结构化、交叉链接的知识页面 |
| **随时间变化** | 越积越多，难以查找 | 越用越聪明，自动关联 |
| **维护者** | 人类 | AI（编译、交叉引用、归档） |

---

## 🚦 快速决策：我该用什么命令？

```
你想做什么？
│
├─ 开始一个新知识库         → ingest（初始化）
│   └─ 例："我想建一个 AI 学习知识库"
│
├─ 保存新资料/文章          → ingest（摄取）
│   └─ 例："这篇好文要存起来"、"剪辑网页保存"
│
├─ 查询已有知识             → query（查询）
│   └─ 例："RAG 是什么？"、"上次那个概念怎么解释"
│
└─ 检查知识库健康度         → lint（检查）
    └─ 例："有没有死链接？"、"检查孤立页面"
```

**常用场景**:
- 第一次用 → `/synapse-wiki init ~/my-wiki "AI 知识库"`
- 看到好文章 → `/synapse-wiki ingest ~/my-wiki raw/articles/xxx.md`
- 有疑问 → `/synapse-wiki query ~/my-wiki "你的问题"`

---

## 📋 命令速查卡片

| 命令 | 用途 | 示例 |
|------|------|------|
| `/synapse-wiki init` | 初始化知识库 | `/synapse-wiki init ~/my-wiki "AI 知识库"` |
| `/synapse-wiki ingest` | 摄取新资料 | `/synapse-wiki ingest ~/my-wiki raw/articles/article.md` |
| `/synapse-wiki query` | 查询知识 | `/synapse-wiki query ~/my-wiki "RAG 是什么"` |
| `/synapse-wiki lint` | 健康检查 | `/synapse-wiki lint ~/my-wiki` |

**使用提示**:
- 首次使用先用 `init` 创建目录结构
- 每次保存资料后用 `ingest` 编译为知识
- 定期运行 `lint` 检查健康度

---

## 三层架构

```
<wiki-root>/
├── CLAUDE.md              ← Schema 定义（范围/规范/工作流）
├── log.md                 ← 只增不减的时间线日志
│
├── raw/                   ← 原始资料层（LLM 只读，永不修改）
│   ├── articles/          ← 网页文章（Obsidian Clipper 保存）
│   ├── papers/            ← 学术论文
│   └── notes/             ← 个人笔记
│
└── wiki/                  ← Wiki 知识层（LLM 编写，用户阅读）
    ├── index.md           ← 主目录：所有页面 + 一句话摘要
    ├── concepts/          ← 概念/主题页面
    ├── entities/          ← 人物、工具、论文、组织
    └── summaries/         ← 每个来源的摘要页面
```

## 命令

### 摄取命令
```bash
# 摄取新资料
/synapse-wiki ingest /path/to/wiki "raw/articles/article.md"
```

### 查询命令
```bash
# 查询 Wiki 知识
/synapse-wiki query /path/to/wiki "LLM Wiki 的核心思想"
```

### 健康检查命令
```bash
# Wiki 健康检查
/synapse-wiki lint /path/to/wiki
```

### 初始化命令
```bash
# 初始化新的 Wiki 知识库
/synapse-wiki init /path/to/wiki "AI 学习知识库"
```

## Scripts

| 脚本 | 用途 |
|------|------|
| `scripts/scaffold.py` | 引导新的 Wiki 目录树 |
| `scripts/ingest.py` | 摄取新资料，编译为 Wiki 页面 |
| `scripts/query.py` | 查询 Wiki，综合答案 |
| `scripts/lint_wiki.py` | 健康检查（死链接/孤立页/矛盾） |

## 页面类型模板

### 概念页面 (400-1200 词)
```markdown
---
title: <Title>
type: concept
created: YYYY-MM-DD
updated: YYYY-MM-DD
sources: [slug1, slug2]
tags: [tag1, tag2]
---

# <Title>

<一句话定义或核心思想。>

## What it is
<清晰解释。>

## How it works
<机制、过程或结构。>

## Key properties / tradeoffs
<重要特征。>

## Relationship to other concepts
<相关概念的 wikilinks。>

## Open questions
<Wiki 尚未解决的问题。>
```

### 实体页面 (200-500 词)
```markdown
---
title: <Name>
type: entity
entity_type: person | tool | paper | organization | project
created: YYYY-MM-DD
updated: YYYY-MM-DD
sources: [slug1]
tags: [tag1]
---

# <Name>

<一句话描述。>

## Key contributions / features
<主要贡献或特性。>

## Related concepts
<相关概念。>
```

### Summary 页面 (150-400 词)
```markdown
---
title: summaries/<slug>
type: summary
source_type: article
date: YYYY-MM-DD
ingested: YYYY-MM-DD
tags: []
---

# <Source Title>

## Key takeaways
- <最重要洞察 1>
- <最重要洞察 2>
- <最重要洞察 3>

## Core claims
<主要论点的 2-4 句话摘要。>

## Concepts introduced / referenced
<概念和实体。>
```

## 索引和日志

### index.md 格式
```markdown
# Index — <Wiki Name>

## Concepts（概念）
- [[Page Name]] — One-line summary

## Entities（实体）
- [[Page Name]] — One-line summary

## Summaries（资料摘要）
- [[summaries/slug]] — One-line summary
```

### log.md 格式
```markdown
## [YYYY-MM-DD] ingest | <slug> — <description>
## [YYYY-MM-DD] query | <question-slug>
## [YYYY-MM-DD] lint | <N> issues found
## [YYYY-MM-DD] promote | <page-name> (from query)
```

## Session 启动检查清单

每个新 Session：
1. 读取 CLAUDE.md，确认范围和规范
2. 读取 log.md 最近 5 条：`grep "^## \[" log.md | tail -5`
3. 如有新 raw/ 资料，执行 Ingest
4. 如用户提问，执行 Query（先查 index.md）
5. 如 ingest 超过 10 次未 lint，执行 Lint

## Brain 调度集成 (v2.0 新增)

Synapse Wiki v2.0 可作为 synapse-brain 的被调度 Hand Agent 运行：

```
用户 → synapse-brain（意图识别：知识查询/保存）
         ↓ 路由到 wiki
       synapse-wiki（执行 ingest/query/lint）
         ↓ 完成后
       synapse-brain（汇总 + 状态保存）
```

通过 Brain 调度使用：
```bash
/synapse-brain dispatch "保存这篇 RAG 文章" --skill synapse-wiki
/synapse-brain dispatch "RAG 是什么？" --skill synapse-wiki
```

## 与 synapse-code 互操作

synapse-code Pipeline 完成后可自动触发 wiki 知识沉淀：

```
synapse-code Pipeline 完成
         ↓ (auto_log enabled)
    synapse-wiki ingest
         ↓
    知识写入 wiki/summaries/
         ↓
    包括：技术决策、代码模式、Bug 修复记录
```

配置方式：
```json
{
  "interop": {
    "wiki_enabled": true,
    "wiki_root": "~/my-project/wiki"
  }
}
```

知识沉淀内容：
- **技术决策** — 为什么选择方案 A 而非 B
- **代码模式** — 项目中常用的架构模式
- **Bug 修复** — 遇到的坑和解决方案
- **API 变更** — 接口设计决策和版本记录

## 安装

```bash
# 方式 1: 使用安装脚本（推荐）
cd ~/.claude/skills/synapse-wiki
./install.sh

# 方式 2: 手动复制
cp -r synapse-wiki ~/.claude/skills/

# 方式 3: OpenClaw (如有 .skill 文件)
claude skill install synapse-wiki.skill
```

## 使用场景

- 📚 **个人知识库建设** — 积累 AI/技术知识，构建第二大脑
- 📝 **项目文档管理** — 维护项目 Wiki，团队成员快速上手
- 🔍 **知识检索** — 快速查找已学概念，不再大海捞针
- 🧹 **知识整理** — 定期健康检查，保持知识网络整洁
