## Description:

Search X (Twitter) posts using the xAI API with handle filters, date ranges, and optional image or video understanding.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pratikbhosale7](https://clawhub.ai/user/pratikbhosale7)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to search public X/Twitter posts through xAI, summarize relevant results, and return citations to original posts. It is useful for finding social media discussion about a topic, person, organization, product, or event.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search terms, filters, and API key-authenticated requests are sent to xAI.

Mitigation: Avoid sensitive personal or confidential searches, protect XAI_API_KEY, and use appropriately scoped credentials.

## Reference(s):

- [xAI X Search documentation](https://docs.x.ai/developers/tools/x-search)
- [xAI Console](https://console.x.ai)
- [xAI Responses API endpoint](https://api.x.ai/v1/responses)
- [ClawHub skill page](https://clawhub.ai/pratikbhosale7/skills/x-search-skill)
- [ClawHub publisher profile](https://clawhub.ai/user/pratikbhosale7)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Configuration guidance]

**Output Format:** [JSON search result with status, query, summary text, citations, search count, and token usage; setup and invocation guidance are Markdown with shell commands.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Python 3 and XAI_API_KEY. Supports allowed or excluded handles, date ranges, and image or video understanding flags.]

## Skill Version(s):

1.0.0 (source: server release evidence and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
