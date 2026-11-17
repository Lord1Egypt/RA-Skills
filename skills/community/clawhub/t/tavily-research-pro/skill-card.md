## Description:

Tavily Research Pro helps agents perform AI-powered public web search, URL extraction, sentiment analysis, and structured research reporting through the Tavily API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[airoom-ai](https://clawhub.ai/user/airoom-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Researchers, analysts, and agents use this skill to search public web information, extract content from URLs, summarize findings, and produce concise research notes from Tavily results.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: User-provided search terms, requested URLs, and the local Tavily API key are sent to Tavily's API.

Mitigation: Use the skill only with public or non-confidential queries and URLs, keep TAVILY_API_KEY in local environment variables, and rotate the key if it is exposed.

Risk: API-derived research outputs can be incomplete, stale, or misleading for high-impact decisions.

Mitigation: Review source URLs and Tavily outputs before using the results for business, legal, medical, financial, or regulated decisions.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/airoom-ai/skills/tavily-research-pro)
- [Tavily](https://tavily.com)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration guidance]

**Output Format:** [Markdown and terminal text produced by Node.js command-line scripts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js and a local TAVILY_API_KEY environment variable.]

## Skill Version(s):

1.1.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
