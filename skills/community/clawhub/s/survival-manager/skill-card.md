## Description:

Survival Manager helps an agent monitor balance-based operating tiers, heartbeat checks, authorization requests, finances, and agent coordination.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fffdz](https://clawhub.ai/user/fffdz)

### License/Terms of Use:

MIT License

## Use Case:

External users and developers use this skill to have an agent produce survival status reports, authorization requests, finance updates, and task coordination guidance. It is intended for workflows where high-risk actions remain subject to user approval.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requests broad autonomous inspection of local files, browser state, messages, calendars, business accounts, and balance data.

Mitigation: Limit the files, accounts, browser origins, APIs, and notification channels available to the agent before enabling the skill.

Risk: Sensitive local or account-linked data could be sent to models, search, APIs, or Telegram during autonomous operation.

Mitigation: Require fresh user approval before reading sensitive account data or sending any data to external models, search providers, APIs, or notification channels.

Risk: The server security verdict is suspicious because the requested autonomy is broader than the documented scoping and controls.

Mitigation: Use a pinned, reviewed package version and review authorization rules before allowing the skill to run recurring checks.

## Reference(s):

- [Survival Manager ClawHub listing](https://clawhub.ai/fffdz/skills/survival-manager)
- [fffdz publisher profile](https://clawhub.ai/user/fffdz)
- [OpenClaw documentation](https://docs.openclaw.ai)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown reports with shell or PowerShell command examples and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include balance, tier, cost, authorization, notification, and next-check fields.]

## Skill Version(s):

1.0.0 (source: server release metadata and clawdbot frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
