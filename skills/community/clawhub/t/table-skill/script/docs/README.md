# Table Preprocess Skills 代码逻辑文档索引

## 文档概览

本目录包含三个表格预处理 Skills 的详细代码逻辑文档，每个文档都深入分析了技能的核心流程、数据流、关键函数和依赖关系。

---

## 文档列表

### 1. [表格拆分 Skill](01_split_table_skill.md)

**文件路径**: `skills/split_table_skill.py`

**功能**: 将 Excel/CSV 文件按空行拆分为多个独立的表格文件

**核心内容**:
- ✅ CSV 文件拆分逻辑
- ✅ Excel 文件拆分（Spire 优先 + 回退方案）
- ✅ 空行识别与分割算法
- ✅ 多层回退机制：Spire → openpyxl → xlrd

**关键流程图**:
```
输入文件 → 文件类型判断 → CSV/Excel 拆分 → 保存为 CSV → 返回文件列表
```

**阅读建议**: 
- 想了解 Excel 拆分的多层回退机制
- 想理解空行分割的算法实现
- 需要处理包含多个表格的 Excel 文件

---

### 2. [表格清洗 Skill](02_clean_table_skill.md)

**文件路径**: `skills/clean_table_skill.py`

**功能**: 清洗表格数据，移除空白行列，处理复杂表头

**核心内容**:
- ✅ 空白行列移除算法
- ✅ 复杂表头检测与扁平化（使用 LLM）
- ✅ CSV 内存转换（处理重复列名、类型推断）
- ✅ LLM 服务回退机制

**关键流程图**:
```
输入 CSV → 移除空白行列 → 处理复杂表头 (可选) → CSV 内存转换 → 输出清洗后的 CSV
```

**阅读建议**:
- 想了解如何使用 LLM 检测表头行数
- 想理解多行表头的扁平化算法
- 需要清洗格式混乱的表格数据

---

### 3. [表格描述生成 Skill](03_describe_table_skill.md)

**文件路径**: `skills/describe_table_skill.py`

**功能**: 为表格生成详细的描述信息，包括列统计、摘要、样本数据等

**核心内容**:
- ✅ 列统计信息生成（数值/日期/分类）
- ✅ LLM 摘要生成
- ✅ 多样本展示（行样本、列样本、尾部样本）
- ✅ JSON 序列化兼容处理

**关键流程图**:
```
输入 CSV → 加载数据 → 生成列统计 → [可选]LLM 摘要 → 生成样本 → JSON 序列化 → 输出描述文件
```

**阅读建议**:
- 想了解如何生成列统计信息
- 想理解 LLM 摘要的 Prompt 设计
- 需要为表格生成元数据描述

---

## 共同特点

### 1. 代码复用

所有三个 Skills 都复用了 `.src/` 目录下的核心代码：

| Skill | 复用的核心函数 |
|-------|---------------|
| 拆分 | `split_workbook_all_sheets_return_worksheets()`, `split_sheet_by_blank_rows()`, `preprocess_excel()` |
| 清洗 | `remove_blank_rows_and_columns()`, `process_complex_header_table()`, `transfer_to_csv_in_memory()` |
| 描述 | `describe_single_table()`, `get_table_schema_origin()`, `get_table_abstract()` |

### 2. 错误处理

所有 Skills 都采用统一的错误处理模式：

```python
try:
    # 核心逻辑
    result = await process()
    return {
        "success": True,
        "output": result
    }
except Exception as e:
    return {
        "success": False,
        "error": str(e)
    }
```

### 3. LLM 服务回退

所有 Skills 都实现了 LLM 服务的回退机制：

```python
def get_llm_service():
    try:
        from table_recon.services.llm_service import get_llm_service as _get
        return _get()
    except ImportError:
        return _get_stub_llm_service()
```

### 4. 统一的输出格式

所有 Skills 都返回统一的字典格式：

```python
{
    "success": True/False,
    "error": "错误信息（如果失败）",
    "output_dir": "/path/to/output",
    ...
}
```

---

## 使用场景对比

| 场景 | 推荐 Skill | 输入 | 输出 |
|------|-----------|------|------|
| Excel 文件包含多个表格 | 拆分 | .xlsx/.xls | 多个 CSV 文件 |
| CSV 文件包含多个表格 | 拆分 | .csv | 多个 CSV 文件 |
| 表格有空白行列 | 清洗 | .csv | 清洗后的 CSV |
| 表格有多行表头 | 清洗 | .csv | 合并表头后的 CSV |
| 需要了解表格内容 | 描述 | .csv | JSON 描述文件 |
| 需要表格统计信息 | 描述 | .csv | JSON 描述文件 |

---

## 完整流程示例

如果需要完整的预处理流程，可以串联三个 Skills：

```python
from skills import split_table, clean_table, describe_table

async def full_pipeline():
    # 1. 拆分
    split_result = await split_table("data.xlsx", "./output")
    
    # 2. 清洗第一个拆分文件
    clean_result = await clean_table(
        split_result["split_files"][0],
        "./output",
        is_merge_header=True
    )
    
    # 3. 生成描述
    describe_result = await describe_table(
        clean_result["output_file"],
        "./output",
        is_abstract=True
    )
    
    return describe_result
```

---

## 文档结构说明

每个文档都包含以下部分：

1. **文件信息**: 文件路径、功能、输入输出
2. **整体架构图**: 类的结构和组件
3. **核心流程**: 主入口函数的详细流程
4. **关键函数详解**: 重要函数的实现逻辑
5. **数据流**: 完整的数据流转过程
6. **关键依赖**: 从 `.src` 导入的函数
7. **错误处理**: 异常捕获和回退机制
8. **输出格式**: 返回结果的格式
9. **使用示例**: 命令行和 Python 的使用方式
10. **总结**: 核心逻辑的简要概括

---

## 下一步

阅读完这些文档后，你可以：

1. ✅ 理解每个 Skill 的核心实现
2. ✅ 了解如何复用现有代码创建新 Skill
3. ✅ 根据需要修改或扩展现有 Skill
4. ✅ 将 Skills 集成到更大的系统中

---

## 相关文档

- **Skill 定义**: `skills/SKILL.md`
- **使用指南**: `skills/USAGE.md`
- **测试用例**: `skills/evals.json`
- **完整说明**: `../README_COMPLETE.md`
