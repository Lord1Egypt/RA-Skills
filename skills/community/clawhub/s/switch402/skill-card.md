## Description:

Provides paid web data tools for agents to retrieve public pages as Markdown, discover site URLs, inspect metadata, capture screenshots, search the web, and extract text from PDFs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[duffey234](https://clawhub.ai/user/duffey234)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and agent operators use the skill to retrieve and inspect public web content through Switch402's pay-per-call API, approving each exact USDC charge before making a paid request.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: URLs and search queries are sent to the Switch402 service.

Mitigation: Submit only public URLs and non-sensitive searches.

Risk: Paid calls spend USDC from the user's wallet, and backend behavior and charging guarantees were not verified during review.

Mitigation: Check the live quote and payment request, approve each exact amount using trusted wallet tooling, and use a separate wallet with limited funds.

## Reference(s):

- [Switch402 agent documentation](https://api.switch402.com/llms.txt)
- [Switch402 OpenAPI specification](https://api.switch402.com/openapi.json)
- [Switch402 x402 payment requirements](https://api.switch402.com/.well-known/x402)
- [Switch402 MCP endpoint](https://api.switch402.com/mcp)
- [Hermes Agent plugin](https://github.com/Duffey234/switch402-hermes)

## Skill Output:

**Output Type(s):** [Markdown, Text, JSON, Images]

**Output Format:** [Endpoint-specific Markdown, text, JSON, or PNG image responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returned content depends on the selected web data endpoint.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
