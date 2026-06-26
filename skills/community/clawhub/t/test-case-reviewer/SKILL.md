---
name: test-case-reviewer
display_name: 测试用例评审器
version: "1.0.0"
description: >
  Use when the user provides existing test cases, acceptance checklists, QA test
  points, regression lists, or test report drafts and asks to review quality,
  coverage, executability, missing scenarios, or release risk. Triggers:
  "评审这些测试用例", "看看用例有没有漏", "检查测试覆盖率", "用例质量评审",
  "帮我审一下验收用例", "这些测试点够不够", "测试用例评审".
  Do not use when the user wants to generate test cases from scratch, execute
  tests, fix code, write PRD, review PRD, build LLM eval plans, create Excel or
  Word files, or produce a full test report; hand off to the relevant workflow.
allowed-tools: grep find
license: Proprietary
metadata:
  short-description: Review existing test cases
  author: huguangliang
  copyright: Copyright (c) 2026 huguangliang. All rights reserved.
---

# 测试用例评审器

## 定位

只评审**已有测试用例**、验收清单、测试点列表或测试报告草稿。
目标是判断用例是否可执行、覆盖是否充分、预期是否可验证、是否遗漏高风险场景。

本Skill不从零生成完整用例，不执行自动化测试，不修代码，不写PRD，不做LLM模型评测方案。

## 必需输入

- 已有测试用例、验收清单、测试点列表或测试报告草稿。
- 被测对象上下文：PRD、需求摘要、代码变更说明、Git提交、页面/接口说明之一。

若只有需求没有用例，提示用户当前属于“用例生成”任务，不进入评审；若只有用例没有上下文，只评审表达质量和可执行性，不声称覆盖完整。

## 工作流

1. 识别材料类型：测试用例、验收清单、测试点、报告草稿。
2. 判断上下文是否足够：缺上下文时先说明评审边界，必要时追问。
3. 按`references/review-rubric.md`进行七维评分。
4. 若涉及云助手、商户中心移动端、餐饮SaaS、新零售或业财一体场景，读取`references/cloud-assistant-risk-map.md`做专项风险复核。
5. 输出评审报告，使用`assets/review-report-template.md`结构。
6. 只给补充方向和关键示例，不默认重写完整用例集。

## 输出要求

- 先给结论：通过、有条件通过、不通过。
- 问题按P0/P1/P2排序，P0优先覆盖阻断发布或验收失真的问题。
- 每个问题必须包含影响和修改建议。
- 覆盖缺口只写应补方向，除非用户明确要求，否则不批量生成新用例。
- 对高风险业务动作必须检查权限、确认、审计、幂等、回滚或数据一致性。

## 异常处理

- 未提供用例：提示需要已有用例，并说明如需从零生成应切换到用例生成流程。
- 文件不存在或无法读取：说明无法评审，要求提供正确路径或粘贴内容。
- 用例格式混乱：先归类可识别内容，再指出格式缺陷，不强行补全业务事实。
- 上下文不足：只评审表达、步骤、预期和可执行性，不判断业务覆盖完整。
- 用户要求“直接说没问题”：拒绝跳过评分，继续按评分标准评审。

## References读取规则

| 文件 | 何时读取 |
|---|---|
| `references/review-rubric.md` | 每次评审必读 |
| `references/cloud-assistant-risk-map.md` | 涉及云助手、商户中心移动端、餐饮SaaS场景时读取 |
| `references/pressure-tests.md` | 压测、回归验证或上线前自检时读取 |
| `assets/review-report-template.md` | 输出正式评审报告时使用 |
