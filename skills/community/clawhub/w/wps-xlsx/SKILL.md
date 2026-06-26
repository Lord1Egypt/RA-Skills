---
name: xlsx
description: 创建、编辑或分析 .xlsx / .xlsm / .csv / .tsv 文件。当用户要求生成、处理、下载 Excel 表格，或提及表格文件名/路径并希望对其操作时，使用本技能。包括：打开、读取、编辑、修复已有文件（增列、计算、格式化、图表、数据清洗），从零或其他数据源创建新表格，以及表格格式间的转换。对于结构混乱的表格数据（错行、表头错位、垃圾数据）清洗为规范表格也适用。交付物须为表格文件；当用户未指定格式时默认生成 .xlsx 而非 .csv 等其他格式。若主要产出为 Word 文档、HTML 报告、独立 Python 脚本或数据库管道，则不应触发本技能。
---

# 核心原则

每份交付的 Excel 文件须同时满足以下四点：

1. **零公式错误**：不得出现 `#REF!` `#DIV/0!` `#VALUE!` `#N/A` `#NAME?`
2. **视觉美观**：使用统一的专业字体（如 Arial、微软雅黑），表头与数据区层次分明，数字格式统一，列宽适配内容，整体风格协调
3. **图表配套**：数据中存在对比、趋势或占比维度时，配套生成相应图表（折线图 / 柱状图 / 饼图等），提升可阅读性
4. **保留已有模板**：修改现有文件时，必须完全匹配原有格式、样式和约定，绝不覆盖已有样式，现有约定优先于本指南
5. **区分任务类型，保护原表数据**：先判断用户意图——若是多个文件汇总为一个新表，可创建新文件；若是基于现有文件进行处理（如分析、汇总、增加图表），则必须在原文件基础上操作，保留所有原始 Sheet 及其数据，将结果写入新增的 Sheet，不得丢弃或覆盖原始数据

---

# 工作流

## 工具使用规则

所有 Python 代码统一通过 **`jupyter_cell_exec`工具** 执行（用户每次提问时自动启动新内核）。输出文件保存到工作目录（`OUTPUT_ROOT`）下。注意：用户每发起新提问时 Jupyter 环境会重置，变量与状态仅在当轮多次调用之间保留。

## 执行步骤

1. **规划结构**：确定 Sheet 划分、数据布局、需要生成的图表类型
2. **选择库**：数据分析用 pandas，公式 / 格式 / 图表处理用 openpyxl
3. **编写并执行代码**：通过 `jupyter_cell_exec`工具 在**同一个代码块**中完成文件创建与公式重算。使用了公式时，必须在保存文件后紧接着调用 `recalc()` 验证：

   ```python
   # ... 创建/编辑 Excel 文件的代码 ...
   wb.save(output_path)

   # 重算公式并验证（使用了公式时必须执行）
   import sys, os
   sys.path.insert(0, os.path.join(os.getenv('skill_path'), 'xlsx', 'scripts'))
   from recalc import recalc
   result = recalc(output_path)
   print(result)
   ```

   - 函数签名：`recalc(filename: str, timeout: int = 60) -> dict`
   - 纯 Python 重算所有公式，并扫描全部单元格检查错误（无需安装外部软件）

4. **验证与修复**：
   - 若返回 `status: "errors_found"`，根据 `error_summary` 中的位置修复后再次调用 `recalc()`
   - 常见错误：`#REF!`（无效引用）、`#DIV/0!`（除以零）、`#VALUE!`（数据类型错误）、`#NAME?`（未识别的公式名）

---

# 关键原则：使用公式，不要硬编码值

**始终使用 Excel 公式，而非在 Python 中计算后将结果硬编码写入。** 这样表格才能在源数据变化时自动重算。

### ❌ 错误做法

```python
total = df['Sales'].sum()
sheet['B10'] = total          # 硬编码为 5000

growth = (df.iloc[-1]['Revenue'] - df.iloc[0]['Revenue']) / df.iloc[0]['Revenue']
sheet['C5'] = growth          # 硬编码为 0.15
```

### ✅ 正确做法

```python
sheet['B10'] = '=SUM(B2:B9)'
sheet['C5'] = '=(C4-C2)/C2'
sheet['D20'] = '=AVERAGE(D2:D19)'
```

所有计算——合计、百分比、比率、差值——均适用此原则。

---

# 多 Sheet 处理复杂任务

当任务涉及多个维度、多个数据集或数据量较大时，将内容合理拆分到多个 Sheet，而非堆在一张表上。每个 Sheet 聚焦单一主题，并在顶部用简短说明交代该 Sheet 的用途与数据范围，帮助读者快速定位所需信息。

