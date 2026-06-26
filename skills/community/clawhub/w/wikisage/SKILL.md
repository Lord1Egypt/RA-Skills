---
name: wikisage
description: "A Karpathy-style persistent LLM wiki. Use when: (1) user says '加进wiki/ingest/摄入', (2) user says '查wiki/wiki里有没有', (3) user says '整理wiki/lint', (4) answering questions that should check long-lived local knowledge first. Also use after answering valuable technical questions to ask if user wants to save to wiki."
metadata:
---

# Wikisage Skill

基于 Karpathy llm-wiki 模式的持久化 Wiki。
LLM 负责写和维护所有内容，用户负责来源、探索方向和提问。
纯本地 markdown 文件，用 index.md 导航，无需向量数据库。

## 📍 路径约定（环境变量驱动）

本 skill 所有路径都基于环境变量，无硬编码：

| 变量 | 默认值 | 作用 |
|------|--------|------|
| `WIKI_ROOT` | `$HOME/.openclaw/workspace/wiki` | Wiki markdown 根目录 |
| `MCPORTER_CONFIG` | `$HOME/.openclaw/workspace/config/mcporter.json` | mcporter 配置文件（可选） |
| `WIKI_SKILL_DIR` | `$HOME/.openclaw/workspace/skills/wikisage` | Skill 自身目录（脚本位置） |

首次部署时，在 shell/agent 环境里 export 一下这三个变量即可（或用默认值）。
下文示例用 `$WIKI_ROOT` 这种写法代替绝对路径。

## 🛠 执行通道：Obsidian MCP（首选，强烈推荐）

> **本 skill 围绕 Obsidian filesystem MCP server 设计。** 没装 MCP 也能跑（走 `read`/`write`/`edit` fallback），但装了会更稳：allowed-dir 边界兜底、错误更规范、LLM 不会意外写到 wiki 外面。

**所有 wiki 文件读写优先走 Obsidian filesystem MCP**，而不是通用 `read`/`write` 工具。

| 操作 | MCP 调用 |
|------|----------|
| 读文件 | `mcporter call obsidian.read_text_file path=<abs path>` |
| 写/覆盖文件 | `mcporter call obsidian.write_file path=<abs> content=<str>` |
| 列目录 | `mcporter call obsidian.list_directory path=<abs>` |
| 搜文件名 | `mcporter call obsidian.search_files path=<abs> pattern=<glob>` |
| 改文件 | `mcporter call obsidian.edit_file path=<abs> edits=...` |
| 看边界 | `mcporter call obsidian.list_allowed_directories` |

**所有调用都需要 `--config $MCPORTER_CONFIG`**
（mcporter 有双 config 坑：会同时读 `~/.claude.json` 和项目 config，不带 `--config` 只会看到 claude.json 里的 server）

**Fallback**：MCP 不可用时（daemon 挂了、server 不 healthy），用通用 `read`/`write`/`edit`/`exec grep` 兜底，但要在回复里告诉用户"MCP 离线，走 fallback"。

**全文搜索不走 MCP**：MCP 的 search 只匹配文件名。找内容用：
- qmd-search（workspace 集合，BM25，快但索引可能滞后）
- `exec grep -rn "关键词" $WIKI_ROOT/`

---

## 触发条件

| 用户说 | 执行 |
|---|---|
| "加进 wiki" / "ingest" / "摄入这篇" | → ingest 流程 |
| "查 wiki" / "wiki 里有没有" / "从 wiki 查" | → query 流程 |
| "整理 wiki" / "wiki 健康检查" / "lint" | → lint 流程 |
| 涉及**客户、历史决策、账号信息**的技术问题 | → 先本地查 wiki，再回答 |
| 通用技术问题（无特定上下文）| → 直接 MCP → LLM |
| 回答完有价值的技术问题后 | → 询问"要把这些存进 wiki 吗？" |

## 三层架构

