---
name: "smart-charts"
version: "3.1.6"
description: "Intelligent chart generation and data analysis skill. Reads user-supplied data files (CSV/Excel/JSON), analyzes data characteristics with LLM assistance, auto-recommends and generates interactive ECharts visualizations."
---

# Smart Charts

Upload a data file → get interactive charts, automatically.

---

## Quick Start / 快速上手

**3 步生成图表：**

1. **上传数据** — 将 CSV / Excel / JSON 文件拖入对话框
2. **确认分析方向** — 查看数据摘要，确认推荐的图表类型
3. **查看结果** — 交互式图表（HTML）

**示例：**

```
用户: 帮我分析这份销售数据 [上传 sales_2024.csv]

AI:  已加载 sales_2024.csv（120 行 × 8 列）
     关键字段: date, region, product, revenue, profit, quantity

     推荐分析方向:
     1. 各区域营收对比 → 柱状图
     2. 月度营收趋势   → 折线图
     3. 产品利润占比   → 饼图

     确认后开始生成？

用户: 确认

AI:  [生成交互式图表] [生成分析报告]
```

---

## Activation Triggers / 触发条件

Load this skill when **any** of the following is met:

- User mentions: "analyze data", "generate chart", "data visualization", "chart", "visualization"
  / 用户提到：「分析数据」「生成图表」「数据可视化」
- User provides a data file and asks for analysis or visualization
- User asks to generate charts or a report from tabular data

---

## Capability Boundaries / 能力边界

**Supported:** CSV (.csv/.tsv/.txt), Excel (.xlsx/.xls), JSON (.json); 16 chart types (see below); up to ~10 files with auto-merge; single file ≤ 100 MB (≤ 50 MB recommended); auto-detects UTF-8/GBK/GB2312.

**Not supported:** Databases (export to CSV first), real-time/streaming data, geo maps, >100 MB files, nested JSON >1 level, non-tabular data (images/audio/video). Auto-merge requires ≥50% column overlap. LLM-generated transform code runs in sandbox (no file I/O, imports, or network).

---

## Installation / 安装

```bash
pip install -r requirements.txt --require-hashes
# To update dependency versions, regenerate hashes first:
python {skill_base}/core/generate_hashes.py
```

Dependencies (pinned with `==` + SHA256 hashes): `pandas==3.0.1`, `numpy==2.4.3`, `openpyxl==3.1.5`, `xlrd==2.0.1`. ECharts loads via CDN — no local install needed.

---

## Security / 安全机制

LLM-generated transform code is executed with multiple safety layers: (1) keyword blacklist (blocks `exec`, `eval`, `open`, `import`, `os.system`, etc.), (2) AST whitelist (only allows assignments, calls, loops, comprehensions), (3) sandbox builtins (only safe functions like `len`, `range`, `sorted`; `open`/`exec`/`eval`/`__import__` removed), (4) user confirmation in interactive mode (skipped when `auto_confirm=True` in programmatic calls, but blacklist + AST checks still apply). Blocked code raises `CodeValidationError` explaining why and how to resolve.

---

## Execution Workflow

1. **Obtain data** — user uploads file(s) or provides path(s).
2. **Parse data** — call `data_parser.py` on all files; for multiple files, assess merge feasibility.
3. **Confirm & recommend** — display summary table; recommend merge/separate/join strategy and chart type(s) based on data semantics; wait for user confirmation.
4. **Transform (if needed)** — if raw data doesn't match target chart's input format, LLM generates pandas transform code → security check (blacklist + AST) → user confirmation (interactive mode) → execute in sandbox → standardized DataFrame. On failure: retry max 2 times, then fall back to original data + auto-detection.
5. **Generate charts** — call `chart_generator.py` → ECharts HTML. Merged data → cross-group comparison; separate data → independent charts per file.
6. **Present results** — interactive charts via `preview_url`.

**Key principles:** multi-file first; confirm before executing; LLM chooses chart types by data semantics (never hard-code mapping); never hard-code absolute paths (resolve at runtime); present results immediately; adapt data via transform code when needed; security by default.

---

## Configuration

```yaml
output_dir: ./smart_charts_output  # optional; never hard-code absolute paths
```

---

## Data Parsing — CLI Reference

> `{skill_base}` = root directory of this skill (contains `SKILL.md`).

```bash
# Single file
python {skill_base}/core/data_parser.py <file_path> [--summary]

# Multiple files
python {skill_base}/core/data_parser.py <file1> <file2> ... [--summary]

# Multiple files with auto-merge
python {skill_base}/core/data_parser.py <file1> <file2> ... [--merge] [--summary]
```

**Merge behavior:** identical columns → vertical concat (adds `source_file` column); ≥50% overlap → horizontal join on shared key; no common structure → error (advise analyzing separately).

**Formats:** CSV/.tsv/.txt (auto-detect delimiter + encoding), .xlsx/.xls (first non-empty sheet), .json (array format + 1-level nested objects).

---

