## Description:

Search X (Twitter) posts using the xAI API. Use when the user wants to find tweets, search X/Twitter, look up what people are saying on X, or find social media posts about a topic.

This skill is ready for commercial/non-commercial use.

## Publisher:

[github2cao](https://clawhub.ai/user/github2cao)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to search recent X/Twitter posts through xAI, optionally filtering by handles, excluded handles, date range, and image or video understanding.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search queries are sent to xAI and may expose sensitive user, project, or credential information if entered as a query.

Mitigation: Do not submit secrets, credentials, private project names, or sensitive personal data; add an explicit privacy note before broad deployment.

Risk: The skill requires an XAI_API_KEY for API access.

Mitigation: Store the API key only in the expected environment or agent configuration and avoid including it in prompts, command examples, logs, or search queries.

## Reference(s):

- [xAI X Search documentation](https://docs.x.ai/developers/tools/x-search)
- [xAI Console](https://console.x.ai)
- [ClawHub skill page](https://clawhub.ai/github2cao/skills/werwe)
- [Publisher profile](https://clawhub.ai/user/github2cao)

## Skill Output:

**Output Type(s):** [Text, JSON]

**Output Format:** [JSON object containing status, query, text, citations, search count, and token usage.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results may include citations linking to original X posts.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
