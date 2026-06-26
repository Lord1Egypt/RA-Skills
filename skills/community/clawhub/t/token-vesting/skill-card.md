## Description: <br>
Create and manage token vesting streams using the Sablier Lockup protocol (linear, dynamic, tranched). <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sneg55](https://clawhub.ai/user/sneg55) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and token operations teams use this skill to prepare Sablier vesting streams, approvals, withdrawals, cancellations, and renounce actions on EVM-compatible chains. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill prepares high-impact blockchain transactions. <br>
Mitigation: Manually verify every address, network, token amount, vesting schedule, and cancelability setting before signing. <br>
Risk: Private keys and RPC URLs may expose funds or API credentials if mishandled. <br>
Mitigation: Use a hardware wallet or encrypted Foundry keystore when possible, never paste private keys into chat, and keep RPC credentials out of logs and committed files. <br>
Risk: Cancel and renounce actions can materially change stream rights. <br>
Mitigation: Treat cancel and renounce as serious actions, and confirm that renounce permanently gives up cancellation rights before execution. <br>


## Reference(s): <br>
- [Sablier Documentation](https://docs.sablier.com) <br>
- [Sablier Lockup Deployments](https://docs.sablier.com/guides/lockup/deployments) <br>
- [Sablier Lockup Source](https://github.com/sablier-labs/lockup) <br>
- [Sablier Lockup Examples](https://github.com/sablier-labs/evm-examples/tree/main/lockup) <br>
- [Sablier Lockup Integration Template](https://github.com/sablier-labs/lockup-integration-template) <br>
- [Sablier App](https://app.sablier.com) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, code, configuration] <br>
**Output Format:** [Markdown with bash and Solidity code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Foundry cast or forge and an ETH_RPC_URL environment variable; signing should use a hardware wallet, encrypted keystore, or environment variable.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
