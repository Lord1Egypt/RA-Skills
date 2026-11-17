---
name: title-keyword-checker
description: |
  检查学术论文标题的关键词质量和可搜索性。
  用于：验证核心词汇、检查通用术语、检查缩写、检查关键词覆盖度。
  触发场景："检查标题关键词"、"标题是否好搜索"、"关键词是否合适"。
---

# Keyword & Searchability Checker - 关键词与可搜索性检查

## 功能说明

确保标题包含有学术价值的关键词，便于文献检索和引用。

## 检查项目

### 1. 核心词汇准确性
检查标题中的关键术语是否正确、专业。

**问题**：使用不准确或不专业的术语
```
The Influence of Smart Phones on Youth
```
问题："Smart Phones"不够学术化。

**优化**：
```
Mobile Phone Use and Adolescent Health: A Systematic Review
```

### 2. 通用术语 vs 专有术语
优先使用通用学术术语，提高可发现性。

**示例**：
```
❌ Our New Scale (专有)
✅ Development and Validation of a Scale (通用)

❌ The XYZ Model
✅ A Theoretical Framework for X: The XYZ Model
```

### 3. 缩写使用
检查是否有过多需要解释的缩写。

**问题**：
```
MHE in ADHD: A Cross-Sectional Study
```
问题：MHE和ADHD需要读者知道缩写含义。

**优化**：
```
Mental Health Effects in Attention-Deficit Hyperactivity Disorder: A Cross-Sectional Study
```
或说明首次使用缩写。

### 4. 关键词覆盖度
检查是否覆盖主要研究内容。

**检查**：
- 研究变量是否出现在标题中
- 研究主题是否清晰
- 关键概念是否可搜索

### 5. 避免过于宽泛或狭窄

**过于宽泛**：
```
Social Media Effects
```
问题：无法体现具体研究内容。

**优化**：
```
Social Media Use and Sleep Quality Among College Students

**过于狭窄**：
```
Effect of WeChat Use on Freshman 2019 GPA in Zhejiang University
```
问题：过于具体，难以被检索到。

**优化**：
```
Mobile Social Media Use and Academic Performance in Chinese University Students
```

## 最佳实践

1. **包含2-4个核心关键词**
2. **使用标准术语**（参考MeSH、常用文献）
3. **避免过多缩写**
4. **平衡具体性与通用性**

## 输出格式

请提供：
1. **关键词评分**：1-10分
2. **核心词汇列表**：识别的关键词
3. **可搜索性评估**：是否容易被找到
4. **改进建议**：如何优化关键词
