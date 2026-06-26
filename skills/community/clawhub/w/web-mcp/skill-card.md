## Description: <br>
WebMCP helps developers add structured AI-agent tools to Next.js and React web applications using tool registration, an event bridge, and contextual tool loading. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[slemo54](https://clawhub.ai/user/slemo54) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill to make web applications accessible to AI agents by defining, registering, and wiring structured tools in Next.js or React projects. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The browser bridge exposes agent tools over cross-frame messages without origin checks. <br>
Mitigation: Add strict origin and source validation, and replace wildcard postMessage targets with trusted origins before production use. <br>
Risk: Mutating tools can allow agents to change application state. <br>
Mitigation: Require user confirmation for mutating or destructive tools and expose only the minimum status metadata needed. <br>
Risk: Sensitive form data could be routed through agent tools or persisted in localStorage. <br>
Mitigation: Avoid routing passwords through agent tools and do not store sensitive form fields in localStorage. <br>
Risk: Install commands that rely on npx or global npm packages can run unverified package code. <br>
Mitigation: Pin and verify npm package versions before running npx or installing packages globally. <br>


## Reference(s): <br>
- [WebMCP Specification Reference](references/webmcp-spec.md) <br>
- [WebMCP Specification](https://github.com/webmcp/spec) <br>
- [WebMCP Examples](https://github.com/webmcp/examples) <br>
- [WebMCP React Integration Guide](https://webmcp.dev/react) <br>
- [Model Context Protocol](https://modelcontextprotocol.io/) <br>
- [ClawHub Skill Page](https://clawhub.ai/slemo54/web-mcp) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with inline code blocks and generated TypeScript, JavaScript, and shell snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May generate or modify project files for WebMCP setup, tools, types, and Next.js/React integration.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
