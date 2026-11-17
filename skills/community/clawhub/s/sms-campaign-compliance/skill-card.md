## Description:

Flags TCPA and disclosure risks in a US marketing text before it sends, and lists the consent record and opt-out handling the sender has to keep.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rapidworker1](https://clawhub.ai/user/rapidworker1)

### License/Terms of Use:

MIT-0

## Use Case:

U.S. brands and agencies can use this skill to review a marketing SMS draft for potential TCPA and disclosure issues and organize consent and opt-out checks. Its reports are not legal advice or clearance to send; review flagged and unflagged drafts with qualified counsel.

### Deployment Geography for Use:

United States

## Known Risks and Mitigations:

Risk: The compliance checker misses obvious risky phrases and omits promised checks, so its reports are unreliable.

Mitigation: Do not treat a 'No flags' result as clearance to send. Require corrected detection and independently complete the consent and opt-out review with qualified counsel.

Risk: The optional Windows application is separate from the Python workflow and requires its own assessment.

Mitigation: Use the Python workflow without the optional application unless and until that application has been separately assessed.

## Reference(s):

- [TCPA and disclosure checks for US marketing texts](references/sms-compliance-rules.md)
- [SMS Campaign Compliance on ClawHub](https://clawhub.ai/rapidworker1/skills/sms-campaign-compliance)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Files]

**Output Format:** [Markdown risk report and review checklist files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Draft-review support only; does not send messages or provide legal advice.]

## Skill Version(s):

1.0.7 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
