## Description:

Sends WeCom text messages for reports, notifications, and alerts, with support for sender labels and user, department, or tag recipients.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xiaoqiangclub](https://clawhub.ai/user/xiaoqiangclub)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to send WeCom notifications from scripts, scheduled jobs, monitoring workflows, and reporting tasks. It can send simple text messages or formatted task reports, job updates, alerts, summaries, and custom messages.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: WeCom application secrets may be exposed if passed through command-line arguments or logged automation.

Mitigation: Prefer environment variables or a protected secret store, avoid the -k/--corp-secret option, and rotate the WeCom secret if it has been used in shell commands or logs.

Risk: Messages may be sent broadly when the default recipient is @all.

Mitigation: Set explicit touser, toparty, or totag values and use @all only when broad delivery is intended.

Risk: The python-dotenv dependency affects how local configuration and secrets are loaded.

Mitigation: Pin python-dotenv to a reviewed version before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/xiaoqiangclub/skills/send-to-me)
- [WeCom configuration tutorial](https://xiaoqiangclub.blog.csdn.net/article/details/144614019)
- [WeCom gettoken API endpoint](https://qyapi.weixin.qq.com/cgi-bin/gettoken)
- [WeCom message send API endpoint](https://qyapi.weixin.qq.com/cgi-bin/message/send)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Plain text and Markdown with Python and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces WeCom text-message content and invocation guidance; message delivery depends on valid WeCom credentials and recipient configuration.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
