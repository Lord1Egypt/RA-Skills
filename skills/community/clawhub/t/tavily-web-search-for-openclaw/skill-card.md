## Description:

Provides Tavily-powered web search for recent information, current events, online sources, and lightweight research in OpenClaw.

This skill is ready for commercial/non-commercial use.

## Publisher:

[goktugcy](https://clawhub.ai/user/goktugcy)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to run Tavily searches from minimal Linux environments and return search results, answer summaries, image links, or raw JSON for downstream summarization.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search queries, search options, and requested content are sent to Tavily using the configured Tavily API key.

Mitigation: Use only in environments where Tavily use is approved, avoid sensitive internal research terms, and keep the API key out of source control.

Risk: The skill reads an API key from a local secrets file or environment variable.

Mitigation: Restrict the secrets directory and key file permissions to the user or service that runs the skill.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/goktugcy/skills/tavily-web-search-for-openclaw)
- [Tavily Search API endpoint](https://api.tavily.com/search)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, JSON]

**Output Format:** [Plain text search results or raw JSON, often embedded in Markdown guidance with shell commands for setup and use.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports general or news search, basic or advanced depth, result limits, answer summaries, raw content, images, and domain filters.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
