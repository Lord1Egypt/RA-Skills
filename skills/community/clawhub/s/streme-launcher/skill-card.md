## Description: <br>
Launch tokens on Streme (streme.fun) - the streaming token platform on Base. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[clawrencestreme](https://clawhub.ai/user/clawrencestreme) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and token launch operators use this skill to prepare and run Streme SuperToken deployments on Base with Uniswap V3 liquidity, optional staking rewards, optional vesting vaults, and hosted token images. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can launch public blockchain tokens using a raw wallet private key. <br>
Mitigation: Use a dedicated low-balance wallet and require manual approval of the exact deployment transaction before execution. <br>
Risk: Incorrect contract addresses, dependencies, or token parameters can affect deployed assets. <br>
Mitigation: Verify contract addresses and dependencies, and set token parameters explicitly before deployment. <br>
Risk: Image hosting workflows may use third-party credentials. <br>
Mitigation: Use scoped image-hosting credentials and avoid reusing broad account credentials for token image uploads. <br>


## Reference(s): <br>
- [Streme Contract Reference](references/contracts.md) <br>
- [Streme API token search](https://api.streme.fun/api/tokens) <br>
- [Streme token page pattern](https://streme.fun/token/{tokenAddress}) <br>
- [ClawHub skill page](https://clawhub.ai/clawrencestreme/streme-launcher) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with TypeScript and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include deployment parameters, environment variable names, contract addresses, image hosting instructions, and blockchain transaction guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
