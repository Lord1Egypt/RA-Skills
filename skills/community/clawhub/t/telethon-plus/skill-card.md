## Description:

Provides HTTP and MCP tools for an already-authorized Telegram user account, including messaging, chat management, media, polls, and incoming-event forwarding.

This skill is ready for commercial/non-commercial use.

## Publisher:

[psyb0t](https://clawhub.ai/user/psyb0t)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use the skill to read and manage chats, send messages or media, and handle Telegram events through an instance connected to their own authorized account. The account has full read, write, and admin access.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The connected Telegram account has full read, write, and admin access, so actions can expose private messages or visibly change chats.

Mitigation: Use only an account the operator owns or is authorized to operate, and confirm the exact target before destructive or administrative actions.

Risk: An exposed API or MCP endpoint can give reachable clients control of the Telegram account, especially when authentication is unset.

Mitigation: Set TELETHON_AUTH_KEY, bind to loopback or use a TLS-protected reverse proxy, and keep the API and MCP endpoints away from untrusted networks and agents.

Risk: Server-side fetching of file_url values can reach internal network addresses, and an incoming-event webhook forwards message content and account activity.

Mitigation: Pass only trusted HTTPS file URLs and configure webhooks only to trusted endpoints under the operator's control.

Risk: ClawScan rates the skill suspicious, citing account-access examples, mutable Docker images, and a shell-scope mismatch; the scan is partial.

Mitigation: Review the setup and script behavior, pin the container image to a trusted version or digest, and verify authentication and exposure settings before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/psyb0t/skills/telethon-plus)
- [Project homepage listed in skill metadata](https://github.com/psyb0t/docker-telethon-plus)
- [Setup and deployment guidance](references/setup.md)
- [Telethon](https://codeberg.org/Lonami/Telethon)
- [Model Context Protocol streamable HTTP transport specification](https://modelcontextprotocol.io/specification/2025-03-26/basic/transports#streamable-http)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Configuration instructions, Shell commands]

**Output Format:** [JSON HTTP requests and MCP tool calls, with Markdown setup guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Actions operate through the connected Telegram account; setup commands are operator-side.]

## Skill Version(s):

0.7.4 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
