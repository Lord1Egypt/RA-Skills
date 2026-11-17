## Description:

Tracks rule, guideline, and constraint compliance so agents can generate task-level rule compliance reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[renyuan000](https://clawhub.ai/user/renyuan000)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to record rule triggers, compliance, and violations during tasks, then generate concise reports for self-review and process improvement.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may create recurring local compliance reports and memory entries when enabled.

Mitigation: Use it only when task-level rule tracking is desired, and disable or narrow auto-trigger behavior when routine task metadata should not be recorded.

Risk: Compliance reports can reflect incomplete or subjective manual rule labels.

Mitigation: Review generated reports before using them to revise agent rules or assess execution quality.

## Reference(s):

- [Rules Tracker skill page](https://clawhub.ai/renyuan000/skills/rules-tracker)
- [Publisher profile](https://clawhub.ai/user/renyuan000)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Markdown reports with rule tables and concise recommendations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce recurring local memory entries named memory/rules-tracker-{YYYY-MM-DD}.json when enabled.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
