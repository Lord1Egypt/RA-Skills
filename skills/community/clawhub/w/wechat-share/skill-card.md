## Description:

Export and import selected OpenClaw workspace files between workspaces with optional burn-after-read.

This skill is ready for commercial/non-commercial use.

## Publisher:

[liuhao6741](https://clawhub.ai/user/liuhao6741)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to share selected workspace-relative text files with another workspace, preview received shares, and import them after reviewing overwrite and path risks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Selected workspace files may contain secrets, profile data, memory, or files that affect future agent behavior.

Mitigation: Review the file list before upload or import, avoid sharing sensitive files unless intentional, and compare sensitive destinations before overwriting.

Risk: Share credentials can allow access to uploaded files while the share remains available.

Mitigation: Treat db_id and api_token as passwords, forward them only to trusted recipients, and use burn or delete for shares that should not stay accessible.

Risk: Imported files can overwrite existing workspace files or change agent instructions.

Mitigation: Run preview first, verify paths and overwrite warnings, and import only after the share contents match the user's intent.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/liuhao6741/skills/wechat-share)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Configuration instructions, Files]

**Output Format:** [Markdown with inline slash commands, shell commands, and file lists]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce workspace file shares, preview summaries, import results, and burn-after-read status.]

## Skill Version(s):

1.0.8 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
