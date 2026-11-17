## Description:

Approval Engine provides rule-driven approval workflows, exception detection, automated recovery handling, and Discord notifications for OpenClaw workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cjboy007](https://clawhub.ai/user/cjboy007)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operations teams use this skill to add configurable business approvals, exception alerts, escalation handling, and recovery workflows around quotation, order, permission-change, and incident processes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Configuration can execute code through evaluated approval trigger expressions.

Mitigation: Remove eval-based expression handling and replace it with a constrained parser or declarative rule evaluator before using the skill in real workflows.

Risk: Approval workflows may be bypassed or completed incorrectly if approver logic is not enforced for every required approver.

Mitigation: Require all configured approvers for parallel approvals and add tests for serial, parallel, rejection, timeout, and escalation paths before production use.

Risk: Discord or webhook notification destinations could send approval or incident details outside approved channels.

Mitigation: Allowlist webhook destinations and channel IDs, keep secrets in environment-managed storage, and rotate any exposed Discord credentials.

Risk: Notification payloads and logs may expose sensitive business, customer, approval, or incident data.

Mitigation: Minimize notification fields, redact sensitive values, and define retention limits for approval records, exception logs, and metrics.

Risk: Local JSON persistence can expose or corrupt approval and exception state if filesystem controls are weak.

Mitigation: Store data files in a restricted directory, enforce least-privilege file permissions, back up state, and monitor failed reads or writes.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/cjboy007/skills/ssa-approval-engine)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JavaScript examples, shell commands, and JSON configuration]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces approval records, exception logs, notification payloads, and recovery status data when installed and invoked.]

## Skill Version(s):

1.0.0 (source: server release evidence and artifact documentation)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
