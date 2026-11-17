## Description:

Sends text or Markdown notifications to Enterprise WeChat group webhooks, including optional user mentions and scheduled reminder examples.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xiekch](https://clawhub.ai/user/xiekch)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to send WeCom group notifications from an agent or shell command, and to set up recurring reminder tasks with OpenClaw cron.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Webhook keys can be exposed through shell history, cron task text, or shared command examples.

Mitigation: Avoid placing live webhook keys directly in reusable command text, rotate any exposed key, and restrict access to important group webhooks.

Risk: Untrusted message content can alter, break, or malformed the shell-constructed JSON payload.

Mitigation: Review or sanitize forwarded content before passing it to the script, especially quoted strings and crafted values.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/xiekch/skills/wecom-webhook)
- [Enterprise WeChat webhook endpoint](https://qyapi.weixin.qq.com/cgi-bin/webhook/send)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON payload examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a WeCom webhook key and curl; supports text, Markdown, userid mentions, and mobile-number mentions.]

## Skill Version(s):

1.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
