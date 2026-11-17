## Description:

Search XiaoHongShu / RED notes through the hosted whatson.red MCP endpoint when users need structured RED search results, note details, or a draft blog payload.

This skill is ready for commercial/non-commercial use.

## Publisher:

[seichris](https://clawhub.ai/user/seichris)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to query XiaoHongShu / RED / RedNote through the hosted whatson.red MCP endpoint and receive structured search results, note details, usage information, and optional draft blog payloads.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires a whatson.red Agent API key and can consume account credits for search requests.

Mitigation: Install only when that credential access and billing model are acceptable, and review usage or credit costs before running large searches.

Risk: Optional blog output is returned as draft content and may require editorial review.

Mitigation: Treat any blog payload as a draft and review it before relying on or publishing it.

## Reference(s):

- [whatson.red Agents](https://www.whatson.red/agents)
- [MCP endpoint](https://www.whatson.red/api/agent/mcp)
- [REST search endpoint](https://www.whatson.red/api/agent/search)

## Skill Output:

**Output Type(s):** [Guidance, Configuration, API calls, Text, Markdown]

**Output Format:** [Structured JSON results with optional draft blog content]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires WHATSON_RED_API_KEY; responses include usage and billing-credit information.]

## Skill Version(s):

1.0.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
