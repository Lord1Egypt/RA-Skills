## Description:

Web search and content extraction using Tavily Search, Extract, and Research APIs with bearer authentication.

This skill is ready for commercial/non-commercial use.

## Publisher:

[doahc](https://clawhub.ai/user/doahc)

### License/Terms of Use:


## Use Case:

Developers and agents use this skill to run Tavily-powered web search, page extraction, research tasks, and account usage checks when current web results or cited source URLs are needed.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search queries, target URLs, research prompts, and account usage requests are sent to Tavily.

Mitigation: Use the skill only when third-party API processing is acceptable, and avoid submitting secrets, personal data, or internal-only URLs.

Risk: The required TAVILY_API_KEY can expose account quota if mishandled.

Mitigation: Store the key in an environment variable or secrets manager, rotate leaked keys, and check usage before high-volume work.

Risk: Redirect behavior may require stricter controls in sensitive environments.

Mitigation: Keep endpoint validation in place or add environment-specific redirect controls before deployment.

## Reference(s):

- [Tavily Search](references/search.md)
- [Tavily Extract](references/extract.md)
- [Create Research Task](references/research.md)
- [Get Research Task Status](references/research-get.md)
- [Research Streaming](references/research-streaming.md)
- [Usage](references/usage.md)
- [Best Practices for Search](references/bp-search.md)
- [Best Practices for Extract](references/bp-extract.md)
- [Best Practices for Research](references/bp-research.md)
- [API Key Management](references/bp-api-key-management.md)
- [ClawHub Skill Page](https://clawhub.ai/doahc/skills/tavily-web)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands; bundled CLI responses are JSON.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires TAVILY_API_KEY and sends requests to api.tavily.com.]

## Skill Version(s):

0.0.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
