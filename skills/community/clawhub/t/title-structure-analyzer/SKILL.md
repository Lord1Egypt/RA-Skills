---
name: title-structure-analyzer
description: |
  分析学术论文标题的结构类型，判断是否符合学术规范。
  用于：识别标题结构类型（概念型/关系型/发现型/问题型/方法型/综述型）、评估结构是否合适。
  触发场景："分析标题结构"、"这个标题是什么类型"、"标题结构是否合适"。
---

# Title Structure Analyzer - 标题结构分析

## 功能说明

分析论文标题采用的语法结构类型，评估是否适合该研究。

## 结构类型

### 1. Concept Title（概念型）
用于：理论框架、概念发展研究

**示例**：
```
Development and Validation of a Conceptual Framework for X
The Role of X: A Theoretical Perspective
```

### 2. Relationship Title（关系型）
用于：实证研究、变量关系研究

**示例**：
```
Social Media Use Improves Academic Performance
X Predicts Y Through Z
```

### 3. Finding Title（发现型）
用于：报告研究发现

**示例**：
```
Climate Change Accelerates Species Extinction Rates
Social Isolation Linked to Increased Health Risks
```

### 4. Question Title（问题型）
用于：探索性研究、验证性研究

**示例**：
```
Does Social Media Use Cause Depression?
Can Exercise Improve Cognitive Function?
```

### 5. Method Title（方法型）
用于：方法论研究、工具开发

**示例**：
```
A New Method for Measuring X
Development and Testing of the Y Scale
```

### 6. Review Title（综述型）
用于：综述类研究

**示例**：
```
A Meta-Analytic Review of Social Media Effects on Mental Health
X: A Systematic Review
```

## 分析要点

1. **识别结构类型**：确定标题属于哪种结构
2. **评估适合度**：判断该结构是否适合研究内容
3. **提出建议**：如不适合，建议其他结构

## 输出格式

请提供：
1. **结构类型**：识别出的标题结构
2. **适合度评估**：是否适合研究内容
3. **建议**：如需优化，提供替代结构建议
