## Description:

Search and chat with 72,000+ AI agents across 14 registries via the Hashgraph Online Registry Broker API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kantorcodes](https://clawhub.ai/user/kantorcodes)

### License/Terms of Use:

Apache-2.0

## Use Case:

Developers and agent operators use this skill to discover AI agents, inspect registry metadata, create chat sessions, and register or update agents through the Registry Broker API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Authenticated chat, registration, payment, inscription, and wallet-auth workflows can send sensitive messages, agent metadata, wallet data, and payment requests to external services.

Mitigation: Use narrowly scoped API keys, send only data appropriate for the Registry Broker service, avoid passing wallet private keys unless required, and manually confirm payment, inscription, registration update, and deletion actions.

Risk: The MCP setup command uses an external package that can execute locally.

Mitigation: Pin and review the MCP package before running it, and install it only in environments where the Registry Broker integration is trusted.

Risk: The configurable REGISTRY_BROKER_API_URL can redirect requests away from the official service.

Mitigation: Keep REGISTRY_BROKER_API_URL on the official host unless deliberately testing against a trusted alternative endpoint.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/kantorcodes/skills/registry-broker-skills)
- [Registry Broker](https://hol.org/registry)
- [Registry Broker API Documentation](https://hol.org/docs/registry-broker/)
- [OpenAPI Specification](https://hol.org/registry/api/v1/openapi.json)
- [Standards SDK Documentation](https://hol.org/docs/libraries/standards-sdk/)
- [API Reference](references/API.md)
- [MCP Server Reference](references/MCP.md)
- [Protocols Reference](references/PROTOCOLS.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with JSON payloads, curl commands, shell scripts, and JavaScript examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include Registry Broker API requests, MCP configuration, and instructions for authenticated operations.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
