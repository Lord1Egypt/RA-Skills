## Description:

VeraData provides autonomous agents with Latin American compliance data for sanctions screening, KYB verification, business registry lookup, central bank rates, and market intelligence through a remote API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[teodorofodocrispin-cmyk](https://clawhub.ai/user/teodorofodocrispin-cmyk)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external agent operators use this skill when an agent needs to screen people or entities against sanctions lists, run LATAM KYB checks, retrieve registry records, fetch central bank rates, or call VeraData market-intelligence endpoints.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Agents may send sensitive compliance, KYB, registry, rates, or sanctions queries to VeraData.

Mitigation: Install only for workflows that intentionally use VeraData, require approval before screening real people or companies, and avoid unnecessary disclosure in request payloads.

Risk: Wallet-payment examples can lead an agent to sign x402 payments.

Mitigation: Enforce local checks for recipient, token, network, endpoint price, and spend limits before any agent signs a payment.

Risk: Remote MCP tools can expand agent capabilities beyond simple API calls.

Mitigation: Review available MCP tools and permissions before enabling the VeraData MCP endpoint.

Risk: Stream tokens and payment signatures are sensitive operational values.

Mitigation: Do not log stream tokens or payment signatures, and keep token lifetime and replay behavior under operator control.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/teodorofodocrispin-cmyk/skills/veradata-latam-compliance)
- [VeraData API base URL](https://api.veradata.dev)
- [Health check](https://api.veradata.dev/health)
- [OpenAPI schema](https://api.veradata.dev/openapi.json)
- [llms.txt](https://api.veradata.dev/llms.txt)
- [MCP endpoint](https://api.veradata.dev/mcp)
- [x402 discovery](https://api.veradata.dev/.well-known/x402)
- [VeraData public repository](https://github.com/teodorofodocrispin-cmyk/veradata-public)

## Skill Output:

**Output Type(s):** [Guidance, API Calls, JSON, Code, Shell commands, Configuration]

**Output Format:** [Markdown guidance with HTTP examples, code snippets, shell commands, and JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Remote API calls may require x402 payment signatures or X-TRIAL headers; paid responses may include audit hashes and compliance metadata.]

## Skill Version(s):

2.3.2 (source: server release metadata and artifact metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
