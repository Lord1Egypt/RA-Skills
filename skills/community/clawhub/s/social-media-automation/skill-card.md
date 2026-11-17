## Description:

A CLI skill for managing social-media posting, scheduling, drafts, templates, timelines, interactions, and rate-limit-aware account workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hirofumiko](https://clawhub.ai/user/hirofumiko)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and social-media operators use this skill to configure and run a CLI for drafting, posting, scheduling, templating, viewing timelines, monitoring mentions, and performing account interactions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can use social-media credentials to act on live accounts.

Mitigation: Use least-privilege API credentials, keep the .env file private, and rotate tokens if configuration output has been logged.

Risk: Commands can post, like, retweet, delete, or schedule actions against account content.

Mitigation: Verify account, platform, post, and target IDs before executing account-changing commands.

Risk: The security guidance flags the undocumented Discord and Telegram integration as unresolved.

Mitigation: Avoid the Discord and Telegram integration until its file-upload and webhook scoping issues are fixed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/hirofumiko/skills/social-media-automation)
- [README](artifact/README.md)
- [Skill documentation](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown and terminal-oriented text with inline shell commands and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May guide creation of local .env settings, SQLite-backed drafts, templates, scheduled jobs, and social-media account actions when commands are executed.]

## Skill Version(s):

0.1.1 (source: server release metadata; pyproject.toml reports 0.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
