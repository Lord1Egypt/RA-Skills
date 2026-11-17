## Description:

Query up-to-date, version-specific library documentation and code examples through Context7 MCP.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jolestar](https://clawhub.ai/user/jolestar)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to resolve library identifiers and query current documentation or code examples for npm packages, Python libraries, and other programming ecosystems.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends documentation queries to the external Context7 MCP service.

Mitigation: Confirm external service use is acceptable before installation and avoid sending proprietary or sensitive query content.

Risk: The skill may create or reuse a fixed context7-mcp-cli command link through the uxc skill.

Mitigation: Check for command conflicts first and stop for maintainer review if the fixed command name cannot be safely reused.

Risk: Documentation coverage and library matches can vary by package.

Mitigation: Resolve the library ID before querying, choose the best match when multiple libraries are returned, and review results before applying guidance.

## Reference(s):

- [Context7 Usage Patterns](references/usage-patterns.md)
- [UXC skill](https://github.com/holon-run/uxc/tree/main/skills/uxc)
- [Context7 MCP endpoint](https://mcp.context7.com/mcp)
- [ClawHub skill page](https://clawhub.ai/jolestar/skills/uxc-context7)
- [Publisher profile](https://clawhub.ai/user/jolestar)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Agent output may include Context7 query results and command suggestions; coverage varies by library.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
