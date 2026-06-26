## Description: <br>
Intelligent single-file version management. Save, restore, diff, and clean file snapshots with per-file version history. Activate when users need version control, file snapshot management, or project state recovery. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[neuhanli](https://clawhub.ai/user/neuhanli) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to save, inspect, compare, restore, and clean per-file snapshots when they need lightweight version history or project state recovery without full-repository version control. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Shared snapshot storage can expose histories from other workspaces. <br>
Mitigation: Avoid snapshotting secrets, credentials, proprietary code, or personal files unless persistent local copies under ~/.workbuddy are acceptable. <br>
Risk: Restore and clean operations can affect snapshot history created outside the current workspace. <br>
Mitigation: Review the target file, version, and operation details carefully before setting confirm=True for restore or clean actions. <br>


## Reference(s): <br>
- [Version-Master usage reference](references/usage.md) <br>
- [ClawHub package page](https://clawhub.ai/neuhanli/version-master) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and command examples with JSON-like operation results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create, restore, diff, or delete local file snapshot records under shared local storage.] <br>

## Skill Version(s): <br>
2.1.1 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
