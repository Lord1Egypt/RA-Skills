## Description:

Search X (Twitter) posts using the xAI API when a user wants to find tweets, look up what people are saying on X, or find social media posts about a topic.

This skill is ready for commercial/non-commercial use.

## Publisher:

[blueworldmarketing](https://clawhub.ai/user/blueworldmarketing)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to search current X/Twitter posts through the xAI Grok API, including handle filters, excluded handles, date ranges, and optional image or video understanding.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search terms, filters, and API-authenticated requests are sent to xAI.

Mitigation: Use only when the xAI account and data-handling expectations are appropriate; avoid secrets, private personal data, and confidential internal topics.

## Reference(s):

- [xAI X Search documentation](https://docs.x.ai/developers/tools/x-search)
- [xAI Console](https://console.x.ai)
- [ClawHub skill page](https://clawhub.ai/blueworldmarketing/skills/x-search-bwm)

## Skill Output:

**Output Type(s):** [text, json, markdown, shell commands, configuration, guidance]

**Output Format:** [JSON search results and Markdown-ready text with citations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires XAI_API_KEY; supports handle include or exclude filters, date ranges, image understanding, and video understanding.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact/_meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
