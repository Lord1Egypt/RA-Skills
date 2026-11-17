## Description:

Use when a user wants social media scheduling and publishing for AI agents on X, LinkedIn, Instagram, Facebook Pages, TikTok, Discord, Telegram, YouTube, Reddit, WordPress, and Pinterest through SocialClaw.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ndesv21](https://clawhub.ai/user/ndesv21)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to operate a SocialClaw workspace from an AI agent: connect social accounts, upload media, validate or preview scheduled posts and campaigns, apply publishing schedules, and inspect results.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can affect real public social accounts through live publishing actions.

Mitigation: Use test workspaces or accounts first and require explicit confirmation before applying schedules or publishing.

Risk: Workspace API keys, bot tokens, and webhook URLs may be exposed if pasted into chat or shell history.

Mitigation: Avoid echoing secrets, prefer environment variables or local credential storage, and redact sensitive values in agent responses.

Risk: The optional npm CLI executes as a separate client for the hosted service.

Mitigation: Install the CLI only from a trusted source, and prefer pinned or isolated installation when using it.

## Reference(s):

- [SocialClaw homepage](https://getsocialclaw.com)
- [SocialClaw ClawHub listing](https://clawhub.ai/ndesv21/skills/socialclaw)
- [SocialClaw workflows](references/workflows.md)
- [SocialClaw CLI](references/cli.md)
- [SocialClaw provider notes](references/providers.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, API calls, guidance]

**Output Format:** [Markdown guidance with shell commands, HTTP examples, and JSON schedule snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a SocialClaw workspace API key and an active trial or paid plan for live CLI/API execution.]

## Skill Version(s):

2.0.4 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
