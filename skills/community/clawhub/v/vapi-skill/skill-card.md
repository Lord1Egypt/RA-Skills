## Description:

Manage Vapi voice assistants, calls, phone numbers, tools, and webhooks through Vapi REST API or CLI workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[colygon](https://clawhub.ai/user/colygon)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill to manage Vapi voice-agent resources, including assistants, calls, phone numbers, tools, and webhooks, from an OpenClaw agent.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review flags the optional Vapi CLI installer because it pipes a remote script directly into Bash.

Mitigation: Prefer REST API workflows or verify the installer source and expected local changes before running the CLI installer.

Risk: Assistant, model, voice, phone-number, webhook, and outbound-call changes can affect billing, privacy, and telephony behavior.

Mitigation: Use read-only list or get actions first, then confirm resource IDs, phone numbers, webhook URLs, consent, and recording constraints before applying changes.

Risk: Vapi API keys can grant access to voice-agent resources if exposed.

Mitigation: Store VAPI_API_KEY in a secret manager or environment variable and avoid printing it in public logs.

## Reference(s):

- [ClawHub Vapi Skill](https://clawhub.ai/colygon/skills/vapi-skill)
- [Vapi Docs Introduction](https://docs.vapi.ai/quickstart/introduction)
- [Vapi API Reference](https://api.vapi.ai/api)
- [Vapi CLI](https://github.com/VapiAI/cli)
- [Vapi MCP Docs](https://docs.vapi.ai/cli/mcp)
- [Vapi Example Server for Node](https://github.com/VapiAI/example-server-javascript-node)
- [OpenClaw](https://github.com/openclaw/openclaw)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, Code]

**Output Format:** [Markdown guidance with inline shell command and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires VAPI_API_KEY for API actions; supports REST API workflows by default and optional Vapi CLI workflows.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
