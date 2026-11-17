## Description:

Monitors Solana perpetual DEX funding rates and helps agents identify, simulate, and optionally run funding-rate arbitrage workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[guohongbin-git](https://clawhub.ai/user/guohongbin-git)

### License/Terms of Use:

MIT

## Use Case:

External users and developers use this skill to scan Solana perpetual DEX funding rates, compare cross-exchange opportunities, run dry-run simulations, and configure cautious execution workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Live-trading and scheduled execution paths could put wallet funds at risk.

Mitigation: Keep the skill in scan or dry-run mode unless live-trading paths have been audited and fixed.

Risk: Wallet secrets used with unattended cron execution can increase loss or exposure risk.

Mitigation: Use a dedicated low-balance wallet and avoid unattended cron jobs that have access to wallet secrets.

Risk: Advertised risk controls may not fully protect against trading losses.

Mitigation: Do not rely on built-in controls as complete protection; review behavior carefully before any funded use.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/guohongbin-git/skills/solana-funding-arb-cn)
- [Publisher Profile](https://clawhub.ai/user/guohongbin-git)
- [OpenClaw Metadata Link](https://clawhub.ai)
- [API Reference](references/api.md)
- [Setup Guide](references/setup.md)
- [Strategy Guide](references/strategies.md)
- [Drift Protocol Docs](https://docs.drift.trade)
- [Flash Trade](https://flash.trade)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands, configuration snippets, and TypeScript code references]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes scanner output, dashboard instructions, dry-run workflows, and live-trading configuration guidance.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
