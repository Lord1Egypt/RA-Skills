---
name: title-optimization
description: |
  学术论文标题（Title）优化工具套件，用于SCI/SSCI英文论文标题的检查、分析和优化。
  适用于：检查论文标题质量、分析标题结构、优化标题表达、提升标题可搜索性。
  包含7个核心功能：贡献度检查、结构分析、清晰度语法检查、证据匹配检查、
  关键词可搜索性检查、风格推荐、综合诊断报告。
---

# Title Optimization - 学术论文标题优化工具

本Skill套件提供7个核心功能，用于优化英文SCI/SSCI论文标题。

## 触发方式

当用户需要以下帮助时使用本Skill：
- 检查论文标题是否清晰传达研究贡献
- 分析标题结构是否符合学术规范
- 检查标题语法和表达清晰度
- 验证标题声明是否有足够证据支持
- 优化标题关键词以提升可搜索性
- 推荐合适的标题风格模板
- 生成综合诊断报告

## 7个核心功能

### 1. Title Contribution Checker（标题贡献度检查）

**目的**：判断标题是否清晰传达了研究的核心理念和价值。

**功能**：
- 判断标题是否回答"研究了什么？"这个问题
- 判断标题是否包含研究焦点
- 识别只描述主题、没有贡献的标题

**示例**：
```
原标题：Social Media Use
优化后：Social Media Use Predicts Sleep Quality Through Emotional Regulation
```

### 2. Title Structure Analyzer（标题结构分析）

**目的**：判断标题采用的结构类型是否合适。

**识别的结构类型**：
- **Concept title（概念型）**：Development and Validation of...
- **Relationship title（关系型）**：X Improves Y
- **Finding title（发现型）**：描述研究发现
- **Question title（问题型）**：Does X Work?
- **Method title（方法型）**：描述研究方法
- **Review title（综述型）**：A Meta-Analytic Review of X

### 3. Title Clarity & Grammar Checker（标题清晰度与语法检查）

**目的**：检查标题是否清晰易懂。

**检查项目**：
1. 词汇密度
2. 句子成分结构
3. 主谓关系
4. 被动结构使用
5. 缩写和可选词

**示例**：
```
问题标题：Adolescent Social Media Anxiety Reduction Intervention Effect Study
建议：修改为更清晰的动宾结构
```

### 4. Evidence Claim Matching Checker（证据声明匹配检查）

**目的**：防止声称超出实际证据范围。

**强声明词汇**（需要强证据支持）：
- causes
- improves
- reduces
- effective
- novel
- robust

**检查**：判断这些词是否有足够的研究证据支持。

**示例**：
```
问题：Social Media Causes Depression（过于强因果）
建议：Social Media Use Is Associated With Depression Symptoms（更准确）
```

### 5. Keyword & Searchability Checker（关键词与可搜索性检查）

**目的**：确保标题包含有学术价值的关键词。

**检查项目**：
1. 核心词汇是否正确
2. 是否使用通用术语
3. 是否包含需要解释的缩写
4. 关键词是否覆盖主要研究内容

### 6. Title Style Recommendation（标题风格推荐）

**目的**：根据研究类型推荐合适的标题表达方式。

**推荐模板**：

**概念研究**：
- The X: Conceptual Framework and Supporting Evidence

**实证研究**：
- X Improves Y

**探究研究**：
- Does X Work?

**元分析**：
- A Meta-Analytic Review of X

### 7. Summary Diagnostic Report（综合诊断报告）

**目的**：整合前6个Skill的检查结果，生成完整报告。

**报告内容**：
1. 各项检查得分
2. 标题优点
3. 存在的问题
4. 每个问题的原因
5. 修改建议
6. 推荐修改版本

**输出格式**：
```
Title Diagnostic Report

Original Title: [原始标题]
Score: [总分]

Strengths:
- [优点列表]

Problems:
- [问题列表]

Suggestions:
- [建议列表]

Recommended Revision:
[优化后的标题]
```

## 使用建议

1. **单独使用**：用户可以请求单个功能的检查
2. **综合使用**：使用第7项（Summary Diagnostic Report）获取完整分析
3. **迭代优化**：根据建议修改后，可再次检查直到满意

## 注意事项

- 所有检查基于50篇高水平学术论文的统计分析
- 建议仅供参考，最终决定权在作者
- 不同学科可能有不同的命名惯例
