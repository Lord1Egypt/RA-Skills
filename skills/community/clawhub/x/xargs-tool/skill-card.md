## Description:

Build and execute command lines from standard input for batch processing, argument substitution, and command pipeline workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dinghaibin](https://clawhub.ai/user/dinghaibin)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to construct and run command-line batch operations from piped input. It is intended for xargs-style workflows such as processing file lists, applying substitutions, and chaining shell commands.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release security summary says the skill advertises safety and control options that the included script does not implement.

Mitigation: Review command behavior before installation and do not rely on --dry-run, -p, -0, -P, -n, or delimiter options unless the implementation is fixed.

Risk: The included script executes user-supplied commands over stdin-derived values.

Mitigation: Avoid destructive commands and untrusted pipeline input; test commands on non-sensitive paths before production use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/dinghaibin/skills/xargs-tool)

## Skill Output:

**Output Type(s):** [shell commands, text]

**Output Format:** [Command-line invocation with command output from executed subprocesses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May execute commands and produce filesystem or process side effects depending on the supplied command.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
