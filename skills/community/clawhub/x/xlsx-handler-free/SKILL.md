---
slug: xlsx-handler-free
name: xlsx-handler-free
version: 1.0.0
displayName: XLSX处理免费版
summary: 安全读写 XLSX 工作簿，保留公式、日期、合并单元格与样式，适合单文件编辑与检查。
license: Proprietary
edition: free
description: XLSX 处理免费版面向需要程序化读写 Excel 工作簿的开发者与运维人员，提供"按任务选工具"的工作流——区分 pandas 与 openpyxl
  适用场景，避免公式丢失、日期损坏、合并单元格错乱等常见陷阱。所有操作在交付前进行校验，确保零公式错误。Use when 需要文件处理、文档转换、格式互转、内容提取时使用。不适用于加密文件破解。
tags:
- 集成工具
- 表格处理
- 开发者工具
tools:
- - read
- exec
homepage: https://skillhub.cn
pricing_tier: L2
pricing_model: per_use
suggested_price: 19.9
tools: ["read", "write", "exec"]
tags: "工具,效率,自动化"
---
# XLSX 处理（免费版）

本 Skill 把 Excel 工作簿读写操作规范化——按任务选工具、保护既有结构、交付前校验。免费版覆盖单文件读写与检查场景。

## 概述

程序化操作 Excel 的常见陷阱不少：用 pandas 读后写，公式被静默替换为缓存值；用 openpyxl 写长 ID，Excel 自动转为科学计数法；合并单元格只有左上角保留值；日期在不同系统下序列号差异。本 Skill 把这些陷阱总结为"七条核心规则"，让 Agent 在读写前先做类型判断与结构检查，避免破坏既有工作簿。

## 核心能力

| 能力模块 | 输入 | 输出 | 说明 |
|----|---|---|---|
| 工作簿读取 | .xlsx 文件 | 数据 + 元信息 | 保留公式与样式 |
| 工作簿写入 | 数据 + 模板 | .xlsx 文件 | 不破坏既有结构 |
| 日期处理 | 日期单元格 | 真实日期 / 序列号 | 兼容 1900/1904 |
| 类型保护 | 长 ID / 电话 | 文本存储 | 避免精度丢失 |
| 结构检查 | 工作簿 | 报告 | 列出问题项 |
| 错误校验 | 工作簿 | 错误清单 | 零错误交付 |
**技术实现要点**：核心能力基于`input_params`参数与`output_format`配置实现,支持创建/查询/修改/删除等操作模式,通过`config_options`进行运行时配置。

### 核心功能执行
用`input_params`参数进行配置。

**输入**: 用户提供核心功能执行所需的指令和必要参数。
**处理**: 解析核心功能执行的输入参数,完成核心逻辑,返回结构化响应。
**输出**: 返回核心功能执行的响应数据,包含状态码、结果和日志。
- 执行此能力时使用`input_params`参数,支持创建/查询/导出操作

### 参数配置与调用
用`config_options`参数进行配置。

**输入**: 用户提供参数配置与调用所需的指令和必要参数。
**处理**: 解析参数配置与调用的输入参数,完成核心逻辑,返回结构化响应。
**输出**: 返回参数配置与调用的响应数据,包含状态码、结果和日志。
- 执行此能力时使用`config_options`参数,支持修改/重置/导入操作

### 结果处理与输出
用`output_format`参数进行配置。

**输入**: 用户提供结果处理与输出所需的指令和必要参数。
**处理**: 解析结果处理与输出的输入参数,完成核心逻辑,返回结构化响应。
**输出**: 返回结果处理与输出的响应数据,包含状态码、结果和日志。
- 执行此能力时使用`output_format`参数,支持导出/保存/转换操作
**能力覆盖范围**：本skill的核心能力覆盖以下场景关键词：安全读写、XLSX、工作簿、保留公式、合并单元格与样式、适合单文件编辑与、处理免费版面向需、要程序化读写、Excel、工作簿的开发者与、运维人员、按任务选工具、的工作流、pandas、openpyxl、适用场景、避免公式丢失、日期损坏、合并单元格错乱等、常见陷阱、所有操作在交付前、进行校验、确保零公式错误、Use、when、需要文件处理、文档转换、格式互转、内容提取时使用、不适用于加密文件等。

## 使用场景

### 场景一：读取既有模板填充数据（运营角色）
财务提供了一份格式精美的模板，需要在指定 Sheet 的指定区域填入数据，且不能破坏样式。本 Skill 输出 openpyxl 加载 → 定位单元格 → 写入 → 保存的步骤，保留所有样式与公式。

