## Description:

Xiaolongxia Assistant is an OpenClaw plugin development assistant that outputs runnable plugin scaffolds, installation commands, and debugging steps.

This skill is ready for commercial/non-commercial use.

## Publisher:

[boleyn](https://clawhub.ai/user/boleyn)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to decide whether an OpenClaw customization should be a Skill or Plugin, generate a minimal runnable plugin skeleton, and obtain install, debug, publish, and rollback commands.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated plugin code or shell commands can modify a local OpenClaw setup if run without review.

Mitigation: Review generated install, publish, rollback, and code outputs before execution; test changes locally before release.

## Reference(s):

- [Xiaolongxia Assistant on ClawHub](https://clawhub.ai/boleyn/skills/xiaolongxia-assistant)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with file outlines, code blocks, shell commands, and troubleshooting guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated commands are intended to be copied and reviewed before execution.]

## Skill Version(s):

1.0.1 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
