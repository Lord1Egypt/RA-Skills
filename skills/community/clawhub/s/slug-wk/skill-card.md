## Description:

Guide for creating effective skills. This skill should be used when users want to create a new skill (or update an existing skill) that extends Claude's capabilities with specialized knowledge, workflows, or tool integrations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wangkang5](https://clawhub.ai/user/wangkang5)

### License/Terms of Use:

Apache 2.0

## Use Case:

Developers and agent builders use this skill to design, initialize, validate, package, and iterate on agent skills with clear instructions, focused resources, and reusable helper scripts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Helper scripts may read or write outside the intended skill folder in edge cases.

Mitigation: Use the skill only with trusted local skill directories, keep paths simple, and confirm generated or packaged paths before execution.

Risk: Packaging an untrusted skill folder may include unexpected files or symlinked content.

Mitigation: Inspect the target folder and symlinks before packaging, and avoid packaging untrusted skill directories.

## Reference(s):

- [Workflow Patterns](artifact/references/workflows.md)
- [Output Patterns](artifact/references/output-patterns.md)
- [ClawHub Skill Page](https://clawhub.ai/wangkang5/skills/slug-wk)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline code blocks and optional generated skill files or .skill packages]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or package local skill directories when the helper scripts are run.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
