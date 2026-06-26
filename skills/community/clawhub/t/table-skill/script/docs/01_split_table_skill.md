# 表格拆分 Skill 代码逻辑文档

## 文件信息

- **文件路径**: `skills/split_table_skill.py`
- **功能**: 将 Excel/CSV 文件按空行拆分为多个独立的表格文件
- **输入**: 单个文件路径 (.xlsx/.xls/.csv)
- **输出**: 拆分后的多个 CSV 文件路径列表

---

## 整体架构

```
┌─────────────────────────────────────────────────────────────┐
│                    SplitTableSkill                          │
├─────────────────────────────────────────────────────────────┤
│  run() - 主入口                                             │
│  ├── 参数验证                                                │
│  ├── 输出目录准备                                            │
│  └── 根据文件类型分发                                        │
│      ├── _split_csv() - CSV 拆分                            │
│      └── _split_excel() - Excel 拆分                        │
│          ├── _split_excel_spire() - Spire 方案 (优先)       │
│          └── _split_excel_fallback() - 回退方案             │
│              ├── openpyxl 处理 .xlsx                        │
│              └── xlrd 处理 .xls                             │
└─────────────────────────────────────────────────────────────┘
```

---

## 核心流程

### 1. 主入口 `run()`

**位置**: L48-95

**流程**:
```python
async def run(self, input_file: str, output_dir: str = None) -> Dict[str, Any]:
    # 1. 文件存在性检查
    if not os.path.exists(input_file):
        return {"success": False, "error": f"文件不存在：{input_file}"}
    
    # 2. 设置输出目录
    if output_dir is None:
        output_dir = os.path.dirname(os.path.abspath(input_file))
    os.makedirs(output_dir, exist_ok=True)
    
    # 3. 提取文件基础名
    base_name = os.path.splitext(os.path.basename(input_file))[0]
    
    # 4. 根据文件类型拆分
    if input_file.endswith('.csv'):
        split_files = await self._split_csv(input_file, output_dir, base_name)
    else:
        split_files = await self._split_excel(input_file, output_dir, base_name)
    
    # 5. 返回结果
    return {
        "split_files": split_files,
        "table_count": len(split_files),
        "success": True,
        "output_dir": output_dir
    }
```

**关键点**:
- ✅ 自动创建输出目录
- ✅ 统一的错误处理
- ✅ 根据文件扩展名自动选择拆分策略

---

### 2. CSV 拆分 `_split_csv()`

**位置**: L94-118

**流程图**:
```
CSV 文件
   ↓
_read_csv(file_path)
   ↓
pd.DataFrame (header=None)
   ↓
remove_blank_rows_and_columns(df) ← 新增：移除开头结尾空白行列
   ↓
_split_by_empty_rows(df)
   ├─ 识别空行 (全为 nan/''/None 的行)
   ├─ 获取空行索引
   ├─ 按空行切分 DataFrame
   └─ 返回 [df1, df2, ...]
   ↓
遍历 sub_dfs
   ├─ idx=0 → "{base_name}.csv"
   ├─ idx>0 → "{base_name}_{idx+1}.csv"
   └─ 保存到 output_dir
   ↓
返回 [file_path1, file_path2, ...]
```

**核心代码**:
```python
async def _split_csv(self, file_path: str, output_dir: str, base_name: str) -> List[str]:
    # 1. 读取 CSV
    df = self._read_csv(file_path)
    
    # 1.5. 移除开头和结尾的空白行列（关键预处理）
    df = remove_blank_rows_and_columns(df)
    
    # 2. 按空行分割
    sub_dfs = self._split_by_empty_rows(df)
    
    # 3. 保存每个子表
    split_files = []
    for idx, sub_df in enumerate(sub_dfs):
        if idx == 0:
            out_name = f"{base_name}.csv"
        else:
            out_name = f"{base_name}_{idx + 1}.csv"
        
        out_path = os.path.join(output_dir, out_name)
        sub_df.to_csv(out_path, index=False, header=False, encoding='utf-8')
        split_files.append(out_path)
    
    return split_files
```

---

### 3. Excel 拆分 - Spire 方案

**位置**: L141-178

