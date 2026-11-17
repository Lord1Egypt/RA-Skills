## Description:

WebMCP helps developers add structured, agent-accessible tool interfaces to Next.js/React web applications using tool registration, contextual loading, and an event bridge.

This skill is ready for commercial/non-commercial use.

## Publisher:

[slemo54](https://clawhub.ai/user/slemo54)

### License/Terms of Use:


## Use Case:

Developers and engineers use WebMCP to scaffold WebMCP support in Next.js/React applications, including core bridge files, hooks, provider components, generated types, and example tools for search, cart, auth, forms, chat, and dashboards.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The browser bridge and examples expose agent-callable web actions with weak origin and source checks.

Mitigation: Add strict postMessage origin and source validation, and use non-wildcard postMessage targets before exposing the bridge to users.

Risk: Mutating tools such as auth, cart, form, chat, and dashboard actions may run without explicit authorization or confirmation.

Mitigation: Require app-level authorization and user confirmation for mutating tools, and clearly distinguish read-only from state-changing tools with annotations.

Risk: Form draft examples can store sensitive user input in localStorage.

Mitigation: Avoid storing sensitive drafts in localStorage, or minimize and protect retained data with explicit retention behavior.

Risk: CLI and generator scripts copy and create project files.

Mitigation: Pin and verify the CLI package or source, review generated files before commit, and validate tool names and script inputs before running generators.

## Reference(s):

- [WebMCP Specification Reference](references/webmcp-spec.md)
- [WebMCP Specification](https://github.com/webmcp/spec)
- [WebMCP Example Projects](https://github.com/webmcp/examples)
- [WebMCP React Integration Guide](https://webmcp.dev/react)
- [Model Context Protocol](https://modelcontextprotocol.io/)
- [ClawHub Skill Page](https://clawhub.ai/slemo54/skills/web-mcp)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline bash, TypeScript, TSX, JavaScript, and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or modify project files for WebMCP integration and example tool definitions.]

## Skill Version(s):

1.0.0 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