---

# 技术参考

## 读取与分析数据

### 使用 pandas（推荐用 jupyter_cell_exec工具）

```python
import pandas as pd

df = pd.read_excel('file.xlsx')
all_sheets = pd.read_excel('file.xlsx', sheet_name=None)

df.head()
df.info()
df.describe()

df.to_excel('output.xlsx', index=False)
```

## 创建新 Excel 文件

```python
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment

wb = Workbook()
sheet = wb.active

sheet['A1'] = 'Hello'
sheet['B1'] = 'World'
sheet.append(['Row', 'of', 'data'])

sheet['B2'] = '=SUM(A1:A10)'

sheet['A1'].font = Font(bold=True, color='FF0000')
sheet['A1'].fill = PatternFill('solid', start_color='FFFF00')
sheet['A1'].alignment = Alignment(horizontal='center')
sheet.column_dimensions['A'].width = 20

wb.save('output.xlsx')
```

## 编辑现有 Excel 文件

```python
from openpyxl import load_workbook

wb = load_workbook('existing.xlsx')
sheet = wb.active

sheet['A1'] = 'New Value'
sheet.insert_rows(2)
sheet.delete_cols(3)

new_sheet = wb.create_sheet('NewSheet')
new_sheet['A1'] = 'Data'

wb.save('modified.xlsx')
```

## 重算公式

openpyxl 写入的公式只是字符串，Excel 打开前不会有计算值。通过 `recalc` 模块使用纯 Python 引擎重算所有公式，并扫描全部单元格检查错误。无需安装任何外部软件。

### 使用方式

```python
import sys, os
sys.path.insert(0, os.path.join(os.getenv('skill_path'), 'xlsx', 'scripts'))
from recalc import recalc

result = recalc("/path/to/output.xlsx")
print(result)
```

### 函数签名

```python
recalc(filename: str, timeout: int = 60) -> dict
```

- `filename`：xlsx 文件的绝对路径
- `timeout`：重算超时秒数，默认 60

### 返回值

```json
{
  "status": "success",
  "total_errors": 0,
  "total_formulas": 42,
  "error_summary": {}
}
```

若 `status` 为 `errors_found`，`error_summary` 会列出每种错误的位置（最多 20 处）：

```json
{
  "status": "errors_found",
  "total_errors": 2,
  "total_formulas": 42,
  "error_summary": {
    "#REF!": {
      "count": 2,
      "locations": ["Sheet1!B5", "Sheet1!C10"]
    }
  }
}
```

### 支持的函数范围

recalc 使用纯 Python 公式引擎，覆盖大多数常用 Excel 函数：

- 数学：SUM, AVERAGE, COUNT, COUNTA, MIN, MAX, ROUND, ABS, MOD
- 逻辑：IF, AND, OR, NOT, IFERROR
- 查找：VLOOKUP, HLOOKUP, INDEX, MATCH, OFFSET
- 条件：SUMIF, SUMIFS, COUNTIF, COUNTIFS, AVERAGEIF
- 文本：LEFT, RIGHT, MID, LEN, CONCATENATE, TRIM, UPPER, LOWER
- 日期：DATE, YEAR, MONTH, DAY, TODAY, NOW
- 财务：NPV, IRR, PMT, FV, PV

若遇到不支持的函数，recalc 会降级为静态分析（检查引用和结构），并在返回值中包含 `warning` 字段说明情况。

## 公式验证清单

### 必要验证

- [ ] 先在 2-3 个单元格上测试公式，确认值正确后再批量应用
- [ ] 列映射：确认 Excel 列对应关系（第 64 列 = BL）
- [ ] 行偏移：Excel 行从 1 开始（DataFrame 第 5 行 = Excel 第 6 行）
- [ ] 验证公式引用的所有单元格确实存在

### 常见陷阱

- [ ] NaN 处理：用 `pd.notna()` 检查空值
- [ ] 远右侧列：财年数据常在第 50+ 列
- [ ] 多重匹配：搜索所有匹配项而非只取第一个
- [ ] 除以零：在公式中使用 `/` 前检查分母（`#DIV/0!`）
- [ ] 跨表引用：使用正确格式（`Sheet1!A1`）
- [ ] 边界测试：包含零值、负数和超大数值的场景

---

# 财务模型规范

### 颜色编码（除非用户或现有模板另有说明）

- **蓝色文字（RGB: 0,0,255）**：硬编码输入值
- **黑色文字（RGB: 0,0,0）**：所有公式和计算结果
- **绿色文字（RGB: 0,128,0）**：同一工作簿内跨工作表的引用链接
- **红色文字（RGB: 255,0,0）**：链接到其他文件的外部引用
- **黄色背景（RGB: 255,255,0）**：关键假设或需要更新的单元格