**流程图**:
```
Excel 文件
   ↓
split_workbook_all_sheets_return_worksheets(file_path)
   ├─ 加载 Workbook
   ├─ 遍历每个工作表
   │   ├─ preprocess_merge_spire() - 填充合并单元格
   │   └─ find_blocks_by_empty_rows() - 找数据块
   └─ 返回 [worksheet1, worksheet2, ...]
   ↓
遍历 worksheets
   ├─ 检查 IsEmpty
   ├─ preprocess_excel() - 类型转换
   │   ├─ 清理字符 (%,逗号等)
   │   ├─ 尝试 int 转换
   │   ├─ 尝试 float 转换
   │   └─ 保持字符串
   └─ 转为 pd.DataFrame
   ↓
保存为 CSV
   ↓
返回 [file_path1, file_path2, ...]
```

**核心代码**:
```python
async def _split_excel_spire(self, file_path: str, output_dir: str, base_name: str) -> List[str]:
    # 1. 拆分工作簿
    worksheets = split_workbook_all_sheets_return_worksheets(file_path)
    
    # 2. 加载样式模板
    from spire.xls import Workbook
    wb_template = Workbook()
    template_path = os.path.join(..., '2012 最新版土地开发整理项目人工预算单价计算表.xls')
    standard_style = None
    if os.path.exists(template_path):
        wb_template.LoadFromFile(template_path)
        standard_style = wb_template.Worksheets[0]['A1'].Style
    
    # 3. 遍历工作表
    split_files = []
    for idx, sheet in enumerate(worksheets):
        if sheet.IsEmpty:
            continue
        
        # 4. 预处理 Excel
        df = preprocess_excel(sheet, remove_chars=[','], standard_style=standard_style)
        
        # 5. 保存 CSV
        if idx == 0:
            out_name = f"{base_name}.csv"
        else:
            out_name = f"{base_name}_{idx + 1}.csv"
        
        out_path = os.path.join(output_dir, out_name)
        df.to_csv(out_path, index=False, header=False, encoding='utf-8')
        split_files.append(out_path)
    
    return split_files
```

---

### 4. Excel 拆分 - 回退方案

**位置**: L180-260

**流程图**:
```
Excel 文件
   ↓
判断文件扩展名
   ├─ .xlsx → openpyxl 路径
   │   ├─ load_workbook(data_only=True)
   │   ├─ 遍历 sheetnames
   │   │   ├─ preprocess_merge(ws) - 填充合并单元格
   │   │   ├─ ws_to_df(ws) - 转换为 DataFrame
   │   │   ├─ remove_blank_rows_and_columns(df) - 删除首尾空白
   │   │   └─ split_df_by_blank_rows(df, name) - 按空行分割
   │   └─ 保存为 CSV
   │
   └─ .xls → xlrd 路径
       ├─ open_workbook(formatting_info=True)
       ├─ 遍历 sheet_names
       │   ├─ preprocess_merge_xlrd(sheet) - 展开合并单元格
       │   ├─ 构建 merge_map
       │   ├─ 转换为 DataFrame
       │   ├─ remove_blank_rows_and_columns(df) - 删除首尾空白
       │   └─ split_df_by_blank_rows(df, name) - 按空行分割
       └─ 保存为 CSV
```

**核心代码 - openpyxl 分支**:
```python
if file_path.endswith('.xlsx'):
    from openpyxl import load_workbook
    wb = load_workbook(file_path, data_only=True)

    for sheet_name in wb.sheetnames:
        ws = wb[sheet_name]
        preprocess_merge(ws)
        # 将 ws 转换为 DataFrame
        df = ws_to_df(ws)
        # 先移除整个 sheet 开头和结尾的空白行列
        df = remove_blank_rows_and_columns(df)
        if df.empty:
            continue
        # 再按空行分割
        tables, filenames = split_df_by_blank_rows(df, sheet_name)
```

**核心代码 - xlrd 分支**:
```python
else:
    from xlrd import open_workbook
    excel = pd.ExcelFile(
        open_workbook(file_path, formatting_info=True),
        engine="xlrd"
    )

    for sheet_name in excel.sheet_names:
        sheet = excel.book[sheet_name]
        if sheet.nrows > 0 and sheet.ncols > 0:
            # 预处理合并单元格
            merge_map = {(r, c): v for (r, c, v) in preprocess_merge_xlrd(sheet)}

            # 将 xlrd sheet 转换为 DataFrame
            data = []
            for i in range(sheet.nrows):
                row = [merge_map.get((i, j), sheet.cell_value(i, j)) for j in range(sheet.ncols)]
                data.append(row)
            df = pd.DataFrame(data)

            # 先移除整个 sheet 开头和结尾的空白行列
            df = remove_blank_rows_and_columns(df)
            if df.empty:
                continue

            # 再按空行分割
            tables, filenames = split_df_by_blank_rows(df, sheet_name)
```

