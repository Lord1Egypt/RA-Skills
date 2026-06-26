---
name: siyuan-llm-wiki
description: >
  在思源笔记中复现 Karpathy 的 LLM Wiki 工作流。
  通过思源 HTTP API 让 AI Agent 维护结构化知识库，支持来源摘要、实体页、概念页、
  综合分析和双向链接。利用思源原生 SQL 查询和块级引用实现比 Obsidian 更精细的知识管理。
---

# Siyuan LLM Wiki Skill

## 简介

本 Skill 用于在**思源笔记**中复现 Karpathy 的 LLM Wiki 工作流。

Karpathy 的原始方案使用 Obsidian + Claude Code 维护一个 Markdown 知识库。本 Skill 将其迁移到思源笔记，利用思源的原生 SQL 查询、块级引用和 HTTP API，构建一个更强大的 AI 维护型个人知识库。

## 核心思想

> 不要把 LLM 当搜索引擎用，而是让它像程序员写代码一样，帮你持续维护一个结构化知识库。

- **你负责**：找资料、提好问题、做判断
- **Agent 负责**：总结、交叉引用、分类整理、保持一致性
- **思源负责**：存储、链接、查询、可视化

## 前置条件

1. **思源笔记**已安装并运行（v3.x 以上）
2. 开启思源 HTTP API：
   - 设置 → 关于 → API Token → 复制 Token
   - 默认地址：`http://127.0.0.1:6806`（如果修改过端口，请使用实际端口）
3. 一个支持本地文件/网络请求的 AI Agent（Claude Code、Kimi CLI、Cursor 等）
4. 在思源中创建一个笔记本，命名为 `LLM-Wiki`（或任意名字）

## 快速开始

### 1. 测试 API 连接

```bash
curl -X POST http://127.0.0.1:6806/api/system/version \
  -H "Authorization: Token <你的Token>" \
  -H "Content-Type: application/json" \
  -d '{}'
```
> 注意：如果思源笔记使用了非默认端口（如 6808、4976 等），请替换为实际端口。

返回 `{"code":0,"data":"3.x.x"}` 即表示连接成功。

### 2. 获取笔记本 ID

```bash
curl -X POST http://127.0.0.1:6806/api/notebook/lsNotebooks \
  -H "Authorization: Token <你的Token>" \
  -H "Content-Type: application/json" \
  -d '{}'
```

找到 `LLM-Wiki` 对应的 `id` 字段，记下来。

### 3. 让 Agent 开始工作

将本目录下的 `agents.md` 的内容复制给你的 Agent，然后告诉它：

> "在思源笔记的 LLM-Wiki 笔记本中，帮我搭建一个知识库。这是思源的 API Token: xxx，笔记本 ID: xxx。"

Agent 会按照 `agents.md` 中的指南自动完成初始化。

## 工作流

### Ingestion（吸收资料）

1. 你将原始资料放入 `raw/`（可以是思源中的一个文件夹，也可以是本地目录）
2. 告诉 Agent："把这篇文章整理进知识库"
3. Agent 读取资料 → 分析 → 调用思源 API 创建结构化文档 → 自动建立链接

### Query（查询知识）+ 记忆反写

1. 你在思源中提问，或直接在 Agent 中提问
2. Agent 调用思源的 SQL API 检索相关内容
3. Agent 综合回答，标注来源
4. **Agent 判断这个回答是否值得永久保存**（跨来源分析、新发现、矛盾、用户明确指示）
5. **如果需要保存**：在 `syntheses/` 创建综合页，记录问题、分析过程、结论、引用来源
6. 更新 `index.md` 和 `log.md`

> **核心洞察**：不是保存聊天记录，而是保存对话中产生的**结构化知识**。每次查询都让知识库更 rich，这就是复利增长。

### Maintenance（维护）

1. 定期让 Agent 运行 `lint`：检查孤立页面、失效链接、重复概念
2. Agent 自动修复或给你报告

## 目录结构

```
siyuan-llm-wiki/
├── SKILL.md              # 本文件：使用说明
├── agents.md             # Agent 操作指南（核心）
├── templates/            # 思源文档模板
│   ├── sy-source.md      # 来源摘要模板
│   ├── sy-entity.md      # 实体页模板
│   ├── sy-concept.md     # 概念页模板
│   ├── sy-synthesis.md   # 综合页模板
│   ├── sy-index.md       # 索引页模板
│   └── sy-log.md         # 日志页模板
├── examples/             # API 调用示例
│   └── api-calls.md
└── scripts/              # 辅助脚本（可选）
    └── siyuan_api.py     # Python API 封装
```

## 思源 vs Obsidian 的关键差异

| 方面 | Obsidian | 思源笔记 |
|------|----------|----------|
| Agent 操作 | 直接读写 `.md` 文件 | HTTP API |
| 查询 | Dataview 插件 | **原生 SQL** |
| 粒度 | 文档级 | **块级** |
| 链接语法 | `[[wikilink]]` | `[[文档]]` / `((块ID))` |
| **双向链接** | Dataview 扫描 | **`((块ID))` 建立真正的引用关系**，`[[文档名]]` 只是普通链接 |
| 属性 | YAML frontmatter | **任意块属性** |

## 进阶技巧

### 使用 SQL 做复杂查询

思源的数据库 schema 核心表：
- `blocks` - 所有内容块
- `refs` - 引用关系
- `attributes` - 块属性

示例查询：
```sql
-- 查找知识库中所有提到 "RAG" 的段落
SELECT id, content, path 
FROM blocks 
WHERE content LIKE '%RAG%' 
  AND path LIKE '/LLM-Wiki/%'
  AND type = 'p'
ORDER BY updated DESC
LIMIT 20;

-- 查找被引用最多的实体页
SELECT defBlockID, COUNT(*) as ref_count 
FROM refs 
WHERE defBlockPath LIKE '/LLM-Wiki/entities/%'
GROUP BY defBlockID 
ORDER BY ref_count DESC 
LIMIT 10;
```

### 块属性作为元数据

思源可以给任意块设置属性（不只是文档），Agent 可以通过 API 打标签：

```json
POST /api/attr/setBlockAttrs
{
  "id": "20240430120000-xxx",
  "attrs": {
    "custom-importance": "high",
    "custom-status": "reviewed",
    "custom-source": "arxiv"
  }
}
```

然后可以用 SQL 按属性筛选：
```sql
SELECT * FROM attributes 
WHERE name = 'custom-importance' 
  AND value = 'high';
```

## 参考

- Karpathy 原始 Gist: https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f
- 思源 API 文档: https://leolee9086.github.io/siyuan-kernelApi-docs/
- 思源社区 API 汇总: https://www.siyuan-note.club/llms.txt
- 思源 GitHub API 文档: https://github.com/siyuan-note/siyuan/blob/master/API_zh_CN.md
