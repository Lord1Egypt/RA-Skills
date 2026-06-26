## Description: <br>
Detect unexpected system reboots and alert when the system comes back online. Tracks boot history and flags suspicious restarts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[elony-7](https://clawhub.ai/user/elony-7) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and system operators use this skill to check whether a machine has rebooted unexpectedly, record boot history, and optionally send a Telegram alert when the machine comes back online. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Telegram alerting uses a bot token and chat ID supplied by the user. <br>
Mitigation: Use a dedicated bot token, restrict ~/.rr-reboot-config to the owning user, and rotate the token if the machine is shared or compromised. <br>
Risk: A cron @reboot entry can continue sending reboot alerts after the agent is no longer active. <br>
Mitigation: Remove the crontab entry when automatic reboot alerts are no longer wanted. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/elony-7/rr-reboot-report-v2) <br>
- [Telegram Bot API endpoint used by the alert script](https://api.telegram.org) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, configuration] <br>
**Output Format:** [Status text or JSON from shell scripts, with Markdown setup guidance.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes local reboot state and history files; Telegram alerts require a user-created ~/.rr-reboot-config file.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
