## Description:

Helps an agent analyze complex tasks, generate multiple execution plans, request clarification when needed, and archive compact task reports for future planning.

This skill is ready for commercial/non-commercial use.

## Publisher:

[louisding9527](https://clawhub.ai/user/louisding9527)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to plan multi-step tasks, compare execution strategies, and preserve concise task outcomes that can inform future planning.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reads planning-resource files such as plan_source.md, which may contain sensitive paths, endpoints, credentials, or private project details.

Mitigation: Keep sensitive values out of plan_source.md unless they are intentionally available for agent planning.

Risk: The skill writes task reports under task_reports/, which may preserve operational context from previous tasks.

Mitigation: Review archived reports before sharing a workspace and remove private details that should not be reused in future planning.

## Reference(s):

- [ClawHub Skill Release Page](https://clawhub.ai/louisding9527/skills/task-plan-generator)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown plans and compact Markdown task reports with structured JSON data blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Task reports are intended to be concise, with a structured DATA block and a short human-readable SUMMARY.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
