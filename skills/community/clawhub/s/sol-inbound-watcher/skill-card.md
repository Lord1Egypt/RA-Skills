## Description:

Watch a Solana address for inbound payments and alert via webhook or stdout so an agent can confirm customer payments without manually checking explorers.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kateryna-sprintcx](https://clawhub.ai/user/kateryna-sprintcx)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and workflow operators use this skill to configure and run a local Solana watcher that detects inbound native SOL payments and emits payment events to stdout or a webhook.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release advertises SOL/USDC detection, but the shipped code only confirms native SOL balance increases.

Mitigation: Use the skill only for native SOL deposits unless SPL token and USDC parsing is added and verified.

Risk: Reliable payment confirmation workflows can be affected by RPC behavior, partial transaction parsing, or missed token support.

Mitigation: Review the watcher before installation and validate payment events against your required confirmation policy before relying on them.

Risk: The optional install command does not pin the httpx dependency.

Mitigation: Pin dependencies in your environment before deployment.

Risk: Webhook events include wallet address and transaction details.

Mitigation: Send webhooks only to trusted endpoints and protect webhook URLs as sensitive configuration.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/kateryna-sprintcx/skills/sol-inbound-watcher)
- [Solana mainnet RPC endpoint](https://api.mainnet-beta.solana.com)

## Skill Output:

**Output Type(s):** [shell commands, configuration, JSON, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON event examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Emits JSON lines to stdout and can POST payment event details to a configured webhook.]

## Skill Version(s):

0.1.0 (source: server release metadata and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
