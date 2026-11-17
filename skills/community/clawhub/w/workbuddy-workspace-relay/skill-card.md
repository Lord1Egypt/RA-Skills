## Description:

Helps a WorkBuddy user move an active project to another device by creating an encrypted .wbpack with project files, local rules, uncommitted changes, and handoff context, or by restoring one to continue work.

This skill is ready for commercial/non-commercial use.

## Publisher:

[taogeo](https://clawhub.ai/user/taogeo)

### License/Terms of Use:

MIT-0

## Use Case:

External WorkBuddy users and developers use this skill to package a current project workspace for transfer to another device or restore a .wbpack package so an agent can continue from the included handoff context. It is not positioned as cloud sync, real-time collaboration, ordinary Git sync, or deployment tooling.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The migration package can contain sensitive project files, project-local .env secrets, Git history, and agent instructions.

Mitigation: Use strong passphrases, transfer .wbpack files like confidential credentials, and package only workspaces intended for migration.

Risk: Restoring a package imports project-local agent rules, skills, and handoff context that may influence subsequent agent behavior.

Mitigation: Restore only packages from trusted sources and review imported rules and handoff context before continuing agent work.

Risk: The security evidence flags the release as suspicious because it handles sensitive workspace migration with too little user control.

Mitigation: Review the scanner guidance and release behavior before deployment, especially in environments that require explicit control over migrated secrets and agent instructions.

## Reference(s):

- [Agent workflow](references/agent-workflow.md)
- [Package format](references/package-format.md)

## Skill Output:

**Output Type(s):** [Files, Markdown, Shell commands, Guidance]

**Output Format:** [Encrypted .wbpack file, Markdown handoff, and JSON status from command-line operations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires age or a compatible local age component; restored files are validated before placement and are not executed automatically.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
