## Description:

Provides agent guidance for using Exa's MCP server for neural web search, content extraction, company and people research, code context lookup, and deep research.

This skill is ready for commercial/non-commercial use.

## Publisher:

[theishangoswami](https://clawhub.ai/user/theishangoswami)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to configure and operate the Exa MCP server for web lookup, source extraction, research reports, company and people research, and code or documentation search from an agent.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: API keys may be exposed if embedded directly in shared MCP URLs, configuration files, logs, or screenshots.

Mitigation: Use the unauthenticated MCP URL where possible, avoid storing API keys directly in shared URLs or configs, and rotate any key that has been exposed.

Risk: People and profile search can raise privacy and platform-terms concerns.

Mitigation: Use people/profile search only for legitimate, authorized public research with appropriate privacy and platform-term checks.

Risk: The release security verdict is suspicious and requires review before installation.

Mitigation: Review the skill and its MCP configuration before deployment, and apply the security guidance from the release evidence.

## Reference(s):

- [Exa Documentation](https://exa.ai/docs)
- [Exa MCP Server](https://mcp.exa.ai/mcp)
- [Exa MCP Server GitHub Repository](https://github.com/exa-labs/exa-mcp-server)
- [Exa API Key Dashboard](https://dashboard.exa.ai/api-keys)
- [ClawHub Skill Page](https://clawhub.ai/theishangoswami/skills/web-search-exa)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline JSON and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes MCP setup guidance, tool selection guidance, query patterns, and token-efficiency recommendations.]

## Skill Version(s):

2.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
