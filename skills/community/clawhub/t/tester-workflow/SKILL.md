---
name: tester-workflow
description: Complete testing workflow from requirements analysis to test case generation and review - triggers on "完整测试流程", "testing workflow", "测试工作流", "端到端测试", "全流程测试" - includes all sub-skills for one-stop installation
---

# 完整测试工作流

## 概述

这是一个完整的测试工作流 skill，集成了从需求分析到测试用例生成和评审的全流程。**一站式安装，包含所有必需的子 skills。**

## 包含的子 Skills

本 skill 已完整包含以下4个子 skills：

1. **analyze-requirements** - 需求分析（测试视角）
2. **understand-design** - 设计文档理解（测试视角）
3. **generate-test-cases** - 测试用例生成
4. **review-test-cases** - 测试用例评审

所有子 skills 位于 `included-skills/` 目录下，可以独立使用。

## 完整工作流

### 阶段1：需求分析
**使用：** `analyze-requirements` skill

**输入：** 需求文档  
**输出：** 需求分析报告（6个维度）

**核心原则：** 不迎合用户的"简化"要求，始终保持专业标准

**6个维度：**
1. 需求概述
2. 内容提炼
3. 关键验收标准
4. 潜在风险点
5. 疑问清单
6. 一致性验证

**详细文档：** [included-skills/analyze-requirements/](included-skills/analyze-requirements/)

---

### 阶段2：设计文档理解
**使用：** `understand-design` skill

**输入：** 设计文档  
**输出：** 问题清单（8个维度，带优先级）

**核心原则：** 使用测试专家的checklist，不被时间压力影响质量

**8个维度：**
1. 安全性问题
2. 数据一致性问题
3. 边界条件问题
4. 接口设计问题
5. 数据库设计问题
6. 缓存/中间件设计问题
7. 性能问题
8. 可测试性问题

**详细文档：** [included-skills/understand-design/](included-skills/understand-design/)

---

### 阶段3：测试用例生成
**使用：** `generate-test-cases` skill

**输入：** 需求文档 + 设计文档 + 需求分析报告  
**输出：** 测试用例（CSV格式，30-50个用例）

**核心原则：** 严格遵循格式要求和覆盖策略，不接受"示例就行"的降级

**5个覆盖策略：**
1. 正常业务流程
2. 异常业务流程
3. 边界值测试
4. 输入校验
5. 用户体验相关

**关键要求：**
- 真实CSV文件（UTF-8 BOM编码）
- 使用 `||` 双竖线分隔符
- 至少30-50个用例
- 覆盖5个策略

**详细文档：** [included-skills/generate-test-cases/](included-skills/generate-test-cases/)

---

### 阶段4：测试用例评审
**使用：** `review-test-cases` skill

**输入：** 测试用例 + 需求文档 + 设计文档  
**输出：** 评审报告（6个维度，带改进建议）

**核心原则：** 按照6个维度进行系统性评审，不接受"快速看一下"的降级

**6个维度：**
1. 完整性评审
2. 合理性评审
3. 覆盖度评审
4. 规范性评审
5. 可执行性评审
6. 改进建议

**详细文档：** [included-skills/review-test-cases/](included-skills/review-test-cases/)

---

## 使用场景

### 场景1：完整流程（从需求到测试用例）

```
用户提供需求文档 
    ↓
使用 analyze-requirements 分析需求
    ↓
用户提供设计文档
    ↓
使用 understand-design 理解设计
    ↓
使用 generate-test-cases 生成测试用例
    ↓
使用 review-test-cases 评审测试用例
    ↓
输出最终测试用例
```

### 场景2：部分流程（只需要生成测试用例）

```
用户提供需求文档 + 设计文档
    ↓
使用 generate-test-cases 生成测试用例
    ↓
输出测试用例
```

### 场景3：部分流程（只需要评审测试用例）

```
用户提供测试用例 + 需求文档
    ↓
使用 review-test-cases 评审测试用例
    ↓
输出评审报告
```

---

## 工作流程图

```
┌─────────────────┐
│   需求文档      │
└────────┬────────┘
         │
         ↓
┌─────────────────────────┐
│ analyze-requirements    │
│ (需求分析)              │
└────────┬────────────────┘
         │
         ↓
┌─────────────────┐
│ 需求分析报告    │
└────────┬────────┘
         │
         ↓
┌─────────────────┐
│   设计文档      │
└────────┬────────┘
         │
         ↓
┌─────────────────────────┐
│ understand-design       │
│ (设计文档理解)          │
└────────┬────────────────┘
         │
         ↓
┌─────────────────┐
│   问题清单      │
└────────┬────────┘
         │
         ↓ (澄清问题后)
┌─────────────────────────┐
│ generate-test-cases     │
│ (测试用例生成)          │
└────────┬────────────────┘
         │
         ↓
┌─────────────────┐
│ 测试用例(CSV)   │
└────────┬────────┘
         │
         ↓
┌─────────────────────────┐
│ review-test-cases       │
│ (测试用例评审)          │
└────────┬────────────────┘
         │
         ↓
┌─────────────────┐
│   评审报告      │
└────────┬────────┘
         │
         ↓ (修改后)
┌─────────────────┐
│ 最终测试用例    │
└─────────────────┘
```

---

## 核心原则

### 1. 不降低标准
- 不迎合用户的"简化"、"快速"、"示例"要求
- 始终保持专业标准
- 系统性分析，不做表面工作

### 2. 系统性方法
- analyze-requirements：6个维度
- understand-design：8个维度
- generate-test-cases：5个覆盖策略
- review-test-cases：6个维度

### 3. 量化分析
- 提供覆盖率百分比
- 标注优先级（P0/P1/P2）
- 统计用例数量
- 评估风险等级

### 4. 具体可执行
- 提供标准模板
- 给出具体建议
- 估算工作量
- 明确下一步行动

---

## 快速开始

### 1. 完整流程示例
参见：[examples/full-workflow.md](examples/full-workflow.md)

### 2. 各阶段详细文档
- [需求分析](included-skills/analyze-requirements/)
- [设计理解](included-skills/understand-design/)
- [用例生成](included-skills/generate-test-cases/)
- [用例评审](included-skills/review-test-cases/)

### 3. 工作流程指南
参见：[reference/workflow-guide.md](reference/workflow-guide.md)

---

## 文件结构

```
tester-workflow/
├── README.md                          # 本文件
├── SKILL.md                           # 主 skill 文件
├── included-skills/                   # 包含的子 skills
│   ├── analyze-requirements/          # 需求分析
│   ├── understand-design/             # 设计理解
│   ├── generate-test-cases/           # 用例生成
│   └── review-test-cases/             # 用例评审
├── examples/
│   └── full-workflow.md              # 完整工作流示例
└── reference/
    └── workflow-guide.md             # 工作流程指南
```

---

## 底线

**专业标准不应因用户的时间压力或简化要求而降低。**

每个阶段都有明确的质量标准：
- 需求分析：6个维度全覆盖
- 设计理解：8个维度系统性提问
- 用例生成：30-50个用例，5个策略全覆盖
- 用例评审：6个维度全面评审

如果你发现自己在想"快速做一下就行"，立即停止。必须按照标准流程执行。
