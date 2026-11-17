## Description:

Role-based social media operations skill for structured social campaigns, including opportunity scouting, content pipeline management, posting, responding, and performance review.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dougbtv](https://clawhub.ai/user/dougbtv)

### License/Terms of Use:

Apache 2.0

## Use Case:

External users and developers use this skill to run auditable social media operations through scoped roles for strategy, research, content creation, publishing, engagement, and analysis. It is intended for agents building long-term presence, launching products, growing communities, or positioning themselves as domain authorities.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Scheduled agents may post or reply publicly on the user's behalf without close supervision.

Mitigation: Use dry-run before enabling cron jobs, keep the Poster limited to one item per run, and review queued posts before scheduled publishing.

Risk: The skill can read configured local files while preparing content and strategy.

Mitigation: Restrict Local-File-References.md to approved non-sensitive files, maintain explicit exclusions, and log skipped or unreadable references.

Risk: Posting credentials or account authority could permit unintended social actions.

Mitigation: Use least-privilege credentials, confirm identity before posting, and keep role boundaries that prevent Scout, Researcher, Content Specialist, Writer, and Analyst from posting.

Risk: Repeated cron installation could create duplicate or stale scheduled jobs.

Mitigation: Use the installer dry-run and check existing cron jobs after installation or updates.

## Reference(s):

- [Social Ops configuration guide](Guidance/CONFIGURATION-GUIDE.md)
- [Role input/output map](references/ROLE-IO-MAP.md)
- [Cron installation guide](references/crons/InstallCrons.md)
- [Local file references template](references/LOCAL-FILE-REFERENCES-TEMPLATE.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance, markdown workspace files, and shell commands for optional cron setup]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces role-scoped plans, logs, content files, recommendations, and posting actions through the configured social workspace.]

## Skill Version(s):

0.0.13 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
