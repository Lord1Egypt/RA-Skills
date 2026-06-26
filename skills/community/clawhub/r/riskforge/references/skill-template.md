---
name: skill-template
description: 基于.md描述的标准skill模板，使用大模型进行代码风险分析
triggers:
  - 风险分析
  - 代码质量
  - 静态分析
role: analyzer
scope: code-analysis
output-format: json
---

# 标准Skill模板

这是一个基于.md描述的标准skill模板，使用大模型进行代码风险分析，替代传统的静态代码分析逻辑。

## Skill定义

### 基本信息
- **名称**: {skill-name}
- **描述**: {skill-description}
- **风险类型**: {risk-type}
- **支持语言**: {supported-languages}

### 检测规则
{detection-rules}

### 风险等级定义
- **高风险**: {high-risk-definition}
- **中风险**: {medium-risk-definition}
- **低风险**: {low-risk-definition}

## 分析方法

### 分析步骤
1. **代码理解**: 理解代码变更的内容和上下文
2. **规则匹配**: 根据上述规则检测潜在风险
3. **风险评估**: 评估风险的严重程度和影响范围
4. **建议生成**: 提供具体的修复建议和测试用例

### 输出格式
```json
{
  "type": "风险类型",
  "module": "具体模块",
  "file": "文件路径",
  "line": 行号,
  "description": "风险描述",
  "codeSnippet": "相关代码片段",
  "suggestion": "修复建议",
  "testCases": ["测试用例1", "测试用例2"],
  "level": "high|medium|low"
}
```

## 使用说明

### 触发条件
- 当检测到{trigger-conditions}时触发分析

### 配置参数
- **语言支持**: {language-support}
- **文件过滤**: {file-filters}
- **忽略规则**: {ignore-patterns}

### 集成方式
此skill通过RiskForge CLI框架自动加载，执行分析时会使用大模型进行智能分析。

## 注意事项
1. 分析结果依赖于大模型的理解能力
2. 对于复杂的代码逻辑，可能需要人工复核
3. 建议结合其他skill进行综合分析