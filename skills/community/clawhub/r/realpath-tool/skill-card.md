## Description:

Resolve relative paths and symbolic links to absolute canonical paths.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dinghaibin](https://clawhub.ai/user/dinghaibin)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to resolve a relative path, symlinked path, or ambiguous filesystem path into a canonical absolute path before using it in scripts or instructions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The helper may expose absolute filesystem paths for inputs supplied to it.

Mitigation: Use it only for paths whose absolute locations are acceptable to disclose, and avoid sharing outputs that contain sensitive directory names.

Risk: The included script is simpler than the documented CLI and does not implement the listed options.

Mitigation: Verify behavior in the target environment before relying on documented flags or multi-path usage.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/dinghaibin/skills/realpath-tool)

## Skill Output:

**Output Type(s):** [text, shell commands]

**Output Format:** [Plain text path output, with Markdown shell command examples in the skill documentation]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns one canonical absolute path for the provided path argument; defaults to the current directory when no path is provided.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
