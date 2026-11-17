## Description:

将 Amazon 商品评论整理为有依据的产品、包装、说明和供应商改进任务。

This skill is ready for commercial/non-commercial use.

## Publisher:

[funewa](https://clawhub.ai/user/funewa)

### License/Terms of Use:

MIT

## Use Case:

面向需要改进 Amazon 商品的产品和运营团队，根据已采集的评论证据识别问题，并形成产品、包装、说明或供应商任务。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Some ARI operations may spend account credits without an in-the-moment confirmation when account or server rules allow automatic confirmation.

Mitigation: Set the account to ask before every charge. For product operations, obtain a quote and run only after explicit user approval; follow the returned price and request ID.

Risk: Recurring review collection can cause continuing credit charges.

Mitigation: Use a manual schedule for one-time collection and obtain separate approval before enabling recurring collection.

## Reference(s):

- [专属运营工作流](references/operation-workflow.md)
- [ARI API 参考](references/reference.md)
- [ARI 运营工作台](https://ari.funewa.com/zh/operations)
- [ARI 用户中心](https://ari.funewa.com/zh/account)

## Skill Output:

**Output Type(s):** [Analysis, Guidance, Text, Markdown]

**Output Format:** [Evidence-based product improvement recommendations, typically in Markdown]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses available review and product data; does not contact buyers, edit product pages, or place supplier orders.]

## Skill Version(s):

1.5.3 (source: changelog)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
