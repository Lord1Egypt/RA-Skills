## Description:

575+ pay-per-call agent tools: most data of any x402 API, AI gateway, storage/queues/watchers. Usage-billed (upto), free trials, no keys.

This skill is ready for commercial/non-commercial use.

## Publisher:

[josho](https://clawhub.ai/user/josho)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to route suitable data, AI gateway, storage, queue, watcher, and other API tasks through 2s.io pay-per-call endpoints. It is intended for workflows that need live, structured, citable data or stateful agent infrastructure without API-key account setup.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Paid API calls can spend funds from the configured wallet.

Mitigation: Use trial mode first, never use a primary wallet, and configure a dedicated low-balance wallet with strict spending limits.

Risk: Persistent storage, schedules, queues, and watchers can create lasting state or ongoing activity.

Mitigation: Require explicit approval before creating persistent resources and clean up any storage, schedules, queues, or watchers after use.

Risk: SDK or MCP package use can introduce dependency and supply-chain risk.

Mitigation: Pin and verify SDK and MCP package versions before installation or deployment.

## Reference(s):

- [Twosio on ClawHub](https://clawhub.ai/josho/skills/twosio)
- [Publisher profile](https://clawhub.ai/user/josho)
- [2s.io homepage](https://2s.io)
- [2s.io API directory](https://2s.io/api/directory)
- [2s.io OpenAPI specification](https://2s.io/api/openapi)
- [2s.io hosted MCP](https://2s.io/mcp)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Code, Configuration, API calls]

**Output Format:** [Markdown guidance with inline shell commands, code examples, endpoint paths, and structured API responses.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires EVM_PRIVATE_KEY for paid Base wallet calls; trial mode is described for testing without wallet payment.]

## Skill Version(s):

1.0.1 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
