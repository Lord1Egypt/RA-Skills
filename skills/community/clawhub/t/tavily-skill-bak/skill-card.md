## Description:

Use Tavily API for real-time web search and content extraction when users need current web results, research, or up-to-date information.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aysun168](https://clawhub.ai/user/aysun168)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to perform real-time Tavily web searches, retrieve current research or news, and generate curl-based API calls for content extraction workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search queries and requested content are sent to Tavily's external API.

Mitigation: Avoid secrets, confidential internal topics, private URLs, and regulated data in search queries.

Risk: The Tavily API key can be exposed through terminal output, logs, screenshots, or shared support artifacts.

Mitigation: Store the API key carefully, avoid printing it, and rotate it if it appears in shared or recorded output.

## Reference(s):

- [Tavily homepage](https://tavily.com)
- [Tavily search API endpoint](https://api.tavily.com/search)
- [ClawHub release page](https://clawhub.ai/aysun168/skills/tavily-skill-bak)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command and JSON configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires curl, jq, and TAVILY_API_KEY; Tavily API responses are returned as JSON.]

## Skill Version(s):

1.0.0 (source: server release evidence and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
