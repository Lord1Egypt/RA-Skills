## Description: <br>
Backs up and restores an OpenClaw agent workspace, including memory, configuration, credentials, skills, and cron jobs, through a Git repository. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[CrypticDriver](https://clawhub.ai/user/CrypticDriver) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to migrate an OpenClaw agent to a new instance, recover from a failed environment, set up recurring backups, or verify that workspace and configuration backups can be restored. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Workspace backups can commit live tokens, API keys, private memory, and recurring agent tasks to a Git repository. <br>
Mitigation: Use a private access-controlled remote, encrypt or exclude raw credential files, review git status before every push, and rotate any credentials that may already have been committed. <br>
Risk: Unattended cron backups may push sensitive or unintended files if paths and remotes are not scoped. <br>
Mitigation: Avoid unattended cron backups until paths and remotes are reviewed, and skip optional community-scan cron jobs unless they are explicitly wanted. <br>


## Reference(s): <br>
- [Cron Job Templates](references/cron-templates.md) <br>
- [ClawHub release page](https://clawhub.ai/CrypticDriver/soul-transfer) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, code] <br>
**Output Format:** [Markdown with shell commands, JSON configuration examples, and procedural checklists] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May reference a helper shell script for Git-based workspace backups.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
