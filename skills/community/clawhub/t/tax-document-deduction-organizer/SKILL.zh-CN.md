---
name: tax-document-deduction-organizer
description: >-
  帮助用户处理“Validated demand: Tax preparers and taxpayers need practical help organizing income statements, receipts, deductions, estimated taxes, and handoff checklists before filing or sending records to an accountant. This requirement is supported by 9 separate online signals across 1 source families, so it represents broader demand rather than a single isolated request.”。当用户提出 business-and-operations, tax documents, deductions, receipts, estimated taxes，或需要围绕该需求获得实用流程、产物、检查清单、分析或实现支持时使用。
---

# Tax Document Deduction Organizer

## 需求

使用这个技能帮助以下用户群体：self-employed workers, small business owners, tax preparers, families, and finance admins preparing tax packets from scattered records

> Validated demand: Tax preparers and taxpayers need practical help organizing income statements, receipts, deductions, estimated taxes, and handoff checklists before filing or sending records to an accountant. This requirement is supported by 9 separate online signals across 1 source families, so it represents broader demand rather than a single isolated request.

需求评分：90/100（需求强度 `70/70`，本地可执行性 `30/30`）。
证据：9 条信号，覆盖 1 个来源类型。

如需查看来源证据、执行计划或评审标准，请阅读 `references/requirement-plan.md`。

## 工作流程

1. 重新说明用户想要的结果、限制、已有输入和成功标准。
2. 把运营问题转化为可复用流程、检查清单、模板或轻量分析。
3. 只有当缺失信息会明显改变输出时才提问；否则先做合理假设并继续推进。
4. 保持本地硬件友好：优先使用脚本、模板、检查清单、小模型或 CPU 可承受的流程，避免依赖云端专用资源或大规模训练。
5. 产出用户需要的文档、流程、清单、分析、代码修改或决策支持。
6. 对照成功标准检查结果，并列出剩余风险或后续事项。

## 预期输出

- 针对用户当前情境的定制回答或产物。
- 当任务可复用时，提供检查清单或工作流程。
- 说明结果如何被检查的验证备注。

## 验证

- 输出直接回应发现的原始需求。
- 用户不需要阅读原始来源帖子也能采取行动。
- 假设、限制和所需输入清晰可见。
- 在有帮助时，最终回复包含简短的使用说明或下一步建议。

## 触发方式

关键词：`business-and-operations`, `tax documents`, `deductions`, `receipts`, `estimated taxes`, `filing checklist`

示例触发句：

- `Help me Tax preparers and taxpayers need practical help organizing income statements, receipts, deductions, estimated taxes, and.`
- `I need a practical workflow for Tax preparers and taxpayers need practical help organizing income statements, receipts, deductions, estimated taxes, and.`
- `Use $tax-document-deduction-organizer to handle Tax preparers and taxpayers need practical help organizing income statements, receipts, deductions, estimated taxes, and.`
