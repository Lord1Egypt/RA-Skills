## Description: <br>
Backup, restore, initialize, and sync core OpenClaw workspace markdown files with the fixed private GitHub repository `soul-undead`. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhao95](https://clawhub.ai/user/zhao95) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to preserve, restore, and sync a fixed set of core workspace markdown files across installs or machines. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can upload sensitive OpenClaw identity and memory files to GitHub. <br>
Mitigation: Before running sync or initialization, verify the active `gh` account, confirm the destination private repository is intended, and review the tracked files for secrets. <br>
Risk: A first-time restore can overwrite local default workspace files from the remote repository. <br>
Mitigation: Use the pre-restore local backup snapshot under `skills/soul-undead/local-backups/` to recover files if the restored version is not intended. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zhao95/soul-undead) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with shell commands and status messages] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update local backup snapshots, a local initialization state file, and files in a private GitHub repository when executed.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
