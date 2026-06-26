---
name: sql-index-optimizer-multi-db
description: 当用户希望“通过建表语句 + 慢 SQL 自动优化索引”时使用此 Skill，支持 MySQL、Oracle、PostgreSQL。脚本使用 Python，自动解析 DDL 与慢 SQL 中的 WHERE/JOIN/ORDER BY 列，生成候选索引及对应数据库的 CREATE INDEX 语句，并输出到文件。
---

# 慢 SQL 索引优化 Skill（MySQL / Oracle / PostgreSQL）

## 适用场景
- 用户提供建表 SQL 与慢 SQL，想要自动出索引优化建议。
- 目标是生成一个文件（`md`/`json`），包含候选索引与建议 DDL。

## 需要的信息
1. `dialect`：`mysql` / `oracle` / `postgresql`
2. `ddl_file`：建表语句文件路径
3. `slow_sql_file`：慢 SQL 文件路径（可多条，分号分隔）
4. `format`（可选）：`md`/`json`（默认 `md`）
5. `out`（可选）：输出路径

## 执行方式
脚本路径：

- `/.cursor/skills/sql-index-optimizer-multi-db/scripts/optimize_indexes.py`

示例：

```bash
python3 "/path/to/optimize_indexes.py" \
  --dialect mysql \
  --ddl-file "/path/to/schema.sql" \
  --slow-sql-file "/path/to/slow.sql" \
  --format md \
  --out "/path/to/index_optimization.mysql.md"
```

## 输出内容
- 统计信息（表数量、慢 SQL 数量、建议索引数）
- 每条候选索引的原因（WHERE/JOIN/ORDER 命中列）
- 对应数据库方言的 `CREATE INDEX` 语句
- 注意事项（需结合执行计划复核）

## 规则说明（启发式）
- 自动识别：
  - WHERE 过滤列
  - JOIN 连接列
  - ORDER BY 排序列
- 复合索引优先顺序：过滤列 -> 连接列 -> 排序列
- 跳过与现有索引前缀重复的候选

## 限制与提醒
- 这是规则建议，不等同于最终执行方案。
- 生产库执行前请结合：
  - MySQL: `EXPLAIN ANALYZE`
  - Oracle: AWR / 执行计划
  - PostgreSQL: `EXPLAIN (ANALYZE, BUFFERS)`、`pg_stat_statements`
- 高写入表需评估索引维护成本。