### 场景二：检查工作簿结构（审计角色）
接手一份陌生工作簿，需要快速了解结构——多少 Sheet、有哪些命名范围、隐藏行列、合并单元格、外部引用。本 Skill 输出结构检查脚本，一键生成报告。

## 错误处理
Excel 中日期看起来是 `2024/01/01`，但实际存储是序列号 `45292`。从不同系统导入的日期可能使用 1904 系统，导致所有日期偏差 1462 天。本 Skill 输出统一的日期解析与转换逻辑。

### 场景四：长 ID 精度保护（开发者角色）
18 位身份证号、20 位订单号、国际电话号码——这些值在 Excel 中容易被转为科学计数法或截断到 15 位精度。本 Skill 强制按文本存储，保留完整字符串。
### 错误场景2

检查`error_code`并按照处理方式进行排查。

### 错误场景3

## 快速开始

1. 阅读## 核心能力章节了解skill功能
2. 按## 依赖说明配置环境
3. 执行所需能力对应的命令
4. 参考## 错误处理章节处理异常
5. 查看## FAQ解答常见疑问

### 工具选择决策树

```text
任务类型？
├── 分析、重塑、CSV 类 → 用 pandas
├── 保留公式 / 样式 / 合并 / 多 Sheet → 用 openpyxl
├── 纯数据交换（无格式） → CSV 更可靠
└── 从零构建模型 → openpyxl + 公式
```

### 读取并保留公式

```python
from openpyxl import load_workbook
# ...
# 保留公式（不计算）
wb = load_workbook('report.xlsx', data_only=False)
ws = wb['Sheet1']
# ...
# 读取公式字符串
formula = ws['A1'].value  # 如 '=SUM(B1:B10)'
# ...
# 读取缓存值（Excel 上次保存时的计算结果）
wb_cached = load_workbook('report.xlsx', data_only=True)
ws_cached = wb_cached['Sheet1']
cached_value = ws_cached['A1'].value  # 如 12345.67
```

### 写入并保留结构

```python
from openpyxl import load_workbook
# ...
# 加载既有模板
wb = load_workbook('template.xlsx')
ws = wb['Data']
# ...
# 在指定区域写入数据（保留其他单元格格式）
data = [['2026-07', '产品A', 1000], ['2026-07', '产品B', 2000]]
for r, row in enumerate(data, 2):  # 从第 2 行开始
    for c, v in enumerate(row, 1):
        ws.cell(row=r, column=c, value=v)
# ...
# 长数字强制文本
ws.cell(row=2, column=4).value = '110101199001011234'
ws.cell(row=2, column=4).number_format = '@'  # 文本格式
# ...
wb.save('output.xlsx')
```

## 示例

### 工作簿结构检查脚本

```python
from openpyxl import load_workbook
# ...
def inspect_workbook(path: str) -> dict:
    """检查工作簿结构，输出问题清单。"""
    wb = load_workbook(path)
    report = {
        'sheets': [],
        'defined_names': list(wb.defined_names),
        'issues': []
    }
# ...
    for ws in wb.worksheets:
        sheet_info = {
            'name': ws.title,
            'dimensions': ws.dimensions,
            'merged_cells': list(ws.merged_cells.ranges),
            'hidden_rows': [],
            'hidden_cols': [],
            'formulas': 0,
            'errors': 0
        }
# ...
        # 检查隐藏行列
        for row_dim in ws.row_dimensions.values():
            if row_dim.hidden:
                sheet_info['hidden_rows'].append(row_dim)
        for col_dim in ws.column_dimensions.values():
            if col_dim.hidden:
                sheet_info['hidden_cols'].append(col_dim)
# ...
        # 检查公式与错误
        for row in ws.iter_rows():
            for cell in row:
                if cell.value and isinstance(cell.value, str):
                    if cell.value.startswith('='):
                        sheet_info['formulas'] += 1
                    if cell.value in ('#REF!', '#DIV/0!', '#VALUE!', '#NAME?'):
                        sheet_info['errors'] += 1
                        report['issues'].append({
                            'sheet': ws.title,
                            'cell': cell.coordinate,
                            'error': cell.value
                        })
# ...
        report['sheets'].append(sheet_info)
# ...
    return report
# ...
import json
report = inspect_workbook('report.xlsx')
print(json.dumps(report, indent=2, ensure_ascii=False, default=str))
```

### 日期处理标准模式

