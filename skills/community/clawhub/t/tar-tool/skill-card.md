## Description:

Create and extract tar archives with optional compression for file bundling, backup, and distribution.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dinghaibin](https://clawhub.ai/user/dinghaibin)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to create and extract tar archives during file bundling, backup, and distribution workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unsafe tar extraction may overwrite files outside the intended directory when processing a crafted archive.

Mitigation: Use only trusted archives in a disposable or tightly scoped directory until archive member paths are validated, unsafe links and traversal are rejected, an explicit destination is required, and overwrite controls are added.

## Reference(s):

- [Tar Tool on ClawHub](https://clawhub.ai/dinghaibin/skills/tar-tool)

## Skill Output:

**Output Type(s):** [Shell commands, Guidance]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Archive extraction should be limited to trusted archives or disposable directories because security evidence flags unsafe extraction behavior.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
