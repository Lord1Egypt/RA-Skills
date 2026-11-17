## Description:

Configure, validate, and troubleshoot a Session Messenger to n8n to OpenClaw bridge for two-way text messaging and image exchange when the hosted relay supports attachments.

This skill is ready for commercial/non-commercial use.

## Publisher:

[droidhackzor](https://clawhub.ai/user/droidhackzor)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to configure, validate, and troubleshoot the n8n and OpenClaw side of a Session Messenger relay. It helps import or patch an n8n workflow, verify relay endpoints, check attachment support, and prepare the bridge for reuse or publication.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Relay API keys and message content may be sent over under-scoped or plaintext network paths.

Mitigation: Use only trusted HTTPS relay and OpenClaw endpoints, and store relay API keys in a credential manager instead of command lines or exported workflow JSON.

Risk: The relay validator can make a real test POST to /send.

Mitigation: Run validation against non-production systems, or only when a test send to the target relay is acceptable.

Risk: An enabled n8n workflow can poll messages and send replies through the relay.

Mitigation: Enable the workflow only after confirming the allowed sender, relay host, credential scope, OpenClaw endpoint payload, and message-sending behavior.

## Reference(s):

- [Session OpenClaw Bridge ClawHub Page](https://clawhub.ai/droidhackzor/skills/session-openclaw-bridge)
- [OpenClaw Session Relay Workflow](references/openclaw-session-relay-workflow.json)
- [Release Notes](references/release.md)
- [Relay Validation Script](scripts/validate_relay.py)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON workflow references and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include relay readiness summaries, endpoint checks, n8n workflow configuration guidance, and packaging steps.]

## Skill Version(s):

0.1.0 (source: release evidence and references/release.md)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
