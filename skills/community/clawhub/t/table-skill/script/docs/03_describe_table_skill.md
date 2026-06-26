# 表格描述生成 Skill 代码逻辑文档

## 文件信息

- **文件路径**: `skills/describe_table_skill.py`
- **功能**: 为表格生成详细的描述信息，包括列统计、摘要、样本数据等
- **输入**: 单个 CSV 文件路径（仅支持 .csv 格式）
- **输出**: JSON 格式的描述文件

---

## 整体架构

```
┌─────────────────────────────────────────────────────────────┐
│                 DescribeTableSkill                          │
├─────────────────────────────────────────────────────────────┤
│  __init__(is_abstract)                                     │
│  run() - 主入口                                             │
│  ├── 参数验证                                                │
│  ├── 输出文件路径生成                                        │
│  ├── _load_file() - 加载 CSV                                │
│  ├── describe_single_table() - 生成描述                    │
│  │   ├── get_table_schema_origin() - 列统计                │
│  │   ├── [可选] get_table_abstract() - LLM 摘要            │
│  │   ├── df_to_markdown() - Markdown 格式 (小表)          │
│  │   └── 生成行/列样本                                      │
│  ├── JSON 序列化                                            │
│  └── 保存结果                                                │
└─────────────────────────────────────────────────────────────┘
```

---

## 核心流程

### 1. 初始化 `__init__()`

**位置**: L38-44

**功能**: 配置描述生成参数

```python
def __init__(self, is_abstract: bool = True):
    """初始化描述生成技能。

    Args:
        is_abstract: 是否生成 LLM 摘要，默认为 True
    """
    self.is_abstract = is_abstract
```

**参数说明**:
- `is_abstract=True`: 默认启用 LLM 摘要生成（如果配置了 LLM）
- `is_abstract=False`: 禁用 LLM 摘要生成（节省时间和成本）

**注意**: 如果 LLM 未配置（没有设置 `OPENAI_API_KEY`），即使 `is_abstract=True` 也不会生成摘要，不会报错。

---

### 2. 主入口 `run()`

**位置**: L70-146

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
   └─ "{base_name}_description.json"
   ↓
5. 加载文件
   └─ df = await _load_file(input_file)
   ↓
6. 空数据检查
   └─ df.empty → 返回 {"success": False, "error": "数据为空"}
   ↓
7. 判断表大小
   └─ size_type = 'small' if rows*cols < 1500 else 'large'
   ↓
8. 生成描述
   └─ description = await describe_single_table(...)
   ↓
9. 添加元数据
   ├─ description['文件路径'] = input_file
   └─ description['表内容'] = base_name
   ↓
10. JSON 序列化
    └─ description_text = json.dumps(..., default=_default_dump)
    ↓
11. 保存到文件
    └─ with open(output_file, 'w') as f: f.write(description_text)
    ↓
12. 返回结果
    └─ {"description": {...}, "description_text": "...", "output_file": "..."}
