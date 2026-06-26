# Smart Task Generator 重构总结

## 问题描述

原始的 `smart_task_generator.py` 存在硬编码问题：
- 硬编码了 PDF 相关的测试文件字典
- 默认 fallback 总是使用 `test.pdf output.pdf`
- 没有根据目标 SKILL.md 的实际内容来推断文件类型

这导致无论目标 skill 是什么类型，都倾向于生成 PDF 测试用例。

## 重构方案

### 1. 添加智能分析功能

在 `__init__` 中添加了三个新属性：
```python
self.inferred_file_types = []        # 从 SKILL.md 推断的文件类型
self.inferred_input_patterns = []    # 输入文件模式
self.inferred_output_patterns = []   # 输出文件模式
```

### 2. 新增 `_analyze_skill_file_patterns()` 方法

该方法在加载 SKILL.md 后自动分析：

**Pattern 1: 从代码示例中提取文件扩展名**
- 使用正则表达式匹配 `.pdf`, `.txt`, `.json`, `.png` 等

**Pattern 2: 从技能描述推断领域关键词**
- 例如：描述中包含 "image" → 推断 `.png`, `.jpg`
- 描述中包含 "log" → 推断 `.log`, `.txt`
- 描述中包含 "pdf" → 推断 `.pdf`

**Pattern 3: 提取实际文件名示例**
- 从命令示例中提取 `input.png`, `output.json` 等
- 区分输入和输出文件模式

**Pattern 4: 分析命令参数**
- 从已提取的命令中分析文件类型

### 3. 重构 `_generate_realistic_command()` 方法

完全移除硬编码的 `test_files` 字典，改为：

1. **读取脚本内容**：分析 `sys.argv` 和 `argparse` 使用情况
2. **智能参数推断**：调用 `_infer_test_value_for_param()` 根据参数名推断值
3. **使用分析结果**：优先使用从 SKILL.md 推断的文件类型
4. **智能 fallback**：只在无法推断时才使用通用的 `.txt` 而非 `.pdf`

### 4. 新增辅助方法

- `_infer_test_value_for_param()`: 根据参数名推断测试值
- `_get_default_input_file()`: 获取默认输入文件（基于推断的文件类型）
- `_get_default_output_file()`: 获取默认输出文件
- `_get_default_data_file()`: 获取默认数据文件（优先 JSON/YAML）
- `_get_default_config_file()`: 获取默认配置文件

## 测试结果

### 测试 1: skills-coach (非 PDF skill)
```
Inferred File Types: ['json', 'md', 'py', 'yaml']
✓ 正确识别为代码/配置相关的 skill
```

### 测试 2: image-processor (图片处理)
```
Inferred File Types: ['jpg', 'png', 'webp']
Generated: python3 /tmp/test_skill/scripts/process.py input.jpg output.jpg
✓ 正确使用图片文件类型，没有默认到 PDF
```

### 测试 3: log-analyzer (日志分析)
```
Inferred File Types: ['log', 'txt']
Generated: python3 /tmp/test_log_skill/scripts/analyze.py input.log output.log
✓ 正确使用日志文件类型
```

### 测试 4: data-processor (通用数据处理)
```
Inferred File Types: ['csv', 'json', 'pdf', 'py']
Generated: python3 /tmp/test_generic_skill/scripts/process.py input.csv output.csv
✓ 从描述中推断出数据相关类型，优先使用 CSV
```

## 改进效果

1. **智能化**：根据 SKILL.md 内容自动推断文件类型
2. **准确性**：不再盲目使用 PDF，而是使用与 skill 功能匹配的文件类型
3. **可扩展性**：新增的分析逻辑可以识别更多文件类型和模式
4. **可维护性**：移除硬编码，逻辑更清晰

## 向后兼容性

- 保持了原有的 API 接口不变
- 对于 PDF 相关的 skill，仍然会正确推断并使用 PDF 文件
- 只是移除了对所有 skill 都默认使用 PDF 的问题
