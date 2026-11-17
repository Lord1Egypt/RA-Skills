## Description:

Guide for creating effective skills. This skill should be used when users want to create a new skill or update an existing skill that extends an agent's capabilities with specialized knowledge, workflows, or tool integrations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wangkang5](https://clawhub.ai/user/wangkang5)

### License/Terms of Use:

Apache 2.0

## Use Case:

Developers and skill authors use this skill to design, create, validate, package, and iterate on agent skills with clear instructions and reusable resources.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The packaging helper can accidentally include files outside the intended skill directory through symlinks.

Mitigation: Use the skill only on directories you control, check for symlinks and unexpected files before packaging, and run packaging in a contained workspace.

Risk: Initializer inputs can create files at user-provided paths.

Mitigation: Avoid untrusted skill names or output paths, and review the target path before running the initializer.

## Reference(s):

- [Workflow Patterns](artifact/references/workflows.md)
- [Output Patterns](artifact/references/output-patterns.md)
- [ClawHub skill page](https://clawhub.ai/wangkang5/skills/wangkang-skill-c)

## Skill Output:

**Output Type(s):** [guidance, markdown, code, shell commands, configuration]

**Output Format:** [Markdown guidance with inline code blocks and optional generated files or shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create SKILL.md, resource folders, validation output, and .skill package files when helper scripts are used.]

## Skill Version(s):

1.3.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
