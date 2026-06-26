## Description: <br>
Qmsg Push sends QQ push notifications through Qmsg using a locally configured Qmsg key. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[timethreesecond](https://clawhub.ai/user/timethreesecond) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and automation users can use this skill to send task completion alerts, reminders, and system status notifications to QQ through Qmsg. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a Qmsg key stored locally. <br>
Mitigation: Treat the Qmsg key as a secret, keep it out of logs and version control, and restrict permissions on the secrets file. <br>
Risk: Notification contents are sent to qmsg.zendee.cn. <br>
Mitigation: Do not send tokens, passwords, personal data, or sensitive command output through this skill. <br>


## Reference(s): <br>
- [Qmsg service](https://qmsg.zendee.cn) <br>
- [ClawHub skill page](https://clawhub.ai/timethreesecond/qmsg-push-skills) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Configuration, API calls] <br>
**Output Format:** [Markdown instructions with shell commands and JSON-like script responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses a locally stored Qmsg key and sends notification text to qmsg.zendee.cn.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
