## Description:

Automates Zalo personal messaging, Official Account workflows, real-time listening, webhooks, and MCP client integration through the zalo-agent CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[phucmpham](https://clawhub.ai/user/phucmpham)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to draft safe zalo-agent commands and configuration for Zalo messaging, group operations, Official Account automation, webhook listeners, and MCP server access.

### Deployment Geography for Use:

Global, subject to Zalo account, Official Account, webhook, and local regulatory availability.

## Known Risks and Mitigations:

Risk: High-impact Zalo actions can send, recall, delete, export credentials, or forward message data.

Mitigation: Require explicit user confirmation before these actions, especially when messages, contact data, credentials, or bulk recipients are involved.

Risk: Credentials, app secrets, access tokens, cookies, proxy passwords, and exported credential files can expose account access.

Mitigation: Do not display credential contents or place secrets directly in commands; use secure transfer and restrictive file permissions when credentials must move between systems.

Risk: Public or plain HTTP QR, webhook, and remote MCP endpoints can expose login flows, message data, or agent controls.

Mitigation: Prefer local or authenticated endpoints, HTTPS, verified webhooks, bearer tokens for remote MCP, and narrow event filters.

Risk: Webhook and listen modes may forward personal or business communications to third-party systems.

Mitigation: Use only user-specified destinations, verify webhook receivers, avoid sensitive data by default, and document what event types are forwarded.

## Reference(s):

- [Zalo Agent CLI project homepage](https://github.com/PhucMPham/zalo-agent-cli)
- [Full Command Reference](references/command-reference.md)
- [Login Flow](references/login-flow.md)
- [Listen Mode Guide](references/listen-mode-guide.md)
- [Official Account Command Reference](references/oa-command-reference.md)
- [MCP Server Guide](references/mcp-guide.md)
- [Evaluation Scenarios](evals/eval-scenarios.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include commands that require human confirmation, local credentials, or explicit webhook and MCP endpoint choices.]

## Skill Version(s):

1.7.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
