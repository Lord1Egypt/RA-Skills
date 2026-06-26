## Description: <br>
Automates qwen-portal OAuth authentication by using tmux to obtain login links, monitor OpenClaw task health, and guide task recovery. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jazzqi](https://clawhub.ai/user/jazzqi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw operators use this skill to recover and monitor qwen-portal authentication for scheduled tasks when interactive OAuth login is unavailable or expired. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can add persistent monitoring through crontab changes. <br>
Mitigation: Back up and review the user's crontab before enabling monitoring, and confirm the scheduled command path and log destination. <br>
Risk: The recovery script can rewrite OpenClaw cron job state. <br>
Mitigation: Reset only verified qwen-portal task IDs and keep a backup of the OpenClaw cron jobs file before making changes. <br>
Risk: OAuth links, device codes, and diagnostic details may be written to local temporary logs. <br>
Mitigation: Treat OAuth details as sensitive and delete or protect /tmp qwen OAuth logs and reports after use. <br>
Risk: The skill runs local tmux and OpenClaw commands during authentication recovery. <br>
Mitigation: Run it only in a trusted local user environment with the expected tmux and openclaw binaries installed. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/jazzqi/qwen-portal-auth-helper) <br>
- [Publisher Profile](https://clawhub.ai/user/jazzqi) <br>
- [Skill Instructions](artifact/SKILL.md) <br>
- [README](artifact/README.md) <br>
- [Quick Recovery Example](artifact/examples/quick-recovery.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and local report file paths] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce OAuth links and device codes, local /tmp reports, cron entries, and OpenClaw task-state update guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence, package.json, and skill metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
