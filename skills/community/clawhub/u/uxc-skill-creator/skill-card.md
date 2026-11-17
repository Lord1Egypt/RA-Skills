## Description:

Create wrapper skills that call remote tools through UXC. Use when defining a new provider skill and you need reusable templates, validation rules, and anti-pattern guidance based on proven UXC skill practices.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jolestar](https://clawhub.ai/user/jolestar)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to create standardized UXC-based provider wrapper skills with reusable templates, validation checks, and guidance for link-first, help-first command flows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide an agent to probe user-provided provider endpoints through UXC.

Mitigation: Use trusted endpoints, avoid private or local network targets unless intentional, and review endpoint candidates before probing.

Risk: Generated shell command examples may include user-controlled host values.

Mitigation: Validate and safely quote host values before executing generated commands.

Risk: Generated wrapper skills may include high-impact write operations for a provider.

Mitigation: Require read-before-write behavior and explicit user confirmation for destructive or high-impact writes.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/jolestar/skills/uxc-skill-creator)
- [Workflow](references/workflow.md)
- [Templates](references/templates.md)
- [Validation Rules](references/validation-rules.md)
- [Anti-Patterns](references/anti-patterns.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with YAML and shell code snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces proposed skill files and validation commands for agent review before installation or release.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
