## Description:

Discover and call remote schema-exposed interfaces with UXC. Use when an agent or skill needs to list operations, inspect operation schemas, and execute OpenAPI, GraphQL, gRPC, MCP, or JSON-RPC calls via one CLI contract.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jolestar](https://clawhub.ai/user/jolestar)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to discover remote schema-exposed APIs, inspect operation schemas, and issue structured calls across OpenAPI, GraphQL, gRPC, MCP, and JSON-RPC endpoints from agent workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Calling untrusted remote endpoints can send prompt or payload data outside the local environment.

Mitigation: Use only endpoints you trust, keep payloads minimal, and avoid sending secrets or local context unless required.

Risk: Credential configuration can expose or misapply API keys, OAuth tokens, or signing material.

Mitigation: Prefer environment variables or managed secret sources, verify credential bindings before live calls, and start with read-only operations.

Risk: Installing the UXC CLI from an unpinned or unaudited source can introduce supply-chain risk.

Mitigation: Prefer a trusted package manager or pinned release and review install scripts before running them.

## Reference(s):

- [ClawHub UXC skill page](https://clawhub.ai/jolestar/skills/uxc)
- [UXC README installation section](https://github.com/holon-run/uxc#installation)
- [Usage Patterns](references/usage-patterns.md)
- [Protocol Cheatsheet](references/protocol-cheatsheet.md)
- [Public Endpoints](references/public-endpoints.md)
- [Authentication Configuration Guide](references/auth-configuration.md)
- [OAuth And Binding](references/oauth-and-binding.md)
- [Error Handling](references/error-handling.md)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, Guidance, JSON]

**Output Format:** [Markdown guidance with inline bash commands and JSON envelope fields]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Default runtime output is a JSON envelope with ok, kind, data, error, and meta fields; automation should parse stdout JSON.]

## Skill Version(s):

1.0.4 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
