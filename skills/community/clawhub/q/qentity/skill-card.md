## Description: <br>
Qentity enables AI agents to create and operate KYC-backed wallets for receiving, holding, transferring, bridging, and off-ramping funds through Netfluid payment infrastructure. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jnysschensol](https://clawhub.ai/user/jnysschensol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to onboard sponsored AI agent wallets, connect payment rails, check balances, move stablecoins across supported chains, and send or off-ramp funds. It is intended for live financial workflows that require human oversight, secure credential handling, and compliance controls. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill gives agents broad real-money and KYC-linked wallet powers without enough built-in consent, limits, or transaction safeguards. <br>
Mitigation: Treat it as a live financial integration: use limited test funds, require human confirmation for wallet creation and every transfer, bridge, off-ramp, KYC-linked action, or child-agent spawn, and enable spending limits, audit logs, revocation, and compliance controls before use. <br>
Risk: Wallet identifiers, PINs, API keys, session tokens, and recovery phrases can provide bank-account-level access if exposed. <br>
Mitigation: Store secrets only in a dedicated encrypted secret store, redact them from prompts and logs, avoid primary wallet or banking credentials in ordinary chat, and rotate or revoke credentials immediately after suspected exposure. <br>


## Reference(s): <br>
- [Qentity on ClawHub](https://clawhub.ai/jnysschensol/qentity) <br>
- [Publisher profile](https://clawhub.ai/user/jnysschensol) <br>
- [Netfluid compliance statement](https://go.netfluid.app/compliance) <br>
- [Netfluid homepage](https://netfluid.io) <br>
- [Netfluid MCP server](https://mcp.netfluid.io/mcp) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, API Calls, Configuration, Shell commands] <br>
**Output Format:** [Markdown with inline API call examples and command-style snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces operational guidance for wallet onboarding, KYC status checks, payment rail setup, transfers, bridges, and off-ramps.] <br>

## Skill Version(s): <br>
1.6.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
