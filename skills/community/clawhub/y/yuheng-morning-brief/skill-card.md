## Description:

Generates a personalized daily stock-market morning brief and sends it to a configured Feishu recipient.

This skill is ready for commercial/non-commercial use.

## Publisher:

[horizoncove](https://clawhub.ai/user/horizoncove)

### License/Terms of Use:

MIT-0

## Use Case:

External users can use this skill to have an agent assemble a daily investment morning brief covering market indexes, hot sectors, portfolio diagnosis, macro and overseas-market context, operating suggestions, and weekly events.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reads portfolio details and can include holdings data in recurring reports.

Mitigation: Install only where the user controls the portfolio source, and avoid storing or sharing holdings data beyond the intended report.

Risk: The bundled configuration sends reports to a hard-coded Feishu recipient without a clear confirmation step.

Mitigation: Replace the hard-coded recipient with user-controlled configuration and require confirmation before outbound messages containing holdings data.

Risk: Broad triggers may cause the skill to run or send reports outside the intended morning-brief workflow.

Mitigation: Narrow the triggers before use so report generation and delivery happen only in the intended schedule or explicit user flow.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/horizoncove/skills/yuheng-morning-brief)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown morning brief with market tables, portfolio notes, event summaries, and action-oriented recommendations.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May be delivered as a Feishu private message when configured.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
