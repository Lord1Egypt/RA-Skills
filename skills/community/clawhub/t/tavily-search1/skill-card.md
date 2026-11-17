## Description:

AI-optimized web search via Tavily API. Returns concise, relevant results for AI agents.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cp33333333333](https://clawhub.ai/user/cp33333333333)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to run Tavily-powered web searches, retrieve concise source summaries, and extract clean content from provided URLs for research and current-events workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search queries and provided URLs are sent to Tavily under the user's API key.

Mitigation: Use the skill only when Tavily is approved for the data being searched or extracted.

Risk: Private intranet links, token-bearing URLs, or confidential research targets may disclose sensitive information to an external service.

Mitigation: Avoid submitting those URLs or queries unless they have been cleared for Tavily processing.

## Reference(s):

- [Tavily](https://tavily.com)
- [ClawHub skill page](https://clawhub.ai/cp33333333333/skills/tavily-search1)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown text with answer sections, source lists, URLs, snippets, and extracted page content.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires TAVILY_API_KEY; search result count is capped at 20.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
