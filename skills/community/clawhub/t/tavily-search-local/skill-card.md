## Description:

AI-optimized web search via Tavily API. Returns concise, relevant results for AI agents.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zenghuwei](https://clawhub.ai/user/zenghuwei)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and AI agents use this skill to run Tavily web searches and extract content from URLs when they need concise, agent-oriented web results.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search queries, provided URLs, and the Tavily API key are sent to Tavily's API.

Mitigation: Use the skill only when sending that data to Tavily is acceptable under the user's account and data-handling expectations.

Risk: Highly sensitive searches or URLs may expose sensitive intent or content to an external service.

Mitigation: Avoid highly sensitive queries and URLs unless external processing by Tavily is explicitly acceptable.

## Reference(s):

- [Tavily](https://tavily.com)
- [Tavily Search Local on ClawHub](https://clawhub.ai/zenghuwei/skills/tavily-search-local)
- [zenghuwei ClawHub profile](https://clawhub.ai/user/zenghuwei)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown-style terminal output with answer, source, extracted content, and failed URL sections]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Search results are capped at 20 by the script; extracted content depends on Tavily API responses.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
