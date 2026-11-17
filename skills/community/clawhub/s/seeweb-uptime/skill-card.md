## Description:

Monitors websites, APIs, and cron jobs using Watch.dog and helps agents review uptime status, manage monitors, and configure watchdogs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[robinson0594](https://clawhub.ai/user/robinson0594)

### License/Terms of Use:

MIT

## Use Case:

Developers, operators, and site reliability teams use this skill to connect an agent to Watch.dog for website, API, port, and cron-job monitoring. It supports checking infrastructure health, creating monitors or watchdogs, pausing or resuming monitors, deleting resources after confirmation, and updating public status pages.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles Watch.dog credentials and may store them in local configuration.

Mitigation: Use platform-managed secrets or environment variables instead of chat-provided plaintext .env storage whenever possible.

Risk: The skill can create, pause, resume, publish, and delete monitoring resources in the connected Watch.dog account.

Mitigation: Install only when the Watch.dog endpoint is trusted, keep WATCHDOG_API_URL pinned to the official endpoint unless a trusted deployment is intended, and review account-changing actions before execution.

Risk: Monitor and watchdog deletion can remove resources from the connected account.

Mitigation: Require explicit user confirmation before delete_monitor or delete_watchdog is invoked.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/robinson0594/skills/seeweb-uptime)
- [ClawHub publisher profile](https://clawhub.ai/user/robinson0594)
- [Watch.dog](https://watch.dog)
- [Watch.dog MCP API endpoint](https://api.watch.dog/api/mcp_server.php)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown text with command snippets, configuration values, and monitoring results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node and Watch.dog credentials through WATCHDOG_API_KEY and WATCHDOG_API_URL.]

## Skill Version(s):

1.0.5 (source: frontmatter, package.json, release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
