## Description:

Schedulala helps agents install and use Schedulala to connect social accounts, draft, validate, schedule, publish, and review social media posts across supported platforms.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ameera48](https://clawhub.ai/user/ameera48)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to connect Schedulala to an agent workflow, plan social content, create drafts, preview or validate posts, publish after confirmation, and inspect analytics, comments, and keyword feeds.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks agents to install mutable npm tools.

Mitigation: Prefer pinned package versions and review the package before enabling it in sensitive environments.

Risk: The skill handles account-linked social publishing credentials and live API keys.

Mitigation: Use test keys or drafts first, avoid placing real passwords or tokens in chat or command arguments, and keep OAuth and payment flows in the Schedulala browser experience.

Risk: Publishing, replies, moderation, and bulk actions can change public social accounts.

Mitigation: Require explicit user confirmation before posting, replying, hiding comments, or running bulk actions, and validate or preview drafts before publishing.

## Reference(s):

- [Schedulala developer docs](https://schedulala.com/developers/docs)
- [Schedulala homepage](https://schedulala.com)
- [ClawHub skill page](https://clawhub.ai/ameera48/skills/schedulala)
- [CLI reference](references/cli.md)
- [Hosted connector widgets](references/connector-widgets.md)
- [Media reference](references/media.md)
- [Per-platform settings reference](references/platforms.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose CLI, MCP connector, account setup, media upload, validation, scheduling, publishing, analytics, engagement, and monitoring steps.]

## Skill Version(s):

1.1.0 (source: SKILL.md frontmatter, evidence release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
