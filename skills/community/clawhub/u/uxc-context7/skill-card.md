## Description: <br>
Query up-to-date library documentation and code examples using Context7 MCP for npm packages, Python libraries, and other programming languages. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jolestar](https://clawhub.ai/user/jolestar) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use this skill to resolve library identifiers and query current, version-specific documentation and code examples through Context7 MCP while working on implementation tasks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security scan marked the bundle suspicious because it may enable powerful workflows that should be inspected before installation. <br>
Mitigation: Install only in a trusted environment, review the skill contents before use, and require explicit human confirmation before applying any generated commands or workflow changes. <br>
Risk: The skill uses shell commands and a networked MCP endpoint, so queries and command setup depend on local tooling and external service availability. <br>
Mitigation: Confirm the uxc installation, inspect the fixed context7-mcp-cli link before reuse, and review command output before relying on returned documentation. <br>


## Reference(s): <br>
- [Context7 usage patterns](references/usage-patterns.md) <br>
- [Context7 MCP endpoint](https://mcp.context7.com/mcp) <br>
- [UXC skill](https://github.com/holon-run/uxc/tree/main/skills/uxc) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Text] <br>
**Output Format:** [Markdown guidance with inline shell commands and Context7 query examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce or summarize Context7 documentation query results; requires uxc and network access to the Context7 MCP endpoint.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
