## Description:

Web search via Yep Search API. Own index, fast results with domain filtering and date ranges.

This skill is ready for commercial/non-commercial use.

## Publisher:

[elrandar](https://clawhub.ai/user/elrandar)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to run Yep Search API queries and retrieve web results with titles, URLs, descriptions, optional highlights, and filters for domains, language, safe search, published dates, and crawl dates.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search queries, domain filters, and date filters are sent to Yep.

Mitigation: Avoid submitting secrets, confidential material, or private personal data in search queries or filters.

Risk: The skill requires a YEP_API_KEY and can make paid Yep API calls.

Mitigation: Provide the key only through the environment, keep it out of prompts and logs, and monitor Yep usage and balance.

## Reference(s):

- [Yep Platform](https://platform.yep.com)
- [Yep API Key Setup](https://platform.yep.com/app)
- [Yep Search API Endpoint](https://platform.yep.com/api/search)
- [ClawHub Skill Page](https://clawhub.ai/elrandar/skills/yep-search)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Guidance]

**Output Format:** [Markdown search results with URLs, titles, descriptions, and optional cost details.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires YEP_API_KEY; supports result limits, highlights, search mode, language, domain filters, safe search, published date filters, and crawl date filters.]

## Skill Version(s):

0.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
