# Semantic Search - 快速参考

## 一句话介绍
企业级语义检索技能，支持表格/字段/文件搜索和 Text-to-SQL 数据生成。基于 LanceDB/FlightSQL 向量数据库，支持 BGE-M3 Embedding 和多种 LLM 模型。

## 快速开始

### 1. 安装
```bash
npx clawhub install semantic-search
```

### 2. 配置

**方式 1: 环境变量（推荐）**
```bash
export FLIGHT_DB_HOST="your-db-host"
export FLIGHT_DB_PORT="31337"
export FLIGHT_DB_USER="admin"
export FLIGHT_DB_PASSWORD="your_password"
export LLM_API_KEY="sk-xxx"
```

**方式 2: .env 文件**
```bash
cp .env.example .env
# 编辑 .env 填入实际配置
```

**方式 3: 项目集成**
```python
# 如果在项目中使用，自动使用项目配置
skill = SemanticSearchSkill()
```

### 3. 使用
```python
from openclaw import skill

# 表格检索
result = await skill.invoke("semantic-search", {
    "action": "table_search",
    "query": "查找用户相关的表",
    "limit": 10
})

# 字段检索
result = await skill.invoke("semantic-search", {
    "action": "field_search",
    "query": "查找创建时间字段",
    "resource_id": 1
})

# Text-to-SQL
result = await skill.invoke("semantic-search", {
    "action": "data_gen",
    "query": "查询最近注册用户数",
    "resource_id": 1
})
```

## 核心功能

| 功能 | Action | 输入 | 输出 |
|------|--------|------|------|
| 表格检索 | `table_search` | query, limit | 表列表 |
| 字段检索 | `field_search` | query, resource_id | 字段列表 |
| 数据生成 | `data_gen` | query, resource_id | 数据 + SQL |
| 文件检索 | `file_search` | query, search_type | 文件列表 |

## 技术特色

- 🔍 **混合检索**: BM25 + 向量 (1024 维)
- 🧠 **AI 原生**: LLM 意图识别 + 查询增强
- ⚡ **高性能**: P95 < 2s, 支持 100+ QPS
- 🔄 **工作流编排**: LangGraph 图引擎
- 💾 **定制向量库**: LanceDB/FlightSQL

## 详细文档

查看 `SKILL.md` 获取完整使用说明。

---

*版本：1.0.0 | 更新时间：2026-03-04*
