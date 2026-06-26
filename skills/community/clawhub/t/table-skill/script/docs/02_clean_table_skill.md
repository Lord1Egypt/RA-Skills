# 表格清洗 Skill 代码逻辑文档

## 文件信息

- **文件路径**: `skills/clean_table_skill.py`
- **功能**: 清洗表格数据，移除空白行列，处理复杂表头
- **输入**: 单个 CSV 文件路径（仅支持 .csv 格式）
- **输出**: 清洗后的 CSV 文件

---

## 整体架构

```
┌─────────────────────────────────────────────────────────────┐
│                   CleanTableSkill                           │
├─────────────────────────────────────────────────────────────┤
│  __init__(is_merge_header, is_default_header)              │
│  run() - 主入口                                             │
│  ├── 参数验证                                                │
│  ├── 输出文件路径生成                                        │
│  ├── _load_file() - 加载 CSV                                │
│  ├── _clean_data() - 清洗数据                              │
│  │   ├── remove_blank_rows_and_columns()                   │
│  │   ├── process_complex_header_table() (可选)             │
│  │   └── transfer_to_csv_in_memory()                       │
│  └── 保存结果                                                │
└─────────────────────────────────────────────────────────────┘
```

---

## 核心流程

### 1. 初始化 `__init__()`

**位置**: L90-100

**功能**: 配置清洗参数

```python
def __init__(self, is_merge_header: bool = True, is_default_header: bool = False, remove_chars: List[str] = None):
    """初始化清洗技能。

    Args:
        is_merge_header: 是否合并多行表头
        is_default_header: 是否使用默认数字表头
        remove_chars: 需要移除的字符列表，如 [','] 移除千分位逗号
    """
    self.is_merge_header = is_merge_header
    self.is_default_header = is_default_header
    self.remove_chars = remove_chars or [',']
```

**参数说明**:
- `is_merge_header=True`: 启用复杂表头处理（使用 LLM 检测表头行数）
- `is_default_header=False`: 使用数据第一行作为表头
- `remove_chars=[',']`: 默认移除千分位逗号，也可移除其他字符如百分号

---

### 2. 主入口 `run()`

**位置**: L70-125

**流程图**:
```
输入
   ↓
1. 文件存在性检查
   └─ 不存在 → 返回 {"success": False, "error": "文件不存在"}
   ↓
2. 文件格式检查
   └─ 非 CSV 文件 → 返回 {"success": False, "error": "不支持的文件格式，仅支持 .csv 文件"}
   ↓
3. 设置输出目录
   └─ output_dir = dirname(input_file) (如果未指定)
   ↓
4. 生成输出文件路径
   └─ "{base_name}_cleaned.csv"
   ↓
5. 加载文件
   └─ df = await _load_file(input_file)
   ↓
6. 空数据检查
   └─ df.empty → 返回 {"success": False, "error": "数据为空"}
   ↓
7. 清洗数据
   └─ df = await _clean_data(df)
   ↓
8. 保存结果
   └─ df.to_csv(output_file, ...)
   ↓
9. 返回结果
   └─ {"success": True, "output_file": "...", "row_count": N, "col_count": M}
```

**核心代码**:
```python
async def run(self, input_file: str, output_dir: str = None) -> Dict[str, Any]:
    # 1. 文件检查
    if not os.path.exists(input_file):
        return {
            "output_file": "",
            "success": False,
            "error": f"文件不存在：{input_file}"
        }
    
    # 2. 设置输出目录
    if output_dir is None:
        output_dir = os.path.dirname(os.path.abspath(input_file))
    os.makedirs(output_dir, exist_ok=True)
    
    # 3. 生成输出路径
    base_name = os.path.splitext(os.path.basename(input_file))[0]
    output_file = os.path.join(output_dir, f"{base_name}_cleaned.csv")
    
    try:
        # 4. 加载文件
        df = await self._load_file(input_file)
        
        # 5. 空数据检查
        if df.empty:
            return {
                "output_file": "",
                "success": False,
                "error": "数据为空"
            }
        
        # 6. 清洗数据
        df = await self._clean_data(df)
        
        # 7. 保存结果
        df.to_csv(output_file, index=False, header=not self.is_default_header, encoding='utf-8')
        
        # 8. 返回结果
        return {
            "output_file": output_file,
            "success": True,
            "row_count": len(df),
            "col_count": len(df.columns),
            "output_dir": output_dir
        }
    except Exception as e:
        return {
            "output_file": "",
            "success": False,
            "error": str(e)
        }
```

