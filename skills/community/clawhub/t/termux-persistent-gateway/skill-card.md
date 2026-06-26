## Description: <br>
Keep an AI agent gateway running persistently on Android/Termux using tmux, wake locks, boot startup, and health monitoring without systemd. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kingofqin2026](https://clawhub.ai/user/kingofqin2026) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers running AI agent gateways on Android/Termux use this skill to keep a gateway active across screen-off, app-switching, and device reboot. It provides shell scripts and setup guidance for tmux sessions, Termux wake locks, Termux:Boot startup, and periodic health checks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Wake-lock, boot startup, and scheduled restart behavior can keep a phone active and continue running the gateway persistently. <br>
Mitigation: Review the persistence setup before installing, monitor battery impact, and remove the Termux:Boot script, cron entry, and wake lock when persistent operation is no longer wanted. <br>
Risk: The configured gateway command and script path run automatically and may write sensitive gateway output to logs. <br>
Mitigation: Set GATEWAY_CMD and SCRIPT only to trusted commands and paths, and review generated logs for sensitive output. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with bash commands and configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes executable shell scripts and a Termux:Boot template in the artifact.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata; artifact frontmatter also states 1.1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