```python
from openpyxl import load_workbook
from datetime import datetime, timedelta
# ...
def safe_parse_date(serial: int, date_system: str = '1900') -> datetime:
    """将 Excel 日期序列号转为真实日期。"""
    if date_system == '1900':
        # Excel 1900 系统包含 1900-02-29 假闰日 bug
        if serial >= 60:
            serial -= 1
        return datetime(1899, 12, 30) + timedelta(days=serial)
    elif date_system == '1904':
        return datetime(1904, 1, 1) + timedelta(days=serial - 1)
    else:
        raise ValueError(f"未知日期系统：{date_system}")
# ...
# 检查工作簿使用哪个日期系统
wb = load_workbook('legacy.xlsx')
ws = wb.active
print(f"使用 1904 日期系统：{ws.sheet_properties.date1904}")
```

## 最佳实践

1. **按任务选工具**：分析用 pandas，保留结构用 openpyxl，纯数据用 CSV。
2. **公式保留**：加载时 `data_only=False`，保存时检查公式未被替换为缓存值。
3. **类型保护**：长 ID、电话、邮编等设置 `number_format = '@'` 强制文本。
4. **日期系统**：处理旧版文件先确认 `sheet_properties.date1904` 标志。
5. **合并单元格**：只有左上角保留值，读取时定位到左上角。
6. **样式继承**：新填充单元格匹配既有样式，避免引入新视觉系统。
7. **交付前校验**：检查无 `#REF!` / `#DIV/0!` / `#VALUE!` / `#NAME?` 残留。
8. **流式读取大文件**：超过 10MB 用 `read_only=True`，避免内存爆炸。
9. **保留视图状态**：冻结窗格、筛选、打印区域需明确处理，避免静默丢失。

## 常见问题

### Q1：用 pandas 读取后公式不见了？
A：pandas 把公式计算结果作为值读入，写回时只剩静态值。需要保留公式必须用 openpyxl 的 `data_only=False` 模式。

### Q2：日期看起来对但排序错乱？
A：可能是文本日期而非真实日期序列号。用 `cell.is_date` 判断，必要时用 `DATEVALUE` 转换。

### Q3：18 位身份证显示为科学计数法？
A：Excel 默认把长数字转为数值，精度截断到 15 位。必须设置 `number_format = '@'` 强制文本存储。

### Q4：合并单元格读取值不对？
A：合并范围内只有左上角单元格保留值，其他单元格为 None。读取时定位到左上角。

### Q5：打开后保存，工作簿大小膨胀？
A：可能是 `read_only=False` 模式加载了全部样式信息。建议保留视图状态时显式指定要保留的属性，避免不必要的元数据写入。

### Q6：跨平台打开后筛选丢失？
A：LibreOffice 与 Numbers 对部分筛选语法支持不全。建议分发前同时测试三个平台。

## 依赖说明

### 运行环境
- **Agent 平台**：支持 SKILL.md 的任意 AI Agent（Claude Code / Cursor / Codex / Gemini CLI 等）
- **操作系统**：Windows / macOS / Linux
- **Python**：3.8+
- **办公软件**：Excel / WPS / LibreOffice 任一，用于打开结果文件

### 依赖详情
| 依赖项 | 类型 | 是否必需 | 获取方式 |
|:-----|:-----|:-----|:-----|
| LLM API | API | 必需 | 由 Agent 平台内置 LLM 提供 |
| Python3 | 运行时 | 必需 | 官网下载 |
| openpyxl | Python 库 | 必需 | `pip install openpyxl` |
| pandas | Python 库 | 可选 | `pip install pandas` |

### API Key 配置
- 本 Skill 基于本地 Python 与 openpyxl，无需额外 API Key
- 不涉及网络调用与外部端点
- 所有数据在本地处理，不上传任何服务器
- 禁止在 SKILL.md 或脚本中硬编码任何密钥或 Token

### 可用性分类
- **分类**：MD+EXEC（纯 Markdown 指令，部分功能需要 exec 命令行执行能力）
- **说明**：基于 Markdown 的 AI Skill，通过自然语言指令驱动 Agent 生成 Python 脚本并执行

## 已知限制

本免费体验版限制以下高级功能：
- 批量文件处理（一次仅处理单个文件）
- 大文件流式处理（建议文件 < 10MB）
- 跨平台深度兼容性测试（仅验证 Excel）
- 工作簿结构差异对比与合并
- 公式审计与依赖追踪
- 高级样式与条件格式生成
- 数据源对接（数据库、API）
- 优先技术支持

解锁全部功能请使用专业版：xlsx-handler-pro
- 当前为免费版本,如需完整功能请升级到付费版获取全部能力

## 输出格式
```json
{
  "success": true,
  "data": {
    "result": "XLSX处理免费版处理结果",
    "execution_time": "0.5s",
    "metadata": {
      "version": "1.0",
      "processor": "xlsx handler"
    }
  },
  "execution_log": ["解析输入参数", "执行核心处理", "格式化输出结果"],
  "error": null
}
```
