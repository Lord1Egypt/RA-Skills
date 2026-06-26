## Description: <br>
Use a Spark Bitcoin L2 wallet proxy for AI agents via HTTP API to check balances, send payments, create invoices, and pay L402 paywalls without exposing the wallet mnemonic. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[echennells](https://clawhub.ai/user/echennells) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and AI agent operators use this skill to connect agents to a self-hosted Spark Bitcoin L2 wallet proxy for balance checks, invoice creation, Lightning payments, Spark transfers, L402 paywall access, and token management. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Bearer tokens can authorize wallet actions and spending up to their assigned role and limits. <br>
Mitigation: Use least-privilege tokens, configure per-transaction and daily spending caps, monitor activity logs, and revoke tokens immediately if behavior is unexpected. <br>
Risk: Autonomous payment workflows can spend real funds, including L402 payments that may require follow-up polling to complete. <br>
Mitigation: Preview costs where possible, test with small amounts, set strict limits, and handle pending L402 payments by polling the status endpoint before treating the workflow as complete. <br>
Risk: Plain HTTP or an untrusted proxy endpoint can expose wallet-proxy credentials. <br>
Mitigation: Use HTTPS-only proxy URLs and prefer a self-hosted proxy deployment controlled by the operator. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/echennells/sparkbtcbot-proxy) <br>
- [sparkbtcbot-proxy source](https://github.com/echennells/sparkbtcbot-proxy) <br>
- [Spark documentation](https://docs.spark.money) <br>
- [L402 specification](https://docs.lightning.engineering/the-lightning-network/l402) <br>
- [Direct SDK skill](https://github.com/echennells/sparkbtcbot-skill) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Code, Configuration] <br>
**Output Format:** [Markdown with curl, JSON, and JavaScript code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires PROXY_URL and PROXY_TOKEN environment variables for agent use.] <br>

## Skill Version(s): <br>
1.1.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
