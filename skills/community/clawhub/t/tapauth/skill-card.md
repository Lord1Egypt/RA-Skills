## Description:

TapAuth helps OpenClaw agents request OAuth tokens or user-entered secrets through browser approval and use them through OpenClaw's exec secrets provider.

This skill is ready for commercial/non-commercial use.

## Publisher:

[schwartzdev](https://clawhub.ai/user/schwartzdev)

### License/Terms of Use:

MIT

## Use Case:

Developers and agent operators use TapAuth to configure delegated OAuth and manual secret access for OpenClaw agents without putting credentials directly in command lines or configuration files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Direct token retrieval examples can expose OAuth tokens if copied into shell commands, logs, or process output.

Mitigation: Use the OpenClaw exec secrets provider and SecretRef configuration for normal operation, and avoid command substitution or inline token use.

Risk: Broad OAuth scopes can grant more access than the task requires.

Mitigation: Request the narrowest provider scopes that satisfy the task and revoke grants when access is no longer needed.

Risk: Shared workspaces or exposed cache and environment data may reveal grant material.

Mitigation: Set TAPAUTH_HOME to a private directory, keep TAPAUTH_BASE_URL unset outside tests, and revoke grants if the cache or process environment may have been exposed.

## Reference(s):

- [TapAuth Skill on ClawHub](https://clawhub.ai/schwartzdev/skills/tapauth)
- [TapAuth Website](https://tapauth.ai)
- [TapAuth Documentation](https://tapauth.ai/docs)
- [OpenClaw Integration](references/openclaw.md)
- [GitHub via TapAuth](references/github.md)
- [Google Workspace via TapAuth](references/google.md)
- [Gmail via TapAuth](references/gmail.md)
- [Slack OAuth Provider](references/slack.md)
- [Linear via TapAuth](references/linear.md)
- [Notion via TapAuth](references/notion.md)
- [Vercel via TapAuth](references/vercel.md)
- [Sentry OAuth Provider](references/sentry.md)
- [Asana OAuth Provider](references/asana.md)
- [Discord OAuth Provider](references/discord.md)
- [Apify via TapAuth](references/apify.md)
- [Atlassian OAuth Provider](references/atlassian.md)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration]

**Output Format:** [Markdown instructions with JSON and bash examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes provider-specific scope references and OpenClaw SecretRef configuration guidance.]

## Skill Version(s):

1.0.6 (source: CHANGELOG.md released 2026-06-23, package.json, skill.json, ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
