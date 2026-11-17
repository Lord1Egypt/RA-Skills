## Description:

Read from stdin and write to both stdout and files. Use for saving pipe output while still displaying it on screen.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dinghaibin](https://clawhub.ai/user/dinghaibin)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to save command output from a pipeline while still viewing it in the terminal.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The bundled implementation overwrites the target file and does not implement the documented append or interrupt options.

Mitigation: Use it only when replacing the target file is intended, and do not rely on documented option behavior unless the implementation is updated.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/dinghaibin/skills/tee-tool)

## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Markdown with inline shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces guidance for tee-like pipe usage; the bundled implementation writes stdin to stdout and overwrites a target file.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
