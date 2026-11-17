## Description:

AI-powered agricultural knowledge management for searching crop management records, livestock data, compliance documentation, and sustainability reports with structured extraction.

This skill is ready for commercial/non-commercial use.

## Publisher:

[roojenkins](https://clawhub.ai/user/roojenkins)

### License/Terms of Use:

MIT-0

## Use Case:

Agriculture teams and supporting agents use this skill to retrieve organization-specific crop, livestock, sustainability, and compliance knowledge through UPLO-backed search and context tools. It supports source-grounded answers, subject matter expert lookup, knowledge-gap reporting, and conversation logging for agricultural workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can export broad organizational context and log conversations, which may expose sensitive agricultural operations, yield data, pricing contracts, or compliance records.

Mitigation: Use classification tiers, limit access to exported or logged data, and avoid sensitive sessions unless logging is acceptable.

Risk: The MCP dependency is executed through an unpinned package command that receives the API token.

Mitigation: Use a pinned or otherwise verified MCP server package and a narrowly scoped, revocable API token before production use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/roojenkins/skills/uplo-agriculture)
- [UPLO](https://uplo.ai)
- [UPLO schemas](https://uplo.ai/schemas)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with MCP tool calls and concise guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Responses should cite UPLO sources, respect classification tiers, and state when the knowledge base lacks an answer.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact skill.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
