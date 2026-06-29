# Conditional Pass: Plugin Discovery

**加载时机：** 📍 仅当 Prompt 涉及外部能力时加载。

---

## 触发条件

Prompt 或 Pass 2 的 IR 中出现以下信号：

| 信号 | 对应插件能力 |
|------|------------|
| search, 搜索, google, bing | Web Search |
| github, git, repo, PR | GitHub |
| database, db, sql, query | Database |
| browser, scrape, crawl, 浏览器 | Browser |
| ocr, image, recognize | OCR / Vision |
| mcp, tool, server | MCP |
| notion, document | Notion / Docs |
| linear, jira, ticket | Issue Tracker |
| api, endpoint, request | External API |

---

## 执行步骤

### Step 1 — 识别外部能力

扫描 IR，列出 Prompt 涉及的所有外部能力。

### Step 2 — 评估插件化必要性

| 条件 | 插件化 |
|------|--------|
| 能力是 Skill 的核心功能 | 不插件化，内联 |
| 能力是可选增强 | 插件化 |
| 能力有多种实现方式 | 插件化 |

### Step 3 — 生成 plugins.md

写入生成的 Skill 的 `references/plugins.md`：

```markdown
# Plugin Opportunities

> 以下能力未来可插件化，当前版本未实现。

## {Plugin Name}
- **能力：** {描述}
- **触发场景：** {什么时候需要}
- **建议接口：** {API 设计草案}
- **优先级：** high | medium | low
```

### Step 4 — 更新 IR

在 IR 中添加 `plugins` 字段，记录插件化决策。
