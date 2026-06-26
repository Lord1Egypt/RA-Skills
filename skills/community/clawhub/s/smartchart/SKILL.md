---
name: smartchart
description: This skill should be used when the user needs to query data, explore available data tools, or execute data operations using the smartchart CLI. Trigger when the user asks to query data, run a smartchart tool, list available tools, fetch metrics, or perform any data retrieval task via the smartchart platform. Requires the Python `smartchart` library to be installed.
---

# SmartChart 数据查询技能

SmartChart 是一个面向开发的数据应用开发平台，提供 CLI 工具用于执行数据查询和工具调用。

## 环境要求

- Python 已安装 `smartchart` 库（`pip install smartchart`）
- CLI 命令：`smartchart`

## 核心 CLI 用法

### 列出所有可用工具（数据集）

```bash
smartchart run_tool -n list_tool
```

输出所有在线数据集的名称（name）和备注（remark）。**在执行任何具体工具前，先运行此命令**了解可用工具。

### 查看具体工具的使用方法

```bash
smartchart run_tool -n help_tool -t <工具名>
```

查看指定工具的详细信息，包括：输入参数说明、SQL 模板、输出字段等。**仅在 remark 中未说明参数用法时使用此命令**。

### 执行具体工具

```bash
smartchart run_tool -n <工具名/数据集名> [--format {raw,json,array}] [<变量>=<值> ...]
```

- `-n`：指定数据集名称或 ID（必填）
- `--format`：输出格式，可选 `raw`（默认）、`json`、`array`
- 其他参数：按数据集定义传入变量值（具体参数名由 remark 说明或 `help_tool` 获取）

**示例：**

```bash
# 列出所有可用工具
smartchart run_tool -n list_tool

# 查询名为「固定数据集」的数据，以 JSON 格式输出
smartchart run_tool -n 固定数据集 --format json

# 查看「查询」工具的详细用法和参数（仅在 remark 未说明时使用）
smartchart run_tool -n help_tool -t 查询

# 查询名为「查询」的工具并传入变量
smartchart run_tool -n 查询 --format json
```

## 标准工作流程

1. **发现工具**：执行 `smartchart run_tool -n list_tool` 获取所有可用数据集列表
2. **判断用法**：若 remark 已说明参数调用方法，直接使用；否则执行 `smartchart run_tool -n help_tool -t <工具名>` 了解参数
3. **执行查询**：用 `smartchart run_tool -n <工具名> --format json <变量>=<值>` 执行查询
4. **处理结果**：解析 JSON 输出，展示给用户

## 输出格式说明

| 格式 | 说明 |
|------|------|
| `raw`（默认） | 原始数组形式，第一行为字段名 |
| `json` | 对象数组，每行是一条记录，包含行数统计 |
| `array` | 纯数组形式 |

## 脚本辅助

使用 `scripts/smartchart_query.py` 可以以编程方式调用 smartchart 工具并格式化输出，适合需要进一步处理数据的场景。

## 注意事项

- 若 `smartchart` 命令不存在，提示用户执行：`pip install smartchart`
- 子命令是 `run_tool`，不是直接使用 `-n` 参数（`smartchart -n xxx` 无效）
- 查询结果默认包含 INFO 日志行，使用 `--format json` 可获得结构化数据
