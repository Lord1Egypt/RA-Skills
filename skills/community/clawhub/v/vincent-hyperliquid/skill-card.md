## Description:

Use this skill to create and operate a Vincent-managed HyperLiquid perpetuals and spot wallet for an agent, including balances, transfers, withdrawals, market data, orders, and trading rules without exposing private keys to the agent.

This skill is ready for commercial/non-commercial use.

## Publisher:

[glitch003](https://clawhub.ai/user/glitch003)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to guide an agent through creating, claiming, funding, and operating a Vincent-managed HyperLiquid wallet. The skill supports trading workflows, balance checks, USDC transfers, withdrawals, order management, and automated stop-loss, take-profit, or trailing-stop rules.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can lead an agent to perform real HyperLiquid trades, transfers, withdrawals, cancel-all actions, and automated trading rules.

Mitigation: Use low wallet limits, require human approval for sensitive actions, test with small amounts first, and monitor wallet activity from the Vincent interface.

Risk: The security evidence flags repeated use of an unpinned latest npm CLI for real fund movements and automated trading actions.

Mitigation: Prefer a pinned and reviewed @vincentai/cli version, and run commands in a sandbox with only the wallet credential access required for the task.

Risk: Loss, revocation, or misuse of scoped API access can interrupt or alter wallet operations.

Mitigation: Have the wallet owner revoke keys when needed, use the documented re-link flow for recovery, and avoid exposing raw secret material to the agent.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/glitch003/skills/vincent-hyperliquid)
- [Publisher Profile](https://clawhub.ai/user/glitch003)
- [Vincent Homepage](https://heyvincent.ai)
- [HyperLiquid Portfolio](https://app.hyperliquid.xyz/portfolio)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with bash command examples and JSON response examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands use @vincentai/cli and generally return JSON to stdout.]

## Skill Version(s):

1.0.70 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
