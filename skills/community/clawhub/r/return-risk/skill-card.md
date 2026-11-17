## Description:

从 Amazon 评论和商品详情中识别可能导致退货的体验落差线索，并提出改进方向；不预测真实退货率。

This skill is ready for commercial/non-commercial use.

## Publisher:

[funewa](https://clawhub.ai/user/funewa)

### License/Terms of Use:

MIT-0

## Use Case:

Amazon 卖家和产品运营人员可用它从评论证据中识别可能导致退货的体验问题，并整理产品改进建议。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Conflicting payment instructions and a confirmed preview bug may cause unexpected credit spending.

Mitigation: Prefer a corrected release. If proceeding, require confirmation before every charge, use the specialized quote-and-confirm workflow, choose manual collection for one-time requests, review recurring schedules, and do not assume deepdive is a free preview.

## Reference(s):

- [ARI API and CLI reference](references/reference.md)
- [Product operations workflow](references/operation-workflow.md)
- [ClawHub release page](https://clawhub.ai/funewa/skills/return-risk)

## Skill Output:

**Output Type(s):** [Text, Markdown, Analysis, Guidance]

**Output Format:** [Markdown summary with review evidence and product improvement suggestions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Grounded in available review data; states scope and evidence limitations.]

## Skill Version(s):

1.5.3 (source: changelog, server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
