## Description:

Uandai Ai helps agents configure Uandai API access, package OpenClaw workspace ZIPs, upload and manage trainer-owned agents, list subscriptions, and invoke runs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[uandai](https://clawhub.ai/user/uandai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, agent trainers, and subscribers use this skill to package OpenClaw agents for Uandai, exchange API keys for session tokens, upload and revise agent listings, inspect subscriptions, invoke runs, and access subscribed agents through the OpenClaw gateway.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Linux/macOS packaging commands may include private key or certificate files in an uploaded workspace ZIP.

Mitigation: Add exclusions for id_rsa, id_dsa, *.p12, and *.crt, then inspect and validate the final ZIP before upload.

Risk: The Uandai API key is a sensitive local credential.

Mitigation: Use a private setup session, avoid echoing or logging the full key, and exchange it for access tokens before business API calls.

Risk: Publishing and delete operations can change or remove trainer-owned agents.

Mitigation: Confirm the intended agent id, revision, and action with the user before submitting proposals, publishing, or deleting agents.

## Reference(s):

- [Uandai Programmatic API docs](https://api.uandai.ai/docs/programmatic-api)
- [Uandai Agent Packaging Guide](artifact/references/agent-packaging.md)
- [Uandai OpenClaw Integration Guide](artifact/references/openclaw-integration.md)
- [Uandai Programmatic API Guide](artifact/references/programmatic-api.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, API calls, guidance]

**Output Format:** [Markdown with inline shell, HTTP, and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce workspace ZIP paths, API request guidance, command sequences, JSON request bodies, response summaries, and configuration updates.]

## Skill Version(s):

1.0.11 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
