---
name: wakatime
description: Query WakaTime coding statistics including time ranges, projects, languages, categories, editors, and machines. Use when the user asks about WakaTime, coding time, project breakdown, language breakdown, or specific daily/weekly/monthly summaries. Works with WakaTime cloud.
metadata: {"openclaw": {"requires": {"env": ["WAKATIME_API_KEY"]}, "primaryEnv": "WAKATIME_API_KEY"}}
---

# Wakatime

## Overview

Wakatime 是一个用于追踪编程时间的工具，可以记录你在不同项目、语言、编辑器中的编码时间。这个技能可以查询 WakaTime 的统计数据，包括时间范围、项目、语言、类别、编辑器和机器的明细。

## Quick Start

```bash
# 健康检查
python3 scripts/wakatime_query.py health

# 查询项目列表
python3 scripts/wakatime_query.py projects

# 查询今日状态
python3 scripts/wakatime_query.py status-bar

# 查询最近 7 天的统计
python3 scripts/wakatime_query.py stats last_7_days

# 查询昨天（Asia/Shanghai）
python3 scripts/wakatime_query.py summaries --range yesterday --timezone Asia/Shanghai

# 查询特定日期范围
python3 scripts/wakatime_query.py summaries --start 2026-03-18 --end 2026-03-18
```

## Config

### Required
- **WAKATIME_API_KEY**WakaTime API key

### Environment Example

```bash
export WAKATIME_API_KEY="your-api-key-here"
```

## Commands

### health
快速健康检查，验证 API 连接是否正常。

### projects
查询项目列表，返回前 20 个项目及其统计数据。

### status-bar
查询今日状态条，显示今日编码时间和活动状态。

### all-time-since
查询自账号创建以来的全部统计数据。

### stats <range>
查询特定时间范围的统计数据，支持以下命名范围：
- `last_7_days`、`last_30_days`、`last_6_months`、`last_year`、`all_time`

### summaries [options]
查询指定日期范围的汇总数据，支持以下选项：

#### 时间范围选择
- `--start YYYY-MM-DD`：开始日期（包含）
- `--end YYYY-MM-DD`：结束日期（包含）
- `--range <preset>`：预设范围
    - `yesterday`：昨天
    - `today`：今天
    - `last_7_days`：最近 7 天
    - `last_30_days`：最近 30 天
    - `all_time`：全部时间

#### 筛选条件
- `--project <name>`：按项目筛选
- `--branches <comma>`：按分支筛选（逗号分隔）
- `--timezone <tz>`：指定时区（如 `Asia/Shanghai`）
- `--timeout <seconds>`：API 查询超时时间

#### 示例

```bash
# 查询昨天（Asia/Shanghai）
python3 scripts/wakatime_query.py summaries --range yesterday --timezone Asia/Shanghai

# 查询最近 30 天
python3 scripts/wakatime_query.py stats last_30_days

# 查询特定项目在最近 7 天的数据
python3 scripts/wakatime_query.py summaries --range last_7_days --project myproject

# 查询特定日期
python3 scripts/wakatime_query.py summaries --start 2026-03-01 --end 2026-03-15
```

## Output

所有命令返回 JSON 格式数据，包含：
- `grand_total`：总统计（时间、小时、文本）
- `projects`：项目列表（按总时间排序）
- `languages`：语言列表（按总时间排序）
- `categories`：类别列表（Browsing、Coding、Writing Docs 等）
- `editors`：编辑器列表（VS Code、IntelliJ IDEA 等）
- `machines`：机器列表
- `dependencies`：依赖包列表

## Notes

- 所有请求使用 HTTP Basic Auth，`Authorization: Basic <base64(api_key)>`
- 只读操作，不会修改任何数据
- 时区参数影响 `--range` 预设的日期边界
- 对于预设范围（如 `yesterday`、`today`），建议配合 `--timezone` 使用以确保日期计算正确

## Troubleshooting

### 常见问题
1. **认证失败**：检查 `WAKATIME_API_KEY` 是否正确
2. **连接超时**：尝试增加 `--timeout` 参数

### 调试
在命令中添加 `-d` 或 `--debug` 打印 HTTP 请求详情。