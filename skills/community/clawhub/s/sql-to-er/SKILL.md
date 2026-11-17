---
name: er-diagram
description: Generate classic Chen-style ER diagrams from SQL DDL, pasted CREATE TABLE, or natural-language data model requests. Trigger on ER/ERD/entity-relationship/schema diagram/SQL转ER图, or when user asks to design tables and draw an ER diagram. Outputs only what the user asked for (Chen PNG by default; Mermaid/Word/GoJS only on request). SQL parse via yanleaf.com API with local fallback.
---

# ER Diagram (SQL → ER)

经典 Chen 风格 ER 图 +（按需）Word 三线表 / Mermaid / GoJS。

## 触发条件

在以下情况使用：

- 用户提供 `.sql` / 粘贴 `CREATE TABLE`，并要求出图或设计文档
- 用户明确要求：ER 图 / ERD / SQL转ER / 数据库设计文档
- 用户用自然语言描述业务并要求「设计表结构并画 ER 图」（由**当前模型**设计 list-of-tables，**不要**调用 yanleaf 的 AI 接口）

不要在仅讨论 SQL 语法、改某一个字段时自动出图。

## 产出什么（按需，不要默认全出）

**只生成用户要的东西。** 未点名的格式不要跑、不要塞给用户。

| 用户说法 | 生成 |
|----------|------|
| 画 ER 图 / 生成 ERD / 看看图 | **仅 PNG**（`--format png`） |
| 要 Mermaid / 要代码块图 | **仅 Mermaid**（`--format mermaid`） |
| 数据库设计文档 / 三线表 / Word / docx | **仅 Word**（`--format word`） |
| GoJS / 给前端用的 JSON | **仅 GoJS**（`--format gojs`） |
| 全部 / 图和文档都要 / 导出全套 | `--format all` |

默认（只说「画个 ER 图」）：**PNG only**。

不要默认执行 `--format all`。

## SQL 路径

```bash
# 只要图（最常见）
python scripts/sql_to_erd.py schema.sql --out /tmp/erd --format png

# 只要 Word
python scripts/sql_to_erd.py schema.sql --out /tmp/design --format word

# 用户明确要全套
python scripts/sql_to_erd.py schema.sql --out /tmp/erd --format all
```

解析：优先 `https://yanleaf.com/api/tools/er-diagram/parse`，失败本地 `sql_parser.py`。

引擎：`--engine auto`（有 `dot` 用 Graphviz，否则 matplotlib）。一般无需改。

## 自然语言路径

1. 按规范设计 list-of-tables（snake_case、主键、外键 `xxx_id`、审计字段、3NF）。
2. 写入 JSON 后只渲染用户要的格式，例如只要图：

```bash
python scripts/render_chen.py /tmp/tables.json /tmp/erd.png yanleaf.com
```

只要 Word 则用 `export_word.py`，不要顺手再出 PNG/Mermaid。

## 关系与精简

- 外键所在表 = **N**，被引用表 = **1**（不要画反）
- 字段很多或用户说「只要关系」：保留 PK + FK + 少量关键字段（`--max-attrs`）
- 用户说重画：按新要求再生成，仍只出其需要的格式

## 依赖（Python 3.9+）

```bash
pip install sqlparse pyyaml python-docx pillow matplotlib graphviz
```

Graphviz 系统包可选；没有也能出 PNG。中文需系统字体或 `assets/` 内字体。

## 脚本

| 文件 | 作用 |
|------|------|
| `sql_to_erd.py` | SQL 入口（用 `--format` 控制产物） |
| `render_chen.py` | matplotlib Chen PNG |
| `api_client.py` | yanleaf parse API |
| `sql_parser.py` | 本地解析回退 |
| `generate_erd.py` | Mermaid / GoJS / Graphviz DOT |
| `export_word.py` | Word 三线表 |
| `watermark.py` | Graphviz PNG 水印 |

在线工具：https://yanleaf.com/tools/sql-to-er
