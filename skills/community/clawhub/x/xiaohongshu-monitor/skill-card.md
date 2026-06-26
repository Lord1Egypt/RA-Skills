## Description: <br>
Monitors configured Xiaohongshu bloggers for new posts, keeps snapshots to avoid duplicate alerts, and sends Feishu notifications. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[KMKNKK](https://clawhub.ai/user/KMKNKK) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Individuals or operators use this skill to monitor configured Xiaohongshu profiles on a schedule and receive Feishu alerts when new posts appear. It is useful when repeated manual checking would be inefficient. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reuses a logged-in Xiaohongshu browser profile, so saved session data may remain on the machine after monitoring. <br>
Mitigation: Use a dedicated Xiaohongshu/OpenClaw browser profile where possible, and remove saved browser session data when monitoring is no longer needed. <br>
Risk: Alert contents are sent to a fixed Feishu recipient that users cannot configure in the release artifact. <br>
Mitigation: Review the script before installing and replace the hard-coded Feishu target with the intended recipient or disable messaging. <br>
Risk: Scheduled monitoring can continue after the user no longer wants notifications or data collection. <br>
Mitigation: Review any cron schedule before use and know how to stop the cron job and remove generated logs and snapshots. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/KMKNKK/xiaohongshu-monitor) <br>
- [Configured Xiaohongshu profile](https://www.xiaohongshu.com/user/profile/5b6150c56b58b741e26b8c7f) <br>


## Skill Output: <br>
**Output Type(s):** [shell commands, markdown, configuration, guidance] <br>
**Output Format:** [Markdown guidance with bash commands; runtime logs, snapshot markdown files, and Feishu notification text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates or updates workspace memory files and may send Feishu messages through OpenClaw.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
