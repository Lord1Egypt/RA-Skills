## Description:

AI-optimized web search with structured summarization, combining Tavily Search API + proven summarization methodology from summarize.

This skill is ready for commercial/non-commercial use.

## Publisher:

[liuxiaolong1988](https://clawhub.ai/user/liuxiaolong1988)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to run Tavily-backed web searches, summarize search results into readable Markdown, and extract page content from supplied URLs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search queries, submitted URLs, and the Tavily API key are sent to Tavily.

Mitigation: Use only with data approved for Tavily in the deployment environment; avoid secrets, private internal URLs, regulated data, and sensitive research terms unless approved.

## Reference(s):

- [Tavily](https://tavily.com)
- [summarize methodology reference](https://github.com/steipete/summarize)
- [ClawHub skill page](https://clawhub.ai/liuxiaolong1988/skills/tavily-summary)

## Skill Output:

**Output Type(s):** [Text, Markdown]

**Output Format:** [Markdown summaries, source lists, and extracted URL content]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Search result count is capped at 20; search and extraction require TAVILY_API_KEY.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact metadata.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
