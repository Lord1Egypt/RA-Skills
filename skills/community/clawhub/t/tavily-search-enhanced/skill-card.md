## Description:

Openclaw Tavily Search lets agents query the Tavily API for web search, news, Q&A, image, and context results with structured links, snippets, and optional answer summaries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nowhere1975](https://clawhub.ai/user/nowhere1975)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to add Tavily-backed web retrieval to an agent for current search, news lookup, Q&A, image discovery, domain-restricted research, and source gathering.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search queries and retrieval parameters are sent to Tavily as a third-party API provider.

Mitigation: Use approved query content, avoid sensitive data in prompts and domain filters, and review Tavily's applicable terms and data handling before deployment.

Risk: The helper can read TAVILY_API_KEY from a shared local credential file at ~/.openclaw/.env when the runtime environment variable is not set.

Mitigation: Prefer setting TAVILY_API_KEY directly in the runtime environment and avoid relying on shared credential files unless that storage pattern is approved.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/nowhere1975/skills/tavily-search-enhanced)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON]

**Output Format:** [Markdown or JSON search results with titles, URLs, snippets, optional answers, related topics, or image URLs.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results are bounded per invocation: up to 10 search, news, or context results, up to 5 Q&A results, and up to 20 image results.]

## Skill Version(s):

0.2.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
