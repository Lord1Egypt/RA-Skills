# 表头合并 Skill 代码逻辑文档

## 文件信息

- **文件路径**: `skills/merge_header_skill.py`
- **功能**: 使用 LLM 智能检测并合并多行表头，将复杂表头扁平化为单行表头
- **输入**: 单个 CSV 文件路径（仅支持 .csv 格式）
- **输出**: 合并表头后的 CSV 文件

---

## 整体架构

```
┌─────────────────────────────────────────────────────────────┐
│                   MergeHeaderSkill                          │
├─────────────────────────────────────────────────────────────┤
│  __init__()                                                 │
│  run() - 主入口                                             │
│  ├── 参数验证                                                │
│  ├── 输出文件路径生成                                        │
│  ├── _load_file() - 加载 CSV                                │
│  ├── _merge_header() - 合并表头                             │
│  │   ├── remove_blank_rows_and_columns()                   │
│  │   └── process_complex_header_table()                        │
│  │       ├── detect_header_row_new() ← LLM                │
│  │       └── flattern_top_n_rows()                         │
│  └── 保存结果                                                │
└─────────────────────────────────────────────────────────────┘
```

---

## 核心流程

### 1. 初始化 `__init__()`

**位置**: L43-45

**功能**: 初始化表头合并技能

```python
def __init__(self):
    """初始化表头合并技能。"""
    pass
```

**说明**:
- 当前版本无需配置参数
- 所有表头处理参数由 LLM 自动判断

---

### 2. 主入口 `run()`

**位置**: L47-103

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
   └─ "{base_name}_merged_header.csv"
   ↓
5. 加载文件
   └─ df = await _load_file(input_file)
   ↓
6. 空数据检查
   └─ df.empty → 返回 {"success": False, "error": "数据为空"}
   ↓
7. 合并表头
   └─ df, header_rows = await _merge_header(df)
   ↓
8. 保存结果
   └─ df.to_csv(output_file, ...)
   ↓
9. 返回结果
   └─ {
        "success": True,
        "output_file": "...",
        "row_count": N,
        "col_count": M,
        "header_rows_detected": K
      }
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
    output_file = os.path.join(output_dir, f"{base_name}_merged_header.csv")
    
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
        
        # 6. 合并表头
        df, header_rows = await self._merge_header(df)
        
        # 7. 保存结果
        df.to_csv(output_file, index=False, encoding='utf-8')
        
        # 8. 返回结果
        return {
            "output_file": output_file,
            "success": True,
            "row_count": len(df),
            "col_count": len(df.columns),
            "header_rows_detected": header_rows
        }
    except Exception as e:
        return {
            "output_file": "",
            "success": False,
            "error": str(e)
        }
```

**关键点**:
- ✅ 自动创建输出目录
- ✅ 统一的错误处理
- ✅ 返回检测到的表头行数
- ✅ 输出文件命名：`{原文件名}_merged_header.csv`

---

### 3. 文件加载 `_load_file()`

**位置**: L105-117

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

### 4. 表头合并 `_merge_header()`

**位置**: L119-140

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
2. 空数据检查
   └─ df.empty → 返回 (df, 0)
   ↓
3. 获取 LLM 服务
   └─ llm_service = get_llm_service()
   ↓
4. process_complex_header_table(df, llm_service)
   ├─ df_head = df.head(10)
   ├─ header_rows_num = await detect_header_row_new(df_head, llm_service)
   │   ├─ 构建前 10 行数据描述
   │   ├─ 调用 LLM 判断表头行数
   │   └─ 解析 LLM 返回的 JSON
   │
   ├─ if header_rows_num == 1:
   │   └─ df_new = df (无需合并)
   │
   └─ else:
       ├─ flattened_header = flattern_top_n_rows(df_head, header_rows_num)
       │   ├─ 提取前 header_rows_num 行
       │   ├─ 纵向填充空值（向下填充）
       │   ├─ 横向回溯填充（向左填充）
       │   ├─ 去除重复值
       │   └─ 用'-'连接，生成新列名
       │
       ├─ header_df = pd.DataFrame([flattened_header])
       ├─ df.columns = range(len(df.columns))
       └─ df_new = pd.concat([header_df, df[header_rows_num:]], ignore_index=True)
   
   ↓
5. 计算表头行数
   └─ header_rows = len(df) - len(df_merged) + 1
   ↓
6. 返回
   └─ (df_merged, header_rows)
```

