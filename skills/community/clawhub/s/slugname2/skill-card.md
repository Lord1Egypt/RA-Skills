## Description:

Search X (Twitter) posts using the xAI API. Use when the user wants to find tweets, search X/Twitter, look up what people are saying on X, or find social media posts about a topic.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kevinbrother](https://clawhub.ai/user/kevinbrother)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to search X/Twitter posts through xAI, optionally filtering by handles, excluded handles, date range, and image or video understanding.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search queries, handles, date filters, and API-authenticated requests are sent to xAI.

Mitigation: Avoid confidential project names, secrets, or personal data unless sharing them with xAI is acceptable under the user's account and policies.

Risk: Search results summarize X/Twitter content and may include claims that need source review.

Mitigation: Review returned citations and source posts before relying on the results for decisions or publication.

## Reference(s):

- [xAI X Search documentation](https://docs.x.ai/developers/tools/x-search)
- [xAI Console](https://console.x.ai)
- [ClawHub skill page](https://clawhub.ai/kevinbrother/skills/slugname2)

## Skill Output:

**Output Type(s):** [text, JSON, guidance]

**Output Format:** [JSON search results with status, query, text, citations, search count, and token usage; agents can present the results as Markdown with citations.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Python 3 and XAI_API_KEY; supports handle filters, date filters, and image or video understanding flags.]

## Skill Version(s):

1.0.0 (source: release evidence and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
