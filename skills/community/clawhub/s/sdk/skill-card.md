## Description: <br>
AI-powered sports betting simulations with Monte Carlo analysis. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cannedoxygen](https://clawhub.ai/user/cannedoxygen) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external agent users use this skill to fetch sports games, daily picks, track records, and paid Monte Carlo betting simulations for NBA, NFL, MLB, and MLS analysis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Simulation calls can spend $0.50 USDC plus Solana fees from the configured wallet. <br>
Mitigation: Use a dedicated low-balance wallet and require explicit user approval before invoking paid simulation methods. <br>
Risk: The skill requires a Solana private key environment variable for wallet-backed usage. <br>
Mitigation: Do not use a main wallet private key, restrict secret exposure, and keep debug logging disabled during paid runs. <br>
Risk: Sports betting simulations and picks can be mistaken for guaranteed outcomes. <br>
Mitigation: Present simulation results as probabilistic analysis and avoid framing them as financial or betting guarantees. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/cannedoxygen/sdk) <br>
- [EdgeBets Website](https://edgebets.fun) <br>
- [EdgeBets API Documentation](https://api.edgebets.fun/api/v1/x402) <br>
- [EdgeBets OpenAPI Spec](https://api.edgebets.fun/api/v1/x402/openapi.json) <br>
- [edgebets-sdk npm Package](https://www.npmjs.com/package/edgebets-sdk) <br>
- [x402 Protocol](https://x402.org) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, API Calls, Guidance] <br>
**Output Format:** [Markdown with JavaScript or TypeScript code examples and structured simulation results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May initiate paid Solana USDC transactions when simulation methods are invoked with a configured wallet.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