---

### 3. 文件加载 `_load_file()`

**位置**: L127-139

**功能**: 加载 CSV 文件，支持编码回退

```python
async def _load_file(self, file_path: str) -> pd.DataFrame:
    try:
        return pd.read_csv(file_path, header=None)
    except:
        return pd.read_csv(file_path, encoding='gbk', header=None)
```

**说明**:
- 默认使用 utf-8 编码
- 失败时自动尝试 gbk 编码
- 不自动推断表头（header=None）

---

### 4. 数据清洗 `_clean_data()`

**位置**: L173-193

**流程图**:
```
输入 DataFrame
   ↓
1. remove_blank_rows_and_columns(df)
   ├─ 移除开头空白行
   ├─ 移除结尾空白行
   ├─ 移除开头空白列
   └─ 移除结尾空白列
   ↓
2. process_csv(df, remove_chars)
   ├─ 遍历每列的每个单元格
   ├─ 移除指定字符（如 ','、'%'）
   ├─ 检测百分比标志
   ├─ 尝试转换为整数
   ├─ 尝试转换为浮点数
   └─ 保留原始字符串（如果转换失败）
   ↓
3. [可选] process_complex_header_table(df)
   ├─ detect_header_row_new() ← LLM
   │   └─ 检测表头行数
   ├─ flattern_top_n_rows()
   │   └─ 扁平化多行表头
   └─ merge_top_rows_as_header()
       └─ 合并为单行表头
   ↓
4. transfer_to_csv_in_memory(df)
   ├─ df.to_csv() → StringIO
   ├─ StringIO.seek(0)
   └─ pd.read_csv(StringIO)
       ├─ 处理重复列名
       └─ 触发类型推断
   ↓
返回清洗后的 DataFrame
```

**核心代码**:
```python
async def _clean_data(self, df: pd.DataFrame) -> pd.DataFrame:
    # 1. 移除空白行列
    df = remove_blank_rows_and_columns(df)
    
    # 2. 移除指定字符（如千分位逗号）
    if self.remove_chars:
        df = process_csv(df, self.remove_chars)
    
    # 3. 处理复杂表头（如果启用）
    if self.is_merge_header and not df.empty:
        llm_service = get_llm_service()
        df = await process_complex_header_table(df, llm_service)
    
    # 4. CSV 内存转换
    if not df.empty:
        df = transfer_to_csv_in_memory(df, self.is_default_header)
    
    return df
```

---

## 关键函数详解

### 1. CSV 预处理函数 `process_csv()`

**位置**: `skills/src/split_region.py`

**功能**: 预处理 CSV DataFrame：移除指定字符并转换数值类型

**流程图**:
```
遍历每列
   ↓
遍历每个单元格
   ↓
1. 转换为字符串
   ↓
2. 检测并标记百分比
   └─ 如果字符以 '%' 结尾，设置 percentage_flag = True
   ↓
3. 移除指定字符
   └─ 遍历 remove_chars 列表，逐个替换为空
   ↓
4. 尝试类型转换
   ├─ 如果 percentage_flag:
   │   └─ 值 = 转换结果 / 100
   ├─ 尝试转换为整数
   │   └─ 成功 → 添加到结果
   ├─ 尝试转换为浮点数
   │   └─ 成功 → 添加到结果
   └─ 都失败 → 保留原始字符串
   ↓
返回处理后的 DataFrame
```

**核心代码**:
```python
def process_csv(df: pd.DataFrame, remove_chars: List[str]) -> pd.DataFrame:
    """预处理 CSV DataFrame：移除指定字符并转换数值类型。"""
    if df.empty:
        return df

    result_df = df.copy()

    for col in result_df.columns:
        col_values = []
        for cell in result_df[col]:
            if pd.isna(cell):
                col_values.append(cell)
                continue

            cell_str = str(cell).strip()
            percentage_flag = False

            for remove_char in remove_chars:
                if remove_char == '%' and cell_str.endswith('%'):
                    percentage_flag = True
                cell_str = cell_str.replace(remove_char, '')

            if percentage_flag:
                try:
                    col_values.append(float(cell_str) / 100)
                    continue
                except ValueError:
                    pass

            try:
                if '.' in cell_str:
                    col_values.append(float(cell_str))
                else:
                    col_values.append(int(cell_str))
            except ValueError:
                col_values.append(cell)

        result_df[col] = col_values

    return result_df
```

