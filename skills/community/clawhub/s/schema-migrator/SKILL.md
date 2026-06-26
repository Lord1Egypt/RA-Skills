---
name: schema-migrator
description: Applies pending database migration files against the target database
tags:
  - database
  - migration
  - schema
  - sql
category: database
version: 1.0.0
---

# 迁移执行器

## 概述

读取索引分析器生成的 Schema 建议文件，验证并对目标数据库执行索引清理操作。记录已执行的清理到数据库。

## 使用场景

- Schema 优化：根据分析建议执行索引清理
- CI/CD 集成：在部署流水线中自动执行 Schema 变更
- 索引维护：基于结构化建议安全执行索引变更

## 使用方法

1. 读取 `/root/.schema/recommendation.json` 获取待清理索引列表。
2. 验证索引名合法性（仅允许 `idx_` 前缀的标识符）。
3. 执行索引删除操作并记录结果。
4. 输出执行报告 JSON。

## 输出格式

```json
{
  "execution_timestamp": "2026-06-01T12:00:10",
  "migrations_executed": ["idx_users_email_unique"],
  "errors": [],
  "status": "completed"
}
```

## 实现代码

见 `scripts/migrate.py`。
