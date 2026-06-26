## Description: <br>
Backup and restore OpenClaw agent configuration, skills, memory, and workspace files. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[liuyue8135](https://clawhub.ai/user/liuyue8135) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
OpenClaw users and agent operators use this skill to create local restore points for agent configuration, skills, memory, credentials, cron jobs, and selected workspace files, then restore that state on the same or a new machine. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Backups may contain API tokens, credentials, identity files, memories, skills, cron jobs, and selected workspace documents. <br>
Mitigation: Keep backup archives private or encrypted and do not share them. <br>
Risk: Restoring an archive can overwrite current OpenClaw state or unsafe paths. <br>
Mitigation: Restore only from trusted archives, preview the archive contents before restoring, and keep a current pre-restore backup. <br>


## Reference(s): <br>
- [OpenClaw Self Backup & Restore on ClawHub](https://clawhub.ai/liuyue8135/yuebao-self-backup) <br>


## Skill Output: <br>
**Output Type(s):** [shell commands, configuration, guidance, files] <br>
**Output Format:** [Markdown with inline shell commands and local archive files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local tar.gz backup archives and restore guidance for OpenClaw state.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
