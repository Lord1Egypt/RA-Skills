## Description:

Xiaogua Tavily Search lets an agent run Tavily-powered live web searches for current information, news, source gathering, and ranked research results.

This skill is ready for commercial/non-commercial use.

## Publisher:

[taowolf](https://clawhub.ai/user/taowolf)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and agents use this skill to run live Tavily searches when current web information, news, source gathering, or ranked research results are needed. It is especially useful when built-in web search is limited or Tavily-backed ranking and filtering are preferred.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search queries and the Tavily API key are sent to Tavily.

Mitigation: Use the skill only for queries suitable for Tavily, avoid sensitive private searches, and prefer the TAVILY_API_KEY environment variable on shared systems.

Risk: A local .secrets/tavily.key file can expose credentials if the skill directory is shared or published.

Mitigation: Keep local secrets private, do not commit or publish real keys, and use environment variables for public or shared installs.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/taowolf/skills/xiaogua-tavily-search)
- [Tavily Search API Endpoint](https://api.tavily.com/search)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, configuration, guidance]

**Output Format:** [Plain text search results, or JSON when the --json flag is used]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a Tavily API key; optional flags can request a synthesized answer, raw page content, image results, recency limits, domain filters, and country or time-range hints.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
