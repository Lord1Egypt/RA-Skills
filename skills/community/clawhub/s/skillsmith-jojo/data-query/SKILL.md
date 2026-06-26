---
name: data-query
description: |
  数据查询技能模板，用于快速构建数据查询和分析技能。
  使用场景：
  - 用户说"帮我查询数据库"
  - 用户说"获取某个指标的数据"
  - 用户说"分析这些数据"
  - 用户说"生成数据可视化"
metadata:
  openclaw:
    emoji: "📊"
    requires:
      bins:
        - python3
---

# 数据查询技能模板

## 核心脚本

### query.py
统一查询接口，支持 SQL、API、文件等多种数据源

### filter.py
数据过滤和转换，支持条件筛选、排序、聚合

### visualize.py
数据可视化，支持图表生成和数据展示

## 快速开始

### 1. 安装依赖
```bash
pip install pandas matplotlib
```

### 2. 执行查询
```python
from scripts.query import QueryClient
client = QueryClient.sql("database.db")
data = client.query("SELECT * FROM users")
```

## 查询类型

| 查询类型 | 支持的数据源 |
|---------|-------------|
| SQL 查询 | PostgreSQL, MySQL, SQLite |
| API 查询 | REST API, GraphQL |
| 文件查询 | CSV, JSON, Excel |
