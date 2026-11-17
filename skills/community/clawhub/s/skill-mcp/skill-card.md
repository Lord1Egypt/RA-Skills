## Description:

An example skill for checking skill-mcp integration and learning how to declare a runnable script and reference file.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chrischall](https://clawhub.ai/user/chrischall)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this example skill to check skill-mcp integration, inspect a declared script's runtime metadata, and learn how to declare runnable scripts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The demo script exposes environment variable names and runtime metadata in its tool result.

Mitigation: Run it in a constrained test environment without sensitive or revealing environment names.

## Reference(s):

- [skill-mcp release on ClawHub](https://clawhub.ai/chrischall/skills/skill-mcp)
- [mcp-host declaration reference](references/declaration.md)

## Skill Output:

**Output Type(s):** [Guidance, JSON]

**Output Format:** [Markdown guidance and JSON runtime report]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The runnable demo reports arguments, working directory, Node.js version, and environment variable names, not values.]

## Skill Version(s):

1.2.2 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
