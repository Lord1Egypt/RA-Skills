## Description: <br>
Create and manage private stablecoin wallets using Senddy's zero-knowledge protocol on Base. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mattt21](https://clawhub.ai/user/mattt21) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agent builders use this skill to configure headless or browser-based payment agents that hold, transfer, and withdraw private USDC on Base through Senddy. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Examples may be unsafe for real-money wallet operations and seed storage if used unchanged. <br>
Mitigation: Use low-balance dedicated wallets, store seeds in a secret manager or encrypted key store, and review and pin @senddy/node before use. <br>
Risk: Agent-controlled transfers or withdrawals can move USDC without sufficient operational controls. <br>
Mitigation: Add authentication, explicit approvals, spend limits, recipient allowlists, logging, and clear withdrawal warnings before enabling transfers or withdrawals. <br>


## Reference(s): <br>
- [Senddy Homepage](https://senddy.com) <br>
- [Senddy ClawHub Skill Page](https://clawhub.ai/mattt21/senddy) <br>
- [Senddy Support](https://github.com/senddy/senddy/issues) <br>
- [API Reference](reference.md) <br>
- [Examples](examples.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown with TypeScript and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes environment variable requirements for SENDDY_API_KEY and AGENT_SEED_HEX.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release metadata and clawhub.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
