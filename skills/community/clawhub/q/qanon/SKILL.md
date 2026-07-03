---
name: QAnon帖子分析服务
description: 一个提供QAnon帖子数据集访问的MCP服务器，用于人类学和社会学研究，支持搜索、过滤和分析功能。
version: 1.0.0
---

# QAnon帖子分析服务

一个提供QAnon帖子数据集访问的MCP服务器，用于人类学和社会学研究，支持搜索、过滤和分析功能。

---

## ⚠️ 强制要求：API 密钥

**此 Skill 必须配置 API 密钥才能使用。**

- 首次使用时，如果 `.env` 中没有 `XBY_APIKEY`，**必须使用 AskUserQuestion 工具向用户询问 API 密钥**
- 拿到用户提供的密钥后，调用 `scripts.config.set_api_key(api_key)` 保存，然后继续处理
- 获取 API 密钥：https://xiaobenyang.com
- **禁止**在缺少 API 密钥时自行搜索或编造数据

---

## 工作流程（必须遵守）

你（大模型）是路由层，负责理解用户意图、选择工具、提取参数。代码只负责调用API。

```
用户输入 → 你选择工具 → 提取该工具需要的参数 → 调用 scripts.tools 中的函数 → 返回结果给用户
```

### 步骤

1. **检查 API 密钥**：如果 `scripts.config.settings.api_key` 为空，使用 AskUserQuestion 询问用户，拿到后调用 `scripts.config.set_api_key(key)` 保存
2. **选择工具**：根据用户意图从下方工具列表中选择对应的工具函数
3. **提取参数**：根据选中的工具，提取该工具需要的参数
4. **调用工具**：使用**关键字参数**调用 `scripts.tools` 中的函数，例如 `scripts.tools.search_schools(score='520', province='北京', category='综合')`
5. **返回结果**：将工具返回的 `raw` 数据整理后展示给用户

---
## 工具选择规则

根据用户意图选择对应的工具函数：

| 用户意图 | 工具函数 | 
|---------|---------|
| 
Retrieve a specific post by its ID.

Args:
    post_id: The ID of the post to retrieve
 | `scripts.tools.get_post_by_id_tool` |
| 
Search for posts/drops containing a specific keyword or phrase.

Args:
    query: The keyword or phrase to search for
    limit: Maximum number of results to return (default: 10)
 | `scripts.tools.search_posts` |
| 
Get posts/drops within a specific date range.

Args:
    start_date: Start date in YYYY-MM-DD format
    end_date: End date in YYYY-MM-DD format (defaults to start_date if not provided)
    limit: Maximum number of results to return (default: 10)
 | `scripts.tools.get_posts_by_date` |
| 
Get posts/drops by a specific author ID.

Args:
    author_id: The author ID to search for
    limit: Maximum number of results to return (default: 10)
 | `scripts.tools.get_posts_by_author_id` |
| 
Get detailed analysis of a specific post/drop including references and context.

Args:
    post_id: The ID of the post to analyze
 | `scripts.tools.analyze_post` |
| 
Get a timeline summary of posts/drops, optionally within a date range.

Args:
    start_date: Optional start date in YYYY-MM-DD format
    end_date: Optional end date in YYYY-MM-DD format
 | `scripts.tools.get_timeline_summary` |
| 
Generate a word cloud analysis showing the most common words used in posts within a specified ID range.

Args:
    start_id: Starting post ID
    end_id: Ending post ID
    min_word_length: Minimum length of words to include (default: 3)
    max_words: Maximum number of words to return (default: 100)
 | `scripts.tools.word_cloud_by_post_ids` |
| 
Generate a word cloud analysis showing the most common words used in posts within a specified date range.

Args:
    start_date: Start date in YYYY-MM-DD format
    end_date: End date in YYYY-MM-DD format
    min_word_length: Minimum length of words to include (default: 3)
    max_words: Maximum number of words to return (default: 100)
 | `scripts.tools.word_cloud_by_date_range` |

**如果参数不完整，使用 AskUserQuestion 向用户询问缺失的参数。**

---

## 工具函数说明

---

## scripts.tools.get_post_by_id_tool
工具描述：
Retrieve a specific post by its ID.

Args:
    post_id: The ID of the post to retrieve

### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|post_id|integer|true| |null|

---

## scripts.tools.search_posts
工具描述：
Search for posts/drops containing a specific keyword or phrase.

Args:
    query: The keyword or phrase to search for
    limit: Maximum number of results to return (default: 10)

### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|query|string|true| |null|
|limit|integer|false|10.0|null|

---

## scripts.tools.get_posts_by_date
工具描述：
Get posts/drops within a specific date range.

Args:
    start_date: Start date in YYYY-MM-DD format
    end_date: End date in YYYY-MM-DD format (defaults to start_date if not provided)
    limit: Maximum number of results to return (default: 10)

### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|start_date|string|true| |null|
|end_date|string|false| |null|
|limit|integer|false|10.0|null|

---

## scripts.tools.get_posts_by_author_id
工具描述：
Get posts/drops by a specific author ID.

Args:
    author_id: The author ID to search for
    limit: Maximum number of results to return (default: 10)

### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|author_id|string|true| |null|
|limit|integer|false|10.0|null|

---

## scripts.tools.analyze_post
工具描述：
Get detailed analysis of a specific post/drop including references and context.

Args:
    post_id: The ID of the post to analyze

### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|post_id|integer|true| |null|

---

## scripts.tools.get_timeline_summary
工具描述：
Get a timeline summary of posts/drops, optionally within a date range.

Args:
    start_date: Optional start date in YYYY-MM-DD format
    end_date: Optional end date in YYYY-MM-DD format

### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|start_date|string|false| |null|
|end_date|string|false| |null|

---

## scripts.tools.word_cloud_by_post_ids
工具描述：
Generate a word cloud analysis showing the most common words used in posts within a specified ID range.

Args:
    start_id: Starting post ID
    end_id: Ending post ID
    min_word_length: Minimum length of words to include (default: 3)
    max_words: Maximum number of words to return (default: 100)

### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|start_id|integer|true| |null|
|end_id|integer|true| |null|
|min_word_length|integer|false|3.0|null|
|max_words|integer|false|100.0|null|

---

## scripts.tools.word_cloud_by_date_range
工具描述：
Generate a word cloud analysis showing the most common words used in posts within a specified date range.

Args:
    start_date: Start date in YYYY-MM-DD format
    end_date: End date in YYYY-MM-DD format
    min_word_length: Minimum length of words to include (default: 3)
    max_words: Maximum number of words to return (default: 100)

### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|start_date|string|true| |null|
|end_date|string|true| |null|
|min_word_length|integer|false|3.0|null|
|max_words|integer|false|100.0|null|

---


---

## 返回值处理

工具函数返回 `dict` 对象：
- `result["raw"]` - API 原始返回数据（JSON），**直接将此数据整理后展示给用户**
- `result["success"]` - 是否成功（True/False）
- `result["message"]` - 状态消息

---

## 项目结构

```
xiaobenyang_gaokao_skill/
├── scripts/
│   ├── __init__.py
│   ├── config.py       # 配置管理 + set_api_key()
│   ├── call_api.py      # API 客户端 + call_api()
│   └── tools.py         # 工具函数（直接调用）
├── requirements.txt
└── SKILL.md
```

---

## 注意事项

1. **API 密钥是必需的**，无密钥时必须通过 AskUserQuestion 询问用户
2. **禁止**在缺少 API 密钥时自行搜索或编造数据