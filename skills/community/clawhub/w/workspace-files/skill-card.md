## Description:

Work safely with files inside the OpenClaw workspace sandbox. Use for listing directories, reading text files, writing text files, and searching files by name inside ~/.openclaw/workspace only.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ecosincronia](https://clawhub.ai/user/ecosincronia)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to inspect, search, read, and write text files inside a fixed OpenClaw workspace sandbox.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The write command can create directories and overwrite existing workspace files.

Mitigation: Review proposed write paths and content before execution, and keep write operations limited to intended text files inside the OpenClaw workspace.

Risk: The skill exposes file listing, search, and read operations within the configured workspace.

Mitigation: Install it only for agents that should inspect files in that workspace, and avoid placing sensitive material there unless the agent is allowed to read it.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ecosincronia/skills/workspace-files)

## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Markdown with inline shell commands and plain text command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create directories and write or overwrite text files inside the configured OpenClaw workspace sandbox.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
