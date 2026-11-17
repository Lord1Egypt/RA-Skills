## Description:

Search the web using SerpAPI with customizable engines (Google, Google AI Mode, Bing, etc.). Use when user needs web search results via SerpAPI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lsl001006](https://clawhub.ai/user/lsl001006)

### License/Terms of Use:


## Use Case:

Developers and agent users use this skill to retrieve web search results through SerpAPI when an agent needs current search results from supported engines.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search queries and related request data are sent to SerpAPI.

Mitigation: Install only in environments where sending search queries to SerpAPI is acceptable.

Risk: The skill requires a SerpAPI key.

Mitigation: Set SERPAPI_API_KEY through an environment variable or secret manager and avoid hardcoding credentials.

Risk: The serpapi dependency is not pinned in the artifact metadata.

Mitigation: Pin or lock the serpapi dependency before operational use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lsl001006/skills/web-search-with-serpapi)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration]

**Output Format:** [Plain text returned from SerpAPI text blocks or an error/status string]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a SERPAPI_API_KEY environment variable and the serpapi Python package; supports query and engine parameters.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
