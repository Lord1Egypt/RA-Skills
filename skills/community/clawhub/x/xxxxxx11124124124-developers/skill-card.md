## Description:

Longbridge helps agents use Longbridge CLI, MCP, Python and Rust SDKs, and documentation for market data, portfolio queries, trading workflows, and financial research.

This skill is ready for commercial/non-commercial use.

## Publisher:

[huacnlee](https://clawhub.ai/user/huacnlee)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, analysts, and AI-agent users use this skill to retrieve market data and news, inspect portfolios, configure Longbridge MCP or CLI access, and write Python or Rust integrations for quote and trade workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security summary flags an unsafe remote installer pattern.

Mitigation: Prefer Homebrew or verified release artifacts over the documented curl-to-shell installer.

Risk: The security summary flags broad access to sensitive financial and trading workflows.

Mitigation: Approve only the OAuth scopes required for the task and periodically revoke unused authorizations.

Risk: The skill can support order placement, cancellation, watchlist changes, and other account-impacting actions.

Mitigation: Require explicit user confirmation before any order placement, cancellation, watchlist change, or sensitive portfolio/account retrieval.

## Reference(s):

- [Longbridge OpenAPI Documentation](https://open.longbridge.com)
- [Longbridge llms.txt](https://open.longbridge.com/llms.txt)
- [Longbridge CLI Overview](references/cli/overview.md)
- [Longbridge MCP Server](references/mcp.md)
- [Longbridge Python SDK Overview](references/python-sdk/overview.md)
- [Longbridge Rust SDK Overview](references/rust-sdk/overview.md)
- [LLM and Markdown Integration](references/llm.md)
- [Longbridge Python SDK Documentation](https://longbridge.github.io/openapi/python/index.html)
- [Longbridge Rust SDK Documentation](https://longbridge.github.io/openapi/rust/longbridge/)
- [ClawHub Skill Page](https://clawhub.ai/huacnlee/skills/xxxxxx11124124124-developers)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with code blocks, shell commands, JSON snippets, and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include financial analysis and executable trading workflow examples; users should verify outputs before acting.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
