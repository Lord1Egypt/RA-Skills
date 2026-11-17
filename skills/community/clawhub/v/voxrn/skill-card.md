## Description:

Place phone calls, send SMS, search contacts, and run agent dispatches via Voxrn. Bridges any OpenClaw-bridged chat (Slack, Telegram, iMessage, WhatsApp, Discord, more) to a real PSTN.

This skill is ready for commercial/non-commercial use.

## Publisher:

[robit-man](https://clawhub.ai/user/robit-man)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to connect Voxrn telephony tools to bridged chat agents so they can place calls, send SMS messages, search or update contacts, stream call transcripts, end calls, and check account balance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can place real phone calls, send SMS messages, end calls, and update contacts, which can affect external people and incur costs.

Mitigation: Require explicit user confirmation for destinations, message content, call termination, and expected costs before executing Voxrn tools.

Risk: The Voxrn bearer token is routed to a configurable endpoint.

Mitigation: Store VOXRN_API_KEY in OpenClaw secrets and keep VOXRN_BASE_URL unset or pinned to the trusted Voxrn HTTPS origin.

Risk: Task briefs, SMS bodies, contacts, and transcripts may contain sensitive content.

Mitigation: Avoid sending sensitive content unless necessary and confirmed, and review transcript or contact access according to workspace policy.

## Reference(s):

- [Voxrn](https://voxrn.com)
- [Voxrn docs - OpenClaw integration](https://voxrn.com/docs/integrations/openclaw)
- [Voxrn docs - MCP overview](https://voxrn.com/docs/agents/mcp)
- [Voxrn API reference](https://voxrn.com/docs/mcp)
- [OpenClaw outbound MCP servers](https://docs.openclaw.ai/cli/mcp)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline text, JSON tool-call examples, and bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires OpenClaw and a Voxrn API key; calls, SMS messages, contacts, transcripts, and balance checks can affect external users or account charges.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