### 数字格式

- **年份**：文本字符串（如 "2024" 而非 "2,024"）
- **货币**：`$#,##0`，表头注明单位（如 "Revenue ($mm)"）
- **零值**：显示为 "-"（格式：`$#,##0;($#,##0);-`）
- **百分比**：`0.0%`
- **倍数**：`0.0x`
- **负数**：括号形式 `(123)`

### 公式构建

- 将所有假设放在独立单元格，公式引用单元格而非硬编码：`=B5*(1+$B$6)` 而非 `=B5*1.05`
- 修改现有模板时，必须完全匹配原有格式、样式和约定，现有约定优先于本指南

### 硬编码值来源文档

- 所有硬编码数值须标注来源，格式：`Source: [系统/文档], [日期], [具体引用], [URL（如有）]`
- 示例：
  - `Source: 公司年报, FY2024, 第45页, 营收附注`
  - `Source: Bloomberg Terminal, 2025/8/15, AAPL US Equity`
  - `Source: Wind, 2025/8/20, 一致预期数据`

### 图表布局（TwoCellAnchor 网格系统）

使用 `TwoCellAnchor` 精确定位，**必须遵循网格布局规则防止重叠**。

#### 网格布局规则（必须遵守）

将图表区域看作网格，先确定布局参数，再算每个图表的坐标：

```
布局参数（先确定再写代码）:
  DATA_END_ROW  = 数据区最后一行（0-indexed）
  CHART_START   = DATA_END_ROW + 2（图表起始行，留 1 行缓冲）
  COLS_PER_CHART = 7（每个图表占的列数，推荐 6-8）
  ROWS_PER_CHART = 15（每个图表占的行数，推荐 14-16）
  GAP_COLS = 1（列间距，必须 ≥ 1）
  GAP_ROWS = 2（行间距，必须 ≥ 2）

网格坐标计算公式:
  第 i 行第 j 列图表（i, j 从 0 开始）:
    from_col = j * (COLS_PER_CHART + GAP_COLS)
    from_row = CHART_START + i * (ROWS_PER_CHART + GAP_ROWS)
    to_col   = from_col + COLS_PER_CHART
    to_row   = from_row + ROWS_PER_CHART
```

**核心规则**：

1. 相邻图表的坐标范围**绝不允许重叠** — 即一个图表的 `to_col` 必须 ≤ 下一列图表的 `from_col`，`to_row` 必须 ≤ 下一行图表的 `from_row`
2. **图表区域内禁止存放任何数据** — 图表网格占据的整个矩形区域（从 `CHART_START` 行、第 0 列开始，到最后一个图表的 `to_row`、`to_col`）内不得写入辅助数据
3. 图表需要的辅助数据（如分布统计、饼图源数据等）必须放在**图表区域之外**：写在主数据表的右侧空列（确保不与图表列重叠），或写在单独的 sheet 中

#### 代码模板（6 个图表 2×3 网格）

```python
from openpyxl.chart import BarChart, PieChart, LineChart
from openpyxl.drawing.spreadsheet_drawing import TwoCellAnchor

# 1. 确定布局参数
CHART_START = 19      # 数据区结束后 +2
COLS = 7              # 每图表占 7 列
ROWS = 15             # 每图表占 15 行
GAP_C = 1             # 列间距（图表之间留 1 列空白）
GAP_R = 2             # 行间距（图表之间留 2 行空白）

def place_chart(ws, chart, grid_row, grid_col):
    """将图表放入网格的 (grid_row, grid_col) 位置，0-indexed"""
    a = TwoCellAnchor()
    a._from.col = grid_col * (COLS + GAP_C)
    a._from.row = CHART_START + grid_row * (ROWS + GAP_R)
    a.to.col = a._from.col + COLS
    a.to.row = a._from.row + ROWS
    chart.anchor = a
    ws._charts.append(chart)

# 2. 创建图表并放入网格（图表之间自动留白）
#    第 0 行: chart1(0,0)  [1列空白]  chart2(0,1)
#    [2行空白]
#    第 1 行: chart3(1,0)  [1列空白]  chart4(1,1)
#    [2行空白]
#    第 2 行: chart5(2,0)  [1列空白]  chart6(2,1)
place_chart(ws, chart1, 0, 0)  # A20:G34
place_chart(ws, chart2, 0, 1)  # I20:O34  (H列空白)
place_chart(ws, chart3, 1, 0)  # A37:G51  (35-36行空白)
place_chart(ws, chart4, 1, 1)  # I37:O51
place_chart(ws, chart5, 2, 0)  # A54:G68
place_chart(ws, chart6, 2, 1)  # I54:O68
```

