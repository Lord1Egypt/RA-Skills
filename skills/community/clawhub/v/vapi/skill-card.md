## Description:

Manage Vapi voice assistants, calls, phone numbers, tools, and webhooks via the Vapi REST API or CLI for voice agent operations and integrations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[colygon](https://clawhub.ai/user/colygon)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill to manage Vapi voice agent resources, including assistants, calls, phone numbers, tools, and webhooks, through REST helper commands or the Vapi CLI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The documented Vapi CLI installation path pipes a remote shell script into bash.

Mitigation: Prefer the bundled REST helper or independently verify the installer source before using the CLI installer.

Risk: The helper can send VAPI_API_KEY to a user-controlled API base URL when VAPI_BASE_URL is changed.

Mitigation: Leave VAPI_BASE_URL unset except in a controlled test environment and keep VAPI_API_KEY narrowly scoped where possible.

Risk: The skill can create outbound calls and alter phone number or webhook routing.

Mitigation: Require explicit approval before initiating calls or changing phone number and webhook configuration.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/colygon/skills/vapi)
- [Vapi Docs Introduction](https://docs.vapi.ai/quickstart/introduction)
- [Vapi API Reference](https://api.vapi.ai/api)
- [Vapi CLI](https://github.com/VapiAI/cli)
- [Vapi MCP Docs](https://docs.vapi.ai/cli/mcp)
- [Vapi Example Server for Node.js](https://github.com/VapiAI/example-server-javascript-node)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires VAPI_API_KEY; REST helper commands can perform read and write operations against Vapi resources.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
