## Description:

Automates social media content generation, scheduling, publishing, interaction monitoring, and reply drafting for Xiaohongshu, Weibo, and Twitter.

This skill is ready for commercial/non-commercial use.

## Publisher:

[openlark](https://clawhub.ai/user/openlark)

### License/Terms of Use:

MIT-0

## Use Case:

External social media operators and developers use this skill to plan topics, generate platform-specific content, schedule posts, prepare publishing commands, monitor interactions, and draft replies across Xiaohongshu, Weibo, and Twitter.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Publishing and reply workflows can affect real public social media accounts.

Mitigation: Use dry-run and manual review by default, and publish only after confirming content, platform, account, and timing.

Risk: Scheduled jobs and generated command messages may contain unsafe scheduling or command construction patterns.

Mitigation: Review the full scheduled agent message and command text before registering or executing cron jobs.

Risk: Untrusted content files or weekly plan files can drive generated posts, replies, or schedules.

Mitigation: Use only trusted and reviewed content or plan files, and validate them before publishing or scheduling.

Risk: Social platform credentials and tokens can be exposed through logs or generated API request details.

Mitigation: Keep credentials in environment variables, avoid logging secrets, and rotate any Weibo token that may have appeared in logs.

## Reference(s):

- [Content Strategy and Topic Selection Methodology](references/content-strategy.md)
- [Reply Template Library](references/reply-templates.md)
- [Twitter (X) Operations Guide](references/twitter-guide.md)
- [Weibo Operations Guide](references/weibo-guide.md)
- [Xiaohongshu Complete Operations Guide](references/xiaohongshu-guide.md)
- [Xiaohongshu Creator Publishing Page](https://creator.xiaohongshu.com/publish/publish)
- [Weibo](https://weibo.com)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance, JSON content plans and reports, and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces platform-specific content plans, dry-run previews, browser/API command descriptions, cron job configuration, and monitoring reports.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