**核心代码**:
```python
async def _merge_header(self, df: pd.DataFrame) -> tuple:
    """合并多行表头。
    
    Args:
        df: 输入 DataFrame
    
    Returns:
        (合并后的 DataFrame, 检测到的表头行数)
    """
    df = remove_blank_rows_and_columns(df)
    
    if df.empty:
        return df, 0
    
    llm_service = get_llm_service()
    df_merged = await process_complex_header_table(df, llm_service)
    
    header_rows = len(df) - len(df_merged) + 1
    if header_rows < 1:
        header_rows = 1
    
    return df_merged, header_rows
```

---

## 关键函数详解

### 1. LLM 表头检测

**调用链**:
```
detect_header_row_new(df_head, llm_service)
   ↓
1. 准备数据
   └─ 格式化前 10 行数据为字符串
   ↓
2. 构建 Prompt
   ├─ 表头特征说明
   ├─ 对比分析要求
   ├─ 疑惑提醒规则
   └─ 输出格式要求 (JSON)
   ↓
3. 调用 LLM
   └─ response = await llm_service.chat_async('', prompt)
   ↓
4. 解析响应
   ├─ 提取 JSON 字符串
   ├─ 解析 header_row 字段
   └─ 返回表头行数
```

**Prompt 示例**:
```python
prompt = f'''你是一个表格数据处理专家，需要根据表格的前 10 行内容，智能判断前几行是表头（标题行）。
请遵循以下规则：
1. **表头特征**：表头通常包含列名、字段描述或汇总信息（如"姓名""年龄""总计"等），而非具体数据；即使这些行看起来像是分类说明、标题、或内容重复，也要判定为表头。
2. **对比分析**：检查前几行与后续行的内容差异，表头行通常与其他行格式或语义不同。
3. **疑惑提醒**：即使这些行看起来像是分类说明、标题、或内容重复，也要判定为表头；表头上边的几行一定是表头。
4. **输出格式**：返回一个 JSON 对象，表头到第几行 "header_row"。

输出示例：
{{"header_row": 2}}

请分析以下表格前 10 行：

{data_str}

先输出你的解释，再最终输出类似{{"header_row": 2}} 。'''
```

**LLM 返回示例**:
```json
{"header_row": 3}
```

---

### 2. 表头扁平化

**函数**: `flattern_top_n_rows(df_head, header_rows_num)`

**位置**: `skills/src/table_cleaning.py:L125-181`

**流程图**:
```
输入：前 N 行表头数据
   ↓
1. 提取列头
   └─ column_headers = [
        [第 1 列的 N 个单元格],
        [第 2 列的 N 个单元格],
        ...
      ]
   ↓
2. 清理字符
   └─ 移除空格、换行符、回车符
   ↓
3. 纵向填充（向下填充）
   ├─ 遍历每一列
   ├─ 如果当前单元格为空：
   │   ├─ 如果上方有非空值 → 使用上方的值
   │   └─ 否则向左回溯查找
   └─ 如果当前单元格非空 → 更新 cur_cell
   ↓
4. 横向回溯填充
   └─ 如果当前单元格为空且上方为空：
       └─ 向左查找最近的非空单元格
   ↓
5. 去除重复值
   └─ 只保留连续重复值中的第一个
   ↓
6. 扁平化
   └─ 用'-'连接所有非空值
   ↓
返回：['列 1-子列 1', '列 2-子列 2', ...]
```

**示例**:
```python
# 输入（3 行表头）
┌─────────────┬─────────────┬─────────────┬─────────────┐
│    地区     │    销售     │    销售     │    利润     │
├─────────────┼─────────────┴─────────────┼─────────────┤
│    省份     │    移动     │    宽带     │    率%      │
├─────────────┼─────────────┼─────────────┼─────────────┤
│    广东     │    1000     │    500      │    20%      │
│    北京     │    800      │    400      │    15%      │

# 扁平化过程
第 1 列：['地区', '省份'] → '地区 - 省份'
第 2 列：['销售', '移动'] → '销售 - 移动'
第 3 列：['销售', '宽带'] → '销售 - 宽带'
第 4 列：['利润', '率%'] → '利润 - 率%'

# 输出（单行表头）
┌─────────────┬─────────────┬─────────────┬─────────────┐
│ 地区 - 省份  │ 销售 - 移动  │ 销售 - 宽带  │ 利润 - 率%  │
├─────────────┼─────────────┼─────────────┼─────────────┤
│    广东     │    1000     │    500      │    20%      │
│    北京     │    800      │    400      │    15%      │
```

