## Description: <br>
Execute on-chain transactions with user-granted permissions. Built on MetaMask ERC-7715. No private keys, full guardrails. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[andreolf](https://clawhub.ai/user/andreolf) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External developers and agent builders use WalletPilot 7715 to configure agents that request scoped wallet permissions and perform permitted on-chain actions such as transactions, token sends, swaps, balance checks, and history lookup. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide agents to execute real crypto transactions under delegated permissions. <br>
Mitigation: Use small spend limits, short expirations, strict chain and contract allowlists, and revoke permissions when the task is complete. <br>
Risk: WalletPilot API keys and active permissions can expose transaction authority if mishandled. <br>
Mitigation: Protect the API key, avoid logging secrets, pin and review the SDK version, and rotate or revoke credentials after use. <br>
Risk: Incorrect recipients, swap calldata, chain IDs, or contract addresses can cause unintended transfers. <br>
Mitigation: Verify recipients, swap calldata, chain IDs, and contract addresses before execution. <br>


## Reference(s): <br>
- [WalletPilot Documentation](https://docs.walletpilot.xyz) <br>
- [WalletPilot API Reference](https://api.walletpilot.xyz) <br>
- [ClawHub Release Page](https://clawhub.ai/andreolf/walletpilot-7715) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with TypeScript examples and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a WalletPilot API key and user-granted wallet permissions before transaction execution.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
