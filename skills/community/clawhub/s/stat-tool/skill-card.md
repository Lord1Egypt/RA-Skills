## Description:

Display detailed file or filesystem status information. Use for checking file permissions, sizes, timestamps, and metadata.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dinghaibin](https://clawhub.ai/user/dinghaibin)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to inspect local file metadata such as size, permissions, ownership, timestamps, and file type when troubleshooting or reviewing filesystem state.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: File metadata such as existence, permissions, size, and timestamps can be sensitive.

Mitigation: Use the skill only on paths intended for inspection and avoid sharing generated metadata outside the intended review context.

Risk: The helper appears less feature-complete than the usage text suggests.

Mitigation: Review expected options and outputs before relying on the skill for complete stat-compatible behavior.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/dinghaibin/skills/stat-tool)

## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Markdown with inline shell command examples and text output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces local file metadata; no network access, persistence, or destructive actions were identified in the provided security evidence.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