**关键点**：

- `anchor._from.col/row` 和 `anchor.to.col/row` 都是 **0-indexed**
- 第 1 行 = `row = 0`，A 列 = `col = 0`
- 占据行数 = `to.row - _from.row`
- **不要手动计算每个图表的坐标** — 用 `place_chart` 函数或等价的公式统一计算，避免算错

#### 图表数据引用（Reference）

**关键原则**：`Reference` 的行列范围必须精确匹配数据区域，避免包含多余的表头或空行。

```python
from openpyxl.chart import Reference

# 假设数据结构：
# A1: 姓名  B1: 语文  C1: 数学  D1: 英语  E1: 总分
# A2: 张三  B2: 85    C2: 90    D2: 88    E2: 263
# A3: 李四  B3: 78    C3: 82    D3: 85    E3: 245
# ... (共 8 行数据，A2:E9)

# ✅ 正确：柱状图显示总分
data = Reference(ws, min_col=5, min_row=1, max_row=9)  # E1:E9（包含表头"总分"）
categories = Reference(ws, min_col=1, min_row=2, max_row=9)  # A2:A9（学生姓名，不含表头）
chart.add_data(data, titles_from_data=True)  # titles_from_data=True 会把 E1 作为系列名
chart.set_categories(categories)

# ✅ 正确：折线图显示三科成绩
data = Reference(ws, min_col=2, max_col=4, min_row=1, max_row=9)  # B1:D9（包含表头）
categories = Reference(ws, min_col=1, min_row=2, max_row=9)  # A2:A9（学生姓名）
chart.add_data(data, titles_from_data=True)  # B1:D1 作为系列名（语文、数学、英语）
chart.set_categories(categories)

# ❌ 错误：data 包含了姓名列
data = Reference(ws, min_col=1, max_col=4, min_row=1, max_row=9)  # 错误地包含了 A 列
chart.add_data(data, titles_from_data=True)  # 会把"姓名"也当成数据系列

# ❌ 错误：categories 包含了表头
categories = Reference(ws, min_col=1, min_row=1, max_row=9)  # 错误地包含了 A1
chart.set_categories(categories)  # 横轴会显示"姓名 张三 李四..."
```

**关键点**：

- `min_row=1` 且 `titles_from_data=True` → 第 1 行作为系列名（图例）
- `min_row=2` → 从第 2 行开始取数据
- `categories` 通常不包含表头（`min_row=2`）
- `data` 包含表头时设置 `titles_from_data=True`

**饼图特殊说明**：

```python
# 饼图通常只有一个数据系列，不需要系列名
# ✅ 正确：data 和 categories 都不包含表头
data = Reference(ws, min_col=2, min_row=2, max_row=5)  # B2:B5（数值）
categories = Reference(ws, min_col=1, min_row=2, max_row=5)  # A2:A5（分类名）
pie_chart.add_data(data, titles_from_data=False)  # 饼图不需要系列名
pie_chart.set_categories(categories)

# ❌ 错误：data 包含表头会导致标签显示 "表头名, 分类名, 值, 百分比"
data = Reference(ws, min_col=2, min_row=1, max_row=5)  # B1:B5（包含表头）
pie_chart.add_data(data, titles_from_data=True)  # 错误！饼图标签会变成 "人数, 90分以上, 10, 100%"
```

#### ⚠️ 禁止使用 `add_chart` + `width/height`

不要使用 `ws.add_chart(chart, 'A3')` + `chart.width/height`，该方案的单位是 cm，极易算错导致重叠。**始终使用上述 TwoCellAnchor 网格系统。**

---

# 最佳实践

### 库的选择

- **pandas**：数据分析、批量操作、简单数据导出
- **openpyxl**：复杂格式、公式、Excel 特有功能

### openpyxl 注意事项

- 单元格索引从 1 开始（row=1, column=1 对应 A1）
- `data_only=True` 读取已计算的值；以此模式保存会永久丢失公式
- 大文件：读取用 `read_only=True`，写入用 `write_only=True`

### pandas 注意事项

- 指定数据类型：`pd.read_excel('file.xlsx', dtype={'id': str})`
- 只读取需要的列：`pd.read_excel('file.xlsx', usecols=['A', 'C', 'E'])`
- 日期处理：`pd.read_excel('file.xlsx', parse_dates=['date_column'])`

## 代码风格规范

**Python 脚本**：编写简洁代码，避免多余注释、冗长变量名和不必要的 print。

**Excel 文件本身**：为复杂公式或关键假设添加单元格注释，为硬编码值注明数据来源。
