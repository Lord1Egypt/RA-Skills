---
name: title-grammar-checker
description: |
  检查学术论文标题的语法正确性和表达清晰度。
  用于：检查词汇密度、句子成分、主谓关系、被动结构、缩写使用。
  触发场景："检查标题语法"、"标题是否清晰"、"帮我看看这个标题的表达"。
---

# Title Clarity & Grammar Checker - 标题清晰度与语法检查

## 功能说明

检查标题的语法正确性和表达清晰度，确保标题易于理解。

## 检查项目

### 1. 词汇密度
检查是否包含过多专业术语或生僻词汇。

**问题**：词汇过于复杂
```
The Psychopathological Manifestations of Adolescent Social Media Utilization
```

**优化**：
```
Social Media Use and Adolescent Mental Health
```

### 2. 句子成分结构
检查主语、谓语、宾语是否完整清晰。

**问题**：成分残缺
```
Effect of Social Media on Sleep (缺少主语和谓语)
```

**优化**：
```
The Effect of Social Media Use on Sleep Quality
```

### 3. 主谓关系
确保主动词与主语一致。

**问题**：
```
Adolescent Social Media Anxiety Reduction Intervention Effect Study
```
分析：多个名词连读，结构混乱。

**优化**：
```
Effects of Social Media Anxiety Reduction Interventions for Adolescents
```

### 4. 被动结构使用
谨慎使用被动语态。

**问题**：
```
The Effects of Social Media on Youth Was Investigated
```

**优化**：
```
Social Media Effects on Youth: A Cross-Sectional Study
```

### 5. 缩写和可选词
检查是否有过多缩写或不必要词汇。

**常见问题词**：
- "A Study on"
- "Research on"
- "Investigation of"
- "An Analysis of"

**示例**：
```
❌ A Study on the Effects of Social Media
✅ Social Media Effects on Mental Health: A Meta-Analysis
```

## 常见问题总结

| 问题类型 | 示例 | 建议 |
|---------|------|------|
| 名词堆砌 | Anxiety Depression Stress Study | 使用动词+名词结构 |
| 缺少动词 | Social Media Use in Adolescents | 添加动词或使用介词结构 |
| 词义重复 | Recent Recent Advances | 删除重复词 |
| 冗余词 | Study on, Research about | 删除无意义词 |

## 输出格式

请提供：
1. **清晰度评分**：1-10分
2. **问题列表**：发现的具体问题
3. **优化建议**：修改建议
4. **优化后标题**：推荐的新标题
