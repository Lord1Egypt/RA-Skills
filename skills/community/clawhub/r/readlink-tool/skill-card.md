## Description:

Display the target of a symbolic link. Use for resolving symlinks to find the actual file or directory they point to.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dinghaibin](https://clawhub.ai/user/dinghaibin)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to inspect where a symbolic link points and resolve symlink chains while working with filesystems.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Advertised options may not work with the bundled script unless the runtime provides a separate readlink-tool wrapper.

Mitigation: Install only when a simple symlink inspection helper is needed, and verify option handling in the target runtime before relying on canonicalization flags.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Plain text path output with concise Markdown command guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
