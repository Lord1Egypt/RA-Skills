## Description:

Uses a Spark Bitcoin L2 wallet proxy over HTTP so agents can check balances, create invoices, send payments, and pay L402 paywalls without holding the wallet mnemonic.

This skill is ready for commercial/non-commercial use.

## Publisher:

[echennells](https://clawhub.ai/user/echennells)

### License/Terms of Use:


## Use Case:

Developers and agent builders use this skill to connect agents to a self-controlled Spark Bitcoin L2 proxy for wallet reads, invoice creation, payments, transfers, and L402 access. It is suited to deployments that need scoped bearer tokens, role-based access, spending limits, logs, and token revocation instead of exposing a wallet mnemonic to the agent.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: An autonomous agent receives bearer-token access to Bitcoin wallet operations.

Mitigation: Use the narrowest token role, avoid admin tokens for agents, set low per-transaction and daily limits, test with small amounts, monitor logs, and keep token revocation ready.

Risk: The sample client can send PROXY_TOKEN to any configured PROXY_URL.

Mitigation: Install only when you control the proxy endpoint, require HTTPS, and enforce a trusted host for PROXY_URL.

Risk: L402 payments can remain pending after funds are sent.

Mitigation: Poll the pending payment status until completion before treating the content fetch as failed or retrying payment.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/echennells/skills/sparkbtcbot-proxy)
- [Proxy Repository](https://github.com/echennells/sparkbtcbot-proxy)
- [Direct SDK Skill](https://github.com/echennells/sparkbtcbot-skill)
- [Spark Documentation](https://docs.spark.money)
- [L402 Documentation](https://docs.lightning.engineering/the-lightning-network/l402)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Code, Configuration]

**Output Format:** [Markdown with HTTP API examples, bash commands, JSON responses, and JavaScript code]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes environment variable guidance for PROXY_URL and PROXY_TOKEN.]

## Skill Version(s):

1.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
