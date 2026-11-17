## Description:

Solana trading and DeFi skill for AI agents that uses the SoulPass CLI for hardware-secured Solana wallets, Jupiter swaps and lending, token risk checks, trading bots, and SOL/SPL payments.

This skill is ready for commercial/non-commercial use.

## Publisher:

[soulpassai](https://clawhub.ai/user/soulpassai)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and agent operators use this skill to let agents manage Solana wallet operations, swaps, lending, payments, copy-trading workflows, and agent-commerce flows through SoulPass. It is intended for agents that need guidance and command patterns for financial actions on Solana.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can manage real crypto funds on Solana.

Mitigation: Start on devnet or an empty low-value wallet, verify balances before transactions, and require owner approval and spending limits before financial automation.

Risk: The install paths use external CLI installation and one source path includes sudo.

Mitigation: Review the CLI source, pin and verify the exact version before installation, and avoid the sudo source install path when possible.

Risk: The daemon and message listener can enable autonomous financial actions.

Mitigation: Do not run the daemon or message listener unless local approvals, spending limits, and monitoring are in place.

Risk: The public diary feature could expose private session details.

Mitigation: Disable or ignore public diary behavior unless the operator explicitly wants those details published.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/soulpassai/skills/soulpass)
- [SoulPass Homepage](https://soulpass.ai)
- [DeFi & Trading Cookbook](references/defi-cookbook.md)
- [Agent Commerce Guide](references/merchant-guide.md)
- [Diary Voice Guide](references/diary-voice.md)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown guidance with inline bash, JSON, and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands generally invoke the soulpass CLI and may output JSON from the underlying tool.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
