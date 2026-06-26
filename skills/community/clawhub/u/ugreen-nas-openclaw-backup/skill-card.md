## Description: <br>
绿联NAS OpenClaw Docker部署的备份与恢复工具 / Ugreen NAS OpenClaw Docker deployment backup and restore tool. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zh40](https://clawhub.ai/user/zh40) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers running OpenClaw on Ugreen NAS use this skill to create tar-based backups of OpenClaw configuration, workspace, data, and skills, and to restore a selected backup when needed. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Backup archives contain OpenClaw configuration, data, workspace content, and skills. <br>
Mitigation: Store backup archives privately and handle them as sensitive deployment data. <br>
Risk: Restoring a backup overwrites the current OpenClaw state. <br>
Mitigation: Restore only trusted archives, confirm the target path, and make a fresh backup before overwriting current state. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zh40/ugreen-nas-openclaw-backup) <br>
- [Publisher profile](https://clawhub.ai/user/zh40) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires tar. Backup archives include OpenClaw configuration, data, workspace content, and skills.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
