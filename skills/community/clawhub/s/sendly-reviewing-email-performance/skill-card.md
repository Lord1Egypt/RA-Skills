## Description:

Summarizes Sendly email delivery, opens, bounces, campaign performance, individual delivery history, and sending-limit usage without changing email resources.

This skill is ready for commercial/non-commercial use.

## Publisher:

[devino](https://clawhub.ai/user/devino)

### License/Terms of Use:

MIT-0

## Use Case:

Sendly users review email delivery and engagement, investigate bounces or a campaign's performance, and check daily and monthly sending limits.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Email analytics and bounce details can reveal recipient information.

Mitigation: Grant access only to the intended Sendly project and share recipient details only when needed for the report.

Risk: Sending or changing email resources would exceed this skill's read-only purpose.

Mitigation: Use only analytics, email-history, campaign-statistics, and usage reads; do not send, create, update, or delete resources.

## Reference(s):

- [Reviewing Email Performance on ClawHub](https://clawhub.ai/devino/skills/sendly-reviewing-email-performance)

## Skill Output:

**Output Type(s):** [Analysis, Guidance]

**Output Format:** [Markdown]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only report with available metrics, relevant delivery details, and up to three suggested next steps.]

## Skill Version(s):

1.0.1 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
