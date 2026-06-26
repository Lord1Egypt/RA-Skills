## Description: <br>
Track the performance of Uniswap LP positions over time — check which positions need attention, are out of range, or have uncollected fees. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wpank](https://clawhub.ai/user/wpank) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users with existing Uniswap liquidity positions use this skill to review position health, fee accumulation, out-of-range status, and action items across wallet, chain, and time-window filters. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill is primarily read-only, but its artifact guidance references configuring a private key when no wallet is configured. <br>
Mitigation: Use a public wallet address or another clearly read-only data source for tracking. Do not provide a private key unless the portfolio analysis environment is fully trusted and transaction signing is explicitly prevented. <br>
Risk: Performance, fee, and range data may be delayed by RPC or subgraph synchronization. <br>
Mitigation: Treat summaries and action items as decision support and verify current on-chain data before rebalancing, collecting fees, or taking other financial action. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wpank/track-performance) <br>
- [README](artifact/README.md) <br>
- [Skill specification](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance] <br>
**Output Format:** [Markdown performance summary with position status, fee notes, value changes, and actionable alerts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports optional wallet, chain, and time-window filters; action items are suggestions and not automatic transactions.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
