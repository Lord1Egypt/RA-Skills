## Description: <br>
Backs up and restores the ~/.openclaw agent folder as GPG-encrypted, chunked snapshots stored in a private GitHub repository. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[KrishBhimani](https://clawhub.ai/user/KrishBhimani) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
OpenClaw users and agent operators use this skill to preserve, migrate, list, and recover OpenClaw agent state through encrypted snapshots in a private GitHub transport repository. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Restoring a snapshot can overwrite persistent OpenClaw agent state. <br>
Mitigation: Restore only after choosing the exact backup version, or intentionally choosing the latest backup, and restart OpenClaw after restore. <br>
Risk: Setup can run privileged package installation for GPG. <br>
Mitigation: Prefer installing GPG and gpg-agent through trusted system administration before running the skill setup script. <br>
Risk: Backups contain full OpenClaw agent state and rely on GitHub credentials plus BACKUP_PASSWORD. <br>
Mitigation: Use a dedicated private repository, a tightly scoped token, a protected and rotated BACKUP_PASSWORD, and review ~/.openclaw before backing up. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/KrishBhimani/snapshot) <br>
- [Publisher profile](https://clawhub.ai/user/KrishBhimani) <br>
- [GitHub personal access token settings](https://github.com/settings/tokens) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and environment-variable configuration] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces backup, restore, setup, and status guidance for OpenClaw snapshot workflows.] <br>

## Skill Version(s): <br>
1.2.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
