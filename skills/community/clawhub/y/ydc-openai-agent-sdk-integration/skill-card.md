## Description:

Helps developers configure the OpenAI Agents SDK with You.com's MCP server using Hosted MCP or Streamable HTTP in Python or TypeScript.

This skill is ready for commercial/non-commercial use.

## Publisher:

[edwardirby](https://clawhub.ai/user/edwardirby)

### License/Terms of Use:

MIT

## Use Case:

Developers use this skill to add You.com MCP search and content tools to OpenAI Agents SDK projects. It supports new files and existing integrations with setup guidance, environment variables, and ready-to-run Python or TypeScript templates.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated or updated files can contain incorrect integration details if copied without review.

Mitigation: Review the generated file before running it and test with non-production API keys where possible.

Risk: Configured agents may send prompts or tool queries to You.com MCP and OpenAI services.

Mitigation: Confirm that prompts, tool queries, and retrieved content are appropriate for those external services before deployment.

Risk: Unpinned package versions can change behavior over time.

Mitigation: Pin package versions for production use and re-test the integration after dependency updates.

## Reference(s):

- [OpenAI Agents SDK for Python](https://openai.github.io/openai-agents-python/)
- [OpenAI Agents SDK for TypeScript](https://openai.github.io/openai-agents-js/)
- [OpenAI Agents SDK MCP Configuration for Python](https://openai.github.io/openai-agents-python/mcp/)
- [OpenAI Agents SDK MCP Configuration for TypeScript](https://openai.github.io/openai-agents-js/guides/mcp/)
- [You.com MCP Server Documentation](https://documentation.you.com/developer-resources/mcp-server)
- [ClawHub Skill Page](https://clawhub.ai/edwardirby/skills/ydc-openai-agent-sdk-integration)

## Skill Output:

**Output Type(s):** [guidance, markdown, code, shell commands, configuration]

**Output Format:** [Markdown guidance with Python, TypeScript, and shell code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces integration instructions and templates for either Hosted MCP or Streamable HTTP.]

## Skill Version(s):

1.0.0 (source: frontmatter and server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