## Chart Generation — CLI Reference

```bash
python {skill_base}/core/chart_generator.py \
  <file_path> <chart_type> \
  --title "Chart Title" \
  --x-axis "date" \
  --y-axis "revenue profit" \
  --transform-code "<pandas code>" \
  --output-dir "./output" \
  [--auto-confirm]
```

**Parameters:** `file_path` (required), `chart_type` (required, see table), `--title` (default: "Data Chart"), `--x-axis` (auto-detected if omitted), `--y-axis` (space-separated; defaults to first 5 numeric columns), `--transform-code` (LLM-generated pandas code, validated + executed before rendering), `--output-dir` (default: `./smart_charts_output`), `--auto-confirm` (skip user confirmation for transform code; blacklist + AST checks still apply).

### Chart Types & Input Format

LLM must check whether raw data matches the required format; if not, generate transform code.

| ID | Best For | Required DataFrame Format | Example Columns |
|----|----------|--------------------------|-----------------|
| `line` | Time-series trends | 1 category/time + 1~N numeric | `month, productA, productB` |
| `bar` | Category comparison | 1 category + 1~N numeric | `city, revenue, profit` |
| `area` | Cumulative change | 1 category/time + 1~N numeric | `date, uv, pv` |
| `pie` | Composition/share | 1 name + 1 value | `category, share` |
| `scatter` | Correlation | 2 numeric, or 1 category + 1 numeric | `height, weight` |
| `radar` | Multi-dimension comparison | 1 indicator + N numeric | `metric, productA, productB` |
| `heatmap` | Density/cross-tab | 2 category + 1 numeric | `row, col, value` |
| `treemap` | Hierarchical proportion | 1 name + 1 value | `category, sales` |
| `graph` | Entity relationships | source + target (+ value) | `from, to, weight` |
| `boxplot` | Distribution/outliers | N numeric | `math, chinese, english` |
| `waterfall` | Incremental change | 1 category + 1 numeric (increments) | `month, profit_delta` |
| `gauge` | KPI progress | 1 numeric (mean used) | `completion_rate` |
| `sankey` | Flow transfer | source + target + value | `origin, destination, amount` |
| `funnel` | Conversion rate | 1 name + 1 value | `stage, count` |
| `sunburst` | Multi-level composition | 1 name + 1 value | `category, value` |
| `wordcloud` | Frequency/keywords | 1 name + 1 value | `word, frequency` |

### Batch Generation (Programmatic)

`generate_multi_charts()` generates multiple charts from one DataFrame in a single call. No CLI entry — CLI supports single chart only; this is for programmatic use.

```python
from core.chart_generator import ChartGenerator

result = ChartGenerator(output_dir="./output").generate_multi_charts(
    df=df,
    chart_configs=[
        {"type": "bar",  "title": "Regional Revenue", "x_axis": "region", "y_axis": ["revenue"]},
        {"type": "line", "title": "Monthly Trend",   "x_axis": "month",  "y_axis": ["revenue", "profit"]},
    ],
    auto_confirm=True,   # skip per-chart confirmation
)
# result = {"charts": [{"type", "title", "html_path", "success", ...}]}
```

Each chart config may include `type`, `title`, `x_axis`, `y_axis`, `transform_code`, `width`, `height`. Charts are independent — failure of one does not block others (marked `success: False` with `error`).

---

## Transform Code Generation

When raw data doesn't match the target chart's input format, use this prompt template:

```
Known information:
- Raw data columns: {columns_with_dtypes}
- Data sample (first 5 rows): {sample}
- Target chart type: {chart_type}
- Required format for this chart: {chart_input_spec}

Generate a pandas code snippet that transforms df into a result DataFrame matching the chart's input format.

Rules:
1. Only use variables: df, pd, np
2. Must produce a variable named result (pd.DataFrame)
3. Do not modify df in-place; use df.copy() or chain operations
4. Keep code concise; prefer pandas built-in methods (pivot_table, melt, groupby, rename, etc.)
5. If raw data already matches the required format, output an empty string
6. Do NOT use: import, open, exec, eval, os, sys, subprocess, file I/O, network calls

Output format:
```python
# {one-line description of what the transform does}
{transform_code}
```
```

**Common transform patterns:**
- Long→multi-series: `result = df.pivot_table(index='<time>', columns='<category>', values='<value>', aggfunc='sum').reset_index()`
- Long→pie (filter): `result = df[df['metric']=='revenue'][['category','value']].rename(columns={'category':'name'})`
- Wide→long: `result = df.melt(id_vars=['date'], var_name='name', value_name='value')`
- Aggregate→bar: `result = df.groupby('<category>')['<value>'].sum().reset_index()`
- Rename columns: `result = df.rename(columns={'来源':'source','去向':'target','金额':'value'})`
- Compute delta→waterfall: `tmp = df.copy(); tmp['delta'] = tmp['profit'].diff().fillna(tmp['profit'].iloc[0]); result = tmp[['month','delta']]`
