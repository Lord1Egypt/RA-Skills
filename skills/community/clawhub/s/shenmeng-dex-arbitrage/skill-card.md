## Description: <br>
DEX arbitrage assistant that helps users identify cross-DEX and cross-chain price differences, calculate profitability, design automation, and reason about execution risks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[shenmeng](https://clawhub.ai/user/shenmeng) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to evaluate DEX arbitrage opportunities, calculate costs and net profit, draft monitoring or automation code, and review MEV, bridge, wallet, and smart-contract risks before acting. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill supports real-money crypto workflows involving funded wallets, signing, bridging, deployment, and trade execution. <br>
Mitigation: Do not use production private keys or funded wallets during evaluation, and require manual approval before any signing, bridge, deployment, or trade action. <br>
Risk: Generated arbitrage bots, contracts, or calculations may be incorrect, stale, or unsafe in live markets. <br>
Mitigation: Audit generated code and calculations, test only on forks or testnets first, and independently verify liquidity, gas, slippage, MEV exposure, and bridge conditions. <br>
Risk: The release includes paid SkillPay behavior and the security evidence flags the charge path as needing review. <br>
Mitigation: Verify pricing, billing configuration, and the SkillPay charge path before installing or running the skill. <br>


## Reference(s): <br>
- [Arbitrage Basics](references/arbitrage-basics.md) <br>
- [Arbitrage Tools](references/arbitrage-tools.md) <br>
- [Bridge Guide](references/bridge-guide.md) <br>
- [Flashloan Arbitrage](references/flashloan-arbitrage.md) <br>
- [MEV Protection](references/mev-protection.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with code blocks, configuration snippets, and generated script or contract templates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include trading calculations, wallet-related setup, payment prompts, and executable examples that require human review before use.] <br>

## Skill Version(s): <br>
2025.4.12 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