**使用示例**:
```python
# 输入数据
┌─────────────┬───────────┐
│   销售额    │   增长率   │
├─────────────┼───────────┤
│  1,000      │   5%      │
│  2,500      │   12%     │
│  1,800      │   8%      │

# 处理过程
remove_chars = [',']
# '1,000' → '1000' → 1000 (int)
# '5%' → '5' → 0.05 (float, 因为检测到%)

# 输出数据
┌─────────────┬───────────┐
│   销售额    │   增长率   │
├─────────────┼───────────┤
│  1000       │   0.05    │
│  2500       │   0.12    │
│  1800       │   0.08    │
```

---

### 2. LLM 服务获取

**位置**: L35-49

```python
def _get_stub_llm_service():
    """返回 stub LLM 服务用于没有真实 LLM 的情况。"""
    class StubLLMService:
        async def chat_async(self, system_prompt: str, user_prompt: str) -> str:
            return "{}"
    return StubLLMService()


def get_llm_service():
    """获取 LLM 服务，如果导入失败则返回 stub。"""
    try:
        from table_recon.services.llm_service import get_llm_service as _get
        return _get()
    except ImportError:
        return _get_stub_llm_service()
```

**说明**:
- 优先从 `table_recon.services.llm_service` 导入
- 导入失败时返回 stub 服务（返回空 JSON）
- 确保在无 LLM 环境下也能运行

---

### 2. 复杂表头处理流程

**调用链**:
```
process_complex_header_table(df, llm_service)
   ↓
merge_top_rows_as_header(df, llm_service)
   ↓
detect_header_row_new(df_head, llm_service)
   ├─ 准备前 10 行数据
   ├─ 构建 prompt
   ├─ 调用 LLM
   │   └─ 返回 {"header_row": N}
   └─ 解析响应，返回 header_rows_num
   ↓
flattern_top_n_rows(df_head, header_rows_num)
   ├─ 提取前 N 行
   ├─ 纵向填充空值
   ├─ 横向回溯填充
   ├─ 去重
   └─ 用'-'连接，生成新列名
   ↓
构建新 DataFrame
   ├─ 第一行：扁平化后的表头
   └─ 剩余行：原始数据
```

**示例**:
```python
# 输入（多行表头）
┌─────────┬─────────┬─────────┐
│  地区   │  销售   │  利润   │
│  省份   │  金额   │  率%    │
├─────────┼─────────┼─────────┤
│  广东   │  1000   │  20%    │
│  北京   │  800    │  15%    │

# 输出（单行表头）
┌─────────────┬───────────┬───────────┐
│ 地区 - 省份  │ 销售 - 金额 │ 利润 - 率% │
├─────────────┼───────────┼───────────┤
│  广东       │  1000     │  20%      │
│  北京       │  800      │  15%      │
```

---

### 3. CSV 内存转换

**位置**: 调用 `transfer_to_csv_in_memory()`

**功能**:
```python
def transfer_to_csv_in_memory(df: pd.DataFrame, is_default_header: bool = False) -> pd.DataFrame:
    # 1. 转为 CSV 字符串
    csv_buffer = StringIO()
    df.to_csv(csv_buffer, index=False, header=False, encoding='utf-8')
    csv_buffer.seek(0)
    
    # 2. 重新读取
    if not df.empty:
        if is_default_header:
            df = pd.read_csv(csv_buffer, on_bad_lines='warn', header=None)
        else:
            df = pd.read_csv(csv_buffer, on_bad_lines='warn')
    
    return df
```

**作用**:
1. **处理重复列名**: pandas 自动重命名为 `col1, col1.1, col1.2...`
2. **触发深度类型推断**: 从字符串重新推断数值、日期等类型
3. **标准化格式**: 统一编码和格式

