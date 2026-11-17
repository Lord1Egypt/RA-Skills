## Description:

Lets an agent proactively send WeChat text messages, images, videos, and files through the wxclawbot CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lroolle](https://clawhub.ai/user/lroolle)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to have an OpenClaw agent send proactive WeChat reminders, alerts, reports, and attachments to configured users.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can send WeChat messages and attachments to external recipients.

Mitigation: Use dry-run or explicit confirmation before sending sensitive files, reports, or user data.

Risk: WXCLAW_TOKEN and local OpenClaw account files grant messaging access.

Mitigation: Keep tokens and account files secret, restrict filesystem access, and rotate credentials if exposed.

Risk: Custom base URLs and URL attachments can route data through untrusted endpoints or fetch untrusted content.

Mitigation: Use only trusted WXCLAW_BASE_URL/account baseUrl values and only send URL attachments from trusted sources.

Risk: A successful CLI run does not always prove the message was delivered or actively pushed.

Mitigation: Request JSON output, inspect the ok field, and verify account context tokens when proactive push behavior matters.

## Reference(s):

- [Programmatic API](references/programmatic-api.md)
- [ClawHub skill page](https://clawhub.ai/lroolle/skills/wxclawbot-send)
- [wxclawbot-cli repository](https://github.com/lroolle/wxclawbot-cli)
- [npm package](https://www.npmjs.com/package/@claw-lab/wxclawbot-cli)
- [WeChat Integration Tutorial](https://mp.weixin.qq.com/s/nYDQ1obQEHe1WavGpNzasQ)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Programmatic use should request JSON output and inspect the ok field.]

## Skill Version(s):

0.5.2 (source: SKILL.md frontmatter, package.json, server release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
