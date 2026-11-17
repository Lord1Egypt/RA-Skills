## Description:

Combines consented study, review, and task reminders into a daily summary, activating only on clear reminder requests.

This skill is ready for commercial/non-commercial use.

## Publisher:

[qizhitang](https://clawhub.ai/user/qizhitang)

### License/Terms of Use:

MIT

## Use Case:

Students and guardians use the skill to set, review, pause, or cancel consented reminders for spaced review, study plans, and exploration tasks.

### Deployment Geography for Use:

Mainland China; designed for Chinese K–12 use, with local safety channels and rules requiring localization before use elsewhere.

## Known Risks and Mitigations:

Risk: The security review flags a possible scope mismatch.

Mitigation: Review the requested reminder behavior and queue contents against the user's stated intent before enabling reminders.

Risk: The security review flags possible extra reminders beyond the intended limit.

Mitigation: Require explicit reminder consent and enforce the documented daily cap and quiet hours; let users inspect, pause, or cancel reminders.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/qizhitang/skills/xiaozhi-im-reminder)
- [Reminder intervals and scheduling](artifact/references/ebbinghaus-schedule.md)
- [Consent and reminder budget](artifact/shared/vocab.md)
- [Reminder handover protocol](artifact/shared/handover-protocol.schema.json)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Concise Chinese reminder messages and Markdown queue summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires explicit consent; normally limited to one daily merged summary and one immediate reminder, subject to quiet hours.]

## Skill Version(s):

2.12.7 (source: frontmatter, server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
