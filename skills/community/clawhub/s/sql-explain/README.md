# sql-explain

**SQL 解释器 CLI 工具** — 本地运行的 SQL 格式化、语法检查、执行计划分析、自然语言转 SQL 工具。

无需 API key，无需联网，纯 Python 实现。

---

## 与 AI Skill 的区别

| | AI Skill (sql-explain) | 本 CLI 工具 |
|---|---|---|
| **交互方式** | AI 对话，解释意图 | 命令行直接输出 |
| **EXPLAIN 解析** | AI 理解执行计划 | 规则引擎解析 |
| **自然语言转 SQL** | AI 生成（可选） | 本地模板转换 |
| **依赖** | AI API (付费/限流) | 无外部依赖 |
| **速度** | 依赖网络 + AI | 毫秒级响应 |
| **适用场景** | 复杂分析、教学 | 快速格式化、CI 检查 |

---

## 安装

```bash
pip install sqlparse

# 或直接下载
curl -O https://raw.githubusercontent.com/your-repo/main/sql_explain.py
chmod +x sql_explain.py
```

---

## 使用方法

### Python API

```python
from sql_explain import format_sql, check_syntax, analyze_sql_structure, nl_to_sql, explain_sql

# 格式化 SQL
print(format_sql("select * from users where id=1"))
# SELECT
#   *
# FROM users
# WHERE id = 1

# 检查语法
result = check_syntax("SELECT * FORM users")  # 注意 FORM 拼写错误
print(result)
# {"valid": false, "errors": [...], "statement_count": 1}

# 分析 SQL 结构
result = analyze_sql_structure("SELECT u.name FROM users u JOIN orders o ON u.id=o.user_id")
print(result)
# {"type": "SELECT", "tables": ["users", "orders"], "complexity": "MODERATE", ...}

# 自然语言转 SQL
sql = nl_to_sql("查询所有订单")
print(sql)
# SELECT * FROM your_table LIMIT 10;

# 解析 EXPLAIN 输出（PostgreSQL）
report = explain_sql("Seq Scan on users (cost=0.00..100.00 rows=1000 width=100)")
print(report)
```

### CLI 命令

```bash
# 格式化 SQL
python sql_explain.py format "SELECT * FROM users WHERE id=1"

# 语法检查
python sql_explain.py check "SELECT * FROM users"

# 分析 SQL 结构
python sql_explain.py analyze "SELECT u.name FROM users u JOIN orders o ON u.id=o.user_id"

# 自然语言转 SQL
python sql_explain.py nl2sql "查询所有订单"

# 解析 EXPLAIN（PostgreSQL 格式）
python sql_explain.py explain "Seq Scan on users (cost=0.00..100.00 rows=1000 width=100)"

# 帮助
python sql_explain.py help
```

### Keyword 风格入口（cli.py）

```bash
# 安装（可选）
sudo ln -s $(pwd)/cli.py /usr/local/bin/sql-explain

# 格式化
sql-explain format "SELECT * FROM users"

# 检查语法
sql-explain check "SELECT * FRM users"

# 分析结构
sql-explain analyze "SELECT u.name FROM users u JOIN orders o ON u.id=o.user_id"

# 自然语言转 SQL
sql-explain nl2sql "查询所有订单"
```

---

## CLI 命令详解

### format

格式化 SQL 语句，关键字大写、缩进对齐。

```bash
python sql_explain.py format "select id,name from users where status=1"
```

### check

检查 SQL 语法错误，返回 JSON 格式结果。

```bash
python sql_explain.py check "SELECT * FORM users"
# {
#   "valid": false,
#   "errors": ["语法错误: ..."],
#   "statement_count": 1
# }
```

### analyze

分析 SQL 结构，返回类型、表名、复杂度评估。

```bash
python sql_explain.py analyze "SELECT * FROM users u JOIN orders o ON u.id=o.user_id"
# {
#   "type": "SELECT",
#   "tables": ["users", "orders"],
#   "complexity": "MODERATE",
#   "complexity_factors": ["+JOIN"],
#   "token_count": 15
# }
```

### nl2sql

将中文描述转为 SQL（模板匹配，非 AI）。

```bash
python sql_explain.py nl2sql "查询 users 表前 10 条数据"
# SELECT * FROM users LIMIT 10;
```

### explain

解析 PostgreSQL EXPLAIN 输出，生成分析报告。

```bash
python sql_explain.py explain "Seq Scan on users (cost=0.00..100.00 rows=1000 width=100)"
# 📊 **EXPLAIN 查询计划分析**
# 🎯 **总成本**: 100.0
# 📦 **预计返回**: 1000 行
# ⚠️ **性能关注点**:
#   - 🔴 使用全表扫描，数据量大时性能差
# 💡 **优化建议**:
#   - 💡 考虑在 WHERE 条件列上建立索引
```

---

## 复杂度评估规则

| 复杂度 | 条件 |
|--------|------|
| SIMPLE | 无复杂因素 |
| MODERATE | 1-2 个复杂因素 |
| COMPLEX | 3+ 个复杂因素 |

**复杂因素包括**: JOIN、GROUP BY、HAVING、ORDER BY、LIMIT、子查询(括号>2)、长语句(>50 tokens)、OR 条件

---

## 支持的数据库

- PostgreSQL（EXPLAIN 格式完全支持）
- MySQL（部分支持）
- SQLite（部分支持）

---

## 项目结构

```
sql-explain/
├── sql_explain.py    # 核心功能（294行）
├── cli.py            # keyword 风格入口
├── test_sql_explain.py  # pytest 测试用例
├── README.md         # 本文件
└── SKILL.md          # AI Skill 设计文档
```

---

## 测试

```bash
pip install pytest
pytest test_sql_explain.py -v
```

---

## License

MIT
