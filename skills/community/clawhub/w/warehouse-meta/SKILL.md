---
name: data-governance
description: |
  LLM 驱动的数仓元数据自动治理。解决企业数仓最普遍的痛点：字段无注释、表无描述、命名混乱、NL2SQL 准确率低。
  自动探测连接模式：pyhive 可用时读写 Hive；否则通过 MCP 工具只读，结果持久化到 SQLite。
  
  触发时机（以下任一即触发）：
  - 用户提到：数据治理、元数据、字段注释、表备注、字段没有描述、数仓治理、data governance
  - 用户提到：NL2SQL 准确率低、字段语义不清、新人看不懂表结构
  - 用户运行 /data-governance 命令
  - 用户想批量生成或补全数仓字段说明
---

# Data Governance Skill

## 连接模式说明

运行任何命令前，脚本自动探测可用模式，**无需手动配置**：

```
pyhive 已安装 且 hive.host 已配置 且连接成功
    → pyhive 模式：脚本直接读取 Hive，推断后写回 COMMENT

否则
    → MCP 模式：Claude 调用 MCP 工具采集 schema，脚本只做推断+SQLite持久化
```

两种模式的 LLM 推断流水线完全一致，区别仅在数据从哪里来、结果写到哪里：

| 能力 | pyhive 模式 | MCP 模式 |
|------|------------|---------|
| 读取表结构 | pyhive → DESC | MCP `get_columns` |
| 读取数据样本 | pyhive → SELECT LIMIT 20 | MCP `submit_query` |
| 读取 DML 逻辑 | pyhive → SHOW CREATE VIEW | MCP `get_table_info` |
| LLM 推断 | ✅ 三级流水线 | ✅ 三级流水线 |
| 持久化 SQLite | ✅ | ✅ |
| 写回 Hive COMMENT | ✅ | ❌（只读） |

---

## 快速判断入口

