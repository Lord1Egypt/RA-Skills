---
name: qc-data-processor
slug: qc-data-processor
displayName: QC Data Processor / QC 数据处理器
description: Quality control data analysis MCP Server. Parse QC data, SPC control charts (Xbar-R, I-MR), process capability (Cp/Cpk/Pp/Ppk), reliability/Weibull analysis (B10/B50/MTTF), and QC report generation (daily/weekly/8D/reliability). 品质数据分析 MCP 服务器。数据解析、SPC 控制图、过程能力指数、可靠性/Weibull 分析、品质报告生成。
version: 1.0.0
author: David
license: MIT
metadata:
  hermes:
    tags: [qc, spc, reliability, weibull, manufacturing, quality]
    related_skills: []
---

# qc-data-processor / QC 数据处理器

## Overview / 概述

QC Data Processor is an MCP Server that provides quality control data analysis tools. It can parse QC data, perform SPC analysis (control charts, process capability), reliability analysis (Weibull/Lognormal fitting), and generate QC reports in Markdown format.

QC 数据处理器是一个 MCP Server，提供品质数据分析工具。支持 QC 数据解析、SPC 分析（控制图、过程能力）、可靠性分析（Weibull/Lognormal 拟合）、Markdown 格式品质报告生成。

## When to Use / 适用场景

- User asks to analyze quality control data (SPC charts, process capability) / 用户要求分析品质数据（SPC 控制图、过程能力）
- User asks to perform reliability/Weibull analysis on life test data / 用户要求对寿命试验数据做可靠性/Weibull 分析
- User asks to generate QC reports (daily, weekly, 8D, reliability) / 用户要求生成品质报告（日报、周报、8D、可靠性）
- User mentions SPC, Cp/Cpk, control charts, Weibull, MTTF, B10 life / 用户提到 SPC、Cp/Cpk、控制图、Weibull、MTTF、B10 寿命
- User provides Excel/CSV files with measurement, time-to-failure, or pass/fail data / 用户提供包含测量值、失效时间或合格/不合格数据的 Excel/CSV 文件

## Trigger Keywords / 触发关键词

SPC, 控制图, 过程能力, Cp, Cpk, 良率, Weibull, 可靠性, 寿命, MTTF, B10, 8D, 品质报告, 日报, 周报, 客诉, QC

## Tools / 工具

### 1. qc_parse_data_tool / 数据解析

Parse QC data file (CSV/Excel) and auto-detect column types, pipeline, and control chart suggestions.

解析 QC 数据文件（CSV/Excel），自动识别列类型、分析管线和控制图建议。

**Input / 输入：**
- `file_path` (str): Path to data file (.csv, .xlsx, .xls) / 数据文件路径
- `mode` (str, optional): "auto" by default / 默认 "auto"

**Output / 输出：** JSON schema with column types, pipeline detection, and chart suggestions / 包含列类型、管线检测和控制图建议的 JSON schema

### 2. qc_spc_analyze_tool / SPC 分析

Perform SPC analysis: control charts (Xbar-R, I-MR), capability indices (Cp, Cpk, Pp, Ppk), Western Electric rules.

执行 SPC 分析：控制图（Xbar-R、I-MR）、过程能力指数（Cp、Cpk、Pp、Ppk）、Western Electric 判异规则。

**Input / 输入：**
- `data_schema` (dict): Output from qc_parse_data_tool (must include `_file_path`) / 来自 qc_parse_data_tool 的输出（必须包含 `_file_path`）
- `column` (str): Measurement column name / 测量值列名
- `subgroup_size` (int, optional): Subgroup size / 子组大小
- `chart_type` (str, optional): "Xbar-R", "I-MR", or "auto" / "Xbar-R"、"I-MR" 或 "auto"

**Output / 输出：** Statistics (control limits, capability indices), alarms, chart data / 统计量（控制限、能力指数）、异常报警、图表数据

### 3. qc_reliability_analyze_tool / 可靠性分析

Fit reliability distributions (Weibull, Lognormal, Exponential) using MLE, select best via AICc.

使用极大似然估计（MLE）拟合可靠性分布（Weibull、Lognormal、Exponential），通过 AICc 选择最优分布。

**Input / 输入：**
- `data_schema` (dict): Output from qc_parse_data_tool (must include `_file_path`) / 来自 qc_parse_data_tool 的输出（必须包含 `_file_path`）
- `time_column` (str): Column containing time-to-failure data / 失效时间列名
- `censor_column` (str): Column containing censor indicators (1=failure, 0=censored) / 删失标记列名（1=失效，0=删失）
- `distribution` (str, optional): "auto" (try all), "Weibull", "Lognormal", or "Exponential" / "auto"（尝试全部）、"Weibull"、"Lognormal" 或 "Exponential"

**Output / 输出：** Best-fit distribution, parameters with CI, B10/B50/MTTF, probability plot data / 最优分布、参数及置信区间、B10/B50/MTTF、概率图数据

### 4. qc_report_generate_tool / 报告生成

Generate QC reports in Markdown format.

生成 Markdown 格式的品质报告。

**Input / 输入：**
- `analysis_result` (dict): Output from SPC or reliability analysis / SPC 或可靠性分析的输出结果
- `template` (str): One of "daily", "weekly", "8d", "reliability" / 模板类型："daily"（日报）、"weekly"（周报）、"8d"（8D 报告）、"reliability"（可靠性报告）
- `metadata` (dict): Product name, date, customer, etc. / 产品名称、日期、客户等元数据

**Output / 输出：** Markdown string / Markdown 字符串

## MCP Configuration / MCP 配置

```json
{
  "mcpServers": {
    "qc-data-processor": {
      "command": "python",
      "args": ["path/to/mcp_server.py"],
      "env": {}
    }
  }
}
```

## Dependencies / 依赖

```
mcp>=1.0.0
pandas>=2.0.0
openpyxl>=3.0.0
numpy>=1.24.0
scipy>=1.10.0
reliability>=0.8.0
```

## Example Usage / 使用示例

### Parse and SPC analysis / 数据解析与 SPC 分析
```
User: Analyze the SPC data in data/spc_sample.csv / 分析 data/spc_sample.csv 的 SPC 数据

1. qc_parse_data_tool("data/spc_sample.csv") -> schema
2. qc_spc_analyze_tool(schema, "measurement") -> spc_result
3. qc_report_generate_tool(spc_result, "daily", {"product": "Widget"})
```

### Reliability analysis / 可靠性分析
```
User: Run Weibull analysis on data/reliability_sample.csv with time column "time" and censor column "censor"
User: 对 data/reliability_sample.csv 做 Weibull 分析，时间列 "time"，删失列 "censor"

1. qc_parse_data_tool("data/reliability_sample.csv") -> schema
2. qc_reliability_analyze_tool(schema, "time", "censor") -> rel_result
3. qc_report_generate_tool(rel_result, "reliability", {"product": "Widget"})
```

## Notes / 备注

- All outputs are text/JSON, no images or GUI / 所有输出均为文本/JSON，无图片或 GUI
- Uses stdio transport, no API keys required / 使用 stdio 传输，无需 API Key
- Process capability formulas match Minitab/JMP standard methods / 过程能力公式对标 Minitab/JMP 标准算法
- Control chart constants (A2, D3, D4, d2) for n=2~25 / 控制图常数（A2, D3, D4, d2）覆盖 n=2~25
