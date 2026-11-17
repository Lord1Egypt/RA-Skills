## Description:

Guide for creating effective skills. This skill should be used when users want to create a new skill (or update an existing skill) that extends Claude's capabilities with specialized knowledge, workflows, or tool integrations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[86293073](https://clawhub.ai/user/86293073)

### License/Terms of Use:

Apache 2.0

## Use Case:

Developers and agent builders use this skill to design, scaffold, validate, and package agent skills with appropriate SKILL.md content, scripts, references, and assets.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The bundled packaging helper can accidentally include sensitive files through symlinks.

Mitigation: Package only dedicated skill directories that have been reviewed for symlinks and sensitive files; avoid packaging untrusted skill folders until symlink handling is hardened.

Risk: The bundled initializer can write outside the intended output directory when given unsafe names or paths.

Mitigation: Run initialization only in a dedicated workspace with simple hyphen-case skill names and verify the resolved output path before using generated files.

## Reference(s):

- [Workflow Patterns](references/workflows.md)
- [Output Patterns](references/output-patterns.md)
- [ClawHub Skill Page](https://clawhub.ai/86293073/skills/skill-creator-0-1-0)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline code and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or package local skill files when the bundled helper scripts are used.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
