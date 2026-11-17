## Description:

Build and orchestrate multi-agent AI systems using the Swarms API, including single agents, multi-agent swarms, Solana token launches, ATP payment protocol, marketplace publishing, sub-agent delegation, streaming responses, and orchestration pipelines.

This skill is ready for commercial/non-commercial use.

## Publisher:

[newsoulontheblock](https://clawhub.ai/user/newsoulontheblock)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to configure Swarms API agents and swarms, choose orchestration patterns, integrate tools or MCP servers, stream responses, and publish or monetize agents through Swarms-related services.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Token launch and ATP examples document sending Solana wallet private keys to remote services.

Mitigation: Use client-side wallet signing, testnet or low-balance burner wallets, and scoped authorization flows instead of sharing funded wallet private keys.

Risk: Swarms API examples send prompts and API keys to remote Swarms services.

Mitigation: Use environment variables for API keys and send only data that is appropriate for the Swarms service.

Risk: Some endpoints require paid Swarms tiers or incur blockchain costs.

Mitigation: Confirm account tier, pricing, and wallet balance before running batch, reasoning-agent, token launch, or ATP workflows.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/newsoulontheblock/skills/swarms-ai)
- [Swarms docs index](https://docs.swarms.ai/llms.txt)
- [Swarms platform API keys](https://swarms.world/platform/api-keys)
- [Swarms marketplace](https://swarms.world)
- [Swarms API Architecture](references/architecture.md)
- [Sub-Agent Delegation](references/sub-agents.md)
- [ATP - Agent Trade Protocol](references/atp-protocol.md)
- [Swarms Marketplace](references/marketplace.md)
- [Streaming Responses](references/streaming.md)
- [Tools Integration](references/tools.md)

## Skill Output:

**Output Type(s):** [guidance, markdown, code, shell commands, configuration]

**Output Format:** [Markdown with API examples, code snippets, shell commands, and configuration tables]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes examples that call remote Swarms services and sections involving Solana wallet handling.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
