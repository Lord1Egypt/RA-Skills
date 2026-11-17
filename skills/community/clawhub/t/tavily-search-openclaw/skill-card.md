## Description:

Tavily AI Search API integration for OpenClaw. Provides web search capabilities using Tavily's AI-powered search engine.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ryan-wuxl](https://clawhub.ai/user/ryan-wuxl)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to add Tavily-powered web search, including configurable search depth, result count, AI-generated answers, and image inclusion.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses Tavily as an external search provider, so search queries may be sent outside the user's environment.

Mitigation: Avoid including private data, credentials, or confidential business information in search queries.

Risk: The Tavily API key is required for use and could be exposed if committed, shared, or logged.

Mitigation: Treat TAVILY_API_KEY as a secret and keep it out of repositories, examples with real values, and logs.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ryan-wuxl/skills/tavily-search-openclaw)
- [Skill homepage](https://github.com/ryan-wuxl/tavily-search)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with JSON, bash, and Python code examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a Tavily API key supplied through OpenClaw configuration or the TAVILY_API_KEY environment variable.]

## Skill Version(s):

1.0.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
