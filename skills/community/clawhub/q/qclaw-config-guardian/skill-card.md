## Description: <br>
QClaw Config Guardian helps agents back up QClaw/OpenClaw configuration, check version changes, and guide recovery after upgrades. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[codingduan](https://clawhub.ai/user/codingduan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and QClaw/OpenClaw operators use this skill to preserve channel, plugin, and cron task settings before or after upgrades and to diagnose configuration drift. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Backups may contain sensitive channel targets, plugin settings, schedules, or secrets embedded in configuration. <br>
Mitigation: Store backup files with appropriate local access controls and delete old backups when they are no longer needed. <br>
Risk: Restore or heartbeat workflows can affect local QClaw/OpenClaw task behavior after an upgrade. <br>
Mitigation: Confirm restore actions and automatic heartbeat behavior before applying changes to live cron or delivery configuration. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/codingduan/qclaw-config-guardian) <br>
- [SKILL.md](artifact/SKILL.md) <br>
- [backup_config.py](artifact/scripts/backup_config.py) <br>
- [check_config.py](artifact/scripts/check_config.py) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JSON reports and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write local backup JSON files under the user's QClaw/OpenClaw configuration backup directory.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
