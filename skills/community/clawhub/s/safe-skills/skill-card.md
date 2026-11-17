## Description:

Safe Skills helps agents create and manage EVM wallets, check balances, transfer tokens, and send transactions through a server-side secret management service without exposing raw private keys.

This skill is ready for commercial/non-commercial use.

## Publisher:

[glitch003](https://clawhub.ai/user/glitch003)

### License/Terms of Use:


## Use Case:

Developers and agent operators use this skill to let an agent work with EVM wallet operations while keeping wallet secrets server-side. It is suited for workflows that need wallet creation, balance checks, token transfers, or contract transactions with explicit controls around API keys and user approval.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can enable an agent to move funds or submit contract transactions.

Mitigation: Require explicit user approval with full transaction details before any transfer or contract interaction.

Risk: A returned API key can authorize future wallet actions.

Mitigation: Store API keys securely, treat them like wallet signing credentials, and do not expose them in logs or conversation.

Risk: Environment-configured service URLs could point to an untrusted endpoint.

Mitigation: Pin the SafeSkills API and frontend URLs to known trusted hosts before use.

## Reference(s):

- [Safe Skills release page](https://clawhub.ai/glitch003/skills/safe-skills)
- [glitch003 publisher profile](https://clawhub.ai/user/glitch003)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes API request examples, environment variable configuration, and operational safety guidance for wallet actions.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
