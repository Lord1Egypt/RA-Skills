---
name: 数据库访问服务
description: MCP Database Server 是一个为AI助手和基于LLM的工具提供安全数据库访问的服务，支持SQLite、PostgreSQL、MySQL和MariaDB，具有查询验证、审计日志和安全控制功能。
version: 1.0.0
---

# 数据库访问服务

MCP Database Server 是一个为AI助手和基于LLM的工具提供安全数据库访问的服务，支持SQLite、PostgreSQL、MySQL和MariaDB，具有查询验证、审计日志和安全控制功能。

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
| List all tables in the database, optionally filtered by schema. Returns qualified table names. | `scripts.tools.db_tables` |
| Get column information for a specific table including column names, data types, and nullability. | `scripts.tools.db_describe_table` |
| Execute a SQL statement. Supports SELECT (read), INSERT/UPDATE/DELETE (write if enabled), and DDL (if enabled). Use named parameters with :param syntax. | `scripts.tools.db_execute` |
| Get query execution plan and performance information using EXPLAIN. Helps analyze query performance and optimization opportunities. | `scripts.tools.db_explain` |

**如果参数不完整，使用 AskUserQuestion 向用户询问缺失的参数。**

---

## 工具函数说明

---

## scripts.tools.db_tables
工具描述：List all tables in the database, optionally filtered by schema. Returns qualified table names.
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|db_url|string|false| |Optional database URL override (e.g., sqlite:///./dev.db, postgresql://...)|
|schema|string|false| |Optional schema name filter (PostgreSQL only)|

---

## scripts.tools.db_describe_table
工具描述：Get column information for a specific table including column names, data types, and nullability.
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|db_url|string|false| |Optional database URL override|
|schema|string|false| |Optional schema name (PostgreSQL only)|
|table|string|true| |Table name to describe|

---

## scripts.tools.db_execute
工具描述：Execute a SQL statement. Supports SELECT (read), INSERT/UPDATE/DELETE (write if enabled), and DDL (if enabled). Use named parameters with :param syntax.
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|db_url|string|false| |Optional database URL override|
|sql|string|true| |SQL statement to execute (single statement only)|
|args|object|false| |Named parameters for the SQL statement (e.g., {name: 'John'})|
|allow_write|boolean|false| |Set to true to allow write operations (requires ALLOW_WRITES=true)|
|row_limit|number|false| |Maximum rows to return for SELECT queries|

---

## scripts.tools.db_explain
工具描述：Get query execution plan and performance information using EXPLAIN. Helps analyze query performance and optimization opportunities.
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|db_url|string|false| |Optional database URL override|
|sql|string|true| |SQL query to explain (typically a SELECT statement)|
|args|object|false| |Named parameters for the SQL statement (e.g., {name: 'John'})|
|analyze|boolean|false| |Run EXPLAIN ANALYZE to get actual execution statistics (executes the query)|

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