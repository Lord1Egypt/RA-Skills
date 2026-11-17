## Description:

日常运营 + 客服售后 + 合规风控三合一 - 仅读 API、不自动修改、客服合规、人工确认

This skill is ready for commercial/non-commercial use.

## Publisher:

[guowaa223](https://clawhub.ai/user/guowaa223)

### License/Terms of Use:

MIT-0

## Use Case:

E-commerce operators and support teams use this skill to generate Taobao shop operations reports, compliance check reports, inventory reminders, customer-service logs, after-sales records, and risk-control alerts. The artifact describes outputs as recommendations and records that require human review before platform changes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Reports and success messages may be based on hard-coded demo data rather than verified Taobao API checks or platform actions.

Mitigation: Treat generated reports and logs as draft outputs until the demo behavior is replaced with verified Taobao API integrations and clear failure handling.

Risk: Operational, compliance, customer-service, inventory, risk, and refund outputs could be mistaken for validated store decisions.

Mitigation: Require explicit human approval before acting on any report, recommendation, customer-service response, or after-sales result.

Risk: Python dependencies are not pinned to exact versions.

Mitigation: Install dependencies in an isolated environment and pin versions before operational use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/guowaa223/skills/taobao-operations)
- [Publisher profile](https://clawhub.ai/user/guowaa223)

## Skill Output:

**Output Type(s):** [Files, Text, JSON, Guidance]

**Output Format:** [Excel reports, JSON logs, and terminal text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs are generated as reports, reminders, task lists, logs, and alerts for human review.]

## Skill Version(s):

1.0.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