---

## 数据流

```
输入 CSV 文件
   ↓
_load_file()
   ├─ 尝试 utf-8 编码
   └─ 失败 → gbk 编码
   ↓
pd.DataFrame (header=None)
   ↓
_clean_data()
   ├─ remove_blank_rows_and_columns()
   │   ├─ 查找首个非空行
   │   ├─ 查找最后一个非空行
   │   ├─ 查找首个非空列
   │   └─ 查找最后一个非空列
   │
   ├─ [可选] process_complex_header_table()
   │   ├─ LLM 检测表头行数
   │   ├─ 扁平化多行表头
   │   └─ 合并为单行表头
   │
   └─ transfer_to_csv_in_memory()
       ├─ to_csv() → StringIO
       └─ read_csv(StringIO)
   
↓
保存为 CSV
   └─ df.to_csv(output_file, index=False, header=not is_default_header)
   
↓
返回结果字典
```

---

## 关键依赖

### 从 `.src` 导入:

```python
from .src import (
    remove_blank_rows_and_columns,      # 移除空白行列
    process_complex_header_table,       # 处理复杂表头
    transfer_to_csv_in_memory,          # CSV 内存转换
    process_csv,                        # CSV 预处理（移除字符、类型转换）
    get_llm_service,                    # LLM 服务
)
```

### 外部库:

- `pandas`: DataFrame 操作
- `openai`: LLM 服务（可选）

---

## 错误处理

1. **文件不存在**: 返回 `{"success": False, "error": "文件不存在：{path}"}`
2. **文件格式错误**: 返回 `{"success": False, "error": "不支持的文件格式，仅支持 .csv 文件"}`
3. **数据为空**: 返回 `{"success": False, "error": "数据为空"}`
4. **编码错误**: 自动回退到 gbk 编码
5. **LLM 失败**: 使用 stub 服务（返回空响应）
6. **异常捕获**: 所有操作都在 try-except 块中

---

## 输出格式

```python
{
    "output_file": "/path/to/output/cleaned.csv",
    "success": True,
    "row_count": 100,
    "col_count": 10,
    "output_dir": "/path/to/output"
}
```

---

## 使用示例

### 命令行:
```bash
# 启用表头合并
python clean_table_skill.py input.csv ./output

# 不合并表头
python clean_table_skill.py input.csv ./output --no-merge-header
```

### Python:
```python
from skills import clean_table

# 启用表头合并
result = await clean_table("input.csv", "./output", is_merge_header=True)

# 不启用表头合并
result = await clean_table("input.csv", "./output", is_merge_header=False)
```

---

## 配置选项

| 参数 | 默认值 | 说明 |
|------|--------|------|
| `is_merge_header` | `True` | 是否合并多行表头 |
| `is_default_header` | `False` | 是否使用默认数字表头 |
| `remove_chars` | `[',']` | 需要移除的字符列表，默认移除千分位逗号 |

---

## 使用示例

### 命令行:
```bash
# 启用表头合并，默认移除逗号
python clean_table_skill.py input.csv ./output

# 不合并表头
python clean_table_skill.py input.csv ./output --no-merge-header

# 自定义移除字符（如移除逗号和百分号）
python clean_table_skill.py input.csv ./output --remove-chars ",%"

# 不移除任何字符
python clean_table_skill.py input.csv ./output --remove-chars ""
```

### Python:
```python
from skills import clean_table

# 启用表头合并，默认移除逗号
result = await clean_table("input.csv", "./output", is_merge_header=True)

# 不启用表头合并
result = await clean_table("input.csv", "./output", is_merge_header=False)

# 自定义移除字符
result = await clean_table("input.csv", "./output", remove_chars=[',', '%'])
```

---

## 总结

表格清洗 Skill 的核心逻辑：

1. **空白行列移除**: 移除首尾的空白行和列
2. **字符移除**: 移除指定字符（如千分位逗号、百分号）并转换数值类型
3. **复杂表头处理**: 使用 LLM 检测并扁平化多行表头
4. **CSV 内存转换**: 处理重复列名，触发类型推断
5. **编码回退**: utf-8 → gbk
6. **LLM 回退**: 真实 LLM → stub 服务
