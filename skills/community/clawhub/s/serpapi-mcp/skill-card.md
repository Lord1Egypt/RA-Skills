## Description:

Run SerpAPI searches via SerpAPI's MCP server using mcporter.

This skill is ready for commercial/non-commercial use.

## Publisher:

[merlintxu](https://clawhub.ai/user/merlintxu)

### License/Terms of Use:


## Use Case:

Developers and agent users use this skill to run SerpAPI web searches from an agent workflow, including optional engine, result count, and mode controls. It can also enrich AI Overview results and optionally persist search results to Airtable when configured.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search queries and full SerpAPI responses may contain sensitive or confidential data, especially when Airtable logging is enabled.

Mitigation: Keep Airtable logging disabled for sensitive searches unless users explicitly consent, and restrict access to the Airtable base when logging is used.

Risk: SerpAPI and Airtable credentials are required for external service access and could be exposed if handled carelessly.

Mitigation: Store scoped, revocable tokens outside the repo or workspace, rotate credentials if exposed, and avoid printing secrets in logs.

Risk: The skill depends on mcporter and external SerpAPI and optional Airtable network calls.

Mitigation: Install only in environments where those services are approved, and prefer a pinned or local mcporter installation where possible.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/merlintxu/skills/serpapi-mcp)
- [SerpAPI Google AI Overview API](https://serpapi.com/google-ai-overview-api)
- [SerpAPI MCP search endpoint](https://mcp.serpapi.com/$SERPAPI_API_KEY/mcp.search)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, configuration guidance]

**Output Format:** [JSON to stdout, with optional Airtable records containing raw and summarized JSON]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports compact or complete search modes, SerpAPI key failover, optional AI Overview enrichment, and optional Airtable truncation flags.]

## Skill Version(s):

1.1.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
