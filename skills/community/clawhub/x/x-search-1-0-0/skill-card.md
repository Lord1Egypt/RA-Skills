## Description:

Search X (Twitter) posts using the xAI API for tweets, X/Twitter discussions, social media posts, and what people are saying about a topic.

This skill is ready for commercial/non-commercial use.

## Publisher:

[perfectworldltd](https://clawhub.ai/user/perfectworldltd)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to search public X/Twitter content through the xAI API with optional handle, exclusion, date range, image, and video filters.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search queries and related filters are sent to xAI under the user's API key.

Mitigation: Avoid submitting secrets, private internal names, regulated data, or sensitive terms unless that use is allowed by the user's data-handling rules.

## Reference(s):

- [xAI X Search documentation](https://docs.x.ai/developers/tools/x-search)
- [xAI Console](https://console.x.ai)
- [ClawHub skill page](https://clawhub.ai/perfectworldltd/skills/x-search-1-0-0)
- [ClawHub publisher profile](https://clawhub.ai/user/perfectworldltd)

## Skill Output:

**Output Type(s):** [text, JSON, citations, shell commands, configuration]

**Output Format:** [JSON response containing status, query, summarized text, citations, search count, and token usage]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3 and XAI_API_KEY; supports handle filters, excluded handles, date ranges, image understanding, and video understanding.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
