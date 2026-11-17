## Description:

Create professional terminal recordings with VHS tape files - guides through syntax, timing, settings, and best practices.

This skill is ready for commercial/non-commercial use.

## Publisher:

[killerapp](https://clawhub.ai/user/killerapp)

### License/Terms of Use:


## Use Case:

Developers and documentation authors use this skill to create VHS tape files for CLI demos, README animations, and documentation videos.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill includes hidden and overbroad destructive command examples that users or agents could run.

Mitigation: Run tape files only in disposable test directories or containers, and replace destructive cleanup commands with narrowly scoped demo-resource cleanup.

Risk: The skill depends on third-party terminal recording tools and command examples that may affect the local environment.

Mitigation: Review generated tape files before execution, confirm prerequisites, and pin third-party tools where possible.

## Reference(s):

- [VHS Tape File Syntax Reference](references/vhs-syntax.md)
- [VHS Timing Control Reference](references/timing-control.md)
- [VHS Settings Reference](references/settings.md)
- [VHS Recording Examples](references/examples.md)

## Skill Output:

**Output Type(s):** [Markdown, Code, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown with VHS tape snippets and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include generated tape-file structure, timing guidance, output-format recommendations, and command examples for VHS recordings.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
