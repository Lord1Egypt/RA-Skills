## Description:

Workspace Trash provides soft-delete protection for workspace files by moving deletion targets to a recoverable trash instead of removing them permanently.

This skill is ready for commercial/non-commercial use.

## Publisher:

[crewhaus](https://clawhub.ai/user/crewhaus)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and coding agents use this skill to replace direct workspace deletion with recoverable trash operations, inspect trashed items, restore files, and empty trash after confirmation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A writable trash manifest could steer restore operations to move files outside the advertised OpenClaw scope.

Mitigation: Use only in trusted workspaces until restore validates manifest entries, rejects traversal, and rechecks source and destination scope immediately before moving files.

Risk: Emptying trash permanently deletes the trash contents.

Mitigation: Require explicit confirmation and show the trash contents before invoking the empty action.

## Reference(s):

- [Workspace Trash on ClawHub](https://clawhub.ai/crewhaus/skills/workspace-trash)
- [CrewHaus publisher profile](https://clawhub.ai/user/crewhaus)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and status text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce file movement actions and trash manifest updates when the agent invokes the bundled shell script.]

## Skill Version(s):

1.2.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
