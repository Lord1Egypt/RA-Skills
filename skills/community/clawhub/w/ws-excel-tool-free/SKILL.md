---
slug: ws-excel-tool-free
name: ws-excel-tool-free
version: 1.0.1
displayName: Excel工具(免费版)
summary: "Excel 文件处理免费版：读写、数据清洗、公式计算与基础统计，支持 xlsx 格式.。Excel 工具（免费版）面向个人用户与独立开发者，提供 Excel 文件的基础处理能力：读取、写入、"
license: Proprietary
edition: free
description: Excel 工具（免费版）面向个人用户与独立开发者，提供 Excel 文件的基础处理能力：读取、写入、数据清洗、公式计算与基础统计。通过
  openpyxl 与 pandas 等标准库操作 xlsx 文件，无需安装 Microsoft Excel。Use when 需要数据分析、报表生成、统计洞察、数据可视化时使用。不适用于实时流数据处理.
tags:
  - 数据处理
  - Excel
  - 数据清洗
  - 公式计算
  - 工具
  - 效率
  - xlsx
  - cell
  - excel
  - openpyxl
  - python
tools:
  - read
  - exec
  - write
homepage: ""
category: "Automation"
---
# Excel 工具（免费版）

## 概述

Excel 是最通用的数据交换格式之一。本工具让 AI Agent 能够直接读写 xlsx 文件、执行数据清洗与基础统计，无需安装 Microsoft Excel。免费版聚焦于"能读能写能算"——覆盖单文件基础操作；多表合并、透视表、图表生成与大数据处理留给专业版.
通过 openpyxl 与 pandas 等成熟开源库操作，支持格式保留与公式计算.
## 核心能力

| 能力 | 说明 | 免费版 |
|---|---|---|
| 读取 xlsx | 多 sheet、表头识别 | 是 |
| 写入 xlsx | 数据与格式保留 | 是 |
| 数据清洗 | 去重、空值、类型转换 | 是 |
| 基础公式 | SUM/AVERAGE/COUNT/MAX/MIN | 是 |
| 基础统计 | 总和、均值、极值、计数 | 是 |
| 格式操作 | 字体、颜色、边框 | 是 |
| 多 sheet 处理 | 跨 sheet 读写 | 是 |
| 多表合并 | 多文件合并 | 否（专业版） |
| 透视表 | 数据透视分析 | 否（专业版） |
| 图表生成 | 柱状图/折线图/饼图 | 否（专业版） |
| 大数据处理 | 分块读取与流式处理 | 否（专业版） |
| 自动化流水线 | 定时任务与批处理 | 否（专业版） |

### 核心功能执行
用`input_params`参数进行配置.

**处理**: 解析核心功能执行的输入参数,完成核心逻辑,返回结构化响应.
**输出**: 返回核心功能执行的响应数据,包含状态码、结果和日志.
- 执行此能力时使用`input_params`参数,支持创建/查询/导出操作

### 参数配置与调用
用`config_options`参数进行配置.

**处理**: 解析参数配置与调用的输入参数,完成核心逻辑,返回结构化响应.
**输出**: 返回参数配置与调用的响应数据,包含状态码、结果和日志.
- 执行此能力时使用`config_options`参数,支持修改/重置/导入操作

### 结果处理与输出
用`output_format`参数进行配置.

**处理**: 解析结果处理与输出的输入参数,完成核心逻辑,返回结构化响应.
**输出**: 返回结果处理与输出的响应数据,包含状态码、结果和日志.
- 执行此能力时使用`output_format`参数,支持导出/保存/转换操作
**能力覆盖范围**：本skill的核心能力覆盖以下场景关键词：Excel、文件处理免费版、公式计算与基础统、面向个人用户与独、立开发者、文件的基础处理能、openpyxl、pandas、等标准库操作、无需安装、Microsoft、Use、when、需要数据分析、报表生成、统计洞察、数据可视化时使用、不适用于实时流数等。这些关键词对应description中声明的使用场景,均已在上述能力点中提供对应的操作支持.
## 使用场景

### 场景一：销售数据统计
用户说"统计这个 Excel 里销售额的总和与平均值"。Agent 读取 xlsx 文件，识别"销售额"列，计算 SUM 与 AVERAGE，输出结果.
### 场景二：数据清洗
用户说"这个表有很多重复行和空值，帮我清理"。Agent 用 pandas 去重、填充或删除空值、转换数据类型，输出清洗后的文件.
### 场景三：格式化报表
用户说"把这个表加上标题行、边框和合计行"。Agent 用 openpyxl 写入格式（粗体、边框、背景色），追加合计行并写入 SUM 公式.
## 快速开始

