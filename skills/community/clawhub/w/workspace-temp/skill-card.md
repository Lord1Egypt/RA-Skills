## Description:

Manage temporary files in workspace temp directory. All non-essential files must go to temp/, keeping workspace root clean. Auto-detects workspace from openclaw.json config.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lichenyang-zk](https://clawhub.ai/user/lichenyang-zk)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to keep temporary, cached, downloaded, and externally copied files in a session-scoped workspace temp directory instead of the workspace root.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reads OpenClaw workspace configuration and uses the session list to resolve a temp directory.

Mitigation: Confirm the required OpenClaw configuration access and session-list capability before enabling the skill.

Risk: User-specified external files may be copied into a workspace temp folder and may contain sensitive data.

Mitigation: Avoid routing secrets through the skill unless the temp directory can be reviewed and cleaned afterward.

Risk: Temporary files can remain in the workspace temp directory after processing.

Mitigation: Use the documented cleanup workflow for large, old, or session-residual temp files when cleanup is requested.

## Reference(s):

- [Workspace Temp on ClawHub](https://clawhub.ai/lichenyang-zk/skills/workspace-temp)

## Skill Output:

**Output Type(s):** [Guidance, Configuration, Files]

**Output Format:** [Markdown guidance with inline pseudocode and file-path conventions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guides agents to copy or create temporary files under <workspace>/temp/<session_id>/ and to avoid falling back to the workspace root.]

## Skill Version(s):

1.1.5 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
