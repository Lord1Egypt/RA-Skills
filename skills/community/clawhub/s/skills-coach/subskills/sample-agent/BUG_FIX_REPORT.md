# Bug Fix Report - 数字扩展名过滤

## 问题描述

在对 stock-analysis skill 运行 skills-coach 时，发现生成的测试任务包含错误的参数：

```bash
uv run .../analyze_stock.py AAPL --fast input.5 output.5
```

其中 `input.5` 和 `output.5` 是错误的文件名，因为 `.5` 不是有效的文件扩展名。

## 根本原因

在 `_analyze_skill_file_patterns()` 方法中，文件类型推断逻辑提取了：

```
Inferred file types: 5, csv, json, py
```

数字 "5" 被错误地识别为文件扩展名。这是因为：

1. stock-analysis 的 SKILL.md 包含版本号如 `v6.2.0`、`v6.1`、`v6.0`
2. 正则表达式 `\b\w+\.(pdf|txt|json|...)\b` 匹配了 `v6.5` 中的 `.5`
3. 没有过滤纯数字的扩展名

## 修复方案

在三个地方添加了数字过滤：

### 1. Pattern 1 - 扩展名提取
```python
# 修复前
file_extensions.update(ext.lower() for ext in extensions_found)

# 修复后
file_extensions.update(ext.lower() for ext in extensions_found if not ext.isdigit())
```

### 2. Pattern 3 - 文件名提取
```python
# 修复前
for filename, ext in filenames_found:
    file_extensions.add(ext.lower())

# 修复后
for filename, ext in filenames_found:
    if not ext.isdigit():
        file_extensions.add(ext.lower())
```

### 3. Pattern 4 - 命令参数分析
```python
# 修复前
if len(ext) <= 5 and ext.isalnum():
    file_extensions.add(ext)

# 修复后
if len(ext) >= 2 and len(ext) <= 5 and ext.isalpha():
    file_extensions.add(ext)
```

关键改进：
- `ext.isdigit()` - 过滤纯数字扩展名
- `ext.isalpha()` - 只接受纯字母扩展名
- `len(ext) >= 2` - 确保至少2个字符

## 验证结果

修复后测试 stock-analysis：

```
✓ Inferred file types: csv, json, py
✓ Correctly filtered out numeric extensions
```

不再包含 "5"，生成的测试命令将使用正确的文件类型：
- `input.csv` / `output.csv`
- `input.json` / `output.json`
- 而不是 `input.5` / `output.5`

## 影响范围

这个修复确保了：
1. 版本号不会被误识别为文件类型
2. 只有有效的文件扩展名会被使用
3. 生成的测试任务参数更加合理

## 相关文件

- `/Users/ranwalker/.openclaw/skills/skills-coach/subskills/sample-agent/smart_task_generator.py`
  - Line ~137: Pattern 1 修复
  - Line ~157: Pattern 3 修复
  - Line ~177: Pattern 4 修复
