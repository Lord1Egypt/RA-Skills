# Data Analyst - Automated Data Analysis & Report Generator

Upload any data file (CSV, Excel, JSON, SQL export) and get a complete analysis report with insights, anomalies, and actionable recommendations — no code required.

---

## 📖 如何使用 / How to Use

### 安装 / Install
```bash
openclaw skills install smart-data-analyst
```

### 支持格式 / Supported Formats
`.csv` · `.xlsx` · `.xls` · `.json` · `.tsv` · 直接粘贴表格内容

### 使用步骤 / Steps
1. 打开 OpenClaw，上传你的数据文件（拖拽或附件按钮）
2. 说一句话触发：

```
帮我分析这个数据
```
```
analyze this CSV and find key insights
```

### 示例场景 / Example Use Cases

| 场景 | 触发语句 |
|------|---------|
| 电商销售分析 | "分析这个月销售数据，找出下滑原因" |
| 财务报表 | "帮我分析这个 Excel，重点看支出异常" |
| 用户行为数据 | "找出用户流失的规律" |
| 库存数据 | "哪些 SKU 是滞销品？" |

### 报告包含 / Report Includes
✅ 数据概览（行列数、数据类型、缺失值统计）
✅ 描述性统计（均值、中位数、异常值）
✅ 相关性分析
✅ 时序趋势（有日期列时自动检测）
✅ 异常检测 + 数据质量评分
✅ 中文数据 → 全程中文输出
✅ 可执行的改进建议

### 追问示例 / Follow-up Prompts
```
把第3个发现展开分析一下
帮我生成一份可以发给老板的摘要，不超过200字
对比今年和去年同期的差异
```

### 常见问题 / FAQ
- **数据安全吗？** 数据只在本地 OpenClaw 和你配置的 AI 之间流转，不存储到第三方
- **文件多大？** 建议不超过 10MB，超大数据集自动采样
- **需要额外配置吗？** OpenClaw 配置好 AI 即可使用，支持阿里云百炼、DeepSeek 等，录入 Key 就行
- **有问题找谁？** ClawHub 页面留言或联系 @ShuaigeSkillBot
- **需要帮你配置好直接用？** Telegram 私信 @ShuaigeSkillBot，配置服务 ¥99，配好即用

---

## Trigger

When the user says any of: "analyze this data", "data analysis", "analyze CSV", "analyze Excel", "what does this data show", "find insights", "data report", "分析数据", "分析这个表", "数据报告", "看看这个数据", "帮我分析"

Or when the user uploads/provides a .csv, .xlsx, .json, .tsv file and asks about its contents.

## Workflow

### Step 1: Data Ingestion
Read the uploaded file. Determine:
- File format and encoding
- Number of rows and columns
- Column names and data types
- Missing values per column
- Sample of first 5 and last 5 rows

Output a **Data Overview** table immediately so the user knows you understood the file.

### Step 2: Automated Analysis

Perform ALL applicable analyses based on the data type:

#### For Numeric Data:
- Descriptive statistics (mean, median, mode, std dev, min, max, quartiles)
- Distribution shape (normal, skewed, bimodal)
- Outlier detection (values beyond 2 standard deviations)
- Correlation matrix between numeric columns
- Trend analysis if time-series data is detected

#### For Categorical Data:
- Value counts and frequency distribution
- Top N most common values
- Cardinality (number of unique values)
- Cross-tabulation with other categorical columns

#### For Time-Series Data:
- Trend direction (increasing / decreasing / stable)
- Seasonality patterns
- Period-over-period changes (day/week/month/year)
- Notable spikes or drops with dates

#### For Mixed Data:
- Group-by analysis (numeric stats per category)
- Segment comparison
- Pivot table summaries

### Step 3: Anomaly Detection
Flag anything unusual:
- Sudden value changes (> 2x standard deviation)
- Missing data patterns (random vs systematic)
- Duplicate rows
- Data quality issues (mixed types, encoding errors, impossible values)

### Step 4: Generate Report

Output a structured report in markdown:

```
## Data Analysis Report

### 1. Overview
- File: [name]
- Records: [count]
- Time Range: [if applicable]
- Data Quality Score: [percentage of clean/complete data]

### 2. Key Findings
- Finding 1: [most important insight]
- Finding 2: [second most important]
- Finding 3: [third]

### 3. Detailed Analysis
[Full analysis results organized by section]

### 4. Anomalies & Warnings
[Flagged issues with severity: HIGH / MEDIUM / LOW]

### 5. Recommendations
- Actionable recommendation 1
- Actionable recommendation 2
- Suggested next steps for deeper analysis

### 6. Data Quality Notes
[Missing values, duplicates, type issues]
```

### Step 5: Interactive Follow-up
After delivering the report, offer:
- "Want me to drill deeper into any specific finding?"
- "Should I compare specific columns or segments?"
- "Want me to generate a summary for your team/boss?"

## Rules
1. Always show the Data Overview first before diving into analysis — the user needs to confirm you read the file correctly.
2. Use plain language for insights. Say "Sales dropped 23% in March" not "The dependent variable exhibited a negative coefficient of -0.23 in period 3."
3. If the dataset has > 100 columns, ask the user which columns to focus on.
4. For Chinese data (Chinese column names, Chinese values), output the entire report in Chinese.
5. Never fabricate data points. If a calculation can't be performed, explain why.
6. For large datasets (> 100K rows), note that analysis is based on statistical sampling and state the sample size.
7. Always end with actionable recommendations, not just observations.

---
📢 每日市场数据播报，关注 Telegram 频道：https://t.me/shuaigeclaw
