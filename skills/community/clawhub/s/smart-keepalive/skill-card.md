## Description: <br>
Smart Keepalive fetches brief source items, uses OpenClaw or configured commands to format them into scheduled keepalive briefings, and sends them with optional wellness and status notes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[east5ringroad-kyle](https://clawhub.ai/user/east5ringroad-kyle) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to configure scheduled OpenClaw, Hermes, or custom-command keepalive messages that fetch source items, generate a concise briefing, and send it to a chosen channel or target. It also provides troubleshooting guidance for CLI resolution, delivery failures, logs, and launchd or cron scheduling. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The scheduled workflow fetches internet sources, invokes OpenClaw or custom commands, and sends messages automatically. <br>
Mitigation: Install only in trusted environments, review channel and target settings, and run the documented doctor or manual-send checks before unattended scheduling. <br>
Risk: Custom agent or send commands can execute shell commands with keepalive prompt, message, channel, and target environment variables. <br>
Mitigation: Do not set KEEPALIVE_AGENT_COMMAND, KEEPALIVE_SEND_COMMAND, source URL overrides, or scheduler settings from untrusted input. <br>
Risk: Logs, state files, rest reminders, or generated status footers may reveal recent activity or message content. <br>
Mitigation: Use appropriate log locations and retention, and disable KEEPALIVE_REST_REMINDER or KEEPALIVE_STATUS_FOOTER when those privacy signals are not desired. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/east5ringroad-kyle/smart-keepalive) <br>
- [Publisher profile](https://clawhub.ai/user/east5ringroad-kyle) <br>
- [Skill documentation](artifact/SKILL.md) <br>
- [Main rewrite prompt](artifact/prompts/rewrite-main.md) <br>
- [Status footer prompt](artifact/prompts/status-footer.md) <br>
- [Wellness prompt](artifact/prompts/wellness.md) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown messages, shell commands, environment-variable settings, and operational troubleshooting guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write local logs and state files, invoke OpenClaw or custom commands, and send scheduled messages when configured.] <br>

## Skill Version(s): <br>
0.1.5 (source: server evidence release.version) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