| 用户意图 | 执行动作 |
|---------|---------|
| init / 初始化 / 首次使用 | → [INIT](#init) |
| detect / 检测连接 | → [DETECT](#detect) |
| scan / 扫描 / 生成注释 | → [SCAN](#scan) |
| review / 审核 / 人工确认 | → [REVIEW](#review) |
| status / 覆盖率 / 进度 | → [STATUS](#status) |

---

## INIT：初始化 {#init}

```bash
python ~/.claude/skills/data-governance/scripts/governance.py init
```

交互式填写配置，**Hive 主机可留空**（留空则自动进入 MCP 模式）。

init 完成后自动探测并打印当前连接模式。

---

## DETECT：探测连接模式 {#detect}

首次使用或连接配置变更后，用此命令确认当前模式：

```bash
python ~/.claude/skills/data-governance/scripts/governance.py detect \
  --config .governance_config.yaml
```

输出示例（pyhive 模式）：
```
🔌 连接模式：pyhive（hive-server.internal）→ 支持读写，可写回 Hive COMMENT
```

输出示例（MCP 模式）：
```
🔌 连接模式：MCP 只读（pyhive 未安装）→ 结果仅持久化到 SQLite
```

---

## SCAN：扫描并生成注释 {#scan}

### pyhive 模式（全自动）

脚本自行完成采集 + 推断 + 写回：

```bash
python ~/.claude/skills/data-governance/scripts/governance.py scan \
  --config .governance_config.yaml \
  --db loan_dw \
  --mode incremental
```

### MCP 模式（两步执行）

**Step 1：由 Claude 调用 MCP 工具采集 schema，写入临时 JSON**

你（Claude）需要执行以下操作，将结果写入 `/tmp/governance_schema.json`：

```python
# 伪代码，实际调用对应 MCP 工具
schema_data = []
for table in mcp__sql__list_tables(database=db):
    columns   = mcp__sql__get_columns(table=table)
    table_info = mcp__sql__get_table_info(table=table)

    # 取数据样本（每个字段最多 20 条非空值）
    samples = {}
    for col in columns:
        result = mcp__sql__submit_query(
            sql=f"SELECT `{col.name}` FROM {table} WHERE `{col.name}` IS NOT NULL LIMIT 20"
        )
        samples[col.name] = mcp__sql__get_query_result(result.query_id)

    schema_data.append({
        "db":        database,
        "table":     table_name,
        "full_name": f"{database}.{table_name}",
        "fields": [
            {"col_name": c.name, "data_type": c.type, "comment": c.comment or ""}
            for c in columns
        ],
        "samples": samples,
        "dml": table_info.get("view_definition", "")
    })

# 写入临时文件
with open("/tmp/governance_schema.json", "w") as f:
    json.dump(schema_data, f, ensure_ascii=False)
```

**Step 2：调用脚本完成 LLM 推断 + SQLite 持久化**

```bash
python ~/.claude/skills/data-governance/scripts/governance.py scan \
  --config .governance_config.yaml \
  --input-schema /tmp/governance_schema.json \
  --mode incremental
```

### 通用参数

| 参数 | 默认 | 说明 |
|------|------|------|
| `--db` | `all` | 指定数据库（pyhive 模式生效） |
| `--table` | `all` | 指定单张表 |
| `--mode` | `incremental` | `incremental` 只处理变更表；`full` 强制全量 |
| `--input-schema` | 无 | MCP 模式下传入的 schema JSON 路径 |
| `--evolve` | false | 强制触发 DSPy 重新编译 |

### 扫描输出

```
📊 扫描完成 → 已写回 Hive COMMENT  （pyhive 模式）
           → 仅持久化到 SQLite      （MCP 模式）
──────────────────────────────────────
  变更表数：34 张
  处理字段：2,847 个
  自动写回：2,341 个 (82%)
  Level2：   398 个 (14%)
  人工队列：  108 个 (4%)
──────────────────────────────────────
```

---

## REVIEW：人工审核 {#review}

```bash
python ~/.claude/skills/data-governance/scripts/governance.py review \
  --config .governance_config.yaml
```

逐条展示低置信度字段（Active Learning 排序）。

- **pyhive 模式**：确认后同时写入 SQLite 和 Hive COMMENT
- **MCP 模式**：确认后只写入 SQLite，并在输出中提示

交互操作：

| 输入 | 动作 |
|------|------|
| 回车 | 接受推断结果 |
| 输入文字 | 替换为输入内容 |
| `s` | 跳过，保留在队列 |
| `q` | 退出，已确认的立即生效 |

---

## STATUS：覆盖率看板 {#status}

```bash
python ~/.claude/skills/data-governance/scripts/governance.py status \
  --config .governance_config.yaml
```

输出中包含 `连接模式` 列，可以看到每个库的数据来自哪种模式采集。

---

## MCP schema JSON 格式

Claude 在 MCP 模式下采集 schema 时，写入的 JSON 格式：

```json
[
  {
    "db": "loan_dw",
    "table": "loan_detail",
    "full_name": "loan_dw.loan_detail",
    "fields": [
      {"col_name": "loan_id",    "data_type": "BIGINT",       "comment": ""},
      {"col_name": "amt_r_d30",  "data_type": "DECIMAL(18,2)", "comment": ""}
    ],
    "samples": {
      "loan_id":   [10001, 10002, 10003],
      "amt_r_d30": [120.5, 0.0, 350.2]
    },
    "dml": "CREATE VIEW loan_detail AS SELECT ..."
  }
]
```

`samples` 和 `dml` 均可为空（`{}` 和 `""`），脚本会跳过对应的增强逻辑。

---

## 注意事项

- **增量模式**：基于 schema 指纹（字段名+类型 MD5），字段内容或 COMMENT 变化不触发重推
- **DSPy 冷启动**：首次 scan（pyhive 模式）自动触发；MCP 模式下样本来自 SQLite 已有备注
- **MCP 模式写回**：若后续安装了 pyhive 并配置了 hive.host，re-run `scan --mode full` 可补写所有已推断字段的 Hive COMMENT
- **数据样本**：MCP 模式下样本通过 `submit_query` 获取，受 MCP 工具的行数限制（通常 10000 行），取前 20 条非空值已足够
- **并发**：SQLite 不支持多进程写入，不要同时运行两个 scan 实例

详细架构见 `references/architecture.md`。
