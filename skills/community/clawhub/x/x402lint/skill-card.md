## Description:

Conformance scanner and graded discovery directory for x402 sellers: lint an origin against 25 checks spanning the protocol surface, agent docs, and directory standing, and get an A-F grade with per-check evidence and one-line fixes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jcislo](https://clawhub.ai/user/jcislo)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use x402lint to inspect public x402 seller origins, understand protocol conformance gaps, browse graded directory entries, and fetch paid or cached reports before integrating with a service.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The MCP setup can require a wallet private key for paid tools.

Mitigation: Use the free endpoints first, then configure paid tools only with a dedicated low-balance wallet and a reviewed, pinned x402lint-mcp version.

Risk: Scanned origins are publicly listed by default.

Mitigation: Do not scan internal, confidential, customer-specific, or third-party origins unless public listing is acceptable.

Risk: A high grade reflects x402 conformance, not service legitimacy or safety.

Mitigation: Treat directory branding and grades as informational signals and perform independent diligence before paying a service.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/jcislo/skills/x402lint)
- [x402lint homepage](https://x402lint.dev)
- [x402lint API](https://api.x402lint.dev)
- [x402lint OpenAPI specification](https://api.x402lint.dev/openapi.json)
- [x402lint discovery document](https://api.x402lint.dev/discovery)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with HTTP examples, endpoint tables, JSON configuration snippets, and operational guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guidance covers free and paid API routes, MCP setup, wallet configuration, payment caveats, directory behavior, and scan-result interpretation.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
