## Description:

Helps agents manage WordPress.com posts, pages, and site content through a connected Maton account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[byungkyu](https://clawhub.ai/user/byungkyu)

### License/Terms of Use:

MIT-0

## Use Case:

WordPress.com site owners and their agents use this skill to inspect sites and create, update, or remove posts and pages with user approval. It also documents optional scheduled or event-driven actions through a connected Maton account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Connected account access can change, delete, or publish content on the wrong site.

Mitigation: Confirm the exact site, connection, and payload before each write, deletion, or publication.

Risk: Scheduled functions and triggers can repeat actions or forward data without a person present.

Mitigation: Require user approval for each function, trigger, and destination, including its scope and data flow.

Risk: A raw API key could be disclosed if used outside the CLI.

Mitigation: Prefer OAuth login through the CLI; use a raw key only when the CLI cannot be installed and never expose it in logs or commands.

## Reference(s):

- [ClawHub WordPress.com skill release](https://clawhub.ai/byungkyu/skills/wordpress-api)
- [Maton homepage](https://maton.ai)
- [WordPress.com REST API reference](https://developer.wordpress.com/docs/api/rest-api-reference/)
- [WordPress.com OAuth authentication](https://developer.wordpress.com/docs/oauth2/)
- [Maton CLI manual](https://cli.maton.ai/manual)
- [Time trigger reference](references/time/triggers.md)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Code, Configuration]

**Output Format:** [Markdown with inline code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only actions by default; confirm the target and payload before changes or automation.]

## Skill Version(s):

1.2.5 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