**核心代码**:
```python
def flattern_top_n_rows(df_head: pd.DataFrame, header_rows_num: int) -> List[str]:
    # 1. 提取列头
    column_headers = [
        df_head.iloc[list(range(header_rows_num)), i].tolist()
        for i in range(len(df_head.columns))
    ]
    
    # 2. 清理字符
    column_headers = [
        [item.replace(' ', '').replace('\n', '').replace('\r', '')
         if isinstance(item, str) else item for item in column]
        for column in column_headers
    ]
    
    # 3. 纵向填充 + 横向回溯
    new_column_headers = []
    for ix_col, col_header in enumerate(column_headers):
        new_col_header = []
        cur_cell = ''
        
        for ix_row, cell in enumerate(col_header):
            if pd.isna(cell):
                if cur_cell != '':
                    col_header[ix_row] = cur_cell
                else:
                    # 向左回溯
                    ix_col_tmp = ix_col - 1
                    while ix_col_tmp >= 0:
                        if not pd.isna(column_headers[ix_col_tmp][ix_row]):
                            col_header[ix_row] = column_headers[ix_col_tmp][ix_row]
                            new_col_header.append(column_headers[ix_col_tmp][ix_row])
                            break
                        ix_col_tmp -= 1
            else:
                cur_cell = cell
                new_col_header.append(cell)
        
        # 4. 去除重复值
        new_col_header_no_repeat = [
            new_col_header[i]
            for i in range(len(new_col_header))
            if i == 0 or new_col_header[i] != new_col_header[i-1]
        ]
        new_column_headers.append(new_col_header_no_repeat)
    
    # 5. 扁平化
    flattened_header = [
        '-'.join([str(i).strip() for i in item if str(i).strip()])
        for item in new_column_headers
    ]
    
    return flattened_header
```

---

### 3. LLM 服务获取

**函数**: `get_llm_service()`

**位置**: `skills/src/llm_service.py:L55-81`

**功能**: 获取 LLM 服务，支持多级回退

```python
def get_llm_service(use_openai: bool = True) -> object:
    """获取 LLM 服务。
    
    Args:
        use_openai: 是否尝试使用 OpenAI 服务
    
    Returns:
        LLM 服务对象（OpenAILLMService 或 StubLLMService）
    """
    if not use_openai:
        return _get_stub_llm_service()
    
    # 1. 优先尝试项目原有的 LLM 服务
    try:
        from table_recon.services.llm_service import get_llm_service as _get
        return _get()
    except ImportError:
        pass
    
    # 2. 其次尝试 OpenAI 服务
    try:
        return OpenAILLMService()
    except Exception:
        pass
    
    # 3. 最后降级到 Stub 服务
    return _get_stub_llm_service()
```

**回退策略**:
1. **项目 LLM 服务** → `table_recon.services.llm_service`
2. **OpenAI 服务** → 需要 `OPENAI_API_KEY` 环境变量
3. **Stub 服务** → 返回空 JSON `{}`（用于无 LLM 环境）

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
_merge_header()
   ├─ remove_blank_rows_and_columns()
   │   ├─ 查找首个非空行
   │   ├─ 查找最后一个非空行
   │   ├─ 查找首个非空列
   │   └─ 查找最后一个非空列
   │
   └─ process_complex_header_table()
       ├─ df_head = df.head(10)
       ├─ detect_header_row_new(df_head, llm_service)
       │   ├─ 格式化前 10 行数据
       │   ├─ 构建 LLM Prompt
       │   ├─ 调用 LLM
       │   └─ 解析 JSON 响应
       │
       ├─ if header_rows_num == 1:
       │   └─ 无需合并，返回原表
       │
       └─ else:
           ├─ flattern_top_n_rows(df_head, header_rows_num)
           │   ├─ 提取前 N 行
           │   ├─ 纵向填充空值
           │   ├─ 横向回溯填充
           │   ├─ 去除重复值
           │   └─ 用'-'连接
           │
           ├─ 构建新表头 DataFrame
           ├─ 合并表头和数据
           └─ 返回新 DataFrame
   
↓
保存为 CSV
   └─ df.to_csv(output_file, index=False, encoding='utf-8')
   