```
$WIKI_ROOT/
├── raw/                  原始文档（只读，用户放入，LLM 不修改）
├── pages/                LLM 生成并维护的 markdown 文件集
│   ├── aws/              AWS 服务、架构、合规
│   ├── ai/               AI/LLM 技术
│   ├── clients/          客户信息（账号、联系人、项目）
│   ├── projects/         具体项目
│   └── ops/              运维、kubectl、DevOps
├── index.md              所有页面目录（标题 + 一行描述 + 路径），每次 ingest 后更新
├── log.md                操作日志（append-only，格式：## [YYYY-MM-DD] ingest | 标题）
└── .ingest-cache.json    SHA256 去重缓存（dedup.py 维护，不进 Obsidian vault）
```

**只有一个 wiki 目录：** `$WIKI_ROOT`（即 Obsidian MCP 的 allowed dir）

## Query 流程

详见 `scripts/query.md`

核心逻辑：
1. `obsidian.read_text_file` 读 `$WIKI_ROOT/index.md`，找相关页面
2. `obsidian.read_text_file` 读相关页面全文，综合回答，标注来源 `> 参考：[[页面名]]`
3. 答案本身有价值 → 询问用户是否存回 wiki

## Ingest 流程

详见 `scripts/ingest.md`

核心逻辑：
0. `dedup.py check` 去重（来源是文件/URL 时）→ DUPLICATE 就停
1. `obsidian.read_text_file` 读 index.md，判断是否已有相关页面
2. `obsidian.write_file` / `obsidian.edit_file` 新建 or 更新页面（一次 ingest 可能触碰 5-15 个页面）
3. `obsidian.edit_file` 更新 index.md
4. `obsidian.edit_file` 追加 log.md（`## [YYYY-MM-DD] ingest | 来源标题`）
5. `dedup.py record` 记录 SHA256 缓存（来源是文件/URL 时）

## Lint 流程

详见 `scripts/lint.md`

检查：孤儿页面、缺失概念页、index.md 不一致、矛盾内容、过时内容
（lint.py 脚本走 Python filesystem 直接读，不经过 MCP；LLM Layer 2 整改时走 MCP）

## 页面模板

```markdown
# 页面标题

**最后更新：** YYYY-MM-DD
**来源数量：** N
**分类：** aws/security
**置信度：** EXTRACTED  <!-- 整页默认值；段落内可局部覆盖 -->

## 概述

## 核心内容

<!-- 置信度可以在段落/句子级别用 inline tag 标注： -->
<!-- [EXTRACTED] 原文直接扒的事实 -->
<!-- [INFERRED]  基于来源推理的结论 -->
<!-- [AMBIGUOUS] 来源本身表述模糊 -->
<!-- [UNVERIFIED] AI 自己补的常识/背景，未经来源验证 -->

## 相关页面
- [[相关页面名]]

## 来源
- [[原始文档页面名]]
- [外部链接](https://...)
```

### 置信度标签规则（强制）

| Tag | 含义 | 什么时候用 |
|-----|------|-----------|
| `EXTRACTED`  | 从来源原文直接扒的事实 | 定价、API 参数、官方原话 |
| `INFERRED`   | 基于来源推理/组合得出 | "所以月成本约 $80"（来源只给了单价） |
| `AMBIGUOUS`  | 来源本身说得不清楚 | 文档自相矛盾或写得模糊 |
| `UNVERIFIED` | AI 补的背景常识，没来源 | 写页面时为了通顺加的常识性描述 |

**原则：**
- 整页默认置信度写在 frontmatter，**不要省略**
- 页面内如果混合了不同置信度的内容，**必须在段落开头/句尾用 inline tag 标注**
- Query 时如果引用了 `INFERRED` / `UNVERIFIED` 的内容，**必须在回答里明说**（"这条是推断的"）

## log.md 格式

每条记录格式：`## [YYYY-MM-DD] {操作} | {标题}`

```
## [2026-04-09] ingest | Karpathy llm-wiki 模式
## [2026-04-09] query | S3 Files POSIX 访问方案
## [2026-04-09] lint | 全库健康检查
```

可用 `grep "^## \[" $WIKI_ROOT/log.md | tail -10` 查最近操作。
