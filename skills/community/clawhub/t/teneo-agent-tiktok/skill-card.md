## Description:

The TikTok Agent helps users retrieve TikTok video metrics, creator profile details, and hashtag post data for trend analysis and creator auditing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[teneoprotocoldev](https://clawhub.ai/user/teneoprotocoldev)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, agents, businesses, and researchers use this skill to access TikTok video, profile, and hashtag data through the Teneo SDK for analytics, audits, and trend monitoring.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup installs an unpinned SDK package.

Mitigation: Pin package versions, commit a lockfile, and review dependency changes before running the SDK.

Risk: The workflow uses automatic USDC wallet payments.

Mitigation: Use a dedicated low-balance wallet and require explicit confirmation for every payment.

Risk: Wallet transactions can be signed on multiple supported networks.

Mitigation: Verify the destination, network, asset, amount, and fees before signing any transaction.

Risk: Broad environment secrets could be exposed to the Node process running the SDK.

Mitigation: Scope environment variables narrowly and avoid loading unrelated secrets into the SDK runtime.

## Reference(s):

- [Tiktok - powered by Teneo Protocol on ClawHub](https://clawhub.ai/teneoprotocoldev/skills/teneo-agent-tiktok)
- [Teneo Agent SDK on ClawHub](https://clawhub.ai/teneoprotocoldev/teneo-agent-sdk)
- [Teneo Protocol](https://teneo-protocol.ai)
- [@teneo-protocol/sdk on npm](https://www.npmjs.com/package/@teneo-protocol/sdk)
- [Teneo Agent SDK GitHub Repository](https://github.com/TeneoProtocolAI/teneo-agent-sdk)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown instructions with TypeScript examples, shell commands, and structured response guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The referenced agent can return formatted text or raw structured content through the Teneo SDK.]

## Skill Version(s):

1.0.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
