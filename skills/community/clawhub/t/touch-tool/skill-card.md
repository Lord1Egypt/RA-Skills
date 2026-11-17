## Description:

Create empty files or update file timestamps. Use for file creation, timestamp management, and build system operations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dinghaibin](https://clawhub.ai/user/dinghaibin)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use Touch Tool to create empty files and perform simple file timestamp operations during build, setup, and workflow tasks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The artifact documentation advertises timestamp flags and timestamp-update behavior that the included script may not implement.

Mitigation: Treat the release as a minimal file-creation helper unless the publisher fixes or verifies the timestamp behavior.

Risk: The helper can create files at paths it is asked to touch.

Mitigation: Run it only in intended workspaces and review requested paths before execution.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/dinghaibin/skills/touch-tool)

## Skill Output:

**Output Type(s):** [text, shell commands, files, guidance]

**Output Format:** [Markdown with inline shell commands and concise command results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates empty files at requested paths; advertised timestamp flags may not be implemented by the included script.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
