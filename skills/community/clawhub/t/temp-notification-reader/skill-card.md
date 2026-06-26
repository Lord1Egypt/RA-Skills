## Description: <br>
Reads macOS Notification Center content and exports notification records or work summaries into OpenClaw memory so an agent can understand recent work activity. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gift-is-coding](https://clawhub.ai/user/gift-is-coding) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
OpenClaw users on macOS use this skill to collect recent notification titles and message bodies into local memory files, including filtered work summaries for tools such as Teams, Outlook, and WeChat. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads notification titles and message bodies, which may include sensitive personal or business information. <br>
Mitigation: Install only when local notification access is acceptable, prefer narrowly scoped work-summary runs, and review generated memory files. <br>
Risk: Granting broad macOS privacy access to python3 can expose more local data than this skill needs for a single run. <br>
Mitigation: Avoid granting Full Disk Access to /usr/bin/python3 unless the system-wide effect is understood and required. <br>
Risk: Scheduled exports can continuously store notification text in local OpenClaw memory. <br>
Mitigation: Prefer manual execution or conservative schedules, and use cleanup commands carefully because they permanently delete matching exports. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/gift-is-coding/temp-notification-reader) <br>
- [OpenClaw documentation](https://docs.openclaw.ai) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown files containing notification exports or work summaries, plus shell-command and configuration guidance.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes local files under OpenClaw memory or a configured output directory; lookback windows can be adjusted with environment variables.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
