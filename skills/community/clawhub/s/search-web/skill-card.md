## Description:

Performs internet searches through a self-hosted SearXNG instance and returns recent structured web results with titles and URLs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lokixshrishi](https://clawhub.ai/user/lokixshrishi)

### License/Terms of Use:


## Use Case:

Developers and agent operators use this skill to let an OpenClaw agent issue web search queries through a self-hosted SearXNG service and receive current result links for research, fact checking, documentation lookup, and recent news.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search queries are sent to a local SearXNG service on localhost:8080.

Mitigation: Install only when the expected SearXNG service is running locally and configured for JSON output.

Risk: Returned web results may be incomplete, stale, or misleading.

Mitigation: Use the results as starting points for current-information lookup and verify important claims against the linked sources.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, configuration, guidance]

**Output Format:** [JSON array of search result objects containing title and url fields]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns up to five results from the configured local SearXNG JSON endpoint.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata and artifact skill.yaml)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
