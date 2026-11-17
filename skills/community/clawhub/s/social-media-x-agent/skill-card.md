## Description:

Social Media Agent helps an agent manage X/Twitter posting, content generation, engagement, scheduling, and analytics using browser automation and OpenClaw-native tools.

This skill is ready for commercial/non-commercial use.

## Publisher:

[qq63523555](https://clawhub.ai/user/qq63523555)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to draft, schedule, publish, and track X/Twitter content for an authenticated account. It is intended for social media workflow assistance where the operator can review account activity and approve posts or schedules.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can publish, reply, quote, and schedule real X/Twitter activity for an authenticated account.

Mitigation: Use draft-only workflows by default and explicitly approve each post, reply, quote, and cron schedule before execution.

Risk: Scheduled posting can create persistent cron jobs that continue after the initial setup.

Mitigation: Track created schedules and verify that the operator knows how to list, review, and remove cron jobs.

Risk: Weak user-control boundaries could allow unintended account activity.

Mitigation: Require human review for account actions and limit automation to clearly scoped social media tasks.

## Reference(s):

- [Content Templates](references/content-templates.md)
- [X/Twitter](https://x.com/)
- [ClawHub Skill Page](https://clawhub.ai/qq63523555/skills/social-media-x-agent)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown instructions with inline command examples and JSON snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce draft social posts, engagement guidance, posting schedules, browser automation steps, and tracking data structures.]

## Skill Version(s):

1.1.0 (source: server release evidence and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
