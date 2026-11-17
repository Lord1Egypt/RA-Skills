## Description:

Extract content from specific URLs using Tavily's extraction API and return clean markdown or text from web pages.

This skill is ready for commercial/non-commercial use.

## Publisher:

[evanydl](https://clawhub.ai/user/evanydl)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill when they already have target URLs and need page content extracted as markdown or text for analysis, summarization, or downstream workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Tavily receives submitted URLs, query text, and extraction request context.

Mitigation: Avoid internal, private, authenticated, or sensitive URLs unless that disclosure is acceptable for the deployment.

Risk: The automatic authentication path can read cached MCP tokens from the local environment.

Mitigation: Prefer setting TAVILY_API_KEY explicitly and review local token handling before use.

Risk: First-run OAuth can invoke an unpinned npm package through mcp-remote.

Mitigation: Review or pin the mcp-remote execution path before relying on the automatic OAuth flow.

## Reference(s):

- [ClawHub Tavily Extract Skill Page](https://clawhub.ai/evanydl/skills/tavily-extract)
- [evanydl ClawHub Publisher Profile](https://clawhub.ai/user/evanydl)
- [Tavily](https://tavily.com)
- [Tavily Extract API Endpoint](https://api.tavily.com/extract)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [JSON responses containing extracted markdown or text, with shell command examples and configuration guidance in the skill documentation]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Extraction accepts up to 20 URLs per request and may include failed URL results and response timing.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