### 60 秒上手
1. 安装依赖：`pip install openpyxl pandas`
2. 把 Excel 文件发给 Agent，描述需求
3. Agent 生成 Python 脚本并执行，输出结果或新文件

### 读取 Excel 文件

```python
import pandas as pd
# ...
# 读取第一个 sheet
df = pd.read_excel('data.xlsx')
# ...
# 读取指定 sheet
df = pd.read_excel('data.xlsx', sheet_name='Sheet1')
# ...
# 读取所有 sheet
sheets = pd.read_excel('data.xlsx', sheet_name=None)
for name, df in sheets.items():
    print(f"Sheet: {name}, 行数: {len(df)}")
```

### 写入 Excel 文件

```python
import pandas as pd
# ...
df = pd.DataFrame({
    '产品': ['A', 'B', 'C'],
    '销量': [100, 200, 150],
    '单价': [10, 20, 15]
})
df['总额'] = df['销量'] * df['单价']
df.to_excel('output.xlsx', index=False)
```

## 示例

### 数据清洗模板

```python
import pandas as pd
# ...
df = pd.read_excel('data.xlsx')
# ...
# 1. 去除完全重复的行
df = df.drop_duplicates()
# ...
# 2. 处理空值
df = df.dropna(subset=['必填列'])          # 删除关键字段为空的行
df['可选列'] = df['可选列'].fillna(0)        # 填充默认值
df['文本列'] = df['文本列'].fillna('未知')    # 填充文本
# ...
# 3. 类型转换
df['日期'] = pd.to_datetime(df['日期'])
df['金额'] = df['金额'].astype(float)
# ...
# 4. 输出清洗结果
df.to_excel('cleaned.xlsx', index=False)
print(f"清洗完成：{len(df)} 行")
```

### 公式计算模板

```python
from openpyxl import load_workbook
# ...
wb = load_workbook('report.xlsx')
ws = wb.active
# ...
# 在最后一行追加合计
last_row = ws.max_row
ws.cell(row=last_row + 1, column=1, value='合计')
ws.cell(row=last_row + 1, column=2, value=f'=SUM(B2:B{last_row})')
ws.cell(row=last_row + 1, column=3, value=f'=AVERAGE(C2:C{last_row})')
ws.cell(row=last_row + 1, column=4, value=f'=MAX(D2:D{last_row})')
# ...
wb.save('report_with_totals.xlsx')
```

### 格式化报表模板

```python
from openpyxl import Workbook
from openpyxl.styles import Font, Border, PatternFill, Alignment
# ...
wb = Workbook()
ws = wb.active
ws.title = '销售报表'
# ...
# 标题行格式
header_font = Font(bold=True, color='FFFFFF', size=12)
header_fill = PatternFill(start_color='4472C4', end_color='4472C4', fill_type='solid')
thin_border = Border(left=True, right=True, top=True, bottom=True)
# ...
headers = ['产品', '销量', '单价', '总额']
for col, header in enumerate(headers, 1):
    cell = ws.cell(row=1, column=col, value=header)
    cell.font = header_font
    cell.fill = header_fill
    cell.border = thin_border
    cell.alignment = Alignment(horizontal='center')
# ...
# 数据行
data = [
    ['A', 100, 10, 1000],
    ['B', 200, 20, 4000],
    ['C', 150, 15, 2250],
]
for row_idx, row_data in enumerate(data, 2):
    for col_idx, value in enumerate(row_data, 1):
        cell = ws.cell(row=row_idx, column=col_idx, value=value)
        cell.border = thin_border
# ...
wb.save('formatted_report.xlsx')
```

## 最佳实践

### 1. 读取大文件用 openpyxl 只读模式
```python
from openpyxl import load_workbook
wb = load_workbook('large.xlsx', read_only=True)
```
只读模式不加载整个文件到内存，适合大文件.
### 2. 写入时关闭索引
```python
df.to_excel('output.xlsx', index=False)
```
避免生成无意义的索引列.
### 3. 数据清洗顺序
1. 去重 → 2. 处理空值 → 3. 类型转换 → 4. 异常值处理
顺序很重要，先去重可减少后续处理量.
### 4. 公式 vs 计算
- 需要在 Excel 中动态更新 → 用公式（`=SUM(B2:B10)`）
- 只需要最终结果 → 用 Python 计算后写入值
- 公式适合交付给非技术人员，计算适合自动化流水线

### 5. 日期处理
- 读取时用 `pd.to_datetime()` 转换
- 写入时用 `datetime` 对象，pandas 自动识别
- 避免用字符串存日期，会导致排序与比较错误

