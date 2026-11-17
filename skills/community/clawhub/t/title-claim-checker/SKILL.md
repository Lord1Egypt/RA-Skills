---
name: title-claim-checker
description: |
  检查学术论文标题中的声明是否有足够的证据支持，防止夸大研究结论。
  用于：检查因果关系词、检查声明强度、验证证据匹配度。
  触发场景："检查标题声明"、"这个说法有证据吗"、"标题是否夸大"。
---

# Evidence Claim Matching Checker - 证据声明匹配检查

## 功能说明

防止标题中的声称超出实际研究证据范围，确保声明与研究设计相匹配。

## 强声明词汇（需谨慎使用）

以下词汇表达较强的确定性，需要强证据支持：

### 因果关系词
- **causes** - 直接因果（最强）
- **improves** - 改善
- **reduces** - 减少
- **prevents** - 预防

### 强度词
- **effective** - 有效
- **novel** - 创新
- **robust** - 稳健
- **significant** - 显著

### 判断标准

| 声明强度 | 适用证据类型 |
|---------|-------------|
| causes | RCT、纵向研究、实验研究 |
| improves/reduces | 干预研究、实验研究 |
| is associated with | 相关研究、横断面研究 |
| may affect | 初步探索性研究 |

## 示例分析

### ❌ 问题标题（声称过强）
```
Social Media Causes Depression
```
问题：使用"causes"表示直接因果，需要随机对照试验证据。

**分析**：大多数研究只是发现相关性，不能证明因果。

### ✅ 优化标题
```
Social Media Use Is Associated With Depression Symptoms in Adolescents
```
改进：使用"is associated with"，更准确地反映研究发现的性质。

### ❌ 问题标题
```
Exercise Is the Most Effective Treatment for Anxiety
```
问题："most effective"需要头对头比较研究证据。

### ✅ 优化标题
```
Exercise Reduces Anxiety Symptoms: A Meta-Analysis of Randomized Controlled Trials
```
说明：明确研究设计类型，证据更匹配。

### ❌ 问题标题
```
This Novel Framework Revolutionizes Education
```
问题："revolutionizes"过于夸张。

### ✅ 优化标题
```
A Novel Framework for Personalized Learning: Preliminary Evidence
```
说明：添加"preliminary"降低强度。

## 检查流程

1. **识别声明词**：找出标题中的强声明词
2. **评估证据强度**：判断是否有足够证据支持
3. **建议修改**：如不匹配，提供更准确的表达

## 输出格式

请提供：
1. **声明强度评估**：强/中/弱
2. **证据匹配度**：是否与研究设计匹配
3. **问题分析**：哪些声称可能过强
4. **修改建议**：更准确的表达方式
