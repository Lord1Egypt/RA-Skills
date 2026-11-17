## Description:

Workspace Project Standard guides OpenClaw agents to organize project work into self-contained directories with a three-layer documentation structure.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lnshyo](https://clawhub.ai/user/lnshyo)

### License/Terms of Use:


## Use Case:

Developers and agent operators use this skill when starting a project, organizing an existing workspace, or creating project documentation. It helps keep project code, temporary work, and agent-maintained records in predictable locations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill directs agents to immediately move root-level files that are not on its whitelist, which may disrupt unrelated workspace data.

Mitigation: Require the agent to list proposed file moves and obtain explicit approval before relocating files.

Risk: The workspace layout may conflict with projects that already use different root files or tool-managed directories.

Mitigation: Review the whitelist against the current workspace before applying the standard.

## Reference(s):

- [ClawHub Skill Release](https://clawhub.ai/lnshyo/skills/workspace-project-standard)
- [Project Documentation Template](artifact/assets/project-template.md)
- [Links and Paths Template](artifact/assets/links-template.md)

## Skill Output:

**Output Type(s):** [guidance, markdown, shell commands, configuration]

**Output Format:** [Markdown guidance with templates and inline PowerShell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces workspace organization instructions and documentation templates for agents.]

## Skill Version(s):

1.0.1 (source: server release metadata; artifact skill.json reports 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
