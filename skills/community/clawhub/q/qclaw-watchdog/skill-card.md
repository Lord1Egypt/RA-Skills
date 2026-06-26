## Description: <br>
QClaw Watchdog monitors QClaw health, attempts automatic restarts when issues are detected, and sends Feishu alerts and command responses. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kf-liu](https://clawhub.ai/user/kf-liu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators who run QClaw use this skill to configure a local watchdog that checks QClaw health, sends Feishu status notifications, and responds to Feishu commands for status, start, restart, quit, config, and help. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The artifact includes real-looking Feishu credentials. <br>
Mitigation: Replace and revoke the bundled Feishu credentials before use, and prefer environment variables or a freshly generated local config. <br>
Risk: Remote Feishu commands can start, restart, or quit QClaw without visible sender authorization. <br>
Mitigation: Restrict command handling to trusted sender or chat IDs before enabling the bot. <br>
Risk: Background startup can keep service-disrupting automation running unattended. <br>
Mitigation: Verify credentials, authorization, and restart behavior before using nohup or LaunchAgent startup. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/kf-liu/qclaw-watchdog) <br>
- [Feishu developer platform](https://open.feishu.cn/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create local log files and uses Feishu interactive messages during operation.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and artifact version.txt) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
