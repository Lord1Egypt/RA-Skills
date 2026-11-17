## Description:

Enable AI agents to register, create, send, sign, and verify legally binding e-signature agreements through SaySigned APIs, email delivery, and MCP workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[klsv](https://clawhub.ai/user/klsv)

### License/Terms of Use:


## Use Case:

Developers and agent operators use this skill to connect agents to SaySigned agreement workflows for registration, envelope creation, delivery, signing, decline, void, billing, usage, audit, and verification tasks. It is intended for contract workflows where human approval and careful secret handling are required before legally consequential actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Agent-driven agreement actions can create legally consequential signatures, declines, voids, sends, or billing events.

Mitigation: Require explicit human approval before every send, sign, decline, void, or billing action, and prefer email delivery when a human signer should review the agreement directly.

Risk: API keys and recipient access tokens can authorize sensitive account or signing actions if exposed.

Mitigation: Never place tokens in URLs, logs, prompts, or saved memory; store API keys only in approved configuration after confirmation and treat the embedded example API key as exposed.

Risk: MCP client configuration changes can persist credentials or alter agent connectivity.

Mitigation: Show proposed MCP configuration changes to the user and obtain confirmation before editing config files, storing API keys, or restarting the MCP client.

## Reference(s):

- [SaySigned ClawHub skill page](https://clawhub.ai/klsv/skills/saysigned)
- [SaySigned homepage](https://www.saysigned.com)
- [SaySigned documentation](https://www.saysigned.com/docs)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, API calls, Guidance]

**Output Format:** [Markdown guidance with JSON configuration snippets, shell commands, REST examples, and MCP tool schemas]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes API-key and access-token handling guidance, human approval steps for configuration changes, and examples for agreement workflows.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
