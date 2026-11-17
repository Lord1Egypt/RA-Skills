## Description:

Display the last lines of files for checking recent file or log entries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dinghaibin](https://clawhub.ai/user/dinghaibin)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to inspect the end of local files or logs when checking recent activity.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The artifact documentation advertises follow, byte, quiet, and multi-file behavior that the implementation does not fully provide.

Mitigation: Use the skill only for basic last-N-lines viewing unless the implementation is updated and retested for those options.

Risk: The implementation can be inefficient on very large files or never-ending input streams.

Mitigation: Avoid huge files and never-ending streams; use a dedicated system tail command for high-volume or continuous log monitoring.

## Reference(s):


## Skill Output:

**Output Type(s):** [Text, Shell commands, Guidance]

**Output Format:** [Plain text and Markdown with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces a single stream of last-N-line file output or usage guidance.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
