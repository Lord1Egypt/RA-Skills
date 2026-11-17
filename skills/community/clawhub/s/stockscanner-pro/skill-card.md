## Description:

Social media automation agent that generates, schedules, publishes, and optionally replies to posts for Twitter, Weibo, and Xiaohongshu.

This skill is ready for commercial/non-commercial use.

## Publisher:

[anson125chen](https://clawhub.ai/user/anson125chen)

### License/Terms of Use:

MIT-0

## Use Case:

External creators, marketers, and operators use this agent to draft, queue, publish, and review scheduled social posts across supported platforms. It can be run manually or via cron after platform credentials are configured.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Configured API keys, tokens, and cookies can grant access to social accounts.

Mitigation: Store credentials outside shared repositories, restrict account privileges where possible, and rotate tokens if exposed.

Risk: Scheduled cron execution can publish queued public posts without a fresh confirmation.

Mitigation: Enable cron only for accounts and workflows where unattended posting is acceptable; review queued tasks before scheduled run windows.

Risk: Generated posts or auto-replies may be inaccurate, off-brand, or inappropriate for public channels.

Mitigation: Require human review for generated content and comment reply rules before publication.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/anson125chen/skills/stockscanner-pro)
- [Project website](https://asmartglobal.com)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with JSON configuration and shell command examples; runtime script output is plain text.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May queue scheduled public posts and write task state under the skill data directory.]

## Skill Version(s):

1.0.0 (source: release metadata, SKILL.md frontmatter, package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