↓
返回结果字典
   └─ {
        "output_file": "...",
        "success": True,
        "row_count": N,
        "col_count": M,
        "header_rows_detected": K
      }
```

---

## 关键依赖

### 从 `.src` 导入:

```python
from .src import (
    remove_blank_rows_and_columns,      # 移除空白行列
    process_complex_header_table,           # 合并多行表头
    get_llm_service,                    # 获取 LLM 服务
)
```

### 底层依赖（`.src/table_cleaning.py`）:

```python
# 被 process_complex_header_table() 调用
- detect_header_row_new()              # LLM 检测表头行数
- flattern_top_n_rows()                # 扁平化多行表头
```

### 外部库:

- `pandas`: DataFrame 操作
- `.src.llm_service`: LLM 服务（支持多级回退）

---

## 错误处理

1. **文件不存在**: 返回 `{"success": False, "error": "文件不存在：{path}"}`
2. **文件格式错误**: 返回 `{"success": False, "error": "不支持的文件格式，仅支持 .csv 文件"}`
3. **数据为空**: 返回 `{"success": False, "error": "数据为空"}`
4. **编码错误**: 自动回退到 gbk 编码
5. **LLM 失败**: 
   - 使用 stub 服务（返回空 JSON）
   - 表头检测失败时默认返回 1 行表头
6. **JSON 解析失败**: 捕获异常，默认返回 1 行表头
7. **异常捕获**: 所有操作都在 try-except 块中

---

## 输出格式

```python
{
    "output_file": "/path/to/output/file_merged_header.csv",
    "success": True,
    "row_count": 100,
    "col_count": 10,
    "header_rows_detected": 3
}
```

**字段说明**:
- `output_file`: 合并表头后的 CSV 文件路径
- `success`: 是否成功
- `row_count`: 合并后的行数
- `col_count`: 合并后的列数
- `header_rows_detected`: LLM 检测到的表头行数

---

## 使用示例

### 命令行:

```bash
# 基本用法
python merge_header_skill.py input.csv ./output

# 输出到当前目录
python merge_header_skill.py input.csv
```

### Python:

```python
from skills.merge_header_skill import MergeHeaderSkill

# 创建技能实例
skill = MergeHeaderSkill()

# 执行表头合并
result = await skill.run("input.csv", "./output")

# 检查结果
if result["success"]:
    print(f"合并成功！")
    print(f"行数：{result['row_count']}")
    print(f"列数：{result['col_count']}")
    print(f"检测到表头行数：{result['header_rows_detected']}")
    print(f"输出文件：{result['output_file']}")
else:
    print(f"合并失败：{result['error']}")
```

### 作为独立函数调用:

```python
from skills.merge_header_skill import run_skill

result = await run_skill("input.csv", "./output")
```

---

## 配置选项

当前版本为简化版本，无需配置参数。

未来可能添加的配置：
- `llm_model`: 指定 LLM 模型
- `skip_llm`: 跳过 LLM 检测，使用固定行数
- `header_rows`: 手动指定表头行数

---

## 与 clean_table_skill 的对比

| 特性 | merge_header_skill | clean_table_skill |
|------|-------------------|-------------------|
| **功能** | 专注于表头合并 | 综合清洗（移除空白行列、字符处理、表头合并） |
| **表头处理** | 核心功能，必选 | 可选功能（通过 `is_merge_header` 控制） |
| **字符处理** | ❌ 不支持 | ✅ 支持（通过 `remove_chars`） |
| **输出命名** | `{name}_merged_header.csv` | `{name}_cleaned.csv` |
| **返回值** | 包含 `header_rows_detected` | 包含 `row_count`, `col_count` |
| **使用场景** | 仅需表头合并 | 完整表格清洗 |

---

## 总结

表头合并 Skill 的核心逻辑：

1. **空白行列移除**: 移除首尾的空白行和列，确保数据整洁
2. **LLM 表头检测**: 使用 LLM 智能判断表头行数（分析前 10 行）
3. **表头扁平化**: 
   - 纵向填充空值（向下填充）
   - 横向回溯填充（向左填充）
   - 去除重复值
   - 用'-'连接生成单行表头
4. **多级回退**: 
   - LLM 服务：项目服务 → OpenAI → Stub
   - 编码：utf-8 → gbk
5. **独立运行**: 可作为独立 skill 或命令行工具使用
6. **详细反馈**: 返回检测到的表头行数，便于调试和验证
