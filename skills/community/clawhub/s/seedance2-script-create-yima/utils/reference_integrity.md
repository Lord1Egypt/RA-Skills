# 引用完整性检查工具

检查技能中所有引用链接的完整性和一致性的工具。

## 功能特性

- 引用链接验证
- 分类映射检查
- 脚本模板匹配
- 交叉引用验证

## 使用方法

### 检查整个技能

```bash
python reference_integrity.py --workspace . --check-all
```

### 检查特定引用

```bash
python reference_integrity.py --ref "@ref_electronics_mobile" --validate
```

### 生成引用图

```bash
python reference_integrity.py --graph references_graph.json
```

## 检查类型

### 引用存在性
- 验证所有 @ref_ 引用指向的文件存在
- 检查 @script_ 模板文件完整性
- 确认分类目录结构正确

### 映射一致性
- 验证产品类别与引用映射匹配
- 检查脚本模板与分类对应关系
- 确认时长和比例参数一致

### 交叉引用
- 检查模板中引用的分类文件存在
- 验证示例中使用的引用正确
- 确认合规检查引用完整

## 输出格式

完整性报告：

```json
{
  "overall_status": "healthy|warning|critical",
  "summary": {
    "total_references": 156,
    "valid_references": 152,
    "broken_references": 4,
    "missing_files": 2
  },
  "issues": [
    {
      "type": "broken_link",
      "reference": "@ref_unknown_category",
      "location": "SKILL.md:45",
      "suggestion": "创建 references/categories/unknown/ 目录"
    }
  ],
  "reference_graph": {
    "nodes": ["SKILL.md", "references/categories/...", "scripts/templates/..."],
    "edges": [
      {"from": "SKILL.md", "to": "@ref_electronics", "type": "category_ref"}
    ]
  }
}
```

## 自动修复

```bash
python reference_integrity.py --fix --backup
```

自动修复功能：
- 创建缺失的目录结构
- 修复错误的引用格式
- 更新过时的映射关系
- 生成缺失的基础文件

## 依赖项

- Python 3.8+
- networkx (用于引用图分析)
- graphviz (可选，用于可视化)

## 安装

```bash
pip install networkx
# 可选: pip install graphviz
```

## 示例

```python
from reference_integrity import ReferenceChecker

checker = ReferenceChecker()
report = checker.check_workspace('.')

print(f"状态: {report['overall_status']}")
print(f"有效引用: {report['summary']['valid_references']}/{report['summary']['total_references']}")

if report['issues']:
    print("发现问题:")
    for issue in report['issues']:
        print(f"- {issue['type']}: {issue['reference']}")
```