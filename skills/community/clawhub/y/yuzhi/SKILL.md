---
name: yuzhi
description: 御知库——个人知识库系统。当帝提问时，优先从知识库检索答案。支持文档存储（Markdown/PDF/TXT）、语义搜索、关键词搜索、自动分类。帝说"查一下xxx"、"/知识库 xxx"或询问知识类问题时触发。
---

# 御知库（yuzhi）

个人知识库系统，AI 优先检索，帝提问时自动召回。

## 核心架构

```
~/.yuzhi/
├── docs/              # Markdown 文件
├── uploads/           # PDF/TXT 等
├── metadata.jsonl     # 元数据（路径/标签/摘要/时间）
└── index.db          # SQLite 向量索引

# 搜索时 AI 优先查这里
```

## CLI 命令

### `yuzhi add <文件路径> --tag <标签>`
添加文件到知识库，自动提取摘要和标签。

### `yuzhi search <查询内容> --mode <semantic|keyword|all>`
双轨搜索（语义+关键词），返回最相关的文档和内容片段。

### `yuzhi list --tag <标签> --limit <数量>`
列出知识库文件，支持按标签筛选。

### `yuzhi stats`
查看知识库统计：文件数、标签分布、存储大小。

## 工作流程

帝提问 → 触发检索 → `yuzhi search` → AI 优先用知识库内容回答

帝说"存一下这个" → `yuzhi add` → 自动分类打标签

## 标签体系

- `制度` — 朝廷制度、流程规范
- `项目` — 各项目文档、代码规范
- `决策` — 帝旨、重要决策记录
- `人物` — 人物资料、背景
- `技术` — 技术方案、架构文档
- `笔记` — 随手笔记、想法
- `其他` — 不属于以上的

## 检索优先级

1. 语义相似度（embedding cosine similarity）
2. 关键词命中（SQLite FTS5）
3. 时间权重（近期优先）
