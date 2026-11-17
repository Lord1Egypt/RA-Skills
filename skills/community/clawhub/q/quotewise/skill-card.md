## Description:

Semantic quote search with source transparency that helps agents find quotes by meaning, not only by keyword.

This skill is ready for commercial/non-commercial use.

## Publisher:

[quotewisio](https://clawhub.ai/user/quotewisio)

### License/Terms of Use:


## Use Case:

External users, agents, and developers use this skill to search for quotations by concept, person, source, exact text, similarity, or random selection, and to check attribution with source transparency.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup instructions use unpinned npm commands, so installation or calls may execute package versions that changed after review.

Mitigation: Prefer pinned package versions, review packages before use, and run setup from a least-privilege shell.

Risk: Authenticated setup may store an API key in persistent home-scoped mcporter configuration.

Mitigation: Avoid exposing API keys in command-line arguments where possible, use least-privilege credentials, and confirm how mcporter stores and removes home-scoped Authorization headers.

## Reference(s):

- [Quotewise homepage](https://quotewise.io)
- [Quotewise MCP documentation](https://quotewise.io/developers/mcp/)
- [Quotewise plans and pricing](https://quotewise.io/plans/)
- [Quotewise MCP setup repository](https://github.com/quotewise/mcp)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with bash and JSON examples; MCP tool responses are JSON.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Optional QUOTEWISE_API_KEY authentication enables collections and higher rate limits; anonymous access is documented as limited to 20 requests per day.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