```

**核心代码**:
```python
async def run(self, input_file: str, output_dir: str = None) -> Dict[str, Any]:
    # 1. 文件检查
    if not os.path.exists(input_file):
        return {
            "description": {},
            "description_text": "",
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
    output_file = os.path.join(output_dir, f"{base_name}_description.json")
    
    try:
        # 4. 加载文件
        df = await self._load_file(input_file)
        
        # 5. 空数据检查
        if df.empty:
            return {
                "description": {},
                "description_text": "",
                "output_file": "",
                "success": False,
                "error": "数据为空"
            }
        
        # 6. 判断表大小
        size_type = 'small' if len(df) * len(df.columns) < 1500 else 'large'
        llm_service = get_llm_service() if self.is_abstract else None
        
        # 7. 生成描述
        description = await describe_single_table(
            df=df,
            size_type=size_type,
            is_abstract=self.is_abstract,
            name=base_name,
            llm_service=llm_service
        )
        
        # 8. 添加元数据
        description['文件路径'] = input_file
        description['表内容'] = base_name
        
        # 9. JSON 序列化
        description_text = json.dumps(description, ensure_ascii=False, indent=2, default=self._default_dump)
        
        # 10. 保存文件
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(description_text)
        
        # 11. 返回结果
        return {
            "description": description,
            "description_text": description_text,
            "output_file": output_file,
            "success": True,
            "output_dir": output_dir
        }
    except Exception as e:
        return {
            "description": {},
            "description_text": "",
            "output_file": "",
            "success": False,
            "error": str(e)
        }
```

---

## 关键函数详解

### 1. 表格描述生成 `describe_single_table()`

**位置**: 调用 `script.utils.describe_single_table()`

**功能**: 生成完整的表格描述

**调用流程**:
```
describe_single_table(df, size_type, is_abstract, name, llm_service)
   ↓
1. 基础元数据
   ├─ '文件路径': ''
   ├─ '表内容': name
   ├─ 'size_type': size_type
   ├─ '数据行数': len(df)
   └─ '数据列名': list(df.columns)
   ↓
2. [小表] Markdown 上下文
   └─ if size_type == 'small': 'context' = df_to_markdown(df)
   ↓
3. 列模式生成
   └─ table_schema = await get_table_schema_origin(df)
       └─ description['列描述'] = table_schema
   ↓
4. [可选] LLM 摘要
   └─ if is_abstract and llm_service:
       └─ table_abstract = await get_table_abstract(table_schema, llm_service)
           └─ description['表描述'] = table_abstract
   ↓
5. 行样本（前 10 行）
   └─ rows_desc = [
       {"第 0 行": df.columns.to_list()},
       {"第 1 行": row1},
       ...
       {"第 9 行": row9}
   ]
   └─ description['这是前 10 行的数据展示'] = rows_desc
   ↓
6. 列样本（每列前 5 行）
   └─ columns_desc = [
       {"第 0 列": [col_name, val1, val2, val3, val4]},
       ...
   ]
   └─ description['这是每列前 5 行的数据展示'] = columns_desc
   ↓
7. 尾部样本（后 5 行）
   └─ tail_desc = [
       {"第 N-4 行": row},
       ...
       {"第 N 行": row}
   ]
   └─ description['这是末尾 5 行的数据展示'] = tail_desc
   ↓
返回 description 字典
```

---

### 2. 列统计信息生成 `get_table_schema_origin()`

**位置**: 调用 `script.utils.get_table_schema_origin()`

**功能**: 为每列生成统计信息

**算法**:
```python
async def get_table_schema_origin(df: pd.DataFrame) -> List[Dict[str, Any]]:
    table_schema = []
    
    for column in df.columns:
        col_type = df[column].dtypes
        type_set = set(df[column].apply(type))
        
        if len(type_set) == 1:
            # 数值类型
            if pd.api.types.is_numeric_dtype(col_type):
                example = {
                    "最小值": df[column].min(),
                    "最大值": df[column].max(),
                    "中位数": df[column].median(),
                    "平均值": df[column].mean()
                }
            
            # 日期时间类型
            elif pd.api.types.is_datetime64_any_dtype(col_type):
                example = {
                    "最早日期": df[column].min().strftime('%Y-%m-%d %H:%M:%S'),
                    "最晚日期": df[column].max().strftime('%Y-%m-%d %H:%M:%S')
                }
            
            # 对象类型
            elif pd.api.types.is_object_dtype(col_type):
                value_counts = df[column].value_counts()
                if len(value_counts) <= 15:
                    example = {"全部类别": value_counts.index.tolist()}
                else:
                    top_categories = value_counts.nlargest(6).index.tolist()
                    example = {
                        "类别示例": top_categories,
                        "总类别数量": len(value_counts),
                        "说明": "该列类型较多，展示前 6 个最常见的类型。"
                    }
        else:
            # 混合类型
            value_counts = df[column].value_counts()
            if len(value_counts) <= 15:
                example = {"全部类别": value_counts.index.tolist()}
            else:
                sampled_elements = sample_from_column(df, column, sample_size=10)
                example = {
                    "类别示例": sampled_elements,
                    "总类别数量": len(value_counts),
                    "说明": "该列类型较多，展示 10 个常见的类型。"
                }
        
        table_schema.append({
            "列名": column,
            "数据类型": str(col_type),
            "示例值": example
        })
    
    return table_schema
```

**输出示例**:
```json
{
  "列名": "年龄",
  "数据类型": "int64",
  "示例值": {
    "最小值": 18,
    "最大值": 65,
    "中位数": 35,
    "平均值": 37.5
  }
}
```

---

### 3. LLM 摘要生成 `get_table_abstract()`

**位置**: 调用 `script.utils.get_table_abstract()`

**功能**: 使用 LLM 生成表格自然语言摘要

**Prompt**:
```python
prompt = f"""请根据我提供的数据表列内容，对表格整体进行概述，生成表描述。
表描述解释了该表的主要内容，可能的用途。

*表格数据如下：*
-----------------------------
{table_schema_des}
-----------------------------

*返回样例：*
该表记录了某网站在一段时间内的访客数、浏览量、推广费用、订单数和销售金额等数据，
可用于分析网站的运营情况和营销效果。

注意仅返回表格描述，不输出任何中间解释结果。"""
```

**调用**:
```python
if llm_service:
    response = await llm_service.chat_async('你是一个表格内容总结专家。', prompt)
    return response
else:
    return ""
```

**输出示例**:
```
"该表记录了某地区 2023 年各季度的 GDP、人均收入、失业率等经济指标，可用于分析地区经济发展趋势。"
```

---

### 4. JSON 序列化兼容处理 `_default_dump()`

**位置**: L162-173

**功能**: 处理 numpy、pandas 类型的 JSON 序列化

```python
def _default_dump(self, obj):
    """JSON 序列化兼容处理。"""
    import numpy as np
    if isinstance(obj, (pd.Timestamp, pd.DatetimeTZDtype)):
        return str(obj)
    elif isinstance(obj, (np.integer, np.floating, np.bool_)):
        return obj.item()
    elif isinstance(obj, np.ndarray):
        return obj.tolist()
    elif isinstance(obj, pd.DataFrame):
        return obj.to_json()
    return str(obj)
```

**处理类型**:
- `pd.Timestamp` → 字符串
- `np.integer/np.floating/np.bool_` → Python 原生类型
- `np.ndarray` → Python list
- `pd.DataFrame` → JSON 字符串

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
判断表大小
   ├─ rows * cols < 1500 → 'small'
   └─ rows * cols >= 1500 → 'large'
   ↓
describe_single_table()
   ├─ 基础元数据
   │   ├─ 文件路径
   │   ├─ 表内容
   │   ├─ size_type
   │   ├─ 数据行数
   │   └─ 数据列名
   │
   ├─ [小表] Markdown 上下文
   │   └─ df_to_markdown(df)
   │
   ├─ 列统计信息
   │   └─ get_table_schema_origin(df)
   │       ├─ 数值列：min/max/median/mean
   │       ├─ 日期列：earliest/latest
   │       └─ 分类列：value_counts/top_n
   │
   ├─ [可选] LLM 摘要
   │   └─ get_table_abstract(table_schema, llm_service)
   │
   ├─ 行样本（前 10 行）
   │
   ├─ 列样本（每列前 5 行）
   │
   └─ 尾部样本（后 5 行）
   
↓
添加元数据
   ├─ description['文件路径'] = input_file
   └─ description['表内容'] = base_name
   
↓
JSON 序列化
   └─ json.dumps(..., default=_default_dump)
   
↓
保存到文件
   └─ {base_name}_description.json
   
↓
返回结果字典
```

---

## 关键依赖

### 从 `.src` 导入:

```python
from .src import (
    describe_single_table,        # 生成完整描述
    get_table_schema_origin,      # 生成列统计
    get_table_abstract,           # 生成 LLM 摘要
    df_to_markdown,               # 转为 Markdown 格式
)
```

### 外部库:

- `pandas`: DataFrame 操作
- `numpy`: 数值类型处理
- `json`: JSON 序列化
- `table_recon.services.llm_service`: LLM 服务（可选）

---

## 输出格式

### JSON 文件结构:

```json
{
  "文件路径": "/path/to/input.csv",
  "表内容": "input",
  "size_type": "small",
  "数据行数": 100,
  "数据列名": ["col1", "col2", "col3"],
  "context": "Markdown 格式的表格内容（仅小表）",
  "列描述": [
    {
      "列名": "col1",
      "数据类型": "int64",
      "示例值": {
        "最小值": 0,
        "最大值": 100,
        "中位数": 50,
        "平均值": 48.5
      }
    },
    ...
  ],
  "表描述": "LLM 生成的自然语言摘要（仅当 is_abstract=True）",
  "这是前 10 行的数据展示": [
    {"第 0 行": ["col1", "col2", "col3"]},
    {"第 1 行": [val1, val2, val3]},
    ...
  ],
  "这是每列前 5 行的数据展示": [
    {"第 0 列": ["col1", val1, val2, val3, val4, val5]},
    ...
  ],
  "这是末尾 5 行的数据展示": [
    {"第 96 行": [val1, val2, val3]},
    ...
  ]
}
```

### 返回字典:

```python
{
    "description": {...},  # 上述 JSON 字典
    "description_text": "...",  # JSON 字符串
    "output_file": "/path/to/output/input_description.json",
    "success": True,
    "output_dir": "/path/to/output"
}
```

---

## 错误处理

1. **文件不存在**: 返回 `{"success": False, "error": "文件不存在：{path}"}`
2. **文件格式错误**: 返回 `{"success": False, "error": "不支持的文件格式，仅支持 .csv 文件"}`
3. **数据为空**: 返回 `{"success": False, "error": "数据为空"}`
4. **编码错误**: 自动回退到 gbk 编码
5. **LLM 失败**: 使用 stub 服务（返回空字符串）
6. **JSON 序列化失败**: 使用 `_default_dump()` 处理特殊类型
7. **异常捕获**: 所有操作都在 try-except 块中

---

## 使用示例

### 命令行:
```bash
# 默认启用 LLM 摘要（如果配置了 LLM）
python describe_table_skill.py input.csv ./output

# 禁用 LLM 摘要生成
python describe_table_skill.py input.csv ./output --no-abstract
```

### Python:
```python
from skills import describe_table

# 默认启用 LLM 摘要（如果配置了 LLM）
result = await describe_table("input.csv", "./output")

# 禁用 LLM 摘要生成
result = await describe_table("input.csv", "./output", is_abstract=False)

# 访问结果
print(f"表名：{result['description']['表内容']}")
print(f"行数：{result['description']['数据行数']}")
print(f"列数：{len(result['description']['数据列名'])}")
```

---

## 配置选项

| 参数 | 默认值 | 说明 |
|------|--------|------|
| `is_abstract` | `True` | 是否生成 LLM 摘要（如果配置了 LLM） |

---

## 表大小判断

```python
size_type = 'small' if len(df) * len(df.columns) < 1500 else 'large'
```

**影响**:
- `small`: 添加 Markdown 格式的完整表格内容
- `large`: 仅添加统计信息和样本数据

---

## 总结

表格描述生成 Skill 的核心逻辑：

1. **基础元数据**: 文件路径、表名、行数、列名
2. **列统计信息**: 数值列的 min/max/median/mean，分类列的 value_counts
3. **LLM 摘要**: 可选的自然语言表格概述
4. **多样本展示**: 前 10 行、每列前 5 行、末尾 5 行
5. **JSON 兼容**: 处理 numpy/pandas 特殊类型
6. **表大小判断**: 小表添加 Markdown 全文
