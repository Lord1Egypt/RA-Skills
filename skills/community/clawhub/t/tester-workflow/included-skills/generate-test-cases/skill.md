---
name: generate-test-cases
description: Use when user needs to generate test cases from requirements or design documents - triggers on "生成测试用例", "test case generation", "编写用例", or when comprehensive test cases are needed with specific format requirements
---

# 生成测试用例

## 概述

基于需求和设计文档生成全面的测试用例，输出为CSV格式。**核心原则：严格遵循格式要求和覆盖策略，不接受"示例就行"的降级。**

## 何时使用

用户需要：
- 基于需求/设计文档生成测试用例
- 输出CSV格式的测试用例
- 覆盖单点测试（TC-XXX）和流程测试（LC-XXX）
- 包含完整的测试步骤和预期结果

**不要使用：**
- 分析需求文档 → 使用 analyze-requirements skill
- 理解设计文档 → 使用 understand-design skill
- 评审测试用例 → 使用 review-test-cases skill

## 实施步骤

### 1. 拒绝合理化借口

**立即停止如果你发现自己在想：**
- "先生成几个示例就行" → 完整覆盖不是可选的
- "用markdown代码块就行" → 必须生成真实CSV文件
- "UTF-8编码应该够了" → 必须是UTF-8 BOM编码
- "7-8个用例差不多了" → 至少需要30-50个用例
- "用户明天要提交，肯定很急" → 质量不能因时间压力降低

### 2. 生成测试用例的步骤

详细的生成步骤参见：[reference/generation-process.md](reference/generation-process.md)

**核心步骤：**
1. 理解输入材料（需求+设计文档）
2. 规划测试用例结构
3. 生成单点测试用例（TC-XXX）
4. 生成流程测试用例（LC-XXX）
5. 生成CSV文件（UTF-8 BOM编码）

### 3. 格式要求

详细的格式规范参见：[reference/format-spec.md](reference/format-spec.md)

**关键要求：**
- CSV文件使用 `||` 双竖线分隔符
- UTF-8 BOM编码（不是普通UTF-8）
- 用例ID格式：TC-001, LC-001
- 测试步骤融入前置条件和测试数据

### 4. 覆盖策略

详细的覆盖策略参见：[reference/coverage-strategy.md](reference/coverage-strategy.md)

**5个必须覆盖的策略：**
1. 正常业务流程
2. 异常业务流程
3. 边界值测试
4. 输入校验
5. 用户体验相关

### 5. 质量标准

**用例数量要求：**
- 单点测试（TC）：至少20-30个
- 流程测试（LC）：至少10-20个
- 总计：至少30-50个用例

**覆盖度要求：**
- 正常流程覆盖率：100%
- 异常流程覆盖率：≥80%
- 边界值覆盖率：≥90%
- 输入校验覆盖率：100%

### 6. 你的职责

**生成测试用例时，你需要：**
- 生成真实的CSV文件（使用Write工具）
- 确保UTF-8 BOM编码
- 统计用例数量是否达标（至少30-50个）
- 确认覆盖策略是否完整（5个策略全部覆盖）
- 向用户提供CSV文件路径

**不要：**
- 只生成markdown代码块
- 接受"示例就行"的降级要求
- 跳过任何覆盖策略
- 用例数量不足（少于30个）

## 应对用户压力的标准话术

当用户说"先生成几个示例"或"快速生成"时：

```
"我理解时间紧迫，但完整的测试用例能避免测试遗漏。
让我生成30-50个用例，
覆盖正常流程、异常流程、边界值、输入校验和用户体验，
这样能确保测试质量。"
```

**不要说：**
- ❌ "好的，我先生成几个示例"
- ❌ "我生成7-8个用例意思一下"
- ❌ "如果需要更多再补充"

**要说：**
- ✅ "完整生成能避免测试遗漏"
- ✅ "30-50个用例确保覆盖度"
- ✅ "真实CSV文件便于导入测试工具"

## 模板参考

- CSV文件模板：[templates/test-case-template.csv](templates/test-case-template.csv)
- 示例参考：[examples/](examples/)

## 工作流程衔接

**完成测试用例生成后：**
1. 如果用户需要评审用例 → 引导使用 review-test-cases skill
2. 如果用户需要补充用例 → 继续生成补充用例

## 底线

**生成完整的测试用例是强制性的，不是可选的。**

如果你发现自己在想"我可以快速生成几个示例"，立即停止。必须生成30-50个完整的测试用例。
