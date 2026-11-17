## Description:

Automates weekly Substack draft generation from a topic queue, saves local Markdown and JSON state, opens the Substack editor for human review, and sends Telegram status notifications.

This skill is ready for commercial/non-commercial use.

## Publisher:

[caoqi](https://clawhub.ai/user/caoqi)

### License/Terms of Use:

MIT-0

## Use Case:

External creators, newsletter operators, and developers use this skill to generate weekly Substack article drafts from a managed topic queue while keeping publishing approval manual.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Recurring autonomous runs can modify local topic queues, logs, and draft files.

Mitigation: Configure a dedicated workspace path, review local state before scheduling, and keep publication manual.

Risk: Browser and Telegram actions can target the wrong Substack publication or recipient if configured incorrectly.

Mitigation: Verify the Substack publication, browser profile, and Telegram recipient before enabling the workflow.

Risk: An unattended cron job with no finite timeout can continue longer than intended.

Mitigation: Set a finite timeout and document how to disable or delete the cron job before enabling it.

## Reference(s):

- [Article Angle Frameworks](references/article-angles.md)
- [Cron Job Prompt Template](references/cron-prompt-template.md)
- [Substack Autopilot ClawHub Listing](https://clawhub.ai/caoqi/skills/substack-autopilot)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Configuration, Guidance]

**Output Format:** [Markdown draft content with JSON state updates, browser review instructions, and concise status notifications]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires human review before publishing; recurring execution should use scoped workspace paths and a finite timeout.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
