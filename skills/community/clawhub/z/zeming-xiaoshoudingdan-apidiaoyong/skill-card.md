## Description:

通过钉钉API导入订单数据，展示20项详细信息供核对，支持确认、重新查询或退出操作。

This skill is ready for commercial/non-commercial use.

## Publisher:

[duanzhen001](https://clawhub.ai/user/duanzhen001)

### License/Terms of Use:

MIT-0

## Use Case:

Sales or operations users can use this skill to display imported DingTalk order records for manual review and choose whether to continue, re-query, or exit the workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The artifact embeds and displays real-looking customer identity, phone, address, and financial order details.

Mitigation: Remove the embedded record, use synthetic examples or authorized runtime retrieval, and mask sensitive fields by default.

Risk: The workflow can show full order data without an explicit access-control step.

Mitigation: Require an authorized user action before revealing full order details and log or constrain access according to the deployment environment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/duanzhen001/skills/zeming-xiaoshoudingdan-apidiaoyong)
- [Publisher profile](https://clawhub.ai/user/duanzhen001)

## Skill Output:

**Output Type(s):** [Text, Guidance]

**Output Format:** [Plain text order checklist with A/B/C action options]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May display personal, contact, address, and financial order details unless the implementation masks or removes them.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
