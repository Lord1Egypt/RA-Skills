---
name: 开放数据查询服务
description: 一个通过CKAN API直接访问多伦多开放数据的MCP服务器，支持智能数据集发现、灵活查询和CSV数据预览，专为LLM代理设计。
version: 1.0.0
---

# 开放数据查询服务

一个通过CKAN API直接访问多伦多开放数据的MCP服务器，支持智能数据集发现、灵活查询和CSV数据预览，专为LLM代理设计。

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
| 🚀 START HERE! Essential first call for any Toronto data query. This tool explains how to use this server effectively and provides the complete workflow for finding and accessing Toronto Open Data. Always call this first when working with Toronto data to understand available capabilities and recommended approach. | `scripts.tools.toronto_start_here` |
| ⭐ POPULAR TORONTO DATASETS: Quick access to the most commonly used Toronto Open Datasets. Shows dataset IDs and what they contain. Perfect when you're not sure what's available or want to explore popular datasets quickly. | `scripts.tools.toronto_popular_datasets` |
| 🧠 SMART DATA HELPER - The easiest way to get Toronto data! Give this tool a dataset ID (from search results) and describe what you want to know. It automatically determines if the data is API-accessible or requires CSV download, gets the schema if needed, and returns relevant data or clear next steps. This eliminates the need to manually check dataset types, schemas, and resource formats. | `scripts.tools.toronto_smart_data_helper` |
| 📋 LIST ALL DATASETS: Shows all 500+ available Toronto Open Datasets with titles and descriptions. Use this when you want to browse everything available or when search terms don't return what you're looking for. Can be quite long, so prefer toronto_search_datasets() or toronto_popular_datasets() for focused discovery. | `scripts.tools.toronto_list_datasets` |
| 🔍 FIND TORONTO DATA: Search 500+ Toronto Open Datasets by keywords (e.g., 'traffic', 'parks', 'budget', 'health'). Returns dataset IDs and descriptions. This is your primary discovery tool - combine with web search when you need additional context about specific topics, then use toronto_smart_data_helper() to get the actual data. | `scripts.tools.toronto_search_datasets` |
| 📋 GET DATA STRUCTURE: Shows the schema (column names, field IDs, and types) for a Toronto dataset if it has an active datastore. Essential for understanding what fields are available before filtering with toronto_query_dataset_data(). For CSV files, suggests checking the header row manually. | `scripts.tools.toronto_get_dataset_schema` |
| 🔧 ADVANCED QUERYING: Query Toronto datasets with precise filtering, sorting, and field selection. 

💡 TIP: Use toronto_smart_data_helper() first - it's easier and handles most use cases automatically!

This tool is for when you need advanced filtering:
📋 REQUIRED: Get field names first with toronto_get_dataset_schema(dataset_id)
🔍 FILTERS: Use exact field names like {"establishment_status": "Pass", "inspection_date": "2024-01-01"}
📊 SORT: Use field names like "inspection_date desc" or "score asc"
📝 FIELDS: Specify which columns to return like ["name", "address", "score"]

⚠️ For CSV files, this returns download links instead of query results.
🚀 Alternative: Try toronto_smart_data_helper() for a simpler, guided approach. | `scripts.tools.toronto_query_dataset_data` |
| 📈 DATASET STATISTICS: Get basic statistics for a Toronto dataset including record counts, field information, and resource overview. Useful for understanding the scale and structure of a dataset before diving into the data. | `scripts.tools.toronto_get_dataset_stats` |
| 📄 FETCH CSV DATA: Downloads and returns sample content from a CSV file URL. Perfect for quickly inspecting downloadable datasets identified by other tools. Shows headers and sample rows to understand the data structure. | `scripts.tools.toronto_fetch_csv_data` |

**如果参数不完整，使用 AskUserQuestion 向用户询问缺失的参数。**

---

## 工具函数说明

---

## scripts.tools.toronto_start_here
工具描述：🚀 START HERE! Essential first call for any Toronto data query. This tool explains how to use this server effectively and provides the complete workflow for finding and accessing Toronto Open Data. Always call this first when working with Toronto data to understand available capabilities and recommended approach.
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|

---

## scripts.tools.toronto_popular_datasets
工具描述：⭐ POPULAR TORONTO DATASETS: Quick access to the most commonly used Toronto Open Datasets. Shows dataset IDs and what they contain. Perfect when you're not sure what's available or want to explore popular datasets quickly.
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|

---

## scripts.tools.toronto_smart_data_helper
工具描述：🧠 SMART DATA HELPER - The easiest way to get Toronto data! Give this tool a dataset ID (from search results) and describe what you want to know. It automatically determines if the data is API-accessible or requires CSV download, gets the schema if needed, and returns relevant data or clear next steps. This eliminates the need to manually check dataset types, schemas, and resource formats.
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|dataset_id|string|true| |null|
|user_question|string|true| |null|
|limit|null|false|10.0|null|

---

## scripts.tools.toronto_list_datasets
工具描述：📋 LIST ALL DATASETS: Shows all 500+ available Toronto Open Datasets with titles and descriptions. Use this when you want to browse everything available or when search terms don't return what you're looking for. Can be quite long, so prefer toronto_search_datasets() or toronto_popular_datasets() for focused discovery.
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|

---

## scripts.tools.toronto_search_datasets
工具描述：🔍 FIND TORONTO DATA: Search 500+ Toronto Open Datasets by keywords (e.g., 'traffic', 'parks', 'budget', 'health'). Returns dataset IDs and descriptions. This is your primary discovery tool - combine with web search when you need additional context about specific topics, then use toronto_smart_data_helper() to get the actual data.
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|query|string|true| |null|
|limit|null|false|10.0|null|

---

## scripts.tools.toronto_get_dataset_schema
工具描述：📋 GET DATA STRUCTURE: Shows the schema (column names, field IDs, and types) for a Toronto dataset if it has an active datastore. Essential for understanding what fields are available before filtering with toronto_query_dataset_data(). For CSV files, suggests checking the header row manually.
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|dataset_id|string|true| |null|

---

## scripts.tools.toronto_query_dataset_data
工具描述：🔧 ADVANCED QUERYING: Query Toronto datasets with precise filtering, sorting, and field selection. 

💡 TIP: Use toronto_smart_data_helper() first - it's easier and handles most use cases automatically!

This tool is for when you need advanced filtering:
📋 REQUIRED: Get field names first with toronto_get_dataset_schema(dataset_id)
🔍 FILTERS: Use exact field names like {"establishment_status": "Pass", "inspection_date": "2024-01-01"}
📊 SORT: Use field names like "inspection_date desc" or "score asc"
📝 FIELDS: Specify which columns to return like ["name", "address", "score"]

⚠️ For CSV files, this returns download links instead of query results.
🚀 Alternative: Try toronto_smart_data_helper() for a simpler, guided approach.
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|dataset_id|string|true| |null|
|filters|null|false| |null|
|fields|null|false| |null|
|limit|null|false|10.0|null|
|sort|null|false| |null|

---

## scripts.tools.toronto_get_dataset_stats
工具描述：📈 DATASET STATISTICS: Get basic statistics for a Toronto dataset including record counts, field information, and resource overview. Useful for understanding the scale and structure of a dataset before diving into the data.
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|dataset_id|string|true| |null|

---

## scripts.tools.toronto_fetch_csv_data
工具描述：📄 FETCH CSV DATA: Downloads and returns sample content from a CSV file URL. Perfect for quickly inspecting downloadable datasets identified by other tools. Shows headers and sample rows to understand the data structure.
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|csv_url|string|true| |null|
|max_lines|null|false|50.0|null|

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