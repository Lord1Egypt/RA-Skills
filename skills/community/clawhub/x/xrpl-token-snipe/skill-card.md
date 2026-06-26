## Description: <br>
Monitor XRPL for new token launches, verify issuer flags for safety, and execute fast token buys while managing XRP reserves to minimize risk. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[HarleysCodes](https://clawhub.ai/user/HarleysCodes) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and crypto trading operators use this skill to monitor XRPL token launches, inspect issuer and liquidity signals, and draft fast purchase flows for new tokens. It is intended for users who can evaluate transaction risk before acting on any generated guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide an agent toward live XRPL crypto trades and transaction submission. <br>
Mitigation: Require manual approval for every transaction and set explicit spend, slippage, and reserve limits before use. <br>
Risk: Wallet credentials or seed phrases could be exposed or over-scoped during trading workflows. <br>
Mitigation: Use a separate low-balance wallet and never expose a primary wallet seed phrase to the agent. <br>
Risk: New-token sniping can lead to losses from illiquid, unaudited, or malicious issuers. <br>
Mitigation: Audit issuer flags, liquidity, sellability, and token controls before approving any purchase. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/HarleysCodes/xrpl-token-snipe) <br>
- [FirstLedger REST API endpoint](https://xlrps-1.xrpl.link/api/v1/) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, code, configuration, guidance] <br>
**Output Format:** [Markdown with TypeScript code blocks and transaction guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include XRPL endpoint URLs, issuer-flag checks, wallet transaction examples, and reserve-management guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
