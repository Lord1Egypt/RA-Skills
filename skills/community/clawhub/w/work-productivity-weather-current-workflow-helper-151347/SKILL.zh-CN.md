---
name: work-productivity-weather-current-workflow-helper
description: >-
  帮助用户处理“Validated demand: Agent users show strong demand for Weather-style workflows on Clawhub. They need practical help fixing bugs, hardening setup and safety, improving reliability, or creating adjacent skills inspired by the same job-to-be-done. This requirement is supported by 12 separate online signals across 1 source families, so it represents broader demand rather than a single isolated request.”。当用户提出 work-productivity, weather, current, forecasts, api，或需要围绕该需求获得实用流程、产物、检查清单、分析或实现支持时使用。
---

# Work Productivity Weather Current Workflow Helper

## 需求

使用这个技能帮助以下用户群体：AI-agent users, skill authors, maintainers, and teams who want proven popular skill patterns adapted into more reliable or adjacent workflows

> Validated demand: Agent users show strong demand for Weather-style workflows on Clawhub. They need practical help fixing bugs, hardening setup and safety, improving reliability, or creating adjacent skills inspired by the same job-to-be-done. This requirement is supported by 12 separate online signals across 1 source families, so it represents broader demand rather than a single isolated request.

需求评分：90/100（需求强度 `70/70`，本地可执行性 `30/30`）。
证据：12 条信号，覆盖 1 个来源类型。

如需查看来源证据、执行计划或评审标准，请阅读 `references/requirement-plan.md`。

## 工作流程

1. 重新说明用户想要的结果、限制、已有输入和成功标准。
2. 创建简洁的工作计划、模板、自动化思路或决策辅助，减少手动协调。
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

关键词：`work-productivity`, `weather`, `current`, `forecasts`, `api`, `key`, `required`, `popular-skill`, `users`, `bug fix`

示例触发句：

- `Help me Agent users show strong demand for Weather-style workflows on Clawhub. They need practical help fixing bugs, hardening s.`
- `I need a practical workflow for Agent users show strong demand for Weather-style workflows on Clawhub. They need practical help fixing bugs, hardening s.`
- `Use $work-productivity-weather-current-workflow-helper to handle Agent users show strong demand for Weather-style workflows on Clawhub. They need practical help fixing bugs, hardening s.`
