## Description:

Tavily Search Up helps agents run Tavily web search, extract webpage content, summarize sources, and produce simple sentiment and mission-brief style reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[airoom-ai](https://clawhub.ai/user/airoom-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent builders use this skill to add Tavily-backed web search, webpage extraction, lightweight sentiment checks, and structured briefing output to agent workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search queries, submitted URLs, and Tavily API credentials are processed by Tavily's external API.

Mitigation: Use only with data your organization permits for external processing, and avoid confidential internal URLs, secrets, regulated data, or proprietary research terms.

## Reference(s):

- [Tavily](https://tavily.com)
- [ClawHub skill page](https://clawhub.ai/airoom-ai/skills/tavily-search-up)
- [ClawHub publisher profile](https://clawhub.ai/user/airoom-ai)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown-like terminal output with source lists, extracted webpage text, and concise analysis.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js and TAVILY_API_KEY; normal use sends submitted search queries and URLs to Tavily.]

## Skill Version(s):

1.1.0 (source: server release evidence and target metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
