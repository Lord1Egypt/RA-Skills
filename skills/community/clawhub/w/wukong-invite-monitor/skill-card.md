## Description: <br>
Monitors DingTalk Wukong invitation-code image version changes with local Tesseract OCR and heartbeat notifications without routine token use. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[teenyboy](https://clawhub.ai/user/teenyboy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to set up and run a lightweight monitor for DingTalk Wukong invitation-code image updates, local OCR extraction, logs, and optional heartbeat notification checks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Recurring cron jobs can continue network checks and local log or state writes after installation. <br>
Mitigation: Review cron commands before installing, preserve the existing crontab, and remove wukong cron lines when monitoring is no longer needed. <br>
Risk: Crontab setup guidance can replace or alter scheduled tasks if applied without review. <br>
Mitigation: Inspect generated cron content before applying it and keep a backup of the previous crontab. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/teenyboy/wukong-invite-monitor) <br>
- [README.md](README.md) <br>
- [QUICKSTART.md](QUICKSTART.md) <br>
- [HEARTBEAT.md](HEARTBEAT.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands, status text, log output, and JSON notification payloads] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create local cron entries, logs, state files, downloaded images, and notification files during use.] <br>

## Skill Version(s): <br>
2.1.0 (source: release evidence and _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
