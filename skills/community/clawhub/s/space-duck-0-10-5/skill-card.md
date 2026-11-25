## Description:

Connects and manages Space Duck identity, trust, peck connections, chats, and Telegram integrations using a Beak Key.

This skill is ready for commercial/non-commercial use.

## Publisher:

[askegor](https://clawhub.ai/user/askegor)

### License/Terms of Use:

MIT-0

## Use Case:

Developers using agent runtimes can pair an agent with Space Duck, manage identity and trust, review connections and permissions, exchange messages, and optionally connect Telegram or MCP services.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: ClawScan marked the release suspicious after reporting weaknesses involving credentials, inbound message handling, file sharing, installation, and background activity; the scan was partial.

Mitigation: Review setup and message-handling behavior before use; keep credentials local, check connection permissions before sharing workspace files, and enable listeners, services, or automatic updates only when needed.

## Reference(s):

- [Space Duck API reference](references/api.md)
- [Connection ceremony](references/CONNECTION-CEREMONY.md)
- [MCP client specification](references/MCP-CLIENT-SPEC.md)
- [ClawHub release page](https://clawhub.ai/askegor/skills/space-duck-0-10-5)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration instructions, API calls, Status and activity summaries, Guidance]

**Output Format:** [CLI commands with text and JSON responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Actions depend on a paired Space Duck identity and any integrations enabled by the operator.]

## Skill Version(s):

0.10.5 (source: server-resolved release metadata, artifact/_meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
