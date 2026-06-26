## Description: <br>
Set up a complete self-funding agent lifecycle in one command by orchestrating wallet provisioning, optional token deployment with a Uniswap V4 pool, treasury management, ERC-8004 identity registration, and x402 micropayment configuration. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wpank](https://clawhub.ai/user/wpank) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill to bootstrap an agent's financial infrastructure across wallet setup, optional token launch, treasury controls, identity registration, and x402 payments. It is intended for end-to-end self-funding setup workflows rather than one-off wallet, token, treasury, identity, or payment configuration tasks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide financially sensitive crypto setup actions, including wallet provisioning, token deployment, treasury configuration, identity registration, and payment setup. <br>
Mitigation: Use it only with intended wallets and chains, and require the agent to present a plan and wait for explicit confirmation before any transaction or deployment. <br>
Risk: The server security summary reports that the skill lacks a clear mandatory confirmation gate for financially sensitive authority. <br>
Mitigation: Run it in a constrained environment, avoid granting access to unrelated credentials or production wallets, and review each proposed on-chain action before execution. <br>
Risk: Artifact behavior notes that token deployment and pool creation are irreversible once executed. <br>
Mitigation: Confirm token name, symbol, chain, liquidity, and pool parameters before approving deployment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wpank/self-funding-setup) <br>
- [Publisher profile](https://clawhub.ai/user/wpank) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration, shell commands, guidance] <br>
**Output Format:** [Markdown progress reports, configuration file descriptions, setup summaries, and recovery guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update x402 configuration and manifest files when the workflow reaches payment configuration.] <br>

## Skill Version(s): <br>
0.1.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
