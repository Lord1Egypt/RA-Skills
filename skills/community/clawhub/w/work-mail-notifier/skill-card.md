## Description: <br>
Monitors QQ work-mail folders for new messages, groups notifications by urgency, and lets users display selected message bodies or mark selected messages as read. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhangjiongjie](https://clawhub.ai/user/zhangjiongjie) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees or developers with QQ work-mail accounts use this skill to check recent work-mail notifications, inspect selected message bodies, and mark numbered messages as read from an agent workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill accesses QQ work-mail metadata and can display full selected email bodies. <br>
Mitigation: Install only for accounts and folders the user expects the agent to access, and avoid showing sensitive message bodies in shared sessions. <br>
Risk: The skill stores recent notification references and anchor IDs in local OpenClaw workspace data files. <br>
Mitigation: Clear the local workspace data files when notification history should no longer be retained. <br>
Risk: The skill can mark selected messages as read through the configured himalaya account. <br>
Mitigation: Review the numbered message list before marking messages read and confirm the configured account and folders are correct. <br>


## Reference(s): <br>
- [Work Mail Notifier on ClawHub](https://clawhub.ai/zhangjiongjie/work-mail-notifier) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Plain text or Markdown-style text with numbered message references and command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Notifications are grouped by alert/risk, failure/exception, and normal categories; selected messages can be shown or marked read by number.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
