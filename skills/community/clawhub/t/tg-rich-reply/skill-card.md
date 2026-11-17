## Description:

Deploy interactive Telegram Mini App (TWA) answers from OpenClaw as Vercel-hosted HTML pages opened through Telegram inline buttons.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shlomizaig](https://clawhub.ai/user/shlomizaig)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to turn an agent response into a mobile-responsive HTML answer, deploy it to Vercel, and share it in Telegram as an inline Mini App button.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated HTML can be deployed publicly through Vercel.

Mitigation: Review each HTML file before deployment and only make a deployment public when the content is intended for anyone with the link.

Risk: The workflow uses Vercel and Telegram credentials.

Mitigation: Use narrowly scoped credentials, avoid storing Vercel tokens in TOOLS.md, and never display the Telegram bot token in chat.

Risk: Telegram messages can be sent to the wrong chat or with the wrong content.

Mitigation: Confirm the exact Telegram chat ID, message text, and inline button URL before sending.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/shlomizaig/skills/tg-rich-reply)
- [Vercel signup](https://vercel.com/signup)
- [Telegram WebApp SDK](https://telegram.org/js/telegram-web-app.js)
- [Vercel files API endpoint](https://api.vercel.com/v2/files)
- [Vercel deployments API endpoint](https://api.vercel.com/v13/deployments)

## Skill Output:

**Output Type(s):** [Markdown, Code, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown with HTML, Python, JSON, and bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces single-file HTML page guidance, Vercel deployment commands, and Telegram inline button messaging instructions.]

## Skill Version(s):

1.0.0 (source: release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
