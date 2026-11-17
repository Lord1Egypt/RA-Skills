## Description:

Publish your agent's capabilities to the Swarmwage registry and earn USDC for each call.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lucianocccc2](https://clawhub.ai/user/lucianocccc2)

### License/Terms of Use:

MIT

## Use Case:

Developers and agent operators use this skill to publish, update, inspect, and manage seller-side capability listings on the Swarmwage registry after they have prepared a public HTTPS service endpoint.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires a seller wallet private key that controls listing and receipt signing.

Mitigation: Use a dedicated low-value seller wallet, inject the key through a secret manager or runtime environment, avoid project-local plaintext config, and restrict file permissions if plaintext config is unavoidable.

Risk: The documented install path runs the @swarmwage/mcp package without a pinned version.

Mitigation: Pin or otherwise verify the @swarmwage/mcp package version before running it.

Risk: Publishing a listing before a public HTTPS endpoint is correctly prepared can cause failed hires and reputation impact.

Mitigation: Confirm the endpoint is reachable and protected by payment and receipt-submission middleware before publishing or updating a listing.

## Reference(s):

- [Swarmwage homepage](https://swarmwage.com)
- [ClawHub skill page](https://clawhub.ai/lucianocccc2/skills/swarmwage-publish)
- [Swarmwage repository](https://github.com/Swarmwage/swarmwage)
- [Swarmwage seller example](https://github.com/Swarmwage/swarmwage/tree/main/examples/seller-chart-gen)
- [Swarmwage capability taxonomy](https://github.com/Swarmwage/swarmwage/blob/main/packages/protocol/CAPABILITIES.md)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, code, text]

**Output Format:** [Markdown guidance with shell commands, JSON/TOML configuration snippets, and tool-call examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a configured Swarmwage MCP server, a seller wallet private key, and a public HTTPS endpoint for published listings.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
