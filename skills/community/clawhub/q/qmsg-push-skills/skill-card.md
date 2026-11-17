## Description:

Qmsg Push sends QQ notification messages through qmsg.zendee.cn using a configured Qmsg key.

This skill is ready for commercial/non-commercial use.

## Publisher:

[timethreesecond](https://clawhub.ai/user/timethreesecond)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and automation users use this skill to send QQ status notifications, completion alerts, and timed reminders from agent or automation workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reads a local Qmsg key and sends message text to qmsg.zendee.cn.

Mitigation: Use a dedicated Qmsg-only secret, keep unrelated credentials out of the same secrets.json file, and avoid sending sensitive message content.

Risk: Failures may expose request details in logs or command output.

Mitigation: Treat logs as potentially sensitive and review them before sharing or retaining them.

## Reference(s):

- [Qmsg](https://qmsg.zendee.cn)
- [ClawHub skill page](https://clawhub.ai/timethreesecond/skills/qmsg-push-skills)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration]

**Output Format:** [Text message sent to QQ with a JSON command result]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a Qmsg key in secrets.json; message text is sent to qmsg.zendee.cn.]

## Skill Version(s):

0.1.0 (source: server release metadata; artifact frontmatter states 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
