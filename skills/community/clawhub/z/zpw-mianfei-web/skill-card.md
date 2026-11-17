## Description:

Use a local free search engine to find information on the web by fetching results with specified keywords.

This skill is ready for commercial/non-commercial use.

## Publisher:

[blue-sky-8](https://clawhub.ai/user/blue-sky-8)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to run web searches through a local search service when prompts ask to search or look something up.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unsafe shell interpolation can allow a search query to become command execution.

Mitigation: Use a structured HTTP client or curl with --get and --data-urlencode, and avoid interpolating untrusted query text into a shell command.

Risk: Search queries are sent to an internal HTTP endpoint with little user control.

Mitigation: Clearly disclose the endpoint and ask before sending sensitive queries.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/blue-sky-8/skills/zpw-mianfei-web)

## Skill Output:

**Output Type(s):** [Shell commands, JSON]

**Output Format:** [JSON search results returned from a curl command]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Queries are sent to a configured local HTTP search endpoint.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
