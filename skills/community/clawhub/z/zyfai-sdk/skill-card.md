## Description: <br>
Earn yield on any Ethereum wallet on Base, Arbitrum, and Plasma using either simple Vault deposits on Base or a Smart Wallet with automated yield optimization. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[pauldefi](https://clawhub.ai/user/pauldefi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to automate DeFi yield workflows, including Vault deposits and withdrawals, Smart Wallet deployment, session-key setup, strategy configuration, and earnings inspection. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide an agent through wallet-connected DeFi actions, including deposits, withdrawals, smart-wallet deployment, session-key permissioning, cross-chain settings, and identity-registry transactions. <br>
Mitigation: Require explicit user approval for each wallet transaction and configuration change, and use only wallets and funds the user is prepared to expose to DeFi risk. <br>
Risk: Raw private keys in an autonomous agent environment can expose wallet funds if logs, prompts, dependencies, or runtime hosts are compromised. <br>
Mitigation: Use wallet providers, hardware-backed KMS, or wallet-as-a-service custody instead of raw private keys, and avoid hardcoding secrets. <br>
Risk: Package or SDK changes could alter transaction behavior in a high-impact financial workflow. <br>
Mitigation: Pin and verify package versions before use, and review generated SDK calls and transaction parameters before signing. <br>


## Reference(s): <br>
- [Zyfai Skill on ClawHub](https://clawhub.ai/pauldefi/zyfai-sdk) <br>
- [Zyfai SDK Documentation](https://docs.zyf.ai) <br>
- [Zyfai SDK API Key Portal](https://sdk.zyf.ai) <br>
- [Zyfai SDK Demo](https://github.com/ondefy/zyfai-sdk-demo) <br>
- [Zyfai MCP Server](https://mcp.zyf.ai/mcp) <br>
- [Zyfai Agent Registration Metadata](https://www.zyf.ai/.well-known/agent-registration.json) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown with TypeScript, bash, HTTP, and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose wallet transactions, SDK calls, API-key setup, and chain-specific DeFi configuration that require explicit user approval before execution.] <br>

## Skill Version(s): <br>
1.0.11 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
