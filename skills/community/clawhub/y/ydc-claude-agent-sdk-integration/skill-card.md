## Description:

Integrates Claude Agent SDK with the You.com HTTP MCP server for Python and TypeScript projects.

This skill is ready for commercial/non-commercial use.

## Publisher:

[edwardirby](https://clawhub.ai/user/edwardirby)

### License/Terms of Use:

MIT

## Use Case:

Developers use this skill to add You.com MCP search and content tools to Claude Agent SDK applications in Python or TypeScript, either by creating a new example file or updating an existing integration.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts, private data, or retrieved content may be sent through external Anthropic and You.com services.

Mitigation: Use the integration only when those services are intended, avoid sending sensitive prompts or private data, and review organization data-handling requirements before use.

Risk: API credentials may be exposed or over-scoped if copied into generated code or shared files.

Mitigation: Keep YDC_API_KEY and ANTHROPIC_API_KEY in environment variables or secret storage, use least-privilege keys where available, and do not hard-code secrets in source files.

Risk: Unpinned package installation commands can introduce dependency supply-chain drift.

Mitigation: Prefer pinned package versions and lockfiles for pip, npm, npx, or equivalent installation flows.

Risk: Generated or updated integration files may introduce incorrect configuration into a project.

Mitigation: Review generated file changes before applying or running them, especially MCP server URL, authorization header, allowed tools, and selected SDK version.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/edwardirby/skills/ydc-claude-agent-sdk-integration)
- [You.com MCP Server](https://documentation.you.com/developer-resources/mcp-server)
- [Claude Agent SDK for Python](https://platform.claude.com/docs/en/agent-sdk/python)
- [Claude Agent SDK for TypeScript](https://platform.claude.com/docs/en/agent-sdk/typescript)
- [Claude Agent SDK TypeScript v2 Preview](https://platform.claude.com/docs/en/agent-sdk/typescript-v2-preview)
- [You.com API keys](https://you.com/platform/api-keys)
- [Anthropic API keys](https://console.anthropic.com/settings/keys)

## Skill Output:

**Output Type(s):** [guidance, code, shell commands, configuration]

**Output Format:** [Markdown with Python and TypeScript code blocks and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires YDC_API_KEY and ANTHROPIC_API_KEY; supports Python 3.10+, Node.js 18+, and TypeScript 5.2+ for the TypeScript v2 path.]

## Skill Version(s):

1.0.0 (source: server release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
