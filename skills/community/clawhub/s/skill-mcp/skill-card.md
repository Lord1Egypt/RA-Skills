## Description:

The example skill shipped with skill-mcp shows the SKILL.md shape, a bundled reference file, and a declared runnable script.

This skill is for demonstration purposes and not for production usage.

## Publisher:

[chrischall](https://clawhub.ai/user/chrischall)

### License/Terms of Use:

MIT-0

## Use Case:

Skill developers use this example to check that skill-mcp is wired up and to learn how to describe bundled references and a runnable script in an SKILL.md file.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security scan was benign but only partially analyzed the script and reported a missing reference.

Mitigation: Review the declared script and check the scanner-reported missing reference before enabling execution.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/chrischall/skills/skill-mcp)
- [mcp-host declaration reference](references/declaration.md)

## Skill Output:

**Output Type(s):** [JSON, Guidance]

**Output Format:** [JSON output from the declared report script and Markdown usage instructions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The report includes the supplied arguments, working directory, environment variable names, and Node.js version.]

## Skill Version(s):

1.2.3 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
