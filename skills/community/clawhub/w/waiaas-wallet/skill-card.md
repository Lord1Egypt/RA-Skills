## Description: <br>
WAIaaS Wallet helps AI agents use a self-hosted EVM and Solana wallet daemon to send transactions, manage DeFi positions, and enforce spending limits without exposing private keys to the agent process. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[minhoyoo-iotrust](https://clawhub.ai/user/minhoyoo-iotrust) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and agent operators use this skill to connect agents to a self-hosted WAIaaS wallet daemon, configure session-based MCP access, and perform wallet, transaction, and DeFi workflows under spending and approval policies. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill intentionally gives an AI agent controlled access to a crypto wallet, which can create financial loss if policies or approvals are too permissive. <br>
Mitigation: Start on testnet, use a dedicated low-fund wallet, configure strict spending and contract policies before connecting agents, and require human approval for meaningful transactions or signatures. <br>
Risk: A leaked or stale WAIAAS_SESSION_TOKEN could allow unwanted wallet operations within the token's permissions. <br>
Mitigation: Store session tokens in environment variables or a secrets manager, revoke or rotate WAIAAS_SESSION_TOKEN when not in use, and avoid hardcoding tokens in configuration files. <br>
Risk: Installing the companion CLI or MCP packages from the wrong source could expose the wallet workflow to supply-chain risk. <br>
Mitigation: Verify the npm packages and upstream project before installation, and install only when the agent is intended to operate a crypto wallet. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/minhoyoo-iotrust/waiaas-wallet) <br>
- [WAIaaS homepage](https://waiaas.ai) <br>
- [WAIaaS source repository](https://github.com/minhoyoo-iotrust/WAIaaS) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guidance centers on installing WAIaaS, configuring session-token based MCP access, and using wallet tools with policy checks.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
