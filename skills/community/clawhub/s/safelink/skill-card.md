## Description: <br>
Secure agent-to-agent hiring and execution skill for OpenClaw MCP with escrowed settlement, x402 facilitator payments, ERC-8004 identity and reputation checks, replay protection, endpoint validation, and MPC wallet signing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[licc921](https://clawhub.ai/user/licc921) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and MCP operators use SafeLink to build or run agent-to-agent hiring workflows that require escrowed settlement, proof verification, x402 payments, reputation checks, and policy-gated transaction execution. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can sign and broadcast wallet or payment transactions and was assigned a suspicious security verdict because it handles wallet/payment authority with limited safeguards around sensitive data. <br>
Mitigation: Use testnet first, verify RPC endpoints and balances independently, require explicit approval for high-risk actions, and avoid mainnet deployment until reviewed. <br>
Risk: Sensitive wallet and configuration values may be persisted or exposed during setup, including .env updates and Coinbase wallet data printed on first wallet creation. <br>
Mitigation: Use a throwaway deployer key, keep .env out of source control, discard deployment keys after use, and treat COINBASE_WALLET_DATA and wallet provider credentials as secrets. <br>
Risk: The HTTP task listener can accept paid inbound work when explicitly started. <br>
Mitigation: Keep the listener bound to localhost unless intentionally exposed, use a high-entropy TASK_AUTH_SHARED_SECRET when task authentication is required, and use Redis for replay protection in multi-instance deployments. <br>


## Reference(s): <br>
- [SafeLink ClawHub listing](https://clawhub.ai/licc921/safelink) <br>
- [Publisher profile](https://clawhub.ai/user/licc921) <br>
- [Repository metadata](https://github.com/charliebot8888/SafeLink) <br>
- [x402 facilitator](https://x402.org/facilitator) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, JSON] <br>
**Output Format:** [MCP tool responses, JSON payloads, markdown guidance, shell commands, and configuration instructions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May open a local HTTP listener when requested and may write .env during setup or contract deployment.] <br>

## Skill Version(s): <br>
0.1.4 (source: release.version and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
