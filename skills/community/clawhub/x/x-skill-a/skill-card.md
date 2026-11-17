## Description:

Searches X (Twitter) posts through the xAI API and returns summarized results with citations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[testmsr](https://clawhub.ai/user/testmsr)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to search public X/Twitter posts, filter by handles or date range, and retrieve concise results with citations to source posts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search queries are sent to xAI using the user's XAI_API_KEY.

Mitigation: Avoid sensitive private information in search queries and install only when use of xAI under the user's account is acceptable.

Risk: API key configuration can expose credentials if mishandled.

Mitigation: Treat XAI_API_KEY and OpenClaw credential configuration as secrets and avoid committing or sharing them.

## Reference(s):

- [xAI x_search documentation](https://docs.x.ai/developers/tools/x-search)
- [xAI Console](https://console.x.ai)

## Skill Output:

**Output Type(s):** [text, JSON]

**Output Format:** [JSON containing status, query, response text, citations, search count, and token usage.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires XAI_API_KEY and may use handle filters, date filters, and image or video understanding options.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