---

### 5. 辅助函数

#### 5.1 `_read_csv()`

**位置**: L241-253

**功能**: 读取 CSV，支持编码回退

```python
def _read_csv(self, file_path: str) -> pd.DataFrame:
    try:
        return pd.read_csv(file_path, header=None)
    except:
        return pd.read_csv(file_path, encoding='gbk', header=None)
```

#### 5.2 `_split_by_empty_rows()`

**位置**: L255-277

**功能**: 按空行分割 DataFrame

**算法**:
```python
def _split_by_empty_rows(self, df: pd.DataFrame) -> List[pd.DataFrame]:
    # 1. 识别空行
    df_str = df.astype(str)
    empty_mask = (df_str == 'nan') | (df_str == '') | df_str.isnull()
    empty_rows = empty_mask.all(axis=1)
    empty_indices = empty_rows[empty_rows].index.tolist()
    
    # 2. 无空行，返回原表
    if not empty_indices:
        return [df]
    
    # 3. 计算切分点
    split_points = [-1] + empty_indices + [len(df)]
    
    # 4. 切分
    sub_dfs = []
    for i in range(len(split_points) - 1):
        start = split_points[i] + 1
        end = split_points[i + 1]
        if start < end:
            sub_dfs.append(df.iloc[start:end].copy())
    
    return sub_dfs
```

---

## 数据流

```
输入文件
   ↓
[文件类型判断]
   ├─ CSV → _split_csv()
   │   └─ _read_csv() → remove_blank_rows_and_columns() → _split_by_empty_rows()
   │
   └─ Excel → _split_excel()
       ├─ Spire 方案 → split_workbook_all_sheets_return_worksheets()
       │                → preprocess_excel()
       │
       └─ 回退方案
           ├─ openpyxl → preprocess_merge() → ws_to_df() → remove_blank_rows_and_columns() → split_df_by_blank_rows()
           └─ xlrd → preprocess_merge_xlrd() → DataFrame → remove_blank_rows_and_columns() → split_df_by_blank_rows()

↓
遍历拆分后的 DataFrames
   ↓
保存为 CSV 文件
   ↓
返回文件路径列表
```

---

## 关键依赖

### 从 `.src` 导入:

```python
from .src import (
    split_workbook_all_sheets_return_worksheets,  # Excel 按工作表和空行拆分
    preprocess_excel,                              # Excel 单元格类型转换
    preprocess_merge,                              # openpyxl 合并单元格处理
    preprocess_merge_xlrd,                         # xlrd 合并单元格展开
    ws_to_df,                                     # openpyxl worksheet 转 DataFrame
    split_df_by_blank_rows,                       # DataFrame 按空行分割
    remove_blank_rows_and_columns,                 # 删除首尾空白行列
)
```

### 外部库:

- `pandas`: DataFrame 操作
- `spire.xls`: Excel 处理（优先）
- `openpyxl`: .xlsx 处理（回退）
- `xlrd`: .xls 处理（回退）

---

## 错误处理

1. **文件不存在**: 返回 `{"success": False, "error": "文件不存在：{path}"}`
2. **Spire 失败**: 自动回退到 openpyxl/xlrd
3. **CSV 编码错误**: 自动尝试 gbk 编码
4. **异常捕获**: 所有操作都在 try-except 块中

---

## 输出格式

```python
{
    "split_files": [
        "/path/to/output/file1.csv",
        "/path/to/output/file2.csv",
        ...
    ],
    "table_count": 3,
    "success": True,
    "output_dir": "/path/to/output"
}
```

---

## 使用示例

### 命令行:
```bash
python split_table_skill.py input.xlsx ./output
```

### Python:
```python
from skills import split_table
result = await split_table("input.xlsx", "./output")
```

---

## 总结

表格拆分 Skill 的核心逻辑：

1. **文件类型识别**: 自动判断 CSV 或 Excel
2. **多层回退**: Spire → openpyxl → xlrd
3. **空行分割**: 识别空行，切分为独立表格
4. **统一输出**: 所有结果保存为 CSV 格式
5. **错误处理**: 完善的异常捕获和回退机制
