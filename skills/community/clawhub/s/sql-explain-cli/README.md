# 🔍 sql-explain

**SQL 解释器 CLI 工具** — 本地运行的 SQL 格式化、语法检查、执行计划分析、自然语言转 SQL 工具。

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![PyPI](https://img.shields.io/badge/pip-installsqlparse-orange.svg)](https://pypi.org/project/sqlparse/)

> ⚡ 无需 API key，无需联网，纯 Python 实现，毫秒级响应。

---

## ✨ 功能特性

| 命令 | 说明 |
|:---|:---|
| `format` | 格式化 SQL，关键字大写、缩进对齐 |
| `check` | 语法检查，返回 JSON 格式错误信息 |
| `analyze` | 分析 SQL 结构（类型、表名、复杂度） |
| `nl2sql` | 中文自然语言转 SQL（模板匹配） |
| `explain` | 解析 PostgreSQL EXPLAIN 输出 |

---

## 🚀 快速开始

### 安装

```bash
# 安装依赖
pip install sqlparse

# 或者直接下载脚本
curl -O https://raw.githubusercontent.com/shenghoo/sql-explain/main/sql_explain.py
chmod +x sql_explain.py
```

### CLI 使用

```bash
# 格式化 SQL
python sql_explain.py format "SELECT * FROM users WHERE id=1"
# 输出:
# SELECT
#   *
# FROM users
# WHERE id = 1

# 语法检查
python sql_explain.py check "SELECT * FORM users"
# {"valid": false, "errors": ["语法错误: ..."], "statement_count": 1}

# 分析结构
python sql_explain.py analyze "SELECT u.name FROM users u JOIN orders o ON u.id=o.user_id"
# {"type": "SELECT", "tables": ["users", "orders"], "complexity": "MODERATE", ...}

# 自然语言转 SQL
python sql_explain.py nl2sql "查询所有订单"
# SELECT * FROM your_table LIMIT 10;

# EXPLAIN 解析
python sql_explain.py explain "Seq Scan on users (cost=0.00..100.00 rows=1000 width=100)"
```

### Python API

```python
from sql_explain import format_sql, check_syntax, analyze_sql_structure, nl_to_sql, explain_sql

# 格式化
formatted = format_sql("select * from users where id=1")

# 语法检查
result = check_syntax("SELECT * FORM users")

# 结构分析
info = analyze_sql_structure("SELECT u.name FROM users u JOIN orders o ON u.id=o.user_id")

# 自然语言转 SQL
sql = nl_to_sql("查询所有订单")

# EXPLAIN 解析
report = explain_sql("Seq Scan on users (cost=0.00..100.00 rows=1000 width=100)")
```

---

## 📊 复杂度评估

| 复杂度 | 条件 |
|:---|:---|
| 🟢 SIMPLE | 无复杂因素 |
| 🟡 MODERATE | 1-2 个复杂因素（JOIN/GROUP BY/ORDER BY 等） |
| 🔴 COMPLEX | 3+ 个复杂因素 |

---

## 🗄️ 支持数据库

- ✅ **PostgreSQL** — EXPLAIN 格式完全支持
- ⚠️ **MySQL** — 部分支持
- ⚠️ **SQLite** — 部分支持

---

## 📁 项目结构

```
sql-explain/
├── sql_explain.py       # 核心功能（294行）
├── cli.py               # keyword 风格入口
├── test_sql_explain.py  # pytest 测试用例
├── README.md            # 本文件
└── SKILL.md             # AI Skill 设计文档
```

---

## 🧪 运行测试

```bash
pip install pytest
pytest test_sql_explain.py -v
```

---

## 🤝 License

MIT License

---

⭐ Star 支持一下！
