## Description:

Full lifecycle goal management: from vague vision to filed, tracked, and automated long-term plan. 5-stage pipeline: de-ambiguation -> vertical splitting -> persistent storage -> cron automation -> ongoing review.

This skill is ready for commercial/non-commercial use.

## Publisher:

[joeyxin-del](https://clawhub.ai/user/joeyxin-del)

### License/Terms of Use:

MIT-0

## Use Case:

External users and productivity-focused agents use this skill to clarify vague long-term goals, split them into milestones and atomic tasks, persist plans as Markdown files, generate reminder payloads, and review progress over time.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Goal plans, progress metrics, and review notes can include sensitive personal, financial, health, or workplace details saved locally and referenced across sessions.

Mitigation: Avoid storing secrets or highly sensitive details unless the user understands where files and memory pointers are kept; periodically review and delete local plan files that are no longer needed.

Risk: Recurring reminders can surface outdated or overly specific goal context after circumstances change.

Mitigation: Review reminder payloads before enabling them and update or disable recurring reminders when the plan changes.

Risk: The included Shenzhen financial planning reference contains time-sensitive rates and calculation assumptions.

Mitigation: Verify financial, tax, social insurance, and housing fund values against current official sources before using them for decisions.

## Reference(s):

- [Shenzhen Financial Planning](references/shenzhen-financial-planning.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown plans, conversational text, JSON cron payloads, and CLI output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Persists goal plans and progress notes to local Markdown files when the workflow saves or updates a plan.]

## Skill Version(s):

2.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
