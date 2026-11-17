## Description:

Send SOL or SPL tokens on the Solana blockchain from OpenClaw agents for payments, rewards, or on-chain settlement.

This skill is ready for commercial/non-commercial use.

## Publisher:

[vortitron](https://clawhub.ai/user/vortitron)

### License/Terms of Use:


## Use Case:

Developers and agent operators use this skill when an OpenClaw agent needs to send SOL or SPL token payments, rewards, or settlements on Solana.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Agent-driven transfers can move real Solana funds immediately from a local wallet.

Mitigation: Use devnet or testnet first, keep only a low balance in a dedicated wallet, and require explicit per-transaction approval before using real funds.

Risk: Incorrect recipients or amounts can create irreversible payments.

Mitigation: Add recipient allowlists, spend caps, and strict amount validation before production use.

Risk: The skill depends on local keypair files and Solana JavaScript dependencies.

Mitigation: Protect the keypair file, use trusted RPC providers, and keep dependencies updated.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/vortitron/skills/solana-transfer)
- [Publisher profile](https://clawhub.ai/user/vortitron)
- [README](artifact/README.md)
- [Skill instructions](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JavaScript examples, shell commands, and JSON command output from the skill CLI.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [CLI commands and exported JavaScript functions can submit Solana transactions and return transaction signatures, balances, wallet addresses, or errors.]

## Skill Version(s):

0.1.0 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
