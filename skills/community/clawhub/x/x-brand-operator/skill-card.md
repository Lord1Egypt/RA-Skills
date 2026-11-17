## Description:

Automates X/Twitter brand account operations, including scheduled posting, keyword engagement, Substack draft generation, and weekly reporting using xurl with browser fallback.

This skill is ready for commercial/non-commercial use.

## Publisher:

[caoqi](https://clawhub.ai/user/caoqi)

### License/Terms of Use:

MIT-0

## Use Case:

Brand operators, social media teams, and developers use this skill to configure agent-run X/Twitter posting, engagement, reporting, and content drafting workflows for a brand account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Recurring cron tasks can publish, reply, like, and follow from a public brand account without timely review.

Mitigation: Review each schedule before enabling it and prefer dry-run or manual approval for posts and engagement until the workflow is trusted.

Risk: The browser fallback can act through a logged-in profile, which may target the wrong account if configuration is incorrect.

Mitigation: Use a dedicated xurl app and browser profile for the intended brand account, and confirm the Telegram recipient before scheduling unattended tasks.

Risk: Dynamic tweet, reply, and command arguments can be unsafe if passed through shell interpolation.

Mitigation: Pass dynamic arguments safely and review generated drafts before execution.

## Reference(s):

- [X Brand Operator on ClawHub](https://clawhub.ai/caoqi/skills/x-brand-operator)
- [Content Strategy](references/content-strategy.md)
- [Cron Job Configuration](references/cron-config.md)
- [Engagement Playbook](references/engagement-playbook.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands and JSON configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce public X/Twitter posts, replies, cron schedules, Telegram summaries, weekly reports, and Substack article drafts.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
