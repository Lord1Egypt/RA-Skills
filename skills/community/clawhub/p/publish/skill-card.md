## Description: <br>
Backup and restore your OpenClaw workspace to GitHub. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nickconstantinou](https://clawhub.ai/user/nickconstantinou) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External developers and OpenClaw users use this skill to back up workspace skills, scripts, and project code to a GitHub repository and restore selected workspace content when needed. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The backup may upload more workspace content than its documentation promises if the safer filtered copy path fails. <br>
Mitigation: Install and use rsync, review files staged for backup before pushing, and use a private GitHub repository. <br>
Risk: A broad or exposed GitHub token could allow unintended access to backed-up workspace content. <br>
Mitigation: Use a fine-grained token limited to the backup repository with only the permissions required for content writes. <br>
Risk: Restoring from an untrusted repository can affect future agent behavior through restored workspace or agent configuration files. <br>
Mitigation: Restore only from repositories you fully trust and review restored content before using the workspace. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/nickconstantinou/publish) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with bash command blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires BACKUP_REPO, OPENCLAW_WORKSPACE, and usually GITHUB_TOKEN; performs GitHub backup and restore operations through bundled shell scripts.] <br>

## Skill Version(s): <br>
1.0.12 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
