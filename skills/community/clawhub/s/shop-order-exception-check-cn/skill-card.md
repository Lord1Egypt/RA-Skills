## Description:

输入脱敏订单状态表、商家正常流程和时效规则，整理超时、缺项与状态矛盾的订单待办清单，并按风险和截止时间给出人工处理顺序。

This skill is ready for commercial/non-commercial use.

## Publisher:

[xxjrq](https://clawhub.ai/user/xxjrq)

### License/Terms of Use:

MIT-0

## Use Case:

中文小店、小说作者和自媒体创作者可用此技能，根据脱敏订单资料、正常流程及时效规则整理异常订单，并安排人工核对顺序。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Suggested exception judgments and priorities depend on the completeness and accuracy of the supplied order data, workflow, and timing rules.

Mitigation: Provide redacted, complete inputs and manually verify the suggested priorities against business records before taking action.

## Reference(s):

- [ERPNext project (functional inspiration)](https://github.com/frappe/erpnext)
- [ERPNext README](https://github.com/frappe/erpnext/blob/develop/README.md)

## Skill Output:

**Output Type(s):** [Markdown, Guidance]

**Output Format:** [Markdown tables and a numbered manual action list]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Preserves supplied order identifiers and field values; lists missing inputs instead of inventing facts.]

## Skill Version(s):

1.0.0 (source: server-resolved release, manifest.yaml)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
