## Description:

Helps users clarify, break down, and schedule long-term goals into manageable tasks with reminders and progress tracking.

This skill is ready for commercial/non-commercial use.

## Publisher:

[joeyxin-del](https://clawhub.ai/user/joeyxin-del)

### License/Terms of Use:

MIT-0

## Use Case:

Individuals and productivity-focused agents use this skill to turn vague long-term goals into clarified plans, milestone and task breakdowns, scheduling payloads, and progress status updates.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Plan files and scheduling payloads may contain personal goals, timelines, and task context.

Mitigation: Review and redact plan Markdown and scheduling JSON before sharing them or importing them into automation tools.

Risk: Scheduling payloads may become stale when plans change or tasks are missed.

Mitigation: Review generated cron configuration and realign the plan before enabling or updating automated reminders.

Risk: Chinese-first prompts may be hard for non-Chinese users to follow.

Mitigation: Translate or adapt prompts before use when the user or deployment context requires another language.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/joeyxin-del/skills/secretaryskills)
- [SKILL.md](artifact/SKILL.md)
- [README.md](artifact/README.md)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Conversational text, Markdown plan files, status reports, and JSON scheduling payloads.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May save local plan files under a configurable plans directory when the user chooses to persist a plan.]

## Skill Version(s):

1.0.2 (source: server release metadata; artifact frontmatter says 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
