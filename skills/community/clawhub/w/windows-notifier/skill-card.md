## Description: <br>
Send native Windows desktop notifications for local reminders, alerts, and background-attention events. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dougzl](https://clawhub.ai/user/dougzl) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agents use this skill to show local desktop popups for reminders, timers, alerts, and background-attention events when chat-only delivery may be missed. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill runs local Node and PowerShell commands and may fetch npm dependencies on first use. <br>
Mitigation: Install and run it only in trusted local environments where that command execution and dependency installation are acceptable. <br>
Risk: Notification text may be visible in local desktop popups. <br>
Mitigation: Avoid putting sensitive or confidential information in notification titles or messages. <br>


## Reference(s): <br>
- [ClawHub Windows Notifier page](https://clawhub.ai/dougzl/windows-notifier) <br>


## Skill Output: <br>
**Output Type(s):** [shell commands, guidance] <br>
**Output Format:** [Markdown guidance with PowerShell and Node command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands pass notification title, message, timeout, sound, mode, and app name options to a local desktop notification helper.] <br>

## Skill Version(s): <br>
1.1.1 (source: evidence.release.version) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
