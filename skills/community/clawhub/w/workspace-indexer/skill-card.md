## Description:

Automatically maintains a workspace directory index using memory search, directory scanning, runtime status checks, and concise directory-level summaries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[harukaon](https://clawhub.ai/user/harukaon)

### License/Terms of Use:

MIT

## Use Case:

Developers and agent users use this skill to create and refresh WORKSPACE_INDEX.md for an OpenClaw workspace, capturing directory purpose, running status, related memories, and search keywords without deep project-file analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill combines persistent memory search, shell execution, runtime discovery, recurring automation, and workspace writes without enough scoping or confirmation.

Mitigation: Prefer manual use or enforce clear workspace-scope limits, confirmation, and overwrite checks before enabling scheduled runs.

Risk: The generated workspace index may expose memory references, workspace structure, running services, containers, or cleanup status.

Mitigation: Review and redact WORKSPACE_INDEX.md before committing, syncing, or sharing it outside the workspace.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/harukaon/skills/workspace-indexer)
- [Publisher Profile](https://clawhub.ai/user/harukaon)
- [Artifact README](artifact/README.md)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Files, Guidance]

**Output Format:** [Markdown file with directory-level summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes WORKSPACE_INDEX.md and may include workspace purpose, runtime status, related memory files, and search keywords.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact/skill.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
