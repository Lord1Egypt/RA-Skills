## Description:

Search 72,000+ AI agents across 14 registries, chat with any agent, register your own. Powered by Hashgraph Online Registry Broker.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kantorcodes](https://clawhub.ai/user/kantorcodes)

### License/Terms of Use:

Apache-2.0

## Use Case:

Developers and agent builders use this skill to discover AI agents across connected registries, inspect agent details, start or continue chat sessions, and register their own agents through the Registry Broker.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends user messages and API-key-authenticated requests to external Registry Broker services.

Mitigation: Use a scoped, rotatable API key and avoid sending secrets, private prompts, regulated data, or internal-only agent endpoints through chat or registration.

Risk: A custom REGISTRY_BROKER_BASE_URL can redirect requests to a non-default endpoint.

Mitigation: Keep the default hol.org registry endpoint unless the alternate endpoint is fully trusted.

Risk: Unversioned npx command usage can execute changing package versions over time.

Mitigation: Prefer locked local installs and reviewed scripts for sensitive environments.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/kantorcodes/skills/registry-broker-hashnet-openclaw)
- [Hashgraph Online Registry Broker](https://hol.org/registry)
- [Registry Broker API Documentation](https://hol.org/docs/registry-broker/)
- [Hashgraph Online Standards SDK Reference](https://hol.org/docs/libraries/standards-sdk/)
- [@hashgraphonline/standards-sdk](https://www.npmjs.com/package/@hashgraphonline/standards-sdk)
- [Registry Broker MCP Server](https://github.com/hashgraph-online/hashnet-mcp-js)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [JSON responses and Markdown guidance with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js and uses REGISTRY_BROKER_API_KEY for authenticated operations.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
