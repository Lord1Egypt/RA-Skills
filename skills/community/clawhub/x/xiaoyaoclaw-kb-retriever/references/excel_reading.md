# Excel 文件读取

> 🌐 语言 / Language：本文档是**内容规范**而非语言约束；默认中文，用户用英文或其他语言提问时就用该语言回答。
> This document is a content spec, not a language mandate — answer in the user's language.

> ⚠️ **使用本文档前请注意**：本文档应在实际处理 Excel 文件之前阅读，以了解正确的 pandas 读取方法。请配合 excel_analysis.md 一起使用。

使用 pandas 读取 Excel 文件的核心方法。

> ⚠️ **读取边界**：示例中的 `kb_path(...)` 来自 `scripts/pathguard.py` 的受控助手
> （见 `references/pdf_reading.md` 顶部完整实现）。所有读取都必须先解析真实路径
> 并确认仍在知识库根内；不要直接把用户给的相对路径交给 pandas。

## 快速入门

**最常用的读取方式**：
```python
import pandas as pd

# 读取第一个工作表（或指定工作表）
df = pd.read_excel(kb_path("data.xlsx"), sheet_name="Sheet1")

# 只读取前几行查看结构
df_preview = pd.read_excel(kb_path("data.xlsx"), nrows=10)

# 只读取需要的列（提高性能）
df = pd.read_excel(kb_path("data.xlsx"), usecols=["列1", "列2", "列3"])
```

## 读取单个工作表

```python
import pandas as pd

# 读取指定工作表
df = pd.read_excel(kb_path("data.xlsx"), sheet_name="Sheet1")

# 查看前几行
print(df.head())

# 基本统计信息
print(df.describe())
```

## 读取整个工作簿的所有工作表

```python
import pandas as pd

# 读取所有工作表
excel_file = pd.ExcelFile(kb_path("workbook.xlsx"))

for sheet_name in excel_file.sheet_names:
    df = pd.read_excel(excel_file, sheet_name=sheet_name)
    print(f"\n{sheet_name}:")
    print(df.head())
```

## 读取特定列

```python
import pandas as pd

# 只读取指定列（提高性能）
df = pd.read_excel(kb_path("data.xlsx"), usecols=["column1", "column2", "column3"])
```

## 性能优化选项

- 使用 `usecols` 只读取需要的列
- 使用 `dtype` 参数指定列类型以加快读取速度
- 根据文件类型选择合适的引擎：`engine='openpyxl'` 或 `engine='xlrd'`

## 处理大文件

对于非常大的 Excel 文件，避免一次性读取整个文件：
- 使用 `nrows` 参数限制读取的行数
- 先读取前若干行了解数据结构
- 按需分批处理数据
