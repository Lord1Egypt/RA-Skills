## Description: <br>
Production Solana RPC for AI agents. Unlimited JSON-RPC, WebSocket. 1 SOL/month via on-chain payment. No rate limits, no tiers. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[DylanPort](https://clawhub.ai/user/DylanPort) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and external AI agents use this skill to configure and access hosted Solana JSON-RPC, WebSocket subscriptions, DEX market data, and historical account data through Whistle RPC. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The subscription flow requires a real SOL payment on Solana mainnet. <br>
Mitigation: Use a dedicated low-value wallet and require explicit human approval for the amount and recipient before signing any transaction. <br>
Risk: API keys passed in query strings can be exposed through logs or shared URLs. <br>
Mitigation: Prefer X-API-Key or Authorization headers, and avoid logging full request URLs. <br>
Risk: The skill depends on whistle.ninja as a hosted RPC provider and references an external npx CLI. <br>
Mitigation: Install only after accepting that provider dependency and inspect the external CLI separately before running it. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/DylanPort/whistle-rpc) <br>
- [Whistle RPC website](https://whistle.ninja) <br>
- [Whistle RPC tools manifest](https://whistle.ninja/tools.json) <br>
- [Whistle RPC NPM CLI](https://npmjs.com/package/whistle-rpc) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Configuration, Shell commands] <br>
**Output Format:** [Markdown with JSON, HTTP, and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes subscription and API-key handling guidance; payment flows require explicit human approval before signing.] <br>

## Skill Version(s): <br>
1.0.5 (source: server release metadata; artifact frontmatter remains 1.0.4) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
