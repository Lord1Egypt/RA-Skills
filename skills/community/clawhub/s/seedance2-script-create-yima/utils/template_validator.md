# 广告模板验证工具

用于验证广告模板的完整性和正确性的工具。

## 功能特性

- 模板结构验证
- 引用完整性检查
- 脚本语法验证
- 合规标注检查

## 使用方法

### 验证单个模板

```bash
python template_validator.py --template references/scripts/templates/elec_15s_v1.md
```

### 批量验证

```bash
python template_validator.py --dir references/scripts/templates/ --report validation_report.json
```

### 参数说明

- `--template`: 指定要验证的模板文件
- `--dir`: 指定模板目录进行批量验证
- `--report`: 输出验证报告文件
- `--fix`: 自动修复发现的问题

## 验证规则

### 结构检查
- YAML格式正确性
- 必需字段完整性
- 字段类型验证

### 引用检查
- @ref_ 引用是否存在
- @script_ 引用是否匹配
- 分类映射正确性

### 脚本验证
- 时间轴连续性
- 音效标注完整性
- 合规标注存在性

### 内容检查
- 违禁词过滤
- 长度限制验证
- 格式规范检查

## 输出格式

验证报告包含：

```json
{
  "template_file": "elec_15s_v1.md",
  "validation_status": "passed|failed|warning",
  "issues": [
    {
      "type": "error|warning",
      "field": "字段名",
      "message": "问题描述",
      "line": 15
    }
  ],
  "statistics": {
    "total_fields": 25,
    "valid_fields": 23,
    "invalid_fields": 2,
    "missing_fields": 0
  }
}
```

## 自动修复

启用 `--fix` 参数时，工具会自动：

- 修复YAML格式问题
- 补充缺失的合规标注
- 修正引用格式
- 标准化字段命名

## 依赖项

- Python 3.8+
- PyYAML
- jsonschema

## 安装

```bash
pip install PyYAML jsonschema
```

## 示例

```python
from template_validator import TemplateValidator

validator = TemplateValidator()
result = validator.validate('references/scripts/templates/elec_15s_v1.md')

if not result['passed']:
    print("发现问题:")
    for issue in result['issues']:
        print(f"- {issue['message']}")
```