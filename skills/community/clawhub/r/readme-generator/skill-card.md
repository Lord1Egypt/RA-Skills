## Description:

Generate a production-quality README.md by analyzing project structure, framework, and code

This skill is ready for commercial/non-commercial use.

## Publisher:

[fratua](https://clawhub.ai/user/fratua)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to have an agent inspect project files, infer the framework and tooling, and draft a framework-aware README.md. It supports common project types and asks before overwriting an existing README.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad trigger phrases can cause the agent to start README generation for an unintended project.

Mitigation: Confirm the intended project root before allowing the skill to inspect files or draft documentation.

Risk: Generated README content can include incorrect framework, command, license, or configuration details.

Mitigation: Review generated README changes before accepting them, especially when README.md already exists.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/fratua/skills/readme-generator)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown file with optional inline shell commands and generated badges]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes README.md in the project root, or offers README.generated.md when README.md already exists.]

## Skill Version(s):

1.0.0 (source: artifact/SKILL.md frontmatter and evidence.release.version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
