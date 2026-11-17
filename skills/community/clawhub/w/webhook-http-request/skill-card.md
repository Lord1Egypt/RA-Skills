## Description:

Webhook Http Request lets agents make configurable HTTP requests to public web services and webhooks using standard methods, headers, query parameters, request bodies, authentication options, and response handling modes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[agentpmt](https://clawhub.ai/user/agentpmt)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to let an agent call REST APIs, submit webhook payloads, fetch web resources, and poll external services from AgentPMT workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can send payloads and credentials to arbitrary endpoints.

Mitigation: Verify every destination before use, keep request payloads minimal, and use least-privilege tokens or credentials.

Risk: Private or loopback network requests can expose internal services when allow_private is enabled.

Mitigation: Leave allow_private disabled unless private-network access is explicitly required and approved.

Risk: PUT, PATCH, and DELETE requests can modify or remove external resources.

Mitigation: Require user confirmation before state-changing requests and review the target URL, method, headers, and body.

Risk: Live schema and instruction behavior can change how integrations are configured.

Mitigation: Use pinned, reviewed setup instructions where possible and refresh live schema details before new production integrations.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/agentpmt/skills/webhook-http-request)
- [AgentPMT marketplace page](https://www.agentpmt.com/marketplace/webhook-http-request)
- [AgentPMT account MCP/REST setup](https://clawhub.ai/agentpmt/agentpmt-account-mcp-rest-api-setup)
- [What AgentPMT is](https://clawhub.ai/agentpmt/what-is-agentpmt)

## Skill Output:

**Output Type(s):** [JSON, text, base64, guidance]

**Output Format:** [JSON object with HTTP status, headers, final URL, content type, and response body as JSON, text, or base64.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports configurable HTTP methods, authentication modes, timeouts, response size limits, and private-network access only when explicitly enabled.]

## Skill Version(s):

1.0.0 (source: release evidence and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