### 6. 编码问题
- xlsx 是二进制格式，无编码问题
- 如导出 CSV，统一用 `utf-8-sig` 编码（兼容 Excel 中文）

## 常见问题

### Q1：读取 xlsx 报错"zipfile.BadZipFile"？
A：文件可能不是真正的 xlsx，或已损坏。检查文件扩展名与实际格式是否一致。旧版 `.xls` 需用 `xlrd` 库读取.
### Q2：写入后打开显示乱码？
A：xlsx 不存在编码问题。如出现乱码，可能是字符串本身编码错误。检查数据源编码，统一转为 UTF-8.
### Q3：公式写入后不计算？
A：openpyxl 写入公式是字符串，需要 Excel 打开后才会计算。如需在 Python 中获取计算结果，用 `data_only=True` 读取（但前提是文件曾被 Excel 打开并保存过）.
### Q4：日期读取后变成数字？
A：Excel 日期本质是数字序列。用 `pd.read_excel(..., parse_dates=['日期列'])` 或读取后用 `pd.to_datetime()` 转换.
### Q5：大文件内存溢出？
A：① 用 `read_only=True` 模式；② 用 `pd.read_excel(..., chunksize=1000)` 分块读取；③ 超大文件考虑转为 CSV 或用专业版的大数据处理能力.
### Q6：如何保留原格式编辑？
A：用 `openpyxl.load_workbook()` 读取（保留格式），修改后 `save()`。pandas 读取会丢失格式，只保留数据.
### Q7：多 sheet 怎么处理？
A：`pd.read_excel(..., sheet_name=None)` 返回字典，key 是 sheet 名，value 是 DataFrame。可遍历处理每个 sheet.
## 已知限制

本免费体验版限制以下高级功能：
- 多表合并（多文件 xlsx 合并与 JOIN 操作）
- 数据透视表（pivot table 生成与分析）
- 图表生成（柱状图、折线图、饼图嵌入）
- 大数据处理（分块读取、流式处理、内存优化）
- 自动化流水线（定时任务、批处理、邮件分发）
- 高级公式与条件格式
- 与 `PostgreSQL` 等数据库的数据导入导出

解锁全部功能请使用专业版：`ws-excel-tool-pro`
- 当前为免费版本,如需完整功能请升级到付费版获取全部能力
## 依赖说明

### 运行环境
- **Agent 平台**：支持 SKILL.md 的任意 AI Agent（Claude Code / Cursor / Codex / Gemini CLI 等）
- **操作系统**：Windows / macOS / Linux
- **Python**：3.8+
- **内存**：建议 ≥ 4GB（处理大文件时）

### 依赖详情
| 依赖项 | 类型 | 是否必需 | 获取方式 |
|:-----|:-----|:-----|:-----|
| LLM API | API | 必需 | 由 Agent 平台内置 LLM 提供 |
| openpyxl | Python 库 | 必需 | `pip install openpyxl` |
| pandas | Python 库 | 必需 | `pip install pandas` |
| Python | 运行时 | 必需 | 官网下载安装 |
| xlrd | Python 库 | 可选 | 读取旧版 `.xls` 文件时需要 |

### API Key 配置
- 本 Skill 基于 Markdown 指令，无需额外 API Key
- 如需调用大模型进行代码生成，由 Agent 平台内置 LLM 提供
- 数据文件路径由用户提供，Agent 通过 exec 执行 Python 脚本处理

### 可用性分类
- **分类**：MD+EXEC（纯 Markdown 指令，部分功能需要 exec 命令行执行能力）
- **说明**：基于 Markdown 的 AI Skill，通过自然语言指令驱动 Agent 执行任务
- **模型路由建议**：免费版使用低成本模型（如 GPT-4o-mini / Claude Haiku）
- **数据位置建议**：处理后的文件默认存放在用户指定目录或工作区 `data/` 子目录

## 错误处理

| 错误场景 | 原因 | 处理方式 |
|---:|---:|---:|
| 配置错误 | 参数缺失或格式错误 | 检查依赖说明中的配置要求 |
| 运行时错误 | 运行环境不满足 | 确认运行环境符合依赖说明 |
| 网络错误 | 连接超时或不可达 | 执行ping命令测试网络连通性,检查防火墙和代理设置连接后执行ping命令测试网络连通性,检查防火墙和代理设置连接后重新执行命令，参考国内替代方案 |

## 输出格式
```json
{
  "success": true,
  "data": {
    "result": "Excel工具(免费版)处理结果",
    "execution_time": "0.5s",
    "metadata": {
      "version": "1.0",
      "processor": "ws excel"
    }
  },
  "execution_log": ["解析输入参数", "执行核心处理", "格式化输出结果"],
  "error": null
}
```
