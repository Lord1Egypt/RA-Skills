## Description: <br>
Self Updater helps OpenClaw users check and apply OpenClaw core and skill updates with cron-aware scheduling, idle detection, risk assessment, approvals, and notifications. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[GhostDragon124](https://clawhub.ai/user/GhostDragon124) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw operators use this skill to keep OpenClaw core and installed skills up to date while avoiding scheduled tasks, waiting for idle time, and requiring approval for high-risk updates. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: This skill can change OpenClaw core and installed skills, including in automated runs. <br>
Mitigation: Install only when a privileged updater is intended, inspect the PowerShell updater and update source before enabling automation, and keep backups or rollback plans. <br>
Risk: AutoApprove or Quiet cron runs can apply updates without interactive review. <br>
Mitigation: Avoid unattended approval modes unless the environment has been tested and the update window is acceptable. <br>
Risk: Notification integrations may require Telegram or Feishu credentials. <br>
Mitigation: Use limited-scope notification credentials and store only the required environment variables. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/GhostDragon124/self-updater) <br>
- [Homepage](https://github.com/GhostDragon124/openclaw-self-updater#readme) <br>
- [README.md](artifact/README.md) <br>
- [SKILL.md](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, text] <br>
**Output Format:** [Markdown with PowerShell and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May describe update status, risk level, approval prompts, and notification setup.] <br>

## Skill Version(s): <br>
1.4.2 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
