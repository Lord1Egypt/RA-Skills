## Description:

AI-optimized web search via Tavily API that returns concise, relevant results for AI agents.

This skill is ready for commercial/non-commercial use.

## Publisher:

[huihui-hb](https://clawhub.ai/user/huihui-hb)

### License/Terms of Use:


## Use Case:

Developers and agent builders use this skill to run Tavily web searches, request deeper or news-focused results, and extract clean content from supplied URLs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search queries and extracted URLs are sent to Tavily using the configured Tavily account.

Mitigation: Avoid confidential, internal, localhost, or otherwise sensitive queries and URLs unless that disclosure is acceptable.

Risk: Returned search answers, snippets, and extracted content may be incomplete or unsuitable for high-stakes decisions.

Mitigation: Review returned sources and content before relying on the output or passing it into downstream workflows.

## Reference(s):

- [Tavily](https://tavily.com)
- [ClawHub skill page](https://clawhub.ai/huihui-hb/skills/tavily-search-1-0-0)

## Skill Output:

**Output Type(s):** [Markdown, Text, Shell commands, API calls]

**Output Format:** [Markdown text with answer, sources, extracted page content, or failed URL entries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js and TAVILY_API_KEY; search results are capped at 20.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
