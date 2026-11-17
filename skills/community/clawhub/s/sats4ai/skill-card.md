## Description:

Sats4AI connects agents to a Bitcoin Lightning-paid MCP marketplace for image, text, video, music, speech, 3D, vision, file conversion, and SMS tools.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cnghockey](https://clawhub.ai/user/cnghockey)

### License/Terms of Use:


## Use Case:

External developers and agent users use this skill to configure Sats4AI as an MCP server and route paid AI generation, analysis, conversion, and SMS tasks through Bitcoin Lightning micropayments.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Lightning wallet credentials or balances could be exposed to unintended spend.

Mitigation: Use a dedicated Lightning wallet with a small balance, strict payment limits, and revocable credentials, and require explicit confirmation before payments.

Risk: Remote file, prompt, or SMS handling could expose confidential or regulated data.

Mitigation: Do not send confidential files, secrets, sensitive prompts, or regulated data through the remote tools, and require explicit confirmation before SMS messages.

Risk: Wallet setup examples include unpinned package execution.

Mitigation: Avoid unpinned or automatic package execution where possible, and review or pin wallet MCP packages before use.

## Reference(s):

- [Sats4AI ClawHub listing](https://clawhub.ai/cnghockey/skills/sats4ai)
- [Sats4AI website](https://sats4ai.com)
- [Sats4AI OpenClaw guide](https://sats4ai.com/openclaw)
- [Sats4AI MCP docs](https://sats4ai.com/mcp)
- [Sats4AI L402 docs](https://sats4ai.com/l402)
- [Sats4AI service discovery](https://sats4ai.com/.well-known/l402-services)
- [Alby AI wallet setup](https://getalby.com/ai)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown instructions with JSON and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May guide agents to call remote paid MCP or L402 services that return generated media, text, analysis, converted files, or SMS delivery results.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
