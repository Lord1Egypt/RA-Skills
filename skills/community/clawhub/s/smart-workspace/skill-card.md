## Description:

Lightweight project file management skill that helps agents organize workspace files, match tasks to project history, create project folders, and update project records.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yaoweizhang](https://clawhub.ai/user/yaoweizhang)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to keep a workspace organized by matching tasks to existing project folders, creating new project folders when needed, and maintaining a PROJECT-HISTORY.md record.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill automatically scans workspace folder names, which can expose project names or other local metadata to the agent context.

Mitigation: Use it only in workspaces where project folder names are appropriate for the agent to inspect.

Risk: The skill can create folders and update PROJECT-HISTORY.md without confirmation.

Mitigation: Review PROJECT-HISTORY.md periodically and avoid enabling the skill in workspaces where unexpected local writes would be sensitive.

Risk: Project history entries may become inaccurate or misleading if task keywords match the wrong project.

Mitigation: Review matched folders and history entries before relying on them for ongoing project organization.

## Reference(s):

- [Smart Workspace ClawHub Page](https://clawhub.ai/yaoweizhang/skills/smart-workspace)
- [README](artifact/README.md)
- [Project History Template](artifact/PROJECT-HISTORY.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Files, Configuration instructions, Guidance]

**Output Format:** [Markdown guidance and workspace file updates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create project folders and update PROJECT-HISTORY.md in the active workspace.]

## Skill Version(s):

1.1.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
