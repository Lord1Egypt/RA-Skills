## Description: <br>
Lightweight project file management skill that helps agents organize workspace files by matching task keywords to project history, reusing existing folders, or creating new project folders. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yaoweizhang](https://clawhub.ai/user/yaoweizhang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to keep an agent workspace organized by scanning existing project folders, maintaining PROJECT-HISTORY.md, and routing new tasks into matching or newly created folders. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill automatically scans top-level workspace folders, creates project folders, and updates PROJECT-HISTORY.md without per-action confirmation. <br>
Mitigation: Install only in workspaces where automatic organization is acceptable, invoke explicitly in sensitive or tightly organized workspaces, and review PROJECT-HISTORY.md after first use. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/yaoweizhang/smart-workspace) <br>
- [README.md](artifact/README.md) <br>
- [PROJECT-HISTORY.md template](artifact/PROJECT-HISTORY.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Files, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with workspace file and folder changes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create project folders and update PROJECT-HISTORY.md in the current workspace.] <br>

## Skill Version(s): <br>
1.1.0 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
