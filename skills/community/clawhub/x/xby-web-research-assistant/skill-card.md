## Description:

A Model Context Protocol web research assistant that routes agent requests to XiaoBenYang-backed tools for web search, URL crawling, package and repository lookup, API documentation discovery, structured extraction, technology comparison, changelog lookup, and service-status checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cainingnk](https://clawhub.ai/user/cainingnk)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to gather and analyze current web information, fetch page text, evaluate software packages or repositories, find API documentation, compare technologies, and troubleshoot errors through a remote XiaoBenYang API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill stores the XiaoBenYang API key in a plaintext .env file.

Mitigation: Use a low-privilege or throwaway API key, keep .env out of shared artifacts and commits, and rotate the key if the workspace may have been exposed.

Risk: Research inputs, URLs, package names, repository identifiers, errors, and other prompts are forwarded to the remote XiaoBenYang API.

Mitigation: Avoid submitting private URLs, proprietary code, secrets, full stack traces, or other sensitive research inputs.

Risk: The remote API may return incomplete, stale, or misleading research results.

Mitigation: Review important outputs against primary sources before using them for decisions or publishing.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/cainingnk/skills/xby-web-research-assistant)
- [XiaoBenYang API key site](https://xiaobenyang.com)
- [XiaoBenYang MCP API endpoint](https://mcp.xiaobenyang.com)

## Skill Output:

**Output Type(s):** [text, markdown, API Calls, configuration, guidance]

**Output Format:** [Markdown summaries of JSON-like tool results returned by the remote API]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a XiaoBenYang API key before tool calls can succeed.]

## Skill Version(s):

1.0.1 (source: server release evidence; artifact frontmatter lists 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
