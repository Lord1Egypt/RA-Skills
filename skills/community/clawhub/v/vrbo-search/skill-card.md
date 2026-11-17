## Description:

Search live Vrbo stays by location, dates and occupancy, returned in one unified schema alongside every other booking platform.

This skill is ready for commercial/non-commercial use.

## Publisher:

[stayingapi](https://clawhub.ai/user/stayingapi)

### License/Terms of Use:

MIT-0

## Use Case:

External users and travel-focused agents use this skill to search Vrbo stays by location, travel dates, occupancy, and platform filters through StayingAPI. It is useful when the user wants candidate Vrbo listings rather than details for one known listing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A live STAYINGAPI_KEY could be persisted in a broad shell profile or shared runtime configuration.

Mitigation: Prefer the MCP/OAuth flow or a sandbox/session-only key for evaluation, and store live keys only in a tightly controlled secret location.

Risk: Searches may return results from platforms beyond Vrbo if the agent omits the platform filter.

Mitigation: When the user asks specifically for Vrbo results, send platforms=vrbo with the search request.

Risk: Live search jobs can be asynchronous, empty, partially complete, rate limited, or failed with the failure nested in the job payload.

Mitigation: Honor Retry-After, cap polling attempts, inspect terminal job status, and treat meta pagination, warnings, and nested job errors as authoritative.

## Reference(s):

- [StayingAPI homepage](https://stayingapi.com)
- [StayingAPI documentation](https://stayingapi.com/docs)
- [StayingAPI OpenAPI contract](https://api.stayingapi.com/openapi.json)
- [StayingAPI MCP server](https://mcp.stayingapi.com/mcp)
- [Auth setup](references/auth-setup.md)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, text]

**Output Format:** [Markdown with inline REST API and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May instruct the agent to call StayingAPI REST or MCP endpoints and interpret JSON search results, async job status, pagination, warnings, and failed jobs.]

## Skill Version(s):

1.1.0 (source: server release metadata; artifact frontmatter says 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
