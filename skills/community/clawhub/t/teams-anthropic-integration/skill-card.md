## Description:

Use @youdotcom-oss/teams-anthropic to add Anthropic Claude models (Opus, Sonnet, Haiku) to Microsoft Teams.ai applications. Optionally integrate You.com MCP server for web search and content extraction.

This skill is ready for commercial/non-commercial use.

## Publisher:

[edwardirby](https://clawhub.ai/user/edwardirby)

### License/Terms of Use:

MIT

## Use Case:

Developers and engineers use this skill to integrate Anthropic Claude models into Microsoft Teams.ai applications, with an optional You.com MCP path for web search and content extraction.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unreviewed or floating npm dependencies can introduce supply-chain or compatibility risk.

Mitigation: Use reviewed and pinned npm versions before installing or deploying the integration.

Risk: Anthropic and You.com API keys may be exposed if environment files are committed or shared.

Mitigation: Keep .env files out of source control, scope keys to the minimum needed access, and rotate keys on a regular schedule.

Risk: Teams messages or retrieved content may be processed by Anthropic and You.com services.

Mitigation: Confirm organizational approval for sending Teams app content and retrieved web content to those services before use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/edwardirby/skills/teams-anthropic-integration)
- [teams-anthropic package](https://github.com/youdotcom-oss/dx-toolkit/tree/main/packages/teams-anthropic)
- [Anthropic API console](https://console.anthropic.com/)
- [You.com MCP server documentation](https://documentation.you.com/developer-resources/mcp-server)
- [You.com API keys](https://you.com/platform/api-keys)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with bash and TypeScript code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes setup paths, model-selection guidance, environment-variable configuration, validation checklists, and troubleshooting notes.]

## Skill Version(s):

1.1.0 (source: SKILL.md frontmatter and server release metadata, released 2026-02-01)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
