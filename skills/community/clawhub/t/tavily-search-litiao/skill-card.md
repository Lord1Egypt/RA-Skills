## Description:

Tavily Search Litiao provides AI-optimized web search and URL content extraction through the Tavily API for agent workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[litiao1224](https://clawhub.ai/user/litiao1224)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to run Tavily searches, retrieve concise source snippets, search recent news, and extract readable content from supplied URLs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search queries and supplied URLs are sent to Tavily.

Mitigation: Avoid submitting private, internal, or sensitive queries and URLs unless the Tavily account and data-handling expectations allow it.

Risk: The skill depends on a Tavily API key from the runtime environment.

Mitigation: Provide TAVILY_API_KEY only through the intended environment and rotate or revoke it if exposure is suspected.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/litiao1224/skills/tavily-search-litiao)
- [Tavily](https://tavily.com)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown with search answers, source lists, extracted URL content, and command usage examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js and TAVILY_API_KEY; search results are capped at 20 per request.]

## Skill Version(s):

1.0.0 (source: server release evidence and artifact metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
